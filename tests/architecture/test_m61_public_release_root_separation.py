"""Protect M61 public-release candidate/output-root separation."""

from __future__ import annotations

import hashlib
import importlib.util
import json
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


def _load() -> tuple[ModuleType, _Main]:
    spec = importlib.util.spec_from_file_location("m61_public_release_verifier", _VERIFIER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    scripts = str(_ROOT / "scripts")
    sys.path.insert(0, scripts)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(scripts)
    return module, cast(_Main, module.main)


def _environment(runner: Path) -> dict[str, str]:
    return {
        "GITHUB_REF_NAME": "v0.1.0a1",
        "GITHUB_REPOSITORY": "xsparc/ludoweave-engine",
        "RELEASE_ID": "123",
        "RELEASE_TITLE": "LudoWeave 0.1.0a1",
        "RUNNER_TEMP": str(runner),
    }


def _forbid_download(module: ModuleType, monkeypatch: pytest.MonkeyPatch) -> None:
    def forbidden_download(*args: object, **kwargs: object) -> None:
        del args, kwargs
        raise AssertionError("network reached before candidate/output-root separation")

    monkeypatch.setattr(module, "_download", forbidden_download)


@pytest.mark.parametrize("relationship", ("same", "descendant"))
def test_output_root_cannot_equal_or_descend_from_expected_candidate(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    relationship: str,
) -> None:
    module, main = _load()
    expected = tmp_path / "expected"
    expected.mkdir()
    runner = expected if relationship == "same" else expected / "runner"
    if runner != expected:
        runner.mkdir()
    _forbid_download(module, monkeypatch)

    assert main([str(expected)], environment=_environment(runner)) == 1
    report = json.loads(capsys.readouterr().err)
    assert report == {
        "code": "public_release.path_overlap",
        "message": "public release candidate and output root overlap",
        "protocol": "ludoweave.public-release-consumer/1",
        "status": "fail",
    }


def test_resolved_parent_alias_overlap_fails_before_download(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module, main = _load()
    expected = tmp_path / "expected"
    expected.mkdir()
    runner = tmp_path / "runner-alias"
    runner.mkdir()
    original_resolve = Path.resolve

    def aliased_resolve(path: Path, strict: bool = False) -> Path:
        if path == runner:
            return expected / "resolved-runner"
        return original_resolve(path, strict=strict)

    monkeypatch.setattr(Path, "resolve", aliased_resolve)
    _forbid_download(module, monkeypatch)

    assert main([str(expected)], environment=_environment(runner)) == 1
    report = json.loads(capsys.readouterr().err)
    assert report["code"] == "public_release.path_overlap"
    assert str(tmp_path) not in report["message"]


def test_filesystem_identity_parent_alias_fails_before_download(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module, main = _load()
    expected = tmp_path / "expected"
    expected.mkdir()
    runner_parent = tmp_path / "runner-parent"
    runner_parent.mkdir()
    runner = runner_parent / "child"
    runner.mkdir()
    original_samefile = Path.samefile

    def aliased_samefile(path: Path, other: Path) -> bool:
        if path == runner_parent and other == expected:
            return True
        return original_samefile(path, other)

    monkeypatch.setattr(Path, "samefile", aliased_samefile)
    _forbid_download(module, monkeypatch)

    assert main([str(expected)], environment=_environment(runner)) == 1
    report = json.loads(capsys.readouterr().err)
    assert report["code"] == "public_release.path_overlap"
    assert str(tmp_path) not in report["message"]


def test_filesystem_identity_inspection_failure_is_content_silent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module, main = _load()
    expected = tmp_path / "expected"
    expected.mkdir()
    runner = tmp_path / "runner"
    runner.mkdir()

    def denied_samefile(path: Path, other: Path) -> bool:
        del path, other
        raise PermissionError("sensitive identity detail")

    monkeypatch.setattr(Path, "samefile", denied_samefile)
    _forbid_download(module, monkeypatch)

    assert main([str(expected)], environment=_environment(runner)) == 1
    report = json.loads(capsys.readouterr().err)
    assert report["code"] == "public_release.temp_unavailable"
    assert str(tmp_path) not in report["message"]
    assert "sensitive" not in report["message"]


@pytest.mark.parametrize(
    ("failed_root", "error_type", "expected_code"),
    (
        ("candidate", PermissionError, "public_release.candidate_unavailable"),
        ("candidate", RuntimeError, "public_release.candidate_unavailable"),
        ("output", PermissionError, "public_release.temp_unavailable"),
        ("output", RuntimeError, "public_release.temp_unavailable"),
    ),
)
def test_root_resolution_failure_is_content_silent_and_precedes_download(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    failed_root: str,
    error_type: type[Exception],
    expected_code: str,
) -> None:
    module, main = _load()
    expected = tmp_path / "expected"
    expected.mkdir()
    runner = tmp_path / "runner"
    runner.mkdir()
    failed_path = expected if failed_root == "candidate" else runner
    original_resolve = Path.resolve

    def denied_resolve(path: Path, strict: bool = False) -> Path:
        if path == failed_path:
            raise error_type("sensitive root detail")
        return original_resolve(path, strict=strict)

    monkeypatch.setattr(Path, "resolve", denied_resolve)
    _forbid_download(module, monkeypatch)

    assert main([str(expected)], environment=_environment(runner)) == 1
    report = json.loads(capsys.readouterr().err)
    assert report["code"] == expected_code
    assert str(tmp_path) not in report["message"]
    assert "sensitive" not in report["message"]


def test_candidate_may_be_a_separate_child_of_output_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module, main = _load()
    runner = tmp_path / "runner"
    runner.mkdir()
    expected = runner / "expected"
    expected.mkdir()

    class ReachedDownload(AssertionError):
        pass

    def reached_download(*args: object, **kwargs: object) -> None:
        del args, kwargs
        raise ReachedDownload

    monkeypatch.setattr(module, "_download", reached_download)

    with pytest.raises(ReachedDownload):
        main([str(expected)], environment=_environment(runner))


def test_download_uses_resolved_output_root(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module, main = _load()
    expected = tmp_path / "expected"
    expected.mkdir()
    runner_alias = tmp_path / "runner-alias"
    runner_alias.mkdir()
    resolved_runner = tmp_path / "resolved-runner"
    resolved_runner.mkdir()
    original_resolve = Path.resolve

    def aliased_resolve(path: Path, strict: bool = False) -> Path:
        if path == runner_alias:
            return resolved_runner
        return original_resolve(path, strict=strict)

    class ReachedDownload(AssertionError):
        pass

    def reached_download(url: str, target: Path, **kwargs: object) -> None:
        del url, kwargs
        assert target == resolved_runner / "release-public.json"
        raise ReachedDownload

    monkeypatch.setattr(Path, "resolve", aliased_resolve)
    monkeypatch.setattr(module, "_download", reached_download)

    with pytest.raises(ReachedDownload):
        main([str(expected)], environment=_environment(runner_alias))


def test_m61_changes_no_workflow_runtime_dependency_or_package_boundary() -> None:
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
        "m61" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m61_docs_define_root_separation_and_nonclaim_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0044-public-release-root-separation.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m61" in document for document in documents)
    for term in (
        "candidate directory",
        "output root",
        "resolved alias",
        "filesystem identity",
        "case-insensitive",
        "before network",
        "before validator",
        "read-only",
        "no race-free",
        "no workflow",
        "not a real public release observation",
    ):
        assert term in combined
