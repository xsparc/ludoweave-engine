# Current Task

- **Task:** M49 - public release connected-peer confinement
- **Status:** Feature and integration record fully validated and
  squash-integrated; closing factual records on `records/m49-closeout`.
- **Started:** 2026-08-09
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  M48 closeout commit `049cdbcf2769a1c2359593f642e37697d5bf7400`.
  Only `main` existed locally/remotely; no open pull request, local/remote tag,
  or GitHub release existed; full Git-object checking passed.
- **Outcome:** Require every fixed API or redirected asset connection to prove
  that its actual TLS socket peer is globally reachable before transmitting an
  HTTP request, without relying on a CDN hostname allowlist or changing release
  authority.
- **Acceptance gate:**
  - Explicitly connect each `HTTPSConnection` within M48's existing timeout and
    validate the actual `getpeername()` result before request transmission.
  - Require a well-formed IPv4/IPv6 address and actual peer port 443; normalize
    IPv4-mapped IPv6 to its embedded IPv4 classification.
  - Allow only globally reachable unicast peers. Reject private, shared,
    loopback, link-local, documentation, benchmarking, unspecified, multicast,
    reserved, and other non-global peers with
    `public_release.peer_forbidden`.
  - Apply the peer check independently to the fixed `api.github.com` request
    and every bounded `302` asset hop so DNS rebinding cannot bypass the check
    between a separate resolution pass and the actual connection.
  - Map connect/peer timeout to `public_release.request_timeout`; malformed,
    unavailable, wrong-port, or other peer inspection failures to
    `public_release.request_failed`; disclose no host, address, URL, or response
    content in public output.
  - Preserve M48's response, header, credential, TLS, deadline, document, plan,
    asset, byte, path, exclusive-partial, exact-validation, and installed-smoke
    bounds.
  - Change no workflow, runner allocation, action, permission, trigger,
    credential, release mutation, retry, cleanup, dependency, lock, version,
    runtime, package, or public API.
  - Add fixture-driven IPv4/IPv6, mapped-address, redirect-hop, ordering, and
    failure-code tests; an accepted RFC; architecture protection; and aligned
    public/maintainer documentation.
  - Pass complete CPython 3.12-3.14, graphics, docs, build, installed
    wheel/release smoke, and the exact three-allocation hosted gate.
- **Non-scope:** Creating or pushing a tag; creating, uploading, publishing,
  editing, deleting, or unpublishing a release; hostname/CDN or fixed-IP
  allowlists; a separate DNS preflight; DNSSEC; packet-level network sandboxing;
  hiding the TLS handshake required to discover the connected peer; retries or
  automatic cleanup; external monitoring; independent verification; every CDN
  or geographic path; future availability; immutability; artifact security;
  PyPI; a supported release channel; runtime/public API, dependency/lock/version,
  or deferred subsystems.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Current evidence:** M48 feature PR #95, documentation record PR #96, and
  zero-run closeout PR #97 are fully validated and squash-integrated. Final
  closeout `049cdbcf2769a1c2359593f642e37697d5bf7400` has reviewed tree
  `3ea3e76c4dc0b5b310df557ba92ca8ab215e18c6`, sole parent the M48 record
  squash, a GitHub-valid signature, standalone DCO, and no post-merge run.
  Only synchronized `main` remained with no open PR, tag, or release. Current
  GitHub documentation retains the bounded asset `200`/`302` shape; current
  Python and IANA sources define actual connected-peer inspection and global
  IPv4/IPv6 reachability. After two test-fixture typing corrections, strict
  Ruff/Pyright and 74 non-documentation M47-M49 assertions pass. A direct
  CPython 3.12-3.14 classification probe produced identical results for the
  documented corrected special-purpose ranges. The documentation-integrated
  focus passes 83 tests; all 292 Python files pass Ruff formatting/lint and
  strict Pyright, and strict docs build. All 457 architecture tests pass. The
  exact graphics-enabled CPython 3.12, 3.13, and 3.14 trees each pass 1,995
  tests with 14 expected skips. Ten real-wgpu tests, both profile contracts,
  Clockwork Arena, Agent World Builder, reproducible distribution,
  isolated-wheel smoke, and complete release smoke pass locally. Final
  record-inclusive static and distribution gates pass; the 94-entry wheel has
  no script, test, native, or WASM payload. Scope, credential, identity,
  documentation, and initial findings-first review passed. Feature PR #98
  exact head `c19d37f24516bbdc8bea71b521936ac7daf1f8e9` then passed exactly three
  hosted allocations, but hosted review correctly identified CPython
  classifications that left deprecated IPv6 site-local and reserved peers
  permitted. The unmerged correction explicitly rejects both classifications
  and adds `fec0::1`/`5f00::1` regressions. Formatting, Ruff, strict Pyright,
  31 focused assertions, and complete graphics-enabled CPython 3.12-3.14
  suites now pass; each complete suite has 1,997 passes and 14 expected skips.
  Ten real-wgpu tests, both three-repeat profiles, Clockwork Arena, and Agent
  World Builder also revalidate. Replacement PR #99 exact head
  `01c955f0256c0c6e3a34afaf317c828e439b87ca` passed run `31307775820` in
  exactly three allocations: Linux `93230730827` in 422 seconds, macOS
  `93231457896` in 143 seconds, and Windows `93231457841` in 230 seconds.
  Linux and both supported Ubuntu compatibility suites passed 2,001 tests;
  each nonbaseline suite had one expected skip. Both desktop compatibility
  suites also passed 2,001 tests with one skip. The PR was clean and mergeable
  with zero review, comment, or thread. GitHub-verified squash
  `842aedc67a7ae4584821c4d8bc96a4ed8cb334c3` has reviewed tree
  `a9755cbf65dfeba5087f5037f73bc6027c408444`, sole parent the M48 closeout,
  and standalone DCO. No post-merge `main` run was allocated; the feature
  branch is deleted locally/remotely. Integration record and zero-run closeout
  remain. No real M49 tag/release execution exists or is claimed.
- **Integration record:** Four-Markdown PR #100 exact head
  `6d04bbf9f77382b5df3c4d1a7f5d0b70496751f9` classified documentation-only.
  Run `31308454299` passed in one 31-second Linux allocation with 457
  architecture tests, strict docs, reproducible build, wheel smoke, and
  release smoke; desktop umbrella job `93232491763` had zero steps and was
  skipped. The PR had no review, comment, or thread. Verified squash
  `d6ef4fef7f42a8bd961ea549eb3deb618a0c073f` has exact reviewed tree, sole
  parent the M49 feature squash, a GitHub-valid signature, standalone DCO, and
  no post-merge run. Its branch is deleted locally/remotely. Only this
  three-file zero-run closeout remains before selecting the next milestone.
