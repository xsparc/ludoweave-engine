# Current Task

- **Task:** M28 - external sample-game adoption admission readiness
- **Status:** Ready PR #44 is `MERGEABLE` and `CLEAN`. Both the initial and
  corrected eight-job hosted runs passed. The two valid P2 review findings are
  corrected, their threads are outdated, and the final reread found no new
  finding. Factual CI-skipping evidence publication and exact squash
  integration remain.
- **Started:** 2026-08-07
- **Base:** Exact clean synchronized GitHub-verified `main` commit
  `17401eb32be30862496bbe02366d886a60752fb3` after PR #43 recorded M27
  integration without starting a workflow run.
- **Outcome:** Make the design plan's longer-term metric counting externally
  authored sample games mechanically auditable without treating bundled
  examples, maintainers, automated agents, CI, or synthetic fixtures as
  external authorship or adoption.
- **Acceptance gate:**
  - Add one strict reviewed manifest whose current sample-game record set is
    empty and whose exact 280 bytes and SHA-256 are pinned by architecture
    tests.
  - Require at least one independently authored, manually reviewed public 2D
    or layered-2D game before the result can become true.
  - Require a public repository, immutable Git revision, installed-wheel use,
    exact headless-fixed-tick, typed-command-receipt, and verified-replay
    capability evidence, plus a validated outcome.
  - Require distinct source, execution, and review SHA-256 identities and an
    explicitly reviewed public SPDX license.
  - Reject project-owned and maintainer-authored games, unreviewed authorship
    or licensing, unsafe locators, duplicate identities, and incomplete
    capabilities.
  - Preserve accepted history as an exact complete executable prefix and bind
    it to the reviewed whole-manifest digest.
  - Emit exact sanitized `not-ready` evidence for the current empty manifest;
    never expose author IDs, repositories, revisions, artifact hashes,
    evidence locations, licenses, local paths, platform facts, or timings.
  - Prove future gate mechanics synthetically while refusing to count those
    fixtures as authors, games, users, repositories, feedback, or adoption.
  - Exercise source, isolated-wheel, and release-sample paths, accept RFC-0011,
    and preserve the two existing workflows and eight essential CI jobs.
- **Non-scope:** Soliciting/contacting authors; discovery or remote repository
  lookup; opening or mutating issues/PRs as evidence; networking, telemetry,
  dynamic imports, subprocesses, installation, provider execution, private
  communication, or personal-data collection; changing runtime source, public
  APIs/exports, persistent formats, protocols, operations, dependencies, lock,
  version, workflows, CI topology, tags, releases, publication, certification,
  support policy, or stability labels.
- **SemVer:** No package or public-Python-surface change; version remains
  `0.1.0a1` and current stability labels are unchanged.
- **Baseline evidence:** M27 feature PR #42 and no-CI integration PR #43 are
  squash-integrated. Local M28 starts from exact verified `main` commit
  `17401eb32be30862496bbe02366d886a60752fb3`; `main`, `origin/main`, and
  `origin/HEAD` matched with a clean worktree and `git fsck --full
  --no-dangling` exited 0. The unchanged lock resolves 46 packages. The focused
  M25/M27/adoption-artifact baseline passed 94 tests with two Windows symlink-
  capability skips in 4.75 seconds. The first sandboxed lock check failed
  before project execution because the existing uv user cache was denied; the
  approved cache-access rerun passed in 0.83 ms.
- **Local acceptance evidence:** The post-review focused M28 suite passes 57
  tests with one Windows symlink-capability skip. The complete gate passes
  unchanged lock/sync, 239-file formatting, Ruff, strict Pyright, strict docs,
  1,265 tests with five Windows symlink-capability skips, a pure build,
  isolated wheel/release smoke, all retained benchmark/profile validators, ten
  real-wgpu tests, and both graphics vertical slices. The final scope audit
  confirms unchanged runtime source, workflows, metadata, lock, version, and
  public exports; a 94-entry wheel with no native file; and a 36-entry sample
  bundle containing both exact M28 evidence files. M1 simulation and both M3
  timing targets remain observed misses and authorize no acceleration.
- **Hosted/review evidence:** Ready PR #44 targets exact base
  `17401eb32be30862496bbe02366d886a60752fb3`. Run `31175906134` passed all
  eight unchanged essential jobs on DCO-signed implementation head
  `a1898a81218ae5674fd0347018c6062a5537f359`. Automated review then correctly
  identified that unreviewed manifests still exposed candidate counts and that
  HTTPS evidence locators were not bound to immutable identities. The local
  correction exposes record aggregates only after exact digest and complete-
  history admission and requires the locator path to contain the record's
  revision or one recorded artifact digest.
- **Corrected hosted acceptance:** Run `31176729893` passed all eight unchanged
  essential jobs on correction head
  `36130c8a3d0923a7330ee2c9e287c11c2a52594c`. GitHub reports PR #44
  `MERGEABLE` and `CLEAN` against the exact assigned base. Both original review
  threads are outdated; no new review or actionable finding exists.
