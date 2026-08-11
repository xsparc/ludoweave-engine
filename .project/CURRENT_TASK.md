# Current Task

- **Task:** M67 - exact sample-bundle inventory conformance
- **Status:** Full local candidate validation, findings-first review, and the
  record-frozen source gate pass. The feature is ready for a DCO commit and
  exact-head hosted qualification.
- **Started:** 2026-08-12
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Branch:** `release/m67-exact-sample-inventory`.
- **Base:** Exact synchronized M66 closeout
  `995fdda097a418a7a0e570bb6b492d3f5609d471`, tree
  `54da91c867211007156d5006512a426815a8374b`. Only `main` existed locally
  and remotely, and no pull request was open before branching.
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
- **Hosted policy:** The implementation changes release verification and must
  receive the existing substantive Linux-first three-allocation qualification.
  No workflow edit or additional allocation is authorized.
- **Integration gate:** After exact-head hosted qualification and review,
  change only `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`,
  `.project/TEST_EVIDENCE.md`, and `ROADMAP.md`; request only the existing
  documentation-qualified Linux allocation and zero-step skipped desktop
  umbrella; then create a three-record closeout with no hosted runner.
