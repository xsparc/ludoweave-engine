# Current Task

- **Task:** M85 - conventional central-directory placement preflight
- **Status:** Feature exact-head qualified and squash-integrated; bounded
  integration records are locally qualified for publication.
- **Base:** Verified M84 closeout squash
  `5b21c4798c16fb69b8ef08d40b02a2662677227a`, tree
  `eb1e76fb5ccf1fb151acbfb4bb149c55c31ba06b`.
- **Branch:** `release/m85-integration-record`

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
- Ready PR #207 exact DCO head
  `6b1d7ef2c712c4d80a6bc4538e7ded3aec3ee5d5`, tree
  `b3cab8d267fa26954b7ef2fe36d9dba530f3d393`, passed exact-head run
  `31739467587` in exactly three allocations. Linux passed in 7m22s, macOS in
  2m24s, and Windows in 4m14s. Every hosted suite reported 2,567 passes, with
  one capability skip outside Linux baseline; each OS passed 10 real-wgpu
  tests, profiles, and both sample applications.
- Two separated audits retained the exact base/head, `MERGEABLE`/`CLEAN`,
  three successful checks, matching DCO identity, and zero feedback. Guarded
  squash `c9bb569fc1476d1aaf92c4fb01bfd9210d0398ed` has the exact qualified
  tree, sole M84-closeout parent, parsed DCO, and valid GitHub verification.
  No postmerge run was allocated; the feature branch is deleted locally and
  remotely.
- The integration record changes exactly the three project records plus
  roadmap. The unchanged lock, 328-file format/Ruff checks, strict Pyright,
  all 1,022 architecture assertions, strict docs, whitespace, Git-object
  checking, reproducible distributions, isolated-wheel smoke, deterministic
  staging, and complete release smoke pass.

## Remaining gates

1. Publish and integrate bounded factual records, close out M85, remove its
   branches/generated targets, and return to clean synchronized `main` before
   selecting M86.
