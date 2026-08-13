# Current Task

- **Task:** M84 - conventional archive entry-count preflight
- **Status:** Feature tree is hosted-qualified, reviewed, and squash-
  integrated; the bounded integration record is active.
- **Base:** Verified M84 feature squash
  `1ec97d0e5003dd92f21be6f49b528765de19506a`, tree
  `1a2bc67118919a6c6090f6bdf14794859f6bc452`.
- **Branch:** `release/m84-integration-record`

## Accepted slice

- After every established M69-M82 policy and M83 archive disk policy,
  read exactly the final conventional 22-byte end-of-central-directory record
  from the owned checksum-admitted snapshot.
- Require both conventional entry counts to equal the standard reader's parsed
  member count and restore the prior snapshot position.
- Reject any mismatch with stable content-silent error `sample bundle archive
  entry counts are inconsistent` before M77 decoded-name policy, metadata,
  exact inventory, staging, or reads.
- Preserve established error precedence and owned source/snapshot/archive
  cleanup.
- Add RFC-0067 plus aligned public, security, architecture, release, roadmap,
  maintainer, and repository evidence records.
- Add no ZIP64 end-record parser, sentinel resolution, end-record search,
  central-directory/local-header parser, neighboring-volume discovery, multi-
  volume assembler, workflow, dependency, lock, version, producer, runtime
  package/API, release authority, tag, release, or publication.

## Direction evidence

- PKWARE APPNOTE sections 4.3.16, 4.4.21, and 4.4.22 define the conventional
  EOCD current-disk and total-entry counts; `0xFFFF` defers a count to a ZIP64
  end record.
- Exact installed CPython 3.12.13, 3.13.13, and 3.14.5 source parses those
  fields but `ZipFile._RealGetContents()` does not consult them.
- Cross-version probes show zero, asymmetric, inflated, and `0xFFFF` pairs all
  preserve one parsed member and readable deflated payload.
- The fixed producer emits 50 in both fields and exposes exactly 50 members.

## Current evidence

- M83 closeout PR #203 changed only the three project records, allocated no
  workflow, passed two exact-head audits, and squash-integrated exact tree
  `c5bcfb19be359c828bcdd413f784ff4a9fa204e7` as
  `1c380897fc8ee43f5885c733c1c11f87878ff2a1` with sole integration-record
  parent, parsed DCO, and valid GitHub verification. Only clean synchronized
  `main` remained locally/remotely; no open PR, tag, release, postmerge run,
  disclosure marker, or M83 generated target remained before M84 selection.
- The static-clean authoritative red baseline passed 9 standard-library,
  established-precedence, producer, and protected-surface controls and failed
  16 missing policy, ordering, cleanup, helper/source, and documentation
  contracts in 0.50 seconds.
- The bounded runtime helper and exact call ordering make 24 assertions pass in
  0.31 seconds; only the deliberately absent RFC/public-document contract
  failed at that checkpoint. RFC-0067 and aligned documentation are now added.
- Review strengthened the helper's malformed-final-record normalization
  contract and corrected stale status wording. The corrected tree passes every
  local gate with no actionable finding remaining.
- Ready PR #204 exact DCO head
  `5c9d4cffb1392b4c7de960544ad13971c6db512b`, tree
  `1a2bc67118919a6c6090f6bdf14794859f6bc452`, passed run `31734854012`,
  classified substantive with 16 paths, in exactly three allocations: Linux
  7m17s, Windows 4m09s, and macOS 2m21s.
- Linux CPython 3.12/3.13/3.14 and both desktop 3.14 suites passed 2,547
  tests, with one compatibility skip outside baseline. Every OS passed 10
  real-wgpu tests, graphics profiling, Clockwork Arena, and Agent World
  Builder; static/docs, installed-wheel, staging, and release smoke passed.
- Hosted reproducibility produced a pure 275,344-byte wheel at
  `25a99abc2bd6f73ee15ccf1ebf524ad29854b34303321b087e8a53f2ab3858d9`
  and 1,329,869-byte sdist at
  `9e1b4ff35c3b6ddcd95c5e442f30ff0e627cce91b89b6ee60f85c237a42b4560`.
- Two separated audits retained exact base/head, `MERGEABLE`/`CLEAN`, three
  successful checks, matching DCO identity, and zero comments, reviews, or
  threads. Exact-head-guarded squash
  `1ec97d0e5003dd92f21be6f49b528765de19506a` has the exact qualified tree,
  sole M83-closeout parent, parsed DCO, and valid GitHub verification at
  `2026-08-13T19:27:56Z`. No postmerge run was allocated; the feature branch
  is deleted locally/remotely and `main` was synchronized before this record.
- The exact four-record integration tree passes the lock/static/architecture/
  docs/repository gate. Two builds reproduce a 275,358-byte wheel at
  `93750692bd8fddc37c9043c0fdfff46c3cce99f9bf15d0dec17189e530d40d20`
  and 1,331,078-byte sdist at
  `7e47faca5ebd49b5e688019c66deb2f465e1f7b74de455926989813e87c8324e`;
  isolated-wheel, ten-artifact staging, and complete release smoke pass.

## Remaining gates

1. Publish and integrate the bounded factual record, close out M84, remove its
   branches/generated targets, and return to clean synchronized `main` before
   selecting M85.
