# Current Task

- **Task:** M32 - CI replay-divergence-rate admission readiness
- **Status:** Complete, hosted-validated, reviewed, squash-integrated, and
  cleaned up on synchronized verified `main` commit
  `36e8d9ed65a619569f3620b2431d977a1fb80a58`.
- **Started:** 2026-08-08
- **Base:** PR #50 squash-integrated the exact corrected M31 feature tree as
  verified `8adb8d46d0ce13ea3687856ae53e899e98dc42a6`; documentation-only PR
  #51 squash-integrated the factual M31 state record as verified
  `b4de1d115ddb620ecddccab84637c0e66cfad9fd`. Local `main`, `origin/main`,
  and `origin/HEAD` matched that commit with a clean worktree before branching.
- **Outcome:** Make the design plan's next longer-term metric—replay-divergence
  rate in CI—mechanically reportable from a complete reviewed execution cohort
  without querying GitHub, collecting telemetry/logs, selecting only completed
  checks, or inferring a zero rate from passing workflows.
- **Acceptance gate:**
  - Add one strict reviewed manifest whose current evaluation-window set is
    empty and whose exact bytes and SHA-256 are pinned by architecture tests.
  - Require bounded chronological non-overlapping execution windows plus a
    strictly later observation cutoff and complete reviewed public CI cohort.
  - Preserve every eligible replay execution as verified, diverged, or not-
    executed; never omit cancellation, pre-replay failure, skipping, or missing
    result evidence.
  - Bind executions to canonical public run/job locations, exact head/workflow/
    case sources, UTC start time, and frozen result evidence.
  - Require verified outcomes to have equal hashes; divergent outcomes to have
    distinct hashes, first divergent tick, and `world.replay.diverged`; and
    non-executed outcomes to claim no replay hashes or tick.
  - Require census and review artifacts at the same immutable project revision,
    unique execution/result identities, and reviewed eligibility, outcome,
    provenance, validation, and cohort completeness.
  - Preserve accepted windows as an exact complete executable prefix and bind
    it to the reviewed whole-manifest digest.
  - Expose an exact integer numerator/denominator rate only for a non-empty
    complete cohort with no non-executed case; define no float, threshold,
    quality verdict, release gate, reliability promise, SLA, or support promise.
  - Emit exact sanitized `not-ready` evidence for the current empty manifest;
    never expose run/job locations, revisions, case names, timestamps, hashes,
    local paths, host facts, environment values, or raw logs.
  - Exercise source, isolated-wheel, and release-sample paths, accept RFC-0015,
    and preserve both workflows and all eight essential CI jobs exactly.
- **Non-scope:** GitHub discovery or remote lookup; workflow mutation;
  telemetry/log collection; runtime source; replay behavior; public APIs/
  exports; persistent formats; protocols; operations; dependencies; lock;
  version; workflows; CI topology; tags; releases; publication; certification;
  stability promotion; reliability targets; service levels; or support policy.
- **SemVer:** No package or public-Python-surface change; version remains
  `0.1.0a1` and current stability labels are unchanged.
- **Baseline evidence:** Exact `HEAD`, `main`, `origin/main`, and `origin/HEAD`
  resolved to `b4de1d115ddb620ecddccab84637c0e66cfad9fd`; the worktree was clean,
  only `main` existed locally/remotely, no PR was open, and
  `git fsck --full --no-dangling` exited 0. The first sandboxed lock attempt
  could not access uv's existing user cache and produced no lock result. The
  corrected host-cache run resolved the unchanged 46-package lock in 0.80 ms
  and passed 65 inherited M31/release tests with one Windows symlink-capability
  skip in 1.44 seconds. CI and release workflow SHA-256 values remain
  `06a5e07918c83fc8de61e6746cb344f865b6421d81f554d79f4455d3718a3b21` and
  `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`.
- **Current local evidence:** The exact 175-byte empty manifest has SHA-256
  `cff8a32428ac8dcd18029be4f70e9d359b4c9d70fd411ffe2f36d35704d68aa7`.
  The evaluator emits deterministic path-free `not-ready` evidence with zero
  windows/executions and no rate. Findings-first review found and corrected a
  noncanonical replay-case URL acceptance gap plus underspecified eligibility
  for deliberately divergent/verification-disabled cases. The reviewed gate
  passes the unchanged 46-package lock, 255-file formatting, Ruff, strict
  Pyright, strict docs, 1,498 tests with nine platform-capability skips, pure
  build, isolated wheel/release smoke, ten real-wgpu tests, and both graphics
  vertical slices. The unchanged 94-entry wheel has no native/WASM file and the
  44-entry sample bundle contains both exact M32 evidence files. Protected
  runtime/workflow/metadata/lock scope is unchanged. Initial exact head
  `7046e59eb4840e6df492c886ce78baf4ad51cd95` passed all eight hosted jobs, but
  hosted review found the evaluator used `world.replay.divergence` instead of
  runtime diagnostic `world.replay.diverged`. The evaluator, fixture, docs, and
  architecture regression are corrected. The post-review gate passes 80
  focused tests with one skip, 1,499 complete-suite tests with nine skips,
  255-file formatting, Ruff, strict Pyright, strict docs, the unchanged lock,
  protected-surface and whitespace checks, pure build, isolated-wheel smoke,
  and a fresh ten-artifact release smoke. Corrected exact head
  `f6f574c2e9b54341e77d1b9ba2d9268bffe5439a` passed all eight essential jobs
  in hosted run `31195402467`; the sole review thread is resolved and outdated.
  PR #52 squash-integrated exact tree
  `e185e24861b74fe11325b7188026af29a9618926` as GitHub-verified commit
  `36e8d9ed65a619569f3620b2431d977a1fb80a58` with sole parent
  `b4de1d115ddb620ecddccab84637c0e66cfad9fd` and the DCO trailer. Literal tree
  comparison and object-integrity checks passed. The temporary feature branch
  is deleted locally and remotely; only the factual integration-record branch
  remains pending its documentation-only PR.
