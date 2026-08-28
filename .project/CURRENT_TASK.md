# Current task

- **Task:** M172 - prove that M171's Windows zero-sharing directory owner does
  not recursively exclude a separately opened descendant file.
- **Status:** M172 is fully locally validated, scratch-clean, DCO-committed,
  and object-audited. Hosted `main` remains exact M99 and lacks M100-M171, so
  push and PR publication are safely withheld without a workflow allocation.
- **Base:** Fully locally validated M171 DCO commit
  `960efe770c48ddbfb925fd2cd7f9d220bca2e3ed`, tree
  `7ffa65efd2519c787a056e18d069bb561bb9764d`, sole parent exact M170.
- **Branch:** `release/m172-windows-descendant-non-exclusion`; exact
  containment allowed the redundant local M171 branch to be pruned.

## Acceptance boundary

- Accept RFC-0155 and retain one Windows-only, test-only, current-host NTFS
  observation around one ordinary `live/candidate.bin` descendant.
- Preserve M149, M155, M171, runtime, examples, scripts, dependencies,
  workflows, metadata, and lock byte-for-byte.
- Use one fixed isolated child that opens only the descendant for generic read
  with read/write/delete sharing, proves the native handle noninheritable,
  emits exact bounded `ready`/`closed` documents, and closes deterministically
  after one fixed release byte.
- Prove both acquisition orders: root owner before descendant holder and
  descendant holder before root owner. Require simultaneous live ownership,
  independent close, exact content, zero exit, and zero leaked parent owners.
- Record the exact negative capability: M171's owner is object-specific and is
  not a recursive subtree lock or complete quiescence primitive.
- Add no runtime adapter, lock, cleanup authority, dependency, workflow,
  job/allocation, permission, release authority, or CI change.

## Direction evidence

- Microsoft documents access/share compatibility for the named file or device;
  its kernel share checker receives the particular file object and associated
  share state. Neither contract grants recursive descendant exclusion.
- GitHub documents that each matrix combination creates another job. M172 uses
  the existing Windows suite and creates no hosted allocation.
- The smallest material next step is negative capability evidence, not runtime
  promotion of an incomplete quiescence primitive.

## Development evidence so far

- Exact M171 was clean. The M149-M171 baseline passed 156 assertions with one
  established skip. Hosted `main` remained exact M99 with no open PR.
- Seven architecture guards plus two live tests pass. The complete M149-M172
  boundary passes 165 assertions with one established capability skip. Twenty
  consecutive focused invocations pass all 40 live cases.
- The unchanged 46-package lock and exact 45-package graphics environment pass.
  All 528 Python files pass Ruff formatting, Ruff, and strict Pyright.
- Exact CPython 3.12.13 passes 3,848 tests with 17 skips; exact CPython 3.13.13
  and 3.14.5 each pass 3,848 tests with 18 skips.
- Ten real-wgpu tests, both one-repeat profile schemas, Clockwork Arena, and
  Agent World Builder pass with their established deterministic identities.
- Two development builds are byte-identical: a 360,956-byte pure wheel at
  SHA-256 `1fa1a84119c30634d5f7e48a8efe58dcc4168f6a8c9dd2f26b910af34b1453bd`
  and a 2,087,257-byte source archive at SHA-256
  `cc1583c6d03ef7e54b9667c7a845bec4fa8261900c4838b6f63e472dd66c61e2`.
  The primary smoke and all 27 additional isolated installed-wheel consumers
  pass.
- Two ten-artifact release stages are byte-identical and pass complete release
  smoke. Inventory is 114 wheel and 849 source entries, with zero native,
  WASM, bytecode, or hidden-control entry, zero M172 wheel entry, and all five
  exact M172 sources in the source archive.
- Static and dated strict governance return zero findings after correcting one
  mistaken repository-root invocation and sandboxing the dated uv cache read.
  Protected surfaces have zero diff and no remaining actionable review finding
  is known.

## Closeout

- Local implementation, validation, review, records, cleanup, DCO, and object
  gates are complete.
- Fresh hosted-state inspection found the preceding M100-M171 stack absent, so
  the authorized publication action was not safe and did not occur.
- Resume from this exact M172 commit for the next bounded milestone; prune M172
  only after its exact successor branch exists and contains it.

## Explicit non-scope

- Writes, deletes, mappings, descendant directories, multiple participants,
  oplocks, leases, cancellation, process death, native close failure,
  filesystem variation, recovery, policy, receipts, or independent-host proof.
- A complete participant/generation protocol, retained-root integration,
  candidate policy, cleanup authority, Windows admission, or private runtime
  adapter.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, dependency,
  native-extension, compiler, workflow, permission, CI-allocation, tag,
  release, publication, or version changes.
