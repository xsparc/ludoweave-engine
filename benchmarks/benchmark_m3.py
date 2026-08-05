"""Record M3 extraction, Null submission, and wgpu submission evidence."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sysconfig
from collections.abc import Callable, Mapping, Sequence
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from time import perf_counter_ns
from typing import Protocol
from uuid import UUID

from ludoweave import __version__
from ludoweave.render import (
    Camera2D,
    CommandList,
    NullRenderDevice,
    PipelineDescriptor,
    SpriteBatchCommand,
    SpriteExtractionSource,
    SpriteInstance,
    TextureDescriptor,
    TextureFormat,
    TextureHandle,
    TextureUsage,
)
from ludoweave.render._sprite import pack_sprite_instances
from ludoweave.render.backends.wgpu import WgpuRenderDevice

_SCHEMA = "ludoweave.benchmark.m3/1"
_SEED = 1
_WARMUPS = 3
_COUNTS = (1_000, 10_000)
_SCOPE = UUID("c78074f7-2ea9-4ab9-8810-719c2fa53af2")


class _Operation(Protocol):
    def __call__(self) -> tuple[int, int]: ...


class _Closer(Protocol):
    def __call__(self) -> None: ...


def _percentile(values: Sequence[int], percentile: int) -> int:
    ordered = sorted(values)
    index = max(0, ((len(ordered) * percentile + 99) // 100) - 1)
    return ordered[index]


def _measure(
    name: str,
    count: int,
    operation: _Operation,
    close: _Closer,
    *,
    samples: int,
    target_ns: int | None,
) -> dict[str, object]:
    try:
        for _ in range(_WARMUPS):
            draw_calls, visible = operation()
            if draw_calls != 1 or visible != count:
                raise RuntimeError("render benchmark invariant failed during warmup")
        durations: list[int] = []
        for _ in range(samples):
            started = perf_counter_ns()
            draw_calls, visible = operation()
            durations.append(perf_counter_ns() - started)
            if draw_calls != 1 or visible != count:
                raise RuntimeError("render benchmark invariant failed")
    finally:
        close()
    p50 = _percentile(durations, 50)
    p95 = _percentile(durations, 95)
    p99 = _percentile(durations, 99)
    target = None
    if target_ns is not None:
        target = {
            "metric": "p95_ns",
            "comparator": "<",
            "limit_ns": target_ns,
            "observed": p95 < target_ns,
        }
    return {
        "name": name,
        "workload_version": 1,
        "warmups": _WARMUPS,
        "samples": samples,
        "parameters": {"visible_sprites": count},
        "durations_ns": durations,
        "p50_ns": p50,
        "p95_ns": p95,
        "p99_ns": p99,
        "draw_calls": 1,
        "target": target,
    }


def _sources(count: int) -> tuple[SpriteExtractionSource, ...]:
    texture = TextureHandle(_SCOPE, 0, 0)
    return tuple(
        SpriteExtractionSource(
            texture,
            index,
            0,
            float(index % 100),
            float(index // 100),
            float(index % 100) + 0.5,
            float(index // 100) + 0.5,
            0.0,
            0.0,
            1.0,
            1.0,
        )
        for index in range(count)
    )


def _extraction_operation(count: int) -> _Operation:
    from ludoweave.render import RenderExtractor

    sources = _sources(count)
    extractor = RenderExtractor()
    camera = Camera2D(viewport_width=100.0, viewport_height=100.0)

    def operation() -> tuple[int, int]:
        frame = extractor.extract_sprites(
            sources,
            completed_ticks=1,
            interpolation_alpha=0.5,
            camera=camera,
        )
        packed = pack_sprite_instances(frame.sprite_groups[0].instances)
        if len(packed) != count * 64:
            raise RuntimeError("packed instance size changed")
        return frame.normal_sprite_draw_count, frame.visible_sprite_count

    return operation


def extraction_profile_operation(count: int = 10_000) -> _Operation:
    """Return the exact extraction-and-pack operation used by the M3 benchmark."""

    if count <= 0:
        raise ValueError("visible sprite count must be positive")
    return _extraction_operation(count)


def _instances(count: int) -> tuple[SpriteInstance, ...]:
    return tuple(
        SpriteInstance(
            float(index % 100),
            float(index // 100),
            1.0,
            1.0,
            0.0,
            0.0,
            0.0,
            1.0,
            1.0,
            entity_index=index,
        )
        for index in range(count)
    )


def _submission_operation(
    count: int, *, graphics: bool
) -> tuple[_Operation, Callable[[], None], Mapping[str, object]]:
    device = WgpuRenderDevice() if graphics else NullRenderDevice()
    sampled = device.create_texture(
        TextureDescriptor(
            1,
            1,
            TextureFormat.RGBA8_UNORM,
            TextureUsage.SAMPLED | TextureUsage.COPY_DESTINATION,
            label="benchmark-sampled",
        )
    )
    target = device.create_texture(
        TextureDescriptor(
            64,
            64,
            TextureFormat.RGBA8_UNORM,
            TextureUsage.RENDER_ATTACHMENT | TextureUsage.COPY_SOURCE,
            label="benchmark-target",
        )
    )
    pipeline = device.create_pipeline(PipelineDescriptor(TextureFormat.RGBA8_UNORM))
    commands = CommandList(
        "benchmark-frame",
        (SpriteBatchCommand(pipeline, sampled, _instances(count)),),
        target,
        Camera2D(viewport_width=100.0, viewport_height=100.0).orthographic_matrix(),
    )

    def operation() -> tuple[int, int]:
        submission = device.submit((commands,))
        return submission.draw_calls, submission.sprite_instances

    def close() -> None:
        device.poll()
        device.close()

    capabilities = device.capabilities
    return (
        operation,
        close,
        {
            "backend": capabilities.backend,
            "max_texture_dimension_2d": capabilities.max_texture_dimension_2d,
            "timestamp_queries": capabilities.timestamp_queries,
        },
    )


def submission_profile_fixture(
    count: int = 10_000, *, graphics: bool
) -> tuple[_Operation, Callable[[], None], Mapping[str, object]]:
    """Return the exact M3 submission operation, cleanup, and capabilities."""

    if count <= 0:
        raise ValueError("visible sprite count must be positive")
    return _submission_operation(count, graphics=graphics)


def _package_version(name: str) -> str:
    try:
        return version(name)
    except PackageNotFoundError:
        return "not-installed"


def _environment(capabilities: Mapping[str, object]) -> dict[str, object]:
    return {
        "os": platform.system(),
        "os_release": platform.release(),
        "architecture": platform.machine() or "unknown",
        "processor": platform.processor() or "unknown",
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "python_build_mode": "debug" if sysconfig.get_config_var("Py_DEBUG") else "release",
        "ludoweave_version": __version__,
        "dependency_versions": {
            "glfw": _package_version("glfw"),
            "rendercanvas": _package_version("rendercanvas"),
            "wgpu": _package_version("wgpu"),
        },
        "render_capabilities": dict(capabilities),
    }


def _git() -> dict[str, object]:
    commit = subprocess.run(
        ("git", "rev-parse", "HEAD"), check=True, capture_output=True, text=True
    ).stdout.strip()
    dirty = bool(
        subprocess.run(
            ("git", "status", "--porcelain"), check=True, capture_output=True, text=True
        ).stdout
    )
    return {"commit": commit, "dirty": dirty}


def run(samples: int) -> dict[str, object]:
    if samples <= 0:
        raise ValueError("samples must be positive")
    workloads: list[dict[str, object]] = []
    for count in _COUNTS:
        workloads.append(
            _measure(
                f"extract_pack_{count}",
                count,
                _extraction_operation(count),
                lambda: None,
                samples=samples,
                target_ns=3_000_000 if count == 10_000 else None,
            )
        )
    null_capabilities: Mapping[str, object] = {}
    for count in _COUNTS:
        operation, close, null_capabilities = _submission_operation(count, graphics=False)
        workloads.append(
            _measure(
                f"null_submit_{count}",
                count,
                operation,
                close,
                samples=samples,
                target_ns=None,
            )
        )
    graphics_capabilities: Mapping[str, object] = {}
    for count in _COUNTS:
        operation, close, graphics_capabilities = _submission_operation(count, graphics=True)
        workloads.append(
            _measure(
                f"wgpu_submit_{count}",
                count,
                operation,
                close,
                samples=samples,
                target_ns=3_000_000 if count == 10_000 else None,
            )
        )
    return {
        "schema": _SCHEMA,
        "seed": _SEED,
        "samples": samples,
        "warmups": _WARMUPS,
        "timer": "time.perf_counter_ns",
        "environment": _environment(graphics_capabilities),
        "null_capabilities": dict(null_capabilities),
        "git": _git(),
        "workloads": workloads,
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=30)
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args(argv)
    document = run(arguments.samples)
    encoded = json.dumps(document, sort_keys=True, separators=(",", ":"))
    if arguments.output is None:
        print(encoded)
    else:
        arguments.output.write_text(f"{encoded}\n", encoding="utf-8")
        print(
            json.dumps(
                {
                    "schema": _SCHEMA,
                    "output": arguments.output.name,
                    "workloads": len(_COUNTS) * 3,
                },
                sort_keys=True,
                separators=(",", ":"),
            )
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
