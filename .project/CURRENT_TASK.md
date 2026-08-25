# Current task

- **Task:** M129 - add deterministic verified asset build planning.
- **Status:** Primary-source direction, exact M128 base, focused retained
  behavior, both governance baselines, and the deliberate-red contract are
  complete. Pure planning, exact cache-key reuse, verified CLI composition,
  installed evidence, focused proof, RFC/public documentation, and the
  documentation-inclusive gate, complete runtime/graphics gates, corrected
  isolated-wheel proof, initial reproducible packages, release rehearsals,
  review, hygiene inspection, record-inclusive validation, and final
  reproducible package/release gates are complete. History/hosted-state audit,
  history/hosted-state audit are complete. Cleanup, the final metadata
  cleanup, and the final metadata separator are complete. The local DCO commit
  and postcommit proof remain.
- **Base:** Fully locally validated M128 DCO commit
  `ad6b43a9d480cd3bd94298799125ee736d15124e`, tree
  `f293f187a5c4f38bc3850c8ba0ffdc679582b472`, with sole parent exact M127.
  The stack remains unpublished under the existing public-review identity hold.
- **Branch:** `release/m129-deterministic-asset-build-plan`.

## Acceptance boundary

- Add strict immutable `ludoweave.asset-build-plan/1` values in the focused
  assets package, with tightening-only decode limits and canonical bytes.
- Add an explicit asset-loader protocol constant while preserving every
  existing M4 cache-key byte and artifact behavior.
- Accept only an exact M126 manifest plus M128 asset-source lock whose canonical
  manifest identity, roots, resolved URI set, and per-entry kinds agree.
- Produce each selected asset exactly once in deterministic dependency-first
  order. When multiple assets are ready, choose logical URI order.
- Precompute the exact existing M4 cache key from URI, kind, settings, source
  SHA-256, loader protocol, and direct dependency cache keys.
- Bind the canonical M128 lock identity and manifest identity in the plan.
- Add read-only `ludoweave source asset-plan PROJECT --manifest FILE --assets
  FILE --lock FILE`; recompute and verify current M128 inputs before planning.
- Emit no success bytes until source verification and complete planning pass.
- Prove the plan and exact cache-key compatibility from an isolated no-
  dependency wheel.
- Document that a plan is prospective deterministic work identity, not decoded
  output, build success, cache presence, artifact integrity, or execution.
- Keep workflows, allocations, permissions, credentials, dependencies, lock,
  metadata, version, root API, existing protocols/reports, release authority,
  and remote state unchanged.

## Direction and baseline evidence

- Primary sources accessed 2026-08-26: current Bazel build-reference and remote-
  caching documentation, Python 3.14 `graphlib`, Unity 6.2 asset dependency
  documentation, and stable Godot import-process documentation. Bazel separates
  graph/action planning from cache lookup and execution; Python defines
  dependency-first ordering but warns same-level order depends on insertion;
  Unity warns referenced dependencies are not automatically build-required;
  Godot separates source/import configuration from generated imports.
- These sources support a pure explicit-closure plan with URI tie-breaking and
  declared action identity. They do not justify cache read/write, remote cache,
  decoder execution, build, automatic import/reimport, watcher, or discovery.
- Exact M128 commit/tree/sole-parent, clean branch, and `0 29` divergence pass.
  The focused M124-M128 asset/source/CLI baseline passes 125 tests in 6.29
  seconds. Static and dated strict governance report zero findings.
- Deliberate red stops behavior collection only on absent plan exports; the
  M129 boundary has three intended absent implementation/CLI/docs failures and
  two protected/evidence passes. No implementation pass is claimed.
- After import/helper and one test-only closure-comparison correction, all
  statics and 36 focused behavior assertions pass in 3.82 seconds. The 1,100-
  node graph orders iteratively; only the intentional M129 docs boundary fails.
- RFC-0112 and public docs are complete. After correcting one nonexistent API-
  test filename, all statics, 147 focused assertions, strict docs, dated
  governance, and whitespace pass.
- Findings-first review found and corrected acceptance of non-URI ordering for
  simultaneously ready decoded entries. The focused red now passes, with all
  statics and 147 focused assertions green.
- The corrected isolated no-dependency wheel passes exact loader/plan identity,
  dependency-first entries, cache-key presence, and no-cache proof.
- The complete source separator passes formatting for 410 Python files, Ruff,
  strict Pyright, 1,657 architecture assertions with one established skip,
  strict docs, both governance modes, and whitespace.
- Exact supported-runtime suites pass: 3.12.13 graphics has 3,377 passes and
  16 skips; 3.13.13 and 3.14.5 base each have 3,367 passes and 17 skips.
- Real-wgpu, fresh base/graphics profiles, Clockwork Arena, and Agent World
  Builder all pass and reproduce their established deterministic identities.
- Two independent builds reproduce the initial wheel/source identities; all
  12 isolated consumers pass on a compact recorded rerun. Two complete ten-
  artifact stages are byte-identical and both complete release smokes pass.
- Findings-first review has no remaining actionable issue after the ready-set
  URI-order fix. Exactly 23 intended paths and all protected/hygiene scans pass.

## Explicit non-scope

- No asset payload read beyond M128 verification, decode, build, import, cache
  lookup, cache write, artifact creation, activation, reimport, watcher, or live
  update.
- No directory discovery, glob, default manifest, component-reference
  inference, unused-asset rejection, or build-inclusion policy beyond the exact
  explicit M127 closure.
- No concurrent scheduler, worker, thread, process, partial execution, resume,
  rollback, atomic filesystem snapshot, provenance, authenticity, or signature.
- No source/project write, world/session, command, transaction, world mutation,
  receipt, dependency, native/backend surface, metadata, version, workflow,
  allocation, permission, credential, release, publication, push, PR, or remote
  change.

## Remaining acceptance work

- Create the exact local DCO commit and run postcommit proof. Do not push or
  create a PR under the standing public-review identity hold.
