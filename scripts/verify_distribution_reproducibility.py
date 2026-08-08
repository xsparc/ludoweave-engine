"""Fail closed unless two LudoWeave distribution builds are byte-identical."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

_PROTOCOL = "ludoweave.distribution-reproducibility/1"
_IGNORED_FILES = frozenset({".gitignore"})


@dataclass(frozen=True, slots=True)
class ArtifactDigest:
    """Stable identity for one built distribution artifact."""

    name: str
    bytes: int
    sha256: str


class DistributionReproducibilityError(ValueError):
    """A distribution directory or byte comparison is invalid."""

    def __init__(self, message: str, *, code: str) -> None:
        super().__init__(message)
        self.code = code


def verify_distributions(first: Path, second: Path) -> tuple[ArtifactDigest, ...]:
    """Return stable artifact identities when two independent builds match."""

    first_root = _directory(first, role="first")
    second_root = _directory(second, role="second")
    if first_root == second_root:
        raise DistributionReproducibilityError(
            "distribution builds must use distinct directories",
            code="distribution.same_directory",
        )

    first_files = _distribution_files(first_root, role="first")
    second_files = _distribution_files(second_root, role="second")
    if first_files.keys() != second_files.keys():
        raise DistributionReproducibilityError(
            "distribution builds contain different artifact names",
            code="distribution.name_mismatch",
        )

    artifacts: list[ArtifactDigest] = []
    for name in first_files:
        first_digest = _digest(first_files[name])
        second_digest = _digest(second_files[name])
        if first_digest != second_digest:
            raise DistributionReproducibilityError(
                f"distribution artifact is not byte-reproducible: {name}",
                code="distribution.bytes_mismatch",
            )
        artifacts.append(ArtifactDigest(name, first_digest[0], first_digest[1]))
    return tuple(artifacts)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("first", type=Path, help="first distribution build directory")
    parser.add_argument("second", type=Path, help="independent repeat build directory")
    args = parser.parse_args(argv)
    try:
        artifacts = verify_distributions(Path(args.first), Path(args.second))
    except DistributionReproducibilityError as error:
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
                "artifacts": [
                    {"name": item.name, "bytes": item.bytes, "sha256": item.sha256}
                    for item in artifacts
                ],
            }
        )
    )
    return 0


def _directory(value: Path, *, role: str) -> Path:
    try:
        resolved = value.resolve(strict=True)
    except OSError as error:
        raise DistributionReproducibilityError(
            f"{role} distribution directory is unavailable",
            code="distribution.invalid_directory",
        ) from error
    if not resolved.is_dir():
        raise DistributionReproducibilityError(
            f"{role} distribution path must be a directory",
            code="distribution.invalid_directory",
        )
    return resolved


def _distribution_files(root: Path, *, role: str) -> dict[str, Path]:
    files: dict[str, Path] = {}
    try:
        entries = sorted(root.iterdir(), key=lambda item: item.name)
    except OSError as error:
        raise DistributionReproducibilityError(
            f"{role} distribution directory could not be read",
            code="distribution.read_failed",
        ) from error
    for path in entries:
        if path.name in _IGNORED_FILES:
            if path.is_symlink() or not path.is_file():
                raise DistributionReproducibilityError(
                    f"{role} distribution contains an invalid ignored entry",
                    code="distribution.invalid_entry",
                )
            continue
        if path.is_symlink() or not path.is_file():
            raise DistributionReproducibilityError(
                f"{role} distribution contains a non-file entry: {path.name}",
                code="distribution.invalid_entry",
            )
        files[path.name] = path

    wheels = tuple(name for name in files if name.endswith(".whl"))
    sdists = tuple(name for name in files if name.endswith(".tar.gz"))
    if len(files) != 2 or len(wheels) != 1 or len(sdists) != 1:
        raise DistributionReproducibilityError(
            f"{role} distribution must contain exactly one wheel and one source archive",
            code="distribution.invalid_artifact_set",
        )
    wheel = wheels[0]
    sdist = sdists[0]
    wheel_identity = wheel.removesuffix("-py3-none-any.whl")
    sdist_identity = sdist.removesuffix(".tar.gz")
    if (
        not wheel.endswith("-py3-none-any.whl")
        or not wheel_identity.startswith("ludoweave-")
        or wheel_identity == "ludoweave-"
        or wheel_identity != sdist_identity
    ):
        raise DistributionReproducibilityError(
            f"{role} distribution filenames do not describe one pure-Python build",
            code="distribution.invalid_artifact_name",
        )
    return dict(sorted(files.items()))


def _digest(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    try:
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b""):
                size += len(block)
                digest.update(block)
    except OSError as error:
        raise DistributionReproducibilityError(
            f"distribution artifact could not be read: {path.name}",
            code="distribution.read_failed",
        ) from error
    return size, digest.hexdigest()


def _json(value: object) -> str:
    return json.dumps(
        value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")
    )


if __name__ == "__main__":
    raise SystemExit(main())
