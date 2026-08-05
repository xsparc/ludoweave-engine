# ADR-0018: bounded deterministic collision and minimal audio

- Status: Accepted
- Date: 2026-08-05

## Context

Clockwork Arena needs enough collision and audio surface to prove a gameplay
vertical slice, without selecting a rigid-body engine or real-time audio
provider prematurely.

## Decision

Implement pure-Python AABB/circle overlap, a sorted spatial grid, and
axis-separated X-then-Y kinematic box resolution. Treat edge touch as
non-overlap and bound grid expansion. Validate grid queries against brute force.

Define a provider-neutral owned audio protocol for clip load, play, stop,
volume, loop, and close. Ship a strict Null adapter only. Do not execute Python
in a real-time callback.

## Consequences

The sample has deterministic movement, projectile collision, and testable
audio ownership. It does not have impulses, rotation, continuous rigid-body
physics, spatial audio, mixing threads, or Box2D. Those require later evidence
and separately accepted decisions.
