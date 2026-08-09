"""Protect M47 portable cross-platform public release consumer rehearsal."""

from __future__ import annotations

import hashlib
import http.client
import importlib.util
import json
import ssl
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from types import ModuleType
from typing import Protocol, cast

import pytest

_ROOT = Path(__file__).parents[2]
_CI = _ROOT / ".github" / "workflows" / "ci.yml"
_RELEASE = _ROOT / ".github" / "workflows" / "release.yml"
_VERIFIER = _ROOT / "scripts" / "verify_public_release.py"
_CI_SHA256 = "258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946"
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
        expected_bytes: int | None = None,
        partial_name: str | None = None,
    ) -> None: ...


class _SmokeMain(Protocol):
    def __call__(self, argv: Sequence[str] | None = None) -> int: ...


class _SmokeModule(Protocol):
    main: _SmokeMain


class _PublishPartial(Protocol):
    def __call__(self, partial: Path, target: Path) -> None: ...


class _AssetPlan(Protocol):
    def __call__(self, path: Path) -> tuple[object, ...]: ...


class _Remaining(Protocol):
    def __call__(self, deadline: float) -> float: ...


class _Response:
    def __init__(self, status: int, body: bytes, headers: Mapping[str, str]) -> None:
        self.status = status
        self._body = body
        self._headers = dict(headers)
        self._offset = 0

    def getheader(self, name: str) -> str | None:
        return self._headers.get(name)

    def read(self, amount: int = -1) -> bytes:
        if amount < 0:
            amount = len(self._body) - self._offset
        result = self._body[self._offset : self._offset + amount]
        self._offset += len(result)
        return result

    def close(self) -> None:
        return None


class _Socket:
    def __init__(self) -> None:
        self.timeouts: list[float] = []

    def settimeout(self, value: float) -> None:
        self.timeouts.append(value)


def _load() -> tuple[ModuleType, _Main, _Download]:
    spec = importlib.util.spec_from_file_location("m47_public_release_verifier", _VERIFIER)
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


def _release_fixture(tmp_path: Path) -> tuple[Path, Path, dict[int, bytes]]:
    expected = tmp_path / "expected"
    expected.mkdir()
    notes = b"# Release notes\n\nExact notes.\n"
    asset = b"asset"
    (expected / "RELEASE_NOTES.md").write_bytes(notes)
    (expected / "asset.bin").write_bytes(asset)
    identities = ((457, "RELEASE_NOTES.md", notes), (456, "asset.bin", asset))
    document = tmp_path / "fixture-public.json"
    document.write_text(
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
                        "name": name,
                        "size": len(content),
                        "digest": f"sha256:{hashlib.sha256(content).hexdigest()}",
                        "state": "uploaded",
                    }
                    for asset_id, name, content in identities
                ],
            }
        ),
        encoding="utf-8",
    )
    return expected, document, {asset_id: content for asset_id, _, content in identities}


def _environment(runner: Path) -> dict[str, str]:
    return {
        "GITHUB_REF_NAME": "v0.1.0a1",
        "GITHUB_REPOSITORY": "xsparc/ludoweave-engine",
        "RELEASE_ID": "123",
        "RELEASE_TITLE": "LudoWeave 0.1.0a1",
        "RUNNER_TEMP": str(runner),
    }


def test_tag_rehearsal_uses_one_exact_three_os_matrix() -> None:
    workflow = _RELEASE.read_text(encoding="utf-8")
    consumer = workflow.split("  fresh-consumer:\n", 1)[1]

    assert "needs: release" in consumer
    assert "fail-fast: false" in consumer
    assert "runs-on: ${{ matrix.os }}" in consumer
    assert consumer.count("          - ubuntu-latest") == 1
    assert consumer.count("          - windows-latest") == 1
    assert consumer.count("          - macos-latest") == 1
    assert "Fresh public release consumer (${{ matrix.os }})" in consumer
    assert workflow.count("\n    runs-on:") == 2
    assert workflow.count("uses: actions/download-artifact@") == 1
    assert workflow.count("uses: actions/checkout@") == 2
    assert workflow.count("uses: astral-sh/setup-uv@") == 2
    assert "enable-cache: false" in consumer
    assert "permissions:\n      contents: read" in consumer
    assert "python scripts/verify_public_release.py .tmp/m47-expected-release" in consumer


def test_portable_verifier_creates_fresh_plan_and_smokes_exact_public_bytes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    module, main, _ = _load()
    expected, public_document, assets = _release_fixture(tmp_path)
    runner = tmp_path / "runner"
    runner.mkdir()
    requests: list[tuple[str, str]] = []

    def fake_download(
        url: str,
        target: Path,
        *,
        accept: str,
        maximum_bytes: int,
        expected_bytes: int | None = None,
        partial_name: str | None = None,
    ) -> None:
        del maximum_bytes, partial_name
        requests.append((url, accept))
        if url.endswith("/releases/123"):
            target.write_bytes(public_document.read_bytes())
            return
        asset_id = int(url.rsplit("/", 1)[1])
        content = assets[asset_id]
        assert expected_bytes == len(content)
        target.write_bytes(content)

    smoked: list[Path] = []

    def fake_smoke(argv: Sequence[str] | None = None) -> int:
        assert argv is not None and len(argv) == 1
        smoked.append(Path(argv[0]))
        return 0

    monkeypatch.setattr(module, "_download", fake_download)
    smoke = cast(_SmokeModule, module.smoke_release)
    monkeypatch.setattr(smoke, "main", fake_smoke)

    assert main([str(expected)], environment=_environment(runner)) == 0

    downloaded = runner / "release-public-download"
    assert (downloaded / "RELEASE_NOTES.md").read_bytes() == assets[457]
    assert (downloaded / "asset.bin").read_bytes() == assets[456]
    assert (runner / "release-assets.plan").is_file()
    assert smoked == [downloaded]
    assert requests == [
        (
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/123",
            "application/vnd.github+json",
        ),
        (
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/assets/457",
            "application/octet-stream",
        ),
        (
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/assets/456",
            "application/octet-stream",
        ),
    ]
    captured = capsys.readouterr()
    assert captured.err == ""
    assert len(captured.out.splitlines()) == 1
    report = json.loads(captured.out)
    assert report == {
        "assets": 2,
        "bytes": len(assets[457]) + len(assets[456]),
        "protocol": "ludoweave.public-release-consumer/1",
        "status": "pass",
    }


@pytest.mark.parametrize(
    ("change", "code"),
    (
        ({"GITHUB_REPOSITORY": "other/project"}, "public_release.invalid_repository"),
        ({"RELEASE_ID": "0"}, "public_release.invalid_identity"),
        ({"GH_TOKEN": "present"}, "public_release.credential_present"),
        ({"GITHUB_TOKEN": "present"}, "public_release.credential_present"),
    ),
)
def test_context_rejects_wrong_identity_or_public_request_credential(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    change: dict[str, str],
    code: str,
) -> None:
    _, main, _ = _load()
    expected = tmp_path / "expected"
    expected.mkdir()
    runner = tmp_path / "runner"
    runner.mkdir()
    environment = _environment(runner)
    environment.update(change)

    assert main([str(expected)], environment=environment) == 1
    report = json.loads(capsys.readouterr().err)
    assert report["code"] == code
    assert report["status"] == "fail"


def test_plan_modes_reject_missing_or_preexisting_plan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    _, main, _ = _load()
    expected = tmp_path / "expected"
    expected.mkdir()
    runner = tmp_path / "runner"
    runner.mkdir()
    environment = _environment(runner)

    assert main([str(expected), "--use-existing-plan"], environment=environment) == 1
    assert json.loads(capsys.readouterr().err)["code"] == "public_release.plan_unavailable"

    (runner / "release-assets.plan").write_text("occupied", encoding="utf-8")
    assert main([str(expected)], environment=environment) == 1
    assert json.loads(capsys.readouterr().err)["code"] == "public_release.plan_exists"


@pytest.mark.parametrize(
    "content",
    (
        "",
        "ludoweave.release-asset-retrieval-plan/1\n",
        "ludoweave.release-asset-retrieval-plan/1\n0\t5\tasset.bin\n",
        "ludoweave.release-asset-retrieval-plan/1\n9223372036854775808\t5\tasset.bin\n",
        "ludoweave.release-asset-retrieval-plan/1\n1\t268435457\tasset.bin\n",
        "ludoweave.release-asset-retrieval-plan/1\n1\t5\t../asset.bin\n",
        "ludoweave.release-asset-retrieval-plan/1\n1\t5\ta.bin\n1\t5\tb.bin\n",
        "ludoweave.release-asset-retrieval-plan/1\n1\t5\ta.bin\n2\t5\ta.bin\n",
        "ludoweave.release-asset-retrieval-plan/1\n"
        "1\t268435456\ta.bin\n2\t268435456\tb.bin\n3\t1\tc.bin\n",
    ),
)
def test_asset_plan_rejects_unbounded_unsafe_or_duplicate_records(
    tmp_path: Path,
    content: str,
) -> None:
    module, _, _ = _load()
    parse_plan = cast(_AssetPlan, module._asset_plan)
    error_type = cast(type[Exception], module.PublicReleaseVerificationError)
    plan = tmp_path / "release-assets.plan"
    plan.write_text(content, encoding="utf-8")

    with pytest.raises(error_type):
        parse_plan(plan)


def test_https_client_follows_at_most_three_remote_https_redirects(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, _, download = _load()
    responses = [
        _Response(302, b"", {"Location": "https://objects.example.test/asset"}),
        _Response(200, b"asset", {"Content-Length": "5"}),
    ]
    connections: list[tuple[str, int | None, float, _Socket]] = []
    requests: list[tuple[str, str, Mapping[str, str]]] = []

    class FakeConnection:
        def __init__(
            self,
            host: str,
            port: int | None,
            *,
            timeout: float,
            context: ssl.SSLContext,
        ) -> None:
            del context
            self.sock = _Socket()
            connections.append((host, port, timeout, self.sock))

        def request(self, method: str, path: str, *, headers: Mapping[str, str]) -> None:
            requests.append((method, path, headers))

        def getresponse(self) -> _Response:
            return responses.pop(0)

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    target = tmp_path / "asset.bin"
    download(
        "https://api.github.com/repos/xsparc/ludoweave-engine/releases/assets/456",
        target,
        accept="application/octet-stream",
        maximum_bytes=5,
        expected_bytes=5,
        partial_name=".asset-456.part",
    )

    assert target.read_bytes() == b"asset"
    assert [entry[0] for entry in connections] == ["api.github.com", "objects.example.test"]
    assert all(0 < entry[2] <= 10 for entry in connections)
    assert all(entry[3].timeouts and max(entry[3].timeouts) <= 10 for entry in connections[1:])
    assert [request[:2] for request in requests] == [
        ("GET", "/repos/xsparc/ludoweave-engine/releases/assets/456"),
        ("GET", "/asset"),
    ]
    assert all(
        "Authorization" not in headers and "Cookie" not in headers for _, _, headers in requests
    )


def test_https_client_rejects_fourth_redirect(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module, _, download = _load()
    responses = [
        _Response(302, b"", {"Location": f"https://objects.example.test/{index}"})
        for index in range(4)
    ]

    class FakeConnection:
        sock = _Socket()

        def __init__(self, *_args: object, **_kwargs: object) -> None:
            return None

        def request(self, *_args: object, **_kwargs: object) -> None:
            return None

        def getresponse(self) -> _Response:
            return responses.pop(0)

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    error_type = cast(type[Exception], module.PublicReleaseVerificationError)
    with pytest.raises(error_type, match="redirect"):
        download(
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/123",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
        )


def test_https_client_rejects_non_https_redirect(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module, _, download = _load()

    class FakeConnection:
        sock = _Socket()

        def __init__(self, *_args: object, **_kwargs: object) -> None:
            return None

        def request(self, *_args: object, **_kwargs: object) -> None:
            return None

        def getresponse(self) -> _Response:
            return _Response(302, b"", {"Location": "http://example.test/asset"})

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    error_type = cast(type[Exception], module.PublicReleaseVerificationError)
    with pytest.raises(error_type, match="HTTPS"):
        download(
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/123",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
        )


@pytest.mark.parametrize(
    ("body", "content_length", "maximum", "expected"),
    (
        (b"asset!", None, 5, 5),
        (b"asset", "6", 5, 5),
        (b"four", "4", 5, 5),
    ),
)
def test_https_client_rejects_declared_or_streamed_size_mismatch(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    body: bytes,
    content_length: str | None,
    maximum: int,
    expected: int,
) -> None:
    module, _, download = _load()
    headers = {} if content_length is None else {"Content-Length": content_length}

    class FakeConnection:
        sock = _Socket()

        def __init__(self, *_args: object, **_kwargs: object) -> None:
            return None

        def request(self, *_args: object, **_kwargs: object) -> None:
            return None

        def getresponse(self) -> _Response:
            return _Response(200, body, headers)

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    error_type = cast(type[Exception], module.PublicReleaseVerificationError)
    with pytest.raises(error_type, match=r"size|length"):
        download(
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/assets/456",
            tmp_path / "asset.bin",
            accept="application/octet-stream",
            maximum_bytes=maximum,
            expected_bytes=expected,
            partial_name=".asset-456.part",
        )
    assert not (tmp_path / "asset.bin").exists()


def test_request_deadline_fails_closed(monkeypatch: pytest.MonkeyPatch) -> None:
    module, _, _ = _load()
    remaining = cast(_Remaining, module._remaining)
    error_type = cast(type[Exception], module.PublicReleaseVerificationError)
    monkeypatch.setattr(module.time, "monotonic", lambda: 31.0)

    with pytest.raises(error_type, match="time limit"):
        remaining(30.0)


def test_socket_read_timeout_is_reported_as_request_timeout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module, _, download = _load()

    class TimeoutResponse(_Response):
        def read(self, amount: int = -1) -> bytes:
            del amount
            raise TimeoutError

    class FakeConnection:
        sock = _Socket()

        def __init__(self, *_args: object, **_kwargs: object) -> None:
            return None

        def request(self, *_args: object, **_kwargs: object) -> None:
            return None

        def getresponse(self) -> _Response:
            return TimeoutResponse(200, b"", {})

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    error_type = cast(type[Exception], module.PublicReleaseVerificationError)
    with pytest.raises(error_type, match="time limit"):
        download(
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/123",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
        )


def test_partial_finalization_never_clobbers_existing_target(tmp_path: Path) -> None:
    module, _, _ = _load()
    publish = cast(_PublishPartial, module._publish_partial)
    error_type = cast(type[Exception], module.PublicReleaseVerificationError)
    partial = tmp_path / ".asset-456.part"
    target = tmp_path / "asset.bin"
    partial.write_bytes(b"new")
    target.write_bytes(b"existing")

    with pytest.raises(error_type, match="already exists"):
        publish(partial, target)
    assert target.read_bytes() == b"existing"
    assert partial.read_bytes() == b"new"

    target.unlink()
    publish(partial, target)
    assert target.read_bytes() == b"new"
    assert not partial.exists()


def test_m47_changes_no_pr_ci_runtime_dependency_or_public_package_boundary() -> None:
    assert hashlib.sha256(_CI.read_bytes()).hexdigest() == _CI_SHA256
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == (
        _PYPROJECT_SHA256
    )
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    assert not (_ROOT / "scripts" / "verify_public_release.sh").exists()
    assert not any(
        "m47" in path.read_text(encoding="utf-8").casefold()
        for path in (_ROOT / "src" / "ludoweave").rglob("*.py")
    )


def test_m47_docs_define_cross_platform_scope_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0030-cross-platform-release-consumer-rehearsal.md",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8").casefold()
        assert "m47" in text
        assert "cross-platform" in text

    normalized = " ".join(paths[-1].read_text(encoding="utf-8").split()).casefold()
    for term in (
        "**status:** accepted",
        "ubuntu",
        "windows",
        "macos",
        "same workflow",
        "not independent",
        "external",
        "future availability",
        "supported release channel",
        "no release mutation",
    ):
        assert term in normalized
