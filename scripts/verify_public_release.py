"""Verify exact public GitHub release bytes and the installed release candidate."""

from __future__ import annotations

import argparse
import contextlib
import http.client
import io
import ipaddress
import json
import os
import re
import ssl
import sys
import time
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, cast
from urllib.parse import SplitResult, urljoin, urlsplit, urlunsplit

import smoke_release
import verify_release_draft

_PROTOCOL = "ludoweave.public-release-consumer/1"
_PLAN_PROTOCOL = "ludoweave.release-asset-retrieval-plan/1"
_REPOSITORY = "xsparc/ludoweave-engine"
_API_HOST = "api.github.com"
_API_VERSION = "2026-03-10"
_MAX_RELEASE_ID = (1 << 63) - 1
_MAX_DOCUMENT_BYTES = 4 * 1024 * 1024
_MAX_ASSETS = 32
_MAX_ASSET_BYTES = 256 * 1024 * 1024
_MAX_TOTAL_BYTES = 512 * 1024 * 1024
_MAX_PLAN_BYTES = 16 * 1024
_CONNECT_TIMEOUT_SECONDS = 10.0
_REQUEST_TIMEOUT_SECONDS = 30.0
_MAX_ASSET_REDIRECTS = 3
_MAX_REDIRECT_URI_OCTETS = 8_000
_READ_BYTES = 1024 * 1024
_HTTP_ALPN = "http/1.1"
_ALLOWED_TLS_VERSIONS = frozenset(("TLSv1.2", "TLSv1.3"))
_MINIMUM_TLS_SECRET_BITS = 128
_REQUIRED_TLS_VERIFY_FLAGS = ssl.VERIFY_X509_PARTIAL_CHAIN | ssl.VERIFY_X509_STRICT
_ID_PATTERN = re.compile(r"[1-9][0-9]{0,18}")
_SIZE_PATTERN = re.compile(r"(?:0|[1-9][0-9]{0,8})")
_NAME_PATTERN = re.compile(r"[0-9A-Za-z][0-9A-Za-z._+-]{0,255}")
_URI_REFERENCE_PATTERN = re.compile(
    r"(?:[0-9A-Za-z._~:/?#\[\]@!$&'()*+,;=\-]|%[0-9A-Fa-f]{2}){1,8000}"
)


@dataclass(frozen=True, slots=True)
class AssetPlanItem:
    """One fully bounded public asset retrieval instruction."""

    asset_id: int
    bytes: int
    name: str


@dataclass(frozen=True, slots=True)
class VerificationContext:
    """Validated workflow-owned paths and exact release identity."""

    expected_directory: Path
    runner_temp: Path
    release_id: int
    release_tag: str
    release_title: str
    use_existing_plan: bool


class PublicReleaseVerificationError(RuntimeError):
    """The bounded public consumer observation failed closed."""

    def __init__(self, message: str, *, code: str) -> None:
        super().__init__(message)
        self.code = code


class _TlsPeer(Protocol):
    context: ssl.SSLContext
    server_side: bool
    server_hostname: str | None
    session_reused: bool

    def getpeercert(self, binary_form: bool = False) -> object: ...

    def version(self) -> str | None: ...

    def cipher(self) -> tuple[str, str, int] | None: ...

    def compression(self) -> str | None: ...

    def selected_alpn_protocol(self) -> str | None: ...


def main(
    argv: Sequence[str] | None = None,
    *,
    environment: Mapping[str, str] | None = None,
) -> int:
    """Run one credential-free, bounded public release consumer observation."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expected_directory", type=Path)
    parser.add_argument("--use-existing-plan", action="store_true")
    args = parser.parse_args(argv)
    values = os.environ if environment is None else environment
    try:
        context = _context(args, values)
        count, total = verify_public_release(context)
    except PublicReleaseVerificationError as error:
        print(
            _json(
                {
                    "protocol": _PROTOCOL,
                    "status": "fail",
                    "code": error.code,
                    "message": str(error),
                }
            ),
            file=sys.stderr,
        )
        return 1
    print(
        _json(
            {
                "protocol": _PROTOCOL,
                "status": "pass",
                "assets": count,
                "bytes": total,
            }
        )
    )
    return 0


def verify_public_release(context: VerificationContext) -> tuple[int, int]:
    """Retrieve, revalidate, and smoke one exact public release."""

    plan = context.runner_temp / "release-assets.plan"
    public_document = context.runner_temp / "release-public.json"
    public_directory = context.runner_temp / "release-public-download"
    if public_document.exists() or public_directory.exists():
        raise PublicReleaseVerificationError(
            "public release output already exists",
            code="public_release.output_exists",
        )
    if context.use_existing_plan:
        if plan.is_symlink() or not plan.is_file():
            raise PublicReleaseVerificationError(
                "existing release plan is unavailable",
                code="public_release.plan_unavailable",
            )
    elif plan.exists():
        raise PublicReleaseVerificationError(
            "fresh release plan path already exists",
            code="public_release.plan_exists",
        )

    release_url = f"https://{_API_HOST}/repos/{_REPOSITORY}/releases/{context.release_id}"
    _download(
        release_url,
        public_document,
        accept="application/vnd.github+json",
        maximum_bytes=_MAX_DOCUMENT_BYTES,
        maximum_redirects=0,
    )
    verify_arguments = [
        str(context.expected_directory),
        str(public_document),
        "--expected-tag",
        context.release_tag,
        "--expected-title",
        context.release_title,
        "--expected-state",
        "published",
    ]
    if not context.use_existing_plan:
        verify_arguments.extend(("--asset-plan", str(plan)))
    if _run_release_validator(verify_arguments) != 0:
        raise PublicReleaseVerificationError(
            "public release document does not match the admitted candidate",
            code="public_release.document_mismatch",
        )

    items = _asset_plan(plan)
    try:
        public_directory.mkdir()
    except OSError as error:
        raise PublicReleaseVerificationError(
            "public release output could not be created",
            code="public_release.output_failed",
        ) from error
    for item in items:
        asset_url = f"https://{_API_HOST}/repos/{_REPOSITORY}/releases/assets/{item.asset_id}"
        _download(
            asset_url,
            public_directory / item.name,
            accept="application/octet-stream",
            maximum_bytes=item.bytes,
            maximum_redirects=_MAX_ASSET_REDIRECTS,
            expected_bytes=item.bytes,
            partial_name=f".asset-{item.asset_id}.part",
        )

    final_arguments = [
        str(public_directory),
        str(public_document),
        "--expected-tag",
        context.release_tag,
        "--expected-title",
        context.release_title,
        "--expected-state",
        "published",
    ]
    if _run_release_validator(final_arguments) != 0:
        raise PublicReleaseVerificationError(
            "downloaded public assets do not match the release document",
            code="public_release.asset_mismatch",
        )
    try:
        smoke_result = smoke_release.main([str(public_directory)])
    except (OSError, RuntimeError, ValueError) as error:
        raise PublicReleaseVerificationError(
            "installed public release smoke failed",
            code="public_release.smoke_failed",
        ) from error
    if smoke_result != 0:
        raise PublicReleaseVerificationError(
            "installed public release smoke failed",
            code="public_release.smoke_failed",
        )
    return len(items), sum(item.bytes for item in items)


def _context(args: argparse.Namespace, environment: Mapping[str, str]) -> VerificationContext:
    if environment.get("GITHUB_REPOSITORY") != _REPOSITORY:
        raise PublicReleaseVerificationError(
            "unexpected release repository",
            code="public_release.invalid_repository",
        )
    if environment.get("GH_TOKEN") or environment.get("GITHUB_TOKEN"):
        raise PublicReleaseVerificationError(
            "public release requests must not receive a release credential",
            code="public_release.credential_present",
        )
    release_id_text = environment.get("RELEASE_ID", "")
    if _ID_PATTERN.fullmatch(release_id_text) is None:
        raise PublicReleaseVerificationError(
            "public release id is invalid",
            code="public_release.invalid_identity",
        )
    release_id = int(release_id_text)
    if release_id > _MAX_RELEASE_ID:
        raise PublicReleaseVerificationError(
            "public release id is invalid",
            code="public_release.invalid_identity",
        )
    release_tag = environment.get("GITHUB_REF_NAME", "")
    release_title = environment.get("RELEASE_TITLE", "")
    if not release_tag or not release_title:
        raise PublicReleaseVerificationError(
            "public release identity is unavailable",
            code="public_release.invalid_identity",
        )
    expected = _path_argument(args, "expected_directory")
    if expected.is_symlink() or not expected.is_dir():
        raise PublicReleaseVerificationError(
            "expected release directory is unavailable",
            code="public_release.candidate_unavailable",
        )
    runner_temp_text = environment.get("RUNNER_TEMP", "")
    runner_temp = Path(runner_temp_text) if runner_temp_text else Path()
    if not runner_temp_text or runner_temp.is_symlink() or not runner_temp.is_dir():
        raise PublicReleaseVerificationError(
            "runner temporary directory is unavailable",
            code="public_release.temp_unavailable",
        )
    return VerificationContext(
        expected_directory=expected,
        runner_temp=runner_temp,
        release_id=release_id,
        release_tag=release_tag,
        release_title=release_title,
        use_existing_plan=bool(args.use_existing_plan),
    )


def _asset_plan(path: Path) -> tuple[AssetPlanItem, ...]:
    try:
        if path.is_symlink() or not path.is_file():
            raise OSError
        with path.open("rb") as stream:
            raw = stream.read(_MAX_PLAN_BYTES + 1)
    except OSError as error:
        raise PublicReleaseVerificationError(
            "release asset plan is unavailable",
            code="public_release.plan_unavailable",
        ) from error
    if len(raw) > _MAX_PLAN_BYTES:
        raise PublicReleaseVerificationError(
            "release asset plan exceeds the size limit",
            code="public_release.invalid_plan",
        )
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError as error:
        raise PublicReleaseVerificationError(
            "release asset plan is not strict UTF-8",
            code="public_release.invalid_plan",
        ) from error
    if not lines or lines[0] != _PLAN_PROTOCOL or not 1 <= len(lines) - 1 <= _MAX_ASSETS:
        raise PublicReleaseVerificationError(
            "release asset plan has an invalid protocol or count",
            code="public_release.invalid_plan",
        )
    items: list[AssetPlanItem] = []
    asset_ids: set[int] = set()
    names: set[str] = set()
    total = 0
    for line in lines[1:]:
        fields = line.split("\t")
        if len(fields) != 3:
            raise PublicReleaseVerificationError(
                "release asset plan contains an invalid record",
                code="public_release.invalid_plan",
            )
        asset_id_text, size_text, name = fields
        if (
            _ID_PATTERN.fullmatch(asset_id_text) is None
            or _SIZE_PATTERN.fullmatch(size_text) is None
            or _NAME_PATTERN.fullmatch(name) is None
        ):
            raise PublicReleaseVerificationError(
                "release asset plan contains an invalid record",
                code="public_release.invalid_plan",
            )
        asset_id = int(asset_id_text)
        size = int(size_text)
        if (
            asset_id > _MAX_RELEASE_ID
            or size > _MAX_ASSET_BYTES
            or asset_id in asset_ids
            or name in names
        ):
            raise PublicReleaseVerificationError(
                "release asset plan contains an invalid or duplicate record",
                code="public_release.invalid_plan",
            )
        total += size
        if total > _MAX_TOTAL_BYTES:
            raise PublicReleaseVerificationError(
                "release asset plan exceeds the total size limit",
                code="public_release.invalid_plan",
            )
        asset_ids.add(asset_id)
        names.add(name)
        items.append(AssetPlanItem(asset_id, size, name))
    return tuple(items)


def _download(
    url: str,
    target: Path,
    *,
    accept: str,
    maximum_bytes: int,
    maximum_redirects: int,
    expected_bytes: int | None = None,
    partial_name: str | None = None,
) -> None:
    if target.exists():
        raise PublicReleaseVerificationError(
            "public release target already exists",
            code="public_release.output_exists",
        )
    partial = target if partial_name is None else target.parent / partial_name
    if partial.exists():
        raise PublicReleaseVerificationError(
            "public release partial target already exists",
            code="public_release.output_exists",
        )
    deadline = time.monotonic() + _REQUEST_TIMEOUT_SECONDS
    current_url = url
    redirects = 0
    while True:
        parsed = _https_url(current_url)
        hostname = parsed.hostname
        assert hostname is not None
        reference_hostname = _tls_reference_hostname(hostname)
        tls_context = _public_tls_context()
        try:
            connection = http.client.HTTPSConnection(
                reference_hostname,
                parsed.port,
                timeout=min(_CONNECT_TIMEOUT_SECONDS, _remaining(deadline)),
                context=tls_context,
            )
        except (OSError, ValueError) as error:
            raise PublicReleaseVerificationError(
                "public release request failed",
                code="public_release.request_failed",
            ) from error
        response: http.client.HTTPResponse | None = None
        try:
            _connect_public_peer(connection, deadline)
            _validate_tls_context_binding(connection, tls_context)
            _validate_tls_session_freshness(connection)
            _validate_tls_identity(connection, reference_hostname)
            _validate_tls_session(connection)
            path = urlunsplit(("", "", parsed.path or "/", parsed.query, ""))
            headers = {
                "Accept": accept,
                "Accept-Encoding": "identity",
                "Connection": "close",
                "User-Agent": "LudoWeave-release-verifier/1",
            }
            if hostname == _API_HOST:
                headers["X-GitHub-Api-Version"] = _API_VERSION
            connection.request(
                "GET",
                path,
                headers=headers,
            )
            _set_socket_timeout(connection, deadline)
            response = connection.getresponse()
            length_header = _validate_http_response_framing(response)
            status = _validate_http_response_status(response)
            if status == 302:
                next_url = _validated_redirect_url(current_url, response)
                redirects += 1
                if redirects > maximum_redirects:
                    raise PublicReleaseVerificationError(
                        "public release redirect is invalid",
                        code="public_release.redirect_failed",
                    )
                current_url = next_url
                continue
            if 300 <= status < 400:
                raise PublicReleaseVerificationError(
                    "public release redirect is invalid",
                    code="public_release.redirect_failed",
                )
            if status != 200:
                raise PublicReleaseVerificationError(
                    "public release request failed",
                    code="public_release.request_failed",
                )
            declared_bytes: int | None = None
            if length_header is not None:
                if not length_header.isascii() or not length_header.isdecimal():
                    raise PublicReleaseVerificationError(
                        "public release response length is invalid",
                        code="public_release.size_mismatch",
                    )
                declared_bytes = int(length_header)
                if declared_bytes > maximum_bytes or (
                    expected_bytes is not None and declared_bytes != expected_bytes
                ):
                    raise PublicReleaseVerificationError(
                        "public release response length does not match",
                        code="public_release.size_mismatch",
                    )
            received = _stream_response(
                response,
                connection,
                partial,
                maximum_bytes=maximum_bytes,
                deadline=deadline,
            )
            if declared_bytes is not None and received != declared_bytes:
                raise PublicReleaseVerificationError(
                    "public release response length does not match",
                    code="public_release.size_mismatch",
                )
            if expected_bytes is not None and received != expected_bytes:
                raise PublicReleaseVerificationError(
                    "public release response length does not match",
                    code="public_release.size_mismatch",
                )
            if partial != target:
                _publish_partial(partial, target)
            return
        except PublicReleaseVerificationError:
            raise
        except TimeoutError as error:
            raise PublicReleaseVerificationError(
                "public release request exceeded the time limit",
                code="public_release.request_timeout",
            ) from error
        except (OSError, http.client.HTTPException, ValueError) as error:
            raise PublicReleaseVerificationError(
                "public release request failed",
                code="public_release.request_failed",
            ) from error
        finally:
            if response is not None:
                response.close()
            connection.close()


def _validate_http_response_framing(
    response: http.client.HTTPResponse,
) -> str | None:
    """Require the documented HTTP/1.1-class response and safe framing metadata."""

    try:
        version = cast(object, response.version)
        transfer_encoding = cast(object, response.getheader("Transfer-Encoding"))
        content_length = cast(object, response.getheader("Content-Length"))
    except (
        AttributeError,
        http.client.HTTPException,
        NotImplementedError,
        OSError,
        TypeError,
        ValueError,
    ) as error:
        raise PublicReleaseVerificationError(
            "public release HTTP response framing failed",
            code="public_release.request_failed",
        ) from error
    if (
        not isinstance(version, int)
        or isinstance(version, bool)
        or version != 11
        or (
            transfer_encoding is not None
            and (
                not isinstance(transfer_encoding, str)
                or transfer_encoding.casefold() != "chunked"
                or content_length is not None
            )
        )
        or (content_length is not None and not isinstance(content_length, str))
    ):
        raise PublicReleaseVerificationError(
            "public release HTTP response framing failed",
            code="public_release.request_failed",
        )
    return content_length


def _validate_http_response_status(response: http.client.HTTPResponse) -> int:
    """Return one documented HTTP status-code integer or fail content-silently."""

    try:
        status = cast(object, response.status)
    except (
        AttributeError,
        http.client.HTTPException,
        NotImplementedError,
        OSError,
        TypeError,
        ValueError,
    ) as error:
        raise PublicReleaseVerificationError(
            "public release HTTP response status failed",
            code="public_release.request_failed",
        ) from error
    if not isinstance(status, int) or isinstance(status, bool) or not 100 <= status <= 599:
        raise PublicReleaseVerificationError(
            "public release HTTP response status failed",
            code="public_release.request_failed",
        )
    return status


def _validated_redirect_url(
    current_url: str,
    response: http.client.HTTPResponse,
) -> str:
    """Resolve exactly one bounded Location URI-reference and revalidate it."""

    try:
        raw_headers = cast(object, response.getheaders())
    except (
        AttributeError,
        http.client.HTTPException,
        NotImplementedError,
        OSError,
        TypeError,
        ValueError,
    ) as error:
        raise PublicReleaseVerificationError(
            "public release redirect is invalid",
            code="public_release.redirect_failed",
        ) from error
    if not isinstance(raw_headers, list):
        raise PublicReleaseVerificationError(
            "public release redirect is invalid",
            code="public_release.redirect_failed",
        )
    locations: list[str] = []
    for raw_header in cast(list[object], raw_headers):
        if not isinstance(raw_header, tuple):
            raise PublicReleaseVerificationError(
                "public release redirect is invalid",
                code="public_release.redirect_failed",
            )
        header = cast(tuple[object, ...], raw_header)
        if len(header) != 2 or not isinstance(header[0], str) or not isinstance(header[1], str):
            raise PublicReleaseVerificationError(
                "public release redirect is invalid",
                code="public_release.redirect_failed",
            )
        name = header[0]
        value = header[1]
        if name.casefold() == "location":
            locations.append(value)
    if len(locations) != 1:
        raise PublicReleaseVerificationError(
            "public release redirect is invalid",
            code="public_release.redirect_failed",
        )
    location = locations[0]
    if (
        len(location) > _MAX_REDIRECT_URI_OCTETS
        or _URI_REFERENCE_PATTERN.fullmatch(location) is None
    ):
        raise PublicReleaseVerificationError(
            "public release redirect is invalid",
            code="public_release.redirect_failed",
        )
    try:
        reference = urlsplit(location)
        if any(
            bracket in component
            for component in (reference.path, reference.query, reference.fragment)
            for bracket in "[]"
        ):
            raise ValueError("bracket delimiter outside URI authority")
        first_path_segment = reference.path.split("/", 1)[0]
        if (
            not reference.scheme
            and not reference.netloc
            and not reference.path.startswith("/")
            and ":" in first_path_segment
        ):
            raise ValueError("relative path starts with a scheme-like segment")
        next_url = urljoin(current_url, location)
    except (TypeError, ValueError) as error:
        raise PublicReleaseVerificationError(
            "public release redirect is invalid",
            code="public_release.redirect_failed",
        ) from error
    _https_url(next_url)
    return next_url


def _public_tls_context() -> ssl.SSLContext:
    """Create one verified client context without ambient TLS key logging."""

    try:
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        context.verify_flags |= ssl.VERIFY_X509_PARTIAL_CHAIN
        context.verify_flags |= ssl.VERIFY_X509_STRICT
        context.load_default_certs(ssl.Purpose.SERVER_AUTH)
        context.set_alpn_protocols([_HTTP_ALPN])
    except (NotImplementedError, OSError, ValueError) as error:
        raise PublicReleaseVerificationError(
            "public release TLS context failed",
            code="public_release.tls_failed",
        ) from error
    _require_public_tls_context(context)
    return context


def _require_public_tls_context(context: ssl.SSLContext) -> None:
    """Require the complete per-hop client verification policy."""

    if (
        context.protocol != ssl.PROTOCOL_TLS_CLIENT
        or context.verify_mode != ssl.CERT_REQUIRED
        or not context.check_hostname
        or context.minimum_version != ssl.TLSVersion.TLSv1_2
        or context.verify_flags & _REQUIRED_TLS_VERIFY_FLAGS != _REQUIRED_TLS_VERIFY_FLAGS
        or getattr(context, "keylog_filename", None) is not None
    ):
        raise PublicReleaseVerificationError(
            "public release TLS context failed",
            code="public_release.tls_failed",
        )


def _validate_tls_context_binding(
    connection: http.client.HTTPSConnection,
    expected_context: ssl.SSLContext,
) -> None:
    """Require the connected client socket to retain the exact verified context."""

    socket = connection.sock
    if socket is None:
        raise PublicReleaseVerificationError(
            "public release TLS context binding failed",
            code="public_release.tls_failed",
        )
    peer = cast(_TlsPeer, socket)
    try:
        actual_context: object = peer.context
        server_side: object = peer.server_side
    except (AttributeError, NotImplementedError, OSError, TypeError, ValueError) as error:
        raise PublicReleaseVerificationError(
            "public release TLS context binding failed",
            code="public_release.tls_failed",
        ) from error
    if actual_context is not expected_context or server_side is not False:
        raise PublicReleaseVerificationError(
            "public release TLS context binding failed",
            code="public_release.tls_failed",
        )
    _require_public_tls_context(expected_context)


def _validate_tls_session_freshness(
    connection: http.client.HTTPSConnection,
) -> None:
    """Reject TLS session resumption before later evidence or HTTP."""

    socket = connection.sock
    if socket is None:
        raise PublicReleaseVerificationError(
            "public release TLS session freshness failed",
            code="public_release.tls_failed",
        )
    peer = cast(_TlsPeer, socket)
    try:
        session_reused: object = peer.session_reused
    except (AttributeError, NotImplementedError, OSError, TypeError, ValueError) as error:
        raise PublicReleaseVerificationError(
            "public release TLS session freshness failed",
            code="public_release.tls_failed",
        ) from error
    if session_reused is not False:
        raise PublicReleaseVerificationError(
            "public release TLS session freshness failed",
            code="public_release.tls_failed",
        )


def _validate_tls_session(connection: http.client.HTTPSConnection) -> None:
    """Reject an unexpected negotiated TLS session before HTTP transmission."""

    socket = connection.sock
    if socket is None:
        raise PublicReleaseVerificationError(
            "public release TLS session failed",
            code="public_release.tls_failed",
        )
    peer = cast(_TlsPeer, socket)
    try:
        version: object = peer.version()
        cipher: object = peer.cipher()
        compression: object = peer.compression()
        alpn: object = peer.selected_alpn_protocol()
    except (AttributeError, NotImplementedError, OSError, TypeError, ValueError) as error:
        raise PublicReleaseVerificationError(
            "public release TLS session failed",
            code="public_release.tls_failed",
        ) from error
    if not isinstance(cipher, tuple) or len(cipher) != 3:
        raise PublicReleaseVerificationError(
            "public release TLS session failed",
            code="public_release.tls_failed",
        )
    cipher_parts = cast(tuple[object, ...], cipher)
    name, cipher_protocol, secret_bits = cipher_parts
    if (
        not isinstance(version, str)
        or version not in _ALLOWED_TLS_VERSIONS
        or not isinstance(name, str)
        or not name
        or not isinstance(cipher_protocol, str)
        or not cipher_protocol
        or not isinstance(secret_bits, int)
        or isinstance(secret_bits, bool)
        or secret_bits < _MINIMUM_TLS_SECRET_BITS
        or compression is not None
        or alpn not in (None, _HTTP_ALPN)
    ):
        raise PublicReleaseVerificationError(
            "public release TLS session failed",
            code="public_release.tls_failed",
        )


def _validate_tls_identity(
    connection: http.client.HTTPSConnection,
    reference_hostname: str,
) -> None:
    """Require the verified socket to retain its URL-derived service identity."""

    socket = connection.sock
    if socket is None:
        raise PublicReleaseVerificationError(
            "public release TLS identity failed",
            code="public_release.tls_failed",
        )
    peer = cast(_TlsPeer, socket)
    try:
        server_hostname: object = peer.server_hostname
        certificate: object = peer.getpeercert(binary_form=True)
    except (
        AttributeError,
        NotImplementedError,
        OSError,
        TypeError,
        ValueError,
    ) as error:
        raise PublicReleaseVerificationError(
            "public release TLS identity failed",
            code="public_release.tls_failed",
        ) from error
    if (
        not reference_hostname
        or not isinstance(server_hostname, str)
        or not server_hostname
        or not server_hostname.isascii()
        or server_hostname.casefold() != reference_hostname.casefold()
        or not isinstance(certificate, bytes)
        or not certificate
    ):
        raise PublicReleaseVerificationError(
            "public release TLS identity failed",
            code="public_release.tls_failed",
        )


def _tls_reference_hostname(hostname: str) -> str:
    """Return the bounded ASCII reference hostname before opening a connection."""

    try:
        reference_hostname = hostname.encode("idna").decode("ascii")
    except UnicodeError as error:
        raise PublicReleaseVerificationError(
            "public release TLS identity failed",
            code="public_release.tls_failed",
        ) from error
    if not reference_hostname:
        raise PublicReleaseVerificationError(
            "public release TLS identity failed",
            code="public_release.tls_failed",
        )
    return reference_hostname


def _connect_public_peer(
    connection: http.client.HTTPSConnection,
    deadline: float,
) -> None:
    """Connect and reject a non-global peer before transmitting HTTP."""

    if connection.sock is None:
        connection.connect()
    socket = connection.sock
    if socket is None:
        raise PublicReleaseVerificationError(
            "public release peer is unavailable",
            code="public_release.request_failed",
        )
    _set_socket_timeout(connection, deadline)
    try:
        peer: object = socket.getpeername()
    except TimeoutError:
        raise
    except OSError as error:
        raise PublicReleaseVerificationError(
            "public release peer is unavailable",
            code="public_release.request_failed",
        ) from error
    if not isinstance(peer, tuple):
        raise PublicReleaseVerificationError(
            "public release peer is unavailable",
            code="public_release.request_failed",
        )
    peer_parts = cast(tuple[object, ...], peer)
    if len(peer_parts) < 2 or not isinstance(peer_parts[0], str) or peer_parts[1] != 443:
        raise PublicReleaseVerificationError(
            "public release peer is unavailable",
            code="public_release.request_failed",
        )
    try:
        address = ipaddress.ip_address(peer_parts[0].split("%", 1)[0])
    except ValueError as error:
        raise PublicReleaseVerificationError(
            "public release peer address is invalid",
            code="public_release.request_failed",
        ) from error
    if isinstance(address, ipaddress.IPv6Address) and address.ipv4_mapped is not None:
        address = address.ipv4_mapped
    if (
        not address.is_global
        or address.is_multicast
        or address.is_reserved
        or address.is_unspecified
        or (isinstance(address, ipaddress.IPv6Address) and address.is_site_local)
    ):
        raise PublicReleaseVerificationError(
            "public release peer is not globally reachable",
            code="public_release.peer_forbidden",
        )


def _stream_response(
    response: http.client.HTTPResponse,
    connection: http.client.HTTPSConnection,
    target: Path,
    *,
    maximum_bytes: int,
    deadline: float,
) -> int:
    received = 0
    try:
        with target.open("xb") as stream:
            while True:
                _set_socket_timeout(connection, deadline)
                block = _read_response_block(
                    response,
                    min(_READ_BYTES, maximum_bytes + 1 - received),
                )
                if not block:
                    break
                received += len(block)
                if received > maximum_bytes:
                    raise PublicReleaseVerificationError(
                        "public release response exceeds the size limit",
                        code="public_release.size_mismatch",
                    )
                stream.write(block)
    except FileExistsError as error:
        raise PublicReleaseVerificationError(
            "public release target already exists",
            code="public_release.output_exists",
        ) from error
    except OSError as error:
        raise PublicReleaseVerificationError(
            "public release output could not be written",
            code="public_release.output_failed",
        ) from error
    return received


def _set_socket_timeout(connection: http.client.HTTPSConnection, deadline: float) -> None:
    socket = connection.sock
    if socket is None:
        return
    try:
        socket.settimeout(min(_CONNECT_TIMEOUT_SECONDS, _remaining(deadline)))
    except TimeoutError as error:
        raise PublicReleaseVerificationError(
            "public release request exceeded the time limit",
            code="public_release.request_timeout",
        ) from error
    except OSError as error:
        raise PublicReleaseVerificationError(
            "public release request failed",
            code="public_release.request_failed",
        ) from error


def _read_response_block(response: http.client.HTTPResponse, amount: int) -> bytes:
    try:
        block = cast(object, response.read(amount))
    except TimeoutError as error:
        raise PublicReleaseVerificationError(
            "public release request exceeded the time limit",
            code="public_release.request_timeout",
        ) from error
    except (
        AttributeError,
        http.client.HTTPException,
        NotImplementedError,
        OSError,
        TypeError,
        ValueError,
    ) as error:
        raise PublicReleaseVerificationError(
            "public release request failed",
            code="public_release.request_failed",
        ) from error
    if type(block) is not bytes or len(block) > amount:
        raise PublicReleaseVerificationError(
            "public release response body is invalid",
            code="public_release.request_failed",
        )
    return block


def _publish_partial(partial: Path, target: Path) -> None:
    try:
        os.link(partial, target)
    except FileExistsError as error:
        raise PublicReleaseVerificationError(
            "public release target already exists",
            code="public_release.output_exists",
        ) from error
    except OSError as error:
        raise PublicReleaseVerificationError(
            "public release output could not be finalized",
            code="public_release.output_failed",
        ) from error
    try:
        partial.unlink()
    except OSError as error:
        raise PublicReleaseVerificationError(
            "public release partial could not be removed",
            code="public_release.output_failed",
        ) from error


def _run_release_validator(arguments: Sequence[str]) -> int:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return verify_release_draft.main(arguments)


def _https_url(url: str) -> SplitResult:
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError as error:
        raise PublicReleaseVerificationError(
            "public release URL is invalid",
            code="public_release.redirect_failed",
        ) from error
    if (
        parsed.scheme != "https"
        or not parsed.hostname
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
        or port not in (None, 443)
    ):
        raise PublicReleaseVerificationError(
            "public release URL must remain bounded HTTPS",
            code="public_release.redirect_failed",
        )
    return parsed


def _remaining(deadline: float) -> float:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise PublicReleaseVerificationError(
            "public release request exceeded the time limit",
            code="public_release.request_timeout",
        )
    return remaining


def _path_argument(args: argparse.Namespace, name: str) -> Path:
    value: object = getattr(args, name, None)
    if not isinstance(value, Path):
        raise TypeError(f"{name} must be a path")
    return value


def _json(value: object) -> str:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")
    )


if __name__ == "__main__":
    raise SystemExit(main())
