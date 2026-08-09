# Current Task

- **Task:** M53 - public release TLS context binding
- **Status:** Feature PR #111 and integration-record PR #112 are fully
  validated and squash-integrated; publishing the exact three-file closeout
  record on `records/m53-closeout`.
- **Started:** 2026-08-10
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** The feature began from exact clean synchronized M52 closeout
  `8d69f5b265277edb95ae47ea3a0af001217a4575`. The current closeout record is
  based on exact synchronized M53 integration-record squash
  `9217862df30d51efa7754cc8a9300c4b05fb2426`; only `main` and this intended
  local record branch exist, no remote feature/record branch or open pull
  request remains, and no tag or release was created.
- **Outcome:** Prove after the handshake that every actual public-release TLS
  socket retained the exact verified client context supplied for its hop and
  an exactly client-side role, then revalidate the complete context policy
  before later TLS evidence or HTTP transmission.
- **Acceptance:** Exact object binding and client role are checked after M49
  peer confinement and before M52 identity, M51 session, or HTTP. The M50
  protocol, certificate verification, hostname checking, TLSv1.2 minimum,
  strict/partial-chain flags, and no-key-log policy are revalidated. Every
  redirect repeats the check independently; failures are content-silent under
  `public_release.tls_failed` with an available cause chained.
- **Boundary:** No workflow, runner allocation, action, permission, trigger,
  credential, release mutation, dependency, lock, version, runtime package,
  public API, trust replacement, pinning, certificate/chain parser,
  revocation, session reuse, channel binding, proxy, or network sandbox.
  Fixture/PR evidence is not a real public release observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Evidence:** Local focused behavior, whole-tree static/architecture/docs,
  complete graphics-enabled CPython 3.12-3.14, real-wgpu, profiles, both
  vertical slices, documented benchmarks, reproducible build, isolated wheel,
  release smoke, integrity, scope, and findings-first review passed. Feature
  head `0b3eaad213a149fb96c138cd4eabc1d861d053e9` passed run `31319422736` in
  exactly three Linux-first allocations. Verified feature squash
  `66f9d84eea57c270e9b18326348eb1ea5c4ebfa4` reproduced the exact reviewed
  tree. Four-file integration head `de488d1e305026f724a155bf692653cd5f8cb454`
  passed run `31320201771` in one 36-second Linux allocation; desktop umbrella
  `93261877229` skipped with zero steps. Verified integration squash
  `9217862df30d51efa7754cc8a9300c4b05fb2426` reproduced the exact reviewed
  record tree with the feature squash as sole parent, valid signature, and
  standalone DCO. No post-merge `main` run, tag, or release was created. The
  closeout changes only three `.project/**` records and must allocate no hosted
  run or check.
