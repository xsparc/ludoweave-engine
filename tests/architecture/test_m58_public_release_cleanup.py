"""Protect M58 public release transport-cleanup conformance."""

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


class _TrackedConnection(Protocol):
    close_calls: int
    target_visible_on_close: bool | None


class _HostileTruthyError(RuntimeError):
    def __bool__(self) -> bool:
        raise AssertionError("cleanup error truthiness must not be evaluated")


class _Response:
    version = 11

    def __init__(
        self,
        blocks: Sequence[bytes] = (b"ok", b""),
        *,
        status: int = 200,
        headers: Sequence[tuple[str, str]] = (("Content-Length", "2"),),
        close_error: BaseException | None = None,
        events: list[str] | None = None,
        target: Path | None = None,
    ) -> None:
        self.status = status
        self._blocks = iter(blocks)
        self._headers = list(headers)
        self._close_error = close_error
        self._events = events
        self._target = target
        self.close_calls = 0
        self.target_visible_on_close: bool | None = None

    def getheader(self, name: str) -> str | None:
        values = [value for key, value in self._headers if key.casefold() == name.casefold()]
        return ", ".join(values) if values else None

    def getheaders(self) -> list[tuple[str, str]]:
        return list(self._headers)

    def read(self, _amount: int = -1) -> bytes:
        return next(self._blocks, b"")

    def close(self) -> None:
        self.close_calls += 1
        if self._events is not None:
            self._events.append("response.close")
        if self._target is not None:
            self.target_visible_on_close = self._target.exists()
        if self._close_error is not None:
            raise self._close_error


class _ReadFailureResponse(_Response):
    def __init__(
        self,
        failure: Exception,
        *,
        close_error: BaseException | None = None,
        events: list[str] | None = None,
    ) -> None:
        super().__init__(close_error=close_error, events=events)
        self._failure = failure

    def read(self, _amount: int = -1) -> bytes:
        raise self._failure


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
    spec = importlib.util.spec_from_file_location("m58_public_release_verifier", _VERIFIER)
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


def _install_connections(
    monkeypatch: pytest.MonkeyPatch,
    specifications: Iterator[tuple[_Response | BaseException, BaseException | None]],
    *,
    events: list[str],
    requests: list[str] | None = None,
    target: Path | None = None,
) -> list[_TrackedConnection]:
    connections: list[_TrackedConnection] = []

    class FakeConnection:
        def __init__(self, host: str, *_args: object, **kwargs: object) -> None:
            self.sock = _Socket(cast(ssl.SSLContext, kwargs["context"]), host)
            self._response, self._close_error = next(specifications)
            self.close_calls = 0
            self.target_visible_on_close: bool | None = None
            connections.append(self)

        def request(self, _method: str, path: str, **_kwargs: object) -> None:
            if requests is not None:
                requests.append(path)

        def getresponse(self) -> _Response:
            if isinstance(self._response, BaseException):
                raise self._response
            return self._response

        def close(self) -> None:
            self.close_calls += 1
            events.append("connection.close")
            if target is not None:
                self.target_visible_on_close = target.exists()
            if self._close_error is not None:
                raise self._close_error

    monkeypatch.setattr(http.client, "HTTPSConnection", FakeConnection)
    return connections


def _download_asset(download: _Download, tmp_path: Path) -> Path:
    target = tmp_path / "asset.bin"
    download(
        "https://api.github.com/releases/assets/123",
        target,
        accept="application/octet-stream",
        maximum_bytes=2,
        maximum_redirects=3,
        expected_bytes=2,
        partial_name=".asset.part",
    )
    return target


def test_success_closes_response_then_connection_before_partial_publication(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, _ = _load()
    events: list[str] = []
    target = tmp_path / "asset.bin"
    response = _Response(events=events, target=target)
    connections = _install_connections(
        monkeypatch,
        iter(((response, None),)),
        events=events,
        target=target,
    )

    assert _download_asset(download, tmp_path) == target

    assert events == ["response.close", "connection.close"]
    assert response.close_calls == 1
    assert response.target_visible_on_close is False
    connection = connections[0]
    assert connection.close_calls == 1
    assert connection.target_visible_on_close is False
    assert target.read_bytes() == b"ok"
    assert not (tmp_path / ".asset.part").exists()


@pytest.mark.parametrize(
    ("response_error", "connection_error", "expected_cause"),
    (
        (RuntimeError("private response close"), None, "private response close"),
        (None, RuntimeError("private connection close"), "private connection close"),
        (
            RuntimeError("first private close"),
            RuntimeError("second private close"),
            "first private close",
        ),
    ),
    ids=("response", "connection", "both-first-wins"),
)
def test_cleanup_only_failures_are_stable_chained_and_attempt_both_closes(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    response_error: BaseException | None,
    connection_error: BaseException | None,
    expected_cause: str,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []
    response = _Response(close_error=response_error, events=events)
    connections = _install_connections(
        monkeypatch,
        iter(((response, connection_error),)),
        events=events,
    )

    with pytest.raises(error_type) as raised:
        _download_asset(download, tmp_path)

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert str(raised.value.__cause__) == expected_cause
    assert expected_cause not in str(raised.value)
    assert events == ["response.close", "connection.close"]
    assert response.close_calls == 1
    assert connections[0].close_calls == 1
    assert not (tmp_path / "asset.bin").exists()
    assert (tmp_path / ".asset.part").read_bytes() == b"ok"


def test_active_read_failure_remains_primary_when_both_closes_fail(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []
    read_error = ValueError("private read detail")
    response = _ReadFailureResponse(
        read_error,
        close_error=RuntimeError("private response close"),
        events=events,
    )
    connections = _install_connections(
        monkeypatch,
        iter(((response, RuntimeError("private connection close")),)),
        events=events,
    )

    with pytest.raises(error_type) as raised:
        _download_asset(download, tmp_path)

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert raised.value.__cause__ is read_error
    assert events == ["response.close", "connection.close"]
    assert connections[0].close_calls == 1


def test_first_cleanup_failure_does_not_invoke_exception_truthiness(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []
    response_error = _HostileTruthyError("private first close")
    connections = _install_connections(
        monkeypatch,
        iter(
            (
                (
                    _Response(close_error=response_error, events=events),
                    RuntimeError("private second close"),
                ),
            )
        ),
        events=events,
    )

    with pytest.raises(error_type) as raised:
        _download_asset(download, tmp_path)

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert raised.value.__cause__ is response_error
    assert events == ["response.close", "connection.close"]
    assert connections[0].close_calls == 1


def test_caller_exception_context_does_not_suppress_cleanup_only_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []
    close_error = RuntimeError("private cleanup-only detail")
    connections = _install_connections(
        monkeypatch,
        iter(((_Response(close_error=close_error, events=events), None),)),
        events=events,
    )

    try:
        raise LookupError("unrelated caller context")
    except LookupError:
        with pytest.raises(error_type) as raised:
            _download_asset(download, tmp_path)

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert raised.value.__cause__ is close_error
    assert events == ["response.close", "connection.close"]
    assert connections[0].close_calls == 1
    assert not (tmp_path / "asset.bin").exists()


def test_getresponse_failure_remains_primary_when_connection_close_fails(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []
    response_error = ValueError("private getresponse detail")
    connections = _install_connections(
        monkeypatch,
        iter(((response_error, RuntimeError("private connection close")),)),
        events=events,
    )

    with pytest.raises(error_type) as raised:
        _download_asset(download, tmp_path)

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert raised.value.__cause__ is response_error
    assert events == ["connection.close"]
    assert connections[0].close_calls == 1


def test_redirect_continues_only_after_successful_cleanup(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, error_type = _load()
    events: list[str] = []
    requests: list[str] = []
    redirect = _Response(
        (),
        status=302,
        headers=(("Location", "/asset"),),
        close_error=RuntimeError("private redirect close"),
        events=events,
    )
    final = _Response(events=events)
    connections = _install_connections(
        monkeypatch,
        iter(((redirect, None), (final, None))),
        events=events,
        requests=requests,
    )

    with pytest.raises(error_type) as raised:
        _download_asset(download, tmp_path)

    assert cast(_CodedError, raised.value).code == "public_release.request_failed"
    assert requests == ["/releases/assets/123"]
    assert events == ["response.close", "connection.close"]
    assert len(connections) == 1


def test_cleanup_control_signal_is_not_wrapped_and_connection_close_is_attempted(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _, download, _ = _load()
    events: list[str] = []
    signal = KeyboardInterrupt()
    response = _Response(close_error=signal, events=events)
    connections = _install_connections(
        monkeypatch,
        iter(((response, None),)),
        events=events,
    )

    with pytest.raises(KeyboardInterrupt) as raised:
        _download_asset(download, tmp_path)

    assert raised.value is signal
    assert events == ["response.close", "connection.close"]
    assert connections[0].close_calls == 1


def test_m58_changes_no_workflow_runtime_dependency_or_package_boundary() -> None:
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
    response_close = source.index("response.close()")
    connection_close = source.index("connection.close()")
    publish = source.index("_publish_partial(partial, target)")
    assert response_close < connection_close < publish


def test_m58_public_and_maintainer_docs_define_the_exact_boundary() -> None:
    paths = (
        _ROOT / "README.md",
        _ROOT / "CHANGELOG.md",
        _ROOT / "SECURITY.md",
        _ROOT / "MAINTAINERS.md",
        _ROOT / "docs" / "architecture.md",
        _ROOT / "docs" / "release-process.md",
        _ROOT / "docs" / "rfcs" / "0041-public-release-cleanup-conformance.md",
    )
    documents = tuple(path.read_text(encoding="utf-8").casefold() for path in paths)
    combined = "\n".join(documents)

    assert all("m58" in document for document in documents)
    for term in (
        "response close",
        "connection close",
        "both close attempts",
        "primary failure",
        "before redirect continuation",
        "before partial publication",
        "no rollback",
        "no workflow",
        "not a real public release observation",
    ):
        assert term in combined
