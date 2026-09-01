# Windows contained source-access refusal probe

**Status:** Accepted M218 current-host test evidence; no cross-principal,
independent-host, or cleanup-authority admission has occurred.

M218 composes one fixed Job-contained same-logon child process with the exact
frozen M212-M217 process, token, session, executable-image, retained-source,
access-refusal, and remote-debug-exclusion boundary. The probe is Windows-only,
test-only, offline, access-only, and fixed-purpose. It does not operate on a
cache fixture or issue a cleanup action. Criteria 6 and 7 remain unresolved,
Windows is not admitted, and cleanup remains unimplemented and unauthorized.

## Exact contender boundary

Each observation creates a fresh private Job Object configured with
`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`, then launches exactly one fixed direct
child process:

```text
pythonw.exe -I -B windows_contained_source_access_contender.py
```

The command accepts no arguments. The contender derives the retained
participant path from its own fixed fixture location. It has no inherited
handles, output channel, network channel, shell, arbitrary evaluation, or
caller-selected path. The child is created suspended, assigned to the private
Job, checked for exact membership and accounting, and verified against the
controller's same logon before it is resumed.

The child is assigned while suspended. The Job uses
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE, and the child issues access-only
CreateFileW requests for write and delete access.

Immediately before resume, the Job must report one assigned process and one
active process. Its process list must contain only the retained child PID, the
process must still be active, and the retained controller/child primary-token
snapshots must agree on user SID, logon SID, authentication ID, and session.
The child must exit with status zero, the Job must settle to one total and zero
active processes, and all controller-owned handles must close. Last-Job-handle
close remains a fail-safe for exceptional paths.

## Access-only observation

The contender makes exactly two access-only `CreateFileW` requests against the
retained participant source: one requesting write access and one requesting
delete access. It uses `OPEN_EXISTING` and broad share flags so its own request
does not narrow sharing. It accepts only exact native
`ERROR_SHARING_VIOLATION` (32) for both requests. An unexpectedly successful
handle is closed before the child fails. The contender never calls a content
write, delete, rename, move, replace, truncate, or metadata-changing API.

A fresh contained contender runs before participant launch, after control
connection, and after the ready challenge. The M217 participant still launches
with exact `-X disable_remote_debug`; the retained token, native session, pipe
DACL, expected executable image, observed image, and retained source remain
stable through release and settlement. After the retained source handles close,
the controller confirms both access classes are available without exercising
their rights. Source bytes remain unchanged from the pre-launch snapshot.

## Evidence and authority boundary

This establishes that an independently executing but Job-contained same-logon
process observed the same sharing refusal as the M216 controller-local helper.
It adds an operating-system process boundary and explicit kill-on-close
containment to the observation. It does not prove a distinct security principal,
hostile executable, independent host, privileged bypass resistance, debugger or
kernel resistance, or a cleanup action.

Source-commit provenance remains unproved. Imported standard-library module
bytes remain unbound, as do interpreter state, native DLLs, loader behavior,
and environment values outside isolated-mode exclusions. Criteria 6 and 7
remain unresolved. Windows is not admitted, cleanup remains unimplemented and
unauthorized, and no public self-hosted runner is introduced.

M218 adds no runtime source, public API, CLI or MCP command, production harness,
collector, credential or account lifecycle, privilege transition, filesystem
mutation, network listener, dependency, package payload, version, workflow,
permission, secret, hosted allocation, or admission decision.

## Primary references

- [CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [Python command-line interface](https://docs.python.org/3/using/cmdline.html)
- [NIST Secure Software Development Framework publications](https://csrc.nist.gov/Projects/ssdf/publications)
- [SLSA provenance](https://slsa.dev/spec/v1.2/provenance)
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
