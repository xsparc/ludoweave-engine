"""Protect M48 public release HTTP response and failure conformance."""

from __future__ import annotations

import hashlib
import http.client
import importlib.util
import ssl
import sys
from collections.abc import Mapping
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
        block = self._body[self._offset : self._offset + amount]
        self._offset += len(block)
        return block

    def close(self) -> None:
        return None


class _Socket:
    def __init__(self, context: ssl.SSLContext, server_hostname: str = "api.github.com") -> None:
        self.timeouts: list[float] = []
        self.context = context
        self.server_side = False
        self.server_hostname = server_hostname

    def settimeout(self, value: float) -> None:
        self.timeouts.append(value)

    def getpeername(self) -> tuple[str, int]:
        return ("8.8.8.8", 443)

    def getpeercert(self, *, binary_form: bool = False) -> bytes:
        assert binary_form
        return b"verified-leaf-certificate"

    def version(self) -> str:
        return "TLSv1.3"

    def cipher(self) -> tuple[str, str, int]:
        return ("TLS_AES_256_GCM_SHA384", "TLSv1.3", 256)

    def compression(self) -> None:
        return None

    def selected_alpn_protocol(self) -> str:
        return "http/1.1"


def _load() -> tuple[ModuleType, _Download, type[Exception]]:
    spec = importlib.util.spec_from_file_location("m48_public_release_verifier", _VERIFIER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    scripts = str(_ROOT / "scripts")
    sys.path.insert(0, scripts)
    try:
        spec.loader.exec_module(module)
    finally:
        sys.path.remove(scripts)
    return (
        module,
        cast(_Download, module._download),
        cast(type[Exception], module.PublicReleaseVerificationError),
    )


@pytest.mark.parametrize("status", (301, 302, 303, 304, 307, 308))
def test_release_document_requires_direct_200_response(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    status: int,
) -> None:
    _, download, error_type = _load()
    requests = 0

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.sock = _Socket(cast(ssl.SSLContext, _kwargs["context"]))

        def request(self, *_args: object, **_kwargs: object) -> None:
            nonlocal requests
            requests += 1

        def getresponse(self) -> _Response:
            return _Response(status, b"", {"Location": "https://objects.example.test/release"})

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/123",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )
    assert cast(_CodedError, raised.value).code == "public_release.redirect_failed"
    assert requests == 1


def test_release_document_and_asset_accept_direct_200(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, _ = _load()
    responses = [
        _Response(200, b"{}", {"Content-Length": "2"}),
        _Response(200, b"asset", {"Content-Length": "5"}),
    ]

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.sock = _Socket(cast(ssl.SSLContext, _kwargs["context"]))

        def request(self, *_args: object, **_kwargs: object) -> None:
            return None

        def getresponse(self) -> _Response:
            return responses.pop(0)

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    document = tmp_path / "release.json"
    asset = tmp_path / "asset.bin"
    download(
        "https://api.github.com/repos/xsparc/ludoweave-engine/releases/123",
        document,
        accept="application/vnd.github+json",
        maximum_bytes=100,
        maximum_redirects=0,
    )
    download(
        "https://api.github.com/repos/xsparc/ludoweave-engine/releases/assets/456",
        asset,
        accept="application/octet-stream",
        maximum_bytes=5,
        maximum_redirects=3,
        expected_bytes=5,
        partial_name=".asset-456.part",
    )

    assert document.read_bytes() == b"{}"
    assert asset.read_bytes() == b"asset"


def test_asset_accepts_302_then_200_and_minimizes_redirect_headers(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, _ = _load()
    responses = [
        _Response(302, b"", {"Location": "https://objects.example.test/asset"}),
        _Response(200, b"asset", {"Content-Length": "5"}),
    ]
    requests: list[tuple[str, Mapping[str, str]]] = []

    class FakeConnection:
        def __init__(self, host: str, *_args: object, **_kwargs: object) -> None:
            self.host = host
            self.sock = _Socket(cast(ssl.SSLContext, _kwargs["context"]), host)

        def request(self, _method: str, _path: str, *, headers: Mapping[str, str]) -> None:
            requests.append((self.host, dict(headers)))

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
        maximum_redirects=3,
        expected_bytes=5,
        partial_name=".asset-456.part",
    )

    assert target.read_bytes() == b"asset"
    assert [host for host, _ in requests] == ["api.github.com", "objects.example.test"]
    assert requests[0][1]["X-GitHub-Api-Version"] == "2026-03-10"
    assert "X-GitHub-Api-Version" not in requests[1][1]
    assert all(
        "Authorization" not in headers and "Cookie" not in headers for _, headers in requests
    )


@pytest.mark.parametrize("status", (301, 303, 304, 307, 308))
def test_asset_rejects_undocumented_redirect_status(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    status: int,
) -> None:
    _, download, error_type = _load()

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.sock = _Socket(cast(ssl.SSLContext, _kwargs["context"]))

        def request(self, *_args: object, **_kwargs: object) -> None:
            return None

        def getresponse(self) -> _Response:
            return _Response(status, b"", {"Location": "https://objects.example.test/asset"})

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/assets/456",
            tmp_path / "asset.bin",
            accept="application/octet-stream",
            maximum_bytes=5,
            maximum_redirects=3,
            expected_bytes=5,
            partial_name=".asset-456.part",
        )
    assert cast(_CodedError, raised.value).code == "public_release.redirect_failed"


@pytest.mark.parametrize("phase", ("request", "response"))
def test_request_and_response_header_timeouts_share_timeout_code(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    phase: str,
) -> None:
    _, download, error_type = _load()

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.sock = _Socket(cast(ssl.SSLContext, _kwargs["context"]))

        def request(self, *_args: object, **_kwargs: object) -> None:
            if phase == "request":
                raise TimeoutError

        def getresponse(self) -> _Response:
            if phase == "response":
                raise TimeoutError
            return _Response(200, b"{}", {})

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/123",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )
    assert cast(_CodedError, raised.value).code == "public_release.request_timeout"


def test_socket_timeout_update_failure_uses_timeout_code(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()

    class TimeoutSocket:
        def getpeername(self) -> tuple[str, int]:
            return ("8.8.8.8", 443)

        def settimeout(self, _value: float) -> None:
            raise TimeoutError

        def version(self) -> str:
            return "TLSv1.3"

        def cipher(self) -> tuple[str, str, int]:
            return ("TLS_AES_256_GCM_SHA384", "TLSv1.3", 256)

        def compression(self) -> None:
            return None

        def selected_alpn_protocol(self) -> str:
            return "http/1.1"

    class FakeConnection:
        sock = TimeoutSocket()

        def __init__(self, *_args: object, **_kwargs: object) -> None:
            return None

        def request(self, *_args: object, **_kwargs: object) -> None:
            return None

        def getresponse(self) -> _Response:
            raise AssertionError("response headers must not be read after timeout")

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/123",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )
    assert cast(_CodedError, raised.value).code == "public_release.request_timeout"


@pytest.mark.parametrize("failure", (ConnectionResetError(), http.client.IncompleteRead(b"")))
def test_response_body_transport_failure_is_not_misreported_as_output_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: BaseException,
) -> None:
    _, download, error_type = _load()

    class BrokenResponse(_Response):
        def read(self, amount: int = -1) -> bytes:
            del amount
            raise failure

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.sock = _Socket(cast(ssl.SSLContext, _kwargs["context"]))

        def request(self, *_args: object, **_kwargs: object) -> None:
            return None

        def getresponse(self) -> _Response:
            return BrokenResponse(200, b"", {})

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/123",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )
    assert cast(_CodedError, raised.value).code == "public_release.request_failed"


def test_local_target_creation_failure_remains_output_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.sock = _Socket(cast(ssl.SSLContext, _kwargs["context"]))

        def request(self, *_args: object, **_kwargs: object) -> None:
            return None

        def getresponse(self) -> _Response:
            return _Response(200, b"{}", {})

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/123",
            tmp_path / "missing" / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )
    assert cast(_CodedError, raised.value).code == "public_release.output_failed"


def test_m48_changes_no_workflow_runtime_dependency_or_package_boundary() -> None:
    assert hashlib.sha256(
        (_ROOT / ".github" / "workflows" / "ci.yml").read_bytes()
    ).hexdigest() == (_CI_SHA256)
    assert (
        hashlib.sha256((_ROOT / ".github" / "workflows" / "release.yml").read_bytes()).hexdigest()
        == _RELEASE_SHA256
    )
    assert hashlib.sha256((_ROOT / "pyproject.toml").read_bytes()).hexdigest() == (
        _PYPROJECT_SHA256
    )
    assert hashlib.sha256((_ROOT / "uv.lock").read_bytes()).hexdigest() == _LOCK_SHA256
    source = _VERIFIER.read_text(encoding="utf-8")
    assert "import requests" not in source
    assert "urllib.request" not in source
    assert "subprocess" not in source


def test_m48_docs_define_response_scope_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0031-public-release-http-response-conformance.md",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8").casefold()
        assert "m48" in text
        assert "response" in text

    normalized = " ".join(paths[-1].read_text(encoding="utf-8").split()).casefold()
    for term in (
        "**status:** accepted",
        "200",
        "302",
        "timeout",
        "transport",
        "same workflow",
        "no release mutation",
        "supported release channel",
    ):
        assert term in normalized
