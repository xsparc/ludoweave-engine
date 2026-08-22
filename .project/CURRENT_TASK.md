# Current task

- **Task:** M94 - local-header flag-consistency preflight
- **Status:** Feature PR #234 and integration-record PR #235 are verified and
  squash-integrated. The closeout-only record is active; no product or policy
  work remains in M94.
- **Base:** Verified M94 integration-record squash
  `f2c5c7865ba1cad42f8dc625f8da0895ca8f0b90`, tree
  `3023d335b15b2e9f6839365551c10d4a8c9b988d`.
- **Branch:** `release/m94-closeout`.

## Accepted result

- After M93 local-name consistency, private release smoke reads exactly two
  little-endian bytes at each parser-exposed `ZipInfo.header_offset + 6` from
  the owned checksum-admitted snapshot.
- The local general-purpose flag field must equal central
  `ZipInfo.flag_bits`; mismatch raises stable content-silent `sample bundle
  local header flags are inconsistent` before decoded-name policy, metadata,
  exact inventory, staging, or reads.
- The position-restoring helper preserves existing cleanup and failure
  precedence. RFC-0077 records the bounded decision.
- No local compression-method or extra-field comparison, broad flag allowlist,
  field-wide parser, inter-member layout policy, workflow, dependency,
  producer, runtime API, tag, release, publication, or release-authority change
  was introduced.

## Verified publication result

- Feature PR #234 exact head `23ad66250455aab68e7478903b7f2238983406aa`
  passed the full three-allocation gate and squash-integrated as
  `7974b6fc110f995cac25f7d69d9c48b55013a764` with the exact qualified tree,
  sole M93-closeout parent, DCO trailer, and valid GitHub signature.
- Integration-record PR #235 exact DCO head
  `77e14ca27eb8cf28fb19787647f7580f5488a4e9`, tree
  `3023d335b15b2e9f6839365551c10d4a8c9b988d`, passed run `32582755728` in
  one 49-second Linux job `97054488280`; desktop job `97054590470` skipped
  with zero steps.
- Hosted integration qualification passed 337-file formatting, Ruff, strict
  docs, all 1,198 documentation-architecture assertions, reproducible builds,
  installed-wheel smoke, ten-artifact staging, and complete release smoke.
- The 276,592-byte wheel retained SHA-256
  `6167497499b5e87fac82007b9db3f2e30912229e64e9ca518e6e5a8d19b6d04d`;
  the 1,404,994-byte source archive has SHA-256
  `e6ee886bee2ab5cfbd41019ac48264fe95b9008ad547bc494393075fb33cb4af`.
- Two separated readiness audits retained exact head/tree/base, one DCO
  commit, five paths, the bounded successful Linux check, a zero-step skipped
  desktop umbrella, `MERGEABLE/CLEAN`, and zero feedback. Their separator
  passed all five metadata-hygiene assertions.
- Guarded integration squash
  `f2c5c7865ba1cad42f8dc625f8da0895ca8f0b90` retained the exact reviewed
  tree, sole feature-squash parent, DCO trailer, and a valid GitHub signature
  at `2026-08-22T15:49:42Z`. Its branch is deleted locally/remotely and no
  postmerge workflow ran.
- The three-record closeout passes five metadata-hygiene assertions, whitespace,
  and full Git checking with no corruption. Remote refresh retains exact
  integration-squash branch/main/origin/merge-base identity, `0 0` divergence,
  only the necessary local closeout branch plus `main`, only remote `main`, and
  empty open-PR, branch-run, release, and tag queries.

## Remaining acceptance work

- Validate, commit, publish, audit, and squash-integrate exactly the three
  project closeout records without runner allocation.
- Delete verified M94 generated targets and all branches except `main`, verify
  the final feature/integration/closeout sole-parent chain, then select M95.
