"""Protect M51 public release negotiated TLS-session conformance."""

from __future__ import annotations

import hashlib
import http.client
import importlib.util
import ssl
import sys
from collections.abc import Callable, Mapping
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
    version = 11

    status = 200

    def __init__(self, body: bytes, *, location: str | None = None) -> None:
        self._body = body
        self._offset = 0
        self._location = location

    def getheader(self, name: str) -> str | None:
        return self._location if name == "Location" else None

    def getheaders(self) -> list[tuple[str, str]]:
        return [] if self._location is None else [("Location", self._location)]

    def read(self, amount: int = -1) -> bytes:
        if amount < 0:
            amount = len(self._body) - self._offset
        block = self._body[self._offset : self._offset + amount]
        self._offset += len(block)
        return block

    def close(self) -> None:
        return None


class _RedirectResponse(_Response):
    status = 302


class _TlsSocket:
    def __init__(
        self,
        context: ssl.SSLContext,
        events: list[str],
        *,
        version: object = "TLSv1.3",
        cipher: object = ("TLS_AES_256_GCM_SHA384", "TLSv1.3", 256),
        compression: object = None,
        alpn: object = "http/1.1",
        server_hostname: object = "api.github.com",
    ) -> None:
        self.context = context
        self.server_side = False
        self.session_reused = False
        self.events = events
        self.server_hostname = server_hostname
        self.negotiated_version = version
        self.negotiated_cipher = cipher
        self.negotiated_compression = compression
        self.negotiated_alpn = alpn

    def getpeername(self) -> tuple[str, int]:
        self.events.append("peer")
        return ("8.8.8.8", 443)

    def settimeout(self, _value: float) -> None:
        return None

    def getpeercert(self, *, binary_form: bool = False) -> bytes:
        assert binary_form
        self.events.append("certificate")
        return b"verified-leaf-certificate"

    def version(self) -> object:
        self.events.append("version")
        return self.negotiated_version

    def cipher(self) -> object:
        self.events.append("cipher")
        return self.negotiated_cipher

    def compression(self) -> object:
        self.events.append("compression")
        return self.negotiated_compression

    def selected_alpn_protocol(self) -> object:
        self.events.append("alpn")
        return self.negotiated_alpn


def _load() -> tuple[ModuleType, _Download, type[Exception]]:
    spec = importlib.util.spec_from_file_location("m51_public_release_verifier", _VERIFIER)
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


def test_tls_context_advertises_only_http_1_1(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module, _, _ = _load()
    advertised: list[list[str]] = []

    class FakeContext:
        protocol = ssl.PROTOCOL_TLS_CLIENT
        verify_mode = ssl.CERT_REQUIRED
        check_hostname = True
        minimum_version = ssl.TLSVersion.TLSv1_2
        keylog_filename = None
        verify_flags = ssl.VERIFY_X509_PARTIAL_CHAIN | ssl.VERIFY_X509_STRICT

        def load_default_certs(self, purpose: ssl.Purpose) -> None:
            assert purpose == ssl.Purpose.SERVER_AUTH

        def set_alpn_protocols(self, protocols: list[str]) -> None:
            advertised.append(protocols)

    def fake_context(protocol: object) -> ssl.SSLContext:
        assert protocol == ssl.PROTOCOL_TLS_CLIENT
        return cast(ssl.SSLContext, FakeContext())

    monkeypatch.setattr(module.ssl, "SSLContext", fake_context)
    context_factory = cast(Callable[[], ssl.SSLContext], module._public_tls_context)

    context_factory()

    assert advertised == [["http/1.1"]]


@pytest.mark.parametrize(
    ("version", "cipher", "alpn"),
    (
        ("TLSv1.2", ("ECDHE-RSA-AES128-GCM-SHA256", "TLSv1.2", 128), None),
        ("TLSv1.2", ("ECDHE-RSA-AES256-GCM-SHA384", "TLSv1.2", 256), "http/1.1"),
        ("TLSv1.3", ("TLS_AES_128_GCM_SHA256", "TLSv1.3", 128), None),
        ("TLSv1.3", ("TLS_AES_256_GCM_SHA384", "TLSv1.3", 256), "http/1.1"),
    ),
)
def test_conforming_tls_session_is_checked_before_request(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    version: str,
    cipher: tuple[str, str, int],
    alpn: str | None,
) -> None:
    _, download, _ = _load()
    events: list[str] = []

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.context = cast(ssl.SSLContext, _kwargs["context"])
            self.sock: _TlsSocket | None = None

        def connect(self) -> None:
            events.append("connect")
            self.sock = _TlsSocket(
                self.context,
                events,
                version=version,
                cipher=cipher,
                alpn=alpn,
            )

        def request(
            self,
            method: str,
            path: str,
            *,
            headers: Mapping[str, str],
        ) -> None:
            del headers
            events.append(f"request:{method}:{path}")

        def getresponse(self) -> _Response:
            return _Response(b"{}")

        def close(self) -> None:
            events.append("close")

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    target = tmp_path / "release.json"
    download(
        "https://api.github.com/repos/xsparc/ludoweave-engine/releases/123",
        target,
        accept="application/vnd.github+json",
        maximum_bytes=100,
        maximum_redirects=0,
    )

    assert target.read_bytes() == b"{}"
    assert events == [
        "connect",
        "peer",
        "certificate",
        "version",
        "cipher",
        "compression",
        "alpn",
        "request:GET:/repos/xsparc/ludoweave-engine/releases/123",
        "close",
    ]


@pytest.mark.parametrize(
    ("overrides", "description"),
    (
        ({"version": None}, "missing protocol"),
        ({"version": []}, "unhashable sequence protocol"),
        ({"version": {}}, "unhashable mapping protocol"),
        ({"version": "TLSv1.1"}, "old protocol"),
        ({"version": "TLSv1.4"}, "unknown protocol"),
        ({"cipher": None}, "missing cipher"),
        ({"cipher": ("", "TLSv1.3", 256)}, "empty cipher name"),
        ({"cipher": ("TLS_AES_256_GCM_SHA384", "", 256)}, "empty cipher protocol"),
        ({"cipher": ("TLS_AES_128_GCM_SHA256", "TLSv1.3", True)}, "boolean bits"),
        ({"cipher": ("TLS_AES_128_GCM_SHA256", "TLSv1.3", 127)}, "weak cipher"),
        ({"compression": "DEFLATE"}, "TLS compression"),
        ({"alpn": "h2"}, "unsupported ALPN"),
    ),
)
def test_nonconforming_tls_session_fails_before_request(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    overrides: dict[str, object],
    description: str,
) -> None:
    del description
    _, download, error_type = _load()
    events: list[str] = []

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            context = cast(ssl.SSLContext, _kwargs["context"])
            self.sock = _TlsSocket(context, events, **overrides)

        def request(self, *_args: object, **_kwargs: object) -> None:
            events.append("request")

        def close(self) -> None:
            events.append("close")

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/123",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )

    assert cast(_CodedError, raised.value).code == "public_release.tls_failed"
    assert "request" not in events
    assert events[-1] == "close"
    assert "api.github.com" not in str(raised.value)


def test_missing_tls_session_accessor_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()
    requests = 0

    class IncompleteSocket:
        def __init__(self, context: ssl.SSLContext) -> None:
            self.context = context
            self.server_side = False
            self.session_reused = False
            self.server_hostname = "api.github.com"

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

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.sock = IncompleteSocket(cast(ssl.SSLContext, _kwargs["context"]))

        def request(self, *_args: object, **_kwargs: object) -> None:
            nonlocal requests
            requests += 1

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

    assert cast(_CodedError, raised.value).code == "public_release.tls_failed"
    assert requests == 0


def test_redirect_revalidates_an_independent_tls_session(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, _ = _load()
    events: list[str] = []
    responses = iter(
        (
            _RedirectResponse(b"", location="https://objects.example.test/asset"),
            _Response(b"asset"),
        )
    )

    class FakeConnection:
        def __init__(self, host: str, *_args: object, **_kwargs: object) -> None:
            self.host = host
            context = cast(ssl.SSLContext, _kwargs["context"])
            self.sock = _TlsSocket(context, events, server_hostname=host)

        def request(self, *_args: object, **_kwargs: object) -> None:
            events.append(f"request:{self.host}")

        def getresponse(self) -> _Response:
            return next(responses)

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
    assert events.count("version") == 2
    assert events.count("cipher") == 2
    assert events.count("compression") == 2
    assert events.count("alpn") == 2
    assert [event for event in events if event.startswith("request:")] == [
        "request:api.github.com",
        "request:objects.example.test",
    ]


def test_m51_changes_no_workflow_runtime_dependency_or_package_boundary() -> None:
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
    assert "context.set_alpn_protocols([_HTTP_ALPN])" in source
    assert "peer.version()" in source
    assert "peer.cipher()" in source
    assert "peer.compression()" in source
    assert "peer.selected_alpn_protocol()" in source
    assert source.index("_validate_tls_session(connection)") < source.index(
        'connection.request(\n                "GET",'
    )


def test_m51_public_and_maintainer_docs_define_the_exact_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0034-public-release-negotiated-tls-session-conformance.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").lower() for path in paths)
    combined = "\n".join(documents)

    assert all("m51" in document for document in documents)
    for term in (
        "actual negotiated",
        "tlsv1.2",
        "tlsv1.3",
        "128",
        "compression",
        "http/1.1",
        "cipher-name allowlist",
        "before",
        "no workflow",
        "not a real public release observation",
    ):
        assert term in combined
