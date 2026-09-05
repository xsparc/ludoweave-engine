# Windows contained source-access image-binding probe

**Status:** Accepted M219 current-host test evidence; no source-provenance,
cross-principal, independent-host, cleanup-authority, or Windows admission has
occurred.

M219 composes one retained interpreter-image observation with the exact frozen
M212-M218 process, token, session, source, access-refusal,
remote-debug-exclusion, and Job-containment boundary. The probe is Windows-only,
test-only, offline, access-only, and fixed-purpose. It does not operate on a
cache fixture or issue a cleanup action.

## Contained source-access image binding

The expected interpreter image is retained before launch. Its normalized name,
volume and file identity, bounded size, and SHA-256 are captured from that open
file handle before the Job or child exists.

For each refusal phase, M218's exact fixed, argument-free contender is created
suspended with no inherited handles and assigned as the sole member of a fresh
private kill-on-close Job. The controller and contender primary-token snapshots
must establish the same logon. The observed process image is retained before
resume, and its normalized name, volume and file identity, bounded size, and
SHA-256 must exactly match the expected snapshot before any contender code
executes.

The child then makes only M218's fixed write- and delete-access `CreateFileW`
requests and must report exact sharing refusal. After the child settles with
status zero, both retained image handles remain stable after child settlement:
the expected and observed handles must reproduce their pre-resume file identity,
size, and digest. The Job must settle to one total and zero active members, and
all controller-owned handles must close.

## Preserved participant boundary

A fresh image-bound contender runs before participant launch, after the control
connection, and after the ready challenge. The participant still launches with
M217's exact remote-debug exclusion. Retained token, native session, pipe DACL,
expected executable image, observed image, retained source, challenge/release,
settlement, post-settlement access, and final source snapshots remain required.
No content or namespace mutation is performed.

## Evidence and authority boundary

This establishes only that M218's same-logon, Job-contained contender was bound
before resume to the controller's retained expected interpreter image. It does
not bind contender script bytes. Source-commit provenance remains unproved.
Imported standard-library module bytes remain unbound, as do native DLLs,
loader behavior, interpreter state, build provenance, and environment values
outside isolated-mode exclusions.

It does not prove a distinct security principal, hostile executable,
independent host, privileged-bypass resistance, debugger/kernel resistance, or
a cleanup action. Criteria 6 and 7 remain unresolved. Windows is not admitted,
cleanup remains unimplemented and unauthorized, and no public self-hosted
runner is introduced.

M219 adds no runtime source, public API, CLI or MCP command, production harness,
collector, credential or account lifecycle, privilege transition, filesystem
mutation, network listener, dependency, package payload, version, workflow,
permission, secret, hosted allocation, or admission decision.

## Primary references

- [QueryFullProcessImageNameW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-queryfullprocessimagenamew)
- [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [Python command-line interface](https://docs.python.org/3/using/cmdline.html)
- [NIST Secure Software Development Framework publications](https://csrc.nist.gov/Projects/ssdf/publications)
- [SLSA provenance](https://slsa.dev/spec/v1.2/provenance)
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
