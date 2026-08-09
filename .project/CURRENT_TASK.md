# Current Task

- **Task:** M57 - public release response-body conformance
- **Status:** The feature is squash-integrated on `main`; preparing the
  four-file integration record on `docs/m57-integration-record`.
- **Started:** 2026-08-10
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact clean synchronized M56 closeout
  `187cbfb1c857e62594e49d1cf8e7591024aff8c9`, with only `main` present and no
  open pull request, tag, release, or post-closeout `main` run.
- **Outcome:** Validate each public-release response-body block and any declared
  body length before successful local publication or later document/artifact
  validation.
- **Acceptance:** Require every successful `HTTPResponse.read(amount)` result
  to be immutable bytes no larger than the requested amount before EOF
  interpretation, byte accounting, or local output. If M55 exposed a valid
  `Content-Length`, require it to equal the total streamed octets after EOF for
  both the public release document and every successful response after an
  asset redirect. Retain independent expected asset-size validation.
- **Failure:** Malformed block shapes and supported read/access failures use
  stable content-silent `public_release.request_failed`; declared-versus-
  streamed disagreement uses `public_release.size_mismatch`. Supported local
  causes remain chained, and timeout, transport, output, byte-limit, and exact-
  artifact failures keep their existing codes and ordering.
- **Boundary:** No private response/socket state, raw HTTP/chunk parser,
  content decoder, alternate client, response-header requirement, cleanup,
  retry, proxy, DNS preflight, network sandbox, workflow, runner, action,
  permission, trigger, credential, release mutation, dependency, lock,
  version, runtime package, public API, or release authority. Unframed close-
  delimited bodies retain their existing boundary without a general
  completeness claim. Fixture/PR evidence is not a real release observation.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Local evidence:** The clean M47-M56 baseline passed 226 assertions. Official
  Python 3.14 documentation defines `HTTPResponse` as a binary buffered reader
  whose `read(amount)` returns up to that many bytes; RFC 9112 defines message
  bodies as octets and a shorter-than-declared body as incomplete. An initial
  tests-first attempt correctly exposed defects but also reloaded the verifier
  inside a helper, invalidating one exception-class assertion; no clean count
  is claimed from it. The corrected unchanged-verifier probe failed 12 cases
  and passed two controls, demonstrating raw type/access exceptions, accepted
  mutable/absent/oversized blocks, and missing declared-length agreement. The
  implementation passed all 14 initial M57 behavior assertions with focused
  format, Ruff, and strict Pyright clean; all 240 inherited M47-M57 behavior
  assertions passed together. After one explicit documentation-phrase
  correction, all 242 focused implementation, compatibility, boundary, and
  documentation assertions passed with strict docs. Findings-first review then
  demonstrated that `isinstance(..., bytes)` admitted a hostile bytes subclass
  whose length operation could raise an unwrapped exception: the regression
  failed and 16 controls passed. Exact built-in-bytes validation corrects that
  finding; all 243 focused assertions now pass. Whole-tree lock/sync,
  formatting, Ruff, strict Pyright, 621 architecture assertions, and strict
  docs pass. Complete graphics-enabled CPython 3.12-3.14 suites each pass 2,161
  tests with 14 expected skips. Ten real-wgpu tests, both three-repeat profile
  contracts, both vertical slices, and all documented M1-M4 benchmark
  validators pass. Two pre-record builds are byte-identical; installed-wheel
  and complete release smoke pass. Findings-first scope, archive, credential,
  identity, history, and integrity review reports no remaining actionable
  issue. Final record-inclusive static, documentation, reproducible-build,
  installed-wheel, and complete release-smoke gates pass.
- **Hosted evidence:** PR #123 exact head
  `f7347965d7e9a78218fa08a34f76aed7d32ba67d` passed run `31332655171` in
  exactly three Linux-first allocations. Linux job `93293248918` passed in
  5m37s before macOS `93293864546` and Windows `93293864554` began; they passed
  in 1m51s and 3m48s. Linux baseline and every compatibility suite passed
  2,165 tests, with one expected skip outside the baseline. Every platform
  passed ten real-graphics tests, profile smoke, Clockwork Arena, and Agent
  World Builder. Hosted reproducibility, installed-wheel smoke, and complete
  release smoke passed.
- **Integration:** Two delayed audits found no issue comment, review comment,
  review, or thread. Head-pinned, GitHub-verified squash
  `800050c74530d74a72338b5d444ee4751c5ad155` has the exact reviewed feature
  tree, sole parent M56 closeout, valid signature, and standalone DCO. The
  feature branch is deleted locally and remotely. Synchronized `main` has no
  post-merge run, open pull request, non-main remote branch, tag, or release.
- **Current gate:** This exact four-file documentation/project record requires
  one Linux allocation; its desktop umbrella must skip with zero steps.
