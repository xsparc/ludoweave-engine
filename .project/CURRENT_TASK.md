# Current task

- **Task:** M94 - record verified feature integration
- **Status:** Feature PR #234 is squash-integrated; the bounded integration-
  record PR remains.
- **Base:** Verified M94 feature squash
  `7974b6fc110f995cac25f7d69d9c48b55013a764`, tree
  `96bd9000efbc473d09f0c75d83c5e1231621409e`.
- **Branch:** `release/m94-integration-record`.

## Verified feature result

- Exact DCO feature head `23ad66250455aab68e7478903b7f2238983406aa`
  had the qualified tree, sole parent exact M93 closeout, one commit, and 16
  intended paths.
- Ready PR #234 passed exact-head run `32581692977` in the unchanged three
  Linux-first allocations: Linux job `97051923558` in 5m32s, macOS job
  `97052612146` in 2m59s, and Windows job `97052612142` in 4m22s.
- Hosted Linux CPython 3.12 passed 2,742 tests. Linux 3.13/3.14 and macOS/
  Windows 3.14 each passed 2,742 with one established capability skip.
- Every OS passed ten real-wgpu tests, graphics profiling, Clockwork Arena,
  and Agent World Builder. Linux also passed format, Ruff, strict Pyright,
  strict docs, base profiling, installed-wheel smoke, ten-artifact staging,
  and complete release smoke.
- Hosted repeat builds reproduced a 276,592-byte pure wheel at SHA-256
  `6167497499b5e87fac82007b9db3f2e30912229e64e9ca518e6e5a8d19b6d04d`
  and a 1,404,176-byte source archive at SHA-256
  `57e87b11f0c5f6b16eb1c6351ca5770896a479e1585eccda268d01ca40f6cf36`.
- Two separated readiness audits retained exact head/tree/base, one DCO commit,
  16 paths, three successful checks, one exact-head run, `MERGEABLE/CLEAN`, and
  zero comments, reviews, review comments, or review threads. Their separator
  passed all 24 M94 plus five metadata-hygiene assertions.
- Guarded squash `7974b6fc110f995cac25f7d69d9c48b55013a764`
  retained the exact qualified tree, sole parent M93 closeout, standalone DCO,
  and a valid GitHub signature verified at `2026-08-22T15:39:19Z`. The feature
  branch is deleted locally/remotely and no postmerge workflow ran.

## Integration-record scope

- Change exactly `.project/CURRENT_TASK.md`, `.project/DECISIONS_PENDING.md`,
  `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md`.
- Record only factual hosted qualification, guarded squash integration, and
  the next closeout boundary.
- Add no public/runtime/test/workflow/build/dependency/version/credential,
  development-tool identity, native/WASM/bytecode, tag, release, publication,
  or release-authority surface.

## Remaining acceptance work

- Run the bounded integration-record source/docs/architecture/metadata,
  reproducible-build, wheel, staging, release, whitespace, history, and scope
  gates.
- Create one DCO-signed record commit, push the neutral branch, open a ready PR,
  and require only the existing documentation-qualified Linux allocation with
  the zero-step skipped desktop umbrella.
- Complete two separated exact-head audits, guarded squash integration, then
  publish the three-record no-workflow closeout PR and clean all M94 branches
  and generated targets.
