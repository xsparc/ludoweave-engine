# Current task

- **Task:** M123 - add a bounded read-only scene/prefab source-check CLI.
- **Status:** Direction research, governance baseline, deliberate-red proof,
  implementation, focused behavior/type validation, installed-wheel verifier,
  RFC-0106, public documentation, and corrected focused architecture/docs are
  complete. Full source, supported-runtime, graphics, reproducible distribution,
  release rehearsal, package hygiene, and security/scope review are complete.
  Review-inclusive rebuild/release rehearsal and its source separator are
  complete. History and hosted-state validation plus bounded scratch cleanup
  are complete. The final record-inclusive source separator passes after one
  corrected governance-check target. The final post-record metadata separator
  passes. Exact scope, protected-surface diff, and regenerated-artifact cleanup
  pass. Only the final record check and local DCO commit remain.
- **Base:** Fully locally validated M122 DCO commit
  `176c21d12adc00c71cab63a777d0cd0eb6d66215`, tree
  `5d130ba83014145ccc398d119de71618bd2a943d`, with sole parent exact M121.
  The stack remains unpublished under the existing public-review identity hold.

## Acceptance boundary

- Add one nested standard-library `ludoweave source check PROJECT` adapter with
  mutually exclusive `--scene FILE` or `--prefab FILE --instance FILE` modes.
- Reuse the M121/M122 project-confined bounded loaders. Prefab mode validates
  exact source identity across two explicit files; no implicit pairing or
  discovery is allowed.
- Emit canonical `ludoweave.cli.source-check/1` JSON with source protocols,
  stable IDs, canonical SHA-256 identities, and bounded counts; never emit host
  paths.
- Preserve structured exit-2 failures for project/path/protocol/pair errors.
- Create no registry, world, or session; call no planner/transaction service;
  perform no compile or world mutation; produce no receipt; write no project
  file.
- Add focused integration/architecture coverage, RFC-0106, public docs, and a
  standalone installed-wheel CLI verifier.
- Keep workflows/allocations, permissions, credentials, dependencies, lock,
  metadata, version, root API, scene/prefab contracts/planners, release
  authority, tags, releases, publication, and public remote state unchanged.

## Evidence so far

- Primary sources accessed 2026-08-26 support explicit project/headless
  operation, separated validation, structured output, and exit 2; they do not
  justify arbitrary scripts, import/build, discovery, registry semantics, or
  cache/live-update policy.
- Exact M122 base and both governance modes validate with a clean worktree.
- Deliberate red produced nine intended absent-capability/docs failures and one
  protected-surface pass in 1.50 seconds.
- All six runtime integration cases passed immediately. Two test-only strict-
  typing inference gaps were corrected with explicit fixture annotations.
- A first docs-inclusive run found two literal boundary-test/prose mismatches;
  after formatting-insensitive matching and an explicit allocation sentence,
  Ruff and strict Pyright pass, all ten focused assertions pass in 1.46 seconds,
  strict docs pass in 1.66 seconds, and whitespace passes.
- The first installed no-dependency wheel proof passes for scene and explicit
  prefab-pair modes with expected stable identities.
- The stale M118 whole-CLI hash was narrowed to its actual Python-support
  surfaces; the corrected full architecture/source/docs/governance gate passes.
- Exact 3.12.13 passes 3,245 tests with 16 skips; exact 3.13.13 and 3.14.5 each
  pass 3,235 with 17 skips. Real-wgpu, both profiles, and both vertical slices
  pass.
- Two distributions are byte-identical; all six wheel smokes pass; two complete
  release stages are identical and pass; package/public identity/secret hygiene
  passes. Findings-first review of 18 paths found no actionable defect.
- The review-inclusive pair reproduces the 293,358-byte wheel and a 1,623,354-
  byte sdist; all six wheel smokes, two identical ten-artifact release stages,
  both release smokes, and package hygiene pass.
- Stacked history, DCO/identity, Git integrity, local/remote branch inventory,
  authentication, and empty M123 PR/run/release/tag state all validate.

## Explicit non-scope

- No compile, component registry or semantic component validation, asset
  resolution, world/session creation, command, transaction, mutation, receipt,
  or project output file.
- No directory discovery, recursion/glob, extension routing, implicit pairing,
  manifest lookup, cache, watcher, live update/reimport, write-back, arbitrary
  script/import/evaluation, file URI, or remote path.
- No dependency, lock, metadata, version, root API, workflow job/allocation,
  hosted runner, release authority, tag, release, publication, push, or PR.

## Remaining acceptance work

- Run final record-inclusive source/governance separators.
- Clean exact scratch targets; verify stacked history, remote/hosted state,
  identity, DCO, protected surfaces, and final scope.
- Create the standalone DCO commit and verify its exact tree, parent, identity,
  scope, and clean worktree. Publication remains held.
