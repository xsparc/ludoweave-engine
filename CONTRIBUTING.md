# Contributing to LudoWeave Engine

Thank you for helping build LudoWeave. The project welcomes focused bug fixes, tests, documentation, and milestone-aligned design work.

## Before opening a change

1. Read [AGENTS.md](AGENTS.md), the [architecture overview](docs/architecture.md), and accepted [ADRs](docs/adr/).
2. Keep the change within one issue or milestone task.
3. Discuss public API, persistent schema, security model, native-code, renderer-backend, networking, editor, or 3D changes before implementation.
4. Do not include credentials, private prompts, model transcripts, or proprietary assets.

## Development setup

Install [uv](https://docs.astral.sh/uv/), then run:

```console
uv sync --frozen --all-groups
```

Run the complete quality suite documented in [README.md](README.md) before requesting review. Include exact commands and results; do not report unexecuted checks as passing.

## Developer Certificate of Origin

LudoWeave uses the [Developer Certificate of Origin 1.1](https://developercertificate.org/) instead of a Contributor License Agreement. Every commit must include a sign-off certifying that you have the right to submit the contribution under the project's license:

```text
Signed-off-by: Your Name <your.email@example.com>
```

Create a signed-off commit with:

```console
git commit -s
```

Use your real name or a legally recognized identity. A pull request with missing sign-offs must be corrected before merge; adding a sign-off is an attestation, not a decorative checkbox.

## Change expectations

- Type all public and core code.
- Add tests for behavior changes and documentation for public semantics.
- Keep canonical world state out of adapters and presentation code.
- Keep backend objects out of public APIs.
- Preserve headless operation and explicit resource cleanup.
- Update `CHANGELOG.md` for user-visible changes.
- Record architectural decisions as ADRs when the existing contract does not answer the question.

All participation is governed by the [Code of Conduct](CODE_OF_CONDUCT.md).
