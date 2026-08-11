"""Protect M63 public-release subordinate-output and status conformance."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
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
_PRIVATE_STDOUT = "private subordinate stdout"
_PRIVATE_STDERR = "private subordinate stderr"


class _Main(Protocol):
    def __call__(
        self,
        argv: Sequence[str] | None = None,
        *,
        environment: Mapping[str, str] | None = None,
    ) -> int: ...


class _HostileStatus:
    def __eq__(self, other: object) -> bool:
        del other
        raise AssertionError("subordinate status equality must not be invoked")

    def __ne__(self, other: object) -> bool:
        del other
        raise AssertionError("subordinate status inequality must not be invoked")


def _load() -> tuple[ModuleType, _Main]:
    spec = importlib.util.spec_from_file_location("m63_public_release_verifier", _VERIFIER)
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


def _run_consumer(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    *,
    validator_status: object = 0,
    smoke_status: object = 0,
    smoke_error: BaseException | None = None,
) -> tuple[int, str, str]:
    module, main = _load()
    expected = tmp_path / "expected"
    expected.mkdir()
    runner = tmp_path / "runner"
    runner.mkdir()

    def fake_download(
        url: str,
        target: Path,
        **kwargs: object,
    ) -> None:
        del kwargs
        target.write_bytes(b"{}" if url.endswith("/releases/123") else b"x")

    def fake_validator(arguments: Sequence[str] | None = None) -> object:
        print(_PRIVATE_STDOUT)
        print(_PRIVATE_STDERR, file=sys.stderr)
        assert arguments is not None
        if "--asset-plan" in arguments:
            plan = Path(arguments[arguments.index("--asset-plan") + 1])
            plan.write_text(
                "ludoweave.release-asset-retrieval-plan/1\n1\t1\tasset.bin\n",
                encoding="utf-8",
            )
        return validator_status

    def fake_smoke(arguments: Sequence[str] | None = None) -> object:
        print(_PRIVATE_STDOUT)
        print(_PRIVATE_STDERR, file=sys.stderr)
        assert arguments is not None
        if smoke_error is not None:
            raise smoke_error
        return smoke_status

    monkeypatch.setattr(module, "_download", fake_download)
    monkeypatch.setattr(module.verify_release_draft, "main", fake_validator)
    monkeypatch.setattr(module.smoke_release, "main", fake_smoke)
    result = main([str(expected)], environment=_environment(runner))
    captured = capsys.readouterr()
    return result, captured.out, captured.err


def test_success_emits_exactly_one_public_consumer_document(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    result, stdout, stderr = _run_consumer(tmp_path, monkeypatch, capsys)

    assert result == 0
    assert stderr == ""
    assert len(stdout.splitlines()) == 1
    assert json.loads(stdout) == {
        "assets": 1,
        "bytes": 1,
        "protocol": "ludoweave.public-release-consumer/1",
        "status": "pass",
    }


def test_validator_streams_restore_after_subordinate_exception(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module, _ = _load()

    def failing_validator(arguments: Sequence[str] | None = None) -> int:
        del arguments
        print(_PRIVATE_STDOUT)
        print(_PRIVATE_STDERR, file=sys.stderr)
        raise RuntimeError("private validator failure")

    monkeypatch.setattr(module.verify_release_draft, "main", failing_validator)
    with pytest.raises(RuntimeError, match="private validator failure"):
        module._run_release_validator(())

    print("restored stdout")
    print("restored stderr", file=sys.stderr)
    captured = capsys.readouterr()
    assert captured.out == "restored stdout\n"
    assert captured.err == "restored stderr\n"


@pytest.mark.parametrize(
    ("smoke_status", "smoke_error"),
    ((1, None), (0, RuntimeError("private smoke failure"))),
    ids=("nonzero", "exception"),
)
def test_smoke_failure_emits_only_one_content_silent_failure_document(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    smoke_status: object,
    smoke_error: BaseException | None,
) -> None:
    result, stdout, stderr = _run_consumer(
        tmp_path,
        monkeypatch,
        capsys,
        smoke_status=smoke_status,
        smoke_error=smoke_error,
    )

    assert result == 1
    assert stdout == ""
    assert len(stderr.splitlines()) == 1
    report = json.loads(stderr)
    assert report["code"] == "public_release.smoke_failed"
    assert _PRIVATE_STDOUT not in stderr
    assert _PRIVATE_STDERR not in stderr
    assert "private smoke failure" not in stderr


@pytest.mark.parametrize(
    ("subordinate", "status", "expected_code"),
    (
        ("validator", False, "public_release.document_mismatch"),
        ("validator", 0.0, "public_release.document_mismatch"),
        ("validator", _HostileStatus(), "public_release.document_mismatch"),
        ("smoke", False, "public_release.smoke_failed"),
        ("smoke", 0.0, "public_release.smoke_failed"),
        ("smoke", _HostileStatus(), "public_release.smoke_failed"),
    ),
)
def test_subordinate_status_requires_exact_zero_integer_without_comparison_hooks(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    subordinate: str,
    status: object,
    expected_code: str,
) -> None:
    validator_status = status if subordinate == "validator" else 0
    smoke_status = status if subordinate == "smoke" else 0

    result, stdout, stderr = _run_consumer(
        tmp_path,
        monkeypatch,
        capsys,
        validator_status=validator_status,
        smoke_status=smoke_status,
    )

    assert result == 1
    assert stdout == ""
    assert len(stderr.splitlines()) == 1
    assert json.loads(stderr)["code"] == expected_code


def test_m63_changes_no_workflow_runtime_dependency_or_package_boundary() -> None:
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
        "m63" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m63_docs_define_subordinate_output_and_status_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0046-public-release-output-confinement.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m63" in document for document in documents)
    completed = re.search(r"m0 through m([0-9]+) are hosted-validated", documents[0])
    assert completed is not None and int(completed.group(1)) >= 62
    for term in (
        "one json document",
        "subordinate stdout",
        "subordinate stderr",
        "exact zero integer",
        "content-silent",
        "single-thread",
        "no workflow",
        "not a real public release observation",
    ):
        assert term in combined
