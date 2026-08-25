# RFC-0106: Add read-only source-check CLI

- **Status:** Accepted
- **Date:** 2026-08-26
- **Decision owners:** LudoWeave maintainers

## Context

M119-M120 define bounded scene, prefab source, and prefab instance protocols.
M121-M122 add explicit project-confined Python file readers. A human or build
tool can validate those files only by writing Python composition code; the CLI
does not yet expose a read-only source preflight.

Current game-engine command lines support explicit project selection and
headless or batch operation. Godot documents `--path` and `--headless`; Unity
documents explicit `-projectPath`, `-batchmode`, and `-quit` build operation.
Unity also permits custom method execution, while Godot supports script-driven
workflows. M123 deliberately does not adopt arbitrary script execution. JSON
Schema defines validation separately from other document interaction behavior
and publishes structured output schemas. Python `argparse` documents exit 2 for
invalid command-line arguments, matching LudoWeave's established CLI failure
convention.

## Decision

Add one nested standard-library command:

```console
ludoweave source check PROJECT --scene FILE
ludoweave source check PROJECT --prefab FILE --instance FILE
```

The modes are mutually exclusive. Scene mode uses the M121 loader. Prefab mode
uses the M122 loaders for two explicit files and additionally requires exact
`prefab_id` agreement. Mixed scene/instance input and a prefab without its
instance fail as structured invalid arguments.

Success writes one canonical `ludoweave.cli.source-check/1` document to standard
output. It identifies the checked kind and protocol(s), stable scene/prefab and
instance IDs, canonical SHA-256 identities, and entity, dependency, or override
counts. It contains no project root or input path. A normalized source hash is
reported rather than a raw-file hash: semantically equivalent accepted JSON
normalizes to the same canonical identity.

## Failure and security behavior

Project, path, size, JSON, protocol, and document failures retain their existing
structured errors and cause chains. A prefab-pair mismatch uses stable code
`tools.prefab_source_mismatch` with only field context. Runtime source failures
return exit 2, write no success document, and disclose no host path. Ordinary
`argparse` syntax failures retain its documented usage/exit-2 behavior.

The command inherits project confinement, regular-file validation, bounded
one-handle reads, and the cooperative-filesystem rather than race-free-sandbox
qualification from RFC-0104/RFC-0105. It opens no remote transport, provider,
renderer, plugin, native module, or arbitrary source executor.

## Determinism, ownership, and mutation

For the same accepted project manifest, bytes, and decoder limits, output bytes
are canonical and deterministic. Filesystem timing and concurrent external
changes remain outside simulation determinism. Each loader owns and closes its
descriptor before the report is emitted; the command owns no persistent source
handle or background resource.

The command performs no compile, creates no component registry, world, or
session, calls no planner or transaction service, causes no world mutation, and
produces no receipt. Structural validity does not prove that component names or
values are compatible with an application-supplied registry. A caller must
still explicitly compile and apply a transaction to mutate canonical state.

## Boundary

M123 adds no directory discovery, recursive check, glob, suffix/extension
routing, manifest source registration, implicit pairing, cache, dependency
traversal, asset loading, watcher, live update, reimport, source write-back,
arbitrary Python or project-script evaluation, remote/file URI access, new
persistent operation, dependency, lock, package version, Python/root export,
provider, renderer, workflow job, workflow allocation, permission, release
authority, tag, release, publication, push, or public remote change.

The command does not implement or claim general JSON Schema support. Existing
LudoWeave protocol decoders remain the sole validators. The existing CI jobs are
unchanged; regular test coverage runs within their current allocation, and a
standalone local installed-wheel verifier proves the packaged CLI path.

## Alternatives considered

- Require Python composition. Rejected because a stable read-only CLI result is
  useful to humans, hooks, packaging checks, and software tools.
- Add a general import/build command. Rejected because importing introduces
  registry, asset, generated-output, cache, and failure-atomicity policy.
- Compile during check. Rejected because a headless project intentionally has
  no arbitrary dynamic component imports or global registry.
- Discover every source beneath the project. Rejected because ordering,
  duplicate IDs, resource limits, and cache/conflict policy are not defined.
- Execute a user-supplied validation script. Rejected because arbitrary code
  evaluation violates the engine's data-only trust boundary.
- Write a report into the project. Rejected because standard output preserves a
  verifiably read-only project tree and composes with existing tooling.

## References

- [Godot command-line tutorial](https://docs.godotengine.org/en/latest/tutorials/editor/command_line_tutorial.html)
- [Unity command-line build documentation](https://docs.unity3d.com/cn/6000.0/Manual/build-command-line.html)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12)
- [Python argparse documentation](https://docs.python.org/3/library/argparse.html)
- [RFC-0104: project-confined scene file loading](0104-add-project-confined-scene-file-loading.md)
- [RFC-0105: project-confined prefab file loading](0105-add-project-confined-prefab-file-loading.md)
