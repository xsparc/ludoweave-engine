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

M65 extends M64's complete staged sample-ZIP preflight with one portable sample
member path identity. The relative path is at most 255 ASCII characters; every
component uses the restricted portable grammar, excludes trailing periods and
Windows device stems, and retains one case-insensitive ancestor spelling.
Duplicate/case-only complete paths, explicit directory entries, explicitly
encoded non-regular file types, and file/directory prefix collisions fail
before extraction. Missing ZIP file-type mode bits remain compatible.

M65 is a narrow private release-smoke lexical boundary, not a general archive
sandbox, Unicode-normalization policy, filesystem portability guarantee, or
transactional cleanup guarantee. It adds no workflow, allocation, dependency,
lock, version, sample producer, runtime source/API, release authority, tag,
release, or publication. Pull-request fixtures are not a real public release
observation.

M66 adds an owned same-filesystem temporary staging directory. Completeness is
validated before a single rename publishes the final sample root; partial pre-
publication failures trigger cleanup, and any final entry that already exists
remains untouched. This is not crash-durable and supplies no concurrent
filesystem race isolation or post-publication rollback. It adds no workflow,
allocation, dependency, lock, version, sample producer, runtime source/API,
release authority, tag, release, or publication. Pull-request fixtures are not
a real public release observation.

M67 compares the complete preflighted archive identity with the exact
source-defined sample-bundle inventory of 50 regular files. Any unexpected
member or missing member fails content-silently before extraction or staging.
This is not content scanning or a general archive sandbox. It adds no workflow,
allocation, dependency, lock, version, sample producer, runtime source/API,
release authority, tag, release, or publication. Pull-request fixtures are not
a real public release observation. M0 through M66 are complete, reviewed,
hosted-validated, and integrated into `main`. M67 starts from exact verified
M66 closeout `995fdda097a418a7a0e570bb6b492d3f5609d471`.

M68 rejects obvious non-regular or oversized project sample archives from path
metadata before opening, revalidates the opened descriptor, and supplies that
same admitted handle to `ZipFile`. Invalid containers fail content-silently
before parser construction or staging. This is not a general archive sandbox
or immutable-input guarantee.
It adds no workflow, allocation, dependency, lock, version, sample producer,
runtime source/API, release authority, tag, release, or publication. Pull-
request fixtures are not a real public release observation. M0 through M67 are
complete, reviewed, hosted-validated, and integrated into `main`. M68 starts
from exact verified M67 closeout
`ea3de73f5ef1792df729c1f271b3d84a28db1028`.

M69 rejects sample members whose ZIP general-purpose bit flags indicate
traditional encryption, strong encryption, or masked header values. The
content-silent rejection occurs before member reads or staging and adds no
password path. This is not a general archive sandbox. It adds no workflow,
allocation, dependency, lock, version, sample producer, runtime source/API,
release authority, tag, release, or publication. Pull-request fixtures are
not a real public release observation. M0 through M68 are complete, reviewed,
hosted-validated, and integrated into `main`. M69 starts from exact verified
M68 closeout `fec3df4d490d363a9ab538f6b99ec86859e7acdc`.

M70 binds sample extraction to the digest already admitted from `SHA256SUMS`.
The same opened handle is checked before ZIP parsing and again before
publication. A persistent mismatch fails content-silently and the second-check
path cleans owned staging. This supplies no immutable-input guarantee and is
not a general archive sandbox. It adds no workflow, allocation, dependency,
lock, version, sample producer, runtime source/API, release authority, tag,
release, or publication. Pull-request fixtures are not a real public release
observation. M0 through M69 are complete, reviewed, hosted-validated, and
integrated into `main`. M70 starts from exact verified M69 closeout
`55b409d40c32c9268ee62b8c2a14aa036bcc935f`.

M71 copies the bounded source into one owned checksum-admitted snapshot and
passes that binary spooled temporary file to `ZipFile`. The parser consumes the
exact bytes matching `SHA256SUMS`, independent of later source changes. This
adds no persistent copy or source-immutability guarantee and is not a general
archive sandbox. It adds no workflow, allocation, dependency, lock, version,
sample producer, runtime source/API, release authority, tag, release, or
publication. Pull-request fixtures are not a real public release observation.
M0 through M70 are complete, reviewed, hosted-validated, and integrated into
`main`. M71 starts from exact verified M70 closeout
`f62631e2541f8f6a34b0ed84f489c2d7f9503747`.

M72 normalizes documented `BadZipFile` and `LargeZipFile` failures from the
private sample parser to one stable error. Archive-controlled parser detail is
retained as programmatic context but hidden from rendered output through
suppressed context; owned cleanup completes before normalization. Verifier
policy failures remain specific. This is not a general archive sandbox and
adds no workflow, allocation, dependency, version, sample producer, runtime
source/API, release authority, tag, release, or publication. Pull-request
fixtures are not a real public release observation. M0 through M71 are
complete, reviewed, hosted-validated, and integrated into `main`. M72 starts
from exact verified M71 closeout
`de510b5cb44a011264a4b28f6fbbf0b59e0339e8`.

M73 adds exactly `UnicodeDecodeError` raised by archive-controlled UTF-8 ZIP
names in the central directory or local header to the existing stable error.
Rendered output remains content-silent through suppressed context, and owned
cleanup completes first. Other Unicode, value, policy, filesystem, and
unexpected failures remain specific. This is not a general archive sandbox
and adds no workflow, allocation, dependency, version, sample producer,
runtime source/API, release authority, tag, release, or publication. M0 through
M72 are complete, reviewed, hosted-validated, and integrated into `main`. M73
starts from exact verified M72 closeout
`f4afb40aade2b1a59b7ceabf6f1db158b450b7cd`.

M74 adds exactly `zlib.error` raised while the standard ZIP reader processes
an invalid checksum-admitted deflated member. Rendered output remains content-
silent through suppressed context, and owned cleanup completes first. EOF,
policy, filesystem, and unexpected failures remain specific. This is not a
general archive sandbox and adds no workflow, allocation, dependency, version,
sample producer, runtime source/API, release authority, tag, release, or
publication. M0 through M73 are complete, reviewed, hosted-validated, and
integrated into `main`. M74 starts from exact verified M73 closeout
`7ecb584e71a375d1ab63ee8134e7493e418dedff`.

M75 rejects compressed patched data, ZIP general-purpose bit 5, during M69's
all-member preflight. It fails content-silently before inventory validation,
member reads, or staging, while encryption retains its established precedence.
This is no broad flag allowlist or general archive sandbox and adds no
workflow, allocation, dependency, version, sample producer, runtime source/API,
release authority, tag, release, or publication. M0 through M74 are complete,
reviewed, hosted-validated, and integrated into `main`. M75 starts from exact
verified M74 closeout `674d74c8fc852846404813ab541aab3deffd8608`.

M76 rejects enhanced deflating when central-directory ZIP general-purpose bit 4
is paired with compression method 8 during the same all-member preflight. It
fails content-silently before inventory validation, member reads, or staging;
established processing errors retain precedence, while stored members and
local-header inconsistencies remain outside this exact decision. This is no
broad flag allowlist or general archive sandbox and adds no workflow,
allocation, dependency, version, sample producer, runtime source/API, release
authority, tag, release, or publication. M0 through M75 are complete, reviewed,
hosted-validated, and integrated into `main`. M76 starts from exact verified
M75 closeout `ddf262dff7a8c93defad5a205adbaec460563439`.

M77 rejects an exact NUL byte in decoded `ZipInfo.orig_filename` during the
same all-member preflight. It fails content-silently before member metadata,
inventory validation, member reads, or staging; established flag errors retain
precedence. This is no general normalized-name comparison, no raw parser, and
no general archive sandbox. It adds no workflow, allocation, dependency,
version, sample producer, runtime source/API, release authority, tag, release,
or publication. M0 through M76 are complete, reviewed, hosted-validated, and
integrated into `main`. M77 starts from exact verified M76 closeout
`701637f99447f4d64c84047e64ec5edfa0c6889f`.

M78 rejects the exact ZIP general-purpose data-descriptor bit 3 in a separate
all-member pass before member metadata, inventory validation, member reads, or
staging. The content-silent policy preserves established M69/M75/M76 flag
precedence and runs before M77 name policy. This is no raw descriptor parser,
no broad flag allowlist, and no general archive sandbox. It adds no workflow,
allocation, dependency, version, sample producer, runtime source/API, release
authority, tag, release, or publication. M0 through M77 are complete,
reviewed, hosted-validated, and integrated into `main`. M78 starts from exact
verified M77 closeout `4bca618578f29629a7270ab5d9d308fd34363a06`.

M79 rejects exact Info-ZIP Unicode Path extra-field ID `0x7075` during a
separate archive-wide pass after established flag/descriptor policy and before
decoded-name checks, metadata, inventory, member reads, or staging. The stable
error is content-silent. This bounded extra-field walk is no broad extra-field
ban or general archive sandbox. It adds no workflow, allocation, dependency,
version, sample producer, runtime source/API, release authority, tag, release,
or publication. M0 through M78 are complete, reviewed, hosted-validated, and
integrated into `main`. M79 starts from exact verified M78 closeout
`5fe3134bf5a56e5cbf986ed33db698c830aa9219`.

M80 rejects exact PKWARE ZIP64 extended-information extra-field ID `0x0001`
during a separate archive-wide pass after M79 policy and before decoded-name
checks, metadata, inventory, member reads, or staging. The stable error is
content-silent. This bounded extra-field walk is no broad extra-field ban, raw
ZIP64 parser, large-file support change, or general archive sandbox. It adds
no workflow, allocation, dependency, version, sample producer, runtime
source/API, release authority, tag, release, or publication. M0 through M79
are complete, reviewed, hosted-validated, and integrated into `main`. M80
starts from exact verified M79 closeout
`892f17fce99d218905c6f624c730f735d21a794f`.

M81 rejects parser-exposed non-empty ZIP archive and member comments after
established flag and extra-field policy, but before decoded-name checks,
metadata, inventory,
member reads, or staging. Archive comments precede a separate all-member
comment pass and both stable errors are content-silent. This is no raw ZIP
parser, general comment scanner, or general archive sandbox. It adds no
workflow, allocation, dependency, version, sample producer, runtime source/
API, release authority, tag, release, or publication. M0 through M80 are
complete, reviewed, hosted-validated, and integrated into `main`. M81 starts
from exact verified M80 closeout
`3241a348a75c24a764f167ade48798ed3ac06af1`.

M82 rejects every parser-exposed nonzero `ZipInfo.volume` after established
flag, extra-field, and comment policy, but before decoded-name checks,
metadata, inventory, member reads, or staging. Its stable error is content-
silent. This is no raw end-record parser, no multi-volume assembler, and no
general archive sandbox. It adds no workflow, allocation, dependency, version,
sample producer, runtime source/API, release authority, tag, release, or
publication. M0 through M81 are complete, reviewed, hosted-validated, and
integrated into `main`. M82 starts from exact verified M81 closeout
`ba90021304760284550e3c458901feb0e3e29dbc`.

M83 requires both disk fields in the final conventional 22-byte end-of-
central-directory record to be zero after established flag, extra-field,
comment, and member-volume checks, but before decoded-name checks, metadata,
inventory, member reads, or staging. Its stable error is content-silent. This
is no ZIP64 end-record parser, end-record search, multi-volume assembler, or
general archive sandbox. It adds no workflow, allocation, dependency, version,
sample producer, runtime source/API, release authority, tag, release, or
publication. M0 through M82 are complete, reviewed, hosted-validated, and
integrated into `main`. M83 starts from exact verified M82 closeout
`e0ade9928e19895d5074a40fd11fcbf6bfa6fbe0`.

M84 requires both conventional end-of-central-directory entry counts to match
the standard reader's parsed member count after M83 disk-field policy, but
before decoded-name checks, metadata, inventory, member reads, or staging. Its
stable error is content-silent. This is no ZIP64 end-record parser, sentinel
resolution, multi-volume assembler, or general archive sandbox. It adds no
workflow, allocation, dependency, version, producer, runtime source/API,
release authority, tag, release, or publication. M0 through M83 are complete,
reviewed, hosted-validated, and integrated into `main`. M84 starts from exact
verified M83 closeout `1c380897fc8ee43f5885c733c1c11f87878ff2a1`.

M85 requires the final conventional central-directory size plus offset to land
exactly at the final end-of-central-directory record after M84 entry-count
policy, but before decoded-name checks, metadata, inventory, member reads, or
staging. Its stable error is content-silent. This is no central-directory
record parser, prepended executable support, self-extracting archive support,
or general archive sandbox. It adds no workflow, allocation, dependency,
version, producer, runtime source/API, release authority, tag, release, or
publication. M0 through M84 are complete, reviewed, hosted-validated, and
integrated into `main`. M85 starts from exact verified M84 closeout
`5b21c4798c16fb69b8ef08d40b02a2662677227a`.

M59 current-tree metadata hygiene remains the repository disclosure convention.
It does not rewrite Git history, attribution, DCO evidence, or external records;
its centralized guard and product-terminology boundary remain in force.

Preserve the release-integrity lineage: M42 keeps one exact release identity
across publication, M43 revalidates authenticated exact-ID asset bytes, M44
checks constrained provenance and wheel-SBOM attestations, M45 repeats exact
public retrieval without a release credential, and M46 separates that public
consumer observation onto a fresh runner, and M47 widens only its verifier and
  cross-platform operating-system portability. M48 narrows response/failure
  semantics, M49 confines the actual connected peer, M50 disables ambient TLS
  key logging, M51 validates the actual negotiated session, M52 observes the
  verified socket's reference hostname and peer certificate, and M53 proves
  the socket retained the exact client context after the handshake. M54 then
  requires the actual socket to report that its session was not reused, and
  M55 validates the documented HTTP/1.1-class value and unambiguous response
  framing without claiming the exact raw status-line token. M56 then validates
  status and redirect references before body use. M57 then validates body
  blocks and declared-length agreement, and M58 orders response/connection
  cleanup before redirect continuation or publication. M60 adds final-entry
  filesystem collision checks before network or validator work, M61 separates
  candidate and output roots, M62 constrains portable asset names, M63 confines
  subordinate text output, M64 bounds staged sample-bundle extraction, M65
  constrains portable sample member paths, M66 stages complete sample roots
  before publication, M67 requires the exact expected inventory, and M68
  bounds the regular archive container before parsing. M69 rejects encrypted
  sample-member indicators before reads or staging. M70 binds sample parsing
  and publication to the staged-release checksum on the same opened handle.
  M71 makes an owned checksum-admitted snapshot the exact parser input, M72
  confines documented parser failures content-silently, M73 adds the exact ZIP
  UTF-8 decoding failure, and M74 adds the exact deflate decompression failure;
  none of these milestones authorizes a real release.

M35 adds strict offline admission readiness for the design plan's final
ordered longer-term metric: the number of independently authored third-party
adapters or plugin-backed adapters passing conformance. The exact reviewed
manifest explicitly asserts a complete project-accepted submission-census
review and contains no submissions, so the current passing count is zero. It
is not a global package census, support matrix, security/performance result,
provider certification, or ecosystem claim. Manual review owns independence,
authorship, license, eligibility, outcome, provenance, validation, privacy,
consent, and census completeness. Project-owned and maintainer-authored
references never count; passed, failed, and not-executed accepted outcomes
remain in history. Only the exact existing M17 render-device, M18 agent-tool,
and M19 WorldStore profiles are accepted. An M12-compatible `render.device`
manifest is required for a plugin-backed record but never counts without a
passing render-device profile. M35 may add only frozen reviewed data, an
explicitly invoked offline evaluator/validator, adversarial tests, RFC/docs,
and source/wheel/release-sample smoke. It may not discover, import, install, or
execute providers; query networks; collect telemetry; or change runtime
source, public APIs/exports, protocols/profiles, plugin fields, formats,
dependencies, lock, version, CI topology, release workflow, tag, publication,
certification, stability label, SLA, or support policy. M0 through M34 are
complete, reviewed, hosted-CI validated, and integrated into `main`. M35 starts
from exact verified M34 integration-record commit
`277de9052e768a5f70d32f1a2f67ec9f93353723` and contains no subsequent
milestone.

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
