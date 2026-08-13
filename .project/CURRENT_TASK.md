# Current Task

- **Task:** M80 - closeout
- **Status:** The corrected feature and integration record are hosted-qualified
  and squash-integrated; the exact three-record closeout passes local and
  record-inclusive gates; publication is active.
- **Base:** Verified integration-record squash
  `218c761c55e71d0367823bdac5ff2c92f4c5adf6`, tree
  `debee0bfa348af18509f8f5f0d7d4e01c4a8a30d`.
- **Branch:** `release/m80-closeout`

## Completed outcome

- Reject exact PKWARE ZIP64 extended-information extra-field ID `0x0001` for
  every sample member during a separate archive-wide preflight.
- Preserve M69/M75/M76/M78 and M79 precedence across every member, then run
  ZIP64 policy before M77 decoded-name checks, metadata, inventory, staging,
  or reads.
- Return stable content-silent error `sample bundle uses a ZIP64 extra field`
  and close owned source, snapshot, and archive resources.
- Use a bounded field walk that ignores unrelated field IDs and does not add
  malformed-extra policy beyond CPython's parser.
- Add RFC-0063 and aligned public, security, architecture, release, roadmap,
  and repository evidence records.
- Add no broad extra-field ban, raw ZIP64 parser, large-file support change,
  workflow, dependency, version, sample producer, runtime package/API, release
  authority, tag, release, or publication.
- Corrected exact head `0a42620d3771bde90978a697b672d51bf66273a5`
  passed run `31713078940` in exactly three allocations after a valid review
  correction distinguished PKWARE disk-start capacity from current CPython
  behavior.
- Feature squash `13439d41551cd9c842b3e7a0a55e7ba72e540582`
  has the exact corrected tree, sole M79-closeout parent, standalone DCO, and
  valid GitHub verification.
- The addressed review thread is resolved and outdated; the feature branch is
  deleted locally/remotely. No tag, release, publication, dependency,
  workflow, producer, runtime-package, version, or release-authority change
  was introduced.
- Integration PR #193 classified exactly four paths as documentation. Run
  `31714883660` used one 42-second Linux allocation, passed 895 hosted
  architecture assertions and every artifact smoke, and skipped desktop with
  zero steps.
- Two separated integration audits found no review, comment, inline comment,
  or thread. Integration squash
  `218c761c55e71d0367823bdac5ff2c92f4c5adf6` has the exact reviewed tree,
  sole feature-squash parent, DCO, and valid GitHub verification.
- All obsolete feature and integration branches are deleted locally/remotely.

## Remaining gates

1. Publish a DCO-signed ready closeout PR, confirm no path-filtered
   workflow is created, perform two review-state audits, and squash with an
   exact-head guard and DCO body file.
2. Delete the closeout branch and all M80 generated targets, return to clean
   synchronized `main`, verify no PR/tag/release or extra branch remains, and
   select M81.
