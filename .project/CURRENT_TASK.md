# Current Task

- **Task:** M40 - draft-release asset integrity
- **Status:** The initial exact-head review finding is corrected and fully
  validated locally on `release/m40-draft-assets`; preparing a correction
  commit and hosted rerun. The passing initial hosted head will not merge.
- **Started:** 2026-08-09
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  commit `49fba13477890bf6bf1c9e6a645e669b3a69492f`. Only `main` existed locally
  and remotely, no pull request, local/remote tag, or GitHub release was
  present, and `git fsck --full --no-dangling` passed.
- **Outcome:** Keep the existing GitHub prerelease private as a draft until the
  authenticated remote asset inventory exactly matches bounded local staging.
- **Acceptance gate:**
  - Strictly validate capped duplicate-free GitHub release JSON plus bounded
    local regular files and safe identities.
  - Require exact tag/title, `draft=true`, `prerelease=true`,
    `immutable=false`, and one complete uploaded remote asset per local file.
  - Require exact asset names, byte sizes, and SHA-256 digests; fail missing,
    extra, duplicate, pending, renamed, truncated, or digest-different assets.
  - Create the draft without assets, upload without clobbering, fetch through a
    pinned REST API version, verify, and only then publish.
  - Leave failed drafts unpublished for deliberate inspection; never delete or
    clobber release evidence automatically.
  - Preserve the M39 pull-request topology and existing tag job; add no runner,
    action, permission, trigger, dependency, credential, cache key, or
    publication authority.
  - Document GitHub as the remote digest authority and explicitly reject
    independent-storage, immutability, PyPI, supported-channel, real-tag, or
    real-publication claims.
  - Run the complete local gate and one substantive hosted pull-request gate.
- **Non-scope:** Creating/pushing a tag, draft, or release; asset upload; GitHub
  release or PyPI publication; automatic failed-draft deletion; immutable
  release settings; independent remote downloads; signer/key lifecycle; runtime
  or public API; persistent formats/protocols; package version/dependency/lock;
  platform/version support; attestation changes; deferred runtime subsystems.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Current evidence:** Complete Python 3.12 passes 1,818 tests with 12 expected
  skips; Python 3.13 and 3.14 each pass 1,808 with 13 expected skips. Real-wgpu,
  both profiles, both vertical samples, deterministic two-build comparison,
  installed-wheel smoke, ten-artifact release smoke, and exact real-staging
  synthetic-draft verification pass. Findings-first review corrected the draft
  lookup to fetch the authenticated numeric release ID and found no remaining
  scope, credential, archive, native, runtime, dependency, lock, or CI drift.
