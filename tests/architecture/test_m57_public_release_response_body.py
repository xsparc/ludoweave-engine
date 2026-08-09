"""Protect M57 public release response-body conformance."""

from __future__ import annotations

import hashlib
import http.client
import importlib.util
import ssl
import sys
from collections.abc import Iterator, Sequence
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


class _HostileBytes(bytes):
    def __len__(self) -> int:
        raise RuntimeError("private length detail")


class _Response:
    version = 11
    status = 200

    def __init__(
        self,
        blocks: Sequence[object],
        *,
        headers: Sequence[tuple[object, object]] = (),
        status: int = 200,
    ) -> None:
        self._blocks = iter(blocks)
        self._headers = list(headers)
        self.status = status
        self.read_amounts: list[int] = []
        self.closed = False

    def getheader(self, name: str) -> object:
        values = [
            value
            for key, value in self._headers
            if isinstance(key, str) and key.casefold() == name.casefold()
        ]
        if not values:
            return None
        if all(isinstance(value, str) for value in values):
            return ", ".join(cast(list[str], values))
        return values[0]

    def getheaders(self) -> object:
        return list(self._headers)

    def read(self, amount: int = -1) -> object:
        self.read_amounts.append(amount)
        return next(self._blocks, b"")

    def close(self) -> None:
        self.closed = True


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
    spec = importlib.util.spec_from_file_location("m57_public_release_verifier", _VERIFIER)
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


def _install_responses(
    monkeypatch: pytest.MonkeyPatch,
    responses: Iterator[_Response],
    requests: list[tuple[str, str]],
) -> None:
    class FakeConnection:
        def __init__(self, host: str, *_args: object, **kwargs: object) -> None:
            self.host = host
            self.sock = _Socket(cast(ssl.SSLContext, kwargs["context"]), host)

        def request(self, _method: str, path: str, **_kwargs: object) -> None:
            requests.append((self.host, path))

        def getresponse(self) -> _Response:
            return next(responses)

        def close(self) -> None:
            return None

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)


def _download_response(
    download: _Download,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    response: _Response,
) -> None:
    _install_responses(monkeypatch, iter((response,)), [])
    download(
        "https://api.github.com/repos/xsparc/ludoweave-engine/releases/123",
        tmp_path / "release.json",
        accept="application/vnd.github+json",
        maximum_bytes=2 * 1024 * 1024,
        maximum_redirects=0,
    )


@pytest.mark.parametrize(
    "block",
    ("text", bytearray(b"mutable"), memoryview(b"view"), _HostileBytes(b"subclass"), None, True),
    ids=("text", "bytearray", "memoryview", "bytes-subclass", "none", "bool"),
)
def test_response_read_requires_exact_immutable_bytes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    block: object,
) -> None:
    _, download, error_type = _load()
    response = _Response((block, b""))

    with pytest.raises(error_type) as raised:
        _download_response(download, tmp_path, monkeypatch, response)

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert str(block) not in str(raised.value)
    assert response.closed


def test_response_read_rejects_more_than_the_requested_amount(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()
    oversized_block = b"x" * (1024 * 1024 + 1)
    response = _Response((oversized_block, b""))

    with pytest.raises(error_type) as raised:
        _download_response(download, tmp_path, monkeypatch, response)

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert response.read_amounts == [1024 * 1024]
    assert response.closed


@pytest.mark.parametrize("body", (b"abc", b"abcdef"), ids=("short", "long"))
def test_declared_content_length_must_equal_streamed_octets(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    body: bytes,
) -> None:
    _, download, error_type = _load()
    response = _Response((body, b""), headers=(("Content-Length", "5"),))

    with pytest.raises(error_type) as raised:
        _download_response(download, tmp_path, monkeypatch, response)

    assert cast(_CodedError, raised.value).code == "public_release.size_mismatch"
    assert response.closed


@pytest.mark.parametrize(
    "failure",
    (AttributeError(), NotImplementedError(), TypeError(), ValueError()),
)
def test_response_read_failures_are_stable_chained_and_content_silent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: Exception,
) -> None:
    _, download, error_type = _load()

    class BrokenResponse(_Response):
        def read(self, amount: int = -1) -> object:
            del amount
            raise failure

    response = BrokenResponse(())
    failure.add_note("private body detail")

    with pytest.raises(error_type) as raised:
        _download_response(download, tmp_path, monkeypatch, response)

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert raised.value.__cause__ is failure
    assert "private body detail" not in str(raised.value)
    assert response.closed


def test_valid_bounded_blocks_and_exact_declared_length_are_written(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, _ = _load()
    response = _Response(
        (b"ab", b"cde", b""),
        headers=(("Content-Length", "5"),),
    )

    _download_response(download, tmp_path, monkeypatch, response)

    assert (tmp_path / "release.json").read_bytes() == b"abcde"
    assert response.closed


def test_redirected_success_rechecks_declared_body_completeness(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()
    responses = iter(
        (
            _Response((), status=302, headers=(("Location", "/asset"),)),
            _Response((b"abc", b""), headers=(("Content-Length", "5"),)),
        )
    )
    requests: list[tuple[str, str]] = []
    _install_responses(monkeypatch, responses, requests)

    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/releases/assets/123",
            tmp_path / "asset.bin",
            accept="application/octet-stream",
            maximum_bytes=10,
            maximum_redirects=3,
        )

    assert cast(_CodedError, raised.value).code == "public_release.size_mismatch"
    assert requests == [
        ("api.github.com", "/releases/assets/123"),
        ("api.github.com", "/asset"),
    ]


def test_m57_changes_no_workflow_runtime_dependency_or_package_boundary() -> None:
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
    framing = source.index("_validate_http_response_framing(response)")
    status = source.index("_validate_http_response_status(response)")
    stream = source.index("received = _stream_response(")
    completeness = source.index("received != declared_bytes")
    publish = source.index("_publish_partial(partial, target)")
    assert framing < status < stream < completeness < publish
    assert "type(block) is not bytes" in source
    assert "len(block) > amount" in source


def test_m57_public_and_maintainer_docs_define_the_exact_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0040-public-release-response-body-conformance.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m57" in document for document in documents)
    for term in (
        "response body",
        "immutable bytes",
        "requested amount",
        "content-length",
        "streamed octets",
        "every successful response",
        "no alternate client",
        "no workflow",
        "not a real public release observation",
    ):
        assert term in combined
