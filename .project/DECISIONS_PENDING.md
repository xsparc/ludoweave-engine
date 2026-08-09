# Decisions Pending

No architecture decision is currently blocked.

RFC-0034 resolves M51 public release negotiated TLS-session conformance. Every
fixed API or redirected asset connection advertises only `http/1.1` and, after
actual connected-peer validation but before HTTP transmission, requires exactly
TLSv1.2 or TLSv1.3, a well-formed cipher report with at least 128 secret bits,
no TLS compression, and ALPN `http/1.1` or no negotiated ALPN. There is no
cipher-name allowlist, workflow/dependency/release mutation, or authority
change. A real pass remains pending an explicitly authorized signed-tag release
execution.

RFC-0033 resolves M50 public release TLS key-log isolation. Every public API or
asset hop receives a new explicit verified client context with system
server-auth roots, certificate/hostname validation, TLS 1.2 minimum, strict
X.509 flags, and disabled key logging. An ambient `SSLKEYLOGFILE` remains
unchanged and cannot create or receive secrets from the verifier. No custom
trust store, pin, workflow, dependency, release mutation, or authority change
is introduced. A real pass remains pending an explicitly authorized signed-tag
release execution.

RFC-0032 resolves M49 public release connected-peer confinement. Every fixed
API or redirected asset connection validates the actual port-443 TLS socket
peer before HTTP transmission and permits only globally reachable unicast IPv4
or IPv6, with IPv4-mapped IPv6 classified by its embedded address. A
non-global peer has one stable forbidden code; timeout and malformed/unavailable
peer inspection retain the request timeout/failure taxonomy. No hostname/IP
allowlist, separate DNS preflight, workflow, dependency, release mutation, or
authority change is introduced. A real pass remains pending an explicitly
authorized signed-tag release execution.

RFC-0031 resolves M48 public release HTTP response conformance. The fixed
release-document request accepts only direct `200`; asset-ID requests accept
direct `200` or at most three bounded `302` responses. API-only headers remain
on `api.github.com`; timeout, other transport/protocol, and local-output
failures have distinct stable codes. All M47 identity, TLS, path, size,
validation, smoke, workflow, allocation, and authority bounds remain. A real
pass remains pending an explicitly authorized signed-tag release execution.

RFC-0030 resolves M47 cross-platform public consumer rehearsal. One typed
standard-library Python verifier replaces the Bash-only public path and the
existing tag-only fresh-consumer job expands to Ubuntu, Windows, and macOS.
Each runner creates a bounded plan, retrieves exact public bytes without a
release credential, and runs complete installed release smoke. The result
remains same-workflow/provider rather than independent/external evidence. Two
tag-only allocations are added; pull-request allocations, release authority,
runtime, dependency, package, and public API remain unchanged. A real pass
remains pending an explicitly authorized signed-tag release execution.

RFC-0029 resolves M46 fresh-runner consumer rehearsal. After the publishing
job succeeds, one additional read-only Linux job receives only the verified
release ID/version, retrieves the exact same-workflow admitted candidate,
creates a fresh bounded plan, repeats public byte validation without a release
credential, and runs installed release smoke. This is not independent/external
or cross-platform verification and adds no release mutation, publication
authority, pull-request CI allocation, runtime, dependency, or package change.
A real fresh-runner pass remains pending an explicitly authorized signed-tag
release execution.

RFC-0028 resolves M45 public release consumer-path integrity. The publishing
job performs bounded credential-free exact-ID public retrieval, revalidates the
downloaded candidate, and runs complete installed release smoke. This is one
same-run observation, not independent/external or cross-platform evidence,
future availability, immutability, artifact security, PyPI, or a supported
channel. A real public-path pass remains pending an explicitly authorized
signed-tag release execution.

RFC-0027 resolves M44 published release attestation integrity. The existing
release job will verify SLSA v1 provenance for every exact M43-retrieved asset
and an SPDX 2.3 SBOM attestation for exactly one pure wheel after publication.
The verifier fixes repository, signer workflow, tag/source identity, signer
commit, GitHub OIDC issuer, hosted-runner class, predicate, bundle count,
process count, timeout, and content-silent output bounds. No authority exists
to create a tag/release, change attestation creation, retry or roll back failed
publication, enable immutability, publish to PyPI, claim artifact security,
independent builds, or predicate truth, or promote a supported release channel.
A real attestation pass remains pending an explicitly authorized signed-tag
release execution; local and pull-request validation cannot substitute for
that hosted evidence.

RFC-0026 resolves M43 published-asset retrieval integrity. Protocol `/4`
requires unique bounded numeric asset IDs and may write one exclusive
published-only retrieval plan after complete verification. The existing tag job
retrieves every exact ID through the authenticated binary API and rehashes the
downloaded directory against the same published document. Failure is observed
after publication and performs no rollback or mutation. The result is one
authenticated point-in-time byte observation, not unauthenticated/global/future
availability, immutability, consumer installation, or attestation evidence.
Jobs, runners, actions, permissions, triggers, dependencies, credentials, tags,
releases, uploads, cleanup, and publication authority remain unchanged.

RFC-0025 resolves M42 published-prerelease observation. The exact numeric
release database ID now crosses the existing publish transition, after which
one read-only authenticated request must report public prerelease state, a
valid UTC publication time, and unchanged notes/assets. Protocol `/3` makes
draft/published state explicit. Failure blocks a successful release-job result
but performs no automatic rollback, deletion, or mutation. Jobs, runners,
actions, permissions, triggers, dependencies, credentials, tags, releases,
uploads, publication authority, and immutable-release policy remain unchanged.

RFC-0024 resolves M41 release-notes body integrity. The existing bounded M40
validator now requires authenticated draft `body` text to exactly equal the
fixed staged `RELEASE_NOTES.md` supplied through `--notes-file`, while emitting
no note content. The internal protocol advances to `/2`; both workflow files,
runner allocations, actions, permissions, triggers, dependencies, credentials,
API calls, tags, releases, and publication authority remain unchanged. Rendered
Markdown, link and factual-content review, immutable-release policy, PyPI, and a
supported release channel remain separate decisions.

RFC-0023 resolves M40 draft-release asset integrity. The existing tag job makes
its final draft/upload/publish sequence explicit and publishes only when a
bounded standard-library validator confirms the authenticated GitHub draft has
the exact local asset names, complete upload state, byte sizes, and SHA-256
digests. Failed verification remains an unpublished draft and assets are never
clobbered or automatically deleted. The gate adds no runner, action, permission,
trigger, dependency, credential, tag, release, or publication authority.
Independent remote download/storage verification, immutable-release policy,
PyPI, and a supported release channel remain separate decisions.

RFC-0022 resolves M39 release-tag identity enforcement. GitHub's annotated-tag
API is the hosted signature-verification authority, while local Git independently
checks the exact tag object, checkout commit, and `origin/main` ancestry before
the existing tag job performs expensive or publishing work. The bounded gate
adds no runner, action, permission, trigger, dependency, credential, tag, or
publication authority. A local trust store, signer/key allowlist, immutable-
release policy, PyPI channel, and supported-release claim remain separate
decisions.

RFC-0021 resolves M38 distribution reproducibility enforcement. The existing
Linux pull-request and tag-release distribution jobs build twice and compare
the exact pure wheel/source pair before smoke, staging, attestation, or
publication. A same-source/same-job byte match is required; cross-platform or
hermetic reproducibility, independent rebuilding, provenance, and publication
are not claimed. A separate rebuild runner and attestation changes are rejected
for this bounded milestone.

RFC-0020 resolves M37 CI change qualification with an exact trusted-base
classifier. Documentation-only work retains one Linux quality/docs/
architecture/distribution allocation; substantive work retains all three M36
allocations and eight slices. Windows/macOS depend on successful Linux
qualification, so an early failure consumes no desktop allocation. The
accepted tradeoff is later substantive desktop feedback. Workflow-level docs
filtering is rejected because GitHub documents a required-check pending risk;
a separate filter job is rejected because it adds a fourth allocation.

RFC-0019 resolves M36 CI runner ownership by preserving all eight existing
validation slices inside three OS-owned allocations. Ubuntu runs quality/
distribution, 3.12 graphics, and sequential 3.13/3.14 compatibility. Windows
and macOS each run 3.12 graphics followed by 3.14 compatibility. The accepted
tradeoff is less per-slice parallelism and rerun granularity in exchange for
five fewer runner allocations and repeated setups. No billed-minute saving is
claimed before hosted evidence; no coverage slice is removed.

RFC-0018 resolves how third-party conformance-adoption evidence is admitted.
The offline harness counts distinct independent external implementation
identities only after a complete project-accepted submission-census review and
a passing exact installed M17-M19 profile. Project-owned and maintainer-
authored references never count. Plugin-backed evidence is limited to the
existing M12 `render.device` capability and requires both compatible inert
manifest evidence and a passing render profile. Failed and not-executed
submissions remain in complete history. The reviewed manifest is empty, so the
current passing count is zero and no ecosystem, support, certification,
security, performance, or global-discovery result exists.

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
