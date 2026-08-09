# Current Task

- **Task:** M54 - public release TLS session freshness
- **Status:** Feature PR #114 and integration-record PR #115 are fully
  validated and squash-integrated; publishing the exact three-file closeout
  record on `records/m54-closeout`.
- **Started:** 2026-08-10
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** The feature began from exact clean synchronized M53 closeout
  `fe585f8bd2313feac39b70cadf088c57bbb1960e`. The closeout record begins from
  GitHub-verified M54 integration-record squash
  `50a14e0674c4e7468faf1c8ec4490846255558ce`; only `main` and this intended
  local closeout branch exist, with no remote working branch, open pull request,
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
  Four-file integration head `baec3a2bac0c0bdd8dd4bceb66cdb6e26973538b`
  passed run `31322470238` in one 37-second Linux allocation; its desktop
  umbrella skipped with zero steps. Integration squash
  `50a14e0674c4e7468faf1c8ec4490846255558ce` reproduces the exact reviewed
  record tree with the feature squash as sole parent, valid GitHub signature,
  and standalone DCO. The integration branch is deleted locally/remotely.
- **Closeout gate:** This exact three-file `.project/**` record must allocate
  no hosted run or check.
