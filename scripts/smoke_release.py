"""Verify checksums/SBOM and run bundled alpha samples from an installed wheel."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import tempfile
import zipfile
import zlib
from collections.abc import Iterable, Sequence
from contextlib import ExitStack
from itertools import pairwise
from pathlib import Path, PurePosixPath
from typing import IO, BinaryIO, cast

from agent_tool_recovery_rate_evidence import validate_agent_tool_recovery_rate_evidence
from benchmark_regression_rate_evidence import validate_benchmark_regression_rate_evidence
from command_receipt_stability_evidence import validate_command_receipt_stability_evidence
from constrained_3d_evidence import validate_constrained_3d_evidence
from cross_version_corpus_evidence import validate_cross_version_corpus_evidence
from external_consumer_feedback_evidence import validate_external_consumer_feedback_evidence
from external_contributor_rehearsal_evidence import (
    validate_external_contributor_rehearsal_evidence,
)
from external_contributor_retention_evidence import (
    validate_external_contributor_retention_evidence,
)
from external_sample_game_adoption_evidence import (
    validate_external_sample_game_adoption_evidence,
)
from installation_matrix_evidence import validate_installation_matrix_evidence
from operation_argument_evidence import validate_operation_argument_evidence
from receipt_reader_evidence import validate_receipt_reader_evidence
from receipt_semantic_evidence import validate_receipt_semantic_evidence
from replay_divergence_rate_evidence import validate_replay_divergence_rate_evidence
from response_review_latency_evidence import validate_response_review_latency_evidence
from supported_release_channel_evidence import validate_supported_release_channel_evidence
from third_party_conformance_adoption_evidence import (
    validate_third_party_conformance_adoption_evidence,
)
from visual_editor_evidence import validate_visual_editor_evidence
from wasm_mod_security_evidence import validate_wasm_mod_security_evidence

_MAX_SAMPLE_ARCHIVE_BYTES = 16 * 1024 * 1024
_MAX_SAMPLE_MEMBERS = 256
_MAX_SAMPLE_MEMBER_BYTES = 1024 * 1024
_MAX_SAMPLE_TOTAL_BYTES = 8 * 1024 * 1024
_SAMPLE_COPY_BYTES = 64 * 1024
_SAMPLE_COMPRESSION_METHODS = frozenset((zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED))
_SAMPLE_ENCRYPTION_FLAGS = 0x0001 | 0x0040 | 0x2000
_SAMPLE_COMPRESSED_PATCH_FLAG = 0x0020
_SAMPLE_ENHANCED_DEFLATE_FLAG = 0x0010
_SAMPLE_DATA_DESCRIPTOR_FLAG = 0x0008
_SAMPLE_UNICODE_PATH_EXTRA_FIELD = 0x7075
_SAMPLE_ZIP64_EXTRA_FIELD = 0x0001
_SAMPLE_EOCD_BYTES = 22
_SAMPLE_EOCD_SIGNATURE = b"PK\x05\x06"
_SAMPLE_LOCAL_HEADER_SIGNATURE = b"PK\x03\x04"
_SAMPLE_FIXED_LOCAL_HEADER_BYTES = 30
_SAMPLE_LOCAL_HEADER_FLAGS_OFFSET = 6
_SAMPLE_LOCAL_HEADER_LENGTH_FIELDS_OFFSET = 26
_SAMPLE_LOCAL_HEADER_LENGTH_FIELDS_BYTES = 4
_SAMPLE_UTF8_FILENAME_FLAG = 1 << 11
_MAX_SAMPLE_PATH_CHARS = 255
_SAMPLE_MEMBER_PATTERN = re.compile(r"[0-9A-Za-z][0-9A-Za-z._+-]{0,254}")
_WINDOWS_DEVICE_STEMS = frozenset(
    ("aux", "con", "nul", "prn"),
) | frozenset(f"{prefix}{number}" for prefix in ("com", "lpt") for number in range(1, 10))
_EXPECTED_SAMPLE_MEMBERS: frozenset[str] = frozenset(
    (
        "README.md",
        "agent_tool_conformance.py",
        "agent_tool_recovery_rate_readiness.py",
        "agent_world_builder.py",
        "alpha_acceptance.py",
        "assets/agent_tool_recovery_rate.json",
        "assets/benchmark_regression_rate.json",
        "assets/clockwork_arena.scene.json",
        "assets/cross_version_receipt_corpus.json",
        "assets/external_contributor_rehearsal.json",
        "assets/external_contributor_retention.json",
        "assets/external_consumer_feedback.json",
        "assets/external_sample_game_adoption.json",
        "assets/installation_matrix.json",
        "assets/receipt_v1/committed.json",
        "assets/receipt_v1/dry_run.json",
        "assets/receipt_v1/manifest.json",
        "assets/receipt_v1/rejected.json",
        "assets/replay_divergence_rate.json",
        "assets/response_review_latency.json",
        "assets/supported_release_channel.json",
        "assets/third_party_conformance_adoption.json",
        "benchmark_regression_rate_readiness.py",
        "clockwork_arena.assets.json",
        "clockwork_arena.py",
        "command_receipt_stability_decision.py",
        "constrained_3d_decision.py",
        "cross_version_corpus_readiness.py",
        "example.plugin.json",
        "external_contributor_rehearsal_readiness.py",
        "external_contributor_retention_readiness.py",
        "external_consumer_feedback_readiness.py",
        "external_sample_game_adoption_readiness.py",
        "fixed_step_world.py",
        "hello_headless.py",
        "hello_sprite.py",
        "installation_matrix_readiness.py",
        "operation_argument_compatibility.py",
        "receipt_reader.py",
        "receipt_semantic_compatibility.py",
        "render_device_conformance.py",
        "replay_divergence_rate_readiness.py",
        "response_review_latency_readiness.py",
        "rich_2d_showcase.py",
        "rollback_readiness.py",
        "supported_release_channel_readiness.py",
        "third_party_conformance_adoption_readiness.py",
        "visual_editor_decision.py",
        "wasm_mod_security_decision.py",
        "world_store_conformance.py",
    )
)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("release", type=Path, help="staged release directory")
    args = parser.parse_args(argv)
    release = _path_argument(args, "release").resolve()
    checksums = _read_checksums(release / "SHA256SUMS")
    actual_files = {path.name for path in release.iterdir() if path.is_file()}
    required_files = {
        "LICENSE",
        "NOTICE",
        "RELEASE_MANIFEST.json",
        "RELEASE_NOTES.md",
        "SHA256SUMS",
        "THIRD_PARTY_NOTICES.md",
    }
    if not required_files <= actual_files:
        raise RuntimeError("staged release is missing required notices or metadata")
    if set(checksums) != actual_files - {"SHA256SUMS"}:
        raise RuntimeError("SHA256SUMS does not cover the exact staged release")
    for name, expected in checksums.items():
        if _sha256(release / name) != expected:
            raise RuntimeError(f"release checksum mismatch for {name}")

    manifest = _json_object(release / "RELEASE_MANIFEST.json")
    version = _text(manifest.get("version"), "manifest version")
    if manifest.get("protocol") != "ludoweave.release-manifest/1":
        raise RuntimeError("release manifest protocol is incompatible")
    wheel = _one(release.glob("ludoweave-*.whl"), "wheel")
    _one(release.glob("ludoweave-*.tar.gz"), "source distribution")
    bundle = _one(release.glob("ludoweave-samples-*.zip"), "sample bundle")
    sbom = _one(release.glob("ludoweave-*.spdx.json"), "SPDX SBOM")
    _verify_manifest(manifest, release=release, actual_files=actual_files)
    _verify_sbom(sbom, wheel=wheel, version=version)

    uv = shutil.which("uv")
    if uv is None:
        raise RuntimeError("uv is required for the isolated release smoke")
    project_root = Path(__file__).resolve().parents[1]
    local_temp = project_root / ".tmp"
    local_temp.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="ludoweave-release-smoke-", dir=local_temp) as name:
        temp_root = Path(name)
        environment = temp_root / "venv"
        _run([uv, "venv", "--python", "3.12", str(environment)], cwd=temp_root)
        python = _python_in(environment)
        _run(
            [uv, "pip", "install", "--python", str(python), "--no-deps", str(wheel)],
            cwd=temp_root,
        )
        samples = temp_root / "samples"
        samples.mkdir()
        sample_root = _extract_bundle(
            bundle,
            samples,
            version=version,
            expected_sha256=checksums[bundle.name],
        )
        _run([str(python), "-I", "hello_headless.py", "--ticks", "5"], cwd=sample_root)
        _run([str(python), "-I", "fixed_step_world.py", "--ticks", "6"], cwd=sample_root)
        conformance_result = _run(
            [str(python), "-I", "render_device_conformance.py"],
            cwd=sample_root,
        )
        conformance = cast(dict[str, object], json.loads(conformance_result.stdout))
        conformance_checks = cast(list[dict[str, object]], conformance.get("checks"))
        if (
            conformance.get("protocol") != "ludoweave.render-device-conformance/1"
            or conformance.get("profile") != "render-device-baseline/1"
            or conformance.get("adapter_id") != "org.ludoweave.null"
            or conformance.get("adapter_name") != "null-device"
            or conformance.get("status") != "pass"
            or len(conformance_checks) != 9
            or any(check.get("status") != "pass" for check in conformance_checks)
        ):
            raise RuntimeError(
                f"bundled render-device conformance report was invalid: {conformance!r}"
            )
        agent_conformance_result = _run(
            [str(python), "-I", "agent_tool_conformance.py"],
            cwd=sample_root,
        )
        agent_conformance = cast(dict[str, object], json.loads(agent_conformance_result.stdout))
        agent_checks = cast(list[dict[str, object]], agent_conformance.get("checks"))
        if (
            agent_conformance.get("protocol") != "ludoweave.agent-tool-conformance/1"
            or agent_conformance.get("profile") != "agent-tool-baseline/1"
            or agent_conformance.get("adapter_id") != "org.ludoweave.agent-service"
            or agent_conformance.get("status") != "pass"
            or len(agent_checks) != 12
            or any(check.get("status") != "pass" for check in agent_checks)
        ):
            raise RuntimeError(
                f"bundled agent-tool conformance report was invalid: {agent_conformance!r}"
            )
        for backend in ("world", "reference"):
            world_conformance_result = _run(
                [
                    str(python),
                    "-I",
                    "world_store_conformance.py",
                    "--backend",
                    backend,
                ],
                cwd=sample_root,
            )
            world_conformance = cast(dict[str, object], json.loads(world_conformance_result.stdout))
            world_checks = cast(list[dict[str, object]], world_conformance.get("checks"))
            if (
                world_conformance.get("protocol") != "ludoweave.world-store-conformance/1"
                or world_conformance.get("profile") != "world-store-baseline/1"
                or world_conformance.get("adapter_id") != f"ludoweave.{backend}"
                or world_conformance.get("status") != "pass"
                or len(world_checks) != 10
                or any(check.get("status") != "pass" for check in world_checks)
            ):
                raise RuntimeError(
                    f"bundled world-store conformance report was invalid: {world_conformance!r}"
                )
        _run([str(python), "-I", "rich_2d_showcase.py", "--ticks", "6"], cwd=sample_root)
        rollback_result = _run(
            [
                str(python),
                "-I",
                "rollback_readiness.py",
                "--ticks",
                "24",
                "--branch-tick",
                "12",
            ],
            cwd=sample_root,
        )
        rollback = cast(dict[str, object], json.loads(rollback_result.stdout))
        if (
            rollback.get("schema") != "ludoweave.evaluation.rollback-readiness/1"
            or rollback.get("status") != "deferred"
            or rollback.get("transport_implemented") is not False
            or cast(dict[str, object], rollback.get("proof", {})).get("input_rehydration_required")
            is not True
        ):
            raise RuntimeError(f"rollback readiness summary was invalid: {rollback!r}")
        constrained_3d_result = _run(
            [str(python), "-I", "constrained_3d_decision.py"],
            cwd=sample_root,
        )
        constrained_3d = cast(dict[str, object], json.loads(constrained_3d_result.stdout))
        validate_constrained_3d_evidence(constrained_3d, version=version)
        visual_editor_result = _run(
            [str(python), "-I", "visual_editor_decision.py"],
            cwd=sample_root,
        )
        visual_editor = cast(dict[str, object], json.loads(visual_editor_result.stdout))
        validate_visual_editor_evidence(visual_editor, version=version)
        wasm_security_result = _run(
            [str(python), "-I", "wasm_mod_security_decision.py"],
            cwd=sample_root,
        )
        wasm_security = cast(dict[str, object], json.loads(wasm_security_result.stdout))
        validate_wasm_mod_security_evidence(wasm_security, version=version)
        command_receipt_result = _run(
            [str(python), "-I", "command_receipt_stability_decision.py"],
            cwd=sample_root,
        )
        command_receipt = cast(dict[str, object], json.loads(command_receipt_result.stdout))
        validate_command_receipt_stability_evidence(command_receipt, version=version)
        operation_argument_result = _run(
            [str(python), "-I", "operation_argument_compatibility.py"],
            cwd=sample_root,
        )
        operation_argument = cast(dict[str, object], json.loads(operation_argument_result.stdout))
        validate_operation_argument_evidence(operation_argument, version=version)
        receipt_reader_result = _run(
            [str(python), "-I", "receipt_reader.py"],
            cwd=sample_root,
        )
        receipt_reader = cast(dict[str, object], json.loads(receipt_reader_result.stdout))
        validate_receipt_reader_evidence(receipt_reader, version=version)
        receipt_semantic_result = _run(
            [str(python), "-I", "receipt_semantic_compatibility.py"],
            cwd=sample_root,
        )
        receipt_semantic = cast(dict[str, object], json.loads(receipt_semantic_result.stdout))
        validate_receipt_semantic_evidence(receipt_semantic, version=version)
        cross_version_result = _run(
            [str(python), "-I", "cross_version_corpus_readiness.py"],
            cwd=sample_root,
        )
        cross_version = cast(dict[str, object], json.loads(cross_version_result.stdout))
        validate_cross_version_corpus_evidence(cross_version, version=version)
        external_feedback_result = _run(
            [str(python), "-I", "external_consumer_feedback_readiness.py"],
            cwd=sample_root,
        )
        external_feedback = cast(dict[str, object], json.loads(external_feedback_result.stdout))
        validate_external_consumer_feedback_evidence(external_feedback, version=version)
        external_contributor_result = _run(
            [str(python), "-I", "external_contributor_rehearsal_readiness.py"],
            cwd=sample_root,
        )
        external_contributor = cast(
            dict[str, object], json.loads(external_contributor_result.stdout)
        )
        validate_external_contributor_rehearsal_evidence(external_contributor, version=version)
        contributor_retention_result = _run(
            [str(python), "-I", "external_contributor_retention_readiness.py"],
            cwd=sample_root,
        )
        contributor_retention = cast(
            dict[str, object], json.loads(contributor_retention_result.stdout)
        )
        validate_external_contributor_retention_evidence(contributor_retention, version=version)
        installation_matrix_result = _run(
            [str(python), "-I", "installation_matrix_readiness.py"],
            cwd=sample_root,
        )
        installation_matrix = cast(dict[str, object], json.loads(installation_matrix_result.stdout))
        validate_installation_matrix_evidence(installation_matrix, version=version)
        response_review_latency_result = _run(
            [str(python), "-I", "response_review_latency_readiness.py"],
            cwd=sample_root,
        )
        response_review_latency = cast(
            dict[str, object], json.loads(response_review_latency_result.stdout)
        )
        validate_response_review_latency_evidence(response_review_latency, version=version)
        replay_divergence_rate_result = _run(
            [str(python), "-I", "replay_divergence_rate_readiness.py"],
            cwd=sample_root,
        )
        replay_divergence_rate = cast(
            dict[str, object], json.loads(replay_divergence_rate_result.stdout)
        )
        validate_replay_divergence_rate_evidence(replay_divergence_rate, version=version)
        benchmark_regression_rate_result = _run(
            [str(python), "-I", "benchmark_regression_rate_readiness.py"],
            cwd=sample_root,
        )
        benchmark_regression_rate = cast(
            dict[str, object], json.loads(benchmark_regression_rate_result.stdout)
        )
        validate_benchmark_regression_rate_evidence(benchmark_regression_rate, version=version)
        agent_tool_recovery_rate_result = _run(
            [str(python), "-I", "agent_tool_recovery_rate_readiness.py"],
            cwd=sample_root,
        )
        agent_tool_recovery_rate = cast(
            dict[str, object], json.loads(agent_tool_recovery_rate_result.stdout)
        )
        validate_agent_tool_recovery_rate_evidence(agent_tool_recovery_rate, version=version)
        third_party_conformance_result = _run(
            [str(python), "-I", "third_party_conformance_adoption_readiness.py"],
            cwd=sample_root,
        )
        third_party_conformance = cast(
            dict[str, object], json.loads(third_party_conformance_result.stdout)
        )
        validate_third_party_conformance_adoption_evidence(third_party_conformance, version=version)
        external_sample_game_result = _run(
            [str(python), "-I", "external_sample_game_adoption_readiness.py"],
            cwd=sample_root,
        )
        external_sample_game = cast(
            dict[str, object], json.loads(external_sample_game_result.stdout)
        )
        validate_external_sample_game_adoption_evidence(external_sample_game, version=version)
        release_channel_result = _run(
            [str(python), "-I", "supported_release_channel_readiness.py"],
            cwd=sample_root,
        )
        release_channel = cast(dict[str, object], json.loads(release_channel_result.stdout))
        validate_supported_release_channel_evidence(release_channel, version=version)
        plugin_result = _run(
            [str(python), "-I", "-m", "ludoweave", "plugin", "check", "example.plugin.json"],
            cwd=sample_root,
        )
        plugin_report = cast(dict[str, object], json.loads(plugin_result.stdout))
        if (
            plugin_report.get("protocol") != "ludoweave.plugin-check/1"
            or plugin_report.get("compatible") is not True
            or plugin_report.get("plugin_count") != 1
        ):
            raise RuntimeError("bundled plugin manifest compatibility smoke failed")
        _run(
            [
                str(python),
                "-I",
                "clockwork_arena.py",
                "--ticks",
                "30",
                "--renderer",
                "null",
                "--render-every",
                "10",
            ],
            cwd=sample_root,
        )
        alpha_result = _run([str(python), "-I", "alpha_acceptance.py"], cwd=sample_root)
        alpha = cast(dict[str, object], json.loads(alpha_result.stdout))
        if (
            alpha.get("protocol") != "ludoweave.sample.alpha_acceptance/1"
            or alpha.get("status") != "ok"
            or alpha.get("ludoweave_version") != version
            or alpha.get("agent_tests_passed") is not True
        ):
            raise RuntimeError(f"alpha acceptance summary was invalid: {alpha!r}")
    print(f"release smoke passed: ludoweave {version}")
    return 0


def _extract_bundle(
    bundle: Path,
    output: Path,
    *,
    version: str,
    expected_sha256: str | None = None,
) -> Path:
    """Extract one admitted sample bundle behind a content-silent ZIP boundary."""

    try:
        return _extract_checksum_admitted_bundle(
            bundle,
            output,
            version=version,
            expected_sha256=expected_sha256,
        )
    except (zipfile.BadZipFile, zipfile.LargeZipFile, UnicodeDecodeError, zlib.error):
        raise RuntimeError("sample bundle ZIP data is invalid") from None


def _extract_checksum_admitted_bundle(
    bundle: Path,
    output: Path,
    *,
    version: str,
    expected_sha256: str | None = None,
) -> Path:
    expected_root = f"ludoweave-samples-{version}"
    root = output / expected_root
    if not output.is_dir() or output.is_symlink() or output.is_junction():
        raise RuntimeError("sample bundle output directory is unavailable")
    if os.path.lexists(root):
        raise RuntimeError("sample bundle output already exists")
    bundle_metadata = bundle.stat()
    _validate_sample_archive_source(
        mode=bundle_metadata.st_mode,
        size=bundle_metadata.st_size,
    )
    with ExitStack() as resources:
        bundle_stream = resources.enter_context(bundle.open("rb"))
        bundle_metadata = os.fstat(bundle_stream.fileno())
        _validate_sample_archive_source(
            mode=bundle_metadata.st_mode,
            size=bundle_metadata.st_size,
        )
        snapshot_stream = resources.enter_context(
            tempfile.SpooledTemporaryFile(
                max_size=_MAX_SAMPLE_ARCHIVE_BYTES,
                mode="w+b",
            )
        )
        _snapshot_sample_archive(
            bundle_stream,
            snapshot_stream,
            expected_sha256=expected_sha256,
        )
        archive = resources.enter_context(zipfile.ZipFile(snapshot_stream))
        infos = tuple(archive.infolist())
        if len(infos) > _MAX_SAMPLE_MEMBERS:
            raise RuntimeError("sample bundle has too many members")
        for info in infos:
            _validate_sample_member_flags(flag_bits=info.flag_bits)
            _validate_sample_compression_flags(
                flag_bits=info.flag_bits,
                compress_type=info.compress_type,
            )

        for info in infos:
            _validate_sample_descriptor_flags(flag_bits=info.flag_bits)

        for info in infos:
            _validate_sample_extra_fields(extra=info.extra)

        for info in infos:
            _validate_sample_zip64_extra_fields(extra=info.extra)

        _validate_sample_archive_comment(comment=archive.comment)

        for info in infos:
            _validate_sample_member_comment(comment=info.comment)

        for info in infos:
            _validate_sample_member_volume(volume=info.volume)

        _validate_sample_archive_disk_fields(snapshot=snapshot_stream)
        _validate_sample_archive_entry_counts(
            snapshot=snapshot_stream,
            parsed_entries=len(infos),
        )
        _validate_sample_archive_placement(snapshot=snapshot_stream)
        _validate_sample_first_local_header(infos=infos)
        _validate_sample_local_header_offsets(infos=infos)
        _validate_sample_local_header_order(infos=infos)
        _validate_sample_local_header_bounds(snapshot=snapshot_stream, infos=infos)
        _validate_sample_local_header_signatures(snapshot=snapshot_stream, infos=infos)
        _validate_sample_local_header_prefix_bounds(snapshot=snapshot_stream, infos=infos)
        _validate_sample_local_header_envelope_bounds(snapshot=snapshot_stream, infos=infos)
        _validate_sample_local_header_names(snapshot=snapshot_stream, infos=infos)
        _validate_sample_local_header_flags(snapshot=snapshot_stream, infos=infos)

        for info in infos:
            _validate_sample_member_name(original_name=info.orig_filename)

        total_bytes = 0
        member_parts: list[tuple[str, ...]] = []
        member_keys: set[tuple[str, ...]] = set()
        observed_members: set[str] = set()
        directory_spellings: dict[tuple[str, ...], tuple[str, ...]] = {}
        for info in infos:
            path = PurePosixPath(info.filename)
            if (
                path.is_absolute()
                or not path.parts
                or path.parts[0] != expected_root
                or ".." in path.parts
                or "\\" in info.filename
            ):
                raise RuntimeError("sample bundle contains an unsafe path")
            relative_parts = _portable_sample_member_parts(info, expected_root=expected_root)
            member_key = tuple(part.casefold() for part in relative_parts)
            if member_key in member_keys:
                raise RuntimeError("sample bundle member paths collide")
            for depth in range(1, len(relative_parts)):
                directory_key = member_key[:depth]
                directory_spelling = relative_parts[:depth]
                previous = directory_spellings.setdefault(directory_key, directory_spelling)
                if previous != directory_spelling:
                    raise RuntimeError("sample bundle member paths collide")
            member_keys.add(member_key)
            member_parts.append((expected_root, *relative_parts))
            observed_members.add("/".join(relative_parts))
            mode = info.external_attr >> 16
            if stat.S_ISLNK(mode):
                raise RuntimeError("sample bundle must not contain symbolic links")
            file_type = stat.S_IFMT(mode)
            if file_type not in (0, stat.S_IFREG):
                raise RuntimeError("sample bundle contains a non-regular member")
            if info.compress_type not in _SAMPLE_COMPRESSION_METHODS:
                raise RuntimeError("sample bundle uses an unsupported compression method")
            if info.file_size > _MAX_SAMPLE_MEMBER_BYTES:
                raise RuntimeError("sample bundle member is too large")
            total_bytes += info.file_size
            if total_bytes > _MAX_SAMPLE_TOTAL_BYTES:
                raise RuntimeError("sample bundle expands beyond the total limit")

        if any(
            member_key[:depth] in member_keys
            for member_key in member_keys
            for depth in range(1, len(member_key))
        ):
            raise RuntimeError("sample bundle member paths collide")
        _validate_sample_inventory(observed_members)

        with tempfile.TemporaryDirectory(
            prefix=".ludoweave-samples-",
            dir=output,
        ) as staging_name:
            staged_root = Path(staging_name) / expected_root
            for info, parts in zip(infos, member_parts, strict=True):
                destination = staged_root.joinpath(*parts[1:])
                destination.parent.mkdir(parents=True, exist_ok=True)
                written = 0
                with archive.open(info) as source, destination.open("wb") as target:
                    while block := source.read(_SAMPLE_COPY_BYTES):
                        written += len(block)
                        if written > info.file_size:
                            raise RuntimeError(
                                "sample bundle member size changed during extraction"
                            )
                        target.write(block)
                if written != info.file_size:
                    raise RuntimeError("sample bundle member size changed during extraction")
            required = {
                "README.md",
                "agent_tool_recovery_rate_readiness.py",
                "agent_tool_conformance.py",
                "alpha_acceptance.py",
                "benchmark_regression_rate_readiness.py",
                "clockwork_arena.py",
                "command_receipt_stability_decision.py",
                "constrained_3d_decision.py",
                "cross_version_corpus_readiness.py",
                "external_contributor_rehearsal_readiness.py",
                "external_contributor_retention_readiness.py",
                "external_consumer_feedback_readiness.py",
                "external_sample_game_adoption_readiness.py",
                "installation_matrix_readiness.py",
                "operation_argument_compatibility.py",
                "render_device_conformance.py",
                "receipt_reader.py",
                "receipt_semantic_compatibility.py",
                "replay_divergence_rate_readiness.py",
                "response_review_latency_readiness.py",
                "rollback_readiness.py",
                "supported_release_channel_readiness.py",
                "third_party_conformance_adoption_readiness.py",
                "visual_editor_decision.py",
                "wasm_mod_security_decision.py",
                "world_store_conformance.py",
            }
            if not staged_root.is_dir() or not required <= {
                path.name for path in staged_root.iterdir()
            }:
                raise RuntimeError("sample bundle is incomplete")
            if os.path.lexists(root):
                raise RuntimeError("sample bundle output already exists")
            staged_root.replace(root)
    return root


def _validate_sample_archive_source(*, mode: int, size: int) -> None:
    """Admit one bounded regular sample archive before ZIP parsing."""

    if not stat.S_ISREG(mode):
        raise RuntimeError("sample bundle is not a regular file")
    if size > _MAX_SAMPLE_ARCHIVE_BYTES:
        raise RuntimeError("sample bundle archive is too large")


def _snapshot_sample_archive(
    source: IO[bytes],
    snapshot: IO[bytes],
    *,
    expected_sha256: str | None,
) -> None:
    """Copy one bounded source into the exact checksum-admitted parser input."""

    source.seek(0)
    snapshot.seek(0)
    snapshot.truncate(0)
    digest = hashlib.sha256()
    remaining = _MAX_SAMPLE_ARCHIVE_BYTES + 1
    total_bytes = 0
    while remaining > 0:
        block = source.read(min(1024 * 1024, remaining))
        if not block:
            break
        total_bytes += len(block)
        remaining -= len(block)
        if total_bytes > _MAX_SAMPLE_ARCHIVE_BYTES:
            _clear_sample_snapshot(source, snapshot)
            raise RuntimeError("sample bundle checksum does not match staged release")
        digest.update(block)
        snapshot.write(block)
    source.seek(0)
    snapshot.seek(0)
    if expected_sha256 is not None and digest.hexdigest() != expected_sha256:
        snapshot.truncate(0)
        raise RuntimeError("sample bundle checksum does not match staged release")


def _clear_sample_snapshot(source: IO[bytes], snapshot: IO[bytes]) -> None:
    source.seek(0)
    snapshot.seek(0)
    snapshot.truncate(0)


def _sha256_stream(stream: BinaryIO) -> str:
    """Hash a complete seekable stream and leave it rewound."""

    stream.seek(0)
    digest = hashlib.sha256()
    for block in iter(lambda: stream.read(1024 * 1024), b""):
        digest.update(block)
    stream.seek(0)
    return digest.hexdigest()


def _validate_sample_inventory(observed_members: set[str]) -> None:
    """Require the exact source-defined project sample inventory."""

    if observed_members != set(_EXPECTED_SAMPLE_MEMBERS):
        raise RuntimeError("sample bundle inventory is unexpected")


def _validate_sample_member_flags(*, flag_bits: int) -> None:
    """Reject unsupported member processing before reads or staging."""

    if flag_bits & _SAMPLE_ENCRYPTION_FLAGS:
        raise RuntimeError("sample bundle contains an encrypted member")
    if flag_bits & _SAMPLE_COMPRESSED_PATCH_FLAG:
        raise RuntimeError("sample bundle uses compressed patched data")


def _validate_sample_compression_flags(*, flag_bits: int, compress_type: int) -> None:
    """Reject compression-method flags outside the fixed sample profile."""

    if compress_type == zipfile.ZIP_DEFLATED and flag_bits & _SAMPLE_ENHANCED_DEFLATE_FLAG:
        raise RuntimeError("sample bundle uses enhanced deflating")


def _validate_sample_descriptor_flags(*, flag_bits: int) -> None:
    """Reject trailing data descriptors outside the fixed sample profile."""

    if flag_bits & _SAMPLE_DATA_DESCRIPTOR_FLAG:
        raise RuntimeError("sample bundle uses a data descriptor")


def _validate_sample_zip64_extra_fields(*, extra: bytes) -> None:
    """Reject alternate ZIP64 metadata outside the fixed sample profile."""

    offset = 0
    while len(extra) - offset >= 4:
        field_id = int.from_bytes(extra[offset : offset + 2], "little")
        field_size = int.from_bytes(extra[offset + 2 : offset + 4], "little")
        field_end = offset + 4 + field_size
        if field_end > len(extra):
            return
        if field_id == _SAMPLE_ZIP64_EXTRA_FIELD:
            raise RuntimeError("sample bundle uses a ZIP64 extra field")
        offset = field_end


def _validate_sample_extra_fields(*, extra: bytes) -> None:
    """Reject alternate Unicode paths outside the fixed sample profile."""

    offset = 0
    while len(extra) - offset >= 4:
        field_id = int.from_bytes(extra[offset : offset + 2], "little")
        field_size = int.from_bytes(extra[offset + 2 : offset + 4], "little")
        field_end = offset + 4 + field_size
        if field_end > len(extra):
            return
        if field_id == _SAMPLE_UNICODE_PATH_EXTRA_FIELD:
            raise RuntimeError("sample bundle uses a Unicode Path extra field")
        offset = field_end


def _validate_sample_archive_comment(*, comment: bytes) -> None:
    """Reject archive comments outside the fixed sample profile."""

    if comment:
        raise RuntimeError("sample bundle uses an archive comment")


def _validate_sample_member_comment(*, comment: bytes) -> None:
    """Reject member comments outside the fixed sample profile."""

    if comment:
        raise RuntimeError("sample bundle uses a member comment")


def _validate_sample_member_volume(*, volume: int) -> None:
    """Reject split-volume placement outside the fixed sample profile."""

    if volume != 0:
        raise RuntimeError("sample bundle uses a split-volume member")


def _validate_sample_archive_disk_fields(*, snapshot: IO[bytes]) -> None:
    """Require base-disk values in the conventional final ZIP end record."""

    end_record, _ = _read_final_sample_eocd(snapshot=snapshot)
    disk = int.from_bytes(end_record[4:6], "little")
    central_disk = int.from_bytes(end_record[6:8], "little")
    if disk != 0 or central_disk != 0:
        raise RuntimeError("sample bundle uses unsupported archive disk fields")


def _validate_sample_archive_entry_counts(
    *,
    snapshot: IO[bytes],
    parsed_entries: int,
) -> None:
    """Require conventional ZIP entry counts to match parsed members."""

    end_record, _ = _read_final_sample_eocd(snapshot=snapshot)
    entries_on_disk = int.from_bytes(end_record[8:10], "little")
    total_entries = int.from_bytes(end_record[10:12], "little")
    if entries_on_disk != parsed_entries or total_entries != parsed_entries:
        raise RuntimeError("sample bundle archive entry counts are inconsistent")


def _validate_sample_archive_placement(*, snapshot: IO[bytes]) -> None:
    """Require zero prepended-data adjustment for the fixed ZIP profile."""

    end_record, end_record_offset = _read_final_sample_eocd(snapshot=snapshot)
    directory_size = int.from_bytes(end_record[12:16], "little")
    directory_offset = int.from_bytes(end_record[16:20], "little")
    if directory_size + directory_offset != end_record_offset:
        raise RuntimeError("sample bundle central directory placement is inconsistent")


def _validate_sample_first_local_header(*, infos: tuple[zipfile.ZipInfo, ...]) -> None:
    """Require the earliest parser-exposed local header to begin at byte zero."""

    if infos and min(info.header_offset for info in infos) != 0:
        raise RuntimeError("sample bundle first local header placement is inconsistent")


def _validate_sample_local_header_offsets(*, infos: tuple[zipfile.ZipInfo, ...]) -> None:
    """Require every parser-exposed local-header offset to identify one member."""

    if len({info.header_offset for info in infos}) != len(infos):
        raise RuntimeError("sample bundle local header offsets are inconsistent")


def _validate_sample_local_header_order(*, infos: tuple[zipfile.ZipInfo, ...]) -> None:
    """Require parser-exposed members to follow physical local-header order."""

    offsets = tuple(info.header_offset for info in infos)
    if any(left >= right for left, right in pairwise(offsets)):
        raise RuntimeError("sample bundle local header offsets are out of order")


def _validate_sample_local_header_bounds(
    *,
    snapshot: IO[bytes],
    infos: tuple[zipfile.ZipInfo, ...],
) -> None:
    """Require parser-exposed local headers to precede the central directory."""

    end_record, _ = _read_final_sample_eocd(snapshot=snapshot)
    directory_offset = int.from_bytes(end_record[16:20], "little")
    if any(info.header_offset >= directory_offset for info in infos):
        raise RuntimeError("sample bundle local header offsets are out of bounds")


def _validate_sample_local_header_signatures(
    *,
    snapshot: IO[bytes],
    infos: tuple[zipfile.ZipInfo, ...],
) -> None:
    """Require every parser-exposed offset to identify a local-file header."""

    position = snapshot.tell()
    try:
        for info in infos:
            snapshot.seek(info.header_offset)
            if snapshot.read(4) != _SAMPLE_LOCAL_HEADER_SIGNATURE:
                raise RuntimeError("sample bundle local header signature is inconsistent")
    finally:
        snapshot.seek(position)


def _validate_sample_local_header_prefix_bounds(
    *,
    snapshot: IO[bytes],
    infos: tuple[zipfile.ZipInfo, ...],
) -> None:
    """Require each local header's fixed prefix to precede the directory."""

    end_record, _ = _read_final_sample_eocd(snapshot=snapshot)
    directory_offset = int.from_bytes(end_record[16:20], "little")
    if any(
        info.header_offset + _SAMPLE_FIXED_LOCAL_HEADER_BYTES > directory_offset for info in infos
    ):
        raise RuntimeError("sample bundle local header prefixes are out of bounds")


def _validate_sample_local_header_envelope_bounds(
    *,
    snapshot: IO[bytes],
    infos: tuple[zipfile.ZipInfo, ...],
) -> None:
    """Require each complete local-header envelope to precede the directory."""

    end_record, _ = _read_final_sample_eocd(snapshot=snapshot)
    directory_offset = int.from_bytes(end_record[16:20], "little")
    position = snapshot.tell()
    try:
        for info in infos:
            snapshot.seek(info.header_offset + _SAMPLE_LOCAL_HEADER_LENGTH_FIELDS_OFFSET)
            lengths = snapshot.read(_SAMPLE_LOCAL_HEADER_LENGTH_FIELDS_BYTES)
            name_length = int.from_bytes(lengths[:2], "little")
            extra_length = int.from_bytes(lengths[2:], "little")
            if (
                info.header_offset + _SAMPLE_FIXED_LOCAL_HEADER_BYTES + name_length + extra_length
                > directory_offset
            ):
                raise RuntimeError("sample bundle local header envelopes are out of bounds")
    finally:
        snapshot.seek(position)


def _validate_sample_local_header_names(
    *,
    snapshot: IO[bytes],
    infos: tuple[zipfile.ZipInfo, ...],
) -> None:
    """Require local-header names to match parser-exposed central names."""

    position = snapshot.tell()
    try:
        for info in infos:
            snapshot.seek(info.header_offset + _SAMPLE_LOCAL_HEADER_LENGTH_FIELDS_OFFSET)
            name_length = int.from_bytes(snapshot.read(2), "little")
            snapshot.seek(info.header_offset + _SAMPLE_FIXED_LOCAL_HEADER_BYTES)
            local_name = snapshot.read(name_length)
            encoding = "utf-8" if info.flag_bits & _SAMPLE_UTF8_FILENAME_FLAG else "cp437"
            try:
                central_name = info.orig_filename.encode(encoding)
            except UnicodeEncodeError:
                raise RuntimeError("sample bundle local header names are inconsistent") from None
            if local_name != central_name:
                raise RuntimeError("sample bundle local header names are inconsistent")
    finally:
        snapshot.seek(position)


def _validate_sample_local_header_flags(
    *,
    snapshot: IO[bytes],
    infos: tuple[zipfile.ZipInfo, ...],
) -> None:
    """Require local-header flags to match parser-exposed central flags."""

    position = snapshot.tell()
    try:
        for info in infos:
            snapshot.seek(info.header_offset + _SAMPLE_LOCAL_HEADER_FLAGS_OFFSET)
            local_flags = int.from_bytes(snapshot.read(2), "little")
            if local_flags != info.flag_bits:
                raise RuntimeError("sample bundle local header flags are inconsistent")
    finally:
        snapshot.seek(position)


def _read_final_sample_eocd(*, snapshot: IO[bytes]) -> tuple[bytes, int]:
    """Read and validate the final conventional EOCD without moving the caller."""

    position = snapshot.tell()
    try:
        snapshot.seek(0, os.SEEK_END)
        end_record_offset = snapshot.tell() - _SAMPLE_EOCD_BYTES
        if end_record_offset < 0:
            end_record = b""
        else:
            snapshot.seek(-_SAMPLE_EOCD_BYTES, os.SEEK_END)
            end_record = snapshot.read(_SAMPLE_EOCD_BYTES)
    finally:
        snapshot.seek(position)
    if (
        len(end_record) != _SAMPLE_EOCD_BYTES
        or end_record[:4] != _SAMPLE_EOCD_SIGNATURE
        or end_record[-2:] != b"\x00\x00"
    ):
        raise zipfile.BadZipFile("invalid final end-of-central-directory record")
    return end_record, end_record_offset


def _validate_sample_member_name(*, original_name: str) -> None:
    """Reject a member name that the standard reader truncated at a NUL."""

    if "\x00" in original_name:
        raise RuntimeError("sample bundle member name contains a NUL byte")


def _portable_sample_member_parts(
    info: zipfile.ZipInfo,
    *,
    expected_root: str,
) -> tuple[str, ...]:
    """Return one portable relative file path or fail before extraction."""

    raw_parts = info.filename.split("/")
    if (
        info.is_dir()
        or len(raw_parts) < 2
        or raw_parts[0] != expected_root
        or len("/".join(raw_parts[1:])) > _MAX_SAMPLE_PATH_CHARS
        or any(not _is_portable_sample_member_name(part) for part in raw_parts[1:])
    ):
        raise RuntimeError("sample bundle contains a non-portable member path")
    return tuple(raw_parts[1:])


def _is_portable_sample_member_name(name: str) -> bool:
    return (
        _SAMPLE_MEMBER_PATTERN.fullmatch(name) is not None
        and not name.endswith(".")
        and name.split(".", 1)[0].casefold() not in _WINDOWS_DEVICE_STEMS
    )


def _verify_sbom(sbom: Path, *, wheel: Path, version: str) -> None:
    document = _json_object(sbom)
    if document.get("spdxVersion") != "SPDX-2.3" or document.get("dataLicense") != "CC0-1.0":
        raise RuntimeError("release SBOM is not SPDX 2.3 JSON")
    packages_value = document.get("packages")
    files_value = document.get("files")
    if not isinstance(packages_value, list):
        raise RuntimeError("release SBOM must describe exactly the baseline package")
    if not isinstance(files_value, list):
        raise RuntimeError("release SBOM must describe exactly the baseline wheel")
    packages = cast(list[object], packages_value)
    files = cast(list[object], files_value)
    if len(packages) != 1:
        raise RuntimeError("release SBOM must describe exactly the baseline package")
    if len(files) != 1:
        raise RuntimeError("release SBOM must describe exactly the baseline wheel")
    package = _object(packages[0], "SBOM package")
    wheel_file = _object(files[0], "SBOM file")
    if package.get("name") != "ludoweave" or package.get("versionInfo") != version:
        raise RuntimeError("release SBOM package identity is invalid")
    if wheel_file.get("fileName") != wheel.name:
        raise RuntimeError("release SBOM wheel identity is invalid")
    expected_hash = _sha256(wheel)
    if not _has_sha256(package, expected_hash) or not _has_sha256(wheel_file, expected_hash):
        raise RuntimeError("release SBOM wheel checksum is invalid")


def _verify_manifest(manifest: dict[str, object], *, release: Path, actual_files: set[str]) -> None:
    artifacts_value = manifest.get("artifacts")
    if not isinstance(artifacts_value, list):
        raise RuntimeError("release manifest artifacts must be a list")
    expected_names = actual_files - {"RELEASE_MANIFEST.json", "SHA256SUMS"}
    seen: set[str] = set()
    for item in cast(list[object], artifacts_value):
        artifact = _object(item, "release manifest artifact")
        name = _text(artifact.get("name"), "release manifest artifact name")
        size = artifact.get("bytes")
        digest = artifact.get("sha256")
        if Path(name).name != name or name in seen or name not in expected_names:
            raise RuntimeError("release manifest contains an unsafe or duplicate artifact")
        path = release / name
        if type(size) is not int or size != path.stat().st_size or digest != _sha256(path):
            raise RuntimeError(f"release manifest metadata mismatch for {name}")
        seen.add(name)
    if seen != expected_names:
        raise RuntimeError("release manifest does not cover the exact staged artifacts")


def _has_sha256(value: dict[str, object], expected: str) -> bool:
    checksums_value = value.get("checksums")
    if not isinstance(checksums_value, list):
        return False
    for item in cast(list[object], checksums_value):
        if not isinstance(item, dict):
            continue
        checksum = cast(dict[str, object], item)
        if checksum.get("algorithm") == "SHA256" and checksum.get("checksumValue") == expected:
            return True
    return False


def _read_checksums(path: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for line in path.read_text(encoding="ascii").splitlines():
        digest, separator, name = line.partition("  ")
        if (
            separator != "  "
            or len(digest) != 64
            or any(c not in "0123456789abcdef" for c in digest)
        ):
            raise RuntimeError("SHA256SUMS contains a malformed record")
        if not name or Path(name).name != name or name in result:
            raise RuntimeError("SHA256SUMS contains an unsafe or duplicate name")
        result[name] = digest
    return result


def _run(command: Sequence[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        rendered = subprocess.list2cmdline(command)
        raise RuntimeError(
            f"command failed with exit {result.returncode}: {rendered}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def _python_in(environment: Path) -> Path:
    return (
        environment / "Scripts" / "python.exe"
        if os.name == "nt"
        else environment / "bin" / "python"
    )


def _json_object(path: Path) -> dict[str, object]:
    value: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"{path.name} must contain a JSON object")
    return cast(dict[str, object], value)


def _one(values: Iterable[Path], role: str) -> Path:
    paths = tuple(values)
    if len(paths) != 1:
        raise RuntimeError(f"expected exactly one {role}")
    return paths[0]


def _path_argument(args: argparse.Namespace, name: str) -> Path:
    value: object = getattr(args, name, None)
    if not isinstance(value, Path):
        raise TypeError(f"{name} must be a path")
    return value


def _text(value: object, role: str) -> str:
    if not isinstance(value, str) or not value:
        raise RuntimeError(f"{role} must be non-empty text")
    return value


def _object(value: object, role: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise RuntimeError(f"{role} must be an object")
    return cast(dict[str, object], value)


def _sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return _sha256_stream(stream)


if __name__ == "__main__":
    raise SystemExit(main())
