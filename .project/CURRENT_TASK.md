# Current Task

- **Task:** M38 - distribution reproducibility enforcement
- **Status:** Complete, hosted-validated, reviewed, squash-integrated, publicly
  recorded, and cleaned up.
- **Started:** 2026-08-08
- **Completed:** 2026-08-09
- **Authority:** The standing maintainer instruction authorizes subsequent
  fully validated milestone pull requests while requiring only necessary,
  vital hosted checks.
- **Feature base:** Exact M37 closeout
  `3578da64b2686cd8d63340aeb1eed30f5c4cb761`.
- **Feature squash:** `9f6ca61ccb1f9b7e0796e5cc60c7dd38e6af99d7`.
- **Public record squash:** `42046d521242147cc5ed56874238d25de9870316`.
- **Outcome:** The existing Linux pull-request and tag-release jobs fail
  closed unless two same-source distribution builds contain exactly one
  matching universal wheel and source archive whose bytes are identical.
- **Acceptance evidence:**
  - Corrected substantive run `31261807768` passed exact head
    `4f3db7446c842df4f36d7cc8f8321a89bbe5997f` in exactly three allocations:
    Linux 6m50s, macOS 1m59s, and Windows 3m44s. Desktop work began only after
    Linux passed.
  - The Linux verifier emitted
    `ludoweave.distribution-reproducibility/1` with `status=pass`, a
    266,797-byte wheel SHA-256
    `6c43bb79ed5de115ee645f1c8a9b4e8338f364c5bb1f53e08cde58e82e9afe06`,
    and an 892,185-byte sdist SHA-256
    `8f21585819f76f289887a6194e44bcf06b72497d70d13451326cc778e48e4f8a`.
  - The sole feature review finding is corrected, resolved, and outdated.
    Both feature commits, feature squash, record commit, and record squash have
    the required DCO trailers; both squash commits have valid GitHub signatures
    and exact reviewed trees.
  - Documentation record run `31262609814` classified four Markdown paths as
    documentation, passed one Linux allocation in 32 seconds, and skipped the
    desktop matrix before expansion in zero seconds with no runner steps.
  - No feature or record merge triggered a `main` run. All M38 feature and
    public-record branches are deleted locally and remotely.
- **Non-scope:** Runtime or public API; persistent formats/protocols; package
  version, dependency, lock, platform/version support; timestamp-policy change;
  cross-platform or independent-rebuilder comparison; attestation changes;
  tag, release, PyPI publication, certification, or deferred runtime subsystem.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Next:** Select the next bounded milestone from repository evidence; do not
  infer release, publication, or deferred subsystem authority.
