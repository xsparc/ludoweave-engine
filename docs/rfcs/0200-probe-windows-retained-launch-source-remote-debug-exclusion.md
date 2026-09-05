# RFC-0200: Probe Windows retained launch-source remote-debug exclusion

**Status:** Accepted
**Milestone:** M217
**Decision class:** Direction-preserving

## Context

M215 executes the fixed participant through a retained source handle, and M216
observes that the live handle refuses competing write/delete access until
settlement. The fixed direct launch remains `pythonw.exe -I -B -`. Python 3.14
adds the PEP 768 remote-debug interface and documents
`-X disable_remote_debug` as an interpreter-startup exclusion switch.

The smallest next observation is whether that exclusion option composes with
the complete frozen M212-M216 boundary. This does not require enabling or
attempting the remote interface, opening process memory, changing a fixture,
or adding a product surface.

## Decision

Adopt the test-only [Windows retained launch-source remote-debug exclusion
probe](../security/windows-cache-cleanup-retained-launch-source-remote-debug-exclusion-probe.md).

Validate the canonical pipe name through M215's frozen composer, then launch
the same direct interpreter with exact arguments
`-I -B -X disable_remote_debug - <canonical-pipe-name>`. Scope the alternate
composer only to process creation and restore M215's composer afterward.

Require the entire M216 retained-source access-refusal lifecycle, native
client/session/DACL binding, same-logon token binding, executable-image
binding, source stability, release, settlement, post-settlement access, and
zero owned handles to remain intact. The probe performs no remote attachment,
injection, or memory access and performs no content or namespace mutation.

On Python 3.14 the option has the documented remote-debug exclusion meaning.
Python 3.12 and 3.13 accept arbitrary `-X` names, so their runs prove only
launch and lifecycle compatibility. This decision is direction-preserving and
makes no collection or cleanup authority increase. Criteria 6 and 7 remain
unresolved, Windows remains unadmitted, and cleanup remains unimplemented and
unauthorized.

## Consequences

- The exact exclusion launch can be required by a later private Windows
  harness proposal without changing the M215 composer or product runtime.
- Python 3.14 supplies the meaningful exclusion observation; 3.12 and 3.13
  remain useful compatibility coverage without an inflated security claim.
- No enabled/disabled remote-attack pair is attempted, so the evidence is
  compositional rather than adversarial.
- Source-commit provenance, imported-module binding, privileged bypasses,
  hostile-process behavior, distinct-principal and independent-host evidence,
  fixture mutation, collection, criteria 6/7, and Windows admission remain
  separate work.
- Local validation adds zero GitHub Actions jobs or hosted allocation.

## Alternatives rejected

### Exercise remote execution against the participant

Rejected because a remote attachment or script-injection attempt would expand
the test into a materially different offensive process-control surface. M217
only establishes that the documented exclusion launch composes with the
existing retained boundary.

### Modify M215's frozen command composer

Rejected because M215 is accepted evidence. A scoped test-only composition
keeps its exact artifact immutable and proves the additional option without
rewriting history.

### Add a product switch or hosted Windows job

Rejected because M217 is a local design-risk probe. It makes no collection or
cleanup authority increase and adds zero GitHub Actions jobs or hosted
allocation.
