# Community-alpha retrospective

## Outcome

The `0.1.0a1` candidate completes the assigned M0-M6 walking path without
adding native code or a mandatory runtime dependency. One pure Python wheel can
run the engine lifecycle, deterministic world core, typed commands/receipts,
snapshot/replay workflows, Clockwork Arena, and the local typed agent acceptance
loop. Optional WebGPU presentation remains isolated behind engine-owned types.

The release candidate adds deterministic sample/archive staging, exact
checksums, an SPDX SBOM, notices, explicit API status, cross-platform artifact
smoke, and a tag-only provenance/prerelease workflow. No tag, GitHub release, or
PyPI upload is created by the milestone implementation itself.

## What worked

- Headless-first design kept M0-M5 scenarios runnable from a clean no-dependency
  wheel and made release acceptance independent of a display or GPU.
- The same canonical command and receipt path supports direct Python, CLI,
  replay, and local stdio agent use without a second mutable world.
- Null adapters and architecture tests let lifecycle, dependency, handle, and
  failure contracts run across the full CPython/desktop matrix.
- Immutable action pins, least-privilege job permissions, artifact checksums,
  and hosted attestations make the future tag workflow inspectable in-repo.
- Explicit public-export metadata removes the earlier ambiguity that a visible
  alpha symbol might be implicitly stable.

## Evidence and misses

M5's inherited hosted baseline passed 14 jobs across CPython 3.12-3.14 and all
three desktop operating systems. M6 run `31002365370` also passed all 14 jobs,
including complete release-candidate smoke and real graphics acceptance on
Windows, macOS, and Linux. Exact local and hosted command records live in
`.ai/TEST_EVIDENCE.md`.

Recorded local benchmarks observed the M1 3,600-tick headless target and the M4
Clockwork Arena baseline target. The representative M1 10,000-entity tick and
M3 10,000-sprite extraction/wgpu CPU-submission targets were not observed. M7
subsequently profiled and reduced all three local p95 values, but none met its
starting target. [RFC-0001](rfcs/0001-defer-first-native-kernel.md) records why
those residual costs still do not authorize Rust, PyO3, or another native
boundary. M2 timings are informational and have no threshold.

No external-contributor first-contribution usability study has been recorded.
The repository now supplies a complete walkthrough and issue-ready starter
cards, but actual contributor feedback is a follow-up metric rather than a
fabricated acceptance result.

## Decisions retained

- Every current Python export and persistent protocol remains experimental.
- Standard GIL CPython 3.12-3.14 is the supported baseline; free-threaded builds
  are not claimed.
- The baseline wheel has no dependencies. Graphics is an exact optional extra.
- Agent control remains local and capability-gated. There is no remote listener,
  authentication claim, shell, arbitrary evaluation, or dynamic project loader.
- Release publication stays maintainer-owned. PyPI name reservation and trusted
  publishing need a separate decision.

## Next questions

Future work begins with evidence and an assigned milestone, not automatically
from this alpha. M20 evaluates the first central preview candidate and retains
command/receipt contracts as experimental under RFC-0003 until the full
compatibility gate is evidenced. M21 completes only the bounded public receipt
reader gate and freezes same-version fixture inputs under RFC-0004. M22
completes only the built-in operation-argument policy gate under RFC-0005. M23
completes only the semantic-diff/diagnostic-code policy gate under RFC-0006.
Three gates remain: cross-version history, external feedback, and a supported
release channel. Remaining priority
questions also include contributor rehearsal feedback and controlled
cross-platform performance evidence. Scene importers,
production audio, rigid-body physics, networking, editor tooling, 3D, device
recovery, and native acceleration remain unimplemented.
