# Current task

- **Task:** M97 - local-header extraction-version consistency preflight
- **Status:** Implementation, complete local qualification, corrected review,
  record-inclusive artifact/release smoke, and final source/history audit pass.
  Publication readiness is active.
- **Base:** Verified M96 closeout squash
  `bb1867f8cc2cd1e7a5cb56cc596761284e7dea42`, tree
  `27b7b4968c64816dcc39a20e01c0410d4e11c78e`.
- **Branch:** `release/m97-local-version-consistency`.

## Accepted scope

- After M96 local-extra consistency, read exactly two bytes at each public
  `ZipInfo.header_offset + 4`.
- Require those local bytes to equal public central
  `bytes((info.extract_version, info.reserved))`.
- Raise stable content-silent error `sample bundle local header extraction
  versions are inconsistent` before decoded-name policy, metadata, exact
  inventory, staging, or member reads.
- Preserve every established policy through M96, empty-archive inventory
  behavior, owned-resource cleanup, and caller snapshot position.
- Add RFC-0080 plus aligned public, security, architecture, release, roadmap,
  maintainer, test, and factual project records.
- Keep workflow, runner allocations, actions, permissions, credentials,
  dependency/lock/version, sample producer, runtime package/API, release
  authority, tag, release, and publication unchanged.

## Explicit non-scope

- No supported-version allowlist, minimum extractor-capability rule,
  reserved-byte policy, or semantic interpretation of the two bytes.
- No time/CRC/size or field-wide local/central comparison.
- No complete local-record or payload bound, next-header bound, gap, adjacency,
  contiguity, physical overlap rule, or inter-member layout validator.
- No archive repair, general archive sandbox, public release observation,
  workflow change, runtime feature, dependency, native/WASM work, tag, release,
  or publication.

## Direction and red evidence

- Clean M96 audit found exact local/remote closeout
  `bb1867f8cc2cd1e7a5cb56cc596761284e7dea42`, only `main`, no open PR,
  release, tag, or remaining M96 scratch target, a valid three-squash
  DCO/signature chain, and exactly the two intended hosted runs.
- PKWARE APPNOTE 6.3.10 defines a two-byte extraction-version pair in
  corresponding local and central member records. CPython exposes the central
  pair through public `ZipInfo.extract_version` and `ZipInfo.reserved`, while
  its member-open path ignores the local pair.
- A temporary probe changed only the second local extraction-version byte from
  20 to 21. Exact CPython 3.12.13, 3.13.13, and 3.14.5 each retained central
  pairs `[(20, 0), (20, 0)]`, observed local pairs `[(20, 0), (21, 0)]`,
  offsets `[0, 54]`, and read both payloads. The corrected probe was
  format/Ruff clean.
- The new 27-assertion contract is format/Ruff clean and strict Pyright reports
  zero findings.
- The exact CPython 3.14.5 red regression passed 17 supported-runtime behavior,
  inherited precedence, empty-archive, producer, and protected-surface
  controls. Ten stable-error, helper, cleanup, ordering, and documentation
  assertions failed because the M97 policy/RFC did not yet exist. No complete
  pass is claimed from that red checkpoint.

## Remaining acceptance work

- Publish one DCO feature commit, qualify the exact head in the existing three
  essential allocations, then perform guarded feature, factual integration-
  record, and closeout PR integration with branch and scratch cleanup.
