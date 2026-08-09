# Current Task

- **Task:** M52 - public release TLS service-identity evidence
- **Status:** Implementation, corrected complete local validation, and final
  review are complete on `security/m52-tls-service-identity`; hosted gates are
  pending.
- **Started:** 2026-08-09
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  M51 closeout `047478d0c7fb873ae94aaa6e322b5b08903ed354`.
  Only `main` existed locally/remotely; no open pull request, tag, GitHub
  release, or post-closeout `main` run existed; full Git-object checking passed.
- **Outcome:** Observe the URL-derived TLS service identity on every fixed API
  or bounded redirected asset hop after connected-peer confinement and before
  negotiated-session inspection or HTTP transmission.
- **Acceptance gate:**
  - Normalize the current URL hostname through built-in IDNA to its ASCII
    reference hostname.
  - Require the actual connected TLS socket's observed `server_hostname` to be
    a non-empty case-insensitive match for that reference hostname.
  - Require `getpeercert(binary_form=True)` to return non-empty immutable DER
    bytes from the actual socket.
  - Perform the check after M49 actual connected-peer validation and before
    the M51 negotiated-session check or any HTTP method, path, or header; repeat
    it for every redirect.
  - Map missing/unsupported accessors, malformed or mismatched values, invalid
    normalization, and inspection failures to `public_release.tls_failed`
    without exposing a host, certificate, peer, URL, session value, response,
    or credential.
  - Preserve M51 session conformance, M50 context/key-log isolation, M49 peer
    confinement, M48 response/failure semantics, and every M47 identity,
    deadline, size, path, exact-validation, and installed-smoke bound.
  - Change no workflow, runner allocation, action, permission, trigger,
    credential, release mutation, retry, cleanup, dependency, lock, version,
    runtime package, or public API.
  - Add fixture-driven valid/invalid identity, IDNA, ordering, redirect
    independence, failure, boundary-hash, architecture, RFC, and aligned
    maintainer/public documentation.
  - Pass complete CPython 3.12-3.14, graphics, docs, build, installed
    wheel/release smoke, and the exact three-allocation substantive hosted gate.
- **Non-scope:** Certificate parsing or independent hostname matching; custom
  CA bundle/trust store; certificate/SPKI/fingerprint pinning; certificate-
  chain export; client certificates; revocation, OCSP, CRL, or certificate-
  transparency policy; DNSSEC; TLS session tickets/reuse/channel binding;
  proxy support; real tag/release execution; publication, edit, delete,
  rollback, or cleanup; independent/external monitoring; every TLS/CDN/
  geographic path; future availability; immutability; artifact security; PyPI;
  supported release-channel claims; runtime/public API, dependency, lock,
  package version, or deferred subsystem changes.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Current evidence:** Python 3.14.7 documents that hostname verification
  requires a supplied `server_hostname`, exposes its IDNA A-label on the socket,
  and returns the peer certificate in DER form. RFC 9525 defines the client
  reference identity and server-presented certificate relationship. Findings-
  first review corrected a non-ASCII case-fold confusable and added missing-
  accessor/invalid-IDNA regressions. Focused M52 behavior, final whole-tree
  static/architecture/docs, complete CPython 3.12-3.14, real-wgpu,
  profiles, both vertical slices, benchmark validation, record-inclusive
  reproducible builds, isolated wheel, and release smoke pass as recorded in
  test evidence. The final exact-tree suites each passed 2,044 tests with 14
  expected skips. Review found that invalid IDNA could fail inside a real
  connection before reaching the intended TLS failure boundary; the corrected
  candidate derives and uses the ASCII reference before connection creation,
  then observes the actual socket after peer confinement. The corrected focused
  gate passes 126 assertions with clean Ruff, strict Pyright, and strict docs;
  every corrected complete CPython 3.12-3.14 suite passes 2,044 tests with 14
  expected skips. Corrected reproducible build, isolated-wheel, and complete
  release smoke, post-record static/architecture/docs, archive/scope scans, and
  repeat findings-first review pass with no remaining finding. Hosted
  validation remains; no hosted run, PR, merge, tag, or release is yet claimed.
