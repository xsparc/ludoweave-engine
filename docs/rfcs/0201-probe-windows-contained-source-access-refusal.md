# RFC-0201: Probe Windows contained source-access refusal

**Status:** Accepted
**Milestone:** M218
**Decision class:** Direction-preserving

## Context

M216 observes retained launch-source write/delete sharing refusal from the
controller process. M217 preserves that boundary while launching the participant
with remote debugging excluded on Python 3.14. The smallest next independent
functional observation is to issue the same access-only requests from a fixed
separate child process whose lifetime is explicitly contained.

Windows Job Objects provide a fixed-purpose process-containment mechanism. A
process created suspended can be assigned before it executes, while
kill-on-last-close supplies an exceptional-path settlement boundary. This adds
an independent process observation without requiring another account, host,
network channel, shell, privileged operation, remote attachment, or fixture
mutation.

## Decision

Adopt the test-only [Windows contained source-access refusal
probe](../security/windows-cache-cleanup-contained-source-access-refusal-probe.md).

For each of M216's three live refusal phases, create one private Job Object with
`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`. Launch one exact fixed, argument-free
`pythonw.exe -I -B` contender suspended and with no inherited handles. Assign it
to the Job before resume, verify exact one-member Job accounting and membership,
verify its primary token is same-logon with the controller, then resume it.

The contender derives one fixed tracked source path and performs only write- and
delete-access `CreateFileW` opens. Both must refuse with exact
`ERROR_SHARING_VIOLATION`. The child must settle with exit status zero; the Job
must settle to one total and zero active members; every retained handle must
close. M217's remote-debug exclusion, identity, protocol, source-stability,
release, settlement, and post-settlement access boundary remains mandatory.

The contender performs no write, delete, rename, or replacement operation.
This decision is direction-preserving and makes no collection or cleanup
authority increase. It does not satisfy distinct-principal or independent-host
evidence, source provenance, imported-module binding, criteria 6/7, or Windows
admission. Cleanup remains unimplemented and unauthorized.

## Consequences

- Sharing refusal is observed from an independently scheduled contained process,
  not only by a helper in the controller process.
- Suspended assignment, same-logon verification, exact membership/accounting,
  kill-on-close, normal settlement, and zero owned handles are all required.
- The fixed child has no caller-selected path, arguments, inherited handles,
  output protocol, shell, network, mutation action, or reusable product surface.
- Distinct-principal, independent-host, hostile-process, privileged-bypass,
  source-provenance, imported-module, collection, criteria 6/7, and Windows
  admission evidence remain separate work.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Reuse the controller-local access helper

Rejected because it would repeat M216 without adding an independently executing
process boundary or explicit containment evidence.

### Accept a target path or command from the parent

Rejected because caller-controlled input would create a broader file-access or
process-launch tool. The contender is fixed, argument-free, access-only, and
test-only.

### Use another account, remote attachment, or a hosted workflow

Rejected because cross-principal and remote execution require separate private
authority and evidence plans. M218 neither attempts them nor adds a public
runner. It adds zero GitHub Actions jobs or hosted allocation.
