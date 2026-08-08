"""Fail closed unless published release assets have exact GitHub attestations."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

_PROTOCOL = "ludoweave.release-attestation-integrity/1"
_ASSET_PLAN_PROTOCOL = "ludoweave.release-asset-retrieval-plan/1"
_EXPECTED_REPOSITORY = "xsparc/ludoweave-engine"
_EXPECTED_SIGNER_WORKFLOW = "xsparc/ludoweave-engine/.github/workflows/release.yml"
_PROVENANCE_PREDICATE = "https://slsa.dev/provenance/v1"
_SBOM_PREDICATE = "https://spdx.dev/Document/v2.3"
_OIDC_ISSUER = "https://token.actions.githubusercontent.com"
_MAX_PLAN_BYTES = 16 * 1024
_MAX_ASSETS = 32
_MAX_ASSET_BYTES = 256 * 1024 * 1024
_MAX_TOTAL_BYTES = 512 * 1024 * 1024
_MAX_ASSET_ID = (1 << 63) - 1
_ATTESTATION_LIMIT = 30
_VERIFY_TIMEOUT_SECONDS = 30.0
_TAG_PATTERN = re.compile(r"v[0-9A-Za-z][0-9A-Za-z._-]{0,127}")
_COMMIT_PATTERN = re.compile(r"[0-9a-f]{40}")
_ASSET_ID_PATTERN = re.compile(r"[1-9][0-9]{0,18}")
_SIZE_PATTERN = re.compile(r"0|[1-9][0-9]{0,8}")
_NAME_PATTERN = re.compile(r"[0-9A-Za-z][0-9A-Za-z._+-]{0,255}")
_WHEEL_PATTERN = re.compile(r"ludoweave-[0-9A-Za-z][0-9A-Za-z._+-]{0,127}-py3-none-any\.whl")

CommandRunner = Callable[[tuple[str, ...]], None]


@dataclass(frozen=True, slots=True)
class PlannedAsset:
    """Validated local identity admitted by the M43 retrieval plan."""

    asset_id: int
    bytes: int
    name: str


@dataclass(frozen=True, slots=True)
class AttestationSummary:
    """Content-silent count of completed cryptographic checks."""

    assets: int
    provenance_checks: int
    sbom_checks: int


class ReleaseAttestationIntegrityError(ValueError):
    """Published release attestation evidence is invalid or unavailable."""

    def __init__(self, message: str, *, code: str) -> None:
        super().__init__(message)
        self.code = code


def verify_attestations(
    download_directory: Path,
    asset_plan: Path,
    *,
    expected_tag: str,
    expected_commit: str,
    run_command: CommandRunner | None = None,
) -> AttestationSummary:
    """Verify exact-source provenance for every asset and SPDX for the wheel."""

    tag = _tag(expected_tag)
    commit = _commit(expected_commit)
    root = _directory(download_directory)
    assets = _asset_plan(asset_plan)
    files = _downloaded_files(root, assets)
    wheel_names = tuple(name for name in files if _WHEEL_PATTERN.fullmatch(name))
    if len(wheel_names) != 1:
        raise ReleaseAttestationIntegrityError(
            "published asset set must contain exactly one pure LudoWeave wheel",
            code="release_attestation.invalid_wheel_set",
        )

    runner = _run_command if run_command is None else run_command
    for asset in assets:
        runner(
            _verification_command(
                files[asset.name],
                predicate_type=_PROVENANCE_PREDICATE,
                tag=tag,
                commit=commit,
            )
        )
    runner(
        _verification_command(
            files[wheel_names[0]],
            predicate_type=_SBOM_PREDICATE,
            tag=tag,
            commit=commit,
        )
    )
    return AttestationSummary(
        assets=len(assets),
        provenance_checks=len(assets),
        sbom_checks=1,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("download_directory", type=Path)
    parser.add_argument("asset_plan", type=Path)
    parser.add_argument("--expected-tag", required=True, help="exact vVERSION release tag")
    parser.add_argument(
        "--expected-commit",
        required=True,
        help="exact lowercase 40-character release commit",
    )
    args = parser.parse_args(argv)
    try:
        summary = verify_attestations(
            Path(args.download_directory),
            Path(args.asset_plan),
            expected_tag=str(args.expected_tag),
            expected_commit=str(args.expected_commit),
        )
    except ReleaseAttestationIntegrityError as error:
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
                "assets": summary.assets,
                "provenance_checks": summary.provenance_checks,
                "sbom_checks": summary.sbom_checks,
            }
        )
    )
    return 0


def _tag(value: str) -> str:
    if _TAG_PATTERN.fullmatch(value) is None:
        raise ReleaseAttestationIntegrityError(
            "expected release tag is invalid",
            code="release_attestation.invalid_identity",
        )
    return value


def _commit(value: str) -> str:
    if _COMMIT_PATTERN.fullmatch(value) is None:
        raise ReleaseAttestationIntegrityError(
            "expected release commit is invalid",
            code="release_attestation.invalid_identity",
        )
    return value


def _directory(value: Path) -> Path:
    try:
        if value.is_symlink():
            raise OSError
        resolved = value.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise ReleaseAttestationIntegrityError(
            "published asset directory is unavailable",
            code="release_attestation.invalid_directory",
        ) from error
    if not resolved.is_dir():
        raise ReleaseAttestationIntegrityError(
            "published asset path must be a directory",
            code="release_attestation.invalid_directory",
        )
    return resolved


def _asset_plan(path: Path) -> tuple[PlannedAsset, ...]:
    try:
        if path.is_symlink() or not path.is_file() or path.stat().st_size > _MAX_PLAN_BYTES:
            raise OSError
        with path.open("rb") as stream:
            payload = stream.read(_MAX_PLAN_BYTES + 1)
    except OSError as error:
        raise ReleaseAttestationIntegrityError(
            "asset retrieval plan is unavailable",
            code="release_attestation.invalid_plan",
        ) from error
    if len(payload) > _MAX_PLAN_BYTES:
        raise ReleaseAttestationIntegrityError(
            "asset retrieval plan exceeds the size limit",
            code="release_attestation.invalid_plan",
        )
    try:
        text = payload.decode("utf-8", errors="strict")
    except UnicodeDecodeError as error:
        raise ReleaseAttestationIntegrityError(
            "asset retrieval plan must be strict UTF-8",
            code="release_attestation.invalid_plan",
        ) from error
    if not text.endswith("\n") or "\r" in text or "\x00" in text:
        raise ReleaseAttestationIntegrityError(
            "asset retrieval plan is not canonical text",
            code="release_attestation.invalid_plan",
        )
    lines = text.removesuffix("\n").split("\n")
    if not lines or lines[0] != _ASSET_PLAN_PROTOCOL:
        raise ReleaseAttestationIntegrityError(
            "asset retrieval plan protocol is invalid",
            code="release_attestation.invalid_plan",
        )
    rows = lines[1:]
    if not rows or len(rows) > _MAX_ASSETS:
        raise ReleaseAttestationIntegrityError(
            "asset retrieval plan must contain a bounded non-empty set",
            code="release_attestation.invalid_plan",
        )

    assets: list[PlannedAsset] = []
    asset_ids: set[int] = set()
    names: set[str] = set()
    total = 0
    for row in rows:
        fields = row.split("\t")
        if len(fields) != 3:
            raise ReleaseAttestationIntegrityError(
                "asset retrieval plan row is invalid",
                code="release_attestation.invalid_plan",
            )
        asset_id_text, size_text, name = fields
        if (
            _ASSET_ID_PATTERN.fullmatch(asset_id_text) is None
            or int(asset_id_text) > _MAX_ASSET_ID
            or _SIZE_PATTERN.fullmatch(size_text) is None
            or int(size_text) > _MAX_ASSET_BYTES
            or _NAME_PATTERN.fullmatch(name) is None
        ):
            raise ReleaseAttestationIntegrityError(
                "asset retrieval plan row is invalid",
                code="release_attestation.invalid_plan",
            )
        asset_id = int(asset_id_text)
        size = int(size_text)
        if asset_id in asset_ids or name in names:
            raise ReleaseAttestationIntegrityError(
                "asset retrieval plan contains a duplicate identity",
                code="release_attestation.invalid_plan",
            )
        asset_ids.add(asset_id)
        names.add(name)
        total += size
        if total > _MAX_TOTAL_BYTES:
            raise ReleaseAttestationIntegrityError(
                "asset retrieval plan exceeds the total size limit",
                code="release_attestation.invalid_plan",
            )
        assets.append(PlannedAsset(asset_id, size, name))
    if tuple(asset.name for asset in assets) != tuple(sorted(names)):
        raise ReleaseAttestationIntegrityError(
            "asset retrieval plan names must be in canonical order",
            code="release_attestation.invalid_plan",
        )
    return tuple(assets)


def _downloaded_files(root: Path, assets: tuple[PlannedAsset, ...]) -> dict[str, Path]:
    try:
        entries = sorted(root.iterdir(), key=lambda item: item.name)
    except OSError as error:
        raise ReleaseAttestationIntegrityError(
            "published asset directory could not be read",
            code="release_attestation.read_failed",
        ) from error
    expected = {asset.name: asset for asset in assets}
    if tuple(path.name for path in entries) != tuple(sorted(expected)):
        raise ReleaseAttestationIntegrityError(
            "published asset directory differs from the retrieval plan",
            code="release_attestation.asset_set_mismatch",
        )
    files: dict[str, Path] = {}
    for path in entries:
        asset = expected[path.name]
        try:
            if path.is_symlink() or not path.is_file() or path.stat().st_size != asset.bytes:
                raise OSError
        except OSError as error:
            raise ReleaseAttestationIntegrityError(
                f"published asset does not match the retrieval plan: {asset.name}",
                code="release_attestation.asset_mismatch",
            ) from error
        files[asset.name] = path
    return files


def _verification_command(
    path: Path,
    *,
    predicate_type: str,
    tag: str,
    commit: str,
) -> tuple[str, ...]:
    return (
        "gh",
        "attestation",
        "verify",
        str(path),
        "--repo",
        _EXPECTED_REPOSITORY,
        "--predicate-type",
        predicate_type,
        "--signer-workflow",
        _EXPECTED_SIGNER_WORKFLOW,
        "--signer-digest",
        commit,
        "--source-ref",
        f"refs/tags/{tag}",
        "--source-digest",
        commit,
        "--cert-oidc-issuer",
        _OIDC_ISSUER,
        "--deny-self-hosted-runners",
        "--limit",
        str(_ATTESTATION_LIMIT),
    )


def _run_command(command: tuple[str, ...]) -> None:
    try:
        result = subprocess.run(
            command,
            check=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=_VERIFY_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as error:
        raise ReleaseAttestationIntegrityError(
            "GitHub attestation verification timed out",
            code="release_attestation.timeout",
        ) from error
    except OSError as error:
        raise ReleaseAttestationIntegrityError(
            "GitHub attestation verifier is unavailable",
            code="release_attestation.unavailable",
        ) from error
    if result.returncode != 0:
        raise ReleaseAttestationIntegrityError(
            "GitHub attestation verification failed",
            code="release_attestation.verification_failed",
        )


def _json(value: object) -> str:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")
    )


if __name__ == "__main__":
    raise SystemExit(main())
