# Cross-version receipt-corpus readiness

M24 adds a deterministic admission harness for RFC-0003's cross-version gate.
It does not claim that the gate is satisfied. The current reader and every
preserved receipt were produced by `0.1.0a1`, and no supported release evidence
exists in the corpus.

The repository admission manifest is
`tests/fixtures/cross_version_receipt_corpus.json`. It references the immutable
M21 `receipt_v1` manifest by exact byte length and SHA-256. Existing source
manifests and receipt bytes are historical inputs: future corpus growth appends
new version records and must not rewrite an old document to make a new reader
pass.

## Admission rule

Gate 1 can become true only when all of these are true together:

1. every referenced manifest and receipt matches its recorded byte length and
   SHA-256;
2. the installed bounded public reader decodes every receipt and reproduces its
   canonical bytes;
3. the installed reader version differs from at least one preserved source
   version, producing at least two distinct observed package versions; and
4. independently verified supported-release records cover every observed
   source and reader version; and
5. every frozen mandatory source/release prefix remains byte-for-byte present,
   so a newly reviewed manifest cannot replace or omit earlier history; and
6. the exact admission-manifest SHA-256 is pinned by the reviewed evidence
   implementation and strict validator.

The last records contain a version, exact `vVERSION` tag, Git commit identity,
and release-artifact SHA-256. Their structure is necessary but not sufficient:
a review must verify the tag, commit, artifact, and support status against the
actual release channel. A project-owned synthetic test is not release history.
An arbitrary `--corpus` document cannot report a satisfied gate because its
identity is not in the reviewed evidence set. Updating that reviewed identity
alone is insufficient: executable mandatory prefixes freeze the M21 source
identity and, as release records are accepted, the earlier release identities.

Today the report therefore returns:

- `cross_version_execution: false`;
- `supported_release_evidence_complete: false`;
- `gate_satisfied: false`; and
- `status: not-ready`.

## Installed evidence

Run from the repository:

```console
python examples/cross_version_corpus_readiness.py
```

The release sample bundle includes exact copies of the admission manifest and
preserved receipt corpus. The example also accepts an explicitly selected local
manifest:

```console
python examples/cross_version_corpus_readiness.py --corpus tests/fixtures/cross_version_receipt_corpus.json
```

It emits one deterministic
`ludoweave.evaluation.cross-version-receipt-corpus/1` JSON document containing
only versions, protocol/status identities, counts, booleans, reason codes, and
the admission-manifest digest. It emits no receipt/world hash, state value,
path, environment fact, timing, credential, or provider message.

## Ownership, failure, and security

The harness is an explicitly invoked repository/release validation tool, not a
runtime loader. It reads only the selected manifest, safe-basename child
manifests, and their declared receipt files. Manifest bytes, source-manifest
count, fixtures per manifest, receipt bytes, and release-record count are all
bounded before proportional work. Unknown fields, unsafe names, duplicate
versions/files, malformed or extra release records, byte/hash drift, incomplete
status coverage, reader failures, or canonical drift fail closed with path-free
errors.

Execution is synchronous on the calling thread. The harness retains no file
handle, world, provider, process, or global registry. It performs no discovery,
dynamic import, installation, subprocess launch, network access, tag lookup, or
release publication.

## Stability boundary

RFC-0007 records readiness machinery only. RFC-0003 gate 1 remains false;
external consumer feedback and a supported deprecation-capable feature-release
channel also remain absent. Command, transaction, receipt, and reader exports
remain experimental.

M26/RFC-0009 defines admission for that release-channel gate, but its reviewed
release set is empty and the gate remains false.

M24 adds no runtime module, public export, protocol field, operation, handler,
migration, dependency, lock change, package version, workflow job, tag,
release, or publication.
