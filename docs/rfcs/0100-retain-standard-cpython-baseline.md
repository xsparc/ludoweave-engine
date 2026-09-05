# RFC-0100: Retain the standard CPython baseline after a free-threaded serial probe

- **Status:** Accepted
- **Date:** 2026-08-25
- **Decision owners:** LudoWeave maintainers

## Context

PEP 779 moved free-threaded CPython to officially supported but still optional
Phase II for Python 3.14. Python's free-threading guide documents that disabling
the GIL does not make arbitrary shared objects or iterators safe and that some
extension modules can re-enable the GIL. uv supports explicit discovery and
installation of free-threaded variants such as `3.14t`.

LudoWeave's accepted ownership model does not rely on the GIL. Engine, world,
render, platform, audio, and agent lifecycles are single-owner. The engine
records its constructing thread and checks that identity before lifecycle state
changes. Standard GIL CPython 3.12-3.14 is the documented support baseline;
free-threaded builds have remained optional experiments.

An exact Windows x86-64 CPython 3.14.5 free-threaded interpreter was installed
through uv. A pure LudoWeave `0.1.0a1` wheel installed into an isolated
environment without dependencies. `python -I -m ludoweave --version` and
`doctor` passed. With `Py_GIL_DISABLED == 1` and
`sys._is_gil_enabled() is False`, the installed wheel completed 120 virtual
ticks and frames in exactly 2,000,000,000 nanoseconds, closed normally, and
rejected a worker-thread initialize call with `engine.wrong_thread`. The
installed-wheel headless example reproduced the same deterministic summary.

## Decision

Retain standard GIL CPython as the supported baseline for CPython 3.12-3.14.
Record the exact Windows CPython 3.14.5t result as installed-wheel serial
compatibility evidence only.

Keep thread ownership explicit and independent of interpreter locking. Do not
branch runtime behavior on the build's GIL configuration and do not add locks
or concurrent mutation merely because the interpreter variant is officially
supported by CPython.

This is one free-threaded serial-compatibility decision. It is not a support
promise and makes no concurrent-safety claim.

## Boundary

M117 adds no parallel execution, performance result, graphics/wgpu evidence,
cross-platform free-threaded evidence, extension compatibility, provider
certification, runtime build branch, new lock, dependency, metadata, version,
runtime package/API, workflow, runner allocation, action, permission,
credential, release mutation, release authority, tag, release, or publication.
It is not a real public release observation.

The existing normal CPython CI matrix remains the support gate. The local
free-threaded probe is an observation, not a new CI or consumer matrix entry.

## Consequences

- The documented support baseline remains unambiguous despite CPython 3.14's
  interpreter-level Phase II promotion.
- Exact serial headless compatibility is recorded without implying that shared
  worlds, backends, services, iterators, or adapters are concurrently safe.
- The pure wheel and explicit owner-thread contract need no runtime change.
- A future support proposal must supply cross-platform lifecycle, world, agent,
  provider, extension, performance, failure, and maintenance evidence.

## Alternatives considered

- Promote free-threaded CPython to the supported matrix. Rejected because one
  Windows serial probe does not cover concurrent safety, graphics/providers,
  extensions, performance, or cross-platform behavior.
- Add a hosted free-threaded job. Rejected because it would consume runner
  allocation without closing the stated support evidence gaps.
- Add runtime GIL/build branches. Rejected because ownership is explicit and
  serial behavior requires no interpreter-specific code.
- Add locks around lifecycle calls. Rejected because the contract intentionally
  rejects cross-thread access rather than silently serializing it.

## References

- [PEP 779](https://peps.python.org/pep-0779/)
- [Python support for free threading](https://docs.python.org/3/howto/free-threading-python.html)
- [uv Python versions and variants](https://docs.astral.sh/uv/concepts/python-versions/)
- [ADR-0006: explicit resources and conflict-aware serial scheduling](../adr/0006-explicit-resources-and-conflict-aware-serial-scheduling.md)
- [ADR-0013: presentation extraction and render-resource ownership](../adr/0013-presentation-extraction-and-render-resource-ownership.md)
- [ADR-0022: defer native acceleration after profiling](../adr/0022-defer-native-acceleration-after-profiling.md)
