# Windows contained source-access source-binding probe

**Status:** Accepted M220 current-host test evidence; no source-commit or build
provenance, cross-principal proof, independent-host proof, cleanup authority,
or Windows admission has occurred.

M220 composes one retained contender-source execution observation with the
exact frozen M212-M219 process, token, session, participant source,
access-refusal, remote-debug-exclusion, interpreter-image, and Job-containment
boundary. The probe is Windows-only, test-only, offline, access-only, and
fixed-purpose. It does not operate on a cache fixture or issue cleanup.

## Contained source-access source binding

The fixed contender source is retained before child creation. Its file
identity, bounded size, and SHA-256 are captured from the open read-only file
handle. The retained file is rewound and the contender is executed through
inherited standard input by the exact direct `pythonw.exe -I -B -` command.

Inheritance is restricted with an explicit handle list to exactly three
inherited handles: the retained source as standard input and two distinct
write-only `NUL` handles as standard output and standard error. The child is
created suspended, assigned as the sole member of a fresh private
kill-on-close Job, and checked against the controller's same-logon token. M219's
retained expected and observed interpreter-image names, identities, sizes, and
digests must agree before resume.

The source snapshot is checked and rewound again before resume. The contender
then makes only M218's fixed write- and delete-access `CreateFileW` requests
and must observe exact sharing refusal. It accepts no arguments, emits no
output, and performs no content or namespace mutation. After exact zero exit,
the source snapshot remains stable after child settlement, both retained image
snapshots remain stable, the Job settles to one total and zero active members,
and all controller-owned handles close. Ordinary source access must then
succeed.

## Preserved participant boundary

A fresh source-bound contender runs before participant launch, after the
control connection, and after the ready challenge. The participant still
launches with M217's exact remote-debug exclusion. Retained token, native
session, pipe DACL, expected executable image, observed image, retained
participant source, challenge/release, settlement, post-settlement access, and
final participant-source snapshots remain required.

## Evidence and authority boundary

This establishes only that the new fixed same-logon Job-contained contender
executed the controller-retained source bytes through inherited standard input
while preserving M219's interpreter-image binding. Imported standard-library
module bytes remain unbound. Native DLLs, loader behavior, interpreter state,
and environment values outside isolated-mode exclusions also remain unbound.
Source-commit provenance remains unproved. Build provenance remains unproved.

It does not prove a distinct security principal, hostile executable,
independent host, privileged-bypass resistance, debugger/kernel resistance, or
a cleanup action. Criteria 6 and 7 remain unresolved. Windows is not admitted,
cleanup remains unimplemented and unauthorized, and no public self-hosted
runner is introduced.

M220 adds no runtime source, public API, CLI or MCP command, production
harness, collector, credential or account lifecycle, privilege transition,
filesystem mutation, network listener, dependency, package payload, version,
workflow, permission, secret, hosted allocation, or admission decision.

## Primary references

- [Handle inheritance](https://learn.microsoft.com/en-us/windows/win32/procthread/inheritance)
- [UpdateProcThreadAttribute](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute)
- [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [Python command-line interface](https://docs.python.org/3/using/cmdline.html)
- [SLSA provenance](https://slsa.dev/spec/v1.2/provenance)
- [NIST Secure Software Development Framework publications](https://csrc.nist.gov/Projects/ssdf/publications)
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
