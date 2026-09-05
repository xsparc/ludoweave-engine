# RFC-0102: Add data-only scene transaction planning

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

LudoWeave already has explicit immutable component schemas, canonical bounded
JSON, atomic world transactions, `entity.spawn`, semantic receipts, and
project-confined `asset://` identities. It does not have a scene format. Games
therefore have no portable declarative way to describe a named hierarchy and
compile it into the same world-command path used by direct Python, tools, and
future adapters.

An arbitrary Python object graph would make loading execute code and would
couple persistence to import paths and live objects. A scene-owned runtime graph
would also compete with the ECS/world store for authority. A scene operation in
the persistent command registry would duplicate the already sufficient atomic
spawn protocol and obscure the component-level receipt evidence.

RFC 8259 permits implementations to encounter duplicate object member names
but describes interoperable objects as having unique names. JSON Schema
2020-12 supplies the vocabulary model for exact property sets and reusable
versioned schemas, without requiring a runtime dependency. RFC 3986 defines
generic URI syntax; LudoWeave's established `asset://` subset remains the
project-confined dependency identity.

## Decision

Add `ludoweave.scene/1` as a bounded versioned data-only scene document. Its
exact root fields are:

- `$schema`: exact `ludoweave.scene/1`;
- `scene_id`: bounded stable identity;
- `entities`: local entity declarations;
- `dependencies`: distinct canonical `asset://` identities.

Each entity has a stable local ID compatible with transaction aliases, a
unique bounded name, an optional parent local ID, and component records keyed
by stable module-qualified schema name. Each component record has an exact
positive version and a canonical JSON object of values. Unknown fields,
duplicate JSON members, duplicate local IDs/names/dependencies, missing or self
parents, parent cycles, invalid asset identities, and configured limit excesses
fail closed. Normalization sorts entities by local ID, component records by
qualified name, and dependencies by URI. Callers may tighten resource limits
but cannot enlarge the format's hard maxima.

Add a deterministic compiler that accepts an explicit `ComponentRegistry`,
world ID, transaction ID, actor, and instance ID. It resolves every named
component, uses the registry's existing migration and current-value validation,
and injects a reserved compiler-owned `SceneNode` component containing scene,
instance, local ID, name, and parent-local-ID provenance. It emits ordinary
`entity.spawn` commands in one existing `CommandTransaction`. Receipt aliases
return the local-ID-to-runtime-entity mapping after atomic application.
In plain protocol terms, the plan contains ordinary entity.spawn commands.

Canonical runtime state remains in the world store. Scene documents and plans
are immutable caller-owned input values, not runtime authority. `SceneNode` is
ordinary canonical ECS data. The compiler owns no world, file, asset loader,
renderer, thread, or closeable resource.

## Determinism and failure behavior

Canonical scene bytes are independent of source entity, component, and
dependency order. Command order follows normalized local IDs. Component
payload order follows persistent type UUID text, and command IDs derive from
the canonical scene plus explicit plan identities. No wall-clock time,
filesystem state, random input, global registry, provider discovery, or backend
object participates.

Document errors use structured `SceneError` codes and immutable contextual
fields. Planning validates registry membership and every component value before
returning a transaction. Transaction application remains the existing staged
all-or-nothing service: an unknown schema, incompatible migration/value,
reserved `SceneNode` declaration, missing `SceneNode` registration, invalid
plan identity, or later transaction rejection cannot partially adopt world
state.

Parent references remain stable local provenance. M119 does not silently turn
them into mutable entity handles or create a second relationship store. Callers
use receipt aliases when runtime IDs are needed.

## Boundary

M119 has no file I/O, no directory traversal, no scene discovery, no asset
loading, no prefab inheritance, no prefab override or composition, no live
update/reimport behavior, no silent propagation, no runtime `EntityRef` facade,
no arbitrary Python evaluation/import, and no scene-specific persistent
operation. It adds no renderer, provider, tool, application, networking,
editor, native, or compiler surface.

There is no dependency, lock, package metadata, version, root-package export,
workflow, runner allocation, action, permission, credential, release authority,
tag, release, publication, or public remote-state change. All new Python
exports are experimental.

## Consequences

- Authors can persist and compare deterministic data-only scene inputs without
  creating a parallel runtime state model.
- Direct Python and future adapters share the existing typed command and receipt
  path rather than receiving a privileged loader mutation path.
- Component compatibility remains composition-owned and explicit; a document
  cannot import or discover a component class.
- Asset dependencies are visible and validated as logical identities, but the
  caller remains responsible for resolving or loading them before application
  when its composition requires that.
- A scene with no entities can be represented, but compilation cannot produce
  the non-empty transaction required by the existing command contract.
- Future prefab work must use explicit fragments/overrides and an instantiation
  command or equally reviewable receipt boundary; it cannot silently mutate
  already-instantiated worlds.

## Alternatives considered

- Deserialize arbitrary Python object graphs. Rejected because imports and
  constructors execute code, make schemas implicit, and weaken portability.
- Make a scene graph the runtime authority. Rejected because the ECS/world
  store is the canonical state owner.
- Add `scene.load` as a built-in world operation. Rejected because deterministic
  planning to existing spawn commands provides finer validation and receipt
  evidence without expanding the command registry.
- Resolve names through a process-global component registry. Rejected because
  composition ownership and test isolation require an explicit registry.
- Implement prefab inheritance together with scenes. Rejected because fragment
  identity, override semantics, mapping receipts, and update policy need a
  separate bounded design and tests.
- Add a JSON Schema runtime dependency. Rejected because the current typed
  decoder can enforce the exact v1 shape and shared limits without increasing
  the runtime supply chain.

## References

- [RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format](https://datatracker.ietf.org/doc/rfc8259/)
- [JSON Schema Core, draft 2020-12](https://json-schema.org/draft/2020-12/json-schema-core)
- [RFC 3986: Uniform Resource Identifier generic syntax](https://datatracker.ietf.org/doc/rfc3986/)
- [ADR-0002: dependency direction and backend isolation](../adr/0002-dependency-direction-and-backend-isolation.md)
- [Persistent command protocol](../commands.md)
