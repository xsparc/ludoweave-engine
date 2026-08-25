# Current task

- **Task:** M128 - add bounded asset-source lock generation and verification.
- **Status:** Direction/baseline proof, deliberate red, bounded lock values,
  project-confined streaming hashing, generation/verification CLI modes,
  RFC/public documentation, and documentation-inclusive focused proof are
  complete. Strengthened closure/descriptor and isolated installed-wheel proof
  pass. Findings-first review passes after one test-evidence correction. All
  complete validation, artifact, release, history, hygiene, cleanup, and final
  metadata gates pass. Exact staging, local DCO commit, and postcommit proof
  remain.
- **Base:** Fully locally validated M127 DCO commit
  `276d869b829735dcca7256cb73f190e15e84d9c0`, tree
  `6eb4384906e37bf708a90a542a8293b15b855d7e`, with sole parent exact M126.
  The stack remains unpublished under the existing public-review identity hold.
- **Branch:** `release/m128-asset-source-lock-verification`.

## Acceptance boundary

- Add strict immutable `ludoweave.asset-source-lock/1` values in the focused
  assets package, with tightening-only decode limits and canonical bytes.
- Bind the canonical M125 source-lock identity, canonical M126 asset-manifest
  identity, unique URI-sorted M127 direct roots, and the exact resolved asset
  set as URI/kind/source-byte-count/source-SHA-256 entries.
- Permit an empty roots/entries lock for valid source documents with no asset
  declarations; require every root to appear in the locked entries.
- Add read-only `ludoweave source asset-lock PROJECT --manifest FILE --assets
  FILE` generation and `source asset-verify ... --lock FILE` verification.
- Reuse unchanged project-confined source/asset readers and M127 closure. Read
  each selected asset source sequentially through the existing descriptor-
  bounded project reader; never disclose an asset source path.
- Limit one source to 256 MiB and accepted aggregate source bytes to 1 GiB.
  Produce no success bytes until all selected sources are hashed.
- Mismatch diagnostics disclose only the first stable field and optional
  logical asset URI, never expected/actual hashes, sizes, or paths.
- Prove generation and verification from an isolated no-dependency wheel.
- Document that a lock is repeatable input identity, not atomic filesystem
  snapshot, provenance, authenticity, decoding, build, import, or cache proof.
- Keep workflows, allocations, permissions, credentials, dependencies, lock,
  metadata, version, root API, scene/source formats, M127 report, world/runtime,
  release authority, and remote state unchanged.

## Direction and baseline evidence

- Primary sources accessed 2026-08-26: Unity 6.2 Asset Database and dependency-
  hash documentation, stable Godot import-process documentation, current Bazel
  remote-cache documentation, and Python 3.14 `hashlib` documentation. They
  distinguish source/input identity from imported or cached outputs and support
  explicit content hashing with caller-owned handle closure. They do not
  justify asset decode/build, automatic import/reimport, cache use/write,
  discovery, watchers, remote cache, or provenance claims.
- Exact M127 commit/tree/sole-parent, clean new branch, and `0 28` divergence
  pass. The focused M124-M127 asset/source/project/CLI baseline passes 119 tests
  with one established Windows symlink-capability skip in 4.24 seconds. Static
  and dated strict governance both report zero findings.
- Deliberate red stops behavior collection only on the absent focused exports;
  the M128 boundary produces three intended absent implementation/CLI/docs
  failures and two protected/evidence passes. No implementation pass is
  claimed.
- After import-order and test-fixture typing corrections, formatting, Ruff,
  strict Pyright, and 48 focused behavior assertions pass. Review replaced
  whole-file allocation with owned 64 KiB streaming hashing. The combined
  implementation/import/API boundary passes 115 assertions; only the
  intentionally absent M128 documentation assertion remains.
- RFC-0111 and public docs now define the exact lock, limits, ownership,
  failure, determinism, compatibility, and non-scope. The documentation-
  inclusive gate passes 164 assertions, statics, strict docs, dated governance,
  and whitespace.
- Generation succeeds with an absent declared-but-unselected source, selected
  source descriptors support a Windows rename round-trip after the command,
  and the isolated no-dependency wheel passes exact generation/verification.
- Findings-first review found and corrected that single closure-evidence
  weakness, then found no remaining actionable implementation issue.
- The complete source separator passes formatting for 405 Python files, Ruff,
  strict Pyright, 1,652 architecture assertions with one established skip,
  strict docs, both governance modes, and whitespace.
- Exact supported-runtime suites pass: 3.12.13 graphics has 3,362 passes and
  16 skips; 3.13.13 and 3.14.5 base each have 3,352 passes and 17 skips.
- Real-wgpu, fresh base/graphics profiles, Clockwork Arena, and Agent World
  Builder all pass and reproduce their established deterministic identities.
- Two initial builds reproduce; all eleven isolated wheel smokes and two byte-
  identical complete ten-artifact release rehearsals pass; archive inventory
  contains no native, WASM, bytecode, or retired control metadata.
- Exact 23-path scope, protected surfaces, backend/native/nondeterministic
  leakage, public tool identity, credentials, and whitespace all pass.
- The review-record-inclusive source, architecture, docs, governance, and
  whitespace separator passes. Final reproducible packages, all eleven wheel
  consumers, and both release rehearsals pass. History, refs, objects, and exact
  hosted non-publication state pass. Guarded cleanup removed all generated
  scratch. The final metadata/boundary separator passes and its explicit pytest
  root is absent.

## Explicit non-scope

- No asset payload decode, validation by kind, build, import, cache lookup,
  cache write, artifact creation, automatic reimport, watcher, or live update.
- No directory discovery, glob, default manifest, unused-asset rejection,
  build-inclusion policy, component-reference inference, or indirect
  redeclaration requirement.
- No atomic multi-file snapshot, signature, provenance, authenticity,
  authorization, freshness, or remote content identity claim.
- No source write, project write, world/session creation, command, transaction,
  world mutation, receipt, component registry, scene/prefab compilation, or
  runtime pipeline activation.
- No dependency, package metadata, version, engine-root export, workflow job or
  allocation, permission, credential, release authority, tag, release,
  publication, push, PR, or remote change.

## Remaining acceptance work

- Verify exact staging, create the single local maintainer-identity DCO commit,
  and run postcommit tree/parent/scope/divergence/worktree/object proof.
