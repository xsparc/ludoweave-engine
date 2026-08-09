"""Protect M56 public release status and redirect-reference conformance."""

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


class _Response:
    version = 11

    def __init__(
        self,
        status: object,
        body: bytes = b"",
        *,
        headers: Sequence[tuple[object, object]] = (),
        events: list[str] | None = None,
    ) -> None:
        self._status = status
        self.body = body
        self.headers = list(headers)
        self.events = [] if events is None else events
        self.offset = 0

    @property
    def status(self) -> object:
        self.events.append("status")
        return self._status

    def getheader(self, name: str) -> object:
        self.events.append(f"header:{name}")
        values = [
            value
            for key, value in self.headers
            if isinstance(key, str) and key.casefold() == name.casefold()
        ]
        if not values:
            return None
        if all(isinstance(value, str) for value in values):
            return ", ".join(cast(list[str], values))
        return values[0]

    def getheaders(self) -> object:
        self.events.append("headers")
        return list(self.headers)

    def read(self, amount: int = -1) -> bytes:
        self.events.append("read")
        if amount < 0:
            amount = len(self.body) - self.offset
        block = self.body[self.offset : self.offset + amount]
        self.offset += len(block)
        return block

    def close(self) -> None:
        self.events.append("response-close")


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
    spec = importlib.util.spec_from_file_location("m56_public_release_verifier", _VERIFIER)
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


@pytest.mark.parametrize(
    ("location", "expected_host", "expected_path"),
    (
        ("/asset%2Ewhl?token=a%2Bb", "api.github.com", "/asset%2Ewhl?token=a%2Bb"),
        (
            "https://objects.example.test/asset?token=a%2Bb",
            "objects.example.test",
            "/asset?token=a%2Bb",
        ),
        (
            "https://[2606:4700:4700::1111]/asset",
            "2606:4700:4700::1111",
            "/asset",
        ),
        ("/" + "a" * 7_999, "api.github.com", "/" + "a" * 7_999),
    ),
    ids=("relative", "cross-host", "ipv6-authority", "eight-thousand-octets"),
)
def test_single_bounded_uri_reference_redirects_after_metadata_validation(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    location: str,
    expected_host: str,
    expected_path: str,
) -> None:
    _, download, _ = _load()
    first_events: list[str] = []
    responses = iter(
        (
            _Response(302, headers=(("Location", location),), events=first_events),
            _Response(200, b"asset", headers=(("Content-Length", "5"),)),
        )
    )
    requests: list[tuple[str, str]] = []
    _install_responses(monkeypatch, responses, requests)

    download(
        "https://api.github.com/releases/assets/123",
        tmp_path / "asset.bin",
        accept="application/octet-stream",
        maximum_bytes=5,
        maximum_redirects=3,
        expected_bytes=5,
        partial_name=".asset-123.part",
    )

    assert requests == [
        ("api.github.com", "/releases/assets/123"),
        (expected_host, expected_path),
    ]
    assert first_events[:5] == [
        "header:Transfer-Encoding",
        "header:Content-Length",
        "status",
        "headers",
        "response-close",
    ]


@pytest.mark.parametrize("status", (200.0, True, "200", None, [200], 99, 600))
def test_malformed_status_fails_before_redirect_or_body_use(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    status: object,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []
    responses = iter((_Response(status, b"asset", events=events),))
    requests: list[tuple[str, str]] = []
    _install_responses(monkeypatch, responses, requests)

    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/releases/assets/123",
            tmp_path / "asset.bin",
            accept="application/octet-stream",
            maximum_bytes=5,
            maximum_redirects=3,
            expected_bytes=5,
            partial_name=".asset-123.part",
        )

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert str(status) not in str(raised.value)
    assert "headers" not in events
    assert "read" not in events


def test_status_accessor_failure_is_stable_chained_and_content_silent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()
    failure = AttributeError("private detail")

    class BrokenStatus(_Response):
        @property
        def status(self) -> object:
            raise failure

    responses = iter((BrokenStatus(200, b"asset"),))
    requests: list[tuple[str, str]] = []
    _install_responses(monkeypatch, responses, requests)

    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/releases/assets/123",
            tmp_path / "asset.bin",
            accept="application/octet-stream",
            maximum_bytes=5,
            maximum_redirects=3,
            expected_bytes=5,
            partial_name=".asset-123.part",
        )

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert raised.value.__cause__ is failure
    assert "private detail" not in str(raised.value)


@pytest.mark.parametrize(
    "headers",
    (
        (),
        (("Location", "/first"), ("location", "/second")),
        (("Location", b"/asset"),),
        ((1, "/asset"),),
        (("Location", "/asset"), ("Broken", object())),
    ),
    ids=("missing", "duplicate", "bytes", "non-string-name", "malformed-pair"),
)
def test_location_requires_one_well_formed_public_header_field(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    headers: Sequence[tuple[object, object]],
) -> None:
    _, download, error_type = _load()
    responses = iter((_Response(302, headers=headers),))
    requests: list[tuple[str, str]] = []
    _install_responses(monkeypatch, responses, requests)

    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/releases/assets/123",
            tmp_path / "asset.bin",
            accept="application/octet-stream",
            maximum_bytes=5,
            maximum_redirects=3,
            expected_bytes=5,
            partial_name=".asset-123.part",
        )

    assert cast(_CodedError, raised.value).code == "public_release.redirect_failed"
    assert requests == [("api.github.com", "/releases/assets/123")]


@pytest.mark.parametrize(
    "location",
    (
        "",
        " /asset",
        "/asset ",
        "/asset\nnext",
        "/asset\\next",
        "/asset%2",
        "/caf\u00e9",
        "/" + "a" * 8_000,
        "/asset[stale]",
        "?token=[bad]",
        "https://[::1",
        "::::",
    ),
    ids=(
        "empty",
        "leading-space",
        "trailing-space",
        "control",
        "backslash",
        "incomplete-percent",
        "non-ascii",
        "over-eight-thousand-octets",
        "brackets-in-path",
        "brackets-in-query",
        "invalid-ipv6",
        "colon-in-first-relative-segment",
    ),
)
def test_invalid_or_oversized_location_fails_before_another_request(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    location: str,
) -> None:
    _, download, error_type = _load()
    responses = iter((_Response(302, headers=(("Location", location),)),))
    requests: list[tuple[str, str]] = []
    _install_responses(monkeypatch, responses, requests)

    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/releases/assets/123",
            tmp_path / "asset.bin",
            accept="application/octet-stream",
            maximum_bytes=5,
            maximum_redirects=3,
            expected_bytes=5,
            partial_name=".asset-123.part",
        )

    assert cast(_CodedError, raised.value).code == "public_release.redirect_failed"
    assert requests == [("api.github.com", "/releases/assets/123")]


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
def test_header_collection_failure_is_stable_chained_and_content_silent(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure: Exception,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []

    class BrokenHeaders(_Response):
        def getheaders(self) -> object:
            raise failure

    responses = iter((BrokenHeaders(302, headers=(("Location", "/asset"),), events=events),))
    requests: list[tuple[str, str]] = []
    _install_responses(monkeypatch, responses, requests)

    with pytest.raises(error_type) as raised:
        download(
            "https://api.github.com/releases/assets/123",
            tmp_path / "asset.bin",
            accept="application/octet-stream",
            maximum_bytes=5,
            maximum_redirects=3,
            expected_bytes=5,
            partial_name=".asset-123.part",
        )

    assert cast(_CodedError, raised.value).code == "public_release.redirect_failed"
    assert raised.value.__cause__ is failure
    assert "read" not in events


def test_m56_changes_no_workflow_runtime_dependency_or_package_boundary() -> None:
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
    location = source.index("_validated_redirect_url(current_url, response)")
    stream = source.index("received = _stream_response(")
    assert framing < status < location < stream
    assert "response.getheaders()" in source
    assert "_URI_REFERENCE_PATTERN.fullmatch(location)" in source
    assert "bracket in component" in source


def test_m56_public_and_maintainer_docs_define_the_exact_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0039-public-release-redirect-reference.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m56" in document for document in documents)
    for term in (
        "status",
        "integer",
        "location",
        "single uri-reference",
        "8,000",
        "bracket",
        "every redirect",
        "no host allowlist",
        "no workflow",
        "not a real public release observation",
    ):
        assert term in combined
