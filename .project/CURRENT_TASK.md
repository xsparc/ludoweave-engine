# Current Task

- **Task:** M92 - local-header variable-envelope bounds preflight
- **Status:** Feature PR #228 passed exact-head hosted qualification, two
  separated clean readiness audits, and guarded squash integration. The
  factual integration record is active before the closeout-only PR.
- **Base:** Verified M91 closeout squash
  `0d89517265ffbca931c5fa9d76f666900371e23c`, tree
  `5e9b52d47d7d9b71ab5e803c30828bed53d8c94e`.
- **Branch:** `release/m92-integration-record`

## Accepted slice

- After every established policy through M91, read exactly the two 16-bit
  little-endian local file-name and extra-field length declarations.
- Require every
  `header_offset + 30 + file_name_length + extra_field_length` to be no greater
  than the conventional central-directory offset.
- Reject a crossing local-header variable envelope with stable content-silent
  error `sample bundle local header envelopes are out of bounds` before
  decoded-name policy, metadata, exact inventory, staging, or reads.
- Preserve empty-archive admission, every M84-M91 precedence rule, snapshot-
  position restoration, every later failure category, and owned-resource close
  rules.
- Add RFC-0075 plus aligned public, security, architecture, release, roadmap,
  maintainer, navigation, and repository evidence records.
- Add one two-field envelope-bound classifier only: no local-name comparison,
  extra-field parsing, field consistency check, next-header or payload bound,
  complete local-record extent, gap/adjacency/contiguity/non-overlap policy,
  inter-member layout validator, archive repair, workflow, dependency, lock,
  version, producer, runtime package/API, release authority, tag, release, or
  publication.

## Direction evidence

- PKWARE APPNOTE 6.3.10 section 4.3.7 defines the two local file-name and extra-
  field lengths as the final four fixed-prefix bytes and places both variable
  regions immediately afterward. Python documents `ZipInfo.header_offset` as
  the byte offset to the file header.
- CPython 3.14's public implementation describes the same fixed structure,
  reads the declared local name, skips the declared extra bytes, and only then
  performs later consistency and overlap checks; M92 does not import or depend
  on its private names.
- Changing only the final local file-name length to 65,535 in a two-member
  archive leaves offsets `[0, 46]`, both `PK\x03\x04` signatures, and the second
  fixed-prefix end at 76 before directory offset 94. The declared envelope ends
  at 65,611. Exact installed CPython 3.12.13, 3.13.13, and 3.14.5 each read the
  first payload and defer public `BadZipFile` until the malformed member opens.
- The fixed 50-member producer keeps every complete local-header variable
  envelope before the conventional central directory.

## Current evidence

- M91 feature PR #225, integration-record PR #226, and closeout PR #227 are
  squash-integrated. M92 feature PR #228 is also squash-integrated as
  `22e26cd732dcc4b0523e6cdb7d89ac7d3946b8ed`, tree
  `803cafd5b8e8e3d7d5d8484137a4d0ab531c2db9`, with sole parent exact M91
  closeout, standalone DCO, and a valid GitHub signature.
- The temporary M92 behavior probe is format/Ruff clean and produces identical
  structural observations on exact supported CPython 3.12.13, 3.13.13, and
  3.14.5.
- The new 22-case M92 contract is format/Ruff clean and strict Pyright reports
  zero findings. Against untouched M91 runtime/docs, its authoritative red run
  passes 12 standard-library behavior, established precedence, empty-archive,
  producer, and protected-surface controls while 10 missing policy, helper,
  cleanup, source-order, and documentation contracts fail in 0.30 seconds. No
  pass is claimed.
- Release smoke now reads the two local length fields and applies the envelope
  bound immediately after M91. RFC-0075 and aligned records define the rule and
  explicit nonclaims. All 42 combined M91-M92 assertions pass on CPython 3.12
  after replacing the fossilized M91 README milestone-number check with a
  structural two-status consistency guard.
- All 22 M92 assertions pass serially on exact CPython 3.12.13, 3.13.13, and
  3.14.5. Complete suites pass 2,681 tests with 16 established skips on each
  interpreter. The first concurrent focused attempt was invalid because three
  uv processes competed for the shared environment; no multi-runtime pass is
  claimed from it.
- The unchanged 46-package lock resolves and the 45-package CPython 3.12
  graphics environment is restored. All 335 Python files are format/Ruff clean,
  strict Pyright reports zero findings, all 1,151 architecture assertions pass
  with one established Windows capability skip, strict docs and whitespace
  pass. One first architecture run hit a transient Windows directory-replace
  denial; its focused and complete fresh-root reruns pass.
- All ten real-wgpu tests, both one-repeat profile shapes, Clockwork Arena, and
  Agent World Builder pass with their established state, capture, and replay
  identities.
- Two fresh builds reproduce a 276,310-byte pure wheel at
  `142f42c79a44b23ef94836127cb011cce361354ce1758ce7e3784a0a464d72f3`
  and a 1,387,194-byte source archive at
  `3324e96e552134eee8151cb1e23598d8bad8c6ecea6f7ba2b2dae5acebde4c0c`.
  Installed-wheel smoke, ten-artifact staging, and complete release smoke pass.
- Findings-first review finds no defect. Exactly 17 intended paths change;
  workflows, producer, project metadata, lock, and runtime package remain
  protected. Metadata hygiene, credential/backend-leak screening, archive
  contents, and whitespace are clean.
- Record-inclusive gates retain 335-file format/Ruff cleanliness, strict
  Pyright zero findings, 1,151 passing architecture assertions with one skip,
  strict docs, five metadata checks, and whitespace. Two fresh builds retain
  the exact wheel and reproduce a 1,388,803-byte source archive at
  `9a5594a7c13d0ad3fa4fc34986b1845aadac5e58cf5f350d69fb880b0dc67952`;
  wheel, staging, and complete release smoke pass.
- The final exact-record separator retains 335-file format/Ruff cleanliness,
  strict Pyright zero findings, 1,151 passing architecture assertions with one
  skip in 10.18 seconds, strict docs in 1.55 seconds, five metadata checks in
  0.43 seconds, and clean whitespace.
- After fetch/prune, branch head, `main`, `origin/main`, and merge base are exact
  M91 closeout with symmetric difference `0 0`. Only `main` and the necessary
  neutral M92 feature branch exist locally and only `origin/main` remotely;
  authentication is valid and open PR, current-branch workflow, tag, and
  release queries are empty. The last three integrated commits retain DCO;
  full Git checking reports no corruption, with expected squash-era dangling
  objects.
- Ready feature PR #228 exact head
  `379e5f74d8b40a36bcc1124a8a173113171a836e` passed run `32575646939` in
  exactly three Linux-first allocations: Linux in 7m22s, macOS in 2m29s, and
  Windows in 4m42s. Each hosted supported-Python suite passed 2,696 tests; the
  3.13/3.14 suites retained one established capability skip. Every platform
  passed ten real-wgpu tests, graphics profiling, Clockwork Arena, and Agent
  World Builder; Linux also passed static, documentation, base-profile,
  reproducible-build, wheel, staging, and complete-release gates.
- Hosted exact-head builds reproduced a 276,297-byte wheel at
  `fdcb1dfcad52c6dd833b00e570d83cd1639f6eb16137ae8c6b2ef856df180858`
  and a 1,389,514-byte source archive at
  `c220e7ddffe34fd0418fdab3c00e4771e40a0f70fea3df21da45c723f2176f83`.
- Two separated readiness audits retained the exact head/tree/base, all three
  successful checks, `MERGEABLE`/`CLEAN`, and zero comments, reviews, or
  threads. The corrected separator passed five metadata assertions in 0.33
  seconds and retained protected hashes and clean whitespace. The feature
  squash allocated no postmerge workflow.

## Remaining acceptance

- Validate, publish, audit, and squash-integrate this factual project-record
  slice with at most the single essential Linux allocation selected by trusted
  change classification.
- Publish and integrate the closeout-only PR without runner allocation, clean
  all M92 branches/generated targets, and select the next bounded milestone.
