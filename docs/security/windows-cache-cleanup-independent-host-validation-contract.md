# Windows cache-cleanup independent-host validation contract

**Status:** Accepted for M207 policy; independent-host evidence has not been
produced.

This contract defines the independent-host and filesystem-capability evidence
required by criterion 7 of the
[M199 readiness decision](../rfcs/0182-refresh-windows-cache-cleanup-readiness.md).
It follows the M205 cross-principal contract and M206 evidence validator but
does not add an independent-host harness, validator, native adapter, cleanup
implementation, or production authority. Criterion 6 must already be satisfied
before criterion 7 can pass. Criterion 7 remains unresolved. M207 does not
resolve criterion 7: `windows_cleanup_admitted is false`, Windows is not
admitted, and cleanup remains unimplemented and unauthorized.

## Independent-host qualification

Every admitted capability profile requires successful reproduction on at
least two independently provisioned Windows hosts. Independence is a property
observed by a trusted coordinator and attested by the operator, not a label
self-reported by a participant. Each host must have a distinct operating-system
installation, distinct boot instance, and distinct storage instance for the
fixture volume. The evidence records only the resulting observer-attested
independence booleans and bounded classifications.

Two processes on one host do not qualify. Two sessions on one host do not
qualify. A container does not qualify as another host. A reboot of one host
does not qualify as a second host. Clones resumed from one VM snapshot do not
qualify because shared pre-run state can reproduce the same hidden fault. Two
virtual machines may qualify only when separately provisioned, separately
booted, and backed by independently instantiated storage. Physical hosts may
qualify when their operating-system and fixture-storage instances are distinct.

Host independence does not authenticate public evidence. A private run record
must bind each ephemeral host role to operator observations, but public
evidence must not expose a stable machine or storage identifier.

## Observed capability profile

Each host produces one bounded capability profile before setup and revalidates
it immediately before every effect. Capabilities are observed, not inferred
from a drive letter, path spelling, Windows edition, or expected filesystem.
The private observation contains enough operating-system output to derive these
public classifications:

- Windows release class and architecture class;
- local or remote classification;
- filesystem family and filesystem version class, with unavailable versions
  represented as `unknown` rather than guessed;
- volume capability flags returned by `GetVolumeInformationW`, including
  `FILE_SUPPORTS_HARD_LINKS`, `FILE_SUPPORTS_REPARSE_POINTS`,
  `FILE_SUPPORTS_OPEN_BY_FILE_ID`, persistent ACL, and read-only state;
- same-volume relationship between root, candidate, quarantine, recovery, and
  every alias location;
- file-ID scope, width, volume binding, and stability class;
- persistence class for volatile VM storage, virtual persistent storage,
  physical storage, or unknown storage; and
- cluster, network-share, redirection, compression, encryption, and reparse
  classifications relevant to the lane.

`FILE_ID_INFO` supplies a volume serial number and 128-bit file identifier that
together identify a file only within one computer. Those values are private
observer inputs, never globally unique authentication. Every use-time check
therefore retains the host and volume scope, and the matrix applies explicit
file-ID reuse pressure.

An unavailable query, unrecognized flag combination, changed profile, remote
volume, or ambiguous root relationship causes refusal. No fallback profile is
chosen.

## Mandatory host and refusal matrix

Every criterion-7 document contains all of these profile lanes. A lane must be
reproduced on at least two qualifying independent hosts. A profile may be
declared unsupported, but unsupported is not a passing refusal and leaves the
criterion unresolved.

| Lane | Required observation |
| --- | --- |
| `local_fixed_ntfs` | Complete M199 through M206 design on a local fixed NTFS fixture with every required capability observed. |
| `refs_refusal` | ReFS is refused before authority or mutation unless a later accepted decision separately admits a ReFS profile. |
| `smb_refusal` | SMB and other remote shares are refused before authority or mutation. |
| `csvfs_refusal` | CsvFS and other clustered-volume semantics are refused before authority or mutation. |
| `cross_volume_refusal` | Any candidate, quarantine, recovery, or alias object crossing the trusted fixture volume is refused. |
| `unknown_filesystem_refusal` | An unknown or unclassified filesystem is refused. |
| `missing_capability_refusal` | A missing, unavailable, contradictory, or changed required capability is refused. |
| `file_id_reuse_aba` | Repeated delete/recreate and allocation pressure cannot authorize a reused or stale file identity. |

The `file_id_reuse_aba` lane passes only after the host actually reuses a
previously observed file identity and the stale authorization still fails
closed. Allocation pressure without observed reuse is unsupported evidence,
not proof that reuse is safe.

The ReFS lane is a non-admission decision, not a claim that current ReFS lacks
hard links or file IDs. The CsvFS lane likewise refuses unvalidated clustered
semantics even when an individual Windows API reports support. There is no
substitute profile: a passing NTFS run cannot stand in for ReFS, SMB, CsvFS,
cross-volume, or unknown-capability refusal evidence.

Safe refusal must be observed as an actual engine result before an external
effect. A documentation statement or a harness-side skip is not proof.
Unsupported is not a passing refusal. Cross-volume behavior must never use
`MOVEFILE_COPY_ALLOWED`; copy/delete fallback is forbidden because it changes
atomicity, security-descriptor, and failure semantics and can leave the source
intact after reported success.

## Topology and execution controls

The operator supplies dedicated disposable hosts or virtual machines. Every
fixture is outside the repository, workspace, user profile, and production
cache and remains confined to one observed local volume. The exact root is a
non-reparse directory with a fresh sentinel. The M205 principal, process,
session, handle, ACL, control-channel, and teardown requirements apply on every
host without weakening.

The same source commit, executable digest, contract digest, cross-principal
evidence digest, fixture recipe, lane order, barrier schedule, and bounded
trial counts apply across the host cohort. Platform-dependent results remain
explicit profile observations; a coordinator must not normalize a failure into
a pass merely to make hosts agree.

## Interruption and durability classes

Graceful close is not interruption evidence. Each admitted profile separates
at least these classes:

- `forced_process_termination`: the engine or recovery coordinator is forcibly
  terminated at every durable-state barrier;
- `vm_power_cut`: the virtual machine loses execution without a guest shutdown
  and is restarted from its existing storage; and
- `physical_host_power_loss`: a dedicated physical test host loses power and
  restarts from the affected persistent storage under operator control.

A VM power cut is not physical-host power-loss evidence. A host reset is not a
storage-device power-loss claim. A successful flush call is not sufficient
proof of the strongest persistence class: operating-system buffering,
controller caching, virtual storage, and device behavior remain part of the
declared profile. Unknown persistence semantics make the affected durability
lane unsupported.

After each interruption, the run performs restart and recovery reconciliation
before another cleanup attempt. It must prove a single valid durable prefix,
consistent intent/state/receipt records, bounded settlement, and no unsafe
external mutation. No lane may infer success solely from process exit, boot
completion, file absence, or a successful API return.

## Outcomes and completeness

Each host/profile/interruption result has exactly one status: passed, failed,
unsupported, or not_run. A refusal result passes only when the engine itself
refuses before gaining cleanup authority or changing the fixture. A positive
profile passes only when every M199 through M206 prerequisite and every
applicable interruption, recovery, alias, identity, and cross-principal lane
passes on every required host.

Failed, unsupported, or not_run keeps criterion 7 unresolved. Missing hosts,
shared host ancestry, incomplete profiles, unavailable physical interruption,
unknown persistence, changed capabilities, teardown ambiguity, or any unsafe
effect also keeps criterion 7 unresolved. A criterion-7 document cannot be
qualifying unless criterion 6 must already be satisfied by a separately valid
M206 document.

Across all hosts there must be no out-of-root mutation, no unauthorized
deletion or restoration, no canonical world-state change, no credential or
identity disclosure, no leaked handle, and no live fixture participant or
descendant after settlement.

## Evidence envelope

The reserved evidence identity is
`ludoweave.windows-cleanup-independent-host-evidence/1`. A future writer emits
one bounded canonical JSON object through atomic private-file replacement. The
document is limited to maximum 32 host results, maximum 128 profile results,
maximum 65,536 observations, and maximum 8,388,608 bytes. Unknown or duplicate
fields, noncanonical bytes, partial output, and conflicting aggregate claims
are invalid.

The document binds the source commit, executable digest, contract digest,
cross-principal evidence digest, capability-profile digest, fixture-recipe
digest, and the exact matrix/result counts. It records ephemeral host ordinals,
independence booleans, fixed classification enums, status values, bounded
counts, and canonical digests. The document sets
`windows_cleanup_admitted` to false unless a later accepted admission decision
validates a complete qualifying artifact.

Public evidence contains only sanitized classifications. It contains no
hostname, machine identifier, volume serial number, file identifier, account
name, SID, path, environment value, credential, or platform error text. It also
contains no address, PID, session identifier, handle value, ACL bytes, firmware
serial, cloud resource identifier, repository credential, or operator contact
information. Canonical hashes are not authentication and must not be described
as signatures or provenance proof.

## Custody, transport, and CI boundary

Independent-host runs occur only on operator-controlled hosts using offline
evidence collection. The fixture and coordinator open no network listener or
network access. Artifacts move out only after the run has settled and after a
separate operator sanitization review. No credential or account secret enters
the repository, evidence, command line, environment, log, or CI secret.

The privileged harness, if separately approved later, must not be attached to
a public-repository workflow. GitHub-hosted Windows administrators with UAC
disabled do not demonstrate the required principal topology, storage custody,
or physical interruption class. A public self-hosted runner would expose an
operator-controlled host to untrusted workflow code. M207 therefore adds no
workflow, runner label, secret, permission, or hosted allocation.

## Admission boundary

This contract makes evidence requirements reviewable; it does not produce the
evidence. The M206 reviewed fixture remains intentionally incomplete, no
independent-host artifact exists, and no cleanup implementation exists.
Windows admission requires a later accepted decision that independently
validates complete criterion-6 and criterion-7 artifacts and rechecks every
earlier policy boundary.

Until then, all Windows cleanup requests remain safe refusals and
`windows_cleanup_admitted is false`.

## Primary references

- [GetVolumeInformationW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getvolumeinformationw)
- [FILE_ID_INFO](https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_id_info)
- [MoveFileExW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)
- [FlushFileBuffers](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-flushfilebuffers)
- [ReFS overview and feature comparison](https://learn.microsoft.com/en-us/windows-server/storage/refs/refs-overview)
- [GitHub-hosted runners reference](https://docs.github.com/en/actions/reference/runners/github-hosted-runners)
- [Adding self-hosted runners](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/add-runners)
