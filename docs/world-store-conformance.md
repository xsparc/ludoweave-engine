# WorldStore conformance

M19 provides an installed, dependency-free behavioral profile for
storage-neutral implementations of the existing `WorldStore` protocol. It lets
an adapter author run the same bounded checks without copying repository-private
fixtures.

A passing report is evidence for one adapter build in one caller-controlled
environment. It is not discovery, certification, provider admission, a
security review, a performance result, or a support-matrix claim.

## Run the built-in references

The release sample bundle includes explicit choices for both project-owned
implementations:

```console
python world_store_conformance.py
python world_store_conformance.py --backend reference
```

An external package imports and selects its own trusted factory:

```python
from my_storage_adapter import MyWorld
from ludoweave.ecs import run_world_store_conformance

report = run_world_store_conformance(
    "org.example.my-world",
    MyWorld,
)
print(report.to_json(), end="")
```

The factory is called exactly once with a new immutable `ComponentRegistry` and
must return a `WorldStore` that retains that exact registry identity. The caller
imports and trusts the adapter. LudoWeave performs no entry-point discovery,
module lookup, installation, filesystem scan, subprocess launch, network
request, or global registration.

## Versioned baseline

Protocol `ludoweave.world-store-conformance/1` identifies reports; profile
`world-store-baseline/1` fixes these checks and their order:

| Check | Contract exercised |
| --- | --- |
| `factory_registry` | One explicit factory call, public method shape, and exact borrowed registry identity. |
| `empty_state` | Zero epochs and no entities or component rows. |
| `direct_mutation_epochs` | Deterministic IDs, component ownership, membership, logical epochs, and structural epochs. |
| `copy_isolation` | Inputs, returned values, `get()`, and inspection rows cannot alias canonical state. |
| `entity_generations` | Destroyed IDs stay stale and deterministic slot reuse advances generation. |
| `query_semantics` | Stable order, exclusions, change filters, detached rows, and zero-component queries. |
| `writable_query_lifecycle` | Explicit writeback, mutation exclusion, abort behavior, and cursor lifecycle errors. |
| `command_buffer_atomicity` | Deferred resolution, exact epochs, failure rollback, retained retry, and ownership. |
| `clone_independence` | State and allocator cloning without value or command-buffer aliases. |
| `structured_failures` | Exact engine errors and unchanged state/allocation after rejected operations. |

Every check must pass for overall success. A failed prerequisite produces one
runner-owned failure code and marks the remaining checks `not_run`; provider
messages and codes are never copied into the report.

## Evidence and disclosure boundary

Reports contain only the validated adapter ID, installed LudoWeave version,
protocol/profile identities, fixed check IDs, statuses, and runner-owned
`world_store_conformance.*` codes. They exclude paths, environment and platform
data, timings, component or entity values, storage layout, credentials,
provider diagnostics, and native objects.

The runner invokes adapter code synchronously in-process on the calling thread.
It has no timeout or containment and cannot stop a malicious or defective
factory from blocking, crashing, allocating excessively, or exercising ambient
authority. Use separate process and operating-system controls when evaluating
untrusted code.

The current public `WorldStore` contract is single-owner, in-memory state and
has no `close()` lifecycle. The runner therefore performs no cleanup call and
does not admit stores that require files, databases, processes, threads, native
handles, or other external resources. Such a lifecycle needs a separate
engine-owned protocol and decision before conformance can cover it.

`World` and `ReferenceWorld` provide project-owned source, isolated-wheel, and
release-bundle evidence. They are reference results, not independent adoption.
The count of independently authored third-party world adapters with accepted
evidence remains zero until maintainers review such a submission. See
[ADR-0033](adr/0033-explicit-installed-world-store-conformance.md), the
[ECS guide](ecs.md), and the [adapter guide](adapter-guide.md).
