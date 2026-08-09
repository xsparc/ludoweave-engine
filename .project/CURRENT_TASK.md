# Current Task

- **Task:** M53 - public release TLS context binding
- **Status:** The 19-path candidate on `security/m53-tls-context-binding` is
  fully validated and findings-first reviewed locally with no actionable
  finding; feature commit, push, ready PR, and hosted exact-head validation are
  next.
- **Started:** 2026-08-10
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized M52 closeout
  `8d69f5b265277edb95ae47ea3a0af001217a4575`, with only `main` present and no
  open pull request, tag, release, or post-closeout `main` run.
- **Outcome:** Prove after the handshake that every actual public-release TLS
  socket retained the exact verified client context supplied for its hop and
  that the complete context policy still holds before later TLS evidence or
  HTTP transmission.
- **Acceptance gate:**
  - Preserve the exact M50 context object passed to each `HTTPSConnection`.
  - After M49 connected-peer confinement, require the actual socket's
    `context` to be that exact object and `server_side` to be exactly `False`.
  - Revalidate `PROTOCOL_TLS_CLIENT`, `CERT_REQUIRED`, hostname checking, exact
    TLSv1.2 minimum, strict plus partial-chain flags, and absent key logging
    after the handshake and before M52 identity, M51 session, or HTTP.
  - Repeat the binding and policy check with an independent context on every
    redirect.
  - Map missing/unsupported accessors, substitution, wrong role, policy
    mutation, and inspection failures to content-silent
    `public_release.tls_failed`, preserving an available chained cause.
  - Preserve M52 identity evidence, M51 session conformance, M50 key-log
    isolation, M49 peer confinement, M48 HTTP semantics, and every M47 bound.
  - Change no workflow, runner allocation, action, permission, trigger,
    credential, release mutation, retry, cleanup, dependency, lock, version,
    runtime package, or public API.
  - Pass complete CPython 3.12-3.14, graphics, docs, build, installed-wheel and
    release smoke, findings-first review, and the exact three-allocation
    substantive hosted gate.
- **Non-scope:** Custom trust, pins, certificate/chain parsing, revocation,
  session reuse or tickets, channel binding, proxies, network sandboxing,
  external monitoring, real tag/release execution, publication mutation,
  independent verification, every TLS/CDN path, future availability,
  immutability, artifact security, PyPI, supported-channel claims, runtime API,
  dependency, lock, package version, or deferred subsystem changes.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Current evidence:** Official Python 3.14 documentation identifies
  `SSLSocket.context`, `SSLSocket.server_side`, `SSLContext`, and
  `HTTPSConnection(context=...)` as the portable contract surfaces. The first
  inherited focused probe exposed only test doubles missing those standard
  socket attributes. Corrected M47-M53 behavior passes all 144 focused
  assertions. All 296 Python files are format clean; Ruff and strict Pyright
  report zero findings; 522 architecture assertions, strict docs, complete
  graphics-enabled CPython 3.12-3.14 suites, real-wgpu, profiles, both vertical
  slices, documented benchmarks, reproducible builds, isolated-wheel smoke,
  and complete release smoke pass. Final record-inclusive static,
  architecture, docs, reproducible build, installed-wheel, and release smoke
  also pass. Findings-first diff, scope, history, integrity, credential,
  identity, backend/native leakage, and public-boundary review found no
  actionable finding. Hosted evidence remains pending and must not be claimed
  before execution.
