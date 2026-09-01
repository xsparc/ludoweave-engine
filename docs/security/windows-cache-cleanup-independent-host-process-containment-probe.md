# Windows independent-host process-containment probe

**Status:** Accepted M211 current-host test evidence; no independent-host
collection has occurred.

M211 exercises the smallest native process-control primitive needed by M209's
future `forced_process_termination` action. It is Windows-only, test-only, and
confined to one fixed participant tree. It does not issue collection authority,
operate on a cache or collection fixture, or satisfy M207's independent-host
requirements. Criteria 6 and 7 remain unresolved, `windows_cleanup_admitted is
false`, Windows is not admitted, and cleanup remains unimplemented and
unauthorized.

## Suspended admission sequence

The test controller creates one unnamed Job Object, applies
`JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE`, and sets neither breakaway limit. It then
calls `CreateProcessW` for one fixed `pythonw.exe` participant with
`CREATE_SUSPENDED`, `CREATE_NO_WINDOW`, and an extended startup attribute that
admits exactly one inherited output handle. The direct base interpreter is used
rather than a virtual-environment redirector so the returned process handle
identifies the interpreter that executes the fixture.

Before `ResumeThread`, the controller proves all of the following:

- the retained root process handle is live;
- the root is associated with the new Job Object;
- Job accounting reports exactly one assigned and active process; and
- the output pipe contains no participant byte.

Only after those checks does the controller resume the retained primary-thread
handle and close that thread handle. A failed assignment never falls back to
PID termination, breakaway, an ordinary unsuspended launch, or a shell. If an
already-job-contained host rejects the required nested assignment with access
denied, the capability is explicitly skipped and remains unproved.

## Fixed descendant and private identity

The root uses one direct fixed `CreateProcessW` call to create one `pythonw.exe`
descendant. Both scripts accept only the closed `participant` and `descendant`
modes plus the controller-created inherited output handle. They cannot select a
program, path, job, action, account, fixture, or termination target. There is no
shell, network access, listener, remote control, or environment-selected
behavior.

The controller accepts two bounded canonical readiness records, opens and
retains the descendant process handle while the descendant is live, checks its
native process identity, and verifies `IsProcessInJob` against the private job.
The Job Object process-ID list must contain exactly the root and descendant
identities; any extra process invalidates the observation. Process identifiers
and handle values remain private test coordination data and are never emitted
as public evidence.

## Termination and close semantics

One test calls `TerminateJobObject` with a fixed test-only exit code. It waits on
both retained process handles with five-second native waits, checks both exit
codes, closes both process handles, and requires Job accounting to settle at
exactly two total and zero active processes. A second test closes the last Job
Object handle and proves `JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE` settles both
retained processes. The output and native handles are engine-independent test
resources and are closed once; context cleanup retains the last-close kill as a
fail-safe for partial failures.

The probe uses bounded waits and stable error categories. It does not infer
success from a PID disappearing, a process exit alone, or a successful native
return. It preserves M209's rule that termination targets a retained private
process tree rather than an unbound PID, service, shell, session, or host
process.

## Evidence boundary

The passing M211 tests are one current Windows host observation of a process
containment primitive. They are not a privileged collector, independently
provisioned host evidence, a cross-principal result, a filesystem-capability
profile, interruption/durability evidence, recovery evidence, or a qualifying
M208 artifact. VM power cut remains external hypervisor authority, and physical
power loss remains operator-only. No public self-hosted runner is introduced.

M211 adds no product runtime source, public API, CLI or MCP command, dependency,
package payload, version, workflow, permission, secret, credential lifecycle,
filesystem mutation, cleanup authority, hosted allocation, or admission
decision.

## Primary references

- [CreateProcessW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
- [Process creation flags](https://learn.microsoft.com/en-us/windows/win32/procthread/process-creation-flags)
- [AssignProcessToJobObject](https://learn.microsoft.com/en-us/windows/win32/api/jobapi2/nf-jobapi2-assignprocesstojobobject)
- [Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)
- [Nested Jobs](https://learn.microsoft.com/en-us/windows/win32/procthread/nested-jobs)
- [JOBOBJECT_BASIC_LIMIT_INFORMATION](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-jobobject_basic_limit_information)
- [WaitForSingleObject](https://learn.microsoft.com/en-us/windows/win32/api/synchapi/nf-synchapi-waitforsingleobject)
- [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
