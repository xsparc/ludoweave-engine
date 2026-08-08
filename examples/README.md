# LudoWeave community-alpha samples

These samples run against an installed `ludoweave` wheel. Start with the
dependency-free headless paths:

```console
python hello_headless.py --ticks 120
python fixed_step_world.py --ticks 6
python clockwork_arena.py --ticks 600
python rich_2d_showcase.py --ticks 6
python rollback_readiness.py --ticks 120 --branch-tick 60
python command_receipt_stability_decision.py
python operation_argument_compatibility.py
python receipt_reader.py
python receipt_semantic_compatibility.py
python cross_version_corpus_readiness.py
python external_consumer_feedback_readiness.py
python supported_release_channel_readiness.py
python external_contributor_rehearsal_readiness.py
python external_contributor_retention_readiness.py
python external_sample_game_adoption_readiness.py
python constrained_3d_decision.py
python visual_editor_decision.py
python wasm_mod_security_decision.py
python render_device_conformance.py
python world_store_conformance.py
python world_store_conformance.py --backend reference
python agent_tool_conformance.py
python alpha_acceptance.py
ludoweave plugin check example.plugin.json
```

`rich_2d_showcase.py` exercises animation, bitmap text, chunked tilemaps,
fixed-point particles, Null-audio mixing, and Null rendering without a display
or audio device. `alpha_acceptance.py` checks engine lifecycle, stale entity generations,
Clockwork Arena, typed agent operations, replay evidence, provider ownership,
and registered Agent World Builder tests without a display, network listener,
or native compiler.

`example.plugin.json` is inert compatibility metadata for the preview M12
manifest protocol. The checker validates it against the current engine,
CPython, and desktop platform without importing or executing plugin code.

`rollback_readiness.py` proves bounded offline replay branching with corrected
future input, records the still-external input-history dependency, and emits a
deferred networking decision. It opens no listener and implements no transport
or live rollback service.

`command_receipt_stability_decision.py` exercises the installed canonical
command, transaction, receipt, and 12-tool agent foundations, then records why
the central protocols remain experimental. It changes no runtime or format and
does not claim cross-version compatibility or external adoption.

`operation_argument_compatibility.py` exercises all seven built-in v1
operation argument contracts, including exact missing-field and unknown-field
rejection. Its same-version report validates the explicit evolution policy; it
does not prove cross-version compatibility or promote the command protocol.

`receipt_reader.py` decodes generated committed, dry-run, and rejected
`ludoweave.receipt/1` documents through the bounded public reader and exercises
its malformed, incompatible, and oversized failures. Its sanitized report is
same-version evidence, not a compatibility or certification claim.

`receipt_semantic_compatibility.py` exercises every semantic-diff record family,
all current top-level transaction rejection codes, strict field rejection, and
the unknown-code fallback. Its same-version report proves RFC-0006's policy;
it does not prove cross-version history or promote receipt stability.

`cross_version_corpus_readiness.py` verifies the exact preserved receipt
manifests and canonical decoding through the installed reader, then reports
that the current single-version/no-release-evidence corpus is not ready. Its
synthetic gate regression is not cross-version history or release evidence.

`external_consumer_feedback_readiness.py` validates the exact empty reviewed
feedback manifest and reports that no independently owned integration evidence
exists. Its synthetic gate regression is not a consumer, adoption, feedback,
release, or stability-promotion claim.

`supported_release_channel_readiness.py` validates the exact empty reviewed
release-channel manifest and reports that no recurring supported final-feature
release history exists. Its synthetic gate regression is not a release,
support promise, channel, publication, or stability-promotion claim.

`external_contributor_rehearsal_readiness.py` validates the exact empty
reviewed rehearsal manifest and reports that the public first-contribution path
has not yet been independently completed without private maintainer knowledge.
Its synthetic gate regressions are not contributors, pull requests, feedback,
usability evidence, or project history.

`external_sample_game_adoption_readiness.py` validates the exact empty reviewed
sample-game manifest and reports that no independently authored public game is
currently admitted. Its synthetic gate regressions and the bundled project
examples are not external authors, games, users, or adoption evidence.

`external_contributor_retention_readiness.py` validates the exact empty
reviewed retention manifest and reports that no independent external human has
yet returned for a later merged project contribution. Its synthetic gate
regressions are not people, contributions, retention, popularity, or project
history.

`installation_matrix_readiness.py` validates the exact empty reviewed
installation manifest and reports that no immutable public release wheel has a
complete reviewed clean-install result across the supported OS/CPython matrix.
Its synthetic gate regressions and source-checkout CI are not released-user
installations, publication, or support evidence.

`response_review_latency_readiness.py` validates the exact empty reviewed
measurement manifest and reports that no complete public issue/PR cohort has
an admitted human-maintainer response/review latency result. Future windows
must preserve pending items; synthetic fixtures and automation are not people,
support work, latency measurements, or SLA evidence.

`replay_divergence_rate_readiness.py` validates the exact empty reviewed CI
execution manifest and reports that no complete replay cohort has an admitted
divergence rate. Future windows must retain cancelled, pre-replay-failed,
skipped, and unavailable-result executions; passing jobs and synthetic fixtures
are not historical rate evidence or a reliability target.

`benchmark_regression_rate_readiness.py` validates the exact empty reviewed
controlled-comparison manifest and reports that no complete paired benchmark
cohort has an admitted regression rate. Future windows must use registered
M1-M4 p95 workloads, bind comparable runner/source artifacts, predeclare exact
integer tolerances, and retain non-execution. Local timings, cProfile output,
passing jobs, and synthetic fixtures are not historical rate evidence.

`agent_tool_recovery_rate_readiness.py` validates the exact empty reviewed
task-directed call manifest and reports that no complete agent-tool cohort has
an admitted completion-without-manual-recovery rate. Future windows must retain
known failures, calls completed after human recovery, and unobserved terminal
states. Conformance runs, tests, maintainer-invoked calls, and synthetic
fixtures are not operational recovery-rate evidence.

`constrained_3d_decision.py` audits the installed public render and built-in
world-operation surfaces. It emits a deterministic deferred decision and adds
no 3D API, provider, asset loader, or runtime implementation.

`visual_editor_decision.py` audits the installed command, receipt, agent-tool,
MCP, and inspector foundation. It records a deterministic deferred admission
decision and adds no GUI, editor runtime, public API, dependency, or project
format.

`wasm_mod_security_decision.py` audits the installed data-only plugin boundary,
proves that executable manifest fields remain rejected, and records a deferred
WASM-mod decision. It does not compile, instantiate, or execute guest code.

`render_device_conformance.py` runs the versioned baseline profile against an
explicitly selected trusted adapter. The dependency-free default validates the
Null device; `--backend wgpu` validates the optional production adapter. It
does not discover, import by name, install, sandbox, or certify third-party
code.

`world_store_conformance.py` runs the versioned storage-neutral baseline against
an explicit built-in `World` or `ReferenceWorld` factory. It validates entity
generations, epochs, copy isolation, queries, atomic command buffers, cloning,
and structured failures without discovery, persistence, provider imports, or an
external-resource lifecycle.

`agent_tool_conformance.py` runs the versioned 12-tool baseline against an
explicit built-in direct-service factory and a fresh clean authority. It does
not accept a module name, discover a transport, install code, start a process,
open a network connection, sandbox, or certify third-party code.

`third_party_conformance_adoption_readiness.py` validates the exact empty
reviewed project-accepted submission manifest and reports zero passing
independently authored implementations. It does not discover packages, import
providers, install wheels, execute factories, or count the bundled conformance
examples as adoption.

For optional WebGPU presentation, install the exact release's `graphics` extra
and run:

```console
python hello_sprite.py
python agent_world_builder.py
python clockwork_arena.py --ticks 600 --renderer wgpu
```

Add `--window --interactive` to the final command for the desktop Clockwork
Arena controls. The bundle is example source, not a plugin/project loader; read
the version-matched user, plugin, and adapter guides before reusing experimental
or preview APIs.
