"""Record informational M2 command, snapshot, and replay performance evidence."""

from __future__ import annotations

import argparse
import json
import platform
import subprocess
import sysconfig
import tracemalloc
from collections.abc import Callable, Mapping, Sequence
from hashlib import sha256
from pathlib import Path
from time import perf_counter_ns
from typing import Protocol, cast

from ludoweave import __version__
from ludoweave.ecs import ComponentRegistry, ResourceRegistry, ResourceStore, World
from ludoweave.world import (
    CommandActor,
    CommandEnvelope,
    CommandTransaction,
    ReplayRecorder,
    ReplayRunner,
    SnapshotCodec,
    TransactionService,
    WorldSession,
)

_SCHEMA = "ludoweave.benchmark.m2/1"
_WORKLOAD_VERSION = 1
_WARMUPS = 3
_COMMAND_COUNT = 100
_SNAPSHOT_ENTITY_COUNT = 1_000
_REPLAY_BATCH_COUNT = 100
_PROJECT_SCHEMA = f"sha256:{sha256(b'm2-benchmark-project').hexdigest()}"
_LOCK_HASH = f"sha256:{sha256(b'm2-benchmark-lock').hexdigest()}"
_PLATFORM_PROFILE = "benchmark-cpython-standard"


class _Operation(Protocol):
    def __call__(self) -> object: ...


class _Factory(Protocol):
    def __call__(self) -> tuple[_Operation, Callable[[], None]]: ...


def _nothing() -> None:
    return None


def _composition(*, entity_count: int = 0) -> tuple[WorldSession, SnapshotCodec]:
    components = ComponentRegistry()
    resources = ResourceRegistry()
    world = World(components)
    for _ in range(entity_count):
        world.spawn()
    session = WorldSession("benchmark-world", world, ResourceStore(resources))
    return session, SnapshotCodec(components, resources)


def _transaction(transaction_id: str, command_count: int) -> CommandTransaction:
    actor = CommandActor("benchmark", "m2")
    return CommandTransaction(
        tuple(
            CommandEnvelope(
                command_id=f"{transaction_id}.command-{index}",
                transaction_id=transaction_id,
                actor=actor,
                operation="entity.spawn",
                arguments={"components": []},
            )
            for index in range(command_count)
        ),
        "benchmark-world",
    )


def _canonical_operation() -> int:
    transaction = _transaction("canonical", _COMMAND_COUNT)
    encoded = transaction.canonical_bytes()
    decoded = CommandTransaction.from_json(encoded)
    if decoded.canonical_bytes() != encoded:
        raise RuntimeError("canonical transaction round trip changed bytes")
    return len(encoded)


def _transaction_factory() -> tuple[_Operation, Callable[[], None]]:
    session, _ = _composition()
    service = TransactionService(session)
    transaction = _transaction("apply", _COMMAND_COUNT)

    def operation() -> str:
        receipt = service.apply(transaction)
        if receipt.status.value != "committed":
            raise RuntimeError("transaction benchmark did not commit")
        return receipt.post_hash

    return operation, _nothing


def _snapshot_fixture() -> tuple[SnapshotCodec, bytes]:
    session, codec = _composition(entity_count=_SNAPSHOT_ENTITY_COUNT)
    return codec, codec.encode(session)


def _snapshot_operation(codec: SnapshotCodec, snapshot: bytes) -> Callable[[], int]:
    def operation() -> int:
        restored = codec.decode(snapshot)
        encoded = codec.encode(restored)
        if encoded != snapshot:
            raise RuntimeError("snapshot benchmark round trip changed bytes")
        return len(encoded)

    return operation


def _replay_fixture() -> tuple[ReplayRunner, bytes]:
    session, codec = _composition()
    recorder = ReplayRecorder(
        session,
        codec,
        timeline_id="benchmark-replay",
        project_schema=_PROJECT_SCHEMA,
        dependency_lock_hash=_LOCK_HASH,
        platform_profile=_PLATFORM_PROFILE,
        checkpoint_interval=10,
    )
    for index in range(_REPLAY_BATCH_COUNT):
        receipt = recorder.record(_transaction(f"replay-{index}", 1))
        if receipt.status.value != "committed":
            raise RuntimeError("replay benchmark fixture did not commit")
    runner = ReplayRunner(
        codec,
        project_schema=_PROJECT_SCHEMA,
        dependency_lock_hash=_LOCK_HASH,
        platform_profile=_PLATFORM_PROFILE,
    )
    return runner, recorder.timeline().canonical_bytes()


def _replay_operation(runner: ReplayRunner, replay: bytes) -> Callable[[], str]:
    def operation() -> str:
        result = runner.replay(replay)
        if result.batches_applied != _REPLAY_BATCH_COUNT:
            raise RuntimeError("replay benchmark applied the wrong batch count")
        return result.session.state_hash

    return operation


def _measure(
    factory: _Factory,
    *,
    warmups: int,
    samples: int,
) -> tuple[tuple[int, ...], tuple[int, ...]]:
    durations: list[int] = []
    peaks: list[int] = []
    for index in range(warmups + samples):
        operation, cleanup = factory()
        tracemalloc.start()
        try:
            started = perf_counter_ns()
            operation()
            elapsed = perf_counter_ns() - started
            _current, peak = tracemalloc.get_traced_memory()
        finally:
            tracemalloc.stop()
            cleanup()
        if index >= warmups:
            durations.append(elapsed)
            peaks.append(peak)
    return tuple(durations), tuple(peaks)


def _reusable(operation: _Operation) -> _Factory:
    def factory() -> tuple[_Operation, Callable[[], None]]:
        return operation, _nothing

    return factory


def _percentile(values: Sequence[int], percentile: int) -> int:
    ordered = sorted(values)
    index = max(0, ((len(ordered) * percentile + 99) // 100) - 1)
    return ordered[index]


def _workload(
    name: str,
    factory: _Factory,
    *,
    warmups: int,
    samples: int,
    parameters: Mapping[str, int],
) -> dict[str, object]:
    durations, peaks = _measure(factory, warmups=warmups, samples=samples)
    return {
        "name": name,
        "workload_version": _WORKLOAD_VERSION,
        "warmups": warmups,
        "samples": samples,
        "parameters": dict(parameters),
        "durations_ns": list(durations),
        "peak_bytes": list(peaks),
        "p50_ns": _percentile(durations, 50),
        "p95_ns": _percentile(durations, 95),
        "p99_ns": _percentile(durations, 99),
        "peak_p95_bytes": _percentile(peaks, 95),
        "target": None,
    }


def _git_metadata() -> dict[str, object]:
    commit = "0" * 40
    dirty = True
    try:
        commit_result = subprocess.run(
            ("git", "rev-parse", "HEAD"),
            check=True,
            capture_output=True,
            text=True,
        )
        status_result = subprocess.run(
            ("git", "status", "--porcelain"),
            check=True,
            capture_output=True,
            text=True,
        )
        candidate = commit_result.stdout.strip()
        if len(candidate) == 40 and all(character in "0123456789abcdef" for character in candidate):
            commit = candidate
        dirty = bool(status_result.stdout)
    except (OSError, subprocess.CalledProcessError):
        pass
    return {"commit": commit, "dirty": dirty}


def _environment() -> dict[str, object]:
    return {
        "os": platform.system() or "unknown",
        "os_release": platform.release() or "unknown",
        "architecture": platform.machine() or "unknown",
        "python_implementation": platform.python_implementation(),
        "python_version": platform.python_version(),
        "python_threading_build": (
            "free-threaded" if sysconfig.get_config_var("Py_GIL_DISABLED") == 1 else "gil"
        ),
        "ludoweave_version": __version__,
    }


def run_benchmarks(*, samples: int, warmups: int, seed: int) -> dict[str, object]:
    snapshot_codec, snapshot = _snapshot_fixture()
    replay_runner, replay = _replay_fixture()
    workloads = [
        _workload(
            "canonical_transaction_100",
            _reusable(_canonical_operation),
            warmups=warmups,
            samples=samples,
            parameters={"command_count": _COMMAND_COUNT},
        ),
        _workload(
            "atomic_transaction_apply_100",
            _transaction_factory,
            warmups=warmups,
            samples=samples,
            parameters={"command_count": _COMMAND_COUNT},
        ),
        _workload(
            "snapshot_roundtrip_1000",
            _reusable(_snapshot_operation(snapshot_codec, snapshot)),
            warmups=warmups,
            samples=samples,
            parameters={
                "entity_count": _SNAPSHOT_ENTITY_COUNT,
                "snapshot_bytes": len(snapshot),
            },
        ),
        _workload(
            "replay_verify_100_batches",
            _reusable(_replay_operation(replay_runner, replay)),
            warmups=warmups,
            samples=samples,
            parameters={
                "batch_count": _REPLAY_BATCH_COUNT,
                "replay_bytes": len(replay),
            },
        ),
    ]
    return {
        "schema": _SCHEMA,
        "seed": seed,
        "samples": samples,
        "warmups": warmups,
        "timer": "time.perf_counter_ns",
        "memory": "tracemalloc.peak_bytes",
        "environment": _environment(),
        "git": _git_metadata(),
        "workloads": workloads,
    }


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be positive")
    return parsed


def _non_negative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must be non-negative")
    return parsed


def main(arguments: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=_positive_int, default=30)
    parser.add_argument("--warmups", type=_non_negative_int, default=_WARMUPS)
    parser.add_argument("--seed", type=_non_negative_int, default=1)
    parser.add_argument("--json-out", type=Path, required=True)
    options = parser.parse_args(arguments)
    result = run_benchmarks(
        samples=cast(int, options.samples),
        warmups=cast(int, options.warmups),
        seed=cast(int, options.seed),
    )
    output = cast(Path, options.json_out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, separators=(",", ":"), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
