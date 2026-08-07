# Current Task

- **Task:** M31 - issue-response and pull-request-review latency admission readiness
- **Status:** In progress on `evidence/m31-response-review-latency` from exact
  clean synchronized verified `main` commit
  `22dc58df8b0c4d17c3619d83e37c6d0ee6184441`.
- **Started:** 2026-08-08
- **Base:** PR #48 squash-integrated the exact validated M30 feature tree as
  verified `675713d15a20a38233b80580e5aa773dc7a8684c`; documentation-only PR
  #49 squash-integrated the factual M30 state record as verified
  `22dc58df8b0c4d17c3619d83e37c6d0ee6184441`. Local `main`, `origin/main`,
  and `origin/HEAD` matched that commit with a clean worktree before branching.
- **Outcome:** Make the design plan's next longer-term metric—issue-response
  and pull-request-review time—mechanically reportable from a complete reviewed
  public cohort without querying GitHub, collecting telemetry or identities,
  selecting only completed actions, or fabricating an SLA.
- **Acceptance gate:**
  - Add one strict reviewed manifest whose current measurement-window set is
    empty and whose exact bytes and SHA-256 are pinned by architecture tests.
  - Require bounded chronological non-overlapping opening windows plus a later
    observation cutoff and complete reviewed public cohort.
  - Require every eligible external-human issue and pull request to remain in
    the cohort as either observed or pending.
  - Require observed actions to identify the first qualifying public human-
    maintainer response/review by a distinct participant with exact public
    resource/action locations and UTC timestamp/latency agreement.
  - Require census and review artifacts at the same immutable project revision,
    distinct evidence hashes, and reviewed eligibility, action state,
    provenance, validation, maintainer status, and participant distinctness.
  - Preserve accepted windows as an exact complete executable prefix and bind
    it to the reviewed whole-manifest digest.
  - Expose only aggregate eligible/observed/pending counts and deterministic
    median/nearest-rank-p95 seconds after exact digest/history admission.
  - Require at least one observed issue response and PR review for a reportable
    metric while defining no target, quality verdict, release gate, SLA, or
    support promise.
  - Emit exact sanitized `not-ready` evidence for the current empty manifest;
    never expose resource/action locations, identities, per-record hashes,
    timestamps, local paths, host facts, raw evidence, or private data.
  - Exercise source, isolated-wheel, and release-sample paths, accept RFC-0014,
    and preserve both workflows and all eight essential CI jobs exactly.
- **Non-scope:** GitHub discovery or remote lookup; issue/PR/contact mutation;
  telemetry; usernames, email addresses, private correspondence or logs;
  automatic role/identity inference; runtime source; public APIs/exports;
  persistent formats; protocols; operations; dependencies; lock; version;
  workflows; CI topology; tags; releases; publication; certification; stability
  promotion; service levels; or support policy.
- **SemVer:** No package or public-Python-surface change; version remains
  `0.1.0a1` and current stability labels are unchanged.
- **Baseline evidence:** Exact `HEAD`, `main`, `origin/main`, and `origin/HEAD`
  resolved to `22dc58df8b0c4d17c3619d83e37c6d0ee6184441`; the worktree was clean and
  `git fsck --full --no-dangling` exited 0. The first sandboxed uv attempt could
  not access its user cache and produced no test result. The corrected host-
  cache run resolved the unchanged 46-package lock in 0.69 ms and passed 59
  M30/artifact/workflow tests with one Windows symlink-capability skip in 2.08
  seconds. CI and release workflow SHA-256 values remain
  `06a5e07918c83fc8de61e6746cb344f865b6421d81f554d79f4455d3718a3b21` and
  `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`.
- **Current local evidence:** The exact 199-byte empty manifest has SHA-256
  `bc40bbcc1636229fa2c78aed5f71854d1221fd3c0d33169edc1321dd07e69d4f`.
  The evaluator emits deterministic path-free `not-ready` evidence with zero
  windows and measurements. Its corrected focused gate passes 49 adversarial
  tests with one Windows symlink-capability skip, and the evaluator/artifact
  group passes 51 tests with the same skip. The corrected architecture/
  evaluator/artifact gate passes 62 tests with one skip and strict docs. The
  final complete gate passes the unchanged lock/sync, 251-file formatting,
  Ruff, strict Pyright, strict docs, 1,435 tests with eight skips, pure build,
  isolated wheel/release smoke, ten real-wgpu tests, and both graphics vertical
  slices. The unchanged 94-entry wheel has no native/WASM file and the 42-entry
  sample bundle contains both exact M31 evidence files. Protected runtime/
  workflow/metadata/lock scope is unchanged. Findings-first local review found
  no issue. Ready PR #50's initial exact head passed all eight hosted jobs, but
  the hosted review correctly found that the evaluator admitted an observation
  cutoff equal to the opening-window close. Admission now requires a strictly
  later cutoff, equality has a regression, and the post-review gate passes 60
  focused tests with one skip, formatting, Ruff, strict Pyright, strict docs,
  1,435 complete-suite tests with eight skips, pure build, installed-wheel
  smoke, and fresh ten-artifact release smoke. No benchmark was run because M31
  changes no runtime or performance path and defines no timing target.
  Correction publication, hosted validation of the corrected exact head,
  final review reread, integration, and cleanup remain pending.
