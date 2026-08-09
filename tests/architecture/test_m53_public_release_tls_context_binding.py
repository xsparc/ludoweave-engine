"""Protect M53 public release TLS context binding."""

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
    version = 11

    status = 200

    def __init__(self, body: bytes = b"{}", *, location: str | None = None) -> None:
        self.body = body
        self.location = location
        self.offset = 0

    def getheader(self, name: str) -> str | None:
        if name == "Location":
            return self.location
        if name == "Content-Length":
            return str(len(self.body))
        return None

    def read(self, amount: int = -1) -> bytes:
        if amount < 0:
            amount = len(self.body) - self.offset
        chunk = self.body[self.offset : self.offset + amount]
        self.offset += len(chunk)
        return chunk

    def close(self) -> None:
        return None


class _RedirectResponse(_Response):
    status = 302


class _BoundSocket:
    def __init__(
        self,
        context: object,
        events: list[str],
        *,
        server_side: object = False,
        server_hostname: str = "api.github.com",
    ) -> None:
        self._context = context
        self._server_side = server_side
        self.session_reused = False
        self.events = events
        self.server_hostname = server_hostname

    @property
    def context(self) -> object:
        self.events.append("context")
        return self._context

    @property
    def server_side(self) -> object:
        self.events.append("server-side")
        return self._server_side

    def getpeername(self) -> tuple[str, int]:
        self.events.append("peer")
        return ("8.8.8.8", 443)

    def settimeout(self, _value: float) -> None:
        return None

    def getpeercert(self, *, binary_form: bool = False) -> bytes:
        assert binary_form
        self.events.append("certificate")
        return b"verified-leaf-certificate"

    def version(self) -> str:
        self.events.append("version")
        return "TLSv1.3"

    def cipher(self) -> tuple[str, str, int]:
        self.events.append("cipher")
        return ("TLS_AES_256_GCM_SHA384", "TLSv1.3", 256)

    def compression(self) -> None:
        self.events.append("compression")
        return None

    def selected_alpn_protocol(self) -> str:
        self.events.append("alpn")
        return "http/1.1"


def _load() -> tuple[ModuleType, _Download, type[Exception]]:
    spec = importlib.util.spec_from_file_location("m53_public_release_verifier", _VERIFIER)
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


def test_exact_client_context_binding_precedes_identity_session_and_request(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, _ = _load()
    events: list[str] = []
    contexts: list[ssl.SSLContext] = []

    class FakeConnection:
        def __init__(
            self,
            host: str,
            _port: int | None,
            *,
            timeout: float,
            context: ssl.SSLContext,
        ) -> None:
            assert host == "api.github.com"
            assert timeout > 0
            contexts.append(context)
            self.context = context
            self.sock: _BoundSocket | None = None

        def connect(self) -> None:
            events.append("connect")
            self.sock = _BoundSocket(self.context, events)

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
            return _Response()

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
    assert len(contexts) == 1
    assert events == [
        "connect",
        "peer",
        "context",
        "server-side",
        "certificate",
        "version",
        "cipher",
        "compression",
        "alpn",
        "request:GET:/repos/xsparc/ludoweave-engine/releases/123",
        "close",
    ]


@pytest.mark.parametrize("server_side", (True, None, 0, "false"))
def test_non_client_socket_role_fails_before_identity_or_request(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    server_side: object,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []

    class FakeConnection:
        def __init__(self, *_args: object, **kwargs: object) -> None:
            context = cast(ssl.SSLContext, kwargs["context"])
            self.sock = _BoundSocket(context, events, server_side=server_side)

        def request(self, *_args: object, **_kwargs: object) -> None:
            events.append("request")

        def close(self) -> None:
            events.append("close")

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/release",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )

    assert cast(_CodedError, raised.value).code == "public_release.tls_failed"
    assert "certificate" not in events
    assert "request" not in events
    assert events[-1] == "close"


def test_substituted_context_fails_closed_and_content_silent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []
    substitute = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.sock = _BoundSocket(substitute, events)

        def request(self, *_args: object, **_kwargs: object) -> None:
            events.append("request")

        def close(self) -> None:
            events.append("close")

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/release",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )

    assert cast(_CodedError, raised.value).code == "public_release.tls_failed"
    assert "api.github.com" not in str(raised.value)
    assert "request" not in events


@pytest.mark.parametrize("missing", ("context", "server_side"))
def test_missing_binding_accessor_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    missing: str,
) -> None:
    _, download, error_type = _load()

    class MissingSocket(_BoundSocket):
        def __getattribute__(self, name: str) -> object:
            if name == missing:
                raise AttributeError("binding accessor unavailable")
            return super().__getattribute__(name)

    class FakeConnection:
        def __init__(self, *_args: object, **kwargs: object) -> None:
            context = cast(ssl.SSLContext, kwargs["context"])
            self.sock = MissingSocket(context, [])

        def request(self, *_args: object, **_kwargs: object) -> None:
            raise AssertionError("request must not follow a missing binding accessor")

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/release",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )

    assert cast(_CodedError, raised.value).code == "public_release.tls_failed"
    assert isinstance(raised.value.__cause__, AttributeError)


@pytest.mark.parametrize(
    "failure",
    (NotImplementedError(), OSError(), TypeError(), ValueError()),
)
def test_binding_inspection_failure_preserves_cause_without_content(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: Exception,
) -> None:
    _, download, error_type = _load()

    class FailingSocket(_BoundSocket):
        @property
        def context(self) -> object:
            raise failure

    class FakeConnection:
        def __init__(self, *_args: object, **kwargs: object) -> None:
            context = cast(ssl.SSLContext, kwargs["context"])
            self.sock = FailingSocket(context, [])

        def request(self, *_args: object, **_kwargs: object) -> None:
            raise AssertionError("request must not follow binding inspection failure")

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/release",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )

    assert cast(_CodedError, raised.value).code == "public_release.tls_failed"
    assert raised.value.__cause__ is failure
    assert "api.github.com" not in str(raised.value)


@pytest.mark.parametrize("mutation", ("hostname", "minimum", "verify-flags"))
def test_post_handshake_context_policy_mutation_fails_before_identity(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    mutation: str,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []

    class FakeConnection:
        def __init__(self, *_args: object, **kwargs: object) -> None:
            self.context = cast(ssl.SSLContext, kwargs["context"])
            self.sock: _BoundSocket | None = None

        def connect(self) -> None:
            self.sock = _BoundSocket(self.context, events)
            if mutation == "hostname":
                self.context.check_hostname = False
            elif mutation == "minimum":
                self.context.minimum_version = ssl.TLSVersion.MINIMUM_SUPPORTED
            else:
                self.context.verify_flags &= ~ssl.VERIFY_X509_STRICT

        def request(self, *_args: object, **_kwargs: object) -> None:
            events.append("request")

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/release",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )

    assert cast(_CodedError, raised.value).code == "public_release.tls_failed"
    assert "certificate" not in events
    assert "request" not in events


def test_redirect_rebinds_an_independent_exact_client_context(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, _ = _load()
    contexts: list[ssl.SSLContext] = []
    responses = iter(
        (
            _RedirectResponse(location="https://objects.example.test/asset"),
            _Response(b"asset"),
        )
    )

    class FakeConnection:
        def __init__(self, host: str, *_args: object, **kwargs: object) -> None:
            context = cast(ssl.SSLContext, kwargs["context"])
            contexts.append(context)
            self.sock = _BoundSocket(context, [], server_hostname=host)

        def request(self, *_args: object, **_kwargs: object) -> None:
            return None

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
    assert len(contexts) == 2
    assert contexts[0] is not contexts[1]


def test_m53_changes_no_workflow_runtime_dependency_or_package_boundary() -> None:
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
    peer = source.index("_connect_public_peer(connection, deadline)")
    binding = source.index("_validate_tls_context_binding(connection, tls_context)")
    identity = source.index("_validate_tls_identity(connection, reference_hostname)")
    session = source.index("_validate_tls_session(connection)")
    request = source.index('connection.request(\n                "GET",')
    assert peer < binding < identity < session < request
    assert "actual_context is not expected_context" in source
    assert "server_side is not False" in source
    assert source.count("_require_public_tls_context(") == 3


def test_m53_public_and_maintainer_docs_define_the_exact_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0036-public-release-tls-context-binding.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").lower() for path in paths)
    combined = "\n".join(documents)

    assert all("m53" in document for document in documents)
    for term in (
        "exact context",
        "client-side",
        "after the handshake",
        "before",
        "every redirect",
        "no workflow",
        "not a real public release observation",
    ):
        assert term in combined
