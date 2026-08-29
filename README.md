# LudoWeave Engine

**Build worlds humans can play and agents can operate.**

LudoWeave is an experimental, deterministic, headless-first Python engine for 2D and layered-2D games. Human-facing tools, tests, replay, and software agents operate the same canonical world through typed, validated commands.

> Current validation: M0 through M99 are hosted-validated and closed; M100 and
> M101 add locally validated stacked size-field consistency from that base;
> M102 adds a local compressed-payload upper bound; M103 requires exact local
> payload contiguity; M104 requires empty sample-member extra fields; M105
> requires zero sample-member general-purpose flags; M106 requires zero
> extraction-version reserved bytes; M107 requires extraction version 2.0;
> M108 requires sample-member creation version 2.0; M109 requires zero
> sample-member internal attributes; M110 retains timestamp compatibility after
> rejecting an exact verifier profile; M111 retains permission-bit
> compatibility while preserving the M65 file-type boundary; M112 retains
> creating-system compatibility without adding a host allowlist; M113 retains
> stored/deflated compression-method compatibility without an exact deflate-
> only profile; M114 retains sample-member compression-level non-observability
> without inferring an exact writer setting; M115 scopes sample-bundle byte
> reproducibility to the fixed release environment; M116 separates semantic
> portability from byte identity; M117 retains the standard CPython support
> baseline after one free-threaded serial probe; M118 retains Python 3.15
> outside the supported range after one prerelease compatibility observation;
> M119 adds bounded versioned data-only scene transaction planning; M120 adds
> one-level data-only prefab fragments and schema-aware instance overrides;
> M121 adds bounded project-confined scene file loading through the existing
> headless composition root; M122 adds two explicit project-confined prefab
> file loads with no implicit pairing or discovery; M123 adds a read-only,
> structured scene/prefab source-check CLI; M124 adds bounded explicit source
> manifests and aggregate read-only checking without directory discovery;
> M125 adds path-independent content-identity locks and exact read-only source
> verification without an import pipeline or cache; M126 adds bounded project-
> confined loading for the existing asset manifest without reading or building
> an asset source; M127 adds read-only checking from explicit scene/prefab
> asset declarations through the validated direct and transitive asset graph;
> M128 adds bounded, path-silent asset-source lock generation and verification
> without decoding, building, importing, or caching an asset; M129 adds pure
> dependency-first planning with exact existing cache-key compatibility after
> verified inputs, without executing a build or reading or writing a cache;
> M130 adds confined saved-plan loading and content-silent verification against
> freshly recomputed inputs, still without build or cache effects; M131 adds
> bounded built-in decoder execution over exact detached inputs and reports
> deterministic output identities without retaining payloads or reading or
> writing a cache; M132 adds explicit verified local cache publication with a
> payload CAS and atomically visible action metadata outside the project; M133
> adds strict read-only current-plan cache hit/miss inspection without creating
> or changing the cache or bypassing a decoder; M134 adds bounded read-only
> cache-assisted realization that verifies every source and cache candidate
> before decoding only exact misses, with no automatic cache publication;
> M135 adds an explicit post-realization population operation that acquires
> cache-write authority only after complete realization succeeds and retains
> M132's atomic per-entry publication boundary; M136 adds bounded read-only
> verification of a saved population report against the exact current plan and
> every referenced cache action, without treating local integrity as
> provenance; M137 adds bounded read-only whole-cache action/CAS integrity and
> aggregate storage inventory without cleanup authority; M138 adds a
> deterministic path-free fingerprint over one exact sequential verified
> storage observation without timestamps or deletion eligibility.
> M139 adds strict saved-fingerprint integrity verification; M140 adds a fixed,
> path-free aggregate comparison that diagnoses count/byte changes while
> retaining exact identity-only change detection.
> M141 adds offline comparison of two canonical saved fingerprints through the
> same fixed report, with no cache access after record admission.
> M142 adds strict bounded admission and offline recomputation of one saved
> comparison report against the exact plan and both admitted fingerprints.
> M143 adds a path-free unreferenced-blob preview from one existing verified
> observation without listing candidates or granting deletion authority.
> M144 reuses strict saved-fingerprint admission to produce that unchanged
> preview offline, after the originating cache is absent.
> M145 strictly admits that saved preview and verifies it against the exact
> plan and admitted fingerprint offline, without cache access or trust claims.
> M146 records why those aggregate records cannot authorize cache cleanup and
> defers mutation until identity, retention, quiescence, and policy gates exist.
> M147 adopts a dedicated [cleanup threat
> model](docs/security/cache-cleanup-threat-model.md) covering filesystem races,
> cross-platform link safety, concurrency, recovery, and safe refusal without
> adding a cleanup implementation.
> M148 rejects a portable standard-library cleanup path after a focused
> [platform-capability
> decision](docs/security/cache-cleanup-platform-capability-decision.md) and
> requires real-host adapter evidence before any platform is admitted.
> M149 adds one test-only [Windows capability
> probe](docs/security/cache-cleanup-windows-capability-probe.md). It exercises
> an owned handle-relative quarantine chain on the current host while leaving
> Windows and runtime cleanup unadmitted.
> M150 adds one test-only [Windows directory-junction
> probe](docs/security/cache-cleanup-windows-junction-probe.md). It executes a
> real NTFS reparse refusal without elevation while preserving the same no-
> admission boundary.
> M151 adds one test-only [Windows retained-parent substitution
> probe](docs/security/cache-cleanup-windows-retained-parent-substitution-probe.md).
> It proves a renamed directory's retained handle stays bound to the original
> object when the former name is rebound to a junction; Windows remains
> unadmitted.
> M152 adds one test-only [Windows cross-process substitution
> probe](docs/security/cache-cleanup-windows-cross-process-substitution-probe.md).
> A fixed child command renames and rebinds the directory while the parent
> retains the original handle; this is not a concurrency or admission claim.
> M153 adds one test-only [Windows share-delete exclusion
> probe](docs/security/cache-cleanup-windows-share-delete-exclusion-probe.md).
> A fixed child rename is blocked while delete sharing is omitted and succeeds
> after deterministic handle close; Windows remains unadmitted.
> M154 adds one test-only [Windows native sharing-violation
> probe](docs/security/cache-cleanup-windows-native-sharing-violation-probe.md).
> A fixed isolated child directly observes native error 32 before close and
> success afterward; the result remains current-host evidence only.
> M155 adds one test-only [Windows child-owned share-delete
> handshake](docs/security/cache-cleanup-windows-child-owned-share-delete-handshake.md).
> A fixed child owns and acknowledges the blocking handle lifecycle while a
> separate native rename child proves denial before close and success afterward.
> M156 adds one test-only [Windows abrupt blocker-owner termination
> probe](docs/security/cache-cleanup-windows-abrupt-blocker-termination-probe.md).
> It bypasses the graceful close token, bounds forced termination, and retries
> the unchanged native rename once without admitting runtime recovery.
> M157 adds one test-only [Windows blocker control-pipe EOF
> probe](docs/security/cache-cleanup-windows-control-pipe-eof-probe.md).
> It closes the parent writer after readiness and bounds the helper's existing
> invalid-control cleanup without admitting arbitrary pipe recovery.
> M158 adds one test-only [Windows blocker invalid-control-token
> probe](docs/security/cache-cleanup-windows-invalid-control-token-probe.md).
> It writes and flushes one fixed invalid byte before the same bounded fixture
> cleanup, without admitting arbitrary malformed input or pipe recovery.
> M159 adds one test-only [Windows blocker broken-control-pipe
> probe](docs/security/cache-cleanup-windows-broken-control-pipe-probe.md).
> A direct late native write reports false/error 232 with zero bytes after
> bounded owner termination, without admitting a recovery or error-code
> contract.
> M160 adds one test-only [Windows live-blocker wait-timeout
> probe](docs/security/cache-cleanup-windows-live-wait-timeout-probe.md).
> One zero-duration wait raises `TimeoutExpired` while the child and denial
> remain live, without admitting timeout recovery or policy.
> M161 adds one test-only [Windows acknowledged-release timeout
> probe](docs/security/cache-cleanup-windows-acknowledged-release-timeout-probe.md).
> A fixed child acknowledges release intent while retaining the denial until a
> separate close token, without admitting graceful-close recovery or policy.
> M162 adds one test-only [Windows duplicated-handle retention
> probe](docs/security/cache-cleanup-windows-duplicated-handle-probe.md). A
> fixed child closes an original no-delete-share handle while retaining its
> same-process duplicate, without admitting inherited handles or cleanup
> policy.
> M163 adds one test-only [Windows inherited-handle retention
> probe](docs/security/cache-cleanup-windows-inherited-handle-probe.md). A
> parent passes exactly one no-delete-share handle through an explicit handle
> list and closes its copy while the fixed child retains the denial, without
> admitting concurrency-safe inheritance or cleanup policy.
> M164 adds one test-only [Windows inherited-launch failure
> probe](docs/security/cache-cleanup-windows-inherited-launch-failure-probe.md).
> A fixed missing executable produces a real process-creation failure while
> the parent restores noninheritability and retains its denial, without
> admitting arbitrary rollback or recovery policy.
> M165 adds one test-only [Windows inherited-handle restoration-failure
> probe](docs/security/cache-cleanup-windows-inherited-restore-failure-probe.md).
> One fixed injected restore error proves the already-created child is reaped
> before propagation and leaves parent repair duty explicit, without claiming
> a real native restore failure or admitting recovery policy.
> M166 adds one test-only [Windows concurrent broad-inheritance leak
> probe](docs/security/cache-cleanup-windows-concurrent-inheritance-leak-probe.md).
> One event-controlled interleaving proves a broad-inheritance child can retain
> the temporarily inheritable blocker after parent and intended-child close,
> without claiming concurrency safety or adding runtime coordination.
> M167 adds one test-only [Windows concurrent explicit-list isolation
> probe](docs/security/cache-cleanup-windows-concurrent-explicit-inheritance-probe.md).
> Two real overlapping launches each receive one distinct blocker and both
> release orders prove pairwise isolation, without claiming a general
> concurrency-safe process-creation contract.
> M168 adds one test-only [Windows concurrent explicit-list launch-failure
> probe](docs/security/cache-cleanup-windows-concurrent-explicit-launch-failure-probe.md).
> A successful fixed child and a real missing-executable launch overlap; after
> parent close, the failed-launch root releases while the successful child
> retains only its own blocker.
> M169 adds one test-only [Windows concurrent explicit-list restoration-failure
> probe](docs/security/cache-cleanup-windows-concurrent-explicit-restore-failure-probe.md).
> Two real children launch in one shared inheritability window; one injected
> restore failure reaps only its child while the surviving child retains only
> its own blocker.
> M170 adds one test-only [Windows concurrent explicit-list abrupt-termination
> probe](docs/security/cache-cleanup-windows-concurrent-explicit-abrupt-termination-probe.md).
> After both parent handles close, one forcibly terminated child releases only
> its root while the survivor remains live and blocking.
> M171 adds one test-only [Windows exclusive-root acquisition
> probe](docs/security/cache-cleanup-windows-exclusive-root-acquisition-probe.md).
> A no-sharing directory owner refuses a late child, while an existing child
> makes the same acquisition fail closed until its acknowledged close.
> M172 adds one test-only [Windows descendant non-exclusion
> probe](docs/security/cache-cleanup-windows-descendant-non-exclusion-probe.md).
> It proves the directory owner is not a recursive subtree lock: a separate
> descendant file owner coexists in either acquisition order.
> M173 adds one test-only [Windows cooperative-lock
> probe](docs/security/cache-cleanup-windows-cooperative-lock-probe.md). Two
> shared participants collectively refuse an exclusive owner through the last
> release, while the exclusive owner refuses a late shared participant.
> M174 adds one test-only [Windows cooperative-lock substitution
> probe](docs/security/cache-cleanup-windows-cooperative-lock-substitution-probe.md).
> Renaming and replacing the coordination pathname splits old and new
> participants into independent file identities and lock generations.
> M175 adds one test-only [Windows live substitution-exclusion
> probe](docs/security/cache-cleanup-windows-cooperative-lock-live-substitution-exclusion-probe.md).
> Omitting delete sharing blocks replacement through the final live protected
> participant, but not across the zero-participant window.
> M176 adds one test-only [Windows cooperative-lock abrupt-settlement
> probe](docs/security/cache-cleanup-windows-cooperative-lock-abrupt-settlement-probe.md).
> Killing and reaping one protected participant preserves both refusals through
> the survivor; killing and reaping the survivor releases both ownership types.
> M177 adds one test-only [Windows protected guardian-handoff
> probe](docs/security/cache-cleanup-windows-protected-guardian-handoff-probe.md).
> A non-range-locking guardian preserves one identity through a participant-free
> interval and hands protection to a later participant without runtime promotion.
> M178 adds one test-only [Windows guardian abrupt-handoff
> probe](docs/security/cache-cleanup-windows-guardian-abrupt-handoff-probe.md).
> After an overlapping participant joins, abrupt guardian termination and bounded
> process wait leave that participant's independent protections intact.
> M179 adds one test-only [Windows overlapping guardian-rotation
> probe](docs/security/cache-cleanup-windows-overlapping-guardian-rotation-probe.md).
> Two fixed guardians overlap before the first is abruptly reaped; the second
> retains namespace protection after the range participant later closes.
> M180 adds one test-only [Windows zero-owner guardian restart-boundary
> probe](docs/security/cache-cleanup-windows-zero-owner-guardian-restart-boundary-probe.md).
> A later guardian attaches to the current identity after the first is reaped;
> substitution during the exposed interval redirects it to the replacement.
> M181 adds one test-only [Windows expected-identity guardian admission
> probe](docs/security/cache-cleanup-windows-expected-identity-guardian-admission-probe.md).
> The guardian compares the caller's expected identity on its already
> protecting handle, admitting a match and closing before reporting a mismatch.
> M182 adds one test-only [Windows hard-link alias non-exclusion
> probe](docs/security/cache-cleanup-windows-hard-link-alias-non-exclusion-probe.md).
> It proves the opened name remains protected while a preexisting alias for the
> same file can be renamed, so identity match is not root-confined ownership.
> M183 adds one test-only [Windows post-admission hard-link creation
> probe](docs/security/cache-cleanup-windows-post-admission-hard-link-creation-probe.md).
> A one-link file gains a peer alias while its matching guardian remains live,
> proving that admission does not freeze the link set.
> M184 adds one test-only [Windows hard-link alias deletion non-exclusion
> probe](docs/security/cache-cleanup-windows-hard-link-alias-deletion-non-exclusion-probe.md).
> A peer alias can be deleted while the matching guardian remains live and
> keeps protecting the exact name it opened, so link removal is not excluded.
> M185 adds one test-only [Windows hard-link alias delete/recreate ABA
> probe](docs/security/cache-cleanup-windows-hard-link-alias-delete-recreate-aba-probe.md).
> The same peer pathname can move from present to absent to present while the
> guardian remains live and the observed link count changes `2 -> 1 -> 2`.
> M186 adds one test-only [Windows independent hard-link alias mutator ABA
> probe](docs/security/cache-cleanup-windows-independent-hard-link-alias-mutator-aba-probe.md).
> A distinct sibling child now owns the delete/recreate calls while the parent
> only coordinates and observes; the result remains same-principal evidence.
> M187 adds one test-only [Windows hard-link alias mutator abrupt-loss
> probe](docs/security/cache-cleanup-windows-hard-link-alias-mutator-abrupt-loss-probe.md).
> After the child-owned delete, abrupt mutator loss leaves the alias absent and
> the original at one link; this is a recovery gap, not automatic rollback.
> M188 adds one test-only [Windows hard-link alias mutator abrupt-loss-after-recreate
> probe](docs/security/cache-cleanup-windows-hard-link-alias-mutator-abrupt-loss-after-recreate-probe.md).
> After child-owned recreation, abrupt mutator loss leaves the alias present and
> both names at two links; this is negative rollback evidence, not durable commit.
> M189 adds one test-only [Windows hard-link alias mutator control-pipe EOF after
> recreation probe](docs/security/cache-cleanup-windows-hard-link-alias-mutator-control-pipe-eof-after-recreate-probe.md).
> Closing only the parent control writer after exact recreation settles the fixed
> child with EOF while leaving the alias present and both names at two links.
> M190 adds one test-only [Windows hard-link alias mutator invalid control token
> after recreation probe](docs/security/cache-cleanup-windows-hard-link-alias-mutator-invalid-control-token-after-recreate-probe.md).
> Writing and flushing one fixed invalid byte after exact recreation settles the
> unchanged child while leaving the alias present and both names at two links.

> Project status: community-alpha release candidate (`0.1.0a1`). M0 through M99 are hosted-validated and integrated into `main`; M100 through M190 are locally validated stacked milestones from the exact M99 closeout. External adoption and release-readiness observations remain explicitly bounded by the reviewed evidence records and roadmap. No public release has been made.

Earlier readiness evidence remains deliberately empty where no external result
exists:

- M28 retains its empty reviewed sample-game manifest.
- M29 retains its empty reviewed contributor-retention manifest.
- M30 retains its empty reviewed installation-matrix manifest.
- M31 retains its empty reviewed measurement manifest and makes no response-time, review-time, or SLA claim.
- M32 retains its empty reviewed execution manifest and makes no measured divergence rate claim.
- M33 retains its empty reviewed benchmark comparison manifest and makes no measured regression rate claim.
- M34 retains its empty reviewed agent-tool call manifest and makes no measured recovery-free completion rate claim.
- M35 retains its empty reviewed third-party conformance submission manifest.

See the roadmap and milestone-specific readiness documents for the complete
boundaries.

M58 through M66 are hosted-validated and integrated. M60-M66 harden public-
release filesystem, asset-name, and consumer-output handling without changing
engine runtime or a public protocol. M59's tool-neutral repository metadata
convention remains enforced.

## What exists

- A typed engine lifecycle with explicit ownership and close semantics.
- Monotonic and deterministic virtual clocks.
- An engine-owned rendering protocol and validation-only null renderer.
- A headless fixed-tick example.
- `ludoweave --version` and a structured `ludoweave doctor` command.
- Architecture rules, ADRs, tests, documentation, packaging, and cross-platform CI.
- Generational entity IDs and a deterministic allocator whose stale handles never revive.
- Explicit immutable component schemas, UUID-sorted registries, and validated forward migrations.
- Canonical pure-Python dense/sparse world storage with copy-safe component ownership.
- Typed storage-neutral queries with explicit writable cursor lifetimes and change filters.
- Atomic local structural command buffers with exact deferred-entity ownership.
- Explicit copy-owned typed resources and deterministic conflict-aware serial schedule planning.
- An additive fixed-step application runner with immutable virtual/recorded input and declared-access system contexts.
- An independent dictionary reference world exercised by state-machine property tests.
- Versioned canonical world commands with atomic transactions, optimistic hashes, dry-run, semantic diffs, and structured receipts.
- A bounded versioned data-only scene document that compiles through an
  explicit component registry into ordinary `entity.spawn` commands; receipt
  aliases return the deterministic local-ID-to-runtime-entity mapping.
- One-level versioned data-only prefab fragments with detached current-schema
  overrides that compile to the same ordinary commands and receipt aliases;
  source changes never silently mutate runtime instances.
- Bounded `ludoweave.source-manifest/1` files that list explicit scene or
  prefab/instance inputs and produce a path-silent aggregate CLI preflight.
- Canonical `ludoweave.source-lock/1` content identities plus read-only
  generation and exact verification for explicit source manifests, without
  import, discovery, cache, or world mutation.
- Bounded project-confined loading and canonical normalization for the existing
  `ludoweave.assets/1` manifest, with no asset source read, asset build, cache,
  discovery, or world mutation.
- Read-only `ludoweave source assets` validation that keeps source-declared
  direct asset URIs distinct from their deterministic resolved graph closure,
  with no asset source read, unused-asset rejection, build, cache, or mutation.
- Canonical `ludoweave.asset-source-lock/1` input identities plus read-only
  generation and content-silent verification for the selected asset closure,
  using bounded streaming hashes with no asset decode, build, import, cache
  write, discovery, or mutation.
- Canonical `ludoweave.asset-build-plan/1` prospective actions in deterministic
  dependency-first order, with exact M4 cache-key compatibility after current
  input verification and no asset build, cache read, or cache write.
- Bounded `ludoweave.asset-build-result/1` identities from dependency-first
  built-in PNG/JSON/WGSL/audio decoder execution over exact detached sources,
  with no retained payload, cache read/write, or project write.
- Explicit local `ludoweave.asset-cache-entry/1` publication with verified
  SHA-256 payload CAS blobs, atomic per-entry action metadata, content-silent
  corruption failure, and no project or remote-cache effect.
- Read-only `ludoweave.asset-cache-lookup/1` inspection of exact current-plan
  action keys with strict canonical metadata and CAS verification, explicit
  misses, and no cache creation, mutation, decoder bypass, or project write.
- Read-only `ludoweave.asset-build-realization/1` materialization from verified
  current-plan cache hits and built-in decoding of exact misses, preserving
  plan order and resource bounds with no project or cache write.
- Explicit `ludoweave.asset-cache-population/1` composition that completes
  read-only realization before acquiring cache-write authority, then reports
  plan-ordered hit/decoded and published/reused evidence without changing the
  project or claiming an all-plan cache transaction.
- Bounded saved-population decoding and read-only
  `ludoweave.asset-cache-population-verification/1` evidence that checks exact
  current plan/action/CAS agreement without decoder fallback, cache mutation,
  signature, authenticity, or provenance claims.
- Bounded read-only `ludoweave.asset-cache-inventory/1` evidence that strictly
  reconstructs every engine-owned action, streams and hashes every admitted CAS
  blob, and reports current-plan/other/no-observed-reference aggregates. A blob
  with no observed action reference is not deletion eligibility.
- Deterministic path-free `ludoweave.asset-cache-fingerprint/1` evidence that
  reuses one bounded inventory pass and binds exact sorted canonical action and
  CAS membership. It is a sequential observation, not an atomic snapshot,
  retention root, or cleanup authorization.
- Strict bounded saved-fingerprint decoding and read-only
  `ludoweave.asset-cache-fingerprint-verification/1` evidence that compares one
  exact record with one fresh observation. Digest agreement is local integrity
  equality, not authenticity, provenance, or mutation authority.
- Fixed path-free `ludoweave.asset-cache-fingerprint-comparison/1` diagnosis
  that reports signed deltas for the twelve existing aggregate inventory
  fields plus one exact-observation equality flag. It exposes no object
  identity, differing digest, path, payload, or cleanup authority.
- Pure offline comparison of two admitted canonical cache fingerprints under
  one exact plan, reusing the same fixed report without cache construction,
  cache access, fresh observation, or new protocol.
- Complete authority snapshots, SHA-256 state hashes, explicit persistent-resource migrations, and deterministic named random streams.
- Self-contained verified replay/checkpoint files and immutable parent-referenced timeline branches.
- Project-confined `apply`, `snapshot`, `replay`, and `diff` CLI workflows for a deliberately data-only empty project composition.
- Immutable presentation extraction, backend-neutral descriptors and scoped generational render handles, explicit render-graph validation, and deferred destruction.
- An optional exactly pinned wgpu/rendercanvas/GLFW adapter with orthographic instanced atlas sprites, tile/debug batches, resize, typed loss, and offscreen RGBA capture.
- Provider-neutral key/pointer/window/gamepad events, explicit gamepad deadzones,
  immutable transition-aware action snapshots, and virtual/recorded/live input
  sources.
- Project-confined `asset://` manifests, content-addressed dependency caching, bounded PNG loading, and retained safe texture replacement.
- Deterministic AABB/circle collision, a property-tested spatial grid, documented kinematic resolution, and a minimal owned Null audio adapter.
- Bounded tick animation, bitmap atlas text layout, immutable chunked tilemaps,
  seeded fixed-point particles, and a Null-audio acyclic mix graph, all
  exercised by one dependency-free headless showcase.
- Preview canonical data-only plugin manifests with deterministic
  environment/policy/dependency checks and no discovery or code execution.
- Bounded offline correction-branch evidence that records the current replay
  input-history gap and defers networking/live rollback under ADR-0027.
- Deterministic installed-surface evidence that retains layered 2D and defers
  constrained 3D under ADR-0028 without adding runtime contracts or providers.
- Deterministic installed-surface evidence that confirms the command/receipt,
  typed-tool, MCP, and inspector foundation through an actual ephemeral
  receipted mutation while deferring a visual editor under ADR-0029 without
  adding a GUI, runtime API, format, or dependency.
- A security threat model and deterministic installed evidence that preserve
  the data-only plugin boundary and defer WASM runtimes, guest execution, WASI,
  and host calls under ADR-0030.
- A versioned installed render-device baseline that produces sanitized,
  deterministic evidence from an explicitly supplied trusted adapter factory;
  it performs no discovery and is not a security certification.
- A versioned installed agent-tool baseline that exercises all 12 typed tools,
  transaction/tick receipts, stale-hash atomicity, query/diff, provider result
  shapes, and close behavior through an explicitly supplied trusted factory.
- A versioned installed `WorldStore` baseline that exercises entity generations,
  epochs, detached copies, queries, command atomicity, cloning, and structured
  failures through an explicitly supplied trusted factory.
- Deterministic installed command/receipt stability evidence that confirms the
  same-version canonical and atomic foundation while retaining experimental
  status under RFC-0003 until every compatibility gate is evidenced.
- A strict bounded `ludoweave.receipt/1` reader with detached immutable output,
  typed failures, configurable resource limits, and frozen `0.1.0a1` fixtures
  that seed—but do not yet satisfy—a cross-version compatibility corpus.
- A deterministic admission harness that verifies those historical bytes and
  requires a different installed reader version plus supported-release
  evidence before any cross-version claim.
- A strict external-consumer-feedback admission harness whose empty reviewed
  manifest keeps the current adoption gate false.
- A strict supported feature-release-channel admission harness whose empty
  reviewed manifest keeps the deprecation-channel gate false.
- A strict external-contributor rehearsal admission harness whose empty
  reviewed manifest explicitly does not claim that an independent human has
  completed the public contribution path without private maintainer knowledge.
- A strict external sample-game adoption admission harness whose empty reviewed
  sample-game manifest keeps the externally authored game count at zero.
- A strict published-wheel installation-matrix admission harness whose empty
  reviewed manifest keeps the current clean-install result false.
- A strict issue-response and pull-request-review latency admission harness
  whose empty reviewed manifest keeps all counts and latency aggregates absent.
- A strict controlled benchmark-regression-rate admission harness whose empty
  reviewed manifest keeps all comparison counts and rate absent.
- A strict agent-tool recovery-rate admission harness whose empty reviewed
  agent-tool call manifest keeps all call counts and recovery-free rate absent.
- A strict third-party conformance-adoption admission harness whose empty
  reviewed submission manifest keeps the passing external implementation count
  at zero without discovering, loading, or executing packages.
- Exact v1 contracts and an explicit versioned evolution policy for all seven
  built-in operation argument shapes, exercised from installed artifacts
  without adding a runtime schema layer.
- ECS-authoritative Clockwork Arena with fixed-seed waves, enemies, projectiles, health, score, restart, exact 3,600-tick replay evidence, optional wgpu presentation, and stress workloads.
- A transport-independent typed agent service with explicit capabilities, quotas, redaction, serialized mutations, and the same canonical command receipts used by direct Python.
- Twelve observation/control tools exposed through Python, a project-confined CLI, and a local-only MCP `2025-11-25` stdio adapter with no network listener.
- An owned local `ludoweave inspect` child composition with read-only defaults,
  explicit receipted sample/tick mutations, versioned semantic observations,
  and verified snapshot/diff hash continuity.
- An Agent World Builder acceptance loop covering typed creation, validation, application, ticks, capture, query, adjustment, diff, telemetry, tests, and replay evidence.
- Deterministic release staging with a pure wheel, source distribution, sample bundle, checksums, SPDX SBOM, notices, manifest, installed-artifact smoke, a pinned provenance workflow, fail-closed repeat-build byte verification, and signed annotated-tag identity/main-ancestry admission.
- Explicit stability metadata for every public Python export, community-alpha user/adapter/contribution guides, and a repository-native triage/roadmap queue.
- Versioned, sanitized profiling for the representative M1/M3 misses plus an accepted RFC retaining the pure-Python/no-compiler baseline.
- A bounded isolated Box2D-candidate probe plus ADR-0024; no physics binding,
  adapter, native object, or runtime dependency is shipped.

Nested prefab inheritance, live scene updates, production audio,
international text shaping,
rigid-body physics, networking or remote agent transport, visual editor
tooling, executable Python/WASM mods, constrained or general 3D, and automatic
GPU recovery are not implemented.

## Requirements

- CPython 3.12, 3.13, or 3.14 (standard GIL builds are the baseline)
- Windows, macOS, or Linux
- [uv](https://docs.astral.sh/uv/) 0.11.x for contributor workflows

No native compiler or GPU is required.

## Quick start

```console
uv sync --frozen --all-groups
uv run ludoweave --version
uv run ludoweave doctor
uv run python examples/hello_headless.py --ticks 120
uv run python examples/fixed_step_world.py --ticks 6
uv run python examples/clockwork_arena.py --ticks 600
uv run python examples/rollback_readiness.py --ticks 120 --branch-tick 60
uv run python examples/cross_version_corpus_readiness.py
uv run python examples/external_consumer_feedback_readiness.py
uv run python examples/supported_release_channel_readiness.py
uv run python examples/external_contributor_rehearsal_readiness.py
uv run python examples/external_contributor_retention_readiness.py
uv run python examples/external_sample_game_adoption_readiness.py
uv run python examples/installation_matrix_readiness.py
uv run python examples/response_review_latency_readiness.py
uv run python examples/replay_divergence_rate_readiness.py
uv run python examples/benchmark_regression_rate_readiness.py
uv run python examples/agent_tool_recovery_rate_readiness.py
uv run python examples/third_party_conformance_adoption_readiness.py
uv run python examples/command_receipt_stability_decision.py
uv run python examples/operation_argument_compatibility.py
uv run python examples/receipt_reader.py
uv run python examples/constrained_3d_decision.py
uv run python examples/visual_editor_decision.py
uv run python examples/wasm_mod_security_decision.py
uv run python examples/render_device_conformance.py
uv run python examples/agent_tool_conformance.py
uv run python examples/world_store_conformance.py
uv run python examples/world_store_conformance.py --backend reference
uv run python examples/alpha_acceptance.py
uv run ludoweave plugin check examples/example.plugin.json
uv run ludoweave inspect --sample agent-world-builder
```

The example prints one JSON summary and uses virtual time plus the null renderer, so it does not open a window or wait in real time.

GPU rendering is an optional locked extra and is selected only by a composition root:

```console
uv sync --frozen --all-groups --extra graphics
uv run --frozen --extra graphics python examples/hello_sprite.py
uv run --frozen --extra graphics python examples/agent_world_builder.py
uv run --frozen --extra graphics python examples/render_device_conformance.py --backend wgpu
```

The sprite example renders two atlas regions in one instanced draw and prints a versioned offscreen-capture summary. Add `--window` to exercise the rendercanvas/GLFW window surface on a desktop session.

Clockwork Arena can use the same optional renderer. Add `--window --interactive`
for WASD/arrows, pointer aim, primary-button fire, and R restart. Gamepad slot 0
uses left/right sticks, A, and Start:

```console
uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 36000 --renderer wgpu --window --interactive
```

## Public API

The root package intentionally exposes only the initial application surface:

```python
from ludoweave import Engine, EngineConfig, LifecycleState, __version__
from ludoweave.core.clock import VirtualClock
from ludoweave.ecs import ComponentRegistry, EntityAllocator, World
from ludoweave.render import NullRenderBackend, RenderDescriptor

clock = VirtualClock()
backend = NullRenderBackend()

with Engine(EngineConfig(), backend, clock=clock) as engine:
    summary = engine.run(ticks=10)

entities = EntityAllocator()
entity_id = entities.create()
entities.validate(entity_id)

world = World(ComponentRegistry())
world_entity = world.spawn()
assert world.entities() == (world_entity,)

for queried_id, in world.query().stable().rows():
    assert queried_id == world_entity

commands = world.commands()
pending = commands.spawn()
result = world.flush(commands)
assert result.resolve(pending) in world.entities()
```

See the [architecture overview](docs/architecture.md), [runtime contract](docs/runtime-contract.md), [entity identity contract](docs/ecs.md), [2D rendering contract](docs/rendering.md), and [M4 gameplay guide](docs/gameplay.md) before depending on these experimental APIs.
The [headless command workflow](docs/cli-workflows.md) documents the M2 data-only
project manifest, full command workflow, and M123-M145 source preflight,
integrity verification, dependency checking, locks, plans, and bounded
in-memory execution.
The [persistent command guide](docs/commands.md) documents M119-M133 scene
normalization, explicit schema resolution, transaction planning, receipt alias
mapping, prefab overrides, bounded project-confined file loading, and explicit
source manifests, locks, and asset dependency checking.
The [agent control interface](docs/agent-control.md) documents M5 tools, capabilities, limits, Python/CLI/MCP composition, and the Agent World Builder loop.
The [live semantic inspector guide](docs/inspector.md) documents M10 local child
ownership, observation events, explicit write receipts, bounds, and failures.
The [rich 2D presentation guide](docs/presentation.md) documents M11 animation,
bitmap text, tilemap, particle, and audio-mix ownership and determinism.
The [plugin compatibility guide](docs/plugins.md) documents M12 inert manifests,
preview compatibility, deterministic reports, and the explicit no-loader boundary.
The [rollback-readiness guide](docs/rollback-readiness.md) documents M13's
offline correction proof, external input-history limitation, network deferral,
and complete revisit gate.
The [constrained 3D decision](docs/constrained-3d-decision.md) documents M14's
installed-surface evidence, retained layered-2D scope, and complete revisit
gate.
The [visual-editor admission decision](docs/visual-editor-decision.md)
documents M15's positive protocol foundation, missing authoring contracts,
target users and jobs, and complete revisit gate. It retains the finite
headless inspector instead of creating a widget-side state model.
The [WASM-mod security decision](docs/wasm-mod-security-decision.md) documents
M16's threat model, current inert boundary, prospective blockers, complete
admission gate, and explicit runtime deferral.
The [render-device conformance guide](docs/render-device-conformance.md)
documents M17's explicit-factory trust boundary, versioned checks, sanitized
report, limitations, and evidence expectations for external adapters.
The [agent-tool conformance guide](docs/agent-tool-conformance.md) documents
M18's fixed 12-check profile, fresh-authority precondition, ownership,
sanitized evidence, and explicit non-certification boundary.
The [WorldStore conformance guide](docs/world-store-conformance.md) documents
M19's fixed 10-check profile, borrowed registry identity, current no-close
in-memory boundary, sanitized evidence, and non-certification limitations.
The [command and receipt stability decision](docs/command-receipt-stability-decision.md)
documents M20's installed same-version evidence, complete preview gate, and
RFC-0003 decision to retain experimental status without changing a wire format.
The [bounded receipt-reader guide](docs/receipt-reader.md) documents M21's
exact v1 schema checks, limits, immutable decoding, failure behavior, and
single-version fixture non-claim under RFC-0004.
The [operation-argument compatibility guide](docs/operation-argument-compatibility.md)
documents M22's exact seven v1 shapes, fail-closed unknown-field rule,
versioned breaking-change policy, installed evidence, and remaining RFC-0003
gates under RFC-0005.
The [receipt semantic compatibility guide](docs/receipt-semantic-compatibility.md)
documents M23's exact v1 diff fields and meanings, status-specific presence,
diagnostic-code identity/fallback rules, installed evidence, and remaining
RFC-0003 gates under RFC-0006.
The [external-contributor rehearsal readiness guide](docs/external-contributor-rehearsal-readiness.md)
documents M27's reviewed-history, human-review, privacy, and installed-artifact
contract while retaining the current empty-record result as false.
The [external sample-game adoption readiness guide](docs/external-sample-game-adoption-readiness.md)
documents M28's authorship, provenance, installed-capability, licensing, and
complete-history gate while retaining the current externally authored game
count at zero.
The [external contributor-retention readiness guide](docs/external-contributor-retention-readiness.md)
documents M29's same-person, chronology, DCO, validation, provenance, and
complete-history gate while retaining the current retained-contributor count
at zero and excluding popularity metrics.
The [installation-matrix readiness guide](docs/installation-matrix-readiness.md)
documents M30's immutable public-wheel, clean-environment, exact-matrix, and
complete-history gate while retaining the current zero-record result.
The [response and review latency readiness guide](docs/response-review-latency-readiness.md)
documents M31's complete-census, pending-item, first-qualifying-action, and
complete-history gate while retaining the current empty reviewed measurement
manifest and defining no SLA.
The [replay-divergence-rate readiness guide](docs/replay-divergence-rate-readiness.md)
documents M32's complete CI execution cohort, preserved non-execution outcomes,
exact rational rate, and history gate while retaining the current empty
reviewed execution manifest and no measured divergence rate.
The [benchmark-regression-rate readiness guide](docs/benchmark-regression-rate-readiness.md)
documents M33's registered paired-benchmark cohort, controlled-comparability,
predeclared integer tolerance, non-execution, and history gates while retaining
the current empty reviewed comparison manifest and no measured regression rate.
The [agent-tool recovery-rate readiness guide](docs/agent-tool-recovery-rate-readiness.md)
documents M34's complete task-directed call cohort, exact manual-recovery
definition, terminal-evidence and history gates while retaining the current
empty reviewed agent-tool call manifest and no measured recovery-free
completion rate.
The [third-party conformance-adoption readiness guide](docs/third-party-conformance-adoption-readiness.md)
documents M35's fixed installed-profile registry, independent-authorship,
plugin-manifest, failure-preservation, and complete-history gates while
retaining the current empty reviewed submission manifest and zero passing
third-party implementations.
The [community-alpha user guide](docs/user-guide.md), [adapter guide](docs/adapter-guide.md), [API policy](API_COMPATIBILITY.md), and [release verification guide](docs/release-process.md) cover the M6 evaluation boundary.

Agent mutation is disabled unless the trusted composition root explicitly
enables it. For example, these launch the built-in sample over local stdio:

```console
uv run ludoweave mcp --sample agent-world-builder
uv run ludoweave mcp --sample agent-world-builder --write --renderer wgpu
uv run ludoweave inspect --sample agent-world-builder
uv run ludoweave inspect --sample agent-world-builder --write --bootstrap --ticks 2
```

The first MCP process and first inspector session are read-only. None of these
commands opens a network listener; the inspector can launch only the built-in
MCP child through the current Python interpreter.

## Quality commands

```console
uv lock --check
uv sync --frozen --all-groups --extra graphics
uv run --frozen ruff format --check .
uv run --frozen ruff check .
uv run --frozen pyright
uv run --frozen pytest -q
uv run --frozen mkdocs build --strict
uv build --out-dir .tmp/dist-first
uv build --out-dir .tmp/dist-second
uv run --frozen python scripts/verify_distribution_reproducibility.py .tmp/dist-first .tmp/dist-second
uv run --frozen python scripts/smoke_wheel.py .tmp/dist-first
uv run --frozen python scripts/smoke_scene_wheel.py .tmp/dist-first
uv run --frozen python scripts/release_artifacts.py .tmp/dist-first .tmp/release-candidate
uv run --frozen python scripts/smoke_release.py .tmp/release-candidate
uv run --frozen python benchmarks/benchmark_m1.py --samples 30 --seed 1 --json-out .tmp/m1-benchmark.json
uv run --frozen python benchmarks/validate_m1_results.py .tmp/m1-benchmark.json
uv run --frozen python benchmarks/benchmark_m2.py --samples 30 --seed 1 --json-out .tmp/m2-benchmark.json
uv run --frozen python benchmarks/validate_m2_results.py .tmp/m2-benchmark.json
uv run --frozen --extra graphics python benchmarks/benchmark_m3.py --samples 30 --output .tmp/m3-benchmark.json
uv run --frozen --extra graphics python benchmarks/validate_m3_results.py .tmp/m3-benchmark.json
uv run --frozen python benchmarks/benchmark_m4.py --samples 300 --warmups 60 --output .tmp/m4-benchmark.json
uv run --frozen python benchmarks/validate_m4_results.py .tmp/m4-benchmark.json
uv run --frozen python -m benchmarks.profile_m7 --repeats 5 --output .tmp/m7-profile-base.json
uv run --frozen python -m benchmarks.validate_m7_profile .tmp/m7-profile-base.json
uv run --frozen --extra graphics python -m benchmarks.profile_m7 --repeats 5 --include-wgpu --output .tmp/m7-profile-graphics.json
uv run --frozen python -m benchmarks.validate_m7_profile .tmp/m7-profile-graphics.json
git diff --check
```

Milestone benchmark/profile commands are not part of every edit's fast gate. M1, M3, and M4 record local target observations; M2 measurements are informational and have no timing pass threshold. M7 profile time is diagnostic rather than a benchmark. Results are recorded only after commands have actually run; see [test evidence](.project/TEST_EVIDENCE.md), the [benchmark methodology](docs/benchmarks.md), and [RFC-0001](docs/rfcs/0001-defer-first-native-kernel.md).

M36 pull-request CI preserves the same eight validation slices while grouping
them into three OS-owned hosted runner allocations: one Ubuntu runner covers
quality/distribution, CPython 3.12-3.14, and Linux graphics; Windows and macOS
each cover CPython 3.12 graphics plus 3.14 compatibility. This uses five fewer
runner allocations without deleting a version, platform, graphics, package,
installed-wheel, release, documentation, or static-analysis slice. The pure
universal wheel is smoke-tested once rather than rebuilding the same artifact
three times, provider tests run only after the required graphics runtime is
installed, and superseded runs are cancelled automatically.
The gate runs only for substantive pull requests: a validated tree is not run
again after merge to unprotected `main`, and `.project/**`-only factual record
pull requests consume no hosted runner quota.

M37 keeps one visible pull-request workflow but qualifies the diff from the
trusted base revision. Documentation-only changes run one Linux allocation for
lock, formatting/lint, strict docs, architecture, build, installed-wheel, and
release-candidate checks. Any unrecognized, empty, mixed, or indeterminate diff
is substantive or fails closed. Substantive changes retain all three hosted
allocations and eight M36 validation slices; Windows and macOS begin only after
the Linux qualification and complete gate succeed.

M38 builds the pure wheel and source distribution twice inside the already
allocated Linux distribution step and fails unless both artifact pairs are
byte-identical. The same comparison runs before smoke, staging, attestation, or
publication in the tag workflow. It adds no runner, matrix entry, dependency,
action, permission, trigger, credential, or cross-platform reproducibility
claim.

M39 makes the existing tag-only release job fail before system setup, tests,
build, attestation, or publication unless the exact `vVERSION` ref is an
annotated tag whose signature GitHub reports as valid, whose local/GitHub tag
object targets the checked-out event commit, and whose commit is reachable from
fetched `origin/main`. The validator emits only safe tag/object/commit identities
and never prints the signature or payload. This adds no runner, action,
permission, trigger, dependency, key allowlist, tag, or publication authority;
RFC-0022 defines the trust boundary.

M40 makes the existing GitHub release transition explicit: create a prerelease
draft without assets, upload every staged file without clobbering, fetch the
version-pinned release document, and compare every uploaded name, byte size,
state, and SHA-256 digest with bounded local staging before publication. A
failure leaves an unpublished draft for inspection. This adds no runner,
action, permission, trigger, dependency, tag, release, or publication authority
and does not enable immutable releases; RFC-0023 defines the boundary.

M41 requires the authenticated private draft's release-notes body to exactly
equal the bounded non-empty UTF-8 `RELEASE_NOTES.md` already supplied through
`--notes-file` and covered as a staged asset. Missing, null, substituted,
truncated, or normalization-different bodies fail without logging note content.
This changes no workflow, runner, permission, dependency, tag, release, or
publication authority; RFC-0024 defines the source-body boundary.

M42 carries the exact authenticated release database ID across the publication
transition and rechecks the resulting public prerelease's state, UTC
publication time, notes, and assets. A mismatch fails the release job but never
automatically unpublishes or deletes evidence. This adds one read-only API
request inside the existing tag job, no runner or permission, and neither
requires nor claims immutable releases; RFC-0025 defines the boundary.

M43 requires each published asset to have a unique bounded numeric ID, writes
an exclusive runner-temporary retrieval plan only after complete validation,
downloads those exact IDs through the authenticated GitHub asset API, and
rehashes the retrieved directory against the same published document. It adds
no job, runner, action, permission, dependency, tag/release authority, clobber,
or rollback. It does not claim unauthenticated availability, global CDN state,
future immutability, or consumer installation; RFC-0026 defines the boundary.

M44 verifies SLSA v1 provenance for every exact M43-retrieved asset and an
SPDX 2.3 SBOM attestation for the single pure wheel. Each content-silent,
30-second-bounded GitHub CLI call fixes the repository, release workflow, tag,
source/signer commit, OIDC issuer, hosted-runner class, predicate, and candidate
limit. Failure occurs after publication and grants no mutation or rollback.
This is an integrity/identity check, not artifact-security, independent-build,
predicate-truth, future-availability, immutability, installation, or supported-
channel evidence; RFC-0027 defines the boundary. No real attestation pass is
claimed until an authorized signed-tag release run executes.

M45 follows M44 by fetching the exact public release ID and every exact M43
asset ID from fixed HTTPS GitHub API endpoints without supplying a GitHub
credential. It revalidates the public document and bounded downloaded set,
then runs complete release smoke—including isolated wheel installation and the
sample bundle—against those public bytes. The step adds no job, runner, action,
permission, dependency, release, or publication authority. It observes one
same-run public API path, not an independent/external consumer, every CDN or
browser path, future availability, immutability, cross-platform installation,
PyPI, or a supported channel; RFC-0028 defines the boundary. No real public-
path pass is claimed until an authorized signed-tag release run executes.

M46 follows M45 with one dependent read-only Linux job on a fresh hosted runner.
It retrieves the exact candidate preserved by the publishing job, creates a new
bounded plan, downloads the public bytes without a release credential,
revalidates them, and runs complete installed release smoke in its own
workspace. This is a same-workflow rehearsal—not independent/external or cross-
platform consumer evidence, a clean machine outside GitHub-hosted Actions,
future availability, immutability, artifact security, PyPI, or a supported
channel. RFC-0029 defines the boundary. No real fresh-runner pass is claimed
until an authorized signed-tag release run executes.

M47 follows M46 by replacing the internal Bash verifier with one typed,
standard-library Python program and running the tag-only fresh-consumer job on
Ubuntu, Windows, and macOS. Every operating-system runner retrieves the same
admitted candidate, creates its own bounded plan, fetches exact public bytes
without a release credential, and runs complete installed release smoke. This
is cross-platform same-workflow evidence, not independent/external verification,
a clean machine outside GitHub-hosted Actions, every delivery path, future
availability, immutability, artifact security, PyPI, or a supported channel.
RFC-0030 defines the boundary. No real cross-platform public-consumer pass is
claimed until an authorized signed-tag release run executes.

M48 follows M47 by accepting only the GitHub-documented response shapes: a
direct `200` for the public release document, and `200` or bounded `302`
handling for assets. API-version headers stay on `api.github.com`; timeout,
transport/protocol, and local-output failures retain distinct stable codes.
RFC-0031 defines the boundary. This changes no workflow, dependency, runtime
API, release authority, or independent/external evidence claim, and no real
M48 pass is claimed without an authorized signed-tag run.

M49 follows M48 by explicitly connecting each fixed API or redirected asset
hop and validating its actual port-443 TLS socket peer before any HTTP request.
Only globally reachable unicast IPv4/IPv6 is accepted; IPv4-mapped IPv6 is
classified by its embedded address. RFC-0032 defines the stable forbidden,
timeout, and request-failure boundary. This is not a hostname/IP allowlist,
separate DNS preflight, network sandbox, real public release observation, or
release-authority change, and no real M49 pass is claimed without an authorized
signed-tag run.

M50 replaces ambient-sensitive default TLS context creation with an explicit
client context for every public API or asset hop. It retains system server-auth
trust, mandatory certificate and hostname validation, TLS 1.2 or newer, and
strict X.509 verification while ensuring `SSLKEYLOGFILE` cannot enable TLS
session-secret logging or create its target. RFC-0033 defines the stable
content-silent TLS-context failure boundary. M50 changes no workflow,
dependency, runtime API, release authority, or real-release claim.

M51 inspects the actual negotiated TLS session after the connected-peer check
and before every HTTP request. It accepts only TLSv1.2 or TLSv1.3, a
well-formed cipher report with at least 128 secret bits, no TLS compression,
and ALPN `http/1.1` or no negotiated ALPN. The client advertises only
`http/1.1`; every redirected hop repeats the complete check. RFC-0034 defines
the content-silent failure and ownership boundary. This adds no cipher-name
allowlist, custom trust, workflow, dependency, runtime API, release authority,
or real public release observation.

M52 observes the actual TLS socket's service identity after the connected-peer
check and before the M51 session check. The URL hostname is normalized with
built-in IDNA to the reference hostname; the socket must retain that hostname
case-insensitively and expose a non-empty DER peer certificate. The M50 verified
context remains authoritative for certificate-path and hostname matching. Every
redirect repeats the check. RFC-0035 defines the content-silent failure and
ownership boundary. This adds no certificate parsing, pinning, custom trust,
revocation/CT policy, workflow, dependency, runtime API, release authority, or
real public release observation.

M53 verifies after the handshake that every actual TLS socket retains the
exact context object supplied for that hop and is strictly client-side. It then
revalidates the complete M50 context policy before M52 service-identity and M51
session checks or any HTTP transmission. Every redirect repeats the binding
and policy check with an independent context. RFC-0036 defines the content-
silent failure and ownership boundary. This adds no custom trust, pinning,
workflow, dependency, runtime API, release authority, or real public release
observation.

M54 reads `session_reused` from that actual socket after M53 context binding
and requires exactly `False` before service identity, negotiated-session
inspection, or HTTP transmission. Every redirect repeats the observation.
RFC-0037 defines the content-silent failure and ownership boundary. This adds
no session cache, ticket control, custom TLS implementation, workflow,
dependency, runtime API, release authority, or real public release observation.

M55 validates every response, including every redirect, through documented
HTTP/1.1-class metadata before status or body use. The public version value must
be integer `11`, while RFC-0038 explicitly records that CPython can normalize
other raw `HTTP/1.x` values and this is not exact status-line token evidence.
`Transfer-Encoding` must be absent or exactly `chunked` case-insensitively; it
may not coexist with `Content-Length`, whose existing bounded ASCII-decimal
checks remain. This adds no alternate HTTP client, private response-state
dependency, workflow, runtime API, release authority, or real public release
observation.

M56 validates the documented response status after M55 framing and before
comparison, redirect resolution, or body use. The status is a non-boolean
integer from 100 through 599. Every followed `302` exposes exactly one Location
field whose value is a single URI-reference from 1 through 8,000 ASCII octets
with complete percent escapes; bracket delimiters are permitted only in a
parsed authority, not a path, query, or fragment. The resolved target then
repeats the bounded HTTPS, peer, TLS, framing, deadline, size, and exact-byte
checks. RFC-0039 adds no host allowlist, raw parser, workflow, dependency,
runtime API, release authority, or real public release observation.

M57 validates each successful response body after M56 status/redirect checks.
Every `HTTPResponse.read(amount)` result must be immutable bytes no larger than
the requested amount before EOF interpretation, accounting, or local output.
Any validated `Content-Length` must exactly equal the streamed octets for both
the release document and final asset responses. RFC-0040 retains short reads,
chunked decoding through the standard-library client, close-delimited bodies
without a declaration, and independent expected asset sizes. It adds no raw
parser or cleanup, introduces no alternate client, and changes no workflow,
dependency, runtime API, release authority, or real public release observation.

M58 closes every obtained response before its created connection and makes
both close attempts even when response close fails. An active primary failure
remains primary; cleanup-only ordinary failures become content-silent
`public_release.request_failed`, while cleanup control signals remain
unwrapped. Successful cleanup occurs before redirect continuation and before
partial publication to a separate final asset path. RFC-0041 adds no rollback,
retry, workflow, dependency, runtime API, release authority, or real public
release observation.

M60 checks each fresh release document, download directory, retrieval plan,
asset target, and asset partial by final-entry `lstat()` before network or
validator work can use it. A file, directory, live link, or dangling link is a
filesystem collision; normal output collisions retain
`public_release.output_exists`, a fresh-plan collision retains
`public_release.plan_exists`, and inspection failure is content-silent. File
and hard-link publication keep their exclusive creation and no clobber
semantics. RFC-0043 makes no race-free filesystem claim and adds no workflow,
dependency, runtime API, release authority, rollback, or real public release
observation.

M61 keeps the expected candidate directory read-only by strictly resolving it
and the runner-owned output root before network or validator side effects. The
output root may not equal or resolve beneath the candidate directory; a
resolved alias receives the same stable `public_release.path_overlap` failure.
Filesystem-identity comparison across the output ancestry also catches aliases
whose resolved spelling differs on a case-insensitive filesystem. Resolution
or identity-inspection failures retain content-silent candidate or temporary-
directory codes, while a separate candidate child of the output root remains
valid. RFC-0044 makes no race-free filesystem claim and adds no workflow,
dependency, runtime API, release authority, rollback, or real public release
observation.

M62 constrains every public-release retrieval-plan asset to a portable asset
name: 1 through 255 allowed ASCII characters, no trailing period, no classic
Windows device stem, and no case-insensitive duplicate. An invalid plan fails
content-silently before asset download or creation of the asset output
directory. RFC-0045 uses no filesystem probing and adds no workflow,
dependency, runtime API, release authority, cleanup, or real public release
observation.

M63 confines subordinate stdout and subordinate stderr while the public
consumer runs its in-process validator and complete smoke. Success now emits
exactly one JSON document, and each subordinate must return an exact zero
integer; booleans, floats, integer subclasses, and custom comparison objects
fail content-silently. RFC-0046 relies on this verifier's single-thread utility
ownership and adds no workflow, dependency, runtime API, release authority, or
real public release observation.

M64 preflights staged sample bundles before extraction: at most 256 members,
1 MiB per member, and 8 MiB total declared expansion. Valid members stream in
64 KiB blocks and must reproduce their declared size. Only stored and deflated
ZIP members are admitted; BZIP2, LZMA, and unknown methods fail before
extraction. RFC-0047 adds no workflow, dependency, runtime API, cleanup
guarantee, release authority, or real public release observation.

M65 adds a portable sample member path policy to that complete preflight.
Relative paths contain at most 255 ASCII characters; each component uses the
existing portable ASCII grammar and excludes trailing periods and Windows
device stems. Exact/case-insensitive duplicates, case-ambiguous ancestors,
explicit directory entries, explicitly encoded non-regular file types, and
file/directory prefix collisions fail before extraction. ZIP members without
file-type mode bits remain compatible with common producers. RFC-0048 performs
no Unicode normalization or filesystem probing and adds no workflow,
dependency, sample-producer, runtime API, cleanup, release-authority, or real
public release observation claim.

M66 extracts admitted sample members beneath an owned same-filesystem temporary
staging directory and validates completeness there. The final sample root must
not already exist and becomes visible only through a single rename after the
staged tree is complete. Any pre-publication copy, validation, or rename failure
cleans the partial staging tree and leaves the final root absent. RFC-0049 adds
no workflow, dependency, runtime API, sample-producer, or release-authority
change; the visibility boundary is not crash-durable, provides no concurrent
filesystem race isolation, and is not a real public release observation.

M67 requires the exact sample-bundle inventory of 50 regular files after the
complete metadata/path preflight. Any unexpected member or missing member fails
with one content-silent category before extraction opens a member or creates a
staging directory. The expectation is source-defined independently of the
unchanged sample producer. RFC-0050 adds no workflow, dependency, runtime API,
sample-producer, or release-authority change; this is not content scanning, a
general archive sandbox, or a real public release observation.

M68 rejects an obvious non-regular or oversized bundle from path metadata,
opens an admitted bundle once, revalidates that its descriptor identifies a
regular file no larger than 16 MiB, and passes the same handle to `ZipFile`.
An oversized or non-regular container fails content-silently before ZIP parser
construction, central-directory parsing, member reads, or staging. RFC-0051
adds no workflow, dependency, runtime API, sample-producer, or release-authority
change; this does not replace expanded-size limits, make archive bytes
immutable, create a general archive sandbox, or establish a real public release
observation.

M69 rejects sample members whose ZIP general-purpose bit flags indicate
traditional encryption, strong encryption, or masked header values. The
content-silent rejection occurs in the complete metadata preflight before
member reads, password handling, or staging. RFC-0052 adds no password,
decryption support, workflow, dependency, runtime API, sample-producer, or
release-authority change; this is not a general archive sandbox or a real
public release observation.

M70 binds sample extraction to the digest already admitted from `SHA256SUMS`.
It hashes and rewinds the same opened handle before ZIP parsing and again after
member reads and completeness checks but before publication. A persistent
content-silent mismatch prevents publication and cleans owned staging. RFC-0053
adds no workflow, dependency, runtime API, sample-producer, or release-authority
change; it provides no immutable-input guarantee, is not a general archive
sandbox, and is not a real public release observation.

M107 requires every parsed sample member's public central
`ZipInfo.extract_version` to equal `20` after M106 and before exact inventory,
staging, or reads. This exact sample-member extraction-version profile
preflight emits stable content-silent error `sample bundle has an unsupported
extraction version`. RFC-0090 defines one central-extraction-version exact-
profile classifier with no general extraction-version semantics parser and no
payload-content read. It adds no workflow, dependency, runtime API, or producer
change, is not a general archive sandbox, and is not a real public release
observation.

M108 requires every parsed sample member's public central
`ZipInfo.create_version` to equal `20` after M107 and before exact inventory,
staging, or reads. This exact sample-member creation-version profile preflight
emits stable content-silent error `sample bundle has an unsupported creation
version`. RFC-0091 defines one central-creation-version exact-profile classifier
with no general creation-version semantics parser and no payload-content read.
It adds no workflow, dependency, runtime API, or producer change, is not a
general archive sandbox, and is not a real public release observation.

M109 requires every parsed sample member's public central
`ZipInfo.internal_attr` to equal zero after M108 and before exact inventory,
staging, or reads. This zero sample-member internal-attribute profile preflight
emits stable content-silent error `sample bundle has unsupported internal
attributes`. RFC-0092 defines one central-internal-attribute exact-profile
classifier with no text/binary content interpretation and no payload-content
read. It adds no workflow, dependency, runtime API, or producer change, is not
a general archive sandbox, and is not a real public release observation.

M110 retains sample-member timestamp compatibility after an exact fixed-
producer tuple caused 22 established architecture regressions in valid
standard-library-written fixtures. M98 still requires local/central timestamp
consistency, and the fixed producer still emits `(1980, 1, 1, 0, 0, 0)` for
reproducibility. RFC-0093 records one central-timestamp compatibility decision
with no timezone or UTC conversion and no payload-content read. It adds no
workflow, dependency, runtime API, verifier, or producer change, is not a
general archive sandbox, and is not a real public release observation.

M111 retains sample-member permission compatibility. M65 still rejects encoded
symlinks and non-regular file types while admitting missing type bits and
regular-file permission variants. The fixed producer remains UNIX mode
`0100644`; extraction performs no permission restoration. RFC-0094 records one
permission-bit compatibility decision with no exact external-attribute profile
and no payload-content read. It adds no workflow, dependency, runtime API,
verifier, or producer change, is not a general archive sandbox, and is not a
real public release observation.

M112 retains sample-member creating-system compatibility. CPython uses host
marker `0` on Windows and `3` elsewhere, while the fixed producer remains
explicitly reproducible at `3`. RFC-0095 records one host-marker compatibility
decision with no creating-system allowlist, no host-specific external-attribute
interpretation, and no payload-content read. M65's file-type boundary remains
unchanged. M112 adds no workflow, dependency, runtime API, verifier, or
producer change, is not a general archive sandbox, and is not a real public
release observation.

M113 retains sample-member compression-method compatibility. PKWARE defines
stored method `0` and deflated method `8`; Python exposes and reads both, and
its writer default is stored. Complete release smoke retains M64's exact
stored/deflated allowlist and M95's local/central method agreement while the
fixed producer remains deflated. RFC-0096 records one compression-method
compatibility decision with no exact deflate-only profile, no new decompressor,
and no payload-content read. M113 adds no workflow, dependency, runtime API,
verifier, or producer change, is not a general archive sandbox, and is not a
real public release observation.

M114 retains sample-member compression-level non-observability. Python's
`compresslevel` controls writing, but reopened sample-member metadata does not
recover that exact setting on supported runtimes. Complete release smoke
therefore does not inspect a public or protected compression-level attribute,
compressed bytes, or compressed size to infer producer configuration. The
fixed producer remains explicit at level `9`; M105's zero general-purpose flags
and M113's stored/deflated allowlist remain unchanged. RFC-0097 records one
compression-level non-observability decision with no exact level-9 verifier
profile, no inferred compressor level, and no payload-content read. M114 adds
no workflow, dependency, runtime API, verifier, or producer change, is not a
general archive sandbox, and is not a real public release observation.

M115 scopes sample-bundle byte reproducibility to the release environment.
Repeated production in one fixed resolved environment remains byte-identical,
while supported runtimes remain consumers and local staging environments rather
than cross-runtime byte-identical producers. Exact Windows probes found the
fixed bundle identical within each of CPython 3.12.13, 3.13.13, and 3.14.5;
Python 3.14's default Windows zlib-ng producer emitted different compressed
bytes from the earlier zlib producer. RFC-0098 records one sample-bundle
reproducibility-scope decision with no cross-runtime byte-identity claim and no
compressor-identity manifest field. M115 adds no workflow, allocation,
dependency, producer, verifier, runtime API, or release-authority change, is
not a general reproducible-build claim, and is not a real public release
observation.

M116 separates sample-bundle semantic portability from byte identity. An exact
Windows 3x3 matrix showed every supported CPython 3.12.13, 3.13.13, and 3.14.5
consumer accepting and extracting all 50 fixed-producer files from every one of
those runtime producers. The zlib-ng-produced archive kept its different M115
digest while yielding the same extracted source tree. RFC-0099 records one
sample-bundle semantic-portability decision and the exact cross-runtime
producer-consumer compatibility evidence. M116 adds no alternate compression
method, cross-runtime byte-identity claim, workflow, allocation, dependency,
producer, verifier, runtime API, or release-authority change. It is not a
general ZIP interoperability claim and is not a real public release
observation.

M117 retains standard GIL CPython as the supported baseline. An exact Windows
CPython 3.14.5 free-threaded installed-wheel serial compatibility probe ran with
the GIL disabled, passed version and doctor, completed 120 deterministic
headless ticks, closed normally, and preserved `engine.wrong_thread`. RFC-0100
records one free-threaded serial-compatibility decision. This observation is
not a support promise, makes no concurrent-safety claim, and adds no graphics,
performance, cross-platform, extension, workflow, dependency, runtime API, or
release-authority change. It is not a real public release observation.

M71 copies the bounded sample source into one owned checksum-admitted snapshot.
The binary spooled temporary file receives at most 16 MiB while SHA-256 is
computed, and `ZipFile` parses those exact bytes after admission. Mismatch is
content-silent before ZIP parsing or staging. RFC-0054 adds no persistent copy,
workflow, dependency, runtime API, sample-producer, or release-authority change;
it is not a general archive sandbox or a real public release observation.

M72 confines the documented `BadZipFile` and `LargeZipFile` boundary around
that private parser. Archive-controlled parser diagnostics become one stable
error, the rendered exception uses suppressed context, and owned cleanup still
runs before control returns. RFC-0055 adds no workflow, dependency, runtime
API, or sample producer change; it is not a general archive sandbox or a real
public release observation.

M73 extends that same narrow boundary to `UnicodeDecodeError` raised while the
standard ZIP reader decodes archive-controlled UTF-8 names in the central
directory or local header. The stable error, suppressed context, and owned
cleanup contract remain unchanged. RFC-0056 adds no broad Unicode catch,
workflow, dependency, runtime API, sample producer, or release authority; it
is not a general archive sandbox or a real public release observation.

M74 extends the boundary with exactly `zlib.error` raised while reading a
checksum-admitted deflated member whose compressed payload is invalid. The
stable error, suppressed context, and owned cleanup contract remain unchanged.
RFC-0057 adds no EOF/filesystem/general catch, workflow, dependency, runtime
API, sample producer, or release authority; it is not a general archive
sandbox or a real public release observation.

M75 rejects ZIP general-purpose bit 5, compressed patched data, during the
existing all-member flag preflight. The exact content-silent policy error wins
before staging, inventory validation, or member reads; M69's encryption error
retains precedence when both indicators are present. RFC-0058 adds no broad
flag allowlist, workflow, dependency, runtime API, sample producer, or release
authority; it is not a general archive sandbox or a real public release
observation.

M76 rejects the central-directory ZIP general-purpose bit 4 exposed on
compression method 8 members during the same all-member preflight. PKWARE
reserves that combination for enhanced deflating. The exact content-silent
policy error wins before staging,
inventory validation, or member reads, while encryption and compressed-patch
checks retain their precedence. Stored members carrying bit 4 remain outside
this exact decision, as do local-header inconsistencies. RFC-0059 adds no broad
flag allowlist, workflow, dependency, runtime API, sample producer, or release
authority; it is not a general archive sandbox or a real public release
observation.

M77 checks each decoded `ZipInfo.orig_filename` for an exact NUL byte before
member metadata, inventory validation, staging, or member reads. This prevents
the standard reader's documented NUL truncation from hiding an unvalidated
suffix behind an otherwise exact visible sample path. Established encryption,
compressed-patch, and enhanced-deflate errors retain precedence. RFC-0060 adds
no general normalized-name comparison, no raw parser, workflow, dependency,
runtime API, sample producer, or release authority; it is not a general archive
sandbox or a real public release observation.

M78 rejects the exact ZIP general-purpose data-descriptor bit 3 in a separate
all-member pass before member metadata, inventory validation, member reads, or
staging. Established encryption, compressed-patch, and enhanced-deflate flag
errors retain archive-wide precedence, while M78 precedes the M77 NUL-name
policy. The stable error is content-silent. RFC-0061 adds no raw descriptor
parser, no broad flag allowlist, workflow, dependency, runtime API, sample
producer, or release authority; it is not a general archive sandbox or a real
public release observation.

M79 rejects the exact Info-ZIP Unicode Path extra-field ID `0x7075` during a
separate all-member preflight before decoded-name policy, member metadata,
inventory validation, member reads, or staging. A bounded extra-field walk
preserves all established flag/descriptor precedence and emits a stable
content-silent error. RFC-0062 adds no broad extra-field ban, general name-
difference rule, workflow, dependency, runtime API, or sample producer change;
it is not a general archive sandbox or a real public release observation.

M80 rejects exact PKWARE ZIP64 extended-information extra-field ID `0x0001`
during a separate all-member preflight after M79 policy and before decoded-
name policy, member metadata, inventory validation, member reads, or staging.
The bounded extra-field walk returns a stable content-silent error. RFC-0063
adds no broad extra-field ban, raw ZIP64 parser, workflow, dependency, runtime
API, large-file support, or sample producer change; it is not a general
archive sandbox or a real public release observation.

M81 rejects parser-exposed non-empty ZIP archive and member comments after all
established flag and extra-field policy, but before decoded-name policy,
member metadata,
inventory validation, member reads, or staging. Archive-comment policy has
precedence over the separate all-member comment pass; both stable errors are
content-silent. RFC-0064 adds no raw ZIP parser, general comment scanner,
workflow, dependency, runtime API, or sample producer change; it is not a
general archive sandbox or a real public release observation.

M82 rejects every parser-exposed nonzero `ZipInfo.volume` in a separate all-
member pass after established comment policy and before decoded-name policy,
member metadata, inventory validation, member reads, or staging. The stable
content-silent error is `sample bundle uses a split-volume member`. RFC-0065
adds no raw end-record parser, no multi-volume assembler, workflow, dependency,
runtime API, or sample producer change; it is not a general archive sandbox or
a real public release observation.

M83 reads exactly the final conventional 22-byte end-of-central-directory
record after established flag, extra-field, comment, and member-volume policy.
Either nonzero disk field raises stable content-silent error
`sample bundle uses unsupported archive disk fields` before decoded-name
policy, metadata, inventory, staging, or reads. RFC-0066 adds no ZIP64 end-
record parser, end-record search, multi-volume assembler, workflow, dependency,
runtime API, or producer change; it is not a general archive sandbox or a real
public release observation.

M84 requires both conventional end-of-central-directory entry counts to equal
the standard reader's parsed member count after M83 disk-field policy and
before decoded-name policy, metadata, inventory, staging, or reads. The stable
content-silent error is `sample bundle archive entry counts are inconsistent`.
RFC-0067 adds no ZIP64 end-record parser, sentinel resolution, multi-volume
assembler, workflow, dependency, runtime API, or producer change; it is not a
general archive sandbox or a real public release observation.

M85 requires the final conventional central-directory size plus offset to land
exactly at the final end-of-central-directory record after M84 entry-count
policy and before decoded-name policy, metadata, inventory, staging, or reads.
The stable content-silent error is `sample bundle central directory placement
is inconsistent`. RFC-0068 adds no central-directory record parser, prepended
executable support, self-extracting archive support, workflow, dependency,
runtime API, or producer change; it is not a general archive sandbox or a real
public release observation.

M86 requires the earliest parser-exposed local-header offset to be zero after
M85 central-directory placement policy and before decoded-name policy,
metadata, inventory, staging, or reads. The stable content-silent error is
`sample bundle first local header placement is inconsistent`. RFC-0069 adds no
local-header parser, inter-member layout validator, workflow, dependency,
runtime API, or producer change; it is not a general archive sandbox or a real
public release observation.

M87 requires all parser-exposed local-header offsets to be distinct after M86
first-offset policy and before decoded-name policy, metadata, inventory,
staging, or reads. The stable content-silent error is `sample bundle local
header offsets are inconsistent`. RFC-0070 adds no local-header parser, offset
ordering/bounds rule, inter-member layout validator, workflow, dependency,
runtime API, or producer change; it is not a general archive sandbox or a real
public release observation.

M88 requires strictly increasing local-header offsets in parser-exposed archive
order after M87 distinctness and before decoded-name policy, metadata,
inventory, staging, or reads. The stable content-silent error is `sample bundle
local header offsets are out of order`. RFC-0071 adds no local-header parser,
central-directory record parser, offset-bounds or physical-contiguity rule, no
inter-member layout validator, workflow, dependency, runtime API, or producer
change. This fixed-producer profile is not a general archive sandbox and is not
a real public release observation.

M89 requires every parser-exposed local-header offset to remain strictly before
the conventional central directory after M88 ordering and before decoded-name
policy, metadata, inventory, staging, or reads. The stable content-silent error
is `sample bundle local header offsets are out of bounds`. RFC-0072 adds no
local-header parser, central-directory record parser, local-record extent rule,
or inter-member layout validator, workflow, dependency, runtime API, or
producer change. This fixed-producer profile is not a general archive sandbox
and is not a real public release observation.

M90 requires the fixed producer's four-byte local-header signature
`PK\x03\x04` at every parser-exposed offset after M89 bounds and before decoded-
name policy, metadata, inventory, staging, or reads. The stable content-silent
error is `sample bundle local header signature is inconsistent`. RFC-0073
defines a signature classifier, with no local-header field parser, central-
directory record parser, record-extent rule, or inter-member layout validator,
workflow, dependency, runtime API, or producer change. This fixed-producer
profile is not a general archive sandbox and is not a real public release
observation.

M91 requires every parser-exposed offset to leave room for ZIP's 30-byte fixed
local-header prefix before the conventional central directory. Its prefix-bound
classifier runs after M90 signatures and before decoded-name policy, metadata,
inventory, staging, or reads. The stable content-silent error is `sample bundle
local header prefixes are out of bounds`. RFC-0074 adds no local-header field
parser, record-extent or payload-bound rule, no inter-member layout validator,
workflow, dependency, runtime API, or producer change. This fixed-producer
profile is not a general archive sandbox and is not a real public release
observation.

M92 reads exactly the local file-name and extra-field length declarations after
M91 prefix bounds, then requires each resulting local-header variable envelope
to end no later than the conventional central directory. Its two-field
envelope-bound classifier runs before decoded-name policy, metadata, inventory,
staging, or reads. The stable content-silent error is `sample bundle local
header envelopes are out of bounds`. RFC-0075 performs no local-name comparison,
extra-field parsing, payload or next-header bound, inter-member layout
validation, workflow, dependency, runtime API, or producer change. This fixed-
producer profile is not a general archive sandbox and is not a real public
release observation.

M93 reads each bounded local file-name and requires its raw bytes to equal the
parser-exposed central name reconstructed with the central UTF-8 flag or
default CP437 encoding. Its one raw local-name consistency classifier runs
after M92 and before decoded-name policy, metadata, inventory, staging, or
reads. The stable content-silent error is `sample bundle local header names are
inconsistent`. RFC-0076 performs no local-flag comparison, extra-field
comparison, payload or next-header bound, inter-member layout validation,
workflow, dependency, runtime API, or producer change. This fixed-producer
profile is not a general archive sandbox and is not a real public release
observation.

M94 reads each two-byte local general-purpose flag field and requires exact
equality with the parser-exposed central `ZipInfo.flag_bits`. Its one two-byte
local-flag consistency classifier runs after M93 and before decoded-name
policy, metadata, inventory, staging, or reads. The stable content-silent error
is `sample bundle local header flags are inconsistent`. RFC-0077 performs no
local compression-method comparison, no extra-field comparison, no field-wide
local/central comparison, no payload or next-header bound, and no inter-member
layout validator, workflow, dependency, runtime API, or producer change. This
fixed-producer profile is not a general archive sandbox and is not a real
public release observation.

M95 reads each two-byte local compression-method field and requires exact
equality with the parser-exposed central `ZipInfo.compress_type`. Its one two-
byte local-compression-method consistency classifier runs after M94 and before
decoded-name policy, metadata, inventory, staging, or reads. The stable
content-silent error is `sample bundle local header compression methods are
inconsistent`. RFC-0078 performs no local extra-field comparison, no
version/time/CRC/size comparison, no field-wide local/central comparison, no
payload or next-header bound, and no inter-member layout validator, workflow,
dependency, runtime API, or producer change. This fixed-producer profile is not
a general archive sandbox and is not a real public release observation.

M96 reads each bounded local extra field and requires exact equality with
public central `ZipInfo.extra`. Its one bounded local-extra equality classifier
runs after M95 and before decoded-name policy, metadata, inventory, staging, or
reads. The stable content-silent error is `sample bundle local header extra
fields are inconsistent`. RFC-0079 adds no extra-field semantics parser, broad
extra-field ban, new field-ID policy, version/time/CRC/size or field-wide
local/central comparison, payload or next-header bound, inter-member layout
validator, workflow, dependency, runtime API, or producer change. This fixed-
producer profile is not a general archive sandbox and is not a real public
release observation.

M97 requires the two-byte local extraction-version pair to exactly equal the
public central `ZipInfo.extract_version` and `ZipInfo.reserved` pair. Its one
two-byte local-extraction-version consistency classifier runs after M96 and
before decoded-name policy, metadata, inventory, staging, or reads. The stable
content-silent error is `sample bundle local header extraction versions are
inconsistent`. RFC-0080 adds no supported-version allowlist, no
time/CRC/size comparison, and no inter-member layout validator, workflow,
dependency, runtime API, or producer change. This fixed-producer profile is
not a general archive sandbox and is not a real public release observation.

M98 requires each four-byte local DOS modification timestamp to exactly equal
the bytes represented by public central `ZipInfo.date_time`. Its one four-byte
local-timestamp consistency classifier runs after M97 and before decoded-name
policy, metadata, inventory, staging, or reads. The stable content-silent error
is `sample bundle local header timestamps are inconsistent`. RFC-0081 is no
timestamp semantics validator, performs no timezone or UTC conversion, adds
no CRC/size comparison or inter-member layout validator, and changes no
workflow, dependency, runtime API, or producer. This fixed-producer profile is
not a general archive sandbox and is not a real public release observation.

M99 requires each four-byte local-header CRC-32 value to exactly equal public
central `ZipInfo.CRC` encoded little-endian. Its one four-byte local-CRC-32
consistency classifier runs after M98 and before decoded-name policy, metadata,
inventory, staging, or reads. The stable content-silent error is `sample bundle
local header CRC-32 values are inconsistent`. RFC-0082 performs no CRC
recomputation, payload-integrity certification, compressed/uncompressed size
comparison, payload or next-header bound, or inter-member layout validator, and
changes no workflow, dependency, runtime API, or producer. This fixed-producer
profile is not a general archive sandbox and is not a real public release
observation.

M100 requires each four-byte local-header compressed size to exactly equal
public central `ZipInfo.compress_size` encoded little-endian. Its one four-byte
local-compressed-size consistency classifier runs after M99 and before decoded-
name policy, metadata, inventory, staging, or reads. The stable content-silent
error is `sample bundle local header compressed sizes are inconsistent`.
RFC-0083 performs no decompression or recompression, no uncompressed-size
comparison, no payload or next-header bound, and no inter-member layout
validator, and changes no workflow, dependency, runtime API, or producer. This
fixed-producer profile is not a general archive sandbox and is not a real
public release observation.

M101 requires each four-byte local-header uncompressed size to exactly equal
public central `ZipInfo.file_size` encoded little-endian. Its one four-byte
local-uncompressed-size consistency classifier runs after M100 and before
decoded-name policy, metadata, inventory, staging, or reads. The stable
content-silent error is `sample bundle local header uncompressed sizes are
inconsistent`. RFC-0084 performs no decompression or recompression, no
compression-ratio policy, no payload or next-header bound, and no inter-member
layout validator, and changes no workflow, dependency, runtime API, or
producer. This fixed-producer profile is not a general archive sandbox and is
not a real public release observation.

M102 requires every calculated compressed payload end to remain at or before
the next ordered local header or conventional central directory. Its one
compressed-payload upper-bound classifier runs after M101 and before decoded-
name policy, metadata, inventory, staging, or reads. The stable content-silent
error is `sample bundle member payloads are out of bounds`. RFC-0085 performs
no decompression or recompression, adds no exact-contiguity requirement, no gap
or adjacency ban, and no payload-integrity certification, and changes no
workflow, dependency, runtime API, or producer. This fixed-producer profile is
not a general archive sandbox and is not a real public release observation.

M103 requires every calculated compressed payload end to equal the next
ordered local header or conventional central directory. Its exact compressed-
payload contiguity preflight runs after M102 and before decoded-name policy,
metadata, inventory, staging, or reads. The stable content-silent error is
`sample bundle member payloads are not contiguous`. RFC-0086 defines one
compressed-payload equality classifier with no decompression or recompression,
no payload-content read, and no payload-integrity certification. It changes no
workflow, dependency, runtime API, or producer, is not a general archive
sandbox, and is not a real public release observation.

M104 requires every parsed sample member's public central `ZipInfo.extra` to be
empty after established Unicode Path, ZIP64, local/central consistency, bounds,
and contiguity policy. This empty sample-member extra-field profile preflight
runs before decoded-name policy, metadata, inventory, staging, or reads. The
stable content-silent error is `sample bundle contains an unsupported extra
field`. RFC-0087 defines one central-extra emptiness classifier with no extra-
field semantics parser and no payload-content read. It adds no workflow,
dependency, runtime API, or producer change, is not a general archive sandbox,
and is not a real public release observation.

M105 requires every parsed sample member's public central `ZipInfo.flag_bits`
to equal zero after established specific-flag, local/central consistency,
payload-layout, and M104 extra-field policy. This zero sample-member general-
purpose-flag profile preflight runs after decoded-name and member-metadata
policy but before exact inventory, staging, or reads. The stable content-silent
error is `sample bundle contains unsupported general-purpose flags`. RFC-0088
defines one central-flag zero-profile classifier with no flag-semantics parser
and no payload-content read. It adds no workflow, dependency, runtime API, or
producer change, is not a general archive sandbox, and is not a real public
release observation.
M76 remains method-specific; M105 also rejects residual nonzero flags such as
bit 4 on a stored member after established member-metadata diagnostics.

M106 requires every parsed sample member's public central `ZipInfo.reserved` to
equal zero after M105 and before exact inventory, staging, or reads. This zero
sample-member extraction-version reserved-byte profile preflight emits stable
content-silent error `sample bundle has a nonzero extraction-version reserved
byte`. RFC-0089 defines one central-reserved zero-profile classifier with no
extraction-version semantics parser and no payload-content read. It adds no
workflow, dependency, runtime API, or producer change, is not a general archive
sandbox, and is not a real public release observation.

The M9 Box2D probe is also evaluation tooling, not a normal quality command or
dependency. Run it only in an isolated environment with an explicit candidate:

```console
uv run --no-project --python 3.12 --with box2d-python==0.1.2 python scripts/probe_box2d_candidate.py
```

A successful result establishes only bounded same-binary headless/lifecycle
smoke. It does not admit the binding or claim cross-platform determinism; see
[ADR-0024](docs/adr/0024-defer-box2d-v3-plugin-after-admission-review.md).

Repeat-build verification and release staging require new empty output
directories. The tag workflow is
defined for a future maintainer-created signed annotated `vVERSION` tag at an
exact `origin/main` commit. This repository task does not create a tag, publish
a GitHub release, configure a signing-key allowlist, or upload to PyPI.

M118 records one unsupported prerelease compatibility observation. One exact
Windows CPython 3.15.0b1 environment installed the pure wheel only through an
explicit metadata override. Version, deterministic headless execution, orderly
close, and owner-thread rejection worked; `doctor` correctly rejected the
unsupported interpreter. This is no support promise, changes no workflow,
metadata, dependency, runtime API, or CI allocation, and is not a real public
release observation. See [RFC-0101](docs/rfcs/0101-retain-python315-prerelease-outside-support.md).

## Contributing and project policy

Contributions use the [Developer Certificate of Origin](CONTRIBUTING.md), not a CLA. Start with the [first-contribution walkthrough](docs/first-contribution.md) and [roadmap board](ROADMAP.md). Please also read the [code of conduct](CODE_OF_CONDUCT.md), [security policy](SECURITY.md), [governance model](GOVERNANCE.md), and repository guidance in [MAINTAINERS.md](MAINTAINERS.md).

LudoWeave Engine is licensed under the [Apache License 2.0](LICENSE).
