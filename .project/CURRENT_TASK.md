# Current Task

- **Task:** M91 - fixed local-header-prefix bounds preflight
- **Status:** Feature and factual integration-record squashes are verified and
  integrated. The exact three-record M91 closeout is active.
- **Base:** Verified M91 integration-record squash
  `9d4a0025e4e5a57a8946bb3a2ed887ca081c9955`, tree
  `276aa74b790300e5128b6243cf7c42277aa1dda5`.
- **Branch:** `release/m91-closeout`

## Accepted slice

- After every established policy through M90, require every parser-exposed
  `ZipInfo.header_offset` to leave room for ZIP's 30-byte fixed local-header
  prefix before the conventional central directory.
- Reject a prefix that crosses that boundary with stable content-silent error
  `sample bundle local header prefixes are out of bounds` before decoded-name
  policy, metadata, exact inventory, staging, or reads.
- Preserve empty-archive admission, every M84-M90 precedence rule, snapshot-
  position restoration, every later failure category, and owned-resource close
  rules.
- Add RFC-0074 plus aligned public, security, architecture, release, roadmap,
  maintainer, navigation, and repository evidence records.
- Add one arithmetic prefix-bound classifier only: no local-header field
  parser, filename/extra-length interpretation, complete local-record extent,
  payload bound, inter-member layout validator, archive repair, workflow,
  dependency, lock, version, producer, runtime package/API, release authority,
  tag, release, or publication.

## Direction evidence

- PKWARE APPNOTE 6.3.10 section 4.3.7 defines the local-file-header fields as
  30 fixed bytes before its variable file name and extra field. Python
  documents `ZipInfo.header_offset` as the byte offset to the file header.
- CPython 3.14's public implementation describes the corresponding fixed
  structure and computes its size before reading it; M91 does not import or
  depend on those private names.
- Patching the final four compressed bytes to `PK\x03\x04` and changing only the
  second central pointer exposes offsets `[0, 90]` below directory offset `94`.
  Exact installed CPython 3.12.13, 3.13.13, and 3.14.5 each expose valid
  signatures at both offsets, read the first payload, and defer public
  `BadZipFile` until the malformed second member is opened.
- The fixed 50-member producer leaves at least the complete fixed prefix before
  the conventional central directory for every public offset.

## Current evidence

- M90 feature PR #222, integration-record PR #223, and closeout PR #224 are
  squash-integrated. Exact synchronized `main` is closeout
  `152a083c2965bf99d54ed5aaba222e6bde1e841f`; only `main` remains locally and
  remotely, with no open PR, current-head run, tag, release, retired control
  path, or M90 generated target. Git object checking reports no corruption.
- The new 20-case M91 regression contract required one mechanical Ruff format
  and is now format/Ruff clean; strict Pyright reports zero findings. Against
  unchanged M90 runtime/docs, its authoritative red run passes 11 standard-
  library behavior, established precedence, empty-archive, producer, and
  protected-surface controls while 9 missing runtime, helper, cleanup, source-
  order, and documentation contracts fail in 0.35 seconds. No pass is claimed.
- Release smoke now applies the 30-byte prefix bound immediately after M90.
  RFC-0074 and all aligned public and repository records define the rule and
  explicit nonclaims. All 39 combined M90-M91 assertions pass on CPython 3.12.
- All 20 M91 assertions pass on exact CPython 3.12.13, 3.13.13, and 3.14.5.
  Complete suites pass 2,659 tests on each interpreter, with 15 established
  skips on 3.12 and 16 on 3.13/3.14. All 1,129 architecture assertions pass
  with one established Windows capability skip.
- All 334 Python files are format/Ruff clean, strict Pyright reports zero
  findings, strict docs and whitespace pass, the unchanged 46-package lock
  resolves, and the locked CPython 3.12 graphics environment is restored.
- All ten real-wgpu tests, both one-repeat profile shapes, Clockwork Arena, and
  Agent World Builder pass with their established state, capture, and replay
  identities.
- Two fresh builds reproduce a 276,152-byte pure wheel at
  `007272e5a687d66ccca7ae1a324b7274dd8b5464f2ae46e909c1303eaeb24750`
  and a 1,377,835-byte source archive at
  `c2b0f8e9dbd34625dc4d92158af6d9a379ca6fa84baefa0fd6a2f596b91c4ef3`.
  Installed-wheel smoke, ten-artifact staging, and complete release smoke pass.
- Findings-first review found no defect. Exactly 16 intended paths change;
  workflows, producer, project metadata, lock, and runtime package remain
  protected. Metadata hygiene, corrected credential and explicit-identity
  screening, archive contents, whitespace, and Git-object integrity are clean.
- Record-inclusive gates retain 334-file format/Ruff cleanliness, strict
  Pyright zero findings, 1,129 passing architecture assertions with one skip,
  strict docs, whitespace, the exact wheel, and a reproducible 1,379,095-byte
  source archive at
  `3ee670767c914049d48226cd245e83fbfe7e4891b6ef12cf71cae436cf880f3d`;
  wheel, staging, and complete release smoke pass.
- After fetch/prune, branch head, `main`, `origin/main`, and merge base are exact
  M90 closeout with symmetric difference `0 0`. Only `main` and the necessary
  neutral M91 feature branch exist locally and only `origin/main` remotely;
  authentication is valid and open PR, current-branch workflow, tag, and
  release queries are empty. The last three integrated commits retain DCO.
- Initial ready PR #225 head
  `0af7816ad989c9e66f7c90748df2f85cb2578861`, tree
  `18eea0ceaa75a8afe47ce2977247ada6d5c2de89`, passed run
  `31811384356` in exactly three Linux-first allocations. The first readiness
  audit then found one actionable stale detailed README status and disqualified
  that tree from merge. A focused regression now requires both README status
  statements to name M0-M90; the correction passes 25 M91/metadata assertions,
  strict Pyright, Ruff, strict docs, and whitespace.
- The complete correction tree retains 334-file format/Ruff cleanliness,
  strict Pyright zero findings, 1,129 passing architecture assertions with one
  established skip, strict docs, and whitespace. The first complete attempt
  was intentionally interrupted and makes no pass claim; the fresh rerun used
  separate absent temporary roots and passed.
- Corrected DCO head `1e4da54e94525a77d087ad76ad069c5aacacb2a3`, tree
  `6268e4a71ba1dc64c2be5eb3b460b97c979e1f4b`, passed run
  `32572856843` in exactly three Linux-first allocations: Linux in 5m23s,
  macOS in 2m39s, and Windows in 4m33s. Every required runtime passed 2,674
  tests, with one established skip outside Linux CPython 3.12; every OS passed
  ten real-wgpu tests, graphics profiling, and both vertical slices.
- Corrected hosted artifacts are a 276,136-byte pure wheel at
  `a497834b481b073b9e31558745f6d42f53cb0c53b6e542331da55d85b0129222`
  and a 1,381,396-byte source archive at
  `5777fbf69ad83964a787eca90a8c28ff4d60c9ad07c8e83fdaf89beab4b3a0c3`;
  installed-wheel, staging, and complete release smoke passed.
- Two separated corrected-head audits retained exact head/tree/base, one DCO
  commit, 16 paths, three successful checks, `MERGEABLE`/`CLEAN`, one exact-
  head run, no issue comments, and the single historical thread resolved. The
  separator passed 25 M91/metadata assertions in 0.46 seconds.
- PR #225 squash `33b9ed5ba0ed5503db82de0ce8ebb8537f67dc2b` has
  the exact qualified tree, sole parent exact M90 closeout, standalone DCO
  trailer, and valid GitHub signature at `2026-08-22T12:35:24Z`. The feature
  branch is deleted remotely and locally; synchronized `main` has divergence
  `0 0` and no postmerge run.
- The factual integration-record gate is green: all 334 Python files are
  format clean; Ruff and strict Pyright report zero findings; all 1,129
  architecture assertions pass with one established Windows capability skip;
  strict docs build with only the known Material notice; five metadata-hygiene
  assertions pass; and whitespace is clean. Two fresh builds reproduce a
  276,150-byte wheel at
  `3df5bb9a259229645b05e20661bea30d41dc15541671ff84f204ff8a4c280ca8`
  and a 1,382,764-byte source archive at
  `2b76156a210dc80955c339a4f445111957e2f91a26b9844e6d6a8b56c512202d`;
  isolated-wheel, ten-artifact staging, and complete release smoke pass.
- Ready integration-record PR #226 exact DCO head
  `c78ffa68563951e38a770491ace112b77e8463e6`, tree
  `276aa74b790300e5128b6243cf7c42277aa1dda5`, passed run
  `32573846472` in one 49-second Linux job `97033170709`; desktop umbrella
  `97033267512` skipped with zero steps. Hosted documentation architecture
  passed 1,130 assertions, and wheel, staging, and release smoke passed.
- Hosted record artifacts retain the 276,136-byte feature wheel at
  `a497834b481b073b9e31558745f6d42f53cb0c53b6e542331da55d85b0129222`;
  the 1,383,520-byte record-tree source archive is
  `b34bb2144f7aa7ca3bd69f021d05210cebe4e8b7eb804a401813b0a82eec351d`.
- Two separated record audits retained exact head/tree/base, one DCO commit,
  five paths, successful bounded Linux, zero-step desktop, and zero feedback.
  Guarded squash `9d4a0025e4e5a57a8946bb3a2ed887ca081c9955` has the exact
  reviewed tree, sole parent feature squash, standalone DCO trailer, and valid
  GitHub signature verified at `2026-08-22T12:47:17Z`. The record branch is
  deleted remotely and locally.
- Closeout proof: exactly three project records change; metadata hygiene passes
  five assertions in 0.35 seconds, whitespace is clean, and full Git object
  checking reports no corruption. Fetch/prune leaves branch head, `main`,
  `origin/main`, and merge base at exact integration squash with divergence
  `0 0`; only `main` plus this necessary closeout branch exist locally and
  only `origin/main` remotely. Open PR, exact-head postmerge run, tag, release,
  and tracked identity-control-path queries are empty.

## Remaining acceptance

- Commit, publish, and squash-integrate the exact three-path closeout.
- Clean all M91 generated targets, verify sole synchronized `main` and no open
  PR/run/tag/release state, then select the next bounded milestone.
