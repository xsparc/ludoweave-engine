# Project State

## Current milestone

M0 through M7 are complete, independently accepted, integrated into `main`,
and validated by hosted CI. M8 gamepad/SDL3 evaluation is complete,
independently accepted, published as PR #9 from
`codex/m8-gamepad-sdl3-evaluation`, and validated across all 14 hosted jobs.
M9 Box2D v3 plugin admission evaluation is locally complete on
`codex/m9-box2d-plugin-evaluation`, stacked from the exact M8 head. ADR-0024
defers the plugin; repeat independent review accepted the ownership correction
with no remaining blockers. It is published as ready stacked PR #10 and GitHub
Actions run `31015885190` passed all 14 hosted jobs.
M10's headless semantic inspector is complete, independently accepted, and
published as ready stacked PR #11 from `codex/m10-live-semantic-inspector`,
based on exact M9 final head
`22bc2de9f8450f60fe483bd4fea10a86702d2f0f`. ADR-0025 accepts one isolated,
owned local MCP child with detached observations and receipted writes. GitHub
Actions run `31020096463` passed all eight essential hosted jobs.
M11 is complete and independently accepted on
`codex/m11-rich-2d-modules`, based on exact M10
evidence head `bae799900671481cfd6f03fe502dea95b2c7f96c`. ADR-0026 bounds it
to dependency-free headless audio mixing, bitmap text, tick animation,
immutable tilemaps, and fixed-point particles through existing render records.
It is published as ready stacked PR #12; GitHub Actions run `31024155710`
passed all eight essential hosted jobs on signed implementation commit
`aca6d93165a52d88451e8e06d5f1aa8d2e323f1d`.
M12 is assigned on `codex/m12-plugin-manifest-compatibility`, based on exact
M11 evidence head `840a8b06d461fa1d5e649911b22f5995154728a7`. Its bounded contract is a
data-only preview plugin-manifest schema and deterministic compatibility
evaluator. RFC-0002 is accepted and implementation plus focused review
hardening are complete. Independent hostile review approved the corrected tree
with no remaining finding, and the complete local/artifact/provider gate
passed. It is published as ready stacked PR #13; GitHub Actions run
`31028863469` passed all eight essential hosted jobs on signed implementation
commit `e1f6e3cd8572d20a4f0a5c62a96b9aa52a986b38`.
M13 is complete and independently accepted on
`codex/m13-rollback-network-readiness`, based on exact
M12 hosted-evidence head
`7cb834c7b5e84e1b1a945905a68b947b3a4bdd3f`. Its bounded contract is an
offline Clockwork Arena correction-branch proof plus an evidence-based network
rollback admission decision. ADR-0027 defers networking/live rollback because
canonical tick input is not replay-owned and protocol, security, simulation,
resource, lifecycle, and maintenance gates remain incomplete. No runtime
package, persistent format, listener, transport, or dependency is added. The
final complete local/artifact/provider gate passes and independent review
reports no remaining finding. It is published as ready stacked PR #14; GitHub
Actions run `31031590206` passed all eight essential hosted jobs on signed
implementation commit `ba62b650191cfb982100692e7ec694da318956ae`.
M14 is complete and independently accepted on
`codex/m14-constrained-3d-decision`, based on exact M13
hosted-evidence head
`48f8f296113e3f2794bae7f4c67997d433e4dd36`. Its bounded contract is an
installed-surface audit and product-scope decision only. ADR-0028 retains
layered 2D and defers constrained 3D behind a complete product, engine-contract,
agent-semantic, headless-conformance, cross-platform, resource-budget,
lifecycle, and maintenance gate. Exact source, isolated-wheel, and release
bundle evidence confirms the current orthographic camera and canonical
layer/z ordering while every 3D admission gate remains false. The final local
gate reports 809 passes and one existing Windows symlink-capability skip;
independent hostile review reports no remaining finding. M14 changes no
runtime package, public Python API, persistent format, dependency, version, or
CI topology. GitHub Actions run `31033924254` passed all eight essential jobs
on signed implementation commit
`47443046834eb423be977973775f80494161533d`. M8-M14 were then
squash-integrated into `main` by PR #16 as verified commit
`2c62c8ed9c4ced6292260f6b8c84b1f069de1eaa`; its tree exactly matches final
M14 evidence head `02426805a11712030b3082ec349696d6d94aca50` at tree
`137a1870b0dd9034ad935b253a13186f6c7cc913`. Stacked PRs #9-#15 are closed as
superseded, with branches retained for audit history.

## Repository identity

M3 rendering is complete on `codex/m3-rendering-vertical-slice`, published as
stacked PR #3, and validated by corrected hosted run `30993554807` across the
14-job quality, CPython/OS, wheel, and graphics matrix. M4 is complete on
`codex/m4-clockwork-arena`, published as stacked PR #4, and validated by hosted
run `30996905660` across the same 14-job matrix.
M5 agent control is complete on `codex/m5-agent-control`, published as stacked
PR #5, and validated by hosted run `30999777517` across the same 14-job matrix.
M6 community-alpha hardening is complete on `codex/m6-release-hardening`,
published as stacked PR #6, and validated by hosted run `31002365370` across the
same 14-job matrix, including complete candidate smoke on all three platforms.
M7 performance/native decision is complete on
`codex/m7-performance-decision`, published as stacked PR #7, and validated by
hosted run `31005165849` across all 14 jobs, including the new base and
real-wgpu profiling-contract smokes.
The validated M1-M7 tree was squash-integrated to `main` by PR #8 as commit
`0237b2bfb11c6032d030dada639c7dbe439e5089`. The validated M8-M14 tree was
squash-integrated by PR #16 as commit
`2c62c8ed9c4ced6292260f6b8c84b1f069de1eaa`. The milestone branches and
hosted-run records remain the audit trail; superseded stacked PRs are closed.

- Canonical repository: `xsparc/ludoweave-engine`.
- Package and CLI: `ludoweave`.
- Alpha candidate version: `0.1.0a1`.
- License and contribution model: Apache-2.0 with DCO sign-off.
- Supported baseline: standard CPython 3.12-3.14 on Windows, macOS, and Linux; no mandatory native compiler.

## Implemented

- Public README, governance, contribution, conduct, security, changelog, NOTICE, issue/PR templates, and agent guidance.
- PEP 621 pure-Python package, uv lockfile, Ruff, strict Pyright, pytest, Hypothesis, MkDocs Material, and typed-package marker.
- Immutable engine configuration and run summary; monotonic and deterministic virtual clocks.
- Explicit single-owner engine lifecycle with initialization, fixed-tick run, shutdown, failure cleanup, idempotent close, and structured exceptions.
- Engine-owned render protocol, backend-neutral descriptor, and lifecycle-validating null renderer.
- `ludoweave --version`, structured `ludoweave doctor`, and deterministic headless example.
- Architecture overview, runtime contract, accepted ADR-0001 through ADR-0007, and AST import rules that test absolute, relative, near-prefix, and reference-model independence constraints.
- Least-privilege GitHub Actions matrices for the supported operating systems/Python versions and installed-wheel smoke tests.
- Immutable two-field entity IDs, deterministic generational allocation, structured stale-handle failures, and installed-wheel ECS smoke coverage.
- Explicit component UUIDs, frozen schemas, immutable UUID-sorted registries, scalar validation metadata, and complete adjacent forward migration chains.
- Storage-neutral `WorldStore`, canonical `World`, private pure-Python dense/sparse component tables, deterministic inspection, change epochs, and independent in-memory cloning.
- Deliberately simple dictionary `ReferenceWorld` with separately implemented allocation, value, epoch, patch, and clone logic, exercised as a Hypothesis state-machine oracle.
- Structured duplicate/missing/malformed-value failures, copy-in/copy-out ownership, generation-safe swap removal, and installed-wheel world lifecycle coverage.
- Storage-neutral typed query builders with include/exclude/changed filters, opt-in stable ordering, detached row values, explicit writable cursor ownership, row-atomic validated writeback, and private structurally invalidated plan caching.
- World-bound reusable `Commands` buffers with copy-on-enqueue values, identity-only deferred entity tokens, clone-staged atomic flush, deterministic direct-operation epochs, retry/clear failure behavior, and local non-receipt `FlushResult` values.
- Production/reference query and flush conformance, extended Hypothesis state-machine coverage, exact reference-import whitelisting, and installed-wheel query/command smoke coverage.
- Explicit identity-owned typed resource keys, immutable registries, copy-owned singleton stores with a trusted read-only-input adapter contract, exact generic return typing, and structured copy failures.
- Immutable module-level Python system declarations, fixed simulation phases, component/resource access metadata, deterministic-eligibility gates, same-phase conflict ambiguity rejection, canonical cycle diagnostics, and input-order-independent serial schedule planning.
- ADR-0006 documentation, generated DAG/property coverage, D0 component rejection in deterministic plans, and installed-wheel resource/scheduler smoke coverage.
- Exact integer-unit fixed-step accumulation, retained catch-up backlog, absolute virtual deadlines, immutable exact-value input snapshots, virtual/recorded input sources, and application-owned input publication.
- Declaration-enforcing invocation contexts, canonical schedule revalidation, serial PRE/SIMULATE/flush/POST execution, structured failure attribution, BaseException-safe cleanup, and an additive installed-wheel fixed-step example.
- Versioned M1 benchmark tooling for seven workloads with raw samples, nearest-rank p50/p95/p99, sanitized CPython/GIL/environment/commit metadata, exact artifact validation, and tamper regressions.
- Bounded canonical JSON with exact finite-float tags, duplicate/Unicode/size validation, immutable command/transaction envelopes, and an explicit versioned operation registry with a compatibility fingerprint.
- Single-owner authoritative world sessions, complete allocator/epoch logical images, explicit persistent resource schemas/codecs, SHA-256 state hashes, clone-staged entity/component/resource/tick transactions, optimistic pre-hash checks, dry-run, deterministic limits, and atomic pointer-swap adoption.
- Canonical committed/dry-run/rejected transaction receipts with sanitized diagnostics, command outcomes, exact alias resolutions, and independent semantic diffs covering net entity/component/resource changes plus allocator, epoch, and tick behavior.
- Canonical complete-authority snapshots with SHA-256 verification, bounded atomic restore, registered component/resource migrations, allocator/epoch preservation, and independently named deterministic PCG32 random streams.
- Self-contained canonical replay timelines with compatibility headers, exact transaction/tick/hash batches, verified checkpoints, one-tick branch boundaries, and immutable parent-referenced branches.
- Data-only project composition plus project-confined `apply`, `snapshot`, `replay`, and `diff` CLI workflows with project-bound snapshots, handle-bounded input, and atomic output replacement.
- Informational M2 benchmark/validator tooling for canonical transactions, atomic application, snapshot round trips, and replay verification.
- Frozen backend-neutral render descriptors, explicit target/camera command lists, scoped generational resource handles, deterministic presentation extraction, and graph dependency/lifetime validation.
- A validation-only `NullRenderDevice` with fence-deferred physical reuse and an optional exact wgpu/rendercanvas/GLFW adapter isolated from package roots and canonical world state.
- Instanced atlas sprites, translated/zoomed/rotated orthographic cameras, stable layer/z/entity ordering, tile batches, debug lines, built-in diagnostic glyphs, resize/minimize behavior, immutable offscreen RGBA capture, and typed device-loss diagnostics.
- M3 renderer benchmark/validator tooling for 1k/10k extraction, Null submission, and wgpu CPU submission with raw p50/p95/p99 evidence and exact draw counts.
- Frozen provider-neutral platform events, immutable action snapshots with transition metadata, deterministic recorded input, and isolated render-surface event draining.
- Strict project-root-confined asset manifests, transitive content-addressed cache keys, bounded pure-Python PNG decoding, and explicitly retired immutable texture revisions.
- Deterministic AABB/circle overlap, stable exact-filter spatial grids, bounded axis-ordered kinematic movement, and a minimal engine-owned null audio backend.
- Clockwork Arena canonical world/resource gameplay, fixed-seed waves, projectiles, collision, score/restart behavior, immutable presentation extraction, and deterministic headless/offscreen/window examples.
- Exact 3,600-tick Clockwork Arena fixture and independently recorded-input replay hash, plus M4 benchmark/validator tooling for baseline and informational stress workloads.
- Transport-independent typed agent command/query service with 12 immutable tool schemas over canonical transactions, receipts, snapshots, diffs, replay, capture, telemetry, and registered tests.
- Default read-only capabilities, explicit write/capture/test grants, bounded requests/results/work, monotonic rate limiting, caller binding, recursive credential redaction, and non-blocking single-thread mutation safe points.
- Project-confined `ludoweave agent` composition and local-only stdio MCP `2025-11-25` initialization, discovery, and tool calls without networking, shell access, arbitrary evaluation, dynamic project imports, or a new runtime dependency.
- Agent World Builder acceptance composition with six typed ECS entities, real offscreen wgpu capture, exact query/adjust/diff/test/telemetry/replay coverage, and installed-wheel execution.
- Deterministic community-alpha release staging with a pure wheel, sdist, fixed-timestamp sample bundle, SHA-256 inventory, versioned manifest, SPDX 2.3 SBOM, and notice set.
- Isolated release smoke that validates exact checksum coverage, SBOM/wheel identity, safe ZIP members, installed CLI/doctor, and bundled headless M0-M5 scenarios before success.
- Explicit `__all__`/`__stability__` policy and architecture coverage for every
  supported Python export. Earlier `0.1.0a1` symbols remain experimental;
  `ludoweave.plugins` is the first preview surface with a documented
  deprecation promise.
- Pinned tag-only provenance/prerelease workflow plus one complete baseline
  release-candidate smoke, compatibility coverage for every supported Python
  version/OS, and real graphics smoke on all three operating systems.
- Community-alpha user, architecture, adapter, release, first-contribution, API, triage, release-note, roadmap, and retrospective material with declarative labels and issue-ready starter cards.
- Versioned M7 base/graphics `cProfile` tooling with exact workload invariants,
  sanitized module/function records, strict validation, and tamper regressions.
- Query metadata/signature traversal reductions mirrored independently in the
  production and reference worlds, validated presentation reconstruction, and
  fixed-record provider-neutral sprite packing.
- Accepted RFC-0001 and ADR-0022: no native kernel is admitted; measurable
  cross-platform, contiguous-buffer, GIL, owner, build, fuzz, fallback, and
  improvement gates govern any future proposal.
- Frozen standardized gamepad connection/button/axis records, bounded logical
  slots, normalized stick/trigger domains, and an engine-owned provider
  protocol implemented by Null and the optional render device.
- Gamepad action bindings with explicit analog scale/deadzone semantics,
  supported-control focus recovery, hotplug cleanup, stable GLFW polling, and
  installed-wheel/Clockwork Arena coverage without provider-object leakage.
- Accepted ADR-0023: the existing pinned GLFW adapter supplies M8 input while
  SDL3 is deferred until its Python binding, binary delivery, ownership,
  cross-platform conformance, and maintenance gates are satisfied.
- A bounded isolated Box2D-candidate probe with versioned sanitized JSON,
  exact single-thread fixed-step traces, repeated lifecycle churn, double
  destruction, strict workload bounds, and no LudoWeave/runtime import.
- Accepted ADR-0024: `box2d-python==0.1.2` is deferred after failing the complete
  CPython/platform wheel and stable-API gates and lacking sufficient
  ownership, GIL/thread, replay, adapter-conformance, and maintenance evidence.
- Architecture fixtures reject case-insensitive Box2D/native-binding imports
  from engine source; the base project metadata, uv lock, wheel, and runtime
  remain unchanged and pure Python.
- `ludoweave inspect` owns one isolated `python -I -m ludoweave mcp` child,
  defaults to read-only, emits bounded `ludoweave.inspector.event/1` semantic
  observations, and verifies MCP identity, typed tools, receipts, completed
  ticks, and exact snapshot/diff/world/query/telemetry hash continuity.
- Inspector sample bootstrap and ticks require explicit write capability and
  reuse existing versioned transaction/tick tools. Child commands, module
  shadowing, option injection, network listeners, remote attach, parallel
  authority, paths, environment values, process IDs, and provider objects are
  excluded and covered by adversarial tests.
- Pull-request CI is consolidated from 14 to eight essential jobs: one complete
  Ubuntu 3.12 quality/test/distribution gate, four compatibility jobs spanning
  CPython 3.13/3.14 and Windows/macOS, and three real cross-platform graphics
  jobs. Superseded runs remain cancelled.
- `ludoweave.presentation` frozen animation, bitmap-glyph, tilemap, and
  fixed-point particle records with exact-tick sampling, integer layout/culling,
  stable seeded stepping/digests, and existing render extraction.
- A bounded acyclic audio mix graph rooted at `master`, enforced by the
  lifecycle-validating Null backend with category and effective-gain checks.
- A dependency-free rich 2D showcase registered in source, isolated-wheel, and
  deterministic release sample-bundle validation paths.
- Accepted RFC-0002 plus strict canonical plugin manifests, frozen explicit
  compatibility contexts/reports, bounded dependency checks, a path-free local
  CLI check, and source/wheel/release example coverage. The package owns no
  discovery, import, execution, filesystem, networking, or mutable registry.
- Bounded M13 parent/correction replay evidence with exact parent lineage,
  repeatable divergent resimulation, explicit external input rehydration, a
  strict sanitized validator, and source/wheel/release-bundle composition.
- Accepted ADR-0027 deferring network rollback and remote authority until the
  complete canonical-input, protocol, security, cross-platform simulation,
  resource-budget, lifecycle, artifact, and maintenance gate is met.

## Next slice

- M13 publication and hosted evidence are complete. Before implementation,
  turn the next authoritative post-alpha item into a bounded task contract
  based on the current design and accepted decisions. Do not infer 3D runtime,
  sockets, remote authority, a live rollback API, editor/GUI, WASM, provider
  adapters, native code, or a persistent format change from roadmap proximity.

## Validation state

- The final reviewed M13 local gate on Windows/uv-managed CPython 3.12.13
  reports 793 passing tests and one existing symlink-capability skip, 174
  formatted Python files, zero Ruff/Pyright findings, strict documentation, a
  pure 91-entry wheel with zero native files and no mandatory dependency,
  isolated-wheel smoke, and fresh complete ten-artifact release smoke.
- Nine real-wgpu integration tests, the versioned 120/60 correction proof,
  strict evidence validation, Clockwork Arena, Agent World Builder, alpha
  acceptance, rich-2D showcase, and plugin compatibility passed. Every
  inherited README benchmark/profile artifact validated; the existing M1 and
  M3 target misses remain recorded and do not authorize acceleration.
- Independent hostile review drove pre/post-open file bounds, canonical JSON,
  exact types/counts/checkpoints, direct-call work limits, closed import/member
  allowlists, and alias/tamper regressions. Final review ran 54 focused tests,
  the maximum 600/300 proof, strict docs/static/diff/secret checks, and reported
  no blocking or non-blocking finding.
- GitHub Actions run `31031590206` passed the unchanged essential eight-job
  topology on M13 implementation commit
  `ba62b650191cfb982100692e7ec694da318956ae`: the complete Ubuntu 3.12
  quality/test/distribution job, Ubuntu 3.13/3.14 plus Windows/macOS 3.14
  compatibility jobs, and real graphics jobs on Ubuntu, Windows, and macOS.
- The final reviewed M12 local gate on Windows/uv-managed CPython 3.12.13
  reports 741 passing tests and one existing symlink-capability skip, 170
  formatted Python files, zero Ruff/Pyright findings, strict documentation, a
  pure 91-entry wheel with four plugin-contract entries and zero native files,
  isolated-wheel smoke, and fresh complete ten-artifact release smoke.
- Nine real-wgpu integration tests, Null/wgpu Clockwork Arena, Agent World
  Builder, alpha acceptance, rich-2D showcase, and the canonical example plugin
  check passed. Every inherited README benchmark/profile artifact validated;
  the existing M1 simulation and M3 renderer target misses remain recorded and
  do not authorize native work.
- Independent hostile review drove boundedness, exact-type, canonical-report,
  sanitized-diagnostic, immutable-decision, import/global-state, I/O/eval, and
  CLI regressions. Final re-review ran 138 focused tests with clean static,
  docs, diff, and isolated CLI checks and reported no remaining finding.
- GitHub Actions run `31028863469` passed the unchanged essential eight-job
  topology on M12 implementation commit
  `e1f6e3cd8572d20a4f0a5c62a96b9aa52a986b38`: the complete Ubuntu 3.12
  quality/test/distribution job, Ubuntu 3.13/3.14 plus Windows/macOS 3.14
  compatibility jobs, and real graphics jobs on Ubuntu, Windows, and macOS.
- The final reviewed M11 local gate on Windows/uv-managed CPython 3.12.13
  reports 663 passing tests and one existing symlink-capability skip, 164
  formatted Python files, zero Ruff/Pyright findings, strict documentation,
  a pure 87-entry wheel with seven presentation entries and zero native files,
  isolated-wheel smoke, and complete ten-artifact release smoke.
- Nine real-wgpu integration tests, base/graphics one-repeat profiling-contract
  smokes, Clockwork Arena, Agent World Builder, alpha acceptance, and the
  repeatable rich-2D showcase passed. M11 defines no timing target and makes no
  performance claim.
- Independent review found exclusive tile-bound, pre-bound traversal, runtime
  parent-fader, bounded-sequence, particle-work/state, and generic-style issues
  during development. The corrected edge/work/iterator/gain regressions passed;
  final re-review ran 78 focused tests plus 58 architecture/API tests with clean
  Ruff/Pyright/provider/diff/credential checks and reported no remaining
  finding.
- GitHub Actions run `31024155710` passed the unchanged essential eight-job
  topology on M11 implementation commit
  `aca6d93165a52d88451e8e06d5f1aa8d2e323f1d`: the complete Ubuntu 3.12
  quality/test/distribution job, Ubuntu 3.13/3.14 plus Windows/macOS 3.14
  compatibility jobs, and real graphics jobs on Ubuntu, Windows, and macOS.
- The final reviewed M10 local gate on Windows/uv-managed CPython 3.12.13
  reports 642 passing tests and one existing symlink-capability skip, 154
  formatted Python files, zero Ruff/Pyright findings, strict documentation
  success, a pure 80-entry wheel with no native entries or mandatory runtime
  dependency, installed-wheel shadow-isolation smoke, and complete 10-artifact
  release smoke.
- Eight real wgpu/GLFW integration tests, base/graphics one-repeat profiling
  contract smokes, Clockwork Arena, Agent World Builder, and alpha acceptance
  passed. M10 defines no performance target and makes no timing claim.
- Independent review first blocked publication on child import shadowing,
  dash-prefixed project option injection, incomplete tick receipt validation,
  and unstructured stream failures. `-I`, option termination/binding, exact
  receipt/hash/tick validation, structured read errors, and adversarial source
  and installed-wheel regressions resolved all findings. Repeat review ran 81
  focused tests with clean Ruff/Pyright/diff checks and approved publication.
- The consolidated eight-job CI workflow parses and its architecture contract
  passes locally. Its exact baseline test command excludes the separately
  gated wgpu integration file and passed 634 tests with one skip; real provider
  execution remains confined to the three jobs that install platform runtime
  prerequisites. GitHub Actions run `31020096463` passed that exact topology on
  implementation commit `2e60b3f1c4884dba71df5f23b779bc49187d68c6`.
- The corrected M9 local gate on Windows/uv-managed CPython 3.12.13 reports 606 passing
  tests and one existing symlink-capability skip, 151 formatted Python files,
  zero Ruff/Pyright findings, strict documentation success, a 79-entry pure
  wheel with zero native entries, installed-wheel and complete 10-artifact
  release smoke, eight real wgpu integration passes, and successful Clockwork
  Arena, Agent World Builder, and alpha-acceptance executions.
- Isolated `box2d-python==0.1.2` probes on Windows CPython 3.12.13 and 3.13.13
  each created/stepped/destroyed 25 worlds, repeated their exact traces, and
  produced trace digest
  `c9e299e715c5f7a3654d7c5794d75347d765cc029b7991d4c8066dfaf7abdfc5`.
  CPython 3.14 resolution failed because the release has only `cp312` and
  `cp313` wheels. These are candidate-admission facts, not performance,
  cross-platform determinism, or runtime-support claims.
- Independent review initially blocked sign-off because the metadata version
  was not linked to the imported module. The corrected probe validates the
  resolved module against the distribution's installed-file inventory before
  import and again afterward. Repeat review ran 54 focused tests, Ruff,
  Pyright, diff checks, and a real CPython 3.12 probe, found no remaining
  blocker, and recommended final sign-off.
- GitHub Actions run `31015885190` passed all 14 M9 jobs for implementation
  commit `8b429aaf07684651f6d538419701c049ee55fc4f`: strict quality/docs; Ubuntu
  CPython 3.12/3.13/3.14; Windows and macOS CPython 3.12/3.14; complete
  installed release-candidate smoke on Ubuntu/Windows/macOS; and real graphics
  smoke on all three systems. PR #10 is open, ready, mergeable, and clean
  against the exact validated M8 head.
- A pre-review M8 gate completed on Windows with uv-managed CPython 3.12.13,
  but an independent review then found production focus propagation, GLFW
  error-disambiguation, and trigger-neutrality defects. Its 589-pass result is
  retained as historical evidence, not accepted as the final M8 gate.
- The corrected final M8 gate reports 594 passing tests and one existing
  Windows symlink-capability skip, 149 formatted Python files, zero
  Ruff/Pyright findings, strict documentation success, a 79-entry pure wheel
  with zero native entries, installed-wheel and complete release-candidate
  smoke, eight real wgpu/GLFW integration passes, and successful Clockwork
  Arena, Agent World Builder, and alpha-acceptance executions. Repeat
  independent review found no blocking findings and recommended PR
  publication. M8 adds no dependency or benchmark; no timing result is
  claimed.
- GitHub Actions run `31012696753` passed all 14 M8 jobs: strict quality/docs;
  Ubuntu CPython 3.12/3.13/3.14; Windows and macOS CPython 3.12/3.14;
  installed-wheel smoke on Ubuntu, Windows, and macOS; and real graphics/GLFW
  gamepad smoke on all three operating systems.
- The complete M1 final local suite reports 303 passing tests, zero Ruff/Pyright findings, a strict documentation build, successful sdist/wheel build, and successful isolated installed-wheel smoke covering both M0 and M1 examples.
- The final 30-sample Windows/CPython 3.12.13 GIL-build benchmark artifact validates all seven versioned workloads. The 3,600-tick headless p95 was 26.8523 ms and observed the local 5×-real-time target. The representative 10,000-entity simulation-tick p95 was 196.8800 ms and did not observe the 4 ms engineering target. These are local observations, not cross-platform claims.
- GitHub Actions run `30936533105` passed quality/documentation, Ubuntu Python 3.12/3.13/3.14, Windows Python 3.12/3.14, macOS Python 3.12/3.14, and installed-wheel smoke on all three operating systems after correcting the invalid planned `actions/checkout` v6.0.2 SHA.
- MkDocs Material emits its upstream informational warning about the future MkDocs 2.0 project; the strict documentation build exits successfully.
- The final M2 local gate on Windows/uv-managed CPython 3.12.13 reports 444 passing tests and one Windows symlink-capability skip, zero Ruff/Pyright findings, strict documentation success, successful sdist/wheel build, and successful isolated installed-wheel workflow smoke.
- The final 30-sample M2 informational benchmark validated four workloads with no timing targets. Local p50/p95 durations were 30.2751/33.7076 ms for canonical 100-command round trips, 13.9896/16.9751 ms for atomic 100-command apply, 17.1209/18.0412 ms for 1,000-entity snapshot round trips, and 216.5521/271.2240 ms for verified 100-batch replay.
- Independent final M2 code/security and quality reviews found no remaining actionable findings and independently reproduced the 444-pass/one-skip suite.
- GitHub Actions run `30947073913` passed all 11 M2 jobs: quality/documentation; Ubuntu tests on Python 3.12/3.13/3.14; Windows and macOS tests on Python 3.12/3.14; and isolated installed-wheel smoke on Ubuntu, Windows, and macOS.
- The final local M3 graphics gate on Windows/uv-managed CPython 3.12.13 reports 485 passing tests and one Windows symlink-capability skip, zero Ruff/Pyright findings, strict documentation success, a pure wheel, and a successful no-dependency installed-wheel smoke. A separate frozen base sync removed all graphics packages and reported 479 passes with the symlink and graphics capability skips.
- The real Windows GLFW example and the offscreen clear/sprite/capture fixtures completed. The 30-sample M3 artifact validated six workloads with one draw each. Local 10k extraction/packing p50/p95/p99 was 35.4460/41.9722/51.8362 ms; wgpu CPU submission was 5.3753/6.5363/6.9215 ms. Neither observed the 3 ms starting target; no target pass is claimed.
- Initial M3 hosted run `30951328011` passed all base test and wheel jobs plus Windows/macOS graphics, but failed the quality type check because optional providers were not installed and failed Ubuntu graphics because no driver was present. The correction installs the exact graphics extra for quality and Mesa Vulkan only for the Ubuntu graphics job.
- Corrected GitHub Actions run `30993554807` passed all 14 jobs: strict quality/documentation; Ubuntu Python 3.12/3.13/3.14; Windows and macOS Python 3.12/3.14; isolated wheel smoke on all three operating systems; and real clear/sprite/capture/resize/loss graphics smoke on Ubuntu software Vulkan, Windows, and macOS.
- The final local M4 gate on Windows/uv-managed CPython 3.12.13 reports 516 passing tests and one existing Windows symlink-capability skip, zero Ruff/Pyright findings, strict documentation success, a pure wheel, successful no-dependency installed-wheel smoke, real offscreen and GLFW Clockwork Arena runs, exact 3,600-tick deterministic fixture/replay agreement, and a valid 300-sample three-workload benchmark artifact.
- The local baseline Clockwork Arena benchmark p50/p95/p99 was 1.5228/2.1228/2.5898 ms and observed its 16.666667 ms p95 target. Stress 4 and 8 p95 values were 3.5029 ms and 4.8371 ms and have no assigned target. These are local observations, not cross-platform claims.
- GitHub Actions run `30996905660` passed all 14 M4 jobs: strict quality/documentation; Ubuntu Python 3.12/3.13/3.14; Windows and macOS Python 3.12/3.14; isolated wheel smoke on all three operating systems; and real graphics smoke, including Clockwork Arena wgpu execution, on Ubuntu software Vulkan, Windows, and macOS.
- The final local M5 gate on Windows/uv-managed CPython 3.12.13 reports 545 passing tests and one existing Windows symlink-capability skip, zero Ruff/Pyright findings, strict documentation success, a pure wheel, successful no-dependency installed-wheel smoke, and a real offscreen wgpu Agent World Builder run.
- Direct Python, the actual `ludoweave agent` subprocess, and MCP return equivalent canonical transaction results/receipts. MCP lifecycle, malformed input, duplicate IDs/keys, capability denial, limits, atomic stale-hash rejection, reentrant/wrong-thread mutation rejection, redaction, provider close, and architecture bans are covered.
- GitHub Actions run `30999777517` passed all 14 M5 jobs: strict quality/documentation; Ubuntu Python 3.12/3.13/3.14; Windows and macOS Python 3.12/3.14; isolated wheel smoke on all three operating systems; and real graphics smoke, including the Agent World Builder typed-tool loop, on Ubuntu software Vulkan, Windows, and macOS.
- The final local M6 gate on Windows/uv-managed CPython 3.12.13 reports 552 passing tests and one existing Windows symlink-capability skip, 143 formatted Python files, zero Ruff/Pyright findings, strict documentation success, a pure `0.1.0a1` wheel, successful no-dependency installed-wheel smoke, and a complete 10-file staged candidate whose checksum/manifest/SBOM/sample smoke passed.
- M6 changes release/community surfaces rather than simulation performance. No new benchmark or performance pass is claimed; inherited M1/M3 misses and M4 observation remain unchanged.
- GitHub Actions run `31002365370` passed all 14 M6 jobs: strict quality/documentation; Ubuntu Python 3.12/3.13/3.14; Windows and macOS Python 3.12/3.14; complete installed release-candidate smoke on all three operating systems; and real graphics smoke, including Clockwork Arena and Agent World Builder, on Ubuntu software Vulkan, Windows, and macOS.
- The final local M7 gate on Windows/uv-managed CPython 3.12.13 reports 564
  passing tests and one existing Windows symlink-capability skip, 148 formatted
  Python files, zero Ruff/Pyright findings, strict documentation success, a
  pure wheel/sdist, successful no-dependency wheel smoke, complete 10-file
  release smoke, six real wgpu integration passes, and successful wgpu sample
  compositions.
- Final valid 30-sample M7 observations are 130.1806/144.0474/150.6699 ms
  p50/p95/p99 for the 10,000-entity simulation tick, 20.8641/30.6902/31.4777 ms
  for 10,000-sprite extraction/packing, and 2.8678/5.1918/5.2584 ms for wgpu
  CPU submission. None observed its starting target; these are local, not
  cross-platform, timing claims.
- Five-repeat `ludoweave.profile.m7/1` base and graphics artifacts validate.
  Remaining simulation cost spans detached query copy/writeback; presentation
  cost spans immutable record construction; packing consumes Python objects
  even where it dominates submission. RFC-0001 therefore defers native code.
- GitHub Actions run `31005165849` passed all 14 M7 jobs: strict
  quality/documentation plus base profile validation; Ubuntu Python
  3.12/3.13/3.14; Windows and macOS Python 3.12/3.14; complete installed
  release-candidate smoke on Ubuntu/Windows/macOS; and real graphics plus wgpu
  profile smoke on all three operating systems. PR #7 is open, mergeable, and
  reports clean merge state against the validated M6 branch.

## External follow-ups

- Verify and reserve the `ludoweave` name before publishing to PyPI.
- Apply `.github/labels.yml` through GitHub settings and open the issue-ready
  starter cards when maintainers are ready to review community contributions.

## Deferred roadmap

Remote/network agent transport, real audio playback, Box2D/rigid-body physics,
networking, editor tooling, automatic device recovery, international text shaping, 3D, and
native acceleration remain unimplemented. RFC-0001 records that the improved
M1/M3 workloads still miss their targets and defines the complete quantified
admission gate before a native proposal may return.
