"""Protect M52 public release TLS service-identity evidence."""

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


class _IdentitySocket:
    def __init__(
        self,
        context: ssl.SSLContext,
        events: list[str],
        *,
        server_hostname: object = "api.github.com",
        certificate: object = b"verified-leaf-certificate",
    ) -> None:
        self.context = context
        self.server_side = False
        self.session_reused = False
        self.events = events
        self._server_hostname = server_hostname
        self.certificate = certificate

    def getpeername(self) -> tuple[str, int]:
        self.events.append("peer")
        return ("8.8.8.8", 443)

    def settimeout(self, _value: float) -> None:
        return None

    @property
    def server_hostname(self) -> object:
        self.events.append("reference-hostname")
        return self._server_hostname

    def getpeercert(self, *, binary_form: bool = False) -> object:
        self.events.append(f"certificate:{binary_form}")
        return self.certificate

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
    spec = importlib.util.spec_from_file_location("m52_public_release_verifier", _VERIFIER)
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


@pytest.mark.parametrize(
    ("url", "observed_hostname", "expected_reference", "expected_path"),
    (
        (
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/123",
            "API.GITHUB.COM",
            "api.github.com",
            "/repos/xsparc/ludoweave-engine/releases/123",
        ),
        (
            "https://PYTHÖN.example/release",
            "xn--pythn-mua.example",
            "xn--pythn-mua.example",
            "/release",
        ),
    ),
)
def test_verified_service_identity_precedes_session_and_request(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    url: str,
    observed_hostname: str,
    expected_reference: str,
    expected_path: str,
) -> None:
    _, download, _ = _load()
    events: list[str] = []

    class FakeConnection:
        def __init__(self, host: str, *_args: object, **_kwargs: object) -> None:
            events.append(f"connection:{host}")
            self.context = cast(ssl.SSLContext, _kwargs["context"])
            self.sock: _IdentitySocket | None = None

        def connect(self) -> None:
            events.append("connect")
            self.sock = _IdentitySocket(
                self.context,
                events,
                server_hostname=observed_hostname,
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
        url,
        target,
        accept="application/vnd.github+json",
        maximum_bytes=100,
        maximum_redirects=0,
    )

    assert target.read_bytes() == b"{}"
    assert events == [
        f"connection:{expected_reference}",
        "connect",
        "peer",
        "reference-hostname",
        "certificate:True",
        "version",
        "cipher",
        "compression",
        "alpn",
        f"request:GET:{expected_path}",
        "close",
    ]


@pytest.mark.parametrize(
    ("url", "server_hostname", "certificate"),
    (
        ("https://api.github.com/release", None, b"verified-leaf-certificate"),
        ("https://api.github.com/release", [], b"verified-leaf-certificate"),
        ("https://api.github.com/release", "", b"verified-leaf-certificate"),
        (
            "https://api.github.com/release",
            "secret.example",
            b"verified-leaf-certificate",
        ),
        ("https://k.example/release", "\u212a.example", b"verified-leaf-certificate"),
        ("https://api.github.com/release", "api.github.com", None),
        ("https://api.github.com/release", "api.github.com", b""),
        (
            "https://api.github.com/release",
            "api.github.com",
            bytearray(b"certificate"),
        ),
    ),
)
def test_invalid_service_identity_fails_before_session_or_request(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    url: str,
    server_hostname: object,
    certificate: object,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.context = cast(ssl.SSLContext, _kwargs["context"])
            self.sock: _IdentitySocket | None = None

        def connect(self) -> None:
            events.append("connect")
            self.sock = _IdentitySocket(
                self.context,
                events,
                server_hostname=server_hostname,
                certificate=certificate,
            )

        def request(self, *_args: object, **_kwargs: object) -> None:
            events.append("request")

        def close(self) -> None:
            events.append("close")

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    with pytest.raises(error_type) as raised:
        download(
            url,
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )

    assert cast(_CodedError, raised.value).code == "public_release.tls_failed"
    assert "request" not in events
    assert "version" not in events
    assert events[-1] == "close"
    assert "api.github.com" not in str(raised.value)
    assert "secret.example" not in str(raised.value)


@pytest.mark.parametrize("missing", ("server_hostname", "getpeercert"))
def test_missing_service_identity_accessor_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    missing: str,
) -> None:
    _, download, error_type = _load()
    requests = 0

    class MissingSocket(_IdentitySocket):
        def __getattribute__(self, name: str) -> object:
            if name == missing:
                raise AttributeError("identity accessor is unavailable")
            return super().__getattribute__(name)

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            context = cast(ssl.SSLContext, _kwargs["context"])
            self.sock = MissingSocket(context, [])

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


def test_invalid_idna_reference_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()
    requests = 0
    connections = 0

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            nonlocal connections
            connections += 1
            context = cast(ssl.SSLContext, _kwargs["context"])
            self.sock = _IdentitySocket(context, [], server_hostname="invalid.example")

        def request(self, *_args: object, **_kwargs: object) -> None:
            nonlocal requests
            requests += 1

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    with pytest.raises(error_type) as raised:
        download(
            "https://\ud800.example/release",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )

    assert cast(_CodedError, raised.value).code == "public_release.tls_failed"
    assert requests == 0
    assert connections == 0


@pytest.mark.parametrize("failure", (NotImplementedError(), OSError(), TypeError()))
def test_certificate_inspection_failure_is_stable_and_content_silent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: Exception,
) -> None:
    _, download, error_type = _load()
    requests = 0

    class FailingSocket(_IdentitySocket):
        def getpeercert(self, *, binary_form: bool = False) -> object:
            assert binary_form
            raise failure

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            context = cast(ssl.SSLContext, _kwargs["context"])
            self.sock = FailingSocket(context, [])

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
    assert raised.value.__cause__ is failure
    assert requests == 0
    assert "api.github.com" not in str(raised.value)


def test_redirect_revalidates_independent_service_identity(
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
            self.sock = _IdentitySocket(
                context,
                events,
                server_hostname=host.encode("idna").decode("ascii"),
                certificate=f"certificate:{host}".encode(),
            )

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
    assert events.count("reference-hostname") == 2
    assert events.count("certificate:True") == 2
    assert [event for event in events if event.startswith("request:")] == [
        "request:api.github.com",
        "request:objects.example.test",
    ]


def test_m52_changes_no_workflow_runtime_dependency_or_package_boundary() -> None:
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
    peer = source.index("_connect_public_peer(connection, deadline)")
    identity = source.index("_validate_tls_identity(connection, reference_hostname)")
    session = source.index("_validate_tls_session(connection)")
    request = source.index('connection.request(\n                "GET",')
    assert peer < identity < session < request
    assert "peer.getpeercert(binary_form=True)" in source
    assert 'hostname.encode("idna").decode("ascii")' in source


def test_m52_public_and_maintainer_docs_define_the_exact_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0035-public-release-tls-service-identity.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").lower() for path in paths)
    combined = "\n".join(documents)

    assert all("m52" in document for document in documents)
    for term in (
        "service identity",
        "reference hostname",
        "peer certificate",
        "idna",
        "before",
        "no workflow",
        "not a real public release observation",
    ):
        assert term in combined
