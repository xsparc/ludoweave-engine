# ADR-0012: Data-only CLI composition and project-relative path confinement

- **Status:** Accepted
- **Date:** 2026-08-05

## Context

M2 needs command, snapshot, replay, and diff CLI acceptance without introducing
arbitrary Python evaluation, dynamic imports from untrusted project files, a
scene format, or a plugin system. Domain command/replay services intentionally
contain no filesystem or transport behavior, so the CLI composition root must
own path policy and artifact I/O.

Accepting unrestricted input/output paths would allow a project command to read
or replace files outside the selected project. Including ambient paths,
hostnames, or environment values in machine diagnostics would also make errors
unsafe and nondeterministic.

## Decision

M2 CLI workflows use an explicit data-only
`ludoweave.headless-project/1` manifest named `ludoweave.project.json`. It
declares a world ID, unsigned 64-bit seed, caller-chosen stable platform
profile, and SHA-256 dependency-lock identity. Its complete canonical bytes
form the project-schema hash.

This composition intentionally registers no components or resources and uses a
deterministic no-op tick executor. It can exercise entity lifetime, exact tick
progression, commands, receipts, snapshots, hashes, replay, checkpoints, and
diffs without pretending that a general project/component loading format
exists. Game-specific Python composition remains a trusted application concern
until a separately designed project schema/plugin boundary exists.

The `apply`, `snapshot`, `replay`, and `diff` adapters accept one explicitly
selected project directory. Every artifact argument is a bounded relative path.
Both POSIX and Windows absolute/drive/root forms are rejected, resolved paths
must remain beneath the real project root, inputs must be regular files, and
outputs use a same-directory temporary file plus atomic replacement. Expected
errors expose only stable roles/codes, never resolved paths or environment
values.

Inputs are opened once, checked as regular files through the open handle, and
read with a hard `limit + 1` cap so file growth cannot cause an unbounded
allocation. Snapshot artifacts also carry the selected manifest's project,
lock, and platform binding. The CLI is not a sandbox against another local
principal concurrently replacing project directories or path ancestors; the
selected project tree must be locally trusted and quiescent during a command.

The CLI parses the same `CommandTransaction`, calls the same
`TransactionService` through `ReplayRecorder`, and emits the exact canonical
`TransactionReceipt` returned by direct Python use. Filesystem code remains in
`ludoweave.tools` and cannot be imported by `ludoweave.world` or
`ludoweave.ecs`.

## Consequences

- The installed wheel supports a complete headless M2 workflow with no compiler,
  GPU, network listener, dynamic import, or arbitrary evaluation.
- A CLI and direct service applied to the same empty-project state produce
  equivalent receipts.
- Static project-relative path traversal, absolute paths, drive-relative
  Windows paths, and symlink escapes are rejected; bounded handle reads close
  the stale-size allocation gap.
- The initial CLI format is deliberately not a general game project format.
  Components, resources, scenes, assets, and Python plugin loading are not
  implied.
- Multiple output artifacts are individually atomic. The in-memory authority
  session is process-local; an output failure cannot partially mutate an
  external live engine.

## Alternatives considered

Importing a Python project module named in the manifest was rejected because it
would make untrusted data select executable code. Defining dynamic component
classes from JSON was rejected as a premature game-project schema. Allowing
arbitrary filesystem paths was rejected because project confinement is an M2
security requirement. Moving path resolution into replay/snapshot domain
services was rejected because transport concerns must remain at the tools
composition root.
