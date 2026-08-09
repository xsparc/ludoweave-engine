# Current Task

- **Task:** M54 - public release TLS session freshness
- **Status:** In implementation and local validation on
  `security/m54-tls-session-freshness`.
- **Started:** 2026-08-10
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized M53 closeout
  `fe585f8bd2313feac39b70cadf088c57bbb1960e`; only `main` existed locally and
  remotely, with no open pull request, tag, release, or post-closeout `main`
  run.
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
- **Validation:** Run focused M47-M54 compatibility and adversarial tests,
  whole-tree format/lint/type/architecture/docs, complete supported-Python
  suites, real-wgpu, profiles, vertical slices, documented benchmarks,
  reproducible build, isolated-wheel and release smoke, then findings-first
  scope/security/integrity review before the bounded hosted gate.
