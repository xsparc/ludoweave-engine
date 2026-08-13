# Current Task

- **Task:** M85 - conventional central-directory placement preflight
- **Status:** Locally qualified and independently reviewed; feature publication
  and exact-head hosted qualification are pending.
- **Base:** Verified M84 closeout squash
  `5b21c4798c16fb69b8ef08d40b02a2662677227a`, tree
  `eb1e76fb5ccf1fb151acbfb4bb149c55c31ba06b`.
- **Branch:** `release/m85-central-directory-placement`

## Accepted slice

- After every established policy through M84, read the final conventional
  22-byte end-of-central-directory record through one shared position-
  restoring structural helper.
- Require declared central-directory size plus offset to equal the absolute
  offset of that final record, admitting no prepended-data adjustment.
- Reject a mismatch with stable content-silent error `sample bundle central
  directory placement is inconsistent` before M77 decoded-name policy,
  metadata, exact inventory, staging, or reads.
- Preserve established error precedence and owned source/snapshot/archive
  cleanup.
- Add RFC-0068 plus aligned public, security, architecture, release, roadmap,
  maintainer, and repository evidence records.
- Add no central-directory/local-header parser, end-record search, ZIP64
  parser or sentinel resolution, prepended executable support, self-extracting
  archive support, multi-volume assembler, workflow, dependency, lock,
  version, producer, runtime package/API, release authority, tag, release, or
  publication.

## Direction evidence

- PKWARE APPNOTE sections 4.4.23 and 4.4.24 define the conventional central-
  directory size and starting offset.
- Exact installed CPython 3.12.13, 3.13.13, and 3.14.5 computes a concatenation
  adjustment from the final-record location minus those fields and applies it
  to parsed member header offsets.
- Cross-version probes show one- and eleven-byte prefixes preserve the same
  parsed member and readable deflated payload; the exposed header offset moves
  by exactly the prefix length.
- The fixed producer starts at byte zero, so its declared size plus offset
  lands exactly at the final record.

## Current evidence

- M84 closeout PR #206 changed only the three project records, allocated no
  workflow, passed two exact-head audits, and squash-integrated exact tree
  `eb1e76fb5ccf1fb151acbfb4bb149c55c31ba06b` as
  `5b21c4798c16fb69b8ef08d40b02a2662677227a` with sole integration-record
  parent, parsed DCO, and valid GitHub verification. Only clean synchronized
  `main` remained locally/remotely; no open PR, tag, release, postmerge run,
  disclosure marker, or M84 generated target remained before M85 selection.
- The static-clean authoritative red baseline passed 6 standard-library,
  established-precedence, producer, and protected-surface controls and failed
  13 missing policy, ordering, cleanup, helper/source, and documentation
  contracts in 0.71 seconds.
- The shared final-record helper removes two duplicate structural readers.
  The placement validator and exact call ordering make the entire M83-M85
  runtime lineage pass 80 assertions in 0.51 seconds; only the deliberately
  absent RFC/public-document contract failed at that checkpoint. RFC-0068 and
  aligned documentation are now added.
- Findings-first review corrected an overstatement: zero concatenation
  adjustment is the enforced arithmetic invariant, not proof that no physical
  prefix could exist. A negative-adjustment extraction fixture now joins the
  positive case. The strengthened 20-case contract passes on CPython
  3.12-3.14.
- The corrected CPython 3.12 suite passes 2,562 tests with 15 capability skips;
  all 1,022 architecture assertions and the 333-case M64-M85 release-consumer
  lineage pass with one Windows capability skip each. Static/type/docs,
  real-wgpu, profiles, samples, diagnostics, builds, wheel smoke, deterministic
  staging, and complete release smoke pass.

## Remaining gates

1. Publish a ready feature PR, require exact-head hosted qualification and two
   separated review audits, then squash-integrate only the qualified tree.
2. Publish and integrate bounded factual records, close out M85, remove its
   branches/generated targets, and return to clean synchronized `main` before
   selecting M86.
