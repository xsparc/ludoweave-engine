# Windows contained source-access source-commit Git executable selection binding probe

**Status:** Accepted M223 current-repository test evidence; executable-file
identity, source/build provenance, cross-principal proof, independent-host
proof, cleanup authority, and Windows admission have not occurred.

M223 composes a Windows-only, test-only binding around M222's complete
source-commit boundary. It performs no cache-fixture operation and issues no
cleanup.

## Git executable selection binding

The probe performs exactly one PATH/PATHEXT lookup through M221's existing
private selector before entering the M222 observation. That lookup must produce
an existing absolute file. The selector is then scoped to return only that
path while the complete M222 boundary executes M221's three participants.

A subprocess observer requires all 48 fixed Git object reads and requires the
first command element of every read to equal the selected path. M222's direct
no-shell execution, fixed repository, no-input, timeout, bounded output,
empty-standard-error, no-replacement-object, no-lazy-fetch, optional-lock, and
prompt exclusions remain in force. The retained M220 source must still match
the exact commit/path/blob before each child creation and after settlement.

The scoped binding is restored even if the inherited boundary raises or skips.
M221 and M222 sources remain byte-for-byte unchanged.

## Evidence and authority boundary

This is Git executable selection binding only. It does not authenticate the
executable file, its content, signer, origin, ACL, or publisher. Path-target
replacement remains outside the observation, as do native DLL and loader
identity. The local object store remains outside the trust boundary.

This is not a source provenance attestation, and build provenance remains
unproved. Repository acquisition, imported modules, distinct-principal
behavior, hostile or privileged bypass, independent-host evidence, and
debugger/kernel resistance remain unbound. Criteria 6 and 7 remain unresolved.
Windows is not admitted, cleanup remains unimplemented and unauthorized, and
no public self-hosted runner is introduced.

M223 adds no runtime source, public API, CLI or MCP command, production
harness, collector, credential lifecycle, filesystem mutation, network
listener, dependency, package payload, version, workflow, permission, secret,
hosted allocation, cleanup action, or admission decision.

## Primary references

- [Python `shutil.which`](https://docs.python.org/3/library/shutil.html#shutil.which)
- [Python subprocess reliability](https://docs.python.org/3/library/subprocess.html)
- [CreateProcessW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)
- [Git global options](https://git-scm.com/docs/git)
- [SLSA source requirements](https://slsa.dev/spec/v1.2/source-requirements)
- [SLSA build track](https://slsa.dev/spec/v1.2/build-track-basics)
- [GitHub artifact attestations](https://docs.github.com/en/actions/concepts/security/artifact-attestations)
- [GitHub Actions billing](https://docs.github.com/en/actions/concepts/billing-and-usage)
- [NIST SSDF publications](https://csrc.nist.gov/Projects/ssdf/publications)
