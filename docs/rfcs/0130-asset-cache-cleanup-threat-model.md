# RFC-0130: adopt the asset-cache cleanup threat model

- **Status:** Accepted
- **Milestone:** M147
- **Date:** 2026-08-27

## Summary

Adopt a dedicated asset-cache cleanup threat model before designing any cache
mutation. Cleanup remains unimplemented and unauthorized.

## Context

RFC-0129 establishes that M137-M145 aggregate evidence cannot identify safe
deletion candidates or prove current reachability. A future design must also
survive hostile filesystem namespace changes, concurrent users, incomplete
metadata, stale evidence, time rollback, partial failure, replay, and recovery
without exposing sensitive paths.

Current platform guidance does not justify a generic portable delete routine.
MITRE classifies validation-to-use races as CWE-367. Python documents symlink-
attack resistance for `shutil.rmtree` only on platforms with supporting fd-
based functions. Windows reparse points require distinct handling. Cache
garbage-collection policy guidance does not replace identity, reachability,
locking, or recovery evidence.

## Decision

Accept the [asset-cache cleanup threat
model](../security/cache-cleanup-threat-model.md) as a blocking design contract.
It defines assets, actors, trust boundaries, twelve threats, eight security
invariants, misuse cases, cross-platform verification, and residual risk.

Any implementation proposal must map every threat and invariant to a concrete
control and adversarial test. In particular it must separate dry-run evidence
from mutation authority, bind identity-bearing candidates to an exact root and
generation, hold cross-process quiescence through use, use proven handle-
relative no-follow semantics, stage same-filesystem quarantine, and provide
durable typed receipts and idempotent recovery.

If a target platform cannot prove the required namespace and handle semantics,
cleanup must fail closed on that platform. Aggregate stability, age, path
normalization, cache idleness, or a saved record is never sufficient authority.

## Consequences

M147 improves the design gate without adding a runtime API, value, protocol,
decoder, CLI command, candidate disclosure, cache access, retention policy,
lock, trusted time, quarantine, repair, deletion, dependency, version, workflow,
permission, release authority, or CI change. Existing runtime and distribution
surfaces remain byte-exact.

There is no candidate disclosure, no cleanup authority, no remote cache, no
dependency, no workflow, and no CI change.

The next cleanup implementation milestone requires a separate accepted RFC and
explicit maintainer approval. It must begin from this threat model rather than
silently weakening it.

## Alternatives considered

- Implement a dry-run candidate list now. Rejected because identity disclosure
  without complete roots and quiescence can invite unsafe external deletion.
- Use `shutil.rmtree` as the portable security boundary. Rejected because its
  protections are capability- and platform-dependent and do not establish
  retained-root, concurrency, policy, or recovery semantics.
- Treat cleanup as a trusted same-user maintenance task. Rejected because
  accidental concurrency, reparse/link substitution, and crash failure still
  threaten integrity even without a remote adversary.
- Add cleanup only on one operating system. Deferred until a platform-specific
  design proves safe refusal, packaging, receipts, and support semantics.

## Validation

Architecture tests must prove the runtime source tree, scripts, dependencies,
lock, and workflows remain byte-exact; the threat model is complete and
registered; cleanup remains absent; and public security, roadmap, and
architecture documents preserve the accepted boundary. Strict documentation,
the complete supported-Python suite, installed-wheel consumers, reproducible
artifacts, release rehearsal, and findings-first review remain required.

## References

- [MITRE CWE-367](https://cwe.mitre.org/data/definitions/367.html)
- [Python 3.12 `shutil.rmtree`](https://docs.python.org/3.12/library/shutil.html#shutil.rmtree)
- [Microsoft reparse points](https://learn.microsoft.com/en-us/windows-hardware/drivers/ifs/reparse-points)
- [Bazel remote caching](https://bazel.build/remote/caching)
- [RFC-0129](0129-defer-asset-cache-cleanup.md)
