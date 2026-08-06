# Current Task

- **Task:** M23 - receipt semantic-diff and diagnostic compatibility policy
- **Status:** Locally complete and findings-first reviewed on
  `codex/m23-receipt-diagnostic-policy`. Implementation, full local/artifact/
  provider validation, documentation, and diff review are complete. Hosted
  validation, publication, and integration remain.
- **Started:** 2026-08-06
- **Base:** Exact clean synchronized `main` commit
  `415859e19d9d29caa1168fabc96def509897b056`.
- **Outcome:** State an exact receipt-v1 semantic-diff and diagnostic-code
  evolution policy independent of implementation and prove installed behavior
  against it without promoting protocol stability.
- **Acceptance gate:**
  - Freeze one machine-readable contract for semantic-diff root/nested fields,
    status presence, ordering, and named meanings.
  - Forbid in-place shape or meaning changes under `ludoweave.receipt/1`; a
    breaking change uses a new receipt protocol.
  - Freeze existing top-level diagnostic-code meanings, allow additive well-
    formed codes with rejected-status fallback, and classify phase/message/
    scalar detail keys as non-authoritative metadata.
  - Exercise every semantic change family, all current top-level rejection
    codes, missing/unknown diff fields, incompatible protocol, changed metadata,
    and an unknown code through installed public APIs.
  - Validate exact, sanitized, repeatable evidence from source, an isolated
    wheel, and the release sample bundle.
  - Accept RFC-0006 and update M20 living readiness schema to `/4`, with only
    the operation-policy, bounded-reader, and receipt-policy gates true.
  - Keep the existing eight essential CI jobs unchanged and create at most one
    hosted implementation run unless a reviewed correction requires another.
- **Non-scope:** Runtime source/API/export changes, receipt/command/operation/
  handler changes, new diagnostic behavior, cross-version/external-adoption
  claims, stability promotion, release-channel implementation, dependency/
  lock/version/workflow changes, storage/backend/provider/native/WASM/network/
  editor work, tag, release, or package publication.
- **SemVer:** No package or public-Python-surface change. Receipt identity
  remains `ludoweave.receipt/1`; package version remains `0.1.0a1`.
- **Final local evidence:** The verified baseline resolves 46 locked packages and
  passes 84 focused receipt/transaction/stability tests. The corrected M23
  evidence example emits an exact repeatable sanitized policy report. Focused
  formatting, Ruff, strict Pyright, 17 integration/architecture tests, then an
  expanded 28-test readiness/release group and strict MkDocs build pass. Two
  expanded gate passes 219-file formatting, Ruff, strict Pyright, strict docs,
  pure build, isolated wheel/release smoke, 1,048 tests with one existing
  Windows symlink skip, 10 real-wgpu tests, both graphics vertical slices, and
  every documented M1-M4/M7 benchmark/profile validator. M1 simulation and
  both M3 timing targets remain observed misses. Two development failures are
  recorded factually in `.ai/TEST_EVIDENCE.md`: the
  first component annotation mode was incompatible with the component schema,
  and `world.transaction.nontransactional_operation` is a nested cause rather
  than a top-level receipt diagnostic code.
