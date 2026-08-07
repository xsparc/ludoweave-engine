# Current Task

- **Task:** M27 - external-contributor rehearsal admission readiness
- **Status:** In progress on
  `codex/m27-external-contributor-rehearsal-readiness`; implementation,
  artifact wiring, public documentation, complete local validation,
  findings-first diff review, DCO commits, ready PR, and hosted validation are
  complete. Final thread-aware reread and integration remain.
- **Started:** 2026-08-07
- **Base:** Exact clean synchronized GitHub-verified `main` commit
  `c1c3be08f7f75d90e7d1b517adbc30d56902ece4` after PR #41 recorded M26
  integration without starting a workflow run.
- **Outcome:** Make the design-plan objective “documentation enables a first
  external contribution without private maintainer knowledge” mechanically
  auditable without treating project-owned documentation, CI, synthetic
  fixtures, maintainers, or automated agents as external human evidence.
- **Acceptance gate:**
  - Add one strict reviewed manifest whose current rehearsal-record set is
    empty and whose exact 270 bytes and SHA-256 are pinned by architecture
    tests.
  - Require at least one independently reviewed human, merged good-first
    project contribution linked to a public issue and pull request before the
    result can become true.
  - Require exact distinct base/head/merge Git objects, reviewed patch and
    feedback SHA-256 identities, valid DCO, clean/focused/complete validation,
    merged outcome, and no private maintainer knowledge.
  - Limit admissible scope to bug fixes, documentation, tests, or tooling and
    reject public-API, persistent-format, dependency, or workflow changes.
  - Preserve accepted history as an exact complete executable prefix and bind
    it to the reviewed whole-manifest digest.
  - Emit exact sanitized `not-ready` evidence for the current empty manifest;
    never expose contributor login, URLs, revisions, or artifact hashes in the
    report.
  - Prove future gate mechanics synthetically while explicitly refusing to
    count those regressions as contributors, issues, pull requests, feedback,
    or usability evidence.
  - Exercise source, isolated-wheel, and release-sample paths, accept RFC-0010,
    and preserve the two existing workflows and eight essential CI jobs.
- **Non-scope:** Soliciting/contacting contributors; opening or mutating issues
  or pull requests as evidence; network/telemetry/discovery/dynamic-import/
  subprocess/provider execution; collecting email or private communication;
  changing runtime source, public APIs/exports, persistent formats, protocols,
  operations, dependencies, lock, package version, stability metadata,
  workflows, CI topology, tags, releases, publication, or support policy.
- **SemVer:** No package or public-Python-surface change; version remains
  `0.1.0a1` and current stability labels are unchanged.
- **Baseline evidence:** M26 feature PR #40 and no-CI state PR #41 are
  squash-integrated. Local M27 starts from exact verified `main` commit
  `c1c3be08f7f75d90e7d1b517adbc30d56902ece4`. The unchanged lock resolves
  46 packages. The prior release/M25/M26 baseline passed 64 tests with two
  Windows symlink-capability skips in 3.73 seconds. The reviewed rehearsal
  manifest is exactly 270 bytes with SHA-256
  `ecb959e90a0033b4dbe3dcfe8a48db1c1eea915e0ef2840510969b9e25cdb9c7`.
  The initial focused M27 evaluator/boundary suite passed 51 tests with one
  Windows symlink-capability skip in 1.74 seconds; artifact wiring then passed
  53 tests with one skip in 2.02 seconds, and Pyright reported zero diagnostics.
  Findings-first review closed cross-role revision/artifact reuse and duplicate-
  JSON-field ambiguity; the corrected focused suite passes 59 tests with one
  skip. The complete local gate passes 235-file formatting, Ruff, strict
  Pyright, strict docs, 1,210 tests with four Windows symlink-capability skips,
  pure build, isolated wheel/release smoke, retained benchmark/profile
  validators, ten real-wgpu tests, and both graphics vertical slices. Initial
  hosted run `31118834216` exposed one case-sensitive test-path defect on both
  Ubuntu compatibility jobs: the tracked lowercase pull-request template was
  referenced with uppercase spelling. The local correction uses the exact
  tracked path. Windows graphics separately failed during GitHub action-
  download setup before checkout; the already-failed run was cancelled to
  avoid spending its remaining queued jobs. Corrected run `31119640551`
  initially encountered GitHub's resolved Actions outage during action
  downloads. Its single failed-job-only rerun preserved three successful jobs,
  reran only the five affected jobs, and completed with all eight effective
  jobs successful on exact head
  `f9e779d83a82795ad68cff22c424b6e94ef13703`.
