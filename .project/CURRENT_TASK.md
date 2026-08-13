# Current Task

- **Task:** M82 - split-volume sample-member preflight
- **Status:** Initial exact-head hosted qualification passed, but hosted review
  found a valid ZIP64 fixture defect; correction and requalification are
  active before integration.
- **Base:** Verified M81 closeout squash
  `ba90021304760284550e3c458901feb0e3e29dbc`, tree
  `63a1caf2bc270a6500466e24c800f4e6f454ddda`.
- **Branch:** `release/m82-split-volume-preflight`

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

## Remaining gates

1. Push the DCO-signed correction to ready PR #198, require a fresh exact-head
   three-allocation substantive gate, address/resolve the review thread, twice
   audit exact head/review state, and guarded-squash only when clean.
2. Publish and integrate the bounded four-record integration and three-record
   closeout PRs, then remove M82 branches/generated targets and return to clean
   synchronized `main` before selecting M83.
