# Installation-matrix readiness

No published-wheel installation matrix is currently admitted. M30 adds a
strict offline path for measuring installation success across the supported
desktop and CPython matrix without reclassifying source-checkout CI, local
builds, or synthetic fixtures as released-user installation evidence.

## What can count

A future reviewed matrix must cover exactly these practical supported
environments:

- Ubuntu with CPython 3.12, 3.13, and 3.14;
- macOS with CPython 3.12 and 3.14; and
- Windows with CPython 3.12 and 3.14.

Every environment must install the same immutable public
`py3-none-any` release wheel in a fresh isolated environment. The record must
show that no dependencies or native compiler were required and that the
installed artifact passed version, doctor, `hello_headless`, and headless
Clockwork Arena checks. Reviewers also verify the canonical project release
and wheel locations, canonical public project Actions job, exact wheel and
installation-log SHA-256 identities, CPython patch version, platform mapping,
successful outcome, provenance, and validation evidence.

The evaluator validates only frozen reviewed facts. It does not download a
wheel, query GitHub, inspect a runner, infer publication, execute installer
commands, or replace human provenance review.

## Current evidence

The reviewed manifest is exactly 462 bytes and contains zero installation
records. Its SHA-256 is
`7c05813a7304e8ff44a009ada37c8e60ff545baec633852fc332e46bdfe03c90`.
The deterministic report is therefore `not-ready`, with zero successful
environments and reason code `installation-matrix-evidence-absent`.

Run the source-tree evidence explicitly:

```console
uv run --frozen python examples/installation_matrix_readiness.py
```

The same evaluator and exact empty manifest run from an isolated wheel and the
deterministic release sample bundle. Reports omit release and wheel locations,
Python patch versions, platform values, log identities, timestamps, local
paths, host metadata, and timings. An unreviewed candidate exposes no
record-derived environment or release aggregates.

## Why current CI does not satisfy the metric

The three M36 pull-request runner allocations execute the same eight source and
locally built-artifact validation slices before merge. They are necessary
engineering gates, but they do not
prove that a public release asset exists or that independent clean installs of
that immutable asset succeeded across the supported matrix. Synthetic complete
records prove only the Boolean gate mechanics.

## History and updates

Before a nonempty manifest is accepted, reviewers must pin its complete ordered
installation identity sequence as mandatory history and pin the exact
whole-manifest SHA-256 in the evaluator and installed validator. A reviewed
manifest cannot silently add, drop, replace, reorder, or reuse an accepted
environment, release artifact, or installation log.

The manifest may contain only public project release/asset and validation-job locations,
immutable artifact and log identities, canonical public validation timestamps,
supported environment identifiers, and bounded review facts. Never add
credentials, private logs, private prompts, local paths, telemetry, or
unpublished user information.

## Boundaries

The evaluator performs one bounded synchronous read of an explicitly selected
local JSON document. It uses no networking, telemetry, discovery, dynamic
imports, subprocesses, installation, provider execution, GitHub API, or
retained external resources. Duplicate fields, more than 16 structural JSON
levels, non-ASCII values, excess records, and incompatible matrix identities
fail closed. M30 changes no runtime source, public API, dependency, lock,
version, workflow, release, tag, publication, or support policy.

See [RFC-0013](rfcs/0013-installation-matrix-admission-readiness.md) for the
accepted decision.
