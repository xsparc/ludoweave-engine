# Current Task

- **Task:** M90 - local-header signature preflight
- **Status:** Runtime, RFC, documentation, complete local, graphics,
  distribution, findings-first, record-inclusive, and prepublication history
  gates are green. The exact 16-path feature candidate is ready to commit.
- **Base:** Verified M89 closeout squash
  `92b3e2c351fe92ea0789b46636e0d0a08d29281a`, tree
  `46fa37f60b603ffa79b5ed7354b55fa2da13b953`.
- **Branch:** `release/m90-local-header-signatures`

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

## Remaining acceptance

- Create one standalone DCO commit for the exact 16-path feature candidate,
  push it, and open one ready PR against `main`.
- Publish one ready feature PR, qualify its exact head through the existing
  quota-conscious hosted topology, perform two separated clean readiness
  audits, and squash-integrate only the exact qualified tree.
- Publish and integrate factual project-record and closeout PRs, clean all M90
  branches/generated targets, and select the next bounded milestone.
