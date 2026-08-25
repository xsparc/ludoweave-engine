# Current task

- **Task:** M122 - add explicit project-confined prefab source and instance
  file loading.
- **Status:** Direction research, governance baseline, deliberate-red proof,
  implementation, focused behavior/property/type validation, RFC-0105, public
  documentation, source/supported-runtime/graphics validation, all five
  installed-wheel verifiers, reproducible distribution, two release rehearsals,
  package hygiene, and findings-first review are complete. Review-inclusive
  rebuild/release rehearsal, final record-inclusive and post-record separators,
  cleanup, and history/hosted-state validation are complete. Only the local DCO
  commit and exact post-commit verification remain.
- **Base:** Fully locally validated M121 DCO commit
  `18d1571badc416801151b6f5df67e3cfcef78ba1`, tree
  `2a2cfae57f9d6546ad74657f8a82b26ca5ac6085`, with sole parent exact M120.
  The stack remains unpublished under the existing public-review identity hold.

## Acceptance boundary

- Add typed `HeadlessProject.load_prefab()` and `load_prefab_instance()`
  methods in the existing tools composition root; keep `ludoweave.scene`
  filesystem- and transport-agnostic.
- Accept two caller-selected project-relative paths plus exact `PrefabLimits`;
  reuse established confinement, regular-file checks, sanitized diagnostics,
  descriptor ownership, metadata size checks, and handle read caps.
- Delegate detached bytes to unchanged `ludoweave.prefab/1` and
  `ludoweave.prefab-instance/1` decoders. Preserve `compile_prefab()` as the
  exact source-matching, planning, and later receipt boundary.
- Return detached immutable records with no world mutation, pairing, discovery,
  cache, watcher, or asset resolution.
- Add focused unit/property/architecture coverage, RFC-0105, aligned public
  docs, and a standalone installed-wheel load/compile/apply verifier.
- Keep commands, operations, transaction service, workflows, allocations,
  actions, permissions, credentials, dependencies, lock, metadata, version,
  root API, scene/prefab schemas and planners, release authority, tags,
  releases, publication, and public remote state unchanged.

## Evidence so far

- Primary-source direction research accessed 2026-08-25 reviewed current Godot
  `ResourceLoader`, current Unity prefab documentation, RFC 8089, and JSON
  Schema Core 2020-12. The adopted high-confidence recommendation is two
  explicit loads with existing path policy and no general resource-loader
  discovery/cache surface; live update and nested composition remain evidence
  gaps and non-scope.
- Static and dated strict governance baselines both returned zero findings.
- Exact CPython 3.12.13 deliberate red produced 15 expected absent-capability or
  documentation failures and one protected-boundary pass. No test-only failure
  appeared until implementation: the generated 108-byte limit equaled the
  smaller fixture and correctly loaded. Tightening the domain strictly below
  both fixture lengths corrected the test; all 12 behavior/property assertions
  then passed in 0.58 seconds.
- Focused formatting, Ruff, and strict Pyright pass; all 16 M122 unit and
  architecture assertions pass in 0.60 seconds; strict docs build in 1.58
  seconds with only the known Material notice.
- The inherited headless-project, scene, prefab, M59, and M119-M122 focused set
  passes 92 tests with two established capability skips in 1.19 seconds.
- The first source/sdist wheel build passed. The isolated no-dependency wheel
  verifier loaded two explicit files, compiled one ordinary command, committed
  one entity, and returned alias `root` with the expected source and instance
  identities.
- Complete source, architecture, docs, governance, and supported-runtime gates
  pass. Exact 3.12.13 passes 3,234 tests with 16 skips; exact 3.13.13 and 3.14.5
  each pass 3,224 with 17 skips.
- Ten real-wgpu tests, both profiles, and both established vertical slices pass.
  Two initial distributions are byte-identical, all five installed-wheel smokes
  pass, two ten-artifact release stages are identical, and both release smokes
  pass.
- Package inventories contain zero forbidden entries; corrected public identity
  and high-confidence secret scans have zero matches. Findings-first review of
  17 intended paths found no actionable defect and protected surfaces retain
  zero diff.
- The review-inclusive pair reproduces the 292,732-byte wheel and a 1,614,073-
  byte sdist; all five wheel smokes, two identical ten-artifact release stages,
  both release smokes, and package hygiene pass.
- Stacked history, DCO/identity, Git integrity, local/remote branch inventory,
  authentication, and empty M122 PR/run/release/tag state all validate.
- Exact M122 build, release, profile, docs, distribution, and pytest scratch
  targets are absent after one corrected exact-path cleanup retry.

## Explicit non-scope

- No implicit pairing, directory discovery, extension routing, manifest lookup,
  include/import graph, asset loading, cache, watcher, live update, reimport,
  write-back, nested prefab composition, file URI, or remote path.
- No new persistent operation, `EntityRef` facade, arbitrary Python import or
  evaluation, global registry, renderer, provider, networking, editor, native
  compiler, or second authority.
- No workflow, hosted allocation, dependency, lock, metadata, version, root API,
  release authority, tag, release, publication, push, or PR.

## Remaining acceptance work

- Create the standalone DCO commit and verify its exact tree, parent, identity,
  scope, and clean worktree. Publication remains held.
