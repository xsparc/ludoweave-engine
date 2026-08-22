# Current Task

- **Task:** M91 - fixed local-header-prefix bounds preflight
- **Status:** Initial exact-head hosted qualification passed, but its first
  readiness audit found one stale README status. The correction, regression
  guard, and complete amended-tree local gate are green; the single DCO feature
  commit is ready to amend and requalify.
- **Base:** Verified M90 closeout squash
  `152a083c2965bf99d54ed5aaba222e6bde1e841f`, tree
  `11a2be31ff96d55cb5f0ac035a2c226000eaf22c`.
- **Branch:** `release/m91-local-header-prefix-bounds`

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

## Remaining acceptance

- Publish one ready feature PR, qualify its exact head through the existing
  quota-conscious hosted topology, perform two separated clean readiness
  audits, and squash-integrate only the exact qualified tree.
- Publish and integrate factual project-record and closeout PRs, clean all M91
  branches/generated targets, and select the next bounded milestone.
