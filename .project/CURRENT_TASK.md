# Current task

- **Task:** M147 - adopt a dedicated asset-cache cleanup threat model before
  any mutation design.
- **Status:** Direction research, RFC, public threat model,
  architecture/roadmap contract, automated no-runtime-change guard, complete
  static/architecture/docs/governance checks, supported-Python suites, real
  wgpu checks, profiles, vertical slices, reproducible distributions, all 28
  installed consumers, two release rehearsals, archive inspection, and
  findings-first review are complete. Final evidence-inclusive reproducibility
  and the final source separator are closed. Bounded cleanup, the initial DCO
  commit, exact local audit, and fresh publication audit are complete.
  Publication is held because authoritative hosted `main` remains exact M99.
- **Base:** Fully locally validated M146 DCO commit
  `15a1294e02c0efc77fdb668430d89413af424c9d`, tree
  `950357cf643ddc9472f1ba6cda47ccb14b798f18`, sole parent exact M145.
- **Branch:** `release/m147-cache-cleanup-threat-model`.

## Acceptance boundary

- Accept RFC-0130 and a dedicated threat model covering protected assets,
  actors, trust boundaries, misuse cases, twelve threats, eight invariants,
  verification, and residual risk.
- Require identity-bound candidates, complete retained roots, quiescence held
  through use, handle-relative no-follow safety, explicit policy/trusted time,
  same-filesystem quarantine, receipts, idempotence, and recovery.
- Protect exact runtime, cache, CLI, dependency, workflow, and release surfaces
  with automated architecture tests.
- Add no runtime API, protocol, decoder, command, cache access, candidate
  disclosure, cleanup authority, mutation, dependency, version, workflow, or CI
  change.

## Direction evidence

- MITRE CWE-367 records integrity risks when a resource changes between check
  and use. Python documents `rmtree` symlink-attack resistance as conditional
  on fd-based platform support, while Windows reparse points require distinct
  namespace handling.
- Bazel's current cache guidance uses explicit policy/idle-driven garbage
  collection and separately warns that changing inputs can produce invalid
  cached results; neither observation grants LudoWeave mutation authority.
- Exact M146 history, clean worktree, DCO, and object integrity were established
  before this branch. Exact ancestry allowed the contained M146 branch to be
  pruned; only local `main` and active M147 remain.

## Explicit non-scope

- No cleanup, garbage collection, prune, repair, deletion, eviction, mutation,
  retained-root implementation, lease/pin, candidate list, cache read/write,
  remote cache, network, or trusted-time implementation.
- No dependency, version, workflow/CI, permission, credential, release, tag,
  push, or PR change.

## Remaining acceptance work

- No local M147 acceptance work remains. Keep the milestone unpublished until
  a fresh hosted audit proves the required preceding stack is present; continue
  the next approved research-gated milestone from the exact committed M147 tip.
