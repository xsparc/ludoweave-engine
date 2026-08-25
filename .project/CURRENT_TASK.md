# Current task

- **Task:** M121 - add bounded project-confined scene file loading.
- **Status:** Direction research, governance baseline, deliberate-red proof,
  implementation, focused behavior/type validation, installed-wheel verifier,
  public documentation, RFC-0104, focused architecture/docs, and findings-first
  review are complete. Complete source, supported-runtime, graphics,
  reproducible distribution, release rehearsal, package hygiene, and final
  scope/security qualification are complete. Record-inclusive separators,
  cleanup, history/hosted-state audit, and the final metadata separator are
  complete. The local DCO commit remains.
- **Base:** Fully locally validated M120 DCO commit
  `dbe8108abc29c93aed4317456ee67efb8b99e1ea`, tree
  `aa2e642ce931775f06f9bb36b34c6ee3ba8d5a22`, with sole parent exact M119.
  The stack remains unpublished under the existing public-review identity hold.

## Acceptance boundary

- Add one typed `HeadlessProject.load_scene()` method in the existing tools
  composition root; keep `ludoweave.scene` path- and transport-agnostic.
- Accept one bounded project-relative path and exact `SceneLimits`; reuse the
  established root confinement, regular-file check, sanitized diagnostics,
  descriptor ownership, metadata size check, and handle read cap.
- Delegate detached bytes to the unchanged `ludoweave.scene/1` decoder and
  return a detached immutable `SceneDocument` with no world mutation.
- Preserve explicit M119 planning and transaction application as the only
  instantiation/receipt boundary; do not resolve `asset://` dependencies.
- Add focused unit/property/architecture coverage, RFC-0104, aligned public
  docs, and a standalone installed-wheel load/compile/apply verifier.
- Keep command/operation registry, transaction service, workflows, allocations,
  actions, permissions, credentials, dependencies, lock, metadata, version,
  root API, scene/prefab schemas and planners, release authority, tags,
  releases, publication, and public remote state unchanged.

## Evidence so far

- A focused primary-source scan reviewed RFC 8089 plus current Python `pathlib`
  and `os` documentation. It supports reusing the existing project-root policy,
  explicit relative paths, bounded one-handle reads, and an explicit
  cooperative-filesystem rather than race-free-sandbox claim.
- Static and dated strict governance checks both began with zero findings.
- The first exact CPython 3.12.13 red run found the intended missing loader,
  verifier, and docs plus one test-only Hypothesis fixture health check. After
  declaring safe fixture reuse, the corrected red retained only the intended
  17 missing-capability/documentation failures, one protected-surface pass, and
  one platform symlink skip.
- The first implementation run passed all 14 executable loader assertions with
  one platform skip; focused formatting and strict Pyright found only a test
  layout and nested-fixture annotation. After correction, Ruff and strict
  Pyright pass and all 14 assertions pass with the one capability skip.
- Public docs and RFC-0104 now define confinement, format identity, detached
  ownership, handle lifetime, determinism, mutation/receipt separation,
  structured failures, threading, race limits, and complete non-scope.

## Explicit non-scope

- No directory discovery, prefab file loader, file URI, include/import graph,
  absolute/remote path, asset loading, source cache, watcher, live update,
  reimport, silent propagation, write-back, or race-free sandbox claim.
- No nested prefab change, `EntityRef` facade, arbitrary Python import or
  evaluation, global registry, scene/prefab persistent operation, renderer,
  provider, networking, editor, native compiler, or second authority.
- No workflow, hosted allocation, dependency, lock, metadata, version, root API,
  release authority, tag, release, publication, push, or PR.

## Remaining acceptance work

- Create the standalone DCO commit and verify its exact tree, parent, identity,
  scope, and clean worktree. Publication remains held.
