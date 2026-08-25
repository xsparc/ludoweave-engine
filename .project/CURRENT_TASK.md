# Current task

- **Task:** M127 - add bounded source-to-asset dependency checking.
- **Status:** Direction research, exact-base governance proof, deliberate red,
  implementation, RFC/public documentation, installed-wheel proof, complete
  source/architecture/docs/governance gates, all three supported runtimes,
  real-wgpu integration, profiles, and both vertical slices are complete.
  Findings review, record-inclusive source separators, initial/final
  reproducible artifacts, all installed-wheel and release smokes, and hygiene
  are complete. Final metadata and exact local/hosted history separators pass.
  Guarded cleanup and the final clean-scratch separator are complete. The local
  DCO commit remains.
- **Base:** Fully locally validated M126 DCO commit
  `9b373698c206982bcb6e86127ac8dffb2385a261`, tree
  `9f2b0b7fceb1241c14a659e26c1f5c95fe775c2e`, with sole parent exact M125.
  The stack remains unpublished under the existing public-review identity hold.
- **Branch:** `release/m127-source-asset-dependency-checking`.

## Acceptance boundary

- Add strict `AssetManifest.dependency_closure()` for an exact tuple of
  distinct direct `AssetUri` roots; return the roots and every reachable graph
  dependency exactly once in URI order.
- Add read-only `ludoweave source assets PROJECT --manifest FILE --assets FILE`.
- Reuse the unchanged explicit source inspection and project-confined asset-
  manifest loader; require every source-declared direct URI to exist.
- Emit canonical `ludoweave.cli.source-asset-check/1` only after complete
  success, with normalized source/asset manifest identities, ordered per-entry
  direct/resolved lists, and unique aggregate counts.
- Return a structured first-entry/first-URI missing-root failure with no success
  bytes, path disclosure, asset-source access, or project mutation.
- Prove the command from an isolated no-dependency wheel.
- Document direct versus resolved ownership, inability to infer application
  component references, admitted unused asset entries, sequential-read limits,
  deterministic ordering, and complete non-scope.
- Keep existing scene/prefab/source-manifest/source-lock and M126 formats,
  workflows/allocations, permissions, credentials, dependencies, lock,
  metadata, version, engine root, world, release authority, and remote state
  unchanged.

## Evidence so far

- Primary sources accessed 2026-08-26: current Unity dependency and direct-
  reference documentation, current Bazel dependency concepts, stable Godot
  `ResourceLoader`, JSON Schema Draft 2020-12 validation, and Python graph
  documentation. They distinguish direct edges from recursive closure and
  semantic validation from loading/building. Confidence is high for the
  declared-graph checker only.
- Exact M126 commit/tree/sole-parent, clean branch, and `0 27` divergence pass.
  Seventy-four asset/source/project/CLI baseline tests pass with one established
  Windows symlink-capability skip in 4.38 seconds; both governance modes return
  zero findings.
- The first deliberate-red attempt was blocked before project execution by uv-
  cache access and makes no contract claim. Its approved rerun produced all
  eight intended absent method/CLI failures. The M127 architecture module
  produced four intended absent implementation/evidence/docs failures and one
  protected-surface pass.
- The first implementation checkpoint passed formatting and Ruff; strict
  Pyright found four test/smoke JSON-container inference gaps and stopped before
  behavior. Explicit annotations changed no runtime behavior.
- Corrected statics pass and 31 new/retained closure, CLI, asset-manifest,
  source-manifest, and source-lock cases pass in 3.61 seconds.
- The first combined M126/M127 boundary run found only the intentionally absent
  M127 docs and an M126 historical guard that froze the entire CLI. M126 now
  protects its actual retained source contracts while M127 owns the new CLI.
- The first combined public-doc patch was rejected atomically on one wrapped
  CLI-guide paragraph; no file changed. Smaller patches added RFC-0110 and the
  public architecture, API, roadmap, command, workflow, changelog, README, and
  navigation updates.
- The documentation-inclusive gate passes seven-file formatting, Ruff, strict
  Pyright, 41 focused behavior/boundary assertions, strict docs, dated
  governance, and whitespace.
- Findings-first review replaced the pre-existing recursive cycle validator
  with iterative DFS and added a 1,100-node graph regression. Direct roots now
  share the 4,096-node bound; empty source and asset graphs remain compatible.
- The first isolated verifier used an obsolete project-protocol fixture and
  failed before M127. A fixture-only correction produced the expected
  no-dependency installed report and proved no asset source directory exists.
  Final statics, whitespace, and 40 focused assertions pass.
- Complete validation passes all 400-file statics, 1,647 architecture tests
  with one established skip, strict docs, both governance modes, and exact
  supported-runtime suites: 3,339/16 on CPython 3.12.13 graphics and
  3,329/17 on exact CPython 3.13.13 and 3.14.5 base.
- Ten real-wgpu tests, fresh one-repeat base/graphics profiles, the exact
  workflow-equivalent Clockwork Arena scenario, and Agent World Builder all
  pass and reproduce their established deterministic identities.
- Findings-first review has no remaining actionable issue. Two independent
  packages and two release stages reproduce byte-for-byte; all ten wheel
  smokes and both release smokes pass. Archive, scope, protected-surface,
  public-identity, credential, and whitespace inspections pass.
- Final record-inclusive package and release pairs reproduce. The source
  archive correctly changes from the initial pair because it contains the
  updated neutral engineering ledger; each same-tree final pair is identical.
- Fetch/prune and read-only hosted queries prove the exact linear local stack,
  required neutral branches, only remote main, exact identity/sign-offs, zero
  critical object findings, and no hosted M127 branch, PR, run, tag, or release.

## Explicit non-scope

- No inference of asset references from application component values and no
  claim that declared direct dependencies match all actual use.
- No requirement to repeat indirect dependencies and no unused-asset rejection,
  build-inclusion policy, default asset manifest, or directory discovery.
- No asset source read, payload decode, build, import, cache use/write,
  reimport, watcher, live update, source write-back, or remote access.
- No component-registry resolution, scene/prefab compile, world/session,
  command, transaction, world mutation, receipt, or project write.
- No dependency, lock, metadata, package version, engine-root export, workflow
  job/allocation, permission, credential, release authority, tag, release,
  publication, push, PR, or remote change.

## Remaining acceptance work

- Run complete source/architecture/governance and supported-runtime suites,
  real-wgpu, profiles, vertical samples, reproducible distributions, all
  installed-wheel paths, deterministic release rehearsal, and hygiene.
- Finish findings-first review, factual records, history/hosted audit, bounded
  scratch cleanup, final separators, exact staging, local DCO commit, and post-
  commit verification.
