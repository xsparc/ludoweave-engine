# Current Task

- **Task:** M2-06 — data-only workflow CLI and M2 milestone closure
- **Status:** Local milestone acceptance complete; signed publication candidate, stacked pull request, and hosted CI remain
- **Started:** 2026-08-05
- **Acceptance gate:** Direct Python and CLI apply produce byte-equivalent committed, dry-run, and rejected receipts; project-confined apply/snapshot/replay/diff complete an installed-wheel workflow; the complete M2 quality, docs, package, benchmark, security, and independent-review gates pass.
- **M2-01 outcome:** Bounded canonical JSON, exact tagged finite floats, immutable command/transaction envelopes, exact canonical equality, explicit operation registry/fingerprint, dependency/evaluation guards, documentation, and ADR-0008 are complete.
- **M2-02 outcome:** `WorldSession` owns one authoritative record; public access is detached, every resource has an explicit role, transactions fully decode before clone staging, and only a complete validated record can be adopted.
- **M2-03 outcome:** Canonical committed/dry-run/rejected receipts and independent pre/post semantic diffs cover entity, component, resource, allocator, epoch, tick, alias, and deterministic limit behavior.
- **M2-04 outcome:** Project-bindable canonical snapshots preserve allocator/epoch/component/state-resource/tick/random authority and future behavior; bounded decode, exact schema validation, migrations, and atomic load are implemented. Existing-session load preserves classified input/runtime resources.
- **M2-05 outcome:** Self-contained replay timelines verify every batch/checkpoint hash, require one-tick branchable persistent tick batches, and support immutable parent-bound branches with parent reproduction.
- **M2-06 outcome:** Data-only project manifests and project-relative `apply`, `snapshot`, `replay`, and `diff` adapters are implemented with bounded handle reads, atomic output replacement, structured diagnostics, exact Python/CLI receipt bytes, and installed-wheel coverage. Informational M2 benchmark/validator tooling is implemented and validated.
- **Review correction gate:** The final local cut passed the complete documented gate with 444 tests and one expected Windows symlink-capability skip. Independent code/security review found no remaining actionable finding. Hosted Windows/macOS/Linux and Python 3.13/3.14 results are not yet claimed.
- **Non-scope retained:** General project/plugin loading, scenes, M4 recorded input, WebGPU, MCP, physics, audio, networking, editor tooling, and native acceleration.
- **SemVer:** Additive and corrective experimental `0.1.0.dev0` surface; no compatibility promise or version bump.
