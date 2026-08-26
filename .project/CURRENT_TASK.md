# Current task

- **Task:** M143 - preview unreferenced local asset-cache blobs from one exact
  current plan and one verified M138 cache observation.
- **Status:** Runtime, focused API, CLI, tests, architecture, documentation,
  complete local validation, reproducible distribution, all installed
  consumers, release rehearsal, findings-first review, final scope/history/
  hosted-state audits, bounded generated cleanup, and the authorized local DCO
  commit are complete. No CI change was needed.
- **Base:** Fully locally validated M142 DCO commit
  `9f4a84b0e1f251d400398da4ef27d5c37eee386b`, tree
  `2e1d9c4c693658036500921cb45039366dda0765`, with sole parent exact M141.
- **Branch:** `release/m143-path-free-unreferenced-blob-preview`.

## Acceptance boundary

- Add one pure function over an exact frozen `AssetBuildPlan` and exact frozen
  M138 `AssetCacheFingerprint`. Recompute and require the plan digest and the
  nested inventory's plan binding before producing evidence.
- Emit frozen, canonical, path-free
  `ludoweave.asset-cache-unreferenced-preview/1` evidence containing only the
  observed status, inventory/fingerprint protocols, plan SHA-256, complete M138
  observation SHA-256, and the two existing aggregate values
  `unreferenced_blobs` and `unreferenced_blob_bytes`.
- Add `source asset-cache-unreferenced-preview`: preflight current sources,
  lock, and plan before resolving the cache; perform exactly one unchanged,
  bounded M138 read-only observation; then apply the pure preview. An absent
  cache reports zero without creating it. A nonzero preview remains successful
  diagnostic output with exit 0; invalid processing remains structured exit 2.
- Prove path/digest/object-identity silence, plan mismatch rejection,
  read-only behavior, absent-cache behavior, referenced-blob exclusion,
  installed-wheel operation, strict documentation, and protected architecture.
- Preserve workflows, dependencies, version, cache layout and mutation code,
  M137-M142 protocols/bytes, engine-root API, and release authority.
- State explicitly that the preview is observation evidence only, not deletion
  eligibility, a retention policy, an atomic snapshot, or cleanup authority.

## Direction and evidence so far

- Primary sources accessed 2026-08-27: CNCF Distribution garbage collection,
  Git garbage collection, Bazel remote caching, Gradle cache cleanup, BuildKit
  garbage collection, the Remote Execution API, OpenTelemetry sensitive-data
  guidance, NIST FIPS 180-4, and GitHub workflow-trigger controls. They support
  a read-only aggregate preview and show that real garbage collection requires
  separately designed roots, grace/age policy, quiescence/concurrency safety,
  and crash recovery. They provide no reason to expand CI for this slice.
- Exact M142 commit, tree, parent, clean worktree, identity, and DCO sign-off
  were established before this neutral branch was created. Exact ancestry
  proved the redundant M142 branch was contained and it was pruned.
- The additive value/function, focused exports, CLI, 19 unit cases, focused CLI
  cases, isolated installed consumer, RFC-0126, public docs, and architecture
  boundary are implemented.
- Focused formatting/Ruff/strict-Pyright checks pass. All 19 unit assertions
  passed in 0.97 seconds; 23 selected CLI assertions passed in 5.42 seconds;
  after correcting one documentation phrase, all 28 selected behavior/CLI/
  boundary assertions passed in 5.36 seconds and strict docs built in 2.12
  seconds with only the known Material notice. Whitespace passes.
- The initial pure wheel is 355,369 bytes at SHA-256
  `91303301c9fa74d07731f549e48246c7a6f59401e652d6d24d81a1181b1fb470`;
  the initial source archive is 1,859,314 bytes at SHA-256
  `94d9450859638c696338fd7f2f69f80ce80332eb0eee512b5f85c9a87c35db19`.
  The new isolated no-dependency preview consumer passed.
- All 464 Python files are format-clean; Ruff and strict Pyright pass; 1,727
  architecture assertions pass with one established skip; strict docs and both
  governance modes pass; exact CPython 3.12-3.14, real-wgpu, profiles, and both
  deterministic vertical slices pass.
- Two evidence-inclusive distributions reproduce byte-for-byte. The final pure
  wheel is 355,411 bytes at SHA-256
  `8e47ee0f28c1e396ecfa1e0614a20d637d172999b77341977f363c83a5b89eb4`;
  all 26 isolated installed consumers pass against that wheel. Two
  byte-identical ten-artifact release rehearsals pass.
- Findings-first, archive, protected-surface, disclosure, identity, credential,
  history, DCO, and object-integrity reviews are clean. Exactly 19 intended
  paths remain, all audited generated scratch is absent, and `.venv` is
  retained.
- A fresh fetch and GitHub branch/merged-PR queries on 2026-08-27 still expose
  only exact M99 `main` at
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`; the reported squash merge is not
  visible on this remote. M143 therefore remains local pending full acceptance
  and a public base that actually contains the preceding stack.

## Explicit non-scope

- No per-object candidate/list/diff, cache key, URI, action/blob/artifact
  identity, filename/path, payload, source contents, timestamp, age, last-use
  fact, policy threshold, expected/current comparison, or new observation.
- No deletion eligibility, retention root, lease, pin, generation, grace
  period, eviction, garbage collection, cleanup, prune, repair, mutation,
  migration, rollback, quota enforcement, hostile-concurrency guarantee,
  quiescence protocol, or atomic snapshot.
- No saved-preview decoder/verifier/storage, signing, authentication,
  attestation, provenance, remote cache, network, telemetry export, watcher,
  scheduler, worker, process, thread, parallelism, plugin, dynamic evaluation,
  renderer upload, project/world mutation, receipt, dependency, native/backend
  surface, metadata, version, engine-root API, workflow/allocation, permission,
  credential, release, publication, push, PR, or remote change in this slice.

## Remaining acceptance work

- No local M143 acceptance work remains. Keep the commit unpublished until a
  fresh remote audit proves the required base is present; the authoritative
  hosted ref currently remains exact M99. Continue the next approved,
  research-gated milestone from the exact committed M143 tip.
