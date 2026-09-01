# Windows independent-host collection-plan validator

**Status:** Accepted for M210 source-only validation; no collection authority or
qualifying run is authorized.

M210 adds an offline, read-only validator for one sanitized structural companion
to the future private run manifest required by the
[M209 collection-authority policy](windows-cache-cleanup-independent-host-collection-authority-policy.md).
The validator makes the planned matrix and refusal posture reviewable before a
privileged harness is proposed. It does not validate private operator identity,
authenticate a host, mint authority, launch a participant, control power, collect
evidence, or admit Windows cleanup.

## Input and identity boundary

The reserved document identity is
`ludoweave.windows-cleanup-independent-host-collection-plan/1`. The validator
reads exactly one stable regular non-symbolic-link file, bounded to 1,048,576
bytes and one exact canonical JSON line. Unknown fields, duplicate keys,
noncanonical bytes, unstable reads, excessive structure, and invalid identity
syntax refuse with a stable path-free error.

The plan may carry the source commit plus SHA-256 identities for the executable,
M207 contract, M209 policy, M206 evidence, fixture recipe, and capability
profile. Presence and syntax establish only structural completeness. The
validator does not fetch, execute, authenticate, or independently recompute
those objects, and a digest cannot prove provenance or grant authority.

The reviewed fixture leaves every identity null, declares zero hosts, retains
all lanes as `not_run`, and sets `plan_complete`, `authority_issued`, criteria 6
and 7, and `windows_cleanup_admitted` to false. It is parser evidence only.

## Closed plan matrix

A document contains the exact ordered M207 profile lanes:

1. `local_fixed_ntfs`;
2. `refs_refusal`;
3. `smb_refusal`;
4. `csvfs_refusal`;
5. `cross_volume_refusal`;
6. `unknown_filesystem_refusal`;
7. `missing_capability_refusal`; and
8. `file_id_reuse_aba`.

It also retains the eight M205/M207 durability barriers, the three distinct
interruption classes (`forced_process_termination`, `vm_power_cut`, and
`physical_host_power_loss`), and M209's closed eight-operation sequence:

1. observe and revalidate;
2. launch the fixed participant;
3. advance one deterministic barrier;
4. apply one bound interruption;
5. restart and reconcile;
6. collect bounded observations;
7. settle and tear down; and
8. stage one artifact.

The validator derives the bounded host/profile/barrier/interruption cross-product
instead of trusting a copied total. At most 32 contiguous ephemeral host ordinals
are accepted. Host entries contain only bounded Windows release, architecture,
and persistence classifications and remain `not_run`; stable host, storage,
process, principal, session, path, or operator identifiers are not schema fields.
Stable identifiers are not schema fields.

## Requirement declarations

`plan_complete` is derived rather than trusted. It can be true only when all
seven identities are present, at least two host ordinals exist, and every exact
requirement declaration is true. Those declarations cover:

- offline networking, disabled clipboard redirection, detached read-only ingress,
  no writable live sharing, no public runner, and no repository credential;
- disposable confined fixtures and exclusion of stable identities;
- private non-serializable, single-run, single-use collection authority kept
  separate from cleanup authority;
- retained process identity and contained process trees;
- external VM power control, forbidden checkpoint restoration, and
  operator-only physical interruption; and
- chronological custody, separate digest retention, atomic same-volume staging,
  sanitization review, and fail-closed teardown.

These booleans are pre-run requirements, not observations. A structurally
complete plan is still not executable authority and is not qualifying evidence.
`authority_issued`, criteria 6 and 7, and `windows_cleanup_admitted` are required
to remain false. `collection_status` is required to remain `not_run`.

## Process and power interpretation

Future process control must use retained private process identity and an
explicitly contained process tree. Windows process identifiers alone are
insufficient because they may be reused after the process object is freed.
Windows Job Objects can manage a process group, but those native handles and
rights remain future private harness concerns and never enter this document or
the engine API.

VM interruption must be external to the guest and bound to the exact VM and
current storage. Guest shutdown, pause, save, checkpoint creation, checkpoint
restore, or replacement storage cannot substitute for a power cut. Physical
power loss remains an operator-only action on dedicated disposable fixtures.

## Failure and output

Every invalid value refuses before any effect. The validator emits one canonical,
path-free result containing only the plan digest, structural counts,
`plan_complete`, fixed false authority/admission claims, and status. It never
echoes input content or a path. Validation is read-only and source-only under
`tests/tools`; it is not installed in the wheel and is not a runtime or CLI
surface.

M210 adds no privileged harness, native call, process launch, power action,
account or credential lifecycle, filesystem mutation, network access, cleanup
authority, dependency, workflow, permission, secret, or hosted allocation. No
qualifying run has occurred and there is no qualifying evidence. Criteria 6 and
7 remain unresolved, Windows remains
unadmitted, and cleanup remains unimplemented and unauthorized.

## Primary references

- [Windows Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [Windows process handles and identifiers](https://learn.microsoft.com/en-us/windows/win32/procthread/process-handles-and-identifiers)
- [Windows `PROCESS_INFORMATION`](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/ns-processthreadsapi-process_information)
- [Hyper-V PowerShell](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/powershell)
- [Hyper-V checkpoints](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/checkpoints)
- [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [NISTIR 8387: Digital Evidence Preservation](https://doi.org/10.6028/NIST.IR.8387)
