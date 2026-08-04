# Project State

## Current milestone

M0 — repository contract and walking skeleton — is complete in the working tree as of 2026-08-04.

## Repository identity

- Canonical target repository: `ludoweave-engine`.
- Package and CLI: `ludoweave`.
- Development version: `0.1.0.dev0`.
- License and contribution model: Apache-2.0 with DCO sign-off.
- Supported baseline: standard CPython 3.12-3.14 on Windows, macOS, and Linux; no mandatory native compiler.

## Implemented

- Public README, governance, contribution, conduct, security, changelog, NOTICE, issue/PR templates, and agent guidance.
- PEP 621 pure-Python package, uv lockfile, Ruff, strict Pyright, pytest, Hypothesis, MkDocs Material, and typed-package marker.
- Immutable engine configuration and run summary; monotonic and deterministic virtual clocks.
- Explicit single-owner engine lifecycle with initialization, fixed-tick run, shutdown, failure cleanup, idempotent close, and structured exceptions.
- Engine-owned render protocol, backend-neutral descriptor, and lifecycle-validating null renderer.
- `ludoweave --version`, structured `ludoweave doctor`, and deterministic headless example.
- Architecture overview, runtime contract, accepted ADR-0001/ADR-0002, and AST import rules that test both absolute and relative forbidden imports.
- Least-privilege GitHub Actions matrices for the supported operating systems/Python versions and installed-wheel smoke tests.

## Validation state

- Local validation completed on Windows with uv-managed CPython 3.12.13.
- The final local suite reports 44 passing tests, zero Ruff/Pyright findings, a strict documentation build, successful sdist/wheel build, and successful isolated installed-wheel smoke.
- GitHub-hosted Windows/macOS/Linux and Python 3.13/3.14 jobs are configured but have not been executed in this working tree. Their status must not be reported as passing until CI runs.
- MkDocs Material emits its upstream informational warning about the future MkDocs 2.0 project; the strict documentation build exits successfully.

## External follow-ups

- Rename the current GitHub repository to `ludoweave-engine`.
- Verify and reserve the `ludoweave` name before publishing to PyPI.
- Run the committed CI workflow after the changes are pushed through the maintainer's normal review process.

## Deferred milestones

ECS/world state, typed commands and receipts, snapshots/replay, WebGPU, MCP, physics, audio, networking, editor tooling, benchmarks, and native acceleration remain unimplemented.
