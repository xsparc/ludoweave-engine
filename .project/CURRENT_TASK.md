# Current Task

- **Task:** M64 - bounded sample-bundle extraction integration record
- **Status:** Feature PR #144 is squash-integrated from its corrected,
  fully-qualified head. The exact four-document integration record passes its
  complete local gate and is ready for one necessary Linux documentation and
  distribution allocation.
- **Started:** 2026-08-12
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** GitHub-verified feature squash
  `8399e0f94838f455ead604eceee0a17e1b2c9a91`, whose tree
  `3f46ec8c23a044a20823a7d9132906cc2efdb3fa` exactly matches corrected PR #144
  head `8b6861df891f12d194bc9b7e98b41ac8ab81f7d1` and whose sole parent is exact
  M63 closeout `a92330c5d592eaeba69e75e25dd94d83b22d367f`. GitHub reports a valid
  signature. The merged feature branch is absent remotely.
- **Outcome:** Bound staged sample-ZIP expansion and memory use before the
  installed-candidate release smoke extracts any member.
- **Acceptance:** Preflight no more than 256 members, 1 MiB declared
  uncompressed per member, and 8 MiB declared uncompressed total before the
  first filesystem write; retain path and symbolic-link validation; admit only
  stored/deflated members; stream in 64 KiB blocks; and require copied size to
  match metadata.
- **Boundary:** Private release-smoke limits only. No general archive sandbox,
  authentication claim, duplicate/case/Unicode filename policy, cleanup or
  rollback guarantee, workflow, runner allocation, dependency, lock, version,
  runtime package/API, release authority, tag, release, publication, or real
  public release observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Local evidence:** The final corrected candidate is format/Ruff/strict-
  Pyright clean; all 13 focused M64 assertions and 704 inherited architecture
  and release-artifact assertions pass. Every supported graphics-enabled
  CPython suite passes 2,242 tests with 14 expected skips; real-wgpu, profiles,
  both vertical slices, and all four diagnostic benchmark validators pass.
  Two builds reproduce a 272,239-byte wheel and 1,163,429-byte source archive;
  isolated-wheel and complete bounded release smoke pass.
- **Hosted evidence:** Corrected exact head
  `8b6861df891f12d194bc9b7e98b41ac8ab81f7d1` passed run `31515782370` in
  exactly three Linux-first allocations. Linux `93860439338` passed in 7m13s;
  macOS `93862476671` passed in 2m55s; Windows `93862476577` passed in 4m06s.
  Baseline passed 2,246 tests; Ubuntu and desktop compatibility suites each
  passed 2,246 with one expected skip. Real-wgpu, profiles, vertical slices,
  reproducible builds, installed-wheel smoke, and complete release smoke all
  passed. Hosted artifacts were a 272,227-byte wheel at
  `4eb1cb0b2524f188056c619c7e5757b41c739ff3d889f49982c026dba7a60a3b` and
  a 1,163,806-byte source archive at
  `718d719b0c0c40cf1af93aa5e5aa398fbfbdd5439de1067003deb6dba40c69b2`.
- **Review:** The initial hosted head was not merged after review exposed
  unbounded-output BZIP2/LZMA decompression beneath `ZipExtFile.read()`. The
  corrected head rejects those codecs before writes; stored/deflated admission
  and fail-before-write regressions pass. The review thread was answered and
  resolved, and two delayed exact-head audits found no later activity.
- **Integration gate:** Change exactly `.project/CURRENT_TASK.md`,
  `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md`;
  run record-focused local static, architecture, docs, distribution, installed-
  wheel, and complete release smoke; request one Linux allocation; then use a
  three-record closeout with no hosted allocation. The local gate is green:
  lock, 307-file formatting, Ruff, strict Pyright, 702 architecture assertions,
  strict docs, reproducible artifacts, installed-wheel smoke, complete release
  smoke, and whitespace all pass.
