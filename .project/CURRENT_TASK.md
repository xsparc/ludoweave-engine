# Current task

- **Task:** M126 - add bounded project-confined asset-manifest loading.
- **Status:** Direction research, exact M125 base/governance proof, deliberate
  red, implementation, public documentation, complete source and supported-
  runtime suites, graphics/vertical samples, initial reproducible artifacts,
  installed-wheel/release rehearsals, hygiene, and findings-first hardening are
  complete. Final record-inclusive artifacts, cleanup, history/hosted audit,
  and post-record separators pass. Exact staging, local DCO commit, and post-
  commit verification remain.
- **Base:** Fully locally validated M125 DCO commit
  `cc440c84dbc53a07b5640ca46410e461fe686cb0`, tree
  `9b9daea68cc32d13a1ba03575ca58db0d511698a`, with sole parent exact M124.
  The stack remains unpublished under the existing public-review identity hold.
- **Branch:** `release/m126-project-confined-asset-manifest-loading`.

## Acceptance boundary

- Retain exact `ludoweave.assets/1` fields and existing path-based loader.
- Add focused experimental `ASSET_MANIFEST_PROTOCOL` and immutable slotted
  `AssetManifestLimits`; keep the engine root unchanged.
- Enforce tightening-only 4 MiB, 4,096-asset, 256-dependency, and 128-setting
  hard maxima plus unique UTF-8 finite JSON.
- Add deterministic `AssetManifest.from_json()`, `as_dict()`, and
  `canonical_bytes()` while retaining existing URI/source/dependency/cycle
  validation and empty-manifest compatibility.
- Make existing `AssetManifest.load()` use one bounded closed handle and the
  same decoder.
- Add internal `HeadlessProject.load_asset_manifest()` through the established
  project-confined bounded reader.
- Prove the focused exports and loader from an isolated no-dependency wheel.
- Document ownership, determinism, compatibility, cooperative confinement, and
  the deferred source-to-asset dependency-resolution boundary.
- Keep CLI, source/lock behavior, workflows/allocations, permissions,
  credentials, dependencies, lock, metadata, version, engine root, world,
  release authority, tags, releases, publication, and remote state unchanged.

## Evidence so far

- Primary sources accessed 2026-08-26: current stable Godot `ResourceLoader`,
  Unity `AssetDatabase.GetDependencies`, current PyPA `pylock.toml`, and JSON
  Schema Draft 2020-12 validation. They distinguish dependency documents and
  direct/recursive inspection from broader import/cache systems, support
  explicit versions and deterministic ordering, and leave semantic resolution
  to application code. Confidence is high for the loader foundation only.
- Exact M125 commit/tree/sole-parent, clean status, and `0 26` divergence pass.
  Thirty-one asset/project/M125 baseline assertions pass with one established
  symlink-capability skip; both governance modes return zero findings.
- Deliberate red: the unit module failed collection only on absent public
  exports; four absent contract/loader/verifier/docs assertions failed and one
  protected-surface assertion passed.
- The first combined implementation patch was rejected atomically because it
  targeted one file in two update blocks; no file changed. Split patches
  applied the same design.
- The first implemented checkpoint formatted three files and passed Ruff;
  strict Pyright found six annotation-only decoded-container gaps and stopped
  before behavior.
- After explicit container annotations, six files are format-clean, Ruff and
  strict Pyright pass, and 32 focused asset/project assertions pass with one
  established symlink-capability skip in 0.39 seconds.
- Ten retained/protected implementation assertions pass; only the deliberately
  absent documentation assertion fails before docs.
- The first pure package build succeeds. Its isolated no-dependency wheel
  verifies the two new focused experimental exports and project loader, returns
  two URI-sorted entries, canonical SHA-256
  `sha256:c8d712bf64a1efb9860674e4b00e5200cd00852dd02276d351ef808df4ff01dd`,
  and proves both asset sources remain absent.
- RFC-0109 and public docs define exact limits, bounded ownership, canonical
  ordering, retained compatibility, cooperative confinement, and explicit
  loader-only non-scope.
- The first documentation-inclusive gate stopped only on one mechanical test
  wrap. After formatting, all 396 files, Ruff, strict Pyright, 46 focused
  assertions with one established skip, strict docs, dated governance, and
  whitespace pass.
- Findings-first review hardened parse-time exponent-overflow rejection and
  above-hard-max diagnostics, then added frozen/slotted, dependency/setting cap,
  and closed-descriptor regressions. All 47 corrected focused assertions pass
  with one established skip; statics and whitespace pass.
- The complete source separator passes the unchanged lock, all 396-file
  formatting, Ruff, strict Pyright, 1,642 architecture assertions with one
  established skip, strict docs, both governance modes, and whitespace.
- Exact CPython 3.12.13 with graphics passes 3,323 tests with 16 skips; exact
  3.13.13 and 3.14.5 base environments each pass 3,313 with 17 skips. Every
  invocation selected and printed its exact runtime.
- The restored exact 45-package 3.12.13 graphics environment passes all ten
  real-wgpu tests. Both one-repeat profiles validate, and both vertical samples
  reproduce their established deterministic identities and acceptance fields.
- Two initial builds reproduce exact wheel/source bytes. All nine isolated
  no-dependency wheel smokes pass, two complete ten-artifact release stages are
  byte-identical and pass release smoke, and package/repository hygiene passes.
- Final adversarial review rejects surrogate-bearing source/setting text and
  NUL source paths before canonical encoding or filesystem use. Static checks,
  whitespace, and 48 focused assertions with one established skip pass.
- The record-inclusive source separator passes after two factual uv-cache-only
  sandbox corrections. Exact CPython 3.12.13 with graphics then passes 3,324
  tests with 16 established skips on the hardened recorded tree.
- Final fresh builds reproduce exact wheel/source bytes; all nine isolated
  wheel smokes, two byte-identical complete release stages and smokes, archive
  hygiene, exact 18-path scope, protected-surface, public identity, credential,
  and whitespace checks pass.
- Fetch/prune and corrected history checks prove the exact linear signed local
  stack, only remote main, and zero critical Git finding. Read-only hosted
  queries return no M126 branch, PR, run, tag, or release.
- All 13 audited generated targets are absent after guarded ordinary cleanup
  and one exact-target elevated retry for Windows-denied `.pytest-tmp`.
- The final factual source separator passes lock, all-source formatting, Ruff,
  strict Pyright, 1,642 architecture assertions with one established skip,
  strict docs, both governance modes, and whitespace.
- The corrected absence-aware post-record separator passes six-file statics,
  strict Pyright, ten M59/M126 assertions, dated governance, protected scope,
  exact 18-path inventory, identity/credential scans, and zero scratch.

## Explicit non-scope

- No directory discovery, recursion, glob, suffix routing, default-manifest
  lookup, source-manifest integration, or source-to-asset dependency check.
- No asset source read, payload decode, asset build, cache use/write, import,
  component resolution, scene/prefab compile, or dependency traversal.
- No watcher, automatic reimport, live update, source write-back, arbitrary
  import/evaluation, file URI, remote access, or hostile-filesystem guarantee.
- No world/session, command, transaction, world mutation, receipt, renderer,
  provider, dependency, lock, metadata, version, engine-root API, CLI, workflow
  job/allocation, permission, credential, release authority, tag, release,
  publication, push, PR, or remote change.

## Remaining acceptance work

- Complete exact staging, local DCO commit, and post-commit verification.
