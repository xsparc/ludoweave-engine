# Current Task

- **Task:** M90 - local-header signature preflight
- **Status:** Feature and factual integration-record squashes are verified and
  integrated. The exact three-record M90 closeout is validated and ready for
  its standalone DCO commit.
- **Base:** Verified M90 integration-record squash
  `808dff848f04f9ed7f665ad3a6f36047db4053b4`, tree
  `e821498016a867fe4811a83ddafbebc6e5b5f641`.
- **Branch:** `release/m90-closeout`

## Accepted slice

- After every established policy through M89, require the four bytes at every
  parser-exposed `ZipInfo.header_offset` to equal the local-file-header
  signature `PK\x03\x04`.
- Reject a missing or different signature with stable content-silent error
  `sample bundle local header signature is inconsistent` before decoded-name
  policy, metadata, exact inventory, staging, or reads.
- Preserve empty-archive admission, every M84-M89 precedence rule, snapshot-
  position restoration, every later failure category, and owned-resource close
  rules.
- Add RFC-0073 plus aligned public, security, architecture, release, roadmap,
  maintainer, and repository evidence records.
- Add one four-byte signature classifier only: no local-header field parser,
  central-directory parser, record-extent/adjacency/contiguity rule, inter-
  member layout validator, archive repair, workflow, dependency, lock, version,
  producer, runtime package/API, release authority, tag, release, or publication.

## Direction evidence

- PKWARE APPNOTE 6.3.10 requires every record type to have an identifying
  signature, defines the local-file-header signature as `0x04034b50`, and
  requires each stored file to be preceded by a local header. Python documents
  `ZipInfo.header_offset` as the byte offset to the file header.
- Changing only the second central pointer by one byte exposes offsets `[0,
  47]` below directory offset `94`. Exact installed CPython 3.12.13, 3.13.13,
  and 3.14.5 each expose bytes `504b0304`, `4b030414`, read the first payload,
  and defer public `BadZipFile` until the shifted second member is read.
- The fixed 50-member producer exposes `504b0304` at every public offset.

## Current evidence

- M89 feature PR #219, integration-record PR #220, and closeout PR #221 are
  squash-integrated. Exact synchronized `main` is closeout
  `92b3e2c351fe92ea0789b46636e0d0a08d29281a`; only `main` remains locally and
  remotely, with no open PR, current-head run, tag, release, identity-control
  path, or M89 generated target. Git object checking reports no corruption.
- The new 19-case M90 regression contract is format/Ruff clean and strict
  Pyright reports zero findings. Against unchanged M89 runtime/docs, its
  authoritative red run passes 10 standard-library behavior, established
  precedence, empty-archive, producer, and protected-surface controls while 9
  missing runtime, helper, cleanup, source-order, and documentation contracts
  fail in 0.48 seconds. No pass is claimed.
- Release smoke now performs the snapshot-backed four-byte signature
  classifier immediately after M89. RFC-0073 and aligned public, security,
  architecture, release, maintainer, navigation, roadmap, and repository
  records define the rule and its explicit nonclaims.
- All 37 combined M89-M90 behavior, precedence, cleanup, source-order, and
  documentation assertions pass on CPython 3.12 in 0.38 seconds. The two
  affected Python files are format/Ruff clean, strict Pyright reports zero
  findings, and strict docs build with only the known upstream Material notice.
- One initial combined-test command named a nonexistent historical M89 file,
  exited 1, and ran no tests. The corrected exact path produced the 37-test
  pass; the failed invocation is retained in factual evidence.
- The 19-case M90 contract passes on exact CPython 3.12.13, 3.13.13, and
  3.14.5. Complete non-wgpu suites pass 2,639 tests on each interpreter with
  15 established skips. The locked CPython 3.12 graphics environment is
  restored.
- All 1,109 architecture assertions pass with one established Windows
  capability skip; all 333 Python files are format/Ruff clean, strict Pyright
  reports zero findings, strict docs and whitespace pass, and the unchanged
  46-package lock resolves.
- All ten real-wgpu tests, both one-repeat profile shapes, Clockwork Arena, and
  Agent World Builder pass with their established state, capture, and replay
  identities.
- Two fresh builds reproduce a 276,061-byte pure wheel at
  `c2b71f657baaaad330c9076a2cef25c13644874196005be74b8a436bcabc8cc2`
  and a 1,371,380-byte source archive at
  `807966575bc9b2141fefda88ef0ea4395dc8fc34e8307b9879ad5adb9883e262`.
  Isolated-wheel smoke, ten-artifact staging, and complete release smoke pass.
- Findings-first review found no defect. Exact scope is 16 intended paths;
  protected hashes, repository metadata hygiene, credential screening,
  archive contents, whitespace, and Git-object integrity are clean.
- The record-inclusive tree retains 333-file format/Ruff cleanliness, strict
  Pyright zero findings, 1,109 passing architecture assertions with one skip,
  strict docs, and whitespace. Two fresh builds retain the exact wheel and
  reproduce a 1,372,739-byte source archive at
  `d3dacd616f590977116ee126a777c448654e78f24f4f5387cdcdb926a7d2215c`;
  wheel, staging, and release smoke pass.
- Fetch/prune leaves branch head, `main`, `origin/main`, and merge base at exact
  M89 closeout with symmetric difference `0 0`. Only `main` and the necessary
  neutral M90 feature branch exist locally, only `origin/main` remotely,
  authentication is valid, and open PR, current-branch workflow, tag, and
  release queries are empty.
- Ready PR #222 exact DCO head
  `e2fa04c4230756042bde239cfdcd2c6c2b1cfc5c`, tree
  `4acdecef4265e972e15e4ce838cb91e530101cda`, passed hosted run
  `31806688540` in exactly three Linux-first allocations. Linux job
  `94787208676` passed in 7m30s, macOS `94789151633` in 3m15s, and Windows
  `94789151556` in 4m05s.
- Hosted Linux passed 2,654 tests on CPython 3.12 and 2,654 with one skip on
  3.13/3.14. macOS and Windows CPython 3.14 each passed 2,654 with one skip.
  Every OS passed ten real-wgpu tests, graphics profiling, Clockwork Arena,
  and Agent World Builder; Linux also passed static/docs, base profiling,
  wheel, staging, and complete release smoke.
- Hosted exact-head builds reproduced a 276,046-byte pure wheel at
  `2b7b53ea14b1beef2d6ba1409e1c5a25920460d676672a8a41df227ba9a4a8a4`
  and a 1,373,598-byte source archive at
  `5b31e083331b030fabf8fd34353e850efd7e3b7830e30b5eb5f305a7fdda8ad9`.
- Two separated readiness audits retained the exact head/tree/base, one DCO
  commit, 16 paths, three successful checks, `MERGEABLE`/`CLEAN`, one hosted
  run, and zero feedback. The 24-case separator passed in 0.48 seconds.
- Guarded squash `b35b2de7725f2a5367cc48e2acd22835220560ca` has the exact
  qualified tree, sole parent exact M89 closeout, standalone DCO trailer, and
  a valid GitHub signature verified at `2026-08-14T14:05:47Z`. The feature
  branch is deleted remotely and locally.
- Integration-record local proof: exactly four project records plus roadmap
  change. All 333 Python files are format/Ruff clean, strict Pyright reports
  zero findings, all 1,109 architecture assertions pass with one established
  skip, and strict docs and whitespace pass. Two fresh builds retain the exact
  local feature wheel and reproduce a 1,374,693-byte source archive at
  `1f637955f3878f088aa13c24b2e77553c537466d1460afc6f8c23c66efb3eb67`;
  wheel, ten-artifact staging, and release smoke pass.
- Final record-tree proof retains 333-file format/Ruff cleanliness, strict
  Pyright zero findings, 1,109 passing architecture assertions with one skip,
  strict docs, and whitespace. The five-case metadata separator passes.
  Fetch/prune leaves branch head, `main`, `origin/main`, and merge base at exact
  feature squash with divergence `0 0`; only `main` plus this necessary record
  branch exist, and open PR, exact-head postmerge run, tag, and release queries
  are empty.
- Ready integration-record PR #223 exact DCO head
  `ba9d19a503cb748adcb05ad179d44c1047d2a5ae`, tree
  `e821498016a867fe4811a83ddafbebc6e5b5f641`, passed bounded run
  `31808445884` in Linux job `94792942983` in 50 seconds; desktop umbrella
  `94793181074` skipped with zero steps. Hosted documentation architecture
  passed 1,110 assertions, and wheel, staging, and release smoke passed.
- Hosted record artifacts retain the 276,046-byte feature wheel at
  `2b7b53ea14b1beef2d6ba1409e1c5a25920460d676672a8a41df227ba9a4a8a4`;
  the 1,375,288-byte record-tree source archive is
  `f6e9d306808c04f1c80233294578dc3304c4df4c5cb062f826f2279ee9ca2ee2`.
- Two separated record audits retained exact head/tree/base, one DCO commit,
  five paths, successful bounded Linux, zero-step desktop, and zero feedback.
  Guarded squash `808dff848f04f9ed7f665ad3a6f36047db4053b4` has the exact
  reviewed tree, sole parent feature squash, standalone DCO trailer, and valid
  GitHub signature verified at `2026-08-14T14:16:01Z`. The record branch is
  deleted remotely and locally.
- Closeout proof: exactly three project records change; metadata hygiene passes
  five assertions, whitespace and Git objects are clean. Fetch/prune leaves
  branch head, `main`, `origin/main`, and merge base at exact integration
  squash with divergence `0 0`; only `main` plus this necessary closeout branch
  exist, and open PR, exact-head postmerge run, tag, and release queries are
  empty.

## Remaining acceptance

- Commit, publish, and squash-integrate the exact three-path closeout.
- Clean all M90 generated targets, verify sole synchronized `main` and no open
  PR/run/tag/release state, then select the next bounded milestone.
