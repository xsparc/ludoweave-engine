# Current Task

- **Task:** M56 - public release status and redirect-reference conformance
- **Status:** Locally complete and review-clean on
  `security/m56-http-redirect-reference`; preparing exact-head publication.
- **Started:** 2026-08-10
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized M55 closeout
  `e7f700454adf1c11c80cb1ba684ed3318f7876e4`, with only `main` present and no
  open pull request, tag, release, or post-closeout `main` run.
- **Outcome:** Validate every public-release response status and every followed
  redirect reference before comparison, resolution, or body use.
- **Acceptance:** Require status to be a non-boolean integer from 100 through
  599. Require every followed `302` to expose a documented header-pair list
  containing exactly one case-insensitive Location field whose value is one
  1-to-8,000-octet ASCII URI-reference with valid RFC 3986 characters and
  complete percent escapes. Revalidate the resolved bounded HTTPS URL before
  another request. Stable content-silent errors preserve supported local
  causes, and every redirect repeats the complete check.
- **Boundary:** Relative and cross-host absolute references remain supported,
  with M49-M55 peer, TLS, framing, deadline, size, and exact-byte checks on
  every hop. No host allowlist, private response state, raw HTTP/URI parser,
  alternate client, proxy, DNS preflight, network sandbox, workflow, runner,
  action, permission, trigger, credential, release mutation, dependency, lock,
  version, runtime package, public API, or release authority. Fixture/PR
  evidence is not a real public release observation or general SSRF defense.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Evidence:** The clean M47-M55 baseline passed 189 assertions. Official
  Python 3.14 and RFC 9110/3986 review established the public metadata and URI
  boundary. A tests-first probe produced 25 failures, six passes, and two
  intentionally deselected documentation/boundary checks, confirming float
  status acceptance, raw malformed-status failures, joined Location use, and
  permissive URL recovery. The implementation and compatible fixtures now pass
  all 34 M56 behavior, boundary, and documentation assertions, while all 223
  focused M47-M56 assertions pass together. Whole-tree formatting, Ruff,
  Pyright, 601 architecture assertions, strict docs, and all graphics-enabled
  CPython 3.12-3.14 suites pass. Real-wgpu, profiles, both vertical slices,
  every documented benchmark validator, reproducible builds, installed-wheel
  smoke, and complete ten-artifact release smoke pass. Findings-first review
  corrected one narrow RFC wording implication, revalidated all 223 focused
  assertions and strict docs, and found no remaining actionable issue. The
  final record-inclusive local gate also passes. Hosted exact-head validation
  remains pending.
- **Hosted gate:** This substantive security/release-tooling change requires
  exactly three Linux-first allocations, with Windows and macOS starting only
  after Linux qualification succeeds.
