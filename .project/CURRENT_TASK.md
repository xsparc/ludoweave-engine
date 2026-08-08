# Current Task

- **Task:** M46 - fresh-runner public consumer rehearsal
- **Status:** Completing final validation of the bounded separate-runner release rehearsal on
  `release/m46-fresh-runner-consumer`.
- **Started:** 2026-08-09
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  M45 closeout commit `086f1ceb3974583ce7a2c386c67f516299c2f1dd`.
  Only `main` existed locally/remotely; no open pull request, local/remote tag,
  or GitHub release existed; full Git-object checking passed.
- **Outcome:** After the existing publishing job succeeds, use a separate
  read-only Linux runner to retrieve the exact same-workflow admitted
  candidate, independently fetch the public bytes without a release
  credential, revalidate them, and run complete installed release smoke.
- **Acceptance gate:**
  - Export only the verified numeric release ID and validated version from the
    successful publishing job.
  - Add exactly one dependent tag-only Ubuntu job with a 25-minute timeout and
    explicit `contents: read`; add no release, attestation, or identity-token
    write permission.
  - Use the existing exact candidate upload through `actions/download-artifact`
    pinned to verified v8.0.1 commit `3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c`.
  - Extract M45's public retrieval into one shell verifier. Publishing mode
    must reuse the existing M43 plan; fresh mode must reject a preexisting plan
    and create one exclusively from candidate plus public document.
  - Retain the fixed repository, positive 63-bit IDs, HTTPS-only three-
    redirect limit, 10/30-second timeouts, 4-MiB document cap, safe basenames,
    no-clobber partials, 32 assets, 256 MiB per asset, and 512 MiB total.
  - Supply no release credential, authorization header, cookie, browser URL,
    or caller-selected host to public HTTP requests.
  - Revalidate the public document and exact downloaded directory, then run
    complete release smoke and isolated wheel installation in the fresh
    workspace.
  - Add no pull-request CI allocation, release trigger, mutation, retry,
    rollback, artifact-set, attestation, dependency, lock, version, runtime,
    package, or public-API change.
  - Document same-workflow/provider, external/independent, cross-platform,
    clean-machine, future, immutability, artifact-security, PyPI, and support
    non-claims.
  - Run the complete local gate and one substantive hosted pull-request gate.
- **Non-scope:** Creating/pushing a tag or release; uploading/publishing;
  modifying the staged candidate; changing attestations; automatic retry,
  unpublish, delete, rollback, or cleanup; external monitoring; independent
  external verification; a cross-platform public installation matrix; a clean
  machine outside GitHub-hosted Actions; every delivery path; future
  availability; immutable releases; artifact security; PyPI; supported release
  channel; runtime/public API; package version/dependency/lock; deferred work.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Current evidence:** M45 feature PR #86, documentation record PR #87, and
  zero-run closeout PR #88 are fully validated and squash-integrated. Final
  closeout `086f1ceb3974583ce7a2c386c67f516299c2f1dd` has exact reviewed
  tree, sole parent the M45 integration-record squash, valid GitHub signature,
  standalone DCO, and no post-merge run. Only synchronized `main` remained with
  no open PR, tag, or release. Official GitHub documentation supports dependent
  job outputs and same-workflow artifact transfer. The official download action
  v8.0.1 tag resolves to verified commit
  `3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c`. The inherited release chain
  passes 147 tests with three capability skips. The first system-Python YAML
  probe failed before parsing because the Windows launcher is unusable; the uv-
  managed rerun parsed the workflow. Shared-script Bash syntax and YAML parse.
  The documentation-integrated architecture suite passes all 383 assertions.
  Complete graphics-enabled CPython 3.12, 3.13, and 3.14 runs each pass 1,923
  tests with 14 capability skips. Static/docs, real wgpu, profiles, samples,
  benchmark validators, reproducible distribution, wheel smoke, and complete
  release smoke pass. Review found that the first extracted shell version used
  a nonexistent plan flag; the correction uses the verifier's established
  exclusive `--asset-plan` option, and the regression now executes that real
  verifier on CPython 3.12-3.14. The final implementation-tree rebuild and
  complete suite pass. Publication, hosted validation, review closure, and
  integration remain pending. No real fresh-runner release pass is claimed.
- **Hosted correction:** Ready PR #89 exact feature head
  `bbfd68ee6b0826b47b573ede4a10910b07945aeb` allocated exactly three
  runners in run `31282550237`. Linux passed in 5m58s and Windows passed in
  3m42s. macOS failed one compatibility assertion after 1,926 passes and one
  skip because Bash 3.2 treats an explicitly empty array expansion as unbound
  under `set -u`. The correction removes the array, uses a shared verifier
  function with safe positional arguments, retains exactly two verifier call
  sites, and passes all 17 focused tests on CPython 3.12-3.14. Corrected full
  local validation passes; corrected hosted validation remains pending and the
  failed head will not merge.
