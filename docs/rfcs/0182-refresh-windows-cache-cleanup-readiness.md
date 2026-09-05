# RFC-0182: refresh Windows cache-cleanup readiness

- **Status:** Accepted
- **Milestone:** M199
- **Date:** 2026-08-30

## Summary

Consolidate the complete M149-M198 Windows cache-cleanup probe sequence into
one explicit readiness decision. Windows readiness remains deferred. The
current evidence is valuable test-only threat-model evidence, but it does not
provide authenticated authority, a complete hard-link policy, durable recovery,
cross-principal validation, or independent-host proof.

Close the method-by-method closed-stream probe tail after M198. Require every
future Windows cleanup milestone to resolve a named admission criterion. Add
one architecture guard and public decision documentation with no authority
increase, runtime code, integration fixture, dependency, workflow, or hosted
allocation.

## Context

M146 deferred cache cleanup until identity-bearing candidates, retention and
quiescence, trusted time, typed mutation receipts, crash recovery, link/reparse
safety, and rollback were designed together. M147 added the threat model. M148
found that portable CPython did not expose the complete handle-relative,
no-follow mutation chain and required an engine-owned adapter plus real-host
evidence before any platform admission.

M149-M198 then added 50 Windows-only, test-only milestones. They cover native
identity and sharing, substitution, process/handle inheritance, cooperative
ranges and guardians, hard-link alias mutation, bounded control settlement,
and concrete buffered-stream failure disposition. They deliberately preserve
the absence of runtime cleanup authority.

The sequence now has enough evidence to restate the admission gap precisely.
Continuing through arbitrary closed-stream methods would not address it.
Python documents even inquiries on a closed stream as undefined, while
Microsoft documents file identity as a single-computer property and file
access as dependent on the caller token and security descriptor. Current-host,
same-principal observations cannot establish those missing trust boundaries.

## Decision

Accept the [Windows cache-cleanup readiness
refresh](../security/cache-cleanup-windows-readiness-refresh.md) as the M199
decision.

Keep Windows cleanup unimplemented and unauthorized. Retain every M146-M198
deferral, security boundary, integration observation, and public non-claim.
Treat the M149-M198 set as complete current-host threat-model evidence, not as
an admission checklist whose size implies readiness.

Close the standalone method-by-method closed-stream investigation after M198.
No future milestone may add an isolated closed-stream inquiry or exception
observation unless its accepted scope names the admission criterion it closes,
explains why existing evidence cannot answer that criterion, and remains
test-only until the complete production design passes.

The reconsideration gate requires one coherent design and validation for:

1. authenticated authority, least privilege, trusted root ownership, and
   durable generation binding;
2. an explicit hard-link refusal or quarantine policy with bounded hard-link
   enumeration if enumeration is used;
3. handle-retained use-time identity, type, link-count, root, and generation
   revalidation immediately at mutation;
4. versioned bounded framing, acknowledgements, and typed receipts;
5. durable intent, same-filesystem quarantine, idempotent recovery,
   reconciliation, and rollback-tamper handling;
6. cross-principal, unrelated-process, hostile-race, ACL, alias, inheritance,
   and reparse adversarial evidence; and
7. independent-host evidence plus explicit safe refusal for unsupported
   Windows/filesystem capability combinations.

This is not a new architecture direction. It is a direction-preserving
readiness checkpoint under ADR-0017 and RFC-0129 through RFC-0131. It makes the
existing deferral easier to audit and prevents local probe results from being
overread as security or production authority.

Use no new hosted allocation. The architecture guard must preserve exact M198,
runtime, examples, scripts, dependencies, and both workflows. It must verify
the complete M149-M198 milestone inventory, the unresolved gate language, the
closed-stream stopping rule, and the absence of cleanup commands or adapters.

## Consequences

The repository gains a concise answer to whether the Windows probe program has
admitted cleanup: it has not. Reviewers can distinguish established local
behavior from unresolved production trust, durability, and recovery work.

The decision reduces roadmap entropy by ending follow-on probes that only add
another concrete stream method. Later work must attack an explicit criterion
and can be evaluated against a stable list rather than an open-ended threat
model tail.

No existing probe is removed or weakened. The evidence remains valuable for a
future adapter design and regression suite. A later RFC may supersede this
decision only with stronger authority and validation evidence.

No runtime API, protocol, decoder, CLI command, public capability probe,
production subprocess/native surface, cache access, cleanup authority,
dependency, compiler requirement, version, workflow, job, matrix, permission,
credential, release authority, tag, package publication, or CI change is
added.

## Alternatives considered

- Continue with `writable()`, `fileno()`, or another closed-stream method.
  Rejected because Python explicitly leaves closed-stream method behavior
  undefined and those outcomes do not resolve a named admission criterion.
- Treat 50 local milestones as sufficient Windows admission. Rejected because
  no authenticated trusted-root authority, durable protocol/recovery, distinct
  principal, or independent host has been proven.
- Delete the probe history as over-specific. Rejected because the current
  evidence documents real Windows threat boundaries and is useful regression
  material for a later adapter.
- Add a Windows-only hosted job for the decision. Rejected because the change
  adds no runtime behavior and the existing suite is the future execution path;
  local validation is sufficient at this unpublished-stack boundary.

## Validation

Architecture validation must:

- preserve exact M198 and the runtime, examples, scripts, lock, metadata, and
  workflows;
- find every architecture milestone number M149 through M198 exactly once as
  a complete set;
- retain exactly 50 pre-M199 Windows integration probes and 50 pre-M199
  security records;
- require the seven unresolved admission criteria and the method-level stopping
  rule in public documentation;
- reject admission, production-readiness, and cleanup-authorization claims;
- prove no cleanup CLI command, adapter, retention, or garbage-collection
  module was added; and
- require public registration of RFC-0182 and the readiness decision.

Run strict documentation, static and current-date governance, supported-Python
regression, packaging/release rehearsal, findings-first review, and exact
scratch cleanup before local closeout. No hosted result may be claimed unless
it is actually allocated and executed later under a safe publication stack.

## References

- [Microsoft: hard links and junctions](https://learn.microsoft.com/en-us/windows/win32/fileio/hard-links-and-junctions)
- [Microsoft: file security and access rights](https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights)
- [Microsoft: file identity and link count](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/ns-fileapi-by_handle_file_information)
- [Python: core I/O tools](https://docs.python.org/3/library/io.html)
- [GitHub Actions secure use](https://docs.github.com/en/actions/reference/security/secure-use)
- [NIST SP 800-218 Rev. 1 initial public draft](https://csrc.nist.gov/pubs/sp/800/218/r1/ipd)
- [SLSA 1.2](https://slsa.dev/spec/v1.2/)
- [RFC-0129](0129-defer-asset-cache-cleanup.md)
- [RFC-0130](0130-asset-cache-cleanup-threat-model.md)
- [RFC-0131](0131-defer-portable-cache-cleanup-capability.md)
- [RFC-0181](0181-probe-windows-hard-link-alias-mutator-closed-stream-write-after-delivery-failure.md)
