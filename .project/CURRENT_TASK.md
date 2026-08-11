# Current Task

- **Task:** M66 - staged sample-root publication
- **Status:** Reviewed local candidate; final record-frozen validation remains
  before hosted qualification.
- **Started:** 2026-08-12
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized M65 closeout
  `0892f4b234be5ea06d6a91f3b1f0b50a1f44eb1f`, tree
  `a8e028df3db9b6eb0293cd9177cedcda3367666a`. Local `main`, `origin/main`,
  and `origin/HEAD` matched; only `main` existed locally and remotely.
- **Outcome:** Prevent a failed release-sample extraction from leaving a
  partial tree at the final versioned sample-root identity.
- **Acceptance:** Require an existing real caller-owned output directory and an
  absent final root, including dangling links; retain complete M64/M65 archive
  preflight; stream into an owned same-filesystem temporary staging directory;
  validate required files there; publish through one rename; clean the owned
  stage on every pre-publication failure; and preserve the original failure.
- **Boundary:** Private single-process release smoke only. No general archive
  sandbox, crash durability, `fsync`, journal, concurrent filesystem race
  isolation, post-publication rollback, cleanup of unowned paths, workflow,
  dependency, sample producer, runtime API, release authority, tag, release,
  publication, or real public release observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Failing baseline:** The new M66 file produced 8 failures, 2 passing guards,
  and 1 Windows symbolic-link capability skip in 0.36 seconds against exact M65
  production code. Stream-size and incomplete-bundle failures left partial
  final roots; existing roots were read into or raised host exceptions; a
  missing output parent was silently created; publish-failure injection was
  never reached; staged source structure and RFC-0049 were absent.
- **Local candidate evidence:** Whole-tree format/Ruff/strict-Pyright, 736
  architecture assertions, strict docs, and whitespace pass. CPython 3.12
  passes 2,266 tests with 15 skips; 3.13 and 3.14 each pass 2,266 with 16 skips.
  Ten real-wgpu tests, both five-repeat profiles, both vertical slices, and all
  four diagnostic benchmark validators pass. Final reviewed builds reproduce a
  pure 272,709-byte wheel and 1,183,308-byte source archive; installed-wheel,
  deterministic staging, and complete updated release smoke pass.
- **Review:** Findings-first review found that the first implementation rejected
  symbolic-link parents but not Windows directory junctions despite the real-
  directory contract. A tests-first junction simulation reproduced the gap and
  now passes. Mid-stream I/O cleanup and a late final-root collision were also
  added as lifecycle proofs. The review-strengthened file passes 13 assertions
  with 1 local symbolic-link capability skip; no further blocker or non-blocking
  finding remains.
- **Environment correction:** Two initial full-suite attempts were invalidated
  by a full system drive. After isolating pytest fixtures on the spacious `D:`
  drive, every supported-version suite passed. No behavioral pass is claimed
  from the two disk-exhausted attempts.
- **Hosted plan:** Because the change touches release-smoke Python, retain the
  existing substantive three-allocation Linux-first CI. Add no workflow or
  runner. Publish only after the record-frozen local gate; squash-integrate only
  after exact-head hosted success and delayed review audits.
