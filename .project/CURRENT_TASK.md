# Current Task

- **Task:** M77 - NUL-suffixed sample-member name preflight
- **Status:** The exact 16-path feature candidate is fully locally qualified,
  reviewed, and frozen for DCO publication.
- **Base:** Exact clean synchronized M76 closeout
  `701637f99447f4d64c84047e64ec5edfa0c6889f`, tree
  `27cfc273accb3190d0c50e6a344685875cce541b`.
- **Branch:** `release/m77-nul-member-name-preflight`

## Acceptance boundary

- Inspect every checksum-admitted member's decoded `ZipInfo.orig_filename` for
  an exact NUL code point after established flag checks and before member
  metadata, inventory validation, staging, or reads.
- Emit the stable content-silent policy error
  `sample bundle member name contains a NUL byte` without rendering any
  archive-controlled name or suffix.
- Preserve M69 encryption, M75 compressed-patch, and M76 enhanced-deflate error
  precedence.
- Check exactly for NUL in `orig_filename`; do not reject arbitrary differences
  between original and normalized names, parse raw ZIP headers, or claim local-
  header/central-directory consistency.
- Prove later-member ordering, owned source/snapshot/archive cleanup, unchanged
  producer compatibility, and the existing exact visible inventory.
- Add RFC-0060 and align public security, architecture, release, changelog,
  maintainer, roadmap, and project-state records.
- Change no workflow, runner allocation, dependency, version, sample producer,
  runtime package/API, release authority, tag, release, or publication surface.

## Evidence so far

- Current CPython source preserves the decoded central-directory filename used
  to construct `ZipInfo` in `orig_filename`, then sanitizes `filename` by
  truncating at the first NUL. Current Python documentation explicitly
  documents NUL truncation for archive names.
- Installed CPython 3.12.13, 3.13.13, and 3.14.5 each read an in-memory member
  stored as `root/README.md\0hidden`, expose the full original name, expose the
  truncated normalized name, and return the payload.
- Against unchanged M76, the new 12-case regression is format/Ruff clean and
  strict Pyright clean. Six standard-library, precedence, producer, and
  protected-surface assertions pass; six early-policy, ordering, cleanup,
  helper/source, and documentation assertions fail in 0.91 seconds.
- One exact private helper now checks `"\x00" in original_name` after the three
  established flag categories. The corrected M69/M75/M76/M77 checkpoint passes
  40 assertions; only the deliberately absent RFC/docs assertion failed before
  documentation was added.
- With RFC-0060 and aligned public/project records present, all 12 M77
  assertions pass in 0.89 seconds. Exact M64-M77 inherited extraction evidence
  passes 148 assertions with 1 local filesystem-capability skip in 1.68
  seconds; affected static checks, strict docs, and whitespace pass.
- The whole-tree gate resolves the unchanged 46-package lock, restores 45
  graphics packages, and passes all 320 formatted files, Ruff, and strict
  Pyright. CPython 3.12, 3.13, and 3.14 each pass 2,367 tests with 15 skips;
  all 837 architecture assertions pass with 1 local capability skip.
- Ten real-wgpu tests, both five-repeat profiles, Clockwork Arena, Agent World
  Builder, and all four diagnostic benchmark validators pass. M1 observes 1 of
  2 targets, M2 has no targets, M3 meets 0 of 2 current targets, and M4 observes
  its baseline target.
- Two builds reproduce a pure 274,448-byte wheel and 1,272,210-byte source
  distribution; isolated-wheel, deterministic ten-artifact staging, and
  complete release smokes pass. The sample remains 111,168 bytes/50 entries at
  its established digest.
- Findings-first review corrected an overbroad documentation implication:
  `orig_filename` is the decoded central-directory filename used to construct
  `ZipInfo`, not a universal record of later name-normalization paths. The
  corrected 12-test focus, 837 architecture assertions, whole-tree static gate,
  strict docs, and whitespace pass.
- Record-inclusive builds reproduce the same pure 274,448-byte wheel at
  `ecf37cf1a420433cdc0b5a3ff07fefff5450e5d7ae0b6cdff1e2d3e88639dea9`
  and a 1,273,541-byte source distribution at
  `11f7a22829654db4dd855bf771bfd8d8cf391136872b7152d1ff5a817ddd765f`;
  installed-wheel, deterministic staging, and complete release smokes pass.
- The final audit is clean at exactly 16 intended paths. Protected workflow,
  producer, metadata, and lock hashes are unchanged; explicit development-tool
  identity, credential/private-key, archive-content, whitespace, and full Git-
  object checks pass. Feature `HEAD`, `main`, `origin/main`, and merge base are
  exact M76 closeout with symmetric difference `0 0`; only `origin/main`
  exists remotely and GitHub reports no open PR, tag, or release.
- The evidence-inclusive post-record gate passes the unchanged lock, all 320
  formatted files, Ruff, strict Pyright, all 837 architecture assertions with
  1 capability skip, strict docs, whitespace, and exact 16-path scope.

## Next gates

1. Create the exact DCO feature commit and publish a ready PR.
2. Wait for exact-head hosted qualification, complete two review-state audits,
   squash-merge, and verify the resulting tree, parent, identity, and signature.
3. Publish bounded integration/closeout records, delete all milestone branches
   and generated artifacts, then return to clean synchronized `main`.
