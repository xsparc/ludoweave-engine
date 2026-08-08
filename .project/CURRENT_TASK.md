# Current Task

- **Task:** M37 - fail-closed CI change qualification
- **Status:** Complete, hosted-validated, squash-integrated, and cleaned up.
- **Completed:** 2026-08-08
- **Authority:** The standing maintainer instruction requires only necessary,
  vital hosted checks and authorizes fully validated milestone pull requests.
- **Integrated commits:** Feature squash
  `407226beae36182d237e32866a86ce19bb93c691` and public record squash
  `7434f310c86dd9acf6c61ff01c1a5f2dfcdffe31` are consecutive, exact-tree,
  validly GitHub-signed, DCO-compliant commits on synchronized main.
- **Outcome:** The trusted base-revision classifier fails closed and admits
  only narrow Markdown/community changes to one bounded Linux gate. All other
  changes retain the complete three-allocation M36 validation gate. Desktop
  allocation depends on successful Linux qualification.
- **Hosted evidence:** Corrected substantive run `31259200818` passed exact
  final feature head in three sequentially qualified allocations. Public
  documentation run `31259908552` passed the one Linux allocation in 32
  seconds; GitHub skipped the unexpanded desktop matrix with no runner steps.
- **Review:** The executable-documentation bypass and tracked lowercase
  pull-request-template mismatch were corrected with regressions. PR #62's
  sole review thread is outdated/resolved; PR #63 has no review thread.
- **Scope:** No runtime, test behavior, dependency, lock, package version,
  release workflow, tag, publication, branch protection, required-check
  setting, provider, certification, support-policy, or deferred-subsystem
  change was made.
- **SemVer:** No package/public-Python change; version remains `0.1.0a1`.
- **Next:** No subsequent milestone has been selected or started in this
  closeout record.
