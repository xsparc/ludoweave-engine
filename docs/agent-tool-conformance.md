# Agent-tool conformance

M18 provides an installed, dependency-free behavioral profile for adapters to
the existing 12-tool `AgentCommandService` contract. It lets an adapter author
exercise the versioned tool surface outside the LudoWeave source tree without
copying repository-private fixtures.

The profile and Python API are **experimental**. A passing report is reference
evidence for one adapter build in one caller-controlled environment. It is not
a sandbox, security or provenance review, cross-platform claim, performance
result, provider admission, or proof of real-world agent recovery rates.

## Run the reference profile

The release sample bundle includes a dependency-free direct-service adapter:

```console
python agent_tool_conformance.py
```

An external local adapter calls the same installed runner with a trusted
factory:

```python
from my_adapter import make_agent_adapter
from ludoweave.agent import run_agent_tool_conformance

report = run_agent_tool_conformance(
    "org.example.my-agent-adapter",
    make_agent_adapter,
)
print(report.to_json(), end="")
raise SystemExit(0 if report.passed else 1)
```

The caller imports and chooses the adapter. LudoWeave performs no entry-point
or package discovery, dynamic import, installation, filesystem scan,
subprocess launch, network request, or global registration. The factory and
adapter execute synchronously in-process and therefore must already be
trusted.

## Baseline profile

Protocol `ludoweave.agent-tool-conformance/1` identifies reports; profile
`agent-tool-baseline/1` fixes these checks and their order:

| Check | Required behavior |
| --- | --- |
| `factory` | Construct exactly one fresh adapter on the calling thread. |
| `service_contract` | Expose the exact 12 tools and read, write, capture, and test capabilities from a clean tick-zero world. |
| `read_isolation` | Return a detached description without mutating authority. |
| `snapshot_baseline` | Return a valid baseline snapshot and matching state hash. |
| `transaction_validation` | Dry-run a canonical entity creation without changing authority. |
| `transaction_commit` | Commit the same command with an exact accepted receipt and predicted post-hash. |
| `stale_hash_atomicity` | Reject a stale optimistic hash and preserve the committed authority unchanged. |
| `entity_query` | Query the created entity through the typed result contract. |
| `tick_receipts` | Advance two ticks with one accepted receipt and an exact hash link per tick. |
| `snapshot_diff` | Diff the baseline against current authority and report the expected semantic change. |
| `capture_tests_telemetry` | Validate bounded capture metadata, registered-test result shape, and telemetry without granting canonical authority to diagnostics. |
| `close_lifecycle` | Close twice, then reject use after close with structured `agent.closed`. |

The registered-test check validates the adapter protocol and result shape. It
does not require the fresh conformance fixture to satisfy application-specific
game tests, so either a true or false `passed` value is valid evidence.

Each check is `pass`, `fail`, or `not_run`. A failed prerequisite prevents
dependent operations, but the runner still attempts cleanup. The overall
status is `pass` only when every check passes.

Reports contain only the validated adapter ID, LudoWeave version, fixed
protocol/profile, stable check IDs, statuses, and runner-owned
`agent_conformance.*` codes. They exclude provider messages and codes, paths,
environment values, platform metadata, timing, snapshots, captures, entity
values, credentials, and native objects.

## Trust, ownership, and limitations

Each run owns one adapter returned by the factory and calls it only from the
caller thread. The runner closes it twice to require idempotence and attempts
best-effort close after any interrupted stage. The adapter must provide a fresh
clean authority with all four baseline capabilities; production authority
must not be supplied.

The runner has no timeout or containment. A malicious or defective factory can
block, crash, consume resources, access ambient process authority, mutate
external systems, or falsify its own responses. Run external adapters with the
isolation appropriate to their provider.

The baseline does not certify transport framing, remote authentication,
filesystem confinement, dependency integrity, supported OS/Python coverage,
thread or free-threaded safety, throughput, maintenance ownership, or how often
a real agent completes tasks without manual recovery. Adapter packages retain
their focused tests and support evidence.

M18 records one project-owned direct-service pass. The count of independently
authored adapters with accepted evidence remains zero until maintainers review
an external contribution. Profile meaning or order changes require a new
profile version; incompatible report-envelope changes require a new protocol
version and architecture decision. See
[ADR-0032](adr/0032-explicit-installed-agent-tool-conformance.md) and the
[adapter guide](adapter-guide.md).
