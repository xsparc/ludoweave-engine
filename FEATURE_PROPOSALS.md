# Ten feature proposals after M244

Status: **draft for discussion, not an implementation commitment**.
Requested 2026-09-30. Baseline: `510c5f31ed752edebd19ce31ef7da8bf0454e0cc`.
The maintainer authorized this proposal and its draft PR, not all ten features.
IDs F01–F10 are proposal identifiers, not assigned milestones or release promises.

## Recommended sequence

Start with F01 and F03: faster replay inspection and actionable failure reports
build directly on the validated recorder/viewer. Then review F02, F04 and F05.
F06–F10 need separate format/API decisions and should be approved individually.
Effort is relative engineering complexity (small/medium/large), not a time estimate.

| ID | Feature | Benefit | Effort | Prerequisites |
| --- | --- | --- | --- | --- |
| F01 | Replay speed presets | Inspect long sessions faster | Small | M244 viewer |
| F02 | Named replay bookmarks | Share exact moments without editing recordings | Medium | Existing seek; sidecar decision |
| F03 | Replay divergence report | Explain where two sessions first differ | Medium | Existing replay and semantic diff |
| F04 | Tick-selected frame export | Attach visual evidence to bug reports | Medium | Existing public capture contract |
| F05 | Read-only replay input timeline | Explain which actions drove a tick | Small | Existing input envelope |
| F06 | Portable input-binding profiles | Let players customize controls | Medium | Existing action mapper; profile decision |
| F07 | Clockwork Arena save slots | Resume a game without replaying from tick zero | Large | Snapshot/composition compatibility decision |
| F08 | Restricted Tiled JSON import | Author levels in an existing external tool | Large | ADR-0026 scope review; import contract |
| F09 | Deterministic grid navigation | Support headless tactical/NPC movement | Large | New algorithm and command integration contract |
| F10 | Data-only agent scenario runner | Repeat and compare command-based gameplay tasks | Medium | Existing local agent service; scenario schema |

## F01 — Replay speed presets

Add explicit 1/4x, 1/2x, 1x, 2x and 4x presentation rates to the replay viewer,
with the selected rate in its status panel. This is new pacing control, not a
change to simulation frequency. Apply rational/integer deadline arithmetic;
pause, step and seek must rebase pacing without skipped or duplicated batches.

Acceptance: each preset produces identical receipts, final hashes and batch
counts; virtual-clock tests verify exact deadline rounding, pause/resume and
seek transitions. Reject unsupported rates before creating a device. Null
headless runs remain unpaced. No audio time stretching or frame dropping.
Primary paths: `examples/play_input_replay.py`, its integration tests and guide.
Risk: accumulated timing drift or resume bursts; retain full preflight.

## F02 — Named replay bookmarks

Add a bounded, explicit JSON sidecar mapping labels to recorded tick boundaries,
bound to the recording digest. Let the viewer select a bookmark through its
existing seek mechanism. Recording bytes and hashes remain unchanged.

Acceptance: duplicate labels, wrong recording digests, oversized strings/counts,
invalid boundaries and unsupported versions fail before presentation. Listing
is stable and read-only; writing uses an explicit destination and refuses
overwrite by default. Round-trip tests prove unchanged replay bytes and results.
No in-window editor, hidden autosave or embedded script. A sidecar schema and
path policy need approval before implementation. Depends on seeking, not F01.
Risk: treating a digest as authentication; it establishes identity only.

## F03 — Replay divergence report

Compare two compatible recorded sessions and report the earliest observed
divergence: input, transaction, checkpoint, or reconstructed canonical state.
Reuse existing snapshot semantic diff rather than inventing another diff engine.
The new value is timeline localization and diagnostic context, not basic diff.

Acceptance: identical sessions, differing lengths, composition mismatch, altered
input, and a known changed component yield bounded, stable versioned JSON.
Classify invalid artifacts separately from valid-but-different recordings.
Walk batches once under existing limits; do not assume divergence is monotonic
or repeatedly replay every growing prefix. Never claim the report proves root
cause. Headless and installed-wheel tests need no GPU. Main risk: diagnostic
output growth; cap changes with explicit truncation metadata.

## F04 — Tick-selected frame export

Render one verified recorded boundary offscreen and save a PNG plus a small
manifest containing recording hash, tick and capture dimensions. Reuse the
public render capture API; renderer objects never appear in output contracts.
Status inclusion must be explicit and a no-status capture must be supported.

Acceptance: reject invalid ticks/dimensions before opening the backend; validate
PNG dimensions and manifest binding; refuse existing output paths by default;
close resources on capture/write failure. A Null device can test orchestration,
but actual image export needs optional graphics and existing graphics checks.
Do not promise cross-GPU pixel identity. No video encoder, GIF, cloud upload or
new dependency. Risk: output size and partial files; define bounded atomic output.

## F05 — Read-only replay input timeline

Provide a headless query over a selected tick range showing recorded digital,
analog and edge values, with optional action-name filtering and bounded paging.
This exposes existing input history; it does not synthesize new gameplay input.

Acceptance: exact values match the envelope for initial/nonzero ticks and page
boundaries; ordering is deterministic; unknown filters, invalid ranges and
excessive limits produce structured errors. Report missing data rather than
silently manufacturing neutral actions. Tests prove no world mutation and no
artifact rewrite. Optional viewer integration can follow separately; the first
slice is JSON inspection only. Primary paths: application replay/tool composition
and replay tests. Risk: unbounded output; retain envelope and page limits.

## F06 — Portable input-binding profiles

Load named, data-only keyboard/mouse/gamepad bindings into the existing action
mapper before a session starts. Include validation and a defaults profile for
Clockwork Arena. This adds persistence and configuration, not another input API.

Acceptance: equivalent events under remapped profiles yield equivalent action
snapshots; duplicate/conflicting controls follow a documented policy; malformed
controls, non-finite deadzones, excessive bindings and unknown schema versions
fail deterministically. Recording stores consumed actions, so replay does not
depend on the current profile. No global mutable mapper or runtime hot-reload
in the first slice. Profile schema needs approval. Risk: held-key state when
switching profiles; initially permit changes only at session creation.

## F07 — Clockwork Arena save slots

Add explicit named save/load operations for the trusted sample composition,
wrapping existing canonical snapshots with version, composition and asset-lock
identity. Do not describe this as a new snapshot facility: snapshots already
exist. The new feature is a bounded user-facing continuation workflow.

Acceptance: an uninterrupted run and save/load continuation consume identical
subsequent inputs and reach the same state hash; cover random-stream state,
tick position, stale handles and incompatible schemas. Load into a fresh session
and publish it only after all validation succeeds. Reject partial/corrupt files;
never deserialize pickle or arbitrary Python. Explicit confined output paths,
overwrite rules and crash-safe replacement need design review. No cloud sync,
automatic migrations or cross-version support claim. Risk/effort is high because
world state alone may not capture all composition-owned continuation state.

## F08 — Restricted Tiled JSON import

Convert a documented finite orthogonal subset of Tiled JSON into existing
immutable tilemap records and asset references. The engine does not gain a
visual editor or a second canonical world store. Tiled parsing was explicitly
outside M11; review ADR-0026 and accept a narrow follow-up decision first.

Acceptance: fixture maps preserve cell/layer order and validated atlas mapping;
deterministic output is byte-stable. Initially support uncompressed integer tile
arrays and confined local assets. Reject infinite maps, compression, unsupported
orientation, unhandled flip flags, external templates and unknown required
features rather than silently losing them. Bound bytes, layers and cell counts;
test path traversal and oversized data. No network fetches or Tiled dependency
at runtime. Risk: format breadth; publish a support matrix, not a compatibility
claim for every Tiled file. Existing tilemap rendering remains unchanged.

## F09 — Deterministic grid navigation

Add bounded four-neighbor path queries over an immutable occupancy/cost grid,
with integer costs, documented neighbor/tie ordering and a node-expansion budget.
Return a detached route; applying movement still uses world commands/receipts.
Start with one small tactical example, not a general physics/navigation stack.

Acceptance: compare small grids with a reference shortest-path solver; equal-cost
ties choose the same route across runs; unreachable goals and budget exhaustion
have distinct results. Reject invalid cells and costs; input enumeration order
must not alter routes. Headless tests and replayed movement verify hashes.
No navmesh, diagonals, crowd simulation, native code or asynchronous worker.
Choose placement through an architecture decision rather than importing world
authority into presentation. Risk: stale routes after world changes; bind queries
to a grid revision and revalidate commands at execution.

## F10 — Data-only agent scenario runner

Define bounded scenarios of existing typed commands, observations and explicit
assertions over a trusted sample composition. Produce machine-readable receipts,
assertion failures and final hashes for repeatable local tasks. This adds a
scenario harness, not a new transport or another agent-control protocol.

Acceptance: the same seed/scenario yields identical semantic results; denied
commands, failed expectations, exhausted tick/step budgets and malformed files
have distinct outcomes. Use an allowlist of assertion operators, never eval or
dynamic imports. Golden scenarios run through existing local service contracts
and one existing installed smoke path. No LLM calls, benchmark leaderboard,
remote orchestration or claimed agent-quality score. Risk: accidentally granting
scenario files authority; capabilities are explicitly supplied by the caller,
not requested by data. Schema and capability policy require approval.

## Focused direction brief (DirectionBriefV1)

- `schema_version`: 1
- `baseline_commit`: `510c5f31ed752edebd19ce31ef7da8bf0454e0cc`
- `scanned_at`: 2026-09-30
- `coverage`: gameplay/replay usability, comparable input authoring, 2D interchange,
  exact timing and local serialization safety. This focused feature request does
  not require a broad vendor/release or governance-tool competitive survey.

All source event dates below are **undated living documentation**, accessed on
the scan date; no publication or release date is inferred. Dispositions are
advisory, not accepted research decisions.

1. **Exact-rate pacing is feasible without another dependency.** Python provides
   rational values through [Fraction](https://docs.python.org/3/library/fractions.html).
   Confidence: high for capability, medium for fit. Relevance: F01. Alignment:
   presentation-only timing. Opportunity: faster inspection; cost: small.
   Disposition: adopt as a proposal. Roadmap delta: candidate F01 only.
   Verification needed: integer deadline and pause/seek tests; no measured benefit yet.
2. **Action remapping is a useful established authoring pattern.** Godot exposes
   action/event mappings and deadzones in [InputMap](https://docs.godotengine.org/en/stable/classes/class_inputmap.html).
   Confidence: high for documented capability, medium for user demand. Relevance:
   F06. Alignment: reuse LudoWeave actions, not Godot's singleton design.
   Opportunity: accessible control choice; cost: medium. Disposition: adopt as a
   proposal. Roadmap delta: candidate F06. Verification needed: profile conflict
   rules and replay independence; no demand survey was conducted.
3. **Tiled offers JSON interchange but a large format surface.** Its
   [format reference](https://docs.mapeditor.org/en/stable/reference/json-map-format/)
   includes multiple orientations, layer types and encodings. Confidence: high.
   Relevance: F08. Alignment: data-only 2D import; risk: silent data loss and
   oversized inputs. Cost: large. Disposition: monitor pending subset/ADR approval.
   Roadmap delta: conditional F08. Verification needed: bounded fixtures and
   explicit unsupported-feature rejection; no importer prototype was executed.
4. **Save/scenario files must remain inert.** Python warns that unpickling
   untrusted data can execute code in its [pickle documentation](https://docs.python.org/3/library/pickle.html).
   Confidence: high. Relevance: F02/F06/F07/F10. Alignment: existing data-only
   boundaries. Risk: executable deserialization; cost: medium to large for safe
   formats. Disposition: no-change to the security rule. Roadmap delta: none
   beyond the proposed bounded formats. Verification needed: malformed-input,
   path, size and capability tests before any implementation.

Overall recommendation: deliver small replay usability slices first, then choose
one player/authoring capability. Do not approve ten parallel implementations.
Evidence gaps: no external-user interviews, no new performance measurements,
no prototype of the proposed formats, and no cross-version compatibility proof.

## Approval and validation gates

Every feature needs its own bounded acceptance approval, DCO-signed-off PR and
appropriate tests before delivery. Format/API changes require an accepted design;
this document changes neither current contracts nor compatibility promises.
Keep ECS/world authority, headless execution and public backend isolation intact.
Networking, a visual editor, 3D, executable plugins and native acceleration remain
deferred. No proposed feature grants Windows cleanup authority.

This draft changes documentation only. Validate strict documentation, existing
architecture tests, whitespace and links; use the trusted existing CI classifier.
Future implementations should extend existing jobs rather than add jobs by
default. GPU observations are separate from deterministic simulation evidence.
No new jobs, dependencies, runtime packages or executable examples are introduced
by this PR. The proposal itself does not claim any feature test has passed.
