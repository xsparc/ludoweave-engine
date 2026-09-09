# RFC-0221: replay-owned input history

Status: M239 locally qualified following maintainer continuation; hosted checks pending.

## Decision and acceptance

Preserve `ludoweave.replay/1` and its timeline hash. Add an application-level
`ludoweave.input-replay/1` envelope embedding that timeline and exact snapshots
for `[initial_tick, final_tick)`. A separate artifact hash binds both. World
code does not import application input types. No networking, native code,
dependency, extra CI job or automatic release is admitted.

The frozen artifact refuses absent ticks, unknown fields and malformed values.
Bounds are 60,000 ticks, 256 actions/transition names per snapshot,
128 characters per name, 250,000 aggregate action/transition entries and
64 MiB canonical bytes, with JSON depth/node limits.
The existing canonical float policy preserves analog values and signed zero.

Replay checks composition compatibility before calling an explicit trusted
executor factory with the embedded input source. No executable names or imports
come from the document. Execution remains synchronous and single-owner; the
caller owns factory-created resources. State/checkpoint verification stays on.

Acceptance requires legacy-byte identity, fresh-process gameplay replay without
the original input generator, malformed/missing/duplicate/oversized input
regressions, analog/digital/transition round trips, nonzero-start and immutable
branch cases, installed-wheel execution, and the existing full quality gates.

## DirectionBriefV1

- schema_version: 1
- baseline_commit: `f57790e1603a1a34085ca1485a6183cc48b3420e`
- scanned_at: 2026-09-09
- coverage: focused persistent encoding, compatibility and deterministic inputs.
- finding: reuse bounded strict JSON. [RFC 8259](https://www.rfc-editor.org/rfc/rfc8259)
  describes interoperability and parser limits (source event: December 2017).
  Confidence: high; relevance/alignment: portable inert replay data; opportunity:
  reuse current codec; cost: low; disposition: adopt; roadmap delta: M239 only;
  verification: duplicate/unknown keys, finite values, count/depth/byte limits.
- finding: retain existing hexadecimal float tags. Python documents exact
  conversion in its [numeric reference](https://docs.python.org/3/library/stdtypes.html#float.hex)
  (undated, retrieved on scan date). Confidence: high; relevance/alignment:
  precise input identity; risk: bool/float confusion; cost: low; disposition:
  adopt; roadmap delta: none beyond M239; verification: signed zero and type
  identity round trips.
- overall_recommendation: embed complete inputs above the unchanged world codec.
- evidence_gaps: hosted M239 checks and external game adoption remain unproven.
  Fresh-process, branch, installed and full local qualification passed; this does
  not admit network rollback.
