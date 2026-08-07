# Current Task

- **Task:** M29 - external contributor-retention admission readiness
- **Status:** In progress on `evidence/m29-contributor-retention-readiness`
  from exact clean synchronized verified `main` commit
  `e4125bf31a751473d2af4fecc05a9744d551063c`.
- **Started:** 2026-08-07
- **Base:** PR #44 squash-integrated M28 as verified
  `90d58a4567e7c7eaff90a28a7c59f2453b6d4538`; documentation-only PR #45
  squash-integrated its exact state record as verified
  `e4125bf31a751473d2af4fecc05a9744d551063c`. Local `main`, `origin/main`,
  and `origin/HEAD` matched that commit with a clean worktree before branching.
- **Outcome:** Make the design plan's next longer-term metric—contributor
  retention rather than raw stars—mechanically auditable without treating
  maintainers, non-human automation, CI, popularity totals, or synthetic
  fixtures as retained external humans.
- **Acceptance gate:**
  - Add one strict reviewed manifest whose current retention record set is
    empty and whose exact bytes and SHA-256 are pinned by architecture tests.
  - Require at least one independently reviewed external human with a first
    and later return contribution before the result can become true.
  - Require distinct public project issues and merged pull requests, exact
    base/head/merge identities, distinct patch/review SHA-256 identities,
    canonical merge chronology, valid DCO, complete validation, and reviewed
    provenance for both contributions.
  - Require explicit human review of identity, independence, same-person
    continuity, chronology, and retention.
  - Reject non-human or maintainer relationships, unreviewed facts,
    open/unmerged contributions, unsafe public references, invalid chronology,
    incomplete validation, duplicate identities, and malformed resources.
  - Preserve accepted history as an exact complete executable prefix and bind
    it to the reviewed whole-manifest digest.
  - Expose record-derived counts and scopes only after exact digest and
    complete-history admission.
  - Emit exact sanitized `not-ready` evidence for the current empty manifest;
    never expose contributor IDs, URLs, revisions, artifact hashes,
    timestamps, local paths, platform facts, or timings.
  - Prove future gate mechanics synthetically while refusing to count those
    fixtures as people, contributions, retention, adoption, or project history.
  - Exercise source, isolated-wheel, and release-sample paths, accept RFC-0012,
    and preserve the two workflows and eight essential CI jobs exactly.
  - Apply the separately authorized neutral repository convention by moving
    maintenance guidance to `MAINTAINERS.md` and state/evidence to `.project/`,
    updating references without rewriting factual Git or DCO history.
- **Non-scope:** Soliciting/contacting contributors; GitHub discovery or remote
  lookup; opening or mutating issues/PRs as evidence; networking, telemetry,
  dynamic imports, subprocesses, installation, provider execution, private
  communication, or unpublished personal-data collection; changing runtime
  source, public APIs/exports, persistent formats, protocols, operations,
  dependencies, lock, version, workflows, CI topology, tags, releases,
  publication, certification, support policy, or stability labels.
- **Repository convention:** The user separately authorized neutral role- and
  purpose-based names for visible maintenance metadata. This changes paths and
  references only; it does not alter authorship, provenance, or milestone scope.
- **SemVer:** No package or public-Python-surface change; version remains
  `0.1.0a1` and current stability labels are unchanged.
- **Baseline evidence:** Exact M29 base, `main`, `origin/main`, and
  `origin/HEAD` all resolved to
  `e4125bf31a751473d2af4fecc05a9744d551063c`; the worktree was clean and
  `git fsck --full --no-dangling` exited 0. Workflow hashes remain
  `06a5e07918c83fc8de61e6746cb344f865b6421d81f554d79f4455d3718a3b21`
  and `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`.
  The first sandboxed lock check failed before project execution because the
  existing uv cache was denied; the approved rerun resolved the unchanged
  46-package lock in 0.74 ms. The focused M27/M28/artifact baseline passed 114
  tests with two Windows symlink-capability skips in 3.93 seconds.
- **Local acceptance evidence:** The reviewed manifest is exactly 274 bytes with SHA-256
  `61785ec165e9f9a7c1025c37f7b714d6fa42b2c7081145a0f843395a325b36ee`
  and contains zero retention records. The evaluator emits exact sanitized
  `not-ready` evidence with zero retained contributors and reason
  `retained-external-contributor-absent`. Findings-first review added case-
  insensitive contributor identity, explicit popularity-field rejection,
  ASCII-only canonical timestamps, and fail-closed excessive-nesting handling.
  The final focused gate passes 111 M28/M29 and artifact tests with two Windows
  symlink-capability skips. The complete gate passes the unchanged lock/sync,
  243-file formatting, Ruff, strict Pyright, strict docs, 1,319 tests with six skips, a
  pure 94-entry wheel, isolated wheel/release smoke, all retained benchmark/
  profile validators, ten real-wgpu tests, and both graphics vertical slices.
  The 38-entry sample bundle contains both exact M29 evidence files. M1
  simulation and both M3 targets remain observed misses and authorize no
  acceleration.
- **Hosted correction:** Ready PR #46 run `31181308306` passed five essential
  jobs and failed only the Ubuntu, macOS, and Windows Python 3.14 jobs on one
  excessive-nesting decoder assumption. The parser-independent correction
  caps structural JSON nesting at 16 while ignoring string contents and
  escapes. Focused CPython 3.12 and 3.14 runs each pass 56 tests with one skip;
  complete CPython 3.12 and 3.14 suites pass 1,321 tests with six skips and
  1,311 tests with seven skips. Static, strict docs, pure build, isolated wheel,
  and fresh release smoke also pass. Correction commit, hosted validation,
  review reread, and squash integration remain pending.
