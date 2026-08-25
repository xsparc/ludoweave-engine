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
hosted runner change. One-level prefab fragments and explicit instantiation
commands remain future assigned work under a separate acceptance boundary.

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
design process in `GOVERNANCE.md`: scene file loading, prefab composition and
live updates, production audio,
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
