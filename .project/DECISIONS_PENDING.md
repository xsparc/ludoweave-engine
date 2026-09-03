# Decisions Pending

No architecture decision is currently blocked.

## M233 Windows source-commit Git message-signer certificate-ID binding

RFC-0216 accepts one direction-preserving, test-only composition: execute
M232's complete correlation in live WinTrust provider state, then retrieve each
exact signer's `CMSG_SIGNER_CERT_ID_PARAM` through a bounded two-phase read.
Validate the explicit discriminant before union access, require the current-
host issuer/serial choice, copy both components within the owning buffer
lifetime, and require equality with M232's same-index legacy selector. Bind
counts, indexes, choices, boundaries, per-index hashes, and one domain-
separated aggregate before and after complete M232.

This binds one explicit execution-local representation. It deliberately
refuses key-ID and hash-ID forms and does not authorize a signer or publisher,
persist identity, pin a certificate, define rotation/recovery, prove revocation
freshness, establish portable chain/timestamp semantics or trust-store
authority, bind native DLL/loader state, authenticate the local object store or
repository acquisition, or provide source/build provenance. Distinct-
principal or independent-host behavior, hostile/privileged bypass, criteria
6/7, cleanup authority, and Windows admission remain pending. No public self-
hosted runner or added hosted check is authorized.

## M232 Windows source-commit Git message-signer certificate-identifier binding

RFC-0215 accepts one direction-preserving, test-only composition: repeat
M231's exact retained-handle cached trust evaluation, retrieve each exact
message signer's `CMSG_SIGNER_CERT_INFO_PARAM` through a bounded two-phase
read, and copy only its issuer and serial-number blobs. Copy those same fields
from the exact verified message certificate and same-index primary provider
certificate while retaining M231's DER equality. Require exact three-source
identifier equality, bind all counts, boundaries, per-source hashes, and one
domain-separated aggregate, and require the same complete observation before
and after M231. Every returned certificate context and provider state closes
after every outcome.

This correlates one execution-local message selector with already byte-equal
verified/provider certificates. It does not authorize a signer or publisher,
persist an identity, create an allowlist or pin, define rotation/recovery,
prove revocation freshness, establish portable chain or timestamp semantics,
authorize a timestamp authority, bind native-loader state, authenticate the
local object store or repository acquisition, or provide source/build
provenance. Distinct-principal or independent-host behavior,
hostile/privileged bypass, criteria 6/7, cleanup authority, and Windows
admission remain pending. No public self-hosted runner or added hosted check is
authorized.

## M231 Windows source-commit Git message-signer certificate binding

RFC-0214 accepts one direction-preserving, test-only composition: repeat
M230's exact retained-handle cached trust evaluation, require bounded equal
provider/message signer counts and a bounded provider-store array, then verify
every exact message signer index with `CryptMsgGetAndVerifySigner`. Copy each
returned bounded certificate before release, resolve the corresponding primary
provider certificate in the same state, require exact DER equality, bind both
hash sequences and one domain-separated aggregate, and require the same
complete observation before and after M230. Every returned certificate context
and provider state closes after every outcome.

This correlates execution-local message and provider certificate identity. It
does not authorize a signer or publisher, make provider stores independently
trusted, persist an identity, create an allowlist or pin, define rotation/
recovery, prove revocation freshness, establish portable chain or timestamp
semantics, authorize a timestamp authority, bind native-loader state,
authenticate the local object store or repository acquisition, or provide
source/build provenance. Distinct-principal or independent-host behavior,
hostile/privileged bypass, criteria 6/7, cleanup authority, and Windows
admission remain pending. No public self-hosted runner or added hosted check is
authorized.

## M230 Windows source-commit Git signed-message SignerInfo binding

RFC-0213 accepts one direction-preserving, test-only composition: repeat
M229's exact retained-handle cached trust evaluation, require a compatible
live provider-message prefix, positive raw encoding, non-null message handle,
and positive bounded provider signer count, then query the exact equal message
count and every encoded SignerInfo by zero-based index through bounded two-
phase `CryptMsgGetParam` retrieval. Copy each exact value before state close;
bind raw encoding, both counts, every boundary, per-signer hashes, and one
domain-separated aggregate; require the same complete observation before and
after M229. Provider state closes after success, rejection, or extraction
failure.

This binds one execution-local opaque encoded-signer sequence. It does not
parse or independently validate SignerInfo, define portable timestamp
semantics, authorize algorithms, attributes, a signer, publisher, or timestamp
authority, persist an identity, pin a certificate, define rotation/recovery,
independently validate a timestamp token or signing time, prove revocation
freshness, establish trust-store authority, bind native DLL/loader state,
authenticate the local object store or repository acquisition, or provide
source/build provenance. Distinct-principal or independent-host behavior,
hostile/privileged bypass, criteria 6/7, cleanup authority, and Windows
admission remain pending. No public self-hosted runner or added hosted check is
authorized.

## M229 Windows source-commit Git countersigner-chain binding

RFC-0212 accepts one direction-preserving, test-only composition: repeat
M228's exact retained-handle cached trust evaluation, then resolve every
countersigner by zero-based provider index and every countersigner certificate
by zero-based provider-chain index while state remains live. Copy positive
per-certificate, per-chain, and aggregate-bounded DER; bind raw signer type,
provider error, verification time, all exact boundaries, per-certificate and
per-chain hashes, and one domain-separated aggregate; require the same complete
observation before and after M228. Provider state closes after success,
rejection, or extraction failure.

This binds one execution-local countersigner provider-index sequence. It does
not establish portable timestamp semantics, authorize a signer, publisher, or
timestamp authority, persist an identity, pin a certificate, define rotation/
recovery, independently validate a timestamp token or signing time, prove
revocation freshness, establish trust-store authority, bind native DLL/loader
state, authenticate the local object store or repository acquisition, or
provide source/build provenance. Distinct-principal or independent-host
behavior, hostile/privileged bypass, criteria 6/7, cleanup authority, and
Windows admission remain pending. No public self-hosted runner or added hosted
check is authorized.

## M228 Windows source-commit Git provider-chain binding

RFC-0211 accepts one direction-preserving, test-only composition: repeat
M227's exact retained-handle cached trust evaluation, then resolve every
provider certificate by zero-based provider index while state remains live.
Copy positive per-certificate and aggregate-bounded DER, compute exact per-
certificate hashes and one domain-separated count/index/length/value digest,
retain the provider's nonzero raw verification time, and require the same
observation before and after M227. Provider state closes after success,
rejection, or extraction failure.

This binds one provider-index sequence within one execution. It does not
define portable leaf/intermediate/root semantics, authorize a signer or
publisher, persist an identity, pin a certificate, define rotation/recovery,
prove revocation freshness or timestamp/countersigner authenticity, establish
trust-store authority, bind native DLL/loader state, authenticate the local
object store or repository acquisition, or provide source/build provenance.
Distinct-principal or independent-host behavior, hostile/privileged bypass,
criteria 6/7, cleanup authority, and Windows admission remain pending. No
public self-hosted runner or added hosted check is authorized.

## M227 Windows source-commit Git signer-certificate binding

RFC-0210 accepts one direction-preserving, test-only composition: repeat
M226's exact retained-handle cached trust evaluation, then resolve live
provider data, the primary signer, and its first provider certificate before
state close. Copy positive bounded DER bytes, hash the detached copy, retain
the provider's nonzero raw verification time, and require the same observation
before and after M226. Provider state closes after success, rejection, or
extraction failure.

This binds one certificate observation within one execution. It is not signer
or publisher authorization, a persisted identity, certificate pin, rotation/
recovery policy, revocation-freshness proof, timestamp/countersigner
authentication, trust-store authority, native DLL/loader binding, local-
object-store trust, repository-acquisition attestation, or source/build
provenance. Distinct-principal or independent-host behavior, hostile/
privileged bypass, criteria 6/7, cleanup authority, and Windows admission
remain pending. No public self-hosted runner or added hosted check is
authorized.

## M226 Windows source-commit Git Authenticode trust

RFC-0209 accepts one direction-preserving, test-only composition: retain the
one real Git selection through M224's existing file handle, then pass that
canonical path and exact readable handle to
`WINTRUST_ACTION_GENERIC_VERIFY_V2` before and after M225's complete boundary.
The verifier must suppress UI and network retrieval, make no-revocation policy
explicit, require exact local trust success, and close provider state after
every verification even when trust is rejected.

This is one cached current-host Windows trust-policy observation. It is not a
signer or publisher allowlist, certificate pin, revocation-freshness proof,
trust-store authority, native DLL/loader binding, local-object-store trust,
repository-acquisition attestation, or source/build provenance. Distinct-
principal or independent-host behavior, hostile/privileged bypass, criteria
6/7, cleanup authority, and Windows admission remain pending. No public self-
hosted runner or added hosted check is authorized.

## M225 Windows source-commit Git child process-image binding

RFC-0208 accepts one direction-preserving, test-only composition: preserve
M224's retained Git executable while each of the 48 inherited CPython Windows
process creations adds `CREATE_SUSPENDED`. Before the primary thread runs,
retain the actual child image and require its normalized path, volume/file
identity, bounded size, and SHA-256 to equal the M224 snapshot. Resume only an
exact initial suspend count of one, preserve normal `Popen` ownership, retain
all image files through settlement, and close them in reverse order.

This binds actual child images to one retained local executable. It is not
executable authenticity, signer/publisher/origin/ACL policy, native DLL/loader
provenance, local-object-store trust, repository acquisition, or source/build
provenance. Distinct-principal or independent-host behavior,
hostile/privileged bypass, criteria 6/7, cleanup authority, and Windows
admission remain pending. No public self-hosted runner or added hosted check is
authorized.

## M224 Windows source-commit Git executable file retention

RFC-0207 accepts one direction-preserving, test-only composition: retain the
canonical Git executable selected once before M223 through a non-inheritable
read handle that permits only `FILE_SHARE_READ`. Require identical normalized
path, volume/file identity, bounded size, and SHA-256 after all 48 inherited
reads and again through a fresh shared post-close handle.

The same retainer's write/delete share behavior is exercised through access-
only opens against its writable test source. This separation prevents an
installed Git file's independent host ACL denial from being misreported as a
sharing-violation result. No file bytes are written, deleted, or renamed.

This is one retained-file interval, not executable authenticity, signer,
publisher, origin, ACL policy, actual child-process image, or native DLL/
loader provenance. Local-object-store trust, repository acquisition,
source/build provenance, distinct-principal or independent-host behavior,
hostile/privileged bypass, criteria 6/7, cleanup authority, and Windows
admission remain pending. No public self-hosted runner or added hosted check is
authorized.

## M223 Windows source-commit Git executable selection binding

RFC-0206 accepts one direction-preserving, test-only composition: resolve
M221's existing Git executable selector once before the complete M222
observation, retain that existing absolute path, and require all 48 fixed
object-read subprocess commands to begin with it. M222's command/environment,
no-lazy-fetch, retained-source, containment, settlement, and participant
requirements remain mandatory. M221 and M222 evidence files remain unchanged.

This binds executable selection, not executable-file content, signer, origin,
path-target replacement, native-loader state, or provenance. Local-object-store
trust, repository acquisition, source/build provenance, distinct-principal or
independent-host behavior, hostile/privileged bypass, criteria 6/7, cleanup
authority, and Windows admission remain pending. No public self-hosted runner
or added hosted check is authorized.

## M222 Windows source-commit no-lazy-fetch exclusion

RFC-0205 accepts one corrective, direction-preserving change: every M221 fixed
Git object read must pass both `--no-lazy-fetch` and a fixed
`GIT_NO_LAZY_FETCH=1` after ambient Git environment values are removed. The
global option precedes repository/object-plumbing arguments, and the complete
M221 contained source-commit boundary remains mandatory.

This excludes implicit promisor retrieval; it does not authenticate the Git
executable or local object store and is not source attestation or build
provenance. Repository acquisition, imported-module/native-loader binding,
distinct-principal behavior, hostile process control, independent-host
evidence, privileged bypass, criteria 6 and 7, cleanup authority, and Windows
admission remain pending. Historical M221 evidence is not rewritten. No public
self-hosted runner or added hosted check is authorized.

## M221 Windows contained source-access source-commit binding probe

RFC-0204 accepts one direction-preserving test-only observation: require
M220's retained fixed contender source to equal the blob selected by the exact
M220 commit, tree, sole parent, repository path, type, size, and SHA-256 before
child creation and after child settlement. Fixed bounded direct Git object
reads fail closed and do not consult moving branch or remote refs.

This is local immutable-object identity, not source provenance attestation or
build provenance. Trust in the Git executable, local object store and
repository acquisition remains pending, as do imported-module/native-loader
binding, distinct-principal behavior, hostile process control,
independent-host evidence, privileged bypass, criteria 6 and 7, cleanup
authority, and Windows admission. No public self-hosted runner or hosted
validation job is authorized by this decision.

## M220 Windows contained source-access source-binding probe

RFC-0203 accepts one direction-preserving test-only observation: retain and
snapshot a new fixed contender source before child creation, execute that open
file as isolated inherited standard input through an exact three-handle
allowlist, and preserve M219 same-logon, interpreter-image, Job, and settlement
requirements. Source and image snapshots must remain stable after exact zero
exit, and source access must settle after controller handles close.

This binds only the executed fixed contender source. Imported standard-library
modules, native DLLs, loader/interpreter state, source-commit provenance, build
provenance, distinct-principal behavior, hostile process control,
independent-host evidence, privileged bypass, criteria 6 and 7, cleanup
authority, and Windows admission remain pending. No public self-hosted runner
or added hosted check is approved.

## M219 Windows contained source-access image-binding probe

RFC-0202 accepts one direction-preserving test-only observation: retain the
expected direct interpreter before child creation, retain M218's suspended
contender process image before resume, and require exact normalized-name,
volume/file-identity, bounded-size, and SHA-256 agreement after same-logon and
sole-Job-member checks. Both retained file observations, M218's three refusal
phases, and the M217 participant boundary must remain stable through settlement.

This does not bind contender script bytes, imported standard-library modules,
native DLLs, loader/interpreter state, source commit, or build provenance. It
does not authorize or establish a distinct principal, hostile process,
independent host, privileged bypass, criterion 6 or 7, cleanup authority, or
Windows admission. Those decisions remain pending. No public self-hosted runner
or added hosted check is approved.

## M218 Windows contained source-access refusal probe

RFC-0201 accepts one direction-preserving test-only observation: a fixed
argument-free same-logon child is assigned suspended to a private kill-on-close
Job before it issues access-only write/delete opens against the retained
participant source. Exact sharing refusal, one-member settlement, unchanged
source bytes, and zero owned handles are required.

This does not authorize or establish a distinct security principal, hostile
process, independent host, privileged bypass, source-commit provenance,
imported standard-library module binding, fixture mutation, collection,
criterion 6 or 7, cleanup authority, or Windows admission. Those decisions
remain pending. No public self-hosted runner or added hosted check is approved.

## M217 Windows retained launch-source remote-debug exclusion probe

RFC-0200 accepts one direction-preserving, test-only composition of
`-X disable_remote_debug` with the exact frozen M212-M216 retained
process/source boundary. M215's original canonical pipe-name validator remains
authoritative; a scoped composer adds only the exclusion option during process
creation and is restored immediately afterward. The full M216 access-refusal,
identity, protocol, settlement, and final-snapshot lifecycle remains required.

Python 3.14 gives the option its documented PEP 768 security meaning. Python
3.12 and 3.13 accept arbitrary `-X` names, so passing observations there are
limited to launch and lifecycle compatibility. The probe performs no remote
attachment, injection, process-memory access, fixture mutation, collection, or
cleanup and adds no runtime/package surface, workflow, public runner, or hosted
allocation.

Deferred decisions remain adversarial process-control evidence, trusted
source-checkout/commit provenance, imported-module binding, hostile ABA/race
evidence, the distinct-principal private harness, account and credential
custody, a disposable offline host cohort, qualifying collection, criteria 6
and 7 resolution, and Windows cleanup admission.

## M216 Windows retained launch-source access-refusal probe

RFC-0199 accepts one direction-preserving, test-only current-host observation
of the M215 retained source's Windows share behavior. While the read-only
source handle is live with read sharing only, access-only `GENERIC_WRITE` and
`DELETE` opens using the competing read/write/delete share mode must fail with
exact `ERROR_SHARING_VIOLATION` before launch, after connection, and after
`ready`. After settlement and retained-handle closure, both opens must succeed
and close without exercising either right, and the source snapshot must remain
unchanged.

The probe deliberately requests access but performs no mutation. It cannot
prove that a future writer or deleter would be authorized by policy, that a
different process or principal sees the same boundary, or that hostile
filesystem races are excluded. It adds no cleanup command, collector,
admission, runtime/package surface, workflow, public runner, or hosted
allocation.

Deferred decisions remain source-checkout provenance, hostile ABA/race
evidence, the distinct-principal private harness, account and credential
custody, a disposable offline host cohort, qualifying collection, criteria 6
and 7 resolution, and Windows cleanup admission.

## M215 Windows retained launch-source binding probe

RFC-0198 accepts one direction-preserving, test-only current-host source-byte
observation layered on the exact frozen M212-M214 boundary. The fixed
participant source is opened read-only, privately snapshotted, rewound, and
inherited as standard input by fixed direct `pythonw.exe -I -B -`. An explicit
`STARTUPINFOEXW` handle list admits only that source and two distinct
write-only `NUL` handles. The source and prior identity bindings must remain
stable after challenge/ready and before release.

The decision avoids a participant script pathname and unstable remote-process
command-line introspection. It does not bind imported standard-library module
bytes, interpreter state, native dependencies, environment outside isolated
mode's exclusions, or source-commit provenance and does not prove hostile ABA
resistance.

Deferred decisions remain the distinct-principal private harness, account and
credential custody, trusted source checkout/commit binding, hostile
filesystem/race evidence, disposable offline host cohort, external VM/operator
power boundaries, qualifying collection, criteria 6 and 7 resolution, and
Windows cleanup admission. No collector, cleanup command, runtime/package
surface, workflow, public runner, or hosted allocation is added.

## M214 Windows retained process-image binding probe

RFC-0197 accepts one direction-preserving, test-only current-host executable
identity observation layered on the exact frozen M212/M213 boundary. A
read-only handle to the fixed direct executable is retained before launch. The
image queried from the retained participant process is opened read-only, and
private normalized-name, volume/file-ID, bounded-size, and SHA-256 snapshots
must match and remain stable across challenge/ready.

The stable uv Python alias and the process-reported versioned target are
normalized through their filesystem target before private name comparison;
retained file identity and digest still must match. No identity value is
serialized. The decision does not bind loaded script/import bytes, command
line, environment, or interpreter state and does not prove hostile ABA
resistance.

Deferred decisions remain the distinct-principal private harness, account and
credential custody, hostile filesystem/race evidence, source-commit binding,
disposable offline host cohort, external VM/operator power boundaries,
qualifying collection, criteria 6 and 7 resolution, and Windows cleanup
admission. No collector, cleanup command, runtime/package surface, workflow,
public runner, or hosted allocation is added.

## M213 Windows local control token-binding probe

RFC-0196 accepts one direction-preserving, test-only current-host probe layered
on the exact frozen M212 control channel. The participant's retained query-only
primary token must match the controller's user, logon, authentication, and
session identity, remain stable across challenge/ready, agree with native pipe
and process session lookups, and revalidate the M212 pipe DACL with its copied
logon SID.

Impersonation is explicitly excluded because retained-token and direct session
queries answer the narrow question without a thread-security transition or a
failed-reversion hazard. Raw SIDs, LUIDs, session/process identifiers, handles,
and pipe names remain private transient test values.

Deferred decisions remain the distinct-principal private harness, account and
credential custody, hostile same-logon and cross-session evidence, disposable
offline host cohort, external VM/operator power boundaries, qualifying
collection, criteria 6 and 7 resolution, and Windows cleanup admission. No
collector, cleanup command, runtime/package surface, workflow, public runner,
or hosted allocation is added.

## M212 Windows local control-channel probe

RFC-0195 accepts one direction-preserving, test-only current-host probe of a
same-logon Windows local control primitive after M211 containment. The accepted
endpoint uses a randomized first-instance, one-instance, remote-rejecting
message pipe with a protected DACL containing exactly one current-logon-SID
allow ACE. Native readback, retained client-process identity, exact Job
membership, a fresh challenge, exact sequences, bounded overlapped controller
I/O, and explicit refusal categories are all required.

The observed generic read/write mapping includes Windows' overlapping pipe-
instance bit; the probe bounds it with the exact logon SID, unpredictable name,
one-instance limit, first-instance ownership, and client identity binding. It
does not exclude a hostile same-logon process and is not cross-principal,
cross-session, independent-host, interruption, durability, recovery, or
admission evidence.

Deferred decisions remain the distinct-principal private harness, credential
and authority custody, hostile connection-race evidence, disposable offline
host cohort, external VM/operator power boundaries, qualifying collection,
criteria 6 and 7 resolution, and Windows cleanup admission. No collector,
cleanup command, runtime/package surface, workflow, public runner, or hosted
allocation is added.

## M211 Windows independent-host process-containment probe

RFC-0194 accepts one direction-preserving, test-only current-host probe of the
future private harness's process-containment primitive. The accepted sequence
uses suspended fixed-interpreter creation, retained-handle Job assignment before
resume, no breakaway, one private output handle, one fixed inherited
descendant, exact two-member Job accounting, and both explicit termination and
kill-on-last-close settlement.

This result does not authorize a collector or cleanup action and is not
independent-host, cross-principal, interruption, durability, recovery, or
admission evidence. Incompatible nested Job assignment remains an explicit
unsupported-host skip; there is no PID-only, ordinary launch, breakaway,
unexpected-member, shell, or public-runner fallback.

Deferred decisions remain the separately reviewed private harness, disposable
offline host cohort, credential and authority custody, external VM power
boundary, operator-only physical interruption, qualifying collection,
criteria 6 and 7 resolution, and Windows cleanup admission.

## M210 Windows independent-host collection-plan validator

RFC-0193 accepts a direction-preserving source-only validator for one sanitized
structural companion to M209's future private run manifest. It validates exact
closed matrices, bounded host classifications, identity syntax, requirements,
and derived totals while forcing collection status `not_run`, authority false,
criteria 6 and 7 false, and Windows admission false.

The reviewed fixture contains no host or stable identity and is parser evidence
only. A structurally complete plan remains neither authentication, provenance,
private executable authority, qualifying evidence, nor an admission decision.
The validator cannot provision a host, mint or consume authority, launch a
process, control power, manage credentials, mutate a fixture, collect evidence,
or authorize cleanup.

The separately reviewed smallest private harness, disposable offline host
cohort, credential custody, native process-tree containment, external VM power
boundary, operator-only physical power action, qualifying collection, criteria
6 and 7 resolution, and Windows cleanup admission remain pending. No workflow
or hosted allocation is added.

## M209 Windows independent-host collection-authority policy

RFC-0192 accepts a direction-preserving policy for any future private M207/M208
evidence collector. A trusted offline coordinator may eventually mint only a
non-serializable, single-run and single-use action bound to one host, fixture,
lane, trial, barrier, interruption class, exact evidence inputs, and closed
operation. Repository input, participant claims, paths, public artifacts, or
digests alone cannot mint or widen that authority.

Collection authority remains separate from M201 cleanup authority, canonical
world commands, production cache access, and Windows admission. Offline hosts
have networking and clipboard disabled, no writable live share, public runner,
or repository credential. Process termination targets only bound fixture
participants; VM power cuts preserve current storage without guest shutdown or
checkpoint restore; physical power loss remains operator-only.

Private collection requires a pre-run manifest, chronological custody, atomic
same-volume staging, separately retained SHA-256, separate sanitization review,
authority expiry, and fail-closed teardown before M208 validation. M209 does
not authorize or implement the privileged harness and produces no qualifying
evidence. Criteria 6 and 7 remain unresolved; Windows cleanup remains
unimplemented and unauthorized. No runtime, native, process, power, credential,
filesystem, dependency, version, workflow, permission, release authority, or
hosted-allocation change is accepted.

## M208 Windows independent-host evidence validator

RFC-0191 accepts one direction-preserving source-only validator for the M207
evidence envelope. It reads one stable canonical independent-host artifact and
one separate M206 artifact, validates the M206 companion through the existing
boundary, recomputes its digest, and derives criterion 6 before evaluating
criterion 7.

The schema contains fixed sanitized host independence, capability, profile,
interruption, status, count, outcome, and digest fields. Passed profile lanes
require at least two passed independent hosts; local fixed NTFS requires the
complete interruption classes, refusal lanes require observed pre-authority
engine refusal, and the ABA lane requires actual identity reuse plus stale-
authorization rejection.

The reviewed fixture has no hosts and all eight profiles `not_run`. Criteria 6
and 7 remain unresolved. Windows cleanup remains unimplemented and
unauthorized, and the admission field remains false even for a structurally
complete artifact pending a later accepted admission decision. No qualifying
run, collector, coordinator, process launch, native call, account or credential
lifecycle, cleanup mutation, runtime command, dependency, version, workflow,
permission, release authority, or hosted allocation is accepted.

## M207 Windows independent-host validation contract

RFC-0190 accepts one direction-preserving, no-authority-increase contract for
future M199 criterion 7 evidence. Every admitted profile needs at least two
independently provisioned Windows hosts with observed operating-system,
filesystem, volume-capability, file-identity, and persistence classifications.
Processes, sessions, containers, reboots, and same-snapshot clones do not
establish host independence.

The future matrix requires local fixed NTFS success plus observed safe refusal
for ReFS, SMB, CsvFS, cross-volume, unknown, and missing-capability profiles,
and explicit file-ID reuse pressure. Forced-process termination, VM power cut,
and physical-host power loss remain distinct evidence classes. Collection is
offline on operator-controlled disposable fixtures and is never attached to a
public-repository self-hosted workflow.

Criterion 6 must pass before criterion 7 can pass. No qualifying artifact or
run exists, so criterion 7 remains unresolved and Windows cleanup remains
unimplemented and unauthorized. No harness, validator, runtime, native call,
process launch, filesystem mutation, account or credential lifecycle,
dependency, version, workflow, permission, release authority, or hosted
allocation is accepted.

## M206 Windows cross-principal evidence validator

RFC-0189 accepts one direction-preserving, source-only validator for the M205
evidence envelope. It reads one stable regular non-symlink file, reuses bounded
canonical JSON, rejects unknown/noncanonical input, and checks exact sanitized
qualification, control, lane, barrier, count, outcome, digest, criterion, and
admission relationships.

The reviewed fixture is intentionally all `not_run`. Structurally valid does
not mean qualifying; only an all-passed complete document can satisfy criterion
6, and M206 always requires the Windows-admission field to remain false.

Criteria 6 and 7 remain unresolved. Windows cleanup remains unimplemented and
unauthorized. No qualifying run, launcher, account or credential lifecycle,
native call, cleanup mutation, runtime command, dependency, version, workflow,
permission, release authority, or hosted allocation is accepted.

## M205 Windows cross-principal validation contract

RFC-0188 accepts one direction-preserving, no-authority-increase contract for
future M199 criterion 6 evidence. A qualifying run uses a genuinely distinct
untrusted local principal under an independently authenticated logon context;
same-user restrictions, integrity changes, AppContainers, impersonation, and
hosted administrator accounts are not substitutes.

The future private fixture requires unrelated process and session topologies,
explicit handle and ACL observations, real hard-link and reparse pressure,
deterministic barriers, bounded observer-derived evidence, and fail-closed
teardown. Accounts and credentials remain operator-owned outside repository
inputs, storage, logs, evidence, and CI.

M205 performs no qualifying run. Criteria 1 through 5 remain resolved as
policy; criteria 6 and 7 remain unresolved. Windows cleanup remains
unimplemented and unauthorized. No runtime, launcher, account mutation,
credential input, adapter, native call, fixture, dependency, workflow,
permission, release authority, version, or CI change is accepted.

## M204 Windows cleanup durable recovery policy

RFC-0187 accepts one direction-preserving, no-authority-increase policy. A
future private recovery store is root-confined and same-volume, admits one
active operation per trusted root and generation, and stores bounded immutable
write-ahead evidence outside canonical world state.

Accepted acknowledgement follows durable intent and replay lookup. Same-volume
quarantine uses the same admitted object, an absent engine-generated target,
and no replacement or copy/delete fallback. Restart reacquires private
authority, replays the complete chain, reconciles exact original/quarantine
observations, and appends only a uniquely justified next record. Restore is
limited to the pre-deletion commit boundary. Ambiguity, invalid chains, unknown
entries, or security/object mismatch block the whole root/generation while
preserving evidence; automatic repair and guessed rollback are excluded.

M204 resolves criterion 5 as policy only. Criteria 1 through 4 remain resolved
as policy. Criteria 6 and 7 remain unresolved, including hostile cross-
principal evidence and independent Windows/filesystem/crash/power-loss proof.
Windows cleanup remains unimplemented and unauthorized. No runtime, recovery
store, adapter, command, protocol constant, public type, dependency, workflow,
permission, version, release authority, or CI change is accepted.

## M203 Windows cleanup protocol and receipt policy

RFC-0186 accepts one direction-preserving, no-authority-increase policy. A
future Windows cleanup boundary uses separate bounded canonical request,
acknowledgement, and receipt documents rather than extending canonical world
transaction protocols.

Requests contain no root, path, candidate, generation, or native data and
cannot mint private authority. Exactly one acknowledgement binds IDs and the
canonical request digest; accepted means only bounded admission and never
mutation or success. A typed receipt binds both request and acknowledgement
digests and exposes only bounded path-free operation-local outcomes. It remains
evidence, not authority, authentication, durability, delivery proof,
non-repudiation, or exactly-once execution.

M203 resolves criterion 4 as policy only. Criteria 1 through 3 remain resolved
as policy. Criteria 5 through 7 remain unresolved, including durable intent,
replay lookup, quarantine/recovery, hostile cross-principal evidence, and
independent-host proof. Windows cleanup remains unimplemented and unauthorized.
No runtime, decoder, public protocol/type, command, transport, receipt store,
dependency, workflow, permission, version, release authority, or CI change is
accepted.

## M202 Windows use-time revalidation policy

RFC-0185 accepts one direction-preserving, no-authority-increase policy. A
future private Windows cleanup adapter must use the same retained effective-
token, trusted-root, durable-generation, acquisition-lineage, and candidate
objects to freshly compare the complete tuple with admission immediately before
every mutation boundary.

Fresh evaluation includes exact effective-token identity/revision, trusted-root
owner/DACL/security digest and least-privilege access, handle-derived
identity/type/link/delete/reparse state, root relationship, and complete
canonical generation-record identity and digest. The same owner retains its
non-reentrant gate and object references into the same-handle mutation without
an application-introduced callback, yield, wait, queue, path lookup, reopen, or
ownership gap.

Failure before the first mutation leaves the candidate untouched. Failure after
a completed transition stops before deletion and enters recovery-required
disposition without guessing rollback. M202 resolves criterion 3 as policy;
criteria 1 and 2 remain resolved as policy, and criteria 4 through 7 remain
unresolved. Windows stays unadmitted, and cleanup stays unimplemented and
unauthorized. No runtime, adapter, command, protocol, receipt, recovery,
dependency, workflow, permission, version, release authority, or CI change is
accepted.

## M201 Windows cleanup-authority admission policy

RFC-0184 accepts one direction-preserving, no-authority-increase policy. A
future private Windows cleanup authority may be issued only by the trusted
composition root after one conjunctive admission binds the exact effective
access-token context, a retained identity/security-bound root, and a separate
immutable root-confined durable generation record.

The effective-token tuple includes user SID, token ID, authentication ID,
modified ID, token type, and impersonation level. The root tuple includes
handle-derived volume/file identity, ordinary non-reparse directory type,
owner SID, non-null trusted DACL, and least-privilege policy. The generation
record separately binds project/cache, root, policy, record identity, and
canonical SHA-256. Every missing, changed, ambiguous, untrusted, invalid, or
unsupported fact refuses before authority issuance.

The future capability is private, engine-owned, non-serializable, operation-
scoped, single-use, cleanup-only, and path/security-material silent.
`AgentCapabilities.write`, CLI/MCP input, project data, paths, environment,
token/logon/process identifiers, and saved evidence cannot mint or widen it.

M201 resolves M199 criterion 1 as policy only. M200's criterion 2 remains
resolved as policy. Criteria 3 through 7 remain unresolved, including
production use-time token/root/security/generation revalidation, typed protocol
and receipts, durable mutation recovery, cross-principal evidence, and
independent-host proof. Windows cleanup remains unimplemented and unauthorized.
No runtime, adapter, generation state, command, dependency, workflow,
permission, version, release authority, or CI change is accepted.

## M200 Windows singleton-link refusal policy

RFC-0183 accepts one direction-preserving, no-authority-increase policy. A
future Windows cleanup candidate is link-eligible only while the same retained
opened object reports a handle-derived link count of exactly one at admission
and immediately before mutation. Zero, multiple, changed, unavailable,
invalid, or unsupported counts refuse before mutation.

Hard-link name enumeration is not admission authority. `FindFirstFileNameW`
and similar results are pathname-based, changing observations; no enumeration,
saved-count, or pathname fallback may turn a candidate eligible. A stable
singleton count remains necessary but not sufficient.

M200 resolves M199 criterion 2 as policy only. Criterion 1 and criteria 3
through 7 remain pending, including production use-time enforcement,
authenticated trusted-root/generation authority, typed protocol and receipts,
durable intent and recovery, cross-principal evidence, and independent-host
proof. Windows cleanup remains unimplemented and unauthorized. No runtime,
fixture, dependency, workflow, hosted allocation, permission, version, release
authority, or cleanup effect is accepted.

## M199 Windows cache-cleanup readiness refresh

RFC-0182 accepts one no-authority-increase readiness checkpoint. The complete
M149-M198 sequence remains 50 current-host, Windows-only, test-only milestones;
its identity, sharing, process, guardian, hard-link, control, and stream
observations do not admit cleanup.

Windows cleanup remains unimplemented and unauthorized. Admission still
requires authenticated trusted-root and generation authority, a complete hard-
link policy, use-time identity and link-count revalidation, acknowledged typed
receipts, durable intent and idempotent recovery, cross-principal adversarial
evidence, and independent-host proof. The standalone method-by-method closed-
stream probe tail closes after M198; a future milestone must resolve one named
criterion rather than add another local method disposition.

M199 adds no runtime, fixture, dependency, workflow, hosted allocation,
permission, version, release authority, cleanup effect, or Windows admission.

## M198 hard-link alias mutator closed-stream write boundary

RFC-0181 accepts one Windows-only, test-only NTFS observation. M197's protected
helper performs the exact terminal invalid settlement, late one-byte buffer
acceptance, first `close()` generic `OSError`, second `close()` returning
`None`, one `flush()` raising generic `ValueError`, and retained closed state.
M198 then calls `write(b"!")` exactly once, requires generic `ValueError`, and
requires the stream still closed. This is local concrete-stream disposition,
not evidence of native-call suppression, delivery retry, or acknowledgement.

The result remains one current-host, three-process, same-principal observation.
It adds no runtime, fixture, dependency, workflow, hosted allocation,
permission, release authority, version, or Windows admission. Authenticated
root and generation authority, explicit framing, acknowledgements, native-call
tracing, link policy, use-time revalidation, durable intent, idempotent
recovery, reconciliation, typed receipts, cross-principal evidence, and
independent-host proof remain future design work.

## M197 hard-link alias mutator closed-stream flush boundary

RFC-0180 accepts one Windows-only, test-only NTFS observation. M196's protected
helper performs the exact terminal invalid settlement, late one-byte buffer
acceptance, first `close()` generic `OSError`, second `close()` returning
`None`, and retained closed state. M197 then calls `flush()` exactly once,
requires generic `ValueError`, and requires the stream still closed. This is
local concrete-stream disposition, not evidence of a second native write,
delivery retry, or acknowledgement.

The result remains one current-host, three-process, same-principal observation.
It adds no runtime, fixture, dependency, workflow, hosted allocation,
permission, release authority, version, or Windows admission. Authenticated
root/generation authority, explicit framing, acknowledgements, native-call
tracing, link policy, use-time revalidation, durable intent, idempotent
recovery, reconciliation, typed receipts, cross-principal evidence, and
independent-host proof remain future design work.

## M196 hard-link alias mutator repeated buffered-close boundary

RFC-0179 accepts one Windows-only, test-only NTFS observation. M195's protected
helper performs the exact terminal invalid settlement, late one-byte buffer
acceptance, and first `close()` that raises generic `OSError` while leaving the
stream closed. M196 then calls `close()` exactly once more, requires `None`,
and requires the stream still closed. The second call is local no-op
disposition, not a delivery retry or acknowledgement.

The result remains one current-host, three-process, same-principal observation.
It adds no runtime, fixture, dependency, workflow, hosted allocation,
permission, release authority, version, or Windows admission. Authenticated
root/generation authority, explicit framing, acknowledgements, link policy,
use-time revalidation, durable intent, idempotent recovery, reconciliation,
typed receipts, cross-principal evidence, and independent-host proof remain
future design work.

## M195 hard-link alias mutator buffered-close delivery-failure boundary

RFC-0178 accepts one Windows-only, test-only NTFS observation. After M186's
unchanged bounded-output mutator has rejected exact `?!`, emitted no `closed`,
and settled with exit 5 while the parent writer remains open, the parent
buffers one late valid `!` byte. Without a preceding failed late flush, direct
`close()` raises generic `OSError` and still leaves the writer closed. No
exception subtype or numeric code is part of the boundary.

The peer alias retains shared identity, bytes, two-link count, and range
availability while M181's matching guardian remains protective. This resolves
only close-triggered delivery and local stream disposition for one late byte
and fixture on the observed host. It is not general framing, acknowledgement,
authenticated authority, durable recovery, or cleanup admission.

Pre-settlement/concurrent late commands; arbitrary buffered, partial, repeated,
or larger input; exact exception translation; duplicated/inherited writers;
cross-principal and unrelated-process behavior; simultaneous racing; trusted-
root placement; enumeration and use-time policy; durable intent, quarantine,
idempotency, reconciliation, typed recovery receipts; independent-host proof;
Windows admission; and cleanup authority remain pending. No runtime,
dependency, fixture, workflow, permission, hosted allocation, release
authority, or CI change is accepted.

## M194 hard-link alias mutator late valid-close delivery-failure boundary

RFC-0177 accepts one Windows-only, test-only NTFS observation. After M186's
unchanged bounded-output mutator has rejected exact `?!`, emitted no `closed`,
and settled with exit 5 while the parent writer remains open, the parent writes
one late valid `!` byte. The buffered call accepts one byte locally, but
`flush()` fails with generic `OSError` because the child can no longer receive
it. No exception subtype or numeric code is part of the boundary.

The peer alias retains shared identity, bytes, two-link count, and range
availability while M181's matching guardian remains protective. This resolves
only local buffer acceptance versus peer delivery for one late byte and fixture
on the observed host. It is not general framing, acknowledgement,
authenticated authority, durable recovery, or cleanup admission.

Pre-settlement/concurrent late commands; arbitrary buffered, partial, repeated,
or larger input; exact exception translation; duplicated/inherited writers;
cross-principal and unrelated-process behavior; simultaneous racing; trusted-
root placement; enumeration and use-time policy; durable intent, quarantine,
idempotency, reconciliation, typed recovery receipts; independent-host proof;
Windows admission; and cleanup authority remain pending. No runtime,
dependency, fixture, workflow, permission, hosted allocation, release
authority, or CI change is accepted.

## M193 hard-link alias mutator open-writer invalid-prefix settlement boundary

RFC-0176 accepts one Windows-only, test-only NTFS observation. After M186's
unchanged bounded-output mutator emits exact `recreated`, the parent writes
fixed `?!` once, requires both bytes accepted, flushes, and keeps its control
writer open across the bounded wait. The child rejects the invalid leading
byte, emits no `closed` event, and exits 5 while the writer remains open.
Stdout is EOF and stderr empty before the parent closes that writer.

The peer alias retains shared identity, bytes, two-link count, and range
availability while M181's matching guardian remains protective. This resolves
only the distinction between invalid-byte settlement and control-pipe EOF for
one fixed sequence and bounded-output fixture on the observed host. It is not
general framing, authenticated authority, durable recovery, or cleanup
admission.

Arbitrary malformed, partial, separate, repeated, or longer input; arbitrary
or unbounded output; duplicated/inherited writers; cross-principal and
unrelated-process behavior; simultaneous racing; trusted-root placement;
enumeration and use-time policy; durable intent, quarantine, idempotency,
reconciliation, typed recovery receipts; independent-host proof; Windows
admission; and cleanup authority remain pending. No runtime, dependency,
fixture, workflow, permission, hosted allocation, release authority, or CI
change is accepted.

## M192 hard-link alias mutator invalid-prefix valid-close-suffix boundary

RFC-0175 accepts one Windows-only, test-only NTFS observation. After M186's
unchanged mutator child emits exact `recreated`, the parent writes fixed `?!`
once, requires both bytes accepted, flushes, and closes its writer. The child
rejects the invalid leading byte, emits no `closed` event, and settles with exit
5, stdout EOF, and empty stderr while M181's matching guardian remains live and
protective.

The peer alias remains present. Original and alias retain shared identity,
bytes, two-link count, and range availability until exact guardian close
permits rename. This resolves only one fixed leading-byte case on the observed
host. It is three-process, same-principal evidence under one parent-owned
process tree, not general message framing, authenticated authority, durable
commit, recovery, or cleanup admission.

Arbitrary malformed, partial, separate, repeated, or longer input;
duplicated/inherited writers; cross-principal and unrelated-process behavior;
simultaneous racing; explicit framing; trusted-root placement; enumeration and
use-time policy; durable intent, quarantine, idempotency, reconciliation, typed
recovery receipts; independent-host proof; Windows admission; and cleanup
authority remain pending. No runtime, dependency, fixture, workflow,
permission, hosted allocation, release authority, or CI change is accepted.

## M191 hard-link alias mutator valid-close-prefix trailing-byte boundary

RFC-0174 accepts one Windows-only, test-only NTFS observation. After M186's
unchanged mutator child emits exact `recreated`, the parent writes fixed `!?`
once and flushes. The child consumes the valid leading byte, emits exact
`closed` while the parent writer remains open, and settles with exit 0, stdout
EOF, and empty stderr while M181's matching guardian remains live and
protective.

The peer alias remains present. Original and alias retain shared identity,
bytes, two-link count, and range availability until exact guardian close
permits rename. This resolves only one fixed byte-prefix case on the observed
host. It is three-process, same-principal evidence under one parent-owned
process tree, not general message framing, authenticated authority, durable
commit, recovery, or cleanup admission.

Arbitrary malformed, partial, separate, repeated, or longer input;
duplicated/inherited writers; cross-principal and unrelated-process behavior;
simultaneous racing; explicit framing; trusted-root placement; enumeration and
use-time policy; durable intent, quarantine, idempotency, reconciliation, typed
recovery receipts; independent-host proof; Windows admission; and cleanup
authority remain pending. No runtime, dependency, fixture, workflow,
permission, hosted allocation, release authority, or CI change is accepted.

## M190 hard-link alias mutator post-recreate invalid-control boundary

RFC-0173 accepts one Windows-only, test-only NTFS observation. M186's unchanged
mutator child deletes the fixed peer alias, receives the exact recreate token,
recreates the alias, and emits exact `recreated`; before any close token, the
parent writes exactly one fixed invalid `?` byte, flushes and closes its writer,
and waits with the existing fixed bound. The child settles with exact exit 5,
no `closed` event, stdout EOF, and empty stderr while M181's matching guardian
remains live and protective.

The peer alias remains present after invalid-control settlement. Original and
alias retain shared identity, bytes, two-link count, and range availability
until exact guardian close permits rename. This resolves only the residual
state for one fixed invalid byte at this controlled protocol phase on the
observed host: there is no automatic rollback to one link. It remains
three-process, same-principal evidence under one parent-owned process tree,
distinct from control-pipe EOF and abrupt termination and not durable commit
or recovery evidence.

Arbitrary malformed, partial, or multiple input, authenticated cancellation,
duplicated or inherited control writers, cross-principal and unrelated-process
behavior, simultaneous racing, crash and power-loss consistency, trusted-root
placement, enumeration, use-time policy, durable intent, quarantine,
idempotency, reconciliation, typed recovery receipts, independent-host proof,
Windows admission, and cleanup authority remain pending. No runtime,
dependency, fixture, workflow, permission, hosted allocation, release
authority, or CI change is accepted.

## M189 hard-link alias mutator post-recreate control-EOF boundary

RFC-0172 accepts one Windows-only, test-only NTFS observation. M186's unchanged
mutator child deletes the fixed peer alias, receives the exact recreate token,
recreates the alias, and emits exact `recreated`; before any close token, the
parent closes only its `Popen.stdin` writer and waits with the existing fixed
bound. The child settles with exact exit 5, no `closed` event, stdout EOF, and
empty stderr while M181's matching guardian remains live and protective.

The peer alias remains present after control-pipe EOF. Original and alias
retain shared identity, bytes, two-link count, and range availability until
exact guardian close permits rename. This resolves only the residual state for
this controlled protocol phase on the observed host: there is no automatic
rollback to one link. It remains three-process, same-principal evidence under
one parent-owned process tree, not abrupt termination, durable commit, or
recovery evidence.

Cross-principal and unrelated-process behavior, duplicated/inherited control
writers, simultaneous racing, crash and power-loss consistency, trusted-root
placement, enumeration, use-time policy, durable intent, quarantine,
idempotency, reconciliation, typed recovery receipts, independent-host proof,
Windows admission, and cleanup authority remain pending. No runtime,
dependency, fixture, workflow, permission, hosted allocation, release
authority, or CI change is accepted.

## M188 hard-link alias mutator post-recreate abrupt-loss boundary

RFC-0171 accepts one Windows-only, test-only NTFS observation. M186's unchanged
mutator child deletes the fixed peer alias, receives the exact recreate token,
recreates the alias, and emits exact `recreated`; before any close token, the
parent terminates and reaps the child and requires a nonzero exit with no
remaining output. M181's matching guardian remains live and continues
protecting the exact original name.

The peer alias remains present after the mutator is reaped. Original and alias
retain shared identity, bytes, two-link count, and range availability until
exact guardian close permits rename. This resolves only the residual state for
this controlled failure phase on the observed host: there is no automatic
rollback to one link. It remains three-process, same-principal evidence under
one parent-owned process tree, not durable commit or recovery evidence.

Cross-principal and unrelated-process behavior, simultaneous racing, crash and
power-loss consistency, trusted-root placement, enumeration, use-time policy,
durable intent, quarantine, idempotency, reconciliation, typed recovery
receipts, independent-host proof, Windows admission, and cleanup authority
remain pending. No runtime, dependency, fixture, workflow, permission, hosted
allocation, release authority, or CI change is accepted.

## M187 hard-link alias mutator abrupt-loss boundary

RFC-0170 accepts one Windows-only, test-only NTFS observation. M186's unchanged
mutator child deletes the fixed peer alias and emits exact `deleted`; the
parent then sends no recreate token, terminates and reaps the child, and
requires a nonzero exit with no remaining output. M181's matching guardian
remains live and continues protecting the exact original name.

The peer alias remains absent after the mutator is reaped. The original retains
its identity, bytes, one-link count, and range availability until exact
guardian close permits rename. This resolves only the residual state for this
controlled failure phase on the observed host: there is no automatic rollback
or recovery. It remains three-process, same-principal evidence under one
parent-owned process tree.

Cross-principal and unrelated-process behavior, simultaneous racing, crash and
power-loss consistency, trusted-root placement, enumeration, use-time policy,
durable intent, quarantine, idempotency, reconciliation, typed recovery
receipts, independent-host proof, Windows admission, and cleanup authority
remain pending. No runtime, dependency, fixture, workflow, permission, hosted
allocation, release authority, or CI change is accepted.

## M186 independent hard-link alias mutation actor boundary

RFC-0169 accepts one Windows-only, test-only NTFS observation. M181's matching
guardian child protects the exact coordination name while a distinct sibling
mutator child deletes and recreates the fixed peer alias through exact bounded
handshakes. The parent only coordinates and observes. Identity, bytes, range
availability, guardian liveness, and exact-name rename refusal remain stable as
link count changes `2 -> 1 -> 2`.

This resolves only whether the M185 result depends on the parent process owning
the mutation calls: it does not on the observed host. The evidence contains
three processes under one principal and one parent-owned process tree. It is
not cross-principal, unrelated-session, hostile-process, simultaneous-race,
trusted-root, enumeration, recovery, admission, or cleanup-authority evidence.
Windows remains unadmitted.

No runtime, dependency, workflow, permission, hosted allocation, release
authority, or CI change is accepted. The existing Windows suite remains the
only future hosted execution path.

## M185 hard-link alias delete/recreate ABA boundary

RFC-0168 accepts one Windows-only, test-only NTFS observation. A coordination
file and peer alias begin with the same `FILE_ID_INFO` and link count two.
While M181's matching guardian child remains live, the parent deletes the
alias, observes count one, recreates the same pathname, and observes count two
through both names. Identity, bytes, range availability, guardian liveness,
and exact-name rename refusal remain stable across the transition.

This resolves only whether guardian admission freezes membership of one peer
pathname: it does not on the observed host. It also corrects M184's process
classification; the mutation actor and guardian are two processes under one
principal. Trusted root placement, link enumeration, cross-principal behavior,
an independent third actor, controlled concurrent racing, link-count policy,
use-time revalidation, file-ID reuse, filesystem variation, durable generation,
recovery, typed receipts, cleanup authority, independent-host proof, and
Windows admission remain pending.

RFC-0168 does not authorize runtime code, a public probe, native declarations,
cache access, mutation, dependency, workflow, CI allocation, permission,
release authority, or publication. No hosted check is added.

## M184 hard-link alias deletion non-exclusion boundary

RFC-0167 accepts one Windows-only, test-only NTFS observation. A coordination
file and peer alias begin with the same `FILE_ID_INFO` and link count two.
While M181's matching guardian is live, rename of the exact opened name fails
with sharing error 32, but deletion of the peer alias succeeds. The original
handle reports link count one and the guardian continues protecting its exact
name.

This resolves only the initial all-links deletion-exclusion hypothesis: it is
false on the observed host. Exact-name protection and a surviving one-link
sample are not root-confined ownership. Trusted root placement, link
enumeration, cross-principal behavior, an independent third mutation actor,
POSIX-delete flags, link-count
policy, use-time revalidation, file-ID reuse, filesystem variation, durable
generation, recovery, typed receipts, cleanup authority, independent-host
proof, and Windows admission remain pending.

RFC-0167 does not authorize runtime code, a public probe, native declarations,
cache access, mutation, dependency, workflow, CI allocation, permission,
release authority, or publication. No hosted check is added.

## M183 post-admission hard-link creation boundary

RFC-0166 accepts one Windows-only, test-only NTFS observation. A coordination
file begins with link count one and is admitted by M181's matching guardian.
While that guardian remains live, `os.link` creates a peer alias; both handles
retain one `FILE_ID_INFO` and report link count two. The guardian continues to
protect the exact name it opened.

This resolves only whether current guardian admission freezes the link set: it
does not on the observed host. Expected identity and a prior count sample are
not root-confined ownership. Trusted root placement, link enumeration,
cross-principal behavior, an independent third mutation actor, alias deletion,
link-count policy, use-time
revalidation, file-ID reuse, filesystem variation, durable generation,
recovery, typed receipts, cleanup authority, independent-host proof, and
Windows admission remain pending.

RFC-0166 does not authorize runtime code, a public probe, native declarations,
cache access, mutation, dependency, workflow, CI allocation, permission,
release authority, or publication. No hosted check is added.

## M182 hard-link alias non-exclusion boundary

RFC-0165 accepts one Windows-only, test-only NTFS observation. A preexisting
peer hard link has the same `FILE_ID_INFO` and a link count of at least two.
While M181's matching guardian is live, rename of the exact opened
coordination name fails with sharing error 32, but rename of the alias
succeeds. The guardian remains live and continues protecting the exact name.

This resolves only the original all-names protection hypothesis: it is false
on the observed host. Expected identity is not sole-name authority and not
root-confined ownership. Trusted root placement, link enumeration,
post-admission link creation, alias deletion, link-count policy, use-time
revalidation, file-ID reuse, filesystem variation, durable generation,
recovery, typed receipts, cleanup authority, independent-host proof, and
Windows admission remain pending.

RFC-0165 does not authorize runtime code, a public probe, native declarations,
cache access, mutation, dependency, workflow, CI allocation, permission,
release authority, or publication. No hosted check is added.

## M181 expected-identity guardian admission probe

RFC-0164 accepts one Windows-only, test-only guardian fixture and two
current-host observations. The child denies delete sharing before comparing a
caller-supplied expected `FILE_ID_INFO` on that same opened handle. It admits a
match while retaining the handle and closes before reporting exact
`identity_mismatch` for a preexisting replacement.

This resolves only the measured same-handle admission ordering. It does not
establish trusted identity provenance, authenticated or durable storage,
generation issuance, guardian election, startup recovery, or policy. Failed
launch, simultaneous owner loss, hostile prior handles, arbitrary process
trees, mapped views, filesystem/driver variation, use-time revalidation,
typed receipts, independent-host proof, and Windows admission remain pending.

RFC-0164 does not authorize a runtime adapter, guardian or lock API,
participant registry, cache access, retained-root integration, candidate
disclosure, cleanup or mutation authority, dependency, workflow, CI
allocation, tag, release, or publication. No hosted check is added.

The supported-Python, repeated Windows, real-wgpu, profile, vertical-slice,
documentation, governance, installed-wheel, release-smoke, findings-first,
and public-hygiene gates support only this bounded observation. They do not
resolve any pending production authority above.

## M180 zero-owner guardian restart-boundary probe

RFC-0163 accepts two Windows-only, test-only post-wait observations. Without
intervening mutation, a later unchanged guardian opens and protects the same
coordination identity. If M174 substitution occurs during the zero-owner
interval, a later guardian instead protects the replacement identity and
blocks a second rename only until its exact close.

This resolves only the measured pathname-open behavior. It demonstrates that
successful guardian restart is not continuity: a pathname-only guardian has no
trusted record with which to identify or recover the displaced generation. It
is not crash recovery, durable generation authority, election,
authentication, trusted placement, or complete admission. Simultaneous loss,
failed launch, hostile prior handles, arbitrary process trees, mapped views,
filesystem/driver variation, generation issuance/retention, use-time
revalidation, policy, receipts, independent-host proof, and Windows admission
remain pending.

RFC-0163 does not authorize a runtime adapter, guardian or lock API,
participant registry, cache access, retained-root integration, candidate
disclosure, cleanup or mutation authority, dependency, workflow, CI
allocation, tag, release, or publication. No hosted check is added.

The supported-Python, integrated and repeated Windows, real-wgpu, profile,
vertical-slice, documentation, governance, installed-wheel, release-smoke,
findings-first, and public-hygiene gates support only these bounded
observations. They do not resolve any pending production authority above.

## M179 overlapping coordination-guardian rotation probe

RFC-0162 accepts one Windows-only, test-only observation that two unchanged
M178 guardians may overlap with one M175 protected participant on the same
coordination identity. After the first guardian is abruptly killed and reaped,
the second guardian and participant retain protection. After participant
close, the second guardian alone retains substitution error 32 while exact
exclusive range ownership is available.

This resolves only one exact current-host overlapping rotation. It is not
guardian discovery, election, restart after failure, crash recovery,
generation authority, trusted placement, or complete admission. A zero-owner
interval, failed replacement start, simultaneous owner loss, hostile prior
handles, arbitrary guardian counts and process trees, mapped views, filesystem
variation, durable generation issuance/retention, use-time revalidation,
policy, receipts, independent-host proof, and Windows admission remain pending.

RFC-0162 does not authorize a runtime adapter, guardian or lock API,
participant registry, cache access, retained-root integration, candidate
disclosure, cleanup or mutation authority, dependency, workflow, CI
allocation, tag, release, or publication. No hosted check is added.

The supported-Python, integrated Windows, repeated live, real-wgpu, profile,
vertical-slice, documentation, governance, installed-wheel, release-smoke,
findings-first, and public-hygiene gates support only this bounded observation.
They do not resolve any pending production authority above.

## M178 guardian abrupt-handoff probe

RFC-0161 accepts one Windows-only, test-only observation that a fixed
noninheritable no-delete-share guardian may be abruptly terminated and reaped
after an M175 protected participant has joined the same coordination identity.
The still-live participant must retain substitution error 32 and exclusive-
range error 33 until its own exact close.

This resolves only one exact post-wait overlapping ownership chain. It is not
guardian restart, crash recovery, generation authority, trusted placement, or
complete admission. A zero-owner interval, multiple guardians, hostile prior
handles, arbitrary process trees, mapped views, filesystem variation, durable
generation issuance/retention, use-time revalidation, policy, receipts,
independent-host proof, and Windows admission remain pending.

RFC-0161 does not authorize a runtime adapter, guardian or lock API,
participant registry, cache access, retained-root integration, candidate
disclosure, cleanup or mutation authority, dependency, workflow, CI
allocation, tag, release, or publication. No hosted check is added.

The supported-Python, corrected cross-version focused, integrated Windows,
repeated live, real-wgpu, profile, vertical-slice, documentation, governance,
installed-wheel, release-smoke, findings-first, and public-hygiene gates
support only this bounded observation. They do not resolve any pending
production authority above.

## M177 protected coordination guardian-handoff probe

RFC-0160 accepts one Windows-only, test-only observation that a private
noninheritable no-delete-share guardian can preserve one coordination identity
through a participant-free range-lock interval. With only the guardian live,
M174 pathname substitution must fail with error 32 while M173 exclusive range
acquire/release succeeds. A later M175 participant must join the same identity
and retain substitution and exclusive-range refusal after guardian release.

This resolves only one exact current-host continuous ownership chain. The
guardian does not own the byte range and is not generation authority. Trusted
root placement, guardian startup/crash recovery, complete admission, hostile
preexisting handles, mapped views, arbitrary termination, filesystem
variation, durable generation issuance/retention, use-time revalidation,
policy, receipts, independent-host proof, and Windows admission remain pending.

RFC-0160 does not authorize a runtime adapter, guardian or lock API,
participant registry, cache access, retained-root integration, candidate
disclosure, cleanup or mutation authority, dependency, workflow, CI
allocation, tag, release, or publication. No hosted check is added.

The supported-Python, integrated Windows, repeated live, real-wgpu, profile,
vertical-slice, documentation, governance, installed-wheel, release-smoke, and
findings-first gates support only this bounded test observation. Review removed
one redundant assertion-failure guardian release; context ownership and an
architecture guard now prevent that double-close path. The evidence does not
resolve any of the pending production authorities above.

## M176 protected coordination-lock abrupt-settlement probe

RFC-0159 accepts one Windows-only, test-only observation that killing and
boundedly waiting for one of two M175 protected participants releases only the
terminated participant. The survivor remains live and continues to refuse
M174 pathname substitution with error 32 and M173 exclusive range ownership
with error 33. Killing and reaping the survivor then permits exact exclusive
acquire/release and M174 substitution with the retained identity split.

This resolves the exact current-host abrupt-settlement order only. Microsoft
warns that operating-system range-lock release can be delayed by available
resources, so no portable immediate-release deadline is inferred. Arbitrary
termination timing, process trees, startup/crash recovery, job objects,
trusted root and coordination identity, generation issuance/retention,
complete admission, mapped views, filesystem variation, policy, receipts, and
independent-host proof remain pending. The zero-participant substitution gap
remains and Windows is not admitted.

RFC-0159 does not authorize a runtime adapter or lock API, participant
registry, cache access, retained-root integration, candidate disclosure,
cleanup or mutation authority, dependency, workflow, CI allocation, tag,
release, or publication. No hosted check is added.

## M175 live cooperative substitution-exclusion probe

RFC-0158 accepts one Windows-only, test-only observation that two shared
`LockFileEx` participants which omit `FILE_SHARE_DELETE` continuously refuse
M174's pathname substitution with native sharing error 32. The same live
participants continue to refuse an exclusive range owner with native lock
error 33 through the final participant's exact release.

After the final participant closes, exclusive acquire/release succeeds and the
unchanged M174 substitution succeeds. `FILE_ID_INFO` proves the displaced file
retains the original identity while its replacement differs. This resolves the
exact cooperative live-ownership question only. A zero-participant interval,
uncooperative actors, trusted root and coordination identity, generation
issuance and revalidation, complete admission, mapped views, abrupt-exit
settlement, filesystem variation, recovery, policy, receipts, and independent-
host proof remain pending. Windows is not admitted.

RFC-0158 does not authorize a runtime adapter or lock API, participant
registry, cache access, retained-root integration, candidate disclosure,
cleanup or mutation authority, dependency, workflow, CI allocation, tag,
release, or publication. No hosted check is added.

## M174 Windows cooperative-lock substitution probe

RFC-0157 accepts one Windows-only, test-only observation that an M173 shared
participant remains bound to the original coordination file after its pathname
is renamed and replaced. `FILE_ID_INFO` proves the displaced original retains
the old identity while the replacement has another. An unchanged fresh
participant locks the replacement concurrently, and both lock generations
settle independently.

This resolves the exact current-host pathname-substitution question as negative
capability evidence. A reusable pathname is insufficient stable authority.
Trusted root identity, coordination identity, generation issuance and
revalidation, uncooperative actors, participant completeness, mapped views,
abrupt-exit settlement, filesystem variation, recovery, policy, receipts, and
independent-host proof remain pending. Windows is not admitted.

RFC-0157 does not authorize a runtime adapter or identity registry, lock API,
cache access, retained-root integration, candidate disclosure, cleanup or
mutation authority, dependency, workflow, CI allocation, tag, release, or
publication. No hosted check is added.

## M173 Windows cooperative-lock probe

RFC-0156 accepts one Windows-only, test-only observation over one fixed
coordination file and byte range. Two distinct shared `LockFileEx` participants
coexist and collectively refuse a fail-immediate exclusive owner through the
last exact release. In reverse order, the exclusive owner refuses a late
shared participant until exact unlock/close. Every handle is noninheritable,
every successful lock is explicitly unlocked, and bytes remain unchanged.

This resolves only the exact current-host NTFS cooperative same-object/range
transition. Uncooperative actors, coordination identity and substitution,
generation binding, complete retained roots, mapped views, cancellation,
abrupt process death, delayed operating-system unlock, native unlock/close
failure, filesystem variation, recovery, policy, receipts, and independent-
host proof remain pending. Windows is not admitted.

RFC-0156 does not authorize a runtime adapter or lock API, participant
registry, cache access, retained-root integration, candidate disclosure,
cleanup or mutation authority, dependency, workflow, CI allocation, tag,
release, or publication. No hosted check is added.

## M172 Windows descendant non-exclusion probe

RFC-0155 accepts one Windows-only, test-only observation that M171's
zero-sharing directory owner and a separately opened descendant file owner can
coexist in either acquisition order. Both remain live simultaneously, close
independently, preserve exact content, and leak no parent ownership. This is
negative capability evidence: the directory primitive is object-specific and
is not a recursive subtree lock. Windows is not admitted.

This resolves only the exact current-host NTFS generic-read/all-sharing
descendant observation. Writes, deletes, mappings, descendant directories,
multiple participants, oplocks, leases, cancellation, process death, native
close failure, filesystem variation, recovery, policy, receipts, and
independent-host proof remain pending.

RFC-0155 does not authorize a runtime adapter or lock, participant registry,
cache access, retained-root integration, candidate disclosure, cleanup or
mutation authority, dependency, workflow, CI allocation, tag, release, or
publication. No hosted check is added.

## M171 Windows exclusive-root acquisition probe

RFC-0154 accepts one Windows-only, test-only two-way observation around one
ordinary directory representing a selected cache root. A private parent owner
uses sharing mode zero and refuses a fixed late child until deterministic
close. In the reverse direction, M155's fixed child remains live while the
parent's identical acquisition fails with native error 32 and adopts no owner;
only the child's acknowledged close and zero exit permit acquisition. Every
successful parent handle is noninheritable.

This resolves only the exact current-host ordinary-directory sharing-mode
transition. Attribute-only access, mapped files, oplocks, leases, descendants,
access/share permutations, multiple participants, cancellation, native close
failure, filesystem variation, recovery, complete quiescence, and independent-
host proof remain pending. Windows is not admitted.

RFC-0154 does not authorize a runtime lock, public probe, production subprocess
or native call, cache access, cleanup authority, retained-root integration,
candidate policy, recovery, dependency, workflow, CI allocation, tag, release,
or publication. No hosted check is added.

## M170 Windows concurrent explicit-list abrupt-termination probe

RFC-0153 accepts one Windows-only, test-only controlled observation in which
two copies of M163's fixed child start simultaneously with distinct explicit
handle lists. After both parent flags restore and both parent handles close,
one assigned child is forcibly terminated and reaped. Only its root renames;
the survivor remains live and blocks only its own root until acknowledged
zero-exit close. Both A/B role assignments pass and every owner settles.

This resolves only the exact current-host two-successful-child, one-forced-
termination interleaving after parent release. Crash recovery, cancellation
semantics, arbitrary termination timing, native close failures, a concurrency-
safe process-creation contract, general leak-freedom, recovery, and
independent-host proof remain pending. Windows is not admitted.

RFC-0153 does not authorize runtime subprocess or `ctypes`, modification of an
accepted helper or fixture, a process-global coordinator, production adapter,
public capability, cleanup authority, recovery policy, dependency, workflow,
CI allocation, tag, release, or publication. No hosted check is added.

## M169 Windows concurrent explicit-list restoration-failure probe

RFC-0152 accepts one Windows-only, test-only controlled observation in which
two copies of M163's fixed child start with distinct explicit handle lists and
one M165-style restoration error is injected after both real children exist.
The helper reaps only the failed side's child before the same error escapes.
After explicit flag repair and both parent closes, the failed-restoration root
renames while the survivor still blocks only its own root; that root renames
only after the survivor closes. Both A/B role assignments pass and every owner
settles.

This resolves only the exact current-host successful/synthetic-restoration-
failure interleaving. A real native restoration failure, a concurrency-safe
process-creation contract, arbitrary launch or restoration failures,
cancellation, reentrancy, every broad and explicit creator, invalid handles,
child crashes, cross-process transfer, native close failure, general leak-
freedom, recovery, and independent-host proof remain pending. Windows is not
admitted.

RFC-0152 does not authorize runtime subprocess or `ctypes`, modification of an
accepted helper or fixture, a process-global coordinator, production adapter,
public capability, cleanup authority, recovery policy, dependency, workflow,
CI allocation, tag, release, or publication. No hosted check is added.

## M168 Windows concurrent explicit-list launch-failure probe

RFC-0151 accepts one Windows-only, test-only controlled observation in which
M163's fixed child starts concurrently with M164's distinct real missing-
executable failure. Both parent blockers remain inheritable through both real
outcomes and both restoration entries. After both parent handles close, the
failed-launch root immediately renames while the successful child still blocks
only its own root; that root renames only after the child closes. Both A/B role
assignments pass and every owner settles.

This resolves only the exact current-host successful/missing-executable
interleaving. A concurrency-safe process-creation contract, arbitrary launch
or restoration failures, cancellation, reentrancy, every broad and explicit
creator, invalid handles, child crashes, cross-process transfer, native close
failure, general leak-freedom, recovery, and independent-host proof remain
pending. Windows is not admitted.

RFC-0151 does not authorize runtime subprocess or `ctypes`, modification of an
accepted helper or fixture, a process-global coordinator, production adapter,
public capability, cleanup authority, recovery policy, dependency, workflow,
CI allocation, tag, release, or publication.

## M167 Windows concurrent explicit-list isolation probe

RFC-0150 accepts one Windows-only, test-only controlled observation in which
two distinct no-delete-share handles remain inheritable across two real
simultaneous one-handle-list process creations. Both helpers reach restoration
before either flag resets. After both parent handles close, child release
orders A-to-B and B-to-A each allow only the released child's root to rename;
the other remains false/error 32 until its own child closes. Both payloads are
preserved and every thread, handle, child, and stream settles.

This resolves only pairwise isolation for one successful current-host overlap.
A concurrency-safe process-creation contract, coordination across every broad
and explicit creator, cancellation/failure/reentrant interleavings, general
leak-freedom, invalid handles, child crashes, cross-process transfer, native
close failure, oplocks, general exclusion, filesystem/driver variation,
recovery, and independent-host proof remain pending. Windows is not admitted.

RFC-0150 does not authorize runtime subprocess or `ctypes`, modification of an
accepted helper or fixture, a process-global lock, production adapter, public
capability, cleanup authority, recovery policy, dependency, workflow, CI
allocation, tag, release, or publication.

## M166 Windows concurrent broad-inheritance leak probe

RFC-0149 accepts one NTFS, Windows-only, test-only controlled observation in
which M163's exact explicit-list launch is event-paused after its no-delete-
share blocker becomes inheritable. A second fixed child starts concurrently
through the captured real `Popen` class with `close_fds=False`. M163 restores
the parent flag after its intended child starts, but the broad child retains
the blocker after parent and intended-child close. M154's identical native
rename remains false/error 32 through those three ownership states and returns
true/code zero only after the broad child acknowledges close and exits zero.

This resolves only whether one documented broad-inheritance interleaving leaks
the exact blocker on the current host. A concurrency-safe inheritance contract,
general leak-freedom, coordination across every process creator, simultaneous
explicit-list launches, cancellation/failure interleavings, real native
restoration failure, invalid inherited values, child crash, cross-process
duplication or transfer, native close failure, oplocks, general exclusion,
filesystem/driver variation, recovery, and independent-host proof remain
pending. Windows is not admitted.

RFC-0149 does not authorize runtime subprocess or `ctypes`, modification of an
accepted helper or fixture, a process-global lock, production adapter, public
capability, cleanup authority, recovery policy, dependency, workflow, CI
allocation, tag, release, or publication.

## M165 Windows inherited-handle restoration-failure probe

RFC-0148 accepts one NTFS, Windows-only, test-only serial observation in which
M163's unchanged helper creates its fixed child with one explicitly allowlisted
blocker handle, then encounters one fixed injected error before its first
native noninheritability restore. The unchanged close-and-reap branch must
settle the child and close its pipe streams before the identical error escapes.
The parent remains explicitly responsible for repairing its still-inheritable
handle and retains owned count one plus M154's false/error 32 denial until
exact parent close, after which the identical second rename returns true/code
zero.

This resolves only one injected restoration-failure ownership observation. A
real native restoration failure, arbitrary restore or process-creation
failures, concurrency-safe inheritance, leak-freedom under concurrent
launches, invalid handle values, child crash, cross-process duplication or
transfer, native close failure, oplocks, controlled interleavings, general
exclusion, filesystem/driver variation, recovery, and independent-host proof
remain pending. Windows is not admitted.

RFC-0148 does not authorize runtime subprocess or `ctypes`, modification of an
accepted fixture, a production adapter, public capability, cleanup authority,
recovery policy, dependency, workflow, CI allocation, tag, release, or
publication.

## M164 Windows inherited-handle launch-failure probe

RFC-0147 accepts one NTFS, Windows-only, test-only serial observation in which
the parent temporarily marks one no-delete-share directory handle inheritable,
lists only that handle for a fixed absent executable, and observes exact
current-host `FileNotFoundError`/`ENOENT`/Windows error 2. `finally` restores
noninheritability with no process owner returned. The parent retains owned
count one and M154's false/error 32 denial until exact parent close, after
which the identical second rename returns true/code zero.

This resolves only one real missing-executable rollback observation.
Restoration-failure injection, arbitrary process-creation failures,
concurrency-safe inheritance, leak-freedom under concurrent launches, invalid
handle values, child crash, cross-process duplication/transfer, native close
failure, oplocks, controlled interleavings, general exclusion,
filesystem/driver variation, recovery, and independent-host proof remain
pending. Windows is not admitted.

RFC-0147 does not authorize runtime subprocess or `ctypes`, modification of an
accepted fixture, a production adapter, public capability, cleanup authority,
recovery policy, dependency, workflow, CI allocation, tag, release, or
publication.

## M163 Windows inherited-handle retention probe

RFC-0146 accepts one NTFS, Windows-only, test-only serial observation in which
the parent places exactly one no-delete-share directory handle in a
`STARTUPINFO` explicit handle list with `close_fds=True`. The handle is
temporarily inheritable only around child creation and immediately restored to
noninheritable. Closing the parent handle leaves M154's identical native rename
false/error 32; fixed byte `!` closes the inherited child handle and orders
exact `closed`, exit zero, and the identical third rename's true/code-zero
result.

This resolves only one explicit inherited-handle retention observation. A
concurrency-safe inheritance contract, broad inheritance, leak-freedom under
concurrent launches, process-creation and restore failures, invalid inherited
values, child crash, cross-process duplication/transfer, native close failure,
oplocks, controlled interleavings, general exclusion, filesystem/driver
variation, recovery, and independent-host proof remain pending. Windows is not
admitted.

RFC-0146 does not authorize runtime subprocess or `ctypes`, modification of an
accepted fixture, a production adapter, public capability, cleanup authority,
recovery policy, dependency, workflow, CI allocation, tag, release, or
publication.

## M162 Windows duplicated-handle retention probe

RFC-0145 accepts one NTFS, Windows-only, test-only observation in which a new
fixed child creates a noninheritable same-process duplicate of its
no-delete-share directory handle before exact `ready`. Fixed byte `1` closes
only the original and emits exact `original-closed`; M154's identical native
rename remains false/error 32. Fixed byte `2` closes the duplicate and orders
exact `closed`, child exit zero, and the identical third rename's true/code-
zero result.

This resolves only one same-process duplicate-retention observation. Inherited
handles, cross-process duplication/transfer, duplicate-creation and native
close failures, oplocks, controlled interleavings, general exclusion,
filesystem/driver variation, recovery, and independent-host proof remain
pending. Windows is not admitted.

RFC-0145 does not authorize runtime subprocess or `ctypes`, modification of an
accepted fixture, a production adapter, public capability, cleanup authority,
recovery policy, dependency, workflow, CI allocation, tag, release, or
publication.

## M161 Windows acknowledged-release timeout probe

RFC-0144 accepts one NTFS, Windows-only, test-only observation in which a new
fixed child acknowledges M155's `!` release-intent byte as exact
`release-held` while retaining its no-delete-share native handle. One
zero-duration `Popen.wait` raises exact `TimeoutExpired`, leaves the return code
unset, and does not change M154's identical false/32 result. A distinct fixed
`.` close byte then orders native close, exact `closed`, child exit zero, and
the identical third rename's true/0 result.

This resolves only one acknowledged-intent/retained-handle observation. Actual
graceful-close and nonzero wait timeouts, native close failure, cancellation,
kill policy, retry or recovery, crash/restart behavior, duplicated handles,
oplocks, controlled interleavings, general exclusion, filesystem/driver
variation, and independent-host proof remain pending. Windows is not admitted.

RFC-0144 does not authorize runtime subprocess or `ctypes`, modification of an
accepted fixture, a production adapter, public capability, cleanup authority,
recovery policy, dependency, workflow, CI allocation, tag, release, or
publication.

## M160 Windows live-blocker immediate-wait timeout

RFC-0143 accepts one NTFS, Windows-only, test-only observation in which M155's
unchanged blocker remains ready and alive while M154's unchanged native rename
returns false/32. One `Popen.wait(timeout=0.0)` raises exact `TimeoutExpired`,
leaves the return code unset, and does not change the identical second
false/32 result. M155's existing graceful release then returns exact `closed`
and child exit zero before the identical third rename returns true/0.

This resolves only one zero-duration process-wait observation. Nonzero wait,
readiness or graceful-close timeout, native close failure, cancellation, kill
policy, retry or recovery, crash/restart behavior, duplicated handles, oplocks,
controlled interleavings, general exclusion, filesystem/driver variation, and
independent-host proof remain pending. Windows is not admitted.

RFC-0143 does not authorize runtime subprocess or `ctypes`, a helper change,
production adapter, public capability, cleanup authority, recovery policy,
dependency, workflow, CI allocation, tag, release, or publication.

## M159 Windows blocker broken-control-pipe probe

RFC-0142 accepts one NTFS, Windows-only, test-only observation in which the
parent kills and boundedly reaps M155's unchanged blocker after readiness and
false/32 denial, requires output EOF, and then attempts one direct native write
through the existing parent stdin handle. The current host returns false,
exact `ERROR_NO_DATA` 232, and zero bytes written. The parent closes its writer
explicitly, and M154's identical native rename then returns true/0.

This resolves only one direct late-write observation. Python exception
mapping, universal Windows error codes, arbitrary pipe faults, partial or
multiple writes, retry, readiness/termination timeout, native close failure,
cancellation, restart recovery, duplicated handles, oplocks, controlled
interleavings, general exclusion, filesystem/driver variation, and
independent-host proof remain pending. Windows is not admitted.

RFC-0142 does not authorize runtime subprocess or `ctypes`, a helper change,
production adapter, public capability, cleanup authority, recovery policy,
dependency, workflow, CI allocation, tag, release, or publication.

## M158 Windows blocker invalid-control-token probe

RFC-0141 accepts one NTFS, Windows-only, test-only observation in which the
parent writes exactly one fixed `?` byte to M155's control-pipe writer after
readiness and false/32 denial, flushes and closes it, and performs one bounded
wait. The unchanged helper closes its native handle in `finally`, returns its
existing invalid-control code 4 without `closed`, and M154's identical native
rename then returns true/0.

This resolves only one fixed invalid-token observation. Arbitrary malformed
input, partial or multiple writes, broken-pipe writes, readiness/termination
timeout, native close failure, cancellation, restart recovery, duplicated
handles, oplocks, controlled interleavings, general exclusion, filesystem/
driver variation, and independent-host proof remain pending. Windows is not
admitted.

RFC-0141 does not authorize runtime subprocess or `ctypes`, a helper change,
production adapter, public capability, cleanup authority, recovery policy,
dependency, workflow, CI allocation, tag, release, or publication.

## M157 Windows blocker control-pipe EOF probe

RFC-0140 accepts one NTFS, Windows-only, test-only observation in which the
parent closes only M155's control-pipe writer after readiness and false/32
denial. The unchanged helper closes its native handle in `finally`, returns its
existing invalid-control code 4 without `closed`, and M154's identical native
rename then returns true/0.

This resolves only one orderly control-pipe EOF observation. Wrong-token input,
broken-pipe writes, readiness/termination timeout, native close failure,
cancellation, restart recovery, duplicated handles, oplocks, controlled
interleavings, general exclusion, filesystem/driver variation, and independent-
host proof remain pending. Windows is not admitted.

RFC-0140 does not authorize runtime subprocess or `ctypes`, a helper change,
production adapter, public capability, cleanup authority, recovery policy,
dependency, workflow, CI allocation, tag, release, or publication.

## M156 Windows abrupt blocker-owner termination probe

RFC-0139 accepts one NTFS, Windows-only, test-only observation in which the
parent kills M155's unchanged blocker child without sending the graceful
release token, performs a bounded process wait, receives no `closed`
acknowledgement, and retries M154's identical native rename once. The current
host reports false/32 before termination and true/0 after the bounded wait.

This resolves only one abrupt blocker-owner termination observation. Pipe
failure, readiness/termination timeout, close failure, restart recovery,
duplicated handles, oplocks, controlled interleavings, general exclusion,
filesystem/driver variation, and independent-host proof remain pending.
Windows is not admitted.

RFC-0139 does not authorize runtime subprocess or `ctypes`, a production
adapter, public capability, cleanup authority, recovery policy, dependency,
workflow, CI allocation, tag, release, or publication.

## M155 Windows child-owned share-delete handshake

RFC-0138 accepts one NTFS, Windows-only, test-only child-owned blocker with a
fixed bounded pipe handshake as current-host feasibility evidence. Windows
remains unadmitted. Controlled interleavings inside native calls, duplicated or
inherited handles, abrupt owner termination, pipe failure, oplocks/share stress,
general exclusion/quiescence, competing descendant activity, other
filesystems/drivers, recovery, policy, receipts, and independent hosts remain
required.

RFC-0138 does not authorize runtime subprocess or `ctypes`, a general process
coordination primitive, a platform adapter, public probe, cleanup authority,
cache access, dependencies, version, workflow/CI, or release authority.
Repository publication is governed separately by maintainer direction and the
hosted-stack safety gate.

## M154 Windows native sharing-violation result

RFC-0137 accepts one NTFS, Windows-only, test-only direct child native-result
fixture as current-host feasibility evidence. Windows remains unadmitted.
Cross-version/filesystem/driver error variation, alternate rename APIs,
controlled concurrent interleavings, explicit synchronization, oplocks/share
stress, general exclusion/quiescence, competing descendant activity, handle
duplication/inheritance, recovery, policy, receipts, and independent hosts
remain required.

RFC-0137 does not authorize runtime subprocess or `ctypes`, inline evaluation,
a platform adapter, public probe, cleanup authority, cache access,
dependencies, version, workflow/CI, or release authority. Repository
publication is governed separately by maintainer direction and the hosted-
stack safety gate.

## M153 Windows cross-process share-delete exclusion

RFC-0136 accepts one NTFS, Windows-only, test-only paired share-mode fixture as
current-host feasibility evidence. Windows remains unadmitted. Direct native
child error capture, controlled concurrent interleavings, explicit
synchronization, oplocks/share stress, general exclusion/quiescence, competing
descendant activity, handle duplication/inheritance, other filesystems,
recovery, policy, receipts, and independent hosts remain required.

RFC-0136 does not authorize runtime subprocess or `ctypes`, a platform adapter,
public probe, cleanup authority, cache access, dependencies, version,
workflow/CI, or release authority. Repository publication is governed
separately by maintainer direction and the hosted-stack safety gate.

## M152 Windows cross-process namespace substitution

RFC-0135 accepts one NTFS, Windows-only, test-only child-process namespace-
substitution fixture as current-host feasibility evidence. Windows remains
unadmitted. Controlled concurrent interleavings, explicit synchronization,
oplocks/share stress, exclusion/quiescence, handle duplication/inheritance,
other tags/filesystems, recovery, policy, receipts, and independent hosts
remain required.

RFC-0135 does not authorize runtime subprocess or `ctypes`, a platform adapter,
public probe, cleanup authority, cache access, dependencies, version,
workflow/CI, or release authority. Repository publication is governed
separately by maintainer direction and the hosted-stack safety gate.

## M151 Windows retained-parent namespace substitution

RFC-0134 accepts one NTFS, Windows-only, test-only retained-parent substitution
fixture as current-host feasibility evidence. Windows remains unadmitted.
Concurrent/cross-process interleavings, oplocks/share stress, pre-acquisition
substitution, other tags/filesystems, recovery, policy, receipts, and
independent hosts remain required.

RFC-0134 does not authorize runtime shelling or `ctypes`, a platform adapter,
public probe, cleanup authority, cache access, dependencies, version,
workflow/CI, or release authority. Repository publication is governed
separately by maintainer direction and the hosted-stack safety gate.

## M150 Windows directory-junction refusal probe

RFC-0133 accepts one NTFS, Windows-only, test-only directory-junction fixture
as current-host feasibility evidence. Windows remains unadmitted. Symbolic
links, mounted folders, other tags/filesystems, all-component substitution,
concurrency, recovery, policy, receipts, and independent hosts remain required.

RFC-0133 does not authorize runtime shelling or `ctypes`, a platform adapter,
public probe, cleanup authority, cache access, dependencies, version,
workflow/CI, or release authority. Repository publication is governed
separately by maintainer direction and the hosted-stack safety gate.

## M149 Windows cache-cleanup capability probe

RFC-0132 accepts a Windows-only, test-only native handle probe as feasibility
evidence. Windows remains unadmitted. The privilege-dependent reparse case,
filesystem coverage, concurrency, recovery, retained roots, policy, durable
receipts, and independent-host execution remain required.

Runtime `ctypes`, a platform adapter, public probe, cleanup authority, cache
access, dependencies, version, workflow/CI, release authority, and remote
change remain unauthorized.

## M148 cache-cleanup platform capability

RFC-0131 adopts the M148 direction: current portable CPython is insufficient
for M147's complete safe mutation chain. No platform is admitted. A future
proposal must provide a private engine-owned adapter, real-host adversarial
evidence, native-object isolation, and safe refusal.

Cleanup, a public probe, adapter implementation, `ctypes`, native code,
mutation, remote cache, dependencies, version, workflow/CI, release authority,
and remote change remain unauthorized.

## M147 asset-cache cleanup threat model

RFC-0130 adopts the asset-cache cleanup threat model as a blocking future
design contract. Any implementation must map every listed threat and invariant
to a control and adversarial test, with explicit cross-platform safe-refusal
semantics.

Cleanup implementation, candidate disclosure, retained-root machinery,
locking, trusted time, quarantine, mutation receipts, repair, remote cache,
dependencies, version, workflow/CI, release authority, and remote change remain
unauthorized.

## M146 cache-cleanup readiness decision

RFC-0129 resolves the adopted M146 direction: do not add cleanup from existing
aggregate evidence. Reconsideration requires identity-bearing candidates,
complete retained roots, generation-bound quiescence, explicit policy/trusted
time, bounded dry-run and mutation receipts, concurrency/crash recovery,
cross-platform link safety, and restore/rollback behavior in one accepted
design.

Runtime cleanup, candidate disclosure, mutation, dependency, version,
workflow/CI, release authority, and remote change remain unauthorized.

## M145 saved unreferenced-preview verification

RFC-0128 resolves the adopted M145 direction: strictly admit one bounded
canonical M143/M144 preview and verify it offline against the exact current plan
and one already-admitted saved M138 fingerprint. The CLI preflights current
source/lock/plan state before either project-confined record read and has no
cache argument.

The success report binds exact preview bytes and supplied plan/observation
identity. It is integrity evidence only. Authenticity, provenance, writer
identity, trusted time, chronology/freshness, current cache state, candidate
disclosure, retention/deletion authority, cleanup/mutation, remote cache,
network, dependencies, version, workflows/CI, release authority, and remote
change remain unauthorized for M145.

## M144 offline unreferenced-blob preview

RFC-0127 resolves the adopted M144 direction: after current source/lock/plan
preflight, read one project-confined saved M138 fingerprint under M139's
existing hard bound and strict canonical decoder, then invoke pure M143.

The CLI emits the unchanged
`ludoweave.asset-cache-unreferenced-preview/1` bytes. It has no cache argument
or access and introduces no new runtime value, protocol, decoder, or root API.
The originating cache may be absent.

Saved-preview persistence/verification, current-state/chronology/freshness,
authenticity/provenance, candidate disclosure, retention/deletion authority,
cleanup/mutation, remote cache/network, dependencies, version, CI/workflows,
release authority, and remote change remain unauthorized for M144.

## M143 path-free unreferenced-blob preview

RFC-0126 resolves the adopted M143 direction: bind one exact current plan to
one unchanged bounded M138 read-only observation, then expose only the existing
unreferenced-blob count and byte aggregate through a frozen path-free preview.

Frozen `ludoweave.asset-cache-unreferenced-preview/1` evidence also carries
only fixed status/protocol fields, the exact plan SHA-256, and the complete
already-public M138 observation SHA-256. The CLI preflights current inputs before
resolving the cache and performs exactly one observation. An absent cache
reports zero without creation; a nonzero diagnostic remains successful exit 0.

Candidate identities and paths, deletion eligibility, age/last-use facts,
retention roots, grace policy, leases/pins/generations, quiescence/concurrency,
atomic snapshots, cleanup/prune/repair/deletion/eviction/garbage collection,
saved-preview persistence, remote cache/network, dependencies, version,
CI/workflows, release authority, and remote change remain unauthorized for
M143.

## M142 saved cache-fingerprint comparison verification

RFC-0125 resolves the adopted M142 direction: strictly decode one bounded
canonical M140 report, rerun M141 from one exact plan and two admitted
fingerprints, then require complete frozen-value equality entirely offline.

Frozen `ludoweave.asset-cache-fingerprint-comparison-verification/1` success
binds the plan, existing fingerprint/comparison protocols, comparison status,
and digest of the already-public comparison report. Correctly derived
`different` evidence verifies with exit 0; invalid or mismatched processing
uses structured stderr exit 2. The CLI has no cache argument or access.

Record storage/naming/retention, chronology, detailed object diffs, signature/
attestation, authenticity/provenance, atomic snapshots, hostile concurrent
writers, retention roots, leases/pins/generations, cleanup/mutation/repair/
deletion/eviction, remote cache/network, dependencies, version, CI/workflows,
release authority, and remote change remain unauthorized for M142.

## M141 offline cache-fingerprint comparison

RFC-0124 resolves the adopted M141 direction: bind two exact admitted M138
fingerprints to one exact current plan and reuse M140's fixed path-free
comparison entirely in memory. Deltas remain `current - expected`; exact
observation equality preserves identity-only change detection.

The CLI verifies current inputs before independently reading and decoding two
bounded project-confined canonical records. It has no cache argument or access.
Equal/different retain stdout exit 0/1; invalid processing remains structured
stderr exit 2. No new report protocol is introduced.

Record storage, chronology, detailed object diffs, signature/attestation,
authenticity/provenance, atomic snapshots, hostile concurrent writers,
retention roots, leases/pins/generations, cleanup/mutation/repair/deletion/
eviction, remote cache/network, dependencies, version, CI/workflows, release
authority, and remote change remain unauthorized for M141.

## M140 path-free cache-fingerprint comparison

RFC-0123 resolves the adopted M140 direction: preflight exact saved plan
identity, reuse exactly one unchanged bounded M138 observation, and diagnose
change only through the twelve existing signed M137 aggregate deltas plus one
exact-observation equality flag.

Frozen `ludoweave.asset-cache-fingerprint-comparison/1` evidence exposes no
cache key, URI, object/artifact digest, action/blob identity, filename, path,
payload, or expected/current observation digest. Equal exits 0; diagnostic
different exits 1 with the report on standard output; invalid processing stays
structured exit 2.

Detailed object diffs, JSON Patch, telemetry export, authenticity/provenance,
atomic snapshots, hostile concurrent writers, retention roots, leases/pins/
generations, cleanup/mutation/repair/deletion/eviction, remote cache/network,
dependencies, version, CI/workflows, release authority, and remote change
remain unauthorized for M140.

## M139 saved cache-fingerprint verification

RFC-0122 resolves the adopted M139 direction: admit only one bounded canonical
exact-schema saved M138 fingerprint, bind its nested plan digest before cache
construction, then compare its complete inventory and observation digest with
exactly one fresh M138 read-only observation.

Frozen `ludoweave.asset-cache-fingerprint-verification/1` success exposes only
valid status, fingerprint protocol, plan digest, and observation digest. Local
digest agreement is integrity equality, not authenticity or provenance: M139
adds no signature, key/root of trust, attestation, authenticated channel,
trusted timestamp, or transparency log.

Per-object diff/listing, atomic snapshots, hostile concurrent writers,
retention roots, leases/pins/generations, cleanup policy, mutation/repair/
deletion/eviction, remote cache/network, dependencies, version, CI/workflows,
release authority, and remote change remain unauthorized for M139.

## M138 deterministic cache-observation fingerprint

RFC-0121 resolves the adopted M138 direction: one M137 bounded read-only
storage observation supplies both the unchanged aggregate inventory and a
plan-independent digest over all exact observed action metadata and CAS
identity/size membership. The fingerprint stream has an explicit protocol
domain, sorted record order, typed tags, unsigned eight-byte length framing,
canonical metadata, raw SHA-256 bytes, and exact content lengths.

Frozen `ludoweave.asset-cache-fingerprint/1` evidence exposes only the nested
path-free inventory and `observation_sha256`. It is equality evidence for one
sequential observation, not an atomic snapshot, diff, last-use fact, retention
root, provenance statement, deletion eligibility, or mutation authority.

Saved-fingerprint decoding/verification, public object lists, timestamps,
leases/pins/generations, cleanup policy, repair/deletion/eviction, remote cache,
authentication, signatures, dependencies, version, CI/workflows, release
authority, and remote change remain unauthorized for M138.

## M137 bounded asset-cache inventory

RFC-0120 resolves the adopted M137 direction: inspect only the engine-owned
`actions/` and `cas/` layout through a bounded deterministic read-only pass.
The pass rejects unknown layout, links/reparse points, noncanonical or
location-inconsistent action metadata, corrupt CAS content, missing references,
and aggregate or per-collection bound violations. Every admitted name is
processed in sorted order and every CAS blob is streamed and verified.

Frozen `ludoweave.asset-cache-inventory/1` evidence compares exact current-plan
cache keys with all verified storage and reports path-free counts for current,
missing, other-action, and no-action-reference entries. A blob with no action
reference is an observation only; it is not proof that the blob is safe to
delete or eligible for eviction, retention change, or garbage collection.

Mutation, repair, deletion, cleanup policy, quota enforcement, hostile-
concurrency snapshot claims, remote cache, authentication, signatures,
provenance, decoder invocation, source acquisition, dependencies, version,
CI/workflows, release authority, and remote change remain unauthorized for
M137.

## M136 saved asset-cache population verification

RFC-0119 resolves the adopted M136 direction: strictly decode one saved M135
population report under hard byte/entry bounds, completely bind it to the exact
current plan before cache construction, then verify every referenced action and
CAS payload through the unchanged read-only M133 boundary.

Frozen `ludoweave.asset-cache-population-verification/1` evidence reports only
the exact plan, entry count, population protocol, and valid status. It invokes
no decoder or fallback and cannot create, publish, repair, delete, or otherwise
change the cache or project. Historical population statuses are validated as
data but are not independently proven events.

Signatures, attestations, provenance/authenticity, builder identity, roots of
trust, remote cache, authenticated transport, snapshot-consistent hostile
concurrency, repair/deletion/eviction, dependencies, version, CI/workflows,
release authority, and remote change remain unauthorized for M136.

## M135 explicit post-realization asset-cache population

RFC-0118 resolves the adopted M135 direction: keep M134 realization read-only
and add one separate explicit operation that opens the cache without write
authority, completes exact source/cache/decoder/limit work, and acquires write
authority only after the complete materialization exists.

The operation invokes unchanged M132 per-entry publication. Frozen
`ludoweave.asset-cache-population/1` evidence pairs each exact `hit`/`decoded`
realization result with `published`/`reused` publication status in plan order.
It contains no payload or path. Failure before publication leaves an absent
cache absent; later publication failure can retain an earlier valid entry or
valid orphan blob and has no rollback or M135 success report.

Implicit publication in `asset-realize`, all-plan transactions, remote cache,
authentication, shared writers, hostile-concurrency claims, repair/deletion/
eviction, discovery, watcher/reimport, parallel workers, plugins/decoder
registration, renderer upload, project write, world mutation, dependencies,
version, CI/workflows, release authority, and remote change remain
unauthorized for M135.

## M134 read-only cache-assisted asset realization

RFC-0117 resolves the adopted M134 direction: validate the complete exact
detached input tuple, verify every current-plan cache candidate, then decode
only exact misses with the unchanged built-in decoder kernel. Verified hits and
decoded misses merge in canonical plan order and obey the same tightening-only
source/artifact limits.

The public operation and `source asset-realize` command never publish. A
missing cache remains absent; a present corrupt action fails before every miss
decoder; project and cache data remain unchanged. Frozen
`ludoweave.asset-build-realization/1` reports logical identities and exact
`hit`/`decoded` statuses without payloads or paths.

Automatic publication, remote transport, authentication, shared writers,
repair/deletion/eviction, discovery, watcher/reimport, parallel workers,
plugins/decoder registration, renderer upload, project write, world mutation,
dependencies, version, CI/workflows, release authority, and remote change
remain unauthorized for M134.

## M133 verified read-only asset cache lookup

RFC-0116 resolves the adopted M133 direction: open one explicit local cache
without write authority, inspect only exact action keys from a freshly verified
current plan, and report deterministic path-free hits and misses.

An absent action is a miss. Present metadata is bounded, strict UTF-8,
duplicate-free, exact-field, and byte-for-byte canonical. It must reconstruct a
valid result entry, match current plan-known identity, and reference an ordinary
CAS payload with the declared bounded length and SHA-256. Present corruption
fails closed without repair, deletion, publication, or re-execution.

Cache-assisted execution, decoder bypass, mixed-hit realization, remote cache,
enumeration, shared writers, repair, eviction, workers, dependencies, version,
CI/workflows, release authority, and remote change remain unauthorized for
M133.

## M132 verified local asset cache publication

RFC-0115 resolves the adopted M132 direction: retain complete decoded payloads
only through a separate bounded materialization value, then publish them to one
caller-authorized local cache after the unchanged M130/M131 verification chain.

Payloads use an artifact-SHA-256 `cas/` namespace. Canonical action metadata
uses the existing cache-key `actions/` namespace and becomes visible only after
its payload. Every hit or collision verifies exact metadata, ordinary-file
layout, byte count, and payload SHA-256. Corruption fails closed without repair,
overwrite, or deletion. Same-filesystem staging and replacement provide atomic
per-entry visibility; valid orphan blobs and earlier complete entries may remain
after a later storage failure.

Remote cache transport, authentication, shared writers, eviction, garbage
collection, quotas, repair/deletion APIs, all-plan transactions, parallel
workers, discovery, watcher/reimport, renderer upload, project write, world
mutation, dependencies, version, CI/workflows, release authority, and remote
change remain unauthorized for M132.

## M131 bounded in-memory asset plan execution

Primary-source review resolves the adopted M131 direction: execute only the
existing built-in PNG/JSON/WGSL/audio transformations over an exact plan-
ordered tuple of detached immutable source bytes after complete source
identity and resource-bound preflight.

The canonical `ludoweave.asset-build-result/1` retains the plan identity,
loader identity, per-entry cache/output identities, and aggregate byte counts,
but no decoded payload or path. Decoder failure is chained and normalized; no
success bytes precede complete success.

Cache lookup/write, persisted artifacts, atomic publication, cache corruption
handling, workers, parallel scheduling, plugins, decoder registration,
discovery, watcher, automatic reimport, project write, renderer upload,
world/session mutation, receipts, dependencies, metadata, version, root API,
workflow/allocation, permission, credential, release authority, and remote
change remain unauthorized for M131.

## M130 confined asset build-plan verification

Primary-source review resolves the adopted M130 direction: load one explicit
saved M129 plan through the existing project-confined regular-file boundary,
recompute and verify current M128 source identities, regenerate the M129 plan,
then compare the two plans exactly before emitting a bounded success summary.

Verification reports only the first stable mismatching field and optional
logical URI. Compared lock/manifest hashes, source sizes/hashes, cache keys,
settings, and paths remain absent. The saved plan is detached immutable input;
the project owns no retained descriptor and receives no write.

M130 adds no plan execution, payload decoder, asset build, cache lookup/write,
artifact creation, import/reimport, scheduler/worker, discovery, watcher,
source/project write, dependency, metadata, version, root API, workflow/job/
allocation, permission, credential, release authority, or remote change.

## M129 deterministic verified asset build planning

Primary-source review resolves the adopted M129 direction: plan only the exact
M127-selected closure after M128 input verification. Entries are dependency-
first with logical-URI tie-breaking, and each prospective cache key must match
the existing M4 identity over URI, kind, settings, source SHA-256, loader
protocol, and ordered direct dependency keys.

The plan binds the canonical M128 lock and M126 manifest. It is prospective
work identity only, not decoder output, build success, cache presence, artifact
integrity, execution, provenance, or authenticity. No payload decode/build,
cache lookup/write, artifact creation, import/reimport, scheduler, discovery,
watcher, source/project write, dependency, metadata, version, root API,
workflow/allocation, permission, credential, release authority, or remote
change is authorized for M129.

## M128 asset-source lock verification

Primary-source review resolves the adopted M128 direction: preserve M127's
explicit source-owned direct roots and asset-manifest-owned transitive graph,
then hash only the resolved project-confined asset source files into one
bounded immutable `ludoweave.asset-source-lock/1`. The lock binds the canonical
M125 source lock, canonical M126 asset manifest, unique direct roots, and exact
resolved URI/kind/source-byte-count/source-SHA-256 entries. Empty closures are
valid.

Generation and verification are separate read-only CLI operations. Verification
fails on the first stable field or logical URI without disclosing expected or
actual hashes, sizes, or paths. Sequential source reads are bounded to 256 MiB
each and 1 GiB accepted aggregate, but are not an atomic filesystem snapshot.

The lock is repeatable input identity only. It is not provenance, authenticity,
authorization, freshness, an imported-artifact identity, or a cache key. No
asset decode/build/import, cache use/write, discovery, watcher, automatic
reimport, live update, unused-asset policy, build-inclusion policy, dependency,
metadata, version, root API, workflow/allocation, permission, credential,
release authority, or remote change is authorized for M128.

## M127 source-to-asset dependency checking

RFC-0110 resolves the adopted M127 direction: source scene/prefab documents own
direct logical asset declarations; the explicit asset manifest owns asset-to-
asset edges. `AssetManifest.dependency_closure()` requires exact distinct roots
and returns roots plus every reachable dependency once in URI order. Read-only
`ludoweave source assets` preserves each direct list separately from its
resolved closure and emits canonical `ludoweave.cli.source-asset-check/1` only
after every explicit source succeeds.

Actual asset reference inference inside application component values remains
unresolved because no universal component-reference schema exists. Unused-
asset rejection and build-inclusion policy remain deferred because shared
catalogs, entry points, packaging, and dead-asset ownership are undefined. No
source repeats indirect dependencies; the asset graph owns those edges.

No asset source read, payload decode, asset build, import, cache, discovery,
watcher, live update, compile, registry resolution, world/session, command,
mutation, receipt, project write, dependency, metadata, version, engine-root
export, workflow/allocation, permission, credential, or release-authority
change is authorized for M127.

## M126 project-confined asset-manifest loading

RFC-0109 resolves the adopted M126 direction: retain exact
`ludoweave.assets/1`, add tightening-only manifest limits and deterministic
detached decoding/canonical bytes, make the existing path loader bounded, and
add one project-confined `HeadlessProject.load_asset_manifest()` composition
method.

This is a loader foundation only. It reads no asset source, builds no asset,
uses or writes no cache, and does not connect M119-M125 source dependencies to
the asset manifest. Direct/transitive dependency checking, unused declaration
policy, and report/failure-disclosure shape require a later decision.

No discovery, import, payload decode, build, cache, watcher, reimport, live
update, write-back, world/session, command, transaction, mutation, receipt,
CLI, dependency, root API, version, workflow/allocation, or release-authority
change is authorized for M126.

## M125 source-integrity lock verification

RFC-0108 resolves the adopted M125 direction: add bounded immutable
`ludoweave.source-lock/1` values plus read-only stdout generation and exact
project-confined verification. The lock contains one normalized M124 manifest
ID/hash and 1-256 entry-ID-ordered accepted source protocol/ID/hash records;
prefabs additionally bind the explicit instance protocol/ID/hash.

`ludoweave source lock` invokes unchanged M121-M124 readers and emits only the
canonical lock. `ludoweave source verify` loads one confined expected lock,
recomputes current identities, and emits
`ludoweave.cli.source-lock-verify/1` only after exact success. Mismatch returns
exit 2, no success document, and only the first field plus optional entry ID;
hash/path values remain silent. Existing source-check output is unchanged.

The lock is content identity, not an atomic filesystem snapshot, signature,
provenance, authenticity, authorization, freshness, or artifact-security
proof. No discovery, import, compile, application schema semantics, asset or
dependency load, cache, watcher, reimport, live update, write-back,
world/session, command, transaction, mutation, receipt, dependency, root API,
workflow/allocation, or release-authority change is authorized for M125.

## M124 explicit source-manifest checking

RFC-0107 resolves the adopted M124 direction: add bounded immutable
`ludoweave.source-manifest/1` values and one explicit
`ludoweave source check PROJECT --manifest FILE` mode. A manifest names only
caller-selected project-relative scenes or prefab source/instance pairs,
normalizes by stable entry ID, rejects duplicates, and emits one path-silent
canonical aggregate report.

The manifest is an explicit input list, not directory discovery, a component
registry, asset database, or import graph. Checking performs no compile,
application-specific component validation, world/session creation, command,
transaction, mutation, write, or receipt. Sequential filesystem reads are not
an atomic snapshot; deterministic output assumes stable input files.

No recursion/glob, suffix routing, implicit pairing, project-manifest source
registry, asset loading, cache, watcher, live update/reimport, write-back,
arbitrary execution, remote/file URI, dependency, lock, metadata, version,
engine-root API, workflow job/allocation, or release-authority change is pending
for M124.

Reopen only for separately assigned discovery, registry-aware compilation,
dependency traversal, persistent reports, or live-update work with explicit
ordering, exclusion/conflict rules, bounds, source identities, failure
atomicity, receipts, ownership, compatibility, security, and installed-artifact
evidence.

## M123 read-only source-check CLI

RFC-0106 resolves the adopted M123 direction: add one nested
`ludoweave source check` adapter for either one project-confined scene or two
explicit prefab source/instance files. Success emits canonical
`ludoweave.cli.source-check/1` JSON with protocol/source identities, canonical
hashes, and bounded counts. Prefab mode enforces exact source identity.

The command performs structural preflight only. It registers or resolves no
application component schema, creates no world or session, calls no planner or
transaction service, performs no compile or world mutation, writes no project
file, and produces no receipt. It does not claim application-specific
component semantic validity.

No directory discovery, recursive/glob input, implicit pairing, suffix routing,
manifest registration, dependency traversal, asset loading, cache, watcher,
live update, write-back, arbitrary script execution, remote/file URI, new
operation, dependency, root API, version, workflow job/allocation, or release-
authority change is pending for M123.

Reopen only for separately assigned compile/import, recursive validation,
registry-aware semantics, or generated-report persistence with explicit bounds,
ownership, atomicity, source identity, diagnostics, compatibility, and
installed-artifact evidence.

## M122 project-confined prefab file loading

RFC-0105 resolves the adopted M122 direction: add two typed methods to the
existing `HeadlessProject` composition root for explicit
`ludoweave.prefab/1` source and `ludoweave.prefab-instance/1` instance files.
Both reuse M121 project confinement and bounded reads. The caller supplies two
explicit files; there is no implicit pairing. Existing `compile_prefab()`
retains exact source matching and planning authority.

Loading performs no world mutation and produces no receipt. Existing explicit
transaction application remains the instantiation and receipt boundary. The
returned records are detached immutable data, and source changes never silently
alter runtime state.

No directory discovery, extension routing, manifest lookup, dependency
traversal, asset loading, cache, watcher, live update/reimport, write-back,
nested prefab inheritance, remote/file URI, new operation, dependency, root API,
schema/planner, workflow, allocation, or release-authority change is pending for
M122.

Reopen only for a separately assigned discovery, nesting, or live-update slice
with explicit source/version identity, conflict precedence, bounds, receipts,
rollback/failure atomicity, ownership, compatibility, platform security, and
installed-artifact evidence.

## M121 project-confined scene file loading

RFC-0104 resolves the adopted M121 direction: add one typed
`HeadlessProject.load_scene()` method that reuses established project-relative
path confinement and bounded descriptor reads before delegating detached bytes
to the unchanged `ludoweave.scene/1` decoder.

Loading performs no world mutation and produces no receipt. Explicit M119
planning and existing transaction application remain the instantiation and
receipt boundary. Asset dependencies remain logical identities. The returned
document is detached immutable data, and source changes never silently mutate
runtime state.

No directory discovery, prefab file loader, file URI, include/import graph,
remote path, asset loading, source cache, watcher, live update/reimport,
write-back, race-free hostile-filesystem claim, arbitrary Python evaluation,
new operation, dependency, root API, scene/prefab schema/planner, workflow,
allocation, or release-authority change is pending for M121.

Reopen only for a separately assigned prefab-file, discovery, live-update, or
adversarial filesystem slice with explicit source identity, conflict policy,
bounds, receipts, rollback/failure atomicity, ownership, compatibility,
platform security, and installed-artifact evidence.

## M120 one-level prefab fragment planning

RFC-0103 resolves the adopted M120 direction: add exact bounded
`ludoweave.prefab/1` fragments and `ludoweave.prefab-instance/1` detached
instance overrides, then compile through M119 into ordinary atomic spawn
commands. Canonical runtime state remains solely in the world store and receipt
aliases supply the local/runtime mapping.

No general JSON Patch/Pointer language, nested prefab inheritance, variant
chain, parameter expression, structural override, source write-back, file I/O,
asset loading, live update/reimport, silent propagation, runtime link graph,
new persistent operation, global discovery, dependency, workflow, allocation,
root API, or release-authority change is pending for M120.

Reopen only for a separately assigned nested-composition, file-loading, or live-
update slice with explicit conflict precedence, source/version identity,
resource bounds, receipts, rollback/failure atomicity, ownership, security,
compatibility, and installed-artifact evidence. Source changes must never
silently mutate existing runtime entities.

## M119 data-only scene transaction planning

RFC-0102 resolves the adopted M119 direction: introduce one exact bounded
`ludoweave.scene/1` document and compile it through an explicitly supplied
component registry into ordinary atomic spawn commands. The world store remains
the sole runtime authority and receipt aliases supply local/runtime mapping.

No scene loader, file I/O, prefab inheritance/override/composition, live
update/reimport, silent propagation, `EntityRef` facade, asset loading,
scene-specific command operation, renderer/tool/provider surface, arbitrary
Python import/evaluation, second authority, global registry, dependency,
workflow, runner allocation, root API, or release-authority change is pending
for M119.

Reopen this decision only for a separately assigned prefab or file-loading
slice with explicit format/version identity, bounded resource/conflict policy,
instantiation/update receipts, ownership, failure atomicity, asset resolution,
security, compatibility, and installed-artifact evidence. Existing runtime
entities must never change silently when source data changes.

## M118 Python 3.15 prerelease compatibility

RFC-0101 resolves the adopted M118 direction: retain Python 3.15 outside the
supported range after one exact Windows CPython 3.15.0b1 installed-wheel
observation. The pure wheel required an explicit metadata override; version and
serial headless execution worked, while doctor correctly retained the
unsupported-version rejection.

No Python 3.15 support, metadata relaxation, doctor relaxation, runtime shim,
final/later-prerelease result, cross-platform, graphics, free-threaded,
full-suite, extension, provider, workflow, runner allocation, dependency, lock,
version, runtime API, or release-authority change is pending for M118.

Reopen this decision after Python 3.15 final when a concrete support proposal
supplies complete supported-platform, tooling, dependency, provider, lifecycle,
world, agent, graphics, installed-artifact, failure, and maintenance evidence.
Prerelease serial compatibility alone is not a support gate.

## M117 free-threaded serial compatibility

RFC-0100 resolves the adopted M117 direction: retain standard GIL CPython as
the supported baseline while recording one exact Windows CPython 3.14.5t
installed-wheel serial-compatibility observation. The GIL-disabled probe
preserved deterministic headless execution, explicit owner-thread rejection,
and orderly close without a runtime or workflow change.

No concurrent-safety claim, parallel-performance target, graphics/wgpu claim,
cross-platform free-threaded evidence, extension compatibility, runtime build
branch, lock, dependency, workflow, runner allocation, version, support
promotion, or release-authority change is pending for M117.

Reopen this decision only when a concrete supported-build proposal supplies
cross-platform lifecycle, world, agent, provider, extension, performance,
failure, and maintenance evidence. Official CPython support for the interpreter
variant does not establish concurrent safety or support for this engine.

## M116 sample-bundle semantic portability

RFC-0099 resolves the M116 decision: separate sample-bundle semantic
portability from byte identity. Supported runtime producers may emit different
valid Deflate bytes under RFC-0098 while supported consumers retain the same
source-defined extraction result. The exact Windows CPython 3.12.13, 3.13.13,
and 3.14.5 3x3 matrix passed all nine combinations with 50 extracted files.
Every extraction produced canonical tree SHA-256
`eb4089dc35539baa9af95c757da9172506d61b6d45ab19d5ad5d8740b77a9ed0`.

No alternate compression method, decoder, compressor pin, recompression,
runtime branch, digest allowlist, workflow, runner allocation, dependency,
producer, verifier, runtime API, or release-authority change is pending for
M116. Each staged release remains bound to its own exact manifest/checksum.

Reopen this decision only if a supported runtime cannot consume another
supported runtime's fixed-producer archive or a concrete release requirement
demands cross-platform producer-consumer evidence. Such a proposal must retain
artifact integrity, bounded extraction, diagnostic order, and exact ownership
evidence rather than inferring a general ZIP interoperability guarantee.

## M115 sample-bundle byte-reproducibility scope

RFC-0098 resolves the M115 decision: sample-bundle byte reproducibility means
repeated production inside one fixed resolved release environment. The current
official producer remains the baseline CPython 3.12 tag job. Supported CPython
3.12-3.14 runtimes remain compatible consumers, verifiers, and local staging
environments without a cross-runtime byte-identity promise.

No compressor allowlist or pin, compressor-identity manifest field, runtime
rejection, recompression, new sample-byte verifier, workflow, runner allocation,
dependency, producer, runtime API, or release-authority change is pending for
M115. RFC-0021's separate wheel/sdist same-source, same-job boundary remains
unchanged.

Reopen this decision only if the official release producer environment changes
or a concrete release requirement demands cross-runtime byte-identical sample
archives. Such a proposal must identify the producer implementation, portable
normalization strategy, compatibility cost, manifest consequences, and exact
cross-platform evidence before changing the current boundary.

RFC-0097 resolves the M114 sample-member compression-level non-observability
decision. PKWARE's Deflate option bits encode broad categories rather than an
exact numeric writer level. Python's `compresslevel` configures writing, while
reopened members on exact CPython 3.12.13, 3.13.13, and 3.14.5 do not recover
requested levels `0`, `1`, `6`, or `9`.

The accepted decision keeps the producer explicit at level `9` without an
exact level-9 verifier profile or inferred compressor level. M105's zero flags
and M113's method compatibility remain unchanged. This is one compression-
level non-observability decision, not a compression-ratio policy, recompressor,
raw Deflate parser, payload-content check, archive repair, general ZIP validity
claim, or general sandbox. RFC-0097 records the accepted policy; no M114 design
decision remains pending.

RFC-0096 resolves the M113 sample-member compression-method compatibility
decision. PKWARE defines compression as optional, method `0` as stored, and
method `8` as deflated. Python exposes and reads both and defaults new archives
to stored. M64 already admits exactly those two methods, while M95 requires
their local and central values to agree.

The accepted decision retains stored/deflated compatibility without an exact
deflate-only profile. Other compression methods remain outside the private
sample profile, and the fixed 50-member producer remains method `8`. This is
one compression-method compatibility decision, not a new decompressor,
compression-level or ratio policy, recompressor, payload-content check, archive
repair, general ZIP validity claim, or general sandbox. RFC-0096 records the
accepted policy; no M113 design decision remains pending.

RFC-0095 resolves the M112 sample-member creating-system compatibility
decision. PKWARE defines the upper `version made by` byte as the host system
with which external attributes are compatible. CPython intentionally defaults
`ZipInfo.create_system` to `0` on Windows and `3` elsewhere, and M108 already
proved that an exact UNIX-only rule regresses 54 established Windows-created
fixtures.

The accepted decision retains parser-exposed creating-system compatibility
without a creating-system allowlist. M65's existing encoded file-type boundary
continues to reject symlinks and non-regular types, extraction continues to
apply no archived host attributes, and the fixed producer remains explicit
host `3`. This is one host-marker compatibility decision, not a host semantics
engine. It adds no host-specific external-attribute interpretation, permission
restoration, payload-content read, workflow, dependency, runtime, producer, or
release-authority change.

RFC-0095 records the accepted policy; no M112 design decision remains pending.

RFC-0094 resolves the M111 sample-member permission compatibility decision.
PKWARE defines external file attributes relative to the creating host encoded
by `version made by`. Python exposes public central `ZipInfo.external_attr`.
Exact CPython 3.12.13, 3.13.13, and 3.14.5 each expose and read multiple UNIX
regular-file permission variants plus missing-type mode `0600`, while the fixed
50-member producer emits only create system `3` and mode `0100644`.

M65's upper-half file-type policy remains authoritative: encoded symlinks and
other encoded non-regular types fail, while missing type bits or a regular-file
type remain admitted across permission variants. This is one permission-bit
compatibility decision, not an exact external-attribute profile, host-system
semantics expansion, permission allowlist, permission restoration, payload-
content check, archive repair, general ZIP validity claim, or general sandbox.
RFC-0094 records the accepted policy; no M111 design decision remains pending.

RFC-0093 resolves the M110 sample-member timestamp compatibility decision.
PKWARE defines member date and time as MS-DOS calendar fields relative to 1980
with two-second resolution, not an absolute UTC instant. Python exposes public
central `ZipInfo.date_time`; exact CPython 3.12.13, 3.13.13, and 3.14.5 each
admitted `(2026, 8, 25, 12, 34, 56)` and read the probe payload, while the
fixed 50-member producer emits only `(1980, 1, 1, 0, 0, 0)`. An exact verifier
profile passed its focused contract but caused 22 established architecture
regressions across supported extraction, atomicity, inventory, snapshot,
decompression, and diagnostic behavior. That classifier was removed.

M98 local/central consistency remains the verifier policy; consistent alternate
timestamps remain admitted; and the producer keeps its exact reproducible
tuple. This is one central-timestamp compatibility decision, not timezone or
UTC conversion, verifier wall-clock use, extra-field timestamp interpretation,
a raw record parser, payload-content check, archive repair, general ZIP validity
claim, or general sandbox. A nonzero-volume candidate was also rejected because
established M82 already rejects split-volume members earlier. RFC-0093 records
the accepted policy; no M110 design decision remains pending.

RFC-0092 resolves the M109 zero sample-member internal-attribute profile
preflight. PKWARE defines the central two-byte field as an advisory apparent-
text bit plus a mainframe record-control bit, with other bits reserved or
unused. Python exposes public `ZipInfo.internal_attr`; CPython initializes it to
zero. Exact CPython 3.12.13, 3.13.13, and 3.14.5 each admitted value `1` and
read the probe payload, while the fixed 50-member producer emits only zero.
Private release smoke therefore requires every public central internal-
attribute value to equal zero after M108 and before exact inventory, staging,
or reads. The stable error is `sample bundle has unsupported internal
attributes`.

This zero sample-member internal-attribute profile preflight is one central-
internal-attribute exact-profile classifier, not text/binary content
interpretation, a record-control semantics parser, supported-bit mask,
external-attribute or host policy, raw record parser, payload-content check,
archive repair, general ZIP validity claim, or general sandbox. RFC-0092 records
the accepted policy; no M109 design decision remains pending.

RFC-0091 resolves the corrected M108 exact sample-member creation-version
profile preflight. PKWARE defines the lower `version made by` byte as the ZIP
specification version supported by the encoder. Python exposes public central
`ZipInfo.create_version`; CPython defaults to `20`. Exact CPython 3.12.13,
3.13.13, and 3.14.5 each admitted public central creation version `21` and read
the probe payload, while the fixed 50-member producer emits sole version-made-
by pair `(20, 3)`. Private release smoke therefore requires every public
central `create_version` value to equal `20` after M107 and before exact
inventory, staging, or reads. The stable error is `sample bundle has an
unsupported creation version`.

This exact sample-member creation-version profile preflight is one central-
creation-version exact-profile classifier, not a general creation-version
semantics parser, supported-version range, producer-capability evaluator,
attribute-host policy, payload-content check, archive repair, general ZIP
validity claim, or general sandbox. The initially considered exact host policy
was rejected after 54 established architecture regressions. RFC-0091 records
the corrected accepted policy; no M108 design decision remains pending.

RFC-0090 resolves the M107 exact sample-member extraction-version profile
preflight. PKWARE assigns version 2.0 to Deflate, Python exposes public central
`ZipInfo.extract_version`, and CPython uses default value `20`. Exact CPython
3.12.13, 3.13.13, and 3.14.5 each exposed matching local/central pairs
`(21, 0)` and read both probe payloads, while the fixed 50-member producer emits
sole pair `(20, 0)`. Private release smoke therefore requires every public
central `ZipInfo.extract_version` value to equal `20` after established local
consistency, payload-layout, extra-field, member-metadata, M105, and M106 checks
and before exact inventory, staging, or reads. The stable error is `sample
bundle has an unsupported extraction version`.

This exact sample-member extraction-version profile preflight is one central-
extraction-version exact-profile classifier, not a general extraction-version
semantics parser, supported-version range, capability evaluator, raw record
parser, payload-content check, archive repair, general ZIP validity claim, or
general sandbox. It changes no workflow, dependency, producer, runtime API, or
release authority. RFC-0090 records the accepted policy; no M107 design
decision remains pending.

RFC-0089 resolves the M106 zero sample-member extraction-version reserved-byte
profile preflight. Python documents public central `ZipInfo.reserved` as zero,
CPython initializes and serializes zero, and PKWARE defines the enclosing two-
byte version-needed-to-extract field. Exact CPython 3.12.13, 3.13.13, and
3.14.5 each exposed matching local/central pairs `(20, 1)` and read both probe
payloads, while the fixed 50-member producer emits sole reserved value zero.
Private release smoke therefore requires every public central
`ZipInfo.reserved` value to equal zero after established local consistency,
payload-layout, extra-field, member-metadata, and M105 checks and before exact
inventory, staging, or reads. The stable error is `sample bundle has a nonzero
extraction-version reserved byte`.

This zero sample-member extraction-version reserved-byte profile preflight is
one central-reserved zero-profile classifier, not an extraction-version
semantics parser, supported-version allowlist, capability rule, raw record
parser, payload-content check, archive repair, general ZIP validity claim, or
general sandbox. It changes no workflow, dependency, producer, runtime API, or
release authority. RFC-0089 records the accepted policy; no M106 design
decision remains pending.

RFC-0088 resolves the M105 zero sample-member general-purpose-flag profile
preflight. PKWARE defines legitimate nonzero flag semantics and currently
unused bits; CPython exposes the central value through public
`ZipInfo.flag_bits`. Exact CPython 3.12.13, 3.13.13, and 3.14.5 each retained
matching unused bit 7 as value `128` and read both probe payloads, while the
fixed 50-member producer emits sole value zero. Private release smoke therefore
requires every public central `ZipInfo.flag_bits` value to equal zero after
established specific-flag, M94 consistency, M102/M103 layout, and M104 extra-
field, decoded-name, and member-metadata checks and before exact inventory,
staging, or reads.
The stable error is `sample bundle contains unsupported general-purpose flags`.

This zero sample-member general-purpose-flag profile preflight is one central-
flag zero-profile classifier, not a flag-semantics parser, bit registry, raw
record parser, payload-content check, archive repair, general ZIP validity
claim, or general sandbox. It changes no workflow, dependency, producer,
runtime API, or release authority. RFC-0088 records the accepted policy; no
M105 design decision remains pending.

RFC-0087 resolves the M104 empty sample-member extra-field profile preflight.
PKWARE defines local and central member extra fields as valid ZIP extensibility;
Python exposes central bytes through public `ZipInfo.extra`; CPython interprets
selected known fields and retains uninterpreted bytes. Exact CPython 3.12.13,
3.13.13, and 3.14.5 each retained equal local/central third-party field
`feca02006f6b` and read both probe payloads, while the fixed 50-member producer
emits empty fields.
Private release smoke therefore requires empty public central `ZipInfo.extra`
after established Unicode Path, ZIP64, M96 consistency, M102 bounds, and M103
contiguity checks and before decoded names, metadata, inventory, staging, or
reads. The stable error is `sample bundle contains an unsupported extra field`.

This empty sample-member extra-field profile preflight is one central-extra
emptiness classifier, not an extra-field semantics parser, field-ID registry,
raw central-record parser, payload-content check, archive repair, general ZIP
validity claim, or general sandbox. It changes no workflow, dependency,
producer, runtime API, or release authority. RFC-0087 records the accepted
policy; no M104 design decision remains pending.

RFC-0081 resolves the M98 local-header timestamp consistency preflight. PKWARE
duplicates a two-byte DOS modification time and two-byte DOS modification date
in corresponding local and central member records. Exact CPython 3.12.13,
3.13.13, and 3.14.5 retain both central tuples as
`(2026, 8, 23, 4, 6, 8)` and read both payloads when only the second local
time's low byte changes from `c4` to `e4`. Private release smoke therefore
reads exactly four bytes at `ZipInfo.header_offset + 10` after M97 and requires
equality with the DOS bytes represented by public central `ZipInfo.date_time`
before decoded names, metadata, inventory, staging, or reads. The stable error
is `sample bundle local header timestamps are inconsistent`.

This is one four-byte local-timestamp consistency classifier, not a timestamp
semantics validator, timezone or UTC conversion, wall-clock comparison,
calendar or reproducibility policy, extended-timestamp interpretation,
CRC/size or field-wide comparison, record/payload/next-header bound,
gap/adjacency/contiguity/non-overlap rule, inter-member layout validator,
archive repair, or general sandbox. It changes no workflow, dependency,
producer, runtime API, or release authority. RFC-0081 records the accepted
policy; no M98 design decision remains pending.

RFC-0080 resolves the M97 local-header extraction-version consistency
preflight. PKWARE duplicates a two-byte version-needed pair in corresponding
local and central member records. Exact CPython 3.12.13, 3.13.13, and 3.14.5
retain central pairs `[(20, 0), (20, 0)]` and read both payloads when only the
second local extraction-version byte changes to 21. Private release smoke
therefore reads exactly two bytes at `ZipInfo.header_offset + 4` after M96 and
requires equality with public central `ZipInfo.extract_version` and
`ZipInfo.reserved` before decoded names, metadata, inventory, staging, or
reads. The stable error is `sample bundle local header extraction versions are
inconsistent`.

This is one two-byte local-extraction-version consistency classifier, not a
supported-version allowlist, minimum extractor-capability rule, reserved-byte
policy, time/CRC/size or field-wide comparison,
record/payload/next-header bound, gap/adjacency/contiguity/non-overlap rule,
inter-member layout validator, archive repair, or general sandbox. It changes
no workflow, dependency, producer, runtime API, or release authority. RFC-0080
records the accepted policy; no M97 design decision remains pending.

RFC-0079 resolves the M96 local-header extra-field consistency preflight.
PKWARE defines separate variable extra fields in corresponding local and
central member records. Exact CPython 3.12.13, 3.13.13, and 3.14.5 retain both
central extras as `feca02006f6b` and read both payloads when only the second
same-length local extra changes to `feca02006f21`. Private release smoke
therefore reads the already bounded local bytes after M95 and requires exact
equality with public central `ZipInfo.extra` before decoded names, metadata,
inventory, staging, or reads. The stable error is `sample bundle local header
extra fields are inconsistent`.

This is one bounded local-extra equality classifier, not an extra-field
semantics parser, broad extra-field ban, new field-ID policy,
version/time/CRC/size or field-wide comparison, record/payload/next-header
bound, gap/adjacency/contiguity/non-overlap rule, inter-member layout validator,
archive repair, or general sandbox. It changes no workflow, dependency,
producer, runtime API, or release authority. RFC-0079 records the accepted
policy; no M96 design decision remains pending.

RFC-0078 resolves the M95 local-header compression-method consistency
preflight. PKWARE duplicates a two-byte compression method in corresponding
local and central member records. Exact CPython 3.12.13, 3.13.13, and 3.14.5
retain central methods `[8, 8]` and read both payloads when only the second
local method changes to stored 0. Private release smoke therefore reads exactly
two little-endian bytes at `ZipInfo.header_offset + 8` after M94 and requires
equality with central `ZipInfo.compress_type` before decoded names, metadata,
inventory, staging, or reads. The stable error is `sample bundle local header
compression methods are inconsistent`.

This is one two-byte local-compression-method consistency classifier, not a
local extra-field comparison/parser, version/time/CRC/size or field-wide
comparison, method allowlist, record/payload/next-header bound, gap/adjacency/
contiguity/non-overlap rule, inter-member layout validator, archive repair, or
general sandbox. It changes no workflow, dependency, producer, runtime API, or
release authority. RFC-0078 records the accepted policy; no M95 design decision
remains pending.

RFC-0077 resolves the M94 local-header flag-consistency preflight. PKWARE
defines a two-byte general-purpose flag in both local and central member
records, while supported CPython exposes the central value and accepts a
demonstrated local-only encryption-bit mutation through both payload reads.
The fixed sample producer emits equal values, so complete release smoke now
compares exactly the two local bytes at `ZipInfo.header_offset + 6` with public
central `ZipInfo.flag_bits` after M93 and before decoded names, metadata,
inventory, staging, or reads. The stable error is `sample bundle local header
flags are inconsistent`.

This is one two-byte local-flag consistency classifier, not a local compression-
method or extra-field comparison, broad flag allowlist, field-wide consistency
check, payload/next-header bound, inter-member layout validator, archive repair,
or general sandbox. It changes no workflow, dependency, producer, runtime API,
or release authority. RFC-0077 records the accepted policy; no M94 design
decision remains pending.

Feature PR #234 integrates the accepted RFC-0077 policy as verified squash
`7974b6fc110f995cac25f7d69d9c48b55013a764` after exact-head hosted run
`32581692977` passed the unchanged three Linux-first allocations. The squash
has exact qualified tree `96bd9000efbc473d09f0c75d83c5e1231621409e`,
sole parent M93 closeout, standalone DCO, and a valid GitHub signature. This
evidence does not widen the decision or establish a real public release
observation. Only the factual integration record and closeout remain; no M94
policy decision is pending.

RFC-0076 resolves the M93 local-header name-consistency preflight. PKWARE
requires corresponding local and central member records, places each variable
name immediately after the fixed local prefix, and specifies CP437 by default
with UTF-8 under bit 11. Python exposes the central decoded name, flags, and
header offset; exact CPython 3.12-3.14 admits a same-length local-only name
mutation and defers `BadZipFile` until member open. The selected fixed-profile
rule reconstructs the central name bytes under the central bit-11 policy and
requires exact equality with the already bounded raw local name after M92 and
before decoded-name policy, metadata, inventory, staging, or reads. It adds no
local-flag comparison, extra-field comparison, field-wide consistency,
inter-member layout validator, repair, workflow, dependency, producer,
runtime API, or release authority. RFC-0076 records the accepted policy;
implementation and exact-head qualification are integrated by feature PR
#231. The factual integration record and closeout remain active; no policy
decision is pending.

RFC-0075 resolves the M92 local-header variable-envelope bound. PKWARE defines
two 16-bit local file-name and extra-field length declarations before their
variable bytes, and Python exposes each purported header offset. Exact CPython
3.12-3.14 admits a 65,535-byte local name declaration whose fixed prefix fits
before the conventional central directory, then defers `BadZipFile` until
member open. The selected narrow fixed-profile rule reads only those two
lengths after M91 and before names, metadata, inventory, staging, or reads. It
adds no local-name comparison, extra-field parsing, next-header or payload
bound, inter-member layout validator, workflow, dependency, producer, runtime
API, or release authority. RFC-0075 records the accepted policy;
implementation and exact-head qualification are integrated by feature PR
#228. The factual integration record and closeout remain active; no policy
decision is pending.

RFC-0074 resolves the M91 fixed local-header-prefix bound. PKWARE defines 30
fixed local-header bytes before variable name and extra fields, and Python
exposes each purported header offset. Exact CPython 3.12-3.14 admits a pointer
with a valid signature but only four bytes before the conventional central
directory and defers `BadZipFile` until member open. The selected narrow fixed-
profile rule is one arithmetic prefix-bound classifier after M90 and before
names, metadata, inventory, staging, or reads. It adds no local-header field
parser, record extent, payload bound, inter-member layout validator, workflow,
dependency, producer, runtime API, or release authority. RFC-0074 records the
accepted policy. The exact corrected feature tree, factual integration record,
and closeout are squash-integrated through PRs #225-#227.

RFC-0073 resolves M90 local-header signature preflight. PKWARE defines the four-byte
local-file-header signature and Python exposes each purported header offset.
Exact CPython 3.12-3.14 admits a pointer shifted one byte into a real header as
ordered, distinct, in-bounds public metadata and defers `BadZipFile` until
member open. The selected narrow fixed-profile rule classifies only four bytes
at each public offset after M89 and before names, metadata, inventory, staging,
or reads. It adds no local-header field parser, record-extent or inter-member
layout validator, workflow, dependency, producer, runtime API, or release
authority. RFC-0073 records the accepted narrow policy. Complete local and
exact-head cross-platform qualification are green, and the exact qualified
feature tree, factual integration record, and closeout are squash-integrated
through PRs #222, #223, and #224.

RFC-0072 resolves M89 local-header-offset bounds preflight. PKWARE places local/data
records before the central-directory sequence, and Python exposes the central
pointer as the byte offset to a member's file header. Exact CPython 3.12-3.14
accepts a pointer equal to the conventional central-directory offset and defers
`BadZipFile` until member open. The selected narrow fixed-profile rule requires
every public offset to be strictly before that boundary after M88 and before
names, metadata, inventory, staging, or reads. It admits no local-header parser,
record-extent or inter-member layout validator, workflow, dependency, producer,
runtime API, or release authority. RFC-0072 records the accepted narrow policy.
Complete local and exact-head hosted qualification are green, and the exact
qualified tree, factual integration record, and closeout are squash-integrated
through PRs #219, #220, and #221.

RFC-0071 resolves M88 local-header-order preflight. PKWARE permits arbitrary
ZIP file order generally, while Python documents `ZipFile.infolist()` as archive-entry
order and the fixed LudoWeave producer emits physical local-header order.
Cross-version CPython 3.12-3.14 probes expose a central-record-only swap as
offsets `[46, 0]` and read both members successfully. The selected narrow rule
requires strictly increasing public offsets after M87 distinctness and before
names, metadata, inventory, staging, or reads. It is not a general ZIP-validity
claim and admits no raw parser, inter-member layout validator, workflow,
dependency, producer, runtime API, or release authority. Exact-head cross-
platform hosted qualification and guarded squash integration are complete.

RFC-0070 resolves M87 distinct local-header-offset preflight. PKWARE assigns a
local header and corresponding central record to each stored file, while exact
CPython 3.12-3.14 exposes duplicate central local-header pointers and defers
their consequences until member open. The selected fixed-profile response is
one aggregate distinctness check over public `ZipInfo.header_offset` values
after M86 and before names, metadata, inventory, staging, or reads. Corrected
exact-head cross-platform hosted qualification and guarded squash integration
are complete. No raw parser, ordering/bounds rule, inter-
member layout validator, workflow, dependency, producer, runtime API, or
release authority is admitted.

RFC-0069 resolves M86 first local-header placement preflight. Private complete
release smoke finishes every established policy through M85, then requires the
minimum parser-exposed `ZipInfo.header_offset` to equal zero before M77 decoded-
name policy, metadata, exact inventory, staging, or reads. The stable policy
error is content-silent; empty archives retain the established later inventory
failure. This is not a local-header parser, central-directory parser, inter-
member layout validator, field-consistency validator, signature classifier,
archive repair path, or general archive sandbox. It adds no workflow,
dependency, producer, runtime API, or release authority. A real pass remains
pending an explicitly authorized signed-tag release execution.

RFC-0068 resolves M85 conventional central-directory placement preflight.
Private complete release smoke finishes every established policy through M84,
then requires the final conventional central-directory size plus offset to
equal the absolute final end-of-central-directory record offset before M77
decoded-name policy, metadata, exact inventory, staging, or reads. The stable
policy error is content-silent and the shared helper restores the previous
snapshot position. This is not a central-directory/local-header parser, end-
record search, ZIP64 parser, executable classifier, prepended executable or
self-extracting archive support, multi-volume assembler, or general archive
sandbox. It adds no workflow, dependency, producer, runtime API, or release
authority. A real pass remains pending an explicitly authorized signed-tag
release execution.

RFC-0067 resolves M84 conventional archive entry-count preflight. Private
complete release smoke finishes every M69-M82 policy pass and M83 archive disk
check, then reads exactly the final conventional 22-byte end-of-central-
directory record from the owned checksum-admitted snapshot. Both entry counts
must equal the standard reader's parsed member count before M77 decoded-name
policy, metadata, exact inventory, staging, or reads. The stable policy error
is content-silent and the previous snapshot position is restored. `0xFFFF` is
rejected as outside the fixed profile, not resolved through ZIP64. This is not
a ZIP64 end-record parser, sentinel resolver, end-record search, central/local-
header parser, neighboring-volume discovery, multi-volume assembler, or
general archive sandbox. It adds no workflow, dependency, producer, runtime
API, or release authority. A real pass remains pending an explicitly
authorized signed-tag release execution.

RFC-0066 resolves M83 conventional archive disk-field preflight. Private
complete release smoke finishes every M69-M82 archive-wide pass, then reads
exactly the final conventional 22-byte end-of-central-directory record from
the owned checksum-admitted snapshot. It requires the signature, zero comment
length, current-disk zero, and central-directory-start disk zero before M77
decoded-name policy, metadata, exact inventory, staging, or reads. The stable
policy error is content-silent and the previous snapshot position is restored.
`0xFFFF` is rejected as outside the fixed profile, not interpreted as proof of
split-volume topology. This is not a ZIP64 end-record parser, end-record search,
central/local-header parser, neighboring-volume discovery, multi-volume
assembler, or general archive sandbox. It adds no workflow, dependency,
producer, runtime API, or release authority. A real pass remains pending an
explicitly authorized signed-tag release execution.

M80 ZIP64 extra-field preflight is resolved for implementation. PKWARE assigns
exact extra-field ID `0x0001` to ZIP64 alternate sizes, header offset, and disk-
start metadata. Current CPython applies the size and header-offset values, not
the defined disk-start value, before release smoke receives `ZipInfo`. The
fixed 50-member sample is small and emits no extra fields, so M80 rejects exact
central-directory ID `0x0001` after established M79 policy and before decoded-
name or metadata policy. Unrelated fields and malformed-extra handling remain
outside M80. No broad extra-field ban, raw ZIP64 parser, large-file support
change, workflow, dependency, producer, runtime API, or release authority is
admitted.

RFC-0062 resolves M79 Unicode Path extra-field preflight. Private complete
release smoke finishes every established archive-wide flag/descriptor pass,
then performs a bounded extra-field walk and rejects exact Info-ZIP field ID
`0x7075` before decoded-name checks, metadata, inventory, staging, or reads.
The stable policy error is content-silent and owned resources close before
control returns. This is not a broad extra-field ban, general name-difference
rule, raw ZIP header parser, repair path, scanner, or general archive sandbox.
It adds no workflow, dependency, sample producer, runtime API, or release
authority. A real pass remains pending an explicitly authorized signed-tag
release execution.

RFC-0061 resolves M78 data-descriptor sample-member preflight. Private complete
release smoke finishes the established archive-wide M69/M75/M76 flag pass,
then rejects exact ZIP general-purpose bit 3 in a separate all-member pass
before M77 name checks, metadata, inventory, staging, or reads. The stable
policy error is content-silent and owned resources close before control
returns. This is not a raw descriptor parser, broad flag allowlist, local-
header consistency claim, repair path, scanner, or general archive sandbox.
It adds no workflow, dependency, sample producer, runtime API, or release
authority. A real pass remains pending an explicitly authorized signed-tag
release execution.

RFC-0060 resolves M77 NUL-suffixed sample-member name preflight. Private
complete release smoke checks every decoded `ZipInfo.orig_filename` for an
exact NUL after established flag checks and before metadata, inventory,
staging, or reads. This prevents CPython's documented NUL truncation from
hiding an unvalidated suffix behind an otherwise exact visible sample path.
The stable policy error is content-silent; later ambiguous members preempt
earlier metadata failures and owned resources close first. This is exactly a
NUL check, not a general original-versus-normalized name comparison, raw ZIP
parser, local-header/central-directory consistency claim, repair path, scanner,
or general archive sandbox. It adds no workflow, dependency, sample producer,
runtime API, or release authority. A real pass remains pending an explicitly
authorized signed-tag release execution.

RFC-0059 resolves M76 enhanced-deflate sample-member preflight. Private
complete release smoke rejects exactly ZIP general-purpose bit 4 when paired
with compression method 8, after established processing checks and before
metadata, inventory, staging, or reads. The stable policy error is content-
silent; later flagged members preempt earlier metadata failures and owned
resources close first. Stored-member bit 4 and other flag/method combinations
remain outside this exact decision. The check consumes central-directory flags
exposed by `ZipInfo`; local-header inconsistencies remain outside scope. This is
not a broad flag allowlist, enhanced-deflate decoder, repair path, raw parser,
scanner, or general archive sandbox. It adds no workflow, dependency, sample
producer, runtime API, or release authority. A real pass remains pending an
explicitly authorized signed-tag release execution.

RFC-0058 resolves M75 compressed-patch sample-member preflight. Private
complete release smoke rejects exactly ZIP general-purpose bit 5 during M69's
all-member flag preflight, after encryption and before metadata, inventory,
staging, or reads. The stable policy error is content-silent; later flagged
members preempt earlier metadata failures and owned resources close first.
This is not a broad flag allowlist, reserved-bit policy, implementation-error
catch, patch decoder, repair path, raw parser, scanner, or general archive
sandbox. It adds no workflow, dependency, sample producer, runtime API, or
release authority. A real pass remains pending an explicitly authorized
signed-tag release execution.

RFC-0057 resolves M74 content-silent sample ZIP decompression-failure
normalization. Private complete release smoke adds exactly `zlib.error` from a
checksum-admitted invalid deflated-member payload to the existing stable outer
error after owned cleanup. Suppressed context confines the decompressor
diagnostic while retaining the original exception programmatically. EOF,
policy, filesystem, and unexpected failures remain specific. This is not a
broad compression/general catch, replacement decompressor, payload repair, raw
parser, scanner, or general archive sandbox. It adds no workflow, dependency,
sample producer, runtime API, or release authority. A real pass remains pending
an explicitly authorized signed-tag release execution.

RFC-0056 resolves M73 content-silent sample ZIP text-failure normalization.
Private complete release smoke adds exactly `UnicodeDecodeError` from strict
archive-controlled UTF-8 name decoding in the central directory or local
header to M72's existing stable outer error after owned cleanup. Suppressed
context confines invalid bytes, offsets, codec, and reason while retaining the
original exception programmatically. This is not a broad Unicode/value catch,
replacement decoder, metadata repair, raw parser, scanner, or general archive
sandbox. It adds no workflow, dependency, sample producer, runtime API, or
release authority. A real pass remains pending an explicitly authorized
signed-tag release execution.

RFC-0055 resolves M72 content-silent sample ZIP failure normalization. Private
complete release smoke catches exactly documented `BadZipFile` and
`LargeZipFile` around its checksum-admitted extractor, lets owned cleanup
finish, then raises one stable error with suppressed rendered context. The
original exception remains available programmatically; verifier policy and
non-parser failures retain their categories. This is not a broad catch, public
error protocol, raw parser, scanner, or general archive sandbox. It adds no
workflow, dependency, sample producer, runtime API, or release authority. A
real pass remains pending an explicitly authorized signed-tag release
execution.

RFC-0054 resolves M71 checksum-admitted sample snapshot parsing. After bounded
source admission, complete release smoke copies at most 16 MiB into one owned
binary spooled temporary file while hashing, clears/fails on mismatch, and
gives that exact rewound snapshot to `ZipFile`. Later source change-and-restore
cannot alter parser input. This creates no persistent copy, source-immutability
guarantee, lock, raw ZIP parser, or general archive sandbox. It adds no
workflow, dependency, sample producer, runtime API, or release authority. A
real pass remains pending an explicitly authorized signed-tag release execution.

RFC-0053 resolves M70 sample-archive checksum binding. Complete release smoke
passes the already admitted `SHA256SUMS` digest into extraction, hashes and
rewinds the same opened handle before ZIP parsing, and repeats the comparison
after reads/completeness but before publication. A persistent mismatch uses one
content-silent category and second-check failure cleans owned staging. This
creates no snapshot, lock, immutable-input guarantee, change-and-restore
defense, raw ZIP parser, or general archive sandbox. It adds no workflow,
dependency, sample producer, runtime API, or release authority. A real pass
remains pending an explicitly authorized signed-tag release execution.

RFC-0049 resolves M66 staged sample-root publication. The existing real output
directory owns a same-filesystem temporary staging directory; completeness is
validated there before one rename exposes the final sample root. A final entry
that already exists fails before archive reads and remains untouched. Copy,
decompression, write, incompleteness, and publication failures clean the partial
owned stage and preserve their cause. This is not crash-durable, a general
archive sandbox, a recovery journal, concurrent filesystem race isolation, or
post-publication rollback. It adds no workflow, dependency, sample producer,
runtime API, or release authority. A real pass remains pending an explicitly
authorized signed-tag release execution.

RFC-0048 resolves M65 portable staged sample-member paths. Every member is a
regular file beneath the exact root with at most 255 relative ASCII characters
and portable components. Complete paths are unique case-insensitively,
directory ancestors retain one exact spelling, and file/directory prefix
collisions fail before extraction. Windows device stems, trailing periods,
Unicode, empty/dot components, explicit directory entries, and explicitly
encoded non-regular file types are rejected. Missing ZIP file-type mode bits
remain common-producer compatible. This performs no Unicode normalization or
filesystem probing and is not a general archive sandbox, absolute-path
portability claim, or cleanup guarantee. It adds no workflow, dependency,
sample producer, runtime API, or release authority. A real pass remains pending
an explicitly authorized signed-tag release execution.

RFC-0047 resolves M64 bounded staged sample-bundle extraction. Complete
count/path/link/declared-size preflight admits at most 256 members, 1 MiB per
member, and 8 MiB total before extraction; admitted files stream in 64 KiB
blocks and must exactly reproduce declared sizes. Only stored and deflated
methods are admitted; BZIP2, LZMA, and unknown methods fail preflight because
their standard-library read paths do not provide the same bounded decompressor-
output behavior. This is not a general archive sandbox, metadata-authentication
claim, filename-policy expansion, or transactional cleanup guarantee. It adds
no workflow, dependency, runtime API, or release authority. A real pass remains
pending an explicitly authorized signed-tag release execution.

RFC-0046 resolves M63 public-release subordinate-output confinement. Both in-
process release-document validation and complete smoke redirect subordinate
stdout and subordinate stderr, restore the process-global streams on return or
exception, and succeed only with an exact built-in zero integer. The consumer
retains one content-silent JSON document on its designated channel. This relies
on the verifier's single-thread utility ownership and adds no descriptor or
arbitrary subprocess capture, concurrency claim, workflow, dependency, runtime
API, or release authority. A real pass remains pending an explicitly authorized
signed-tag release execution.

RFC-0045 resolves M62 portable public-release asset-name conformance. The plan
consumer admits 1 through 255 restricted ASCII characters, rejects a trailing
period or case-insensitive Windows device stem, and requires case-insensitive
uniqueness before asset download or output-directory creation. Violations use
content-silent `public_release.invalid_plan`. This uses no filesystem probing,
locale, normalization, rewriting, cleanup, rollback, retry, workflow,
dependency, runtime API, or release authority. A real pass remains pending an
explicitly authorized signed-tag release execution.

RFC-0044 resolves M61 public release candidate/output-root separation. The
expected candidate directory is read-only input. It and the runner-owned output
root are strictly resolved before network or validator side effects; an output
root that equals or resolves beneath the candidate fails with stable
`public_release.path_overlap`. Filesystem-identity comparison across the output
ancestry also rejects differently spelled aliases on a case-insensitive
filesystem. Resolution and identity-inspection failures retain content-silent
candidate/temporary-directory codes, while a separate candidate child of the
output root remains valid. This adds no race-free guarantee, filesystem sandbox,
rollback, cleanup, retry, workflow, dependency, runtime API, or release
authority. A real pass remains pending an explicitly authorized signed-tag
release execution.

RFC-0041 resolves M58 public release transport-cleanup conformance. Every
obtained response receives one response close attempt before its created
connection receives one connection close attempt, and both close attempts
occur when response close fails. Active failures remain primary. Cleanup-only
ordinary failures use content-silent `public_release.request_failed` with the
first cause chained; cleanup control signals remain unwrapped. Redirect
continuation and separate partial publication require successful cleanup. This
adds no rollback, retry, private state, alternate client, workflow, dependency,
runtime API, or release authority. A real pass remains pending an explicitly
authorized signed-tag release execution.

RFC-0040 resolves M57 public release response-body conformance. Every
successful `HTTPResponse.read(amount)` returns immutable bytes no larger than
the requested amount before EOF interpretation, accounting, or output. Any
validated `Content-Length` must equal the total streamed octets for the release
document and every successful response after an asset redirect. Malformed read
shapes use content-silent request failure; declared-length disagreement remains
a size mismatch. This adds no private response/socket state, raw parser,
content decoder, alternate client, workflow, dependency, runtime API, cleanup,
or release authority and makes no general completeness claim for unframed
close-delimited bodies. A real pass remains pending an explicitly authorized
signed-tag release execution.

RFC-0039 resolves M56 public release status and redirect-reference conformance.
Every response status is a non-boolean integer from 100 through 599. Every
followed `302` exposes exactly one Location field through the documented header-
pair list; its value is one 1-to-8,000-octet ASCII URI-reference using valid RFC
3986 characters and complete percent escapes. Bracket delimiters are accepted
only inside the parsed authority and rejected in its path, query, or fragment.
The resolved target repeats the existing bounded HTTPS and per-hop peer/TLS/HTTP
checks. This adds no host
allowlist, private parser state, raw HTTP/URI parser, alternate client,
workflow, dependency, runtime API, or release authority and makes no general
SSRF claim. A real pass remains pending an explicitly authorized signed-tag
release execution.

RFC-0038 resolves M55 public release HTTP response-framing conformance. Every
response must expose documented HTTP/1.1-class value `11`; this is explicitly
not exact raw status-line token evidence because CPython can normalize another
`HTTP/1.x` value. Transfer encoding is
absent or exactly `chunked` case-insensitively, cannot coexist with content
length, and any present content length is a string before existing bounded
checks. Every redirect repeats the validation before status or body use. This
adds no private response-state dependency, raw HTTP parser, alternate client,
workflow, dependency, runtime API, or release authority and makes no general
request-smuggling claim. A real pass remains pending an explicitly authorized
signed-tag release execution.

RFC-0037 resolves M54 public release TLS session freshness. Every fixed API or
bounded redirected asset connection must report `session_reused` as exactly
`False` after the handshake and M53 binding, before service identity,
negotiated-session inspection, or HTTP. Missing, unsupported, resumed,
malformed, and raising observations fail content-silently. This adds no session
cache, session assignment, ticket control, workflow, dependency, runtime API,
or release authority, and does not claim a reconstructed handshake or
certificate exchange. A real pass remains pending an explicitly authorized
signed-tag release execution.

RFC-0034 resolves M51 public release negotiated TLS-session conformance. Every
fixed API or redirected asset connection advertises only `http/1.1` and, after
actual connected-peer validation but before HTTP transmission, requires exactly
TLSv1.2 or TLSv1.3, a well-formed cipher report with at least 128 secret bits,
no TLS compression, and ALPN `http/1.1` or no negotiated ALPN. There is no
cipher-name allowlist, workflow/dependency/release mutation, or authority
change. A real pass remains pending an explicitly authorized signed-tag release
execution.

RFC-0033 resolves M50 public release TLS key-log isolation. Every public API or
asset hop receives a new explicit verified client context with system
server-auth roots, certificate/hostname validation, TLS 1.2 minimum, strict
X.509 flags, and disabled key logging. An ambient `SSLKEYLOGFILE` remains
unchanged and cannot create or receive secrets from the verifier. No custom
trust store, pin, workflow, dependency, release mutation, or authority change
is introduced. A real pass remains pending an explicitly authorized signed-tag
release execution.

RFC-0032 resolves M49 public release connected-peer confinement. Every fixed
API or redirected asset connection validates the actual port-443 TLS socket
peer before HTTP transmission and permits only globally reachable unicast IPv4
or IPv6, with IPv4-mapped IPv6 classified by its embedded address. A
non-global peer has one stable forbidden code; timeout and malformed/unavailable
peer inspection retain the request timeout/failure taxonomy. No hostname/IP
allowlist, separate DNS preflight, workflow, dependency, release mutation, or
authority change is introduced. A real pass remains pending an explicitly
authorized signed-tag release execution.

RFC-0031 resolves M48 public release HTTP response conformance. The fixed
release-document request accepts only direct `200`; asset-ID requests accept
direct `200` or at most three bounded `302` responses. API-only headers remain
on `api.github.com`; timeout, other transport/protocol, and local-output
failures have distinct stable codes. All M47 identity, TLS, path, size,
validation, smoke, workflow, allocation, and authority bounds remain. A real
pass remains pending an explicitly authorized signed-tag release execution.

RFC-0030 resolves M47 cross-platform public consumer rehearsal. One typed
standard-library Python verifier replaces the Bash-only public path and the
existing tag-only fresh-consumer job expands to Ubuntu, Windows, and macOS.
Each runner creates a bounded plan, retrieves exact public bytes without a
release credential, and runs complete installed release smoke. The result
remains same-workflow/provider rather than independent/external evidence. Two
tag-only allocations are added; pull-request allocations, release authority,
runtime, dependency, package, and public API remain unchanged. A real pass
remains pending an explicitly authorized signed-tag release execution.

RFC-0029 resolves M46 fresh-runner consumer rehearsal. After the publishing
job succeeds, one additional read-only Linux job receives only the verified
release ID/version, retrieves the exact same-workflow admitted candidate,
creates a fresh bounded plan, repeats public byte validation without a release
credential, and runs installed release smoke. This is not independent/external
or cross-platform verification and adds no release mutation, publication
authority, pull-request CI allocation, runtime, dependency, or package change.
A real fresh-runner pass remains pending an explicitly authorized signed-tag
release execution.

RFC-0028 resolves M45 public release consumer-path integrity. The publishing
job performs bounded credential-free exact-ID public retrieval, revalidates the
downloaded candidate, and runs complete installed release smoke. This is one
same-run observation, not independent/external or cross-platform evidence,
future availability, immutability, artifact security, PyPI, or a supported
channel. A real public-path pass remains pending an explicitly authorized
signed-tag release execution.

RFC-0027 resolves M44 published release attestation integrity. The existing
release job will verify SLSA v1 provenance for every exact M43-retrieved asset
and an SPDX 2.3 SBOM attestation for exactly one pure wheel after publication.
The verifier fixes repository, signer workflow, tag/source identity, signer
commit, GitHub OIDC issuer, hosted-runner class, predicate, bundle count,
process count, timeout, and content-silent output bounds. No authority exists
to create a tag/release, change attestation creation, retry or roll back failed
publication, enable immutability, publish to PyPI, claim artifact security,
independent builds, or predicate truth, or promote a supported release channel.
A real attestation pass remains pending an explicitly authorized signed-tag
release execution; local and pull-request validation cannot substitute for
that hosted evidence.

RFC-0026 resolves M43 published-asset retrieval integrity. Protocol `/4`
requires unique bounded numeric asset IDs and may write one exclusive
published-only retrieval plan after complete verification. The existing tag job
retrieves every exact ID through the authenticated binary API and rehashes the
downloaded directory against the same published document. Failure is observed
after publication and performs no rollback or mutation. The result is one
authenticated point-in-time byte observation, not unauthenticated/global/future
availability, immutability, consumer installation, or attestation evidence.
Jobs, runners, actions, permissions, triggers, dependencies, credentials, tags,
releases, uploads, cleanup, and publication authority remain unchanged.

RFC-0025 resolves M42 published-prerelease observation. The exact numeric
release database ID now crosses the existing publish transition, after which
one read-only authenticated request must report public prerelease state, a
valid UTC publication time, and unchanged notes/assets. Protocol `/3` makes
draft/published state explicit. Failure blocks a successful release-job result
but performs no automatic rollback, deletion, or mutation. Jobs, runners,
actions, permissions, triggers, dependencies, credentials, tags, releases,
uploads, publication authority, and immutable-release policy remain unchanged.

RFC-0024 resolves M41 release-notes body integrity. The existing bounded M40
validator now requires authenticated draft `body` text to exactly equal the
fixed staged `RELEASE_NOTES.md` supplied through `--notes-file`, while emitting
no note content. The internal protocol advances to `/2`; both workflow files,
runner allocations, actions, permissions, triggers, dependencies, credentials,
API calls, tags, releases, and publication authority remain unchanged. Rendered
Markdown, link and factual-content review, immutable-release policy, PyPI, and a
supported release channel remain separate decisions.

RFC-0023 resolves M40 draft-release asset integrity. The existing tag job makes
its final draft/upload/publish sequence explicit and publishes only when a
bounded standard-library validator confirms the authenticated GitHub draft has
the exact local asset names, complete upload state, byte sizes, and SHA-256
digests. Failed verification remains an unpublished draft and assets are never
clobbered or automatically deleted. The gate adds no runner, action, permission,
trigger, dependency, credential, tag, release, or publication authority.
Independent remote download/storage verification, immutable-release policy,
PyPI, and a supported release channel remain separate decisions.

RFC-0022 resolves M39 release-tag identity enforcement. GitHub's annotated-tag
API is the hosted signature-verification authority, while local Git independently
checks the exact tag object, checkout commit, and `origin/main` ancestry before
the existing tag job performs expensive or publishing work. The bounded gate
adds no runner, action, permission, trigger, dependency, credential, tag, or
publication authority. A local trust store, signer/key allowlist, immutable-
release policy, PyPI channel, and supported-release claim remain separate
decisions.

RFC-0021 resolves M38 distribution reproducibility enforcement. The existing
Linux pull-request and tag-release distribution jobs build twice and compare
the exact pure wheel/source pair before smoke, staging, attestation, or
publication. A same-source/same-job byte match is required; cross-platform or
hermetic reproducibility, independent rebuilding, provenance, and publication
are not claimed. A separate rebuild runner and attestation changes are rejected
for this bounded milestone.

RFC-0020 resolves M37 CI change qualification with an exact trusted-base
classifier. Documentation-only work retains one Linux quality/docs/
architecture/distribution allocation; substantive work retains all three M36
allocations and eight slices. Windows/macOS depend on successful Linux
qualification, so an early failure consumes no desktop allocation. The
accepted tradeoff is later substantive desktop feedback. Workflow-level docs
filtering is rejected because GitHub documents a required-check pending risk;
a separate filter job is rejected because it adds a fourth allocation.

RFC-0019 resolves M36 CI runner ownership by preserving all eight existing
validation slices inside three OS-owned allocations. Ubuntu runs quality/
distribution, 3.12 graphics, and sequential 3.13/3.14 compatibility. Windows
and macOS each run 3.12 graphics followed by 3.14 compatibility. The accepted
tradeoff is less per-slice parallelism and rerun granularity in exchange for
five fewer runner allocations and repeated setups. No billed-minute saving is
claimed before hosted evidence; no coverage slice is removed.

RFC-0018 resolves how third-party conformance-adoption evidence is admitted.
The offline harness counts distinct independent external implementation
identities only after a complete project-accepted submission-census review and
a passing exact installed M17-M19 profile. Project-owned and maintainer-
authored references never count. Plugin-backed evidence is limited to the
existing M12 `render.device` capability and requires both compatible inert
manifest evidence and a passing render profile. Failed and not-executed
submissions remain in complete history. The reviewed manifest is empty, so the
current passing count is zero and no ecosystem, support, certification,
security, performance, or global-discovery result exists.

RFC-0017 resolves how agent-tool recovery-rate evidence is admitted. The
offline harness requires a complete reviewed cohort of task-directed sessions
and every dispatched call, keeps known failure and manual-recovery outcomes in
the denominator, blocks publication on unobserved terminal state, and preserves
complete history. The reviewed manifest is empty, so no measured rate or
recovery-free result exists. Human review owns session/call eligibility,
manual-recovery status, outcome, provenance, validation, and census
completeness. The eight essential CI jobs now run only for substantive pull
requests, avoiding redundant post-merge and `.project/**`-only runs.

RFC-0001 resolves the M7 first-native-kernel question by deferring Rust/PyO3
until its quantified cross-platform, buffer/GIL, ownership, build, fallback,
fuzz, and maintenance-owner gate is satisfied.

ADR-0023 resolves the M8 SDL3 question by using the already-pinned GLFW gamepad
surface and deferring SDL3 until a stable Python binding, auditable offline
binary delivery, explicit lifecycle ownership, cross-platform conformance, and
maintenance owner are evidenced.

ADR-0024 resolves the M9 Box2D question by deferring the preview binding until
the complete CPython/OS wheel and provenance matrix, stable API, lifecycle and
stale-object soak, documented GIL/thread ownership, cross-platform
snapshot/replay classification, copied engine adapter conformance, and a named
maintenance owner are evidenced.

ADR-0025 resolves the M10 inspector boundary with one isolated, owned local
MCP child, detached semantic observations, explicit receipted writes, exact
hash continuity, and no arbitrary process, network, remote-attach, or editor
surface.

RFC-0002 resolves the M12 plugin boundary with canonical inert manifests,
explicit environment/policy/dependency checks, and no discovery, import,
execution, installation, or ambient global registry.

ADR-0027 resolves the M13 rollback/network-snapshot question by admitting only
a bounded offline correction-branch proof and deferring transport/live rollback
until canonical tick-input history, protocol/security, cross-platform network
simulation, resource budgets, lifecycle ownership, and maintenance gates are
complete.

ADR-0028 resolves the M14 constrained-3D question by retaining layered 2D and
deferring any 3D runtime until a bounded product slice, provider-neutral
spatial/render/asset contracts, canonical agent/replay semantics, equivalent
Null behavior, cross-platform installed conformance, measured resource
budgets, lifecycle ownership, and a named maintainer are evidenced together.

ADR-0029 resolves the M15 visual-editor question by retaining the finite
headless inspector and deferring GUI/editor implementation until public
compatibility, document/scene, selection/hierarchy, undo/conflict, property,
viewport, asset, recovery, accessibility/usability, cross-platform packaging,
resource-budget, and maintenance-owner gates are evidenced together.

ADR-0030 resolves the M16 WASM-mod question by retaining the inert M12 plugin
boundary and deferring executable guests until runtime provenance/support,
package identity/distribution, default-deny copied capabilities,
command/receipt mutation mapping, bounded execution, atomic trap/lifecycle,
deterministic replay, guest-state migration, isolation, adversarial
conformance, cross-platform installation, and named security/update ownership
are evidenced together.

ADR-0031 resolves the first external-adapter conformance boundary with one
versioned installed `RenderDevice` baseline over an explicitly supplied trusted
factory. It forbids discovery/loading/installation and records that passing
behavior is not security, provenance, cross-platform, performance, or provider
admission evidence. No independently authored adapter is counted until
external evidence is reviewed.

ADR-0032 resolves the installed agent-adapter conformance boundary with one
versioned 12-tool baseline over an explicitly supplied trusted factory. It
forbids discovery, dynamic import, installation, subprocesses, networking, and
global registration, and records that a project-owned pass is reference
behavior rather than security, provenance, external adoption, cross-platform,
performance, or manual-recovery evidence.

RFC-0003 resolves the first central API-stability candidate by retaining the
command, transaction, and receipt contracts as experimental. Same-version
canonical/atomic behavior is confirmed, but preview promotion remains gated on
a cross-version corpus, external consumer feedback, operation and receipt-field
evolution rules, a bounded public receipt reader, and a supported deprecation-
capable feature-release channel.

RFC-0004 resolves the bounded-reader gate with a strict resource-limited
decoder for the unchanged receipt/1 graph and immutable committed, dry-run,
and rejected fixtures from `0.1.0a1`. This satisfies only gate 4 of RFC-0003.
The fixture set is explicitly a single-version baseline; cross-version
compatibility, external adoption, evolution rules, a release channel, and
stability promotion remain unresolved.

RFC-0005 resolves the built-in operation-argument policy gate. Exact required
and optional fields, unknown-field rejection, and named semantic rules are
fixed per operation/version identity; a breaking change uses a new operation
version and a new identity is additive. This satisfies only gate 3 of
RFC-0003. Cross-version history, external feedback, receipt semantic-diff/
diagnostic evolution, and a supported deprecation release channel remain
unresolved.

RFC-0006 resolves the receipt semantic-diff and diagnostic-code policy gate.
Exact v1 field sets, presence, ordering, and meanings cannot change in place;
existing code meanings are fixed, new well-formed codes are additive, and
phase/message/scalar detail metadata is non-authoritative. This satisfies only
gate 5 of RFC-0003. Cross-version history, external feedback, and a supported
deprecation release channel remain unresolved.

RFC-0007 resolves how cross-version receipt-corpus evidence is admitted. The
offline harness preserves exact historical identities and requires a distinct
installed reader version plus supported-release records for every observed
version. Its current result is explicitly false because all evidence is
`0.1.0a1` and the release set is empty. Actual cross-version history, external
feedback, and a supported deprecation release channel remain unresolved.

RFC-0008 resolves how external-consumer-feedback evidence is admitted. The
offline harness requires manually reviewed independent-consumer records with
exact public repository, revision, protocol, outcome, and artifact identities;
the evaluator verifies only the frozen data contract and cannot establish
independence by itself. The reviewed manifest is empty, so actual external
feedback and adoption remain absent. Cross-version history and a supported
deprecation release channel also remain unresolved.

RFC-0009 resolves how supported deprecation-capable feature-release-channel
evidence is admitted. The offline harness requires two reviewed supported,
non-yanked final releases on distinct feature lines with exact publication
identities and append-only history. The reviewed manifest is empty, so the
actual channel remains absent. Cross-version release execution and external
consumer feedback also remain unresolved; no stability promotion is implied.

RFC-0010 resolves how the first-external-contribution documentation objective
is admitted. The offline harness requires at least one manually reviewed human
good-first contribution linked to a public project issue and merged pull
request, with exact Git/patch/feedback identities, DCO, documented validation,
no private maintainer knowledge, and no public-API, persistent-format,
dependency, or workflow change. The reviewed manifest is empty, so actual
external-contributor usability evidence remains absent. The evaluator cannot
establish independence or undisclosed assistance; human review owns those
facts, and no synthetic fixture or CI pass is an external contribution.

RFC-0011 resolves how externally authored sample games are admitted as a
longer-term adoption metric. The offline harness requires manually reviewed
independent authorship, immutable public provenance, installed-wheel headless/
command-receipt/replay evidence, distinct artifact identities, and reviewed
licensing while preserving exact complete history. The reviewed manifest is
empty, so the current external sample-game count remains zero. Project-owned
examples, maintainers, agents, CI, and synthetic fixtures are not adoption.

RFC-0012 resolves how external contributor-retention evidence is admitted. The
offline harness requires the same independently reviewed external human to
complete distinct first and later merged public contributions with exact
issue/PR/revision/artifact identities, chronology, DCO, validation, provenance,
and complete history. The reviewed manifest is empty, so retained-contributor
and return-contribution counts remain zero; popularity and synthetic fixtures
are not retention.

RFC-0013 resolves how published-wheel installation-matrix evidence is admitted.
The offline harness requires one immutable public pure-Python release wheel to
pass reviewed clean isolated installation and installed checks across the exact
practical OS/CPython matrix with complete history. The reviewed manifest is
empty, so source-checkout CI, local builds, and synthetic fixtures are not
published installation success.

RFC-0014 resolves how issue-response and pull-request-review latency evidence
is admitted. The offline harness requires a complete reviewed public cohort of
eligible external-human issues and pull requests, preserves pending items,
binds first qualifying human-maintainer actions to exact frozen evidence and
timestamp/latency agreement, and preserves complete history. The reviewed
manifest is empty, so no latency aggregate, responsiveness result, SLA, or
support claim exists. The evaluator cannot establish human roles, participant
distinctness, first-action state, or census completeness; manual review owns
those facts.

RFC-0015 resolves how CI replay-divergence-rate evidence is admitted. The
offline harness requires a complete reviewed public cohort of eligible replay
executions, preserves cancellation, early failure, skips, and missing result
evidence as non-executed, binds verified/diverged outcomes to exact workflow,
case, and frozen result identities, and preserves complete history. The
reviewed manifest is empty, so no measured rate or zero-divergence result
exists. Human review owns cohort completeness, eligibility, outcome,
provenance, and validation.

RFC-0016 resolves how benchmark-regression-rate evidence is admitted. The
offline harness requires a complete reviewed controlled cohort of paired
registered M1-M4 `perf_counter_ns` p95 comparisons, binds exact base/head
sources and frozen runner/result artifacts, requires predeclared integer
tolerances, preserves non-execution, and preserves complete history. M7
cProfile output is diagnostic and ineligible. The reviewed manifest is empty,
so no measured rate or zero-regression result exists. Human review owns runner
control, parameter equality, eligibility, comparability, tolerance
predeclaration, outcome, provenance, validation, and census completeness.

Operational follow-ups outside repository implementation:

- Verify and reserve the `ludoweave` package name before the first publication.
