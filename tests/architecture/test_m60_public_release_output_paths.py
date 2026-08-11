"""Protect M60 public-release filesystem collision conformance."""

from __future__ import annotations

import hashlib
import http.client
import importlib.util
import json
import os
import stat
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from types import ModuleType
from typing import Protocol, cast

import pytest

_ROOT = Path(__file__).parents[2]
_VERIFIER = _ROOT / "scripts" / "verify_public_release.py"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
_RELEASE_SHA256 = "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"


class _Main(Protocol):
    def __call__(
        self,
        argv: Sequence[str] | None = None,
        *,
        environment: Mapping[str, str] | None = None,
    ) -> int: ...


class _Download(Protocol):
    def __call__(
        self,
        url: str,
        target: Path,
        *,
        accept: str,
        maximum_bytes: int,
        maximum_redirects: int,
        expected_bytes: int | None = None,
        partial_name: str | None = None,
    ) -> None: ...


class _CodedError(Protocol):
    code: str


def _load() -> tuple[ModuleType, _Main, _Download]:
    spec = importlib.util.spec_from_file_location("m60_public_release_verifier", _VERIFIER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    scripts = str(_ROOT / "scripts")
    sys.path.insert(0, scripts)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(scripts)
    return module, cast(_Main, module.main), cast(_Download, module._download)


def _environment(runner: Path) -> dict[str, str]:
    return {
        "GITHUB_REF_NAME": "v0.1.0a1",
        "GITHUB_REPOSITORY": "xsparc/ludoweave-engine",
        "RELEASE_ID": "123",
        "RELEASE_TITLE": "LudoWeave 0.1.0a1",
        "RUNNER_TEMP": str(runner),
    }


def _simulate_dangling_entry(monkeypatch: pytest.MonkeyPatch, collision: Path) -> None:
    original_lstat = Path.lstat
    dangling = os.stat_result((stat.S_IFLNK, 0, 0, 0, 0, 0, 0, 0, 0, 0))

    def fake_lstat(path: Path) -> os.stat_result:
        if path == collision:
            return dangling
        return original_lstat(path)

    monkeypatch.setattr(Path, "lstat", fake_lstat)


@pytest.mark.parametrize(
    ("relative_path", "expected_code"),
    (
        ("release-public.json", "public_release.output_exists"),
        ("release-public-download", "public_release.output_exists"),
        ("release-assets.plan", "public_release.plan_exists"),
    ),
)
def test_dangling_preflight_collision_fails_before_download(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    relative_path: str,
    expected_code: str,
) -> None:
    module, main, _ = _load()
    expected = tmp_path / "expected"
    expected.mkdir()
    runner = tmp_path / "runner"
    runner.mkdir()
    _simulate_dangling_entry(monkeypatch, runner / relative_path)

    def forbidden_download(*args: object, **kwargs: object) -> None:
        del args, kwargs
        raise AssertionError("network path reached after a lexical output collision")

    monkeypatch.setattr(module, "_download", forbidden_download)

    assert main([str(expected)], environment=_environment(runner)) == 1
    report = json.loads(capsys.readouterr().err)
    assert report["code"] == expected_code
    assert report["status"] == "fail"


@pytest.mark.parametrize("collision_kind", ("target", "partial"))
def test_download_rejects_dangling_collision_before_connection(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    collision_kind: str,
) -> None:
    module, _, download = _load()
    target = tmp_path / "asset.bin"
    partial_name = ".asset-123.part"
    collision = target if collision_kind == "target" else tmp_path / partial_name
    _simulate_dangling_entry(monkeypatch, collision)

    class ForbiddenConnection:
        def __init__(self, *args: object, **kwargs: object) -> None:
            del args, kwargs
            raise AssertionError("connection created after a lexical output collision")

    monkeypatch.setattr(http.client, "HTTPSConnection", ForbiddenConnection)
    error_type = cast(type[Exception], module.PublicReleaseVerificationError)

    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/assets/123",
            target,
            accept="application/octet-stream",
            maximum_bytes=5,
            maximum_redirects=3,
            expected_bytes=5,
            partial_name=partial_name,
        )

    assert cast(_CodedError, raised.value).code == "public_release.output_exists"


def test_output_identity_inspection_failure_is_content_silent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module, _, download = _load()
    target = tmp_path / "asset.bin"
    original_lstat = Path.lstat

    def denied_lstat(path: Path) -> os.stat_result:
        if path == target:
            raise PermissionError("sensitive path detail")
        return original_lstat(path)

    class ForbiddenConnection:
        def __init__(self, *args: object, **kwargs: object) -> None:
            del args, kwargs
            raise AssertionError("connection created after path inspection failed")

    monkeypatch.setattr(Path, "lstat", denied_lstat)
    monkeypatch.setattr(http.client, "HTTPSConnection", ForbiddenConnection)
    error_type = cast(type[Exception], module.PublicReleaseVerificationError)

    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/assets/123",
            target,
            accept="application/octet-stream",
            maximum_bytes=5,
            maximum_redirects=3,
            expected_bytes=5,
            partial_name=".asset-123.part",
        )

    error = cast(_CodedError, raised.value)
    assert error.code == "public_release.output_failed"
    assert str(tmp_path) not in str(raised.value)
    assert "sensitive" not in str(raised.value)


def test_late_download_directory_collision_keeps_output_exists(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module, main, _ = _load()
    expected = tmp_path / "expected"
    expected.mkdir()
    runner = tmp_path / "runner"
    runner.mkdir()
    output_directory = runner / "release-public-download"
    plan = runner / "release-assets.plan"
    original_mkdir = Path.mkdir
    downloads: list[Path] = []

    def fake_download(
        url: str,
        target: Path,
        *,
        accept: str,
        maximum_bytes: int,
        maximum_redirects: int,
        expected_bytes: int | None = None,
        partial_name: str | None = None,
    ) -> None:
        del url, accept, maximum_bytes, maximum_redirects, expected_bytes, partial_name
        downloads.append(target)
        target.write_bytes(b"{}")

    def fake_validator(arguments: Sequence[str]) -> int:
        assert "--asset-plan" in arguments
        plan.write_text(
            "ludoweave.release-asset-retrieval-plan/1\n1\t5\tasset.bin\n",
            encoding="utf-8",
        )
        return 0

    def racing_mkdir(
        path: Path,
        mode: int = 0o777,
        parents: bool = False,
        exist_ok: bool = False,
    ) -> None:
        if path == output_directory:
            raise FileExistsError
        original_mkdir(path, mode=mode, parents=parents, exist_ok=exist_ok)

    monkeypatch.setattr(module, "_download", fake_download)
    monkeypatch.setattr(module, "_run_release_validator", fake_validator)
    monkeypatch.setattr(Path, "mkdir", racing_mkdir)

    assert main([str(expected)], environment=_environment(runner)) == 1
    report = json.loads(capsys.readouterr().err)
    assert report["code"] == "public_release.output_exists"
    assert downloads == [runner / "release-public.json"]


def test_fresh_plan_inspection_failure_precedes_download(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module, main, _ = _load()
    expected = tmp_path / "expected"
    expected.mkdir()
    runner = tmp_path / "runner"
    runner.mkdir()
    plan = runner / "release-assets.plan"
    original_lstat = Path.lstat

    def denied_lstat(path: Path) -> os.stat_result:
        if path == plan:
            raise PermissionError("sensitive plan detail")
        return original_lstat(path)

    def forbidden_download(*args: object, **kwargs: object) -> None:
        del args, kwargs
        raise AssertionError("download reached after plan inspection failed")

    monkeypatch.setattr(Path, "lstat", denied_lstat)
    monkeypatch.setattr(module, "_download", forbidden_download)

    assert main([str(expected)], environment=_environment(runner)) == 1
    report = json.loads(capsys.readouterr().err)
    assert report["code"] == "public_release.plan_unavailable"
    assert str(tmp_path) not in report["message"]
    assert "sensitive" not in report["message"]


def test_m60_changes_no_workflow_runtime_dependency_or_package_boundary() -> None:
    assert (
        hashlib.sha256((_ROOT / ".github" / "workflows" / "ci.yml").read_bytes()).hexdigest()
        == _CI_SHA256
    )
    assert (
        hashlib.sha256((_ROOT / ".github" / "workflows" / "release.yml").read_bytes()).hexdigest()
        == _RELEASE_SHA256
    )
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == (
        _PYPROJECT_SHA256
    )
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert not any(
        "m60" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m60_docs_define_exact_collision_and_nonclaim_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0043-public-release-output-path-conformance.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m60" in document for document in documents)
    for term in (
        "filesystem collision",
        "dangling link",
        "before network",
        "before validator",
        "exclusive creation",
        "no clobber",
        "no race-free",
        "no workflow",
        "not a real public release observation",
    ):
        assert term in combined
