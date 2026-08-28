# Current task

- **Task:** M173 - prove a cooperative Windows shared/exclusive coordination
  barrier over one fixed file identity and byte range.
- **Status:** Implementation, supported-Python regression, rendering, package,
  release rehearsal, documentation, governance, findings-first, evidence-
  inclusive source, artifact, record-only, cleanup, scope, and hygiene gates
  pass. The initial DCO object audit and hosted publication-safety gate pass.
  Publication is correctly withheld because hosted `main` lacks M100-M172;
  the final amended-object audit follows this factual record.
- **Base:** Fully locally validated M172 DCO commit
  `00eceb56246307f6fa57172fe674488189bfff4e`, tree
  `edd0f778ab9ced8f09145a4728b2e40a41651ef2`, sole parent exact M171.
- **Branch:** `release/m173-windows-cooperative-lock`; exact containment
  allowed the redundant local M172 branch to be pruned.

## Acceptance boundary

- Accept RFC-0156 and retain one Windows-only, test-only, current-host NTFS
  shared/exclusive `LockFileEx` observation over byte zero/length one of fixed
  ordinary `live/coordination.lock`.
- Preserve M172, runtime, examples, scripts, dependencies, workflows,
  metadata, and lock byte-for-byte.
- Use two fixed isolated shared participant children with generic-read/all-
  sharing opens, null security attributes, noninheritable handles, exact
  bounded `ready`/`closed` phases, explicit unlock, and deterministic close.
- Require an exclusive fail-immediate parent request to return native error 33
  while two shared owners remain, again after one closes, and to acquire only
  after the last owner closes.
- Reverse the order: require the exclusive owner to make a late shared child
  emit exact `refused`/33, then admit a fresh shared child after exact release.
- Record the exact positive boundary as cooperative only. It is not general
  exclusion, participant completeness, Windows admission, or cleanup authority.
- Add no runtime adapter, lock API, cleanup authority, dependency, workflow,
  job/allocation, permission, release authority, or CI change.

## Direction evidence

- Microsoft documents overlapping shared `LockFileEx` ranges, incompatible
  exclusive locks, fail-immediate requests, explicit unlock, termination-
  release caveats, and mapped-view noncoverage.
- Python exposes a narrower Windows `msvcrt.locking` surface, which is not
  treated as proof of the complete required shared/exclusive lifecycle.
- GitHub documents that each matrix combination creates another job. M173 uses
  the existing Windows suite and creates no hosted allocation.
- NIST SSDF remains risk- and outcome-driven. The smallest material next step
  is a bounded cooperative primitive, not runtime promotion.

## Development evidence so far

- Exact M172 was clean. The M149-M172 baseline passed 165 assertions with one
  established skip in 8.00 seconds; static and dated strict governance returned
  zero findings. Local `origin/main` remained exact M99.
- Eight architecture guards plus two live tests pass. The complete M149-M173
  boundary passes 175 assertions with one established capability skip. Twenty
  consecutive focused invocations pass all 40 live cases.
- The unchanged 46-package lock and exact 45-package graphics environment pass.
  All 531 Python files pass Ruff formatting, Ruff, and strict Pyright.
- Exact CPython 3.12.13 passes 3,858 tests with 17 skips; exact CPython 3.13.13
  and 3.14.5 each pass 3,858 tests with 18 skips.
- Ten real-wgpu tests, both one-repeat profile schemas, Clockwork Arena, and
  Agent World Builder pass with their established deterministic identities.
- Two development builds are byte-identical: a 361,025-byte pure wheel at
  SHA-256 `56614442ebfbaea633edfbf0860da022707e177d91aa6bfb83d492187ce1321f`
  and a 2,096,856-byte source archive at SHA-256
  `42251b3a98f94ef0e229ee7ee9a90e570723ec681dccc24b57990253d27ca1a4`.
  The primary smoke and all 27 additional isolated installed-wheel consumers
  pass.
- Two ten-artifact release stages are byte-identical and pass complete release
  smoke. Inventory is 114 wheel and 854 source entries, with zero native,
  WASM, bytecode, or hidden-control entry, zero M173 wheel entry, and all five
  exact M173 sources in the source archive.
- Static and dated strict governance return zero findings. Protected surfaces
  have zero diff and no remaining actionable review finding is known.

## Publication boundary

- Fresh hosted `main` is exact M99, no PR is open, and PR #251 is the latest
  merge. M173 is 74 commits ahead and includes the unpublished prerequisite
  stack. No push, PR, or hosted workflow is authorized until that stack is
  intentionally published or hosted `main` otherwise contains it.
- Audit the final amended object after this record; do not amend afterward.

## Explicit non-scope

- Uncooperative actors, coordination-file substitution or replacement,
  generation binding, complete retained roots, mapped views, multiple ranges,
  wait/fairness policy, cancellation, abrupt exit, delayed operating-system
  unlock, native close/unlock failure, filesystem variation, recovery, policy,
  receipts, or independent-host proof.
- Cache-root integration, candidate policy, cleanup authority, Windows
  admission, or a private production adapter.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, dependency,
  native-extension, compiler, workflow, permission, CI-allocation, tag,
  release, publication, or version changes.
