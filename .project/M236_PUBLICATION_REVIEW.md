# M236 consolidated publication review

## Approved scope

On 2026-09-05 the maintainer approved auditing M100-M235 and preparing one
consolidated pull request against main, retaining the existing three-job CI.
This does not authorize a merge, release, additional hosted jobs, or a new
Windows cleanup policy. Preserve existing commit identities and DCO authorship.

## Exact review baseline

- Main: `5238941c77fbbbd0ff5fd72834d3bead66b2ed3e` (M99).
- Stack tip: `1273e367949a94e7e99dc4a3418d2cf26daf14ef` (M235).
- History: 136 commits, no merge commits, zero commits exclusive to main.
- Net diff: 570 paths, 142,104 insertions and 179 deletions.
- Path groups: 24 source, 28 scripts, 275 tests, 233 documentation, four
  project records, and six other root/configuration paths.
- Remote refresh found only main and no open pull requests.
- All 136 commits have DCO trailers matching their recorded authors. Git object integrity and diff whitespace
  checks pass. These checks do not substitute for behavioral or security review.

## Reviewer navigation

| Range | Primary area | Review concern |
| --- | --- | --- |
| M100-M118 | Release archive checks and compatibility decisions | Narrow parser bounds and retained platform policy |
| M119-M125 | Scene/prefab planning and confined source loading | Transaction reuse, path confinement, integrity versus authority |
| M126-M145 | Asset planning, realization, cache, and observations | Explicit filesystem effects, deterministic identities, read-only previews |
| M146-M210 | Cleanup deferral, Windows probes, admission policies | Local observations do not authorize production cleanup |
| M211-M235 | Contained participant and Git identity probes | Process/resource ownership, local evidence, checkout portability |

Use the existing RFCs, tests, and dated evidence for each range. The entire
142,104-line added surface has not received a new line-by-line review in M236.
Earlier local validation remains historical evidence, not hosted qualification.

## Blocking finding: historical object required by shallow-checkout tests

The Windows job in `.github/workflows/ci.yml` uses the checkout action's default
shallow checkout, then runs the CPython 3.14 test suite. M221's
`_load_committed_source()` unconditionally reads exact commit
`734d4eb943c3da7a1a8357ef3e180cac4353cb6b`, its parent, tree, and source blob.
Its module skips only on non-Windows platforms. Later M222-M235 compositions
reuse this boundary.

A local depth-one clone of the stack reproduces the problem without a hosted
run. `git cat-file -t` for the M220 commit exits 128 there, while the original
full checkout reports `commit`. The same
`test_committed_source_descriptor_is_exact` passes in the full checkout and
fails in the shallow checkout with `fixed Git object read returned nonzero`.

Therefore the current stack is not ready for a passing Windows PR check.
Fetching full history alone would address the immediate PR checkout but would
not provide a durable solution after the requested squash merge: the original
M220 commit would not be an ancestor of the squash commit. The probe also
deliberately prohibits lazy object fetching. Do not weaken the assertion,
silently skip the failure, add a network fallback, or represent it as passing.

The next required decision is a bounded test-portability repair that preserves
the real source-binding assertions in shallow and squash-merged checkouts.
Options must distinguish a portable, controlled Git-object fixture from the
existing historical current-host observation. Accepted exact-history contracts
and their guards would need explicit review; this audit does not change them.

## CI budget and publication disposition

Both workflow files and the change classifier match main byte-for-byte. The
existing substantive path allocates Linux plus Windows and macOS jobs; the
documentation-only path allocates Linux. Superseded PR runs are cancelled.
Release publication is tag-triggered and is outside this approval.

No workflow edits, push, PR, merge, tag, release, or hosted allocation occurred.
Publication is withheld at the reproduced blocker rather than launching a
known-failing hosted run. Further validation and complete consolidated review
remain required after the repair is approved. No admission or security policy
is promoted by this review.

The five metadata-hygiene tests and strict documentation build pass after
recording this finding. The isolated ignored `.tmp/m236-shallow-checkout`
remains available for reproducing the failure and validating a future repair.

## Approved repair and focused research

The maintainer subsequently approved the portability repair without weakening
binding assertions or changing the three-job CI. RFC-0219 records the decision.
The historical findings above remain a record of the pre-repair state.

DirectionBriefV1: schema version 1; baseline
`1340e8b7eaabfee6a9062bbb3cc8e348e24d75ec`; scanned 2026-09-05. Coverage was
focused on Git object format, checkout depth, squash semantics, and test
reliability. The reference pages are living documents; no new release-event
date is asserted.

- **Finding:** [Git's repository layout](https://git-scm.com/docs/gitrepository-layout)
  and [loose-object format](https://git-scm.com/docs/gitformat-loose) support
  an isolated object-store fixture. Confidence high; aligned with offline test
  portability. Engineering cost is a test fixture, composition, negative tests,
  and documentation. Disposition adopt within the approved repair; no runtime
  roadmap expansion. Verify exact object identities and real traversal.
- **Finding:** [checkout defaults](https://github.com/actions/checkout) and
  [squash semantics](https://docs.github.com/en/pull-requests/reference/pull-request-merges)
  do not guarantee original intermediate commit objects. Confidence high;
  direct relevance to the reproduced failure. Disposition no-change to CI;
  retain existing jobs and verify both absent-history layouts locally.
- **Recommendation:** bind the unchanged probe family explicitly to five pinned
  original objects for every automated run, with no environment-dependent
  fallback. Evidence gap: this proves fixture binding, not checkout provenance
  or complete history connectivity. Next review trigger is a changed probe
  object inventory, Git format, pytest loading behavior, or support policy.

Focused validation corrected a mistaken unused-parent-object expectation,
pytest's dual module-import wiring, and console-script helper discovery. The
repaired depth-one and synthetic squash checkouts each pass the 44-test focus,
including the original direct M221 test and complete M235 composition. Full
suite and publication gates were pending at that point; no assertions were removed.

## Local qualification conclusion

Final Windows CPython 3.12.13 validation passes 4,933 tests with 19 skips.
Formatting, lint, typing, documentation, reproducibility, installed wheel/scene,
release smoke, and benchmark-schema checks complete. No new source, dependency,
workflow, or original-probe diff is present. The high-confidence historical
credential-pattern scan is clear. M3 informational timing targets remain unmet.
Detailed commands and failures corrected during development are recorded in
TEST_EVIDENCE.md.

Proceed with one approved consolidated PR, preserving all commits and their
DCO identity. Do not claim a new exhaustive line-by-line security audit of the
entire historical stack or hosted cross-platform success from this local run.
The large review surface, current-host native assumptions, deliberately partial
fixture database, and deferred Windows cleanup remain explicit review risks.
The PR's check suite is authoritative for hosted qualification; no merge or
release is performed as part of this publication step.
