# ADR-0016: provider-neutral platform events and action snapshots

- Status: Accepted
- Date: 2026-08-05

## Context

Interactive input arrives through platform providers, while headless tests and
replays need the same deterministic gameplay representation. Provider objects
cannot enter application or canonical world APIs.

## Decision

Define immutable logical-surface events in `ludoweave.platform`. Concrete
window adapters translate provider data to those records and expose a draining
method on the engine-owned render-device protocol. Application action maps
consume key, mouse, pointer, and focus records and publish immutable,
tick-indexed snapshots with transition metadata.

Only an action snapshot selected for a tick may influence simulation. Event
poll timing, resize, close, and unrecorded provider state remain presentation
data. The mapped source is sequential and single-owner.

## Consequences

Virtual, recorded, and live controls share one gameplay boundary. The wgpu
adapter can support a playable window without exposing rendercanvas or GLFW.
Applications that require replay must retain or serialize action snapshots;
raw event timing is deliberately not a replay format.
