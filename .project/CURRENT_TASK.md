# Current task

- **Task:** M146 - record why existing aggregate evidence cannot authorize
  asset-cache cleanup and define the complete reconsideration gate.
- **Status:** Direction research, RFC, public architecture/roadmap contract,
  complete local acceptance, installed-wheel proof, reproducibility, release
  rehearsal, findings-first review, and final evidence closure are complete.
  Bounded cleanup, the initial DCO commit, and fresh publication audit are
  complete. Publication is held because authoritative hosted `main` remains
  exact M99.
- **Base:** Fully locally validated M145 DCO commit
  `2a08a5cde25cab2b6a9950c0013c69286da873bb`, tree
  `a53ff7c7427695689337d8e120579abd74fbc883`, sole parent exact M144.
- **Branch:** `release/m146-cache-cleanup-readiness-decision`.

## Acceptance boundary

- Accept RFC-0129 and document that M137-M145 aggregate evidence cannot prove
  blob identity, current reachability, or deletion safety.
- Require identity-bearing candidates, retained roots/leases/pins, atomic or
  generation-bound quiescence, explicit grace/quota and trusted time, bounded
  dry-run plus typed mutation receipts, concurrent-writer and crash recovery,
  link/reparse safety, and restore/rollback before reconsideration.
- Protect exact runtime, cache, CLI, dependency, workflow, and release surfaces
  with automated architecture tests.
- Add no runtime API, protocol, decoder, command, cache access, candidate
  disclosure, cleanup authority, mutation, dependency, version, workflow, or CI
  change.

## Direction evidence

- Bazel's current disk-cache documentation describes policy/idle-driven garbage
  collection rather than treating aggregate observation as deletion authority.
- RFC 8785 supports stable canonical evidence identity but not reachability or
  concurrency claims. SLSA verification requires subject digests, expectations,
  and trust roots before authenticity claims.
- M140 already exposes the relevant aggregate deltas; another aggregate
  comparison would duplicate API without establishing candidate identity.
- Exact M145 history, clean worktree, DCO, and object integrity were established
  before this branch. Its contained local branch was pruned after exact ancestry
  proof; only local `main` and active M146 remain.

## Explicit non-scope

- No cleanup, garbage collection, prune, repair, deletion, eviction, mutation,
  retained-root implementation, lease/pin, candidate list, cache read/write,
  remote cache, network, or trusted-time implementation.
- No dependency, version, workflow/CI, permission, credential, release, tag,
  push, or PR change.

## Remaining acceptance work

- No local M146 acceptance work remains. Keep the milestone unpublished until
  a fresh hosted audit proves the required preceding stack is present; continue
  the next approved research-gated milestone from the exact committed M146 tip.
