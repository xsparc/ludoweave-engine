# Current Task

- **Task:** M30 - published-wheel installation-matrix admission readiness
- **Status:** In progress on `evidence/m30-installation-matrix-readiness` from
  exact clean synchronized verified `main` commit
  `c88b166a39a793c91741bfa762af5627a87c53b4`.
- **Started:** 2026-08-07
- **Base:** PR #46 squash-integrated exact corrected M29 feature tree as
  verified `fc969a981ecdbbf842477f46486e29277119e05b`; documentation-only PR
  #47 squash-integrated the factual M29 state record as verified
  `c88b166a39a793c91741bfa762af5627a87c53b4`. Local `main`, `origin/main`,
  and `origin/HEAD` matched that commit with a clean worktree before branching.
- **Outcome:** Make the design plan's next longer-term metric—installation
  success across the supported OS/CPython matrix—mechanically auditable without
  treating source-checkout CI, local builds, automation, or synthetic fixtures
  as installations of one immutable public release wheel.
- **Acceptance gate:**
  - Add one strict reviewed manifest whose current installation record set is
    empty and whose exact bytes and SHA-256 are pinned by architecture tests.
  - Require Ubuntu CPython 3.12/3.13/3.14 and macOS/Windows CPython 3.12/3.14.
  - Require every record to identify the same canonical public project release,
    universal wheel URL, release version/tag, and wheel SHA-256.
  - Require fresh isolation, release-wheel installation, no dependencies, no
    native compiler, and passing installed version, doctor, `hello_headless`,
    and headless Clockwork Arena checks.
  - Require platform/Python agreement, distinct log identities, successful
    outcomes, canonical timestamps, and reviewed provenance and validation.
  - Preserve accepted history as an exact complete executable prefix and bind
    it to the reviewed whole-manifest digest.
  - Expose record-derived environments and release versions only after exact
    digest and complete-history admission.
  - Emit exact sanitized `not-ready` evidence for the current empty manifest;
    never expose URLs, Python patch/platform values, hashes, timestamps, local
    paths, host facts, or timings.
  - Prove future gate mechanics synthetically while refusing to count fixtures
    as releases, users, installations, publication, or support evidence.
  - Exercise source, isolated-wheel, and release-sample paths, accept RFC-0013,
    and preserve both workflows and all eight essential CI jobs exactly.
- **Non-scope:** Publishing or downloading a release; GitHub discovery or
  remote lookup; running installer commands from manifest data; networking,
  telemetry, dynamic imports, subprocess launch by the evaluator, provider
  execution, credentials/private logs, runtime source, public APIs/exports,
  persistent formats, protocols, dependencies, lock, version, workflows, CI
  topology, tags, releases, certification, or support policy.
- **SemVer:** No package or public-Python-surface change; version remains
  `0.1.0a1` and current stability labels are unchanged.
- **Baseline evidence:** Exact `HEAD`, `main`, `origin/main`, `origin/HEAD`, and
  merge base all resolved to
  `c88b166a39a793c91741bfa762af5627a87c53b4`; the worktree was clean and
  `git fsck --full --no-dangling` exited 0. The unchanged 46-package lock
  resolved in 0.84 ms. The inherited M29/artifact baseline passed 61 tests with
  one Windows symlink-capability skip in 2.20 seconds. CI and release workflow
  hashes remain `06a5e07918c83fc8de61e6746cb344f865b6421d81f554d79f4455d3718a3b21`
  and `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`.
- **Current local evidence:** The exact 462-byte empty manifest has SHA-256
  `7c05813a7304e8ff44a009ada37c8e60ff545baec633852fc332e46bdfe03c90`.
  The evaluator emits deterministic path-free `not-ready` evidence with zero
  successful environments. Findings-first review corrected the canonical
  GitHub asset download path, required a unique public validation-job locator,
  enforced required environment order, and added real calendar validation. The
  focused evaluator, architecture, and release-artifact suite passes 56 tests
  with one Windows symlink-capability skip. The final complete gate passes the
  unchanged lock/sync, 247-file formatting, Ruff, strict Pyright, strict docs,
  1,375 tests with seven skips, pure build, isolated wheel/release smoke, ten
  real-wgpu tests, and both graphics vertical slices. The 94-entry wheel has no
  native/WASM file and the 40-entry sample bundle contains both exact M30
  evidence files. Protected runtime/workflow/metadata/lock scope is unchanged.
  No benchmark was run because M30 changes no runtime or performance path and
  makes no performance claim. Ready-PR publication, hosted validation, review
  reread, and integration remain pending.
