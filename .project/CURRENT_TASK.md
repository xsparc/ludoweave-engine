# Current Task

- **Task:** M51 - public release negotiated TLS-session conformance
- **Status:** Corrected feature PR #105 and corrected integration-record PR
  #106 are fully validated and squash-integrated; publishing the exact
  three-file closeout record on `records/m51-closeout`.
- **Started:** 2026-08-09
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** The feature began from exact clean synchronized M50 closeout
  `53f3804010f1556ecaff21a61b1e9c405a26e203`. The current closeout record is
  based on exact synchronized M51 integration-record squash
  `d2cc5d630b15351289008976d192232cde184afc`; only `main` and this intended
  local record branch exist, no remote feature/record branch remains, no open
  pull request, tag, GitHub release, or post-merge `main` run exists, and full
  Git-object checking passes.
- **Outcome:** Validate the actual negotiated TLS session on every fixed API or
  bounded redirected asset hop after connected-peer confinement and before any
  HTTP request.
- **Acceptance gate:**
  - Advertise only `http/1.1` from every M50 client context.
  - Require actual negotiated TLSv1.2 or TLSv1.3, a three-field non-empty
    cipher report with an integer secret-bit count of at least 128, no TLS
    compression, and ALPN `http/1.1` or no negotiated ALPN.
  - Perform the check after M49 actual connected-peer validation and before the
    HTTP method, path, or headers are sent; repeat it for every redirect.
  - Map missing/unsupported accessors, malformed values, and failed invariants
    to `public_release.tls_failed` without exposing a host, peer, URL, session
    value, response, or credential.
  - Preserve M50 context/key-log isolation, M49 peer confinement, M48 response/
    failure semantics, and every M47 identity, deadline, size, path, exact-
    validation, and installed-smoke bound.
  - Change no workflow, runner allocation, action, permission, trigger,
    credential, release mutation, retry, cleanup, dependency, lock, version,
    runtime package, or public API.
  - Add fixture-driven valid/invalid session, ordering, redirect independence,
    failure, boundary-hash, architecture, RFC, and aligned maintainer/public
    docs.
  - Pass complete CPython 3.12-3.14, graphics, docs, build, installed
    wheel/release smoke, and the exact three-allocation substantive hosted gate.
- **Non-scope:** A cipher-name allowlist; custom CA bundle or trust store;
  certificate/SPKI pinning; client certificates; revocation policy; TLS
  fingerprinting; session ticket/reuse/channel-binding policy; proxy support;
  real tag/release execution; release publication, edit, delete, rollback, or
  cleanup; external/independent monitoring; every
  CDN/geographic path; future availability; immutability; artifact security;
  PyPI; supported release-channel claims; runtime/public API, dependency, lock,
  package version, or deferred subsystem changes.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Current evidence:** Python 3.14.7 documentation defines the actual session
  accessors and custom-context ALPN ownership used by RFC-0034. The final local
  corrected candidate has zero Ruff/strict-Pyright findings, 485 passing
  architecture assertions, strict docs, and complete graphics-enabled CPython
  3.12-3.14 suites of 2,025 passing tests plus 14 expected skips each. Real-wgpu,
  profiles, both vertical slices, documented benchmarks, reproducible build,
  isolated wheel, and complete release smoke also pass on the corrected
  candidate.
  Corrected attempts and exact results are recorded in
  `.project/TEST_EVIDENCE.md`. Corrected head
  `a0612236aa13c2892fd95e55c2a77286d21572d4` passed run `31312987430` in
  exactly three Linux-first allocations. The one prior review finding is
  corrected, outdated, and resolved; no unresolved thread remains. Verified
  squash `ce4184b4ecedd9163a654cc96ae6c96086683760` has the exact reviewed
  tree, sole M50-closeout parent, valid GitHub signature, and standalone DCO.
  No post-merge `main` run, real tag, or release was created or claimed.
  Four-file integration-record PR #106 first passed docs-only run
  `31313663654` at head `bea144e9d0444237c08a3be6a56905f6d66b2c65`.
  Review found one stale pending-validation sentence, which was corrected and
  revalidated at head `aa94d62a06d51f635a6dce1dcbfd686a8c0ac2dd` by run
  `31313847857` in one Linux allocation; its zero-step desktop umbrella was
  skipped. The thread is resolved. Verified squash
  `d2cc5d630b15351289008976d192232cde184afc` exactly matches the corrected
  record tree, has the feature squash as its sole parent, a valid GitHub
  signature, and standalone DCO. The closeout changes only the three
  `.project/**` records and must allocate no hosted runner.
