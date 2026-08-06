# Current Task

- **Task:** M22 - built-in operation argument compatibility and evolution policy
- **Status:** Complete and squash-integrated by PR #32. GitHub-verified
  `main` commit `8a4d288c4edf55d0299828b8edee1bd1885884d9` has the exact
  final M22 tree. No M23 work is included.
- **Started:** 2026-08-06
- **Base:** Exact clean synchronized `main` commit
  `291dfb3fd6895a2fdac7a2f0016bb181f0e5bca4`.
- **Outcome:** State an exact compatibility/deprecation policy independent of
  current handlers for every built-in v1 operation argument schema and prove
  current installed behavior against it.
- **Acceptance gate:**
  - Freeze one machine-readable contract for all seven built-in v1 operations,
    including required/optional fields and named semantic rules.
  - Forbid in-place changes to an operation/version identity; breaking changes
    use a new operation version, new identities are additive, and unknown
    fields fail closed.
  - Exercise every valid shape plus missing-required and unexpected-field
    rejection through installed public APIs on fresh deterministic worlds.
  - Validate exact, sanitized, repeatable evidence from source, an isolated
    wheel, and the release sample bundle.
  - Accept RFC-0005 and update M20 living readiness schema to `/3`, with only
    the operation-policy and bounded-reader gates true.
  - Keep the existing eight essential CI jobs unchanged and create at most one
    hosted implementation run.
- **Non-scope:** Runtime source/API/export changes, new operations or handlers,
  command/receipt reinterpretation, cross-version/external-adoption claims,
  stability promotion, semantic-diff/diagnostic policy, release channel,
  dependency/lock/version/workflow changes, storage/backend/provider/native/
  WASM/network/editor work, tag, release, or package publication.
- **SemVer:** No package or public-Python-surface change. Existing persistent
  IDs remain `ludoweave.command/1` plus operation version 1; package version
  remains `0.1.0a1`.
- **Final local evidence:** Lock/sync, 215-file formatting, Ruff, strict
  Pyright, strict MkDocs, pure build, isolated wheel/release smoke, 1,030 tests
  with one existing Windows symlink skip, 10 real-wgpu tests, both graphics
  vertical slices, and all documented M1-M4/M7 benchmark/profile validators
  pass. M1 simulation and both M3 timing targets remain observed misses. The
  first sandboxed uv attempt and first Ruff findings are recorded with their
  successful corrections in `.ai/TEST_EVIDENCE.md`. DCO-signed implementation
  commit `f1a89ad460467039f966ed37955144840cd96a12` is published through ready
  PR #32. GitHub Actions run `31100821087` passed all eight unchanged
  essential jobs. One automated review clarification about defaulted component
  fields was corrected in DCO-signed commit
  `cf3ae540e71cda128837ea698f5f175a7abf2fc4`. Necessary follow-up run
  `31101607485` passed all eight unchanged jobs; the original thread is now
  outdated and no actionable thread remains. PR #32 squash-integrated final
  evidence head `a5a49dcca277f28bb3e6097f37d5418d5d3c2c9d` as
  GitHub-verified commit `8a4d288c4edf55d0299828b8edee1bd1885884d9`;
  both trees are `f513bec716d1735cc47a6aab862bca0f5f770af9`.
