# Current task

- **Task:** M137 - inspect the complete engine-owned local asset cache through
  a bounded deterministic read-only inventory.
- **Status:** Implementation, documentation, focused/complete behavior,
  supported-Python, static, architecture, governance, real-wgpu, retained
  profile, vertical-slice, findings-first, record-inclusive reproducibility,
  all installed-wheel consumers, release rehearsal, scope/security review,
  bounded cleanup, history/hosted audit, and final metadata separation pass.
  M137 is ready for the authorized local DCO commit.
- **Base:** Fully locally validated M136 DCO commit
  `d090131871594c8d49410c8d66e101376c010acc`, tree
  `c4b2e3fb3c85330fb45730649410a1b83b3d0433`, with sole parent exact M135.
  The stack remains unpublished under the existing public-review identity
  hold.
- **Branch:** `release/m137-bounded-asset-cache-inventory`.

## Acceptance boundary

- Inspect only the complete engine-owned `actions/` and `cas/` cache layout
  through one read-only `AssetCacheStore` without creating an absent cache.
- Apply hard entry, metadata-byte, and CAS-byte limits; classify directory
  entries without following links/reparse points; and process admitted names
  in deterministic sorted order.
- Strictly reconstruct exact canonical action metadata, bind each record to its
  location and cache key, verify every CAS blob by streamed size and digest,
  and require action-to-blob closure.
- Compare the exact current saved plan against all verified storage and return
  immutable path-free counts for current-plan, missing, other-action, and
  no-action-reference blobs.
- Treat "no action reference" as an observation only, never deletion,
  eviction, garbage-collection, or retention eligibility.
- Add `source asset-cache-inventory`, isolated-wheel proof, RFC-0120, public
  documentation, and architecture enforcement while keeping workflows,
  dependencies, metadata, version, engine root, release authority, and prior
  cache contracts unchanged.

## Direction and evidence so far

- Primary sources accessed 2026-08-27: current Bazel remote-caching, Gradle
  9.7.1 cache-directory/cleanup, and Python 3.12 `os.scandir`/`DirEntry`
  documentation. They support separating action/CAS inspection from cleanup
  policy and explicit no-follow classification.
- Exact M136 commit/tree/parent and clean baseline passed before branch
  creation. The additive inventory, CLI, tests, installed smoke, RFC-0120, and
  public docs are present while protected prior surfaces, dependencies,
  metadata, workflows, and CI allocations remain exact.
- Review hardened deterministic bounded collection, current-plan cache-key
  uniqueness, pre-open aggregate budgets, race-growth read bounds, exact
  canonical metadata, and the maximum valid CAS artifact budget.
- All 442 Python files are format-clean; Ruff and strict Pyright pass; strict
  docs and whitespace pass; 1,694 architecture assertions pass with one
  established Windows capability skip; both governance modes return zero
  findings.
- Accepted suites pass 3,525 tests with 16 skips on exact CPython 3.12.13 and
  3,515 tests with 17 skips on exact CPython 3.13.13 and 3.14.5.
- All ten real-wgpu tests, eight M7 profile assertions, Clockwork Arena, Agent
  World Builder, and 1,727 selected exact-tree assertions with one established
  skip pass. The initial isolated inventory consumer passes against a
  342,498-byte pure wheel at SHA-256
  `3d43bba54ddb70dcf3b74295475019407d395e2914f87215a2bcc61b97934ed3`.

## Explicit non-scope

- No cache creation, publication, write, repair, deletion, eviction, garbage
  collection, quota enforcement, retention decision, migration, or snapshot
  claim under hostile concurrent mutation.
- No remote cache, network, authentication, authorization, signature,
  attestation, provenance/authenticity claim, shared writer, or external
  provider.
- No decoder, fallback, source acquisition, discovery outside the fixed cache
  layout, watcher, reimport, scheduler, worker, process, thread, parallelism,
  callback, plugin, dynamic import, or arbitrary evaluation.
- No renderer upload, source/project write-back, world/session mutation,
  receipt, dependency, native/backend surface, metadata, version, engine-root
  API, workflow/job/allocation, permission, credential, release, publication,
  push, PR, or remote change.

## Remaining acceptance work

- Create the authorized local DCO commit and prove it postcommit. Do not push or
  create a PR while the public-review identity hold remains.
