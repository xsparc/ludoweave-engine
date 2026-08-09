# Current Task

- **Task:** M54 - public release TLS session freshness
- **Status:** Feature PR #114 is fully validated and squash-integrated;
  publishing the exact four-file integration record on
  `records/m54-integration`.
- **Started:** 2026-08-10
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** The feature began from exact clean synchronized M53 closeout
  `fe585f8bd2313feac39b70cadf088c57bbb1960e`. The integration record begins
  from GitHub-verified feature squash
  `c333f2b9aad98b9a55d986076fe8b09153d30762`; only `main` and this intended
  local record branch exist, with no remote feature branch, open pull request,
  tag, release, or post-merge `main` run.
- **Outcome:** Observe after the handshake that every actual public-release TLS
  socket reports a fresh, non-reused session before later TLS evidence or HTTP
  transmission.
- **Acceptance:** After M49 peer confinement and M53 exact context binding,
  require `session_reused` to be exactly `False` before M52 service identity,
  M51 negotiated-session inspection, or a request. Every redirect repeats the
  observation independently. Missing, unsupported, malformed, resumed, and
  raising observations fail content-silently under `public_release.tls_failed`
  with an available local cause chained.
- **Boundary:** No workflow, runner allocation, action, permission, trigger,
  credential, release mutation, dependency, lock, version, runtime package,
  public API, session cache, session assignment, ticket control, custom TLS
  implementation, trust replacement, pinning, certificate/chain parser,
  revocation, channel binding, proxy, or network sandbox. The reported value
  does not independently prove a full handshake or certificate exchange.
  Fixture/PR evidence is not a real public release observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Evidence:** Feature head `d5d02a38ea302c0e314f966376e267c45508d14b`
  passed run `31321661693` in exactly three Linux-first allocations. Every
  static, supported-Python, real-graphics, profile, sample, reproducible-build,
  installed-wheel, and release-smoke step passed. Delayed review found no
  review, comment, or thread. Squash `c333f2b9aad98b9a55d986076fe8b09153d30762`
  reproduces the exact reviewed tree with the M53 closeout as sole parent,
  valid GitHub signature, and standalone DCO. The feature branch is deleted
  locally/remotely; no post-merge run, tag, or release exists.
- **Record gate:** This four-file documentation change must use one Linux
  allocation; the desktop umbrella must skip with zero steps.
