# Current Task

- **Task:** M38 - distribution reproducibility integration record
- **Status:** The implementation is complete and squash-integrated. A bounded
  documentation-only public record is awaiting its one-allocation hosted gate.
- **Started:** 2026-08-08
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Base:** Exact verified M38 feature squash
  `9f6ca61ccb1f9b7e0796e5cc60c7dd38e6af99d7` on synchronized `main`.
- **Outcome:** The existing Linux pull-request and tag-release jobs now fail
  closed unless two same-source distribution builds contain exactly one
  matching universal wheel and source archive whose bytes are identical.
- **Accepted feature evidence:**
  - Final DCO-signed head
    `4f3db7446c842df4f36d7cc8f8321a89bbe5997f` passed pull-request run
    `31261807768` in exactly three allocations: Linux in 6m50s, macOS in
    1m59s, and Windows in 3m44s. Desktop work started only after Linux passed.
  - The Linux verifier emitted
    `ludoweave.distribution-reproducibility/1` with `status=pass`, a
    266,797-byte wheel SHA-256
    `6c43bb79ed5de115ee645f1c8a9b4e8338f364c5bb1f53e08cde58e82e9afe06`,
    and an 892,185-byte sdist SHA-256
    `8f21585819f76f289887a6194e44bcf06b72497d70d13451326cc778e48e4f8a`.
  - Review found one real symlink-cycle failure path. Correction
    `4f3db7446c842df4f36d7cc8f8321a89bbe5997f` normalizes it to structured
    JSON, the replacement run passed, and the sole thread is resolved and
    outdated.
  - PR #65 squash `9f6ca61ccb1f9b7e0796e5cc60c7dd38e6af99d7`
    has exact parent
    `3578da64b2686cd8d63340aeb1eed30f5c4cb761`, exact reviewed tree
    `1a96d02b8b23410732fc7ac746179459a14d3f44`, a valid GitHub signature,
    and a parsed DCO trailer. The feature branch is deleted locally and
    remotely, and no post-merge `main` run was allocated.
- **Remaining acceptance gate:** Validate this Markdown-only record through
  the trusted documentation lane: one Linux allocation, desktop matrix skipped
  before runner expansion, no change to runtime, dependency, lock, release
  authority, or workflow topology.
- **Non-scope:** Runtime or public API; persistent formats/protocols; package
  version, dependency, lock, platform/version support; timestamp-policy change;
  cross-platform or independent-rebuilder comparison; attestation changes;
  tag, release, PyPI publication, certification, or deferred runtime subsystem.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
