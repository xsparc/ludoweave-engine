# Windows contained source-access source-commit binding probe

**Status:** Accepted M221 current-repository test evidence; no source
attestation, build provenance, cross-principal proof, independent-host proof,
cleanup authority, or Windows admission has occurred.

M221 composes M220's retained source and three-phase contained access-refusal
observation with a read-only check against one immutable local Git object. The
probe is Windows-only, test-only, offline, fixed-purpose, and fail-closed. It
does not operate on a cache fixture or issue cleanup.

## Contained source-access source-commit binding

The test names the exact M220 commit
`734d4eb943c3da7a1a8357ef3e180cac4353cb6b`, tree, sole parent, repository
path, and blob. A direct, fixed Git invocation verifies the object types and
identities, reads the bounded blob, and requires its exact byte count and
SHA-256. Moving branch names and remote refs are not inputs.

The complete immutable descriptor is the commit, tree, parent, path, and blob;
no subset is accepted as an equivalent identity.

Git runs without a shell or input stream, with a short timeout, bounded
standard output, empty standard error, disabled replacement objects, disabled
optional locks and prompts, and Git-specific environment values replaced by
fixed local settings. Any nonzero exit, unexpected output, type, identity,
size, or content fails the observation.

For each M220 refusal phase, the contender source is retained first. The exact
commit descriptor is resolved, and the retained source matches the committed
blob before child creation. M220 then executes that retained source through
the exact three inherited standard handles while preserving its Job, token,
interpreter-image, access, zero-exit, settlement, and close requirements. The
commit descriptor and retained source are checked again so the committed blob
remains stable after child settlement. Ordinary source access must still
succeed after retained handles close.

## Evidence and authority boundary

This binds the M220 fixed contender bytes used by the current-repository test
to one exact local commit object. It is not a source provenance attestation.
The trusted Git executable and local object store remain outside the measured
boundary. Object transport, repository acquisition, signer identity, trusted
builder inputs, dependencies, imported modules, native DLLs, loader behavior,
and runtime environment remain unbound; build provenance remains unproved.

It does not prove a distinct security principal, hostile executable,
independent host, privileged-bypass resistance, debugger/kernel resistance, or
a cleanup action. Criteria 6 and 7 remain unresolved. Windows is not admitted,
cleanup remains unimplemented and unauthorized, and no public self-hosted
runner is introduced.

M221 adds no runtime source, public API, CLI or MCP command, production
harness, collector, credential or account lifecycle, privilege transition,
filesystem mutation, network listener, dependency, package payload, version,
workflow, permission, secret, hosted allocation, or admission decision.

## Primary references

- [Git cat-file](https://git-scm.com/docs/git-cat-file)
- [Git revisions](https://git-scm.com/docs/gitrevisions.html)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
- [SLSA provenance](https://slsa.dev/spec/v1.2/provenance)
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
- [NIST Secure Software Development Framework publications](https://csrc.nist.gov/Projects/ssdf/publications)
