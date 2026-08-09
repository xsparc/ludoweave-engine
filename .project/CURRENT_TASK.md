# Current Task

- **Task:** M47 - cross-platform public consumer rehearsal
- **Status:** Feature fully validated and squash-integrated; recording exact
  hosted and integration evidence on `records/m47-integration`.
- **Started:** 2026-08-09
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  M46 closeout commit `2d27b139c6bf4a130ca97e7f0b518f6ebfe191c5`.
  Only `main` existed locally/remotely; no open pull request, local/remote tag,
  or GitHub release existed; full Git-object checking passed.
- **Outcome:** Replace the Bash-only public release verifier with one portable,
  typed standard-library Python program and run the tag-only fresh consumer on
  Ubuntu, Windows, and macOS without widening release authority or pull-request
  allocations.
- **Acceptance gate:**
  - Keep the release job's verified numeric release ID and validated version as
    the only scalar handoff; retain the exact named same-workflow candidate.
  - Expand the existing dependent fresh-consumer job to exactly
    `ubuntu-latest`, `windows-latest`, and `macos-latest` with `fail-fast:
    false`, a 25-minute timeout, explicit `contents: read`, and no dependency
    cache or release/attestation/identity-token write permission.
  - Use one Python verifier in the publishing and fresh jobs. Publishing mode
    must require M43's plan; fresh mode must reject a preexisting plan and
    create one exclusively after candidate/public-document validation.
  - Make initial hosts repository-fixed, reject credentials and non-HTTPS,
    user information, fragments, non-default ports, and more than three remote
    redirects; use verified TLS, 10-second blocking time, and a 30-second
    monotonic deadline without ambient proxy/client configuration.
  - Retain the 4-MiB document, 16-KiB plan, positive 63-bit IDs, safe unique
    names, exclusive ID-derived partials, 32 assets, 256 MiB per asset, 512 MiB
    total, exact length/set validation, and complete installed release smoke.
  - Emit only a versioned status, stable generic failure, and bounded aggregate
    count/bytes; do not expose paths, URLs, response bodies, notes, environment
    values, or credentials.
  - Add no pull-request CI allocation, release trigger, credential, mutation,
    retry, rollback, artifact-set, attestation, publication command, dependency,
    lock, version, runtime, package, or public-API change.
  - Document same-workflow/repository/account/provider and independent/external,
    clean-machine, delivery-path, future, immutability, artifact-security,
    PyPI, and supported-channel non-claims.
  - Pass fixture-driven plan, exact-byte, timeout/redirect, credential, and
    architecture tests; complete CPython 3.12-3.14, graphics, docs, build,
    installed wheel/release smoke, and the exact three-allocation hosted gate.
- **Non-scope:** Creating or pushing a tag; creating, uploading, publishing,
  editing, deleting, or unpublishing a release; external monitoring or
  independently owned verification; machines outside GitHub-hosted Actions;
  automatic retry/rollback/cleanup; every delivery path; future availability;
  immutable releases; artifact security; PyPI; a supported release channel;
  runtime/public API, package version/dependency/lock, or deferred subsystems.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Current evidence:** M46 feature PR #89, documentation record PR #90, and
  zero-run closeout PR #91 are fully validated and squash-integrated. Final
  closeout `2d27b139c6bf4a130ca97e7f0b518f6ebfe191c5` has the exact reviewed
  tree, sole parent the M46 integration-record squash, a GitHub-valid signature,
  standalone DCO, and no post-merge run. Only synchronized `main` remained with
  no open PR, tag, or release. Official GitHub documentation supports
  same-workflow artifact handoff and OS matrices; current Python documentation
  supports explicit verified HTTPS connections, blocking timeouts, response
  status/headers, and bounded reads. The focused M45-M47 gate passes 39 tests
  under strict static typing. The final graphics-enabled CPython 3.12, 3.13,
  and 3.14 suites each pass 1,945 tests with 14 expected capability skips.
  Ten real-wgpu tests, both profile contracts, Clockwork Arena, Agent World
  Builder, reproducible distribution, isolated-wheel smoke, and complete
  release smoke pass locally. The final static gate covers 290 formatted files,
  zero Ruff/Pyright findings, 405 architecture assertions, strict docs/YAML,
  and reproducible wheel/sdist bytes; isolated wheel and complete release smoke
  pass. Ready PR #92 exact head
  `fdddaa986b647e68a0a027445c11547b878ad246` passed run `31286321895` in
  exactly three allocations: Linux first in 7m20s, then macOS in 2m40s and
  Windows in 3m55s. The PR was clean with no review, comment, or thread.
  Verified squash `c3f5d9c4b9f21315b7ae8f113cc643f978d75746` has exact reviewed tree
  `e222ebff0655b9d86548bab6e8d19fb79ba3afc5`, sole parent the M46
  closeout, a GitHub-valid signature, standalone DCO, and no post-merge run.
  The feature branch is deleted locally/remotely. No real M47 tag/release
  execution exists or is claimed.
