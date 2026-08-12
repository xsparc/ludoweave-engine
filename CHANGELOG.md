# Changelog

All notable changes to LudoWeave Engine will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project intends to use [Semantic Versioning](https://semver.org/spec/v2.0.0.html) once release compatibility levels are defined.

## Unreleased

- Add M71/RFC-0054 bounded checksum-admitted sample snapshots. Complete
  release smoke copies at most 16 MiB into an owned spooled temporary file
  while hashing, then parses those exact admitted bytes without changing
  workflows, dependencies, the sample producer, runtime APIs, or release
  authority.
- Add M70/RFC-0053 same-opened-handle sample-archive checksum validation
  before ZIP parsing and again before staged-root publication, binding the
  consumer to the sample digest already admitted from `SHA256SUMS` without
  changing workflows, dependencies, the sample producer, runtime APIs, or
  release authority.
- Add M69/RFC-0052 preflight rejection for traditional encryption, strong
  encryption, and masked header values in sample ZIP members before reads or
  staging, without adding password handling or changing workflows,
  dependencies, the sample producer, runtime APIs, or release authority.
- Add M68/RFC-0051 regular-file and 16 MiB sample-archive container
  admission before ZIP parsing, using the same opened handle for descriptor
  validation and archive reads without changing workflows, dependencies, the
  sample producer, runtime APIs, or release authority.
- Add M67/RFC-0050 exact sample-bundle inventory preflight. The verifier now
  rejects any unexpected member or missing member among the 50 source-defined
  regular files before extraction, using one content-silent failure category,
  without changing workflows, dependencies, the sample producer, runtime APIs,
  or release authority.
- Add M66/RFC-0049 same-filesystem temporary staging and single-rename sample
  publication. An incomplete or otherwise failed extraction cleans its partial
  owned staging tree, existing final roots fail before archive reads, and no
  workflow, dependency, sample producer, runtime API, or release authority
  changes.
- Add M65/RFC-0048 portable sample member path preflight, rejecting non-ASCII,
  Windows-device, trailing-period, duplicate/case-ambiguous, explicit-directory,
  explicitly non-regular, over-255-character, and file/directory prefix
  collision members before extraction, without changing workflows,
  dependencies, the sample producer, runtime APIs, or release authority.
- Add M64/RFC-0047 complete preflight and 64 KiB streaming extraction for
  staged sample bundles, limiting them to 256 members, 1 MiB per member, and
  8 MiB total declared expansion while admitting only bounded-read stored and
  deflated codecs, without changing workflows, dependencies, runtime APIs, or
  release authority.
- Add M63/RFC-0046 public-release subordinate-output confinement and exact
  built-in integer exit-status validation, preserving one content-silent JSON
  document without changing workflows, dependencies, runtime APIs, or release
  authority.
- Add M62/RFC-0045 deterministic portable asset name validation for public-
  release plans, rejecting Windows device stems, trailing periods, over-255-
  character names, and case-insensitive collisions before asset download,
  without changing workflows, dependencies, runtime APIs, or release authority.
- Add M61/RFC-0044 alias- and filesystem-identity-aware separation between the
  read-only public-release candidate directory and runner-owned output root
  before network or validator work, without changing workflows, dependencies,
  runtime APIs, version, or release authority.
- Add M60/RFC-0043 fail-before-side-effect public-release filesystem collision
  handling for files, directories, live links, and dangling links while
  retaining exclusive creation, no clobber behavior, workflows, dependencies,
  runtime APIs, version, and release authority.
- Add M59/RFC-0042 tool-neutral current-tree repository metadata, centralized
  absence enforcement, neutral fixtures, and descriptive historical-record
  redaction without rewriting Git history or changing runtime, workflows,
  dependencies, version, or release authority.
- Add M58/RFC-0041 ordered public-release response close and connection close
  attempts that preserve the primary failure and complete before redirect
  continuation or separate partial publication, with no rollback, workflow,
  dependency, runtime API, or release-authority change.
- Add M57/RFC-0040 immutable bytes-block and declared-versus-streamed
  `Content-Length` validation for every successful response body, without an
  alternate client, workflow, dependency, runtime API, or release-authority
  change.
- Add M56/RFC-0039 strict integer response-status and single bounded Location
  URI-reference validation before public-release redirect resolution, without
  adding a host allowlist, workflow, dependency, runtime API, or release
  authority.
- Add M55/RFC-0038 documented HTTP/1.1-class response-value and framing
  validation on every public-release response, rejecting unsupported transfer
  codings and `Transfer-Encoding`/`Content-Length` ambiguity before status or
  body use while explicitly not claiming exact raw status-line token evidence.
- Add M54/RFC-0037 exact post-handshake public-release TLS session-freshness
  evidence through `session_reused is False` on every hop before later TLS
  observations or HTTP, without changing workflows, dependencies, runtime
  APIs, or release authority.
- Add M53/RFC-0036 exact post-handshake TLS context binding, client-role
  validation, and complete context-policy revalidation before later public-
  release TLS evidence or HTTP, without changing workflows, dependencies,
  runtime APIs, or release authority.
- Add M52/RFC-0035 URL-derived public-release TLS service-identity and non-empty
  peer-certificate observations before negotiated-session validation or HTTP,
  without replacing platform trust or changing workflows, dependencies,
  runtime APIs, or release authority.
- Add M51/RFC-0034 actual negotiated TLS-session validation before every
  public-release HTTP request: exact TLSv1.2/TLSv1.3, a well-formed cipher
  report with at least 128 secret bits, no compression, and HTTP/1.1-compatible
  ALPN, without changing workflows, dependencies, runtime APIs, or release
  authority.
- Add M50/RFC-0033 explicit verified public-release TLS contexts that preserve
  system trust and modern certificate/hostname validation while preventing
  ambient `SSLKEYLOGFILE` session-secret logging, without changing workflows,
  dependencies, runtime APIs, or release authority.
- Add M46/RFC-0029 fresh-runner public release consumer rehearsal using the
  exact admitted same-workflow candidate, a shared bounded verifier, read-only
  permissions, and one pinned download action without new release mutation,
  publication authority, runtime, dependency, or pull-request CI allocation.
- Add M45/RFC-0028 credential-free exact-ID public release retrieval,
  revalidation, and installed-candidate smoke after M44 in the existing tag
  job, with bounded HTTPS requests and no new workflow allocation, action,
  permission, dependency, release mutation, or publication authority.
- Add M44/RFC-0027 exact-source SLSA provenance verification for every
  retrieved release asset and SPDX SBOM verification for the pure wheel, with
  bounded content-silent subprocesses and no new workflow allocation, action,
  permission, dependency, trigger, release mutation, or rollback authority.
- Add M43/RFC-0026 exact-ID published asset retrieval and byte revalidation to
  the existing tag job, without clobber, rollback, immutable-release claims,
  or a new runner, action, permission, dependency, trigger, or release authority.
- Add M42/RFC-0025 exact same-ID postpublication prerelease verification to the
  existing tag job, without automatic rollback, immutable-release claims, or a
  new runner, action, permission, dependency, trigger, or publication authority.
- Add M41/RFC-0024 exact bounded release-notes body verification to the existing
  private-draft gate, without logging note content or changing workflow
  allocations, permissions, dependencies, tags, releases, or publication
  authority.
- Add M40/RFC-0023 fail-closed GitHub draft-release asset verification before
  publication, with exact uploaded name, state, size, and SHA-256 equality and
  no new runner, action, permission, trigger, dependency, tag, release, or
  publication authority.
- Add M39/RFC-0022 fail-closed annotated release-tag, GitHub signature,
  checkout identity, and `origin/main` ancestry verification before the
  existing tag job performs expensive or publishing work, with no new runner,
  action, permission, trigger, dependency, tag, or publication authority.
- Add M38/RFC-0021 fail-closed wheel/sdist reproducibility verification to the
  existing Linux pull-request and tag-release distribution steps without a new
  runner, action, dependency, permission, trigger, or publication claim.
- Add M37/RFC-0020 fail-closed CI change qualification: documentation-only
  changes retain one Linux quality/docs/distribution allocation, substantive
  changes retain all three M36 allocations, and failed Linux qualification
  prevents two unnecessary desktop allocations.
- Consolidate the unchanged eight pull-request validation slices into three
  OS-owned hosted runner allocations under M36/RFC-0019, retaining exact
  Python/platform/graphics/distribution coverage, least privilege, pins,
  caching, timeouts, PR-only triggers, and record-only exclusions.
- Add M35/RFC-0018 third-party conformance-adoption admission evidence that
  fixes the three existing installed profiles, preserves failed and
  not-executed submissions, and retains the current empty-manifest result with
  zero passing external implementations.
- Add M34/RFC-0017 agent-tool recovery-rate admission evidence that preserves
  known failures, calls completed after manual recovery, and unobserved
  terminal states while retaining the current empty-manifest result without a
  measured recovery-free completion rate.
- Run the unchanged eight essential CI jobs only for substantive pull requests,
  avoiding duplicate post-merge `main` runs and `.project/**`-only record runs.
- Add M33/RFC-0016 benchmark-regression-rate admission evidence that restricts
  comparisons to reviewed controlled paired M1-M4 p95 artifacts, preserves
  non-execution, and retains the current empty-manifest result without
  claiming a measured zero rate.
- Add M32/RFC-0015 CI replay-divergence-rate admission evidence that preserves
  non-executed cases, emits only an exact admitted ratio, and retains the
  current empty-manifest result without claiming a measured zero rate.
- Add M31/RFC-0014 issue-response and pull-request-review latency admission
  evidence that preserves pending items, rejects completed-only selection, and
  retains the current empty-manifest result without defining an SLA.
- Add M30/RFC-0013 published-wheel installation-matrix admission evidence that
  rejects source-checkout/local-build substitutes and retains the current
  result as false until one immutable public wheel passes the complete reviewed
  clean-install matrix.
- Use neutral repository-maintenance names: `MAINTAINERS.md` for contributor
  guidance and `.project/` for current state, decisions, and test evidence.
- Add M29/RFC-0012 external contributor-retention admission evidence that
  rejects popularity and synthetic substitutes and retains the current count
  as zero until an independently reviewed human returns for a later merged
  project contribution.
- Add M28/RFC-0011 external sample-game adoption admission evidence that
  rejects project-owned substitutes and retains the externally authored game
  count as zero until a reviewed independent installed-wheel game exists.
- Add M27/RFC-0010 external-contributor rehearsal admission evidence that
  preserves a complete reviewed history and explicitly retains the public-
  documentation usability result as false until an independent human completes
  a reviewed merged good-first contribution without private maintainer knowledge.
- Add M26/RFC-0009 supported-release-channel admission evidence that rejects
  prerelease/local/CI substitutes and explicitly retains gate 6 as false until
  two reviewed supported final feature lines exist.
- Add M25/RFC-0008 external-consumer-feedback admission evidence that rejects
  project-owned substitutes and explicitly retains gate 2 as false until a
  reviewed independent command/receipt integration supplies feedback.
- Add M24/RFC-0007 cross-version receipt-corpus admission evidence that
  verifies immutable historical bytes and explicitly retains gate 1 as false
  until a different supported reader version and release evidence exist.
- Add RFC-0006, a frozen machine-readable receipt-v1 semantic-diff and
  diagnostic-code policy, plus deterministic installed source/wheel/release
  evidence for exact meanings, fail-closed fields, and unknown-code fallback.
- Version the command/receipt readiness report to `/4`; its operation-policy,
  public-reader, and receipt-policy gates are true while three gates and
  overall preview promotion remain incomplete.
- Add RFC-0005, a frozen machine-readable v1 contract, and installed
  source/wheel/release evidence for the exact argument shapes of all seven
  built-in operations; breaking changes require a new operation version.
- Version the command/receipt readiness report to `/3`; its operation-policy
  and public-reader gates were true while four gates and overall preview
  promotion remain incomplete.
- Add a bounded experimental `TransactionReceipt` reader, structured receipt
  decode failures, deterministic limits, frozen receipt/1 baseline fixtures,
  and installed source/wheel/release evidence under RFC-0004.
- Version the command/receipt readiness report to `/2`; its public-reader gate
  is now true while the overall experimental-retention decision remains.
- Add deterministic installed command/receipt preview-readiness evidence and
  RFC-0003, retaining the central contracts as experimental until the complete
  compatibility gate is evidenced.

### Added

- M19 experimental installed `WorldStore` baseline conformance profile with a
  fixed 10-check storage-neutral path, frozen sanitized reports, and production/
  reference evidence from source, isolated wheel, and release sample bundle.
- ADR-0033 retaining explicit trusted composition: the storage conformance
  runner performs no discovery, dynamic import, installation, subprocess,
  networking, provider admission, external-resource lifecycle, or
  certification.
- M18 experimental installed agent-tool baseline conformance profile with a
  fixed 12-check command/receipt path, frozen sanitized reports, and isolated
  source/wheel/release-sample smoke.
- ADR-0032 retaining explicit trusted composition: the agent conformance
  runner performs no discovery, dynamic import, installation, subprocess,
  networking, provider admission, or security certification.
- M17 experimental installed `RenderDevice` baseline conformance profile with
  frozen versioned reports, sanitized failure codes, Null/real-wgpu evidence,
  and isolated wheel/release sample smoke.
- ADR-0031 retaining explicit trusted composition: the conformance runner
  performs no discovery, dynamic import, installation, provider admission, or
  security certification.
- M16 deterministic installed security evidence for the WASM-mod admission
  decision, exercised from source, isolated wheel, and release sample bundle.
- ADR-0030 and a prospective threat model retaining the data-only plugin
  boundary and deferring executable WASM mods until least-privilege, resource,
  determinism, lifecycle, persistence, isolation, conformance, supply-chain,
  and maintenance gates are complete.
- M15 deterministic installed-surface evidence for the visual-editor admission
  decision, exercised from source, isolated wheel, and release sample bundle.
- ADR-0029 retaining the bounded headless inspector and deferring a visual
  editor until public compatibility, authoring, recovery, usability,
  cross-platform packaging, resource-budget, and ownership gates are complete.
- M14 deterministic installed-surface evidence for the constrained-3D scope
  decision, exercised from source, isolated wheel, and release sample bundle.
- ADR-0028 retaining layered 2D and deferring constrained 3D until product,
  engine-contract, agent-semantic, headless, cross-platform, resource-budget,
  lifecycle, and maintenance gates are complete.
- M13 bounded offline rollback-readiness evidence over existing canonical
  snapshots and immutable replay branches, with strict artifact validation and
  source/wheel/release-bundle smoke.
- ADR-0027 deferring networking and live rollback until canonical tick-input
  history, protocol/security semantics, cross-platform network simulation,
  resource budgets, lifecycle ownership, and maintenance gates are complete.
- M12 preview data-only plugin manifests with canonical v1 serialization,
  deterministic engine/CPython/platform/capability/native/determinism and
  dependency-graph compatibility checks, plus installed CLI/sample smoke.
- RFC-0002 defining the persistent manifest schema, preview deprecation
  promise, stable issue/report semantics, and prohibition on discovery,
  loading, execution, installation, networking, or ambient registries.
- M11 dependency-free headless 2D presentation authoring: exact-tick sprite
  animation, bitmap glyph layout/extraction, bounded immutable tilemaps,
  seeded fixed-point particles, and a lifecycle-validating audio mix graph.
- ADR-0026 plus an installed-wheel/release-bundle rich 2D showcase covering all
  five M11 module areas through the existing Null render/audio boundaries.
- M10 owned local semantic inspector over the existing MCP stdio tools with a
  read-only default, explicit receipted bootstrap/ticks, versioned NDJSON
  observations, semantic diffs, and exact authority-hash continuity checks.
- ADR-0025 recording the finite headless child-process boundary, pipe
  ownership, protocol validation, architecture bans, and deliberate deferral
  of GUI/editor, network, remote-attach, and arbitrary process-launch features.
- M9 bounded isolated Box2D-candidate lifecycle/repeat-trace probe and
  architecture fixtures that keep the native binding out of engine source.
- ADR-0024 recording the evidence-based Box2D v3 plugin deferral and complete
  wheel, ownership, headless, stability, threading, determinism, conformance,
  authority, and maintenance revisit gate.
- M8 provider-neutral gamepad connection/button/axis events, explicit
  deadzone/scale action bindings, Null/GLFW providers, and Clockwork Arena
  controls. The GLFW adapter deliberately omits ambiguous trigger axes instead
  of converting an unavailable axis into false input.
- ADR-0023 recording the evidence-based SDL3 adapter deferral and measurable
  binding/binary/ownership/conformance revisit gate.
- M7 versioned, sanitized `cProfile` evidence and strict tamper-resistant
  validation for the representative 10,000-entity and 10,000-sprite workloads.
- RFC-0001 and ADR-0022 recording the evidence-based decision to defer the
  first Rust/PyO3 kernel.

### Changed

- Consolidated pull-request CI from 14 to 8 essential jobs: one complete
  Ubuntu 3.12 quality/test/distribution gate, four Python/OS compatibility
  jobs, and three real cross-platform graphics jobs. Universal-wheel and
  release smoke now run once instead of redundantly on every operating system.
- Reduced detached query overhead by resolving column metadata once, skipping
  unused read-only signatures, and sharing copy/signature traversals.
- Reduced presentation extraction and float32 sprite-packing allocations while
  preserving exact validation, error, ownership, and provider-neutral layout
  behavior.

## 0.1.0a1 - 2026-08-05

### Added

- M0 repository contract and deterministic headless walking skeleton.
- M1 generational entity IDs and deterministic slot allocator with structured stale-handle failures.
- Explicit component UUIDs, immutable schema registries, validation metadata, and adjacent forward migrations.
- Canonical dense/sparse world storage, copy-safe component ownership, change epochs, cloning, and an independent dictionary reference model.
- Storage-neutral typed queries, changed-epoch filters, explicit writable row cursors, and private plan caching.
- World-bound local structural command buffers with exact deferred-token ownership and atomic clone-staged flush.
- Explicit typed resources with copy-owned singleton storage and deterministic conflict-aware serial schedule planning.
- Additive fixed-step application runtime with immutable input, declaration-enforcing system contexts, retained catch-up backlog, and one PRE/SIM command flush before POST.
- Sanitized M1 benchmark and validation tooling with raw samples, p50/p95/p99 distributions, environment metadata, and explicit local target observations.
- M2 bounded canonical JSON, immutable versioned command/transaction envelopes, and explicit operation registry.
- Atomic clone-staged world sessions with optimistic hashes, dry-run, authoritative resource codecs, staged ticks, canonical receipts, and exact semantic diffs.
- Canonical authority snapshots with bounded atomic restore, registered forward migrations, SHA-256 verification, and deterministic named PCG32 random streams.
- Self-contained canonical replay timelines with exact tick/hash batches, verified checkpoints, composition headers, and immutable parent-referenced branches.
- Project-confined data-only CLI workflows for equivalent command receipts, snapshot extraction, replay verification, and semantic snapshot diffing.
- Exhaustive session resource roles, detached authority views, project-bound snapshots, one-tick replay branch boundaries, and handle-bounded CLI artifact reads.
- M3 backend-neutral render descriptors, scoped generational handles, immutable presentation extraction, and deterministic render-graph validation.
- Optional exactly pinned wgpu/rendercanvas/GLFW rendering with instanced atlas sprites, tiles, orthographic cameras, debug primitives, offscreen RGBA capture, resize/minimize behavior, and typed device loss.
- Reproducible 1k/10k renderer benchmarks, tolerant GPU fixtures, and graphics-extra CI coverage.
- M4 provider-neutral keyboard, mouse, pointer, resize, focus, and close records with deterministic digital transitions and 2D action mapping.
- Validated `asset://` manifests, project path confinement, content-addressed dependency invalidation, bounded PNG decoding, and safe retained texture replacement.
- Pure-Python AABB/circle overlap, a property-tested deterministic spatial grid, documented kinematic resolution, and a lifecycle-validating Null audio backend.
- ECS-authoritative Clockwork Arena gameplay with deterministic waves, enemies, projectiles, health, score, restart, exact 3,600-tick fixture/replay evidence, optional wgpu rendering, and stress benchmark tooling.
- M5 transport-independent typed agent service with immutable tool schemas, explicit read/write/capture/test capabilities, quotas, redaction, mutation serialization, and provider ownership.
- Equivalent direct Python, project-confined CLI, and local stdio MCP `2025-11-25` tool calls over the existing transaction, receipt, snapshot, diff, replay, capture, telemetry, and acceptance-test contracts.
- Agent World Builder acceptance composition exercising describe, validate, apply, fixed ticks, offscreen capture, query, adjustment, semantic diff, replay evidence, telemetry, and registered in-process checks.
- M6 deterministic release staging with a pure wheel, source distribution, sample bundle, SPDX 2.3 SBOM, checksums, notices, manifest, and isolated cross-platform artifact smoke.
- Explicit `internal`, `experimental`, `preview`, and `stable` compatibility policy with exact `__all__`/`__stability__` metadata validation for every public Python export.
- Community-alpha user, adapter, release, contribution, triage, roadmap, and retrospective documentation.
- Tag-only, immutable-action release automation for build-provenance and SBOM attestations plus staged GitHub prerelease creation; no PyPI publishing step.
- Declarative triage labels, focused issue forms, and an issue-ready good-first contribution queue.

## 0.1.0.dev0 - 2026-08-04

- Initial pre-alpha development version reserved for the M0 walking skeleton.
