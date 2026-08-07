# Decisions Pending

No architecture decision is currently blocked.

RFC-0017 resolves how agent-tool recovery-rate evidence is admitted. The
offline harness requires a complete reviewed cohort of task-directed sessions
and every dispatched call, keeps known failure and manual-recovery outcomes in
the denominator, blocks publication on unobserved terminal state, and preserves
complete history. The reviewed manifest is empty, so no measured rate or
recovery-free result exists. Human review owns session/call eligibility,
manual-recovery status, outcome, provenance, validation, and census
completeness. The eight essential CI jobs now run only for substantive pull
requests, avoiding redundant post-merge and `.project/**`-only runs.

RFC-0001 resolves the M7 first-native-kernel question by deferring Rust/PyO3
until its quantified cross-platform, buffer/GIL, ownership, build, fallback,
fuzz, and maintenance-owner gate is satisfied.

ADR-0023 resolves the M8 SDL3 question by using the already-pinned GLFW gamepad
surface and deferring SDL3 until a stable Python binding, auditable offline
binary delivery, explicit lifecycle ownership, cross-platform conformance, and
maintenance owner are evidenced.

ADR-0024 resolves the M9 Box2D question by deferring the preview binding until
the complete CPython/OS wheel and provenance matrix, stable API, lifecycle and
stale-object soak, documented GIL/thread ownership, cross-platform
snapshot/replay classification, copied engine adapter conformance, and a named
maintenance owner are evidenced.

ADR-0025 resolves the M10 inspector boundary with one isolated, owned local
MCP child, detached semantic observations, explicit receipted writes, exact
hash continuity, and no arbitrary process, network, remote-attach, or editor
surface.

RFC-0002 resolves the M12 plugin boundary with canonical inert manifests,
explicit environment/policy/dependency checks, and no discovery, import,
execution, installation, or ambient global registry.

ADR-0027 resolves the M13 rollback/network-snapshot question by admitting only
a bounded offline correction-branch proof and deferring transport/live rollback
until canonical tick-input history, protocol/security, cross-platform network
simulation, resource budgets, lifecycle ownership, and maintenance gates are
complete.

ADR-0028 resolves the M14 constrained-3D question by retaining layered 2D and
deferring any 3D runtime until a bounded product slice, provider-neutral
spatial/render/asset contracts, canonical agent/replay semantics, equivalent
Null behavior, cross-platform installed conformance, measured resource
budgets, lifecycle ownership, and a named maintainer are evidenced together.

ADR-0029 resolves the M15 visual-editor question by retaining the finite
headless inspector and deferring GUI/editor implementation until public
compatibility, document/scene, selection/hierarchy, undo/conflict, property,
viewport, asset, recovery, accessibility/usability, cross-platform packaging,
resource-budget, and maintenance-owner gates are evidenced together.

ADR-0030 resolves the M16 WASM-mod question by retaining the inert M12 plugin
boundary and deferring executable guests until runtime provenance/support,
package identity/distribution, default-deny copied capabilities,
command/receipt mutation mapping, bounded execution, atomic trap/lifecycle,
deterministic replay, guest-state migration, isolation, adversarial
conformance, cross-platform installation, and named security/update ownership
are evidenced together.

ADR-0031 resolves the first external-adapter conformance boundary with one
versioned installed `RenderDevice` baseline over an explicitly supplied trusted
factory. It forbids discovery/loading/installation and records that passing
behavior is not security, provenance, cross-platform, performance, or provider
admission evidence. No independently authored adapter is counted until
external evidence is reviewed.

ADR-0032 resolves the installed agent-adapter conformance boundary with one
versioned 12-tool baseline over an explicitly supplied trusted factory. It
forbids discovery, dynamic import, installation, subprocesses, networking, and
global registration, and records that a project-owned pass is reference
behavior rather than security, provenance, external adoption, cross-platform,
performance, or manual-recovery evidence.

RFC-0003 resolves the first central API-stability candidate by retaining the
command, transaction, and receipt contracts as experimental. Same-version
canonical/atomic behavior is confirmed, but preview promotion remains gated on
a cross-version corpus, external consumer feedback, operation and receipt-field
evolution rules, a bounded public receipt reader, and a supported deprecation-
capable feature-release channel.

RFC-0004 resolves the bounded-reader gate with a strict resource-limited
decoder for the unchanged receipt/1 graph and immutable committed, dry-run,
and rejected fixtures from `0.1.0a1`. This satisfies only gate 4 of RFC-0003.
The fixture set is explicitly a single-version baseline; cross-version
compatibility, external adoption, evolution rules, a release channel, and
stability promotion remain unresolved.

RFC-0005 resolves the built-in operation-argument policy gate. Exact required
and optional fields, unknown-field rejection, and named semantic rules are
fixed per operation/version identity; a breaking change uses a new operation
version and a new identity is additive. This satisfies only gate 3 of
RFC-0003. Cross-version history, external feedback, receipt semantic-diff/
diagnostic evolution, and a supported deprecation release channel remain
unresolved.

RFC-0006 resolves the receipt semantic-diff and diagnostic-code policy gate.
Exact v1 field sets, presence, ordering, and meanings cannot change in place;
existing code meanings are fixed, new well-formed codes are additive, and
phase/message/scalar detail metadata is non-authoritative. This satisfies only
gate 5 of RFC-0003. Cross-version history, external feedback, and a supported
deprecation release channel remain unresolved.

RFC-0007 resolves how cross-version receipt-corpus evidence is admitted. The
offline harness preserves exact historical identities and requires a distinct
installed reader version plus supported-release records for every observed
version. Its current result is explicitly false because all evidence is
`0.1.0a1` and the release set is empty. Actual cross-version history, external
feedback, and a supported deprecation release channel remain unresolved.

RFC-0008 resolves how external-consumer-feedback evidence is admitted. The
offline harness requires manually reviewed independent-consumer records with
exact public repository, revision, protocol, outcome, and artifact identities;
the evaluator verifies only the frozen data contract and cannot establish
independence by itself. The reviewed manifest is empty, so actual external
feedback and adoption remain absent. Cross-version history and a supported
deprecation release channel also remain unresolved.

RFC-0009 resolves how supported deprecation-capable feature-release-channel
evidence is admitted. The offline harness requires two reviewed supported,
non-yanked final releases on distinct feature lines with exact publication
identities and append-only history. The reviewed manifest is empty, so the
actual channel remains absent. Cross-version release execution and external
consumer feedback also remain unresolved; no stability promotion is implied.

RFC-0010 resolves how the first-external-contribution documentation objective
is admitted. The offline harness requires at least one manually reviewed human
good-first contribution linked to a public project issue and merged pull
request, with exact Git/patch/feedback identities, DCO, documented validation,
no private maintainer knowledge, and no public-API, persistent-format,
dependency, or workflow change. The reviewed manifest is empty, so actual
external-contributor usability evidence remains absent. The evaluator cannot
establish independence or undisclosed assistance; human review owns those
facts, and no synthetic fixture or CI pass is an external contribution.

RFC-0011 resolves how externally authored sample games are admitted as a
longer-term adoption metric. The offline harness requires manually reviewed
independent authorship, immutable public provenance, installed-wheel headless/
command-receipt/replay evidence, distinct artifact identities, and reviewed
licensing while preserving exact complete history. The reviewed manifest is
empty, so the current external sample-game count remains zero. Project-owned
examples, maintainers, agents, CI, and synthetic fixtures are not adoption.

RFC-0012 resolves how external contributor-retention evidence is admitted. The
offline harness requires the same independently reviewed external human to
complete distinct first and later merged public contributions with exact
issue/PR/revision/artifact identities, chronology, DCO, validation, provenance,
and complete history. The reviewed manifest is empty, so retained-contributor
and return-contribution counts remain zero; popularity and synthetic fixtures
are not retention.

RFC-0013 resolves how published-wheel installation-matrix evidence is admitted.
The offline harness requires one immutable public pure-Python release wheel to
pass reviewed clean isolated installation and installed checks across the exact
practical OS/CPython matrix with complete history. The reviewed manifest is
empty, so source-checkout CI, local builds, and synthetic fixtures are not
published installation success.

RFC-0014 resolves how issue-response and pull-request-review latency evidence
is admitted. The offline harness requires a complete reviewed public cohort of
eligible external-human issues and pull requests, preserves pending items,
binds first qualifying human-maintainer actions to exact frozen evidence and
timestamp/latency agreement, and preserves complete history. The reviewed
manifest is empty, so no latency aggregate, responsiveness result, SLA, or
support claim exists. The evaluator cannot establish human roles, participant
distinctness, first-action state, or census completeness; manual review owns
those facts.

RFC-0015 resolves how CI replay-divergence-rate evidence is admitted. The
offline harness requires a complete reviewed public cohort of eligible replay
executions, preserves cancellation, early failure, skips, and missing result
evidence as non-executed, binds verified/diverged outcomes to exact workflow,
case, and frozen result identities, and preserves complete history. The
reviewed manifest is empty, so no measured rate or zero-divergence result
exists. Human review owns cohort completeness, eligibility, outcome,
provenance, and validation.

RFC-0016 resolves how benchmark-regression-rate evidence is admitted. The
offline harness requires a complete reviewed controlled cohort of paired
registered M1-M4 `perf_counter_ns` p95 comparisons, binds exact base/head
sources and frozen runner/result artifacts, requires predeclared integer
tolerances, preserves non-execution, and preserves complete history. M7
cProfile output is diagnostic and ineligible. The reviewed manifest is empty,
so no measured rate or zero-regression result exists. Human review owns runner
control, parameter equality, eligibility, comparability, tolerance
predeclaration, outcome, provenance, validation, and census completeness.

Operational follow-ups outside repository implementation:

- Verify and reserve the `ludoweave` package name before the first publication.
