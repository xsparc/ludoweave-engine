# Current Task

- **Task:** M67 - exact sample-bundle inventory conformance
- **Status:** Feature PR #153 and integration-record PR #154 are fully
  validated, reviewed, squash-integrated, and verified. This exact three-record
  closeout establishes the clean M68 selection base without requesting hosted
  CI.
- **Started:** 2026-08-12
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** GitHub-verified integration squash
  `5025877d31a2bc8a9a0a1b7bb2e106869f76066f`, whose tree
  `eb532eddbd368efaaa1a896efd930727cc5b3059` exactly matches reviewed PR
  #154 head `565053e8cf0f3961f8bfbc1a54df04a604240183`. Its sole parent is the
  M67 feature squash `bc8a3d9a24bab5860e48af919dbeab4ca4c913f2`; GitHub reports a valid
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
  Pyright, 747 reviewed architecture assertions with 1 local capability skip,
  2 release-artifact tests, strict docs, and whitespace. CPython 3.12 passes 2,286 tests
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
- **Integration hosted evidence:** Exact four-file head `565053e` passed run
  `31536520514` in one 41-second Linux allocation; the desktop umbrella skipped
  with zero steps. Hosted formatting, Ruff, strict docs, 748 documentation-
  selected architecture assertions, reproducibility, installed-wheel smoke,
  staging, and complete release smoke passed.
- **Integration review resolution:** One delayed review incorrectly claimed the
  sole integration commit lacked DCO. GitHub's commit endpoint and local
  `git interpret-trailers --parse` each returned the exact authorized trailer.
  Evidence reply `3765169173` was posted, thread
  `PRRT_kwDOTtqoGs6YYOGq` resolved, and two post-resolution audits found no
  later activity.
- **Closeout gate:** Change exactly `.project/CURRENT_TASK.md`,
  `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md`; run architecture,
  strict docs, scope, Git-object, and whitespace checks; create a DCO-signed
  ready PR that requests no hosted runner; verify its squash; delete every M67
  branch locally/remotely; remove only verified generated outputs; and leave
  synchronized clean `main` before selecting M68.
- **Closeout local evidence:** The exact three-file record passes all 747
  architecture assertions with 1 local capability skip, strict docs,
  whitespace, full Git-object checking, and exact scope. It changes no
  workflow, runtime, verifier, producer, dependency, package, test, public-doc,
  or roadmap surface and is excluded from CI by the existing path policy.
