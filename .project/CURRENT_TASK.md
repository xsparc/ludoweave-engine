# Current Task

- **Task:** M36 - CI runner consolidation without validation-slice loss
- **Status:** In progress on `maintenance/m36-ci-runner-consolidation`.
- **Started:** 2026-08-08
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  commit `ba9125389ab2b2b760ca7115b5b1b03c447f4190`. Only `main` existed locally
  and remotely, no pull request was open, and `git fsck --full --no-dangling`
  passed. M35 feature run `31231410432` passed all eight allocations; its
  feature and zero-run record PRs are squash-integrated.
- **Outcome:** Reduce per-pull-request runner allocations and repeated setup
  from eight to three while preserving every existing validation slice and all
  security, trigger, version, platform, graphics, and distribution boundaries.
- **Acceptance gate:**
  - Allocate exactly one Ubuntu runner and a two-entry Windows/macOS desktop
    matrix: three hosted allocations total instead of eight.
  - Preserve Ubuntu CPython 3.12 quality, non-provider tests, docs, base profile,
    build, isolated-wheel smoke, and release smoke.
  - Preserve full compatibility tests on Ubuntu 3.13/3.14 and Windows/macOS
    3.14 using explicit managed-Python environment transitions.
  - Preserve real-graphics tests, graphics profile, Clockwork Arena, and Agent
    World Builder on CPython 3.12 across Ubuntu, Windows, and macOS.
  - Retain pull-request-only and `.project/**` exclusions, `contents: read`,
    exact action/uv pins, disabled checkout credentials, cache, timeouts,
    desktop fail-fast isolation, and superseded-run cancellation.
  - Add architecture tests proving allocation count, every retained slice,
    security/trigger invariants, and unchanged runtime/release surfaces.
  - Accept RFC-0019 and align the smallest authoritative maintenance docs.
- **Non-scope:** Removing or weakening a validation slice; changing test
  behavior; runtime/API/protocol/format changes; dependencies, lock, package
  version, release workflow, tag/publication, provider admission, support
  policy, or any deferred engine subsystem.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Baseline evidence:** The current workflow expands three YAML job definitions
  into eight runner allocations and repeats checkout/setup eight times. Exact
  M35 run `31231410432` passed all slices. Twenty-five inherited M34/M35
  workflow-boundary tests passed in 0.64 seconds. The first sandboxed lock
  check could not read the managed uv cache; the corrected check resolved the
  unchanged 46-package lock. CPython 3.12, 3.13, and 3.14 are locally present.
- **Current evidence:** The workflow has one Ubuntu job and a two-entry desktop
  matrix. Ubuntu sequentially owns quality/distribution, 3.12 graphics, and
  3.13/3.14 compatibility; each desktop runner owns 3.12 graphics then 3.14
  compatibility. Exact local transitions pass 1,714 tests on both 3.13 and
  3.14; restored 3.12 passes 1,724 tests with nine skips. Whole-tree static/
  docs, YAML parsing, 34 focused workflow/release tests, universal build,
  isolated wheel/release smoke, real-wgpu/profile, and both vertical slices
  pass. Findings-first review moved later-interpreter installation before
  expensive work and found no remaining issue. Scope/security audit passes and
  the final implementation-tree 3.12 suite passes 1,724 tests with nine skips.
  Only factual `.project/**` rows followed. Hosted
  three-allocation proof remains pending.
