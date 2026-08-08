# Current Task

- **Task:** M44 - published release attestation integrity
- **Status:** Implementation is locally validated on
  `release/m44-attestation-verification`; final review and pull-request
  publication are in progress.
- **Started:** 2026-08-09
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized `main`, `origin/main`, and `origin/HEAD`
  commit `0b3b9eb982a67eee1833f3a8f920671f8ffd006b`. Only `main` existed locally
  and remotely, no pull request, local/remote tag, or GitHub release was
  present, and `git fsck --full --no-dangling` passed.
- **Outcome:** Require every exact published asset retrieved and revalidated by
  M43 to have SLSA v1 provenance from the exact release workflow/source, and
  require the one pure wheel to have an SPDX 2.3 SBOM attestation.
- **Acceptance gate:**
  - Consume only the canonical bounded M43 retrieval plan, exact downloaded
    directory, event tag, and checked-out commit.
  - Revalidate plan and directory equality, safe regular files, size bounds,
    exact tag/commit syntax, and exactly one pure LudoWeave wheel before any
    attestation command.
  - Bind every verification to repository `xsparc/ludoweave-engine`, signer
    workflow `xsparc/ludoweave-engine/.github/workflows/release.yml`, the exact
    tag ref, exact source/signer commit, GitHub Actions OIDC issuer, hosted
    runner class, predicate type, and at most 30 candidate bundles.
  - Verify SLSA v1 provenance for at most 32 assets and SPDX 2.3 for exactly
    one wheel: at most 33 sequential child calls, each with null streams and a
    30-second timeout.
  - Emit only versioned aggregate counts on success and structured generic
    errors on failure; do not expose attestation, predicate, certificate,
    environment, path, token, or artifact content.
  - Run only after M43's exact downloaded-byte verification in the existing
    tag job.
  - Add no job, runner, action, permission, trigger, dependency, credential,
    tag, release, upload, publication, rollback, cleanup, runtime, package,
    public-API, lock, or SemVer change.
  - Document the exact integrity/identity claim and all security, independent-
    build, predicate-truth, future availability/revocation, global access,
    immutability, consumer, and support non-claims.
  - Run the complete local gate and one substantive hosted pull-request gate.
- **Non-scope:** Creating/pushing a tag or release; uploading/publishing;
  changing attestation creation; parsing bundles or predicates; automatic
  retry/unpublish/delete/rollback/cleanup; immutable-release settings;
  artifact vulnerability/security certification; independent/trusted builds;
  unauthenticated/global availability; future monitoring or revocation policy;
  consumer installation; PyPI; supported release channel; runtime/public API;
  package version/dependency/lock; deferred subsystems.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Current evidence:** M43 zero-run closeout PR #82 squash-integrated as exact
  clean base `0b3b9eb982a67eee1833f3a8f920671f8ffd006b` with sole parent the M43
  integration record, exact reviewed tree, valid GitHub signature, standalone
  DCO trailer, and no post-merge run. Baseline inherited release tests passed
  86 tests with two capability skips. Official GitHub CLI documentation and
  installed CLI help expose the required SLSA/SPDX predicate and identity
  policy flags. The standard-library verifier, focused adversarial tests,
  release workflow integration, RFC-0027, architecture guards, and public
  documentation are complete locally. The final recorded tree passes 366
  architecture tests and the 1,906-test CPython 3.12 graphics suite; CPython
  3.13/3.14, real wgpu, profiles, deterministic samples, documented benchmark
  validators, reproducible builds, isolated-wheel smoke, and complete release
  smoke also pass. No real release or hosted attestation pass is claimed.
