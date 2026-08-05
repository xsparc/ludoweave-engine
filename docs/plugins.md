# Plugin manifests and compatibility

LudoWeave M12 provides an inert manifest format and compatibility evaluator.
It does not provide a plugin loader. Applications still import trusted adapter
packages explicitly and inject implementations through engine-owned protocols.

The public `ludoweave.plugins` surface is **preview**. Manifest wire protocol
`ludoweave.plugin-manifest/1` is persistent and governed by
[RFC-0002](rfcs/0002-data-only-plugin-manifest-compatibility.md).

## What a manifest can say

A v1 manifest declares one lowercase dotted plugin identity, its release,
half-open LudoWeave and CPython ranges, supported desktop platforms, extension
capabilities, highest claimed determinism tier, whether implementation code is
native, and bounded plugin dependencies.

```json
{
  "capabilities": ["render.device"],
  "determinism": "d0",
  "engine": {
    "maximum_exclusive": "0.2.0",
    "minimum": "0.1.0a1"
  },
  "native": false,
  "platforms": ["linux", "macos", "windows"],
  "plugin_id": "org.ludoweave.example.render-device",
  "plugin_version": "0.1.0a1",
  "protocol": "ludoweave.plugin-manifest/1",
  "python": {
    "maximum_exclusive": "3.15",
    "minimum": "3.12"
  },
  "requires": []
}
```

The checked sample is [`examples/example.plugin.json`](https://github.com/xsparc/ludoweave-engine/blob/main/examples/example.plugin.json).

Manifest v1 recognizes these engine-owned capability IDs:

- `render.backend` and `render.device`;
- `audio.backend`;
- `agent.capture`, `agent.telemetry`, and `agent.test`;
- `resource.adapter`; and
- `simulation.tick_executor`.

The list is deliberately closed. A manifest does not create a new extension
boundary or admit a deferred physics/platform/audio provider merely by naming
one. Unknown capability text is invalid.

## What a manifest cannot say

There is no field for a Python module, callable, packaging entry point, file
path, URL, command, process, environment variable, credential, or provider
object. Unknown fields are rejected. The plugin contracts package does not use
entry-point discovery, importlib, package installation, subprocesses,
networking, arbitrary evaluation, or a global registry.

This keeps project data inert and prevents ambient installed packages from
changing composition. A positive compatibility report is metadata evidence,
not trust, conformance, security, determinism, or provider admission evidence.

Executable WASM fields are equally absent: a manifest cannot name a `.wasm`
artifact, module, entry point, WASI context, or host imports. M16 deliberately
retains this fail-closed boundary. The [WASM-mod security
decision](wasm-mod-security-decision.md) defines the separate threat model and
complete gate that must be satisfied before a superseding executable-mod
proposal can change it.

## Local compatibility check

Check one or more explicitly selected manifests against the current LudoWeave
release, CPython minor, and desktop platform:

```console
ludoweave plugin check examples/example.plugin.json
```

The command emits one canonical JSON document using protocol
`ludoweave.plugin-check/1`. It returns:

- `0` when every manifest is compatible;
- `1` when all documents are valid but one or more compatibility issues exist;
- `2` when a document, path read, or command request is invalid.

Use `--minimum-determinism d1` or `d2` when the composition requires a stronger
tier. Native manifests fail by default; `--allow-native` changes only that
local policy fact and does not override RFC-0001 or any adapter admission gate.

The report checks engine/Python ranges, CPython implementation, platform,
capabilities, native policy, minimum determinism, duplicate identities,
dependency presence/version, ambiguous duplicates, and dependency cycles.
Issue ordering and the manifest-set fingerprint do not depend on input order.
Output includes normalized engine/Python/platform facts and plugin identities,
but never manifest paths or raw environment values.

## Python use

Trusted tooling can decode and check bytes without touching the filesystem:

```python
from ludoweave.plugins import (
    PluginManifest,
    check_plugin_compatibility,
    current_plugin_context,
)

manifest = PluginManifest.from_json(document_bytes)
report = check_plugin_compatibility((manifest,), current_plugin_context())
if not report.compatible:
    for issue in report.issues:
        print(issue.code, issue.plugin_id, dict(issue.details))
```

Filesystem policy belongs to the caller or CLI. The compatibility evaluator is
a pure bounded operation over frozen values and creates no runtime ownership.

## Explicit composition remains required

After a positive report, application code may explicitly import a package it
already trusts, construct the adapter, and inject it. Existing lifecycle,
close, conformance, optional-dependency, and provider-isolation requirements in
the [adapter guide](adapter-guide.md) still apply. Implementations and provider
objects never enter the manifest or canonical world state.

Dependency declarations describe manifest compatibility only. LudoWeave does
not install missing packages or choose versions. Packaging tools and application
owners remain responsible for a reproducible environment and lockfile.
