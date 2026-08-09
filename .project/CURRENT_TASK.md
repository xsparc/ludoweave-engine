# Current Task

- **Task:** M56 - public release status and redirect-reference conformance
- **Status:** Complete. Corrected feature PR #120 and integration-record PR
  #121 are fully validated, review-clean, squash-integrated, and branch-clean;
  publishing the exact three-file closeout on `records/m56-closeout`.
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
  complete percent escapes. Permit bracket delimiters only inside the parsed
  authority, not its path, query, or fragment. Revalidate the resolved bounded
  HTTPS URL before another request. Stable content-silent errors preserve
  supported local causes, and every redirect repeats the complete check.
- **Boundary:** Relative and cross-host absolute references remain supported,
  with M49-M55 peer, TLS, framing, deadline, size, and exact-byte checks on
  every hop. No host allowlist, private response state, raw HTTP/URI parser,
  alternate client, proxy, DNS preflight, network sandbox, workflow, runner,
  action, permission, trigger, credential, release mutation, dependency, lock,
  version, runtime package, public API, or release authority. Fixture/PR
  evidence is not a real public release observation or general SSRF defense.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Local evidence:** The final corrected candidate passes all 226 focused
  M47-M56 assertions, 604 architecture assertions, strict static/docs gates,
  and 2,144 tests with 14 expected skips on each supported Python. Ten
  real-wgpu tests, both profiles, both vertical slices, reproducible builds,
  isolated-wheel smoke, complete release smoke, archive/scope checks, and
  repeat findings-first review pass. The reviewer-derived tests-first probe
  failed the two malformed bracket references while 14 controls passed; the
  component-aware correction then passed all 16 cases, including a bracketed
  IPv6 authority.
- **Hosted evidence:** Corrected PR #120 head
  `35b94a42b10cbd8f75048d3200e95a4aca81fa5d` passed run `31329613114` in
  exactly three Linux-first allocations. Linux passed in 7m22s before macOS
  and Windows began; they passed in 2m19s and 4m00s. Baseline and every
  compatibility suite passed 2,148 tests, with one expected skip outside the
  baseline. Every platform passed real graphics, profiles, Clockwork Arena,
  and Agent World Builder. Hosted reproducibility, installed-wheel smoke, and
  complete release smoke passed.
- **Integration:** The sole valid P2 review thread was answered and resolved.
  Two delayed audits found no new issue comment, review activity, or unresolved
  thread. Head-pinned, GitHub-verified squash
  `22c432310fae2f9ac372062cbd465cc2617fb95c` has the exact corrected feature
  tree, sole parent M55 closeout, valid signature, and standalone DCO. The
  feature branch is deleted locally and remotely. Synchronized `main` has no
  post-merge run, open PR, non-main remote branch, tag, or release. Integration
  PR #121 exact head `db7c50009243fa7cf3bf9cd8f57afb4589dec7e7`
  passed run `31330464522` in one 38-second Linux allocation; all 604
  architecture assertions, strict docs, reproducible builds, installed-wheel
  smoke, and complete release smoke passed, while the desktop umbrella skipped
  with zero steps. Two delayed audits found no comment, review, or thread.
  GitHub-verified squash `acc6893ef4cadf9a17c87cd578e38b7802a3ed77`
  reproduces the reviewed integration-record tree with the feature squash as
  sole parent, valid signature, and standalone DCO. Both integration branches
  are deleted locally/remotely.
- **Closeout gate:** The exact three-file `.project/**` record must allocate
  zero hosted runs or checks.
