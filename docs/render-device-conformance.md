# Render-device conformance

M17 provides an installed, dependency-free baseline profile for explicit
`RenderDevice` adapters. It turns the adapter guide's minimum behavioral rules
into versioned evidence that an adapter author can run outside the LudoWeave
source tree.

The profile and Python API are **experimental**. A passing report is behavioral
evidence for one adapter build in one caller-controlled environment. It is not
a security review, sandbox, provenance statement, cross-platform claim, plugin
admission, or compatibility guarantee.

## Run the reference profiles

The bundled example selects only two built-in composition roots:

```console
python render_device_conformance.py
python render_device_conformance.py --backend wgpu
```

The first command uses the dependency-free `NullRenderDevice`. The second
requires the version-matched `graphics` extra and constructs the optional
`WgpuRenderDevice` directly. The example does not accept a module, entry point,
package, path, URL, or command.

An external adapter package calls the same installed runner with a trusted
factory:

```python
from my_adapter import MyRenderDevice
from ludoweave.render import run_render_device_conformance

report = run_render_device_conformance(
    "org.example.my-renderer",
    MyRenderDevice,
)
print(report.to_json(), end="")
raise SystemExit(0 if report.passed else 1)
```

The caller imports and chooses the adapter. LudoWeave performs no discovery,
dynamic import, installation, filesystem scan, subprocess launch, network
request, or global registration.

## Baseline profile

Protocol `ludoweave.render-device-conformance/1` identifies reports; profile
`render-device-baseline/1` fixes these checks and their order:

1. `factory` constructs one device on the calling thread.
2. `identity_capabilities` requires a bounded diagnostic name and exact
   engine-owned `RenderCapabilities` whose backend identity matches it.
3. `resource_handles` creates a buffer, texture, pipeline, and offscreen
   surface and requires exact engine-owned handles from one device scope.
4. `clear_submission` submits one provider-neutral clear and validates the
   exact submission record and counters.
5. `completion_capture` polls one fence and checks capture behavior against the
   advertised capability. Captures remain immutable RGBA bytes and are not
   placed in the report.
6. `resize_events` exercises a positive resize and requires copied tuples of
   engine-owned platform and gamepad records.
7. `stale_handle` retires a buffer and requires a structured stale-generation
   rejection on repeated destruction.
8. `close_idempotence` closes the device twice.
9. `closed_rejection` requires a structured `render.device_closed` failure
   after close.

Each check is `pass`, `fail`, or `not_run`. A prerequisite failure prevents
dependent operations but does not suppress best-effort close. The overall
status is `pass` only when every check passes. The report includes the selected
adapter ID, validated backend name, LudoWeave version, profile, stable check
IDs, statuses, and runner-owned `conformance.*` error codes. It excludes
provider error codes, exception messages,
captures, paths, environment values, platform metadata, timings, and provider
objects.

## Trust, ownership, and limitations

The runner invokes adapter code in-process and has no timeout or containment.
Run only factories you already trust, in isolation appropriate to that
provider. A malicious or defective adapter can block, crash, allocate without
bound, access ambient process authority, or falsify a copied report. Conformance
does not make executable code safe.

The baseline intentionally does not certify windows, input hardware, device
loss/recovery, sprite pixels, performance, native wheels, dependency
provenance, free-threaded safety, every supported OS/Python pair, or full
provider cleanup after an uncatchable process failure. Official adapters retain
their focused tests and hosted matrix. Third-party contributors must supply
their own package identity, dependency provenance, support matrix, and repeated
installed evidence.

M17 records two project-owned passing implementations: Null and the optional
wgpu adapter. The count of independently authored third-party adapters with
accepted repository evidence remains zero until an external contribution is
reviewed; the project will not infer adoption from package discovery or stars.

Changing check meaning or order requires a new profile version. Changing the
JSON envelope incompatibly requires a new protocol version and an architecture
decision. See [ADR-0031](adr/0031-explicit-installed-render-device-conformance.md)
and the [adapter guide](adapter-guide.md).
