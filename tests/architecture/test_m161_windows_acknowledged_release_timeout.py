"""Protect M161's test-only acknowledged-release timeout boundary."""

from __future__ import annotations

import hashlib
from pathlib import Path

_ROOT = Path(__file__).parents[2]
_PROTECTED_FILES = {
    ".github/workflows/ci.yml": "883674592dd8cfc7f2c292f379591f863c797fdb0cd65f2c0c83a47e232db686",
    ".github/workflows/release.yml": (
        "c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5"
    ),
    "docs/rfcs/0143-probe-windows-live-wait-timeout.md": (
        "ceaf61688edb81ae0baed5850915eb8e11647754c7519c99dc6f5a74d177ab9b"
    ),
    "docs/security/cache-cleanup-windows-live-wait-timeout-probe.md": (
        "a44c89ab47778780d9efd407ec36d0931eb5158bf66fe6e3ba3f488d51c80d01"
    ),
    "pyproject.toml": "f64730d1e8083e294e21b12b2ed876cf32975dd2b5bbc62c5feb33fe3cb95e3d",
    "tests/architecture/test_m160_windows_live_wait_timeout.py": (
        "559e9ee3412b9c3e519487b8027b094e923fcf95db5e6ffd8fc25d1945504bee"
    ),
    "tests/integration/test_windows_cache_cleanup_live_wait_timeout_probe.py": (
        "cc63d5528ad538bcfa7497b5a2cfc31fd53fbeb8eb648af6ce97773123ce5f5f"
    ),
    "uv.lock": "55e1a195ecb088547bfeecb5ee85f60f23af98a16859f2a5d7b08438991f2c18",
}
_PROTECTED_TREES = {
    "examples": "8ea46a667dd765fa61bfdd8a7e20bd95d1f86cf51fbf0ad2696a1b9be5b24a93",
    "scripts": "d31a8fad25034053383e645c74725dec5744f474d86aa8b6c3936c51c19053e2",
    "src/ludoweave": "e6c951393b86b0673a25e0f6b1f4cf41224d3cb7807dd85c76aad482820cde36",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _tree_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    for candidate in sorted(
        path.rglob("*"),
        key=lambda item: (tuple(part.casefold() for part in item.parts), item.parts),
    ):
        if (
            candidate.is_file()
            and "__pycache__" not in candidate.parts
            and candidate.suffix != ".pyc"
        ):
            digest.update(candidate.relative_to(path).as_posix().encode())
            digest.update(b"\0")
            digest.update(candidate.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def test_m161_changes_no_runtime_example_script_dependency_ci_or_m160_boundary() -> None:
    assert {path: _sha256(_ROOT / path) for path in _PROTECTED_FILES} == _PROTECTED_FILES
    assert {path: _tree_sha256(_ROOT / path) for path in _PROTECTED_TREES} == _PROTECTED_TREES


def test_m161_fixture_holds_handle_between_release_and_close_tokens() -> None:
    fixture = (
        _ROOT / "tests/fixtures/windows_share_delete_acknowledged_release_child.py"
    ).read_text(encoding="utf-8")
    for required in (
        '_SCHEMA = "ludoweave.test.windows-acknowledged-release-blocker/1"',
        '_RELEASE_TOKEN = b"!"',
        '_CLOSE_TOKEN = b"."',
        '_emit("ready")',
        "sys.stdin.buffer.read(1) != _RELEASE_TOKEN",
        '_emit("release-held")',
        "sys.stdin.buffer.read(1) != _CLOSE_TOKEN",
        "close_handle(wintypes.HANDLE(handle))",
        '_emit("closed")',
    ):
        assert required in fixture
    release_index = fixture.index('_emit("release-held")')
    close_token_index = fixture.index("sys.stdin.buffer.read(1) != _CLOSE_TOKEN")
    close_handle_index = fixture.index("close_handle(wintypes.HANDLE(handle))")
    closed_index = fixture.index('_emit("closed")')
    assert release_index < close_token_index < close_handle_index < closed_index
    assert fixture.count("close_handle(wintypes.HANDLE(handle))") == 1
    assert "time.sleep" not in fixture


def test_m161_probe_orders_acknowledged_hold_timeout_before_close() -> None:
    probe = (
        _ROOT / "tests/integration/test_windows_cache_cleanup_acknowledged_release_timeout_probe.py"
    ).read_text(encoding="utf-8")
    for required in (
        '(sys.executable, "-I", "-B", str(_CHILD))',
        "close_fds=True",
        "cwd=tmp_path",
        "shell=False",
        "stdin=subprocess.PIPE",
        "stdout=subprocess.PIPE",
        "stderr=subprocess.PIPE",
        'assert _read_phase(blocker) == "ready"',
        "except queue.Empty:",
        "process.kill()",
        "process.wait(timeout=_TIMEOUT_SECONDS)",
        "reader.join(timeout=_TIMEOUT_SECONDS)",
        "stdin.write(_RELEASE_TOKEN)",
        'assert _read_phase(blocker) == "release-held"',
        "pytest.raises(subprocess.TimeoutExpired)",
        "blocker.wait(timeout=_IMMEDIATE_WAIT_SECONDS)",
        "raised.value.cmd == blocker.args",
        "raised.value.timeout == _IMMEDIATE_WAIT_SECONDS",
        "blocker.returncode is None",
        "stdin.write(_CLOSE_TOKEN)",
        'assert _read_phase(blocker) == "closed"',
        "blocker.wait(timeout=_TIMEOUT_SECONDS) == 0",
        "_ERROR_SHARING_VIOLATION",
        "succeeded=False",
        "succeeded=True",
    ):
        assert required in probe
    rename_call = "_attempt_native_child_rename(tmp_path)"
    rename_indexes: list[int] = []
    next_index = 0
    for _ in range(3):
        next_index = probe.index(rename_call, next_index)
        rename_indexes.append(next_index)
        next_index += len(rename_call)
    release_index = probe.index("stdin.write(_RELEASE_TOKEN)")
    held_index = probe.index('assert _read_phase(blocker) == "release-held"')
    wait_index = probe.index("blocker.wait(timeout=_IMMEDIATE_WAIT_SECONDS)")
    close_index = probe.index("stdin.write(_CLOSE_TOKEN)")
    closed_index = probe.index('assert _read_phase(blocker) == "closed"')
    assert rename_indexes[0] < release_index < held_index < wait_index < rename_indexes[1]
    assert rename_indexes[1] < close_index < closed_index < rename_indexes[2]
    assert probe.count(rename_call) == 3
    assert probe.count("blocker.wait(timeout=_IMMEDIATE_WAIT_SECONDS)") == 1
    assert "blocker.kill()" not in probe
    assert "communicate(" not in probe
    assert '"-c"' not in probe
    assert "time.sleep" not in probe


def test_m161_documents_narrow_acknowledged_release_evidence() -> None:
    decision = (
        _ROOT / "docs/security/cache-cleanup-windows-acknowledged-release-timeout-probe.md"
    ).read_text(encoding="utf-8")
    compact = " ".join(decision.casefold().split())
    for required in (
        "windows is not admitted",
        "test-only",
        "acknowledged release intent",
        "not a graceful-close timeout contract",
        "no hosted check is added",
    ):
        assert required in compact


def test_m161_rfc_and_public_boundary_are_registered() -> None:
    rfc = (_ROOT / "docs/rfcs/0144-probe-windows-acknowledged-release-timeout.md").read_text(
        encoding="utf-8"
    )
    assert "**Status:** Accepted" in rfc
    assert "windows is not admitted" in " ".join(rfc.casefold().split())
    for path in (
        "docs/readme-history.md",
        "CHANGELOG.md",
        "ROADMAP.md",
        "SECURITY.md",
        "docs/architecture.md",
        "docs/index.md",
        "mkdocs.yml",
    ):
        content = (_ROOT / path).read_text(encoding="utf-8")
        assert "cache-cleanup-windows-acknowledged-release-timeout-probe" in content
    rfc_index = (_ROOT / "docs/rfcs/index.md").read_text(encoding="utf-8")
    assert "0144-probe-windows-acknowledged-release-timeout.md" in rfc_index
