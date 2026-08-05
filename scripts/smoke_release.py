"""Verify checksums/SBOM and run bundled alpha samples from an installed wheel."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
import zipfile
from collections.abc import Iterable, Sequence
from pathlib import Path, PurePosixPath
from typing import cast

from constrained_3d_evidence import validate_constrained_3d_evidence
from visual_editor_evidence import validate_visual_editor_evidence
from wasm_mod_security_evidence import validate_wasm_mod_security_evidence


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
        sample_root = _extract_bundle(bundle, samples, version=version)
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


def _extract_bundle(bundle: Path, output: Path, *, version: str) -> Path:
    expected_root = f"ludoweave-samples-{version}"
    with zipfile.ZipFile(bundle) as archive:
        for info in archive.infolist():
            path = PurePosixPath(info.filename)
            if (
                path.is_absolute()
                or not path.parts
                or path.parts[0] != expected_root
                or ".." in path.parts
                or "\\" in info.filename
            ):
                raise RuntimeError("sample bundle contains an unsafe path")
            mode = info.external_attr >> 16
            if stat.S_ISLNK(mode):
                raise RuntimeError("sample bundle must not contain symbolic links")
            destination = output.joinpath(*path.parts)
            destination.parent.mkdir(parents=True, exist_ok=True)
            if not info.is_dir():
                destination.write_bytes(archive.read(info))
    root = output / expected_root
    required = {
        "README.md",
        "agent_tool_conformance.py",
        "alpha_acceptance.py",
        "clockwork_arena.py",
        "constrained_3d_decision.py",
        "render_device_conformance.py",
        "rollback_readiness.py",
        "visual_editor_decision.py",
        "wasm_mod_security_decision.py",
    }
    if not root.is_dir() or not required <= {path.name for path in root.iterdir()}:
        raise RuntimeError("sample bundle is incomplete")
    return root


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
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
