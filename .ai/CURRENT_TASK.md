# Current Task

- **Task:** M6 — Community-alpha release hardening
- **Status:** Complete; DCO-signed PR #6 is published and hosted run `31002365370` passed all 14 jobs
- **Started:** 2026-08-05
- **Acceptance gate:** A clean consumer must be able to verify and launch the pure wheel plus bundled M0-M5 headless scenarios on Windows, macOS, and Linux; public exports need explicit stability; release/security/community artifacts must be actionable and evidence-backed.
- **Distribution outcome:** Version `0.1.0a1` stages a pure wheel, sdist, deterministic sample ZIP, Apache/project/optional-dependency notices, SPDX 2.3 SBOM, manifest, and exact SHA-256 inventory. The isolated release smoke verifies these artifacts before installing or extracting them.
- **Release outcome:** The tag-only workflow validates source/docs/tests/artifacts, uses immutable action revisions and scoped attestation/release permissions, creates build-provenance and SBOM attestations, and stages a GitHub prerelease. No tag, release, or PyPI upload is created in this task.
- **API/docs outcome:** Every supported export has exact `__stability__` metadata; all are experimental. User, adapter, release, contribution, triage, roadmap, release-note, and retrospective guides document the alpha boundary.
- **Community outcome:** A declarative label catalog, focused issue forms, triage rules, repository-native roadmap board, and three issue-ready good-first cards define the contribution queue. The live repository still has only default labels and no issues until maintainers apply/open the checked-in queue.
- **Local gate:** The complete frozen suite reports 552 passed and one existing Windows symlink-capability skip; Ruff, strict Pyright, strict MkDocs, pure-wheel build, isolated installed-wheel smoke, deterministic staging, checksum/SBOM validation, and bundled-sample acceptance all pass.
- **Hosted gate:** PR #6 is published against the validated M5 branch. Run `31002365370` passed quality/docs, seven CPython/OS test jobs, three complete installed release-candidate smokes, and three real graphics smokes.
- **Non-scope retained:** PyPI publication/name reservation, an actual release tag or GitHub release, dynamic plugin loading, remote/network agent transport, production audio, rigid-body physics, editor tooling, 3D, automatic device recovery, Rust, PyO3, and native acceleration.
- **SemVer:** First community-alpha candidate `0.1.0a1`; every current Python export and persistent protocol remains experimental.
