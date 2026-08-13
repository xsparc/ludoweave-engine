# Current Task

- **Task:** M78 - exact data-descriptor sample-member preflight
- **Status:** Complete local qualification, findings-first correction, final
  audit, record-inclusive release, and post-record gates are green; ready-PR
  publication is active.
- **Base:** Verified M77 closeout
  `4bca618578f29629a7270ab5d9d308fd34363a06`, tree
  `a47d36363bdc48a91ef55feae8e8f3b53077907a`.
- **Branch:** `release/m78-data-descriptor-preflight`

## Intended outcome

- Reject exact ZIP general-purpose data-descriptor bit 3 for every sample
  member during a separate archive-wide preflight.
- Preserve established M69/M75/M76 flag precedence across every member, then
  run descriptor policy before M77 decoded-name checks, metadata, inventory,
  staging, or reads.
- Return stable content-silent error `sample bundle uses a data descriptor`
  and close owned source, snapshot, and archive resources before returning.
- Retain current fixed producer compatibility and leave unrelated flag bits
  outside this exact policy.
- Add RFC-0061 and align public, security, architecture, release, roadmap, and
  repository evidence records.
- Add no raw descriptor parser, broad flag allowlist, workflow, dependency,
  version, sample producer, runtime package/API, release authority, tag,
  release, or publication.

## Remaining gates

1. Publish a DCO-signed ready PR, exact-head qualify it on the existing three-
   allocation essential CI, audit review state twice, and squash only after the
   complete result is clean.
