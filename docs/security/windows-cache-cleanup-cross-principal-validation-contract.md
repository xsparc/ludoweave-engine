# Windows cache-cleanup cross-principal validation contract

**Status:** Accepted for M205 policy; qualifying evidence has not been produced.

This contract defines the adversarial Windows evidence required by criterion 6
of the [M199 readiness decision](../rfcs/0182-refresh-windows-cache-cleanup-readiness.md).
It does not add a cleanup implementation, a principal launcher, or production
authority. Criteria 1 through 5 are resolved as policy. Criteria 6 and 7 remain
unresolved. M205 does not resolve criterion 6: no qualifying cross-principal run
has occurred. Windows is not admitted, and cleanup remains unimplemented and
unauthorized.

## Trust and principal qualification

A qualifying run uses a genuinely distinct untrusted local principal. The
coordinator must prove all of the following from operating-system observations:

- the participant's TOKEN_USER SID must differ from the trusted principal;
- the participant has an independently authenticated logon context;
- token ID, authentication ID, and modified ID are recorded only as private
  observer inputs and are distinct where the lane requires distinction;
- the launched engine and adversary each use a primary token, and the session ID
  is checked against the declared lane;
- the hostile principal is not the trusted-root owner, is not a member of
  Administrators, and lacks administrative bypass privileges.

Same-principal isolation is useful for other tests but is not criterion 6
evidence. A restricted copy of the trusted token does not qualify. An
integrity-level change does not qualify. A same-user AppContainer does not
qualify. The same SID in another logon session does not qualify. Impersonation
of the trusted SID does not qualify. A GitHub-hosted administrator account does
not qualify.

## Credential and account custody

The launcher authority is operator-provisioned. The operator provisions the
independent account and credentials outside this repository. A private
engine-owned launcher authority may receive an already
authenticated primary token through a local, non-public integration boundary,
but repository code never accepts a username, password, credential, token
value, or account secret. Repository tooling must not create, delete, enable,
disable, or modify an account. It must not change group membership, logon
rights, or local security policy.

Credentials never enter environment variables, files, command lines, logs,
evidence, or CI secrets. The operator retains account and credential lifecycle
ownership. Failure to obtain a qualifying token makes the run unsupported; it
must not trigger a same-user fallback.

## Fixture confinement

Every lane runs beneath one disposable fixture root that is outside the
repository, workspace, user profile, and production cache. The root must be an
ordinary non-reparse directory on the same local volume as all candidates,
quarantine entries, and recovery records. A fresh root sentinel binds the exact
fixture identity. Setup and teardown enforce exact cleanup confinement. Network
shares are forbidden, and the harness opens no network listener or network
access.

The coordinator rejects pre-existing children, a missing or changed sentinel,
unexpected volume identity, any reparse point in the trusted ancestry, and any
path that resolves outside the exact fixture. Lane-created aliases and reparse
objects may exist only at their declared hostile locations and only while the
coordinator retains the handles required to identify them.

## Process and session topology

A run has a trusted coordinator, a trusted engine process, and an unrelated
hostile process. The adversary must be in a separate process tree and a separate
authenticated logon context. The suite also contains a separate Windows session
lane. Parent-owned cooperation is not proof of unrelated-process behavior. No
participant receives an inherited cleanup handle. There is no inherited cleanup
handle in a participant, and the harness permits no arbitrary shell, script, or
evaluation.

The coordinator creates each process suspended or behind a private start
barrier, verifies its effective token and image before release, and assigns
bounded lifetime supervision. Process exit is not sufficient settlement:
descendants and retained handles must also be accounted for.

## Handle inheritance and duplication

The coordinator captures an explicit handle inventory before every launch and
requires zero unlisted inheritable handles. If a private control-channel handle
must be inherited, launch uses `PROC_THREAD_ATTRIBUTE_HANDLE_LIST` and the list
contains only that handle. There is no root, candidate, quarantine,
recovery-store, token, process, or job handle in the inherited set.

The cross-session lane cannot rely on handle inheritance. DuplicateHandle
attempts must cover denied and permitted control cases, recording whether the
target references the same object and access rights without publishing handle
values. A leaked, unexpectedly duplicated, or unaccounted handle fails the
lane.

## Mandatory adversarial lanes

Every qualifying evidence document contains all of these lanes:

| Lane | Required pressure |
| --- | --- |
| `baseline_denial` | Untrusted direct mutation without delegated fixture rights. |
| `acl_flip` | DACL change at every protected transition barrier. |
| `owner_dacl_takeover_denial` | Attempts to take ownership or rewrite the DACL. |
| `hard_link_alias` | Real same-volume hard-link alias pressure. |
| `reparse_substitution` | Real reparse-point replacement pressure. |
| `rename_substitution` | Rename and replacement between authorization and effect. |
| `delete_recreate` | Delete/recreate pressure against retained identity. |
| `inherited_handle` | Launch-time handle-leakage pressure. |
| `duplicate_handle` | Cross-process duplication attempts. |
| `unrelated_open` | Unrelated hostile opens with each relevant access mask. |
| `cross_session` | Distinct principal in a separate Windows session. |
| `recovery_tamper` | Recovery-store and generation tampering during reconciliation. |
| `control_channel_failure` | Authentication, replay, disconnect, and timeout failures. |

Each lane runs adversary-first and engine-first orders across every applicable
barrier. Unsupported platform capability is recorded as `unsupported`; it is
never silently replaced with a weaker simulation.

## Deterministic schedule

The harness uses a deterministic barrier schedule. Sleep, polling luck, and
elapsed-time overlap are not proof. Applicable adversarial actions are released:

1. before authority admission;
2. after authority admission but before intent;
3. after intent but before a pending record;
4. after quarantine_pending but before quarantine;
5. after quarantine but before quarantined;
6. after delete_pending but before deletion;
7. after deletion but before deleted; and
8. during recovery reconciliation.

Each schedule uses adversary-first and engine-first release orders plus a
bounded timeout and settlement rule. A timeout is a failed or unsupported lane
according to its cause, never a successful race result.

## ACL and access evidence

The coordinator observes root, candidate, quarantine, recovery-store, and
generation security before and after each relevant transition. It records the
owner, DACL, and security-descriptor control flags in sanitized classifications.
The classification covers explicit, inherited, and protected DACL state. A
NULL DACL is forbidden.

For both principals, the suite checks requested rights and the actual allowed or
denied operation result for DELETE, FILE_DELETE_CHILD, WRITE_DAC, WRITE_OWNER,
FILE_WRITE_ATTRIBUTES, FILE_ADD_FILE, and FILE_ADD_SUBDIRECTORY. Lane-specific
delegated rights are not production
authority. The coordinator must revalidate after every ACL transition; an
inherited ACE copied by a move or a changed parent is not assumed safe.

## Alias, reparse, and object identity

The alias lanes use a real same-volume hard link and a real reparse point.
Path-string simulation is not evidence. The coordinator keeps retained handles
to the trusted root and target objects and observes volume and file identity,
link count, reparse tag, and root relationship at every effect boundary.

If the environment cannot create the requested hard link or reparse point under
the declared untrusted principal, unsupported creation capability keeps the
lane unsupported. It does not permit privilege elevation, a substitute
principal, or a mocked filesystem result.

## Pass, failure, and admission rules

A lane passes only when the operating system denies the hostile action, or the
engine refuses before an unsafe effect, or the engine enters recovery_required
before another effect. Across the complete run there must be
no out-of-root mutation, no unauthorized deletion or restoration, no canonical
world-state change, no leaked handle, and no participant or descendant remains
alive.

Every mandatory lane has exactly one status: passed, failed, unsupported, or
not_run. An unsupported, not_run, or failed mandatory lane keeps criterion
6 unresolved. Criterion 7 may be evaluated only after every mandatory criterion
6 lane has passed under this contract.

## Evidence envelope

The internal evidence identity is
`ludoweave.windows-cleanup-cross-principal-evidence/1`. One run is bounded to a
maximum 32 lanes, maximum 512 trials, maximum 32,768 events, and maximum
4,194,304 bytes. The writer emits one complete canonical JSON object through an
atomic private-file replacement; partial or duplicate documents are invalid.

Publicly retain only fixed enums, counts, bounded booleans, source commit,
executable digest, contract version, lane status, barrier status, and canonical
digest. Principal qualification is reduced to these booleans:

- `principal_sid_distinct`
- `authentication_context_distinct`
- `administrator_membership_absent`
- `bypass_privileges_absent`

Evidence contains no account name, domain, SID, token identifier,
authentication identifier, session identifier, PID, path, handle, ACL bytes,
environment value, or platform error text. Canonical hashes are not
authentication and must not be described as signatures or provenance proof.

## Observer and control-channel integrity

Participant self-report is not identity evidence. The coordinator uses
coordinator-owned process and token handles to query the effective token of each
participant. Those observations bind the exact executable digest and bind the
source commit before releasing a lane.

Coordination uses an authenticated local control channel with an exact
principal-scoped DACL and a fresh unpredictable challenge for every connection.
Messages are bounded, schema-validated, replay-rejected, and sequenced. This
local authentication protects the fixture run; it does not prove public
artifact authenticity.

## Teardown

The operator retains account and credential lifecycle ownership throughout
teardown. The coordinator performs bounded participant and descendant
settlement, must close every owned handle, must verify the exact root sentinel,
and uses a reparse-free teardown walk confined to the fixture.

The harness must not restore an external ACL or mutate any object outside the
fixture. It must preserve the fixture on ambiguous teardown and emit only
path-free failure evidence. Account cleanup, credential rotation, and local
security-policy restoration remain operator responsibilities outside the
repository.

## Primary references

- [Access tokens](https://learn.microsoft.com/en-us/windows/win32/secauthz/access-tokens)
- [CreateProcessAsUser](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessasusera)
- [LogonUser](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-logonusera)
- [Process inheritance](https://learn.microsoft.com/en-us/windows/win32/procthread/inheritance)
- [File security and access rights](https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights)
- [Automatic propagation of inheritable ACEs](https://learn.microsoft.com/en-us/windows/win32/secauthz/automatic-propagation-of-inheritable-aces)
- [Hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Reparse points](https://learn.microsoft.com/en-us/windows/win32/fileio/reparse-points)
