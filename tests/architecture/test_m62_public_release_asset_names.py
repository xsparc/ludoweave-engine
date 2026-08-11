"""Protect M62 portable public-release asset-name conformance."""

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


class _Main(Protocol):
    def __call__(
        self,
        argv: Sequence[str] | None = None,
        *,
        environment: Mapping[str, str] | None = None,
    ) -> int: ...


class _AssetPlanParser(Protocol):
    def __call__(self, path: Path) -> tuple[object, ...]: ...


def _load() -> tuple[ModuleType, _Main, _AssetPlanParser]:
    spec = importlib.util.spec_from_file_location("m62_public_release_verifier", _VERIFIER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    scripts = str(_ROOT / "scripts")
    sys.path.insert(0, scripts)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(scripts)
    return module, cast(_Main, module.main), cast(_AssetPlanParser, module._asset_plan)


def _write_plan(path: Path, names: Sequence[str]) -> None:
    records = ["ludoweave.release-asset-retrieval-plan/1"]
    records.extend(f"{index}\t1\t{name}" for index, name in enumerate(names, start=1))
    path.write_text("\n".join(records) + "\n", encoding="utf-8")


def _environment(runner: Path) -> dict[str, str]:
    return {
        "GITHUB_REF_NAME": "v0.1.0a1",
        "GITHUB_REPOSITORY": "xsparc/ludoweave-engine",
        "RELEASE_ID": "123",
        "RELEASE_TITLE": "LudoWeave 0.1.0a1",
        "RUNNER_TEMP": str(runner),
    }


@pytest.mark.parametrize(
    "name",
    (
        "CON",
        "con.txt",
        "PRN.whl",
        "AUX",
        "NUL.json",
        "COM1",
        "com9.zip",
        "LPT1",
        "lpt9.whl",
        "release.",
        "a" * 256,
    ),
)
def test_nonportable_asset_name_is_rejected_content_silently(
    tmp_path: Path,
    name: str,
) -> None:
    module, _, asset_plan = _load()
    path = tmp_path / "release-assets.plan"
    _write_plan(path, (name,))

    with pytest.raises(RuntimeError) as caught:
        asset_plan(path)

    assert getattr(caught.value, "code", None) == "public_release.invalid_plan"
    assert name not in str(caught.value)
    assert isinstance(caught.value, module.PublicReleaseVerificationError)


def test_ascii_case_insensitive_asset_name_collision_is_rejected(
    tmp_path: Path,
) -> None:
    _, _, asset_plan = _load()
    path = tmp_path / "release-assets.plan"
    _write_plan(path, ("ludoweave.whl", "LUDOWEAVE.WHL"))

    with pytest.raises(RuntimeError) as caught:
        asset_plan(path)

    assert getattr(caught.value, "code", None) == "public_release.invalid_plan"


def test_portable_asset_names_remain_valid(tmp_path: Path) -> None:
    _, _, asset_plan = _load()
    path = tmp_path / "release-assets.plan"
    _write_plan(
        path,
        (
            "ludoweave-0.1.0a1-py3-none-any.whl",
            "ludoweave+samples_0.1.0a1.zip",
            "SHA256SUMS",
        ),
    )

    assert len(asset_plan(path)) == 3


def test_invalid_existing_plan_precedes_asset_output_and_download(
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
    _write_plan(plan, ("CON.txt",))
    downloads: list[Path] = []

    def fake_download(url: str, target: Path, **kwargs: object) -> None:
        del url, kwargs
        downloads.append(target)
        if len(downloads) > 1:
            raise AssertionError("asset download reached for invalid portable name")
        target.write_bytes(b"{}")

    def validator_succeeds(arguments: Sequence[str]) -> int:
        del arguments
        return 0

    monkeypatch.setattr(module, "_download", fake_download)
    monkeypatch.setattr(module, "_run_release_validator", validator_succeeds)

    assert (
        main(
            [str(expected), "--use-existing-plan"],
            environment=_environment(runner),
        )
        == 1
    )
    report = json.loads(capsys.readouterr().err)
    assert report["code"] == "public_release.invalid_plan"
    assert downloads == [runner / "release-public.json"]
    assert not (runner / "release-public-download").exists()


def test_m62_changes_no_workflow_runtime_dependency_or_package_boundary() -> None:
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
        "m62" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m62_docs_define_portable_asset_names_and_nonclaim_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0045-portable-public-release-asset-names.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m62" in document for document in documents)
    completed = re.search(r"m0 through m([0-9]+) are hosted-validated", documents[0])
    assert completed is not None and int(completed.group(1)) >= 61
    for term in (
        "portable asset name",
        "windows device",
        "trailing period",
        "255",
        "case-insensitive",
        "before asset download",
        "no filesystem probing",
        "no workflow",
        "not a real public release observation",
    ):
        assert term in combined
