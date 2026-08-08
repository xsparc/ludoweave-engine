# Current Task

- **Task:** M34 - agent-tool recovery-rate admission readiness and CI quota hardening
- **Status:** Complete. The corrected implementation passed the full local and
  hosted gates, its review thread is resolved, and PR #56 is squash-integrated.
- **Started:** 2026-08-08
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  commit `d12c30a02782c0ebf892e27c5daf6e9fec1c93ee`. Only `main` existed locally
  and remotely, no pull request was open, `git fsck --full --no-dangling`
  passed, and the post-M33 main CI run `31226750474` passed all eight jobs.
- **Outcome:** Make the design plan's next ordered longer-term metric—the
  percentage of agent tool calls that complete without manual recovery—
  mechanically reportable from a complete reviewed task-directed call cohort
  without runtime instrumentation, private telemetry, provider queries, or a
  fabricated result. Preserve the necessary eight-job hosted gate while
  removing redundant post-merge and record-only runs.
- **Acceptance gate:**
  - Add one strict reviewed manifest whose current evaluation-window set is
    empty and whose exact 195 bytes and SHA-256 are pinned.
  - Admit only dispatched calls to the exact 12 product tool names under
    `ludoweave.agent.service/1` in complete reviewed task-directed sessions.
  - Fix eligibility before outcomes; exclude synthetic fixtures, conformance,
    benchmark/CI contract exercises, maintainer-driven calls, and unreviewed or
    private sessions.
  - Bind immutable service-contract, call, terminal-result, and manual-recovery
    evidence while requiring explicit privacy/consent review and excluding raw
    session content from aggregate output.
  - Preserve `completed-without-manual-recovery`,
    `completed-after-manual-recovery`, `not-completed`, and
    `terminal-unobserved`; known failures remain in the denominator and an
    unobserved terminal state blocks rate publication.
  - Require complete sequential per-session call indices, canonical order,
    reviewed eligibility/task context/manual recovery/outcome/provenance/
    validation, and complete accepted history.
  - Emit only sanitized aggregate evidence and an exact integer
    numerator/denominator rate after complete admission; define no success
    target, verdict, guarantee, release gate, certification, SLA, or support
    promise.
  - Exercise source, isolated-wheel, and release-sample paths and accept
    RFC-0017 without changing runtime, public API, protocol, dependency, lock,
    version, or release workflow surfaces.
  - Keep the existing eight substantive CI jobs, trigger them only for pull
    requests with changes outside `.project/**`, and remove the redundant
    `push: main` run.
- **Non-scope:** Runtime logging or telemetry; provider/session discovery;
  prompts, private correspondence, usernames, credentials, world content,
  environment/path collection; new tools/protocols; runtime/API/format changes;
  dependencies/lock/version; job removal; releases/publication; reliability or
  support claims; Rust, PyO3, WASM, networking, editor, physics, or 3D work.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1` and
  stability labels remain unchanged.
- **Baseline evidence:** Repository/history/branch audit was clean at the exact
  base. GitHub reported no open pull request and no branch protection. The
  latest main run completed successfully across the eight existing jobs. A
  focused inherited agent-service/conformance/M33 boundary baseline passed 47
  tests. The first sandboxed uv command could not access the user cache; the
  same command ran successfully with the existing managed cache outside the
  sandbox.
- **Current evidence:** The exact empty manifest has SHA-256
  `e952c045b039055e8439069cf88176b6ac1d2ad7de49a94d39b2737e5d06e1d5`.
  Its evaluator emits deterministic path-free `not-ready` evidence with zero
  windows/calls and no rate. Findings-first review added explicit per-window and
  per-call privacy/consent admission and found no remaining issue. The complete
  suite passes 1,625 tests with nine skips; all static/docs gates, universal
  build, isolated wheel/release smoke, ten real-wgpu tests, graphics profile,
  both vertical slices, and final scope/security/artifact audits pass. Initial
  hosted run `31228373123` exposed one POSIX traceback disclosure and delayed
  review found one excessive-nesting exception escape. Both have focused
  regressions and pass the corrected complete local gate. Corrected hosted run
  `31229138742` passed all eight jobs on exact head `600f71a416f0df46af68e63d28a2711893ec4675`;
  the sole thread is resolved. PR #56 squash-integrated the exact tree as
  GitHub-verified `a0d80851821b569156979d8d2ae0e473cea768f9` with sole parent
  exact M34 base. The feature branch is deleted locally and remotely, and the
  PR-only workflow created no redundant post-merge `main` run.
