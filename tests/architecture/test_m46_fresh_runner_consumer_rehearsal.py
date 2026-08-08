"""Protect M46 fresh-runner public release consumer rehearsal boundaries."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).parents[2]
_CI = _ROOT / ".github" / "workflows" / "ci.yml"
_RELEASE = _ROOT / ".github" / "workflows" / "release.yml"
_PUBLIC_SCRIPT = _ROOT / "scripts" / "verify_public_release.sh"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"
_CHECKOUT = "actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd"
_SETUP_UV = "astral-sh/setup-uv@08807647e7069bb48b6ef5acd8ec9567f424441b"
_DOWNLOAD = "actions/download-artifact@3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c"


def _job(source: str, name: str) -> str:
    start = source.index(f"  {name}:\n")
    if name == "release":
        return source[start : source.index("\n  fresh-consumer:\n", start)]
    return source[start:]


def _bash() -> str:
    candidates = [shutil.which("bash")]
    if os.name == "nt":
        candidates.extend(
            (
                r"C:\Program Files\Git\bin\bash.exe",
                r"C:\Program Files\Git\usr\bin\bash.exe",
            )
        )
    for candidate in candidates:
        if candidate is None or not Path(candidate).is_file():
            continue
        try:
            probe = subprocess.run(
                [candidate, "-c", "true"],
                check=False,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        if probe.returncode == 0:
            return candidate
    pytest.skip("a working Bash runtime is unavailable")


def test_fresh_consumer_runs_only_after_successful_release_job() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")
    release = _job(workflow, "release")
    consumer = _job(workflow, "fresh-consumer")

    assert workflow.index("  release:\n") < workflow.index("  fresh-consumer:\n")
    assert "release_id: ${{ steps.verify_draft.outputs.release_id }}" in release
    assert "release_version: ${{ steps.version.outputs.version }}" in release
    assert "needs: release" in consumer
    assert "name: Fresh-runner public release consumer rehearsal" in consumer
    assert "runs-on: ubuntu-latest" in consumer
    assert "timeout-minutes: 25" in consumer
    assert "permissions:\n      contents: read" in consumer
    assert workflow.count("\n    runs-on:") == 2


def test_fresh_consumer_uses_exact_pinned_candidate_handoff() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")
    consumer = _job(workflow, "fresh-consumer")

    assert workflow.count(f"uses: {_CHECKOUT}") == 2
    assert workflow.count(f"uses: {_SETUP_UV}") == 2
    assert workflow.count("uses: actions/upload-artifact@") == 1
    assert workflow.count(f"uses: {_DOWNLOAD}") == 1
    assert "# v8.0.1" in consumer
    assert "persist-credentials: false" in consumer
    assert 'python-version: "3.12"' in consumer
    assert "enable-cache: false" in consumer
    assert "name: ludoweave-${{ needs.release.outputs.release_version }}" in consumer
    assert "path: .tmp/m46-expected-release" in consumer
    for forbidden in ("github-token:", "run-id:", "repository:", "merge-multiple:"):
        assert forbidden not in consumer


def test_fresh_consumer_reuses_exact_bounded_public_verifier() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")
    release = _job(workflow, "release")
    consumer = _job(workflow, "fresh-consumer")
    script = _PUBLIC_SCRIPT.read_text(encoding="utf-8")

    assert "bash scripts/verify_public_release.sh release --use-existing-plan" in release
    assert "RELEASE_ID: ${{ needs.release.outputs.release_id }}" in consumer
    assert "RELEASE_TITLE: LudoWeave ${{ needs.release.outputs.release_version }}" in consumer
    assert "bash scripts/verify_public_release.sh .tmp/m46-expected-release" in consumer
    assert '[[ "$GITHUB_REPOSITORY" != "xsparc/ludoweave-engine" ]]' in script
    assert 'plan_arguments=(--asset-plan "$plan")' in script
    assert '"$2" != "--use-existing-plan"' in script
    assert 'test ! -e "$plan"' in script
    assert '"${plan_arguments[@]}"' in script
    assert script.count("curl --disable --fail --silent --show-error --location") == 2
    assert script.count("--proto '=https' --proto-redir '=https'") == 2
    assert script.count("--connect-timeout 10 --max-time 30") == 2
    assert "head -c 4194305" in script
    assert 'head -c "$((expected_bytes + 1))"' in script
    assert "scripts/smoke_release.py" in script


def test_fresh_consumer_shell_creates_plan_and_smokes_exact_public_bytes(
    tmp_path: Path,
) -> None:
    script = _PUBLIC_SCRIPT.read_text(encoding="utf-8")
    runner = tmp_path / "runner"
    runner.mkdir()
    expected = tmp_path / "expected"
    expected.mkdir()
    notes = b"# Release notes\n\nExact notes.\n"
    (expected / "RELEASE_NOTES.md").write_bytes(notes)
    (expected / "asset.bin").write_bytes(b"asset")
    public_document = tmp_path / "public.json"
    public_document.write_text(
        json.dumps(
            {
                "tag_name": "v0.1.0a1",
                "name": "LudoWeave 0.1.0a1",
                "draft": False,
                "prerelease": True,
                "immutable": False,
                "published_at": "2026-08-09T00:00:00Z",
                "body": notes.decode("utf-8"),
                "assets": [
                    {
                        "id": asset_id,
                        "name": path.name,
                        "size": path.stat().st_size,
                        "digest": f"sha256:{hashlib.sha256(path.read_bytes()).hexdigest()}",
                        "state": "uploaded",
                    }
                    for asset_id, path in (
                        (457, expected / "RELEASE_NOTES.md"),
                        (456, expected / "asset.bin"),
                    )
                ],
            }
        ),
        encoding="utf-8",
    )
    harness = """curl() {
test -z "${GH_TOKEN-}"
test -z "${GITHUB_TOKEN-}"
printf '%s\\n' "$*" >> "$M46_CURL_LOG"
case "${@: -1}" in
  https://api.github.com/repos/xsparc/ludoweave-engine/releases/123)
    command cat "$M46_PUBLIC_DOCUMENT" ;;
  https://api.github.com/repos/xsparc/ludoweave-engine/releases/assets/456)
    command cat expected/asset.bin ;;
  https://api.github.com/repos/xsparc/ludoweave-engine/releases/assets/457)
    command cat expected/RELEASE_NOTES.md ;;
  *) exit 92 ;;
esac
}
python() {
printf '%s\\n' "$*" >> "$M46_PYTHON_LOG"
case "$1" in
  scripts/verify_release_draft.py)
    shift
    "$M46_REAL_PYTHON" "$M46_VERIFY_SCRIPT" "$@" ;;
  scripts/smoke_release.py)
    return 0 ;;
  *)
    return 93 ;;
esac
}
"""
    environment = os.environ.copy()
    environment.pop("GH_TOKEN", None)
    environment.pop("GITHUB_TOKEN", None)
    environment.update(
        {
            "GITHUB_REF_NAME": "v0.1.0a1",
            "GITHUB_REPOSITORY": "xsparc/ludoweave-engine",
            "M46_CURL_LOG": "curl.log",
            "M46_PYTHON_LOG": "python.log",
            "M46_PUBLIC_DOCUMENT": public_document.as_posix(),
            "M46_REAL_PYTHON": Path(sys.executable).as_posix(),
            "M46_VERIFY_SCRIPT": (_ROOT / "scripts" / "verify_release_draft.py").as_posix(),
            "RELEASE_ID": "123",
            "RELEASE_TITLE": "LudoWeave 0.1.0a1",
            "RUNNER_TEMP": "runner",
        }
    )

    result = subprocess.run(
        [
            _bash(),
            "--noprofile",
            "--norc",
            "-e",
            "-o",
            "pipefail",
            "-c",
            harness + script,
            "verify_public_release.sh",
            "expected",
        ],
        cwd=tmp_path,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=15,
    )

    assert result.returncode == 0, result.stderr
    downloaded = runner / "release-public-download"
    assert (downloaded / "asset.bin").read_bytes() == b"asset"
    assert (downloaded / "RELEASE_NOTES.md").read_bytes() == notes
    assert not (downloaded / ".asset-456.part").exists()
    curl_lines = (tmp_path / "curl.log").read_text(encoding="utf-8").splitlines()
    assert len(curl_lines) == 3
    python_lines = (tmp_path / "python.log").read_text(encoding="utf-8").splitlines()
    assert len(python_lines) == 3
    assert "--asset-plan runner/release-assets.plan" in python_lines[0]
    assert sum("scripts/verify_release_draft.py" in line for line in python_lines) == 2
    assert sum("scripts/smoke_release.py" in line for line in python_lines) == 1


@pytest.mark.parametrize(
    ("repository", "arguments", "preexisting_plan"),
    (
        ("different/repository", ("expected",), False),
        ("xsparc/ludoweave-engine", ("expected", "--use-existing-plan"), False),
        ("xsparc/ludoweave-engine", ("expected",), True),
    ),
)
def test_fresh_consumer_rejects_wrong_repository_or_plan_ownership(
    tmp_path: Path,
    repository: str,
    arguments: tuple[str, ...],
    preexisting_plan: bool,
) -> None:
    runner = tmp_path / "runner"
    runner.mkdir()
    (tmp_path / "expected").mkdir()
    if preexisting_plan:
        (runner / "release-assets.plan").write_text("unexpected", encoding="utf-8")
    environment = os.environ.copy()
    environment.update(
        {
            "GITHUB_REPOSITORY": repository,
            "RELEASE_ID": "123",
            "RUNNER_TEMP": "runner",
        }
    )
    result = subprocess.run(
        [
            _bash(),
            "--noprofile",
            "--norc",
            "-e",
            "-o",
            "pipefail",
            "-c",
            _PUBLIC_SCRIPT.read_text(encoding="utf-8"),
            "verify_public_release.sh",
            *arguments,
        ],
        cwd=tmp_path,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=5,
    )
    assert result.returncode != 0


def test_fresh_consumer_has_no_release_mutation_or_public_request_credential() -> None:
    consumer = _job(_RELEASE.read_text(encoding="utf-8"), "fresh-consumer")
    script = _PUBLIC_SCRIPT.read_text(encoding="utf-8")

    for forbidden in (
        "GH_TOKEN",
        "GITHUB_TOKEN",
        "github.token",
        "Authorization:",
        "Cookie:",
        "gh release",
        "gh api",
        "--retry",
        "--clobber",
        "unpublish",
        "delete",
    ):
        assert forbidden not in consumer
        assert forbidden not in script
    for forbidden_permission in ("contents: write", "attestations: write", "id-token: write"):
        assert forbidden_permission not in consumer


def test_m46_changes_no_ci_runtime_dependency_or_public_package_boundary() -> None:
    assert hashlib.sha256(_CI.read_bytes()).hexdigest() == _CI_SHA256
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == (
        _PYPROJECT_SHA256
    )
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert not any(
        "m46" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m46_docs_define_fresh_runner_rehearsal_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0029-fresh-runner-consumer-rehearsal.md",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8").casefold()
        assert "m46" in text
        assert "fresh" in text

    normalized = " ".join(paths[-1].read_text(encoding="utf-8").split()).casefold()
    assert "**status:** accepted" in normalized
    for term in (
        "same workflow",
        "not independent",
        "external",
        "cross-platform",
        "future availability",
        "supported release channel",
        "one additional",
        "no release mutation",
    ):
        assert term in normalized
