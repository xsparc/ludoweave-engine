# Current Task

- **Task:** M45 - public release consumer-path integrity
- **Status:** Local implementation, review, and validation are complete on
  `release/m45-public-consumer-verification`; exact-head hosted pull-request
  validation remains pending.
- **Started:** 2026-08-09
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  commit `2c5e312a97028d0b835fc174b8abb51df22ea314`. Only `main` existed locally
  and remotely, no open pull request, local/remote tag, or GitHub release was
  present, and `git fsck --full --no-dangling` passed.
- **Outcome:** After M44, verify that the exact public GitHub API release ID and
  every exact M43 asset ID are retrievable without a GitHub credential, still
  match the admitted candidate, and pass complete installed release smoke.
- **Acceptance gate:**
  - Run only after M44 in the existing tag job and receive only the exact
    retained release ID plus expected public title.
  - Fetch only fixed `api.github.com` release/asset numeric-ID endpoints; do
    not consume browser URLs, caller-selected hosts, credentials,
    authorization headers, cookies, client configuration, or unbounded
    redirects.
  - Require HTTPS for initial/redirect protocols, at most three redirects,
    10-second connects, 30-second requests, and a 4-MiB public-document cap.
  - Revalidate the public document against exact local staging, tag, title,
    notes, assets, and published state before downloading any public asset.
  - Reparse the canonical M43 plan and retain positive 63-bit IDs, safe
    basenames, at most 32 assets, 256 MiB per asset, and 512 MiB total.
  - Stream at most each expected size plus one byte into a new partial path,
    reject short/long content, rename only after exact length, then revalidate
    the complete public directory.
  - Run the existing complete release smoke against the public directory,
    including checksums, manifest, SPDX metadata, safe sample extraction,
    isolated wheel installation, and bundled scenarios.
  - Add no job, runner, action, permission, trigger, dependency, credential,
    tag, release, upload, publication, rollback, cleanup, runtime, package,
    public-API, lock, or SemVer change.
  - Document the exact one-point claim and all independent/external consumer,
    clean-machine/cross-platform, browser/CDN/cache/geographic, future,
    immutability, artifact-security, PyPI, and support non-claims.
  - Run the complete local gate and one substantive hosted pull-request gate.
- **Non-scope:** Creating/pushing a tag or release; uploading/publishing;
  enabling immutable releases; automatic retry/unpublish/delete/rollback/
  cleanup; external monitoring; every public delivery path; independent
  verification; cross-platform public installation; PyPI; supported release
  channel; runtime/public API; package version/dependency/lock; deferred
  subsystems.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Current evidence:** M44 feature PR #83, documentation-only record PR #84,
  and zero-run closeout PR #85 are squash-integrated. Final closeout squash
  `2c5e312a97028d0b835fc174b8abb51df22ea314` has sole parent the exact M44
  integration squash, exact reviewed tree, a valid GitHub signature, and a
  standalone DCO trailer; no post-merge `main` run occurred. Only synchronized
  `main` remained and GitHub had no open PR, tag, or release before this branch.
  Official GitHub REST documentation states that public release and asset
  endpoints can be used without authentication and that the numeric asset
  endpoint returns or redirects to binary content for the octet-stream accept
  type. The inherited M39-M44/release baseline passes 100 tests with three
  capability skips. After correcting one stale M43 wording guard and scoping
  historical workflow tests to their own steps, the focused release chain
  passes 106 tests with three capability skips. The final recorded tree passes
  all 373 architecture tests and seven exact extracted-shell regressions on
  each of CPython 3.12-3.14. The complete 3.12 graphics suite passes 1,913
  tests with 14 expected skips; 3.13 and 3.14 each pass 1,902 tests with 15
  skips. Real wgpu,
  profiling contracts, deterministic samples, byte-reproducible distributions,
  isolated-wheel smoke, complete release smoke, and every documented benchmark
  validator pass. Static analysis, strict docs, YAML, Bash syntax, whitespace,
  scope/credential review, and full Git object checking pass. Exact-head
  hosted validation, review, and integration remain pending. No real public
  release-path pass is claimed.
