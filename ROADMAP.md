# LudoWeave roadmap board

This repository-native board states outcomes and readiness; it is not a delivery-date
promise. Accepted ADRs and milestone acceptance evidence override an older card. Public
issues become the discussion and assignment record once a card is opened.

## Community-alpha release candidate

| Lane | Outcome | Evidence gate |
| --- | --- | --- |
| Done | M0 repository/runtime walking skeleton | Installed pure wheel and cross-platform CI |
| Done | M1 deterministic world core | Reference-model properties and benchmark evidence |
| Done | M2 command/snapshot/replay workflow | Artifact and installed-wheel scenario tests |
| Done | M3 isolated 2D presentation | Null/wgpu vertical slice and graphics CI |
| Done | M4 Clockwork Arena gameplay slice | 3,600-tick replay plus stress evidence |
| Done | M5 local typed agent interface | Agent World Builder and local stdio acceptance |
| Done | M6 community alpha | Release artifact, docs, API, security, and contribution gates |
| Done | M7 performance/native decision | Versioned profiles, ordinary Python optimization, RFC admission decision, and cross-platform smoke |
| Done | M8 gamepad/SDL3 evaluation | Provider-neutral gamepad mapping, pinned GLFW smoke, SDL3 maturity ADR, and cross-platform validation |
| Done | M9 Box2D v3 plugin evaluation | Binding/wheel/lifecycle/headless/API/threading/determinism/conformance admission evidence, ADR, and hosted validation |
| Done | M10 live semantic inspector | Separate local process, versioned semantic stream, command/query reuse, explicit write receipts, lifecycle/security bounds, and quota-conscious essential CI |
| Done | M11 rich 2D authoring | Headless tick animation, bitmap text, immutable tilemaps, fixed-point particles, Null-audio mixing, installed showcase, and hosted validation |
| Done | M12 plugin manifest compatibility | Canonical data-only manifests, deterministic environment/dependency checks, preview compatibility policy, installed CLI smoke, and hosted validation |
| Done | M13 rollback/network-snapshot readiness | Hosted-validated bounded correction-branch evidence, explicit input-history gap, network deferral ADR, and no transport implementation |
| Done | M14 constrained 3D decision | Hosted-validated installed-surface evidence, retained layered-2D scope, complete admission gate, and no 3D runtime implementation |
| Done | M15 visual-editor admission decision | Hosted-validated installed semantic-mutation evidence, retained headless inspector, complete authoring/support gate, and no GUI/editor implementation |
| Done | M16 WASM-mod security admission decision | Hosted-validated installed inert-boundary evidence, prospective threat model, complete security/determinism gate, and no runtime or guest execution |
| Done | M17 installed render-device conformance | Versioned explicit-factory baseline, Null/wgpu evidence, isolated artifact smoke, and unchanged essential CI topology |
| Done | M18 installed agent-tool conformance | Hosted-validated explicit-factory 12-tool baseline, direct-service artifact evidence, and unchanged essential CI topology |
| Done | M19 installed WorldStore conformance | Hosted-validated versioned explicit-factory storage baseline, production/reference artifact evidence, and unchanged essential CI topology |
| Done | M20 command/receipt stability decision | PR #28 squash-integrated; installed same-version evidence, complete preview gate, RFC-0003 decision, and unchanged runtime/CI topology |
| Done | M21 bounded receipt reader and v1 baseline | PR #30 squash-integrated; reviewed strict detached decoding, deterministic limits, frozen single-version fixtures, installed evidence, and all eight essential hosted jobs passed without stability promotion |
| Done | M22 built-in operation argument compatibility | PR #32 squash-integrated; reviewed exact seven-operation v1 policy, installed valid/missing/unknown/default-omission evidence, RFC-0005, artifact smoke, and all eight unchanged essential jobs passed on the corrected head |
| Done | M23 receipt semantic-diff and diagnostic compatibility | PR #34 squash-integrated the corrected exact policy/evidence; 1,050 local tests and both eight-job hosted runs passed with no current actionable review finding |
| Done | M24 cross-version corpus admission readiness | PR #36 squash-integrated; exact preserved history, false current gate, append-only correction, installed artifact smoke, RFC-0007, and both eight-job hosted runs passed |
| Done | M25 external-consumer-feedback admission readiness | PR #38 squash-integrated; strict reviewed manifest, false current gate, reviewed non-IP correction, installed artifact smoke, RFC-0008, and both eight-job hosted runs passed |
| Done | M26 supported release-channel admission readiness | PR #40 squash-integrated; strict empty reviewed manifest, false current gate, complete-prefix correction, installed artifact smoke, RFC-0009, and both eight-job hosted runs passed |
| Done | M27 external-contributor rehearsal admission readiness | PR #42 squash-integrated; strict empty reviewed manifest, false current result, complete-history admission, installed artifact smoke, RFC-0010, and all eight effective essential jobs passed |
| Done | M28 external sample-game adoption admission readiness | PR #44 squash-integrated; strict empty reviewed manifest, zero current count, corrected authorship/provenance/history gates, installed artifact smoke, RFC-0011, and both eight-job hosted runs passed |
| Done | M29 contributor-retention admission readiness | PR #46 squash-integrated; strict empty reviewed manifest, zero current count, same-person/chronology/history gates, installed artifact smoke, RFC-0012, and all eight essential hosted jobs passed on the corrected head |
| Done | M30 installation-matrix admission readiness | PR #48 squash-integrated; strict empty reviewed manifest, zero current count, immutable public-wheel/full-matrix/history gates, installed artifact smoke, RFC-0013, and all eight essential hosted jobs passed |
| Done | M31 response/review-latency admission readiness | Strict empty reviewed manifest, complete public cohort and pending-item preservation, deterministic aggregates, installed artifact smoke, RFC-0014, and all eight essential jobs passed before verified PR #50 integration |
| Done | M32 replay-divergence-rate admission readiness | PR #52 squash-integrated; strict empty reviewed manifest, complete CI replay-execution cohort and non-execution preservation, exact rational rate, installed artifact smoke, RFC-0015, and all eight essential hosted jobs passed on the corrected head |
| Done | M33 benchmark-regression-rate admission readiness | PR #54 squash-integrated; strict empty reviewed manifest, controlled paired-comparison cohort and non-execution preservation, exact rational rate, installed artifact smoke, RFC-0016, and all eight essential hosted jobs passed |

M6's implementation head passed hosted Windows, macOS, and Linux CI. Creating
or publishing the `v0.1.0a1` tag remains a separate maintainer release action.
M7's implementation head passed the same 14-job hosted matrix, including base
and real-wgpu profiling-contract smokes on all three operating systems.
M8 PR #9 passed the same 14-job hosted matrix, including standardized gamepad
contract and real GLFW smoke on all three operating systems. Haptics, sensors,
raw joysticks, remapping UI, and SDL windows remain future proposals.
M9 evaluates the external rigid-body candidate only. The dependency, adapter,
and canonical-physics integration remain absent unless every admission gate is
evidenced.
M9 PR #10 passed the same 14-job hosted matrix against the validated M8 branch.
The binding remains deferred and no dependency changed.
M10 is a headless protocol client, not a visual editor. It may spawn only the
built-in local stdio composition and cannot listen on a network interface.
M10 PR #11 passed its consolidated eight-job hosted matrix: one complete
quality/test/distribution gate, four compatibility jobs, and real graphics on
all three operating systems.
M11 is a bounded authoring and extraction slice, not a new world store. Real
audio playback, font parsing/shaping, editor-scale tile import, particle DSLs,
and provider objects remain deferred.
M11 PR #12 passed the consolidated eight-job hosted matrix on implementation
commit `aca6d93165a52d88451e8e06d5f1aa8d2e323f1d`.
M14 PR #15 passed the unchanged eight-job hosted matrix on implementation
commit `47443046834eb423be977973775f80494161533d`; layered 2D remains the
accepted scope and no runtime or dependency was added.
PR #16 squash-integrated the exact validated M8-M14 tree into `main` as
verified commit `2c62c8ed9c4ced6292260f6b8c84b1f069de1eaa`. Stacked PRs
#9-#15 are closed as superseded; their branches remain as audit history.
PR #18 integrated the repository-state evidence as verified main commit
`bfea67d2d922e8c591224d18f56c14d572d7f7da`; M15 starts from that exact base.
M15 ready PR #19 passed the unchanged eight-job hosted matrix as run
`31036925179` on implementation commit
`7e85570056dde3678aaeee13eee4036067876d8c`.
PR #19 squash-integrated the exact final M15 tree into `main` as verified
commit `c013dad38b1b64f0f4ccddc19681d643f6414427`. M16 starts from that
exact clean base and treats WASM mods as a separate security decision, not a
runtime implementation.
M16 ready PR #20 passed the unchanged eight-job hosted matrix as run
`31039403209` on implementation commit
`bcaf78fbc78bda8a13a95e397ab15d003dd4a6ce`.
PR #20 squash-integrated exact final M16 head
`808e48a5cb2727c8e1f4d7e896c4f8c7d41bfe1a` into `main` as verified commit
`e2bd57c057c0c16861953c0702b2012c4cabfe90`; both trees are
`05367be9bd85014fe6c70995ac1a69a39f90ef1e`.
M17 starts from integrated `main` commit
`27d2ee9d1f7f75dacc17568650f00ce833ef4fce`. It turns the existing
`RenderDevice` checklist into one installed baseline profile. The profile
executes only an explicitly supplied trusted factory and does not discover,
load, install, sandbox, or certify third-party code. Project-owned Null/wgpu
passes do not count as independent third-party adoption.
Ready PR #22 passed the unchanged eight-job hosted matrix as run
`31042903689` on DCO-signed implementation commit
`8e592f329424719214239bf97bd85dad9c9c5928`. PR #22 squash-integrated exact
final evidence head `148600cdaf9c419fbf552c68f833e0d55655731f` into
`main` as GitHub-verified commit
`610261c8450afc3d7db6ebb2b0425a1829737aec`; both trees are
`1e82568a463c62d0a1cf988b67eea09885ec50e3`.
M18 starts from integrated `main` commit
`ed65b12fa02f672113eac5939a0f616079fee44a`. It turns the existing internal
agent-service acceptance loop into one installed baseline for an explicitly
supplied trusted adapter factory. It does not discover, load, install, launch,
connect to, sandbox, certify, or admit third-party code, and project-owned
direct-service evidence does not count as independent adoption.
Ready PR #24 passed the unchanged eight-job hosted matrix as run
`31046172544` on DCO-signed implementation commit
`c4dde705393eebb7c99af428745e9383750f6b4d`.
PR #24 squash-integrated exact final evidence head
`cb617be0f678528fadc82877ec6910e42c6daf6b` into `main` as GitHub-verified
commit `1000d362432f19c912edf51c67e29c79bf444443`; both trees are
`1b6676ca7c1a6aaa223057a35e0c95242f4e9462`.
M19 starts from integrated `main` commit
`4076f3d7ac0c0a82834a1c98dcb36426ba67ac5e`. It turns existing private
production/reference storage conformance into one installed profile for an
explicitly supplied trusted `factory(ComponentRegistry)`. It does not discover,
load, install, sandbox, certify, or admit code and adds no backend or storage
format. Ready PR #26 passed the unchanged eight-job hosted matrix as run
`31092244573` on DCO-signed implementation commit
`1da692a693c1f92e10b676c2d4539354ce3ff59f`.
PR #26 squash-integrated exact final evidence head
`b93ca591f7063a1500cf105e6b0496b33573c69a` into `main` as GitHub-verified
commit `1a7219e540d8f4cb3c1f60ff12981513c6860ef9`; both trees are
`7fcd614fdde76daf1807f27dbe78ec306a501cc3`.
M20 starts from integrated `main` commit
`2fdeccd697f09f3e165130eb8564a6c585d472d2`. It evaluates whether the
installed command/transaction/receipt contracts are ready for preview without
changing their runtime or wire formats. RFC-0003 retains experimental status
until the complete cross-version, external-feedback, operation/receipt
evolution, bounded-reader, and supported-release-channel gate is evidenced.
Ready PR #28 passed the unchanged eight-job hosted matrix as run
`31095009029` on DCO-signed implementation commit
`d96d132da5ee847d6e86645be5e87a1e4aa5e89e`. PR #28 squash-integrated exact
final evidence head `d04561184996fac507071ad9e7dd0ef9c5e3cb7c` into `main` as
GitHub-verified commit `d166ef86bf25526d9d7715f63263d3cac6db78d4`; both trees are
`c3e2dc1224f530fb483d1b9684ff55329bf9557b`.
M21 starts from integrated `main` commit
`feed793e94c345fac4b146c358a68264ef6e5f62`. It adds the bounded public reader
identified by RFC-0003 and freezes exact `0.1.0a1` receipt/1 fixtures. RFC-0004
marks only the reader-and-bounds gate complete; the fixture corpus remains a
single-version baseline, and no command/receipt stability promotion or
cross-version claim is made.
M22 starts from integrated `main` commit
`291dfb3fd6895a2fdac7a2f0016bb181f0e5bca4`. It records the exact v1
argument contract independently of handler implementation and requires
breaking argument changes to use a new operation version. The installed
composition exercises all seven valid operations plus missing-required and
unknown-field rejection. This satisfies only RFC-0003 gate 3; cross-version
history, external feedback, semantic-diff/diagnostic evolution, and a supported
release channel remain absent. No runtime API, operation, format, dependency,
version, or CI job is added.
Ready PR #32 passed sole GitHub Actions run `31100821087` across all eight
unchanged essential jobs on DCO-signed implementation commit
`f1a89ad460467039f966ed37955144840cd96a12`.
Automated review clarification commit
`cf3ae540e71cda128837ea698f5f175a7abf2fc4` passed necessary follow-up run
`31101607485` across the same eight jobs; the original review thread is
outdated and no actionable thread remains.
PR #32 squash-integrated exact final evidence head
`a5a49dcca277f28bb3e6097f37d5418d5d3c2c9d` into `main` as
GitHub-verified commit `8a4d288c4edf55d0299828b8edee1bd1885884d9`;
both trees are `f513bec716d1735cc47a6aab862bca0f5f770af9`. The branch is
retained for audit history, and no M23 work is included.

M23 starts from integrated `main` commit
`415859e19d9d29caa1168fabc96def509897b056`. It records exact receipt-v1
semantic-diff field sets, presence, ordering, meanings, diagnostic-code
identity, and unknown-code fallback. This satisfies only RFC-0003 gate 5;
cross-version history, external feedback, and a supported release channel
remain absent. No runtime API, protocol field, operation, dependency, version,
or CI job is added.
Ready PR #34 passed initial GitHub Actions run `31104052702` across all eight
unchanged essential jobs on DCO-signed implementation commit
`a6dc30ec62d91b1f6640db2c23797967f2aefefe`. Automated review identified two
valid evidence gaps; DCO-signed correction commit
`4eb61cd49542b0a4753629f31ebe80229c7d45b8` passed necessary follow-up run
`31105197045` across the same eight jobs. PR #34 squash-integrated exact final
evidence head `eacb0153d8ac6e5f65d4d52f02c493bf9a891219` into `main` as
GitHub-verified commit `2f7152565d369225dbf69055b7d42a4c80f46d1a`;
both trees are `6ba709c29688041992bef75a2a83831275ff32db`.

M24 starts from integrated `main` commit
`55c7a72337913303b6b1f6bd31edbca7ff28683b`. It adds an offline admission
harness over the immutable M21 receipt corpus and requires a different reader
version plus supported-release evidence before gate 1 can become true. The
current `0.1.0a1`/empty-release result remains false. No runtime API, protocol,
dependency, version, workflow job, tag, release, or publication is added.
Ready PR #36 targets that exact base from DCO-signed implementation commit
`e590d482246d122120c011969b47f79f9680efa2`. Its sole GitHub Actions run
`31107800179` passed all eight unchanged essential jobs; GitHub reports the PR
`MERGEABLE` and `CLEAN`. Delayed automated review found one valid append-only-
history gap. The locally validated correction freezes mandatory source/release
prefixes and proves a newly pinned future manifest cannot replace the M21 entry;
DCO correction commit `b393d6857f0a60c5d124fdeb25b3779c8f9dab86`
passed necessary run `31108924069` across all eight unchanged essential jobs.
Final thread-aware reread found no actionable finding; squash integration
completed through PR #36 at GitHub-verified `main` commit
`b7b16697d28410567cbddf8eb962c7e6c9e664b8`. Its tree
`fa3c455ccd9722c666cc07cae325f1b50e37ddc7` exactly matches final evidence head
`1a8bd6f19f656eb5c4a0d6bd90f057a69bddbc34`; the branch is retained.

M25 starts from integrated `main` commit
`680e90dd8f9377fece23c43bd9f07ca9d76297de`. It adds an offline admission
harness for manually reviewed independent-consumer feedback and requires exact
public repository, immutable revision, protocol, outcome, and artifact
identities before gate 2 can become true. The reviewed manifest is empty, so
the current result remains false; the synthetic `.invalid` regression proves
only gate logic and is not feedback or adoption evidence. No runtime API,
protocol, dependency, version, workflow job, network activity, release, or
publication is added. Ready PR #38 targets the exact assigned base from
DCO-signed implementation commit
`9667e020c2213d415072b7c7efbd880f6b58abfa`; sole GitHub Actions run
`31111498136` passed all eight unchanged essential jobs, and the first thread-
aware read found no review finding. Delayed review then found one valid numeric-
IP locator gap. The locally validated correction requires a non-IP DNS-style
authority and adds loopback/link-local regressions. DCO correction commit
`90ed57e360765cf7f2d0973e41b8f8ec06dc4b50` passed necessary run
`31112342328` across all eight unchanged jobs. Final thread-aware reread found
no actionable finding. PR #38 squash-integrated exact final evidence head
`d0866967832fe80a49942184e1ab81d3c426a478` into `main` as GitHub-verified
commit `9ec6eeaaed40fefeb64d738d4eaaf3f7a9c4009b`; both trees are
`fcaa7b11a4aa8d1c87e57a810db16682cf9f00e6`, and the branch is retained.

M26 started from integrated `main` commit
`0de919a699dee6b10b6fef9ba2cdce5e3c0f2e62`. It adds an offline admission
harness requiring at least two reviewed supported, non-yanked final releases on
distinct feature lines plus exact publication identities before gate 6 can
become true. The reviewed release set is empty, so the current result remains
false; the prerelease workflow, local candidates, CI, and synthetic regression
are not a supported channel. No runtime API, protocol, dependency, version,
workflow job, tag, GitHub release, PyPI configuration, support promise, or
publication is added. Delayed review found and corrected an incomplete-prefix
admission gap; 1,153 local tests and necessary corrected hosted run
`31116147333` passed. PR #40 squash-integrated exact final evidence head
`ac8dd43e6b93bc89af1f5dd1821948e4860ac88b` as GitHub-verified `main` commit
`a62d28e8c36d9a590e7ad7e7a9e8b49266dcbdde`; both trees are
`e1f39a9c5d2bc81f76b45288225b27a7c782bf50`, and the branch is retained.

M27 starts from verified integrated `main` commit
`c1c3be08f7f75d90e7d1b517adbc30d56902ece4`. It adds an offline admission
harness requiring at least one independently reviewed human good-first
contribution linked to a public project issue and merged pull request, with
exact revisions, patch/feedback hashes, DCO, documented validation, no private
maintainer knowledge, and no protected API/format/dependency/workflow change.
The reviewed rehearsal set is empty, so the current result remains false;
documentation, CI, project-owned fixtures, maintainers, and non-human automation
are not external-contributor usability evidence. No runtime source, public API,
format, dependency, version, workflow job, network activity, contributor
contact, telemetry, publication, or support promise is added. Corrected hosted
run `31119640551` passed all eight effective essential jobs after a minimal
failed-job-only outage recovery. PR #42 squash-integrated exact final evidence
head `349dc3b78dcae2b1c725ed3dc8e5e646ca3d3ac1` as GitHub-verified `main`
commit `ff1c81f8aaa96245706586096f400a5fb03bdd04`; both trees are
`f957c2e40eec5bd2d70cc274079ea334d6a34cc3`.

M28 starts from verified integrated `main` commit
`17401eb32be30862496bbe02366d886a60752fb3`. It adds an offline admission
harness for the longer-term metric counting externally authored sample games.
A future record requires manually reviewed independent authorship, a public
repository and immutable revision, installed-wheel execution, exact headless/
command-receipt/replay capability evidence, distinct source/run/review
identities, and reviewed public licensing. The reviewed set is empty, so the
current count remains zero; bundled examples, maintainers, agents, CI, and
synthetic fixtures are not adoption. M28 adds no runtime source, API, protocol,
format, dependency, version, workflow job, network activity, author contact,
telemetry, tag, release, publication, certification, or support promise.
Both necessary eight-job hosted runs passed after correcting the two valid
review findings. PR #44 squash-integrated exact final evidence head
`c383a4f143fd8682059a89ff6b645104a6b4332d` as GitHub-verified `main` commit
`90d58a4567e7c7eaff90a28a7c59f2453b6d4538` with the exact final tree.

M29 starts from verified integrated `main` commit
`e4125bf31a751473d2af4fecc05a9744d551063c`. It adds an offline admission
harness for the next longer-term metric: contributor retention rather than raw
stars. A future record requires one independently reviewed external human to
complete two distinct merged public project contributions, with exact
issue/PR/revision/artifact identities, valid DCO, complete validation,
reviewed provenance, and a return merge later than the first. The reviewed set
is empty, so the current retained-contributor and return-contribution counts
remain zero; maintainers, agents, CI, popularity totals, and synthetic fixtures
are not retention. M29 adds no runtime source, API, protocol, format,
dependency, version, workflow job, network activity, contributor contact,
telemetry, tag, release, publication, certification, or support promise.
Initial hosted validation found one CPython 3.14 decoder-behavior assumption in
the excessive-nesting regression. The corrected evaluator applies an explicit
16-level structural JSON limit while ignoring strings and escapes. Correction
run `31183032073` passed all eight essential jobs, and PR #46 squash-integrated
the exact corrected tree as GitHub-verified `main` commit
`fc969a981ecdbbf842477f46486e29277119e05b`.

M30 starts from verified integrated `main` commit
`c88b166a39a793c91741bfa762af5627a87c53b4`. It adds an offline admission
harness for the next longer-term metric: installation success across the
supported OS/CPython matrix. A future record set requires one immutable public
pure-Python release wheel to pass clean isolated installation, version,
doctor, headless example, and Clockwork Arena checks in all seven practical
environments, with exact artifact/log identities and reviewed provenance. The
reviewed set is empty, so the current successful-environment count remains
zero; source-checkout CI, local builds, automation, and synthetic fixtures are
not released-user installation evidence. M30 adds no runtime source, API,
protocol, format, dependency, version, workflow job, network activity,
installation, tag, release, publication, certification, or support promise.
Ready PR #48 ran the unchanged essential CI topology on exact feature commit
`576dd070b547bef853ee47ece4c928b4e9962a7d`; run `31186083454` passed all
eight jobs. PR #48 then squash-integrated the exact feature tree as
GitHub-verified `main` commit
`675713d15a20a38233b80580e5aa773dc7a8684c`.

M31 starts from verified integrated `main` commit
`22dc58df8b0c4d17c3619d83e37c6d0ee6184441`. It adds an offline admission
harness for the next longer-term metric: issue-response and pull-request-review
time. A future window requires a complete reviewed public cohort of eligible
external-human issues and pull requests, preserves pending items, and binds
first qualifying human-maintainer actions to exact public evidence and
timestamp/latency agreement. The reviewed set is empty, so no latency aggregate
or SLA is claimed; automation, project history, and synthetic fixtures are not
human responsiveness evidence. M31 adds no runtime source, API, protocol,
format, dependency, version, workflow job, network activity, telemetry,
contributor contact, issue/PR mutation, tag, release, publication,
certification, stability change, SLA, or support promise.
Corrected head `dd4058b71439b5bade9d091831ba5453a51db35c` passed all eight
essential jobs in run `31190559197`; PR #50 squash-integrated the exact tree as
GitHub-verified `main` commit
`8adb8d46d0ce13ea3687856ae53e899e98dc42a6`.

M32 starts from verified integrated `main` commit
`b4de1d115ddb620ecddccab84637c0e66cfad9fd`. It adds an offline admission
harness for the next longer-term metric: replay-divergence rate in CI. A future
window requires a complete reviewed public cohort of eligible replay
executions, preserves cancellation, pre-replay failure, skipping, and missing
result evidence as `not-executed`, and binds verified/diverged outcomes to
exact public workflow, case, and frozen result evidence. The reviewed set is
empty, so no execution count or divergence rate is claimed; passing jobs and
synthetic fixtures are not historical rate evidence. M32 adds no runtime
source, API, replay protocol, format, dependency, version, workflow job,
network activity, telemetry, tag, release, publication, certification,
stability change, reliability target, or support promise.
Initial head `7046e59eb4840e6df492c886ce78baf4ad51cd95` passed all eight
essential jobs in run `31194645068`, but hosted review identified a mismatched
replay-divergence diagnostic. Corrected head
`f6f574c2e9b54341e77d1b9ba2d9268bffe5439a` uses and pins runtime code
`world.replay.diverged`, resolved the sole review thread, and passed all eight
essential jobs in run `31195402467`; PR #52 squash-integrated the exact tree as
GitHub-verified `main` commit
`36e8d9ed65a619569f3620b2431d977a1fb80a58`.

M33 starts from verified integrated M32 state-record commit
`60ddf57216d1054ac44df8d834756312c3864e3e`. It adds an offline admission
harness for the next longer-term metric: benchmark regression rate. A future
window requires a complete reviewed controlled cohort of paired base/head
M1-M4 `perf_counter_ns` workloads, exact p95 evidence, comparable frozen runner
profiles, and predeclared integer tolerances. Non-execution remains counted and
blocks publication. The reviewed set is empty, so no comparison count or
regression rate is claimed; local timings, M7 cProfile output, passing smokes,
and synthetic fixtures are not controlled historical rate evidence. M33 adds
no runtime or benchmark implementation, optimization, API, protocol, format,
dependency, lock, version, workflow job, telemetry, native boundary, tag,
release, publication, certification, performance target, or support promise.
Ready PR #54 exact head `3bd7e17eed26028592cb39d37e77e15c6f4371f1`
passed all eight essential jobs in run `31225942698`, had no review comment or
thread, and squash-integrated the exact tree as GitHub-verified `main` commit
`0993c73b3290809ef4e0c36d64d39e5ee5891a9b`.

## Good-first contribution queue

These are issue-ready cards, not assigned work. A maintainer opens one with the
`good first issue`, `help wanted`, `status:ready`, and listed area labels before a
contributor starts.

| Card | Outcome | Scope | Acceptance |
| --- | --- | --- | --- |
| GF-01 glossary | Add a concise glossary for authority, canonical state, composition root, receipt, deterministic, presentation, and adapter | `docs/glossary.md`, `mkdocs.yml`; documentation only | Terms link to their defining guide/ADR; `uv run --frozen mkdocs build --strict` passes |
| GF-02 expected sample output | Add sanitized example JSON and explain stable versus diagnostic fields | `examples/README.md`; do not change sample behavior or protocols | Run the documented null examples and record matching output; docs build passes |
| GF-03 release checksum negative test | Add one focused test for an extra unlisted staged artifact | `tests/unit/test_release_artifacts.py`; no script/API change unless a demonstrated defect exists | Test fails against the intentional invalid fixture and full pytest passes |

Use the [good-first task form](.github/ISSUE_TEMPLATE/good_first_issue.yml) to propose
another card. The [triage contract](docs/triage.md) defines when it is ready.

## Proposal backlog

These areas remain uncommitted proposals and require milestone assignment plus the
design process in `GOVERNANCE.md`: general scene importers, production audio,
rigid-body physics, network transports, international text shaping, automatic GPU
recovery. Constrained and general 3D are deferred under
[ADR-0028](docs/adr/0028-retain-layered-2d-and-defer-constrained-3d.md).
Visual-editor implementation is deferred under
[ADR-0029](docs/adr/0029-retain-headless-inspector-and-defer-visual-editor.md).
Executable WASM mods are deferred under
[ADR-0030](docs/adr/0030-retain-data-only-plugins-and-defer-wasm-mods.md).
Native acceleration is deferred under
[RFC-0001](docs/rfcs/0001-defer-first-native-kernel.md); its complete admission
and quantified revisit gate applies before another proposal.
