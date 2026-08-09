# Current Task

- **Task:** M55 - public release HTTP response framing
- **Status:** PR #117's first exact-head gate passed, then delayed review found
  that CPython normalizes other raw `HTTP/1.x` status-line tokens to public
  `version=11`. The contract/test correction on
  `security/m55-http-response-framing` is fully validated locally and review-
  clean; corrected DCO commit and hosted exact-head validation remain. No merge
  is authorized yet.
- **Started:** 2026-08-10
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized M54 closeout
  `aab15d601eb4402213f2e058f270237b964f1000`, with only `main` present and no
  open pull request, tag, release, or post-closeout `main` run.
- **Outcome:** Validate documented HTTP/1.1 response framing on every public-
  release response before status, redirect, or body data is consumed.
- **Acceptance:** Require the documented HTTP/1.1-class response value integer
  `11` without claiming exact raw status-line token identity; permit
  `Transfer-Encoding` only when its string value is exactly `chunked` under
  case-insensitive comparison; reject transfer coding with `Content-Length`;
  and require any content length to be a string before existing syntax and
  bounds. Repeat on every redirect. Stable content-silent failures preserve a
  supported local cause.
- **Boundary:** No workflow, runner allocation, action, permission, trigger,
  credential, release mutation, dependency, lock, version, runtime package,
  public API, private response-state dependency, raw HTTP/chunk parser,
  alternate client, HTTP/2 or HTTP/3, proxy, decompression, retry, cache, or
  network sandbox. Fixture/PR evidence is not a real public release observation
  or exact status-line evidence or a general request-smuggling defense.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Evidence:** Official Python 3.14 and RFC 9112 review defines the public
  metadata and ambiguity boundary. All 157 inherited M47-M54 assertions passed
  after compatible valid fakes exposed `version=11`; all 30 M55 behavior
  assertions excluding docs passed, then all 188 focused M47-M55 assertions and
  strict docs passed after RFC/public/maintainer documentation was added. All
  supported-Python, real-graphics, profile, vertical-slice, benchmark,
  reproducible-build, installed-wheel, and release-smoke gates pass locally;
  findings-first local review had no actionable issue. Hosted run
  `31324078779` passed exactly three Linux-first allocations, but delayed review
  produced one valid P2 about CPython status-line normalization. The correction
  must pass full local and hosted validation before merge.
- **Hosted gate:** A substantive ready PR must allocate exactly three
  Linux-first jobs, followed only by Windows and macOS after Linux succeeds.
