# Release process and artifact verification

Only maintainers publish official releases. The `release.yml` workflow runs for
an exact signed annotated `vVERSION` tag and refuses a tag that differs from
`pyproject.toml`, lacks GitHub-verified signature evidence, targets a different
checkout, or is not reachable from `origin/main`. The repository does not
publish a release from pull-request CI.

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

Before installed-wheel smoke or staging, M38 builds the wheel and source
distribution twice in distinct directories and runs
`scripts/verify_distribution_reproducibility.py`. Both directories must contain
exactly one matching pure wheel/source-archive pair and the bytes must match.
The deterministic JSON result records exact sizes and SHA-256 identities. This
same-job check is not an independent or cross-platform rebuild claim; see
[RFC-0021](rfcs/0021-enforce-distribution-reproducibility.md).

## Maintainer gate

1. Require the milestone PR's complete local and hosted gates to pass.
2. Confirm the changelog, version, date, release notes, compatibility status,
   security policy, notices, and retrospective agree.
3. Confirm the intended release commit is integrated into `origin/main`.
4. Build twice, verify byte reproducibility, then stage/smoke the candidate
   from that clean signed commit.
5. Create and push a signed annotated `vVERSION` tag at that exact commit.
6. M39 makes the tag job fail first unless GitHub reports a valid tag
   signature and local Git confirms the same annotated object, checkout commit,
   and `origin/main` ancestry. The verifier is loaded from fetched `origin/main`,
   not the tag checkout. `--verify-tag` remains an existence check, not the
   signature gate.
7. The least-privilege tag workflow reruns quality/tests/docs, builds/stages and
   smokes artifacts, and creates GitHub build-provenance and SPDX attestations.
8. M40 creates a private prerelease draft without assets, uploads the complete
   staged set without clobbering, fetches the authenticated GitHub release
   document, and requires every uploaded name, state, size, and SHA-256 digest
   to match local staging before publishing the draft.
9. M41 additionally requires the authenticated draft's source release-notes
   body to exactly match bounded staged `RELEASE_NOTES.md`; note content is not
   emitted by the validator.
10. Download the published assets, verify checksums and attestations, install the
   wheel in a clean environment, and run the sample bundle before announcing.

No PyPI upload is configured in community alpha. Name reservation, trusted
publishing, and a non-prerelease support policy require separate maintainer
decisions.

M39/RFC-0022 trusts GitHub's annotated-tag verification result and separately
checks local object/checkout/main ancestry. It does not install a local trust
store, define a signer or key allowlist, authorize tag creation, enable
immutable releases, or claim that a valid signature alone authorizes a release.
Repository tag rules, protected deployment environments, and workflow-file
governance remain operational controls; this workflow cannot authenticate a
replacement of its own definition by an already-authorized tag actor.

M40/RFC-0023 makes the GitHub draft boundary explicit. The standard-library
validator consumes only bounded local files and a capped strict JSON document;
network and publication remain workflow-owned. Upload or identity failure
leaves an unpublished draft for inspection, and retries never use `--clobber`.
The remote digest is GitHub's authenticated report, not independent storage
verification. M40 does not enable immutable releases, create a real release,
change attestations, or authorize automatic draft deletion.

M41/RFC-0024 advances that internal validator contract to
`ludoweave.release-draft-integrity/2`. It reads only the fixed staged
`RELEASE_NOTES.md` member, caps it at 256 KiB, requires non-empty strict UTF-8
without NUL, and compares it exactly with the authenticated release `body`.
Missing, null, substituted, truncated, or normalization-different text fails
before publication. The gate does not log note content, inspect rendered
Markdown, evaluate links or factual accuracy, or add a network call, workflow
allocation, permission, dependency, release, or publication authority.

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

M33/RFC-0016 adds the empty reviewed benchmark-regression-rate fixture and
evaluator to the deterministic sample bundle. Release smoke proves only that
the installed offline evidence path works; it is not a controlled paired
benchmark cohort, measured regression rate, performance result, native-code
decision, or release gate. See the
[benchmark-regression-rate readiness guide](benchmark-regression-rate-readiness.md).

M34/RFC-0017 adds the empty reviewed agent-tool recovery-rate fixture and
evaluator to the deterministic sample bundle. Release smoke proves only that
the installed offline evidence path works; it is not a task-directed
operational cohort, measured recovery-free completion rate, reliability
result, provider certification, or release gate. See the
[agent-tool recovery-rate readiness guide](agent-tool-recovery-rate-readiness.md).

M35/RFC-0018 adds the empty reviewed third-party conformance-adoption fixture
and evaluator to the deterministic sample bundle. Release smoke proves only
that the installed offline evidence path works; it is not an independently
authored adapter or plugin, passing external conformance result, provider
certification, support matrix, or adoption claim. See the
[third-party conformance-adoption readiness guide](third-party-conformance-adoption-readiness.md).

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
Matching repeat builds are also not provenance: they do not identify the
builder or prove that the environment was trustworthy.
