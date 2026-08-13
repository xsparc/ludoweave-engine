# Current Task

- **Task:** M82 - split-volume sample-member preflight
- **Status:** Corrected feature and bounded integration record are qualified,
  reviewed, and squash-integrated; the three-record closeout is active.
- **Base:** Verified M82 integration-record squash
  `f0558e4e3864e54d8bf81c46c656becc505c7f80`, tree
  `53295683df88430e6731fb75a794836ccafdc9f9`.
- **Branch:** `release/m82-closeout`

## Accepted slice

- Reject every parser-exposed nonzero `ZipInfo.volume` with stable content-
  silent error `sample bundle uses a split-volume member`.
- Preserve every established M69/M75/M76/M78/M79/M80/M81 category across all
  members, then apply volume, M77 decoded-name, metadata, exact-inventory,
  staging, and read policy in that order.
- Close the owned source, checksum-admitted snapshot, and archive before the
  policy error returns.
- Add RFC-0065 plus aligned public, security, architecture, release, roadmap,
  and repository evidence records.
- Add no raw end-record parser, local-header parser, multi-volume assembler,
  neighboring-volume discovery, workflow, dependency, lock, version, sample
  producer, runtime package/API, release authority, tag, release, publication,
  or general archive-sandbox claim.

## Direction evidence

- PKWARE APPNOTE section 4.4.13 defines central-directory disk number start as
  the disk on which a file begins.
- CPython assigns that parsed field to `ZipInfo.volume`. Installed CPython
  3.12.13, 3.13.13, and 3.14.5 each exposed patched value one, no extra field,
  no general-purpose flag, and read the same deflated payload.
- The fixed producer emits 50 members whose parser-exposed volume is zero, so
  split-volume placement is outside the intended sample profile.

## Current evidence

- M81 closeout PR #197 changed only the three project records, allocated no
  workflow run, passed two exact-head audits, and squash-integrated exact tree
  `63a1caf2bc270a6500466e24c800f4e6f454ddda` as
  `ba90021304760284550e3c458901feb0e3e29dbc` with sole integration parent,
  parsed DCO, and valid GitHub verification. Only clean synchronized `main`
  remained locally/remotely; no open PR, tag, release, postmerge run, or M81
  generated target remained before M82 selection.
- The static-clean authoritative red baseline passed 12 controls and failed 8
  missing policy, ordering, cleanup, helper/source, and documentation contracts
  in 0.42 seconds.
- One separate `ZipInfo.volume` pass and typed validator make 19 assertions
  pass in 0.29 seconds; only the deliberately absent documentation contract
  remained at that checkpoint. RFC-0065 and aligned public docs are now added.
- Findings-first review corrected the ZIP64-precedence fixture to use an actual
  `0xFFFF` disk-start sentinel and kept the stable error unbroken in RFC-0065.
  The corrected 20-assertion contract passes on CPython 3.12.13, 3.13.13, and
  3.14.5.
- Complete local qualification is clean: CPython 3.12 passes 2,480 tests with
  15 capability skips; the pre-correction full 3.13/3.14 suites each passed
  2,470 with 16 skips and the corrected focused contract passes on both. Real-
  wgpu, profiles, both vertical slices, M1-M4 diagnostic validators, byte-
  reproducible builds, isolated-wheel smoke, ten-artifact staging, and release
  smoke pass. Exact scope is 15 paths and protected/hygiene scans are clean.
- Ready PR #198 initial head `d7e1eef7e857ef82a26af5ae27f2418592bfa745`
  passed run `31723899463` in exactly three allocations. Hosted review then
  correctly found that the ZIP64-precedence fixture set central disk start to
  `0xFFFF` but omitted the corresponding 32-bit disk-start value from the
  ZIP64 extra field. That head is not mergeable evidence. The helper now emits
  the conditional 32-bit value and the test observes the well-formed field,
  parser-exposed sentinel, and readable payload before checking precedence.
- Corrected focused execution passes all 20 assertions on CPython 3.12.13,
  3.13.13, and 3.14.5; affected format/Ruff/Pyright, strict docs, and whitespace
  pass. The corrected complete 3.12 graphics-baseline suite passes 2,480 tests
  with 15 capability skips.
- Corrected exact DCO head `9edbe5e5bf706bd11b31546bd26fcb8421f1f5d9`
  passed run `31725451119`, classified substantive with 15 paths, in exactly
  three allocations: Linux 7m12s, Windows 4m17s, and macOS 2m16s. Linux
  CPython 3.12/3.13/3.14 and both desktop 3.14 suites passed 2,485 tests, with
  one compatibility skip outside baseline; every OS passed 10 real-wgpu tests,
  graphics profiling, Clockwork Arena, and Agent World Builder.
- Hosted reproducibility produced a 275,086-byte pure wheel at
  `fff5a33caafb89572e74cb41dd308611cae896e1c5a62630058f157e17214b99`
  and 1,315,802-byte sdist at
  `d16eb754e00e01d59aff425fedb0bd74db318c1b7e9ab044af3343c9a9db2a46`;
  installed-wheel, ten-artifact staging, and release smoke passed.
- The exact hosted finding received a concrete correction response and is now
  resolved/outdated. Two separated corrected-head audits retained exact base/
  head, `MERGEABLE`/`CLEAN`, three successful checks, zero issue comments, and
  no unresolved thread or later finding.
- Exact-head-guarded squash `f34b42f1ac9813ec2c46063774e8e86087dd67cf`
  has the exact qualified tree, sole M81-closeout parent, parsed DCO, and valid
  GitHub verification at `2026-08-13T17:37:04Z`. No postmerge run was allocated;
  the feature branch is deleted locally/remotely and `main` is synchronized.
- The exact four-record integration tree passes the lock/static/architecture/
  docs/repository gate. Two builds reproduce a 275,100-byte wheel at
  `b0fb35139e5c6bc47beb133d3602bd83b050ff282e78465a9708e3b996e01da5`
  and 1,317,216-byte sdist at
  `b668144e40744981c7b2e5b03dbeb885f31b2394c2a44996d1a4084e7e50ed96`;
  isolated-wheel, ten-artifact staging, and complete release smoke pass.
- Ready integration PR #199 exact DCO head
  `78e440e87a3af11fa7123f40596bead906ef5786`, tree
  `53295683df88430e6731fb75a794836ccafdc9f9`, classified documentation with
  four paths. Run `31727082001` used one 43-second Linux job; the desktop
  umbrella skipped with zero steps. All 325 files were format/Ruff clean,
  strict docs built in 1.71 seconds, and all 941 hosted architecture assertions
  passed in 10.40 seconds.
- Hosted integration builds reproduced a 275,086-byte wheel at
  `fff5a33caafb89572e74cb41dd308611cae896e1c5a62630058f157e17214b99`
  and 1,317,719-byte sdist at
  `030ba0cc1a60452af81c260771c7ade982f576fc8753602e867766a5b8a40833`;
  installed-wheel, ten-artifact staging, and release smoke passed.
- Two separated audits retained exact base/head, `MERGEABLE`/`CLEAN`, one
  successful bounded Linux check, one skipped zero-step desktop umbrella, and
  zero comments, reviews, or threads. Exact-head-guarded squash
  `f0558e4e3864e54d8bf81c46c656becc505c7f80` has the exact reviewed tree,
  sole feature-squash parent, parsed DCO, and valid GitHub verification at
  `2026-08-13T17:44:59Z`. No postmerge run was allocated and the integration
  branch is deleted locally/remotely.
- The exact three-record closeout passes the complete static, architecture,
  docs, whitespace, Git-object, protected-surface, and added-content hygiene
  gate. It changes no workflow, runtime, verifier, producer, dependency,
  package, test, public documentation, roadmap, or release-authority surface.

## Remaining gates

1. Publish and integrate exactly the three-record closeout; confirm no workflow
   allocation and twice audit exact head/review state.
2. Remove M82 branches/generated targets and return to clean synchronized
   `main` before selecting M83.
