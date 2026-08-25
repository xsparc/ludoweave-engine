# Current task

- **Task:** M119 - add bounded data-only scene transaction planning.
- **Status:** Direction research, deliberate-red proof, implementation, focused
  behavior/type/architecture validation, documentation, and a standalone local
  installed-wheel verifier are complete. Complete supported-runtime, initial
  distribution, review correction, focused post-review validation,
  review-inclusive artifacts, final precommit validation, and bounded scratch
  cleanup pass. The reviewed 22-path slice is ready for its standalone DCO
  commit and postcommit verification.
- **Base:** Fully locally validated M118 DCO commit
  `7b68f3d02987ee9824785c1699592c4670dbe267`, tree
  `a60c9e3668a0ed1f5462015210a8b8e9ee593a3f`, with sole parent exact M117.
  The stack remains unpublished under the existing public-review identity hold.

## Acceptance boundary

- Add exact `ludoweave.scene/1` data-only documents with bounded canonical JSON,
  stable local IDs, unique names, validated parent DAGs, versioned component
  values, canonical asset dependencies, and detached immutable ownership.
- Compile through an explicit `ComponentRegistry` into ordinary
  `entity.spawn` commands in one existing atomic `CommandTransaction`.
- Store compiler-owned scene provenance as ordinary canonical `SceneNode` ECS
  data and expose local-ID-to-runtime-entity mapping through receipt aliases.
- Preserve the world store as sole canonical runtime authority and retain
  existing owner-thread, staging, receipt, and failure semantics.
- Add structured scene failures, focused unit/integration/property/architecture
  coverage, RFC-0102, aligned public docs, and a standalone installed-wheel
  verifier without changing the existing hosted smoke allocation.
- Keep workflows, runner allocation, actions, permissions, credentials,
  dependencies, lock, metadata, version, root API, command operations,
  providers, release authority, tags, releases, publication, and public remote
  state unchanged.

## Evidence so far

- Primary-source direction review used RFC 8259, JSON Schema Core draft
  2020-12, and RFC 3986. The selected contract reuses canonical JSON,
  `asset://`, component-schema migration, and ordinary world transactions
  without adding a runtime schema dependency.
- Exact CPython 3.12.13 behavioral deliberate red failed collection only because
  `ludoweave.scene` was absent. The first architecture red passed protected
  surfaces and failed only absent package/dependency-rule/docs boundaries.
- The first implementation launch exposed postponed component annotations in
  the new component definitions; removing postponement only where schemas are
  declared preserved the existing authoring contract.
- The next run passed 17 assertions and exposed two test/ordering defects: the
  session hash is a property, and reserved `SceneNode` detection must precede
  component-value compilation. Both were corrected.
- The following run passed 18 assertions and exposed only the test's use of a
  nonexistent `WorldStore.entity_count`; the test now uses the storage-neutral
  `entities()` contract. Strict type checking then identified only new-test
  typing gaps, which were repaired without product relaxation.
- Focused behavior first passed 19 assertions with zero strict type findings.
  Architecture then passed 102 assertions and failed only absent M119 docs.
  Strict docs built in 1.75 seconds; the first documented boundary failed one
  plain-phrase assertion because Markdown code formatting interrupted the
  phrase. The corrected architecture boundary passed all 103 assertions.
- After direct-construction/plan-identity hardening, Hypothesis coverage, and a
  standalone wheel verifier, Ruff, strict Pyright, and all 124 focused
  behavior/architecture assertions pass in 1.39 seconds.
- RFC-0102 and public docs explicitly define dependency direction, ownership,
  deterministic ordering, structured pre-mutation failures, receipt alias
  mapping, canonical world authority, and the no-file-I/O/no-prefab boundary.

## Explicit non-scope

- No scene file loading, directory discovery, prefab inheritance/overrides,
  prefab instantiation operation, live update/reimport, silent propagation,
  runtime `EntityRef` facade, asset loading, or parent-to-runtime-handle store.
- No arbitrary Python graph, evaluation or import; no scene-specific persistent
  operation; no second authority; no renderer, provider, tool, application,
  networking, editor, native, compiler, or global registry surface.
- No workflow, hosted allocation, dependency, lock, metadata, version, root API,
  release authority, tag, release, publication, push, or PR.

## Remaining acceptance work

- Commit the reviewed slice with exact DCO identity and verify the resulting
  standalone history/tree/scope.
