# ADR-0003: Explicit component identity and forward migrations

- **Status:** Accepted
- **Date:** 2026-08-05

## Context

Component type identity and schema versions will become persistent data in M2 snapshots, commands, hashes, and replay. A process-global registry would make composition depend on import order and leak state across tests. Name-derived identifiers would change when Python modules or classes are renamed. Arbitrary migration graphs would create ambiguous paths and rollback behavior.

## Decision

Every component declaration supplies an explicit, nonzero UUID that is never reused for a different semantic type. The Python `module.qualname` is a diagnostic alias, not persistent identity.

`@component` validates a slotted dataclass, attaches one frozen schema descriptor, and returns the class unchanged. It does not register globally. A caller constructs an explicit immutable `ComponentRegistry` from the complete component set. The registry validates unique UUIDs, qualified names, and Python classes before exposing deterministic UUID-sorted indexes.

Schema versions are positive integers. Version `N` carries one complete ordered migration chain `1→2`, `2→3`, through `N-1→N`. Migrations are named module-level callables over copied scalar mappings. Only forward migration to the registered current version is supported. The framework selects and preflights the path deterministically, prevents mutation of each input mapping, chains callable failures, and validates current fields and scalar values. Migration purity remains a trusted author-code responsibility.

M1 supports `bool`, `int`, finite `float`, `str`, and optional forms as component fields. Defaults are matching immutable literals; factories and unresolved postponed annotations remain unsupported until the canonical codec contract is defined.

Authoritative schemas use canonical serialization metadata and determinism tier D1 or D2. D0 and serialization exclusion are available only to non-authoritative schemas. Storage hints remain backend-neutral.

## Consequences

- Schema identity survives Python renames when the UUID is preserved.
- No registry behavior depends on import order or mutable global state.
- M2 receives one unambiguous forward migration path for legacy raw component records.
- A released UUID must never be reused, a released version must never be decremented, and all historical forward edges must be retained.
- Older releases cannot read newer schemas unless they already contain a compatible reader; rollback is not a downgrade migration.
- The initial field domain is intentionally narrow and can be expanded only with an explicit codec-compatible decision.
