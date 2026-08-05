# ADR-0021: Explicit public API stability metadata

- Status: Accepted
- Date: 2026-08-05

## Context

Community alpha needs an unambiguous public surface without pretending that the
large experimental API is stable. Python's default underscore convention alone
cannot distinguish supported experimental exports from implementation names or
express future preview/stable commitments.

## Decision

An official public Python symbol is a name in a module's explicit `__all__`.
Every exporting module also defines `__stability__` with exactly the same keys
and one of `experimental`, `preview`, or `stable`. Non-exported implementation
names are internal and carry no compatibility promise.

All `0.1.0a1` exports are experimental. CI discovers every source module that
defines `__all__`, imports it, and verifies exact metadata coverage, allowed
labels, and existing attributes. Persistent protocol revisions remain separate
from Python package/symbol stability.

## Consequences

- Users and tools can inspect status without importing implementation helpers.
- A new export cannot enter the supported surface without machine-checked
  metadata.
- Alpha releases may still change experimental names, but documentation and the
  changelog must say so honestly.
- Promoting a symbol to preview/stable creates the deprecation/SemVer obligations
  in `API_COMPATIBILITY.md`; policy changes require an RFC.

## Alternatives considered

Treating every non-underscore name as public was rejected because imports and
implementation helpers would accidentally become commitments. Decorating each
object was rejected because constants and protocol aliases do not share one
mutable metadata mechanism. A separate generated manifest was rejected because
it could drift from runtime exports; the colocated mapping is checked directly.
