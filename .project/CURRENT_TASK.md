# Current Task

- **Task:** M86 - first local-header placement preflight
- **Status:** Runtime, documentation, findings-first review, and pre-record
  local qualification are complete; exact recorded-tree qualification and
  publication are active.
- **Base:** Verified M85 closeout squash
  `3eb38c5e591f0d73687293f130254d8c8b3256c7`, tree
  `2425b4bbe9fbdb302797fdc4618be9c34662f196`.
- **Branch:** `release/m86-first-local-header-placement`

## Accepted slice

- After every established policy through M85, require the minimum parser-
  exposed `ZipInfo.header_offset` to equal zero.
- Reject a nonzero earliest offset with stable content-silent error `sample
  bundle first local header placement is inconsistent` before M77 decoded-name
  policy, metadata, exact inventory, staging, or reads.
- Preserve the later exact-inventory error for an empty parsed archive and
  preserve every established error precedence and owned-resource close rule.
- Add RFC-0069 plus aligned public, security, architecture, release, roadmap,
  maintainer, and repository evidence records.
- Add no local-header parser, central-directory parser, inter-member layout
  validator, field-consistency validator, signature classifier, archive repair,
  workflow, dependency, lock, version, producer, runtime package/API, release
  authority, tag, release, or publication.

## Direction evidence

- PKWARE APPNOTE sections 4.3.2, 4.3.6, 4.3.7, and 4.3.12 define local headers,
  their position before the central directory, and each central header's
  relative local-header offset.
- Exact installed CPython 3.12.13, 3.13.13, and 3.14.5 reads one- and eleven-
  byte leading-gap fixtures when their relative offsets are updated.
- Those fixtures retain zero M85 concatenation adjustment while the parser-
  exposed earliest local-header offset moves by exactly the gap length.
- The fixed producer exposes 50 members and an earliest offset of zero.

## Current evidence

- M85 feature PR #207 passed exact three-allocation hosted qualification and
  guarded squash integration. Its documentation-only integration PR #208 used
  one 42-second Linux allocation while the desktop umbrella skipped with zero
  steps. Closeout PR #209 changed only three project records and allocated no
  workflow. Exact synchronized `main` is the sole local/remote branch; no open
  PR, tag, release, postmerge run, disclosure marker, or M85 generated target
  remained before M86 selection.
- Cross-version probes on CPython 3.12.13, 3.13.13, and 3.14.5 each read
  zero-, one-, and eleven-byte-gap fixtures. All retained zero M85 geometry
  adjustment; exposed header offsets were exactly 0, 1, and 11.
- The static-clean authoritative red baseline passed 6 compatibility,
  precedence, producer, and protected-surface controls and failed 10 missing
  runtime, ordering, cleanup, helper/source, and documentation contracts in
  0.67 seconds.
- The runtime helper and exact call order make the combined M85-M86 contract
  pass 35 assertions in 0.37 seconds; only the deliberately absent RFC/public-
  documentation contract failed at that checkpoint. RFC-0069 and aligned
  documentation are now added.
- Findings-first review found no production defect and added an end-to-end
  empty-archive regression for the explicitly preserved exact-inventory error.
  The strengthened 17-case M86 contract passes on CPython 3.12-3.14.

## Remaining gates

1. Pass exact recorded-tree static, architecture, lineage, reproducible-build,
   installed-wheel, release-smoke, archive, scope, and hygiene gates.
2. Publish a ready feature PR, require exact-head hosted qualification and two
   separated review audits, then squash-integrate only the qualified tree.
3. Publish and integrate bounded factual records, close out M86, remove its
   branches/generated targets, and return to clean synchronized `main` before
   selecting M87.
