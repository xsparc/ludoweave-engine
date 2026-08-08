# Current Task

- **Task:** M42 - published prerelease integrity
- **Status:** Implementation squash-integrated; publishing the documentation-
  only integration record on `records/m42-integration`.
- **Started:** 2026-08-09
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  commit `0dec2254a9d9483b27d158aaad108340e9c94e28`. Only `main` existed locally
  and remotely, no pull request, local/remote tag, or GitHub release was
  present, and `git fsck --full --no-dangling` passed.
- **Outcome:** Require one exact authenticated release database identity to
  satisfy both the private-draft contract and the final public-prerelease
  contract before the release job can succeed.
- **Acceptance gate:**
  - Advance the internal draft-integrity protocol from `/2` to `/3` and make
    expected `draft` or `published` state explicit on every invocation.
  - Require drafts to remain mutable prereleases with null `published_at`.
  - Require published records to have `draft=false`, `prerelease=true`, a JSON
    boolean immutable field, and a syntactically/calendrically valid UTC
    `published_at`.
  - Retain exact tag, title, bounded notes-body, and uploaded asset identity
    verification in both states; emit only state plus existing safe identities.
  - Carry only the validated numeric release ID across `gh release edit`, fetch
    that same ID once after publication, and fail if the public record differs.
  - Add no job, runner, action, permission, trigger, dependency, credential,
    cache key, tag, release, upload, or publication authority.
  - Document that this is postpublication observation, not automatic rollback,
    later-mutation prevention, or immutable-release policy.
  - Run the complete local gate and one substantive hosted pull-request gate.
- **Non-scope:** Creating/pushing a tag, draft, or release; uploading or
  publishing; automatic unpublish/delete/rollback; enabling or requiring
  immutable releases; public-asset download; rendered Markdown, link, or
  factual review; signer/key policy; deployment environments or tag rules;
  PyPI; supported release channel; runtime/public API; persistent formats;
  package version/dependency/lock; platform support; deferred subsystems.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Current evidence:** M41 closeout PR #76 exact head
  `5d891d0bfa030ff8387d9c384fafa4aa81abbdf8` changed only three `.project`
  paths and allocated no run, check, review, comment, or thread. Squash
  `0dec2254a9d9483b27d158aaad108340e9c94e28` has sole parent the M41
  integration-record squash, preserves reviewed tree
  `a028eb0492019b42658045bf112ca2fcafd211b4`, has a valid GitHub signature and
  standalone DCO trailer, and allocated no post-merge run. M42 inherited 37
  release-integrity tests with two Windows symlink-capability skips. The first
  implementation behavior run passed 39 tests with two skips while formatting
  identified two files; after mechanical formatting and a UTC-alias lint
  correction, focused static/type checks and all 39 behavior tests pass. Two
  intentional M41 historical guards then failed on the stronger protocol and
  workflow hash; after updating that boundary and adding M42 architecture
  coverage, all 54 focused tests pass with two capability skips. Findings-first
  review strengthened published drift/confidentiality and non-mutation guards.
  The corrected complete Python 3.12 suite passes 1,850 tests with 13 expected
  skips; Python 3.13 and 3.14 each pass 1,840 with 14 expected skips; real
  graphics, profiles, deterministic samples, reproducible distributions,
  installed-wheel smoke, complete release smoke, and exact mutable/immutable
  synthetic state verification all pass. Exact implementation head
  `45cd04e627f44400e8bd3adcbeeaf1756160f745` passed run `31271273535` in
  three allocations: Linux 6m54s, Windows 3m39s, and macOS 1m59s. With no
  review, issue comment, review comment, or thread, PR #77 squash-integrated as
  `28dd9d7e282ec85c06b71ed340f3cfcea379d6be`; the reviewed tree, exact parent,
  valid signature, standalone DCO, and zero post-merge run are verified. The
  feature branch is deleted locally and remotely.
