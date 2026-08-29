# LudoWeave roadmap board

This repository-native board states outcomes and readiness; it is not a delivery-date
promise. Accepted ADRs and milestone acceptance evidence override an older card. Public
issues become the discussion and assignment record once a card is opened.

## Community-alpha release candidate

| Lane | Outcome | Evidence gate |
| --- | --- | --- |
| Done | M0 repository/runtime walking skeleton | Installed pure wheel and cross-platform CI |
| Done | M1 deterministic world core | Reference-model properties and benchmark evidence |
| Done | M2 command/snapshot/replay workflow | Artifact and installed-wheel scenario tests |
| Done | M3 isolated 2D presentation | Null/wgpu vertical slice and graphics CI |
| Done | M4 Clockwork Arena gameplay slice | 3,600-tick replay plus stress evidence |
| Done | M5 local typed agent interface | Agent World Builder and local stdio acceptance |
| Done | M6 community alpha | Release artifact, docs, API, security, and contribution gates |
| Done | M7 performance/native decision | Versioned profiles, ordinary Python optimization, RFC admission decision, and cross-platform smoke |
| Done | M8 gamepad/SDL3 evaluation | Provider-neutral gamepad mapping, pinned GLFW smoke, SDL3 maturity ADR, and cross-platform validation |
| Done | M9 Box2D v3 plugin evaluation | Binding/wheel/lifecycle/headless/API/threading/determinism/conformance admission evidence, ADR, and hosted validation |
| Done | M10 live semantic inspector | Separate local process, versioned semantic stream, command/query reuse, explicit write receipts, lifecycle/security bounds, and quota-conscious essential CI |
| Done | M11 rich 2D authoring | Headless tick animation, bitmap text, immutable tilemaps, fixed-point particles, Null-audio mixing, installed showcase, and hosted validation |
| Done | M12 plugin manifest compatibility | Canonical data-only manifests, deterministic environment/dependency checks, preview compatibility policy, installed CLI smoke, and hosted validation |
| Done | M13 rollback/network-snapshot readiness | Hosted-validated bounded correction-branch evidence, explicit input-history gap, network deferral ADR, and no transport implementation |
| Done | M14 constrained 3D decision | Hosted-validated installed-surface evidence, retained layered-2D scope, complete admission gate, and no 3D runtime implementation |
| Done | M15 visual-editor admission decision | Hosted-validated installed semantic-mutation evidence, retained headless inspector, complete authoring/support gate, and no GUI/editor implementation |
| Done | M16 WASM-mod security admission decision | Hosted-validated installed inert-boundary evidence, prospective threat model, complete security/determinism gate, and no runtime or guest execution |
| Done | M17 installed render-device conformance | Versioned explicit-factory baseline, Null/wgpu evidence, isolated artifact smoke, and unchanged essential CI topology |
| Done | M18 installed agent-tool conformance | Hosted-validated explicit-factory 12-tool baseline, direct-service artifact evidence, and unchanged essential CI topology |
| Done | M19 installed WorldStore conformance | Hosted-validated versioned explicit-factory storage baseline, production/reference artifact evidence, and unchanged essential CI topology |
| Done | M20 command/receipt stability decision | PR #28 squash-integrated; installed same-version evidence, complete preview gate, RFC-0003 decision, and unchanged runtime/CI topology |
| Done | M21 bounded receipt reader and v1 baseline | PR #30 squash-integrated; reviewed strict detached decoding, deterministic limits, frozen single-version fixtures, installed evidence, and all eight essential hosted jobs passed without stability promotion |
| Done | M22 built-in operation argument compatibility | PR #32 squash-integrated; reviewed exact seven-operation v1 policy, installed valid/missing/unknown/default-omission evidence, RFC-0005, artifact smoke, and all eight unchanged essential jobs passed on the corrected head |
| Done | M23 receipt semantic-diff and diagnostic compatibility | PR #34 squash-integrated the corrected exact policy/evidence; 1,050 local tests and both eight-job hosted runs passed with no current actionable review finding |
| Done | M24 cross-version corpus admission readiness | PR #36 squash-integrated; exact preserved history, false current gate, append-only correction, installed artifact smoke, RFC-0007, and both eight-job hosted runs passed |
| Done | M25 external-consumer-feedback admission readiness | PR #38 squash-integrated; strict reviewed manifest, false current gate, reviewed non-IP correction, installed artifact smoke, RFC-0008, and both eight-job hosted runs passed |
| Done | M26 supported release-channel admission readiness | PR #40 squash-integrated; strict empty reviewed manifest, false current gate, complete-prefix correction, installed artifact smoke, RFC-0009, and both eight-job hosted runs passed |
| Done | M27 external-contributor rehearsal admission readiness | PR #42 squash-integrated; strict empty reviewed manifest, false current result, complete-history admission, installed artifact smoke, RFC-0010, and all eight effective essential jobs passed |
| Done | M28 external sample-game adoption admission readiness | PR #44 squash-integrated; strict empty reviewed manifest, zero current count, corrected authorship/provenance/history gates, installed artifact smoke, RFC-0011, and both eight-job hosted runs passed |
| Done | M29 contributor-retention admission readiness | PR #46 squash-integrated; strict empty reviewed manifest, zero current count, same-person/chronology/history gates, installed artifact smoke, RFC-0012, and all eight essential hosted jobs passed on the corrected head |
| Done | M30 installation-matrix admission readiness | PR #48 squash-integrated; strict empty reviewed manifest, zero current count, immutable public-wheel/full-matrix/history gates, installed artifact smoke, RFC-0013, and all eight essential hosted jobs passed |
| Done | M31 response/review-latency admission readiness | Strict empty reviewed manifest, complete public cohort and pending-item preservation, deterministic aggregates, installed artifact smoke, RFC-0014, and all eight essential jobs passed before verified PR #50 integration |
| Done | M32 replay-divergence-rate admission readiness | PR #52 squash-integrated; strict empty reviewed manifest, complete CI replay-execution cohort and non-execution preservation, exact rational rate, installed artifact smoke, RFC-0015, and all eight essential hosted jobs passed on the corrected head |
| Done | M33 benchmark-regression-rate admission readiness | PR #54 squash-integrated; strict empty reviewed manifest, controlled paired-comparison cohort and non-execution preservation, exact rational rate, installed artifact smoke, RFC-0016, and all eight essential hosted jobs passed |
| Done | M34 agent-tool recovery-rate admission readiness | PR #56 squash-integrated; strict empty reviewed task-directed call manifest, complete cohort and terminal-evidence preservation, exact rational rate, installed artifact smoke, RFC-0017, and one substantive pull-request CI gate |
| Done | M35 third-party conformance-adoption readiness | PR #58 squash-integrated; strict empty reviewed project-accepted submission census, exact existing profile registry, failure/non-execution preservation, zero current count, installed artifact smoke, and RFC-0018 |
| Done | M36 CI runner consolidation | PR #60 squash-integrated; all eight Python/platform/graphics/distribution slices passed in three OS-owned allocations, with five fewer repeated runner setups and RFC-0019 |
| Done | M37 CI change qualification | PR #62 squash-integrated; corrected substantive run `31259200818` passed fail-closed trusted-base classification, the three-allocation M36 gate, Linux-before-desktop qualification, and RFC-0020 |
| Done | M38 distribution reproducibility enforcement | PR #65 squash-integrated; corrected same-source wheel/sdist byte gate passed all three bounded hosted allocations with no new runner or publication authority |
| Done | M39 release-tag integrity enforcement | PR #68 passed exact-head trusted tag identity/ancestry validation plus the three-allocation hosted gate, then squash-integrated with no new runner or publication authority |
| Done | M40 draft-release asset integrity | PR #71 corrected pathological JSON failures after review, passed the exact draft-asset boundary in three bounded hosted allocations, and squash-integrated without new release authority |
| Done | M41 release-notes body integrity | PR #74 passed exact source-body and asset verification in three bounded hosted allocations, then squash-integrated without workflow or release-authority change |
| Done | M42 published prerelease integrity | PR #77 passed exact same-ID draft/public state, timestamp, notes, and asset verification in three bounded hosted allocations, then squash-integrated without new release authority |
| Done | M43 published asset retrieval integrity | PR #80 corrected and passed bounded exact-ID retrieval, same-document byte revalidation, and the three-allocation hosted gate before verified squash integration |
| Done | M44 published release attestation integrity | PR #83 passed exact-source SLSA provenance policy for every retrieved asset plus SPDX wheel-SBOM verification in three bounded hosted allocations, then squash-integrated with unchanged release authority |
| Done | M45 public release consumer-path integrity | PR #86 passed credential-free exact-ID public document/assets, complete revalidation, installed release smoke, and the three-allocation hosted gate before verified squash integration |
| Done | M46 fresh-runner public consumer rehearsal | PR #89 corrected Bash 3.2 plan reuse, passed the exact three-allocation hosted gate, and squash-integrated the separate read-only same-workflow consumer without new release authority |
| Done | M47 cross-platform public consumer rehearsal | PR #92 passed the exact three-allocation hosted gate and squash-integrated the portable verifier plus Ubuntu/Windows/macOS tag-only consumer matrix with unchanged pull-request allocations and release authority |
| Done | M48 public release HTTP response conformance | PR #95 passed the documented `200`/`302` response policy, API-header confinement, stable timeout/transport/output failures, and unchanged workflow/release authority |
| Done | M49 public release connected-peer confinement | PR #99 corrected reserved/site-local handling, passed actual port-443 peer confinement in the exact three-allocation gate, and squash-integrated with unchanged workflows and release authority |
| Done | M50 public release TLS key-log isolation | PR #102 passed explicit verified per-hop context, ambient `SSLKEYLOGFILE` noninterference, stable TLS-context failure, and the exact three-allocation gate before verified squash integration |
| Done | M51 public release negotiated TLS-session conformance | PR #105 corrected malformed unhashable-version handling after review, passed the exact three-allocation gate, and squash-integrated pre-request TLSv1.2/TLSv1.3, cipher-strength, compression, and ALPN checks without changing release authority |
| Done | M52 public release TLS service-identity evidence | PR #108 corrected real-connection invalid-IDNA ordering during review, passed actual socket identity/certificate checks in the exact three-allocation gate, and squash-integrated with unchanged workflows, dependencies, and release authority |
| Done | M53 public release TLS context binding | PR #111 passed exact post-handshake socket/context identity, strict client-role and policy revalidation in the three-allocation hosted gate, then squash-integrated with unchanged workflows, dependencies, and release authority |
| Done | M54 public release TLS session freshness | PR #114 passed exact post-handshake `session_reused is False` evidence on every hop in the three-allocation hosted gate, then squash-integrated with unchanged workflows, dependencies, and release authority |
| Done | M55 public release HTTP response framing | PR #117 corrected the CPython status-line normalization overclaim, passed the corrected exact three-allocation gate, resolved its review finding, and squash-integrated documented HTTP/1.1-class framing checks with unchanged workflows/release authority |
| Done | M56 public release redirect-reference conformance | PR #120 corrected bracket-component validation, passed the corrected exact three-allocation gate, resolved its review finding, and squash-integrated strict status/Location checks with unchanged workflows/release authority |
| Done | M57 public release response-body conformance | PR #123 passed exact built-in bytes-block and declared-versus-streamed `Content-Length` checks in the exact three-allocation gate, then squash-integrated with unchanged workflow/release authority |
| Done | M58 public release cleanup conformance | PR #126 passed ordered response/connection cleanup, primary-failure preservation, and publication-after-cleanup in the exact three-allocation gate, then squash-integrated with unchanged workflow/release authority |
| Done | M59 repository metadata hygiene | PR #129 corrected dangling-root-link detection after review, passed the corrected exact three-allocation gate, and squash-integrated tool-neutral current-tree metadata with immutable provenance and runtime/workflow boundaries intact |
| Done | M60 public release filesystem collision conformance | PR #132 passed final-entry collision detection before network/validator side effects, stable errors, exact three-allocation hosted validation, and verified squash integration with unchanged workflow/release authority |
| Done | M61 public release candidate/output-root separation | PR #135 passed alias- and filesystem-identity-aware read-only candidate ownership, corrected exact three-allocation hosted validation after review, and verified squash integration with unchanged workflow/release authority |
| Done | M62 portable public release asset names | PR #138 passed deterministic portable retrieval-plan basenames, fail-before-asset-side-effect validation, exact three-allocation hosted qualification, and verified squash integration with unchanged workflow/release authority |
| Done | M63 public release output confinement | PR #141 passed one-document consumer output, exact subordinate status conformance, exact three-allocation hosted qualification, and verified squash integration with unchanged workflow/release authority |
| Done | M64 bounded sample-bundle extraction | PR #144 corrected codec admission after review, passed exact three-allocation hosted qualification, and squash-integrated bounded preflight plus 64 KiB stored/deflated streaming without changing workflow or release authority |
| Done | M65 portable sample member paths | PR #147 corrected explicit non-regular mode admission after review, passed exact three-allocation hosted qualification, and squash-integrated portable collision-free staged sample paths without changing workflow, producer, runtime, or release authority |
| Done | M66 staged sample-root publication | PR #150 passed exact three-allocation hosted qualification and squash-integrated same-filesystem staging, completeness-before-publication, single-rename visibility, and owned failure cleanup without workflow, runtime, or release-authority expansion |
| Done | M67 exact sample-bundle inventory conformance | PR #153 passed exact three-allocation hosted qualification and squash-integrated the independent exact 50-file product shape before extraction without a workflow, producer, runtime, or release-authority change |
| Done | M68 bounded sample-archive container admission | PR #156 passed exact three-allocation hosted qualification and squash-integrated pre-open regular-file/16 MiB admission plus same-handle descriptor revalidation before ZIP parsing without a workflow, producer, runtime, or release-authority change |
| Done | M69 encrypted sample-member preflight rejection | PR #159 corrected archive-order masking after review, passed the corrected exact three-allocation hosted gate, resolved its finding, and squash-integrated all-member encryption-flag preflight before any per-member metadata validation without changing workflow, producer, runtime, or release authority |
| Done | M70 sample-archive checksum binding | PR #162 corrected unbounded growth during review, passed exact three-allocation hosted qualification, and squash-integrated bounded same-opened-handle digest checks before ZIP parsing and publication without changing workflow, producer, runtime, or release authority |
| Done | M71 checksum-admitted sample snapshot | PR #165 passed exact three-allocation hosted qualification and squash-integrated a bounded owned spooled snapshot as the exact checksum-admitted ZIP parser input without changing workflow, producer, runtime, dependency, or release authority |
| Done | M72 content-silent sample ZIP failures | PR #168 passed exact three-allocation hosted qualification and squash-integrated stable content-silent normalization for documented ZIP parser failures after owned cleanup without changing workflow, producer, runtime, dependency, or release authority |
| Done | M73 content-silent sample ZIP text failures | PR #171 passed exact three-allocation hosted qualification and squash-integrated stable content-silent normalization for malformed UTF-8 archive names after owned cleanup without changing workflow, producer, runtime, dependency, or release authority |
| Done | M74 content-silent sample ZIP decompression failures | PR #174 passed exact three-allocation hosted qualification and squash-integrated stable content-silent normalization for invalid raw-deflate payloads after owned cleanup without changing workflow, producer, runtime, dependency, or release authority |
| Done | M75 compressed-patch sample-member preflight | PR #177 passed exact three-allocation hosted qualification and squash-integrated exact ZIP general-purpose bit-5 rejection before metadata, inventory, staging, or reads without changing workflow, producer, runtime, dependency, or release authority |
| Done | M76 enhanced-deflate sample-member preflight | PR #180 passed exact three-allocation hosted qualification and squash-integrated method-8 ZIP general-purpose bit-4 rejection before metadata, inventory, staging, or reads without changing workflow, producer, runtime, dependency, or release authority |
| Done | M77 NUL-suffixed sample-member name preflight | PR #183 corrected archive-wide flag precedence after review, passed corrected exact three-allocation hosted qualification, and squash-integrated separate all-member flag/name preflights before metadata, inventory, staging, or reads without a general normalized-name comparison, raw parser, workflow, producer, runtime, dependency, or release-authority change |
| Done | M78 data-descriptor sample-member preflight | PR #186 passed exact three-allocation hosted qualification and squash-integrated exact ZIP general-purpose bit-3 rejection in a separate archive-wide pass before names, metadata, inventory, staging, or reads without a raw descriptor parser, broad flag allowlist, workflow, producer, runtime, dependency, or release-authority change |
| Done | M79 Unicode Path extra-field preflight | PR #189 passed exact three-allocation hosted qualification and squash-integrated exact Info-ZIP extra-field ID `0x7075` rejection before decoded-name policy, metadata, inventory, staging, or reads without a broad extra-field ban, workflow, producer, runtime, dependency, or release-authority change |
| Done | M80 ZIP64 extra-field preflight | PR #192 corrected the CPython disk-start evidence boundary after review, passed corrected exact three-allocation hosted qualification, and squash-integrated exact PKWARE extra-field ID `0x0001` rejection before decoded-name policy, metadata, inventory, staging, or reads without a broad extra-field ban, raw ZIP64 parser, workflow, producer, runtime, dependency, large-file-support, or release-authority change |
| Done | M81 ZIP comment preflight | PR #195 passed exact three-allocation hosted qualification and squash-integrated parser-exposed archive/member comment rejection after established flag/extra-field policy and before decoded-name policy, metadata, inventory, staging, or reads without a raw ZIP parser, general comment scanner, workflow, producer, runtime, dependency, or release-authority change |
| Done | M82 split-volume sample-member preflight | PR #198 corrected its ZIP64 disk-start fixture after review, passed corrected exact three-allocation hosted qualification, and squash-integrated parser-exposed nonzero `ZipInfo.volume` rejection after established flag/extra-field/comment policy and before decoded-name policy, metadata, inventory, staging, or reads without a raw end-record parser, multi-volume assembler, workflow, producer, runtime, dependency, or release-authority change |
| Done | M83 conventional archive disk-field preflight | PR #201 passed exact three-allocation hosted qualification and squash-integrated base-disk enforcement for both conventional final end-of-central-directory disk fields after established flag/extra-field/comment/member-volume policy and before decoded-name policy, metadata, inventory, staging, or reads without a ZIP64 end-record parser, end-record search, multi-volume assembler, workflow, producer, runtime, dependency, or release-authority change |
| Done | M84 conventional archive entry-count preflight | PR #204 passed exact three-allocation hosted qualification and squash-integrated equality checks between both conventional final end-of-central-directory entry counts and the standard reader's parsed member count after M83 disk policy and before decoded-name policy, metadata, inventory, staging, or reads without a ZIP64 end-record parser, sentinel resolution, multi-volume assembler, workflow, producer, runtime, dependency, or release-authority change |
| Done | M85 conventional central-directory placement preflight | PR #207 passed exact three-allocation hosted qualification and squash-integrated the requirement that final conventional central-directory size plus offset land exactly at the final end-of-central-directory record after M84 entry-count policy and before decoded-name policy, metadata, inventory, staging, or reads without a central-directory record parser, prepended executable support, workflow, producer, runtime, dependency, or release-authority change |
| Done | M86 first local-header placement preflight | PR #210 passed exact three-allocation hosted qualification and squash-integrated the requirement that the earliest parser-exposed local-header offset is zero after M85 placement policy and before decoded-name policy, metadata, inventory, staging, or reads without a local-header parser, inter-member layout validator, workflow, producer, runtime, dependency, or release-authority change |
| Done | M87 distinct local-header-offset preflight | PR #213 corrected an implementation-dependent warning assertion, passed exact three-allocation hosted qualification, and squash-integrated distinct parser-exposed local-header offsets after M86 first-offset policy and before decoded-name policy, metadata, inventory, staging, or reads without a local-header parser, offset ordering/bounds rule, inter-member layout validator, workflow, producer, runtime, dependency, or release-authority change |
| Done | M88 local-header-order preflight | PR #216 passed exact three-allocation hosted qualification and squash-integrated strictly increasing parser-exposed local-header offsets for the fixed sample-producer profile after M87 distinctness and before names, metadata, inventory, staging, or reads without a local-header parser, inter-member layout validator, workflow, producer, runtime, dependency, or release-authority change |
| Done | M89 local-header-offset bounds preflight | PR #219 passed exact three-allocation hosted qualification and squash-integrated the requirement that every parser-exposed local-header offset remain strictly before the conventional central directory after M88 order policy and before names, metadata, inventory, staging, or reads without a local-header parser, record-extent or inter-member layout validator, workflow, producer, runtime, dependency, or release-authority change |
| Done | M90 local-header signature preflight | PR #222 passed exact three-allocation hosted qualification and squash-integrated the fixed-producer four-byte local-header signature classifier after M89 bounds policy and before names, metadata, inventory, staging, or reads without a local-header field parser, record-extent or inter-member layout validator, workflow, producer, runtime, dependency, or release-authority change |
| Done | M91 fixed local-header-prefix bounds preflight | PR #225 resolved one stale-status review finding, passed corrected exact three-allocation hosted qualification, and squash-integrated the fixed-producer 30-byte local-header-prefix bound after M90 signatures and before names, metadata, inventory, staging, or reads without a local-header field parser, record-extent or inter-member layout validator, workflow, producer, runtime, dependency, or release-authority change |
| Done | M92 local-header variable-envelope bounds preflight | PR #228 passed exact three-allocation hosted qualification and squash-integrated the two-field local-header variable-envelope bound after M91 and before names, metadata, inventory, staging, or reads without local-name comparison, extra-field parsing, next-header or payload bounds, an inter-member layout validator, workflow, producer, runtime, dependency, or release-authority change |
| Done | M93 local-header name-consistency preflight | PR #231 passed exact three-allocation hosted qualification and squash-integrated the raw local-name consistency classifier after M92 and before decoded-name policy, metadata, inventory, staging, or reads without local-flag or extra-field comparison, next-header or payload bounds, an inter-member layout validator, workflow, producer, runtime, dependency, or release-authority change |
| Done | M94 local-header flag-consistency preflight | PR #234 passed exact three-allocation hosted qualification and squash-integrated the two-byte local/central general-purpose flag consistency classifier after M93 and before decoded-name policy, metadata, inventory, staging, or reads without local compression-method or extra-field comparison, field-wide consistency checking, next-header or payload bounds, an inter-member layout validator, workflow, producer, runtime, dependency, or release-authority change |
| Done | M95 local-header compression-method consistency preflight | PR #237 passed exact three-allocation hosted qualification and squash-integrated the two-byte local/central compression-method consistency classifier after M94 and before decoded-name policy, metadata, inventory, staging, or reads without local extra-field comparison, version/time/CRC/size or field-wide consistency checking, next-header or payload bounds, an inter-member layout validator, workflow, producer, runtime, dependency, or release-authority change |
| Done | M96 local-header extra-field consistency preflight | PR #240 passed exact three-allocation hosted qualification and squash-integrated the bounded local/central extra-field consistency classifier after M95 and before decoded-name policy, metadata, inventory, staging, or reads without an extra-field semantics parser, broad extra-field ban, version/time/CRC/size or field-wide consistency checking, next-header or payload bounds, an inter-member layout validator, workflow, producer, runtime, dependency, or release-authority change |
| Done | M97 local-header extraction-version consistency preflight | PR #243 passed exact three-allocation hosted qualification and squash-integrated the two-byte local/central extraction-version consistency classifier after M96 and before decoded-name policy, metadata, inventory, staging, or reads without a supported-version allowlist, time/CRC/size comparison, inter-member layout validator, workflow, producer, runtime, dependency, or release-authority change |
| Done | M98 local-header timestamp consistency preflight | PR #246 passed exact three-allocation hosted qualification and squash-integrated the four-byte local/central DOS timestamp consistency classifier after M97 and before decoded-name policy, metadata, inventory, staging, or reads without timestamp semantics, timezone/UTC conversion, CRC/size comparison, inter-member layout validation, workflow, producer, runtime, dependency, or release-authority change |
| Done | M99 local-header CRC-32 consistency preflight | PR #249 passed exact three-allocation hosted qualification and squash-integrated the four-byte local/central CRC-32 consistency classifier after M98 and before decoded-name policy, metadata, inventory, staging, or reads without CRC recomputation, size comparison, payload/layout bounds, workflow, producer, runtime, dependency, or release-authority change |
| Active | M100 local-header compressed-size consistency preflight | Require each bounded four-byte local compressed size to equal public central `ZipInfo.compress_size` after M99 and before decoded-name policy, metadata, inventory, staging, or reads without decompression or recompression, uncompressed-size comparison, payload/layout bounds, workflow, producer, runtime, dependency, or release-authority change |
| Active | M101 local-header uncompressed-size consistency preflight | Require each bounded four-byte local uncompressed size to equal public central `ZipInfo.file_size` after M100 and before decoded-name policy, metadata, inventory, staging, or reads without decompression or recompression, compression-ratio policy, payload/layout bounds, workflow, producer, runtime, dependency, or release-authority change |
| Active | M102 compressed-payload upper-bound preflight | Require each compressed payload end to remain at or before the next ordered local header or conventional central directory after M101 and before decoded-name policy, metadata, inventory, staging, or reads without decompression, exact contiguity, gap/adjacency bans, workflow, producer, runtime, dependency, or release-authority change |
| Active | M103 exact compressed-payload contiguity preflight | Require each compressed payload end to equal the next ordered local header or conventional central directory after M102 and before decoded-name policy, metadata, inventory, staging, or reads without decompression, payload-content inspection, workflow, producer, runtime, dependency, or release-authority change |
| Active | M104 empty sample-member extra-field profile preflight | Require public central `ZipInfo.extra` to be empty after established extra-field, local-header, payload-bound, and contiguity checks and before decoded-name policy, metadata, inventory, staging, or reads without an extra-field semantics parser, payload-content inspection, workflow, producer, runtime, dependency, or release-authority change |
| Active | M105 zero sample-member general-purpose-flag profile preflight | Require public central `ZipInfo.flag_bits` to equal zero after established specific-flag, local-header, payload-layout, M104 extra-field, decoded-name, and member-metadata checks and before exact inventory, staging, or reads without a flag-semantics parser, payload-content inspection, workflow, producer, runtime, dependency, or release-authority change |
| Active | M106 zero sample-member extraction-version reserved-byte profile preflight | Require public central `ZipInfo.reserved` to equal zero after established local-header, payload-layout, extra-field, member-metadata, and M105 flag-profile checks and before exact inventory, staging, or reads without an extraction-version semantics parser, payload-content inspection, workflow, producer, runtime, dependency, or release-authority change |
| Active | M107 exact sample-member extraction-version profile preflight | Require public central `ZipInfo.extract_version` to equal `20` after established local-header, payload-layout, extra-field, member-metadata, M105 flag-profile, and M106 reserved-byte checks and before exact inventory, staging, or reads without a general extraction-version semantics parser, payload-content inspection, workflow, producer, runtime, dependency, or release-authority change |
| Active | M108 exact sample-member creation-version profile preflight | Require public central `ZipInfo.create_version` to equal `20` after established local-header, payload-layout, extra-field, member-metadata, M105 flag-profile, M106 reserved-byte, and M107 extraction-version checks and before exact inventory, staging, or reads without a general creation-version semantics parser, payload-content inspection, workflow, producer, runtime, dependency, or release-authority change |
| Active | M109 zero sample-member internal-attribute profile preflight | Require public central `ZipInfo.internal_attr` to equal zero after established local-header, payload-layout, extra-field, member-metadata, and M105-M108 profile checks and before exact inventory, staging, or reads without text/binary content interpretation, payload-content inspection, workflow, producer, runtime, dependency, or release-authority change |
| Active | M110 retain sample-member timestamp compatibility | Retain M98 local/central timestamp consistency and the fixed producer's reproducible tuple after an exact verifier profile caused 22 established architecture regressions; add no timezone or UTC conversion, payload-content inspection, workflow, producer, runtime, dependency, or release-authority change |
| Active | M111 retain sample-member permission compatibility | Retain M65's encoded symlink/non-regular rejection while admitting missing type bits and regular-file permission variants; keep the fixed producer's `0100644` mode without exact external-attribute admission, permission restoration, payload-content inspection, workflow, producer, runtime, dependency, or release-authority change |
| Active | M112 retain sample-member creating-system compatibility | Retain parser-exposed host markers after an exact UNIX-only rule caused 54 established Windows-fixture regressions; preserve M65's file-type boundary and the producer's fixed host `3` without a creating-system allowlist, host-specific external-attribute interpretation, payload-content inspection, workflow, producer, runtime, dependency, or release-authority change |
| Active | M113 retain sample-member compression-method compatibility | Retain M64's stored/deflated allowlist and M95's local/central method agreement while preserving the producer's fixed deflate method, without an exact deflate-only profile, new decompressor, payload-content inspection, workflow, producer, runtime, dependency, or release-authority change |
| Active | M114 retain sample-member compression-level non-observability | Retain verifier independence from writer-only compression-level configuration while preserving the producer's explicit level `9`, M105's zero flags, and M113's method policy, without an exact level-9 verifier profile, inferred compressor level, payload-content inspection, workflow, producer, runtime, dependency, or release-authority change |
| Active | M115 scope sample-bundle byte reproducibility to the release environment | Define sample-bundle byte reproducibility as repeated production inside one fixed resolved release environment while supported runtimes remain compatible consumers/local staging environments, without a cross-runtime byte-identity claim, compressor-identity manifest field, workflow, allocation, producer, verifier, runtime API, dependency, or release-authority change |
| Active | M116 separate sample-bundle semantic portability from byte identity | Retain exact supported-runtime producer-consumer extraction of the same fixed 50-file source tree while M115 permits different valid Deflate bytes, without an alternate compression method, cross-runtime byte-identity claim, cross-platform proof, workflow, allocation, producer, verifier, runtime API, dependency, or release-authority change |
| Active | M117 retain the standard CPython baseline after a free-threaded serial probe | Record exact Windows CPython 3.14.5t installed-wheel serial compatibility while standard GIL CPython 3.12-3.14 remains the supported baseline, without a concurrent-safety, graphics, performance, cross-platform, extension, workflow, allocation, dependency, runtime API, or support-promotion claim |
| Active | M118 retain Python 3.15 prerelease outside support | Record one exact Windows CPython 3.15.0b1 installed-wheel compatibility observation while retaining `>=3.12,<3.15`, exact doctor rejection, and the unchanged supported matrix without a metadata override in normal use, runtime, dependency, workflow, allocation, or support-promotion change |

M6's implementation head passed hosted Windows, macOS, and Linux CI. Creating
or publishing the `v0.1.0a1` tag remains a separate maintainer release action.
M7's implementation head passed the same 14-job hosted matrix, including base
and real-wgpu profiling-contract smokes on all three operating systems.
M8 PR #9 passed the same 14-job hosted matrix, including standardized gamepad
contract and real GLFW smoke on all three operating systems. Haptics, sensors,
raw joysticks, remapping UI, and SDL windows remain future proposals.
M9 evaluates the external rigid-body candidate only. The dependency, adapter,
and canonical-physics integration remain absent unless every admission gate is
evidenced.
M9 PR #10 passed the same 14-job hosted matrix against the validated M8 branch.
The binding remains deferred and no dependency changed.
M10 is a headless protocol client, not a visual editor. It may spawn only the
built-in local stdio composition and cannot listen on a network interface.
M10 PR #11 passed its consolidated eight-job hosted matrix: one complete
quality/test/distribution gate, four compatibility jobs, and real graphics on
all three operating systems.
M11 is a bounded authoring and extraction slice, not a new world store. Real
audio playback, font parsing/shaping, editor-scale tile import, particle DSLs,
and provider objects remain deferred.
M11 PR #12 passed the consolidated eight-job hosted matrix on implementation
commit `aca6d93165a52d88451e8e06d5f1aa8d2e323f1d`.
M14 PR #15 passed the unchanged eight-job hosted matrix on implementation
commit `47443046834eb423be977973775f80494161533d`; layered 2D remains the
accepted scope and no runtime or dependency was added.
PR #16 squash-integrated the exact validated M8-M14 tree into `main` as
verified commit `2c62c8ed9c4ced6292260f6b8c84b1f069de1eaa`. Stacked PRs
#9-#15 are closed as superseded; their branches remain as audit history.
PR #18 integrated the repository-state evidence as verified main commit
`bfea67d2d922e8c591224d18f56c14d572d7f7da`; M15 starts from that exact base.
M15 ready PR #19 passed the unchanged eight-job hosted matrix as run
`31036925179` on implementation commit
`7e85570056dde3678aaeee13eee4036067876d8c`.
PR #19 squash-integrated the exact final M15 tree into `main` as verified
commit `c013dad38b1b64f0f4ccddc19681d643f6414427`. M16 starts from that
exact clean base and treats WASM mods as a separate security decision, not a
runtime implementation.
M16 ready PR #20 passed the unchanged eight-job hosted matrix as run
`31039403209` on implementation commit
`bcaf78fbc78bda8a13a95e397ab15d003dd4a6ce`.
PR #20 squash-integrated exact final M16 head
`808e48a5cb2727c8e1f4d7e896c4f8c7d41bfe1a` into `main` as verified commit
`e2bd57c057c0c16861953c0702b2012c4cabfe90`; both trees are
`05367be9bd85014fe6c70995ac1a69a39f90ef1e`.
M17 starts from integrated `main` commit
`27d2ee9d1f7f75dacc17568650f00ce833ef4fce`. It turns the existing
`RenderDevice` checklist into one installed baseline profile. The profile
executes only an explicitly supplied trusted factory and does not discover,
load, install, sandbox, or certify third-party code. Project-owned Null/wgpu
passes do not count as independent third-party adoption.
Ready PR #22 passed the unchanged eight-job hosted matrix as run
`31042903689` on DCO-signed implementation commit
`8e592f329424719214239bf97bd85dad9c9c5928`. PR #22 squash-integrated exact
final evidence head `148600cdaf9c419fbf552c68f833e0d55655731f` into
`main` as GitHub-verified commit
`610261c8450afc3d7db6ebb2b0425a1829737aec`; both trees are
`1e82568a463c62d0a1cf988b67eea09885ec50e3`.
M18 starts from integrated `main` commit
`ed65b12fa02f672113eac5939a0f616079fee44a`. It turns the existing internal
agent-service acceptance loop into one installed baseline for an explicitly
supplied trusted adapter factory. It does not discover, load, install, launch,
connect to, sandbox, certify, or admit third-party code, and project-owned
direct-service evidence does not count as independent adoption.
Ready PR #24 passed the unchanged eight-job hosted matrix as run
`31046172544` on DCO-signed implementation commit
`c4dde705393eebb7c99af428745e9383750f6b4d`.
PR #24 squash-integrated exact final evidence head
`cb617be0f678528fadc82877ec6910e42c6daf6b` into `main` as GitHub-verified
commit `1000d362432f19c912edf51c67e29c79bf444443`; both trees are
`1b6676ca7c1a6aaa223057a35e0c95242f4e9462`.
M19 starts from integrated `main` commit
`4076f3d7ac0c0a82834a1c98dcb36426ba67ac5e`. It turns existing private
production/reference storage conformance into one installed profile for an
explicitly supplied trusted `factory(ComponentRegistry)`. It does not discover,
load, install, sandbox, certify, or admit code and adds no backend or storage
format. Ready PR #26 passed the unchanged eight-job hosted matrix as run
`31092244573` on DCO-signed implementation commit
`1da692a693c1f92e10b676c2d4539354ce3ff59f`.
PR #26 squash-integrated exact final evidence head
`b93ca591f7063a1500cf105e6b0496b33573c69a` into `main` as GitHub-verified
commit `1a7219e540d8f4cb3c1f60ff12981513c6860ef9`; both trees are
`7fcd614fdde76daf1807f27dbe78ec306a501cc3`.
M20 starts from integrated `main` commit
`2fdeccd697f09f3e165130eb8564a6c585d472d2`. It evaluates whether the
installed command/transaction/receipt contracts are ready for preview without
changing their runtime or wire formats. RFC-0003 retains experimental status
until the complete cross-version, external-feedback, operation/receipt
evolution, bounded-reader, and supported-release-channel gate is evidenced.
Ready PR #28 passed the unchanged eight-job hosted matrix as run
`31095009029` on DCO-signed implementation commit
`d96d132da5ee847d6e86645be5e87a1e4aa5e89e`. PR #28 squash-integrated exact
final evidence head `d04561184996fac507071ad9e7dd0ef9c5e3cb7c` into `main` as
GitHub-verified commit `d166ef86bf25526d9d7715f63263d3cac6db78d4`; both trees are
`c3e2dc1224f530fb483d1b9684ff55329bf9557b`.
M21 starts from integrated `main` commit
`feed793e94c345fac4b146c358a68264ef6e5f62`. It adds the bounded public reader
identified by RFC-0003 and freezes exact `0.1.0a1` receipt/1 fixtures. RFC-0004
marks only the reader-and-bounds gate complete; the fixture corpus remains a
single-version baseline, and no command/receipt stability promotion or
cross-version claim is made.
M22 starts from integrated `main` commit
`291dfb3fd6895a2fdac7a2f0016bb181f0e5bca4`. It records the exact v1
argument contract independently of handler implementation and requires
breaking argument changes to use a new operation version. The installed
composition exercises all seven valid operations plus missing-required and
unknown-field rejection. This satisfies only RFC-0003 gate 3; cross-version
history, external feedback, semantic-diff/diagnostic evolution, and a supported
release channel remain absent. No runtime API, operation, format, dependency,
version, or CI job is added.
Ready PR #32 passed sole GitHub Actions run `31100821087` across all eight
unchanged essential jobs on DCO-signed implementation commit
`f1a89ad460467039f966ed37955144840cd96a12`.
Automated review clarification commit
`cf3ae540e71cda128837ea698f5f175a7abf2fc4` passed necessary follow-up run
`31101607485` across the same eight jobs; the original review thread is
outdated and no actionable thread remains.
PR #32 squash-integrated exact final evidence head
`a5a49dcca277f28bb3e6097f37d5418d5d3c2c9d` into `main` as
GitHub-verified commit `8a4d288c4edf55d0299828b8edee1bd1885884d9`;
both trees are `f513bec716d1735cc47a6aab862bca0f5f770af9`. The branch is
retained for audit history, and no M23 work is included.

M23 starts from integrated `main` commit
`415859e19d9d29caa1168fabc96def509897b056`. It records exact receipt-v1
semantic-diff field sets, presence, ordering, meanings, diagnostic-code
identity, and unknown-code fallback. This satisfies only RFC-0003 gate 5;
cross-version history, external feedback, and a supported release channel
remain absent. No runtime API, protocol field, operation, dependency, version,
or CI job is added.
Ready PR #34 passed initial GitHub Actions run `31104052702` across all eight
unchanged essential jobs on DCO-signed implementation commit
`a6dc30ec62d91b1f6640db2c23797967f2aefefe`. Automated review identified two
valid evidence gaps; DCO-signed correction commit
`4eb61cd49542b0a4753629f31ebe80229c7d45b8` passed necessary follow-up run
`31105197045` across the same eight jobs. PR #34 squash-integrated exact final
evidence head `eacb0153d8ac6e5f65d4d52f02c493bf9a891219` into `main` as
GitHub-verified commit `2f7152565d369225dbf69055b7d42a4c80f46d1a`;
both trees are `6ba709c29688041992bef75a2a83831275ff32db`.

M24 starts from integrated `main` commit
`55c7a72337913303b6b1f6bd31edbca7ff28683b`. It adds an offline admission
harness over the immutable M21 receipt corpus and requires a different reader
version plus supported-release evidence before gate 1 can become true. The
current `0.1.0a1`/empty-release result remains false. No runtime API, protocol,
dependency, version, workflow job, tag, release, or publication is added.
Ready PR #36 targets that exact base from DCO-signed implementation commit
`e590d482246d122120c011969b47f79f9680efa2`. Its sole GitHub Actions run
`31107800179` passed all eight unchanged essential jobs; GitHub reports the PR
`MERGEABLE` and `CLEAN`. Delayed automated review found one valid append-only-
history gap. The locally validated correction freezes mandatory source/release
prefixes and proves a newly pinned future manifest cannot replace the M21 entry;
DCO correction commit `b393d6857f0a60c5d124fdeb25b3779c8f9dab86`
passed necessary run `31108924069` across all eight unchanged essential jobs.
Final thread-aware reread found no actionable finding; squash integration
completed through PR #36 at GitHub-verified `main` commit
`b7b16697d28410567cbddf8eb962c7e6c9e664b8`. Its tree
`fa3c455ccd9722c666cc07cae325f1b50e37ddc7` exactly matches final evidence head
`1a8bd6f19f656eb5c4a0d6bd90f057a69bddbc34`; the branch is retained.

M25 starts from integrated `main` commit
`680e90dd8f9377fece23c43bd9f07ca9d76297de`. It adds an offline admission
harness for manually reviewed independent-consumer feedback and requires exact
public repository, immutable revision, protocol, outcome, and artifact
identities before gate 2 can become true. The reviewed manifest is empty, so
the current result remains false; the synthetic `.invalid` regression proves
only gate logic and is not feedback or adoption evidence. No runtime API,
protocol, dependency, version, workflow job, network activity, release, or
publication is added. Ready PR #38 targets the exact assigned base from
DCO-signed implementation commit
`9667e020c2213d415072b7c7efbd880f6b58abfa`; sole GitHub Actions run
`31111498136` passed all eight unchanged essential jobs, and the first thread-
aware read found no review finding. Delayed review then found one valid numeric-
IP locator gap. The locally validated correction requires a non-IP DNS-style
authority and adds loopback/link-local regressions. DCO correction commit
`90ed57e360765cf7f2d0973e41b8f8ec06dc4b50` passed necessary run
`31112342328` across all eight unchanged jobs. Final thread-aware reread found
no actionable finding. PR #38 squash-integrated exact final evidence head
`d0866967832fe80a49942184e1ab81d3c426a478` into `main` as GitHub-verified
commit `9ec6eeaaed40fefeb64d738d4eaaf3f7a9c4009b`; both trees are
`fcaa7b11a4aa8d1c87e57a810db16682cf9f00e6`, and the branch is retained.

M26 started from integrated `main` commit
`0de919a699dee6b10b6fef9ba2cdce5e3c0f2e62`. It adds an offline admission
harness requiring at least two reviewed supported, non-yanked final releases on
distinct feature lines plus exact publication identities before gate 6 can
become true. The reviewed release set is empty, so the current result remains
false; the prerelease workflow, local candidates, CI, and synthetic regression
are not a supported channel. No runtime API, protocol, dependency, version,
workflow job, tag, GitHub release, PyPI configuration, support promise, or
publication is added. Delayed review found and corrected an incomplete-prefix
admission gap; 1,153 local tests and necessary corrected hosted run
`31116147333` passed. PR #40 squash-integrated exact final evidence head
`ac8dd43e6b93bc89af1f5dd1821948e4860ac88b` as GitHub-verified `main` commit
`a62d28e8c36d9a590e7ad7e7a9e8b49266dcbdde`; both trees are
`e1f39a9c5d2bc81f76b45288225b27a7c782bf50`, and the branch is retained.

M27 starts from verified integrated `main` commit
`c1c3be08f7f75d90e7d1b517adbc30d56902ece4`. It adds an offline admission
harness requiring at least one independently reviewed human good-first
contribution linked to a public project issue and merged pull request, with
exact revisions, patch/feedback hashes, DCO, documented validation, no private
maintainer knowledge, and no protected API/format/dependency/workflow change.
The reviewed rehearsal set is empty, so the current result remains false;
documentation, CI, project-owned fixtures, maintainers, and non-human automation
are not external-contributor usability evidence. No runtime source, public API,
format, dependency, version, workflow job, network activity, contributor
contact, telemetry, publication, or support promise is added. Corrected hosted
run `31119640551` passed all eight effective essential jobs after a minimal
failed-job-only outage recovery. PR #42 squash-integrated exact final evidence
head `349dc3b78dcae2b1c725ed3dc8e5e646ca3d3ac1` as GitHub-verified `main`
commit `ff1c81f8aaa96245706586096f400a5fb03bdd04`; both trees are
`f957c2e40eec5bd2d70cc274079ea334d6a34cc3`.

M28 starts from verified integrated `main` commit
`17401eb32be30862496bbe02366d886a60752fb3`. It adds an offline admission
harness for the longer-term metric counting externally authored sample games.
A future record requires manually reviewed independent authorship, a public
repository and immutable revision, installed-wheel execution, exact headless/
command-receipt/replay capability evidence, distinct source/run/review
identities, and reviewed public licensing. The reviewed set is empty, so the
current count remains zero; bundled examples, maintainers, agents, CI, and
synthetic fixtures are not adoption. M28 adds no runtime source, API, protocol,
format, dependency, version, workflow job, network activity, author contact,
telemetry, tag, release, publication, certification, or support promise.
Both necessary eight-job hosted runs passed after correcting the two valid
review findings. PR #44 squash-integrated exact final evidence head
`c383a4f143fd8682059a89ff6b645104a6b4332d` as GitHub-verified `main` commit
`90d58a4567e7c7eaff90a28a7c59f2453b6d4538` with the exact final tree.

M29 starts from verified integrated `main` commit
`e4125bf31a751473d2af4fecc05a9744d551063c`. It adds an offline admission
harness for the next longer-term metric: contributor retention rather than raw
stars. A future record requires one independently reviewed external human to
complete two distinct merged public project contributions, with exact
issue/PR/revision/artifact identities, valid DCO, complete validation,
reviewed provenance, and a return merge later than the first. The reviewed set
is empty, so the current retained-contributor and return-contribution counts
remain zero; maintainers, agents, CI, popularity totals, and synthetic fixtures
are not retention. M29 adds no runtime source, API, protocol, format,
dependency, version, workflow job, network activity, contributor contact,
telemetry, tag, release, publication, certification, or support promise.
Initial hosted validation found one CPython 3.14 decoder-behavior assumption in
the excessive-nesting regression. The corrected evaluator applies an explicit
16-level structural JSON limit while ignoring strings and escapes. Correction
run `31183032073` passed all eight essential jobs, and PR #46 squash-integrated
the exact corrected tree as GitHub-verified `main` commit
`fc969a981ecdbbf842477f46486e29277119e05b`.

M30 starts from verified integrated `main` commit
`c88b166a39a793c91741bfa762af5627a87c53b4`. It adds an offline admission
harness for the next longer-term metric: installation success across the
supported OS/CPython matrix. A future record set requires one immutable public
pure-Python release wheel to pass clean isolated installation, version,
doctor, headless example, and Clockwork Arena checks in all seven practical
environments, with exact artifact/log identities and reviewed provenance. The
reviewed set is empty, so the current successful-environment count remains
zero; source-checkout CI, local builds, automation, and synthetic fixtures are
not released-user installation evidence. M30 adds no runtime source, API,
protocol, format, dependency, version, workflow job, network activity,
installation, tag, release, publication, certification, or support promise.
Ready PR #48 ran the unchanged essential CI topology on exact feature commit
`576dd070b547bef853ee47ece4c928b4e9962a7d`; run `31186083454` passed all
eight jobs. PR #48 then squash-integrated the exact feature tree as
GitHub-verified `main` commit
`675713d15a20a38233b80580e5aa773dc7a8684c`.

M31 starts from verified integrated `main` commit
`22dc58df8b0c4d17c3619d83e37c6d0ee6184441`. It adds an offline admission
harness for the next longer-term metric: issue-response and pull-request-review
time. A future window requires a complete reviewed public cohort of eligible
external-human issues and pull requests, preserves pending items, and binds
first qualifying human-maintainer actions to exact public evidence and
timestamp/latency agreement. The reviewed set is empty, so no latency aggregate
or SLA is claimed; automation, project history, and synthetic fixtures are not
human responsiveness evidence. M31 adds no runtime source, API, protocol,
format, dependency, version, workflow job, network activity, telemetry,
contributor contact, issue/PR mutation, tag, release, publication,
certification, stability change, SLA, or support promise.
Corrected head `dd4058b71439b5bade9d091831ba5453a51db35c` passed all eight
essential jobs in run `31190559197`; PR #50 squash-integrated the exact tree as
GitHub-verified `main` commit
`8adb8d46d0ce13ea3687856ae53e899e98dc42a6`.

M32 starts from verified integrated `main` commit
`b4de1d115ddb620ecddccab84637c0e66cfad9fd`. It adds an offline admission
harness for the next longer-term metric: replay-divergence rate in CI. A future
window requires a complete reviewed public cohort of eligible replay
executions, preserves cancellation, pre-replay failure, skipping, and missing
result evidence as `not-executed`, and binds verified/diverged outcomes to
exact public workflow, case, and frozen result evidence. The reviewed set is
empty, so no execution count or divergence rate is claimed; passing jobs and
synthetic fixtures are not historical rate evidence. M32 adds no runtime
source, API, replay protocol, format, dependency, version, workflow job,
network activity, telemetry, tag, release, publication, certification,
stability change, reliability target, or support promise.
Initial head `7046e59eb4840e6df492c886ce78baf4ad51cd95` passed all eight
essential jobs in run `31194645068`, but hosted review identified a mismatched
replay-divergence diagnostic. Corrected head
`f6f574c2e9b54341e77d1b9ba2d9268bffe5439a` uses and pins runtime code
`world.replay.diverged`, resolved the sole review thread, and passed all eight
essential jobs in run `31195402467`; PR #52 squash-integrated the exact tree as
GitHub-verified `main` commit
`36e8d9ed65a619569f3620b2431d977a1fb80a58`.

M33 starts from verified integrated M32 state-record commit
`60ddf57216d1054ac44df8d834756312c3864e3e`. It adds an offline admission
harness for the next longer-term metric: benchmark regression rate. A future
window requires a complete reviewed controlled cohort of paired base/head
M1-M4 `perf_counter_ns` workloads, exact p95 evidence, comparable frozen runner
profiles, and predeclared integer tolerances. Non-execution remains counted and
blocks publication. The reviewed set is empty, so no comparison count or
regression rate is claimed; local timings, M7 cProfile output, passing smokes,
and synthetic fixtures are not controlled historical rate evidence. M33 adds
no runtime or benchmark implementation, optimization, API, protocol, format,
dependency, lock, version, workflow job, telemetry, native boundary, tag,
release, publication, certification, performance target, or support promise.
Ready PR #54 exact head `3bd7e17eed26028592cb39d37e77e15c6f4371f1`
passed all eight essential jobs in run `31225942698`, had no review comment or
thread, and squash-integrated the exact tree as GitHub-verified `main` commit
`0993c73b3290809ef4e0c36d64d39e5ee5891a9b`.

M34 starts from verified M33 integration-record commit
`d12c30a02782c0ebf892e27c5daf6e9fec1c93ee`. It adds an offline admission
harness for the next longer-term metric: the percentage of agent tool calls
that complete without manual recovery. A future window requires a complete
reviewed cohort of task-directed sessions and every dispatched product-tool
call. Known failures and calls completed after recovery remain in the
denominator; `terminal-unobserved` remains counted and blocks publication. The
reviewed set is empty, so no call count or recovery-free completion rate is
claimed; examples, conformance profiles, tests, maintainer-invoked calls, and
synthetic fixtures are not operational history. M34 adds no runtime or agent
implementation, API, protocol, format, dependency, lock, version, telemetry,
provider, release, publication, certification, reliability target, or support
promise. It retains the eight essential CI jobs but runs them once per
substantive pull request, not again after merge or for `.project/**`-only
records.

M35 starts from verified M34 integration-record commit
`277de9052e768a5f70d32f1a2f67ec9f93353723`. It adds an offline admission
harness for the design plan's final ordered longer-term metric: the number of
independently authored third-party adapters or plugin-backed adapters passing
existing installed conformance profiles. The exact reviewed manifest asserts
that the complete project-accepted submission census was reviewed and contains
no submissions, so the current count is zero and no support, certification,
security, performance, ecosystem, or global package-census result is claimed.
Future records must preserve passed, failed, and not-executed outcomes and
complete accepted history. Project-owned and maintainer-authored references
never count. A compatible M12 render-device manifest is necessary for a
plugin-backed record but is never sufficient without a passing installed M17
profile. M35 adds no discovery, installation, provider execution, network,
telemetry, runtime/API/protocol/profile, dependency, lock, version, workflow
job, release, publication, or support-policy change.

M36 starts from verified M35 integration-record commit
`ba9125389ab2b2b760ca7115b5b1b03c447f4190`. It preserves the exact eight
validation slices exercised by corrected M35 run `31231410432` while grouping
them into one Ubuntu allocation and one allocation each for Windows and macOS.
The Ubuntu runner owns quality/distribution, 3.12 graphics, and sequential
3.13/3.14 compatibility. Each desktop runner owns 3.12 graphics followed by
3.14 compatibility. The structural change removes five runner allocations and
five repeated checkout/setup sequences without removing a Python, platform,
graphics, package, installed-wheel, release, docs, or static-analysis slice.
It retains PR-only and `.project/**` exclusions, least privilege, exact pins,
caching, timeouts, fail-fast isolation across desktop OSes, and cancellation of
superseded runs. M36 changes no runtime, API, protocol, format, dependency,
lock, version, release workflow, tag, publication, or support policy.

M37 starts from verified M36 integration-record commit
`46ef98447706c94763a236841a38c2dbb5b444ca`. It keeps the pull-request workflow
visible while using the exact base-revision classifier to distinguish a narrow
documentation-only path set from substantive work. Documentation-only changes
retain one Linux lock/static/docs/architecture/build/wheel/release allocation.
Substantive and indeterminate changes retain or fail into the complete three-
allocation M36 gate, and Windows/macOS wait for successful Linux qualification.
M37 changes no runtime, test behavior, dependency, lock, package version,
release workflow, tag, publication, or support policy.

PR #62 is squash-integrated as
`407226beae36182d237e32866a86ce19bb93c691`. Corrected substantive run
`31259200818` passed exact reviewed head
`8214227c99831310546147977bf354b5ae956bce` in three allocations: Linux passed
before Windows and macOS were allocated, and all three completed successfully.
The public integration record is intentionally composed only of paths admitted
by the trusted base classifier so its pull request can verify the bounded
one-allocation documentation lane without spending desktop allocations. That
record's hosted result is not pre-claimed here.

M38 starts from verified M37 closeout commit
`3578da64b2686cd8d63340aeb1eed30f5c4cb761`. It turns observed Hatch build
reproducibility into an executable project gate: the existing Linux CI and tag-
release distribution steps each build twice and reject any filename, artifact-
set, portability, or byte mismatch before smoke, staging, attestation, or
publication. The comparison consumes no additional runner allocation and
claims neither cross-platform/independent reproducibility nor provenance.

PR #65 corrected symlink-cycle failure handling and passed exact final head
`4f3db7446c842df4f36d7cc8f8321a89bbe5997f` in run `31261807768`. Linux
completed in 6m50s before the desktop allocations began; macOS passed in 1m59s
and Windows in 3m44s. Squash `9f6ca61ccb1f9b7e0796e5cc60c7dd38e6af99d7`
has the exact reviewed tree, a valid GitHub signature, and a DCO trailer. No
post-merge main run was allocated and the feature branch is deleted.

M39 starts from verified M38 closeout commit
`185e206d6b9c1e97512e289bcba84701dc29c147`. It closes the gap between remote
tag existence and release identity: the existing tag job must verify an
annotated GitHub-valid signature, exact event/checkout/tag-object commit, and
`origin/main` ancestry before system setup, tests, builds, attestations, or
publication. The check adds no hosted allocation, action, permission, trigger,
dependency, tag, release, key allowlist, or publication authority.

PR #68 passed exact head `f71d8ddbf816873cf9af8ea6538112ff0e75553e` in run
`31264314307` with exactly three allocations. Linux completed in 6m43s before
the desktop jobs began; macOS passed in 2m33s and Windows in 3m30s. The Linux
job built a 267,110-byte wheel at SHA-256
`b09d2727d39ae8b750f6aa9f13035cad34477d287eab07eb5ee52341221cd02a`
and a 906,680-byte sdist at SHA-256
`ef6e4fbf6f05d664a0311249c46106b0001b949a16373025dec171e60cca4314`,
then passed the complete ten-artifact release-candidate smoke. No review,
comment, or review thread was present. Squash
`4e30b4bf3b911270ab4e1bd117d49ca0d090a0a7` has sole parent the exact M38
closeout, tree `e08a1956e1b6ec9005b1455c5020ee716f6fbdef` exactly equal to the
reviewed head, a valid GitHub signature, and a standalone DCO trailer. No
post-merge `main` run was allocated, and the feature branch is deleted locally
and remotely.

M40 starts from verified M39 closeout commit
`49fba13477890bf6bf1c9e6a645e669b3a69492f`. It makes the existing release
CLI's internal draft/upload/publish ordering explicit and adds a bounded local
validator for the authenticated GitHub draft document. Publication may proceed
only when the exact tag/title/state and every uploaded asset name, size, and
SHA-256 digest match local staging. The slice adds no runner, action,
permission, trigger, dependency, tag, release, credential, or publication
authority and does not enable the separate immutable-release repository setting.

PR #71 corrected a review finding so pathological JSON nesting and overlong
integers also fail through the structured validator contract. Corrected head
`967147b3bbc83414d0ce303845975dea0c4e9d26` passed exactly three hosted
allocations, then squash-integrated as
`e9d9850e11f572a1d4ddc78d06c79b23a5584f87`. The squash tree exactly matches
the reviewed head, its sole parent is the M39 closeout, its GitHub signature and
DCO trailer are valid, no `main` run was allocated, and the feature branch is
deleted locally and remotely.

M41 starts from verified M40 closeout commit
`9983e0da88b6aef999d26498cc6438f0b3c5927b`. It advances the internal draft
validator to protocol `/2` and requires the authenticated release `body` to
exactly equal the bounded non-empty UTF-8 `RELEASE_NOTES.md` already supplied
through `--notes-file`. The slice logs no note content and changes no workflow,
runner, action, permission, trigger, dependency, tag, release, credential,
publication authority, or immutable-release setting.

M42 starts from verified M41 closeout commit
`0dec2254a9d9483b27d158aaad108340e9c94e28`. It advances the internal release
validator to protocol `/3`, makes expected draft/published state explicit, and
rechecks the same numeric release ID after `gh release edit --draft=false`.
The published observation requires an exact public prerelease state, valid UTC
publication time, and unchanged notes/assets. It adds one read-only API request
inside the existing tag job but no runner, action, permission, trigger,
dependency, credential, tag, release, upload, automatic rollback, immutable-
release setting, or publication authority.

M43 starts from verified M42 closeout commit
`2ed26ebc5e5a388a02ddd1ae0fd8114f4c3e1e79`. It advances the internal release
validator to protocol `/4`, requires unique bounded numeric asset IDs, and can
write one exclusive published-only retrieval plan after complete verification.
The existing tag job retrieves each exact ID through the authenticated asset
API and rehashes the downloaded directory against the same published document.
It adds no runner, action, permission, trigger, dependency, credential, tag,
release, upload, rollback, cleanup, immutable-release setting, or publication
authority, and makes no unauthenticated/global/future availability claim.

Corrected PR #80 head `3a5004217598c82eca5b8286442e7d8a502642b1`
passed run `31274622529` in exactly three allocations: Linux in 7m13s before
desktop allocation, macOS in 1m48s, and Windows in 3m53s. The sole P2 review
thread was resolved after the bounded-stream correction. Squash
`8b7038cc203cead16d1dd88c746b584b6d0c37ca` has the exact reviewed tree, sole
parent the M42 closeout, a valid GitHub signature, and a standalone DCO trailer.
No post-merge `main` run was allocated, and the feature branch is deleted.

M44 starts from verified M43 closeout commit
`0b3b9eb982a67eee1833f3a8f920671f8ffd006b`. It consumes the bounded M43 plan
and exact downloaded subject set after publication, requiring SLSA v1
provenance for every asset and an SPDX 2.3 SBOM attestation for the one pure
wheel under exact repository, workflow, tag, source/signer commit, issuer, and
hosted-runner policy. It adds no runner, action, permission, trigger,
dependency, credential, tag, release, upload, publication, rollback, cleanup,
runtime, package, or public-API change. A real attestation pass remains
unclaimed until an authorized signed-tag release run executes.

PR #83 exact head `494ae4f32209c8e679633d528bb63cf4b1093800`
passed run `31277236908` in exactly three allocations: Linux in 7m04s before
desktop allocation, macOS in 2m35s, and Windows in 3m50s. One automated P1
predicate-URI suggestion was disproved by the exact pinned action source and
official GitHub documentation, answered, and resolved without code change.
Squash `781ca0d1692b309ca3dd7ea9ca8dc6af88f77b09` has the exact reviewed
tree, sole parent the M43 closeout, a valid GitHub signature, and a standalone
DCO trailer. No post-merge `main` run was allocated, and the feature branch is
deleted.

M45 starts from verified M44 closeout commit
`2c5e312a97028d0b835fc174b8abb51df22ea314`. It follows M44 with one
credential-free observation of the exact public release ID and every exact M43
asset ID through fixed HTTPS GitHub API endpoints. The same bounded validators
recheck public metadata and bytes before the existing complete release smoke
installs the wheel and runs bundled scenarios. It adds no job, runner, action,
permission, trigger, dependency, credential, tag, release, upload,
publication, rollback, cleanup, runtime, package, or public-API change. A real
public-path pass remains unclaimed until an authorized signed-tag release run
executes.

M46 starts from verified M45 closeout commit
`086f1ceb3974583ce7a2c386c67f516299c2f1dd`. It extracts M45's bounded
public retrieval into a shared script and adds one dependent read-only Linux
job after successful publication. The fresh runner retrieves the exact
candidate preserved by the same workflow, creates its own plan, revalidates
public bytes, and runs installed release smoke. It adds one tag-only runner and
one pinned download action but no pull-request CI allocation, release mutation,
publication authority, artifact-set, dependency, runtime, package, or public-
API change. Same-workflow rehearsal is not independent/external or cross-
platform evidence; a real pass remains unclaimed until an authorized signed-
tag run.

PR #89 corrected Bash 3.2 reuse-mode portability after the first hosted run
blocked on macOS. Corrected run `31283211266` passed the exact three-allocation
gate, including the macOS regression, complete compatibility, real-wgpu
profiles/samples, reproducible distribution, installed wheel, and release
smoke. Verified squash `d4cb4410d1dd9f684d3b169932ea3251801d3884`
has the exact reviewed tree, sole M45-closeout parent, valid signature, and DCO;
no post-merge run was allocated and the feature branch is deleted.

M47 starts from verified M46 closeout commit
`2d27b139c6bf4a130ca97e7f0b518f6ebfe191c5`. It replaces the internal
Bash public-release verifier with one typed standard-library Python program and
expands the existing tag-only fresh-consumer job to Ubuntu, Windows, and macOS.
Every fresh runner receives only the verified release ID/version and exact
same-workflow candidate, creates its own bounded plan, fetches exact public
bytes without a release credential, and runs complete installed release smoke.
The slice adds two tag-only allocations but no pull-request allocation,
credential, trigger, release mutation, publication authority, artifact,
dependency, runtime, package, or public-API change. Same-workflow cross-platform
evidence is not independent/external verification; a real pass remains
unclaimed until an authorized signed-tag release run executes.

PR #92 exact head `fdddaa986b647e68a0a027445c11547b878ad246` passed run
`31286321895` in exactly three allocations: Linux qualified first in 7m20s,
then macOS passed in 2m40s and Windows in 3m55s. The PR had no review, comment,
or thread. Verified squash `c3f5d9c4b9f21315b7ae8f113cc643f978d75746`
has exact reviewed tree `e222ebff0655b9d86548bab6e8d19fb79ba3afc5`,
sole parent the M46 closeout, valid GitHub signature, and standalone DCO. No
post-merge run was allocated, the feature branch is deleted, and no real tag or
release was created.

M48 starts from verified M47 closeout commit
`8d8d9e4a5790d7b74ec06139d314ffdf30a4ef41`. It narrows the portable public
release client to a direct `200` release document and either direct `200` or at
most three bounded `302` asset responses. Other redirects fail closed;
`X-GitHub-Api-Version` remains on `api.github.com`. Socket deadlines are
refreshed before response headers and body reads, with stable distinct codes for
timeouts, other transport/protocol failures, and local-output failures.

The slice changes no workflow, runner allocation, action, permission,
credential, trigger, release mutation, retry, cleanup, dependency, runtime,
package, or public API. Fixture and pull-request evidence are not a real public
release observation, independent/external verification, future availability,
immutability, artifact security, PyPI, or a supported release channel. A real
pass remains unclaimed until an authorized signed-tag release run executes.

PR #95 exact head `9b5c533d1e73ee985945fa0feb7e876417ee0126`
passed run `31288303182` in exactly three allocations: Linux qualified first in
415 seconds, then macOS passed in 118 seconds and Windows in 228 seconds. The
PR had no review, comment, or thread. Verified squash
`c32ff1bf71b53278ef2ff616c2fc3cfce5cf20a3` has exact reviewed tree
`1986f691633d94a5b980c2be0b7e1d0b364de37e`, sole parent the M47 closeout,
valid GitHub signature, and standalone DCO. No post-merge run was allocated,
the feature branch is deleted, and no real tag or release was created.

M49 starts from verified M48 closeout commit
`049cdbcf2769a1c2359593f642e37697d5bf7400`. It explicitly connects each
fixed API or redirected asset hop and validates the actual port-443 TLS socket
peer before transmitting HTTP. IPv4-mapped IPv6 is classified by its embedded
address; only globally reachable unicast IPv4/IPv6 is accepted. Non-global
peers fail with a stable content-silent code, while timeout and malformed peer
inspection preserve M48's request taxonomy.

The slice adds no hostname/IP allowlist, separate DNS preflight, workflow,
runner allocation, action, permission, credential, trigger, release mutation,
retry, cleanup, dependency, runtime, package, or public API. Fixture and
pull-request evidence are not a real public release observation, network
sandbox, independent/external verification, every delivery path, future
availability, immutability, artifact security, PyPI, or a supported channel. A
real pass remains unclaimed until an authorized signed-tag release run executes.

Initial PR #98 passed its exact three-allocation gate but remained unmerged
after hosted review identified that supported CPython could classify deprecated
IPv6 site-local and reserved peers as global. The replacement explicitly
rejects both classifications and adds the reported ranges as regressions.

Replacement PR #99 exact head
`01c955f0256c0c6e3a34afaf317c828e439b87ca` passed run `31307775820` in
exactly three allocations: Linux first in 422 seconds, then macOS in 143
seconds and Windows in 230 seconds. The PR was clean and mergeable with no
review, comment, or thread. GitHub-verified squash
`842aedc67a7ae4584821c4d8bc96a4ed8cb334c3` has reviewed tree
`a9755cbf65dfeba5087f5037f73bc6027c408444`, sole parent the M48 closeout,
valid signature, and standalone DCO. No post-merge run was allocated, the
feature branch is deleted, and no real tag or release was created.

M50 starts from verified M49 closeout commit
`f6214992b02a9ef0bc44d6a9e4e6d72dc9d33de0`. It replaces the portable public
verifier's ambient-sensitive default-context helper with a new explicit
verified client context per fixed API or redirected asset hop. System
server-auth roots, certificate and hostname validation, TLS 1.2 or newer, and
strict/partial-chain X.509 verification remain mandatory. Ambient
`SSLKEYLOGFILE` must remain untouched and may neither enable key logging nor
create its target. Context construction or invariant failure uses a stable,
content-silent code.

The slice adds no custom trust store, certificate/SPKI pin, client certificate,
proxy, workflow, runner allocation, action, permission, credential, trigger,
release mutation, retry, cleanup, dependency, runtime, package, or public API.
Fixture and pull-request evidence are not a real public release observation,
negotiated-session audit, independent/external verification, every delivery
path, future availability, immutability, artifact security, PyPI, or a
supported channel. A real pass remains unclaimed until an authorized signed-tag
release run executes.

Ready PR #102 exact head
`99134b6be68bb7978431710228e788250561659e` passed run `31309759226` in
exactly three allocations: Linux first in 7m43s, then macOS in 2m08s and
Windows in 3m01s. The PR was clean and mergeable with no review, comment, or
thread. GitHub-verified squash
`5fb56120e1a96a0a25db96baa3836699e435611c` has reviewed tree
`2ec52b638069d23aabd68af04f3ada426aab803d`, sole parent the M49 closeout,
valid signature, and standalone DCO. No post-merge run was allocated, the
feature branch is deleted, and no real tag or release was created.

M51 starts from verified M50 closeout commit
`53f3804010f1556ecaff21a61b1e9c405a26e203`. It advertises only HTTP/1.1 and,
after connected-peer confinement but before HTTP transmission, validates the
actual negotiated TLS version, cipher report, compression, and ALPN on every
fixed API or redirected asset hop. The accepted session is exactly TLSv1.2 or
TLSv1.3, at least 128 reported secret bits, no compression, and ALPN
`http/1.1` or no negotiated ALPN. Failures remain content-silent under
`public_release.tls_failed`.

The slice adds no cipher-name allowlist, custom trust, certificate/SPKI pin,
revocation policy, TLS fingerprint, workflow, runner allocation, action,
permission, credential, trigger, release mutation, retry, cleanup, dependency,
runtime, package, or public API. Fixture and pull-request evidence are not a
real public release observation, independent/external verification, every
delivery path, future availability, immutability, artifact security, PyPI, or
a supported channel. A real pass remains unclaimed until an authorized signed-
tag release run executes.

Corrected PR #105 head `a0612236aa13c2892fd95e55c2a77286d21572d4`
passed run `31312987430` in exactly three allocations: Linux first in 7m16s,
then macOS in 2m02s and Windows in 3m55s. The initial green head was not merged
because review found an unhashable malformed-version escape; the corrected
head added string guarding plus sequence/mapping regressions and the sole
thread was resolved. GitHub-verified squash
`ce4184b4ecedd9163a654cc96ae6c96086683760` has reviewed tree
`c331ea93e5332b47a3df20906dfb6f6e77c6cdb3`, sole parent the M50 closeout,
valid signature, and standalone DCO. No post-merge run was allocated, the
feature branch is deleted, and no real tag or release was created.

M52 starts from verified M51 closeout commit
`047478d0c7fb873ae94aaa6e322b5b08903ed354`. After connected-peer confinement
and before negotiated-session inspection or HTTP transmission, it normalizes
the current URL hostname with built-in IDNA, requires the actual socket's
reference hostname to match case-insensitively, and requires a non-empty DER
peer certificate on every fixed API or redirected asset hop. The existing M50
verified context remains authoritative for certificate-path, validity, and
hostname matching. Failures remain content-silent under
`public_release.tls_failed`.

The slice adds no certificate parser/export, custom trust, certificate/SPKI
pin, fingerprint allowlist, revocation/OCSP/CRL/CT policy, DNSSEC, workflow,
runner allocation, action, permission, credential, trigger, release mutation,
retry, cleanup, dependency, runtime, package, or public API. Fixture and pull-
request evidence are not a real public release observation, independent or
external verification, every TLS/CDN path, future availability, immutability,
artifact security, PyPI, or a supported channel. A real pass remains unclaimed
until an authorized signed-tag release run executes.

Feature PR #108 exact head `170db846112e27b9d11377da69784c69a6565bb4`
passed run `31316474864` in exactly three Linux-first allocations, including
all supported-Python, graphics, profile, vertical-slice, reproducible-build,
installed-wheel, and release-smoke gates. A delayed review audit found no
review, comment, or thread. GitHub-verified squash
`eb083089bfff774c0df2b115428901357c9084b2` has the exact reviewed tree, the
M51 closeout as sole parent, valid signature, and standalone DCO. No post-merge
run was allocated, the feature branch is deleted, and no real tag or release
was created.

M53 starts from verified M52 closeout commit
`8d69f5b265277edb95ae47ea3a0af001217a4575`. After the handshake and M49
connected-peer confinement, but before M52 service-identity evidence, M51
negotiated-session inspection, or HTTP transmission, it requires the actual
socket to retain the exact context object supplied for that hop and an exactly
client-side role. It then revalidates the complete M50 context policy. Every
redirect owns and checks an independent exact context.

The slice adds no trust replacement, pinning, certificate/chain parser,
revocation, TLS-session reuse, channel binding, proxy, network sandbox,
workflow, runner allocation, action, permission, credential, trigger, release
mutation, retry, cleanup, dependency, runtime, package, or public API. Fixture
and pull-request evidence are not a real public release observation,
independent or external verification, every TLS/CDN path, future availability,
immutability, artifact security, PyPI, or a supported channel. A real pass
remains unclaimed until an authorized signed-tag release run executes.

M54 starts from verified M53 closeout commit
`fe585f8bd2313feac39b70cadf088c57bbb1960e`. After the handshake, M49
connected-peer confinement, and M53 exact context binding, but before M52
service-identity evidence, M51 negotiated-session inspection, or HTTP
transmission, it requires the actual socket's `session_reused` observation to
be exactly `False`. Every redirect repeats that freshness check independently.

The slice adds no session cache, session assignment, ticket control, custom TLS
implementation, trust replacement, pinning, certificate/chain parser,
revocation, channel binding, proxy, network sandbox, workflow, runner
allocation, action, permission, credential, trigger, release mutation, retry,
cleanup, dependency, runtime, package, or public API. The implementation's
reported non-reuse state does not independently prove a full handshake or
certificate exchange. Fixture and pull-request evidence are not a real public
release observation, independent or external verification, every TLS/CDN path,
future availability, immutability, artifact security, PyPI, or a supported
channel. A real pass remains unclaimed until an authorized signed-tag release
run executes.

Feature PR #114 exact head `d5d02a38ea302c0e314f966376e267c45508d14b`
passed run `31321661693` in exactly three Linux-first allocations, including
all supported-Python, graphics, profile, vertical-slice, reproducible-build,
installed-wheel, and release-smoke gates. Delayed review found no review,
comment, or thread. GitHub-verified squash
`c333f2b9aad98b9a55d986076fe8b09153d30762` has the exact reviewed tree, the
M53 closeout as sole parent, valid signature, and standalone DCO. No post-merge
run was allocated, the feature branch is deleted, and no real tag or release
was created.

M55 starts from verified M54 closeout commit
`aab15d601eb4402213f2e058f270237b964f1000`. After all connected-peer and TLS
checks and `getresponse()`, but before response status, redirect, or body use,
it requires documented HTTP/1.1-class integer version value `11`, permits
absent or case-insensitive exact `chunked` `Transfer-Encoding`, rejects its coexistence with
`Content-Length`, and requires any content length to be a string before the
existing bounded syntax and exact-size checks. Every redirect repeats the
framing validation independently.

CPython may normalize another raw `HTTP/1.x` status-line token into public
value `11`; the slice therefore does not claim exact wire-token identity and
does not add private parser introspection to manufacture that evidence.

The slice adds no private response-state dependency, raw HTTP/chunk parser,
alternate client, HTTP/2 or HTTP/3, proxy, decompression, retry, cache, network
sandbox, workflow, runner allocation, action, permission, credential, trigger,
release mutation, dependency, runtime, package, or public API. Fixture and
pull-request evidence are not a real public release observation, general
request-smuggling protection, independent/external verification, every
intermediary or delivery path, future availability, immutability, artifact
security, PyPI, or a supported channel. A real pass remains unclaimed until an
authorized signed-tag release run executes.

M56 starts from verified M55 closeout commit
`e7f700454adf1c11c80cb1ba684ed3318f7876e4`. After M55 framing and before
comparison, redirect resolution, or body use, every response status must be a
non-boolean integer from 100 through 599. Every followed `302` must expose
exactly one Location field through the documented header-pair list. Its value
must be a single 1-to-8,000-octet ASCII URI-reference using valid RFC 3986
characters and complete percent escapes. The resolved URL must pass the
existing bounded HTTPS policy before the next request. Bracket delimiters are
valid only inside a parsed authority, not its path, query, or fragment.

Relative and cross-host absolute references remain supported, so every hop
repeats M49-M55 peer, TLS, framing, deadline, size, and exact-byte checks. The
slice adds no host allowlist, private response state, raw HTTP/URI parser,
alternate client, proxy, DNS preflight, network sandbox, workflow, runner
allocation, action, permission, credential, release mutation, dependency,
runtime package, public API, or release authority. Fixture and pull-request
evidence are not a real public release observation or a general SSRF defense.
A real pass remains unclaimed until an authorized signed-tag release run
executes.

M57 exact head `f7347965d7e9a78218fa08a34f76aed7d32ba67d` passed run
`31332655171` in exactly three Linux-first allocations. Linux passed in 5m37s
before macOS and Windows began; they passed in 1m51s and 3m48s. Hosted tests,
real graphics, profiles, both vertical slices, reproducible builds, installed-
wheel smoke, and complete release smoke passed. Two delayed audits found no
comment, review, or thread. GitHub-verified squash
`800050c74530d74a72338b5d444ee4751c5ad155` has the exact reviewed tree, sole
parent M56 closeout, standalone DCO, and no workflow, dependency, runtime
package, public API, or release-authority change. The feature branch is deleted
locally/remotely; the four-file integration record requires one Linux
documentation allocation and a zero-step skipped desktop umbrella.

M56 PR #120 corrected one delayed review finding by rejecting bracket
delimiters in path, query, and fragment components while retaining valid
bracketed IPv6 authorities. Corrected exact head
`35b94a42b10cbd8f75048d3200e95a4aca81fa5d` passed exactly three Linux-first
hosted allocations. GitHub-verified squash
`22c432310fae2f9ac372062cbd465cc2617fb95c` has the exact corrected feature
tree, sole parent M55 closeout, standalone DCO, and no workflow, dependency,
runtime package, public API, or release-authority change. The feature branch
was deleted locally/remotely; at feature integration, the remaining four-file
record required one Linux documentation allocation and a zero-step skipped
desktop umbrella.

That M56 integration record subsequently passed run `31330464522` in one
38-second Linux allocation while the desktop umbrella skipped with zero steps.
GitHub-verified record squash `acc6893ef4cadf9a17c87cd578e38b7802a3ed77`
and closeout squash `187cbfb1c857e62594e49d1cf8e7591024aff8c9` preserve exact reviewed trees,
standalone DCO, and no workflow or release-authority change. Only `main`
remained after closeout.

M57 starts from verified M56 closeout commit
`187cbfb1c857e62594e49d1cf8e7591024aff8c9`. Each successful response-body
read must return immutable bytes no larger than the requested amount before
EOF handling, byte accounting, or local output. If M55 exposed a valid
`Content-Length`, the declaration must equal the total streamed octets for the
release document and each final asset response. Existing expected asset sizes
remain independently enforced.

The slice adds no private response/socket state, raw HTTP/chunk parser,
content decoder, alternate client, cleanup, proxy, DNS preflight, network
sandbox, workflow, runner allocation, action, permission, credential, release
mutation, dependency, runtime package, public API, or release authority. It
makes no general completeness claim for unframed close-delimited responses.
Fixture and pull-request evidence are not a real public release observation.
A real pass remains unclaimed until an authorized signed-tag release run
executes.

M58 starts from verified M57 closeout commit
`26826822547d6d8df6ce1bfc05d8cf728a32d505`. Every obtained response receives
one response close attempt before its created connection receives one
connection close attempt. Both close attempts occur when response close fails.
An active primary failure remains primary; cleanup-only ordinary failures use
content-silent `public_release.request_failed`, and cleanup control signals
remain unwrapped.

Successful cleanup occurs before redirect continuation and before partial
publication from a separate asset partial path. The slice adds no rollback,
retry, private response/socket state, raw parser, alternate client, workflow,
runner allocation, action, permission, credential, release mutation,
dependency, runtime package, public API, or release authority. Fixture and
pull-request evidence are not a real public release observation. A real pass
remains unclaimed until an authorized signed-tag release run executes.

M58 exact head `8bd11f0ab6575edee6a5e7b5c78e36af59e55088` passed run
`31478254138` in exactly three Linux-first allocations. Linux passed in 7m48s
before macOS and Windows began; they passed in 2m00s and 4m01s. Hosted tests,
real graphics, profiles, both vertical slices, reproducible builds, installed-
wheel smoke, and complete release smoke passed. Two delayed audits found no
comment, review, or thread. GitHub-verified squash
`17ea7354c80b9d140350b88cd0ae3e615f700e45` has the exact reviewed tree, sole
parent M57 closeout, standalone DCO, and no workflow, dependency, runtime
package, public API, or release-authority change. The feature branch is deleted
locally/remotely; the four-file integration record requires one Linux
documentation allocation and a zero-step skipped desktop umbrella.

M59 starts from verified M58 closeout
`d4487565d4fda57ec05437dfcadc687d2507dafa`. It replaces one legacy fixture
identity, redacts retired labels from current maintenance records, and
centralizes the absent-root and tracked-text convention in one architecture
test. Immutable Git history, commit/PR/workflow/artifact evidence, product-
facing agent language, runtime source, public protocols, workflows,
dependencies, version, and release authority remain unchanged.

M59 corrected exact head `28e80e66eb16656a998353627ef78a8fe6e4c80b`
passed run `31484028669` in exactly three Linux-first allocations. Linux passed
in 6m05s before macOS and Windows began; they passed in 2m53s and 4m08s. The
valid dangling-root-link P2 was corrected tests-first, answered, and resolved;
two delayed audits found no unresolved or later review activity. GitHub-
verified squash `f12f65ab7c1f8426b0232bb4b414e48276bbad56` has the exact
corrected tree, sole parent M58 closeout, standalone DCO, and no runtime,
workflow, dependency, version, or release-authority change. The feature branch
is deleted locally/remotely; the four-file integration record requires one
Linux documentation allocation and a zero-step skipped desktop umbrella.

M60 starts from verified M59 closeout
`9ba74e55b5c47d5f0bd030b53ad6a35a361c5735`. It treats any pre-existing final
directory entry for fresh release output or plan paths as a filesystem
collision before network or validator work, while retaining exclusive creation
and no clobber publication. No workflow, dependency, version, runtime API,
release authority, tag, release, or publication changes.

## M119 data-only scene transaction planning

M119 starts from fully locally validated M118 commit
`7b68f3d02987ee9824785c1699592c4670dbe267`. It adds the first deliberately
bounded scene-authoring contract: a versioned data-only scene document with
stable local IDs, unique names, optional local parent references, versioned
component records, and canonical `asset://` dependencies.

The compiler resolves component names only through an explicit immutable
`ComponentRegistry`, validates or migrates all values before mutation, adds one
compiler-owned `SceneNode` provenance component, and emits ordinary
`entity.spawn` commands in one atomic transaction. Receipt aliases provide the
local-ID-to-runtime-entity mapping after application. Canonical runtime state
remains in the world store; the scene document is input data, never a parallel
authority.

The slice has no file I/O, no prefab inheritance, no live scene update or
reimport behavior, no `EntityRef` facade, no arbitrary Python graph or import,
no renderer or tool dependency, no runtime dependency, and no workflow or
hosted runner change. M120 supplies the separately bounded one-level prefab
fragment planning contract.

## M120 one-level prefab fragment planning

M120 starts from fully locally validated M119 commit
`b30ca99c3ae639653394a378465c0088ee5c2995`. It adds exact
`ludoweave.prefab/1` scene fragments and `ludoweave.prefab-instance/1`
instance requests. Stable local IDs, names, parent DAGs, component values, and
`asset://` dependencies reuse the M119 document invariants. Instance overrides
are canonically ordered non-empty current-schema field replacements against an
existing local entity/component pair.

The planner validates the fragment and all schema-aware overrides before it
adds compiler-owned `PrefabNode` provenance and delegates to M119. The result
is ordinary `entity.spawn` commands in one existing atomic transaction;
receipt aliases return the local-ID-to-runtime-entity mapping. Canonical
runtime state remains in the world store, and source changes never silently
propagate into an already instantiated world.

The slice is deliberately one-level. It has no nested prefab inheritance or
variant chain, parameter expression, component/entity add or remove override,
file I/O, asset loading, live update, reimport, source write-back, runtime link
graph, new persistent operation, dependency, root API, workflow, or hosted
runner change.

## M121 project-confined scene file loading

M121 starts from fully locally validated M120 commit
`dbe8108abc29c93aed4317456ee67efb8b99e1ea`. The existing
`HeadlessProject` composition root gains one typed `load_scene()` method. It
accepts one bounded project-relative path and exact `SceneLimits`, reuses the
established path confinement and bounded handle read, and delegates the
detached bytes to the unchanged `ludoweave.scene/1` decoder.

Loading is synchronous and returns a detached immutable scene document. It
owns no persistent handle, cache, watcher, world, renderer, or background
resource. The load performs no world mutation; later explicit scene planning
and existing transaction application remain the only instantiation path and
produce the receipt. Asset dependencies remain logical `asset://` identities
and are not loaded.

The slice has no directory discovery, prefab file loader, file URI handling,
include/import graph, arbitrary Python import/evaluation, source cache, watch,
live update, reimport, write-back, remote access, new persistent operation,
dependency, root API, workflow, or hosted runner change. Project confinement is
not a race-free filesystem sandbox against concurrent hostile mutation.

## M122 project-confined prefab file loading

M122 starts from fully locally validated M121 commit
`18d1571badc416801151b6f5df67e3cfcef78ba1`. The existing `HeadlessProject`
composition root gains `load_prefab()` and `load_prefab_instance()`. Each
accepts one bounded project-relative path plus exact `PrefabLimits`, reuses the
M121 confinement and bounded read, and delegates detached bytes to the existing
`ludoweave.prefab/1` or `ludoweave.prefab-instance/1` decoder.

The caller supplies two explicit files. There is no implicit pairing:
`compile_prefab()` still validates the exact `prefab_id` relationship after
both detached records have loaded. A load performs no world mutation and owns
no persistent file handle. Existing explicit compilation and transaction
application remain the only instantiation path and receipt boundary.

The slice has no directory discovery, extension routing, manifest lookup,
include/import graph, asset loading, cache, watcher, live update, reimport,
source write-back, nested prefab composition, remote access, new persistent
operation, dependency, root API, workflow, or hosted runner change. Project
confinement remains a cooperative local-project boundary, not a race-free
filesystem sandbox.

## M123 read-only source-check CLI

M123 starts from fully locally validated M122 commit
`176c21d12adc00c71cab63a777d0cd0eb6d66215`. The existing standard-library CLI
gains one nested `ludoweave source check` workflow. Callers select either one
project-confined scene file or two explicit files for a prefab source and
instance. Successful checks emit canonical `ludoweave.cli.source-check/1` JSON
with protocol identities, stable source IDs, canonical SHA-256 identities, and
bounded entity/dependency/override counts.

The command performs structural protocol preflight only. It creates no world or
session, resolves no application component schema or asset, invokes no planner,
performs no compile and no world mutation, and therefore produces no receipt. Prefab
mode does enforce exact source/instance `prefab_id` agreement. Failures retain
the established exit-2 and sanitized structured CLI error behavior.

M123 has no directory discovery, implicit pairing, extension routing, manifest
lookup, source cache, watcher, live update, write-back, remote access, arbitrary
script execution, component semantic validation, dependency, root API, version,
or workflow allocation change. The existing consolidated CI topology is
unchanged.

## M124 explicit source-manifest checking

M124 starts from fully locally validated M123 commit
`1b092a85487b355fac688e15daeaed0ebcfa665a`. It adds bounded
`ludoweave.source-manifest/1` values with one stable manifest ID and a nonempty,
canonically ordered list of explicit entries. Each entry names either one
normalized project-relative scene file or one exact prefab source/instance
pair. Entry IDs and exact source references are unique, and callers may tighten
the hard byte, entry-count, and path limits.

`ludoweave source check PROJECT --manifest FILE` loads the confined manifest,
then checks every listed file through the unchanged M121/M122 readers. Success
emits one path-silent canonical `ludoweave.cli.source-manifest-check/1` report
with manifest/source identities, normalized SHA-256 values, per-entry results,
and bounded aggregate counts. Any entry failure emits no success report and
leaves the project tree unchanged.

The explicit manifest is not directory discovery, a registry, or an import
database. M124 performs no compile, component semantic validation, asset load,
world/session creation, command, transaction, world mutation, or receipt. It
adds no glob/recursion, implicit pairing, cache, watcher, live update,
write-back, remote access, dependency, root-package API, version, workflow job,
or hosted allocation. Multiple filesystem reads are not an atomic snapshot;
deterministic output assumes stable inputs for the duration of the check.

## M125 source-integrity lock verification

M125 starts from fully locally validated M124 commit
`c73242b29325977484df271a107287d688fbdb54`. It adds bounded immutable
`ludoweave.source-lock/1` values. One lock binds the normalized manifest ID and
canonical SHA-256 identity plus an entry-ID-ordered list of accepted source
protocols, stable IDs, and canonical content identities. Prefab entries also
bind their explicit instance protocol, ID, and identity. Locks contain no
project root or source path.

`ludoweave source lock PROJECT --manifest FILE` emits canonical lock bytes to
stdout without writing the project. `ludoweave source verify PROJECT --manifest
FILE --lock FILE` loads one confined bounded expected lock, recomputes current
identities through the unchanged M121-M124 readers, and requires an exact
match. Success emits canonical `ludoweave.cli.source-lock-verify/1`; mismatch
returns exit 2 with only the first differing field and optional entry ID.

The lock records content identity and is not an atomic filesystem snapshot,
signature, provenance, authenticity, import result, or cache. M125 adds no
discovery, import, compile, registry semantics, asset/dependency loading,
watcher, live update, write-back, world/session, command, transaction, world
mutation, receipt, dependency, root-package API, version, workflow job, hosted
allocation, or release-authority change.

## M126 project-confined asset-manifest loading

M126 starts from fully locally validated M125 commit
`cc440c84dbc53a07b5640ca46410e461fe686cb0`. It retains the exact existing
`ludoweave.assets/1` document while adding focused protocol/limit exports,
bounded UTF-8 decoding, deterministic canonical bytes, and one internal
`HeadlessProject.load_asset_manifest()` method.

The existing path-based `AssetManifest.load()` delegates to the same bounded
decoder. The project loader reuses the established portable project-relative
path policy and capped open-handle read before it returns the manifest with its
existing project-root composition context. Entries normalize by logical URI;
settings and dependencies retain deterministic order. Empty manifests remain
compatible.

M126 performs no asset source read, asset build, cache use or creation,
directory discovery, source-manifest integration, source-to-asset resolution,
import, compile, watcher, live update, write-back, world/session creation,
command, transaction, world mutation, or receipt. It adds no dependency,
engine-root API, version, CLI, workflow job, hosted allocation, or release-
authority change. A later milestone must separately decide dependency-check
semantics.

## M127 source-to-asset dependency checking

M127 starts from fully locally validated M126 commit
`9b373698c206982bcb6e86127ac8dffb2385a261`. It adds strict
`AssetManifest.dependency_closure()` over exact distinct direct roots and the
read-only command:

```console
ludoweave source assets PROJECT --manifest config/sources.json --assets config/assets.json
```

The command checks every explicit M124 scene or prefab through the unchanged
readers, loads one explicit M126 asset manifest, requires every source-declared
direct asset URI to exist, and reports each entry's direct declarations
separately from the unique URI-sorted closure resolved through the validated
acyclic asset graph. Success emits canonical
`ludoweave.cli.source-asset-check/1` only after every entry succeeds.

M127 does not infer asset references from component values, require sources to
repeat indirect dependencies, or reject unused asset-manifest entries. It
performs no asset source read, payload decode, asset build, import, cache use
or creation, compile, registry resolution, world/session creation, command,
transaction, world mutation, receipt, write, discovery, watcher, or live
update. It adds no dependency, engine-root API, version, workflow job, hosted
allocation, or release-authority change. Sequential reads are not an atomic
filesystem snapshot.

## M128 asset-source lock verification

M128 starts from fully locally validated M127 commit
`276d869b829735dcca7256cb73f190e15e84d9c0`. It adds bounded immutable
`ludoweave.asset-source-lock/1` values and two read-only commands:

```console
ludoweave source asset-lock PROJECT --manifest config/sources.json --assets config/assets.json
ludoweave source asset-verify PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json
```

The lock binds the canonical M125 source lock, canonical M126 asset manifest,
M127 direct roots, and the exact resolved URI/kind/source-byte-count/source-
SHA-256 entries. Empty closures remain valid. Selected sources are streamed in
URI order through project-confined owned descriptors, at most 256 MiB each and
1 GiB accepted aggregate. Mismatch errors expose only the first stable field
and optional logical URI, never compared hashes, sizes, or paths.

M128 is repeatable input identity, not an atomic filesystem snapshot,
signature, provenance, authenticity, imported artifact, build result, or cache
key. There is no asset decode, no asset build, no import, no cache read, no
cache write, no artifact creation, no reimport, no watcher, no discovery, no
world/session, mutation, receipt, or project write. It adds no dependency,
engine-root API, version, workflow job, workflow allocation, hosted allocation,
permission, credential, release authority, or remote change.

## M129 deterministic verified asset build planning

M129 starts from fully locally validated M128 commit
`ad6b43a9d480cd3bd94298799125ee736d15124e`. It adds bounded immutable
`ludoweave.asset-build-plan/1` values and one read-only command:

```console
ludoweave source asset-plan PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json
```

The command recomputes and verifies the current M128 input lock, then plans
exactly the M127-selected closure. Each asset appears once after all direct
dependencies; simultaneously ready assets use logical URI order. Entries bind
kind, settings, source SHA-256/byte count, direct dependency URIs, and the exact
existing M4 cache key. The plan also binds the canonical source-lock and asset-
manifest identities. Empty selected closures remain valid.

M129 is prospective deterministic work identity, not decoded output, build
success, cache presence, artifact integrity, provenance, or execution. It
performs no asset payload decode, asset build, import, cache read, cache write,
artifact creation, scheduler/worker execution, discovery, watcher, reimport,
world/session, mutation, receipt, or project write. It adds no dependency,
engine-root API, version, workflow job, workflow allocation, hosted allocation,
permission, credential, release authority, or remote change.

## M130 confined asset build-plan verification

M130 starts from fully locally validated M129 commit
`ae1b2bf01a001ea157e170626544a2d487055d09`. It adds exact content-silent
verification for `AssetBuildPlan`, project-confined loading for one explicit
saved plan, and one read-only command:

```console
ludoweave source asset-plan-verify PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json
```

The command strictly loads the saved M129 plan, recomputes and verifies current
M128 inputs, regenerates the current plan, and compares every stable field
before emitting bounded `ludoweave.cli.asset-build-plan-verify/1` success.
Mismatch diagnostics contain only the first field and optional logical URI,
never compared content or paths.

M130 is verification only. It performs no plan execution, payload decode,
asset build, import, cache read, cache write, artifact creation, scheduler/
worker execution, discovery, watcher, reimport, world/session, mutation,
receipt, or project write. It adds no dependency, engine-root API, version,
workflow job, workflow allocation, hosted allocation, permission, credential,
release authority, or remote change.

## M131 bounded in-memory asset plan execution

M131 starts from fully locally validated M130 commit
`1b69a30820d94c23272d7e1982ec80f978da8194`. It adds exact detached source
inputs, tightening-only execution limits, deterministic built-in decoder
execution, immutable `ludoweave.asset-build-result/1` identities, and one
command:

```console
ludoweave source asset-build PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json
```

The command loads the saved plan, recomputes and verifies current M128 inputs,
regenerates and verifies the M129 plan, then reads each selected source through
the existing project-confined bounded reader. Before decoding, the executor
requires exact plan order, byte counts, hashes, per-source bounds, and aggregate
source bounds. PNG, JSON, WGSL, and audio use only the existing built-in M4
behavior. Result entries bind URI, kind, cache key, source byte count, and
decoded artifact SHA-256/byte count; decoded payloads are not retained.

M131 performs no cache read, cache write, persisted artifact creation, project
write, atomic publication, scheduler/worker/process/thread execution, plugin or
decoder registration, discovery, watcher, import/reimport, live update,
renderer upload, world/session, mutation, or receipt. It adds no dependency,
engine-root API, version, workflow job, workflow allocation, hosted allocation,
permission, credential, release authority, or remote change.

## M132 verified local asset cache publication

M132 starts from fully locally validated M131 commit
`ea472476ee5cfca05afeda90fa888bf5557a3128`. It adds explicit bounded artifact
materialization, a verified local payload CAS plus action index, deterministic
`ludoweave.asset-cache-entry/1` metadata, path-free
`ludoweave.asset-cache-publish/1` reports, and one command:

```console
ludoweave source asset-cache PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --cache ../ludoweave-cache
```

The CLI completes M130 verification and all M131 materialization before it
creates the explicit cache root outside the project. Payloads publish by
artifact SHA-256 before atomic per-entry action metadata becomes visible under
the existing cache key. Every hit rechecks canonical metadata, byte count, and
payload SHA-256. Equivalent entries are reused without rewrite; corrupt
collisions fail closed; all still-owned staging paths are cleaned.

M132 has no remote cache, network, authentication, eviction, deletion, repair,
quota, discovery, watcher, reimport, scheduler/worker/process/thread, plugin,
decoder registration, renderer upload, world/session, mutation, or receipt. It
adds no project write, dependency, engine-root API, version, workflow job,
workflow allocation, hosted allocation, permission, credential, release
authority, or CI change.

## M133 verified read-only asset cache lookup

M133 starts from fully locally validated M132 commit
`da62eda909cbf47abfd7ef1e8c83a52466d8210a`. It adds explicit read-versus-write
cache authority, strict action metadata decoding, plan-ordered
`ludoweave.asset-cache-lookup/1` evidence, and one command:

```console
ludoweave source asset-cache-check PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --cache ../ludoweave-cache
```

The CLI completes exact current source-lock and build-plan verification before
opening the caller-selected cache read-only. It inspects only action keys from
that current plan. Missing actions are explicit misses, including when an
orphan CAS blob exists. Present entries must have duplicate-free exact canonical
metadata matching all plan-known fields and an ordinary payload matching its
bounded byte count and SHA-256. Corruption fails closed without mutation.

M133 has no cache-assisted execution, decoder bypass, cache write, repair,
deletion, eviction, remote cache, network, authentication, discovery,
enumeration, watcher, reimport, worker/process/thread, plugin, renderer upload,
project write, world/session, mutation, or receipt. It adds no dependency,
engine-root API, version, workflow job/allocation, hosted allocation,
permission, credential, release authority, or CI change.

## M134 read-only cache-assisted asset realization

M134 starts from fully locally validated M133 commit
`e3f79339bc5765ec8f11a0dee6b6e8cb3e687845`. It adds frozen
`ludoweave.asset-build-realization/1` evidence and one command:

```console
ludoweave source asset-realize PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --cache ../ludoweave-cache
```

The CLI completes current lock and plan verification, acquires the exact
project-confined detached source tuple, and opens the explicit cache read-only.
The realization boundary preflights every source before any cache action read,
then resolves and verifies every plan action before running a decoder. Verified
hits and decoded misses are merged in canonical plan order and obey the same
tightening-only per-entry and aggregate source/artifact limits. A missing cache
remains absent. Present corruption fails closed before any miss decoder runs.

M134 performs no automatic cache publication, cache creation/write/repair/
deletion/eviction, project write, remote cache, network, authentication,
discovery, watcher, reimport, worker/process/thread, plugin, renderer upload,
world/session, mutation, or receipt. It adds no dependency, native/backend
surface, engine-root API, version, workflow job/allocation, hosted allocation,
permission, credential, release authority, or CI change.

## M135 explicit post-realization cache population

M135 starts from fully locally validated M134 commit
`a6263a2e7d0df18ff1a34d32f02f88be29ee006c`. It adds frozen
`ludoweave.asset-cache-population/1` evidence and one explicit command:

```console
ludoweave source asset-cache-populate PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --cache ../ludoweave-cache
```

The operation opens the explicit cache read-only and completes all M134 source
preflight, cache verification, miss decoding, and limit checks. Only complete
realization permits a second store to acquire write authority and invoke the
unchanged M132 publisher. The canonical report combines plan-ordered
`hit`/`decoded` and `published`/`reused` statuses without payloads or paths.

Publication remains atomic per entry, not across the whole plan. Later
publication failure emits no success report but may leave earlier valid entries
or valid unreferenced CAS blobs. M135 adds no rollback, implicit publication to
`asset-realize`, repair/deletion/eviction, remote cache, shared-writer claim,
project write, dependency, version, workflow job/allocation, permission,
credential, release authority, or CI change.

## M136 saved asset-cache population verification

M136 starts from fully locally validated M135 commit
`59796814ee340254c11ccfde9330184ba7ef148d`. It adds bounded strict decoding of
saved `ludoweave.asset-cache-population/1` evidence and one command:

```console
ludoweave source asset-cache-population-verify PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --population config/population.json --cache ../ludoweave-cache
```

The command completes current lock and exact saved-plan verification, reads the
project-confined report under hard byte/entry bounds, rejects ambiguous or
inconsistent JSON, and preflights the complete report/plan identity before
opening the cache read-only. Every current action and CAS payload must verify
and match the saved output identity. Success is path-free
`ludoweave.asset-cache-population-verification/1` evidence.

M136 invokes no decoder and performs no cache/project write, repair, deletion,
or fallback. The unsigned report is local integrity evidence, not provenance,
authenticity, builder identity, or a trusted timestamp. It adds no remote cache,
signature/attestation system, dependency, version, workflow job/allocation,
permission, credential, release authority, or CI change.

## M137 bounded read-only asset-cache inventory

M137 starts from fully locally validated M136 commit
`d090131871594c8d49410c8d66e101376c010acc`. It adds one bounded complete local
cache integrity operation and command:

```console
ludoweave source asset-cache-inventory PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --cache ../ludoweave-cache
```

After current lock and exact saved-plan verification, the operation opens the
explicit cache read-only. It incrementally admits only exact engine-owned
`actions/` and `cas/` layout under hard action/blob/metadata/CAS-byte limits,
strictly reconstructs canonical action metadata, streams and hashes every CAS
blob, requires every action reference to resolve, and classifies current-plan
versus other storage in path-free `ludoweave.asset-cache-inventory/1` evidence.

The report can count CAS blobs with no action reference observed during the
scan. That is not deletion eligibility: the sequential scan has no atomic
snapshot, lease, generation, retention, last-use, or concurrent-writer proof.
M137 adds no write, deletion, repair, eviction, garbage collector, remote
cache, dependency, version, workflow job/allocation, permission, credential,
release authority, or CI change.

## M138 deterministic cache-observation fingerprint

M138 starts from fully locally validated M137 commit
`b5b904b22303991474ed99a8ed4473738070dd45`. It adds one path-free exact
identity over the M137 sequential verified storage observation and one command:

```console
ludoweave source asset-cache-fingerprint PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --cache ../ludoweave-cache
```

After current lock and exact saved-plan verification, one M137 bounded read-only
pass supplies both the nested aggregate inventory and a plan-independent
`observation_sha256`. Sorted action frames bind exact canonical metadata;
sorted CAS frames bind raw content digest and byte count. Both use explicit
record tags and unsigned eight-byte length framing under the
`ludoweave.asset-cache-fingerprint/1` domain.

The fingerprint is exact equality evidence for one sequential observation. It
is not an atomic snapshot, saved-state verifier, diff, lease, last-use record,
retention root, provenance statement, or deletion eligibility. M138 adds no
write, cleanup, deletion, repair, eviction, garbage collector, timestamp/age
policy, remote cache, dependency, version, workflow job/allocation, permission,
credential, release authority, or CI change.

## M139 saved cache-fingerprint verification

M139 starts from fully locally validated M138 commit
`aeca2b3ea1c1e6122df4080641f707e36a9a43d7`. It adds strict bounded decoding
of one canonical saved M138 fingerprint and one command:

```console
ludoweave source asset-cache-fingerprint-verify PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --fingerprint config/cache.fingerprint.json --cache ../ludoweave-cache
```

The command completes current lock and exact saved-plan verification, reads the
project-confined record under a 65,536-byte bound, and rejects duplicate names,
non-finite numbers, schema/type/protocol/digest/aggregate drift, or noncanonical
encoding. Complete record/plan identity preflights before one fresh M138
read-only observation. Exact inventory and observation-digest equality emits
path-free `ludoweave.asset-cache-fingerprint-verification/1` evidence.

Agreement is local integrity equality, not authenticity or provenance: M139
adds no signature, key/root of trust, attestation, trusted timestamp, remote
cache, atomic snapshot, diff, retention/deletion authority, cache/project
mutation, dependency, version, workflow job/allocation, permission, credential,
release authority, or CI change.

## M140 path-free cache-fingerprint comparison

M140 starts from fully locally validated M139 commit
`e7c01044da87004cea065fd07f379ea7ba09128f`. It adds one diagnostic command:

```console
ludoweave source asset-cache-fingerprint-compare PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --fingerprint config/cache.fingerprint.json --cache ../ludoweave-cache
```

Current source identities, lock, and exact regenerated plan are verified before
the bounded canonical saved record is read. Saved plan identity then preflights
before exactly one unchanged M138 read-only observation. Success or diagnostic
difference emits canonical path-free
`ludoweave.asset-cache-fingerprint-comparison/1` evidence: status, fingerprint
protocol, plan digest, one exact-observation equality flag, and signed deltas
for exactly the twelve existing M137 aggregate inventory fields.

Exit 0 means the exact observation and every aggregate are equal. Exit 1 is a
normal diagnostic difference on standard output. Invalid records, stale plans,
corrupt caches, or active-limit failures remain structured errors with exit 2.
Same-size object substitution is detectable through the equality flag even
when every aggregate delta is zero.

The fixed report is path-free and exposes no cache key, URI, artifact digest,
object identity, differing observation digest, filename, path, or payload. It
is not authenticity or provenance and grants no write, repair, cleanup,
retention, eviction, or deletion authority. M140 adds no generic diff/patch,
remote cache, atomic snapshot, dependency, version, workflow job/allocation,
permission, credential, release authority, or CI change.

## M141 offline saved cache-fingerprint comparison

M141 starts from fully locally validated M140 commit
`81d55ac7b531d5782aec8723a8df9b0be18b49ca`. It adds one pure comparison and
one CLI composition:

```console
ludoweave source asset-cache-fingerprint-record-compare PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --expected-fingerprint config/cache-before.json --current-fingerprint config/cache-after.json
```

Current source identities, lock, and exact regenerated plan verify before two
project-confined fingerprint reads. Each record retains M139's independent
65,536-byte bound and strict canonical decoder. Both saved nested plan digests
must match the exact current plan before the pure function compares them.

The operation reuses `ludoweave.asset-cache-fingerprint-comparison/1` unchanged:
twelve signed `current - expected` aggregate deltas and one exact-observation
equality flag. Equal emits canonical stdout with exit 0; different emits the
same fixed report with exit 1; invalid processing remains structured exit 2.
Same-size identity substitution remains detectable with all-zero deltas.

There is no cache argument, cache construction, or cache access. Both records
can be compared after their originating cache is absent. The report remains
path-free and publishes neither record's observation digest or object
identities.

This is comparison of two unsigned admitted values, not authenticity or
provenance. M141 adds no record store, trust/signature system, atomic snapshot,
detailed diff, retention/deletion/cleanup authority, remote cache, dependency,
version, workflow job/allocation, permission, credential, release authority,
or CI change.

## M142 saved cache-fingerprint comparison verification

M142 starts from fully locally validated M141 commit
`bff0e111b40a6e4b342fe4e5b93307d770b7be95`. It adds strict bounded admission
of the M140 comparison record and one pure offline verifier plus CLI composition:

```console
ludoweave source asset-cache-fingerprint-comparison-verify PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --expected-fingerprint config/cache-before.json --current-fingerprint config/cache-after.json --comparison config/cache-comparison.json
```

The command verifies current sources, saved lock, and exact regenerated plan
before reading two independently bounded canonical fingerprints and one
independently 4,096-byte bounded canonical comparison. Duplicate names,
non-finite values, overlong integers, unknown/missing fields, wrong types or
protocols, inconsistent status, out-of-range signed deltas, and noncanonical
bytes fail closed.

The pure operation reruns M141 comparison and requires exact equality with the
saved frozen value. Successful path-free
`ludoweave.asset-cache-fingerprint-comparison-verification/1` evidence binds the
plan, fingerprint/comparison protocols, comparison status, and SHA-256 of the
canonical aggregate report. A valid `different` report exits 0 because verifier
success means correct derivation, not equal observations. Invalid processing
or mismatch exits 2.

There is no cache argument or access after record admission. M142 is local
integrity evidence, not authenticity or provenance. It adds no detailed object
disclosure, signature/trust system, atomic snapshot, record store/retention,
cache cleanup/mutation, remote cache, dependency, version, workflow job or
allocation, permission, credential, release authority, or CI change.

## M143 path-free unreferenced-blob preview

M143 starts from fully locally validated M142 commit
`9f4a84b0e1f251d400398da4ef27d5c37eee386b`. It adds one pure preview value and
one read-only CLI composition:

```console
ludoweave source asset-cache-unreferenced-preview PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --cache CACHE
```

The command verifies current sources, the saved lock, and the exact regenerated
plan before resolving the cache. It performs exactly one unchanged bounded M138
fingerprint observation. An absent cache reports zero without creation.

Frozen path-free `ludoweave.asset-cache-unreferenced-preview/1` output contains
`observed` status, inventory/fingerprint protocols, plan and full-observation
SHA-256 values, and the existing unreferenced blob count/bytes. It lists no
candidate identity, key, URI, path, payload, timestamp, age, or policy. A
nonzero preview exits 0.

M143 deliberately does not equate unreferenced with deletable. It adds no
retained roots, last-use data, grace/age or quota policy, lock/quiescence,
atomic snapshot, cleanup, garbage collection, prune, repair, deletion,
eviction, remote cache, dependency, version, workflow job/allocation,
permission, credential, release authority, or CI change.

## M144 offline unreferenced-blob preview

M144 starts from fully locally validated M143 commit
`1e9eedd5307d3c1249fe1dcd2b22acf4a01ccfc2`. It adds one cache-free CLI
composition over the existing strict M139 saved-fingerprint decoder and pure
M143 preview:

```console
ludoweave source asset-cache-fingerprint-record-preview PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --fingerprint config/cache.fingerprint.json
```

The command preflights current sources, lock, and exact regenerated plan before
one bounded project-confined record read. It admits only exact canonical M138
fingerprint bytes, requires the nested plan binding, and emits the unchanged
M143 preview. There is no cache argument or cache access, so the originating
cache may be absent.

M144 adds no new runtime value/protocol/decoder, fresh observation, candidate
identity, path/payload/age disclosure, chronology or authenticity claim,
retention/deletion eligibility, atomic snapshot, cleanup/mutation, remote
cache, dependency, version, workflow job/allocation, permission, credential,
release authority, or CI change.

## M145 saved unreferenced-preview verification

M145 starts from fully locally validated M144 commit
`d6bbf33e35b5e21fa48d6553e1b3b73d104b0cd6`. It adds strict admission and
offline verification for the saved M143/M144 aggregate preview:

```console
ludoweave source asset-cache-unreferenced-preview-verify PROJECT --manifest config/sources.json --assets config/assets.json --lock config/assets.lock.json --plan config/assets.plan.json --fingerprint config/cache.fingerprint.json --preview config/cache.unreferenced-preview.json
```

The command preflights current sources, the saved lock, and the exact
regenerated plan before resolving either saved record. It then admits one M138
fingerprint under the existing 65,536-byte limit and one exact-schema canonical
preview under a new tightening-only 2,048-byte limit. A pure verifier
recomputes M143 from those values and requires exact frozen-value equality.
Success emits a fixed path-free verification record binding the exact preview
bytes by SHA-256. There is no cache argument or cache access.

M145 adds no current-cache observation, chronology/freshness guarantee,
authenticity/provenance or writer-identity claim, trusted timestamp, candidate
identity, retention/deletion eligibility, mutation, remote cache, dependency,
version, workflow job/allocation, permission, credential, release authority,
or CI change.

## M146 cache-cleanup readiness decision

M146 starts from fully locally validated M145 commit
`2a08a5cde25cab2b6a9950c0013c69286da873bb`. It deliberately adds no cache
cleanup API. M137-M145 provide bounded integrity observations and path-free
aggregate evidence, but they neither disclose candidate identity nor prove that
an apparently unreferenced blob remains unreferenced at deletion time.

Cleanup remains deferred until one approved design jointly specifies exact
identity-bearing candidate evidence, retained roots, leases/pins, an atomic or
generation-bound quiescent observation, explicit grace/quota policy and trusted
time semantics, bounded dry-run and mutation receipts, concurrent-writer and
crash recovery, link/reparse safety, and restore/rollback behavior. Aggregate
equality or age alone is insufficient.

M146 adds no runtime value, protocol, decoder, CLI command, candidate listing,
retention policy, cleanup/prune/garbage-collection/deletion/eviction authority,
cache read or write, dependency, version, workflow job/allocation, permission,
credential, release authority, or CI change.

## M147 asset-cache cleanup threat model

M147 starts from fully locally validated M146 commit
`15a1294e02c0efc77fdb668430d89413af424c9d`. It accepts a dedicated
[asset-cache cleanup threat model](docs/security/cache-cleanup-threat-model.md)
before any mutation design. The model covers assets, actors, trust boundaries,
TOCTOU and link/reparse substitution, hard-link aliases, concurrent readers and
writers, incomplete or stale evidence, trusted-time rollback, crash recovery,
idempotence, quarantine, rollback tampering, privacy, and safe refusal.

A future implementation must separately type dry-run and mutation authority,
bind identity-bearing candidates to an exact cache root and generation, hold
cross-process quiescence through use, revalidate with proven handle-relative
no-follow semantics, stage same-filesystem quarantine, and emit durable typed
receipts. The design must fail closed where a platform cannot prove those
semantics and must pass adversarial Windows, macOS, and Linux tests.

M147 adds no runtime API, protocol, decoder, CLI command, cache access,
candidate disclosure, retention implementation, trusted time, lock,
quarantine, repair, cleanup authority, mutation, remote cache, dependency,
version, workflow job/allocation, permission, credential, release authority,
or CI change. RFC-0130 records the accepted threat boundary.

## M148 cache-cleanup platform-capability decision

M148 starts from fully locally validated M147 commit
`752334dd981799c95d24308087222be487c0587e`. It accepts a focused
[platform-capability
decision](docs/security/cache-cleanup-platform-capability-decision.md): current
portable CPython does not expose the complete handle-relative, no-follow,
identity-at-use mutation chain required by M147.

Exact Windows CPython 3.12.13, 3.13.13, and 3.14.5 probes expose no `dir_fd`
support for open/unlink/rmdir/rename/replace and report
`shutil.rmtree.avoids_symlink_attacks == False`. POSIX, Linux, macOS, and Win32
provide lower-level partial primitives, but no platform is admitted without a
private engine-owned adapter, complete adversarial real-host evidence, and safe
refusal. A public boolean probe would be insufficient and is not added.

M148 adds no runtime API, protocol, decoder, CLI command, public probe, cache
access, candidate disclosure, cleanup authority, platform adapter, native code,
`ctypes`, mutation, remote cache, dependency, version, workflow job/allocation,
permission, credential, release authority, or CI change. RFC-0131 records the
accepted decision.

## M149 Windows cache-cleanup capability probe

M149 starts from fully locally validated M148 commit
`4f6b59ef37877ba3575ca19e0f15cfdadcc6a253`. It adds one test-only
[Windows capability
probe](docs/security/cache-cleanup-windows-capability-probe.md) under
RFC-0132. The probe uses documented user-mode native file operations only
inside pytest-owned temporary directories.

The current host demonstrates directory-handle-relative opens of ordinary
components while requesting the documented final-component reparse-suppression
option; volume/file identity and hard-link-count observation; non-replacing
handle-relative quarantine; identity-preserving reopen; deletion disposition;
and deterministic close. Exact CPython 3.12.13, 3.13.13, and 3.14.5 expose the
required system symbols. Symbolic-link creation is not granted on the current
non-administrator host, so the reparse-refusal case remains an explicit skip
and missing admission evidence.

Windows remains unadmitted. The probe does not establish filesystem coverage,
all-component reparse/junction safety, race or cross-process exclusion,
recovery, retained roots, policy, trusted time, durable receipts, or independent
installed-host behavior.

M149 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes`, adapter, cache access, candidate disclosure, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing test suite is the only future hosted execution path.

## M150 Windows directory-junction refusal probe

M150 starts from fully locally validated M149 commit
`b9c3a3b38b3cf22cf5351e13b362602d0c46d9eb`. It adds one Windows-only,
test-only [directory-junction refusal
probe](docs/security/cache-cleanup-windows-junction-probe.md) under RFC-0133.

The current host's opened pytest root reports NTFS and reparse-point support.
A fixed `mklink /j` fixture creates one directory junction without elevation;
M149's retained-handle relative open observes the junction object, refuses its
reparse attribute, closes the rejected handle, and leaves the target marker
unchanged after explicit link-only removal.

Windows remains unadmitted. The earlier symbolic-link case remains privilege-
skipped, and M150 does not establish mounted-folder, unknown-tag, other-
filesystem, all-component substitution, concurrency, recovery, policy,
receipt, or independent-host safety.

M150 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or shell invocation, adapter, cache access, candidate
disclosure, cleanup authority, dependency, native extension, compiler
requirement, version, workflow job/allocation, permission, credential, release
authority, or CI change. The existing Windows suite is the only future hosted
execution path.

## M151 Windows retained-parent namespace-substitution probe

M151 starts from fully locally validated M150 commit
`42cac8b6ade92af3bb29bbd2e9781cb0799ddc58`. It adds one Windows-only,
test-only [retained-parent substitution
probe](docs/security/cache-cleanup-windows-retained-parent-substitution-probe.md)
under RFC-0134.

The current NTFS host retains an opened `live` directory, renames it to
`displaced`, and replaces the former name with a fixed directory junction to a
distinct `target`. A fresh root-relative `live` open refuses the junction. An
open relative to the retained parent identifies the file under `displaced` and
differs from the same-named file under `target`; explicit link-only cleanup
preserves both contents.

Windows remains unadmitted. This deterministic same-process fixture is not a
concurrent race, cross-process exclusion, oplock/share stress, ancestor-
acquisition, other-reparse-tag, other-filesystem, recovery, policy, receipt, or
independent-host proof.

M151 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or shell invocation, adapter, cache access, candidate
disclosure, cleanup authority, dependency, native extension, compiler
requirement, version, workflow job/allocation, permission, credential, release
authority, or CI change. The existing Windows suite is the only future hosted
execution path.

## M152 Windows cross-process namespace-substitution probe

M152 starts from fully locally validated M151 commit
`3df94f419f14e230275d4dd38ee9f0bcb53b49f6`. It adds one Windows-only,
test-only [cross-process substitution
probe](docs/security/cache-cleanup-windows-cross-process-substitution-probe.md)
under RFC-0135.

The current NTFS host retains an opened `live` directory in the parent process.
A fixed non-inheriting child `cmd.exe` invocation renames it to `displaced` and
creates a junction at the former name. After child exit, a fresh root-relative
`live` open refuses the junction, while the retained parent identifies the
original file under `displaced` rather than the same-named file under `target`.
Explicit link-only cleanup preserves both contents.

Windows remains unadmitted. This deterministic child-process fixture is not a
concurrent race, cross-process exclusion, controlled native-call interleaving,
oplock/share stress, quiescence, handle-inheritance, other-filesystem, recovery,
policy, receipt, or independent-host proof.

M152 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, dependency, native extension, compiler
requirement, version, workflow job/allocation, permission, credential, release
authority, or CI change. The existing Windows suite is the only future hosted
execution path.

## M153 Windows cross-process share-delete exclusion probe

M153 starts from fully locally validated M152 commit
`44953ff23ed84a50cdeed47c4564ebbc45c8447a`. It adds one Windows-only,
test-only [share-delete exclusion
probe](docs/security/cache-cleanup-windows-share-delete-exclusion-probe.md)
under RFC-0136.

The current NTFS host retains an opened `live` directory with read and write
sharing but without delete sharing. A fixed non-inheriting child `cmd.exe`
invocation cannot rename it to `displaced`; the namespace and candidate bytes
remain unchanged. After deterministic close of that blocking handle, the
identical child command succeeds and the unchanged candidate is available
under the new name. The root handle then closes to zero owned handles.

Windows remains unadmitted. This paired current-host observation is not
general cross-process exclusion, a controlled race, an interleaving at a
selected native call, an oplock protocol, quiescence, descendant-activity
proof, other-filesystem evidence, recovery, policy, receipt, or independent-
host proof.

M153 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, dependency, native extension, compiler
requirement, version, workflow job/allocation, permission, credential, release
authority, or CI change. The existing Windows suite is the only future hosted
execution path.

## M154 Windows native sharing-violation probe

M154 starts from fully locally validated M153 commit
`f34bf8032c523a60e80711745c2776b5ca6d99ab`. It adds one Windows-only,
test-only [native sharing-violation
probe](docs/security/cache-cleanup-windows-native-sharing-violation-probe.md)
under RFC-0137.

The current NTFS host retains M153's no-delete-share `live` handle. A fixed
repository-owned helper runs in an isolated non-inheriting child and calls
`MoveFileExW` directly with only `live` and `displaced`. While the blocker is
open, the native result is false with `ERROR_SHARING_VIOLATION` (32), and the
namespace/content remain unchanged. After deterministic close, the identical
child returns true with normalized code zero and the candidate is unchanged
under `displaced`.

Windows remains unadmitted. This is one direct current-host native error
observation, not a universal error-code contract, general cross-process
exclusion, controlled race, selected interleaving, oplock protocol,
quiescence, other-filesystem/driver evidence, recovery, policy, receipt, or
independent-host proof.

M154 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, dependency, native extension, compiler
requirement, version, workflow job/allocation, permission, credential, release
authority, or CI change. The existing Windows suite is the only future hosted
execution path.

## M155 Windows child-owned share-delete handshake

M155 starts from fully locally validated M154 commit
`e831a1cc098ea22d94cd87c7f7d9cf785012d97e`. It adds one Windows-only,
test-only [child-owned share-delete
handshake](docs/security/cache-cleanup-windows-child-owned-share-delete-handshake.md)
under RFC-0138.

A fixed isolated child opens ordinary `live` with M153's exact directory access
mask and read/write sharing without delete sharing. It emits bounded `ready`,
then waits for one fixed release byte. A separate unchanged M154 rename child
returns false/error 32 while the blocker remains alive. After the owner closes
and emits bounded `closed`, the identical rename child returns true/code zero
and the candidate remains unchanged under `displaced`.

Windows remains unadmitted. This ordered current-host ownership transition is
not a concurrent race, selected native-call interleaving, general exclusion,
quiescence, oplock protocol, duplicated-handle result, other-filesystem/driver
evidence, recovery, policy, receipt, or independent-host proof. A metadata-only
prototype did not block the rename, so the accepted fixture preserves M153's
exact nonzero access mask rather than inferring exclusion from share flags.

M155 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, dependency, native extension, compiler
requirement, version, workflow job/allocation, permission, credential, release
authority, or CI change. The existing Windows suite is the only future hosted
execution path.

## M156 Windows abrupt blocker-owner termination probe

M156 starts from fully locally validated M155 commit
`40aee9c75a8d10bc9876869788b9e39db73c1151`. It adds one Windows-only,
test-only [abrupt blocker-owner termination
probe](docs/security/cache-cleanup-windows-abrupt-blocker-termination-probe.md)
under RFC-0139.

The parent reuses M155's fixed blocker and bounded `ready` handshake but sends
no release token. M154's unchanged native rename child returns false/error 32
while the blocker remains alive. The parent then forces termination, waits
with M155's fixed timeout, requires a nonzero but not numerically standardized
exit and no `closed` acknowledgement, and invokes the identical rename once.
That retry returns true/code zero and preserves the candidate under
`displaced`.

Windows remains unadmitted. This single current-host forced-termination
transition is not crash or restart recovery, a close-failure protocol,
controlled concurrent interleaving, general exclusion, duplicated-handle or
oplock behavior, other-filesystem/driver evidence, policy, receipt, or
independent-host proof.

M156 adds no runtime API, protocol, decoder, CLI command, public probe, helper,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, dependency, native extension, compiler
requirement, version, workflow job/allocation, permission, credential, release
authority, or CI change. The existing Windows suite is the only future hosted
execution path.

## M157 Windows blocker control-pipe EOF probe

M157 starts from fully locally validated M156 commit
`b0076e48e6538744a8ffc1909c725d1293d56eba`. It adds one Windows-only,
test-only [blocker control-pipe EOF
probe](docs/security/cache-cleanup-windows-control-pipe-eof-probe.md) under
RFC-0140.

The parent reuses M155's fixed blocker and bounded `ready` handshake. M154's
unchanged native rename child returns false/error 32 while the blocker remains
alive. The parent writes no control byte, closes only `Popen.stdin`, and waits
with M155's fixed timeout. The helper closes its native handle in `finally`,
emits no `closed`, and returns its existing invalid-control code 4. The
identical rename then returns true/code zero and preserves the candidate under
`displaced`.

Windows remains unadmitted. This single current-host EOF-triggered helper path
is not arbitrary pipe failure, broken-pipe write behavior, readiness or
termination timeout, native close failure, cancellation, crash or restart
recovery, controlled concurrent interleaving, general exclusion, duplicated-
handle or oplock behavior, policy, receipt, or independent-host proof.

M157 adds no runtime API, protocol, decoder, CLI command, public probe, helper,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. The existing Windows suite is the
only future hosted execution path.

## M158 Windows blocker invalid-control-token probe

M158 starts from fully locally validated M157 commit
`7c28ad99d2d13c64a7d45cdbd9d6f2181eb24c99`. It adds one Windows-only,
test-only [blocker invalid-control-token
probe](docs/security/cache-cleanup-windows-invalid-control-token-probe.md)
under RFC-0141.

The parent reuses M155's fixed blocker and bounded `ready` handshake. M154's
unchanged native rename child returns false/error 32 while the blocker remains
alive. The parent writes exactly one repository-fixed `?` byte, requires the
buffered write to accept it, flushes and closes `Popen.stdin`, and waits with
M155's fixed timeout. The helper closes its native handle in `finally`, emits
no `closed`, and returns its existing invalid-control code 4. The identical
rename then returns true/code zero and preserves the candidate under
`displaced`.

Windows remains unadmitted. This single current-host fixed invalid-token path
is not arbitrary malformed input, partial or multiple writes, broken-pipe
behavior, readiness or termination timeout, native close failure,
cancellation, crash or restart recovery, controlled concurrent interleaving,
general exclusion, duplicated-handle or oplock behavior, policy, receipt, or
independent-host proof.

M158 adds no runtime API, protocol, decoder, CLI command, public probe, helper,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. The existing Windows suite is the
only future hosted execution path.

## M159 Windows blocker broken-control-pipe probe

M159 starts from fully locally validated M158 commit
`9061edfe4fd04685a57425bb049834a9fc1bffd5`. It adds one Windows-only,
test-only [blocker broken-control-pipe
probe](docs/security/cache-cleanup-windows-broken-control-pipe-probe.md) under
RFC-0142.

The parent reuses M155's fixed blocker and bounded `ready` handshake. M154's
unchanged native rename child returns false/error 32 while the blocker remains
alive. The parent kills the blocker once, completes the bounded wait, requires
output EOF, and then passes the existing release byte to one direct test-only
`WriteFile`. The current host returns false/error 232 with zero bytes. The
parent writer closes normally, the identical rename returns true/code zero,
and the candidate remains preserved under `displaced`.

The initial high-level probe instead exposed `OSError(errno.EINVAL)`, not
Python's documented `BrokenPipeError`; M159 therefore records only the exact
native current-host result. Windows remains unadmitted. This is not a Python
exception-mapping or universal Windows error contract, arbitrary pipe failure,
retry or recovery policy, timeout, native close failure, cancellation, crash or
restart recovery, controlled concurrent interleaving, general exclusion,
duplicated-handle or oplock behavior, policy, receipt, or independent-host
proof.

M159 adds no runtime API, protocol, decoder, CLI command, public probe, helper,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. Test-only native calls remain
outside the package and the existing Windows suite is the only future hosted
execution path.

## M160 Windows live-blocker wait-timeout probe

M160 starts from fully locally validated M159 commit
`78837a61695a38207f06ca474f50f58d9bb9c62e`. It adds one Windows-only,
test-only [live-blocker wait-timeout
probe](docs/security/cache-cleanup-windows-live-wait-timeout-probe.md) under
RFC-0143.

The parent reuses M155's fixed blocker and bounded `ready` handshake. M154's
unchanged native rename child returns false/error 32 while the blocker remains
alive. One `Popen.wait(timeout=0.0)` raises exact `TimeoutExpired`; the child
return code remains unset, the blocker remains alive, and the identical rename
returns false/error 32 again with namespace/content unchanged. M155's existing
graceful release then returns exact `closed` and child exit zero before the
identical rename returns true/code zero with content preserved.

Windows remains unadmitted. This is not a timeout recovery contract, nonzero
timeout guarantee, readiness or graceful-close timeout, cancellation, kill
policy, native close failure, crash or restart recovery, controlled concurrent
interleaving, general exclusion, duplicated-handle or oplock behavior, policy,
receipt, or independent-host proof.

M160 adds no runtime API, protocol, decoder, CLI command, public probe, helper,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. The existing Windows suite is the
only future hosted execution path.

## M161 Windows acknowledged-release timeout probe

M161 starts from fully locally validated M160 commit
`2ef87449a23b05e637b876cdee238cc58b10bd10`. It adds one Windows-only,
test-only [acknowledged-release timeout
probe](docs/security/cache-cleanup-windows-acknowledged-release-timeout-probe.md)
under RFC-0144.

A fixed standalone child opens ordinary `live` without delete sharing, emits
exact `ready`, accepts M155's `!` release-intent byte, and emits exact
`release-held` while deliberately retaining its native handle. One
`Popen.wait(timeout=0.0)` raises exact `TimeoutExpired`; the child remains live
and M154's identical rename remains false/error 32. A distinct fixed `.` close
byte then orders native handle close, exact `closed`, child exit zero, and the
identical rename's true/code-zero result with content preserved.

Windows remains unadmitted. This is not a graceful-close timeout contract,
timeout recovery, nonzero timeout guarantee, cancellation, kill policy,
native close-failure result, crash or restart recovery, controlled concurrent
interleaving, general exclusion, duplicated-handle or oplock behavior, policy,
receipt, or independent-host proof.

M161 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. The fixed child is test-only and
the existing Windows suite is the only future hosted execution path.

## M162 Windows duplicated-handle retention probe

M162 starts from fully locally validated M161 commit
`d0cac5376e4c67c2e1609b1e2119df28a8e057e3`. It adds one Windows-only,
test-only [duplicated-handle retention
probe](docs/security/cache-cleanup-windows-duplicated-handle-probe.md) under
RFC-0145.

A fixed standalone child opens ordinary `live` without delete sharing and
creates one noninheritable same-process duplicate with
`DUPLICATE_SAME_ACCESS` before exact `ready`. Fixed byte `1` closes only the
original and emits exact `original-closed`; M154's identical rename remains
false/error 32 with namespace and content unchanged. Fixed byte `2` closes the
duplicate and orders exact `closed`, child exit zero, and the identical
rename's true/code-zero result with content preserved.

Windows remains unadmitted. This is not inherited-handle evidence,
cross-process duplication or transfer, general handle-count verification,
native close-failure behavior, crash or restart recovery, controlled
concurrent interleaving, general exclusion, oplock behavior, policy, receipt,
or independent-host proof.

M162 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. The fixed child is test-only and
the existing Windows suite is the only future hosted execution path.

## M163 Windows inherited-handle retention probe

M163 starts from fully locally validated M162 commit
`82f39fcccae309db6fde508ed04b468661fcaa6e`. It adds one Windows-only,
test-only [inherited-handle retention
probe](docs/security/cache-cleanup-windows-inherited-handle-probe.md) under
RFC-0146.

The parent opens ordinary `live` without delete sharing, places only that
handle in `STARTUPINFO.lpAttributeList`'s explicit handle list, temporarily
marks it inheritable around fixed child creation, and immediately restores it
to noninheritable. The child accepts only the canonical positive decimal
handle value and emits exact `ready` before awaiting fixed byte `!`.

M154's identical native rename remains false/error 32 before and after the
parent closes its handle while the inherited child handle remains live. The
fixed token closes the child's handle exactly once and orders exact `closed`,
child exit zero, output EOF, and the identical rename's true/code-zero result
with content preserved.

Windows remains unadmitted. This is not a concurrency-safe inheritance
contract, broad inheritance, cross-process duplication or transfer, native
close-failure behavior, crash or restart recovery, controlled concurrent
interleaving, leak-freedom under concurrent launches, general exclusion,
oplock behavior, policy, receipt, or independent-host proof.

M163 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. The fixed child is test-only and
the existing Windows suite is the only future hosted execution path.

## M164 Windows inherited-handle launch-failure probe

M164 starts from fully locally validated M163 commit
`86ba05218f8bae79153677e8c6fae200a61f019f`. It adds one Windows-only,
test-only [inherited-launch failure
probe](docs/security/cache-cleanup-windows-inherited-launch-failure-probe.md)
under RFC-0147.

The parent opens ordinary `live` without delete sharing, places only that
handle in a `STARTUPINFO` explicit handle list, and temporarily marks it
inheritable around a fixed missing-executable launch. The real process-
creation failure returns exact current-host `FileNotFoundError`, errno
`ENOENT`, and Windows error 2; `finally` restores the handle to
noninheritable without returning a process owner.

The parent retains owned count one and M154's identical native rename remains
false/error 32 with namespace/content unchanged. Closing that parent handle
exactly once reduces owned count to zero and orders the identical second
rename's true/code-zero result with content preserved.

Windows remains unadmitted. This is not restoration-failure injection,
arbitrary process-creation failure coverage, leak-freedom under concurrent
launches, a concurrency-safe inheritance contract, invalid-handle evidence,
child-crash behavior, recovery, general exclusion, policy, receipt, or
independent-host proof.

M164 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. The probe is test-only and the
existing Windows suite is the only future hosted execution path.

## M165 Windows inherited-handle restoration-failure probe

M165 starts from fully locally validated M164 commit
`70ca584aeda0f0f718ef83438e67b3422acde184`. It adds one Windows-only,
test-only [inherited-handle restoration-failure
probe](docs/security/cache-cleanup-windows-inherited-restore-failure-probe.md)
under RFC-0148.

The test uses M163's unchanged successful-child launch helper. It delegates
the initial inheritable transition to the real setter, permits the fixed child
to start with one explicitly allowlisted blocker handle, and injects one fixed
exception before the first native restore for that exact parent handle. The
existing helper must close and reap the child before re-raising the identical
error; no process owner is returned and all three child pipe streams are
closed.

Because the native restore was bypassed, the parent handle remains observably
inheritable until the caller repairs it with the captured original setter in
`finally`. After repair, parent owned count remains one and M154's identical
native rename remains false/error 32. Exact parent close reduces owned count to
zero and orders the identical second rename's true/code-zero result with
content preserved.

Windows remains unadmitted. This is not a real native restoration failure,
arbitrary failure coverage, leak-freedom under concurrent launches, a
concurrency-safe inheritance contract, native-close evidence, recovery,
general exclusion, policy, receipt, or independent-host proof.

M165 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. The probe is test-only and the
existing Windows suite is the only future hosted execution path.

## M166 Windows concurrent broad-inheritance leak probe

M166 starts from fully locally validated M165 commit
`5ec5e79330c5798e13424dfea5a11522b6c93f7a`. It adds one Windows-only,
test-only [concurrent broad-inheritance leak
probe](docs/security/cache-cleanup-windows-concurrent-inheritance-leak-probe.md)
under RFC-0149.

The test preserves M163's helper and fixed child fixture byte-for-byte. A
module-local subprocess proxy and two bounded events pause the exact explicit-
list `Popen` call after M163 makes the blocker handle inheritable. During that
controlled window, the caller uses the captured real `Popen` class to start the
same fixed child with `close_fds=False`, fixed executable/path arguments,
`shell=False`, trusted pytest cwd, and owned pipes.

Both children must emit exact `ready`, and M163's unchanged `finally` restores
the parent flag to noninheritable. M154's identical native rename remains
false/error 32 before parent close, after parent close, and after the intended
explicit-list child closes and exits zero while the broad child remains live.
Only the broad child's acknowledged close and zero exit permit the identical
fourth rename's true/code-zero result with content preserved.

Windows remains unadmitted. This is one deliberately controlled real leak
observation, not a concurrency-safe inheritance contract, general leak-
freedom, a runtime spawn coordinator, arbitrary process-creator or failure
coverage, recovery, general exclusion, policy, receipt, or independent-host
proof.

M166 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. The probe is test-only and the
existing Windows suite is the only future hosted execution path.

## M167 Windows concurrent explicit-list isolation probe

M167 starts from fully locally validated M166 commit
`86b0e49d0d91ab2e134a8d7b9cb247012883fe7e`. It adds one Windows-only,
test-only [concurrent explicit-list isolation
probe](docs/security/cache-cleanup-windows-concurrent-explicit-inheritance-probe.md)
under RFC-0150.

The test preserves M163's helper and fixed child fixture plus M166's complete
boundary byte-for-byte. Two worker threads each use M163's exact helper with a
distinct noninheritable no-delete-share blocker and pytest-owned root. Bounded
module-local proxies require both handles inheritable, allow both real one-
handle-list `Popen` calls to complete while both flags remain true, and hold
both restoration calls until the overlap is observed.

Both children must become ready/live and both parent flags must return false.
M154's identical native rename remains false/error 32 for both roots before
and after both parent handles close. The child release orders A-to-B and B-to-A
must each permit true/code-zero rename only for the released child's root while
the other remains false/error 32, then permit the second root after its child
closes. Both distinct payloads remain preserved.

Windows remains unadmitted. This is one controlled pairwise isolation
observation, not a concurrency-safe process-creation contract, coverage of
every creator/handle/failure/reentrant interleaving, general leak-freedom, a
runtime launch coordinator, recovery, general exclusion, policy, receipt, or
independent-host proof.

M167 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. The probe is test-only and the
existing Windows suite is the only future hosted execution path.

## M168 Windows concurrent explicit-list launch-failure probe

M168 starts from fully locally validated M167 commit
`dc3a1d154b4706518a0abb7e09f0531230e7de11`. It adds one Windows-only,
test-only [concurrent explicit-list launch-failure
probe](docs/security/cache-cleanup-windows-concurrent-explicit-launch-failure-probe.md)
under RFC-0151.

The test preserves M163's successful helper, M164's missing-executable helper,
M167's complete boundary, and the fixed child fixture byte-for-byte. Separate
threads exercise the successful and failing helpers with distinct blocker
handles and roots. Bounded module-local proxies require both handles true and
both launch boundaries ready, then hold both real outcomes and both restoration
entries while both flags remain inheritable.

The failure must be exact `FileNotFoundError`/Windows error 2 with no returned
process; the successful child must be ready/live and both flags must restore.
Both roots deny native rename before parent close. After both parents close,
the failed-launch root must return true/code zero while the successful root
remains false/error 32 until its child acknowledges close and exits zero. Both
success/failure label orientations preserve distinct content.

Windows remains unadmitted. This is one controlled successful/missing-
executable isolation observation, not a concurrency-safe process-creation
contract, arbitrary failure/cancellation/reentrancy coverage, general leak-
freedom, a runtime coordinator, recovery, exclusion, policy, receipt, or
independent-host proof.

M168 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. The probe is test-only and the
existing Windows suite is the only future hosted execution path.

## M169 Windows concurrent explicit-list restoration-failure probe

M169 starts from fully locally validated M168 commit
`54a123e59e8d5905750c2946786dedd534181884`. It adds one Windows-only,
test-only [concurrent explicit-list restoration-failure
probe](docs/security/cache-cleanup-windows-concurrent-explicit-restore-failure-probe.md)
under RFC-0152.

The test preserves M163's successful helper, M165's restoration-failure type
and boundary, M168's complete boundary, and the fixed child fixture byte-for-
byte. Separate threads launch two real children with distinct blocker handles
and roots. Bounded module-local proxies require both handles true, then hold
both launch outcomes and both restoration entries before injecting one exact
failure.

The helper must close and reap only the failed-restoration child before the
same error escapes. The survivor remains ready and live. After explicit repair
and both parent closes, the failed-restoration root must rename while the
survivor root remains false/error 32 until its child closes. Both A/B role
orientations preserve their distinct payloads and settle every owner.

This is not a real native restoration failure, not a concurrency-safe process-
creation contract, arbitrary failure coverage, cancellation, reentrancy,
general leak-freedom, a runtime coordinator, recovery, exclusion, policy,
receipt, Windows admission, or independent-host proof.

M169 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. The probe is test-only and the
existing Windows suite is the only future hosted execution path; no hosted
check is added.

## M170 Windows concurrent explicit-list abrupt-termination probe

M170 starts from fully locally validated M169 commit
`3707e1bfe38b3fa21f66183dbe827888bb6e24ea`. It adds one Windows-only,
test-only [concurrent explicit-list abrupt-termination
probe](docs/security/cache-cleanup-windows-concurrent-explicit-abrupt-termination-probe.md)
under RFC-0153.

The test preserves M156's forced-termination boundary, M163's successful
helper and fixture, M167's pairwise isolation boundary, and M169's complete
boundary byte-for-byte. Two real children start with distinct blocker handles
and roots while bounded module-local proxies hold both inheritability and
restoration windows.

After both flags restore and both parent handles close, both roots remain
false/error 32. One assigned child is killed and waited for with a fixed bound;
its nonzero exit and pipe EOF occur without a graceful `closed` phase. Only
that root may then rename. The survivor remains live and denied until its
existing acknowledged zero-exit close. Both A/B orientations preserve their
distinct payloads and settle every owner.

This is not crash recovery, cancellation semantics, arbitrary termination-
timing or native-close-failure coverage, a concurrency-safe process-creation
contract, general leak-freedom, a runtime coordinator, recovery, exclusion,
policy, receipt, Windows admission, or independent-host proof.

M170 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. The probe is test-only and the
existing Windows suite is the only future hosted execution path; no hosted
check is added.

## M171 Windows exclusive-root acquisition probe

M171 starts from fully locally validated M170 commit
`0c658d43886c986b129aa76dcc0ab413fd5cf618`. It adds one Windows-only,
test-only [exclusive-root acquisition
probe](docs/security/cache-cleanup-windows-exclusive-root-acquisition-probe.md)
under RFC-0154.

The test preserves M149's native capability, M153's share-delete boundary,
M155's fixed child and handshake, and M170's complete boundary byte-for-byte.
One private owner opens an ordinary `live` directory with sharing mode zero,
rejects reparse identity, and proves its handle noninheritable. A fixed child
all-sharing open must return false/error 32 until that owner closes, then true/
error zero.

The reverse direction starts M155's fixed child and waits for exact `ready`.
The parent's zero-sharing acquisition must return the existing native error
with code 32, adopt no handle, leave the child live, and preserve content. Only
the child's acknowledged close and zero exit permit the same parent acquisition
to succeed. That owner is also noninheritable and closes deterministically.

Windows remains unadmitted. This is one current-host two-way share-mode
observation, not a complete quiescence protocol, lock API, general exclusion,
oplock/lease contract, coverage of attribute-only or every access/share mode,
recovery, policy, receipt, cleanup authority, or independent-host proof.

M171 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. The probe is test-only and the
existing Windows suite is the only future hosted execution path; no hosted
check is added.

## M172 Windows descendant non-exclusion probe

M172 starts from fully locally validated M171 commit
`960efe770c48ddbfb925fd2cd7f9d220bca2e3ed`. It adds one Windows-only,
test-only [descendant non-exclusion
probe](docs/security/cache-cleanup-windows-descendant-non-exclusion-probe.md)
under RFC-0155.

The test preserves M149's native capability, M155's bounded ownership
handshake, and M171's complete boundary byte-for-byte. One fixed child opens
only `live/candidate.bin` for generic read with read/write/delete sharing and a
noninheritable handle. It emits exact `ready`, waits for one fixed release byte,
closes, emits exact `closed`, and exits zero.

Both acquisition orders succeed on the current NTFS host. A late descendant
holder becomes ready while M171's zero-sharing directory owner remains live;
an existing descendant holder remains live while that directory owner is
acquired. Each owner closes independently, and candidate bytes remain exact.

The result is negative capability evidence: a zero-sharing directory handle is
not recursive subtree quiescence. It cannot be promoted alone into the private
adapter required by M147. Complete participant/generation binding, retained
roots, mappings, oplocks, leases, multiple actors, filesystem variation,
recovery, policy, receipts, cleanup authority, and independent-host proof
remain open. Windows remains unadmitted.

M172 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. The probe is test-only and the
existing Windows suite is the only future hosted execution path; no hosted
check is added.

## M173 Windows cooperative-lock probe

M173 starts from fully locally validated M172 commit
`00eceb56246307f6fa57172fe674488189bfff4e`. It adds one Windows-only,
test-only [cooperative-lock
probe](docs/security/cache-cleanup-windows-cooperative-lock-probe.md) under
RFC-0156.

One fixed ordinary `live/coordination.lock` and one byte range provide a
shared/exclusive participant boundary. Two isolated children each hold a
shared fail-immediate `LockFileEx` lock. The parent requests an exclusive
fail-immediate lock over the identical range. All opens use generic read,
read/write/delete sharing, null security attributes, and noninheritable
handles; every successful owner explicitly unlocks and closes.

Both directions succeed on the current NTFS host. Two shared participants
coexist and collectively refuse the exclusive request with native error 33.
Closing one leaves the refusal intact; closing the last permits exact exclusive
acquisition and release. With the exclusive owner held first, a late shared
child reports refusal/error 33; after release, a fresh shared child completes
normally. Coordination bytes remain exact and every owner settles.

The result is positive but cooperative capability evidence. It cannot exclude
an uncooperative process and does not establish stable coordination identity,
generation binding, complete retained roots, mapped-view coverage,
substitution resistance, abrupt-exit settlement, recovery, policy, receipts,
cleanup authority, or independent-host proof. Windows remains unadmitted.

M173 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, candidate
disclosure, cleanup authority, recovery, dependency, native extension,
compiler requirement, version, workflow job/allocation, permission,
credential, release authority, or CI change. The probe is test-only and the
existing Windows suite is the only future hosted execution path; no hosted
check is added.

## M174 Windows cooperative-lock substitution probe

M174 starts from fully locally validated M173 commit
`767337f7ea8138bdc14455296c54d0261cd20e9e`. It adds one Windows-only,
test-only [cooperative-lock substitution
probe](docs/security/cache-cleanup-windows-cooperative-lock-substitution-probe.md)
under RFC-0157.

One unchanged M173 shared participant remains live while a fixed isolated child
renames `live/coordination.lock` to `live/coordination.displaced` and creates a
new ordinary file with identical bytes at the original pathname. Retained
`FILE_ID_INFO` observations prove the original and displaced handles share one
identity and that the replacement has another.

A fresh unchanged M173 participant locks the replacement concurrently. Each
generation independently refuses exclusive ownership. After the replacement
participant closes, the replacement accepts an exclusive owner while the old
participant remains live and still blocks only the displaced original. Closing
the old participant permits exact exclusive ownership there. Both files retain
the expected bytes and every owner settles.

The result is negative capability evidence. A reusable pathname can split a
cooperative protocol across independently quiescent identities, so a later
design must bind and revalidate trusted root identity, coordination identity,
and generation. Participant completeness, substitution resistance, mapped
views, abrupt-exit settlement, recovery, policy, receipts, cleanup authority,
and independent-host proof remain open. Windows remains unadmitted.

M174 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing Windows suite is the only future hosted execution path;
no hosted check is added.

## M175 Windows live substitution-exclusion probe

M175 starts from fully locally validated M174 commit
`f4aa920fa3b6cbcb8a9711111aaeb102f60902d4`. It adds one Windows-only,
test-only [live substitution-exclusion
probe](docs/security/cache-cleanup-windows-cooperative-lock-live-substitution-exclusion-probe.md)
under RFC-0158.

Two fixed participants hold M173's shared range while opening the coordination
file with read/write sharing and no delete sharing. M174's unchanged native
substitution child returns error 32 while both participants remain live and
again after one closes. M173's exclusive range owner returns error 33 through
the same final-live-participant boundary.

After the final protected participant closes, exact exclusive acquire/release
succeeds and the unchanged substitution child renames and replaces the file.
The displaced original retains its captured identity while the replacement
differs, and both contents remain exact.

The result is positive evidence only for continuous live ownership. It does not
bind a later participant across the zero-participant window. Trusted root and
coordination identity, generation issuance and retention, complete participant
admission, mapped views, abrupt-exit settlement, recovery, policy, receipts,
cleanup authority, and independent-host proof remain open. Windows remains
unadmitted.

M175 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing Windows suite is the only future hosted execution path;
no hosted check is added.

## M176 Windows cooperative-lock abrupt-settlement probe

M176 starts from fully locally validated M175 commit
`9e5d440b9c16687c7291c6abdf63b806b2cd33cf`. It adds one Windows-only,
test-only [cooperative-lock abrupt-settlement
probe](docs/security/cache-cleanup-windows-cooperative-lock-abrupt-settlement-probe.md)
under RFC-0159.

Two unchanged M175 protected participants first preserve M174 substitution
refusal/error 32 and M173 exclusive-range refusal/error 33. The first
participant is killed and reaped with the fixed process bound. It exits
nonzero with EOF after `ready` and no graceful `closed` record. The survivor
remains live and preserves both refusals.

The survivor is then killed and reaped through the same exact path. Exclusive
acquire/release and M174 substitution succeed without retry or sleep. The
displaced original retains its captured identity, the replacement differs,
both contents remain exact, and every owner settles.

The result is positive current-host evidence for one abrupt settlement order,
not crash recovery or a portable immediate-release guarantee. Microsoft notes
that operating-system lock release can be delayed by available resources. The
zero-participant substitution window, trusted identity/generation authority,
complete admission, arbitrary termination timing, process trees, mapped views,
filesystem variation, recovery, policy, receipts, cleanup authority, and
independent-host proof remain open. Windows remains unadmitted.

M176 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing Windows suite is the only future hosted execution path;
no hosted check is added.

## M177 Windows protected guardian-handoff probe

M177 starts from fully locally validated M176 commit
`16c6c730c4b7756dc38b5b8de8eef479efa32c12`. It adds one Windows-only,
test-only [protected guardian-handoff
probe](docs/security/cache-cleanup-windows-protected-guardian-handoff-probe.md)
under RFC-0160.

One private noninheritable guardian opens M173's coordination file for generic
read with read/write sharing while omitting delete sharing. With no range-lock
participant present, M174 substitution returns error 32 while M173 exclusive
range acquire/release succeeds. This proves namespace continuity without
misclassifying the guardian as a quiescence participant.

M175's unchanged participant joins, holds the shared range, and later closes
while the guardian remains. The participant-free interval retains substitution
error 32 and restores exclusive range availability. A second unchanged
participant joins the same observed `FILE_ID_INFO`; the guardian closes while
that participant remains live, and both substitution error 32 and exclusive-
range error 33 persist. Only final participant close permits exact exclusive
acquire/release and M174 substitution with the retained identity split.

This is one current-host continuous ownership chain, not generation authority,
trusted placement, complete admission, startup or crash recovery, or cleanup
authority. Guardian/process failure, hostile preexisting handles, mapped views,
filesystem variation, durable generation issuance, revalidation through use,
policy, receipts, Windows admission, and independent-host proof remain open.

M177 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing Windows suite is the only future hosted execution path;
no hosted check is added.

## M178 Windows guardian abrupt-handoff probe

M178 starts from fully locally validated M177 commit
`afa5aed0862c4a560a262a61a395b228d56afc3e`. It adds one Windows-only,
test-only [guardian abrupt-handoff
probe](docs/security/cache-cleanup-windows-guardian-abrupt-handoff-probe.md)
under RFC-0161.

One fixed isolated non-range-locking guardian child opens M173's coordination
identity for generic read with read/write sharing while omitting delete
sharing. It accepts no caller-selected path, argument, or environment value,
opens the final component without following a reparse point, rejects reparse
identity, and proves its handle noninheritable. Guardian-only substitution
returns error 32 while exact exclusive range acquire/release succeeds.

M175's unchanged protected participant joins the original `FILE_ID_INFO` and
adds shared range ownership. The guardian is then killed and reaped through
M176's bounded helper. Only after wait completes, the still-live participant
must retain original identity, substitution error 32, and exclusive-range
error 33. Its exact close then permits exclusive acquire/release and M174
substitution with retained displaced identity, distinct replacement identity,
and exact bytes.

This is one current-host overlapping ownership chain, not crash recovery,
generation authority, trusted placement, complete admission, startup recovery,
or cleanup authority. A crash without a compatible survivor, a zero-owner
interval, multiple guardians, hostile prior handles, mapped views, filesystem
variation, durable generation issuance, use-time revalidation, policy,
receipts, Windows admission, and independent-host proof remain open.

M178 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing Windows suite is the only future hosted execution path;
no hosted check is added.

## M179 Windows overlapping guardian-rotation probe

M179 starts from fully locally validated M178 commit
`e77068a9a2150e6820c979a4b809e76f21d36bc0`. It adds one Windows-only,
test-only [overlapping guardian-rotation
probe](docs/security/cache-cleanup-windows-overlapping-guardian-rotation-probe.md)
under RFC-0162.

M178's unchanged fixed guardian starts over M173's coordination identity, then
M175's unchanged protected participant joins. A second unchanged guardian
opens while all owners overlap. Exact `ready` events and fresh `FILE_ID_INFO`
observations retain the original identity with substitution error 32 and
exclusive-range error 33.

The first guardian is killed and reaped through M176's bounded helper. The
second guardian and participant remain live with both refusals intact. The
participant then closes exactly. With only the second guardian live, the
original identity and substitution error 32 persist while exact exclusive
range acquire/release succeeds. Final guardian close permits M174 substitution
with retained displaced identity, distinct replacement identity, and exact
bytes.

This is one current-host overlapping rotation, not guardian restart, crash
recovery, election, generation authority, trusted placement, complete
admission, startup recovery, or cleanup authority. Both guardians already
exist before failure. A zero-owner interval, replacement after failure,
simultaneous loss, hostile prior handles, mapped views, filesystem variation,
durable generation issuance, use-time revalidation, policy, receipts, Windows
admission, and independent-host proof remain open.

M179 adds no fixture, runtime API, protocol, decoder, CLI command, public
probe, production `ctypes` or subprocess invocation, adapter, cache access,
cleanup authority, dependency, native extension, compiler requirement,
version, workflow job/allocation, permission, credential, release authority,
or CI change. The existing Windows suite is the only future hosted execution
path; no hosted check is added.

## M180 Windows zero-owner guardian restart-boundary probe

M180 starts from fully locally validated M179 commit
`2d6312fbc59358f8ef080f5b335a815c6ffe2d15`. It adds one Windows-only,
test-only [zero-owner guardian restart-boundary
probe](docs/security/cache-cleanup-windows-zero-owner-guardian-restart-boundary-probe.md)
under RFC-0163.

Each of two sequences starts M178's unchanged fixed guardian over M173's exact
coordination identity, requires exact readiness and namespace protection with
the cooperative range available, then kills and boundedly waits for that
guardian through M176's unchanged helper.

In the benign sequence, the exposed pathname still names the original
`FILE_ID_INFO`. A later guardian reacquires that identity, retains substitution
error 32 without owning the range, and closes exactly before M174 substitution
succeeds. In the mutation sequence, M174 substitution succeeds during the
zero-owner interval. The later guardian attaches to the replacement identity,
blocks a second rename with error 32 while leaving the range available, and
after exact close permits that rename. Both sequences retain exact identities,
bytes, bounded waits, and complete cleanup without retry or sleep.

This is one current-host restart-boundary observation, not crash recovery,
generation authority, election, trusted placement, startup authentication,
continuity, complete admission, or cleanup authority. A pathname-only guardian
cannot recover or distinguish the displaced generation. Simultaneous loss,
failed restart launch, hostile prior handles, arbitrary process trees, mapped
views, filesystem variation, durable generation issuance, use-time
revalidation, policy, receipts, Windows admission, and independent-host proof
remain open.

M180 adds no fixture, runtime API, protocol, decoder, CLI command, public
probe, production `ctypes` or subprocess invocation, adapter, cache access,
cleanup authority, dependency, native extension, compiler requirement,
version, workflow job/allocation, permission, credential, release authority,
or CI change. The existing Windows suite is the only future hosted execution
path; no hosted check is added.

## M181 Windows expected-identity guardian admission probe

M181 starts from fully locally validated M180 commit
`d19e03ec9f83134d72086b93ebd988a5cade8f0d`. It adds one Windows-only,
test-only [expected-identity guardian admission
probe](docs/security/cache-cleanup-windows-expected-identity-guardian-admission-probe.md)
under RFC-0164.

The child receives an expected `FILE_ID_INFO`, opens M173's fixed coordination
pathname with no delete sharing, rejects inheritable or reparse handles, and
queries the identity on that same already protecting handle. An exact match
emits `ready`; a mismatch closes first and emits `identity_mismatch`.

The matching case requires direct rename error 32 and exact exclusive range
availability while the guardian is live, then exact close, successful rename,
original identity, bytes, and complete cleanup. The mismatch case uses M174 to
substitute a distinct replacement before launch. It requires exact mismatch
and bounded settlement, then successful replacement rename, range availability,
both retained identities, bytes, and complete cleanup without retry or sleep.

This is same-handle expected-identity admission evidence, not trusted identity
provenance, durable storage, generation authority, election, authentication,
recovery, policy, receipts, complete admission, or cleanup authority. Failed
launch, simultaneous loss, hostile handles, arbitrary process trees, mapped
views, filesystem variation, use-time revalidation, Windows admission, and
independent-host proof remain open.

M181 adds no runtime API, protocol, decoder, CLI command, public probe,
production `ctypes` or subprocess invocation, adapter, cache access, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing Windows suite is the only future hosted execution path;
no hosted check is added.

## M182 Windows hard-link alias non-exclusion probe

M182 starts from fully locally validated M181 commit
`d808b94102acd576c7ac8e458fe119692d614c4e`. It adds one Windows-only,
test-only [hard-link alias non-exclusion
probe](docs/security/cache-cleanup-windows-hard-link-alias-non-exclusion-probe.md)
under RFC-0165.

The probe creates a peer hard-link alias for M173's exact coordination file,
requires equal `FILE_ID_INFO` and link counts of at least two, then starts
M181's matching guardian. The exact opened name rejects rename with sharing
error 32, but the preexisting alias can be renamed while the guardian remains
live. The moved alias retains identity and link count, byte-range ownership is
available through both names, and a second exact-name rename remains refused.
After exact guardian close, the coordination entry can be renamed and both
remaining names retain identity, link count, and bytes.

This is hard-link alias non-exclusion evidence, not root-confined ownership,
hard-link enumeration, link-count policy, trusted root placement, durable
generation authority, deletion behavior, recovery, complete admission, or
cleanup authority. Windows remains unadmitted. The failed initial all-names
protection hypothesis is retained factually rather than converted into a
security claim.

M182 adds no runtime API, protocol, decoder, CLI command, public probe,
production native or subprocess surface, adapter, cache access, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing Windows suite is the only future hosted execution path;
no hosted check is added.

## M183 Windows post-admission hard-link creation probe

M183 starts from fully locally validated M182 commit
`b9d02dbdfbb13f290079970305e2e1c5c6cd783f`. It adds one Windows-only,
test-only [post-admission hard-link creation
probe](docs/security/cache-cleanup-windows-post-admission-hard-link-creation-probe.md)
under RFC-0166.

The probe starts with M173's exact coordination file at link count one and
admits M181's matching guardian. The exact opened name rejects rename with
sharing error 32, but standard-library `os.link` creates a peer alias while the
guardian remains live. Both handles retain the original identity and report
link count two, byte-range ownership remains available through both names, and
the guardian continues protecting the exact name it opened. After exact close,
that name can be renamed and both entries retain identity, count, and bytes.

This proves that guardian admission does not freeze the link set. It is not
trusted-root ownership, cross-process or cross-principal evidence, hard-link
enumeration, link-count policy, deletion behavior, durable generation
authority, recovery, complete admission, or cleanup authority. Windows
remains unadmitted.

M183 adds no runtime API, protocol, decoder, CLI command, public probe,
production native or subprocess surface, adapter, cache access, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing Windows suite is the only future hosted execution path;
no hosted check is added.

## M184 Windows hard-link alias deletion non-exclusion probe

M184 starts from fully locally validated M183 commit
`e44ce6a12d61a5c1b857b88e81c45015a986df77`. It adds one Windows-only,
test-only [hard-link alias deletion non-exclusion
probe](docs/security/cache-cleanup-windows-hard-link-alias-deletion-non-exclusion-probe.md)
under RFC-0167.

The probe starts with M173's exact coordination file and a peer alias at link
count two, then admits M181's matching guardian. The exact opened name rejects
rename with sharing error 32, but standard-library `Path.unlink` removes the
peer alias while the guardian remains live. The retained original handle then
reports link count one, byte-range ownership remains available, and the
guardian continues protecting the exact name it opened. After exact close,
that name can be renamed with identity, count, and bytes retained.

The initial hypothesis expected alias deletion to fail with sharing error 32;
the first live run falsified it. M184 preserves the narrower deletion
non-exclusion boundary. The deletion actor and guardian are separate parent
and child processes under one principal; M185 corrects the earlier process
classification. This is not trusted-root ownership, cross-principal evidence,
an independent third mutation actor, hard-link enumeration, link-count policy,
POSIX-delete behavior, durable generation authority, recovery, complete
admission, or cleanup authority. Windows remains unadmitted.

M184 adds no runtime API, protocol, decoder, CLI command, public probe,
production native or subprocess surface, adapter, cache access, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing Windows suite is the only future hosted execution path;
no hosted check is added.

## M185 Windows hard-link alias delete/recreate ABA probe

M185 starts from fully locally validated M184 commit
`5f4d1863984063fe3bc53951424a7b2b606f8f03`. It adds one Windows-only,
test-only [hard-link alias delete/recreate ABA
probe](docs/security/cache-cleanup-windows-hard-link-alias-delete-recreate-aba-probe.md)
under RFC-0168.

The probe starts with M173's exact coordination file and a peer alias at link
count two, then admits M181's matching guardian child. While the guardian
remains live, the parent deletes the alias, observes link count one, recreates
the same alias pathname, and observes link count two through both names. The
file identity and bytes remain unchanged, byte-range ownership remains
available, and the exact guarded pathname continues rejecting rename until
guardian close.

This records pathname-membership and link-count ABA (`2 -> 1 -> 2`) within one
guardian lifetime. It also corrects the M184 process classification: the
mutation actor and guardian are separate processes under one principal. It is
not trusted-root ownership, cross-principal evidence, an independent third
mutation actor, controlled concurrent racing, hard-link enumeration,
link-count policy, durable generation authority, recovery, admission, or
cleanup authority. Windows remains unadmitted.

M185 adds no runtime API, protocol, decoder, CLI command, public probe,
production native or subprocess surface, adapter, cache access, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing Windows suite is the only future hosted execution path;
no hosted check is added.

## M186 Windows independent hard-link alias mutator ABA probe

M186 starts from fully locally validated M185 commit
`4dd880402a8e6f6f1e74bd69be1cd3ad0366b513`. It adds one Windows-only,
test-only [independent hard-link alias mutator ABA
probe](docs/security/cache-cleanup-windows-independent-hard-link-alias-mutator-aba-probe.md)
under RFC-0169.

The probe retains M185's initial shared identity and exact `2 -> 1 -> 2`
transition but moves the alias delete/recreate calls into a distinct sibling
child process. M181's guardian child remains live throughout the mutation and
observation intervals. The parent only coordinates exact bounded handshakes
and verifies identity, bytes, link counts, range availability, child liveness,
exact-name rename refusal, exact close, and final cleanup.

This supplies a three-process, same-principal observation: parent coordinator,
guardian child, and independent mutation child. “Independent” means process
and mutation ownership only. It is not cross-principal, unrelated-process-tree
or unrelated-session evidence, controlled simultaneous racing, trusted-root
ownership, hard-link enumeration, link-count policy, recovery, admission, or
cleanup authority. Windows remains unadmitted.

M186 adds no runtime API, protocol, decoder, CLI command, public probe,
production subprocess or native surface, adapter, cache access, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing Windows suite is the only future hosted execution path;
no hosted check is added.

## M187 Windows hard-link alias mutator abrupt-loss probe

M187 starts from fully locally validated M186 commit
`3357f1e38de6b25ecdf15502ae46124bebcb3597`. It adds one Windows-only,
test-only [hard-link alias mutator abrupt-loss
probe](docs/security/cache-cleanup-windows-hard-link-alias-mutator-abrupt-loss-probe.md)
under RFC-0170.

The probe retains M186's initial shared identity, matching guardian, and fixed
sibling mutator child. After the mutator emits its exact `deleted` event, the
parent sends no recreate token. It terminates and reaps the child, requires a
nonzero exit and empty remaining output, and then verifies that the alias
remains absent while the original retains its identity, bytes, one-link count,
range availability, and guardian-enforced exact-name rename refusal. Exact
guardian close then permits rename of the unchanged one-link identity.

This records a missing recovery property: abrupt process loss after deletion
does not automatically restore the alias. It is not rollback, repair, crash
consistency, or cleanup admission. The observation remains three processes
under one principal and one parent-owned process tree. Cross-principal and
unrelated-process behavior, hostile simultaneous racing, durable intent,
quarantine, idempotency, typed recovery receipts, ReFS/SMB/other-host evidence,
Windows admission, and cleanup authority remain unresolved.

M187 adds no runtime API, protocol, decoder, CLI command, public probe,
production subprocess or native surface, adapter, cache access, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing Windows suite is the only future hosted execution path;
no hosted check is added.

## M188 Windows hard-link alias mutator abrupt-loss-after-recreate probe

M188 starts from fully locally validated M187 commit
`2f0869c3aeb632daa68a2e460f2b2cb3d34a1e7e`. It adds one Windows-only,
test-only [hard-link alias mutator abrupt-loss-after-recreate
probe](docs/security/cache-cleanup-windows-hard-link-alias-mutator-abrupt-loss-after-recreate-probe.md)
under RFC-0171.

The probe retains M186's fixed sibling mutator and M181's matching guardian.
After exact child-owned alias deletion, the parent sends the recreate token and
requires exact `recreated`, restored shared identity and bytes, link count two,
and range availability through both names. Before any close token, the parent
terminates and reaps the mutator, requires a nonzero exit and empty remaining
output, and verifies that the alias remains present with the same two-link
identity while the guardian remains live and protective.

This records negative rollback evidence: abrupt process loss after recreation
does not automatically restore the preceding one-link state. It is not durable
commit, recovery, crash consistency, or cleanup admission. The observation
remains three processes under one principal and one parent-owned process tree.
Cross-principal and unrelated-process behavior, hostile simultaneous racing,
durable intent, quarantine, reconciliation, typed recovery receipts,
ReFS/SMB/other-host evidence, Windows admission, and cleanup authority remain
unresolved.

M188 adds no runtime API, protocol, decoder, CLI command, public probe,
production subprocess or native surface, adapter, cache access, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing Windows suite is the only future hosted execution path;
no hosted check is added.

## M189 Windows hard-link alias mutator control-pipe EOF after recreation probe

M189 starts from fully locally validated M188 commit
`137442543d50f6795308372230c6677f34eec087`. It adds one Windows-only,
test-only [hard-link alias mutator control-pipe EOF after recreation
probe](docs/security/cache-cleanup-windows-hard-link-alias-mutator-control-pipe-eof-after-recreate-probe.md)
under RFC-0172.

The probe retains M186's fixed sibling mutator and M181's matching guardian.
After exact child-owned alias deletion, the parent sends the recreate token and
requires exact `recreated`, restored shared identity and bytes, link count two,
and range availability through both names. Before any close token, it closes
only the parent control writer and waits with the fixed bound for exact fixture
exit 5, stdout EOF, and empty stderr. The alias remains present with the same
two-link identity while the guardian remains live and protective.

This records negative rollback evidence: control-pipe EOF after recreation
does not automatically restore the preceding one-link state. It is not abrupt
process termination, durable commit, recovery, crash consistency, or cleanup
admission. The observation remains three processes under one principal and one
parent-owned process tree. Cross-principal behavior, inherited/duplicated
control writers, hostile simultaneous racing, durable intent, quarantine,
reconciliation, typed recovery receipts, ReFS/SMB/other-host evidence, Windows
admission, and cleanup authority remain unresolved.

M189 adds no runtime API, protocol, decoder, CLI command, public probe,
production subprocess or native surface, adapter, cache access, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing Windows suite is the only future hosted execution path;
no hosted check is added.

## M190 Windows hard-link alias mutator invalid control token after recreation probe

M190 starts from fully locally validated M189 commit
`2f7c61379ccd608a869c866e4937e7937906a64c`. It adds one Windows-only,
test-only [hard-link alias mutator invalid control token after recreation
probe](docs/security/cache-cleanup-windows-hard-link-alias-mutator-invalid-control-token-after-recreate-probe.md)
under RFC-0173.

The probe retains M186's fixed sibling mutator and M181's matching guardian.
After exact child-owned alias deletion, the parent sends the recreate token and
requires exact `recreated`, restored shared identity and bytes, link count two,
and range availability through both names. Before any close token, it writes
exactly one fixed invalid `?` byte, requires the buffered write to accept one
byte, flushes and closes the parent writer, and waits with the fixed bound for
exact fixture exit 5, stdout EOF, and empty stderr. The alias remains present
with the same two-link identity while the guardian remains live and protective.

This records negative rollback evidence: a fixed invalid control token after
recreation does not automatically restore the preceding one-link state. It is
not control-pipe EOF, abrupt process termination, arbitrary malformed-input
handling, durable commit, recovery, crash consistency, or cleanup admission.
The observation remains three processes under one principal and one parent-
owned process tree. Cross-principal behavior, inherited/duplicated control
writers, hostile simultaneous racing, durable intent, quarantine,
reconciliation, typed recovery receipts, ReFS/SMB/other-host evidence, Windows
admission, and cleanup authority remain unresolved.

M190 adds no runtime API, protocol, decoder, CLI command, public probe,
production subprocess or native surface, adapter, cache access, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing Windows suite is the only future hosted execution path;
no hosted check is added.

## M191 Windows hard-link alias mutator valid close prefix with trailing byte after recreation probe

M191 starts from fully locally validated M190 commit
`3d84bda9e41caf82a683e359210b7b9e74e9f8cc`. It adds one Windows-only,
test-only [hard-link alias mutator valid close prefix with trailing byte after
recreation
probe](docs/security/cache-cleanup-windows-hard-link-alias-mutator-valid-close-prefix-trailing-byte-after-recreate-probe.md)
under RFC-0174.

The probe retains M186's unchanged sibling mutator and M181's matching
guardian. After exact child-owned alias deletion and recreation, it writes the
fixed two-byte sequence `!?` once, requires both bytes accepted and flushed,
then requires exact `closed` while the parent writer remains open. The child
settles with exit 0, stdout EOF, and empty stderr. The alias remains present
with shared identity, bytes, and link count two while the guardian remains live
and protective.

This records bounded byte-prefix acceptance: the fixture reads the valid
leading close byte and does not reject the one trailing invalid byte. It is not
general message framing, arbitrary malformed-input handling, separate- or
partial-write evidence, durable commit, recovery, cleanup admission, or a
production protocol contract. The observation remains three processes under
one principal and one parent-owned process tree. Authenticated authority,
explicit framing, durable intent, reconciliation, cross-principal evidence,
ReFS/SMB/other-host evidence, Windows admission, and cleanup authority remain
unresolved.

M191 adds no runtime API, protocol, decoder, CLI command, public probe,
production subprocess or native surface, adapter, cache access, cleanup
authority, dependency, native extension, compiler requirement, version,
workflow job/allocation, permission, credential, release authority, or CI
change. The existing Windows suite is the only future hosted execution path;
no hosted check is added.

## Good-first contribution queue

These are issue-ready cards, not assigned work. A maintainer opens one with the
`good first issue`, `help wanted`, `status:ready`, and listed area labels before a
contributor starts.

| Card | Outcome | Scope | Acceptance |
| --- | --- | --- | --- |
| GF-01 glossary | Add a concise glossary for authority, canonical state, composition root, receipt, deterministic, presentation, and adapter | `docs/glossary.md`, `mkdocs.yml`; documentation only | Terms link to their defining guide/ADR; `uv run --frozen mkdocs build --strict` passes |
| GF-02 expected sample output | Add sanitized example JSON and explain stable versus diagnostic fields | `examples/README.md`; do not change sample behavior or protocols | Run the documented null examples and record matching output; docs build passes |
| GF-03 release checksum negative test | Add one focused test for an extra unlisted staged artifact | `tests/unit/test_release_artifacts.py`; no script/API change unless a demonstrated defect exists | Test fails against the intentional invalid fixture and full pytest passes |

Use the [good-first task form](.github/ISSUE_TEMPLATE/good_first_issue.yml) to propose
another card. The [triage contract](docs/triage.md) defines when it is ready.

## Proposal backlog

These areas remain uncommitted proposals and require milestone assignment plus the
design process in `GOVERNANCE.md`: nested prefab composition and live updates,
production audio,
rigid-body physics, network transports, international text shaping, automatic GPU
recovery. Constrained and general 3D are deferred under
[ADR-0028](docs/adr/0028-retain-layered-2d-and-defer-constrained-3d.md).
Visual-editor implementation is deferred under
[ADR-0029](docs/adr/0029-retain-headless-inspector-and-defer-visual-editor.md).
Executable WASM mods are deferred under
[ADR-0030](docs/adr/0030-retain-data-only-plugins-and-defer-wasm-mods.md).
Native acceleration is deferred under
[RFC-0001](docs/rfcs/0001-defer-first-native-kernel.md); its complete admission
and quantified revisit gate applies before another proposal.
