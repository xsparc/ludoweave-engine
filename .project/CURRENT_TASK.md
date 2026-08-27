# Current task

- **Task:** M148 - decide whether current CPython exposes a portable safe
  asset-cache cleanup capability.
- **Status:** Direction research, exact Windows supported-runtime probes, RFC,
  public platform decision, architecture/roadmap contract, and automated no-
  runtime-change guard, complete static/architecture/docs/governance checks,
  supported-Python suites, real wgpu checks, profiles, and vertical slices are
  complete. Reproducible distributions, all 28 installed consumers, two
  identical release rehearsals, archive inspection, and findings-first review
  are complete. Final evidence-inclusive closure, source separation, bounded
  cleanup, the initial DCO commit, exact local audit, and fresh hosted-state
  audit are complete. Publication is held because authoritative hosted `main`
  remains exact M99.
- **Base:** Fully locally validated M147 DCO commit
  `752334dd981799c95d24308087222be487c0587e`, tree
  `273f80c3740d5ad21d27afbc872f6457f204a566`, sole parent exact M146.
- **Branch:** `release/m148-cache-cleanup-capability-decision`.

## Acceptance boundary

- Accept RFC-0131 and document whether present CPython can satisfy M147's
  complete handle-relative/no-follow mutation chain.
- Require an engine-owned platform adapter, native-object isolation, real-host
  adversarial proof, and safe refusal before any platform is admitted.
- Protect exact runtime, cache, CLI, dependency, workflow, and release surfaces
  plus the M147 threat model with automated architecture tests.
- Add no runtime API, command, probe, adapter, native code, cleanup authority,
  dependency, workflow, or CI change.

## Direction evidence

- Python 3.14 documents directory-relative and no-follow support as conditional
  per function/platform. Exact Windows CPython 3.12.13, 3.13.13, and 3.14.5
  probes expose no relevant `dir_fd` mutation and report non-resistant
  `shutil.rmtree` behavior.
- POSIX directory-relative operations, Linux `openat2`, macOS
  `O_NOFOLLOW_ANY`, and Win32 handle operations are partial platform primitives;
  none is a current portable CPython contract or complete adapter proof.
- Exact M147 history, clean worktree, DCO, and object integrity were established
  before this branch. Exact ancestry allowed the contained M147 branch to be
  pruned; only local `main` and active M148 remain.

## Explicit non-scope

- No cleanup, adapter, capability probe, `ctypes`, native code, deletion,
  retained-root implementation, candidate list, cache read/write, remote cache,
  network, or trusted-time implementation.
- No dependency, version, workflow/CI, permission, credential, release, tag,
  push, or PR change.

## Remaining acceptance work

- No local M148 acceptance work remains. Keep the milestone unpublished until
  a fresh hosted audit proves the required preceding stack is present; continue
  the next approved research-gated milestone from the exact committed M148 tip.
