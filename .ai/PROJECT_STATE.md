# Project State

## Current milestone

M0 through M6 are complete, independently accepted, published as stacked pull
requests, and validated by hosted CI.

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
- Explicit `__all__`/`__stability__` policy and architecture coverage for every supported Python export; all `0.1.0a1` symbols remain experimental.
- Pinned tag-only provenance/prerelease workflow plus complete release-candidate smoke in all three regular cross-platform wheel jobs.
- Community-alpha user, architecture, adapter, release, first-contribution, API, triage, release-note, roadmap, and retrospective material with declarative labels and issue-ready starter cards.

## Next slice

- Stop at the authorized M6 boundary. Do not create a release tag, GitHub
  release, PyPI publication, or begin another milestone without a separate
  maintainer decision.

## Validation state

- Local validation completed on Windows with uv-managed CPython 3.12.13.
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

## External follow-ups

- Verify and reserve the `ludoweave` name before publishing to PyPI.
- Apply `.github/labels.yml` through GitHub settings and open the issue-ready
  starter cards when maintainers are ready to review community contributions.

## Deferred roadmap

Remote/network agent transport, real audio playback, Box2D/rigid-body physics,
networking, editor tooling, automatic device recovery, rich text, 3D, and
native acceleration remain unimplemented. The measured M1 and M3 target misses
are profiling evidence only and do not satisfy the later native-code admission
gate.
