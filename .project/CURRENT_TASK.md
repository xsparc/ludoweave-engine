# Current Task

- **Task:** M93 - local-header name-consistency preflight
- **Status:** Feature PR #231 is exact-head qualified and squash-integrated.
  The factual integration record is active; no product or policy work remains
  in this branch.
- **Base:** Verified M93 feature squash
  `64dbd6495ebeb0f8460340d84662a218498f9f03`, tree
  `5eb11bd7dbdb62d61bafdd94d2c94ec0ae4355aa`.
- **Branch:** `release/m93-integration-record`

## Accepted slice

- After every established policy through M92, read each already bounded local
  file-name from the owned checksum-admitted snapshot.
- Reconstruct `ZipInfo.orig_filename` as UTF-8 when central `flag_bits` bit 11
  is set and CP437 otherwise, then require exact raw-byte equality.
- Reject a mismatch or impossible central reconstruction with stable content-
  silent error `sample bundle local header names are inconsistent` before
  decoded-name policy, metadata, exact inventory, staging, or reads.
- Preserve empty-archive admission, every M84-M92 precedence rule, snapshot-
  position restoration, every later failure category, and owned-resource close
  rules.
- Add RFC-0076 plus aligned public, security, architecture, release, roadmap,
  maintainer, navigation, and repository evidence records.
- Add one raw local-name consistency classifier only: no local-flag comparison,
  extra-field comparison or parsing, field-wide local/central consistency,
  next-header or payload bound, complete local-record extent, gap/adjacency/
  contiguity/non-overlap policy, inter-member layout validator, repair,
  workflow, dependency, lock, version, producer, runtime package/API, release
  authority, tag, release, or publication.

## Direction evidence

- PKWARE APPNOTE 6.3.10 sections 4.3.2 and 4.3.7 require corresponding local
  and central member records and place the variable name immediately after the
  fixed local prefix. Appendix D defines CP437 by default and UTF-8 under bit
  11.
- Python documents the same metadata encoding precedence and public
  `ZipInfo.flag_bits`/`header_offset` fields. CPython 3.14 reads the local name,
  decodes it under the local bit-11 policy, and compares it with
  `orig_filename` only during member open; M93 does not import private names.
- A same-length `second.txt` to `second.txu` local-only mutation leaves central
  names `first.txt`/`second.txt` and offsets `[0, 46]` visible. Exact installed
  CPython 3.12.13, 3.13.13, and 3.14.5 each read the first payload and defer
  public `BadZipFile` until the malformed second member opens.
- The fixed producer's 50 local names match the central names reconstructed
  through their public central encoding flags.

## Current evidence

- M92 feature PR #228, integration-record PR #229, and closeout PR #230 are
  squash-integrated as a sole-parent chain ending at exact synchronized
  `main` `74972042525041e9251ce245a1fd4ea75add6047`. All three squashes retain
  standalone DCO and valid GitHub signatures.
- Only `main` remains locally and remotely; divergence is `0 0`. There is no
  open PR, current-head run, tag, release, tracked retired identity-control
  path, or M92 generated target. Thirty-eight verified M92 temporary targets
  were removed. Full Git checking reports no corruption, with expected squash-
  era dangling objects.
- The temporary M93 behavior probe is format/Ruff clean and produces identical
  structural observations on exact supported CPython 3.12.13, 3.13.13, and
  3.14.5.
- The first static-clean contract estimate named 22 cases, but collection
  revealed 21. Its non-authoritative red run passed 13 controls and failed
  eight missing-policy assertions in 0.32 seconds.
- An explicit UTF-8 mismatch case corrects the contract to 22 cases. The
  corrected contract is format/Ruff clean and strict Pyright reports zero
  findings. Its authoritative red run passes 13 inherited behavior,
  precedence, empty-archive, producer, and protected-surface controls while
  nine missing stable-error, helper, cleanup, source-order, and documentation
  assertions fail in 0.35 seconds. No complete pass is claimed.
- Release smoke now contains the intended raw local-name comparison immediately
  after M92. RFC-0076 and aligned public records define the rule and explicit
  nonclaims.
- The corrected contract passes all 44 combined M92-M93 assertions and each of
  its 22 cases on exact CPython 3.12.13, 3.13.13, and 3.14.5. Complete suites
  pass 2,703 tests with 16 established skips on each interpreter.
- The first complete 3.12 run exposed one retired-marker record phrase and two
  stale M72/M73 error-precedence expectations. The record phrase is neutral,
  and both inherited tests now assert M93's earlier content-silent classifier;
  the corrected targeted and complete gates pass.
- The unchanged lock and protected files are verified. All 336 Python files
  are format/Ruff clean, strict Pyright reports zero findings, all 1,173
  architecture assertions pass with one established Windows skip, strict docs
  and metadata hygiene pass, and whitespace is clean.
- Ten real-wgpu tests, both profiles, both deterministic vertical slices, two
  byte-identical builds, isolated-wheel smoke, ten-artifact staging, and
  complete release smoke pass. Independent scope/security/archive review finds
  no actionable issue across the exact 18-path change.
- Precommit remote refresh retains exact M92 base/main/origin/merge-base
  identity and `0 0` divergence. Only `main` and the necessary M93 branch exist
  locally and only remote `main` exists; authentication is valid and open PR,
  current-branch run, release, and tag queries are empty. Git checking finds no
  corruption.
- Ready PR #231 exact DCO head
  `a0e160f4248cf8de88ee318960ee9bef41242f55`, tree
  `5eb11bd7dbdb62d61bafdd94d2c94ec0ae4355aa`, passed run `32578695971` in
  exactly three Linux-first allocations: Linux in 7m21s, macOS in 2m04s, and
  Windows in 4m14s. Every hosted supported-Python suite passed 2,718 tests;
  the 3.13/3.14 suites retained one established capability skip.
- Every platform passed ten real-wgpu tests, graphics profiling, Clockwork
  Arena, and Agent World Builder. Linux also passed formatting, Ruff, strict
  Pyright, strict docs, base profiling, reproducible builds, installed-wheel
  smoke, ten-artifact staging, and complete release smoke.
- Hosted builds reproduced a 276,453-byte wheel at
  `d30047cb6671e83592009410c9d75449084c80bfcafb6f828431150cbcd93b9a`
  and a 1,397,392-byte source archive at
  `e63abf65b518a4eb36a7753b1f93f7168bc26e5e498ad62f5a319003107914ad`.
- Two separated audits retained exact head/tree/base, three successful checks,
  one exact-head run, `MERGEABLE`/`CLEAN`, and zero feedback. Their separator
  passed all 22 M93 plus five metadata assertions with protected hashes and
  whitespace clean.
- Guarded feature squash `64dbd6495ebeb0f8460340d84662a218498f9f03`
  has the exact qualified tree, sole parent exact M92 closeout, standalone DCO,
  and a valid GitHub signature. Local `main` is exact synchronized; the feature
  branch is deleted locally/remotely and no postmerge workflow ran.
- The five-record factual update is format/Ruff clean, strict Pyright reports
  zero findings, all 1,173 architecture assertions pass with one established
  skip, strict docs and metadata hygiene pass, and whitespace is clean.
- Two fresh integration-record builds retain the 276,467-byte feature wheel at
  `ca8d9bd9a94270f7b0a63b4e0bee173d47cddd88fb7fda46c5abec1e4ec3b1d7`
  and reproduce a 1,398,640-byte source archive at
  `4236d5f574d13cfddb7c6728aa68607552c8a93dfbad08deb307a9d109a386e2`;
  installed-wheel, ten-artifact staging, and complete release smoke pass.
- The final record separator retains 336-file format/Ruff cleanliness, strict
  Pyright zero findings, 1,173 passing architecture assertions with one skip,
  strict docs, five metadata assertions, and clean whitespace.
- Precommit refresh retains exact feature-squash head/main/origin/merge-base
  identity and `0 0` divergence. Only `main` and the necessary five-record
  branch exist locally, only remote `main` exists, and open PR, branch-run,
  release, and tag queries are empty.

## Remaining acceptance

- Validate, commit, publish, audit, and squash-integrate this five-record
  factual integration update through the bounded documentation gate.
- Publish and integrate the closeout-only record without runner allocation,
  clean all M93 branches/generated targets, and select the next bounded
  milestone.
