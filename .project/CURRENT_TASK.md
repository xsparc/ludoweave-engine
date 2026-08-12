# Current Task

- **Task:** M67 - exact sample-bundle inventory conformance
- **Status:** Feature PR #153 is fully validated, reviewed, squash-integrated,
  and verified. The exact four-file integration record is in progress.
- **Started:** 2026-08-12
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Branch:** `docs/m67-integration-record`.
- **Base:** GitHub-verified feature squash
  `bc8a3d9a24bab5860e48af919dbeab4ca4c913f2`, whose tree
  `cd8833bbd93e11c7e7e678ee324711503a921d97` exactly matches reviewed PR
  #153 head `3cb44d412d71a930f84a1545e59f893643d68666`. Its sole parent is exact M66
  closeout `995fdda097a418a7a0e570bb6b492d3f5609d471`; GitHub reports a valid
  signature and exact parsed DCO trailer.
- **Outcome:** Reject any unexpected or missing file in the project-produced
  sample ZIP before extraction or publication.
- **Acceptance:** Define the independent exact 50-file relative inventory;
  collect identities only after the complete M64/M65 metadata/path preflight;
  reject either set mismatch with one stable content-silent category before
  member reads or staging; preserve archive-order independence and M64-M66
  behavior; and prove that the unchanged producer emits the expected set.
- **Boundary:** Private release smoke only. No content scanning, malware
  detection, file-format validation, general archive sandbox, workflow,
  dependency, version, sample-producer, runtime API, release authority, tag,
  release, publication, or real public release observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Research:** Focused primary-source review of Python `zipfile`, OWASP upload
  validation, and SLSA 1.2 expectation verification supports exact fail-closed
  source-defined inventory validation. This is advisory design evidence, not a
  claim of SLSA compliance or general archive safety.
- **Failing baseline:** The new M67 file produced 5 failures and 3 passing
  guards in 0.33 seconds against exact M66 production code. The verifier had no
  exact inventory expectation; both an extra portable member and a missing
  nested receipt asset reached member reads; source ordering and RFC-0050 were
  absent. The producer-inventory, exact-valid-bundle, and protected-surface
  guards passed.
- **Local candidate:** The unchanged lock and restored 45-package CPython 3.12
  graphics environment pass whole-tree formatting for 310 files, Ruff, strict
  Pyright, 747 reviewed architecture assertions with 1 local capability skip, 2 release-
  artifact tests, strict docs, and whitespace. CPython 3.12 passes 2,286 tests
  with 15 skips; 3.13 and 3.14 each pass 2,276 with 16 skips. Ten real-wgpu
  tests, both five-repeat profiles, both vertical slices, and all four
  diagnostic benchmark validators pass. Two builds reproduce a pure 272,880-
  byte wheel and 1,190,493-byte source archive; installed-wheel, deterministic
  staging, and complete M67 release smoke pass.
- **Review:** Findings-first review found a test-strength gap: separate 49- and
  51-member fixtures could be satisfied by a count-only check. A 50-member
  one-for-one substitution and direct no-staging proof now pass. The correction
  changes tests only; the strengthened M64-M67 contract passes 58 assertions
  with 1 capability skip. No blocking or non-blocking finding remains.
- **Environment:** Full-suite temporary repositories used disposable
  `D:\LudoWeaveValidation\m67` paths to avoid the known low-space system drive;
  the locked CPython 3.12 graphics environment was restored afterward.
- **Hosted evidence:** Run `31534773135` passed exact head `3cb44d4` in the
  unchanged three Linux-first allocations: Linux in 7m44s, macOS in 3m22s, and
  Windows in 4m15s. Baseline and every compatibility suite passed 2,292 tests,
  with one compatibility skip; real-wgpu, profiles, vertical slices,
  reproducibility, installed-wheel smoke, staging, and complete M67 release
  smoke passed.
- **Hosted review:** Two delayed exact-head audits found no review, comment, or
  unresolved thread. PR #153 remained clean, mergeable, exact-head, and exact-
  base before squash integration.
- **Integration gate:** Change exactly `.project/CURRENT_TASK.md`,
  `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md`;
  request only the existing documentation-qualified Linux allocation and a
  skipped zero-step desktop umbrella; then create a three-record closeout that
  requests no hosted runner.
- **Integration local evidence:** The exact four-file record passes the
  unchanged lock, formatting for 310 files, Ruff, strict Pyright, all 747
  architecture assertions with 1 local capability skip, 2 release-artifact
  tests, strict docs, whitespace, full Git-object checking, two-build
  reproducibility, installed-wheel smoke, 10-artifact staging, and complete M67
  release smoke.
