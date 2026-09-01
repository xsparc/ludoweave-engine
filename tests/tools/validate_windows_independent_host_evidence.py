"""Validate one offline Windows independent-host evidence artifact."""

from __future__ import annotations

import argparse
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from hashlib import sha256
from os import fstat
from pathlib import Path
from stat import S_ISLNK, S_ISREG
from typing import NoReturn, cast

from ludoweave.world import JsonLimits, canonical_dumps, canonical_loads

if __package__:
    from tests.tools.validate_windows_cross_principal_evidence import (
        EvidenceValidationError as CrossPrincipalEvidenceValidationError,
    )
    from tests.tools.validate_windows_cross_principal_evidence import (
        validate_evidence_file as validate_cross_principal_evidence_file,
    )
else:
    from validate_windows_cross_principal_evidence import (
        EvidenceValidationError as CrossPrincipalEvidenceValidationError,
    )
    from validate_windows_cross_principal_evidence import (
        validate_evidence_file as validate_cross_principal_evidence_file,
    )

_SCHEMA = "ludoweave.windows-cleanup-independent-host-evidence/1"
_RESULT_SCHEMA = "ludoweave.windows-cleanup-independent-host-evidence-validation/1"
_MAX_DOCUMENT_BYTES = 8_388_608
_MAX_HOSTS = 32
_MAX_PROFILE_RESULTS = 128
_MAX_TRIALS = 4_096
_MAX_OBSERVATIONS = 65_536
_LIMITS = JsonLimits(
    max_bytes=_MAX_DOCUMENT_BYTES,
    max_depth=10,
    max_nodes=16_384,
    max_collection_items=1_024,
    max_string_bytes=256,
)
_PROFILES = (
    "local_fixed_ntfs",
    "refs_refusal",
    "smb_refusal",
    "csvfs_refusal",
    "cross_volume_refusal",
    "unknown_filesystem_refusal",
    "missing_capability_refusal",
    "file_id_reuse_aba",
)
_INTERRUPTIONS = (
    "forced_process_termination",
    "vm_power_cut",
    "physical_host_power_loss",
)
_INDEPENDENCE_FIELDS = (
    "os_installation_distinct",
    "boot_instance_distinct",
    "storage_instance_distinct",
    "observer_attested",
)
_CAPABILITY_FIELDS = (
    "hard_links",
    "reparse_points",
    "open_by_file_id",
    "persistent_acls",
    "read_only_volume",
    "same_volume",
    "profile_stable",
)
_OUTCOME_FIELDS = (
    "no_out_of_root_mutation",
    "no_unauthorized_deletion_or_restoration",
    "no_canonical_world_state_change",
    "no_credential_or_identity_disclosure",
    "no_leaked_handle",
    "no_live_participant_or_descendant",
    "refused_before_authority_or_mutation",
    "file_id_reuse_observed",
    "stale_authorization_rejected",
)
_SAFETY_OUTCOME_FIELDS = _OUTCOME_FIELDS[:6]
_STATUSES = frozenset(("passed", "failed", "unsupported", "not_run"))
_WINDOWS_RELEASE_CLASSES = frozenset(
    ("windows_10", "windows_11", "windows_server_2022", "windows_server_2025", "other_supported")
)
_ARCHITECTURE_CLASSES = frozenset(("x86_64", "arm64"))
_PERSISTENCE_CLASSES = frozenset(("volatile_vm", "persistent_vm", "physical", "unknown"))
_LOCALITIES = frozenset(("local_fixed", "local_virtual", "remote", "clustered", "unknown"))
_FILESYSTEM_FAMILIES = frozenset(("ntfs", "refs", "smb", "csvfs", "other", "unknown"))
_FILESYSTEM_VERSION_CLASSES = frozenset(("known_supported", "known_unadmitted", "unknown"))
_FILE_ID_SCOPES = frozenset(
    ("host_volume_128", "host_volume_64", "unavailable", "unstable", "unknown")
)


class EvidenceValidationError(ValueError):
    """A stable, path-free independent-host validation failure."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


@dataclass(frozen=True, slots=True)
class ValidationSummary:
    """Sanitized result of validating one bound evidence pair."""

    criterion_6_satisfied: bool
    criterion_7_satisfied: bool
    cross_principal_evidence_sha256: str
    evidence_sha256: str
    host_status_counts: Mapping[str, int]
    profile_status_counts: Mapping[str, int]
    windows_cleanup_admitted: bool = False

    def as_dict(self) -> dict[str, object]:
        """Return the canonical, path-free CLI result."""

        return {
            "criterion_6_satisfied": self.criterion_6_satisfied,
            "criterion_7_satisfied": self.criterion_7_satisfied,
            "cross_principal_evidence_sha256": self.cross_principal_evidence_sha256,
            "evidence_sha256": self.evidence_sha256,
            "host_status_counts": dict(self.host_status_counts),
            "profile_status_counts": dict(self.profile_status_counts),
            "schema": _RESULT_SCHEMA,
            "status": "valid",
            "windows_cleanup_admitted": self.windows_cleanup_admitted,
        }


@dataclass(frozen=True, slots=True)
class _Host:
    ordinal: int
    persistence_class: str
    status: str


def validate_evidence_files(
    evidence_file: Path, cross_principal_evidence_file: Path
) -> ValidationSummary:
    """Validate one independent-host artifact and its exact M206 companion."""

    try:
        cross_summary = validate_cross_principal_evidence_file(cross_principal_evidence_file)
    except CrossPrincipalEvidenceValidationError as error:
        raise EvidenceValidationError(
            "companion.invalid",
            "cross-principal companion evidence is invalid",
        ) from error

    encoded = _read_stable_regular_file(evidence_file)
    try:
        decoded = canonical_loads(encoded, limits=_LIMITS)
        if canonical_dumps(decoded, limits=_LIMITS) != encoded:
            raise EvidenceValidationError(
                "evidence.noncanonical",
                "evidence artifact must use exact canonical bytes",
            )
    except EvidenceValidationError:
        raise
    except Exception as error:
        raise EvidenceValidationError(
            "evidence.invalid_json",
            "evidence artifact is not bounded canonical JSON",
        ) from error

    document = _mapping(decoded, "document")
    criterion_7, host_counts, profile_counts = _validate_document(
        document,
        cross_principal_evidence_sha256=cross_summary.evidence_sha256,
        criterion_6_satisfied=cross_summary.criterion_6_satisfied,
    )
    return ValidationSummary(
        criterion_6_satisfied=cross_summary.criterion_6_satisfied,
        criterion_7_satisfied=criterion_7,
        cross_principal_evidence_sha256=cross_summary.evidence_sha256,
        evidence_sha256=f"sha256:{sha256(encoded).hexdigest()}",
        host_status_counts=host_counts,
        profile_status_counts=profile_counts,
    )


def _read_stable_regular_file(evidence_file: Path) -> bytes:
    try:
        before = evidence_file.lstat()
    except OSError as error:
        raise EvidenceValidationError(
            "evidence.read_failed", "evidence artifact could not be inspected"
        ) from error
    if S_ISLNK(before.st_mode) or not S_ISREG(before.st_mode):
        raise EvidenceValidationError(
            "evidence.not_regular",
            "evidence artifact must be a regular non-symbolic-link file",
        )
    if before.st_size > _MAX_DOCUMENT_BYTES:
        raise EvidenceValidationError(
            "evidence.too_large", "evidence artifact exceeds the byte limit"
        )

    try:
        with evidence_file.open("rb") as stream:
            opened = fstat(stream.fileno())
            if (
                before.st_dev != opened.st_dev
                or before.st_ino != opened.st_ino
                or before.st_size != opened.st_size
                or not S_ISREG(opened.st_mode)
            ):
                raise EvidenceValidationError(
                    "evidence.changed", "evidence artifact changed while being opened"
                )
            encoded = stream.read(_MAX_DOCUMENT_BYTES + 1)
            after_read = fstat(stream.fileno())
        after = evidence_file.lstat()
    except EvidenceValidationError:
        raise
    except OSError as error:
        raise EvidenceValidationError(
            "evidence.read_failed", "evidence artifact could not be read"
        ) from error

    if len(encoded) > _MAX_DOCUMENT_BYTES:
        raise EvidenceValidationError(
            "evidence.too_large", "evidence artifact exceeds the byte limit"
        )
    identity_before = (before.st_dev, before.st_ino, before.st_size)
    identity_after_read = (after_read.st_dev, after_read.st_ino, after_read.st_size)
    identity_after = (after.st_dev, after.st_ino, after.st_size)
    if (
        identity_before != identity_after_read
        or identity_before != identity_after
        or S_ISLNK(after.st_mode)
        or not S_ISREG(after.st_mode)
        or len(encoded) != before.st_size
    ):
        raise EvidenceValidationError(
            "evidence.changed", "evidence artifact changed while being opened"
        )
    return encoded


def _validate_document(
    document: Mapping[str, object],
    *,
    cross_principal_evidence_sha256: str,
    criterion_6_satisfied: bool,
) -> tuple[bool, dict[str, int], dict[str, int]]:
    _exact_fields(
        document,
        (
            "schema",
            "source_commit",
            "executable_sha256",
            "contract_sha256",
            "cross_principal_evidence_sha256",
            "capability_profile_sha256",
            "fixture_recipe_sha256",
            "hosts",
            "profiles",
            "totals",
            "criterion_7_satisfied",
            "windows_cleanup_admitted",
        ),
        "document",
    )
    _equal(document["schema"], _SCHEMA, "schema")
    _equal(
        document["cross_principal_evidence_sha256"],
        cross_principal_evidence_sha256,
        "cross_principal_evidence_sha256",
        code="binding.cross_principal",
    )

    hosts, host_counts = _validate_hosts(document["hosts"])
    profile_counts, profile_result_count, total_trials, total_observations = _validate_profiles(
        document["profiles"], hosts
    )
    _validate_totals(
        document["totals"],
        host_count=len(hosts),
        profile_result_count=profile_result_count,
        trial_count=total_trials,
        observation_count=total_observations,
    )

    all_not_run = profile_counts["not_run"] == len(_PROFILES)
    identities = (
        ("source_commit", "git-sha1:", 40),
        ("executable_sha256", "sha256:", 64),
        ("contract_sha256", "sha256:", 64),
        ("capability_profile_sha256", "sha256:", 64),
        ("fixture_recipe_sha256", "sha256:", 64),
    )
    if all_not_run:
        if any(document[field] is not None for field, _, _ in identities):
            _invalid("identity.unattempted", "unattempted evidence must omit identities")
        if hosts:
            _invalid("host.unattempted", "unattempted evidence must contain no hosts")
    else:
        for field, prefix, length in identities:
            _validate_prefixed_hex(document[field], prefix, length, field)

    expected_criterion = (
        criterion_6_satisfied
        and len(hosts) >= 2
        and all(host.status == "passed" for host in hosts.values())
        and profile_counts["passed"] == len(_PROFILES)
    )
    criterion = _boolean(document["criterion_7_satisfied"], "criterion_7_satisfied")
    if criterion != expected_criterion:
        _invalid(
            "claim.criterion_7",
            "criterion_7_satisfied does not match the bound complete evidence",
        )
    admitted = _boolean(document["windows_cleanup_admitted"], "windows_cleanup_admitted")
    if admitted:
        _invalid(
            "claim.windows_cleanup",
            "windows_cleanup_admitted must remain false pending a later admission decision",
        )
    return criterion, host_counts, profile_counts


def _validate_hosts(value: object) -> tuple[dict[int, _Host], dict[str, int]]:
    sequence = _sequence(value, "hosts")
    if len(sequence) > _MAX_HOSTS:
        _invalid("limits.hosts", "evidence exceeds the host-result limit")
    hosts: dict[int, _Host] = {}
    counts = {status: 0 for status in sorted(_STATUSES)}
    for host_value in sequence:
        host = _mapping(host_value, "host")
        _exact_fields(
            host,
            (
                "ordinal",
                "windows_release_class",
                "architecture_class",
                "persistence_class",
                "independence",
                "status",
            ),
            "host",
        )
        ordinal = _positive_integer(host["ordinal"], "host.ordinal")
        if ordinal in hosts:
            _invalid("host.ordinal", "host ordinals must be unique")
        if ordinal != len(hosts) + 1:
            _invalid("host.ordinal", "host ordinals must be contiguous and canonical")
        _text_member(
            host["windows_release_class"],
            _WINDOWS_RELEASE_CLASSES,
            "host.windows_release_class",
        )
        _text_member(
            host["architecture_class"],
            _ARCHITECTURE_CLASSES,
            "host.architecture_class",
        )
        persistence_class = _text_member(
            host["persistence_class"],
            _PERSISTENCE_CLASSES,
            "host.persistence_class",
        )
        independence = _boolean_record(
            host["independence"], _INDEPENDENCE_FIELDS, "host.independence"
        )
        status = _text_member(host["status"], _STATUSES, "host.status")
        if status == "passed" and (
            not all(independence.values()) or persistence_class == "unknown"
        ):
            _invalid(
                "host.passed",
                "passed hosts require complete observed independence and persistence",
            )
        counts[status] += 1
        hosts[ordinal] = _Host(
            ordinal=ordinal,
            persistence_class=persistence_class,
            status=status,
        )
    return hosts, counts


def _validate_profiles(
    value: object, hosts: Mapping[int, _Host]
) -> tuple[dict[str, int], int, int, int]:
    profiles = _sequence(value, "profiles")
    if len(profiles) != len(_PROFILES):
        _invalid("schema.profiles", "evidence must contain exactly eight profile lanes")
    counts = {status: 0 for status in sorted(_STATUSES)}
    profile_result_count = 0
    total_trials = 0
    total_observations = 0
    for index, profile_value in enumerate(profiles):
        profile = _mapping(profile_value, "profile")
        status, result_count, trials, observations = _validate_profile(
            profile, _PROFILES[index], hosts
        )
        counts[status] += 1
        profile_result_count += result_count
        total_trials += trials
        total_observations += observations
    if profile_result_count > _MAX_PROFILE_RESULTS:
        _invalid("limits.profile_results", "evidence exceeds the profile-result limit")
    if total_trials > _MAX_TRIALS:
        _invalid("limits.trials", "evidence exceeds the trial limit")
    if total_observations > _MAX_OBSERVATIONS:
        _invalid("limits.observations", "evidence exceeds the observation limit")
    return counts, profile_result_count, total_trials, total_observations


def _validate_profile(
    profile: Mapping[str, object], expected_id: str, hosts: Mapping[int, _Host]
) -> tuple[str, int, int, int]:
    _exact_fields(profile, ("id", "status", "host_results", "totals"), "profile")
    _equal(profile["id"], expected_id, "profile.id")
    claimed_status = _text_member(profile["status"], _STATUSES, "profile.status")
    host_results = _sequence(profile["host_results"], "profile.host_results")

    statuses: list[str] = []
    ordinals: set[int] = set()
    total_trials = 0
    total_observations = 0
    for result_value in host_results:
        result = _mapping(result_value, "profile.host_result")
        ordinal, status, trials, observations = _validate_profile_host_result(
            result, expected_id, hosts
        )
        if ordinal in ordinals:
            _invalid("profile.host_ordinal", "profile host ordinals must be unique")
        ordinals.add(ordinal)
        statuses.append(status)
        total_trials += trials
        total_observations += observations

    derived_status = _derive_profile_status(statuses)
    if claimed_status != derived_status:
        _invalid("claim.profile_status", "profile status does not match its host results")
    _validate_profile_totals(profile["totals"], len(host_results), total_trials, total_observations)
    if claimed_status == "passed" and len(host_results) < 2:
        _invalid("profile.hosts", "passed profiles require at least two independent hosts")
    return claimed_status, len(host_results), total_trials, total_observations


def _validate_profile_host_result(
    result: Mapping[str, object], profile_id: str, hosts: Mapping[int, _Host]
) -> tuple[int, str, int, int]:
    _exact_fields(
        result,
        (
            "host_ordinal",
            "locality",
            "filesystem_family",
            "filesystem_version_class",
            "file_id_scope",
            "capabilities",
            "status",
            "trial_count",
            "observation_count",
            "interruptions",
            "outcomes",
        ),
        "profile.host_result",
    )
    ordinal = _positive_integer(result["host_ordinal"], "profile.host_ordinal")
    host = hosts.get(ordinal)
    if host is None:
        _invalid("profile.host_ordinal", "profile references an unknown host ordinal")
    locality = _text_member(result["locality"], _LOCALITIES, "profile.locality")
    filesystem_family = _text_member(
        result["filesystem_family"], _FILESYSTEM_FAMILIES, "profile.filesystem_family"
    )
    filesystem_version_class = _text_member(
        result["filesystem_version_class"],
        _FILESYSTEM_VERSION_CLASSES,
        "profile.filesystem_version_class",
    )
    file_id_scope = _text_member(result["file_id_scope"], _FILE_ID_SCOPES, "profile.file_id_scope")
    capabilities = _boolean_record(
        result["capabilities"], _CAPABILITY_FIELDS, "profile.capabilities"
    )
    status = _text_member(result["status"], _STATUSES, "profile.host_status")
    trial_count = _nonnegative_integer(result["trial_count"], "profile.trial_count")
    observation_count = _nonnegative_integer(
        result["observation_count"], "profile.observation_count"
    )
    interruptions = _validate_interruptions(result["interruptions"])
    outcomes = _boolean_record(result["outcomes"], _OUTCOME_FIELDS, "profile.outcomes")

    if status == "not_run":
        if (
            trial_count != 0
            or observation_count != 0
            or any(value[0] != "not_run" or value[1] or value[2] for value in interruptions)
            or any(outcomes.values())
        ):
            _invalid("profile.not_run", "not_run host results must contain no observations")
        return ordinal, status, trial_count, observation_count

    if trial_count == 0 or observation_count == 0:
        _invalid("profile.attempted", "attempted host results require positive observations")
    interruption_trials = sum(item[1] for item in interruptions)
    interruption_observations = sum(item[2] for item in interruptions)
    if trial_count < interruption_trials or observation_count < interruption_observations:
        _invalid(
            "profile.interruption_totals",
            "host result totals must include all interruption observations",
        )

    if status == "passed":
        if host.status != "passed":
            _invalid("profile.host", "passed profile results require a passed host")
        if not all(outcomes[field] for field in _SAFETY_OUTCOME_FIELDS):
            _invalid("profile.outcomes", "passed results require every safety outcome")
        _validate_passed_profile(
            profile_id,
            host,
            locality,
            filesystem_family,
            filesystem_version_class,
            file_id_scope,
            capabilities,
            interruptions,
            outcomes,
        )
    return ordinal, status, trial_count, observation_count


def _validate_interruptions(value: object) -> list[tuple[str, int, int]]:
    interruptions = _sequence(value, "profile.interruptions")
    if len(interruptions) != len(_INTERRUPTIONS):
        _invalid(
            "schema.interruptions",
            "host results must contain exactly three interruption classes",
        )
    validated: list[tuple[str, int, int]] = []
    for index, interruption_value in enumerate(interruptions):
        interruption = _mapping(interruption_value, "interruption")
        _exact_fields(
            interruption,
            ("id", "status", "trial_count", "observation_count"),
            "interruption",
        )
        _equal(interruption["id"], _INTERRUPTIONS[index], "interruption.id")
        status = _text_member(interruption["status"], _STATUSES, "interruption.status")
        trials = _nonnegative_integer(interruption["trial_count"], "interruption.trial_count")
        observations = _nonnegative_integer(
            interruption["observation_count"], "interruption.observation_count"
        )
        if status == "not_run":
            if trials != 0 or observations != 0:
                _invalid(
                    "interruption.not_run",
                    "not_run interruptions must contain no observations",
                )
        elif trials == 0 or observations == 0:
            _invalid(
                "interruption.attempted",
                "attempted interruptions require positive observations",
            )
        validated.append((status, trials, observations))
    return validated


def _validate_passed_profile(
    profile_id: str,
    host: _Host,
    locality: str,
    filesystem_family: str,
    filesystem_version_class: str,
    file_id_scope: str,
    capabilities: Mapping[str, bool],
    interruptions: Sequence[tuple[str, int, int]],
    outcomes: Mapping[str, bool],
) -> None:
    statuses = tuple(item[0] for item in interruptions)
    if profile_id == "local_fixed_ntfs":
        if (
            host.persistence_class != "physical"
            or locality != "local_fixed"
            or filesystem_family != "ntfs"
            or filesystem_version_class != "known_supported"
            or file_id_scope != "host_volume_128"
            or not all(
                capabilities[field]
                for field in (
                    "hard_links",
                    "reparse_points",
                    "open_by_file_id",
                    "persistent_acls",
                    "same_volume",
                    "profile_stable",
                )
            )
            or capabilities["read_only_volume"]
            or statuses != ("passed", "passed", "passed")
            or outcomes["refused_before_authority_or_mutation"]
            or outcomes["file_id_reuse_observed"]
            or outcomes["stale_authorization_rejected"]
        ):
            _invalid(
                "profile.local_fixed_ntfs",
                "passed local NTFS results require the complete capability and interruption profile",
            )
        return

    if statuses != ("not_run", "not_run", "not_run"):
        _invalid(
            "profile.refusal_interruptions",
            "safe-refusal and ABA profiles must not claim interruption evidence",
        )
    if not outcomes["refused_before_authority_or_mutation"]:
        _invalid("profile.refusal", "passed refusal profiles require observed engine refusal")

    if profile_id == "refs_refusal":
        valid = filesystem_family == "refs"
    elif profile_id == "smb_refusal":
        valid = locality == "remote" and filesystem_family == "smb"
    elif profile_id == "csvfs_refusal":
        valid = locality == "clustered" and filesystem_family == "csvfs"
    elif profile_id == "cross_volume_refusal":
        valid = not capabilities["same_volume"]
    elif profile_id == "unknown_filesystem_refusal":
        valid = filesystem_family == "unknown" or filesystem_version_class == "unknown"
    elif profile_id == "missing_capability_refusal":
        required = (
            capabilities["hard_links"],
            capabilities["reparse_points"],
            capabilities["open_by_file_id"],
            capabilities["persistent_acls"],
            capabilities["same_volume"],
            capabilities["profile_stable"],
        )
        valid = not all(required) or capabilities["read_only_volume"]
    else:
        valid = (
            profile_id == "file_id_reuse_aba"
            and locality == "local_fixed"
            and filesystem_family == "ntfs"
            and filesystem_version_class == "known_supported"
            and file_id_scope == "host_volume_128"
            and all(
                capabilities[field]
                for field in (
                    "hard_links",
                    "reparse_points",
                    "open_by_file_id",
                    "persistent_acls",
                    "same_volume",
                    "profile_stable",
                )
            )
            and not capabilities["read_only_volume"]
            and outcomes["file_id_reuse_observed"]
            and outcomes["stale_authorization_rejected"]
        )
    if not valid:
        _invalid(
            "profile.classification", "passed profile does not match its required classification"
        )
    if profile_id != "file_id_reuse_aba" and (
        outcomes["file_id_reuse_observed"] or outcomes["stale_authorization_rejected"]
    ):
        _invalid("profile.aba", "only the ABA profile may claim file-identity reuse evidence")


def _derive_profile_status(statuses: Sequence[str]) -> str:
    if not statuses or all(status == "not_run" for status in statuses):
        return "not_run"
    if "failed" in statuses:
        return "failed"
    if "unsupported" in statuses:
        return "unsupported"
    if "not_run" in statuses or len(statuses) < 2:
        return "unsupported"
    return "passed"


def _validate_profile_totals(
    value: object, host_result_count: int, trial_count: int, observation_count: int
) -> None:
    totals = _mapping(value, "profile.totals")
    _exact_fields(
        totals,
        ("host_result_count", "trial_count", "observation_count"),
        "profile.totals",
    )
    _equal(totals["host_result_count"], host_result_count, "profile.totals.host_result_count")
    _equal(totals["trial_count"], trial_count, "profile.totals.trial_count")
    _equal(totals["observation_count"], observation_count, "profile.totals.observation_count")


def _validate_totals(
    value: object,
    *,
    host_count: int,
    profile_result_count: int,
    trial_count: int,
    observation_count: int,
) -> None:
    totals = _mapping(value, "totals")
    _exact_fields(
        totals,
        (
            "host_count",
            "profile_count",
            "profile_result_count",
            "trial_count",
            "observation_count",
        ),
        "totals",
    )
    expected = {
        "host_count": host_count,
        "profile_count": len(_PROFILES),
        "profile_result_count": profile_result_count,
        "trial_count": trial_count,
        "observation_count": observation_count,
    }
    for field, expected_value in expected.items():
        _equal(totals[field], expected_value, f"totals.{field}")


def _validate_prefixed_hex(value: object, prefix: str, length: int, field: str) -> None:
    if type(value) is not str:
        _invalid("identity.invalid", f"{field} must use the required digest identity")
    text = value
    payload = text.removeprefix(prefix)
    if (
        not text.startswith(prefix)
        or len(payload) != length
        or any(character not in "0123456789abcdef" for character in payload)
    ):
        _invalid("identity.invalid", f"{field} must use the required digest identity")


def _boolean_record(value: object, fields: tuple[str, ...], location: str) -> dict[str, bool]:
    record = _mapping(value, location)
    _exact_fields(record, fields, location)
    return {field: _boolean(record[field], f"{location}.{field}") for field in fields}


def _mapping(value: object, location: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        _invalid("schema.type", f"{location} must be an object")
    return cast(Mapping[str, object], value)


def _sequence(value: object, location: str) -> Sequence[object]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes, bytearray)):
        _invalid("schema.type", f"{location} must be an array")
    return cast(Sequence[object], value)


def _exact_fields(value: Mapping[str, object], expected: tuple[str, ...], location: str) -> None:
    if set(value) != set(expected):
        _invalid("schema.fields", f"{location} contains missing or unknown fields")


def _boolean(value: object, field: str) -> bool:
    if type(value) is not bool:
        _invalid("schema.type", f"{field} must be a boolean")
    return value


def _text(value: object, field: str) -> str:
    if type(value) is not str:
        _invalid("schema.type", f"{field} must be text")
    return value


def _text_member(value: object, allowed: frozenset[str], field: str) -> str:
    text = _text(value, field)
    if text not in allowed:
        _invalid("schema.value", f"{field} contains an unsupported value")
    return text


def _nonnegative_integer(value: object, field: str) -> int:
    if type(value) is not int or value < 0:
        _invalid("schema.type", f"{field} must be a non-negative integer")
    return value


def _positive_integer(value: object, field: str) -> int:
    integer = _nonnegative_integer(value, field)
    if integer == 0:
        _invalid("schema.type", f"{field} must be a positive integer")
    return integer


def _equal(
    value: object,
    expected: object,
    field: str,
    *,
    code: str = "schema.value",
) -> None:
    if type(value) is not type(expected) or value != expected:
        _invalid(code, f"{field} contains an unexpected value")


def _invalid(code: str, message: str) -> NoReturn:
    raise EvidenceValidationError(code, message)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate one offline Windows independent-host evidence pair."
    )
    parser.add_argument("evidence_file", type=Path)
    parser.add_argument("cross_principal_evidence_file", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Validate a bound artifact pair and print one canonical path-free result."""

    arguments = _parser().parse_args(argv)
    try:
        summary = validate_evidence_files(
            arguments.evidence_file,
            arguments.cross_principal_evidence_file,
        )
        result = summary.as_dict()
        exit_code = 0
    except EvidenceValidationError as error:
        result = {
            "error": {"code": error.code, "message": error.message},
            "schema": _RESULT_SCHEMA,
            "status": "invalid",
        }
        exit_code = 1
    print(canonical_dumps(result).decode("utf-8"))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
