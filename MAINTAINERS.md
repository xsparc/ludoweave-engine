# MAINTAINERS.md

This file is the operating contract for LudoWeave Engine maintainers and contributors.

## Read first

1. The assigned issue or milestone acceptance criteria.
2. `docs/architecture.md` and relevant accepted ADRs.
3. `.project/PROJECT_STATE.md`, `.project/CURRENT_TASK.md`, and `.project/TEST_EVIDENCE.md`.
4. Current code, tests, CI, and `git status`.

## Authoritative rules

1. Canonical runtime state belongs to the ECS/world store as it is introduced through M1.
2. Headless execution is first-class.
3. Every externally initiated world mutation must eventually be a versioned command that produces a receipt.
4. Public APIs must not expose wgpu, GLFW, NumPy storage, or native extension objects.
5. No arbitrary Python evaluation or unauthenticated remote control.
6. Normal CPython 3.12-3.14 is the baseline; free-threaded builds are optional experiments.
7. Apache-2.0 and DCO sign-off govern contributions.
8. Never claim a check passed unless it was executed and its result was recorded.
9. Do not create empty speculative packages or abstractions without an exercised test or example.
10. Stop at the assigned milestone; do not opportunistically implement adjacent roadmap items.

## Dependency direction

Contracts and core code do not import application, tool, or concrete-backend modules. Application code depends on engine-owned protocols. Concrete adapters implement those protocols. CLI and examples are composition roots and may choose a concrete adapter. See ADR-0002 and the architecture tests.

## Working method

- Keep one task in progress and map changes to acceptance criteria.
- Preserve unrelated user changes and never use destructive Git commands to discard work.
- Add focused tests and public documentation with behavior changes.
- Run focused checks first, then every command in the README quality suite.
- Review the diff for scope growth, secrets, dependency violations, backend leakage, nondeterminism, packaging effects, and stale documentation.
- Update `.project/PROJECT_STATE.md` and `.project/TEST_EVIDENCE.md` with reproducible facts only.

Repository-facing maintenance records use role- and purpose-based names.
Contribution identity and authorship remain governed by Git history and DCO
sign-off; do not rewrite historical evidence or make unsupported provenance
claims.

## Current boundary

M34 adds strict offline agent-tool recovery-rate admission readiness for the
next longer-term metric in the design plan. The reviewed manifest is empty, so
its window and call counts remain zero, its exact rational rate is absent, and
no recovery-free, reliability, quality, release-gate, certification, SLA, or
support result may be claimed. Manual review, not evaluator logic, owns the
complete task-directed session census, call eligibility, task context, manual-
recovery status, outcome, provenance, and validation. Known failures and calls
completed after recovery remain in the denominator; `terminal-unobserved`
blocks publication. M34 may add only frozen data evidence, an explicitly
invoked evaluator/validator, synthetic gate tests, RFC/docs, and source/wheel/
release-sample artifact smoke. It may not query providers, collect telemetry,
expose private session content, or change runtime source, agent tools,
protocols, APIs/exports, formats, dependencies, lock, version, release
workflow, native/WASM boundaries, tag, publication, certification, stability
label, success target, SLA, or support policy. The only CI change keeps all
eight essential jobs and limits them to one substantive pull-request run,
excluding duplicate post-merge and `.project/**`-only runs. M0 through M33 are
complete, reviewed, hosted-CI validated, and integrated into `main`. M34 starts
from exact verified M33 integration-record commit
`d12c30a02782c0ebf892e27c5daf6e9fec1c93ee` and contains no subsequent
milestone.

M33 adds only strict offline benchmark-regression-rate admission readiness for
the next longer-term metric in the design plan. The reviewed manifest is empty,
so its window and comparison counts remain zero, its exact rational rate is
absent, and no zero-regression, performance, quality, release-gate, native-code,
or support result may be claimed. Manual review, not evaluator logic, owns
controlled-runner census completeness, eligibility, base/head comparability,
parameter equality, tolerance predeclaration, outcome, provenance, and
validation. Eligible comparisons are registered M1-M4 `perf_counter_ns` p95
workloads; M7 cProfile diagnostics are not timing evidence. Future cohorts must
preserve cancellation, pre-benchmark failure, skips, and unavailable evidence
as `not-executed`. M33 may add only frozen data evidence, an explicitly invoked
evaluator/validator, synthetic gate tests, RFC/docs, and source/wheel/release-
sample artifact smoke through the unchanged eight essential CI jobs. It may
not query GitHub, collect telemetry, change benchmarks or CI, optimize runtime,
execute providers, or change runtime source, public APIs/exports, formats,
protocols, dependencies, lock, version, workflows, CI topology, native/WASM
boundaries, tag, release, publication, certification, stability label,
performance target, SLA, or support policy. M0 through M32 are complete,
reviewed, hosted-CI validated, and integrated into `main`. M33 starts from
exact verified M32 integration-record commit
`60ddf57216d1054ac44df8d834756312c3864e3e` and contains no subsequent
milestone.

M32 adds only strict offline CI replay-divergence-rate admission readiness for
the next longer-term metric in the design plan. The reviewed manifest is empty,
so its window and execution counts remain zero, its exact rational rate remains
absent, and no zero-divergence, reliability, quality, release-gate, or support
result may be claimed. Manual review, not evaluator logic, owns eligible CI
replay-execution scope, complete cohort coverage, outcome, provenance, and
validation. Eligibility is fixed before outcomes and covers verification cases
expected to reproduce canonical state with hash verification enabled; it
excludes intentionally divergent negative fixtures and verification-disabled
diagnostics. Future cohorts must preserve cancellation, pre-replay failure,
skips, and unavailable result evidence as `not-executed` rather than selecting
only completed checks. M32 may add only frozen data evidence, an explicitly
invoked evaluator/validator, synthetic gate tests, RFC/docs, and source/wheel/
release-sample artifact smoke through the unchanged eight essential CI jobs. It
may not query GitHub, collect telemetry or logs, change CI, execute providers,
or change runtime source, public APIs/exports, replay/persistent formats,
protocols, operations, dependencies, lock, version, workflows, CI topology,
tag, release, publication, certification, stability label, reliability target,
SLA, or support policy. M0 through M31 are complete, reviewed, hosted-CI
validated, and integrated into `main`. M32 starts from exact verified M31
integration-record commit `b4de1d115ddb620ecddccab84637c0e66cfad9fd` and
contains no subsequent milestone.

M31 adds only strict offline issue-response and pull-request-review latency
admission readiness for the next longer-term metric in the design plan. The
reviewed manifest is empty, so its window and measurement counts remain zero,
latency aggregates remain absent, and no response-time, review-time, service-
level, support, or responsiveness result may be claimed. Manual review, not
evaluator logic, owns external-human eligibility, human-maintainer status,
participant distinctness, first-qualifying-action state, complete cohort
coverage, provenance, and validation. Future cohorts must preserve pending
items rather than selecting only completed actions. M31 may add only frozen
data evidence, an explicitly invoked evaluator/validator, synthetic gate tests,
RFC/docs, and source/wheel/release-sample artifact smoke through the unchanged
eight essential CI jobs. It may not query or mutate issues/PRs; contact
contributors; collect usernames, private correspondence, personal data, or
telemetry; use networking, discovery, dynamic imports, subprocesses,
installation, or provider execution; or change runtime source, public APIs/
exports, persistent formats, protocols, operations, dependencies, lock,
version, workflows, CI topology, tag, release, publication, certification,
stability label, SLA, or support policy. M0 through M30 are complete, reviewed,
hosted-CI validated, and integrated into `main`. M31 starts from exact verified
M30 integration-record commit
`22dc58df8b0c4d17c3619d83e37c6d0ee6184441` and contains no subsequent
milestone.

M29 adds only strict offline external contributor-retention admission readiness
for the second longer-term adoption metric in the design plan. The reviewed
manifest is empty, so its retained-contributor and return-contribution counts
and result must remain zero/false and must not claim an external person,
contribution, retention, popularity, or adoption result. Manual review, not
evaluator logic, owns identity, independence, same-person continuity,
chronology, provenance, validation, DCO state, and retention. M29 may add only
frozen data evidence, an explicitly invoked evaluator/validator, synthetic gate
tests, RFC/docs, and source/wheel/release-sample artifact smoke through the
unchanged eight essential CI jobs. It may not contact contributors; discover
or query remote records; open or mutate issues/PRs as evidence; collect private
communication or personal data; use networking, telemetry, discovery, dynamic
imports, subprocesses, installation, or provider execution; or change runtime
source, public APIs/exports, persistent formats, protocols, operations,
dependencies, lock, version, workflows, CI topology, tag, release,
publication, certification, support policy, or stability label. The separately
authorized repository-convention migration may only rename maintenance guidance
and state paths and update their references; it may not change runtime or
milestone semantics. M0 through M28
are complete, independently accepted, hosted-CI validated, and integrated into
`main`. M29 starts from exact verified M28 integration-record commit
`e4125bf31a751473d2af4fecc05a9744d551063c` and contains no subsequent
milestone.

M28 adds only strict offline external sample-game adoption admission readiness
for the first longer-term adoption metric in the design plan. The reviewed
manifest is empty, so its current game count and result must remain zero/false
and must not claim an external author, user, game, adoption, licensing result,
or compatibility. Manual review, not evaluator logic, owns authorship,
independence, repository provenance, license state, and outcome. M28 may add
only frozen data evidence, an explicitly invoked evaluator/validator,
synthetic gate tests, RFC/docs, and source/wheel/release-sample artifact smoke
through the unchanged eight essential CI jobs. It may not solicit/contact
authors; discover/query remote repositories; open or mutate issues/PRs as
evidence; collect private communication or personal data; use networking,
telemetry, discovery, dynamic imports, subprocesses, installation, or provider
execution; or change runtime source, public APIs/exports, persistent formats,
protocols, operations, dependencies, lock, version, workflows, CI topology,
tag, release, publication, certification, support policy, or stability label.
M0 through M28 are complete, independently accepted, hosted-CI validated, and
integrated into `main`. M28 started from exact verified integration-record
commit `17401eb32be30862496bbe02366d886a60752fb3`. PR #44 passed both necessary
eight-job hosted runs after correcting two valid review findings and squash-
integrated exact final evidence head
`c383a4f143fd8682059a89ff6b645104a6b4332d` as GitHub-verified `main` commit
`90d58a4567e7c7eaff90a28a7c59f2453b6d4538`; both trees are
`2f5ebf96af70741deb8d2b7d18ffa6d84effc494`. M28 contains no subsequent
milestone.

M27 adds only strict offline external-contributor rehearsal admission readiness
for the design-plan objective that public documentation enable a first external
contribution without private maintainer knowledge. The reviewed manifest is
empty, so its current result must remain false and must not claim usability,
adoption, feedback, or external contribution. Manual review, not evaluator
logic, owns contributor independence, absence of private assistance, merge/DCO
state, and provenance. M27 may add only frozen data evidence, an explicitly
invoked evaluator/validator, synthetic gate tests, RFC/docs, and source/wheel/
release-sample artifact smoke through the unchanged eight essential CI jobs. It
may not solicit/contact contributors; open or mutate issues/PRs as evidence;
collect private correspondence or personal data; use networking, telemetry,
discovery, dynamic imports, subprocesses, or provider execution; or change
runtime source, public APIs/exports, persistent formats, protocols, operations,
dependencies, lock, version, workflow, CI topology, tag, release, publication,
support policy, or stability label.
Ready PR #42 passed all eight unchanged essential jobs after one failed-job-
only rerun recovered GitHub's resolved Actions outage. Its final thread-aware
reread found no actionable review issue. PR #42 squash-integrates exact final
evidence head `349dc3b78dcae2b1c725ed3dc8e5e646ca3d3ac1` into `main` as
GitHub-verified commit `ff1c81f8aaa96245706586096f400a5fb03bdd04` with the exact
final tree.

M26 adds only strict offline supported deprecation release-channel
admission readiness for RFC-0003 gate 6. The reviewed manifest is empty, so its
current result must remain false and must not claim support or publication.
Manual review, not evaluator logic, owns release existence, support/yank status,
and provenance. M26 may add only frozen data evidence, an explicitly invoked
evaluator/validator, synthetic gate tests, RFC/docs, and source/wheel/release-
sample artifact smoke through the unchanged eight essential CI jobs. It may not
create/push a tag; publish a GitHub release or PyPI package; configure trusted
publishing; change the release workflow, package version, runtime/API/exports,
protocol, dependency, lock, stability metadata, or support policy; or use
networking, telemetry, discovery, subprocesses, or provider execution.
Ready PR #40 passed the initial and necessary corrected eight-job hosted runs;
the correction binds every reviewed manifest digest to its complete mandatory
history. PR #40 squash-integrates exact final evidence head
`ac8dd43e6b93bc89af1f5dd1821948e4860ac88b` into `main` as GitHub-verified
commit `a62d28e8c36d9a590e7ad7e7a9e8b49266dcbdde` with the exact final tree.

M25 is assigned only to strict offline external-consumer-feedback admission
readiness for RFC-0003 gate 2. The reviewed manifest is empty, so its current
result must remain false and must not claim external adoption. Manual review,
not evaluator logic, owns independence and provenance. M25 may add only frozen
data evidence, an explicitly invoked evaluator/validator, synthetic gate tests,
RFC/docs, and source/wheel/release-sample artifact smoke through the unchanged
eight essential CI jobs. It may not solicit or contact consumers; use network,
telemetry, discovery, dynamic imports, subprocesses, or provider execution;
change runtime source, public APIs/exports, protocols, operations, dependencies,
lock, version, workflow, or stability labels; or publish a tag, release, or
package.
The locally validated implementation is published through ready PR #38 at
DCO-signed commit `9667e020c2213d415072b7c7efbd880f6b58abfa`. Its sole
GitHub Actions run `31111498136` passed all eight unchanged essential jobs;
the first thread-aware read found no review finding. Delayed automated review
then found one valid P2 in the future locator gate. The locally validated
correction rejects numeric IP authorities and adds loopback/link-local
regressions. DCO correction commit
`90ed57e360765cf7f2d0973e41b8f8ec06dc4b50` passed necessary run
`31112342328` across all eight unchanged essential jobs. Final thread-aware
reread found no actionable finding; no reply or manual resolution was
performed. PR #38 squash-integrated exact final evidence head
`d0866967832fe80a49942184e1ab81d3c426a478` into `main` as GitHub-verified
commit `9ec6eeaaed40fefeb64d738d4eaaf3f7a9c4009b`; both trees are
`fcaa7b11a4aa8d1c87e57a810db16682cf9f00e6`, and the sole parent is the
assigned base. The milestone branch remains the audit trail.

M24 adds only strict offline cross-version receipt-corpus admission readiness.
Its current result remains false and does not claim actual history or adoption.
Delayed review's append-only finding is corrected by executable mandatory
source/release prefixes and a replacement-corpus regression. Runs `31107800179`
and `31108924069` passed all eight unchanged essential jobs. PR #36 squash-
integrated exact final evidence head
`1a8bd6f19f656eb5c4a0d6bd90f057a69bddbc34` into `main` as GitHub-verified
commit `b7b16697d28410567cbddf8eb962c7e6c9e664b8`; both trees are
`fa3c455ccd9722c666cc07cae325f1b50e37ddc7`, and the sole parent is the
assigned base. The milestone branch remains the audit trail.

M0 through M26 are complete, independently accepted, hosted-CI validated, and
integrated into `main`. M27 starts from exact verified integration-record
commit `c1c3be08f7f75d90e7d1b517adbc30d56902ece4` and contains no subsequent
milestone.
M22 adds only the built-in v1 operation-argument compatibility and deprecation
policy identified by RFC-0003: a frozen repository contract, deterministic
installed evidence, tests, RFC/docs, artifact smoke, and gate bookkeeping. It
changes no runtime source, operation/handler/command/receipt field, dependency,
lock, version, workflow job, or stability label. Ready PR #32 passed Actions
runs `31100821087` and `31101607485` across all eight unchanged essential jobs.
It squash-integrates final evidence head
`a5a49dcca277f28bb3e6097f37d5418d5d3c2c9d` into `main` as
GitHub-verified commit `8a4d288c4edf55d0299828b8edee1bd1885884d9`;
both trees are `f513bec716d1735cc47a6aab862bca0f5f770af9`. No
cross-version or external-adoption claim, stability promotion, storage,
provider, transport, networking, native/WASM, 3D, editor, or M23 work is
included.

M23 starts from exact integrated `main` commit
`415859e19d9d29caa1168fabc96def509897b056`. RFC-0006 freezes exact
receipt-v1 semantic-diff field sets/meanings and diagnostic-code evolution,
while phase/message/scalar details remain non-authoritative metadata. Only
RFC-0003 gate 5 may become true; cross-version history, external feedback, and
a supported release channel remain false. No runtime source, public export,
protocol field, dependency, lock, version, workflow, or CI job changes.
Ready PR #34 and GitHub Actions run `31104052702` validate all eight unchanged
essential jobs on DCO-signed M23 implementation commit
`a6dc30ec62d91b1f6640db2c23797967f2aefefe`. Delayed automated review found two
valid evidence gaps: per-code meanings and exact full-diff contents/order were
not independently frozen. Both corrections pass the local full/artifact gate
and follow-up GitHub Actions run `31105197045` across the unchanged eight jobs.
Thread-aware reread confirms the unresolved anchors now sit beside the exact
requested evidence and neither finding remains actionable. Exact squash
integration is complete. PR #34 squash-integrated exact final evidence head
`eacb0153d8ac6e5f65d4d52f02c493bf9a891219` into `main` as GitHub-verified
commit `2f7152565d369225dbf69055b7d42a4c80f46d1a`; both trees are
`6ba709c29688041992bef75a2a83831275ff32db`, and the sole parent is the
assigned base. The milestone branch remains the audit trail.

M1-M7 are integrated into `main` by PR #8; M8-M14 are squash-integrated by PR
#16 as verified commit `2c62c8ed9c4ced6292260f6b8c84b1f069de1eaa` with the
exact final M14 tree. Superseded stacked PRs #9 through #15 are closed and
their branches remain for audit history. M13 is only a bounded offline rollback/network-snapshot
readiness evaluation. M9 defers the Box2D v3 plugin. M10 adds only the headless
owned-child semantic inspector. M11 adds bounded headless 2D audio-mix,
bitmap-text, tick-animation, tilemap, and particle authoring through existing
backend-neutral extraction. M12 adds only strict data-only preview plugin
manifests, deterministic compatibility checks, and an explicitly invoked local
validation CLI. M13 proves immutable local correction branches and records the
external tick-input limitation; it may not add a transport or live
rollback service. M14 is only the installed-surface constrained-3D decision.
It retains layered 2D and adds evidence, tests, and documentation, but no
runtime package, public 3D contract, persistent format, provider, or dependency.
Repository-state evidence is integrated in `main` by PR #18 at
`bfea67d2d922e8c591224d18f56c14d572d7f7da`.
M15 retains the headless inspector and defers visual-editor implementation
under ADR-0029. Its evidence-only implementation is published through ready PR
#19 and validated by hosted run `31036925179`; it adds no runtime source,
public API, persistent format, dependency, lock, version, or CI change.
PR #19 squash-integrates the exact M15 tree as verified `main` commit
`c013dad38b1b64f0f4ccddc19681d643f6414427`. M16 is assigned only to a
WASM-mod security admission decision. It must retain data-only plugins and add
threat-model, installed evidence, tests, and documentation without selecting or
adding a runtime, loader, executable manifest field, guest ABI, WASI, host
function, public API, persistent format, dependency, lock, version, or CI job.
Its implementation is complete and independently accepted on the M16
milestone branch. Ready PR #20 and GitHub Actions run
`31039403209` validate all eight unchanged essential jobs on DCO-signed
implementation commit `bcaf78fbc78bda8a13a95e397ab15d003dd4a6ce`.
PR #20 squash-integrates exact final head
`808e48a5cb2727c8e1f4d7e896c4f8c7d41bfe1a` into `main` as GitHub-verified
commit `e2bd57c057c0c16861953c0702b2012c4cabfe90` with the exact final tree.
M17 is assigned only to an installed `RenderDevice` baseline conformance
profile derived from the design plan's third-party-adoption metric. It accepts
an explicitly supplied trusted factory, returns sanitized versioned evidence,
and passes against Null plus the existing optional wgpu adapter through the
unchanged essential CI topology. Ready PR #22 and GitHub Actions run
`31042903689` validate all eight jobs on DCO-signed implementation commit
`8e592f329424719214239bf97bd85dad9c9c5928`. PR #22 squash-integrates final
evidence head `148600cdaf9c419fbf552c68f833e0d55655731f` into `main` as
GitHub-verified commit `610261c8450afc3d7db6ebb2b0425a1829737aec`
with the exact final tree.
It may not discover, dynamically import,
install, sandbox, certify, or admit provider code, change plugin manifests, or
add a concrete provider, dependency, lock, version, persistent world format,
canonical state, or package-root export. Do not add discovery, imports, hook execution,
installation/resolution, a global plugin registry, GUI/editor, sockets,
networking or remote attach, arbitrary child commands, another world store, a
Box2D adapter,
release tag, GitHub release, or PyPI publication. Real audio playback, font
parsing/shaping, network agent transports, editor work, constrained/general 3D,
SDL3, executable WASM, and native code remain out of scope.
RFC-0001 records the evidence-based native-code deferral; local performance
misses are not automatic authorization for acceleration.

M18 adds only an installed baseline conformance profile over the existing
12-tool transport-independent agent service. M19 is assigned only to an
installed baseline conformance profile over the existing public `WorldStore`
contract. It must accept an explicit trusted `factory(ComponentRegistry)`,
return sanitized versioned evidence, pass production and reference worlds
through isolated wheel/release smoke, and add no CI job. It may not discover,
import, install, or launch provider code; add a storage backend, database,
external-resource lifecycle, native/archetype/NumPy storage, format, plugin
field, dependency, lock, version, or package-root export; or claim project-
owned evidence as third-party adoption or certification.
Ready PR #26 and GitHub Actions run `31092244573` validate all eight unchanged
essential jobs on DCO-signed M19 implementation commit
`1da692a693c1f92e10b676c2d4539354ce3ff59f`. PR #26 squash-integrates exact
final evidence head `b93ca591f7063a1500cf105e6b0496b33573c69a` into `main` as
GitHub-verified commit `1a7219e540d8f4cb3c1f60ff12981513c6860ef9`; both trees are
`7fcd614fdde76daf1807f27dbe78ec306a501cc3`. M19 is complete; no M20 work was
included in it.

M20 adds only an installed command/receipt preview-readiness decision. It
confirms the current same-version canonical and atomic behavior, reuses the
existing M18 agent-tool profile, defines the complete compatibility gate, and
records the result under RFC-0003 through source, isolated-wheel, and release-
bundle evidence. It does not add or reinterpret a
command, operation, receipt field/reader, schema, migration, public runtime
symbol, stability label, root export, dependency, lock, package version, or CI
job. No external adoption, cross-version compatibility, tag, release,
publication, or certification may be claimed without direct evidence.
Ready PR #28 and GitHub Actions run `31095009029` validate all eight unchanged
essential jobs on DCO-signed M20 implementation commit
`d96d132da5ee847d6e86645be5e87a1e4aa5e89e`. PR #28 squash-integrates exact
final evidence head `d04561184996fac507071ad9e7dd0ef9c5e3cb7c` into `main` as
GitHub-verified commit `d166ef86bf25526d9d7715f63263d3cac6db78d4`; both trees are
`c3e2dc1224f530fb483d1b9684ff55329bf9557b`. M20 is complete; no M21 work is
included in that integration.

M21 adds only a strict resource-bounded public reader for the unchanged
`ludoweave.receipt/1` graph, structured decoding failures, exact committed/
dry-run/rejected `0.1.0a1` fixture inputs, installed source/wheel/release
evidence, and RFC-0004. The fixture set is a single-version baseline, not
cross-version compatibility evidence. Only the public-reader gate from
RFC-0003 may become true; all command/transaction/receipt contracts remain
experimental. It may not reinterpret a protocol or field, add a command,
operation, migration, provider loader, ambient filesystem/network reader,
dependency, lock, version, CI job, backend, storage implementation, root
export, native/WASM code, tag, release, or publication, or claim external
adoption, certification, cross-version compatibility, or stability promotion.
Ready PR #30 and GitHub Actions run `31098563810` validate all eight unchanged
essential jobs on DCO-signed M21 implementation commit
`cec339be07318a7c1586bb3405e8f9b1904859f5`. PR #30 squash-integrates exact
final evidence head `4e378756b2a1733de28e7160ac2d6d72921f3e4a` into `main` as
GitHub-verified commit `6bfb56555cafc93a7312f64465ea15cd7c450e79`;
both trees are `ea3f410fac31d7a32faee4e697c4fb0941b657df`. No hosted pass or
integration widens the M21 boundary or establishes cross-version compatibility.
