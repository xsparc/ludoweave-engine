# Current Task

- **Task:** M58 - public release transport-cleanup conformance
- **Status:** The feature is squash-integrated on `main`; preparing the
  four-file integration record on `docs/m58-integration-record`.
- **Started:** 2026-08-10
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized M57 closeout
  `26826822547d6d8df6ce1bfc05d8cf728a32d505`, with only `main` present and no
  open pull request, tag, release, or post-closeout `main` run.
- **Outcome:** Make public-release response/connection ownership cleanup
  ordered, complete, stable, and subordinate to any active primary failure.
- **Acceptance:** Every obtained response receives one close attempt before its
  created connection receives one close attempt. Both attempts occur when the
  first fails. Active failures remain primary. Cleanup-only ordinary failures
  use content-silent `public_release.request_failed`; cleanup control signals
  remain unwrapped. Redirect continuation and separate partial publication
  occur only after successful cleanup.
- **Boundary:** No rollback, retry, private response/socket state, raw parser,
  alternate client, workflow, allocation, dependency, package/runtime API,
  version, credential, release mutation, or release authority. Direct-target
  and partial bytes may remain after failure. Fixture and pull-request evidence
  are not a real public release observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Local evidence:** The clean M47-M57 baseline passed 243 assertions. Official
  Python 3.14 documentation confirms the public `HTTPConnection.close()` and
  stream close contracts. Against the unchanged verifier, all nine focused
  behavior/boundary assertions failed on early partial publication, raw or
  masking cleanup failures, a skipped connection attempt, redirect progress,
  and source ordering. The corrected implementation passes all ten focused
  behavior/boundary/documentation assertions with Ruff and strict Pyright
  clean; all 253 inherited M47-M58 assertions and strict docs pass. Whole-tree
  static/docs and 631 architecture assertions pass. Complete graphics-enabled
  CPython 3.12-3.14 suites each pass 2,171 tests with 14 expected skips. Ten
  real-wgpu tests, both five-repeat profiles, both vertical slices, and all
  documented M1-M4 benchmark validators pass. Findings-first review then found
  that first-error selection invoked attacker-defined exception truthiness; a
  reviewer-derived regression failed tests-first and now passes with explicit
  identity selection. All 11 focused M58, 254 inherited M47-M58, and 632
  architecture assertions pass on the correction with static/docs clean.
  Corrected complete graphics-enabled CPython 3.12-3.14 suites each pass 2,172
  tests with 14 expected skips. Corrected real-wgpu, both five-repeat profiles,
  both vertical slices, and all documented M1-M4 benchmark validators pass. A
  second reviewer-derived regression proved ambient `sys.exception()` could
  suppress cleanup failure inside a caller's unrelated exception handler; it
  failed tests-first and now passes with an explicit exchange-local failure
  flag. The final candidate passes all 12 focused M58, 255 inherited M47-M58,
  and 633 architecture assertions; whole-tree static/docs; graphics-enabled
  complete suites on CPython 3.12-3.14 with 2,173 passes and 14 expected skips
  each; ten real-wgpu tests; both five-repeat profiles; both vertical slices;
  and all documented M1-M4 benchmark validators. Two final-record builds
  reproduce the pure wheel and source distribution; isolated-wheel and
  complete release smoke pass. Findings-first scope, archive, credential,
  identity, history, and integrity review found no actionable M58 issue. Final
  record-inclusive lock/static/633-assertion/docs/integrity validation passes.
- **Hosted evidence:** PR #126 exact head
  `8bd11f0ab6575edee6a5e7b5c78e36af59e55088` passed run `31478254138` in
  exactly three Linux-first allocations. Linux job `93736984444` passed in
  7m48s before macOS `93738860983` and Windows `93738860996` began; they
  passed in 2m00s and 4m01s. Linux baseline and every compatibility suite
  passed 2,177 tests, with one expected skip outside the baseline. Every
  platform passed ten real-graphics tests, profile smoke, Clockwork Arena, and
  Agent World Builder. Hosted reproducibility, installed-wheel smoke, and
  complete release smoke passed.
- **Integration:** Two delayed audits found no issue comment, review comment,
  review, or thread. Head-pinned, GitHub-verified squash
  `17ea7354c80b9d140350b88cd0ae3e615f700e45` has the exact reviewed feature
  tree, sole parent M57 closeout, valid signature, and standalone DCO. The
  feature branch is deleted locally and remotely. Synchronized `main` has no
  post-merge run or non-main branch.
- **Current gate:** This exact four-file documentation/project record requires
  one Linux allocation; its desktop umbrella must skip with zero steps.
