"""Published release attestation verification is bounded and content-silent."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from collections.abc import Callable, Sequence
from pathlib import Path
from types import ModuleType
from typing import Protocol, cast

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_SCRIPT = _ROOT / "scripts" / "verify_release_attestations.py"
_TAG = "v0.1.0a1"
_COMMIT = "a" * 40
_REPOSITORY = "xsparc/ludoweave-engine"
_WORKFLOW = "xsparc/ludoweave-engine/.github/workflows/release.yml"
_OIDC_ISSUER = "https://token.actions.githubusercontent.com"
_PROVENANCE = "https://slsa.dev/provenance/v1"
_SBOM = "https://spdx.dev/Document/v2.3"


class _Summary(Protocol):
    assets: int
    provenance_checks: int
    sbom_checks: int


class _CodedError(Protocol):
    code: str


class _Verifier(Protocol):
    def verify_attestations(
        self,
        download_directory: Path,
        asset_plan: Path,
        *,
        expected_tag: str,
        expected_commit: str,
        run_command: Callable[[tuple[str, ...]], None] | None = None,
    ) -> _Summary: ...


def _load_verifier() -> ModuleType:
    name = "verify_release_attestations"
    spec = importlib.util.spec_from_file_location(name, _SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError("could not load release attestation verifier")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


_MODULE = _load_verifier()
_VERIFIER = cast(_Verifier, _MODULE)
_RUN_COMMAND = cast(Callable[[tuple[str, ...]], None], vars(_MODULE)["_run_command"])
_MAIN = cast(Callable[[Sequence[str] | None], int], vars(_MODULE)["main"])
_SUBPROCESS = cast(ModuleType, vars(_MODULE)["subprocess"])


def _release(tmp_path: Path) -> tuple[Path, Path]:
    downloaded = tmp_path / "release-download"
    downloaded.mkdir(parents=True)
    contents = {
        "LICENSE": b"license\n",
        "RELEASE_NOTES.md": b"# Release notes\n",
        "SHA256SUMS": b"checksums\n",
        "ludoweave-0.1.0a1-py3-none-any.whl": b"wheel\n",
    }
    for name, content in contents.items():
        (downloaded / name).write_bytes(content)
    plan = tmp_path / "release-assets.plan"
    rows = ["ludoweave.release-asset-retrieval-plan/1"]
    rows.extend(
        f"{asset_id}\t{len(contents[name])}\t{name}"
        for asset_id, name in enumerate(sorted(contents), start=1_001)
    )
    plan.write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    return downloaded, plan


def _verify(
    downloaded: Path,
    plan: Path,
    run_command: Callable[[tuple[str, ...]], None] | None = None,
) -> _Summary:
    return _VERIFIER.verify_attestations(
        downloaded,
        plan,
        expected_tag=_TAG,
        expected_commit=_COMMIT,
        run_command=run_command,
    )


def _error(
    downloaded: Path,
    plan: Path,
    *,
    expected_tag: str = _TAG,
    expected_commit: str = _COMMIT,
) -> ValueError:
    with pytest.raises(ValueError) as captured:
        _VERIFIER.verify_attestations(
            downloaded,
            plan,
            expected_tag=expected_tag,
            expected_commit=expected_commit,
            run_command=lambda _command: None,
        )
    return captured.value


def _code(error: ValueError) -> str:
    return cast(_CodedError, error).code


def test_exact_assets_verify_provenance_and_one_wheel_sbom(tmp_path: Path) -> None:
    downloaded, plan = _release(tmp_path)
    commands: list[tuple[str, ...]] = []

    summary = _verify(downloaded, plan, commands.append)

    assert (summary.assets, summary.provenance_checks, summary.sbom_checks) == (4, 4, 1)
    assert len(commands) == 5
    provenance = commands[:4]
    sbom = commands[4]
    assert all(_argument(command, "--predicate-type") == _PROVENANCE for command in provenance)
    assert _argument(sbom, "--predicate-type") == _SBOM
    assert sbom[3].endswith("ludoweave-0.1.0a1-py3-none-any.whl")
    for command in commands:
        assert command[:3] == ("gh", "attestation", "verify")
        assert _argument(command, "--repo") == _REPOSITORY
        assert _argument(command, "--signer-workflow") == _WORKFLOW
        assert _argument(command, "--signer-digest") == _COMMIT
        assert _argument(command, "--source-ref") == f"refs/tags/{_TAG}"
        assert _argument(command, "--source-digest") == _COMMIT
        assert _argument(command, "--cert-oidc-issuer") == _OIDC_ISSUER
        assert _argument(command, "--limit") == "30"
        assert command.count("--deny-self-hosted-runners") == 1


def _argument(command: Sequence[str], flag: str) -> str:
    index = command.index(flag)
    return command[index + 1]


@pytest.mark.parametrize(
    ("tag", "commit"),
    [
        ("release/0.1.0", _COMMIT),
        ("v0.1.0\n", _COMMIT),
        (_TAG, "A" * 40),
        (_TAG, "a" * 39),
    ],
)
def test_invalid_release_identity_fails_before_any_command(
    tmp_path: Path, tag: str, commit: str
) -> None:
    downloaded, plan = _release(tmp_path)
    error = _error(downloaded, plan, expected_tag=tag, expected_commit=commit)
    assert _code(error) == "release_attestation.invalid_identity"


@pytest.mark.parametrize(
    "payload",
    [
        b"",
        b"wrong/1\n1\t1\tLICENSE\n",
        b"ludoweave.release-asset-retrieval-plan/1",
        b"ludoweave.release-asset-retrieval-plan/1\r\n1\t1\tLICENSE\r\n",
        b"ludoweave.release-asset-retrieval-plan/1\n1\t1\tLICENSE\x00\n",
        b"ludoweave.release-asset-retrieval-plan/1\n\xff\n",
        b"ludoweave.release-asset-retrieval-plan/1\n0\t1\tLICENSE\n",
        b"ludoweave.release-asset-retrieval-plan/1\n01\t1\tLICENSE\n",
        b"ludoweave.release-asset-retrieval-plan/1\n9223372036854775808\t1\tLICENSE\n",
        b"ludoweave.release-asset-retrieval-plan/1\n1\t01\tLICENSE\n",
        b"ludoweave.release-asset-retrieval-plan/1\n1\t268435457\tLICENSE\n",
        b"ludoweave.release-asset-retrieval-plan/1\n1\t1\t../LICENSE\n",
        b"ludoweave.release-asset-retrieval-plan/1\n1\t1\tLICENSE\textra\n",
        b"ludoweave.release-asset-retrieval-plan/1\n1\t1\tLICENSE\n1\t1\tNOTICE\n",
        b"ludoweave.release-asset-retrieval-plan/1\n1\t1\tLICENSE\n2\t1\tLICENSE\n",
        b"ludoweave.release-asset-retrieval-plan/1\n1\t268435456\tLICENSE\n2\t268435456\tNOTICE\n3\t1\tSHA256SUMS\n",
    ],
    ids=[
        "empty",
        "protocol",
        "no-final-newline",
        "carriage-return",
        "nul",
        "non-utf8",
        "zero-id",
        "leading-zero-id",
        "large-id",
        "leading-zero-size",
        "large-size",
        "unsafe-name",
        "extra-field",
        "duplicate-id",
        "duplicate-name",
        "large-total",
    ],
)
def test_noncanonical_or_unbounded_plan_fails_closed(tmp_path: Path, payload: bytes) -> None:
    downloaded, plan = _release(tmp_path)
    plan.write_bytes(payload)
    assert _code(_error(downloaded, plan)) == "release_attestation.invalid_plan"


def test_oversized_or_too_many_plan_rows_fail_closed(tmp_path: Path) -> None:
    downloaded, plan = _release(tmp_path)
    plan.write_bytes(b"x" * (16 * 1024 + 1))
    assert _code(_error(downloaded, plan)) == "release_attestation.invalid_plan"

    rows = ["ludoweave.release-asset-retrieval-plan/1"]
    rows.extend(f"{index + 1}\t0\tasset-{index:02}.txt" for index in range(33))
    plan.write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    assert _code(_error(downloaded, plan)) == "release_attestation.invalid_plan"


def test_plan_order_and_downloaded_set_are_exact(tmp_path: Path) -> None:
    downloaded, plan = _release(tmp_path)
    lines = plan.read_text(encoding="utf-8").splitlines()
    plan.write_text("\n".join([lines[0], lines[2], lines[1], *lines[3:]]) + "\n")
    assert _code(_error(downloaded, plan)) == "release_attestation.invalid_plan"

    downloaded, plan = _release(tmp_path / "second")
    (downloaded / "extra.txt").write_bytes(b"extra")
    assert _code(_error(downloaded, plan)) == "release_attestation.asset_set_mismatch"


def test_missing_size_drift_and_nonfile_assets_fail_closed(tmp_path: Path) -> None:
    downloaded, plan = _release(tmp_path)
    (downloaded / "LICENSE").unlink()
    assert _code(_error(downloaded, plan)) == "release_attestation.asset_set_mismatch"

    downloaded, plan = _release(tmp_path / "size")
    (downloaded / "LICENSE").write_bytes(b"different length")
    assert _code(_error(downloaded, plan)) == "release_attestation.asset_mismatch"

    downloaded, plan = _release(tmp_path / "directory")
    (downloaded / "LICENSE").unlink()
    (downloaded / "LICENSE").mkdir()
    assert _code(_error(downloaded, plan)) == "release_attestation.asset_mismatch"


@pytest.mark.skipif(not hasattr(os, "symlink"), reason="symlink support unavailable")
def test_symlinked_inputs_fail_closed_when_supported(tmp_path: Path) -> None:
    downloaded, plan = _release(tmp_path)
    link = tmp_path / "plan-link"
    try:
        link.symlink_to(plan)
    except OSError:
        pytest.skip("symlink creation is not permitted")
    assert _code(_error(downloaded, link)) == "release_attestation.invalid_plan"

    target = downloaded / "LICENSE"
    target.unlink()
    try:
        target.symlink_to(downloaded / "SHA256SUMS")
    except OSError:
        pytest.skip("symlink creation is not permitted")
    assert _code(_error(downloaded, plan)) == "release_attestation.asset_mismatch"


@pytest.mark.parametrize("wheel_count", [0, 2])
def test_exactly_one_pure_wheel_is_required(tmp_path: Path, wheel_count: int) -> None:
    downloaded, _plan = _release(tmp_path)
    original = downloaded / "ludoweave-0.1.0a1-py3-none-any.whl"
    if wheel_count == 0:
        original.rename(downloaded / "ludoweave-0.1.0a1.tar.gz")
    else:
        (downloaded / "ludoweave-0.1.0a2-py3-none-any.whl").write_bytes(b"second")
    plan = tmp_path / "wheel-set.plan"
    rows = ["ludoweave.release-asset-retrieval-plan/1"]
    rows.extend(
        f"{index}\t{path.stat().st_size}\t{path.name}"
        for index, path in enumerate(
            sorted(downloaded.iterdir(), key=lambda item: item.name), start=1
        )
    )
    plan.write_text("\n".join(rows) + "\n", encoding="utf-8", newline="\n")
    assert _code(_error(downloaded, plan)) == "release_attestation.invalid_wheel_set"


def test_command_failures_are_structured_and_suppress_child_streams(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    observed: dict[str, object] = {}

    def failed_run(command: Sequence[str], **kwargs: object) -> subprocess.CompletedProcess[bytes]:
        observed["command"] = tuple(command)
        observed.update(kwargs)
        return subprocess.CompletedProcess(command, 1)

    monkeypatch.setattr(_SUBPROCESS, "run", failed_run)
    with pytest.raises(ValueError) as captured:
        _RUN_COMMAND(("gh", "attestation", "verify", "artifact"))
    assert _code(captured.value) == "release_attestation.verification_failed"
    assert observed["stdin"] is subprocess.DEVNULL
    assert observed["stdout"] is subprocess.DEVNULL
    assert observed["stderr"] is subprocess.DEVNULL
    assert observed["timeout"] == 30.0
    assert observed["check"] is False


@pytest.mark.parametrize(
    ("failure", "code"),
    [
        (subprocess.TimeoutExpired(("gh",), 30), "release_attestation.timeout"),
        (OSError("unavailable secret"), "release_attestation.unavailable"),
    ],
)
def test_timeout_or_unavailable_verifier_is_structured(
    monkeypatch: pytest.MonkeyPatch, failure: BaseException, code: str
) -> None:
    def fail(*_args: object, **_kwargs: object) -> None:
        raise failure

    monkeypatch.setattr(_SUBPROCESS, "run", fail)
    with pytest.raises(ValueError) as captured:
        _RUN_COMMAND(("gh",))
    assert _code(captured.value) == code
    assert "secret" not in str(captured.value)


def test_cli_failure_is_content_silent_and_has_no_traceback(tmp_path: Path) -> None:
    downloaded, plan = _release(tmp_path)
    secret = "sensitive-plan-content"
    plan.write_text(secret, encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable,
            str(_SCRIPT),
            str(downloaded),
            str(plan),
            "--expected-tag",
            _TAG,
            "--expected-commit",
            _COMMIT,
        ],
        cwd=_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert result.stdout == ""
    assert "Traceback" not in result.stderr
    assert secret not in result.stderr
    assert str(plan) not in result.stderr
    assert json.loads(result.stderr) == {
        "code": "release_attestation.invalid_plan",
        "message": "asset retrieval plan is not canonical text",
        "protocol": "ludoweave.release-attestation-integrity/1",
        "status": "fail",
    }


def test_cli_success_emits_only_protocol_status_and_counts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    downloaded, plan = _release(tmp_path)

    def verified(
        _downloaded: Path,
        _plan: Path,
        *,
        expected_tag: str,
        expected_commit: str,
        run_command: Callable[[tuple[str, ...]], None] | None = None,
    ) -> _Summary:
        del expected_tag, expected_commit, run_command
        return cast(
            _Summary,
            type(
                "Summary",
                (),
                {"assets": 4, "provenance_checks": 4, "sbom_checks": 1},
            )(),
        )

    monkeypatch.setattr(_MODULE, "verify_attestations", verified)
    assert (
        _MAIN(
            [
                str(downloaded),
                str(plan),
                "--expected-tag",
                _TAG,
                "--expected-commit",
                _COMMIT,
            ]
        )
        == 0
    )
    captured = capsys.readouterr()
    assert captured.err == ""
    assert json.loads(captured.out) == {
        "assets": 4,
        "protocol": "ludoweave.release-attestation-integrity/1",
        "provenance_checks": 4,
        "sbom_checks": 1,
        "status": "pass",
    }
    for secret in (_TAG, _COMMIT, str(downloaded), str(plan), "SLSA", "SPDX"):
        assert secret not in captured.out
