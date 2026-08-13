# Current Task

- **Task:** M81 - ZIP comment preflight
- **Status:** The runtime policy, regression contract, RFC, and aligned public
  documentation are hosted-qualified, twice audited, and squash-integrated;
  the bounded integration record is active.
- **Base:** Verified feature squash
  `8a3a156d08a7c40c9b34ae726311776c0e2f8611`, tree
  `30d6bf6db4272279c3f32dc3c9901399018e55bc`.
- **Branch:** `release/m81-integration-record`

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

## Hosted outcome

- Exact DCO head `fbff420391675c6519c606a251cc4a697efe9d62`
  passed run `31718815561` in exactly three allocations: Linux job
  `94510280379` in 7m08s, macOS job `94512364384` in 2m30s, and Windows job
  `94512364395` in 4m10s.
- Linux CPython 3.12 passed 2,465 tests; Linux 3.13/3.14 and both desktop 3.14
  suites passed 2,465 tests with one capability skip. Every OS passed 10 real-
  wgpu tests, graphics profiles, Clockwork Arena, and Agent World Builder.
- Hosted reproducibility produced a pure 274,962-byte wheel at
  `71faae79b33898e5ed417445bdb14793b934efb01c464db73e0f40eec173342e`
  and a 1,306,054-byte sdist at
  `6d257296b8595e76cc1f1fdb73cdfea31d5152013c63ca1d69859e9ea40ef27f`;
  installed-wheel, deterministic staging, and release smoke passed.
- Two separated exact-head audits found no review, comment, inline comment, or
  thread. Guarded squash `8a3a156d08a7c40c9b34ae726311776c0e2f8611`
  has the exact qualified tree, sole M80-closeout parent, standalone DCO, and
  valid GitHub verification. No postmerge workflow was allocated and the
  feature branch is deleted locally/remotely.

## Remaining gates

1. Validate and publish the exact four-path integration record through the
   documentation gate; audit and squash it only after the bounded result is
   clean.
2. Publish the exact three-record closeout, then
   delete milestone branches/generated targets and return to clean synchronized
   `main` before selecting M82.
