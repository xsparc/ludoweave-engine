# Current Task

- **Task:** M37 - fail-closed CI change qualification
- **Status:** In progress on `maintenance/m37-ci-change-qualification`.
- **Started:** 2026-08-08
- **Authority:** The standing maintainer instruction requires only necessary,
  vital hosted checks and authorizes subsequent fully validated milestone PRs.
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  commit `46ef98447706c94763a236841a38c2dbb5b444ca`. Only `main` existed locally
  and remotely, no pull request was open, and `git fsck --full --no-dangling`
  passed. M36 feature run `31232803658` passed exactly three allocations; its
  feature and zero-run record PRs are squash-integrated.
- **Outcome:** Use one existing Linux allocation to qualify pull-request
  changes, retain one bounded Linux gate for documentation-only work, preserve
  the complete three-allocation M36 gate for substantive work, and avoid two
  desktop allocations when Linux qualification or validation fails.
- **Acceptance gate:**
  - Load the classifier from the exact pull-request base revision rather than
    the candidate copy; first introduction and missing policy are substantive.
  - Admit only root Markdown, Markdown below `docs/` and `.project/`, issue
    forms, the pull-request template, and labels as documentation-only;
    `mkdocs.yml` and non-Markdown documentation inputs remain substantive.
  - Treat empty, mixed, ambiguous, invalid, undecodable, and unknown changes as
    substantive or fail the Linux job.
  - Keep lock, formatting/lint, strict docs, all architecture tests, universal
    build, isolated-wheel smoke, and release-candidate smoke in the one-
    allocation documentation gate.
  - Keep all eight M36 Python/platform/graphics/distribution slices in exactly
    three allocations for substantive changes.
  - Make Windows/macOS depend on successful Linux qualification and run only
    for `substantive=true`, while retaining desktop matrix isolation.
  - Preserve pull-request-only and `.project/**` exclusions, `contents: read`,
    exact pins, disabled checkout credentials, cache, timeouts, and cancellation.
  - Add strict classifier unit/integration tests, workflow architecture tests,
    RFC-0020, and aligned public/project documentation.
  - Hosted-prove three allocations on the substantive feature PR, then one
    Linux allocation and two successful conditional skips on the public
    documentation/status record PR.
- **Non-scope:** Removing a substantive validation slice; altering runtime or
  test behavior; dependencies, lock, package version, release workflow, tag,
  publication, branch protection, required-check settings, external evidence,
  provider admission, certification, support policy, or a deferred subsystem.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Baseline evidence:** The first sandboxed `uv lock --check` could not read
  the managed cache; the approved identical check resolved the unchanged 46-
  package lock. All 34 inherited M34-M36 workflow/release boundary tests pass
  in 1.41 seconds. The official GitHub direction scan records that conditionally
  skipped jobs report success, `needs` gates dependent jobs, and path-skipped
  workflows can leave required checks pending.
- **Current evidence:** The hardened classifier has 30 passing tests, including
  a real temporary Git repository, NUL-safe spaced path, fail-closed empty/
  mixed inputs, narrow allowlist, and invalid-revision option-injection
  regression. Review found and closed one valid bypass: `docs/**` plus
  `mkdocs.yml` could admit executable hooks, so only Markdown documentation is
  now admitted and documentation configuration is substantive. The exact no-
  graphics documentation lane passes lock/static/docs, 334 architecture tests,
  build, wheel, and release smoke. The final 3.12 suite passes 1,760 tests with
  nine skips; earlier complete 3.13/3.14 suites pass 1,745 with ten skips each,
  and the correction's 36 focused tests pass on both. Whole-tree static/docs,
  YAML, real-wgpu, profiles, both vertical slices, rebuilt wheel, and fresh
  release smoke pass. Hosted substantive and documentation-lane proof remain
  pending.
