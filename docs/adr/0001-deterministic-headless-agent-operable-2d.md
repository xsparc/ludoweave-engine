# ADR-0001: Deterministic, headless-first, agent-operable 2D scope

- **Status:** Accepted
- **Date:** 2026-08-04

## Context

A general-purpose Python replacement for mature 2D/3D engines would create too much surface before the project proves a differentiated, reliable workflow. LudoWeave needs a narrow identity that aligns Python authoring, deterministic testing, and safe software-agent operation.

## Decision

LudoWeave will target deterministic 2D and layered-2D games and simulations. Headless operation has equal standing with graphical operation. Python is the primary authoring language, and normal CPython is the baseline.

The future ECS/world store will own canonical runtime state. Every externally initiated world mutation must eventually be representable as a versioned, validated command and produce a receipt usable by humans, tests, replay, CLI tools, and software-agent adapters.

Presentation state, GPU resources, wall-clock timestamps, audio-device state, and tooling selections are not canonical simulation state. Determinism guarantees will be tiered and will not overclaim bit-identical GPU output or arbitrary cross-platform floating-point behavior.

M0 establishes only the repository and lifecycle skeleton. It does not implement ECS, the command protocol, WebGPU, MCP, physics, audio, networking, editor tooling, or native acceleration.

## Consequences

- Every milestone must include a headless acceptance path.
- Agent access will be a typed adapter over engine domain services, never arbitrary evaluation.
- Scope growth into networking, 3D, a visual editor, mandatory physics, or native code requires later evidence and the appropriate RFC.
- A smaller initial feature set is accepted in exchange for testability, auditability, and a credible vertical slice.
