# Current task

- **Task:** M116 - separate sample-bundle semantic portability from byte
  identity.
- **Status:** M115 commit/cleanup verification, primary-source research, exact
  supported-runtime producer-consumer probing, implementation, complete local
  qualification, and initial artifact qualification are complete. Independent
  findings-first review has no actionable finding. Review-inclusive artifact
  qualification passes. Final source/history/hosted-state/precommit separators,
  are in progress: the corrected final source separator passes. History and
  hosted-state audit passes. Post-audit/precommit separators, commit, and
  cleanup remain. The post-audit separator passes; final precommit metadata
  verification also passes. All local M116 qualification is complete; commit
  and cleanup remain.
- **Base:** Fully locally validated M115 DCO commit
  `b16e5dc0b1f2b67edddce36e3e7ae10799467da1`, tree
  `b3877bf9a11cddbb4dca28cc5a8488ff29cfaf68`, with sole parent exact M114.
  The stack remains unpublished under the existing public-review identity hold.

## Acceptance boundary

- Separate sample-bundle semantic portability from byte identity: supported
  runtime producers may emit different valid Deflate bytes while supported
  consumers extract the same fixed source-defined sample tree.
- Record the exact Windows CPython 3.12.13/3.13.13/3.14.5 3x3 producer-
  consumer compatibility matrix without inferring cross-platform proof.
- Keep method `8`, M64/M95/M113 method policy, M114 level non-observability,
  M115 fixed-environment byte scope, exact release checksums, and diagnostic
  order unchanged.
- Add RFC-0099, one focused architecture contract, and aligned public,
  security, architecture, release, roadmap, maintainer, and factual project
  records.
- Keep workflows, runner allocation, actions, permissions, credentials,
  dependencies, lock, version, verifier/runtime scripts, sample producer,
  runtime package/API, release authority, tags, releases, publication, and
  public branch state unchanged.

## Evidence so far

- M115 is exact standalone DCO commit
  `b16e5dc0b1f2b67edddce36e3e7ae10799467da1`, tree
  `b3877bf9a11cddbb4dca28cc5a8488ff29cfaf68`, sole parent M114, exact
  maintainer identity, one sign-off, 15 intended paths, and `0 16` divergence.
  Twelve audited M115/test scratch targets were removed and zero remain.
- PKWARE assigns ZIP compression method `8` to Deflate. Python documents
  `ZIP_DEFLATED` as the usual ZIP compression method and uses the available
  zlib-compatible module. Python 3.14 reports no known incompatibility from its
  default Windows zlib-ng change; zlib-ng documents a zlib-compatible API.
- The ignored producer/consumer probe is format- and Ruff-clean.
- Exact Windows CPython 3.12.13, 3.13.13, and 3.14.5 each produced the fixed
  sample bundle. Every runtime consumed all three bundles through complete
  extraction: all nine combinations passed and extracted 50 files. The
  canonical extracted-tree SHA-256 was
  `eb4089dc35539baa9af95c757da9172506d61b6d45ab19d5ad5d8740b77a9ed0`
  in every combination. The
  3.12/3.13 archive remained 111,168 bytes at SHA-256
  `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`;
  the 3.14 archive remained 111,413 bytes at SHA-256
  `d592e99c8c3a65ae63f0cf89ed7eff6094365ca98ba58d08c2099fac4316834b`.
- The first focused-contract format check found one mechanical formatting
  change; Ruff formatting corrected it and lint passed.
- The exact CPython 3.12.13 deliberate-red contract passed five behavior,
  compressor-representation, producer, checksum-separation, and protected-
  surface assertions and failed only the intended absent-documentation
  assertion in 0.32 seconds.
- RFC-0099 now records one sample-bundle semantic-portability decision. No
  runtime, workflow, producer, verifier, manifest, dependency, lock, or public
  API change is introduced.
- All six focused assertions pass on exact CPython 3.12.13, 3.13.13, and
  3.14.5. The unchanged lock, 359-file format check, Ruff, strict Pyright,
  1,595 architecture assertions with one established Windows capability skip,
  strict docs, protected surfaces, and whitespace pass.
- Complete suites pass 3,135 tests with 15 skips on exact CPython 3.12.13 with
  graphics and 3,125 tests with 16 skips on exact CPython 3.13.13 and 3.14.5
  base environments. The first 3.14.5 process was interrupted and supplies no
  result; the clean rerun supplies the stated pass.
- All ten real-wgpu tests, fresh base/graphics profiles, Clockwork Arena, and
  Agent World Builder pass with the established deterministic identities.
- Two initial builds reproduce a 278,345-byte pure wheel at SHA-256
  `0d399846d6222fa62c5a7dfd84c4344bf5268f597d2f617cd88804adb0df153c`
  and a 1,542,886-byte source archive at SHA-256
  `2e9b7fe85ca29c5bb845a3aa9dcc578b325b2c2d40bd2286948e4b75bc20bbd3`.
  Wheel smoke, twice-staged ten-artifact byte identity, complete release smoke,
  and 94/598-entry package hygiene pass.
- Findings-first review covers exactly 15 intended paths. Protected workflows,
  producer, verifier, reproducibility script, metadata, lock, runtime package/
  API, dependencies, version, and release authority have zero diff. Public
  tool-identity, high-confidence secret, package-hygiene, and whitespace scans
  are clean; no actionable finding remains.
- Review-inclusive builds reproduce the unchanged 278,345-byte pure wheel at
  SHA-256
  `0d399846d6222fa62c5a7dfd84c4344bf5268f597d2f617cd88804adb0df153c`
  and a 1,544,475-byte source archive at SHA-256
  `69e4adf74f2b5425b5cedbe45b692ec8f4ba63b266b93c4f5571668ab1f96b41`.
  Reproducibility, isolated-wheel smoke, twice-staged ten-artifact byte
  identity, complete release smoke, and 94/598-entry package hygiene pass.
- Corrected final source separator passes the unchanged 46-package lock,
  359-file formatting, Ruff, strict Pyright, strict docs, protected surfaces,
  whitespace, all 1,595 architecture assertions with one established Windows
  capability skip, and all 11 focused M59/M116 assertions.
- The precommit audit confirms exact M115 head/tree/parent, exact M99 local and
  remote `main`, `0 16` divergence, the linear M100-M115 stack, 15 intended
  paths, exact maintainer identity and DCO sign-off across all 16 stacked
  commits, protected-surface integrity, and required-only branch inventory.
  Full Git checking reports 44 dangling-only lines and zero critical finding;
  GitHub reports no M116 PR/run, release, or tag. No hosted Actions allocation
  was triggered.
- The post-audit separator passes strict docs, all 11 focused M59/M116
  assertions, protected-surface integrity, whitespace, exact 15-path scope,
  and public tool-identity/high-confidence secret scans.
- The final precommit metadata separator passes all 11 focused assertions in
  0.50 seconds and whitespace after the post-audit task-state update.

## Explicit non-scope

- No alternate compression method, new decoder, recompression, runtime branch,
  digest allowlist, cross-runtime byte identity, cross-platform proof, or
  general ZIP interoperability claim.
- No workflow, allocation, dependency, producer, runtime package/API, native/
  WASM, version, release authority, tag, release, publication, push, or PR.

## Remaining acceptance work

- Commit and perform bounded scratch cleanup.
