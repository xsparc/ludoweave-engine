# Current task

- **Task:** M145 - strictly admit and verify one saved unreferenced-blob
  preview against its exact plan and admitted saved fingerprint offline.
- **Status:** Implementation, complete local acceptance, supported-Python
  validation, installed-wheel proof, reproducibility, release rehearsal,
  findings-first review, final evidence closure, and bounded cleanup are
  complete. The initial DCO commit and fresh publication audit are complete.
  Publication is held because authoritative hosted `main` remains exact M99.
- **Base:** Fully locally validated M144 DCO commit
  `d6bbf33e35b5e21fa48d6553e1b3b73d104b0cd6`, tree
  `197792e9cc5226084a1d947916349b5e9cc0f1af`, with sole parent exact M143.
- **Branch:** `release/m145-saved-unreferenced-preview-verification`.

## Acceptance boundary

- Add a tightening-only 2,048-byte preview-record limit and strict canonical
  exact-schema decoder for `ludoweave.asset-cache-unreferenced-preview/1`.
- Add a pure verifier over exact `AssetBuildPlan`, admitted
  `AssetCacheFingerprint`, and admitted `AssetCacheUnreferencedPreview` values.
  Recompute unchanged M143 once, require exact equality, and emit fixed
  `ludoweave.asset-cache-unreferenced-preview-verification/1` evidence binding
  the exact canonical preview bytes by SHA-256.
- Add `source asset-cache-unreferenced-preview-verify`. Preflight current
  sources, saved lock, and exact regenerated plan before resolving either saved
  record; reuse M139 fingerprint admission and read the preview under its new
  bound. Expose no cache argument and perform no mutation.
- Prove bounded/canonical admission, tamper rejection, stable path-free output,
  cache-absent use, current-input preflight ordering, installed-wheel behavior,
  architecture isolation, supported-Python behavior, strict docs, reproducible
  artifacts, and unchanged release surfaces.
- Preserve M137-M144 bytes/protocols, cache layout and behavior, root API,
  package version, dependencies/lock, workflows/allocations/permissions,
  release behavior, and backend/native boundaries.

## Direction evidence

- RFC 8785 and Python 3.12 JSON guidance support duplicate-free canonical
  admission with explicit non-finite rejection; SLSA verification guidance
  keeps integrity separate from authenticity and trust roots; GitHub workflow
  guidance supplies no reason to expand quota-conscious CI.
- Exact M144 history, tree, parent, DCO, identity, clean worktree, and object
  integrity were established before this neutral branch was created. Exact
  ancestry proved the contained M144 branch redundant and it was pruned; only
  local `main` and active M145 remain.
- The first unit gate exposed generic digest-field diagnostics; the decoder now
  reports the exact invalid digest field and all 17 unit cases pass.
- The first CLI gate exposed one test-fixture name typo while the product
  implementation compiled; after correction, formatting, Ruff, strict Pyright,
  and all three selected integration cases pass.
- An initial pure wheel and source archive were built, and the isolated
  no-dependency M145 consumer passed twice after deleting the originating cache.

## Explicit non-scope

- No cache observation or access, candidate identity, path/payload/age
  disclosure, current-state or chronology/freshness guarantee, authenticity,
  provenance, writer identity, trusted timestamp, atomic snapshot, retention or
  deletion eligibility, cleanup, prune, garbage collection, repair, eviction,
  or mutation.
- No remote cache, network, ECS/world, command/receipt, renderer, physics,
  audio, editor, 3D, native/Rust/PyO3, dependency, version, workflow, runner,
  permission, credential, release, tag, or public-package change.
- No push or PR until complete local acceptance and a fresh hosted audit proves
  the required preceding stack is already present on the intended base.

## Remaining acceptance work

- No local M145 acceptance work remains. Keep the milestone unpublished until
  a fresh hosted audit proves the required preceding stack is present; continue
  the next approved research-gated milestone from the exact committed M145 tip.
