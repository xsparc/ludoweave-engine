# Current Task

- **Task:** M64 - bounded sample-bundle extraction closeout
- **Status:** Feature and integration-record PRs are fully validated,
  squash-integrated, and reviewed. This exact three-record closeout will
  establish the clean M65 selection base without requesting hosted CI.
- **Started:** 2026-08-12
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** GitHub-verified integration squash
  `6f3c0352420d39f9c4666101f7de3c23a52ac2d2`, whose tree
  `7fec531dd168a8ae96a074177d72c9589975264c` exactly matches reviewed PR #145
  head `49857245d37aaf8ea1b8a0cf702897a17b3f79ab` and whose sole parent is M64
  feature squash `8399e0f94838f455ead604eceee0a17e1b2c9a91`. GitHub reports a valid
  signature and exact parsed DCO trailer.
- **Outcome:** M64 bounds staged sample-ZIP expansion and memory use before the
  installed-candidate release smoke extracts any member.
- **Implemented contract:** Complete preflight admits at most 256 members,
  1 MiB declared uncompressed per member, and 8 MiB declared uncompressed
  total; path, symbolic-link, codec, count, and size checks precede writes;
  stored/deflated members stream in 64 KiB blocks and must exactly match their
  declared size; BZIP2, LZMA, and unknown methods fail closed.
- **Boundary:** Private release-smoke limits only. No general archive sandbox,
  cleanup or rollback guarantee, workflow, dependency, runtime API, release
  authority, tag, release, publication, or real public release observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Feature evidence:** Corrected PR #144 head
  `8b6861df891f12d194bc9b7e98b41ac8ab81f7d1` passed exactly three Linux-first
  allocations in run `31515782370`, including all supported Python, real-wgpu,
  profiles, vertical slices, reproducible builds, installed-wheel smoke, and
  complete release smoke. Its sole review thread was answered and resolved;
  two delayed audits found no later activity. Squash `8399e0f` has the exact
  reviewed tree and sole parent exact M63 closeout.
- **Integration evidence:** Four-document PR #145 exact head
  `49857245d37aaf8ea1b8a0cf702897a17b3f79ab` passed run `31517725574` in one
  42-second Linux allocation; the desktop umbrella skipped with zero steps.
  Hosted formatting, Ruff, strict docs, all 702 architecture assertions,
  reproducible distribution, installed-wheel smoke, and complete release smoke
  passed. Two delayed audits were empty. Squash `6f3c035` has the exact reviewed
  tree, valid signature, sole parent the feature squash, and parsed DCO.
- **Closeout gate:** Change exactly `.project/CURRENT_TASK.md`,
  `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md`; run architecture
  and whitespace checks; create a DCO-signed ready PR; request no hosted runner;
  verify the squash; delete every merged milestone branch locally/remotely; and
  leave only synchronized `main` before selecting M65.
