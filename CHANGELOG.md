# Changelog

All notable changes to LudoWeave Engine will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project intends to use [Semantic Versioning](https://semver.org/spec/v2.0.0.html) once release compatibility levels are defined.

## Unreleased

- Add M164/RFC-0147's test-only [Windows inherited-launch failure
  probe](docs/security/cache-cleanup-windows-inherited-launch-failure-probe.md).
  It proves one real missing-executable failure restores noninheritability
  while preserving parent ownership and denial, without adding runtime
  behavior or CI allocation.
- Add M163/RFC-0146's test-only [Windows inherited-handle retention
  probe](docs/security/cache-cleanup-windows-inherited-handle-probe.md). It
  proves one explicitly allowlisted inherited handle retains the native rename
  denial after the parent closes its handle, without adding runtime behavior
  or CI allocation.
- Add M162/RFC-0145's test-only [Windows duplicated-handle retention
  probe](docs/security/cache-cleanup-windows-duplicated-handle-probe.md). It
  proves one same-process duplicate retains the native rename denial after the
  original closes, without adding runtime behavior or CI allocation.
- Add M161/RFC-0144's test-only [Windows acknowledged-release timeout
  probe](docs/security/cache-cleanup-windows-acknowledged-release-timeout-probe.md).
  It separates accepted release intent from native handle close without adding
  runtime behavior or CI allocation.
- Add M160/RFC-0143's test-only [Windows live-blocker wait-timeout
  probe](docs/security/cache-cleanup-windows-live-wait-timeout-probe.md).
  It captures one immediate live-child wait timeout without adding runtime
  behavior or CI allocation.
- Add M159/RFC-0142's test-only [Windows blocker broken-control-pipe
  probe](docs/security/cache-cleanup-windows-broken-control-pipe-probe.md).
  It captures one exact post-termination native pipe-write failure without
  adding runtime behavior or CI allocation.
- Add M158/RFC-0141's test-only [Windows blocker invalid-control-token
  probe](docs/security/cache-cleanup-windows-invalid-control-token-probe.md).
  It distinguishes one fixed non-release byte from EOF without adding runtime
  behavior or CI allocation.
- Add M157/RFC-0140's test-only [Windows blocker control-pipe EOF
  probe](docs/security/cache-cleanup-windows-control-pipe-eof-probe.md). It
  exercises the existing helper's invalid-control cleanup without adding
  runtime or CI allocation.
- Add M156/RFC-0139's test-only [Windows abrupt blocker-owner termination
  probe](docs/security/cache-cleanup-windows-abrupt-blocker-termination-probe.md).
  It bypasses the graceful release handshake and verifies one bounded
  forced-termination transition without adding runtime or CI allocation.
- Add M155/RFC-0138's test-only [Windows child-owned share-delete
  handshake](docs/security/cache-cleanup-windows-child-owned-share-delete-handshake.md).
  It orders a distinct blocker process's acquisition and close around the
  unchanged native rename probe without adding runtime or CI allocation.
- Add M154/RFC-0137's test-only [Windows native sharing-violation
  probe](docs/security/cache-cleanup-windows-native-sharing-violation-probe.md).
  It captures one direct child `MoveFileExW` denial/release result without
  adding runtime, dependency, workflow, or CI allocation.
- Add M153/RFC-0136's test-only [Windows share-delete exclusion
  probe](docs/security/cache-cleanup-windows-share-delete-exclusion-probe.md).
  It pairs one blocked child rename with the identical post-close success
  without adding runtime, dependency, workflow, or CI allocation.
- Add M152/RFC-0135's test-only [Windows cross-process substitution
  probe](docs/security/cache-cleanup-windows-cross-process-substitution-probe.md).
  It executes one fixed child-process namespace change without adding runtime,
  dependency, workflow, or CI allocation.
- Add M151/RFC-0134's test-only [Windows retained-parent substitution
  probe](docs/security/cache-cleanup-windows-retained-parent-substitution-probe.md).
  It executes one deterministic namespace substitution without adding runtime,
  dependency, workflow, or CI allocation.
- Add M150/RFC-0133's test-only [Windows directory-junction refusal
  probe](docs/security/cache-cleanup-windows-junction-probe.md). It executes an
  NTFS reparse case without elevation and adds no runtime, dependency,
  workflow, or CI allocation.
- Add M149/RFC-0132's test-only [Windows cache-cleanup capability
  probe](docs/security/cache-cleanup-windows-capability-probe.md). It exercises
  private owned handles only under pytest temporary storage; Windows remains
  unadmitted and no runtime, dependency, workflow, or CI allocation is added.
- Accept M148/RFC-0131's [cache-cleanup platform-capability
  decision](docs/security/cache-cleanup-platform-capability-decision.md).
  Current portable CPython is insufficient for the complete M147 safe-mutation
  chain; no platform, cleanup API, dependency, workflow, or CI change is added.
- Adopt M147/RFC-0130's [asset-cache cleanup threat
  model](docs/security/cache-cleanup-threat-model.md). It defines the assets,
  trust boundaries, filesystem/concurrency/recovery threats, invariants, and
  cross-platform verification gate while adding no cleanup authority, runtime,
  dependency, workflow, or CI change.
- Record M146/RFC-0129 cache-cleanup readiness deferral. Existing aggregate
  evidence does not identify deletion candidates or prove current-state safety;
  cleanup remains deferred with explicit identity, roots, quiescence, policy,
  recovery, and authorization gates and no runtime, dependency, workflow, or CI
  change.
- Add M145/RFC-0128 strict saved unreferenced-preview verification. One bounded
  canonical preview is recomputed against the exact plan and admitted saved
  fingerprint entirely offline; success binds the preview digest without cache
  access, authenticity claims, mutation, dependency, workflow, or CI changes.
- Add M144/RFC-0127 offline unreferenced-blob preview composition. The new
  command strictly admits one bounded saved fingerprint after current-input
  preflight and emits the unchanged M143 aggregate preview without cache access,
  a new protocol, trust claim, mutation, dependency, workflow, or CI change.
- Add M143/RFC-0126 path-free unreferenced-blob preview evidence. The new
  command reuses one verified read-only fingerprint observation and reports
  only existing aggregate count/bytes plus plan/observation identity; it grants
  no deletion eligibility, mutation, policy, dependency, workflow, or CI.
- Add M142/RFC-0125 strict saved cache-fingerprint comparison verification.
  One bounded canonical report is recomputed from the exact current plan and
  two admitted fingerprints entirely offline; success binds the path-free
  report digest without claiming authenticity, reading a cache, adding a
  dependency, changing a workflow, or expanding CI.
- Add M141/RFC-0124 offline comparison of two canonical saved cache
  fingerprints. Both records bind to one exact current plan and reuse M140's
  fixed path-free aggregate report with no cache access, fresh observation,
  new protocol, authenticity claim, dependency, workflow, or CI change.
- Add M140/RFC-0123 path-free saved cache-fingerprint comparison. One exact
  plan preflight and one unchanged bounded observation produce fixed signed
  deltas for the twelve existing M137 aggregate fields plus an identity-equality
  boolean. It adds no per-object diff, identity/path disclosure, authenticity,
  cleanup authority, dependency, workflow, or CI change.
- Add M139/RFC-0122 strict saved cache-fingerprint verification. Bounded
  duplicate/non-finite-rejecting canonical decoding binds the saved M138 record
  to the exact current plan before one fresh read-only observation; success is
  path-free `ludoweave.asset-cache-fingerprint-verification/1` integrity
  equality, not authenticity, provenance, cleanup authority, dependency,
  workflow, or CI change.
- Add M138/RFC-0121 deterministic cache-observation fingerprinting. One M137
  bounded verification pass now emits path-free
  `ludoweave.asset-cache-fingerprint/1` evidence binding exact canonical action
  metadata and CAS digest/size membership under sorted length-framed SHA-256.
  It adds no timestamp, atomic-snapshot claim, deletion eligibility, cleanup
  authority, dependency, workflow, or CI change.
- Add M137/RFC-0120 bounded read-only whole-cache inventory. The additive
  `ludoweave.asset-cache-inventory/1` contract strictly verifies engine-owned
  action metadata and streams every CAS blob under tightening-only entry and
  byte limits, then reports current-plan, other, and no-observed-reference
  storage aggregates. It adds no deletion eligibility, cleanup authority,
  dependency, workflow, or CI change.
- Add M136/RFC-0119 bounded saved asset-cache population verification. Strict
  duplicate-rejecting decoding reconstructs `ludoweave.asset-cache-population/1`
  under hard byte/entry bounds; the new `source
  asset-cache-population-verify` command preflights the complete exact current
  plan before read-only verification of every referenced action and CAS
  payload. It adds no decoder fallback, cache/project write, signature,
  authenticity/provenance claim, dependency, workflow, or CI change.
- Add M135/RFC-0118 explicit post-realization cache population. The new
  `ludoweave.asset-cache-population/1` operation and `source
  asset-cache-populate` command verify current inputs and every cache candidate,
  decode only misses, and acquire write authority only after complete
  realization. Publication retains M132's atomic per-entry behavior and
  possible valid-prefix/orphan effects on later failure; it adds no rollback,
  remote cache, dependency, engine-root API, version, workflow, or CI change.
- Add M134/RFC-0117 read-only cache-assisted asset realization. Complete
  detached-source preflight and all cache verification precede decoding of
  exact misses; hit and decoded artifacts share the existing bounds and
  canonical plan order, with no automatic cache publication or CI change.
- Add M133/RFC-0116 verified read-only asset-cache lookup. Exact current plan
  actions now produce path-free hit/miss evidence only after duplicate-free
  canonical metadata and referenced CAS payload verification, without creating
  or changing the cache, decoding an asset, or changing CI.
- Add M132/RFC-0115 explicit local asset-cache publication. Materialized M131
  payloads are stored in a verified SHA-256 CAS before atomically visible
  action metadata; corrupt collisions fail closed and no project, remote cache,
  dependency, workflow, or CI surface changes.
- Add M131/RFC-0114 bounded built-in decoder execution through `ludoweave
  source asset-build`. Exact detached inputs are revalidated before decoding;
  canonical `ludoweave.asset-build-result/1` records output identities with no
  retained payload, cache read/write, project write, worker, plugin, or
  workflow allocation.
- Add M130/RFC-0113 confined saved-plan loading plus read-only `ludoweave
  source asset-plan-verify`. Verification recomputes current M128 inputs and
  the M129 plan, reports mismatches without compared content, and performs no
  asset decode/build, cache read/write, artifact creation, or workflow
  allocation.
- Add M129/RFC-0112 canonical `ludoweave.asset-build-plan/1` values plus
  read-only `ludoweave source asset-plan`. Plans verify current M128 inputs,
  order the exact selected closure dependency-first with URI tie-breaking, and
  precompute unchanged M4 cache keys without asset decode/build, cache read or
  write, artifact creation, scheduler execution, or workflow allocation.
- Add M128/RFC-0111 canonical `ludoweave.asset-source-lock/1` values plus
  read-only `ludoweave source asset-lock` generation and `asset-verify`.
  Selected sources are hashed through project-confined bounded descriptors;
  there is no asset decode, asset build, import, cache write, world mutation,
  or workflow allocation.
- Add M127/RFC-0110 deterministic source-to-asset dependency checking through
  `ludoweave source assets`. The read-only report preserves direct declarations
  separately from their resolved asset-graph closure, reads no asset source,
  rejects no unused asset, builds no asset, mutates no world, and adds no
  workflow allocation.
- Add M126/RFC-0109 bounded project-confined loading, deterministic decoding,
  and canonical normalization for the existing `ludoweave.assets/1` manifest.
  The loader reads no asset source, builds no asset, creates no cache, performs
  no source-to-asset resolution or world mutation, and adds no workflow
  allocation.
- Add M125/RFC-0108 canonical `ludoweave.source-lock/1` values plus read-only
  `ludoweave source lock` generation and `ludoweave source verify`. Locks bind
  the normalized manifest and every explicit scene/prefab content identity;
  they are not atomic filesystem snapshots, signatures, imports, caches, world
  mutations, receipts, or new workflow allocations.
- Add M124/RFC-0107 bounded `ludoweave.source-manifest/1` values and
  `ludoweave source check PROJECT --manifest FILE`. The aggregate canonical
  report validates only explicit project-confined scene or prefab/instance
  entries; there is no discovery, compile, application-schema resolution,
  world mutation, receipt, write, dependency, root-API, or workflow allocation
  change.
- Add M123/RFC-0106 `ludoweave source check` for read-only, project-confined
  scene or explicit prefab-pair preflight. Success emits canonical
  `ludoweave.cli.source-check/1` JSON; there is no compile, world mutation,
  receipt, directory discovery, cache, dependency, root-API, or workflow
  allocation change.
- Add M122/RFC-0105 project-confined prefab file loading through two explicit
  `HeadlessProject` methods. Callers select separate `ludoweave.prefab/1` and
  `ludoweave.prefab-instance/1` files; there is no implicit pairing, directory
  discovery, cache, live update, world mutation, workflow, dependency, or
  root-API change.
- Add M121/RFC-0104 project-confined scene file loading to the existing
  headless composition root. Reads are relative, bounded, synchronous, and
  detached before the unchanged `ludoweave.scene/1` decoder; there is no world
  mutation, directory discovery, prefab file loading, file URI handling, live
  update, dependency, workflow, or root-API change.
- Add M120/RFC-0103 one-level `ludoweave.prefab/1` fragments and
  `ludoweave.prefab-instance/1` schema-aware field replacements. Planning adds
  canonical prefab provenance and compiles to ordinary `entity.spawn` commands
  with receipt aliases, with no nested prefab inheritance, live update, file
  I/O, new persistent operation, dependency, workflow, or root-API change.
- Add M119/RFC-0102 versioned data-only scene documents and deterministic
  compilation to ordinary `entity.spawn` commands. Receipt aliases expose the
  local-ID-to-runtime-entity mapping while canonical runtime state remains in
  the world store; there is no file I/O, prefab inheritance, live update,
  dependency, workflow, or root-API change.
- Record M118/RFC-0101 decision to retain Python 3.15 outside the supported
  range after one exact Windows CPython 3.15.0b1 installed-wheel observation,
  with no metadata, doctor, runtime, dependency, workflow, or support change.
- Record M117/RFC-0100 decision to retain standard GIL CPython as the supported
  baseline after an exact CPython 3.14.5t installed-wheel serial-compatibility
  observation, with no concurrent-safety, graphics, performance, workflow,
  dependency, runtime API, or support-promotion claim.
- Record M116/RFC-0099 decision to separate sample-bundle semantic portability
  from byte identity. The exact supported-runtime Windows producer-consumer
  matrix extracts the same 50-file source tree despite different valid Deflate
  bytes, with no alternate compression method, workflow, dependency, producer,
  verifier, runtime API, or release-authority change.
- Record M115/RFC-0098 decision to scope sample-bundle byte reproducibility to
  the release environment. Repeated fixed-environment production remains the
  claim; supported runtimes receive no cross-runtime byte-identity promise and
  manifests gain no compressor identity. There is no workflow, allocation,
  dependency, producer, verifier, runtime API, or release-authority change.
- Record M114/RFC-0097 decision to retain sample-member compression-level non-
  observability. The fixed producer remains explicit at level `9`, while the
  verifier adds no exact level-9 profile, inferred compressor level, payload-
  content read, workflow, dependency, producer, runtime API, or release-
  authority change.
- Record M113/RFC-0096 decision to retain sample-member compression-method
  compatibility. M64's stored/deflated allowlist and M95's local/central
  agreement remain unchanged while the producer stays deflated, with no exact
  deflate-only profile, new decompressor, payload-content read, workflow,
  dependency, producer, runtime API, or release-authority change.
- Record M112/RFC-0095 decision to retain sample-member creating-system
  compatibility. Standard-library host markers remain admitted without a
  creating-system allowlist or host-specific external-attribute interpretation;
  M65's file-type boundary and the producer's fixed host `3` remain unchanged,
  with no payload-content read, workflow, dependency, producer, runtime API,
  or release-authority change.
- Record M111/RFC-0094 decision to retain sample-member permission
  compatibility. M65's symlink/non-regular rejection remains the verifier
  boundary, with no exact external-attribute profile, permission restoration,
  payload-content read, workflow, dependency, producer, runtime API, or
  release-authority change.
- Record M110/RFC-0093 decision to retain sample-member timestamp compatibility.
  An exact fixed-producer tuple caused 22 established architecture regressions,
  so M98 local/central consistency remains the verifier boundary with no
  timezone or UTC conversion, payload-content read, workflow, dependency,
  producer, runtime API, or release-authority change.
- Add M109/RFC-0092 zero sample-member internal-attribute profile preflight.
  Public central `ZipInfo.internal_attr` must equal zero after established
  local-header, payload-layout, extra-field, member-metadata, and M105-M108
  profile checks and before exact inventory, reads, or staging, with no text/
  binary content interpretation, payload-content read, workflow, dependency,
  producer, runtime API, or release-authority change.
- Add M108/RFC-0091 exact sample-member creation-version profile preflight.
  Public central `ZipInfo.create_version` must equal `20` after established
  local-header, payload-layout, extra-field, member-metadata, M105 flag, M106
  reserved-byte, and M107 extraction-version checks and before exact inventory,
  reads, or staging, with no general creation-version semantics parser,
  payload-content read, workflow, dependency, producer, runtime API, or release-
  authority change.
- Add M107/RFC-0090 exact sample-member extraction-version profile preflight.
  Public central `ZipInfo.extract_version` must equal `20` after established
  local-header, payload-layout, extra-field, member-metadata, M105 flag, and
  M106 reserved-byte checks and before exact inventory, reads, or staging, with
  no general extraction-version semantics parser, no payload-content read, and
  no workflow, dependency, producer, runtime API, or release-authority change.
- Add M106/RFC-0089 zero sample-member extraction-version reserved-byte
  profile preflight. Public central `ZipInfo.reserved` must equal zero after
  established local-header, payload-layout, extra-field, member-metadata, and
  M105 flag-profile checks and before exact inventory, reads, or staging, with
  no extraction-version semantics parser, no payload-content read, and no
  workflow, dependency, producer, runtime API, or release-authority change.
- Add M105/RFC-0088 zero sample-member general-purpose-flag profile preflight.
  Public central `ZipInfo.flag_bits` must equal zero after established specific-
  flag, local-header, payload-layout, and extra-field checks, then after decoded-
  name/member-metadata policy and before exact inventory, reads, or staging,
  with no flag-semantics parser, no payload-content read, and no workflow,
  dependency, producer, runtime API, or release-authority change.
- Add M104/RFC-0087 empty sample-member extra-field profile preflight. Public
  central `ZipInfo.extra` must be empty after established extra-field,
  local-header, payload-bound, and contiguity checks and before decoded-name
  policy, metadata, inventory, reads, or staging, with no extra-field semantics
  parser, no payload-content read, and no workflow, dependency, producer,
  runtime API, or release-authority change.
- Add M103/RFC-0086 exact compressed-payload contiguity preflight. Each
  calculated payload end must equal the next local header or conventional
  central directory before decoded-name policy, metadata, inventory, reads, or
  staging, with M102 overlap precedence, no decompression or recompression, no
  payload-content read, no payload-integrity certification, and no workflow,
  dependency, producer, runtime API, or release-authority change.
- Add M102/RFC-0085 compressed-payload upper-bound preflight. Each calculated
  compressed payload end must not exceed the next local header or conventional
  central directory before decoded-name policy, metadata, inventory, reads, or
  staging, with no decompression or recompression, no exact-contiguity
  requirement, no gap or adjacency ban, no payload-integrity certification,
  and no workflow, dependency, producer, runtime API, or release-authority
  change.
- Add M101/RFC-0084 local-header uncompressed-size consistency preflight. Each
  bounded four-byte local uncompressed size must equal public central
  `ZipInfo.file_size` before decoded-name policy, metadata, inventory, reads,
  or staging, with no decompression or recompression, no compression-ratio
  policy, no payload or next-header bound, no inter-member layout validator,
  and no workflow, dependency, producer, runtime API, or release-authority
  change.
- Add M100/RFC-0083 local-header compressed-size consistency preflight. Each
  bounded four-byte local compressed size must equal public central
  `ZipInfo.compress_size` before decoded-name policy, metadata, inventory,
  reads, or staging, with no decompression or recompression, no uncompressed-
  size comparison, no payload or next-header bound, no inter-member layout
  validator, and no workflow, dependency, producer, runtime API, or release-
  authority change.
- Add M99/RFC-0082 local-header CRC-32 consistency preflight. Each bounded
  four-byte local CRC must equal public central `ZipInfo.CRC` before decoded-
  name policy, metadata, inventory, reads, or staging, without CRC
  recomputation, compressed/uncompressed size comparison, payload or next-
  header bounds, inter-member layout validation, workflow, dependency,
  producer, runtime API, or release-authority change.
- Add M98/RFC-0081 local-header timestamp consistency preflight. Each bounded
  four-byte local DOS timestamp must exactly equal the bytes represented by
  public central `ZipInfo.date_time` before decoded-name policy, metadata,
  inventory, reads, or staging, without timestamp semantics, timezone or UTC
  conversion, CRC/size comparison, inter-member layout validation, workflow,
  dependency, producer, runtime API, or release-authority change.
- Add M97/RFC-0080 local-header extraction-version consistency preflight. Each
  bounded two-byte local pair must exactly equal public central
  `ZipInfo.extract_version` and `ZipInfo.reserved` before decoded-name policy,
  metadata, inventory, reads, or staging, without a supported-version
  allowlist, time/CRC/size comparison, inter-member layout validator, workflow,
  dependency, producer, runtime API, or release-authority change.
- Add M96/RFC-0079 local-header extra-field consistency preflight. Each bounded
  local extra field must exactly equal public central `ZipInfo.extra` before
  decoded-name policy, metadata, inventory, reads, or staging, without an
  extra-field semantics parser, broad extra-field ban, version/time/CRC/size
  comparison, next-header or payload bound, inter-member layout validator,
  workflow, dependency, producer, runtime API, or release-authority change.
- Add M95/RFC-0078 local-header compression-method consistency preflight. Each
  bounded two-byte local compression method must equal the parser-exposed
  central `ZipInfo.compress_type` before decoded-name policy, metadata,
  inventory, reads, or staging, without a local extra-field comparison,
  version/time/CRC/size comparison, field-wide consistency check, next-header
  or payload bound, an inter-member layout validator, workflow, dependency,
  producer, runtime API, or release-authority change.
- Add M94/RFC-0077 local-header flag-consistency preflight. Each bounded two-
  byte local general-purpose flag field must equal the parser-exposed central
  `ZipInfo.flag_bits` before decoded-name policy, metadata, inventory, reads,
  or staging, without a local compression-method or extra-field comparison,
  field-wide consistency check, next-header or payload bound, an inter-member
  layout validator, workflow, dependency, producer, runtime API, or release-
  authority change.
- Add M93/RFC-0076 local-header name-consistency preflight. Each bounded local
  file-name must byte-match the parser-exposed central name under the central
  CP437/UTF-8 encoding before decoded-name policy, metadata, inventory, reads,
  or staging, without local-flag or extra-field comparison, next-header or
  payload bounds, an inter-member layout validator, workflow, dependency,
  producer, runtime API, or release-authority change.
- Add M92/RFC-0075 local-header variable-envelope bounds preflight. The two
  local length declarations must keep each complete header envelope before
  decoded-name policy, metadata, inventory, reads, or staging, without local-
  name comparison, extra-field parsing, next-header or payload bounds, an
  inter-member layout validator, workflow, dependency, producer, runtime API,
  or release-authority change.
- Add M91/RFC-0074 fixed local-header-prefix bounds preflight. Every parser-
  exposed offset must leave room for the 30-byte fixed local-header prefix
  before decoded-name policy, metadata, inventory, reads, or staging, without
  a local-header field parser, inter-member layout validator, workflow,
  dependency, producer, runtime API, or release-authority change.
- Add M90/RFC-0073 local-header-signature preflight. Every parser-exposed
  offset must now identify the fixed producer's four-byte local-header
  signature before decoded-name policy, metadata, inventory, reads, or staging,
  without a local-header field parser, inter-member layout validator, workflow,
  dependency, producer, runtime API, or release-authority change.
- Add M89/RFC-0072 local-header-offset bounds preflight. Every parser-exposed
  offset must now remain strictly before the conventional central directory
  before decoded-name policy, metadata, inventory, reads, or staging, without
  a local-header parser, inter-member layout validator, workflow, dependency,
  producer, runtime API, or release-authority change.
- Add M88/RFC-0071 local-header-order preflight. Parser-exposed archive entries
  must now have strictly increasing local-header offsets before decoded-name
  policy, metadata, inventory, reads, or staging, without a local-header parser,
  inter-member layout validator, workflow, dependency, producer, runtime API,
  or release-authority change.
- Add M87/RFC-0070 distinct local-header-offset preflight. Parser-exposed local-
  header offsets must now be distinct before decoded-name policy, metadata,
  inventory, reads, or staging, without a local-header parser, offset ordering/
  bounds rule, inter-member layout validator, workflow, dependency, producer,
  runtime API, or release-authority change.
- Add M86/RFC-0069 first local-header placement preflight. The earliest parser-
  exposed local-header offset must now be zero before decoded-name policy,
  metadata, inventory, reads, or staging, without a local-header parser, inter-
  member layout validator, workflow, dependency, producer, runtime API, or
  release-authority change.
- Add M85/RFC-0068 exact conventional central directory placement preflight.
  The final record's declared size plus offset must now land exactly at that
  final record before decoded-name policy, metadata, inventory, reads, or
  staging, without a central-directory record parser, prepended executable
  support, workflow, dependency, producer, runtime API, or release-authority
  change.
- Add M84/RFC-0067 conventional archive entry-count consistency preflight.
  Both final end-record counts must now match the standard reader's parsed
  member count before decoded-name policy, metadata, inventory, reads, or
  staging, without a ZIP64 end-record parser, sentinel resolution, multi-volume
  assembler, workflow, dependency, producer, runtime API, or release-authority
  change.
- Add M83/RFC-0066 conventional archive disk-field preflight. Nonzero current-
  disk or central-directory-start disk fields now fail content-silently before
  decoded-name policy, member metadata, inventory, reads, or staging, without
  a ZIP64 end-record parser, end-record search, multi-volume assembler,
  workflow, dependency, sample producer, runtime API, or release-authority
  change.
- Add M82/RFC-0065 split-volume sample-member preflight. Every parser-exposed
  nonzero `ZipInfo.volume` now fails content-silently before decoded-name
  policy, member metadata, inventory, reads, or staging, without a raw end-
  record parser, multi-volume assembler, workflow, dependency, sample
  producer, runtime API, or release-authority change.
- Add M81/RFC-0064 ZIP comment preflight. Parser-exposed non-empty archive and
  member comments now fail content-silently before decoded-name policy, member
  metadata, inventory, reads, or staging, without a raw ZIP parser, general
  comment scanner, workflow, dependency, sample producer, runtime API, or
  release-authority change.
- Add M80/RFC-0063 ZIP64 sample-member preflight. Exact extra-field ID
  `0x0001` now fails content-silently before member metadata, inventory,
  reads, or staging, using a bounded extra-field walk without a broad extra-
  field ban, raw ZIP64 parser, workflow, dependency, sample producer, runtime
  API, large-file support, or release-authority change.
- Add M79/RFC-0062 Unicode Path sample-member preflight. Exact extra-field ID
  `0x7075` now fails content-silently before member metadata, inventory,
  reads, or staging, using a bounded extra-field walk without a broad extra-
  field ban, workflow, dependency, sample producer, runtime API, or release-
  authority change.
- Add M78/RFC-0061 data-descriptor sample-member preflight. Exact ZIP general-
  purpose bit 3 now fails content-silently before member metadata, inventory
  validation, reads, or staging, without a raw descriptor parser, broad flag
  allowlist, workflow, dependency, sample producer, runtime API, or release-
  authority change.
- Add M77/RFC-0060 NUL-suffixed sample-member name preflight. An exact NUL byte
  in decoded `ZipInfo.orig_filename` now fails content-silently before member
  metadata, inventory validation, reads, or staging, without a general
  normalized-name comparison, raw parser, workflow, dependency, sample
  producer, runtime API, or release-authority change.
- Add M76/RFC-0059 enhanced-deflate sample-member preflight. Central-directory
  ZIP general-purpose bit 4 on compression method 8 now fails content-silently
  before inventory validation, member reads, or staging. Stored members and
  local-header inconsistencies remain outside this exact decision; no broad
  flag allowlist, workflow, dependency, sample producer, runtime API, or
  release authority is added.
- Add M75/RFC-0058 compressed-patch sample-member preflight. ZIP general-
  purpose bit 5 now fails content-silently before inventory validation, member
  reads, or staging, without adding a broad flag allowlist or changing
  workflows, dependencies, the sample producer, runtime APIs, or release
  authority.
- Add M74/RFC-0057 content-silent sample ZIP decompression-failure
  normalization. Exact `zlib.error` from checksum-admitted deflated members
  now uses the existing stable outer error after owned cleanup, without
  broadening to EOF/filesystem/general failures or changing workflows,
  dependencies, the sample producer, runtime APIs, or release authority.
- Add M73/RFC-0056 content-silent sample ZIP text-failure normalization.
  `UnicodeDecodeError` from archive-controlled UTF-8 central-directory or
  local-header names now uses the existing stable outer error after owned
  cleanup, without broadening to all Unicode/value failures or changing
  workflows, dependencies, the sample producer, runtime APIs, or release
  authority.
- Add M72/RFC-0055 content-silent sample ZIP failure normalization. Documented
  `BadZipFile` and `LargeZipFile` failures now use one stable outer error with
  suppressed rendered context and owned cleanup, without changing workflows,
  dependencies, the sample producer, runtime APIs, or release authority.
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
