"""Protect M55 public release HTTP response-framing conformance."""

from __future__ import annotations

import hashlib
import http.client
import importlib.util
import io
import socket
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
    status = 200

    def __init__(
        self,
        body: bytes = b"{}",
        *,
        version: object = 11,
        headers: Mapping[str, object] | None = None,
        events: list[str] | None = None,
    ) -> None:
        self.body = body
        self._version = version
        self.headers = {} if headers is None else dict(headers)
        self.events = [] if events is None else events
        self.offset = 0

    @property
    def version(self) -> object:
        self.events.append("version")
        return self._version

    def getheader(self, name: str) -> object:
        self.events.append(f"header:{name}")
        return self.headers.get(name)

    def read(self, amount: int = -1) -> bytes:
        self.events.append("read")
        if amount < 0:
            amount = len(self.body) - self.offset
        chunk = self.body[self.offset : self.offset + amount]
        self.offset += len(chunk)
        return chunk

    def close(self) -> None:
        self.events.append("response-close")


class _RedirectResponse(_Response):
    status = 302


class _Socket:
    def __init__(self, context: ssl.SSLContext, host: str) -> None:
        self.context = context
        self.server_side = False
        self.session_reused = False
        self.server_hostname = host

    def getpeername(self) -> tuple[str, int]:
        return ("8.8.8.8", 443)

    def settimeout(self, _value: float) -> None:
        return None

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
    spec = importlib.util.spec_from_file_location("m55_public_release_verifier", _VERIFIER)
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


def _install_response(
    monkeypatch: pytest.MonkeyPatch,
    response: _Response,
    events: list[str],
) -> None:
    class FakeConnection:
        def __init__(self, host: str, *_args: object, **kwargs: object) -> None:
            self.sock = _Socket(cast(ssl.SSLContext, kwargs["context"]), host)

        def request(self, *_args: object, **_kwargs: object) -> None:
            events.append("request")

        def getresponse(self) -> _Response:
            events.append("response")
            return response

        def close(self) -> None:
            events.append("connection-close")

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)


@pytest.mark.parametrize(
    "headers",
    (
        {"Content-Length": "2"},
        {"Transfer-Encoding": "chunked"},
        {"Transfer-Encoding": "CHUNKED"},
        {},
    ),
)
def test_version_11_accepted_framing_streams_decoded_bounded_body(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    headers: Mapping[str, object],
) -> None:
    _, download, _ = _load()
    events: list[str] = []
    response = _Response(headers=headers, events=events)
    _install_response(monkeypatch, response, events)

    target = tmp_path / "release.json"
    download(
        "https://api.github.com/repos/xsparc/ludoweave-engine/releases/123",
        target,
        accept="application/vnd.github+json",
        maximum_bytes=100,
        maximum_redirects=0,
    )

    assert target.read_bytes() == b"{}"
    assert events[:5] == [
        "request",
        "response",
        "version",
        "header:Transfer-Encoding",
        "header:Content-Length",
    ]
    assert "read" in events
    assert events[-2:] == ["response-close", "connection-close"]


def test_cpython_version_11_bucket_is_not_exact_status_line_evidence() -> None:
    class RawSocket:
        def makefile(self, _mode: str) -> io.BytesIO:
            return io.BytesIO(b"HTTP/1.9 200 OK\r\nContent-Length: 0\r\n\r\n")

    response = http.client.HTTPResponse(cast(socket.socket, RawSocket()))
    response.begin()

    assert response.version == 11


@pytest.mark.parametrize("version", (10, 9, 20, True, None, "11"))
def test_non_version_11_value_fails_before_status_or_body_use(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    version: object,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []
    response = _Response(version=version, headers={"Content-Length": "2"}, events=events)
    _install_response(monkeypatch, response, events)

    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/release",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert str(version) not in str(raised.value)
    assert "read" not in events
    assert events[-2:] == ["response-close", "connection-close"]


@pytest.mark.parametrize(
    "transfer_encoding",
    ("", "gzip", "gzip, chunked", "chunked, chunked", 1, ["chunked"]),
)
def test_unsupported_or_malformed_transfer_encoding_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    transfer_encoding: object,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []
    response = _Response(
        headers={"Transfer-Encoding": transfer_encoding},
        events=events,
    )
    _install_response(monkeypatch, response, events)

    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/release",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert "read" not in events


def test_transfer_encoding_and_content_length_conflict_fails_before_body(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []
    response = _Response(
        headers={"Transfer-Encoding": "chunked", "Content-Length": "2"},
        events=events,
    )
    _install_response(monkeypatch, response, events)

    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/release",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert "read" not in events


@pytest.mark.parametrize("content_length", (2, True, [], {}))
def test_non_string_content_length_fails_as_framing_error(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    content_length: object,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []
    response = _Response(headers={"Content-Length": content_length}, events=events)
    _install_response(monkeypatch, response, events)

    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/release",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert "read" not in events


def test_joined_duplicate_content_lengths_retain_size_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []
    response = _Response(headers={"Content-Length": "2, 2"}, events=events)
    _install_response(monkeypatch, response, events)

    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/release",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )

    assert cast(_CodedError, raised.value).code == "public_release.size_mismatch"
    assert "read" not in events


@pytest.mark.parametrize(
    "failure",
    (
        AttributeError(),
        http.client.HTTPException(),
        NotImplementedError(),
        OSError(),
        TypeError(),
        ValueError(),
    ),
)
def test_framing_inspection_failure_is_stable_chained_and_content_silent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: Exception,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []

    class FailingResponse(_Response):
        @property
        def version(self) -> object:
            raise failure

    response = FailingResponse(events=events)
    _install_response(monkeypatch, response, events)
    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/release",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert raised.value.__cause__ is failure
    assert "api.github.com" not in str(raised.value)


def test_redirect_revalidates_framing_before_using_second_response(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()
    responses = iter(
        (
            _RedirectResponse(
                headers={"Location": "https://objects.example.test/asset"},
            ),
            _Response(body=b"asset", version=10),
        )
    )
    requests: list[str] = []

    class FakeConnection:
        def __init__(self, host: str, *_args: object, **kwargs: object) -> None:
            self.host = host
            self.sock = _Socket(cast(ssl.SSLContext, kwargs["context"]), host)

        def request(self, *_args: object, **_kwargs: object) -> None:
            requests.append(self.host)

        def getresponse(self) -> _Response:
            return next(responses)

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

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert requests == ["api.github.com", "objects.example.test"]
    assert not (tmp_path / ".asset-456.part").exists()


def test_m55_changes_no_workflow_runtime_dependency_or_package_boundary() -> None:
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
    source = _VERIFIER.read_text(encoding="utf-8")
    response = source.index("response = connection.getresponse()")
    framing = source.index("_validate_http_response_framing(response)")
    status = source.index("if response.status == 302:")
    stream = source.index("received = _stream_response(")
    assert response < framing < status < stream
    assert 'response.getheader("Transfer-Encoding")' in source
    assert 'transfer_encoding.casefold() != "chunked"' in source
    assert "version != 11" in source
    for term in ("response.chunked", "response.length", "response.will_close"):
        assert term not in source


def test_m55_public_and_maintainer_docs_define_the_exact_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0038-public-release-http-response-framing.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").lower() for path in paths)
    combined = "\n".join(documents)

    assert all("m55" in document for document in documents)
    for term in (
        "http/1.1",
        "status-line token",
        "transfer-encoding",
        "content-length",
        "chunked",
        "every redirect",
        "no workflow",
        "not a real public release observation",
    ):
        assert term in combined
