# Current Task

- **Task:** M41 - release-notes body integrity
- **Status:** Implementation squash-integrated; publishing the documentation-
  only integration record on `records/m41-integration`.
- **Started:** 2026-08-09
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  commit `9983e0da88b6aef999d26498cc6438f0b3c5927b`. Only `main` existed locally
  and remotely, no pull request, local/remote tag, or GitHub release was
  present, and `git fsck --full --no-dangling` passed.
- **Outcome:** Publish the private draft only when its authenticated release-
  notes body exactly matches bounded staged `RELEASE_NOTES.md`.
- **Acceptance gate:**
  - Advance the internal draft-integrity protocol from `/1` to `/2` because the
    acceptance contract becomes stronger.
  - Read only the fixed staged `RELEASE_NOTES.md` regular non-symlink member;
    require non-empty strict UTF-8 without NUL and cap it at 256 KiB.
  - Require exact equality with the authenticated GitHub release `body`; reject
    missing, null, non-text, substituted, truncated, newline-, whitespace-, or
    Unicode-different bodies.
  - Emit no release-note content on success or failure; preserve structured
    stable errors and the complete M40 asset checks.
  - Preserve both workflow files exactly; add no runner, action, permission,
    trigger, dependency, credential, cache key, API call, or publication
    authority.
  - Document source-body trust and explicitly reject rendered-Markdown, link,
    factual-completeness, immutability, PyPI, and supported-channel claims.
  - Run the complete local gate and one substantive hosted pull-request gate.
- **Non-scope:** Creating/pushing a tag, draft, or release; asset upload; GitHub
  release or PyPI publication; rendered Markdown or link validation; factual
  release-note review; immutable-release settings; independent remote download;
  signer/key lifecycle; runtime or public API; persistent formats/protocols;
  package version/dependency/lock; platform support; attestations; deferred
  runtime subsystems.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Current evidence:** M40 closeout PR #73 exact head
  `e1b07f781096370fa3b6f820bc80dc1d4c585279` changed only three `.project`
  paths and allocated no run, check, review, comment, or thread. Squash
  `9983e0da88b6aef999d26498cc6438f0b3c5927b` preserves the reviewed tree,
  exact parent, valid GitHub signature, standalone DCO trailer, and zero
  post-merge runner usage. M41 inherited 25 validator/workflow tests with one
  Windows symlink skip. After correcting Windows fixture newline and case-ID
  behavior, focused format/lint/strict typing pass and 26 behavior/adversarial
  tests pass with the same capability skip. RFC-0024 and the release/security/
  architecture surfaces are integrated; a further 30-test focused gate proves
  release-note content remains absent from both success and failure output.
  Findings-first review corrected notes-member error taxonomy. The corrected
  complete Python 3.12 suite passes 1,830 tests with 13 expected skips; Python
  3.13 and 3.14 each pass 1,820 with 13 expected skips; real graphics, profiles,
  deterministic samples, reproducible distributions, installed-wheel smoke,
  complete release smoke, and exact synthetic-draft verification all pass.
  Exact implementation head `ec051d4fd2da80235da1a94642158ebe384cb2b0`
  passed run `31269399211` in three allocations: Linux 6m55s, Windows 2m44s,
  and macOS 2m12s. With no review/comment/thread, PR #74 squash-integrated as
  `89a641559c246e971869a3ae06a878de81bffcee`; the reviewed tree, exact parent,
  valid signature, standalone DCO, and zero post-merge run are verified. The
  feature branch is deleted locally and remotely.
