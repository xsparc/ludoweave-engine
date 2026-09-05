# Windows independent-host collection-authority policy

**Status:** Accepted for M209 policy; no privileged harness or qualifying run
is authorized.

This policy defines how a future private harness could receive narrowly scoped
authority to collect the M207 evidence checked by the M208 validator. It does
not add that harness, issue an executable capability, or run a fixture.
Criteria 6 and 7 remain unresolved, `windows_cleanup_admitted is false`,
Windows is not admitted, and cleanup remains unimplemented and unauthorized.

## Authority origin and binding

Only a trusted offline coordinator acting within an operator-controlled test
environment may issue future collection authority. The authority is private,
non-serializable, single-run, single-use, and unavailable to product code. A
fresh authority binds exactly one:

- independently provisioned host ordinal and disposable fixture root;
- profile lane, trial ordinal, barrier ordinal, and interruption class;
- source commit and executable digest;
- M207 contract digest and this policy's contract digest;
- separately reviewed cross-principal evidence digest;
- fixture-recipe digest and capability-profile digest; and
- fixed operation from the allowed collection action set.

The private run manifest records these bindings before any participant starts.
The coordinator rechecks the bound host, storage, fixture sentinel, executable,
policy inputs, and effective channel configuration immediately before issuing
each single-use action. A stale, duplicated, transferred, partially consumed,
or mismatched authority refuses.

Repository content, public evidence, participant output, a pathname, command-
line or MCP input, environment data, a digest alone, a host label, a process
identifier, an account identifier, or a saved manifest cannot mint or widen
collection authority. Credentials and service identities remain outside
repository code and evidence. The future issuer must refuse every missing,
changed, ambiguous, unauthenticated, unsupported, or extra binding.

## Separation from product and cleanup authority

Collection authority is not cleanup authority. It cannot mint M201 cleanup
authority, cannot authorize production cache access, cannot set
windows_cleanup_admitted, and cannot bypass M202 use-time revalidation or the
M203/M204 protocol and recovery requirements. It is valid only inside a fresh
disposable fixture whose root is outside the repository, workspace, user
profile, and every production cache.

Collection performs no canonical world-state mutation. No authority object,
host object, process handle, filesystem handle, credential, native adapter, or
operator identity enters the public engine API. M209 adds no public runtime API
and no CLI or MCP command. A public evidence document is evidence only; it
cannot be replayed as authority.

## Roles and permitted operations

The trusted offline coordinator admits the private run, observes barriers,
mints one action at a time, receives settled observations, and closes the run.
The operator provisions and isolates hosts, retains credentials, controls the
external VM or physical power boundary, reviews teardown, and mediates
artifact transfer. A separate sanitization review occurs after settlement and
before any artifact leaves private custody. A participant cannot attest its own
independence, capability profile, interruption, or teardown.

The future collection action set is closed:

1. observe and revalidate one bound host and fixture profile;
2. launch one fixed fixture participant from the bound executable;
3. advance one deterministic fixture barrier;
4. apply exactly one bound interruption action;
5. restart and reconcile the same current storage instance;
6. collect bounded private observations;
7. settle and tear down the fixture; or
8. stage one private canonical artifact after complete settlement.

No action grants arbitrary command execution, shell input, path selection,
account management, ACL widening, general process termination, production
filesystem access, cleanup, deletion, restoration, or network control.

## Offline channel isolation

Every run is offline. The coordinator, participants, and fixture have no
network listener or network access. Networking disabled is an effective
observed configuration, not an assumed label. There is no package download,
remote control plane, remote logging sink, repository credential, cloud
metadata access, or time-dependent network service during the run.

Clipboard redirection disabled is mandatory. There is no writable mapped
folder and no live host-shared write channel. Any read-only ingress is detached
before the run: ingress completes before the run begins. Artifact egress begins
only after settlement, teardown review, authority expiry, and sanitization.
Windows Sandbox may isolate an auxiliary preparation step only with those
channels disabled; it remains a container and cannot qualify as either M207
independent host.

The harness must not be attached to a public-repository workflow or to any
public self-hosted runner. A workflow token, GitHub token, CI secret, runner
registration token, deploy key, or repository credential cannot be present on
the hosts. There is no GitHub token on a collection host. M209 adds no workflow,
runner label, permission, secret, or hosted allocation.

## Interruption authority

The three M207 interruption classes remain distinct:

- `forced_process_termination` targets only the exact spawned participant or
  coordinator process and descendants bound by retained private process
  identity. It must not target an unbound process, PID-only observation,
  unrelated service, shell, desktop session, or host process.
- `vm_power_cut` acts through an external hypervisor control bound to the exact
  VM and current persistent storage. The action must be equivalent to
  disconnecting power. It uses no guest shutdown, save, pause, checkpoint
  creation, checkpoint restore, snapshot rollback, or replacement disk. A
  restored checkpoint is a different trial and cannot prove crash recovery of
  the interrupted state. There is no checkpoint restore within a trial.
- `physical_host_power_loss` applies only to a dedicated disposable physical
  fixture and its bound storage. The physical action remains operator-only and
  must not be automated by repository code. A VM action, reboot, sleep,
  hibernate, reset label, successful flush, or controller claim cannot replace
  this observation.

Every action is authorized separately at its deterministic barrier. On restart,
recovery reconciles the same affected storage before any new attempt. The
coordinator records the observed action class and outcome without converting a
weaker interruption into a stronger one.

## Private evidence custody

Raw observations remain in private offline storage protected by individual
authentication, access control, and a chronological custody record. The private
run manifest documents each artifact's source, creation, transfer, reviewer,
and disposition. It binds the exact host/action inputs and records every
authorized transition without placing stable machine, storage, principal, or
operator identities in the public document.

A future writer stages each completed private record through atomic same-volume
replacement. The SHA-256 digest retained separately from the staged file is
entered in the custody record before transfer. A digest mismatch, incomplete write,
noncanonical document, failed replacement, or unexplained custody gap
invalidates the affected artifact. Canonical hashes are not authentication,
signatures, or provenance proof.

After teardown, a separate sanitization review checks the exact M207 exclusion
list and the M208 schema before export. Public evidence contains only sanitized
classifications, bounded counts, statuses, ordinals, booleans, and canonical
digests. It contains no hostname, machine or storage identifier, account, SID,
path, environment value, credential, address, PID, session, handle, ACL bytes,
firmware serial, cloud identifier, repository credential, operator contact, or
platform error text. The unchanged M208 validator then independently checks the
exported artifact and its M206 companion.

## Failure, invalidation, and teardown

A binding change, authority replay, unexpected process, channel exposure,
barrier mismatch, wrong interruption, power-controller ambiguity, storage
substitution, observer disagreement, unsafe external effect, custody gap, or
teardown ambiguity must invalidate the affected trial. The coordinator must
not normalize, retry away, or relabel the result as a pass. The exact status
remains failed, unsupported, or not_run as applicable.

Settlement requires no live fixture participant or descendant, no open fixture
handle, no active interruption action, and no pending private write. Collection
authority expires before export. Temporary accounts, credentials, controllers,
and host configuration remain operator-owned and are revoked or returned to
their reviewed pre-run state outside repository code.

If full teardown cannot be proven, the fixture and private evidence are
quarantined for operator review. They are not reused, exported, or treated as
qualifying. Destruction of a disposable fixture is an operator action after
custody and retention decisions; it is not LudoWeave cache cleanup.

## Admission boundary

M209 defines a future authority envelope. M209 does not authorize the privileged
harness, provision hosts, control processes or power, collect evidence, or
satisfy any M199 criterion. No qualifying run has occurred. Criteria 6 and 7
remain unresolved, `windows_cleanup_admitted is false`, Windows is not
admitted, and cleanup remains unimplemented and unauthorized.

A later milestone must separately review and implement the smallest private
harness, prove the controls on disposable offline hosts, and retain all failed,
unsupported, and not-run outcomes. A still-later decision may evaluate complete
validated artifacts against the entire M199-M209 policy chain.

## Primary references

- [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [Windows Sandbox configuration](https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file)
- [Hyper-V `Stop-VM`](https://learn.microsoft.com/en-us/powershell/module/hyper-v/stop-vm)
- [Hyper-V checkpoints](https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/checkpoints)
- [Windows file caching](https://learn.microsoft.com/en-us/windows/win32/fileio/file-caching)
- [NISTIR 8387: Digital Evidence Preservation](https://doi.org/10.6028/NIST.IR.8387)
