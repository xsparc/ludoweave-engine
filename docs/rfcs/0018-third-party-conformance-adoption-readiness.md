# RFC-0018: Third-party conformance-adoption readiness

- **Status:** Accepted
- **Date:** 2026-08-08

## Context

M35 addresses the design plan's final ordered longer-term metric: the number of
third-party adapters or plugins passing conformance. M17-M19 provide installed baseline
profiles for render devices, agent-tool adapters, and WorldStore
implementations. M12 provides an inert plugin manifest. All current passing
examples are project-owned references; they are not independent adoption.

Inferring external use from downloads, installed packages, repository stars,
compatible manifests, synthetic tests, or the project's own CI would fabricate
the metric. Discovering or executing ambient providers would also violate the
explicit composition and security boundaries.

## Decision

Adopt the versioned `ludoweave.adoption.third-party-conformance/1` reviewed
manifest and explicitly invoked offline evaluator described in the
[readiness guide](../third-party-conformance-adoption-readiness.md).

The manifest:

1. counts distinct implementation identities, not runs, versions, stars,
   downloads, or packages present in an environment;
2. admits only independent external implementations that are neither
   project-owned nor maintainer-authored;
3. accepts only the exact installed M17 render-device, M18 agent-tool, and M19
   WorldStore protocols/profiles and their fixed check counts;
4. admits a plugin-backed implementation only when a reviewed compatible M12
   manifest accompanies a passing `render.device` conformance result;
5. treats compatible inert manifests without adapter conformance as
   non-counting metadata;
6. binds public immutable repository, revision, wheel, report, plugin, review,
   license, CPython, platform, and LudoWeave-version evidence;
7. preserves passed, failed, and not-executed project-accepted submissions;
8. requires explicit authorship, independence, license, eligibility, outcome,
   provenance, validation, privacy, and consent review;
9. requires an explicit complete project-accepted submission-census review and
   preserves canonical order, unique implementation/report/review identities,
   bounded input, and the complete mandatory accepted-history prefix; and
10. emits only aggregate passing, failure, non-execution, kind, and profile
    counts.

Human review establishes third-party status and evidence authenticity. The
evaluator verifies only the frozen contract and cannot infer undisclosed
relationships or global ecosystem completeness. The census is explicitly the
complete set of project-accepted submissions, not every package that may exist
on the internet.

## Current result

The exact reviewed manifest has no submissions. The report is `not-ready`, the
passing implementation count is zero, and no external adapter, plugin,
adoption, support, certification, or ecosystem result is claimed.

## Consequences

- Future accepted public evidence can produce one auditable count without
  provider discovery or execution inside LudoWeave.
- Failed, cancelled, unavailable, or withdrawn-before-run submissions cannot be
  silently selected away.
- One passing environment is behavioral evidence only; it is not a support
  matrix, security review, performance result, provenance guarantee, or
  maintenance commitment.
- Plugin compatibility remains inert and cannot become executable authority or
  conformance by assertion.
- Reports remain sanitized and exclude implementation/package/author identities
  and raw evidence locations.
- No runtime, public API, protocol/profile, plugin manifest, dependency, lock,
  package version, CI topology, release, publication, certification, stability,
  SLA, or support-policy change is introduced.

## Alternatives considered

Counting the built-in Null, wgpu, direct-service, `World`, or `ReferenceWorld`
passes was rejected because they are project-owned reference evidence. Counting
compatible M12 manifests was rejected because compatibility is not behavioral
conformance. Package-index discovery was rejected because it cannot establish
authorship, exact execution evidence, or consent and would add network and
supply-chain authority. Executing submitted factories in the evaluator was
rejected because installed conformance is already an explicit caller-owned
operation and untrusted code has no in-process containment. Counting only
passes was rejected because it would hide failed and not-executed submissions.
