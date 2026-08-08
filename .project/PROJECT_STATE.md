# Project State

## M42 implementation complete

M42 starts from exact clean synchronized M41 closeout commit
`0dec2254a9d9483b27d158aaad108340e9c94e28`. It closes the final-state
observation gap after the verified private draft is published. The exact
numeric release database ID now crosses the existing CLI transition and is
fetched once more through the pinned authenticated API.

The internal validator advances to `ludoweave.release-draft-integrity/3` and
requires explicit `draft` or `published` state. Drafts require mutable
prerelease state and null `published_at`; published records require public
prerelease state, a boolean immutable field, and a valid UTC publication time.
Both states retain exact tag, title, bounded notes, and asset verification.

One new read-only postpublication request runs inside the existing tag job.
M42 adds no job, runner, action, permission, trigger, dependency, credential,
tag, release, upload, publication, automatic rollback, or immutable-release
policy. RFC-0025 and the release/security/architecture surfaces document the
boundary. Findings-first review strengthened content-silent published drift and
non-mutation coverage. The complete corrected Python 3.12 suite passes 1,850
tests with 13 expected skips; Python 3.13/3.14 each pass 1,840 with 14 expected
skips. Real wgpu, profiles, vertical slices, reproducible distributions,
installed-wheel smoke, complete release smoke, and exact mutable/immutable
synthetic release states pass. CI, runtime, metadata, dependency, lock,
permission, action, and runner boundaries remain unchanged.

Ready PR #77 exact head `45cd04e627f44400e8bd3adcbeeaf1756160f745`
passed run `31271273535` in exactly three allocations: Linux 6m54s, Windows
3m39s, and macOS 1m59s. No review, issue comment, review comment, or thread was
present. Squash `28dd9d7e282ec85c06b71ed340f3cfcea379d6be` has sole parent the exact
M41 closeout, preserves reviewed tree
`7e65795a6b44de7b3ff393128274eda207c58dc3`, has a valid GitHub signature and
standalone DCO trailer, and allocated no post-merge `main` run. The feature
branch is deleted locally and remotely. Only the documentation-only integration
and closeout records remain.

## M41 complete

M41 starts from exact clean synchronized M40 closeout commit
`9983e0da88b6aef999d26498cc6438f0b3c5927b`. It closes the remaining private-
draft metadata gap: the staged release notes already feed
`gh release create --notes-file`, but M40 did not compare the authenticated
release `body` with that source before publication.

The internal validator advances to `ludoweave.release-draft-integrity/2`. It
reads only the fixed staged `RELEASE_NOTES.md` regular non-symlink file, caps it
at 256 KiB, requires non-empty strict UTF-8 without NUL, and rejects any remote
body difference. Missing, null, substituted, truncated, newline-, whitespace-,
or Unicode-different text fails with a stable structured code; note content is
never emitted.

Official GitHub CLI and REST documentation confirms `--notes-file` supplies the
release notes and the authenticated release document exposes them as `body`.
The existing M40 API document and verifier invocation are therefore sufficient:
M41 changes neither workflow file and adds no runner, action, permission,
trigger, dependency, credential, API call, tag, release, or publication
authority. RFC-0024 and the release/security/architecture surfaces now document
the boundary. Focused static checks and 26 behavior/adversarial tests pass with
one Windows symlink-capability skip after correcting a Windows-only byte-fixture
and pytest case-ID defect. Findings-first review then made notes validation
precede asset scanning so a symlinked notes member uses the notes-specific code;
the complete corrected Python 3.12 suite passes 1,830 tests with 13 expected
skips, and Python 3.13/3.14 each pass 1,820 with 13 expected skips. Real wgpu,
profiles, vertical slices, reproducible distributions, installed-wheel smoke,
complete release smoke, and exact synthetic draft verification pass. Workflow,
runtime, metadata, dependency, lock, permission, and runner boundaries remain
unchanged.

Ready PR #74 exact head `ec051d4fd2da80235da1a94642158ebe384cb2b0`
passed run `31269399211` in exactly three allocations: Linux 6m55s,
Windows 2m44s, and macOS 2m12s. No review, comment, or thread was present.
Squash `89a641559c246e971869a3ae06a878de81bffcee` has sole parent the exact M40
closeout, preserves reviewed tree `6446826ee0b35c02dcebc78b9fad3f55caaca0c5`,
has a valid GitHub signature and standalone DCO trailer, and allocated no
post-merge `main` run. The feature branch is deleted locally and remotely.
Documentation-only PR #75 exact head
`d967624c618e433beda1052a7715872b0f256540` classified four paths as
documentation and passed run `31270041957` in one 33-second Linux allocation;
the desktop umbrella skipped with zero steps and no runner. With no feedback,
it squash-integrated as `b05dbda471edf2ac14c5e0b6bf4bd75aaf23f252`,
preserving its reviewed tree, exact feature-squash parent, valid signature,
standalone DCO, and zero post-merge run. Its branch is deleted locally and
remotely. Only the zero-run closeout record remains.

## M40 complete

M40 starts from exact clean synchronized M39 closeout commit
`49fba13477890bf6bf1c9e6a645e669b3a69492f`. It makes the existing GitHub
release CLI's internal draft/upload/publish sequence explicit. The tag job will
create an asset-free prerelease draft, upload the staged set without clobbering,
fetch the draft with REST API version `2026-03-10`, validate it, and only then
publish.

The standard-library validator caps duplicate-free strict JSON, local asset
count, individual and total bytes, safe basenames, and identity fields. It
requires exact tag/title/draft state, a complete duplicate-free remote set,
`state=uploaded`, and exact local/remote names, sizes, and SHA-256 digests.
Success emits only sorted safe identities; failures are structured and leave an
unpublished draft for inspection. The validator owns no network, token, shell,
dynamic import, release mutation, clobber, or cleanup authority.

Focused format/lint/strict-type and 18 behavior/adversarial tests pass with one
Windows symlink-capability skip after one typing/order correction. The explicit
workflow and M38-M40 architecture focus pass 33 tests with the same skip after
one mechanical format correction. Findings-first review then corrected the
draft lookup: GitHub documents the tag-name REST route for published releases,
so the workflow now resolves the authenticated draft's numeric database ID,
validates it, and fetches that exact release by ID.

The complete Python 3.12 suite passes 1,818 tests with 12 expected skips;
Python 3.13 and 3.14 each pass 1,808 with 13 expected skips. Real-wgpu,
base/graphics profiles, Clockwork Arena, Agent World Builder, deterministic
two-build comparison, installed-wheel smoke, ten-artifact release smoke, and a
real-staging synthetic-draft verification all pass. Review found no credential,
archive, native-object, runtime, dependency, lock, or CI drift after the exact
draft-route correction. M40 changes no pull-request CI workflow,
runner/job/matrix count, action, permission, trigger, dependency, lock, package
version, runtime/public API, attestation, tag, release, credential, immutable-
release setting, PyPI configuration, supported release policy, or deferred
subsystem. Final recorded-tree static, architecture, docs, and complete Python
3.12 validation passes. The initial exact implementation head passed all three
hosted allocations, but review correctly found that pathological JSON nesting
and overlong integers could escape as unstructured parser exceptions. No merge
is claimed for that head. The parser correction and both pathological-input
regressions pass focused static/behavior checks, the complete architecture gate,
strict docs, and all 1,818 Python 3.12 tests.

Corrected head `967147b3bbc83414d0ce303845975dea0c4e9d26` passed exact run
`31267396755` in three allocations: Linux 6m43s, macOS 2m51s, and Windows
3m35s. The resolved review thread is outdated and no unresolved thread remains.
Squash `e9d9850e11f572a1d4ddc78d06c79b23a5584f87` has sole parent the exact M39
closeout, tree `974b790ab2d925562185c2c18707f3878b0e7bdd` exactly equal to the
reviewed head, a valid GitHub signature, and standalone DCO trailer. It
allocated no `main` run. The feature branch is deleted locally/remotely; clean
synchronized `main` is the sole branch, no PR, tag, or release is open/present,
and full Git object checking passes.

Documentation-only integration record PR #72 changed four paths and passed run
`31268048294` in one 35-second Linux allocation; the desktop umbrella skipped
with zero steps and no runner. It had no review, comment, or thread. Squash
`67d03d41430dc24bf81a894752b3641de8e521ed` has sole parent the M40 feature
integration, tree `896461bbfd43975ca1ee49962409d9b38695c10f` exactly equal to the
reviewed head, a valid GitHub signature, and standalone DCO trailer. It
allocated no `main` run. The record branch is deleted locally/remotely; before
this closeout branch, clean synchronized `main` was the sole branch, no PR was
open, and full Git object checking passed. Zero-run closeout PR #73 exact head
`e1b07f781096370fa3b6f820bc80dc1d4c585279` changed only three `.project`
paths and had no run, check, review, comment, or thread. Squash
`9983e0da88b6aef999d26498cc6438f0b3c5927b` has sole parent the record
integration, tree `d76b9a348690d6a35af774755cdc4a836240069a` exactly equal to the
reviewed head, a valid GitHub signature, and standalone DCO trailer. It
allocated no `main` run. The closeout branch is deleted locally/remotely; clean
synchronized `main` is the sole branch, no PR, tag, or release is present, and
full Git object checking passes.

## M39 complete

M39 starts from exact clean synchronized M38 closeout commit
`185e206d6b9c1e97512e289bcba84701dc29c147`. It closes the existing gap between
remote tag existence and release identity. The standard-library verifier
requires strict bounded GitHub ref/tag documents, an exact annotated tag whose
signature GitHub reports as valid, matching local/GitHub tag and target commit,
an exact event checkout, and reachability from fetched `origin/main`. Success
emits only safe tag/object/commit/ref identities; signature and payload content
remain private. Structured failures cover malformed/duplicate/oversized input,
identity drift, unsigned/lightweight tags, detached checkout, missing Git state,
and non-main commits.

The existing tag workflow fetches full history/tags, reads the version, obtains
the two read-only GitHub API documents, materializes the verifier from fetched
`origin/main`, and runs it with setup Python before system-package installation,
dependency sync, tests, builds, M38 comparison, staging, attestation, or
publication. GitHub is the signature-verification authority; local Git checks
exact object, checkout, and ancestry identity without a signing-key trust store.
RFC-0022 rejects treating `gh release create --verify-tag` as a signature check
and records the absence of a signer/key allowlist. It also records that the
workflow cannot authenticate replacement of its own definition by an already-
authorized tag actor; tag and environment rules remain operational controls.

Focused behavior, adversarial, static, workflow, and YAML gates passed after one
strict-typing correction, one helper-specificity correction, and two findings-
first workflow trust corrections. Exact head
`f71d8ddbf816873cf9af8ea6538112ff0e75553e` passed hosted run `31264314307`
in exactly three allocations: Linux in 6m43s before macOS and Windows began,
then macOS in 2m33s and Windows in 3m30s. The Linux job passed the full quality,
graphics, sample, distribution, installed-wheel, release-candidate, and CPython
3.13/3.14 gates. No review, comment, or review thread was present.

PR #68 squash `4e30b4bf3b911270ab4e1bd117d49ca0d090a0a7` has sole parent exact M38
closeout, tree `e08a1956e1b6ec9005b1455c5020ee716f6fbdef` exactly equal to the
reviewed feature head, a valid GitHub signature, and a standalone DCO trailer.
No post-merge `main` run was allocated, and the feature branch is deleted
locally and remotely. Public integration-record PR #69 changed exactly four
Markdown paths. Run `31265044941` classified them as documentation and allocated
only Linux job `93121720961`, which passed in 33 seconds; desktop umbrella
`93121781802` skipped with no runner steps. No review, comment, or review thread
was present. Record squash `166dcb2dc619dbc721207eece273c0fd9437f9ff` has sole
parent the implementation squash, tree
`1071165a0bf41397dfbeee38b09eee606299686e` exactly equal to the reviewed
record head, a valid GitHub signature, and a standalone DCO trailer. It
allocated no post-merge `main` run, and the record branch is deleted locally and
remotely.

M39 changes no CI workflow, runner/job/matrix count, action, permission,
trigger, dependency, lock, package version, runtime/public API, attestation,
tag, release, PyPI configuration, supported release policy, or deferred
subsystem. Zero-run closeout PR #70 changed only three `.project` paths, had no
run, review, comment, or thread, and squash-integrated exact head
`4d31f46008bf5efd7475a9b432226748e484d891` as
`49fba13477890bf6bf1c9e6a645e669b3a69492f`. The squash has sole parent the
record integration, tree `46df243de9b6f9f773723412af2580fe8682f27a` exactly equal to the reviewed
head, a valid GitHub signature, and standalone DCO trailer. It allocated no
`main` run. The closeout branch is deleted locally/remotely; clean synchronized
`main` is the sole branch, no PR is open, and full Git object checking passes.

## M38 complete

M38 starts from exact clean synchronized M37 closeout commit
`3578da64b2686cd8d63340aeb1eed30f5c4cb761`. It adds a standard-library,
fail-closed comparison for two distinct wheel/sdist build directories and
wires one repeat build into each existing Linux pull-request and tag-release
distribution step. The verifier requires one matching pure wheel/source pair,
ordinary files, exact bytes, and deterministic JSON identities. Invalid entry
types, missing/extra artifacts, inconsistent or platform-specific names,
unreadable data, and byte divergence fail nonzero.

The existing same-source build probe produces exact matching wheel and sdist
bytes on Windows. Corrected focused tests cover valid output and adversarial
directory, name, artifact-set, byte, unreadable-directory, and symlink-cycle
cases. CI/release architecture tests preserve the M37 two-job/three-allocation
pull-request topology, one-job tag workflow, exact action pins, existing
permissions, and triggers. RFC-0021 and public release/architecture
documentation define the narrow same-source/same-job guarantee.

PR #65 review identified that `Path.resolve(strict=True)` raises
`RuntimeError`, rather than `OSError`, for a symlink loop. DCO-signed correction
`4f3db7446c842df4f36d7cc8f8321a89bbe5997f` returns the promised structured
invalid-directory failure and adds a capability-aware regression. Replacement
run `31261807768` passed exact corrected head in exactly three allocations:
Linux in 6m50s, macOS in 1m59s, and Windows in 3m44s. Linux passed before either
desktop allocation began. Its same-source rebuild comparison reported a
266,797-byte wheel at SHA-256
`6c43bb79ed5de115ee645f1c8a9b4e8338f364c5bb1f53e08cde58e82e9afe06`
and an 892,185-byte sdist at SHA-256
`8f21585819f76f289887a6194e44bcf06b72497d70d13451326cc778e48e4f8a`.
All expected steps passed; the sole review thread is resolved and outdated.

PR #65 squash `9f6ca61ccb1f9b7e0796e5cc60c7dd38e6af99d7` has sole parent exact M37
closeout, tree `1a96d02b8b23410732fc7ac746179459a14d3f44` exactly equal to the reviewed
feature head, a valid GitHub signature, and a parsed DCO trailer. The feature
branch is deleted locally and remotely, synchronized main contains the squash,
and no post-merge main run was allocated.

Public record PR #66 changed exactly four Markdown paths. Its exact committed
classifier result was `classification=documentation`, `substantive=false`, and
`changed_count=4`. Hosted run `31262609814` allocated only Linux, which passed
the complete bounded documentation gate in 32 seconds. GitHub skipped the
desktop matrix before expansion in zero seconds; its umbrella check had no
runner steps. Record squash `42046d521242147cc5ed56874238d25de9870316`
has exact sole parent the feature squash, tree
`0776afee4c20884240cd4828095ac3b03ae46423` exactly equal to the reviewed
record head, a valid GitHub signature, and a parsed DCO trailer. PR #66 had no
comment, review, or review thread. The record branch is deleted locally and
remotely, synchronized main contains both M38 squashes, and no post-merge main
run was allocated.

M38 changes no runtime, public API, dependency, lock, version, supported
platform/Python contract, attestation action/permission, tag, publication, or
deferred subsystem. Its guarantee remains same-source/same-job byte equality,
not cross-platform, hermetic, independent-rebuilder, provenance, certification,
or publication evidence.

## M37 complete

M37 starts from exact clean synchronized M36 integration-record commit
`46ef98447706c94763a236841a38c2dbb5b444ca`. Its bounded outcome is fail-closed
change qualification inside the existing Linux CI allocation. A classifier
loaded from the exact base revision admits only a narrow documentation/community
path set; empty, mixed, ambiguous, invalid, unknown, or indeterminate input is
substantive or blocks the Linux gate. Documentation-only work retains one Linux
lock/static/docs/architecture/build/wheel/release allocation. Substantive work
retains all eight M36 slices and three allocations, with Windows/macOS gated on
successful Linux `substantive=true` output.

RFC-0020 and the public architecture, maintenance, roadmap, changelog, and
README contracts describe the policy and tradeoff. Findings-first review
closed one valid executable-documentation bypass by restricting `docs/` and
`.project/` to Markdown and making `mkdocs.yml` substantive. PR #62 review then
identified that the pull-request-template allowlist used the wrong filename
case; signed correction `8214227c99831310546147977bf354b5ae956bce` aligned it
with the tracked lowercase path and updated the regression fixture. The only
review thread is outdated and resolved.

Corrected substantive run `31259200818` passed exact head
`8214227c99831310546147977bf354b5ae956bce` in three allocations. Linux passed
all qualification, quality, compatibility, graphics, vertical-slice, and
distribution steps in 6m48s; only then did Windows and macOS start, passing in
3m40s and 2m45s. Feature squash
`407226beae36182d237e32866a86ce19bb93c691` has the exact reviewed tree, exact
M36-record parent, a valid GitHub signature, and a parsed DCO trailer. PR #62
and its feature branch are closed/deleted, synchronized main contains the
feature squash, and no main-branch run was allocated.

Public record PR #63 changed exactly four admitted Markdown paths. Its exact
committed classifier result was `classification=documentation`,
`substantive=false`, and `changed_count=4`. Hosted run `31259908552` allocated
only Linux, which passed the complete bounded documentation gate in 32 seconds.
GitHub evaluated the desktop job condition before matrix expansion and emitted
one skipped matrix-umbrella check with no steps and no Windows/macOS runner
allocation. Record squash `7434f310c86dd9acf6c61ff01c1a5f2dfcdffe31`
has exact reviewed tree `9dc7f0bc50b7b5b8309405ce491978f3ef39cbe4`, sole feature-squash parent, a
valid GitHub signature, and a parsed DCO trailer. The PR and branch are deleted,
main is synchronized, and no main-branch run was allocated.

M37 changes no runtime, test behavior, dependency, lock, package version,
release workflow, supported platform/version, tag, publication, provider,
certification, or support policy.

## M36 complete

M36 starts from exact clean synchronized M35 integration-record commit
`ba9125389ab2b2b760ca7115b5b1b03c447f4190`. It changes CI orchestration only:
the same eight validation slices move from eight runner allocations to three
OS-owned allocations. One Ubuntu runner owns CPython 3.12 quality,
distribution, base/graphics profiling, real graphics, and the sequential 3.13/
3.14 compatibility slices. A two-entry desktop matrix gives Windows and macOS
one runner each for 3.12 graphics followed by 3.14 compatibility.

The structural target is five fewer runner allocations and five fewer repeated
checkout/setup sequences, not removal of coverage. PR-only and `.project/**`
filters, least privilege, disabled credential persistence, exact pins, frozen
lock, caching, timeouts, desktop failure isolation, and superseded-run
cancellation remain. Runtime, tests, dependencies, lock, package version,
release workflow, public contracts, supported platforms/versions, tag,
publication, and support policy remain unchanged. Workflow implementation,
architecture regressions, RFC-0019, and documentation are integrated. Exact
sequential 3.13 and 3.14
transitions pass complete 1,714-test suites on Windows; restored 3.12 passes
1,724 tests. Static/docs/YAML, distribution, isolated wheel/release, real-
wgpu/profile, vertical-slice, and focused workflow/release gates pass.
Findings-first review moved compatibility-interpreter installation before
expensive work. Scope/security and final implementation-tree 1,724-test gates
pass; only factual `.project/**` rows followed.

Ready PR #60 used exact base
`ba9125389ab2b2b760ca7115b5b1b03c447f4190` and DCO-signed final head
`38589bbe6b4c688b581bc972f0ba1e4e39d5cd93`. Pull-request run `31232803658`
passed exactly three hosted allocations: Linux in 6m36s, Windows in 3m32s, and
macOS in 2m16s. Its step-level evidence covers every retained quality,
distribution, compatibility, real-graphics, profiling, and vertical-slice
gate. GitHub reported the PR mergeable and clean, with no comment, review, or
review thread. PR #60 squash-integrated the exact feature tree
`39d29fa863fee46665bf02856f4d9657068b573f` as GitHub-verified commit
`0b8b39052d79ee9c8a2f909f8ac70045adf5a785`, with sole parent exact base and a
valid DCO trailer. The feature branch is deleted locally and remotely. The
PR-only workflow scheduled no post-merge `main` run; the latest listed main run
remains pre-M34 run `31226750474`.

## M35 complete

M35 starts from exact clean synchronized M34 integration-record commit
`277de9052e768a5f70d32f1a2f67ec9f93353723`. Its bounded outcome is strict
offline admission readiness for the design plan's final ordered longer-term
metric: independently authored third-party adapters or plugin-backed adapters
passing existing installed conformance. The exact reviewed 250-byte manifest
has SHA-256
`adee8c68b5d89923ee2682162eb24cd9542a4601b1ff6fb901709ebcc0066767`,
explicitly asserts complete review of the project-accepted submission census,
and contains no submissions. The current passing count is therefore zero; no
global package census, ecosystem adoption, support matrix, security,
performance, provider certification, or release gate is claimed.

Future admission is limited to distinct independent external implementation
identities using the exact installed M17 render-device, M18 agent-tool, or M19
WorldStore baseline and fixed check count. Project-owned and maintainer-
authored implementations are excluded before outcome. A plugin-backed record
is possible only for the existing M12 `render.device` capability and requires
both compatible reviewed inert-manifest evidence and a passing installed
render-device result. Passed, failed, and not-executed submissions remain in
complete accepted history; only passes count. Public immutable wheels,
revisions, reports, reviews, supported CPython/platform evidence, and explicit
authorship/independence/license/eligibility/outcome/provenance/validation/
privacy/consent review are required.

The evaluator is an explicitly invoked bounded offline reader outside the
runtime package. It performs no discovery, import, install, provider execution,
network request, sandboxing, or telemetry and emits only sanitized aggregates.
M35 changes no runtime source, public API/export, protocol/profile, plugin
field, format, dependency, lock, version, CI topology, release workflow, tag,
publication, certification, or support policy. Implementation and focused
evaluator tests exist on `evidence/m35-third-party-conformance`. Findings-first
review hardened public evidence against reserved non-public domains and non-
wheel paths. The complete local gate passes 1,716 tests with nine skips, strict
static/docs checks, universal build, installed wheel/release smoke, real-wgpu/
profile and vertical-slice checks, and scope/security/artifact audits. Hosted
run `31231040437` passed all eight essential jobs on the initial head, but
automated review found that its generic identifier grammar disagreed with the
exact shared M17-M19 adapter grammar. The correction uses the installed runner
grammar for equal implementation/adapter identities; 100 focused tests, the
complete 1,718-test suite, strict static/docs gates, real-wgpu, rebuilt wheel,
isolated-wheel smoke, and fresh release smoke pass. Corrected hosted validation
run `31231410432` passed all eight essential jobs on exact final head
`fb0d887eed80a2d96c4b3348d950df371e58db56`. The correction evidence was
posted and the sole review thread resolved. PR #58 squash-integrated the exact
final tree as GitHub-verified commit
`603403967e333342c5ff72222ea3567d3252fd6f`, with sole parent exact base
`277de9052e768a5f70d32f1a2f67ec9f93353723`, tree
`59c049ebdb957818aba2252c74d5b5f8ef9cb72f`, and a valid standalone DCO
trailer. Local and remote feature branches are deleted. The PR-only workflow
created no post-merge `main` run; the latest listed main run remains pre-M34
run `31226750474`.

## M34 complete

M34 starts from exact clean synchronized M33 integration-record commit
`d12c30a02782c0ebf892e27c5daf6e9fec1c93ee`. Its bounded outcome is strict
offline admission readiness for the percentage of agent tool calls that
complete without manual recovery, plus the directly authorized elimination of
redundant CI runs. The reviewed 195-byte manifest contains no evaluation
windows and has SHA-256
`e952c045b039055e8439069cf88176b6ac1d2ad7de49a94d39b2737e5d06e1d5`, so
no call count, manual-recovery count, recovery-free completion rate,
reliability result, certification, or release gate is claimed.

Future admission requires every dispatched call from a complete reviewed
cohort of eligible task-directed sessions. It freezes the exact 12 product
tools and `ludoweave.agent.service/1`, immutable service/dispatch/result/
recovery evidence, sequential per-session indices, canonical order, complete
history, and explicit privacy/consent plus behavioral reviews. Known non-
completions and calls completed after
manual recovery remain in the denominator; `terminal-unobserved` remains
counted and blocks publication. Synthetic fixtures, conformance, tests,
benchmarks, maintainer-driven calls, and unreviewed/private sessions are
ineligible. Aggregate output omits raw sessions, tools, prompts, arguments,
results, errors, and evidence locations.

The eight existing CI jobs remain the substantive supported Python/OS/
graphics/distribution gate. M34 changes only their trigger: substantive pull
requests run the gate once; the same tree is not rerun after merging to
unprotected `main`, and `.project/**`-only factual record pull requests use no
hosted runner. Runtime, agent tools/protocols, public APIs, formats,
dependencies, lock, version, release workflow, providers, telemetry, and
native/WASM surfaces remain unchanged. Implementation, the 1,624-test complete
suite, strict static/docs gates, universal build, isolated wheel/release smoke,
real-wgpu/vertical-slice checks, scope/security audits, and findings-first
review pass on `evidence/m34-agent-tool-recovery`. Initial hosted run
`31228373123` failed one missing-manifest regression on Ubuntu and macOS because
the uncaught chained traceback disclosed the test path; the Windows
compatibility and all three graphics jobs passed. Delayed review also found
that sufficiently deep JSON could escape through `RecursionError`. The CLI now
prints only its sanitized outer error, and both parser and recursive depth-walk
exhaustion normalize to the documented validation error. Regressions cover no
traceback and excessive nesting. The corrected local gate passes 1,625 tests
with nine skips, strict static/docs checks, a universal build, isolated wheel
smoke, and a fresh ten-artifact release smoke. Corrected hosted run
`31229138742` passed all eight jobs on exact head
`600f71a416f0df46af68e63d28a2711893ec4675`: quality/tests/distribution;
Ubuntu CPython 3.13 and 3.14; Windows and macOS CPython 3.14; and real graphics
on Ubuntu, Windows, and macOS. The sole review finding was acknowledged and its
thread resolved; GitHub reported PR #56 mergeable and clean. PR #56
squash-integrated the exact validated tree as GitHub-verified commit
`a0d80851821b569156979d8d2ae0e473cea768f9` with sole parent exact base
`d12c30a02782c0ebf892e27c5daf6e9fec1c93ee`. Both source commits are
DCO-signed and remain attached to the PR. GitHub's squash body retained literal
escaped newline text before its displayed sign-off, so this record does not
claim the generated squash commit has a parsed DCO trailer and does not rewrite
public history. The remote and local feature branches are deleted. The new
PR-only trigger created no redundant post-merge `main` run; the latest listed
main run remains pre-M34 run `31226750474`.

## M33 complete

M33 starts from exact clean synchronized M32 integration-record commit
`60ddf57216d1054ac44df8d834756312c3864e3e`. Its bounded outcome is strict
offline admission readiness for benchmark-regression rate. The reviewed
manifest contains no evaluation windows, so no comparison count, regression
count, rate, zero-regression result, performance verdict, native decision, or
release gate is claimed. Future admission is restricted to registered M1-M4
`time.perf_counter_ns` p95 workload pairs on reviewed comparable controlled
runner profiles with distinct base/head revisions, exact sources/artifacts,
and predeclared integer tolerances. M7 cProfile output is diagnostic and
ineligible. Stable, regressed, and not-executed outcomes are preserved;
non-execution blocks rate publication. No runtime/benchmark source, API,
protocol, format, dependency, lock, version, workflow, provider, telemetry, or
native/WASM boundary changes. The exact 199-byte manifest SHA-256 is
`720ae794e2a4ba76303196cd43d6ba0f3b21f81cffd4fa8584f526e2a0d48dca`.
Implementation, adversarial tests, distribution wiring, RFC-0016, and public
documentation exist on `evidence/m33-benchmark-regression-rate`. Complete local
static/docs/test/build/wheel/release/benchmark/profile/graphics validation and
findings-first review pass. Protected-surface, archive, credential-pattern,
neutral-metadata, and object-integrity audits pass. Ready PR #54 exact head
`3bd7e17eed26028592cb39d37e77e15c6f4371f1` passed all eight essential jobs in
hosted run `31225942698`; no comment, review, or review thread existed and
GitHub reported the PR mergeable/clean. PR #54 squash-integrated the exact
validated tree as GitHub-verified `main` commit
`0993c73b3290809ef4e0c36d64d39e5ee5891a9b` with sole parent exact M33 base
`60ddf57216d1054ac44df8d834756312c3864e3e` and DCO trailer. The feature branch
was deleted locally and remotely. Synchronized `main` remains at the verified
feature squash while this documentation-only `records/m33-integration` branch
and PR #55 await their own hosted gate. M33 feature work is complete; no
measured rate, release, publication, performance guarantee, or native-code
authorization is claimed.

## Current milestone

M32 is complete, hosted-validated, reviewed, squash-integrated, and cleaned up.
It started from exact clean synchronized verified `main` commit
`b4de1d115ddb620ecddccab84637c0e66cfad9fd`. Its bounded outcome is a strict
offline admission harness for the design plan's next longer-term metric:
replay-divergence rate in CI. The reviewed manifest contains no evaluation
windows, so no execution count, divergence count, rate, reliability result, or
release gate is claimed. A future admitted window requires a complete reviewed
public cohort of eligible CI replay executions started during a bounded
interval and preserves verified, diverged, and not-executed cases. Cancellation,
pre-replay failure, skips, and unavailable result evidence cannot disappear
from the cohort. Each execution binds canonical project workflow run/job
locations, exact head/workflow/case sources, UTC time, and frozen result
evidence. Verified outcomes require equal expected/actual hashes; divergences
require distinct hashes, first divergent tick, and the stable divergence code;
non-execution claims no replay hashes or tick. Public census and review
artifacts share one immutable project revision. Manual review owns cohort
completeness, eligibility, outcome, provenance, and validation. Only exact
reviewed whole-manifest identity and complete mandatory history expose admitted
counts; an exact numerator/denominator rate additionally requires a non-empty
cohort with no non-executed case. `ready` means reportable, not that any
threshold, quality target, release gate, reliability promise, SLA, or support
promise is met. M32 changes no runtime source, replay behavior, public API/
export, persistent format, protocol, operation, dependency, lock, package
version, stability label, workflow, CI topology, tag, release, publication,
certification, reliability target, SLA, or support policy. The manifest is
exactly 175 bytes with SHA-256
`cff8a32428ac8dcd18029be4f70e9d359b4c9d70fd411ffe2f36d35704d68aa7`.
The evaluator, exact validator, adversarial future/non-execution/history
regressions, source/wheel/release artifact wiring, RFC-0015, and public
documentation are complete. Findings-first review corrected noncanonical case-
source URL acceptance and fixed eligibility before outcomes to exclude
intentionally divergent negative fixtures and verification-disabled diagnostic
runs. The reviewed tree passes the unchanged 46-package lock, 255-file
formatting, Ruff, strict Pyright, strict docs, 1,498 tests with nine platform-
capability skips, pure build, isolated wheel/release smoke, ten real-wgpu tests,
and both graphics vertical slices. The 94-entry wheel remains universal pure
Python with no native/WASM file; the 44-entry sample bundle contains the exact
evaluator and manifest. Protected runtime/workflow/metadata/lock scope remains
unchanged. Ready PR #52 is published. Initial exact PR head
`7046e59eb4840e6df492c886ce78baf4ad51cd95` passed all eight hosted jobs, but
hosted review correctly found the evaluator required nonexistent diagnostic
`world.replay.divergence` instead of the runtime's `world.replay.diverged`.
Evaluator, fixture, docs, and an architecture regression are corrected. The
post-review gate passes 80 focused tests with one skip, 1,499 complete-suite
tests with nine skips, 255-file formatting, Ruff, strict Pyright, strict docs,
the unchanged lock, protected-surface and whitespace checks, pure build,
isolated-wheel smoke, and a fresh ten-artifact release smoke. Corrected hosted
head `f6f574c2e9b54341e77d1b9ba2d9268bffe5439a` passed all eight essential jobs
in run `31195402467`, and the sole hosted-review thread is resolved and
outdated. PR #52 squash-integrated exact tree
`e185e24861b74fe11325b7188026af29a9618926` as GitHub-verified commit
`36e8d9ed65a619569f3620b2431d977a1fb80a58` with sole parent
`b4de1d115ddb620ecddccab84637c0e66cfad9fd` and its DCO trailer. The temporary
feature branch is deleted locally and remotely. No benchmark was rerun because
M32 changes no runtime or performance path and defines no performance target.

M31 is complete, hosted-validated, reviewed, squash-integrated, and cleaned up.
It started from exact clean synchronized verified `main` commit
`22dc58df8b0c4d17c3619d83e37c6d0ee6184441`. Its bounded outcome is a strict
offline admission harness for the design plan's next longer-term metric:
issue-response and pull-request-review time. The reviewed manifest contains no
measurement windows, so no cohort, response/review count, latency aggregate,
responsiveness result, or SLA is claimed. A future admitted window requires a
complete reviewed public cohort of eligible external-human issues and pull
requests opened during a bounded interval, preserves both observed and pending
items, and binds first qualifying public human-maintainer actions to exact
resource/action locations, UTC timestamp/latency agreement, frozen source and
review identities, and reviewed eligibility, role, distinctness, provenance,
and validation. Public census and review artifacts must share one immutable
project revision. Only exact reviewed whole-manifest identity and complete
mandatory history expose aggregate eligible/observed/pending counts and
deterministic median/nearest-rank-p95 seconds. `ready` means reportable, not
that any threshold, quality target, release gate, SLA, or support promise is
met. M31 changes no runtime source, public API/export, persistent format,
protocol, operation, dependency, lock, package version, stability label,
workflow, CI topology, tag, release, publication, certification, SLA, or
support policy. The manifest is exactly 199 bytes with SHA-256
`bc40bbcc1636229fa2c78aed5f71854d1221fd3c0d33169edc1321dd07e69d4f`.
The evaluator, exact validator, adversarial future/pending/history regressions,
source/wheel/release artifact wiring, RFC-0014, and public documentation are
complete. The corrected focused evaluator gate passes 49 tests with one Windows
symlink-capability skip; the evaluator/artifact group passes 51 tests with the
same skip; and the corrected architecture/evaluator/artifact gate passes 62
tests with one skip and strict docs. The final complete gate passes the
unchanged lock/sync, 251-file formatting, Ruff, strict Pyright, strict docs,
1,435 tests with eight skips, pure build, isolated wheel/release smoke, ten
real-wgpu tests, and both graphics vertical slices. Protected runtime/workflow/
metadata/lock scope is unchanged; the unchanged 94-entry wheel has no native/
WASM file and the 42-entry sample bundle contains both exact M31 evidence
files. Findings-first local review found no issue. Ready PR #50's initial exact
head passed all eight hosted jobs in run `31189729885`, but the hosted review
correctly found that equality between the observation cutoff and the opening-
window close was admitted. The evaluator now requires a strictly later cutoff,
equality has an explicit regression, and the public admission text is aligned.
The post-review gate passes 60 focused tests with one skip, formatting, Ruff,
strict Pyright, strict docs, 1,435 complete-suite tests with eight skips, pure
build, installed-wheel smoke, and fresh ten-artifact release smoke. No
benchmark was run because M31 changes no runtime/performance path and defines
no timing target. Corrected exact head
`dd4058b71439b5bade9d091831ba5453a51db35c` passed all eight essential jobs in
run `31190559197`. The sole review thread is resolved and outdated, no
unresolved thread or top-level comment remains, and PR #50 was `MERGEABLE` and
`CLEAN`. PR #50 squash-integrated exact tree
`2ec80742556e62b34dc9275fd0b268a484e9eace` as GitHub-verified commit
`8adb8d46d0ce13ea3687856ae53e899e98dc42a6` with sole parent
`22dc58df8b0c4d17c3619d83e37c6d0ee6184441`. Literal tree comparison and object
integrity passed. The temporary feature branch is deleted locally and remotely;
no feature PR remains open. M0-M31 are complete; select the next bounded slice
from current authoritative project goals before changing runtime scope.

M30 is complete, hosted-validated, reviewed, and squash-integrated by PR #48 as
GitHub-verified `main` commit
`675713d15a20a38233b80580e5aa773dc7a8684c`. It started from exact clean
synchronized verified `main` commit
`c88b166a39a793c91741bfa762af5627a87c53b4`. Its bounded outcome is a strict
offline admission harness for the design plan's next longer-term metric:
installation success across the supported OS/CPython matrix. The reviewed
manifest contains zero records, so the successful-environment count remains
zero and the sanitized result is deterministically `not-ready`; source-checkout
CI, local builds, automation, downloads, and synthetic fixtures do not
establish clean installation of one immutable public release wheel. A future
true result requires the same canonical public pure-Python wheel to pass fresh
isolated installs on Ubuntu CPython 3.12/3.13/3.14 and macOS/Windows CPython
3.12/3.14, with no dependencies or native compiler, all four installed checks,
distinct log identities, canonical provenance, and reviewed validation. The
complete reviewed identity sequence must equal the executable mandatory
prefix. Candidate or history-incomplete manifests expose no record-derived
environment or release aggregates. M30 changes no runtime source, public
API/export, persistent format, protocol, dependency, lock, package version,
stability label, workflow, CI topology, tag, release, publication, or support
policy. The manifest is exactly 462 bytes with SHA-256
`7c05813a7304e8ff44a009ada37c8e60ff545baec633852fc332e46bdfe03c90`.
The evaluator, exact validator, initial fail-closed regressions, source/wheel/
release artifact wiring, RFC-0013, and public documentation are complete.
Findings-first review corrected the canonical GitHub asset download path,
required unique public validation-job locators, enforced canonical environment
order, and added real calendar validation. The corrected focused gate passes
56 evaluator/architecture/artifact tests with one Windows symlink-capability
skip. The final complete gate passes the unchanged lock/sync, 247-file
formatting, Ruff, strict Pyright, strict docs, 1,375 tests with seven skips,
pure build, isolated wheel/release smoke, ten real-wgpu tests, and both graphics
vertical slices. Protected runtime/workflow/metadata/lock scope is unchanged;
the 94-entry wheel has no native/WASM file and the 40-entry sample bundle
contains both exact M30 evidence files. No benchmark was run because M30
changes no runtime/performance path and makes no performance claim. Ready PR
#48 contained single DCO-signed feature commit
`576dd070b547bef853ee47ece4c928b4e9962a7d`; hosted run `31186083454` passed
all eight essential jobs on that exact head. The final GitHub audit found zero
reviews, zero review threads, and eight successful checks. PR #48
squash-integrated exact feature tree
`6c421ece852d822270f3de1e9ece9c7cc1568678` as verified commit
`675713d15a20a38233b80580e5aa773dc7a8684c` with sole parent
`c88b166a39a793c91741bfa762af5627a87c53b4`; the feature branch is deleted
locally and remotely.

M29 is complete, hosted-validated, and squash-integrated. It started from exact
clean synchronized verified `main` commit
`e4125bf31a751473d2af4fecc05a9744d551063c`. Its bounded outcome is a strict
offline admission harness for the design plan's next longer-term metric:
contributor retention rather than raw stars. The reviewed manifest contains
zero records, so retained-contributor and return-contribution counts remain
zero and the sanitized result is deterministically `not-ready`; maintainers,
non-human automation, CI, stars, forks, downloads, and synthetic fixtures do not
establish retention. A future true result requires the same independently
reviewed external human to complete a first and later return contribution with
distinct public issues and merged pull requests, exact Git and artifact
identities, canonical chronology, valid DCO, complete validation, reviewed
provenance, and explicit human review of identity, independence, same-person
continuity, chronology, and retention. The complete reviewed identity sequence
must equal the executable mandatory prefix. Candidate or history-incomplete
manifests expose no record-derived counts or scopes. M29 changes no runtime
source, public API/export, persistent format, protocol, dependency, lock,
package version, stability label, workflow, or CI topology. The manifest is
exactly 274 bytes with SHA-256
`61785ec165e9f9a7c1025c37f7b714d6fa42b2c7081145a0f843395a325b36ee`.
The evaluator, exact validator, initial fail-closed regressions, artifact
wiring, RFC-0012, and public documentation are complete. They are accompanied
by the user-authorized neutral
repository convention: maintenance guidance now lives in `MAINTAINERS.md`, and
current state, decisions, templates, and reproducible evidence live under
`.project/`. This path migration changes no authorship or historical fact.
Findings-first review
closed case-variant double counting, made popularity-field rejection explicit,
required ASCII canonical timestamps, and made excessive JSON nesting fail
closed. Ready PR #46's initial hosted run `31181308306` passed five essential
jobs but exposed one CPython 3.14 decoder-behavior assumption in all three
compatibility jobs. The corrected evaluator now applies an explicit,
parser-independent 16-level structural nesting limit while ignoring JSON
string contents and escapes. Focused CPython 3.12 and 3.14 suites each pass 56
tests with one Windows capability skip. Complete local CPython 3.12 and 3.14
suites pass 1,321 tests with six skips and 1,311 tests with seven skips,
respectively. The complete local gate also passes 243-file formatting, Ruff,
strict Pyright, strict docs, pure build, isolated wheel/release smoke, all retained
benchmark/profile validators, ten real-wgpu tests, and both graphics vertical
slices. Protected runtime/workflow/metadata/lock scope is unchanged; the
94-entry wheel has no native library and the 38-entry sample bundle contains
both exact M29 evidence files. Correction run `31183032073` passed all eight
essential jobs on DCO-signed head
`897a3db5b0901835c6929eda5f94ed1774afac16`. The final audit found no review
thread or actionable finding, and GitHub reported PR #46 `MERGEABLE` and
`CLEAN`. PR #46 squash-integrated the exact corrected tree as GitHub-verified
commit `fc969a981ecdbbf842477f46486e29277119e05b`; its sole parent is the
assigned base and its tree is
`d98c25f156aaeee863ff8dc88b00355daa921d2e`. The obsolete feature branch is
deleted locally and remotely.

M28 is complete, independently reviewed, hosted-validated, and squash-
integrated. It started from exact clean synchronized GitHub-verified `main` commit
`17401eb32be30862496bbe02366d886a60752fb3`. Its bounded outcome is a strict
offline admission harness for the design plan's longer-term metric counting
externally authored sample games. The reviewed manifest contains zero records,
so the current count remains zero and the sanitized result is deterministically
`not-ready`; project examples, maintainers, project-controlled automation, CI,
and synthetic fixtures do not establish adoption. A future true result requires manually
reviewed independent authorship, a public repository and immutable revision,
an installed-wheel 2D/layered-2D game, exact headless fixed-tick, typed command-
receipt, and verified-replay capability evidence, distinct source/execution/
review artifact identities, a validated outcome, and reviewed public licensing.
The complete reviewed identity sequence must equal the executable mandatory
prefix. M28 changes no runtime source, public API/export, persistent format,
protocol, dependency, lock, package version, stability label, workflow, or CI
topology. The initial baseline resolves the unchanged 46-package lock and
passes 94 related tests with two Windows symlink-capability skips. The reviewed
manifest is exactly 280 bytes with SHA-256
`ecdd0be75e42f047037c6799205786079274eb6d73d788f81e1061acc82008dd`.
The evaluator, exact validator, synthetic regressions, source/wheel/release
artifact paths, RFC-0011, and public documentation are complete. Findings-
first review added explicit independence/provenance/outcome attestations,
cross-role artifact and locator uniqueness, duplicate-field rejection,
resource bounds, and complete mandatory-prefix enforcement. Corrected focused
validation initially passed 56 tests with one Windows symlink-capability skip.
Ready PR #44 and run `31175906134` passed all eight unchanged essential jobs on
DCO-signed head `a1898a81218ae5674fd0347018c6062a5537f359`. Thread-aware
review then found two valid P2 issues: unreviewed manifests could publish
candidate game/author aggregates, and HTTPS evidence locators were not bound
to an immutable record identity. The corrected evaluator exposes aggregates
only after exact digest and complete-history admission and requires the
locator path to contain the revision or one source/execution/review digest.
Post-correction formatting, Ruff, strict Pyright, strict docs, 57 focused
tests with one skip, 1,265 full tests with five skips, pure build, isolated
wheel smoke, and fresh ten-artifact release smoke pass. Correction run
`31176729893` also passes all eight unchanged essential jobs on exact head
`36130c8a3d0923a7330ee2c9e287c11c2a52594c`. GitHub reports PR #44
`MERGEABLE` and `CLEAN`; both original P2 threads are outdated, and the final
thread-aware reread found no new finding. The factual `[skip ci]` final head
`c383a4f143fd8682059a89ff6b645104a6b4332d` created no third workflow run.
PR #44 squash-integrated that exact head as GitHub-verified commit
`90d58a4567e7c7eaff90a28a7c59f2453b6d4538`; both trees are
`2f5ebf96af70741deb8d2b7d18ffa6d84effc494`, its sole parent is the assigned
base, and the squash message retains DCO sign-off.

M27 is complete, reviewed, hosted-validated, and squash-integrated. It was
implemented on
`codex/m27-external-contributor-rehearsal-readiness` from exact clean
synchronized GitHub-verified `main` commit
`c1c3be08f7f75d90e7d1b517adbc30d56902ece4`. Its bounded outcome is a strict
offline admission harness for the design-plan objective that documentation
enable a first external contribution without private maintainer knowledge.
The reviewed manifest contains zero records, so the sanitized result is
deterministically `not-ready`; project documentation, hosted CI, maintainers,
non-human automation and synthetic fixtures do not establish an independent
human contribution rehearsal. A future true result requires at least one manually
reviewed human good-first contribution linked to a public project issue and
merged pull request, exact base/head/merge objects, patch/feedback hashes,
valid DCO, the clean/focused/complete validation sequence, and explicit review
that no private maintainer knowledge or protected API/format/dependency/workflow
change was involved. The complete reviewed identity sequence must equal the
executable mandatory prefix. M27 changes no runtime source, public API/export,
persistent format, protocol, dependency, lock, package version, stability
label, workflow, or CI topology. The manifest is exactly 270 bytes with
SHA-256 `ecb959e90a0033b4dbe3dcfe8a48db1c1eea915e0ef2840510969b9e25cdb9c7`.
The core focused suite passed 51 tests with one Windows symlink-capability skip
in 1.74 seconds; source/wheel/release artifact wiring then passed 53 tests with
one skip in 2.02 seconds, Ruff passed after import ordering was corrected, and
Pyright reported zero diagnostics. Findings-first review then closed cross-role
revision/artifact reuse and duplicate-JSON-field ambiguity; 59 corrected
focused tests pass with one skip. The complete local gate passes 235-file
formatting, Ruff, strict Pyright, strict docs, 1,210 tests with four Windows
symlink-capability skips, pure build, isolated wheel/release smoke, all retained
benchmark/profile validators, ten real-wgpu tests, and both graphics vertical
slices. Protected runtime/workflow/metadata/lock scope is unchanged; the
94-entry wheel has no native library and the 34-entry sample bundle contains
both M27 evidence files. Initial hosted run `31118834216` found that the M27
architecture test spelled the tracked lowercase pull-request template with an
uppercase filename; both Ubuntu compatibility jobs failed that same case-
sensitive lookup. The local correction uses the exact tracked path. Windows
graphics separately failed during GitHub action-download resolution before
checkout with `Service Unavailable`; macOS graphics passed. The already-failed
run was cancelled rather than spending its remaining queued jobs. Corrected
run `31119640551` first preserved three successful jobs while four jobs failed
before checkout and macOS graphics remained unassigned during GitHub's
subsequently resolved Actions outage. One failed-job-only rerun then executed
only the five affected jobs. The resulting effective eight-job matrix is fully
successful on exact corrected head
`f9e779d83a82795ad68cff22c424b6e94ef13703`: quality/distribution, Ubuntu
3.13/3.14, Windows 3.14, macOS 3.14, and graphics on Ubuntu, Windows, and
macOS all pass.

The final evidence commit used `[skip ci]` and created no additional workflow
run. The final thread-aware reread found one unresolved bot comment that
mistook GitHub's ephemeral PR test-merge commit for a branch commit; every
branch commit has the required DCO trailer, so the finding is not actionable
and was neither answered nor resolved. PR #42 squash-integrated exact final
evidence head `349dc3b78dcae2b1c725ed3dc8e5e646ca3d3ac1` as GitHub-verified
`main` commit `ff1c81f8aaa96245706586096f400a5fb03bdd04`. Both trees are
`f957c2e40eec5bd2d70cc274079ea334d6a34cc3`; the squash commit has exact
assigned base `c1c3be08f7f75d90e7d1b517adbc30d56902ece4` as its sole parent
and carries the DCO sign-off. The milestone branch remains the audit trail.

M26 is complete, reviewed, hosted-validated, and squash-integrated. It was
implemented on `codex/m26-supported-release-channel-readiness` from exact clean
synchronized `main` commit
`0de919a699dee6b10b6fef9ba2cdce5e3c0f2e62`. Its bounded outcome is a strict
offline admission harness for RFC-0003 gate 6. The current reviewed manifest is
empty, so the sanitized result is deterministically `not-ready`: the tag-only
prerelease workflow, local candidates, CI, and synthetic records do not establish
a supported deprecation-capable feature-release channel. A future gate requires
at least two reviewed supported non-yanked final releases on distinct feature
lines, exact publication identities, the one-feature-release deprecation window,
and append-only history. M26 changes no runtime source, public API/export,
protocol, dependency, lock, package version, stability label, release workflow,
or CI topology. The manifest is exactly 278 bytes with SHA-256
`f23b4314696384ad288b86c63bc101606f1aa9f323c4fb186486d8c74915ec41`;
findings-first review hardened exact project-tag URLs, final-release state, and
publication identity. The complete local gate passes 231-file formatting,
Ruff, strict Pyright, strict docs, 1,152 tests with three Windows symlink-
capability skips, pure build, isolated wheel/release smoke, all documented
benchmark/profile validators, 10 real-wgpu tests, and both graphics vertical
slices. The post-documentation full gate passes on the exact final local tree;
ready PR #40 targets the exact assigned base from DCO-signed implementation
commit `835ac2b2f3dd8bfe5a31fe9f880a43555e86fd34`. Initial hosted run
`31115252696` passes all eight unchanged essential jobs. GitHub reports the PR
`MERGEABLE` and `CLEAN`; the first thread-aware read found no comment, review,
or inline thread. Delayed review found one valid P2: a reviewed nonempty
manifest could be admitted without a matching complete mandatory prefix. The
local correction binds the reviewed digest to the entire prefix and passes
1,153 tests with the same three Windows capability skips plus complete
static/docs and isolated wheel/release validation. Corrected run `31116147333`
is successful across all eight checks after a failed-job-only rerun recovered a
GitHub action-download setup outage. Final thread-aware review finds the
original P2 outdated and no actionable finding. PR #40 squash-integrated exact
final evidence head `ac8dd43e6b93bc89af1f5dd1821948e4860ac88b` as GitHub-verified
`main` commit `a62d28e8c36d9a590e7ad7e7a9e8b49266dcbdde`; both trees are
`e1f39a9c5d2bc81f76b45288225b27a7c782bf50`, the squash commit has the exact
assigned base as its sole parent, and the milestone branch remains the audit
trail.

M25 is complete, reviewed, hosted-validated, and squash-integrated. It was
implemented on `codex/m25-external-consumer-feedback-readiness` from
exact clean synchronized `main` commit
`680e90dd8f9377fece23c43bd9f07ca9d76297de`. Its bounded outcome is a strict
offline admission harness for RFC-0003 gate 2. A record can count only after
manual review establishes an independent consumer and freezes a public HTTPS
repository, immutable revision, exact protocol set, bounded outcome, and exact
integration/feedback artifact identities. The evaluator verifies those frozen
facts but cannot establish independence itself. The reviewed manifest is empty,
so the current sanitized result is deterministically `not-ready` and makes no
external-adoption claim. M25 changes no runtime source, public API/export,
protocol, dependency, lock, package version, stability label, workflow, or CI
topology. The manifest is exactly 283 bytes with SHA-256
`b113444f60946461ec6774e2c278b9e82e7d80e08a37450b6cc153e5c5c1500e`;
focused formatting, Ruff, strict Pyright, report execution, and 29 tests pass.
Findings-first review corrected explicit-path symlink enforcement and rejected
credential-bearing, local-host, Unicode, and backslash HTTPS locators. The
final local gate passes 227-file formatting, Ruff, strict Pyright, strict docs,
1,109 tests with two Windows symlink-capability skips, pure build, isolated
wheel/release smoke, all documented benchmark/profile validators, 10 real-wgpu
tests, and both graphics vertical slices.
The DCO-signed implementation is published as ready PR #38 at exact head
`9667e020c2213d415072b7c7efbd880f6b58abfa` against assigned base
`680e90dd8f9377fece23c43bd9f07ca9d76297de`. Sole GitHub Actions run
`31111498136` passed all eight unchanged essential jobs. GitHub reports the PR
`MERGEABLE` and `CLEAN`; the first thread-aware read found no issue comment,
review, or inline review thread. Delayed automated review found one valid P2:
numeric loopback/private/link-local IP authorities could pass the future
locator syntax gate. The local correction requires a non-IP DNS-style
authority, adds exact loopback/link-local regressions, and passes 1,111 tests
with the two Windows capability skips plus the complete static/docs and
isolated wheel/release gate. DCO correction commit
`90ed57e360765cf7f2d0973e41b8f8ec06dc4b50` passed necessary GitHub Actions
run `31112342328` across all eight unchanged essential jobs. PR #38 is
`MERGEABLE` and `CLEAN`. The original thread remains unresolved and non-outdated
because its anchor persists, but the adjacent non-IP gate and exact loopback/
link-local regressions directly satisfy it; no finding remains actionable, and
no reply or manual resolution was performed. A final CI-skipping evidence
head `d0866967832fe80a49942184e1ab81d3c426a478` was squash-integrated by PR
#38 as GitHub-verified `main` commit
`9ec6eeaaed40fefeb64d738d4eaaf3f7a9c4009b`. Both trees are
`fcaa7b11a4aa8d1c87e57a810db16682cf9f00e6`; the squash commit's sole parent
is assigned base `680e90dd8f9377fece23c43bd9f07ca9d76297de`, and its message contains the
DCO sign-off. The milestone branch remains the audit trail.

M24 is complete, reviewed, hosted-validated, and squash-integrated. It was
implemented on `codex/m24-cross-version-corpus-readiness` from exact clean
synchronized `main` commit
`55c7a72337913303b6b1f6bd31edbca7ff28683b`. Its bounded outcome is a strict
offline admission harness over the immutable M21 receipt corpus. Gate 1 can
become true only when an installed reader differs from a preserved source
version, at least two versions are observed, every receipt remains canonically
readable, and supported-release records cover every observed version. The
current `0.1.0a1`/empty-release report is deterministically `not-ready` and
does not claim history. M24 changes no runtime source, API/export, protocol,
dependency, lock, package version, stability label, workflow, or CI topology.
The exact manifest/reader baseline passes 71 tests. The final reviewed gate
passes 223-file formatting, Ruff, strict Pyright, strict docs, 1,074 tests with
one existing Windows symlink skip, pure build, isolated wheel/release smoke, 10
real-wgpu tests, both graphics vertical slices, and base/graphics profile
contract smokes. Review hardened bounded streaming/path confinement, reviewed-
manifest identity, exact release coverage, and child/per-receipt resource caps;
26 focused post-hardening tests pass with no remaining finding. DCO-signed
implementation commit `e590d482246d122120c011969b47f79f9680efa2` is published
through ready PR #36. Sole GitHub Actions run `31107800179` passed all eight
unchanged essential jobs. GitHub reports the PR `MERGEABLE` and `CLEAN`; the
first thread-aware read found no comment, review, or inline thread. Delayed
automated review then found one valid P1: a newly pinned future corpus could
replace the current source list instead of retaining the M21 audit trail. The
local correction freezes executable mandatory source/release prefixes, adds an
explicit history-preservation gate and regression, and passes 28 focused tests,
1,076 full-suite tests with the existing skip, the complete static/docs gate,
pure build, isolated wheel smoke, and a fresh ten-artifact release smoke. DCO
correction commit `b393d6857f0a60c5d124fdeb25b3779c8f9dab86` passed necessary
GitHub Actions run `31108924069` across all eight unchanged essential jobs. PR
#36 is `MERGEABLE` and `CLEAN`. The original thread remains unresolved and non-
outdated because its loop anchor persists, but the adjacent frozen-prefix gate
and replacement-corpus regression directly satisfy it; no finding remains
actionable, and no reply or manual resolution was performed. CI-skipping final
evidence head `1a8bd6f19f656eb5c4a0d6bd90f057a69bddbc34` was squash-integrated
by PR #36 as GitHub-verified `main` commit
`b7b16697d28410567cbddf8eb962c7e6c9e664b8`. Both trees are
`fa3c455ccd9722c666cc07cae325f1b50e37ddc7`; the sole parent is assigned base
`55c7a72337913303b6b1f6bd31edbca7ff28683b`, and the commit contains the DCO
sign-off. The milestone branch remains the audit trail.

M23 is complete, reviewed, hosted-validated, and squash-integrated. It was
implemented on
`codex/m23-receipt-diagnostic-policy` from exact clean
synchronized `main` commit
`415859e19d9d29caa1168fabc96def509897b056`. Its bounded result is an exact
machine-readable receipt-v1 semantic-diff and diagnostic-code evolution policy,
deterministic installed evidence, RFC-0006, and RFC-0003 schema `/4`
bookkeeping. It changes no runtime package, public API, receipt field, operation,
diagnostic behavior, dependency, lock, version, or CI topology. The complete
local gate passes lock/sync,
219-file formatting, Ruff, strict Pyright,
1,048 tests with one existing Windows symlink skip, strict docs, pure build,
isolated wheel/release smoke, 10 real-wgpu tests, both graphics vertical slices,
and every documented M1-M4/M7 benchmark/profile validator. M1 simulation and
both M3 timing targets remain observed misses rather than pass claims.
The optional `.agents` task/ledger files expected by the review role
are absent, so the authoritative `.ai` task, accepted RFCs, AGENTS boundary,
call sites, tests, and executed evidence were used as the review baseline.
DCO-signed implementation commit
`a6dc30ec62d91b1f6640db2c23797967f2aefefe` is published through ready PR
#34. GitHub Actions run `31104052702` passed all eight unchanged essential jobs.
Delayed automated review produced two valid P1 findings: diagnostic identities
were not bound to exact meanings, and the installed evidence did not compare
every generated diff value and declared order. The local correction now freezes
all six code/meaning/scenario triples and an exact full complex-diff oracle. It
passes 20 focused tests, 1,050 full-suite tests with one existing skip, static
and strict-doc gates, pure build, isolated wheel smoke, and a fresh 10-artifact
release smoke. DCO-signed correction commit
`4eb61cd49542b0a4753629f31ebe80229c7d45b8` is published, and follow-up
GitHub Actions run `31105197045` passed all eight unchanged essential jobs.
Thread-aware reread shows both original discussions still unresolved and
non-outdated because their anchors remain in the diff; current adjacent code
directly supplies the requested definitions and full-diff assertion, so no
finding remains actionable. No reply or manual resolution was performed. Final
`[skip ci]` evidence head
`eacb0153d8ac6e5f65d4d52f02c493bf9a891219` was squash-integrated by PR
#34 as GitHub-verified `main` commit
`2f7152565d369225dbf69055b7d42a4c80f46d1a`. Both trees are
`6ba709c29688041992bef75a2a83831275ff32db`; the sole parent is exact assigned
base `415859e19d9d29caa1168fabc96def509897b056`, and the commit contains the
DCO sign-off. The milestone branch remains the audit trail.

M22 is complete, reviewed, hosted-validated, and squash-integrated. It was
implemented on
`codex/m22-operation-argument-policy` from exact clean
synchronized `main` commit
`291dfb3fd6895a2fdac7a2f0016bb181f0e5bca4`. Its bounded result is an exact
machine-readable policy for all seven built-in operation-v1 argument shapes,
deterministic installed valid/missing/unknown-field evidence, RFC-0005, and
RFC-0003 gate bookkeeping. It changes no runtime package, public API,
operation, persistent format, dependency, lock, version, or CI topology.
DCO-signed implementation commit
`f1a89ad460467039f966ed37955144840cd96a12` is published through ready PR
#32. GitHub Actions run `31100821087` passed all eight unchanged essential
jobs. Automated review then requested an explicit defaulted-component-field
omission rule. The contract clarification, installed behavioral regression,
full local gate, wheel, and release smoke pass in DCO-signed correction commit
`cf3ae540e71cda128837ea698f5f175a7abf2fc4`. Follow-up GitHub Actions run
`31101607485` passed all eight unchanged essential jobs. Thread-aware review
now reports the sole review thread outdated and no actionable thread remains.
PR #32 squash-integrated exact final evidence head
`a5a49dcca277f28bb3e6097f37d5418d5d3c2c9d` into `main` as
GitHub-verified commit `8a4d288c4edf55d0299828b8edee1bd1885884d9`;
both trees are `f513bec716d1735cc47a6aab862bca0f5f770af9`, and the sole
parent is the assigned base. The milestone branch remains the audit trail.

M21 is complete, independently reviewed, hosted-validated, and squash-
integrated. It started on `codex/m21-receipt-reader-baseline` from exact clean
synchronized `main` commit `feed793e94c345fac4b146c358a68264ef6e5f62`.
Its bounded result is a public resource-limited reader for the unchanged
`ludoweave.receipt/1` graph plus exact single-version fixtures, installed
evidence, RFC-0004, and compatibility-gate bookkeeping. Implementation is
findings-first reviewed. Ready PR #30 published DCO-signed
implementation commit `cec339be07318a7c1586bb3405e8f9b1904859f5`; sole hosted
run `31098563810` passed all eight unchanged essential jobs. PR #30 squash-
integrated exact final evidence head `4e378756b2a1733de28e7160ac2d6d72921f3e4a`
as GitHub-verified `main` commit
`6bfb56555cafc93a7312f64465ea15cd7c450e79`; both trees are
`ea3f410fac31d7a32faee4e697c4fb0941b657df`.

M0 through M7 are complete, independently accepted, integrated into `main`,
and validated by hosted CI. M8 gamepad/SDL3 evaluation is complete,
independently accepted, published as PR #9 from
`codex/m8-gamepad-sdl3-evaluation`, and validated across all 14 hosted jobs.
M9 Box2D v3 plugin admission evaluation is locally complete on
`codex/m9-box2d-plugin-evaluation`, stacked from the exact M8 head. ADR-0024
defers the plugin; repeat independent review accepted the ownership correction
with no remaining blockers. It is published as ready stacked PR #10 and GitHub
Actions run `31015885190` passed all 14 hosted jobs.
M10's headless semantic inspector is complete, independently accepted, and
published as ready stacked PR #11 from `codex/m10-live-semantic-inspector`,
based on exact M9 final head
`22bc2de9f8450f60fe483bd4fea10a86702d2f0f`. ADR-0025 accepts one isolated,
owned local MCP child with detached observations and receipted writes. GitHub
Actions run `31020096463` passed all eight essential hosted jobs.
M11 is complete and independently accepted on
`codex/m11-rich-2d-modules`, based on exact M10
evidence head `bae799900671481cfd6f03fe502dea95b2c7f96c`. ADR-0026 bounds it
to dependency-free headless audio mixing, bitmap text, tick animation,
immutable tilemaps, and fixed-point particles through existing render records.
It is published as ready stacked PR #12; GitHub Actions run `31024155710`
passed all eight essential hosted jobs on signed implementation commit
`aca6d93165a52d88451e8e06d5f1aa8d2e323f1d`.
M12 is assigned on `codex/m12-plugin-manifest-compatibility`, based on exact
M11 evidence head `840a8b06d461fa1d5e649911b22f5995154728a7`. Its bounded contract is a
data-only preview plugin-manifest schema and deterministic compatibility
evaluator. RFC-0002 is accepted and implementation plus focused review
hardening are complete. Independent hostile review approved the corrected tree
with no remaining finding, and the complete local/artifact/provider gate
passed. It is published as ready stacked PR #13; GitHub Actions run
`31028863469` passed all eight essential hosted jobs on signed implementation
commit `e1f6e3cd8572d20a4f0a5c62a96b9aa52a986b38`.
M13 is complete and independently accepted on
`codex/m13-rollback-network-readiness`, based on exact
M12 hosted-evidence head
`7cb834c7b5e84e1b1a945905a68b947b3a4bdd3f`. Its bounded contract is an
offline Clockwork Arena correction-branch proof plus an evidence-based network
rollback admission decision. ADR-0027 defers networking/live rollback because
canonical tick input is not replay-owned and protocol, security, simulation,
resource, lifecycle, and maintenance gates remain incomplete. No runtime
package, persistent format, listener, transport, or dependency is added. The
final complete local/artifact/provider gate passes and independent review
reports no remaining finding. It is published as ready stacked PR #14; GitHub
Actions run `31031590206` passed all eight essential hosted jobs on signed
implementation commit `ba62b650191cfb982100692e7ec694da318956ae`.
M14 is complete and independently accepted on
`codex/m14-constrained-3d-decision`, based on exact M13
hosted-evidence head
`48f8f296113e3f2794bae7f4c67997d433e4dd36`. Its bounded contract is an
installed-surface audit and product-scope decision only. ADR-0028 retains
layered 2D and defers constrained 3D behind a complete product, engine-contract,
agent-semantic, headless-conformance, cross-platform, resource-budget,
lifecycle, and maintenance gate. Exact source, isolated-wheel, and release
bundle evidence confirms the current orthographic camera and canonical
layer/z ordering while every 3D admission gate remains false. The final local
gate reports 809 passes and one existing Windows symlink-capability skip;
independent hostile review reports no remaining finding. M14 changes no
runtime package, public Python API, persistent format, dependency, version, or
CI topology. GitHub Actions run `31033924254` passed all eight essential jobs
on signed implementation commit
`47443046834eb423be977973775f80494161533d`. M8-M14 were then
squash-integrated into `main` by PR #16 as verified commit
`2c62c8ed9c4ced6292260f6b8c84b1f069de1eaa`; its tree exactly matches final
M14 evidence head `02426805a11712030b3082ec349696d6d94aca50` at tree
`137a1870b0dd9034ad935b253a13186f6c7cc913`. Stacked PRs #9-#15 are closed as
superseded, with branches retained for audit history.

Repository-state evidence was then integrated through PR #18 as verified main
commit `bfea67d2d922e8c591224d18f56c14d572d7f7da`. M15 is locally complete and
independently accepted from that exact clean base on
`codex/m15-visual-editor-admission`. Its bounded contract is
an installed-surface product decision only: confirm the versioned
command/receipt, typed-tool, local MCP, and read-only inspector foundation;
retain the headless inspector; and defer visual-editor implementation until
the complete ADR-0029 compatibility, authoring, recovery, usability,
cross-platform packaging, resource-budget, and maintenance gate is satisfied.
The final local gate reports 834 passes and one existing Windows
symlink-capability skip, clean static/docs/build/artifact/provider checks, and
successful validation of every inherited documented benchmark/profile. No
GUI/TUI, runtime package, public API, persistent format, dependency, lock,
version, or CI change is introduced. It is published through ready PR #19;
GitHub Actions run `31036925179` passed all eight unchanged essential jobs on
DCO-signed implementation commit `7e85570056dde3678aaeee13eee4036067876d8c`.

PR #19 squash-integrated the exact final M15 tree into `main` as verified
commit `c013dad38b1b64f0f4ccddc19681d643f6414427`. M16 is assigned on
`codex/m16-wasm-mod-security-decision` from that exact clean base. Its bounded
contract is an executable-WASM-mod security admission decision only: preserve
the M12 data-only plugin boundary, document the prospective threat surface and
complete gate, and add deterministic source/wheel/release evidence plus
architecture guards. It does not add a runtime, loader, guest ABI, WASI, host
call, public API, persistent format, dependency, lock, version, or CI job.
The implementation is complete and independently accepted. The final
post-review gate reports 870 passes and one existing Windows symlink-capability
skip, clean static/docs/build/artifact/provider checks, and successful
validation of every inherited documented benchmark/profile. It is published
through ready PR #20; GitHub Actions run `31039403209` passed all eight
unchanged essential jobs on DCO-signed implementation commit
`bcaf78fbc78bda8a13a95e397ab15d003dd4a6ce`.
PR #20 then squash-integrated exact final M16 head
`808e48a5cb2727c8e1f4d7e896c4f8c7d41bfe1a` into `main` as GitHub-verified
commit `e2bd57c057c0c16861953c0702b2012c4cabfe90`. Both trees are
`05367be9bd85014fe6c70995ac1a69a39f90ef1e`; the milestone branch remains the
audit trail.

M16 integration evidence was then squash-integrated through PR #21 as verified
`main` commit `27d2ee9d1f7f75dacc17568650f00ce833ef4fce`. M17 is assigned on
`codex/m17-render-device-conformance` from that exact clean base. Its bounded
contract is one installed experimental `RenderDevice` baseline profile over an
explicit trusted factory. It adds sanitized versioned reports, Null/wgpu
evidence, artifact smoke, architecture guards, ADR-0031, and public guidance.
It adds no discovery, dynamic import, installation, provider adapter,
dependency, lock, version, canonical/persistent world format, or CI job. The
complete local quality/artifact/provider gate passes with 895 tests and one
existing symlink skip. Ready PR #22 targets `main` from DCO-signed
implementation commit `8e592f329424719214239bf97bd85dad9c9c5928`; GitHub
Actions run `31042903689` passed all eight unchanged essential jobs. PR #22
then squash-integrated exact final evidence head
`148600cdaf9c419fbf552c68f833e0d55655731f` into `main` as GitHub-verified
commit `610261c8450afc3d7db6ebb2b0425a1829737aec`; both trees are
`1e82568a463c62d0a1cf988b67eea09885ec50e3`, and the milestone branch is
retained.

M17 integration evidence was then squash-integrated through PR #23 as verified
`main` commit `ed65b12fa02f672113eac5939a0f616079fee44a`. M18 is assigned on
`codex/m18-agent-tool-conformance` from that exact clean base. Its bounded
contract is one installed experimental 12-tool agent-service profile over an
explicit trusted factory, with sanitized reports, source/wheel/release smoke,
architecture guards, ADR-0032, and public guidance. It adds no discovery,
dynamic import, installation, subprocess, network transport, provider,
dependency, lock, version, persistent format, canonical state, or CI job.
The final local gate passes, ready PR #24 targets `main` from DCO-signed
implementation commit `c4dde705393eebb7c99af428745e9383750f6b4d`, and GitHub
Actions run `31046172544` passed all eight unchanged essential jobs.
PR #24 then squash-integrated exact final evidence head
`cb617be0f678528fadc82877ec6910e42c6daf6b` into `main` as GitHub-verified
commit `1000d362432f19c912edf51c67e29c79bf444443`; both trees are
`1b6676ca7c1a6aaa223057a35e0c95242f4e9462`, and the milestone branch is
retained.

## Repository identity

M3 rendering is complete on `codex/m3-rendering-vertical-slice`, published as
stacked PR #3, and validated by corrected hosted run `30993554807` across the
14-job quality, CPython/OS, wheel, and graphics matrix. M4 is complete on
`codex/m4-clockwork-arena`, published as stacked PR #4, and validated by hosted
run `30996905660` across the same 14-job matrix.
M5 agent control is complete on `codex/m5-agent-control`, published as stacked
PR #5, and validated by hosted run `30999777517` across the same 14-job matrix.
M6 community-alpha hardening is complete on `codex/m6-release-hardening`,
published as stacked PR #6, and validated by hosted run `31002365370` across the
same 14-job matrix, including complete candidate smoke on all three platforms.
M7 performance/native decision is complete on
`codex/m7-performance-decision`, published as stacked PR #7, and validated by
hosted run `31005165849` across all 14 jobs, including the new base and
real-wgpu profiling-contract smokes.
The validated M1-M7 tree was squash-integrated to `main` by PR #8 as commit
`0237b2bfb11c6032d030dada639c7dbe439e5089`. The validated M8-M14 tree was
squash-integrated by PR #16 as commit
`2c62c8ed9c4ced6292260f6b8c84b1f069de1eaa`. The milestone branches and
hosted-run records remain the audit trail; superseded stacked PRs are closed.
Repository-state evidence is integrated by PR #18 as main commit
`bfea67d2d922e8c591224d18f56c14d572d7f7da`.

- Canonical repository: `xsparc/ludoweave-engine`.
- Package and CLI: `ludoweave`.
- Alpha candidate version: `0.1.0a1`.
- License and contribution model: Apache-2.0 with DCO sign-off.
- Supported baseline: standard CPython 3.12-3.14 on Windows, macOS, and Linux; no mandatory native compiler.

## Implemented

- Public README, governance, contribution, conduct, security, changelog, NOTICE, issue/PR templates, and agent guidance.
- PEP 621 pure-Python package, uv lockfile, Ruff, strict Pyright, pytest, Hypothesis, MkDocs Material, and typed-package marker.
- Immutable engine configuration and run summary; monotonic and deterministic virtual clocks.
- Explicit single-owner engine lifecycle with initialization, fixed-tick run, shutdown, failure cleanup, idempotent close, and structured exceptions.
- Engine-owned render protocol, backend-neutral descriptor, and lifecycle-validating null renderer.
- `ludoweave --version`, structured `ludoweave doctor`, and deterministic headless example.
- Architecture overview, runtime contract, accepted ADR-0001 through ADR-0007, and AST import rules that test absolute, relative, near-prefix, and reference-model independence constraints.
- Least-privilege GitHub Actions matrices for the supported operating systems/Python versions and installed-wheel smoke tests.
- Immutable two-field entity IDs, deterministic generational allocation, structured stale-handle failures, and installed-wheel ECS smoke coverage.
- Explicit component UUIDs, frozen schemas, immutable UUID-sorted registries, scalar validation metadata, and complete adjacent forward migration chains.
- Storage-neutral `WorldStore`, canonical `World`, private pure-Python dense/sparse component tables, deterministic inspection, change epochs, and independent in-memory cloning.
- Deliberately simple dictionary `ReferenceWorld` with separately implemented allocation, value, epoch, patch, and clone logic, exercised as a Hypothesis state-machine oracle.
- Structured duplicate/missing/malformed-value failures, copy-in/copy-out ownership, generation-safe swap removal, and installed-wheel world lifecycle coverage.
- Storage-neutral typed query builders with include/exclude/changed filters, opt-in stable ordering, detached row values, explicit writable cursor ownership, row-atomic validated writeback, and private structurally invalidated plan caching.
- World-bound reusable `Commands` buffers with copy-on-enqueue values, identity-only deferred entity tokens, clone-staged atomic flush, deterministic direct-operation epochs, retry/clear failure behavior, and local non-receipt `FlushResult` values.
- Production/reference query and flush conformance, extended Hypothesis state-machine coverage, exact reference-import whitelisting, and installed-wheel query/command smoke coverage.
- Explicit identity-owned typed resource keys, immutable registries, copy-owned singleton stores with a trusted read-only-input adapter contract, exact generic return typing, and structured copy failures.
- Immutable module-level Python system declarations, fixed simulation phases, component/resource access metadata, deterministic-eligibility gates, same-phase conflict ambiguity rejection, canonical cycle diagnostics, and input-order-independent serial schedule planning.
- ADR-0006 documentation, generated DAG/property coverage, D0 component rejection in deterministic plans, and installed-wheel resource/scheduler smoke coverage.
- Exact integer-unit fixed-step accumulation, retained catch-up backlog, absolute virtual deadlines, immutable exact-value input snapshots, virtual/recorded input sources, and application-owned input publication.
- Declaration-enforcing invocation contexts, canonical schedule revalidation, serial PRE/SIMULATE/flush/POST execution, structured failure attribution, BaseException-safe cleanup, and an additive installed-wheel fixed-step example.
- Versioned M1 benchmark tooling for seven workloads with raw samples, nearest-rank p50/p95/p99, sanitized CPython/GIL/environment/commit metadata, exact artifact validation, and tamper regressions.
- Bounded canonical JSON with exact finite-float tags, duplicate/Unicode/size validation, immutable command/transaction envelopes, and an explicit versioned operation registry with a compatibility fingerprint.
- Single-owner authoritative world sessions, complete allocator/epoch logical images, explicit persistent resource schemas/codecs, SHA-256 state hashes, clone-staged entity/component/resource/tick transactions, optimistic pre-hash checks, dry-run, deterministic limits, and atomic pointer-swap adoption.
- Canonical committed/dry-run/rejected transaction receipts with sanitized diagnostics, command outcomes, exact alias resolutions, and independent semantic diffs covering net entity/component/resource changes plus allocator, epoch, and tick behavior.
- Canonical complete-authority snapshots with SHA-256 verification, bounded atomic restore, registered component/resource migrations, allocator/epoch preservation, and independently named deterministic PCG32 random streams.
- Self-contained canonical replay timelines with compatibility headers, exact transaction/tick/hash batches, verified checkpoints, one-tick branch boundaries, and immutable parent-referenced branches.
- Data-only project composition plus project-confined `apply`, `snapshot`, `replay`, and `diff` CLI workflows with project-bound snapshots, handle-bounded input, and atomic output replacement.
- Informational M2 benchmark/validator tooling for canonical transactions, atomic application, snapshot round trips, and replay verification.
- Frozen backend-neutral render descriptors, explicit target/camera command lists, scoped generational resource handles, deterministic presentation extraction, and graph dependency/lifetime validation.
- A validation-only `NullRenderDevice` with fence-deferred physical reuse and an optional exact wgpu/rendercanvas/GLFW adapter isolated from package roots and canonical world state.
- An installed experimental `RenderDevice` baseline conformance profile that
  exercises explicit trusted factories and emits deterministic sanitized
  evidence without discovery, loading, installation, or provider admission.
- Instanced atlas sprites, translated/zoomed/rotated orthographic cameras, stable layer/z/entity ordering, tile batches, debug lines, built-in diagnostic glyphs, resize/minimize behavior, immutable offscreen RGBA capture, and typed device-loss diagnostics.
- M3 renderer benchmark/validator tooling for 1k/10k extraction, Null submission, and wgpu CPU submission with raw p50/p95/p99 evidence and exact draw counts.
- Frozen provider-neutral platform events, immutable action snapshots with transition metadata, deterministic recorded input, and isolated render-surface event draining.
- Strict project-root-confined asset manifests, transitive content-addressed cache keys, bounded pure-Python PNG decoding, and explicitly retired immutable texture revisions.
- Deterministic AABB/circle overlap, stable exact-filter spatial grids, bounded axis-ordered kinematic movement, and a minimal engine-owned null audio backend.
- Clockwork Arena canonical world/resource gameplay, fixed-seed waves, projectiles, collision, score/restart behavior, immutable presentation extraction, and deterministic headless/offscreen/window examples.
- Exact 3,600-tick Clockwork Arena fixture and independently recorded-input replay hash, plus M4 benchmark/validator tooling for baseline and informational stress workloads.
- Transport-independent typed agent command/query service with 12 immutable tool schemas over canonical transactions, receipts, snapshots, diffs, replay, capture, telemetry, and registered tests.
- An installed experimental 12-tool agent-service baseline conformance profile
  that exercises explicit trusted factories and emits deterministic sanitized
  evidence without discovery, loading, installation, transport selection, or
  provider admission.
- An installed experimental `WorldStore` baseline conformance profile that
  exercises explicit trusted `factory(ComponentRegistry)` implementations and
  emits deterministic sanitized evidence without discovery, concrete storage,
  persistence, external-resource lifecycle, or provider admission.
- Default read-only capabilities, explicit write/capture/test grants, bounded requests/results/work, monotonic rate limiting, caller binding, recursive credential redaction, and non-blocking single-thread mutation safe points.
- Project-confined `ludoweave agent` composition and local-only stdio MCP `2025-11-25` initialization, discovery, and tool calls without networking, shell access, arbitrary evaluation, dynamic project imports, or a new runtime dependency.
- Agent World Builder acceptance composition with six typed ECS entities, real offscreen wgpu capture, exact query/adjust/diff/test/telemetry/replay coverage, and installed-wheel execution.
- Deterministic community-alpha release staging with a pure wheel, sdist, fixed-timestamp sample bundle, SHA-256 inventory, versioned manifest, SPDX 2.3 SBOM, and notice set.
- Isolated release smoke that validates exact checksum coverage, SBOM/wheel identity, safe ZIP members, installed CLI/doctor, and bundled headless M0-M5 scenarios before success.
- Explicit `__all__`/`__stability__` policy and architecture coverage for every
  supported Python export. Earlier `0.1.0a1` symbols remain experimental;
  `ludoweave.plugins` is the first preview surface with a documented
  deprecation promise.
- Pinned tag-only provenance/prerelease workflow plus one complete baseline
  release-candidate smoke, compatibility coverage for every supported Python
  version/OS, and real graphics smoke on all three operating systems.
- Community-alpha user, architecture, adapter, release, first-contribution, API, triage, release-note, roadmap, and retrospective material with declarative labels and issue-ready starter cards.
- Versioned M7 base/graphics `cProfile` tooling with exact workload invariants,
  sanitized module/function records, strict validation, and tamper regressions.
- Query metadata/signature traversal reductions mirrored independently in the
  production and reference worlds, validated presentation reconstruction, and
  fixed-record provider-neutral sprite packing.
- Accepted RFC-0001 and ADR-0022: no native kernel is admitted; measurable
  cross-platform, contiguous-buffer, GIL, owner, build, fuzz, fallback, and
  improvement gates govern any future proposal.
- Frozen standardized gamepad connection/button/axis records, bounded logical
  slots, normalized stick/trigger domains, and an engine-owned provider
  protocol implemented by Null and the optional render device.
- Gamepad action bindings with explicit analog scale/deadzone semantics,
  supported-control focus recovery, hotplug cleanup, stable GLFW polling, and
  installed-wheel/Clockwork Arena coverage without provider-object leakage.
- Accepted ADR-0023: the existing pinned GLFW adapter supplies M8 input while
  SDL3 is deferred until its Python binding, binary delivery, ownership,
  cross-platform conformance, and maintenance gates are satisfied.
- A bounded isolated Box2D-candidate probe with versioned sanitized JSON,
  exact single-thread fixed-step traces, repeated lifecycle churn, double
  destruction, strict workload bounds, and no LudoWeave/runtime import.
- Accepted ADR-0024: `box2d-python==0.1.2` is deferred after failing the complete
  CPython/platform wheel and stable-API gates and lacking sufficient
  ownership, GIL/thread, replay, adapter-conformance, and maintenance evidence.
- Architecture fixtures reject case-insensitive Box2D/native-binding imports
  from engine source; the base project metadata, uv lock, wheel, and runtime
  remain unchanged and pure Python.
- `ludoweave inspect` owns one isolated `python -I -m ludoweave mcp` child,
  defaults to read-only, emits bounded `ludoweave.inspector.event/1` semantic
  observations, and verifies MCP identity, typed tools, receipts, completed
  ticks, and exact snapshot/diff/world/query/telemetry hash continuity.
- Inspector sample bootstrap and ticks require explicit write capability and
  reuse existing versioned transaction/tick tools. Child commands, module
  shadowing, option injection, network listeners, remote attach, parallel
  authority, paths, environment values, process IDs, and provider objects are
  excluded and covered by adversarial tests.
- Pull-request CI is consolidated from 14 to eight essential jobs: one complete
  Ubuntu 3.12 quality/test/distribution gate, four compatibility jobs spanning
  CPython 3.13/3.14 and Windows/macOS, and three real cross-platform graphics
  jobs. Superseded runs remain cancelled.
- `ludoweave.presentation` frozen animation, bitmap-glyph, tilemap, and
  fixed-point particle records with exact-tick sampling, integer layout/culling,
  stable seeded stepping/digests, and existing render extraction.
- A bounded acyclic audio mix graph rooted at `master`, enforced by the
  lifecycle-validating Null backend with category and effective-gain checks.
- A dependency-free rich 2D showcase registered in source, isolated-wheel, and
  deterministic release sample-bundle validation paths.
- Accepted RFC-0002 plus strict canonical plugin manifests, frozen explicit
  compatibility contexts/reports, bounded dependency checks, a path-free local
  CLI check, and source/wheel/release example coverage. The package owns no
  discovery, import, execution, filesystem, networking, or mutable registry.
- Bounded M13 parent/correction replay evidence with exact parent lineage,
  repeatable divergent resimulation, explicit external input rehydration, a
  strict sanitized validator, and source/wheel/release-bundle composition.
- Accepted ADR-0027 deferring network rollback and remote authority until the
  complete canonical-input, protocol, security, cross-platform simulation,
  resource-budget, lifecycle, artifact, and maintenance gate is met.

## Next slice

- M0 through M32 are complete, hosted-validated, reviewed, and squash-
  integrated.
- Select the next bounded slice from current authoritative project goals; no
  subsequent milestone is assigned by this factual integration record.
- Actual cross-version package history, external consumer feedback, and a
  supported deprecation-capable feature-release channel remain absent. Do not
  promote the experimental command/receipt surface by inference.

## Validation state

- The exact M21 base resolves 46 locked packages. Its focused receipt,
  persistent-schema, canonical-JSON, API/import-boundary, and artifact baseline
  passes 138 tests in 1.70 seconds; its inherited full suite passes 972 tests
  with one existing Windows symlink-capability skip in 69.25 seconds. The final
  reviewed M21 gate passes 1,015 tests with the same single skip in 69.87
  seconds, 211-file formatting, zero Ruff/Pyright findings, strict docs, a pure
  94-entry wheel, isolated-wheel smoke, a fresh complete ten-artifact release
  smoke, 255 expanded receipt/transaction/agent/release/architecture tests, and
  ten real-wgpu tests. Every inherited benchmark/profile artifact validates;
  M1 simulation and both M3 targets remain observed misses and authorize no
  acceleration. Workflow, metadata, lock, version, and root exports are
  unchanged. Ready PR #30 is mergeable and clean after sole hosted run
  `31098563810` passed all eight essential jobs on the DCO-signed implementation
  commit. PR #30 squash-integrated the exact final branch tree as verified
  `main` commit `6bfb56555cafc93a7312f64465ea15cd7c450e79`.

- The exact M20 base resolves 46 locked packages. Its focused canonical
  command/transaction/receipt/agent/API baseline passes 91 tests in 1.52
  seconds, and its full suite passes 955 tests with the existing Windows
  symlink-capability skip in 72.22 seconds. The final M20 Windows/uv-managed
  CPython 3.12.13 gate passes 972 tests with that one skip in 73.99 seconds,
  205-file formatting, zero Ruff/Pyright findings, strict documentation, a pure
  94-entry wheel with no mandatory dependency or native/WASM file, isolated-
  wheel smoke, a fresh complete ten-artifact release smoke, 211 expanded
  focused passes, and ten real-wgpu passes. All inherited benchmark/profile
  artifacts validate; the M1 simulation and both M3 targets remain observed
  misses and authorize no acceleration. Review hardened forbidden-import
  prefix detection and reports no remaining finding. Workflows, runtime source,
  project metadata, lock, version, protocol, stability labels, and package-root
  exports are unchanged. Ready PR #28's sole hosted run `31095009029` passed
  all eight unchanged essential jobs. The exact final head is squash-integrated
  as verified `main` commit `d166ef86bf25526d9d7715f63263d3cac6db78d4`
  with matching tree `c3e2dc1224f530fb483d1b9684ff55329bf9557b`.
- The final hardened M19 local gate on Windows/uv-managed CPython 3.12.13
  reports 955 passing tests and one existing symlink-capability skip, 201
  formatted Python files, zero Ruff/Pyright findings, strict documentation, a
  pure 94-entry wheel with no mandatory dependency or native/WASM file,
  isolated-wheel smoke, fresh complete ten-artifact release smoke, 149 focused
  conformance/release/architecture passes, and ten real-wgpu passes. All
  inherited benchmark/profile artifacts validate; the existing M1 simulation
  and both M3 targets still miss and authorize no native work. Workflows,
  project metadata, lock, version, and package-root exports are unchanged.
- The final reviewed M18 local gate on Windows/uv-managed CPython 3.12.13
  reports 925 passing tests and one existing symlink-capability skip, 196
  formatted Python files, zero Ruff/Pyright findings, strict documentation, a
  pure 93-entry wheel with no mandatory dependency or native/WASM file,
  isolated-wheel smoke, fresh complete ten-artifact release smoke, 145 focused
  conformance/release/architecture passes, and ten real-wgpu integration
  passes. All inherited benchmark/profile artifacts validate; the existing M1
  simulation and both M3 targets still miss and authorize no native work.
- The final reviewed M16 local gate on Windows/uv-managed CPython 3.12.13
  reports 870 passing tests and one existing symlink-capability skip, 186
  formatted Python files, zero Ruff/Pyright findings, strict documentation, a
  pure 91-entry wheel with no mandatory dependency or native/WASM file,
  isolated-wheel smoke, and fresh complete ten-artifact release smoke.
- Nine real-wgpu integration tests and every inherited benchmark/profile
  artifact validator passed. Current M1 and M3 target misses remain recorded
  engineering evidence and do not authorize native or WASM acceleration.
  Repeat independent security review approved after exact distribution-
  requirement evidence, named/dynamic runtime guards, residual-risk ownership,
  and current-flow accuracy corrections, with no remaining finding.
- The final reviewed M13 local gate on Windows/uv-managed CPython 3.12.13
  reports 793 passing tests and one existing symlink-capability skip, 174
  formatted Python files, zero Ruff/Pyright findings, strict documentation, a
  pure 91-entry wheel with zero native files and no mandatory dependency,
  isolated-wheel smoke, and fresh complete ten-artifact release smoke.
- Nine real-wgpu integration tests, the versioned 120/60 correction proof,
  strict evidence validation, Clockwork Arena, Agent World Builder, alpha
  acceptance, rich-2D showcase, and plugin compatibility passed. Every
  inherited README benchmark/profile artifact validated; the existing M1 and
  M3 target misses remain recorded and do not authorize acceleration.
- Independent hostile review drove pre/post-open file bounds, canonical JSON,
  exact types/counts/checkpoints, direct-call work limits, closed import/member
  allowlists, and alias/tamper regressions. Final review ran 54 focused tests,
  the maximum 600/300 proof, strict docs/static/diff/secret checks, and reported
  no blocking or non-blocking finding.
- GitHub Actions run `31031590206` passed the unchanged essential eight-job
  topology on M13 implementation commit
  `ba62b650191cfb982100692e7ec694da318956ae`: the complete Ubuntu 3.12
  quality/test/distribution job, Ubuntu 3.13/3.14 plus Windows/macOS 3.14
  compatibility jobs, and real graphics jobs on Ubuntu, Windows, and macOS.
- The final reviewed M12 local gate on Windows/uv-managed CPython 3.12.13
  reports 741 passing tests and one existing symlink-capability skip, 170
  formatted Python files, zero Ruff/Pyright findings, strict documentation, a
  pure 91-entry wheel with four plugin-contract entries and zero native files,
  isolated-wheel smoke, and fresh complete ten-artifact release smoke.
- Nine real-wgpu integration tests, Null/wgpu Clockwork Arena, Agent World
  Builder, alpha acceptance, rich-2D showcase, and the canonical example plugin
  check passed. Every inherited README benchmark/profile artifact validated;
  the existing M1 simulation and M3 renderer target misses remain recorded and
  do not authorize native work.
- Independent hostile review drove boundedness, exact-type, canonical-report,
  sanitized-diagnostic, immutable-decision, import/global-state, I/O/eval, and
  CLI regressions. Final re-review ran 138 focused tests with clean static,
  docs, diff, and isolated CLI checks and reported no remaining finding.
- GitHub Actions run `31028863469` passed the unchanged essential eight-job
  topology on M12 implementation commit
  `e1f6e3cd8572d20a4f0a5c62a96b9aa52a986b38`: the complete Ubuntu 3.12
  quality/test/distribution job, Ubuntu 3.13/3.14 plus Windows/macOS 3.14
  compatibility jobs, and real graphics jobs on Ubuntu, Windows, and macOS.
- The final reviewed M11 local gate on Windows/uv-managed CPython 3.12.13
  reports 663 passing tests and one existing symlink-capability skip, 164
  formatted Python files, zero Ruff/Pyright findings, strict documentation,
  a pure 87-entry wheel with seven presentation entries and zero native files,
  isolated-wheel smoke, and complete ten-artifact release smoke.
- Nine real-wgpu integration tests, base/graphics one-repeat profiling-contract
  smokes, Clockwork Arena, Agent World Builder, alpha acceptance, and the
  repeatable rich-2D showcase passed. M11 defines no timing target and makes no
  performance claim.
- Independent review found exclusive tile-bound, pre-bound traversal, runtime
  parent-fader, bounded-sequence, particle-work/state, and generic-style issues
  during development. The corrected edge/work/iterator/gain regressions passed;
  final re-review ran 78 focused tests plus 58 architecture/API tests with clean
  Ruff/Pyright/provider/diff/credential checks and reported no remaining
  finding.
- GitHub Actions run `31024155710` passed the unchanged essential eight-job
  topology on M11 implementation commit
  `aca6d93165a52d88451e8e06d5f1aa8d2e323f1d`: the complete Ubuntu 3.12
  quality/test/distribution job, Ubuntu 3.13/3.14 plus Windows/macOS 3.14
  compatibility jobs, and real graphics jobs on Ubuntu, Windows, and macOS.
- The final reviewed M10 local gate on Windows/uv-managed CPython 3.12.13
  reports 642 passing tests and one existing symlink-capability skip, 154
  formatted Python files, zero Ruff/Pyright findings, strict documentation
  success, a pure 80-entry wheel with no native entries or mandatory runtime
  dependency, installed-wheel shadow-isolation smoke, and complete 10-artifact
  release smoke.
- Eight real wgpu/GLFW integration tests, base/graphics one-repeat profiling
  contract smokes, Clockwork Arena, Agent World Builder, and alpha acceptance
  passed. M10 defines no performance target and makes no timing claim.
- Independent review first blocked publication on child import shadowing,
  dash-prefixed project option injection, incomplete tick receipt validation,
  and unstructured stream failures. `-I`, option termination/binding, exact
  receipt/hash/tick validation, structured read errors, and adversarial source
  and installed-wheel regressions resolved all findings. Repeat review ran 81
  focused tests with clean Ruff/Pyright/diff checks and approved publication.
- The consolidated eight-job CI workflow parses and its architecture contract
  passes locally. Its exact baseline test command excludes the separately
  gated wgpu integration file and passed 634 tests with one skip; real provider
  execution remains confined to the three jobs that install platform runtime
  prerequisites. GitHub Actions run `31020096463` passed that exact topology on
  implementation commit `2e60b3f1c4884dba71df5f23b779bc49187d68c6`.
- The corrected M9 local gate on Windows/uv-managed CPython 3.12.13 reports 606 passing
  tests and one existing symlink-capability skip, 151 formatted Python files,
  zero Ruff/Pyright findings, strict documentation success, a 79-entry pure
  wheel with zero native entries, installed-wheel and complete 10-artifact
  release smoke, eight real wgpu integration passes, and successful Clockwork
  Arena, Agent World Builder, and alpha-acceptance executions.
- Isolated `box2d-python==0.1.2` probes on Windows CPython 3.12.13 and 3.13.13
  each created/stepped/destroyed 25 worlds, repeated their exact traces, and
  produced trace digest
  `c9e299e715c5f7a3654d7c5794d75347d765cc029b7991d4c8066dfaf7abdfc5`.
  CPython 3.14 resolution failed because the release has only `cp312` and
  `cp313` wheels. These are candidate-admission facts, not performance,
  cross-platform determinism, or runtime-support claims.
- Independent review initially blocked sign-off because the metadata version
  was not linked to the imported module. The corrected probe validates the
  resolved module against the distribution's installed-file inventory before
  import and again afterward. Repeat review ran 54 focused tests, Ruff,
  Pyright, diff checks, and a real CPython 3.12 probe, found no remaining
  blocker, and recommended final sign-off.
- GitHub Actions run `31015885190` passed all 14 M9 jobs for implementation
  commit `8b429aaf07684651f6d538419701c049ee55fc4f`: strict quality/docs; Ubuntu
  CPython 3.12/3.13/3.14; Windows and macOS CPython 3.12/3.14; complete
  installed release-candidate smoke on Ubuntu/Windows/macOS; and real graphics
  smoke on all three systems. PR #10 is open, ready, mergeable, and clean
  against the exact validated M8 head.
- A pre-review M8 gate completed on Windows with uv-managed CPython 3.12.13,
  but an independent review then found production focus propagation, GLFW
  error-disambiguation, and trigger-neutrality defects. Its 589-pass result is
  retained as historical evidence, not accepted as the final M8 gate.
- The corrected final M8 gate reports 594 passing tests and one existing
  Windows symlink-capability skip, 149 formatted Python files, zero
  Ruff/Pyright findings, strict documentation success, a 79-entry pure wheel
  with zero native entries, installed-wheel and complete release-candidate
  smoke, eight real wgpu/GLFW integration passes, and successful Clockwork
  Arena, Agent World Builder, and alpha-acceptance executions. Repeat
  independent review found no blocking findings and recommended PR
  publication. M8 adds no dependency or benchmark; no timing result is
  claimed.
- GitHub Actions run `31012696753` passed all 14 M8 jobs: strict quality/docs;
  Ubuntu CPython 3.12/3.13/3.14; Windows and macOS CPython 3.12/3.14;
  installed-wheel smoke on Ubuntu, Windows, and macOS; and real graphics/GLFW
  gamepad smoke on all three operating systems.
- The complete M1 final local suite reports 303 passing tests, zero Ruff/Pyright findings, a strict documentation build, successful sdist/wheel build, and successful isolated installed-wheel smoke covering both M0 and M1 examples.
- The final 30-sample Windows/CPython 3.12.13 GIL-build benchmark artifact validates all seven versioned workloads. The 3,600-tick headless p95 was 26.8523 ms and observed the local 5×-real-time target. The representative 10,000-entity simulation-tick p95 was 196.8800 ms and did not observe the 4 ms engineering target. These are local observations, not cross-platform claims.
- GitHub Actions run `30936533105` passed quality/documentation, Ubuntu Python 3.12/3.13/3.14, Windows Python 3.12/3.14, macOS Python 3.12/3.14, and installed-wheel smoke on all three operating systems after correcting the invalid planned `actions/checkout` v6.0.2 SHA.
- MkDocs Material emits its upstream informational warning about the future MkDocs 2.0 project; the strict documentation build exits successfully.
- The final M2 local gate on Windows/uv-managed CPython 3.12.13 reports 444 passing tests and one Windows symlink-capability skip, zero Ruff/Pyright findings, strict documentation success, successful sdist/wheel build, and successful isolated installed-wheel workflow smoke.
- The final 30-sample M2 informational benchmark validated four workloads with no timing targets. Local p50/p95 durations were 30.2751/33.7076 ms for canonical 100-command round trips, 13.9896/16.9751 ms for atomic 100-command apply, 17.1209/18.0412 ms for 1,000-entity snapshot round trips, and 216.5521/271.2240 ms for verified 100-batch replay.
- Independent final M2 code/security and quality reviews found no remaining actionable findings and independently reproduced the 444-pass/one-skip suite.
- GitHub Actions run `30947073913` passed all 11 M2 jobs: quality/documentation; Ubuntu tests on Python 3.12/3.13/3.14; Windows and macOS tests on Python 3.12/3.14; and isolated installed-wheel smoke on Ubuntu, Windows, and macOS.
- The final local M3 graphics gate on Windows/uv-managed CPython 3.12.13 reports 485 passing tests and one Windows symlink-capability skip, zero Ruff/Pyright findings, strict documentation success, a pure wheel, and a successful no-dependency installed-wheel smoke. A separate frozen base sync removed all graphics packages and reported 479 passes with the symlink and graphics capability skips.
- The real Windows GLFW example and the offscreen clear/sprite/capture fixtures completed. The 30-sample M3 artifact validated six workloads with one draw each. Local 10k extraction/packing p50/p95/p99 was 35.4460/41.9722/51.8362 ms; wgpu CPU submission was 5.3753/6.5363/6.9215 ms. Neither observed the 3 ms starting target; no target pass is claimed.
- Initial M3 hosted run `30951328011` passed all base test and wheel jobs plus Windows/macOS graphics, but failed the quality type check because optional providers were not installed and failed Ubuntu graphics because no driver was present. The correction installs the exact graphics extra for quality and Mesa Vulkan only for the Ubuntu graphics job.
- Corrected GitHub Actions run `30993554807` passed all 14 jobs: strict quality/documentation; Ubuntu Python 3.12/3.13/3.14; Windows and macOS Python 3.12/3.14; isolated wheel smoke on all three operating systems; and real clear/sprite/capture/resize/loss graphics smoke on Ubuntu software Vulkan, Windows, and macOS.
- The final local M4 gate on Windows/uv-managed CPython 3.12.13 reports 516 passing tests and one existing Windows symlink-capability skip, zero Ruff/Pyright findings, strict documentation success, a pure wheel, successful no-dependency installed-wheel smoke, real offscreen and GLFW Clockwork Arena runs, exact 3,600-tick deterministic fixture/replay agreement, and a valid 300-sample three-workload benchmark artifact.
- The local baseline Clockwork Arena benchmark p50/p95/p99 was 1.5228/2.1228/2.5898 ms and observed its 16.666667 ms p95 target. Stress 4 and 8 p95 values were 3.5029 ms and 4.8371 ms and have no assigned target. These are local observations, not cross-platform claims.
- GitHub Actions run `30996905660` passed all 14 M4 jobs: strict quality/documentation; Ubuntu Python 3.12/3.13/3.14; Windows and macOS Python 3.12/3.14; isolated wheel smoke on all three operating systems; and real graphics smoke, including Clockwork Arena wgpu execution, on Ubuntu software Vulkan, Windows, and macOS.
- The final local M5 gate on Windows/uv-managed CPython 3.12.13 reports 545 passing tests and one existing Windows symlink-capability skip, zero Ruff/Pyright findings, strict documentation success, a pure wheel, successful no-dependency installed-wheel smoke, and a real offscreen wgpu Agent World Builder run.
- Direct Python, the actual `ludoweave agent` subprocess, and MCP return equivalent canonical transaction results/receipts. MCP lifecycle, malformed input, duplicate IDs/keys, capability denial, limits, atomic stale-hash rejection, reentrant/wrong-thread mutation rejection, redaction, provider close, and architecture bans are covered.
- GitHub Actions run `30999777517` passed all 14 M5 jobs: strict quality/documentation; Ubuntu Python 3.12/3.13/3.14; Windows and macOS Python 3.12/3.14; isolated wheel smoke on all three operating systems; and real graphics smoke, including the Agent World Builder typed-tool loop, on Ubuntu software Vulkan, Windows, and macOS.
- The final local M6 gate on Windows/uv-managed CPython 3.12.13 reports 552 passing tests and one existing Windows symlink-capability skip, 143 formatted Python files, zero Ruff/Pyright findings, strict documentation success, a pure `0.1.0a1` wheel, successful no-dependency installed-wheel smoke, and a complete 10-file staged candidate whose checksum/manifest/SBOM/sample smoke passed.
- M6 changes release/community surfaces rather than simulation performance. No new benchmark or performance pass is claimed; inherited M1/M3 misses and M4 observation remain unchanged.
- GitHub Actions run `31002365370` passed all 14 M6 jobs: strict quality/documentation; Ubuntu Python 3.12/3.13/3.14; Windows and macOS Python 3.12/3.14; complete installed release-candidate smoke on all three operating systems; and real graphics smoke, including Clockwork Arena and Agent World Builder, on Ubuntu software Vulkan, Windows, and macOS.
- The final local M7 gate on Windows/uv-managed CPython 3.12.13 reports 564
  passing tests and one existing Windows symlink-capability skip, 148 formatted
  Python files, zero Ruff/Pyright findings, strict documentation success, a
  pure wheel/sdist, successful no-dependency wheel smoke, complete 10-file
  release smoke, six real wgpu integration passes, and successful wgpu sample
  compositions.
- Final valid 30-sample M7 observations are 130.1806/144.0474/150.6699 ms
  p50/p95/p99 for the 10,000-entity simulation tick, 20.8641/30.6902/31.4777 ms
  for 10,000-sprite extraction/packing, and 2.8678/5.1918/5.2584 ms for wgpu
  CPU submission. None observed its starting target; these are local, not
  cross-platform, timing claims.
- Five-repeat `ludoweave.profile.m7/1` base and graphics artifacts validate.
  Remaining simulation cost spans detached query copy/writeback; presentation
  cost spans immutable record construction; packing consumes Python objects
  even where it dominates submission. RFC-0001 therefore defers native code.
- GitHub Actions run `31005165849` passed all 14 M7 jobs: strict
  quality/documentation plus base profile validation; Ubuntu Python
  3.12/3.13/3.14; Windows and macOS Python 3.12/3.14; complete installed
  release-candidate smoke on Ubuntu/Windows/macOS; and real graphics plus wgpu
  profile smoke on all three operating systems. PR #7 is open, mergeable, and
  reports clean merge state against the validated M6 branch.

## External follow-ups

- Verify and reserve the `ludoweave` name before publishing to PyPI.
- Apply `.github/labels.yml` through GitHub settings and open the issue-ready
  starter cards when maintainers are ready to review community contributions.

## Deferred roadmap

Remote/network agent transport, real audio playback, Box2D/rigid-body physics,
networking, visual-editor implementation, automatic device recovery,
international text shaping, 3D, and
native acceleration remain unimplemented. RFC-0001 records that the improved
M1/M3 workloads still miss their targets and defines the complete quantified
admission gate before a native proposal may return.
