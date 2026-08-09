"""Protect M50 public release TLS key-log isolation."""

from __future__ import annotations

import hashlib
import http.client
import importlib.util
import os
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


class _PeerSocket:
    def __init__(self, context: ssl.SSLContext, server_hostname: str = "api.github.com") -> None:
        self.context = context
        self.server_side = False
        self.session_reused = False
        self.server_hostname = server_hostname

    def getpeername(self) -> tuple[str, int]:
        return ("8.8.8.8", 443)

    def getpeercert(self, *, binary_form: bool = False) -> bytes:
        assert binary_form
        return b"verified-leaf-certificate"

    def settimeout(self, _value: float) -> None:
        return None

    def version(self) -> str:
        return "TLSv1.3"

    def cipher(self) -> tuple[str, str, int]:
        return ("TLS_AES_256_GCM_SHA384", "TLSv1.3", 256)

    def compression(self) -> None:
        return None

    def selected_alpn_protocol(self) -> str:
        return "http/1.1"


def _load() -> tuple[
    ModuleType,
    _Download,
    Callable[[], ssl.SSLContext],
    type[Exception],
]:
    spec = importlib.util.spec_from_file_location("m50_public_release_verifier", _VERIFIER)
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
        cast(Callable[[], ssl.SSLContext], module._public_tls_context),
        cast(type[Exception], module.PublicReleaseVerificationError),
    )


def test_explicit_context_retains_verified_modern_tls_without_key_logging() -> None:
    _, _, context_factory, _ = _load()

    context = context_factory()

    assert context.protocol == ssl.PROTOCOL_TLS_CLIENT
    assert context.verify_mode == ssl.CERT_REQUIRED
    assert context.check_hostname
    assert context.minimum_version == ssl.TLSVersion.TLSv1_2
    assert context.maximum_version == ssl.TLSVersion.MAXIMUM_SUPPORTED
    assert context.verify_flags & ssl.VERIFY_X509_PARTIAL_CHAIN
    assert context.verify_flags & ssl.VERIFY_X509_STRICT
    assert context.keylog_filename is None


def test_ambient_keylog_path_is_not_created_or_used(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, _, _ = _load()
    keylog = tmp_path / "ambient-tls-secrets.log"
    monkeypatch.setenv("SSLKEYLOGFILE", str(keylog))
    contexts: list[ssl.SSLContext] = []

    class FakeConnection:
        def __init__(
            self,
            _host: str,
            _port: int | None,
            *,
            timeout: float,
            context: ssl.SSLContext,
        ) -> None:
            assert timeout > 0
            contexts.append(context)
            self.context = context
            self.host = _host
            self.sock: _PeerSocket | None = None

        def connect(self) -> None:
            self.sock = _PeerSocket(self.context, self.host)

        def request(
            self,
            method: str,
            path: str,
            *,
            headers: Mapping[str, str],
        ) -> None:
            assert method == "GET"
            assert path.startswith("/repos/")
            assert "Authorization" not in headers

        def getresponse(self) -> _Response:
            return _Response(b"{}")

        def close(self) -> None:
            return None

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
    assert os.environ["SSLKEYLOGFILE"] == str(keylog)
    assert not keylog.exists()
    assert len(contexts) == 1
    assert contexts[0].keylog_filename is None


def test_redirect_hop_receives_an_independent_isolated_context(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, _, _ = _load()
    contexts: list[ssl.SSLContext] = []
    responses = iter(
        (
            _RedirectResponse(b"", location="https://objects.example.test/asset"),
            _Response(b"asset"),
        )
    )

    class FakeConnection:
        def __init__(
            self,
            _host: str,
            _port: int | None,
            *,
            timeout: float,
            context: ssl.SSLContext,
        ) -> None:
            assert timeout > 0
            contexts.append(context)
            self.context = context
            self.host = _host
            self.sock: _PeerSocket | None = None

        def connect(self) -> None:
            self.sock = _PeerSocket(self.context, self.host)

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
    assert all(context.keylog_filename is None for context in contexts)


def test_tls_context_failure_is_stable_and_content_silent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module, download, _, error_type = _load()
    secret_path = tmp_path / "must-not-appear.log"
    monkeypatch.setenv("SSLKEYLOGFILE", str(secret_path))

    def fail_context(_protocol: object) -> ssl.SSLContext:
        raise OSError("context source mentioned a sensitive local path")

    monkeypatch.setattr(module.ssl, "SSLContext", fail_context)
    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/repos/xsparc/ludoweave-engine/releases/123",
            tmp_path / "release.json",
            accept="application/vnd.github+json",
            maximum_bytes=100,
            maximum_redirects=0,
        )

    assert cast(_CodedError, raised.value).code == "public_release.tls_failed"
    message = str(raised.value)
    assert str(secret_path) not in message
    assert "sensitive" not in message
    assert not secret_path.exists()


def test_tls_context_invariant_failure_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    module, _, context_factory, error_type = _load()

    class InsecureContext:
        protocol = ssl.PROTOCOL_TLS_CLIENT
        verify_mode = ssl.CERT_REQUIRED
        check_hostname = False
        minimum_version = ssl.TLSVersion.MINIMUM_SUPPORTED
        keylog_filename = None
        verify_flags = ssl.VerifyFlags(0)

        def load_default_certs(self, _purpose: ssl.Purpose) -> None:
            return None

        def set_alpn_protocols(self, _protocols: list[str]) -> None:
            return None

    def insecure_context(_protocol: object) -> ssl.SSLContext:
        return cast(ssl.SSLContext, InsecureContext())

    monkeypatch.setattr(module.ssl, "SSLContext", insecure_context)
    with pytest.raises(error_type) as raised:
        context_factory()

    assert cast(_CodedError, raised.value).code == "public_release.tls_failed"


def test_m50_changes_no_workflow_runtime_dependency_or_package_boundary() -> None:
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
    assert "ssl.create_default_context" not in source
    assert "ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)" in source
    assert 'getattr(context, "keylog_filename", None) is not None' in source
    assert 'code="public_release.tls_failed"' in source


def test_m50_docs_define_keylog_boundary_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0033-public-release-tls-keylog-isolation.md",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8").casefold()
        assert "m50" in text
        assert "key" in text
        assert "tls" in text

    normalized = " ".join(paths[-1].read_text(encoding="utf-8").split()).casefold()
    for term in (
        "sslkeylogfile",
        "session secrets",
        "protocol_tls_client",
        "cert_required",
        "hostname",
        "tls 1.2",
        "system",
        "no real m50 signed-tag execution",
        "no workflow",
        "not a real public release observation",
    ):
        assert term in normalized
