"""Protect M45 credential-free public retrieval and installed consumer smoke."""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import textwrap
from pathlib import Path

import pytest

_ROOT = Path(__file__).parents[2]
_CI = _ROOT / ".github" / "workflows" / "ci.yml"
_RELEASE = _ROOT / ".github" / "workflows" / "release.yml"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
_PYPROJECT_SHA256 = "42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1"
_LOCK_SHA256 = "e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed"


def _step(source: str, name: str, next_name: str | None = None) -> str:
    start = source.index(f"      - name: {name}\n")
    if next_name is None:
        return source[start:]
    return source[start : source.index(f"      - name: {next_name}\n", start + 1)]


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


def _run_script(source: str) -> str:
    marker = "        run: |\n"
    assert marker in source
    return textwrap.dedent(source.split(marker, 1)[1])


def test_public_consumer_path_follows_attestation_verification() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")
    public = _step(workflow, "Verify public release consumer path")

    required = (
        "Publish verified GitHub prerelease",
        "Verify published GitHub prerelease",
        "Retrieve and verify published release assets",
        "Verify published release attestations",
        "Verify public release consumer path",
    )
    offsets = [workflow.index(name) for name in required]
    assert offsets == sorted(offsets)

    assert "RELEASE_ID: ${{ steps.verify_draft.outputs.release_id }}" in public
    assert '[[ ! "$RELEASE_ID" =~ ^[1-9][0-9]{0,18}$ ]]' in public
    assert "[[ ${#RELEASE_ID} -eq 19" in public
    assert '"9223372036854775807"' in public
    assert 'test ! -e "$public_document"' in public
    assert 'test ! -e "$public_dir"' in public
    assert 'mkdir "$public_dir"' in public


def test_public_document_and_assets_use_exact_bounded_https_requests() -> None:
    public = _step(
        _RELEASE.read_text(encoding="utf-8"),
        "Verify public release consumer path",
    )

    assert public.count("curl --disable --fail --silent --show-error --location") == 2
    assert public.count("--max-redirs 3") == 2
    assert public.count("--connect-timeout 10 --max-time 30") == 2
    assert public.count("--proto '=https' --proto-redir '=https'") == 2
    assert '"Accept: application/vnd.github+json"' in public
    assert '"Accept: application/octet-stream"' in public
    assert public.count('"X-GitHub-Api-Version: 2026-03-10"') == 2
    assert '"https://api.github.com/repos/$GITHUB_REPOSITORY/releases/$RELEASE_ID"' in public
    assert '"https://api.github.com/repos/$GITHUB_REPOSITORY/releases/assets/$asset_id"' in public
    assert "head -c 4194305" in public
    assert 'test "$(wc -c < "$public_document")" -le 4194304' in public
    assert 'head -c "$((expected_bytes + 1))"' in public
    assert 'test "$(wc -c < "$partial")" -eq "$expected_bytes"' in public

    for forbidden in (
        "GH_TOKEN",
        "GITHUB_TOKEN",
        "github.token",
        "Authorization:",
        "Cookie:",
        "--netrc",
        "browser_download_url",
        "gh api",
        "gh release",
        "wget ",
        "http://",
        "--location-trusted",
        "--retry",
    ):
        assert forbidden not in public


def test_public_retrieval_revalidates_plan_set_and_installed_candidate() -> None:
    public = _step(
        _RELEASE.read_text(encoding="utf-8"),
        "Verify public release consumer path",
    )

    for required in (
        'plan="$RUNNER_TEMP/release-assets.plan"',
        'exec 3< "$plan"',
        'test "$protocol" = "ludoweave.release-asset-retrieval-plan/1"',
        "IFS=$'\\t' read -r asset_id expected_bytes asset_name <&3",
        "^[1-9][0-9]{0,18}$",
        '"9223372036854775807"',
        "^(0|[1-9][0-9]{0,8})$",
        '"268435456"',
        "^[0-9A-Za-z][0-9A-Za-z._+-]{0,255}$",
        'test "$asset_count" -lt 32',
        'test "$expected_total" -le 536870912',
        'test ! -e "$target"',
        'test ! -e "$partial"',
        'mv "$partial" "$target"',
        'test "$asset_count" -gt 0',
    ):
        assert required in public

    assert public.count("scripts/verify_release_draft.py") == 2
    assert 'release "$public_document"' in public
    assert '"$public_dir" "$public_document"' in public
    assert public.count("--expected-state published") == 2
    assert 'scripts/smoke_release.py "$public_dir"' in public
    assert public.index('release "$public_document"') < public.index("while IFS=")
    assert public.index('"$public_dir" "$public_document"') < public.index(
        'scripts/smoke_release.py "$public_dir"'
    )


def test_public_consumer_shell_executes_exact_bounded_plan_without_credentials(
    tmp_path: Path,
) -> None:
    script = _run_script(
        _step(
            _RELEASE.read_text(encoding="utf-8"),
            "Verify public release consumer path",
        )
    )
    runner = tmp_path / "runner"
    runner.mkdir()
    (runner / "release-assets.plan").write_text(
        "ludoweave.release-asset-retrieval-plan/1\n456\t5\tasset.bin\n",
        encoding="utf-8",
        newline="\n",
    )
    harness = """curl() {
test -z "${GH_TOKEN-}"
test -z "${GITHUB_TOKEN-}"
printf '%s\\n' "$*" >> "$M45_CURL_LOG"
case "${@: -1}" in
  https://api.github.com/repos/xsparc/ludoweave-engine/releases/123)
    printf '%s' '{"public":true}' ;;
  https://api.github.com/repos/xsparc/ludoweave-engine/releases/assets/456)
    printf '%s' 'asset' ;;
  *) exit 92 ;;
esac
}
uv() {
printf '%s\\n' "$*" >> "$M45_UV_LOG"
}
"""
    environment = os.environ.copy()
    environment.pop("GH_TOKEN", None)
    environment.pop("GITHUB_TOKEN", None)
    environment.update(
        {
            "GITHUB_REF_NAME": "v0.1.0a1",
            "GITHUB_REPOSITORY": "xsparc/ludoweave-engine",
            "M45_CURL_LOG": "curl.log",
            "M45_UV_LOG": "uv.log",
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
    assert not (downloaded / ".asset-456.part").exists()
    curl_lines = (tmp_path / "curl.log").read_text(encoding="utf-8").splitlines()
    assert len(curl_lines) == 2
    assert all("--disable --fail --silent --show-error --location" in line for line in curl_lines)
    assert all("Authorization:" not in line and "Cookie:" not in line for line in curl_lines)
    uv_lines = (tmp_path / "uv.log").read_text(encoding="utf-8").splitlines()
    assert len(uv_lines) == 3
    assert sum("scripts/verify_release_draft.py" in line for line in uv_lines) == 2
    assert sum("scripts/smoke_release.py" in line for line in uv_lines) == 1


def test_m45_adds_no_runner_action_permission_trigger_or_dependency() -> None:
    release = _RELEASE.read_text(encoding="utf-8")

    assert hashlib.sha256(_CI.read_bytes()).hexdigest() == _CI_SHA256
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == (
        _PYPROJECT_SHA256
    )
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert release.count("\n    runs-on:") == 1
    assert "if: github.repository == 'xsparc/ludoweave-engine'" in release
    assert release.count("uses: actions/checkout@") == 1
    assert release.count("uses: astral-sh/setup-uv@") == 1
    assert release.count("uses: actions/attest@") == 2
    assert release.count("uses: actions/upload-artifact@") == 1
    assert release.count("gh release create") == 1
    assert release.count("gh release upload") == 1
    assert release.count("gh release edit") == 1
    assert "attestations: write" in release
    assert "contents: write" in release
    assert "id-token: write" in release
    assert 'tags:\n      - "v*"' in release
    assert "pull_request:" not in release
    assert "workflow_dispatch:" not in release
    assert "schedule:" not in release


def test_m45_changes_no_runtime_or_public_package_boundary() -> None:
    assert not any(
        "m45" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m45_docs_define_public_consumer_path_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0028-verify-public-release-consumer-path.md",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8").casefold()
        assert "m45" in text
        assert "public" in text

    rfc = paths[-1].read_text(encoding="utf-8")
    normalized = " ".join(rfc.split()).casefold()
    assert "**status:** accepted" in normalized
    assert "without a github credential" in normalized
    assert "does not" in normalized
    for term in (
        "independent",
        "future availability",
        "immutability",
        "supported release channel",
        "job",
        "runner",
        "action",
        "permission",
        "publication",
    ):
        assert term in normalized
