# Current Task

- **Task:** M80 - exact ZIP64 extra-field preflight
- **Status:** Implementation, complete local qualification, independent review,
  exact-scope audit, and prepublication history audit are green; DCO feature
  publication is active.
- **Base:** Verified M79 closeout
  `892f17fce99d218905c6f624c730f735d21a794f`, tree
  `1fca519b95832978516a22c3c6bd19ff93955afd`.
- **Branch:** `release/m80-zip64-extra-preflight`

## Intended outcome

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

## Remaining gates

1. Publish a DCO-signed ready PR, exact-head qualify it on the existing three-
   allocation essential CI, audit review state twice, and squash only after the
   complete result is clean.
