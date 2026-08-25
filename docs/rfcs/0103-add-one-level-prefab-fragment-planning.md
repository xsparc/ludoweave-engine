# RFC-0103: Add one-level prefab fragment planning

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

M119 adds bounded versioned scene documents and deterministic planning into
ordinary world transactions. The engine still lacks a reusable data-only scene
fragment and an explicit way to apply instance-specific values without
mutating source data or bypassing the command/receipt boundary.

General JSON Patch supports ordered add, remove, replace, move, copy, and test
operations addressed by JSON Pointer. LudoWeave's current canonical component
domain is deliberately narrower: registered flat scalar/optional fields with an
existing current-version `component.patch` contract. A general pointer language
would add unused path, array, move/copy, and partial-update semantics.

Multi-level prefab systems also require an apply-target policy. Official Unity
documentation describes source-versus-nearest-source choices for overrides in
nested prefabs and variants. That ambiguity is unnecessary for the first
reusable fragment contract.

## Decision

Add exact `ludoweave.prefab/1` documents with root fields `$schema`,
`prefab_id`, `entities`, and `dependencies`. Entities and dependencies reuse
the complete M119 scene-fragment invariants: stable local IDs, unique names,
acyclic local parents, versioned named components, canonical `asset://`
identities, deterministic ordering, detached ownership, duplicate-member
rejection, and hard resource maxima.

Add exact `ludoweave.prefab-instance/1` documents with root fields `$schema`,
`prefab_id`, `instance_id`, and `overrides`. Each override names one stable
local ID, one component qualified name, the exact current component schema
version, and a non-empty `changes` object. Override targets are unique and
canonically ordered. Only existing component fields may be replaced; M120 does
not add/remove components, entities, or parent relationships.

`compile_prefab()` receives both immutable documents, an explicit
`ComponentRegistry`, and the existing transaction identities. It verifies the
source identity, migrates each base component to its registered current schema,
applies and validates the schema-aware field replacements, adds compiler-owned
`PrefabNode` source provenance, then delegates to the M119 scene planner. The
result contains ordinary `entity.spawn` commands in one existing atomic world
transaction. Receipt aliases return the deterministic local-ID-to-runtime-
entity mapping.
In plain protocol terms, the plan contains ordinary entity.spawn commands.

The stored `PrefabNode` contains the prefab ID, instance ID, and local ID.
`SceneNode` continues to contain the fragment name and parent provenance. Both
are ordinary canonical ECS components. Canonical runtime state remains in the
world store; documents, overrides, plans, and source fragments are detached
inputs, not a live linked authority.

## Determinism, failure, and ownership

Fragment, dependency, and override source ordering cannot affect canonical
bytes or command bytes. Plan identity depends only on canonical effective
fragment values and explicit world, transaction, actor, and instance inputs.
No wall-clock time, random value, environment, path, discovery, global
registry, provider, or backend participates.

Malformed documents, source mismatch, duplicate targets, missing entities or
components, non-current override versions, unknown fields, invalid values,
reserved provenance, missing schemas, and limit excesses raise structured
`PrefabError` before a transaction exists. A later stale hash or other
transaction rejection preserves the existing staged all-or-nothing behavior.

The caller owns the immutable documents and returned plan. Planning owns no
world, file, loader, provider, thread, renderer, or closeable resource. World
session owner-thread and close behavior remain unchanged.

## Boundary

M120 is one-level composition: a prefab is exactly one fragment and an
instance document applies exactly one override set. There is no nested prefab
inheritance, variant chain, parameter expression, file I/O, asset loading,
source discovery, live update, reimport, silent propagation, write-back to a
source fragment, runtime link graph, or `EntityRef` facade.

There is no new persistent operation. Instantiation compiles to the already
versioned ordinary `entity.spawn` commands so command outcomes and receipt
aliases remain inspectable. No command registry, transaction service,
dependency, lock, metadata, version, root-package API, renderer, tool, provider,
workflow, hosted allocation, release authority, tag, release, publication, or
public remote state changes.

## Consequences

- Games can deterministically reuse a bounded authoring fragment with
  instance-specific values while retaining canonical ECS authority.
- Overrides share the current component schema and validation model rather
  than introducing a second patch language.
- Updating a source document never mutates existing runtime entities. A caller
  must explicitly instantiate another receipted transaction.
- Nested composition and general JSON Pointer/Patch remain deferred until the
  component value domain and real use cases justify their conflict semantics.
- All new exports remain experimental.

## Alternatives considered

- Adopt complete RFC 6902 JSON Patch. Rejected for M120 because move, copy,
  remove, array addressing, and general JSON Pointer semantics exceed the flat
  registered component field domain.
- Add a `scene.instantiate` or `prefab.instantiate` persistent operation.
  Rejected because deterministic expansion to ordinary spawn commands provides
  finer per-entity receipt evidence without changing the operation registry.
- Retain a live source-instance link and propagate prefab changes. Rejected
  because it creates a second runtime authority and silent mutation policy.
- Support nested prefab inheritance and variants. Rejected because multi-level
  apply targets and conflict precedence require a separate accepted contract.
- Resolve prefab/component identities through global discovery or imports.
  Rejected because composition ownership and data-only safety require explicit
  supplied values and registries.

## References

- [RFC 6902: JavaScript Object Notation Patch](https://datatracker.ietf.org/doc/html/rfc6902)
- [RFC 6901: JavaScript Object Notation Pointer](https://datatracker.ietf.org/doc/html/rfc6901)
- [Godot PackedScene stable documentation](https://docs.godotengine.org/en/stable/classes/class_packedscene.html)
- [Unity prefab introduction](https://docs.unity3d.com/Manual/prefabs-introduction.html)
- [Unity overrides at multiple levels](https://docs.unity3d.com/ru/current/Manual/PrefabOverridesMultiLevel.html)
- [RFC-0102: data-only scene transaction planning](0102-add-data-only-scene-transaction-planning.md)
- [ADR-0003: component identity and migrations](../adr/0003-component-identity-and-migrations.md)
- [Persistent command protocol](../commands.md)
