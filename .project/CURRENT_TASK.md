# Current Task

- **Task:** M79 - exact Unicode Path extra-field preflight
- **Status:** Complete local qualification, findings-first review, final audit,
  record-inclusive release, and post-record gates are green; ready-PR
  publication is active.
- **Base:** Verified M78 closeout
  `5fe3134bf5a56e5cbf986ed33db698c830aa9219`, tree
  `1e1da7d8062433c2297d170643626413dfbd457f`.
- **Branch:** `release/m79-unicode-path-preflight`

## Intended outcome

- Reject exact Info-ZIP Unicode Path extra-field ID `0x7075` for every sample
  member during a separate archive-wide preflight.
- Preserve M69/M75/M76/M78 precedence across every member, then run exact
  extra-field policy before M77 decoded-name checks, metadata, inventory,
  staging, or reads.
- Return stable content-silent error `sample bundle uses a Unicode Path extra
  field` and close owned source, snapshot, and archive resources.
- Use a bounded field walk that ignores unrelated field IDs and does not add
  malformed-extra policy beyond CPython's parser.
- Add RFC-0062 and aligned public, security, architecture, release, roadmap,
  and repository evidence records.
- Add no broad extra-field ban, general name-difference rule, workflow,
  dependency, version, sample producer, runtime package/API, release authority,
  tag, release, or publication.

## Remaining gates

1. Publish a DCO-signed ready PR, exact-head qualify it on the existing three-
   allocation essential CI, audit review state twice, and squash only after the
   complete result is clean.
