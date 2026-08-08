# Current Task

- **Task:** M35 - third-party conformance-adoption admission readiness
- **Status:** In progress on `evidence/m35-third-party-conformance`.
- **Started:** 2026-08-08
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  commit `277de9052e768a5f70d32f1a2f67ec9f93353723`. Only `main` existed locally
  and remotely, no pull request was open, `git fsck --full --no-dangling`
  passed, and the latest valid hosted run was M34 pull-request run
  `31229138742`, whose eight essential jobs passed.
- **Outcome:** Make the design plan's final ordered longer-term metric—the
  number of independently authored third-party adapters or plugin-backed
  adapters passing conformance—mechanically reportable from a complete
  reviewed project-accepted submission census without discovering, importing,
  installing, or executing providers and without fabricating adoption.
- **Acceptance gate:**
  - Add one strict reviewed manifest that explicitly asserts complete
    project-accepted submission-census review, is empty today, and pins exact
    bytes and SHA-256.
  - Admit only distinct independent external implementation identities that
    are neither project-owned nor maintainer-authored.
  - Accept only the exact installed M17 render-device, M18 agent-tool, and M19
    WorldStore protocols/profiles and fixed reference check counts.
  - Require a reviewed compatible M12 `render.device` manifest plus a passing
    render-device profile for plugin-backed evidence; compatibility alone
    never counts.
  - Bind public installed wheels, immutable repository revisions, reports,
    reviews, license, supported CPython/platform, and complete human review.
  - Preserve passed, failed, and not-executed accepted submissions plus the
    complete mandatory history prefix; count only passed implementations.
  - Emit only deterministic sanitized aggregates and keep the current result
    `not-ready` with zero passing implementations.
  - Exercise source, isolated-wheel, and release-sample paths and accept
    RFC-0018 without changing runtime, public API, conformance profiles,
    dependencies, lock, version, or CI topology.
- **Non-scope:** Global package discovery or ecosystem census; provider import,
  installation, execution, sandboxing, networking, or telemetry; new adapters,
  plugin capabilities, conformance protocols/profiles, runtime/API/format
  changes, dependencies/lock/version, workflow jobs, release/publication,
  certification/support claims, Rust, PyO3, WASM, editor, physics, or 3D work.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1` and
  stability labels remain unchanged.
- **Baseline evidence:** Repository/history/branch audit was clean at the exact
  base. GitHub reported no open pull request and no branch protection. The
  latest M34 hosted pull-request run passed all eight existing jobs. The
  unchanged lock contains 46 packages, and 154 inherited conformance/plugin/
  release tests passed in 3.54 seconds.
- **Current evidence:** The exact empty 250-byte manifest has SHA-256
  `adee8c68b5d89923ee2682162eb24cd9542a4601b1ff6fb901709ebcc0066767`.
  The first evaluator gate passed formatting and Ruff, while strict Pyright
  found four redundant test casts and 73 of 74 tests passed because one direct
  evaluator assertion expected JSON's list rather than the evaluator's tuple.
  After focused test-only corrections, formatting, Ruff, and strict Pyright
  passed and all 74 evaluator tests passed in 2.21 seconds. Findings-first
  review then rejected reserved non-public domains and non-wheel paths from
  public-wheel evidence. The final focused gate passes 160 tests; the complete
  suite passes 1,716 tests with nine skips; all static/docs, universal build,
  isolated wheel/release, real-wgpu/profile, vertical-slice, scope, archive,
  credential-pattern, neutral-identity, and Git-object checks pass. Initial
  hosted run `31231040437` passed all eight jobs, but automated review found an
  identifier-grammar mismatch with the installed runners. The exact grammar
  correction now passes 100 focused tests and the complete 1,718-test suite,
  plus static/docs, real-wgpu, rebuilt wheel, isolated-wheel, and fresh release
  smoke. Corrected hosted validation remains pending.
