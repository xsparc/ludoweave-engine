# ADR-0024: defer a Box2D v3 plugin after admission review

- Status: Accepted
- Date: 2026-08-06

## Context

The post-alpha sequence calls for evaluating, not automatically integrating, a
Box2D v3 plugin. Any external solver would own mutable native bodies, shapes,
contacts, and allocation lifetimes while LudoWeave's ECS/world store remains
the sole canonical authority. Admission therefore requires evidence for the
complete supported Python/platform matrix, explicit ownership, headless use,
API stability, GIL/thread behavior, determinism classification, and an adapter
that copies values at deliberate command/tick boundaries.

The evaluated distribution is `box2d-python==0.1.2`, released on 2025-03-09.
Its project page describes a CFFI binding, an early development preview whose
API may change, and partial Box2D v3.0 functionality. PyPI publishes no source
distribution and only CPython 3.12/3.13 wheels: Windows x86-64, Linux
x86-64/i686, and macOS ARM64. It publishes no CPython 3.14 or macOS x86-64
wheel. The evaluated files were not uploaded with Trusted Publishing.

Official Box2D documentation now describes 3.1.0. Its determinism FAQ says
cross-platform determinism begins with Box2D 3.1 for identical inputs, while
also distinguishing determinism from rollback support. The community Python
binding describes partial v3.0 support and does not identify its bundled C
revision, GIL-release rules, cross-platform replay contract, or thread-safety
policy. The upstream 3.1 claim therefore cannot be inherited by this binding.

## Admission evidence

| Gate | Evidence | Result |
| --- | --- | --- |
| Supported wheels | PyPI has CPython 3.12/3.13 wheels for a subset of OS/architectures, no source distribution, and no CPython 3.14 wheel. An isolated CPython 3.14 resolution fails because only `cp312`/`cp313` ABIs exist. | Fail |
| Ownership/lifetime | The bounded probe creates, steps, and explicitly destroys 25 worlds per run and calls `destroy()` twice. Windows CPython 3.12 and 3.13 pass, but cross-platform soak, stale-object, GC/finalizer, callback, and partial-failure coverage do not exist. | Incomplete |
| Clean headless | The same isolated Windows runs step a body without a window or testbed. Other supported systems were not probed. | Incomplete |
| API stability | The package explicitly labels itself an early preview with an API subject to change. The installed wheel also rejected the tuple-position form shown on its PyPI example before the probe was corrected to its installed call shape. | Fail |
| GIL/thread behavior | The API accepts a worker-thread count, but the binding documents no GIL-release, callback, free-threaded, or concurrent ownership contract. | Unknown |
| Replay/determinism | Two Windows Python versions produced the same exact trace digest across 25 single-thread repetitions. That is useful same-binary smoke only, not cross-platform, snapshot, rollback, contact-order, or engine replay conformance. | D0 only |
| Adapter conformance | No engine adapter, copied descriptor/observation contract, state reconciliation policy, installed-wheel smoke, or maintenance owner exists. | Not demonstrated |

## Decision

Defer the Box2D plugin. Do not add `box2d-python` to project metadata, the uv
lock, a LudoWeave package, public APIs, release artifacts, or hosted quality
matrices. Keep the pure-Python collision slice as the only implemented
collision behavior. Architecture tests reject `box2d`, `Box2D`, and
`box2d_python` imports from engine source.

Retain `scripts/probe_box2d_candidate.py` as a bounded repository evaluation
tool. It dynamically imports a candidate supplied by an isolated environment,
first proves that the resolved module belongs to the named distribution's
installed-file inventory, uses one worker thread and an exact fixed step,
requires observable movement, records finite positions as hexadecimal floats,
requires repeat-identical traces, exercises repeated explicit destruction, and
emits sanitized versioned JSON. It does not import LudoWeave, measure
performance, or establish an adapter contract.

A future external-physics proposal must treat the ECS/world store as canonical.
It may consume copied engine-owned descriptors at explicit safe points and
return copied observations or command proposals; provider bodies, shapes,
contacts, allocators, callbacks, pointers, and snapshots must never enter
public APIs or canonical records. External physics is D0 by default. A stronger
classification requires snapshot/restore, replay, cross-platform hash, contact
ordering, and failure-reconciliation conformance against exact versioned
provider artifacts.

Reconsider admission only when one proposal supplies all of this evidence:

1. a maintained, non-preview Python binding with a documented compatibility
   policy and exact bundled Box2D revision;
2. auditable wheels for every supported CPython 3.12-3.14 and CI
   OS/architecture, plus an auditable source/build path and provenance;
3. bounded cross-platform headless, initialization-failure, lifecycle-soak,
   repeated-close, stale-object, finalizer, and callback cleanup tests;
4. documented GIL release, thread affinity, worker ownership, callbacks, and
   normal/free-threaded CPython behavior;
5. same-binary and cross-platform replay evidence, with explicit limitations
   for rollback, floating point, worker counts, contacts, and provider upgrades;
6. an exercised adapter conformance suite proving copied engine types,
   command/receipt boundaries, ECS authority, bounded work, and atomic failure
   reconciliation; and
7. a named maintainer accepting binding, native-binary, security, and
   cross-platform support responsibility.

## Consequences

- The base install, lock, release wheel, and compiler-free headless path remain
  unchanged and pure Python.
- The project gains reproducible candidate evidence without implying that a
  successful local trace admits the provider.
- Rigid bodies, impulses, joints, rotations, contacts, and native solver state
  remain unavailable.
- A future plugin needs an exercised implementation before a runtime protocol
  is added; M9 does not create an empty speculative physics package.

## Evidence sources

- [box2d-python project status and files](https://pypi.org/project/box2d-python/)
- [box2d-python documentation](https://box2d-py.readthedocs.io/en/latest/)
- [Box2D 3.1 documentation](https://box2d.org/documentation/)
- [Box2D determinism FAQ](https://box2d.org/documentation/md_faq.html)
- [Box2D 3.1 release discussion](https://box2d.org/posts/2025/04/box2d-3.1/)
