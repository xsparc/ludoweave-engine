# Current Task

- **Task:** M38 - distribution reproducibility enforcement
- **Status:** In progress on `maintenance/m38-distribution-reproducibility`.
- **Started:** 2026-08-08
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  commit `3578da64b2686cd8d63340aeb1eed30f5c4cb761`. Only `main` existed locally
  and remotely, no pull request or issue was open, and
  `git fsck --full --no-dangling` passed.
- **Outcome:** Fail closed unless two same-source distribution builds contain
  the exact matching pure wheel/source pair and are byte-identical. Run the
  comparison inside the existing Linux pull-request and tag-release build jobs
  before smoke, staging, attestation, or publication.
- **Acceptance gate:**
  - Strictly validate distinct directories, exact ordinary-file artifact sets,
    pure-wheel/source filename identity, byte counts, and SHA-256 values.
  - Reject missing, extra, nested, symlinked, unreadable, inconsistently named,
    platform-specific, or byte-divergent artifacts with structured failures.
  - Emit deterministic versioned JSON on success and failure.
  - Prove two actual clean-source builds match and synthetic mismatches fail.
  - Preserve the M37 trusted documentation lane and complete three-allocation
    substantive gate.
  - Add only one repeat build to each existing distribution job; add no runner,
    job, matrix entry, action, permission, trigger, credential, or dependency.
  - Document the same-source/same-job guarantee and explicitly reject cross-
    platform, hermetic, independent-rebuilder, provenance, or publication claims.
  - Run the complete local gate and one substantive hosted pull-request gate.
- **Non-scope:** Runtime or public API; persistent formats/protocols; package
  version, dependency, lock, platform/version support; timestamp-policy change;
  cross-platform comparison; artifact-attestation changes; tag, release, PyPI
  publication, certification, or any deferred runtime subsystem.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Current evidence:** The exact baseline lock resolves 46 packages and 17
  inherited release/CI tests pass. Two clean Windows builds match byte-for-byte
  at wheel SHA-256 `bccd986ef625342167f45a49d9d7837fd9137c97ec796026d2cb546b659b2eed`
  and sdist SHA-256
  `12a61a083cce7bbe318f9ff12c3d0cd9a55bf50f1ee5eb7c8c32c6cda58dbdaa`.
  The corrected verifier has ten passing behavior/adversarial cases plus one
  Windows symlink-capability skip and validates those real artifacts. Complete
  verifier/release/architecture focus passes 352 tests plus that skip. Strict
  Pyright passes after restoring the locked graphics extra removed by M37's
  documentation-lane local proof.
