# Release process and artifact verification

Only maintainers publish official releases. The `release.yml` workflow runs for
an exact `vVERSION` tag and refuses a tag that differs from `pyproject.toml`.
The repository does not publish a release from pull-request CI.

## Candidate contents

`scripts/release_artifacts.py` stages a new empty directory containing:

- the pure `py3-none-any` wheel and source distribution;
- a deterministic versioned sample ZIP;
- Apache-2.0 `LICENSE` and project `NOTICE`;
- the direct optional-dependency notice inventory;
- versioned release notes;
- an SPDX 2.3 JSON SBOM describing the baseline wheel;
- a versioned JSON release manifest with sizes and SHA-256 digests;
- `SHA256SUMS` covering every other staged file.

The baseline SBOM has one package because the wheel has no runtime dependencies
and redistributes no optional graphics providers. Locked contributor/graphics
packages are installed separately under their own distributions and notices.

## Maintainer gate

1. Require the milestone PR's complete local and hosted gates to pass.
2. Confirm the changelog, version, date, release notes, compatibility status,
   security policy, notices, and retrospective agree.
3. Build/stage/smoke the candidate from a clean signed commit.
4. Create a signed `vVERSION` tag at that exact commit and push the tag.
5. The least-privilege tag workflow reruns quality/tests/docs, builds/stages and
   smokes artifacts, creates GitHub build-provenance and SPDX attestations, and
   creates a prerelease with the staged files.
6. Download the published assets, verify checksums and attestations, install the
   wheel in a clean environment, and run the sample bundle before announcing.

No PyPI upload is configured in community alpha. Name reservation, trusted
publishing, and a non-prerelease support policy require separate maintainer
decisions.

M26/RFC-0009 adds offline admission machinery for the future supported
deprecation-capable feature-release channel. The current workflow remains
prerelease-only, no release record is admitted, and gate 6 remains false. See
the [supported release channel readiness guide](supported-release-channel-readiness.md).

M27/RFC-0010 adds the empty reviewed external-contributor rehearsal fixture and
evaluator to the deterministic sample bundle. Release smoke proves only that
the installed offline evidence path works; it is not an external contribution,
feedback artifact, or usability result. See the
[external-contributor rehearsal readiness guide](external-contributor-rehearsal-readiness.md).

M30/RFC-0013 adds the empty reviewed published-wheel installation-matrix
fixture and evaluator to the deterministic sample bundle. Release smoke proves
only that the installed offline evidence path works; it is not a public
release, independent installation, matrix result, or support claim. See the
[installation-matrix readiness guide](installation-matrix-readiness.md).

M31/RFC-0014 adds the empty reviewed response/review-latency fixture and
evaluator to the deterministic sample bundle. Release smoke proves only that
the installed offline evidence path works; it is not a human response, review,
latency measurement, service-level result, or support claim. See the
[response and review latency readiness guide](response-review-latency-readiness.md).

M32/RFC-0015 adds the empty reviewed replay-divergence-rate fixture and
evaluator to the deterministic sample bundle. Release smoke proves only that
the installed offline evidence path works; it is not a complete CI replay
cohort, measured divergence rate, reliability result, or release gate. See the
[replay-divergence-rate readiness guide](replay-divergence-rate-readiness.md).

## Consumer verification

Verify local checksums using the platform's SHA-256 tool, then verify official
GitHub provenance:

```console
gh attestation verify ludoweave-VERSION-py3-none-any.whl -R xsparc/ludoweave-engine
gh attestation verify ludoweave-VERSION-py3-none-any.whl -R xsparc/ludoweave-engine --predicate-type https://spdx.dev/Document/v2.3
```

Artifact attestations are stored by GitHub and bind the subject digest to the
tag workflow. `RELEASE_MANIFEST.json` is reproducible release metadata, not a
cryptographic signature or substitute for the hosted attestation.
