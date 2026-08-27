# Current task

- **Task:** M144 - derive the unchanged path-free unreferenced-blob preview
  offline from one strictly admitted saved cache fingerprint.
- **Status:** M144 implementation, complete local acceptance, installed-wheel
  proof, reproducibility, release rehearsal, findings-first review, bounded
  cleanup, DCO commit, and fresh publication-eligibility audit are complete.
  Publication is held because authoritative hosted `main` remains exact M99.
- **Base:** Fully locally validated M143 DCO commit
  `1e9eedd5307d3c1249fe1dcd2b22acf4a01ccfc2`, tree
  `a2320515ef4e97b5d4be3a9091dd6f90a11ad86b`, with sole parent exact M142.
- **Branch:** `release/m144-offline-unreferenced-blob-preview`.

## Acceptance boundary

- Add `source asset-cache-fingerprint-record-preview` as a composition root
  only. Preflight current sources, the saved lock, and exact regenerated plan
  before resolving or reading one project-relative fingerprint record.
- Reuse M139's exact 65,536-byte hard maximum, project-confinement/no-follow
  reader, strict canonical decoder, exact schema, and aggregate bounds.
- Pass the exact plan and admitted fingerprint to the unchanged pure M143
  function and emit the unchanged
  `ludoweave.asset-cache-unreferenced-preview/1` bytes with exit 0.
- Prove stable read-only operation after the originating cache is absent,
  wrong-plan rejection, current-input preflight before record access,
  path/object-identity silence, isolated installed-wheel behavior, strict docs,
  and architecture protection.
- Preserve M137-M143 protocols/bytes, cache layout, fingerprint admission,
  workflows, dependencies, version, engine-root API, and release authority.
- State explicitly that an unsigned offline record supplies neither current
  cache state nor chronology, freshness, authenticity, provenance, trusted
  timestamp, or deletion eligibility.

## Direction and evidence so far

- Primary sources accessed 2026-08-27: RFC 8785, Python 3.12 JSON decoder,
  SLSA 1.2 artifact verification, and GitHub workflow-trigger guidance. They
  support reuse of one strict canonical admission path, require separate trust
  policy for authenticity, and provide no reason to change quota-conscious CI.
- Exact M143 commit/tree/parent, clean worktree, maintainer identity, DCO, and
  object integrity were established before the neutral M144 branch was created.
  Exact ancestry proved the redundant M143 branch was contained and it was
  pruned; only local `main` and active M144 remain.
- The CLI parser/dispatch/composition and three offline integration cases are
  format/Ruff/strict-Pyright clean. The first pytest attempt stopped before
  product setup because the cleaned `.tmp` parent was absent; after recreating
  that ignored parent, all three cases passed with 42 deselected in 6.88
  seconds.
- The initial wheel built, but its smoke fixture retained the CLI presentation
  newline and was correctly rejected as noncanonical. Persisting exact
  canonical record bytes fixed the fixture. The corrected script is format/
  Ruff/strict-Pyright clean and its isolated no-dependency consumer passes.
- The corrected initial pure wheel is 355,497 bytes at SHA-256
  `436e5542bc0bc3a3fb57cf5fcacab19204fd38a3285d8b08e4ac2374d7643f7c`;
  its pre-record source archive is 1,867,734 bytes at SHA-256
  `bdacb4814433a3ddf733b02c6d674b0a23a92623a20efa97179ec885e49ed8a7`.
- Complete static, architecture, docs, and governance gates pass: 466 Python
  files are format-clean, Ruff and strict Pyright are clean, all 1,731
  architecture assertions pass with one established skip, and both governance
  modes report zero findings.
- Exact CPython 3.12.13 passes 3,654 tests with 16 established skips; fresh
  exact CPython 3.13.13 and 3.14.5 each pass 3,644 with 17 skips. All ten
  real-wgpu tests, both profiles, and both deterministic vertical slices pass
  with their established identities.
- Two record-inclusive builds reproduce a 355,539-byte pure wheel at SHA-256
  `51d5ce7187cff20429f40374b8cfaa923a24e3b8686006da837961ccfbb6fc47`;
  all 27 installed consumers pass, and two byte-identical ten-artifact release
  rehearsals pass.
- Findings-first review leaves exactly 16 intended paths. Workflows,
  dependencies, lock, protected runtime/release surfaces, public identity,
  credentials, backend/native imports, disclosure, and mutation boundaries are
  clean.
- The authoritative hosted `main` remains exact M99
  `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e`, with no open PR and PR #251 as
  the newest merge. M144 remains local pending full acceptance and a hosted
  base that actually contains the preceding stack.

## Explicit non-scope

- No new runtime value/protocol/decoder, saved-preview format, preview
  verification, cache argument/access, fresh observation, candidate list,
  detailed diff, cache/object/action/artifact identity, filename/path/payload,
  timestamp, age, last-use fact, policy threshold, or new disclosure.
- No chronology/freshness/authenticity/provenance claim, signature, key/trust
  root, attestation, transparency log, trusted timestamp, remote cache,
  authentication, network, or telemetry export.
- No retention root, lease, pin, generation, grace/quota policy, quiescence,
  lock, atomic snapshot, cleanup, garbage collection, prune, repair, deletion,
  eviction, mutation, migration, rollback, watcher, scheduler, worker, process,
  thread, parallelism, plugin, dynamic evaluation, renderer upload,
  project/world mutation, receipt, dependency, native/backend surface,
  metadata, version, engine-root API, workflow/allocation, permission,
  credential, release, publication, push, PR, or remote change in this slice.

## Remaining acceptance work

- No local M144 acceptance work remains. Keep the milestone unpublished until
  a fresh hosted audit proves the required preceding stack is present; continue
  the next approved research-gated milestone from the exact committed M144 tip.
