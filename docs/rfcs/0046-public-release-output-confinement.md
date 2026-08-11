# RFC-0046: Confine public release subordinate output

- **Status:** Accepted
- **Date:** 2026-08-12
- **Owners:** LudoWeave maintainers
- **Milestone:** M63

## Context

The portable public-release consumer documents one JSON document on stdout for
success and one content-silent JSON document on stderr for an admitted failure.
Its nested release-document validator already redirected subordinate stdout and
subordinate stderr, but the complete release smoke ran directly. The real smoke
prints a success line, so a successful consumer emitted that line before its
protocol document. A nested failure could likewise write before the consumer's
stable failure document.

The caller also used numeric inequality to interpret both subordinate return
values. Because Python `bool` is a subclass of `int`, `False` and `0.0` compare
equal to integer zero. A custom object can additionally execute comparison
hooks. None is an exact process-style success status.

## Decision

The standalone verifier owns its text output channels for the duration of each
in-process subordinate call:

1. Both release-document validator calls and the complete release smoke redirect
   subordinate stdout and subordinate stderr to private text sinks.
2. Redirection is restored on success and exception through the context-manager
   boundary.
3. A subordinate succeeds only when its result has exact built-in `int` type and
   value zero. Booleans, floats, integer subclasses, and custom comparison
   objects fail without invoking their equality or truth hooks.
4. Invalid validator status retains content-silent
   `public_release.document_mismatch`; invalid smoke status or an ordinary
   admitted smoke exception retains content-silent
   `public_release.smoke_failed`.
5. Consumer success emits exactly one JSON document on stdout and nothing on
   stderr. An admitted consumer failure emits nothing on stdout and exactly one
   JSON document on stderr.

## Boundary

Python documents `redirect_stdout()` and `redirect_stderr()` as temporary
process-global stream replacement. That is suitable here only because this is a
single-thread command-line utility and subordinate calls do not yield control
to concurrent in-process work. M63 does not make the helper a thread-safe or
general library abstraction.

The redirection covers Python writes through `sys.stdout` and `sys.stderr`. It
does not claim to intercept direct operating-system file-descriptor writes or
arbitrary subprocess output. The existing smoke runner already captures its
own subprocess stdout and stderr. Control-flow `BaseException` values retain
their prior propagation behavior after stream restoration.

M63 adds no subprocess, thread, logging system, cleanup, rollback, retry,
workflow, runner allocation, action, permission, trigger, credential,
dependency, lock, version, runtime package/API, release mutation, release
authority, tag, release, or publication. Pull-request evidence is not a real
public release observation, independent verification, future availability,
immutability, artifact security, PyPI availability, or a supported channel.

## Consequences

- Successful public-consumer output is machine-readable as one JSON line.
- Admitted failure output cannot be prefixed by nested validator or smoke text.
- Exact integer status validation cannot call attacker-defined comparison or
  truth hooks.
- Existing failure codes and consumer payload fields remain unchanged.

## Alternatives considered

- Keep the smoke success line. Rejected because it violates the documented
  one-document protocol and complicates strict consumers.
- Accept any value equal to zero. Rejected because equality admits booleans,
  floats, and custom comparison behavior.
- Change `smoke_release` globally so it never prints. Rejected because its
  standalone human-facing success output is useful and the ownership boundary
  belongs at the embedding consumer.
- Capture operating-system descriptors or spawn the smoke in another wrapper
  process. Rejected as unnecessary scope for the current in-process utility.

## References

- [Python 3.14 `contextlib` stream redirection](https://docs.python.org/3/library/contextlib.html#contextlib.redirect_stdout)
- [Python boolean type](https://docs.python.org/3/library/stdtypes.html#boolean-type-bool)
- [RFC-0030: add a cross-platform public release consumer rehearsal](0030-cross-platform-release-consumer-rehearsal.md)
