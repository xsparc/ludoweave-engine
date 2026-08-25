# Current task

- **Task:** M124 - add bounded explicit source-manifest checking.
- **Status:** Direction research, exact-base/governance proof, deliberate red,
  immutable manifest implementation, project-confined loading, aggregate CLI
  checking, focused behavior/static validation, installed-wheel proof,
  RFC-0107, public documentation, and corrected complete source/architecture/
  governance validation are complete. All supported-runtime suites, real-wgpu,
  profiles, both vertical slices, reproducible distributions, all seven
  installed-wheel paths, deterministic release rehearsal, and package/security
  hygiene are complete. Findings-first scope/API review and corrected installed
  focused-API proof plus review-inclusive rebuild/release rehearsal are
  complete. The final factual source separator and precommit local/hosted
  history audit also pass. Exact scratch cleanup and the record-inclusive source
  separator are complete. The final metadata/scope separator and its bounded
  regenerated-output cleanup pass; only local DCO-commit evidence remains.
- **Base:** Fully locally validated M123 DCO commit
  `1b092a85487b355fac688e15daeaed0ebcfa665a`, tree
  `7f71d824ee30fd7cbc7b996aa6913f0b0a1a2074`, with sole parent exact M122.
  The stack remains unpublished under the existing public-review identity hold.

## Acceptance boundary

- Add exact bounded `ludoweave.source-manifest/1` values in the focused
  `ludoweave.scene` package; keep the engine root unchanged.
- Require one stable manifest ID and 1-256 canonically entry-ID-ordered explicit
  scene or prefab source/instance entries.
- Require stable unique entry IDs, reject exact duplicate references, and use
  normalized forward-slash project-relative paths with hard byte limits.
- Add one internal `HeadlessProject.load_source_manifest()` method that reuses
  existing project confinement, bounded reads, and detached ownership.
- Add mutually exclusive `ludoweave source check PROJECT --manifest FILE`.
- Reuse M121/M122 readers for every listed source and validate exact prefab
  source/instance identity.
- Emit canonical `ludoweave.cli.source-manifest-check/1` JSON with normalized
  manifest/source hashes, ordered entry results, bounded totals, and no paths.
- On any failure emit no success report, leave the project tree unchanged, and
  retain structured exit-2 behavior.
- Add unit, integration, architecture, installed-wheel, RFC, and public-doc
  evidence.
- Keep workflows/allocations, permissions, credentials, dependencies, lock,
  metadata, version, engine root, existing scene/prefab contracts/planners,
  release authority, tags, releases, publication, and remote state unchanged.

## Evidence so far

- Current primary sources support explicit project/profile batch boundaries,
  structural bounded lists, canonical JSON, nested CLI arguments, and SHA-256;
  they do not justify discovery, arbitrary execution, or compile semantics.
- Exact M123 base and both governance modes pass with a clean worktree and
  `0 24` divergence.
- Deliberate red produced five intended absent-capability/docs failures and one
  protected-surface pass in 0.21 seconds.
- The first implementation checkpoint passed Ruff but strict Pyright found one
  redundant runtime cast and three test-only immutable-detail/negative-typing
  issues. The corrected checkpoint passes strict typing and all 22 unit and
  integration cases in 1.26 seconds.
- The implementation boundary then passed five assertions and failed only the
  intentionally absent docs assertion. The initial isolated no-dependency
  installed-wheel manifest check passes.
- RFC-0107 and public docs define limits, ownership, failure, deterministic
  normalization, non-atomic multi-file reads, compatibility, and non-scope.
  All 28 focused assertions pass in 1.29 seconds; strict docs pass in 1.61
  seconds with the known Material notice; formatting, Ruff, strict Pyright, and
  whitespace pass.
- The complete source separator passes after mechanically formatting one new
  assertion and narrowing two stale historical exact-package inventories:
  1,631 architecture assertions pass with one established skip; lock,
  formatting, Ruff, strict Pyright, strict docs, both governance modes, and
  whitespace pass.
- Exact CPython 3.12.13 passes 3,277 tests with 16 skips; exact 3.13.13 and
  3.14.5 each pass 3,267 with 17 skips. The ten real-wgpu tests, base/graphics
  profiles, Clockwork Arena, and Agent World Builder reproduce their
  established passing identities.
- Two independent builds reproduce a 297,737-byte pure wheel and 1,636,936-byte
  source archive. All seven wheel smokes pass; two complete ten-artifact stages
  are byte-identical and pass. Package/native/control-metadata and repository
  identity/secret hygiene scans are clean.
- Review covers exactly 26 intended paths, finds no remaining actionable issue,
  and confirms zero protected-surface diff. The corrected isolated-wheel
  verifier directly checks the four new experimental `ludoweave.scene` exports
  as well as the CLI; strict typing and all 32 focused assertions pass.
- The review-inclusive pair preserves the 297,737-byte wheel and produces a
  reproducible 1,638,466-byte source archive; all seven wheel smokes, both
  byte-identical ten-artifact stages, both release smokes, and package hygiene
  pass.
- The final factual source separator passes the unchanged lock, all 388 Python
  files, Ruff, strict Pyright, 1,631 architecture assertions with one
  established skip, strict docs, both governance modes, and whitespace.
- Local/remote main and the merge base remain exact M99. The 24-commit
  M100-M123 stack is linear, single-parent, exact-identity, and singly
  DCO-signed; full Git checking has only the established 287 dangling records.
  Hosted M124 branch, PR, run, release, and tag queries are empty.
- All 13 exact M124 build, release, profile, docs, and pytest scratch targets
  were verified confined, untracked, and non-reparse, then removed. Ordinary
  access removed 12; a separately verified elevated retry removed only the
  access-denied `.pytest-tmp`; the remaining count is zero.
- The cleanup-record-inclusive separator passes the unchanged lock, all 388
  Python files, Ruff, strict Pyright, 1,631 architecture assertions with one
  established skip, strict docs, both governance modes, and whitespace.
- All 25 final metadata and M119/M120/M123/M124 boundary assertions pass.
  Dated strict governance, exact 26-path scope, protected-surface isolation,
  public-identity hygiene, high-confidence credential hygiene, and whitespace
  pass. The two regenerated outputs were verified and removed exactly.

## Explicit non-scope

- No directory discovery, recursion, glob, suffix routing, implicit pairing,
  project-manifest source registry, import graph, or asset database.
- No compile, application component registration or semantic validation, asset
  load, world/session creation, command, transaction, mutation, receipt, or
  report file.
- No atomic filesystem snapshot, cache, watcher, live update/reimport,
  write-back, arbitrary script/import/evaluation, file URI, or remote access.
- No dependency, lock, metadata, version, engine-root API, workflow job or
  allocation, hosted runner, release authority, tag, release, publication,
  push, PR, or remote change.

## Remaining acceptance work

- Create the standalone local DCO commit and verify its exact tree, parent,
  identity, scope, and clean worktree. Publication remains held.
