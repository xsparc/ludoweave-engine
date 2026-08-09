# Current Task

- **Task:** M50 - public release TLS key-log isolation
- **Status:** Feature and integration record are fully validated and
  squash-integrated; closing factual records on `records/m50-closeout`.
- **Started:** 2026-08-09
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  M49 closeout commit `f6214992b02a9ef0bc44d6a9e4e6d72dc9d33de0`.
  Only `main` existed locally/remotely; no open pull request, tag, or GitHub
  release existed; full Git-object checking passed at M49 closeout.
- **Outcome:** Prevent the portable public-release verifier from inheriting
  CPython's ambient `SSLKEYLOGFILE` behavior while retaining explicit verified
  modern TLS and every earlier public-consumer bound.
- **Acceptance gate:**
  - Create a new `SSLContext(PROTOCOL_TLS_CLIENT)` for every fixed API or
    bounded redirected asset hop.
  - Load system server-auth roots, require `CERT_REQUIRED` plus hostname
    validation, set TLS 1.2 as the minimum, and retain strict/partial-chain
    X.509 flags.
  - Require key logging to remain disabled. A controlled ambient
    `SSLKEYLOGFILE` value must remain unchanged and its target must not be
    created or written.
  - Map context construction, root-loading, or invariant failure to
    `public_release.tls_failed` without exposing an environment value, local
    path, URL, peer, response, or credential.
  - Preserve M49 connected-peer confinement, M48 response/header/failure
    semantics, and every M47 identity, deadline, size, path, exact-validation,
    and installed-smoke bound.
  - Change no workflow, runner allocation, action, permission, trigger,
    credential, release mutation, retry, cleanup, dependency, lock, version,
    runtime package, or public API.
  - Add fixture-driven context, ambient-keylog, redirect independence, failure,
    boundary-hash, architecture, RFC, and aligned maintainer/public docs.
  - Pass complete CPython 3.12-3.14, graphics, docs, build, installed
    wheel/release smoke, and the exact three-allocation substantive hosted gate.
- **Non-scope:** A custom CA bundle or trust store; certificate/SPKI pinning;
  client certificates; proxy support; environment mutation; negotiated
  cipher/session reporting; real tag/release execution; release publication,
  edit, delete, rollback, or cleanup; external/independent monitoring; every
  CDN/geographic path; future availability; immutability; artifact security;
  PyPI; supported release-channel claims; runtime/public API, dependency, lock,
  package version, or deferred subsystem changes.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Current evidence:** Python 3.14.7 documentation confirms that
  `create_default_context()` enables key logging when `SSLKEYLOGFILE` is set
  and that the debug file receives TLS session secrets. The explicit
  implementation passes the full local static, architecture, supported-Python,
  graphics, profile, vertical-slice, reproducible-build, isolated-wheel, and
  complete release-smoke gates recorded in `.project/TEST_EVIDENCE.md`. Ready
  PR #102 exact head `99134b6be68bb7978431710228e788250561659e`
  passed run `31309759226` in exactly three allocations: Linux first, then
  macOS and Windows. The PR had zero reviews, comments, or review threads and
  squash-integrated as `5fb56120e1a96a0a25db96baa3836699e435611c`
  with the exact reviewed tree, sole M49-closeout parent, GitHub-valid
  signature, and DCO. No `main` run was allocated and only synchronized
  `main` remains locally/remotely. Documentation-only PR #103 exact head
  `7441e9fae142a67a9d30075ac4c28127978cc750` then passed run
  `31310482277` in one 40-second Linux allocation; the desktop umbrella had
  zero steps and was skipped. It had zero reviews/comments/threads and
  squash-integrated as `7764ea32645c3455fb08bfbd5a3c4e2d8cabbd47`
  with exact reviewed tree, sole feature-squash parent, valid signature, DCO,
  no `main` run, and deleted branch. Only the three-`.project/**` zero-run
  closeout remains. No real tag or release has been created or claimed.
