# Current task

- **Task:** M171 - prove two-way Windows exclusive-directory acquisition and
  refusal around one ordinary selected cache-root directory.
- **Status:** M171 is fully locally validated, DCO-committed, object-audited,
  and scratch-clean. Hosted `main` remains exact M99 and lacks M100-M170, so
  push and PR publication are safely withheld without a workflow allocation.
- **Base:** Fully locally validated M170 DCO commit
  `0c658d43886c986b129aa76dcc0ab413fd5cf618`, tree
  `24b543ba5c230e2d7907d03187c803db1290a731`, sole parent exact M169.
- **Branch:** `release/m171-windows-exclusive-root-acquisition`; exact
  containment allowed the redundant local M170 branch to be pruned.

## Acceptance boundary

- Accept RFC-0154 and retain one Windows-only, test-only, event-controlled
  two-way sharing-mode observation beneath pytest temporary storage.
- Preserve M149's native capability, M153's share-delete boundary, M155's
  fixed child/handshake, and M170's complete boundary byte-for-byte.
- Open one ordinary `live` directory with list/read-attribute/synchronize
  access, sharing mode zero, backup semantics, open-reparse-point behavior,
  and null security attributes. Reject reparse identity, own the handle, and
  prove it noninheritable.
- Require one fixed all-sharing child open to return false/error 32 while that
  owner remains live, then true/error zero after the exact owner closes.
- Reverse ownership with M155's unchanged fixed child. Require parent
  acquisition to raise the existing native error 32, adopt no handle, preserve
  the live child and content, then succeed only after exact `closed` and zero
  exit.
- Bound every child, stream, output, wait, and owner without sleeps, retries,
  shells, arbitrary commands, path input, or environment-selected behavior.
- Add no runtime API, public probe, cleanup authority, dependency, workflow,
  job/allocation, permission, release authority, or CI change.

## Direction evidence

- Microsoft documents that sharing mode zero prevents later read/write/delete
  opens, conflicting existing handles cause `ERROR_SHARING_VIOLATION`, sharing
  remains until close, and null security attributes make a handle
  noninheritable.
- Python exposes direct handle-inheritability inspection.
- GitHub documents that each matrix combination creates a job; M171 preserves
  the existing essential workflow and creates no hosted allocation.
- NIST SSDF remains risk-driven. The bounded current-host evidence slice is
  adopted; a complete quiescence design and Windows admission remain deferred.

## Development evidence so far

- Exact M170 was clean. The M149-M170 baseline passed 147 assertions with one
  established skip; static and dated strict governance returned zero findings.
  Hosted `main` remained exact M99 with no open PR.
- Seven architecture guards plus two live tests pass. The complete M149-M171
  boundary passes 156 assertions with one established capability skip. Twenty
  consecutive focused invocations pass all 40 live cases.
- The unchanged 46-package lock and exact 45-package graphics environment
  pass. All 525 Python files pass Ruff formatting, Ruff, and strict Pyright.
- Exact CPython 3.12.13 passes 3,839 tests with 17 skips; exact CPython 3.13.13
  and 3.14.5 each pass 3,839 tests with 18 skips.
- Ten real-wgpu tests, both one-repeat profile schemas, Clockwork Arena, and
  Agent World Builder pass with their established deterministic identities.
- Two development builds are byte-identical: a 360,880-byte pure wheel at
  SHA-256 `539aebac6aabe325fef9e6a6e6e6b66d38cf550f85a3473117501f15c62d25b5`
  and a 2,078,343-byte source archive at SHA-256
  `f6af972bbc63942e792f59dd534597ad7a3fe6e391705ae695e0eca05d941a45`.
  The primary smoke and all 27 additional isolated installed-wheel consumers
  pass.
- Two ten-artifact release stages are byte-identical and pass complete release
  smoke. Inventory is 114 wheel and 844 source entries, with zero native,
  WASM, bytecode, or hidden-control entry, zero M171 wheel entry, and all five
  exact M171 sources in the source archive.
- Static and 2026-08-29 dated strict governance each return zero findings.
  Protected surfaces have zero diff; public identity, credential, and local-
  path scans have zero match. Review corrected one inaccurate use of
  `parametrically`; no remaining actionable finding is known.

## Closeout

- Local implementation, validation, review, records, cleanup, DCO, and object
  gates are complete.
- Fresh hosted-state inspection found the preceding M100-M170 stack absent, so
  the authorized publication action was not safe and did not occur.
- Resume from this exact M171 commit for the next bounded milestone; prune M171
  only after its exact successor branch exists and contains it.

## Explicit non-scope

- A complete quiescence or lock protocol, attribute-only access, mapped files,
  oplocks, leases, descendants, arbitrary access/share combinations, multiple
  participants, cancellation, native close failure, crash recovery, or
  independent-host proof.
- Retained-root integration, candidate policy, cleanup receipts, finalization,
  quarantine recovery, platform admission, or a private production adapter.
- Runtime, CLI, world, command, receipt, ECS, renderer, asset, dependency,
  native-extension, compiler, workflow, permission, CI-allocation, publication,
  tag, release, or version changes.
