# ADR-0017: content-addressed, project-confined assets

- Status: Accepted
- Date: 2026-08-05

## Context

Logical game content needs stable identity, deterministic invalidation, and a
safe path boundary without embedding provider handles or executing project
Python.

## Decision

Use validated `asset://` URIs and an exact data-only JSON manifest. Resolve
sources beneath an explicit project root. Derive each cache key from source
bytes, URI, kind, loader version, canonical settings, and dependency keys.
Store immutable SHA-256-addressed payload and metadata artifacts.

The M4 PNG loader supports only a bounded, CRC-verified 8-bit RGB/RGBA subset.
Hot replacement swaps immutable CPU revisions and retains the old revision
until a rendering safe point. GPU/native handles never enter manifests or
artifacts.

## Consequences

Changed content invalidates exactly its dependency closure. The first
implementation is synchronous and filesystem-backed. General importers,
watchers, databases, background build workers, and arbitrary loader plugins
are deferred.
