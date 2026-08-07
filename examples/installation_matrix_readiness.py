"""Evaluate reviewed clean-install matrix evidence without claiming source CI as adoption."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Sequence
from datetime import date
from pathlib import Path
from typing import cast

from ludoweave import __version__

type _InstallationIdentity = tuple[
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    str,
    bool,
    bool,
    bool,
    bool,
    tuple[str, ...],
    bool,
    bool,
]

_SCHEMA = "ludoweave.evaluation.installation-matrix-readiness/1"
_MANIFEST_SCHEMA = "ludoweave.community.installation-matrix/1"
_REQUIRED_ENVIRONMENTS = (
    "ubuntu-cpython-3.12",
    "ubuntu-cpython-3.13",
    "ubuntu-cpython-3.14",
    "macos-cpython-3.12",
    "macos-cpython-3.14",
    "windows-cpython-3.12",
    "windows-cpython-3.14",
)
_ENVIRONMENT_CONTRACTS = {
    "ubuntu-cpython-3.12": ("linux", "3.12"),
    "ubuntu-cpython-3.13": ("linux", "3.13"),
    "ubuntu-cpython-3.14": ("linux", "3.14"),
    "macos-cpython-3.12": ("macos", "3.12"),
    "macos-cpython-3.14": ("macos", "3.14"),
    "windows-cpython-3.12": ("windows", "3.12"),
    "windows-cpython-3.14": ("windows", "3.14"),
}
_REQUIRED_CHECKS = (
    "version",
    "doctor",
    "hello-headless",
    "clockwork-arena-headless",
)
_REVIEWED_MATRIX_SHA256 = "7c05813a7304e8ff44a009ada37c8e60ff545baec633852fc332e46bdfe03c90"
_MANDATORY_INSTALLATION_PREFIX: tuple[_InstallationIdentity, ...] = ()
_MAX_MANIFEST_BYTES = 65_536
_MAX_JSON_NESTING = 16
_MAX_INSTALLATION_RECORDS = 16


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--matrix",
        type=Path,
        default=None,
        help="explicit local reviewed clean-install matrix manifest",
    )
    arguments = parser.parse_args(tuple(sys.argv[1:] if argv is None else argv))
    selected: object = getattr(arguments, "matrix", None)
    matrix = _default_matrix() if selected is None else _path(selected)
    print(json.dumps(evaluate(matrix), ensure_ascii=True, separators=(",", ":"), sort_keys=True))
    return 0


def evaluate(matrix: Path) -> dict[str, object]:
    """Return deterministic, path-free clean-install matrix evidence."""

    raw_manifest = _read_bounded(matrix, _MAX_MANIFEST_BYTES, "installation-matrix manifest")
    document = _object(
        _loads(raw_manifest, "installation-matrix manifest"),
        "installation-matrix manifest",
    )
    _exact_fields(
        document,
        {
            "schema",
            "source_project",
            "required_environments",
            "required_checks",
            "installation_records",
        },
        "installation-matrix manifest",
    )
    if document["schema"] != _MANIFEST_SCHEMA:
        raise RuntimeError("installation-matrix manifest schema is incompatible")
    if document["source_project"] != "ludoweave-engine":
        raise RuntimeError("installation-matrix project identity is invalid")
    required_environments = tuple(
        _bounded_ascii_text(item, 64, "required environment")
        for item in _list(document["required_environments"], "required environments")
    )
    if required_environments != _REQUIRED_ENVIRONMENTS:
        raise RuntimeError("installation-matrix required environments are incompatible")
    required_checks = tuple(
        _bounded_ascii_text(item, 64, "required check")
        for item in _list(document["required_checks"], "required checks")
    )
    if required_checks != _REQUIRED_CHECKS:
        raise RuntimeError("installation-matrix required checks are incompatible")

    raw_records = _list(document["installation_records"], "installation records")
    if len(raw_records) > _MAX_INSTALLATION_RECORDS:
        raise RuntimeError("installation-matrix manifest exceeds its record limit")
    identities: list[_InstallationIdentity] = []
    environments: set[str] = set()
    validation_urls: set[str] = set()
    log_hashes: set[str] = set()
    artifact: tuple[str, str, str, str, str] | None = None
    for item in raw_records:
        identity = _installation_identity(_object(item, "installation record"), required_checks)
        if identity[0] in environments:
            raise RuntimeError("installation-matrix manifest repeats an environment")
        if identity[8] in validation_urls:
            raise RuntimeError("installation-matrix manifest repeats a validation URL")
        if identity[9] in log_hashes:
            raise RuntimeError("installation-matrix manifest repeats an installation log")
        if identity[0] != required_environments[len(identities)]:
            raise RuntimeError("installation-matrix records must follow required environment order")
        record_artifact = identity[3:8]
        if artifact is None:
            artifact = record_artifact
        elif record_artifact != artifact:
            raise RuntimeError("installation-matrix records must share one release wheel")
        environments.add(identity[0])
        validation_urls.add(identity[8])
        log_hashes.add(identity[9])
        identities.append(identity)

    manifest_hash = hashlib.sha256(raw_manifest).hexdigest()
    manifest_identity_reviewed = manifest_hash == _REVIEWED_MATRIX_SHA256
    historical_matrix_preserved = tuple(
        identities[: len(_MANDATORY_INSTALLATION_PREFIX)]
    ) == _MANDATORY_INSTALLATION_PREFIX and (
        not manifest_identity_reviewed or len(identities) == len(_MANDATORY_INSTALLATION_PREFIX)
    )
    admitted = identities if manifest_identity_reviewed and historical_matrix_preserved else []
    admitted_environments = tuple(identity[0] for identity in admitted)
    complete_environment_matrix = set(admitted_environments) == set(required_environments) and len(
        admitted_environments
    ) == len(required_environments)
    immutable_release_artifact = bool(admitted)
    isolated_clean_install = bool(admitted) and all(
        identity[12] and identity[13] and identity[14] and identity[15] for identity in admitted
    )
    gate_satisfied = (
        manifest_identity_reviewed
        and historical_matrix_preserved
        and complete_environment_matrix
        and immutable_release_artifact
        and isolated_clean_install
    )
    reasons: list[str]
    if manifest_identity_reviewed and historical_matrix_preserved and not admitted:
        reasons = ["installation-matrix-evidence-absent"]
    else:
        reasons = []
        if not manifest_identity_reviewed:
            reasons.append("installation-matrix-manifest-identity-unreviewed")
        if not historical_matrix_preserved:
            reasons.append("historical-installation-matrix-record-missing")
        if not complete_environment_matrix:
            reasons.append("installation-matrix-incomplete")
        if not immutable_release_artifact:
            reasons.append("immutable-release-wheel-absent")
        if not isolated_clean_install:
            reasons.append("isolated-clean-install-absent")

    return {
        "admission": {
            "complete_environment_matrix": complete_environment_matrix,
            "historical_matrix_preserved": historical_matrix_preserved,
            "immutable_release_artifact": immutable_release_artifact,
            "isolated_clean_install": isolated_clean_install,
            "manifest_identity_reviewed": manifest_identity_reviewed,
            "reason_codes": tuple(reasons),
        },
        "evidence_level": (
            "reviewed-installation-matrix"
            if gate_satisfied
            else "installation-matrix-admission-readiness"
        ),
        "gate_satisfied": gate_satisfied,
        "installation": {
            "environments": admitted_environments,
            "manifest_sha256": manifest_hash,
            "records_verified": True,
            "release_versions": tuple(sorted({identity[3] for identity in admitted})),
            "required_checks": required_checks,
            "required_environment_count": len(required_environments),
            "successful_environment_count": len(admitted_environments),
        },
        "installation_matrix_proven": gate_satisfied,
        "ludoweave_version": __version__,
        "schema": _SCHEMA,
        "status": "ready" if gate_satisfied else "not-ready",
    }


def _installation_identity(
    record: dict[str, object], required_checks: tuple[str, ...]
) -> _InstallationIdentity:
    _exact_fields(
        record,
        {
            "environment_id",
            "python_version",
            "platform_system",
            "release_version",
            "release_tag",
            "release_url",
            "wheel_url",
            "wheel_sha256",
            "validation_url",
            "installation_log_sha256",
            "validated_at",
            "outcome",
            "isolated_environment",
            "installed_from_release_wheel",
            "dependencies_absent",
            "native_compiler_absent",
            "checks_passed",
            "provenance_reviewed",
            "validation_reviewed",
        },
        "installation record",
    )
    environment_id = _bounded_ascii_text(record["environment_id"], 64, "environment ID")
    contract = _ENVIRONMENT_CONTRACTS.get(environment_id)
    if contract is None:
        raise RuntimeError("installation environment is unsupported")
    platform_system = _bounded_ascii_text(record["platform_system"], 16, "platform system")
    if platform_system != contract[0]:
        raise RuntimeError("installation platform does not match its environment")
    python_version = _python_version(record["python_version"], contract[1])
    release_version = _bounded_ascii_text(record["release_version"], 64, "release version")
    if release_version != __version__:
        raise RuntimeError("installation release version does not match LudoWeave")
    release_tag = _bounded_ascii_text(record["release_tag"], 65, "release tag")
    if release_tag != f"v{release_version}":
        raise RuntimeError("installation release tag is incompatible")
    release_url = _bounded_ascii_text(record["release_url"], 256, "release URL")
    expected_release_url = f"https://github.com/xsparc/ludoweave-engine/releases/tag/{release_tag}"
    if release_url != expected_release_url:
        raise RuntimeError("installation release URL is incompatible")
    wheel_url = _bounded_ascii_text(record["wheel_url"], 384, "wheel URL")
    wheel_name = f"ludoweave-{release_version}-py3-none-any.whl"
    expected_wheel_url = (
        f"https://github.com/xsparc/ludoweave-engine/releases/download/{release_tag}/{wheel_name}"
    )
    if wheel_url != expected_wheel_url:
        raise RuntimeError("installation wheel URL is incompatible")
    wheel_hash = _sha256_text(record["wheel_sha256"], "wheel sha256")
    validation_url = _actions_job_url(record["validation_url"])
    installation_log_hash = _sha256_text(
        record["installation_log_sha256"], "installation log sha256"
    )
    validated_at = _utc_timestamp(record["validated_at"], "installation validation timestamp")
    outcome = _bounded_ascii_text(record["outcome"], 16, "installation outcome")
    if outcome != "passed":
        raise RuntimeError("installation outcome must be passed")
    isolated_environment = _required_true(
        record["isolated_environment"], "isolated environment review"
    )
    installed_from_release_wheel = _required_true(
        record["installed_from_release_wheel"], "release-wheel installation review"
    )
    dependencies_absent = _required_true(
        record["dependencies_absent"], "dependency-free installation review"
    )
    native_compiler_absent = _required_true(
        record["native_compiler_absent"], "native-compiler absence review"
    )
    checks_passed = tuple(
        _bounded_ascii_text(item, 64, "installation check")
        for item in _list(record["checks_passed"], "installation checks")
    )
    if checks_passed != required_checks:
        raise RuntimeError("installation checks are incomplete")
    provenance_reviewed = _required_true(
        record["provenance_reviewed"], "installation provenance review"
    )
    validation_reviewed = _required_true(
        record["validation_reviewed"], "installation validation review"
    )
    return (
        environment_id,
        python_version,
        platform_system,
        release_version,
        release_tag,
        release_url,
        wheel_url,
        wheel_hash,
        validation_url,
        installation_log_hash,
        validated_at,
        outcome,
        isolated_environment,
        installed_from_release_wheel,
        dependencies_absent,
        native_compiler_absent,
        checks_passed,
        provenance_reviewed,
        validation_reviewed,
    )


def _default_matrix() -> Path:
    bundled = Path(__file__).resolve().parent / "assets" / "installation_matrix.json"
    if bundled.is_file():
        return bundled
    return Path(__file__).resolve().parents[1] / "tests" / "fixtures" / bundled.name


def _read_bounded(path: Path, maximum: int, role: str) -> bytes:
    try:
        if path.is_symlink():
            raise RuntimeError(f"{role} must not be a symbolic link")
        with path.open("rb") as stream:
            value = stream.read(maximum + 1)
    except OSError as error:
        raise RuntimeError(f"{role} is unavailable") from error
    if len(value) > maximum:
        raise RuntimeError(f"{role} exceeds its byte limit")
    return value


def _loads(value: bytes, role: str) -> object:
    _reject_excessive_nesting(value, role)
    try:
        return json.loads(value, object_pairs_hook=_unique_object)
    except (UnicodeDecodeError, json.JSONDecodeError, RecursionError, ValueError) as error:
        raise RuntimeError(f"{role} is not valid JSON") from error


def _reject_excessive_nesting(value: bytes, role: str) -> None:
    depth = 0
    in_string = False
    escaped = False
    for character in value:
        if in_string:
            if escaped:
                escaped = False
            elif character == ord("\\"):
                escaped = True
            elif character == ord('"'):
                in_string = False
            continue
        if character == ord('"'):
            in_string = True
        elif character in (ord("{"), ord("[")):
            depth += 1
            if depth > _MAX_JSON_NESTING:
                raise RuntimeError(f"{role} exceeds its nesting limit")
        elif character in (ord("}"), ord("]")) and depth > 0:
            depth -= 1


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON field")
        result[key] = value
    return result


def _exact_fields(value: dict[str, object], expected: set[str], role: str) -> None:
    if set(value) != expected:
        raise RuntimeError(f"{role} fields are incompatible")


def _path(value: object) -> Path:
    if not isinstance(value, Path):
        raise TypeError("matrix must be a path")
    return value


def _object(value: object, role: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise RuntimeError(f"{role} must be an object")
    return cast(dict[str, object], value)


def _list(value: object, role: str) -> list[object]:
    if not isinstance(value, list):
        raise RuntimeError(f"{role} must be a list")
    return cast(list[object], value)


def _bounded_ascii_text(value: object, maximum: int, role: str) -> str:
    if type(value) is not str or not value or len(value) > maximum:
        raise RuntimeError(f"{role} is invalid")
    text = value
    if not text.isascii() or text != text.strip():
        raise RuntimeError(f"{role} is invalid")
    return text


def _python_version(value: object, required_minor: str) -> str:
    text = _bounded_ascii_text(value, 16, "Python version")
    parts = text.split(".")
    if len(parts) != 3 or any(not _canonical_decimal(part) for part in parts):
        raise RuntimeError("Python version is invalid")
    if ".".join(parts[:2]) != required_minor:
        raise RuntimeError("Python version does not match its environment")
    return text


def _canonical_decimal(value: str) -> bool:
    return value.isascii() and value.isdecimal() and (value == "0" or not value.startswith("0"))


def _sha256_text(value: object, role: str) -> str:
    text = _bounded_ascii_text(value, 64, role)
    if len(text) != 64 or any(character not in "0123456789abcdef" for character in text):
        raise RuntimeError(f"{role} is invalid")
    return text


def _actions_job_url(value: object) -> str:
    text = _bounded_ascii_text(value, 256, "validation URL")
    prefix = "https://github.com/xsparc/ludoweave-engine/actions/runs/"
    if not text.startswith(prefix):
        raise RuntimeError("installation validation URL is incompatible")
    parts = text.removeprefix(prefix).split("/job/")
    if len(parts) != 2 or any(not _canonical_decimal(part) or part == "0" for part in parts):
        raise RuntimeError("installation validation URL is incompatible")
    return text


def _utc_timestamp(value: object, role: str) -> str:
    text = _bounded_ascii_text(value, 20, role)
    if (
        len(text) != 20
        or text[4] != "-"
        or text[7] != "-"
        or text[10] != "T"
        or text[13] != ":"
        or text[16] != ":"
        or text[19] != "Z"
        or any(
            not text[index].isascii() or not text[index].isdecimal()
            for index in (*range(4), 5, 6, 8, 9, 11, 12, 14, 15, 17, 18)
        )
    ):
        raise RuntimeError(f"{role} is invalid")
    year = int(text[:4])
    month = int(text[5:7])
    day = int(text[8:10])
    hour = int(text[11:13])
    minute = int(text[14:16])
    second = int(text[17:19])
    try:
        date(year, month, day)
    except ValueError as error:
        raise RuntimeError(f"{role} is invalid") from error
    if hour > 23 or minute > 59 or second > 59:
        raise RuntimeError(f"{role} is invalid")
    return text


def _required_true(value: object, role: str) -> bool:
    if type(value) is not bool or value is not True:
        raise RuntimeError(f"{role} must be true")
    return True


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        raise SystemExit(1) from error
