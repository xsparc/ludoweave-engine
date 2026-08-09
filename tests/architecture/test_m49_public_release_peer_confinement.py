"""Protect M49 public release connected-peer confinement."""

from __future__ import annotations

import hashlib
import http.client
import importlib.util
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

    def __init__(self, body: bytes) -> None:
        self._body = body
        self._offset = 0

    def getheader(self, _name: str) -> str | None:
        return None

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

    def __init__(self, location: str) -> None:
        super().__init__(b"")
        self.location = location

    def getheader(self, name: str) -> str | None:
        return self.location if name == "Location" else None


class _PeerSocket:
    def __init__(self, address: str, port: int = 443) -> None:
        self.address = address
        self.port = port
        self.timeouts: list[float] = []

    def getpeername(self) -> tuple[str, int]:
        return (self.address, self.port)

    def settimeout(self, value: float) -> None:
        self.timeouts.append(value)


def _load() -> tuple[ModuleType, _Download, type[Exception]]:
    spec = importlib.util.spec_from_file_location("m49_public_release_verifier", _VERIFIER)
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
    "address",
    (
        "0.0.0.0",
        "10.0.0.1",
        "100.64.0.1",
        "127.0.0.1",
        "169.254.169.254",
        "192.0.2.1",
        "224.0.0.1",
        "255.255.255.255",
        "::",
        "::1",
        "::ffff:127.0.0.1",
        "2001:db8::1",
        "fc00::1",
        "fe80::1",
        "ff02::1",
    ),
)
def test_non_global_connected_peer_is_rejected_before_request(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    address: str,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.sock: _PeerSocket | None = None

        def connect(self) -> None:
            events.append("connect")
            self.sock = _PeerSocket(address)

        def request(self, *_args: object, **_kwargs: object) -> None:
            events.append("request")

        def getresponse(self) -> _Response:
            raise AssertionError("response must not be read from a forbidden peer")

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

    assert cast(_CodedError, raised.value).code == "public_release.peer_forbidden"
    message = str(raised.value)
    assert address not in message
    assert "api.github.com" not in message
    assert "https://" not in message
    assert events == ["connect", "close"]
    assert not (tmp_path / "release.json").exists()


@pytest.mark.parametrize("address", ("8.8.8.8", "2606:4700:4700::1111", "::ffff:8.8.8.8"))
def test_global_connected_peer_is_accepted_before_request(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    address: str,
) -> None:
    _, download, _ = _load()
    events: list[str] = []
    socket = _PeerSocket(address)

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.sock: _PeerSocket | None = None

        def connect(self) -> None:
            events.append("connect")
            self.sock = socket

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
            events.append("response")
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
        "request:GET:/repos/xsparc/ludoweave-engine/releases/123",
        "response",
        "close",
    ]
    assert socket.timeouts


def test_redirect_peer_is_rechecked_before_redirect_request(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()
    addresses = iter(("8.8.8.8", "127.0.0.1"))
    responses = iter(
        (
            _RedirectResponse("https://objects.example.test/asset"),
            _Response(b"asset"),
        )
    )
    requests: list[str] = []

    class FakeConnection:
        def __init__(self, host: str, *_args: object, **_kwargs: object) -> None:
            self.host = host
            self.sock: _PeerSocket | None = None

        def connect(self) -> None:
            self.sock = _PeerSocket(next(addresses))

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

    assert cast(_CodedError, raised.value).code == "public_release.peer_forbidden"
    assert requests == ["api.github.com"]


@pytest.mark.parametrize(
    ("phase", "code"),
    (
        ("connect_timeout", "public_release.request_timeout"),
        ("peer_timeout", "public_release.request_timeout"),
        ("peer_oserror", "public_release.request_failed"),
        ("missing_socket", "public_release.request_failed"),
    ),
)
def test_peer_discovery_failures_retain_stable_request_codes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    phase: str,
    code: str,
) -> None:
    _, download, error_type = _load()

    class BrokenPeerSocket(_PeerSocket):
        def getpeername(self) -> tuple[str, int]:
            if phase == "peer_timeout":
                raise TimeoutError
            if phase == "peer_oserror":
                raise OSError
            return super().getpeername()

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.sock: BrokenPeerSocket | None = None

        def connect(self) -> None:
            if phase == "connect_timeout":
                raise TimeoutError
            if phase != "missing_socket":
                self.sock = BrokenPeerSocket("8.8.8.8")

        def request(self, *_args: object, **_kwargs: object) -> None:
            raise AssertionError("request must not follow peer-discovery failure")

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
    assert cast(_CodedError, raised.value).code == code


@pytest.mark.parametrize(
    ("peer", "code"),
    (
        (("8.8.8.8", 444), "public_release.request_failed"),
        (("not-an-address", 443), "public_release.request_failed"),
        ((8, 443), "public_release.request_failed"),
        ("8.8.8.8", "public_release.request_failed"),
    ),
)
def test_malformed_or_wrong_port_peer_fails_closed(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    peer: object,
    code: str,
) -> None:
    _, download, error_type = _load()

    class PeerSocket:
        def settimeout(self, _value: float) -> None:
            return None

        def getpeername(self) -> object:
            return peer

    class FakeConnection:
        def __init__(self, *_args: object, **_kwargs: object) -> None:
            self.sock: PeerSocket | None = None

        def connect(self) -> None:
            self.sock = PeerSocket()

        def request(self, *_args: object, **_kwargs: object) -> None:
            raise AssertionError("request must not reach an invalid peer")

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
    assert cast(_CodedError, raised.value).code == code


def test_m49_changes_no_workflow_runtime_dependency_or_package_boundary() -> None:
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
    assert "import ipaddress" in source
    assert "getpeername()" in source
    assert "is_global" in source
    assert source.index("_connect_public_peer(connection, deadline)") < source.index(
        'connection.request(\n                "GET",'
    )


def test_m49_docs_define_peer_scope_and_nonclaims() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0032-public-release-peer-confinement.md",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8").casefold()
        assert "m49" in text
        assert "peer" in text

    normalized = " ".join(paths[-1].read_text(encoding="utf-8").split()).casefold()
    for term in (
        "globally reachable",
        "connected peer",
        "before",
        "ipv4",
        "ipv6",
        "no hostname allowlist",
        "no release mutation",
        "not a real public release observation",
        "signed-tag",
    ):
        assert term in normalized
