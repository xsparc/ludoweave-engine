# Current Task

- **Task:** M48 - public release HTTP response conformance
- **Status:** Feature fully validated and squash-integrated; recording exact
  hosted and integration evidence on `records/m48-integration`.
- **Started:** 2026-08-09
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  M47 closeout commit `8d8d9e4a5790d7b74ec06139d314ffdf30a4ef41`.
  Only `main` existed locally/remotely; no open pull request, local/remote tag,
  or GitHub release existed; full Git-object checking passed.
- **Outcome:** Constrain the portable public release client to GitHub's
  documented release/asset response shapes and make timeout,
  transport/protocol, and local-output failures consistently actionable without
  changing workflow topology or release authority.
- **Acceptance gate:**
  - Require the fixed public release-document request to return a direct `200`.
  - Allow a fixed asset-ID request to return `200` or follow at most three
    `302` responses through M47's HTTPS/default-port/user-info/fragment bounds;
    reject every other `3xx` response.
  - Send `X-GitHub-Api-Version` only when the current request host is the fixed
    `api.github.com`; never send authorization, cookies, ambient client/proxy
    configuration, browser URLs, or caller-selected initial hosts.
  - Retain a ten-second blocking timeout inside one 30-second monotonic request
    deadline; refresh the connected socket timeout before response headers and
    every bounded body read.
  - Map request/header/body `TimeoutError` to
    `public_release.request_timeout`, other socket/HTTP protocol failures to
    `public_release.request_failed`, and only local create/write/finalize/remove
    failures to `public_release.output_failed`.
  - Retain M47's fixed repository/IDs, verified TLS, document/plan/count/byte,
    safe-name, exclusive-partial, exact-validation, and installed-smoke bounds.
  - Change no workflow, runner allocation, action, permission, trigger,
    credential, release mutation, retry, cleanup, dependency, lock, version,
    runtime, package, or public API.
  - Add fixture-driven direct/redirect/header/timeout/transport/output tests,
    an accepted RFC, architecture protection, and aligned public/maintainer
    documentation.
  - Pass complete CPython 3.12-3.14, graphics, docs, build, installed
    wheel/release smoke, and the exact three-allocation hosted gate.
- **Non-scope:** Creating or pushing a tag; creating, uploading, publishing,
  editing, deleting, or unpublishing a release; redirect-host allowlists;
  retries or automatic cleanup; external monitoring; independently owned
  verification; every CDN/geographic path; future availability; immutability;
  artifact security; PyPI; a supported release channel; runtime/public API,
  dependency/lock/version, or deferred subsystems.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Current evidence:** M47 feature PR #92, documentation record PR #93, and
  zero-run closeout PR #94 are fully validated and squash-integrated. Final
  closeout `8d8d9e4a5790d7b74ec06139d314ffdf30a4ef41` has exact reviewed tree,
  sole parent the M47 integration-record squash, a GitHub-valid signature,
  standalone DCO, and no post-merge run. Only synchronized `main` remained with
  no open PR, tag, or release. Official GitHub documentation defines `200` for
  Get a release and `200`/`302` for Get a release asset; Python documentation
  defines blocking socket timeout behavior and `TimeoutError` as an `OSError`.
  The documentation-integrated M45/M47/M48 focus passes all 54 tests under
  strict Ruff and Pyright. The final graphics-enabled CPython 3.12, 3.13, and
  3.14 suites each pass 1,966 tests with 14 expected skips. Ten real-wgpu tests,
  both profile contracts, Clockwork Arena, Agent World Builder, reproducible
  distribution, isolated-wheel smoke, and complete release smoke pass locally.
  The final static gate covers 291 formatted files, zero Ruff/Pyright findings,
  426 architecture assertions, strict docs, whitespace, and healthy Git
  objects. Commit-candidate reproducibility, isolated-wheel smoke, and complete
  release smoke pass. Ready PR #95 exact head
  `9b5c533d1e73ee985945fa0feb7e876417ee0126` passed run `31288303182` in
  exactly three allocations: Linux first in 415 seconds, then macOS in 118
  seconds and Windows in 228 seconds. Every job and non-skipped step succeeded.
  The PR was clean with no review, comment, or thread. Verified squash
  `c32ff1bf71b53278ef2ff616c2fc3cfce5cf20a3` has exact reviewed tree
  `1986f691633d94a5b980c2be0b7e1d0b364de37e`, sole parent the M47
  closeout, a GitHub-valid signature, standalone DCO, and no post-merge run.
  The feature branch is deleted locally/remotely. No real M48 tag/release
  execution exists or is claimed.
