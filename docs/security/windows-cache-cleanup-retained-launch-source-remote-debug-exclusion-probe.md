# Windows retained launch-source remote-debug exclusion probe

**Status:** Accepted M217 current-host test evidence; no remote-attachment,
cross-principal, or independent-host collection has occurred.

M217 composes one current-host remote-debug exclusion observation with the
exact frozen M212-M216 process, token, session, executable-image,
retained-source, and access-refusal boundary. The probe is Windows-only,
test-only, offline, and fixed-purpose. It neither issues a collection action
nor operates on a cache fixture. Criteria 6 and 7 remain unresolved, Windows
is not admitted, and cleanup remains unimplemented and unauthorized.

## Exact launch composition

The fixed direct participant launch is:

```text
pythonw.exe -I -B -X disable_remote_debug - <canonical-pipe-name>
```

The executable is the same uv-managed direct interpreter retained by M212-M216.
`-I` preserves isolated mode, `-B` suppresses bytecode-cache writes,
`-X disable_remote_debug` requests interpreter-level remote-debug exclusion,
and `-` continues to execute the exact retained participant source from
standard input. The canonical private pipe name remains the sole variable
argument.

The M217 composer first calls M215's frozen command-line validator. It then
adds only the exclusion option. A scoped test patch supplies that composer to
M215's existing `CreateProcessW` path during process creation and restores the
frozen composer immediately afterward. The inherited three-handle allowlist,
working directory, suspended creation, private Job Object assignment, resume,
challenge/release protocol, and settlement logic remain unchanged.

Python 3.14 gives this option security meaning: the documented switch disables
the PEP 768 remote-debug interface for the process. Python 3.12 and 3.13 accept
arbitrary `-X` option names but do not implement that remote-debug interface,
so their successful runs establish launch compatibility and the retained
boundary only. They are not evidence that a nonexistent remote-debug facility
was disabled.

## Retained launch-source access refusal

The complete M216 lifecycle remains required. Write and delete access to the
retained participant source must refuse with exact native sharing error 32
before launch, after connection, and after ready. Native client/session/DACL,
same-logon token, expected executable-image, retained image, and retained
source observations must remain stable through challenge and before release.
After participant settlement and retained source close, both access classes
must become available and close without exercising their rights, and the final
source snapshot must equal the pre-launch snapshot.

The probe does not attempt remote attachment, code injection, or process-memory
access. It does not call `sys.remote_exec`, open a target process for virtual
memory operations, supply a remote script, or test an enabled/disabled attack
pair. It also performs no source write, rename, replace, truncate, or delete.

## Evidence and authority boundary

This remains a same-process cooperative observation on one same-host,
same-logon, same-session checkout. A Python 3.14 passing run demonstrates that
the documented exclusion launch composes with the frozen local boundary and
completes its protocol; it does not demonstrate resistance to privileged,
kernel-mode, debugger, injection, process-memory, environment, loader, or
hostile ABA behavior.

Source-commit provenance remains unproved. Imported standard-library module
bytes remain unbound, as do interpreter state, native DLLs, environment values
outside isolated-mode exclusions, and operating-system loader behavior. The
tracked fixture is not mutated, and no cleanup or collection action occurs.

M217 adds no runtime source, public API, CLI or MCP command, production
harness, collector, account lifecycle, privilege transition, filesystem
mutation, network listener, dependency, package payload, version, workflow,
permission, secret, hosted allocation, or admission decision. No public
self-hosted runner is introduced.

## Primary references

- [PEP 768 - Safe external debugger interface for CPython](https://peps.python.org/pep-0768/)
- [Python command-line interface](https://docs.python.org/3/using/cmdline.html)
- [Windows process security and access rights](https://learn.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights)
- [CreateFileW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew)
- [SLSA provenance](https://slsa.dev/spec/v1.2/provenance)
- [GitHub Actions matrix jobs](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations)
- [GitHub Actions secure-use reference](https://docs.github.com/en/actions/reference/security/secure-use)
