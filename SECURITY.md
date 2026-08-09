# Security Policy

## Supported versions

LudoWeave `0.1.0a1` is a community-alpha candidate, not a long-term support line. Security fixes are applied on a best-effort basis to the default branch and the current alpha until a version-support policy is announced. Older development snapshots are unsupported.

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability.

Use the repository's **Security** tab and choose **Report a vulnerability** to create a private GitHub security advisory. Include the affected revision, impact, reproduction steps, and any suggested mitigation. Do not include unrelated secrets or personal data.

If private vulnerability reporting is unavailable, use GitHub Support to contact the repository owner rather than disclosing the report publicly.

Maintainers will acknowledge the report through the same private channel, assess impact, coordinate a fix when warranted, and credit reporters who request attribution. No response or remediation deadline is guaranteed during community alpha.

## Release supply chain

- The baseline wheel has no runtime dependencies and is built as `py3-none-any`.
- Release candidates include SHA-256 checksums, an SPDX SBOM, Apache/project notices, and a versioned manifest.
- The tag workflow uses immutable action revisions and grants write, identity-token, and attestation permissions only to the release job.
- M39 requires the exact release ref to be an annotated tag whose signature
  GitHub reports as valid, whose local/GitHub target is the checked-out commit,
  and whose commit is reachable from `origin/main`. The validator is loaded
  from fetched `origin/main`, not from the unadmitted tag checkout.
- Official tagged artifacts receive GitHub build-provenance and SBOM attestations. Consumers should verify both the local checksums and hosted attestations as documented in `docs/release-process.md`.
- M40 keeps the GitHub release as an unpublished prerelease draft while the
  workflow verifies that every authenticated API asset is fully uploaded and
  exactly matches local staging by safe name, byte size, and SHA-256 digest.
  Failed verification leaves the draft for inspection and never clobbers an
  existing asset.
- M41 also requires the authenticated draft's source `body` to exactly match
  bounded staged `RELEASE_NOTES.md` before publication. It rejects missing,
  null, substituted, truncated, or normalization-different notes without
  emitting their content.
- M42 retains the exact authenticated release database ID across publication
  and rechecks the final public prerelease state, valid UTC publication time,
  notes, and assets before the release job can succeed.
- M43 retrieves every validated numeric asset ID through the authenticated
  binary asset endpoint and rehashes the complete downloaded set against the
  same published release document before the release job can succeed.
- M44 then verifies SLSA v1 provenance for every retrieved asset and an SPDX
  2.3 SBOM attestation for the one pure wheel, constrained to the exact
  repository, tag, source/signer commit, release workflow, GitHub OIDC issuer,
  hosted runner class, and bounded candidate count.
- M45 then fetches the exact public release and asset IDs without supplying a
  GitHub credential, revalidates the bounded downloaded set, and runs complete
  isolated release smoke against those public bytes.
- M46 repeats the bounded public retrieval and installed smoke from a dependent
  fresh Linux runner with read-only contents permission. It retrieves the exact
  admitted candidate through the pinned same-workflow artifact channel and
  supplies no release credential to public HTTP requests.
- M47 replaces the Bash-only verifier with one typed standard-library Python
  program and expands that tag-only fresh rehearsal to Ubuntu, Windows, and
  macOS. Each runner creates its own bounded plan and isolated installation;
  all retain read-only contents permission and credential-free public requests.
- No PyPI trusted-publishing or upload step exists in community alpha.
- M26 release-channel evidence is offline and empty; it does not publish,
  download, resolve, or establish a supported release channel.
- M27 contributor-rehearsal evidence is offline and empty. Future reviewed
  evidence may contain a public login and project references, but must exclude
  email, private correspondence, credentials, prompts, telemetry, and other
  unpublished personal data.
- M39 does not define a signer/key allowlist, local trust store, or workflow-
  file self-authentication. Repository tag rules, deployment-environment
  approval, signing-key lifecycle, and workflow governance remain operational
  controls; report suspected unauthorized tag/workflow changes privately.
- M40 does not enable or claim immutable releases, independently verify GitHub
  storage, or replace build/SBOM attestations. Release immutability and failed-
  draft cleanup remain explicit repository operations.
- M41 compares the API source body, not GitHub's rendered Markdown; it does not
  validate links or factual completeness, sanitize maintainer-authored text, or
  replace human release review.
- M42 observes the authenticated state only after publication. Failure blocks
  a successful job result but does not automatically unpublish, delete, or
  mutate evidence, prevent later edits, or claim immutable-release policy.
- M43 writes only an exclusive bounded runner-temporary retrieval plan and new
  temporary download files. It neither clobbers nor mutates release assets and
  does not prove unauthenticated availability, all CDN/cache paths, future
  bytes, immutability, consumer installation, or attestation verification.
- M44 attestation identity and subject verification does not establish
  artifact security, an independent or trusted build, predicate truth beyond
  the constrained type/identity, future availability or non-revocation,
  immutable release state, consumer installation, or a supported channel.
- M45 observes one fixed public GitHub API path on the same hosted Linux runner.
  It does not establish an independent or external consumer, a clean-machine or
  cross-platform matrix, every browser/CDN/cache/geographic path, future
  availability, immutability, artifact security, PyPI, or a supported channel.
- M46 adds workspace/runner separation but remains inside the same GitHub-hosted
  workflow and uses scoped checkout/artifact services. M46 alone is not a
  cross-platform public matrix.
- M47 supplies the three supported hosted operating-system observations but
  remains inside the same workflow, repository, account, and provider. It is
  not independent or external verification, a clean machine outside that
  provider, every delivery path, future availability, immutability, artifact
  security, PyPI, or a supported channel.

## Initial security boundaries

- The M5 agent interface is local-only and provides no network listener or remote-control claim. MCP is confined to process stdio.
- The CLI performs no arbitrary Python evaluation.
- M2 artifact paths are bounded, project-relative, resolved beneath an explicitly selected project root, and reported only by stable roles in expected diagnostics.
- Input files are read through one bounded open handle; stale size metadata cannot cause an unbounded read.
- Project confinement protects normal workflows and static symlink/traversal mistakes. It is not a sandbox against a hostile local principal concurrently replacing files, directories, junctions, or symlinks inside the selected project tree; run commands only against a locally trusted, quiescent project directory.
- The M2 CLI project manifest is data-only and cannot select Python modules, callables, components, or plugins.
- M12 plugin manifests are exact-schema inert compatibility metadata. They do
  not discover, import, install, resolve, or execute code, and unknown
  executable fields fail closed.
- M16 adds no WASM runtime, loader, guest ABI, WASI context, host call, or mod
  package. Untrusted WebAssembly is not executed. ADR-0030 requires a complete
  least-privilege, resource, determinism, lifecycle, persistence, isolation,
  conformance, supply-chain, and maintenance gate before that boundary may
  change.
- Diagnostics must not expose environment variables or credentials.
- Agent-facing mutations are typed, validated, capability-gated, caller-attributed, serialized at safe points, and return canonical receipts. Write access is disabled by default.
- Agent requests, results, transactions, ticks, queries, snapshots, captures, tests, and call rates are bounded. Credential-shaped diagnostics and telemetry values are redacted.
- The MCP adapter cannot launch a shell, evaluate Python, load a module named by request data, or open a socket. Anyone able to launch the process and access its stdio has the capabilities granted by that composition root.

## Future executable-mod reports

Treat any unexpected plugin-driven import, execution, dynamic loading, WASM
instantiation, ambient filesystem/network/process access, or world mutation
without a canonical receipt as a security report. Also report any accepted
plugin-manifest field outside its documented exact schema. Use the private
reporting route above; do not attach hostile modules or sensitive files to a
public issue.

The [M16 WASM-mod security decision](docs/wasm-mod-security-decision.md)
records the prospective assets, actors, entry points, trust boundaries,
blocking findings, verification requirements, and residual risk. Its findings
are feature-admission blockers, not claims of a current executable-mod
vulnerability.
