# Windows cache-cleanup independent-host evidence validator

**Status:** Accepted for M208 source validation; qualifying evidence has not
been produced.

M208 adds one offline, read-only validator for the evidence envelope defined by
the [M207 independent-host validation
contract](windows-cache-cleanup-independent-host-validation-contract.md).
Structurally valid does not mean criterion 7 satisfied. The reviewed artifact
is intentionally incomplete, criterion 6 and criterion 7 remain unresolved,
Windows is not admitted, and cleanup remains unimplemented and unauthorized.
No qualifying host execution exists.

## Two-file input boundary

The validator accepts an independent-host document and a separately validated M206
cross-principal document. It validates the cross-principal document with the
M206 validator, computes its SHA-256, and requires the independent-host
document to bind that exact digest. Criterion 6 is derived from the validated
companion; a copied boolean or unverified digest cannot satisfy criterion 7.

Both inputs must be regular non-symbolic-link files. Each validator compares
the path identity and size before open with the opened descriptor, the
descriptor after the bounded read, and the path after close. A difference
refuses validation. The independent-host input is capped at 8,388,608 bytes,
16,384 JSON nodes, ten levels, 1,024 members per collection, and 256 UTF-8
bytes per string.

The independent-host schema is
`ludoweave.windows-cleanup-independent-host-evidence/1`. It uses LudoWeave's
existing bounded canonical JSON contract. Duplicate or unknown fields,
noncanonical bytes, partial input, conflicting totals, and non-finite numbers
are invalid. The validator reads only; it performs no collection, process
launch, network access, filesystem cleanup, or artifact rewrite.

## Hosts and bounded classifications

The document contains no more than 32 host records. Host ordinals are positive,
unique, contiguous, and canonical. A host records only fixed Windows release,
architecture, and persistence classes; four observer-derived independence
booleans; and one closed status. A passed host requires all of these observed
independence facts:

- distinct operating-system installation;
- distinct boot instance;
- distinct fixture-storage instance; and
- trusted-observer attestation.

Unknown persistence cannot pass. The public shape contains no hostname,
machine identifier, cloud-resource identifier, storage serial, account, SID,
path, session, process, handle, ACL, credential, or platform error text.

## Exact profile matrix

Every document contains these eight profile lanes in canonical order:

1. `local_fixed_ntfs`
2. `refs_refusal`
3. `smb_refusal`
4. `csvfs_refusal`
5. `cross_volume_refusal`
6. `unknown_filesystem_refusal`
7. `missing_capability_refusal`
8. `file_id_reuse_aba`

Each lane contains per-host results and exact totals. Across the document there
may be no more than 128 profile/host results, 4,096 trials, or 65,536
observations. Each result uses fixed locality, filesystem family/version,
file-ID scope, capability booleans, statuses, counts, outcomes, and the three
interruption identities. File identity remains host-and-volume scoped; its
digest or classification is not operator authentication.

A passed lane requires at least two distinct passed host records. The positive
local fixed NTFS result requires an observed writable same-volume NTFS profile,
stable 128-bit host/volume-scoped file identity, hard-link, reparse-point,
open-by-ID, persistent-ACL, and profile-stability capabilities, plus passed
forced-process, VM-power-cut, and physical-host-power-loss results. The hosts
used for this positive durability claim must have physical persistence.

Every refusal lane must contain an actual engine refusal before authority or
mutation. ReFS, remote SMB, clustered CsvFS, cross-volume, unknown filesystem,
and missing or contradictory capability classifications are checked against
their matching result. Their interruption fields remain `not_run` because the
refusal occurs before mutation. The ABA lane passes only when identity reuse was
actually observed on the local fixed NTFS stable 128-bit host/volume-scoped
identity profile and the stale authorization was rejected. All passed results
also require the complete sanitized safety outcome set.

## Claims and reviewed fixture

Host, profile, and interruption statuses are limited to `passed`, `failed`,
`unsupported`, and `not_run`. Counts and every aggregate status are derived
from the contained results. An all-`not_run` document omits source, executable,
contract, capability-profile, and fixture-recipe identities and contains no
host records. An attempted document binds exact lower-case `git-sha1:` or
`sha256:` identities.

Criterion 7 can be true only when the separately validated companion satisfies
criterion 6, at least two hosts pass, and all eight profile lanes pass their
exact per-host rules. Failed, unsupported, incomplete, or not-run evidence
cannot qualify. M208 still requires `windows_cleanup_admitted` to remain false:
a later accepted admission decision must recheck the complete policy chain.

The reviewed independent-host fixture is exact canonical JSON with all eight
lanes `not_run`, no hosts, zero observations, and a binding to the reviewed
incomplete M206 fixture. It proves parser, binding, sanitization, and
false-claim behavior only. It is not a host run, interruption run, or security
result.

Success prints one canonical, path-free summary with both evidence digests,
derived criterion values, fixed status counts, and false Windows admission.
Failure prints a stable path-free typed error. Input locations and operating-
system error text are never echoed.

## Authority, packaging, and CI boundary

The validator and fixtures are source-only test tooling and do not enter the
wheel or public runtime API. M208 adds no host coordinator, account or
credential lifecycle, native Windows call, process launcher, filesystem
adapter, cleanup operation, dependency, workflow, runner, secret, permission,
or hosted allocation. Independent-host collection remains a separately
reviewed privileged milestone and must remain offline on operator-controlled
disposable fixtures.

## Primary references

- [RFC 8259: The JavaScript Object Notation (JSON) Data Interchange
  Format](https://www.rfc-editor.org/rfc/rfc8259)
- [RFC 8785: JSON Canonicalization
  Scheme](https://www.rfc-editor.org/rfc/rfc8785)
- [Python `Path.lstat`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.lstat)
- [Python `os.fstat`](https://docs.python.org/3/library/os.html#os.fstat)
- [Microsoft `FILE_ID_INFO`](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [Microsoft `GetVolumeInformationW`](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getvolumeinformationw)
