# RFC-0050: Require the exact sample-bundle inventory

- **Status:** Accepted
- **Date:** 2026-08-12
- **Owners:** LudoWeave maintainers
- **Milestone:** M67

## Context

M64 bounds and streams every sample-ZIP member, M65 requires portable and
collision-free member paths, and M66 stages a complete root before publication.
The remaining completeness check recognizes only a required subset of root-level
scripts after extraction. A portable unexpected member can therefore enter the
published sample tree, and a nested asset outside that subset can be missing
without failing release smoke.

The project producer currently emits a deterministic, source-defined inventory
of 50 regular files. Staged-release checksums authenticate the ZIP bytes, but
they do not establish that those archive members are the exact sample product
the verifier expects.

## Decision

The private release-smoke verifier defines the exact 50-member relative POSIX
inventory independently of the unchanged sample producer. During the existing
complete M64/M65 preflight, it collects each validated relative member identity.
After collision, mode, compression, and expansion checks, the observed set must
equal the source-defined expected set.

An unexpected member or missing member fails with the stable content-silent
`sample bundle inventory is unexpected` category. The comparison occurs before
extraction creates a staging directory or opens any archive member. Archive
order does not affect identity. Existing staged-root and streamed-size checks
remain in force after inventory admission.

The architecture contract independently builds the current sample ZIP and
requires its inventory to match the verifier's expectation. Any intentional
sample addition, removal, or rename therefore requires an explicit verifier and
test review in the same change.

## Boundary

M67 is an exact project-product policy for the current deterministic sample
bundle. It is not a general archive sandbox, content scanner, malware detector,
file-format validator, provenance system, or permission policy. It does not
inspect file contents beyond the inherited streamed-size agreement, and it
does not claim that the listed scripts are safe for arbitrary execution.

M67 adds no workflow, runner allocation, action, permission, credential,
dependency, lock, version, runtime package/API, sample producer, release
mutation, release authority, tag, release, or publication. Pull-request
evidence is not a real public release observation.

## Consequences

- The verifier rejects both missing nested assets and unexpected portable files
  before extraction.
- The stable failure category does not disclose the mismatching member name.
- The producer and verifier remain independently reviewable while one test
  proves their current agreement.
- An intentional sample-inventory change must update the explicit expectation;
  silent producer drift fails closed.

## Alternatives considered

- Keep only the post-extraction required root-file subset. Rejected because it
  admits extra members and does not cover nested fixture completeness.
- Import the producer's private file list into the verifier. Rejected because a
  shared mutable expectation would let producer drift redefine verifier policy.
- Embed a self-declared inventory inside the ZIP. Rejected because an
  unauthenticated self-description does not supply an independent expectation.
- Validate member contents or execute every file during preflight. Rejected as
  a broader content-analysis and execution policy without evidence or need.

## References

- [RFC-0049: stage sample extraction before publication](0049-atomic-sample-extraction.md)
- [Python `zipfile` documentation](https://docs.python.org/3/library/zipfile.html)
- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [SLSA 1.2 artifact verification](https://slsa.dev/spec/v1.2/verifying-artifacts)
