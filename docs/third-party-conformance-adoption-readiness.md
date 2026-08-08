# Third-party conformance-adoption readiness

M35 defines how LudoWeave may count independently authored third-party
adapters or plugin-backed adapters that pass an existing installed conformance
profile. The evaluator is an explicitly invoked offline evidence reader. It
does not discover packages, import providers, install wheels, execute adapter
code, query package indexes, contact authors, or run during engine operation.

Run the current reviewed evidence:

```console
uv run python examples/third_party_conformance_adoption_readiness.py
```

The committed manifest is exactly 250 bytes with SHA-256
`adee8c68b5d89923ee2682162eb24cd9542a4601b1ff6fb901709ebcc0066767`. Its
reviewed identity includes an explicit
`submission_census_complete_reviewed` assertion and contains no submissions.
The deterministic result is `not-ready` with reason
`third-party-conformance-evidence-absent`, zero reviewed submissions, and zero
passing third-party implementations. Project-owned Null, wgpu, direct agent
service, `World`, and `ReferenceWorld` passes remain reference evidence and do
not establish external adoption.

## Counted unit and accepted profiles

The counted unit is one distinct independently authored implementation
identity with a reviewed `passed` result from one exact installed profile:

| Implementation kind | Protocol | Profile | Checks |
| --- | --- | --- | ---: |
| Agent-tool adapter | `ludoweave.agent-tool-conformance/1` | `agent-tool-baseline/1` | 12 |
| Render-device adapter | `ludoweave.render-device-conformance/1` | `render-device-baseline/1` | 9 |
| Render-device plugin adapter | `ludoweave.render-device-conformance/1` | `render-device-baseline/1` | 9 |
| WorldStore adapter | `ludoweave.world-store-conformance/1` | `world-store-baseline/1` | 10 |

An implementation identity appears once in accepted history and therefore
cannot be double-counted across repeated runs. A package that contains several
independently identified implementations may submit each separately. The
aggregate report omits implementation, package, author, repository, and
artifact identities.

The existing M12 manifest is inert compatibility metadata, not executable
conformance. A plugin-backed record is admitted only for the already-recognized
`render.device` capability and requires both a compatible reviewed manifest
check and a passing render-device profile. A compatible manifest by itself
never counts. Agent-tool and WorldStore packages remain explicit adapters
because the current manifest protocol does not define matching whole-service
capabilities.

## Eligibility and evidence

Eligibility is fixed before outcome review. Every submission must be an
independent external implementation, not owned by the project or authored by a
LudoWeave maintainer. Human review owns authorship, independence, license,
eligibility, outcome, provenance, validation, privacy and consent, and the
completeness of project-accepted submission history. The evaluator only checks
the frozen bounded record.

Each submission binds:

- a public repository and exact 40-character revision;
- package, implementation, adapter, license, and implementation-kind
  identities;
- one public installed package wheel and the exact LudoWeave wheel;
- CPython 3.12-3.14 and one supported desktop platform;
- the exact conformance protocol, profile, and fixed check count;
- immutable conformance-report and project-review evidence identities; and
- for a render-device plugin adapter, immutable plugin-manifest and
  compatibility-report evidence.

Passing evidence requires every fixed check to pass. A single environment pass
does not establish a complete support matrix, security, performance,
determinism, maintenance, or provider certification.

## Failure and history preservation

Accepted history retains `passed`, `failed`, and `not-executed` submissions.
Cancellation, inability to start, unavailable execution evidence, and
withdrawal before execution are `not-executed`; they cannot disappear from the
reviewed submission count. Only `passed` implementations contribute to the
passing count. Failed and not-executed counts remain visible as aggregates.

Admission requires the exact reviewed whole-manifest SHA-256, canonical
sequential submission IDs, unique implementation/report/review identities,
complete required reviews, an explicit complete project-accepted submission
census review, and a mandatory prefix equal to all previously accepted
history. Replacing or omitting a historical submission suppresses all counts.

## Security and disclosure boundary

External factories still execute synchronously in their caller and are not
sandboxed by the conformance profiles. M35 consumes only already-produced
public reviewed artifacts and never executes those factories. Public evidence
must not contain credentials, private correspondence, personal identifiers,
local paths, environment values, provider diagnostics, or raw adapter data.

The sanitized report contains only aggregate counts, profile identities,
schema/policy identities, and admission reasons. It does not publish package,
implementation, adapter, author, repository, revision, artifact, platform, or
evidence locations.

## Boundary

M35 adds no runtime source, discovery, loader, registry, dynamic import,
installation, provider execution, network request, telemetry, plugin field,
conformance protocol/profile, public API/export, dependency, lockfile, package
version, workflow job, release workflow, tag, publication, certification,
stability label, SLA, or support promise. The existing eight essential jobs
remain the one substantive pull-request gate; `.project/**`-only records use no
hosted runner.
