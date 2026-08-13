# Current Task

- **Task:** M81 - ZIP comment preflight
- **Status:** The runtime policy, regression contract, RFC, and aligned public
  documentation are implemented; the complete local qualification and
  findings-first review pass; publication is pending.
- **Base:** Verified M80 closeout squash
  `3241a348a75c24a764f167ade48798ed3ac06af1`, tree
  `f5a1375cff72dfbbffa8ba755210815dac1bdfd7`.
- **Branch:** `release/m81-zip-comment-preflight`

## Accepted slice

- Reject a parser-exposed non-empty end-of-central-directory archive comment
  with stable content-silent error `sample bundle uses an archive comment`.
- Reject every parser-exposed non-empty central-directory member comment in a
  separate all-member pass with stable content-silent error `sample bundle
  uses a member comment`.
- Preserve every established M69/M75/M76/M78/M79/M80 category across all
  members, then apply archive-comment policy, member-comment policy, M77 name
  policy, metadata, exact inventory, staging, and reads in that order.
- Close the owned source, checksum-admitted snapshot, and archive before either
  policy error returns.
- Add RFC-0064 plus aligned public, security, architecture, release, roadmap,
  and repository evidence records.
- Add no raw ZIP parser, general comment scanner, comment decoder, workflow,
  dependency, lock, version, sample producer, runtime package/API, release
  authority, tag, release, publication, or general archive-sandbox claim.

## Direction evidence

- PKWARE defines the archive comment in the end-of-central-directory record and
  the member comment in each central-directory file header.
- Installed CPython 3.12.13, 3.13.13, and 3.14.5 preserve both exact byte
  strings while reading the same deflated payload; the fixture has no member
  extra field or general-purpose flag.
- The fixed LudoWeave producer emits 50 members with empty archive and member
  comments, so comments are outside the intended sample profile.

## Remaining gates

1. Publish a DCO-signed ready feature PR, require the exact three-allocation
   substantive gate, address review findings, and squash only after two clean
   exact-head audits.
2. Publish the bounded integration record and exact three-record closeout, then
   delete milestone branches/generated targets and return to clean synchronized
   `main` before selecting M82.
