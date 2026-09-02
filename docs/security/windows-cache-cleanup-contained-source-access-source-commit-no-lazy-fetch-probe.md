# Windows contained source-access source-commit no-lazy-fetch probe

**Status:** Accepted M222 corrective current-repository test evidence; no
source attestation, build provenance, cross-principal proof, independent-host
proof, cleanup authority, or Windows admission has occurred.

M222 corrects M221's source-commit reader so its direct local Git object queries
categorically exclude lazy object fetching. The probe is Windows-only,
test-only, fixed-purpose, read-only, and fail-closed. It does not operate on a
cache fixture or issue cleanup.

## Source-commit no-lazy-fetch exclusion

Git may request a missing object from a configured promisor remote. Every M221
object query now includes the global `--no-lazy-fetch` option before repository
and plumbing arguments. The sanitized child environment also fixes
`GIT_NO_LAZY_FETCH=1` after removing every ambient `GIT_*` value. An ambient
attempt to set lazy fetching to `0` or redirect the object directory cannot
cross the invocation boundary.

A regression spies on the exact subprocess call and preserves M221's resolved
executable, fixed repository root, no-shell, no-input, timeout, output bounds,
empty-standard-error, replacement-object, optional-lock, and prompting rules.
It also runs the complete M221 source-commit binding boundary. The retained
M220 contender source must therefore still match the exact fixed commit/path/
blob before child creation and after settlement.

Historical M221 evidence is not rewritten. Its earlier offline wording was
stronger than the implementation because prompt and environment sanitization
did not exclude a configured promisor transport. M222 makes that current-tree
claim match the executable boundary.

## Evidence and authority boundary

The correction excludes one implicit object-retrieval path. The trusted Git
executable and local object store remain outside the measured boundary. It is
not a source provenance attestation; repository acquisition, signer identity,
builder identity, dependency inputs, imported modules, native DLLs, loader
behavior, and runtime environment remain unbound. Build provenance remains
unproved.

It does not prove a distinct security principal, hostile executable,
independent host, privileged-bypass resistance, debugger/kernel resistance, or
a cleanup action. Criteria 6 and 7 remain unresolved. Windows is not admitted,
cleanup remains unimplemented and unauthorized, and no public self-hosted
runner is introduced.

M222 adds no runtime source, public API, CLI or MCP command, production harness,
collector, credential or account lifecycle, privilege transition, filesystem
mutation, network listener, dependency, package payload, version, workflow,
permission, secret, hosted allocation, or admission decision.

## Primary references

- [Git global options](https://git-scm.com/docs/git)
- [Git cat-file](https://git-scm.com/docs/git-cat-file)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
- [SLSA build track](https://slsa.dev/spec/v1.2/build-track-basics)
- [GitHub Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
