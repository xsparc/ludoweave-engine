# LudoWeave Engine

**Build worlds humans can play and agents can operate.**

LudoWeave is a community-alpha release candidate for deterministic, headless-first Python 2D and layered-2D worlds. M0 established the repository contract and lifecycle skeleton. M1 added the deterministic world/application core. M2 added typed persistent commands, atomic transactions and receipts, canonical authority snapshots and hashes, deterministic random streams, verified replay/checkpoints, immutable branches, and a data-only headless CLI workflow. M3 added isolated Null and wgpu 2D rendering. M4 added provider-neutral input, content-addressed assets, bounded collision/audio contracts, and Clockwork Arena. M5 added typed capability-gated agent control through Python, CLI, and local stdio MCP. M6 added deterministic release artifacts, explicit API status, contribution guides, and release provenance staging. M7-M10 recorded native/SDL3/Box2D deferrals and added a bounded semantic inspector. M11 adds headless rich 2D authoring records. M12 adds preview data-only plugin manifests and deterministic compatibility checks without a plugin loader. M13 evaluates offline correction branches, records the replay input-history gap, and defers network rollback. M14 retains layered 2D and defers constrained 3D after an installed-surface audit. M15 confirms the command/inspector foundation but defers a visual editor until the authoring and support contract is complete. M16 retains the inert plugin boundary and defers executable WASM mods behind a complete security gate. M17 adds explicit installed render-device conformance. M18 adds explicit installed agent-tool conformance over the existing 12-tool service. M19 adds explicit installed `WorldStore` conformance over production and reference implementations. M20 retains experimental command/receipt stability after an installed readiness audit identifies the missing compatibility evidence. M21 adds a bounded receipt/1 reader and frozen single-version compatibility baseline without promoting stability. M22 fixes the exact built-in operation/version argument policy and exercises all seven shapes from installed artifacts. M23 fixes receipt-v1 semantic-diff meanings and diagnostic-code evolution with installed same-version evidence. M24 adds strict cross-version corpus admission machinery while retaining its current one-version result as false. M25 adds strict external-feedback admission with an empty reviewed corpus. M26 adds strict supported-release-channel admission with an empty reviewed release set. M27 adds strict external-contributor rehearsal admission while retaining its empty reviewed result as false. M28 adds strict external sample-game adoption admission while retaining its empty reviewed result and zero count. M29 adds strict contributor-retention admission while retaining its empty reviewed result and zero count. M30 adds strict published-wheel installation-matrix admission while retaining its empty reviewed result. M31 adds strict issue-response and pull-request-review latency admission while retaining its empty reviewed result and defining no SLA. M32 adds strict CI replay-divergence-rate admission while retaining its empty reviewed execution manifest and no measured rate. M33 adds strict controlled benchmark-regression-rate admission while retaining its empty reviewed comparison manifest and no measured rate. M34 adds strict agent-tool recovery-rate admission while retaining its empty reviewed call manifest and no measured rate. M35 adds strict third-party conformance-adoption admission while retaining an empty reviewed submission manifest and zero passing external implementations. None of these runners discovers or admits providers. This is not yet a complete game runtime; most APIs remain experimental and the M12 plugin surface is preview.

M36-M44 reduce hosted-runner waste, qualify documentation changes from a
trusted base, enforce same-source distribution byte reproducibility, and reject
unverified/non-main release tags before expensive work. M40 additionally keeps
the GitHub release private as a draft until its exact uploaded asset names,
sizes, and SHA-256 digests match local staging, without weakening substantive
validation. M41 also requires the draft's authenticated release-notes body to
exactly match staged `RELEASE_NOTES.md` without adding a hosted allocation.
M42 then confirms the same authenticated release ID's final public prerelease
state, timestamp, notes, and assets without adding a hosted allocation.
M43 retrieves every validated numeric asset ID through the authenticated binary
endpoint and rehashes the downloaded set against that same release document,
again without adding a hosted allocation. M44 then verifies exact-source SLSA
provenance for every retrieved asset and the pure wheel's SPDX SBOM
attestation, with the same allocation topology.

## Current capabilities

- Explicit engine initialization, fixed-tick run, shutdown, and close behavior.
- Monotonic real time and deterministic virtual time behind one protocol.
- A backend-neutral rendering boundary with a null validation backend.
- Structured errors, JSON diagnostics, and a headless example.
- Tested architecture rules and a pure-Python wheel.
- Deterministic generational entity allocation with checked stale-handle failures.
- Explicit immutable component schemas and forward migration paths without global registration.
- Canonical dense/sparse world storage checked against an independent dictionary model.
- Storage-neutral queries with stable-order, changed-epoch, and explicit writeback contracts.
- Atomic local command buffers whose deferred entity tokens are exact buffer identities.
- Copy-owned typed resource singletons and input-order-independent conflict-aware schedule planning.
- Exact fixed-step application pumping with immutable input and declaration-enforcing system contexts.
- Canonical versioned commands, atomic staged application, semantic diffs, and machine receipts.
- Complete snapshots and engine-owned deterministic named random streams.
- Self-contained verified replay/checkpoint files and immutable parent-referenced branches.
- Project-confined `apply`, `snapshot`, `replay`, and `diff` command workflows.
- Backend-neutral render resources, immutable extraction, explicit render graphs, and deferred generational-handle destruction.
- An optional wgpu/rendercanvas/GLFW adapter with instanced atlas sprites, tiles, orthographic cameras, debug fixtures, resize, and offscreen capture.
- Immutable platform events/action snapshots, validated `asset://` content, deterministic 2D collision, minimal Null audio, and an ECS-authoritative playable sample.
- A transport-independent agent service with 12 typed tools, default read-only capabilities, bounded/redacted data, serialized safe-point mutations, and canonical receipts.
- A local MCP `2025-11-25` stdio adapter and Agent World Builder acceptance loop with no network listener or arbitrary code execution.
- Exact-tick sprite animation, bitmap text layout, immutable tilemaps,
  fixed-point particles, and a Null-audio mix graph through existing render
  records.
- Canonical inert plugin manifests, deterministic environment/dependency
  compatibility reports, and an explicitly invoked local checker with no
  discovery or code execution.
- Deterministic constrained-3D decision evidence that leaves the public and
  provider-neutral runtime surfaces layered-2D-only.
- Deterministic visual-editor admission evidence that confirms the existing
  semantic foundation while leaving GUI/editor runtime surfaces absent.
- Deterministic WASM-mod security evidence that confirms the inert plugin
  boundary while leaving runtimes, guest execution, WASI, and host calls absent.
- An accepted [asset-cache cleanup threat
  model](security/cache-cleanup-threat-model.md) that defines the future
  filesystem, concurrency, recovery, and safe-refusal gate while leaving
  cleanup unimplemented.
- An accepted [cache-cleanup platform-capability
  decision](security/cache-cleanup-platform-capability-decision.md) that rejects
  partial portable primitives and admits no platform without real-host adapter
  evidence.
- A test-only [Windows cache-cleanup capability
  probe](security/cache-cleanup-windows-capability-probe.md) that exercises a
  bounded owned-handle chain without admitting Windows or runtime cleanup.
- A test-only [Windows directory-junction refusal
  probe](security/cache-cleanup-windows-junction-probe.md) that executes one
  NTFS reparse case without adding runtime shelling or platform admission.
- A test-only [Windows retained-parent substitution
  probe](security/cache-cleanup-windows-retained-parent-substitution-probe.md)
  that distinguishes an opened original directory from a junction rebound at
  its former name without adding runtime behavior or platform admission.
- A test-only [Windows cross-process substitution
  probe](security/cache-cleanup-windows-cross-process-substitution-probe.md)
  that moves the fixed namespace change to a non-inheriting child process
  without adding runtime behavior, another CI allocation, or platform admission.
- A test-only [Windows share-delete exclusion
  probe](security/cache-cleanup-windows-share-delete-exclusion-probe.md) that
  pairs a blocked child rename with the identical post-close success without
  adding runtime behavior, another CI allocation, or platform admission.
- A test-only [Windows native sharing-violation
  probe](security/cache-cleanup-windows-native-sharing-violation-probe.md) that
  captures one direct bounded child native result without adding runtime
  behavior, another CI allocation, or platform admission.
- A test-only [Windows child-owned share-delete
  handshake](security/cache-cleanup-windows-child-owned-share-delete-handshake.md)
  that orders a distinct blocker process's acquisition and close without
  adding runtime behavior, another CI allocation, or platform admission.
- A test-only [Windows abrupt blocker-owner termination
  probe](security/cache-cleanup-windows-abrupt-blocker-termination-probe.md)
  that bypasses graceful close and bounds one forced owner-termination
  transition without adding runtime behavior, recovery, or CI allocation.
- A test-only [Windows blocker control-pipe EOF
  probe](security/cache-cleanup-windows-control-pipe-eof-probe.md) that closes
  the parent control writer after readiness without adding runtime behavior,
  arbitrary pipe recovery, or CI allocation.
- A test-only [Windows blocker invalid-control-token
  probe](security/cache-cleanup-windows-invalid-control-token-probe.md) that
  sends one fixed non-release byte after readiness without adding runtime
  behavior, arbitrary malformed-input handling, or CI allocation.
- A test-only [Windows blocker broken-control-pipe
  probe](security/cache-cleanup-windows-broken-control-pipe-probe.md) that
  captures one direct late native write result after bounded owner termination
  without adding runtime recovery, a universal error contract, or CI
  allocation.
- A test-only [Windows live-blocker wait-timeout
  probe](security/cache-cleanup-windows-live-wait-timeout-probe.md) that
  captures one immediate wait timeout while ownership and denial remain live,
  without adding runtime recovery, timeout policy, or CI allocation.
- A test-only [Windows acknowledged-release timeout
  probe](security/cache-cleanup-windows-acknowledged-release-timeout-probe.md)
  that separates accepted release intent from native handle close without
  adding runtime recovery, graceful-close policy, or CI allocation.
- A test-only [Windows duplicated-handle retention
  probe](security/cache-cleanup-windows-duplicated-handle-probe.md) that proves
  one same-process duplicate retains the observed denial after the original
  closes, without adding inherited-handle claims, runtime behavior, or CI
  allocation.
- A test-only [Windows inherited-handle retention
  probe](security/cache-cleanup-windows-inherited-handle-probe.md) that proves
  one explicitly allowlisted child handle retains the observed denial after
  the parent closes its handle, without adding concurrency-safe inheritance,
  runtime behavior, or CI allocation.
- A test-only [Windows inherited-launch failure
  probe](security/cache-cleanup-windows-inherited-launch-failure-probe.md) that
  proves one real missing-executable failure restores noninheritability while
  preserving parent ownership, without adding arbitrary rollback, runtime
  behavior, or CI allocation.
- A test-only [Windows inherited-handle restoration-failure
  probe](security/cache-cleanup-windows-inherited-restore-failure-probe.md) that
  proves one already-created child is reaped before an injected restore error
  escapes while keeping parent repair duty explicit, without adding runtime
  behavior or CI allocation.
- A test-only [Windows concurrent broad-inheritance leak
  probe](security/cache-cleanup-windows-concurrent-inheritance-leak-probe.md)
  that proves one controlled broad launch retains the temporarily inheritable
  blocker after parent and intended-child close, without adding runtime
  coordination or CI allocation.
- A test-only [Windows concurrent explicit-list isolation
  probe](security/cache-cleanup-windows-concurrent-explicit-inheritance-probe.md)
  that proves two overlapping one-handle lists isolate distinct blockers in
  both release orders, without adding runtime coordination or CI allocation.
- A test-only [Windows concurrent explicit-list launch-failure
  probe](security/cache-cleanup-windows-concurrent-explicit-launch-failure-probe.md)
  that proves a concurrent missing-executable launch releases its distinct root
  while the successful child retains only its own blocker, without runtime or
  CI expansion.
- A test-only [Windows concurrent explicit-list restoration-failure
  probe](security/cache-cleanup-windows-concurrent-explicit-restore-failure-probe.md)
  that proves one injected restoration error reaps only its child while the
  concurrent survivor retains only its distinct blocker, without runtime or
  CI expansion.
- A test-only [Windows concurrent explicit-list abrupt-termination
  probe](security/cache-cleanup-windows-concurrent-explicit-abrupt-termination-probe.md)
  that proves one forcibly terminated child releases only its inherited
  blocker while the concurrent survivor remains live, without runtime or CI
  expansion.
- A test-only [Windows exclusive-root acquisition
  probe](security/cache-cleanup-windows-exclusive-root-acquisition-probe.md)
  that proves two-way fail-closed no-sharing acquisition and deterministic
  release without introducing a runtime lock, cleanup authority, or CI
  expansion.
- A test-only [Windows descendant non-exclusion
  probe](security/cache-cleanup-windows-descendant-non-exclusion-probe.md) that
  proves a zero-sharing directory owner does not recursively exclude a separate
  descendant file owner, without runtime or CI expansion.
- A test-only [Windows cooperative-lock
  probe](security/cache-cleanup-windows-cooperative-lock-probe.md) that proves
  multiple shared owners collectively refuse one exclusive coordination-range
  owner through the last release, without granting cleanup authority.
- A test-only [Windows cooperative-lock substitution
  probe](security/cache-cleanup-windows-cooperative-lock-substitution-probe.md)
  that proves pathname replacement splits live participants across independent
  file identities and lock generations, without runtime or CI expansion.
- A test-only [Windows live substitution-exclusion
  probe](security/cache-cleanup-windows-cooperative-lock-live-substitution-exclusion-probe.md)
  that blocks rename/replacement through the final protected participant while
  preserving the zero-participant identity gap and no-authority boundary.
- A test-only [Windows cooperative-lock abrupt-settlement
  probe](security/cache-cleanup-windows-cooperative-lock-abrupt-settlement-probe.md)
  that proves one abruptly terminated owner settles while a survivor retains
  both protections, before final settlement releases both ownership types.
- A test-only [Windows protected guardian-handoff
  probe](security/cache-cleanup-windows-protected-guardian-handoff-probe.md)
  that bridges a participant-free interval without treating identity
  protection as cooperative range ownership or runtime authority.
- A test-only [Windows guardian abrupt-handoff
  probe](security/cache-cleanup-windows-guardian-abrupt-handoff-probe.md) that
  proves a joined participant retains independent protection after the
  overlapping guardian is abruptly terminated and reaped.
- A test-only [Windows overlapping guardian-rotation
  probe](security/cache-cleanup-windows-overlapping-guardian-rotation-probe.md)
  that preserves namespace protection through one already-overlapped guardian
  loss and later participant close without claiming restart or recovery.
- A test-only [Windows zero-owner guardian restart-boundary
  probe](security/cache-cleanup-windows-zero-owner-guardian-restart-boundary-probe.md)
  that distinguishes benign identity reacquisition from pathname substitution
  during an unprotected interval without claiming recovery or authority.
- A test-only [Windows expected-identity guardian admission
  probe](security/cache-cleanup-windows-expected-identity-guardian-admission-probe.md)
  that compares the expected identity on the same protecting handle and
  rejects a preexisting replacement without claiming identity authority.
- A test-only [Windows hard-link alias non-exclusion
  probe](security/cache-cleanup-windows-hard-link-alias-non-exclusion-probe.md)
  that distinguishes exact-name protection from root-confined ownership.
- A test-only [Windows post-admission hard-link creation
  probe](security/cache-cleanup-windows-post-admission-hard-link-creation-probe.md)
  that proves matching guardian admission does not freeze the link set.
- A test-only [Windows hard-link alias deletion non-exclusion
  probe](security/cache-cleanup-windows-hard-link-alias-deletion-non-exclusion-probe.md)
  that proves exact-name protection does not exclude peer-link removal.
- A test-only [Windows hard-link alias delete/recreate ABA
  probe](security/cache-cleanup-windows-hard-link-alias-delete-recreate-aba-probe.md)
  that proves guardian admission does not freeze peer-path membership or make
  a one-link observation durable ownership.
- A test-only [Windows independent hard-link alias mutator ABA
  probe](security/cache-cleanup-windows-independent-hard-link-alias-mutator-aba-probe.md)
  that reproduces the transition with a distinct sibling mutation process
  while preserving the same-principal evidence limit.
- A test-only [Windows hard-link alias mutator abrupt-loss
  probe](security/cache-cleanup-windows-hard-link-alias-mutator-abrupt-loss-probe.md)
  that records the alias-absent, one-link state after the mutation child is
  terminated and reaped before recreation.
- A test-only [Windows hard-link alias mutator abrupt-loss-after-recreate
  probe](security/cache-cleanup-windows-hard-link-alias-mutator-abrupt-loss-after-recreate-probe.md)
  that records the alias-present, two-link state after the mutation child is
  terminated and reaped following exact recreation.
- A test-only [Windows hard-link alias mutator control-pipe EOF after
  recreation
  probe](security/cache-cleanup-windows-hard-link-alias-mutator-control-pipe-eof-after-recreate-probe.md)
  that records exact fixture exit 5 and the persistent alias-present, two-link
  state after closing only the parent control writer following recreation.
- A test-only [Windows hard-link alias mutator invalid control token after
  recreation
  probe](security/cache-cleanup-windows-hard-link-alias-mutator-invalid-control-token-after-recreate-probe.md)
  that records exact fixture exit 5 and the persistent alias-present, two-link
  state after writing and flushing one fixed invalid byte following recreation.
- A test-only [Windows hard-link alias mutator valid close prefix with trailing
  byte after recreation
  probe](security/cache-cleanup-windows-hard-link-alias-mutator-valid-close-prefix-trailing-byte-after-recreate-probe.md)
  that records exact `closed`, exit 0, and the persistent two-link state after
  writing and flushing fixed `!?` once following recreation.
- A test-only [Windows hard-link alias mutator invalid prefix with valid close
  suffix after recreation
  probe](security/cache-cleanup-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-after-recreate-probe.md)
  that records no close acknowledgement, exit 5, and the persistent two-link
  state after writing and flushing fixed `?!` once following recreation.
- A test-only [Windows hard-link alias mutator invalid-prefix open-writer
  settlement after recreation
  probe](security/cache-cleanup-windows-hard-link-alias-mutator-invalid-prefix-valid-close-suffix-open-writer-settlement-after-recreate-probe.md)
  that records exit 5 while the parent writer remains open, separating the
  fixed rejection from control-pipe EOF for the bounded fixture.
- A test-only [Windows hard-link alias mutator late valid-close delivery-
  failure after invalid settlement
  probe](security/cache-cleanup-windows-hard-link-alias-mutator-late-valid-close-delivery-failure-after-invalid-settlement-probe.md)
  that records one local buffered-byte acceptance followed by failed flush
  delivery after the child has already exited.
- A test-only [Windows hard-link alias mutator buffered-close delivery-failure
  after invalid settlement
  probe](security/cache-cleanup-windows-hard-link-alias-mutator-buffered-close-delivery-failure-after-invalid-settlement-probe.md)
  that records generic delivery failure from direct close and final stream
  closure without a preceding failed late flush.
- A test-only [Windows hard-link alias mutator repeated buffered-close after
  delivery-failure
  probe](security/cache-cleanup-windows-hard-link-alias-mutator-repeated-buffered-close-after-delivery-failure-probe.md)
  that records a second close returning `None` after the failed first close
  has already left the parent stream closed.
- A test-only [Windows hard-link alias mutator closed-stream flush after
  delivery-failure
  probe](security/cache-cleanup-windows-hard-link-alias-mutator-closed-stream-flush-after-delivery-failure-probe.md)
  that records one later flush raising generic `ValueError` while the concrete
  stream remains closed.
- A test-only [Windows hard-link alias mutator closed-stream write after
  delivery-failure
  probe](security/cache-cleanup-windows-hard-link-alias-mutator-closed-stream-write-after-delivery-failure-probe.md)
  that records one later `write(b"!")` raising generic `ValueError` while the
  concrete stream remains closed.
- A [Windows cache-cleanup readiness
  refresh](security/cache-cleanup-windows-readiness-refresh.md) that consolidates
  M149-M198, keeps cleanup deferred, and requires future work to resolve a
  named admission criterion rather than extend standalone stream probing.
- A [Windows singleton-link refusal
  policy](security/windows-cache-cleanup-singleton-link-refusal-policy.md) that
  requires exactly one handle-derived link at admission and immediately before
  mutation, refuses every other or uncertain count, and rejects name
  enumeration as authority without admitting cleanup.
- A [Windows cleanup-authority admission
  policy](security/windows-cache-cleanup-authority-admission-policy.md) that
  requires exact effective-token, retained trusted-root, and separate durable-
  generation bindings before any future private authority can be issued,
  without adding runtime cleanup or CI allocation.
- A [Windows use-time revalidation
  policy](security/windows-cache-cleanup-use-time-revalidation-policy.md) that
  requires the complete admitted token, root, generation, lineage, and
  candidate state to be freshly equal immediately before every future mutation
  boundary.
- A [Windows cleanup protocol and receipt
  policy](security/windows-cache-cleanup-protocol-receipt-policy.md) that
  separates bounded canonical request, acknowledgement, and path-free typed
  receipt evidence from canonical world transactions and private authority.
- A [Windows cleanup durable recovery
  policy](security/windows-cache-cleanup-durable-recovery-policy.md) that
  requires bounded write-ahead intent, same-filesystem no-replace quarantine,
  idempotent reconciliation, and fail-closed handling of ambiguous or altered
  recovery evidence before Windows cleanup can be admitted.
- A [Windows cache-cleanup cross-principal validation
  contract](security/windows-cache-cleanup-cross-principal-validation-contract.md)
  that requires a genuinely distinct untrusted principal, unrelated process
  and session topologies, deterministic barriers, and real ACL, handle, alias,
  and reparse pressure before criterion 6 can be resolved.
- A source-only [Windows cross-principal evidence
  validator](security/windows-cache-cleanup-cross-principal-evidence-validator.md)
  that checks one stable bounded canonical artifact and ships an explicitly
  all-`not_run` reviewed fixture without claiming criterion 6 or admitting
  cleanup.
- A [Windows independent-host validation
  contract](security/windows-cache-cleanup-independent-host-validation-contract.md)
  that requires observed capability profiles, independent hosts, explicit
  filesystem refusals, and separated interruption classes before criterion 7
  can be resolved.
- A source-only [Windows independent-host evidence
  validator](security/windows-cache-cleanup-independent-host-evidence-validator.md)
  that checks a bounded canonical host artifact only when bound to a separately
  validated M206 companion, while retaining an all-`not_run` reviewed fixture
  and false Windows admission.
- A [Windows independent-host collection-authority
  policy](security/windows-cache-cleanup-independent-host-collection-authority-policy.md)
  that confines any future privileged collector to offline, single-use,
  host/lane/barrier-bound actions with reviewed evidence custody and teardown,
  without adding a harness or qualifying run.
- A source-only [Windows independent-host collection-plan
  validator](security/windows-cache-cleanup-independent-host-collection-plan-validator.md)
  that checks one bounded sanitized all-`not_run` plan, exact closed matrices,
  and false authority/admission claims without adding a privileged harness.
- A test-only [Windows independent-host process-containment
  probe](security/windows-cache-cleanup-independent-host-process-containment-probe.md)
  that proves suspended assignment, exact retained root/descendant Job
  membership, and bounded termination settlement on one current host without
  collecting evidence or admitting Windows cleanup.
- A test-only [Windows local control-channel
  probe](security/windows-cache-cleanup-local-control-channel-probe.md) that
  proves an explicit logon-SID DACL, native retained-client identity, bounded
  challenged sequencing, and replay/wrong-challenge/disconnect refusal on one
  current host without collecting evidence or admitting Windows cleanup.
- A test-only [Windows local control token-binding
  probe](security/windows-cache-cleanup-local-control-token-binding-probe.md)
  that proves retained primary-token identity, native pipe/process/token
  session agreement, DACL revalidation, and token stability through one local
  challenge barrier without impersonation, collection, or admission.
- A test-only [Windows retained process-image binding
  probe](security/windows-cache-cleanup-retained-process-image-binding-probe.md)
  that binds the fixed expected executable to the retained participant process
  through private, bounded file-identity snapshots before and after one local
  challenge barrier without collection, cleanup, or admission.
- Versioned, sanitized render-device conformance evidence over explicitly
  supplied trusted factories, with no adapter discovery or certification.
- Versioned, sanitized 12-tool agent conformance evidence over explicitly
  supplied trusted factories, with no transport discovery or certification.
- Versioned, sanitized WorldStore conformance evidence over explicitly supplied
  trusted factories, with no implementation discovery, storage admission, or
  certification.
- Strict bounded receipt/1 decoding with detached immutable values, structured
  errors, configurable limits, and exact historical baseline fixtures.
- Exact built-in v1 operation argument contracts with fail-closed unknown
  fields and versioned breaking evolution under RFC-0005.
- Strict offline external-contributor rehearsal admission with a reviewed empty
  manifest, sanitized output, and no inferred usability or adoption claim.
- Strict offline external contributor-retention admission with a reviewed
  empty manifest, sanitized zero result, and no stars or telemetry input.
- Strict offline issue-response and pull-request-review latency admission with
  a reviewed empty manifest, pending-item preservation, and no inferred SLA.
- A pure-wheel community-alpha candidate with a deterministic sample bundle, checksums, SPDX SBOM, notices, explicit stability metadata, command/receipt readiness evidence, and cross-platform release smoke.

Start with the [community-alpha user guide](user-guide.md), then read the [architecture overview](architecture.md), [runtime contract](runtime-contract.md), [entity identity contract](ecs.md), [headless command workflow](cli-workflows.md), [command and receipt stability decision](command-receipt-stability-decision.md), [operation-argument compatibility guide](operation-argument-compatibility.md), [bounded receipt-reader guide](receipt-reader.md), [external-contributor rehearsal readiness guide](external-contributor-rehearsal-readiness.md), [external contributor-retention readiness guide](external-contributor-retention-readiness.md), [rendering contract](rendering.md), [render-device conformance guide](render-device-conformance.md), [agent-tool conformance guide](agent-tool-conformance.md), [WorldStore conformance guide](world-store-conformance.md), [rich 2D presentation guide](presentation.md), [plugin compatibility guide](plugins.md), [constrained 3D decision](constrained-3d-decision.md), [visual-editor admission decision](visual-editor-decision.md), [WASM-mod security decision](wasm-mod-security-decision.md), [asset-cache cleanup threat model](security/cache-cleanup-threat-model.md), [cache-cleanup platform-capability decision](security/cache-cleanup-platform-capability-decision.md), [Windows cache-cleanup capability probe](security/cache-cleanup-windows-capability-probe.md), [Windows directory-junction refusal probe](security/cache-cleanup-windows-junction-probe.md), [Windows retained-parent substitution probe](security/cache-cleanup-windows-retained-parent-substitution-probe.md), [Windows cross-process substitution probe](security/cache-cleanup-windows-cross-process-substitution-probe.md), [Windows share-delete exclusion probe](security/cache-cleanup-windows-share-delete-exclusion-probe.md), [Windows native sharing-violation probe](security/cache-cleanup-windows-native-sharing-violation-probe.md), [Windows child-owned share-delete handshake](security/cache-cleanup-windows-child-owned-share-delete-handshake.md), [gameplay guide](gameplay.md), [agent control interface](agent-control.md), [API status](api-status.md), and [accepted decisions](adr/index.md) before building on the experimental and preview APIs.

## Quick check

```console
uv sync --frozen --all-groups
uv run ludoweave doctor
uv run python examples/hello_headless.py --ticks 120
uv run python examples/clockwork_arena.py --ticks 600
uv run python examples/rich_2d_showcase.py --ticks 6
uv run python examples/constrained_3d_decision.py
uv run python examples/visual_editor_decision.py
uv run python examples/wasm_mod_security_decision.py
uv run python examples/render_device_conformance.py
uv run python examples/agent_tool_conformance.py
uv run python examples/world_store_conformance.py
uv run ludoweave plugin check examples/example.plugin.json
uv run python examples/alpha_acceptance.py
uv run python examples/command_receipt_stability_decision.py
uv run python examples/operation_argument_compatibility.py
uv run python examples/receipt_reader.py
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
uv run ludoweave mcp --sample agent-world-builder
```

None of these commands needs a display, GPU, native compiler, or network listener.

The optional GPU slice has a separate locked install and smoke:

```console
uv sync --frozen --all-groups --extra graphics
uv run --frozen --extra graphics python examples/hello_sprite.py
uv run --frozen --extra graphics python examples/agent_world_builder.py
uv run --frozen --extra graphics python examples/render_device_conformance.py --backend wgpu
```
