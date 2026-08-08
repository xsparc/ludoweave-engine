# Current Task

- **Task:** M39 - release-tag integrity enforcement
- **Status:** Implementation and public integration record are complete and
  squash-integrated; publishing the zero-run closeout record on
  `records/m39-closeout`.
- **Started:** 2026-08-09
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  commit `185e206d6b9c1e97512e289bcba84701dc29c147`. Only `main` existed locally
  and remotely, no pull request, issue, or local/remote tag was open/present,
  and `git fsck --full --no-dangling` passed.
- **Outcome:** Fail the existing tag-release job before expensive or publishing
  work unless the exact version ref is an annotated GitHub-verified signed tag
  at the checked-out event commit and that commit is reachable from
  `origin/main`.
- **Acceptance gate:**
  - Strictly validate bounded tag/SHA identities and capped duplicate-free
    GitHub ref/tag JSON without emitting signature or payload content.
  - Require exact GitHub ref, annotated tag object, tag/commit targets,
    `verified=true`, `reason=valid`, and non-empty verification evidence.
  - Require matching local annotated tag/commit objects, exact `HEAD`, and
    `origin/main` ancestry.
  - Fail malformed, missing, oversized, unsigned, lightweight, retargeted,
    detached, missing-Git, and non-main cases with versioned structured errors.
  - Run immediately after version validation and before system setup,
    dependency synchronization, tests, build, staging, attestation, or
    publication in the existing tag job.
  - Preserve the M38 pull-request topology and release job; add no runner,
    action, permission, trigger, dependency, credential, cache key, or
    publication authority.
  - Document GitHub as signature-verification authority and explicitly reject
    signer/key allowlist, local trust-store, immutable-release, PyPI, supported-
    channel, tag-creation, or publication claims.
  - Run the complete local gate and one substantive hosted pull-request gate.
- **Non-scope:** Creating/pushing a tag; GitHub release or PyPI publication;
  signer authorization or key lifecycle; immutable release settings; runtime or
  public API; persistent formats/protocols; package version/dependency/lock;
  platform/version support; attestation changes; deferred runtime subsystems.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Current evidence:** Exact implementation head
  `f71d8ddbf816873cf9af8ea6538112ff0e75553e` passed run `31264314307` in
  exactly three allocations: Linux 6m43s, macOS 2m33s, and Windows 3m30s.
  Squash `4e30b4bf3b911270ab4e1bd117d49ca0d090a0a7` preserves the reviewed tree,
  exact base parent, valid GitHub signature, and standalone DCO trailer. Public
  record PR #69 passed its 33-second Linux documentation allocation while the
  desktop umbrella skipped without a runner; squash
  `166dcb2dc619dbc721207eece273c0fd9437f9ff` also preserves the reviewed tree,
  exact parent, valid signature, and DCO trailer. Neither merge allocated a
  `main` run. Before this closeout branch, only clean synchronized `main`
  remained locally/remotely and no pull request was open.
