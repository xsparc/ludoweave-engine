# Current task

- **Task:** M120 - add bounded one-level prefab fragment planning.
- **Status:** Direction research, deliberate-red proof, implementation,
  schema/ownership review, documentation, RFC-0103, focused and complete
  source validation, supported-runtime suites, graphics slices, reproducible
  distribution, release rehearsal, package hygiene, and final scope review are
  complete. Governance/history closeout and bounded cleanup are complete. The
  final metadata separator is complete; the local DCO commit remains.
- **Base:** Fully locally validated M119 DCO commit
  `b30ca99c3ae639653394a378465c0088ee5c2995`, tree
  `8d51081377cdef16fda69c17ebbec9008b44deef`, with sole parent exact M118.
  The stack remains unpublished under the existing public-review identity hold.

## Acceptance boundary

- Add exact `ludoweave.prefab/1` scene fragments with stable local IDs and all
  bounded M119 entity/component/asset/hierarchy invariants.
- Add exact `ludoweave.prefab-instance/1` instance intent with one matching
  source ID, stable instance ID, and canonical unique override targets.
- Restrict overrides to non-empty current-schema field replacements against an
  existing local entity/component pair; migrate base values before merging.
- Add compiler-owned canonical `PrefabNode` provenance and compile through
  M119 into ordinary `entity.spawn` commands in one existing atomic
  transaction; retain receipt aliases for local/runtime mapping.
- Preserve immutable source ownership, canonical world-store authority,
  structured pre-mutation failures, owner-thread rules, and transaction
  rejection atomicity.
- Add focused unit/integration/property/architecture coverage, RFC-0103,
  aligned public docs, and a standalone installed-wheel verifier.
- Keep command/operation registry, transaction service, workflows, allocations,
  actions, permissions, credentials, dependencies, lock, metadata, version,
  root API, release authority, tags, releases, publication, and public remote
  state unchanged.

## Evidence so far

- A focused primary-source scan reviewed RFC 6902, RFC 6901, JSON Schema,
  stable Godot PackedScene behavior, and official Unity prefab/override
  behavior. It supports exact field maps and a one-level detached instantiation
  boundary rather than general JSON Patch or live nested source links.
- Static and dated strict governance checks both began with zero findings.
- Corrected exact CPython 3.12.13 deliberate red fails collection only because
  the new prefab exports are absent. The architecture red passes the protected
  command/workflow/metadata assertion and fails only the absent module,
  standalone verifier, and docs/RFC boundaries.
- Implementation feedback remains factual: the first focused launch found
  test import-order/strict-typing issues and tuple-detail access while 22
  behavior assertions passed; the next launch found only two incorrect expected
  component cause codes. Corrected focused behavior then passed all 24 tests
  with zero Ruff/Pyright findings.
- Public docs and RFC-0103 define exact schemas, canonical ordering, schema-aware
  replacements, ordinary commands, receipt aliases, world authority,
  ownership, failure behavior, and the no-nesting/no-live-update boundary.
- The first documented focused gate passed 133 assertions and strict docs.
  Findings-first review added base migration/default-instance, explicit
  provenance registry, hard-maximum, and direct-construction phase coverage.
  The tightened gate passes all 136 assertions in 1.58 seconds, strict docs in
  1.69 seconds, strict Pyright, Ruff, formatting, and whitespace.

## Explicit non-scope

- No nested prefab inheritance, variant chain, parameter expression,
  component/entity add or remove override, hierarchy override, file I/O,
  directory discovery, asset loading, live update, reimport, silent
  propagation, source write-back, or runtime source-instance link graph.
- No `EntityRef` facade, arbitrary Python graph/import/evaluation, global
  registry, scene/prefab persistent operation, renderer, provider, tool,
  application, networking, editor, native, compiler, or second authority.
- No workflow, hosted allocation, dependency, lock, metadata, version, root API,
  release authority, tag, release, publication, push, or PR.

## Remaining acceptance work

- Create the standalone DCO commit and verify its exact tree, parent, identity,
  scope, and clean worktree. Publication remains held.
