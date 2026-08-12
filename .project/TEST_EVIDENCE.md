# Test Evidence

Only commands actually executed in the current repository are recorded here.

## M71 local development evidence - 2026-08-13, Windows, CPython 3.12

M71 starts from exact synchronized M70 closeout
`f62631e2541f8f6a34b0ed84f489c2d7f9503747`, tree
`f1e8ecc9b0d681a6fb4006354c8d983b2f4f119c`. The worktree was clean and only
`main` existed locally and remotely before the neutral branch was created.

| Command or review | Exit | Result |
| --- | ---: | --- |
| Focused primary-source direction scan | Advisory | Python 3.12 documents binary spooled temporary file objects and seekable `ZipFile` file-object input; CWE-367 motivates reducing separation between resource validation and use; SLSA describes consumer artifact digest verification. The selected response is one bounded private checksum-admitted parser snapshot, not a source-immutability or general archive-safety claim. |
| `uv run --frozen pytest -q tests/architecture/test_m71_checksum_admitted_sample_snapshot.py --basetemp D:\LudoWeaveValidation\m71\baseline` | 1 | Seven assertions failed and two producer/protected-surface guards passed in 0.36 seconds against exact M70. The snapshot helper, source-independent exact-byte copy, distinct owned parser input, ordering contract, RFC, and documentation were absent; `ZipFile` still received the source descriptor. |
| Runtime/test implementation checkpoint | 1 | M70/M71 produced 13 passing assertions and only the deliberately absent M71 documentation/RFC assertion failed in 0.41 seconds. Strict Pyright reported zero findings. Ruff reported only import ordering in the two files that added the `IO` type; no behavior defect remained in this checkpoint. |
| First inherited M64-M71 chain | 1 | M71 itself passed 9 assertions and static/docs checks passed, but one M68 source-text assertion still required `ZipFile` to receive the source descriptor directly. M71 intentionally supersedes only that detail; the guard was updated to retain path/descriptor admission ordering and require the snapshot copy before parser construction. |
| Focused implementation/static/docs gate | 0 | Four affected Python files were format clean; Ruff and strict Pyright reported zero findings. M71 passed 9 assertions in 0.29 seconds; M64-M71 passed 90 assertions with 1 local capability skip in 0.90 seconds. Strict docs built in 1.20 seconds with only the known upstream Material notice, and whitespace passed. |
| Lock, environment, whole-tree static, and CPython 3.12 gate | 0 | The unchanged lock resolved 46 packages and the locked graphics environment checked 45 packages. All 314 Python files were format clean; Ruff and strict Pyright reported zero findings. CPython 3.12 passed 2,309 non-wgpu tests with 15 skips in 115.17 seconds. |
| Architecture and supported-Python gate | 0 | All 779 architecture assertions passed with 1 local capability skip in 5.53 seconds. CPython 3.13 passed 2,309 tests with 16 skips in 107.67 seconds; CPython 3.14 passed 2,309 with 16 skips in 111.16 seconds. The CPython 3.12 graphics environment was restored afterward. |
| Real-wgpu, profiles, and vertical slices | 0 | All 10 real-wgpu tests passed in 8.28 seconds. Five-repeat base and graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, and replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`. |
| M1-M4 diagnostic benchmark validators | 0 | All four stored artifacts validate. M1 recorded seven workloads and observed one of two targets; M2 validated four informational workloads with no targets; M3 validated six workloads and observed neither target; M4 validated three workloads and observed its baseline target. These remain diagnostic evidence, not release gates. |
| Pre-review reproducible distribution and release gate | 0 | Two builds reproduced a pure 273,524-byte wheel at `791f2c909cf9b89381443f0b89d6baa79ed56f7a0bd96fa7de4d09521f597671` and a 1,225,504-byte sdist at `ef631bcdb169baa8e41036cafaaa0720edd38402db127847fb9a683e3d8e3166`. Installed-wheel smoke, deterministic ten-artifact staging, and complete release smoke passed. The 111,168-byte 50-entry sample ZIP has SHA-256 `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`; the wheel has 94 entries, the sdist 508, and no inspected archive contains native/WASM entries. |
| Findings-first review | No finding | Exact scope is 18 paths. No workflow, runtime package, sample producer, benchmark, dependency, package metadata, lock, credential/private-key marker, or explicit development-tool identity marker changed. RFC-0054 accurately confines the claim to the private bounded parser snapshot. Review strengthened runtime proof by observing `ZipFile` receive the distinct snapshot and by checking both owned streams close after checksum failure. |
| `uv run --frozen ruff format --check tests/architecture/test_m71_checksum_admitted_sample_snapshot.py`; Ruff; strict Pyright; focused pytest | 0 | The strengthened regression file was already formatted, Ruff clean, and strict-Pyright clean; all 10 M71 assertions passed in 0.28 seconds. |
| Record-inclusive lock/static/architecture/docs/Git-object gate | 0 | The unchanged lock resolved 46 packages in 0.74 ms; the graphics environment checked 45 packages. All 314 files were format clean; Ruff and strict Pyright reported zero findings; all 780 architecture assertions passed with 1 local capability skip in 5.49 seconds; strict docs built in 1.25 seconds with only the known upstream notice; whitespace passed; full Git-object checking reported only pre-existing unreachable objects and exited zero. |
| Record-inclusive reproducibility and release gate | 0 | Two builds reproduced the feature-identical pure 273,524-byte wheel at `791f2c909cf9b89381443f0b89d6baa79ed56f7a0bd96fa7de4d09521f597671` and a 1,227,248-byte record-updated sdist at `530ebef65bd489cf16a74760c84d4b308fc9180b62849345da4bf70b19349de0`. Installed-wheel smoke, deterministic ten-artifact staging, and complete release smoke passed. Recording this result changes the sdist; exact commit artifact identity is delegated to hosted qualification. |
| Final frozen lock/static/architecture/docs/whitespace gate | 0 | The unchanged lock resolved 46 packages in 0.78 ms; all 314 files were format clean; Ruff and strict Pyright reported zero findings; all 780 architecture assertions passed with 1 local capability skip in 5.32 seconds; strict docs built in 1.33 seconds with only the known upstream notice; whitespace passed. |
| Exact prepublication scope/history/remote audit | Clean | After `git fetch --prune origin`, feature `HEAD`, local `main`, and `origin/main` all resolve to exact M70 closeout `f62631e2541f8f6a34b0ed84f489c2d7f9503747`; the symmetric difference is `0 0`. History is linear through the verified M70 feature/integration/closeout sequence. The candidate is exactly 18 intended paths. GitHub reports no open pull request, only remote `main`, no tag, and no release. Changed content contains no credential/private-key or explicit development-tool identity marker. |

## M70 local development evidence - 2026-08-13, Windows, CPython 3.12

M70 starts from exact synchronized M69 closeout
`55b409d40c32c9268ee62b8c2a14aa036bcc935f`, tree
`51b5bdfad0a139d141ea4ea2c0195fa8ece72d6c`. The worktree was clean and only
`main` existed locally and remotely before the neutral feature branch was
created.

| Command or review | Exit | Result |
| --- | ---: | --- |
| Focused primary-source direction scan | Advisory | Python 3.12 documents seekable file-object ZIP input and binary hashing; CWE-367 describes changes between resource check and use; SLSA describes consumer artifact verification. The selected response is a same-opened-handle digest comparison before parsing and before publication, not an immutable-input guarantee. |
| Initial focused command with missing `D:\LudoWeaveValidation\m70` parent | Invalid setup | Pytest produced 5 setup errors, 2 failures, and 1 pass because the requested basetemp parent did not exist. This is an environment/setup failure and is not counted as the behavioral baseline. |
| `uv run --frozen pytest -q tests/architecture/test_m70_sample_archive_checksum_binding.py --basetemp D:\LudoWeaveValidation\m70\baseline` | 1 | Seven assertions failed and one protected-surface guard passed in 0.28 seconds against unchanged M69 code. The helper/signature, two same-handle comparisons, main call, ordering contract, RFC, and public documentation were absent. |
| Runtime/test implementation checkpoint | 1 | Seven assertions passed and only the deliberately absent documentation/RFC assertion failed in 0.30 seconds. This proves the code checkpoint, not the completed milestone. |
| Focused implementation, static, docs, and whitespace gate | 0 | Both changed Python files were already formatted and passed Ruff; strict Pyright reported zero findings. M70 passed 8 assertions in 0.26 seconds; inherited M64-M70 passed 84 assertions with 1 local capability skip in 0.71 seconds. Strict docs built in 1.22 seconds with only the known upstream Material notice, and whitespace passed. |
| Initial full-gate launch under managed sandbox | Environment failure | Six sequential uv commands each failed before execution because the sandbox denied access to `C:\Users\louij\AppData\Local\uv\cache\sdists-v9\.git`. The identical gate was rerun with approved cache access; the denied attempt is not test evidence. |
| Lock, environment, whole-tree static, and CPython 3.12 gate | 0 | The unchanged lock resolved 46 packages in 0.80 ms and the restored graphics environment checked 45 packages in 4 ms. All 313 Python files were format clean; Ruff and strict Pyright reported zero findings. CPython 3.12.13 passed 2,303 non-wgpu tests with 15 skips in 100.21 seconds. |
| Architecture and supported-Python gate | 0 | All 773 architecture assertions passed with 1 local capability skip in 4.89 seconds. CPython 3.13.13 passed 2,303 tests with 16 skips in 100.65 seconds; CPython 3.14.5 passed 2,303 with 16 skips in 106.49 seconds. The locked CPython 3.12 graphics environment was restored with 45 packages. |
| Real-wgpu, profiles, and vertical slices | 0 | All 10 real-wgpu tests passed in 9.07 seconds. Five-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`, 3 draws, and 16 sprites. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, 6 query matches, 5 replay batches, and passing registered tests. |
| Diagnostic M1-M4 benchmark gate | 0 | All four fresh dirty-tree artifacts validated. M1 accepted 7 workloads with 1 of 2 historical targets observed; M2 accepted 4 informational workloads with no timing targets; M3 accepted 6 workloads with 0 of 2 historical targets met; M4 accepted 3 workloads with its baseline target observed. These are diagnostic measurements, not regression, support, release, or native-admission claims. |
| Reproducible distribution and release gate | 0 | Two builds reproduced a pure 273,388-byte wheel at `865d6a8275886ecb3dab9e407c6401ab3eccf2e63a25a07ace91c4a641406f11` and a 1,216,959-byte source archive at `892b2cefdf9300f87d504dca89cf1a4cf654f46e77cea0c3b9366c6717372dc6`. Installed-wheel smoke, deterministic ten-artifact staging, and complete M70 release smoke passed. The wheel has 94 entries, the sdist 506 including the M70 test/RFC, and the 50-member sample has SHA-256 `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`; no inspected archive contains native/WASM content. This factual row changes the sdist afterward, so exact commit-tree artifact identity remains delegated to hosted qualification. |
| Findings-first review | Corrected | The first implementation read until EOF after descriptor admission. A concurrently growing source could therefore make checksum work exceed M68's 16 MiB bound. The sample-specific hash now reads at most 16 MiB plus one rejection byte, rewinds, and uses the same stable mismatch. A synthetic unbounded stream proves the cap. No general artifact hash, workflow, dependency, producer, runtime, or release-authority surface changed. |
| Review-corrected focused/static/docs gate | 0 | Ruff formatted the added regression and then reported no findings; strict Pyright was clean. M70 passed 9 assertions in 0.32 seconds; M64-M70 passed 85 assertions with 1 local capability skip in 0.78 seconds; strict docs built in 1.36 seconds with only the known upstream notice; whitespace passed. |
| Review-corrected CPython gate | 0 | The complete CPython 3.12.13 non-wgpu suite passed 2,304 tests with 15 skips in 110.05 seconds. The corrected M64-M70 contract passed 85 assertions with 1 local capability skip on CPython 3.13.13 in 1.16 seconds and CPython 3.14.5 in 1.21 seconds. The locked CPython 3.12 graphics environment was restored with 45 packages. |
| Record-inclusive static, architecture, docs, and Git gate | 0 | The unchanged lock resolved 46 packages in 0.98 ms; all 313 Python files were format clean; Ruff and strict Pyright reported zero findings; all 774 architecture assertions passed with 1 local capability skip in 5.99 seconds; strict docs built in 1.23 seconds with only the known upstream notice; whitespace and `git fsck --full --no-dangling` passed. |
| Reviewed reproducible distribution and release gate | 0 | Two builds reproduced the same pure 273,388-byte wheel at `865d6a8275886ecb3dab9e407c6401ab3eccf2e63a25a07ace91c4a641406f11` and a 1,219,320-byte source archive at `acb09696c3f920423262c81fdacd1d072eb00491a7028c0b48b3124e6f3aafb2`. Installed-wheel smoke, deterministic ten-artifact staging, and complete M70 release smoke passed. This factual row changes the sdist afterward, so exact commit-tree artifact identity remains delegated to hosted qualification. |
| Scope, protected-surface, credential, and metadata-identity audit | 0 | The candidate has exactly 15 intended paths: the private release verifier, one M70 regression, one accepted RFC, eight public release/security/architecture/index/nav documents, and four neutral project records. Pull-request/release workflows, runtime source, sample producer, benchmarks, pyproject, and lock are unchanged. CI, release-workflow, producer, pyproject, and lock SHA-256 values remain `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`, `c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5`, `d6533cb45eac8d87e0ea47a59c0e03271e3e89bc38eea5c6db690785cfa131ca`, `42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1`, and `e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed`. Changed content has zero credential/private-key and zero explicit development-tool identity matches. Only `main` plus the intended neutral M70 branch exist locally; only `origin/main` exists remotely. |
| Record-frozen qualification | 0 | The unchanged lock resolved 46 packages in 0.86 ms; all 313 files were format clean; Ruff and strict Pyright reported zero findings; all 774 architecture assertions passed with 1 local capability skip in 5.25 seconds; strict docs built in 1.23 seconds with only the known upstream notice; whitespace and full Git-object checking passed. |

## M70 hosted feature evidence - 2026-08-12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Ready PR #162 run `31611083245` | 0 | Exact DCO head `7dfadaf72e74ee29d5fc0c98ef6484f6fec423a8`, tree `7a3ac1bb2ef9f89934325fb44228d770881c0528`, passed in exactly three Linux-first allocations. Linux job `94162276734` passed in 7m12s; only then did macOS `94164509233` and Windows `94164509371` begin, passing in 3m08s and 4m08s. |
| Hosted supported-Python and static/docs gates | 0 | All 313 files were format clean; Ruff and strict Pyright were clean; strict docs built in 1.56 seconds. Linux CPython 3.12 passed 2,319 tests. Ubuntu 3.13/3.14 and macOS/Windows 3.14 each passed 2,319 tests with 1 expected skip. |
| Hosted graphics, profiles, examples, distribution, and smoke | 0 | Every allocated OS passed 10 real-wgpu tests, its graphics profile, Clockwork Arena, and Agent World Builder; Linux also passed the base profile. Two exact-head builds reproduced a pure 273,374-byte wheel at `18390d39f6c267fedb832e41a0b030a03838a04c9c574fc159b45e263d67e91a` and a 1,220,441-byte source archive at `f3c9705985eb8bc3a12d71147269c181149c3dcbb77d3aa47c183b4236310790`. Installed-wheel smoke, deterministic ten-artifact staging, and complete M70 release smoke passed. |
| Delayed exact-head review audits | 0 | Two separated audits found no issue comment, review, inline comment, or review thread. PR #162 remained ready, clean, mergeable, exact-head, exact-base, and fully checked. |
| Feature squash verification | 0 | PR #162 squash `cae3454089b4f0453859360de00129399533e2d7` has tree `7a3ac1bb2ef9f89934325fb44228d770881c0528`, exactly matching reviewed head `7dfadaf72e74ee29d5fc0c98ef6484f6fec423a8`; its sole parent is exact M69 closeout `55b409d40c32c9268ee62b8c2a14aa036bcc935f`. GitHub reports a valid signature verified at `2026-08-12T15:26:46Z` and an exact DCO trailer. The remote branch returns 404, and the exact-tree-equivalent local feature branch was deleted. |

## M70 integration-record local evidence - 2026-08-13, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Four-file documentation and architecture gate | 0 | The unchanged lock resolved 46 packages in 0.79 ms. All 313 Python files were format clean; Ruff and strict Pyright reported zero findings; all 774 architecture assertions passed with 1 local capability skip in 5.27 seconds; strict docs built in 1.25 seconds with only the known upstream notice; whitespace and full Git-object checking passed. The diff is exactly the three neutral `.project` records plus `ROADMAP.md`, with no substantive change from verified feature squash `cae3454`. |
| Reproducible distribution and smoke | 0 | Two builds reproduced the feature-identical pure 273,388-byte wheel at `865d6a8275886ecb3dab9e407c6401ab3eccf2e63a25a07ace91c4a641406f11` and a 1,221,890-byte record-updated source archive at `af404f69f25311480130913367a1459deb21437cd0b9a800963a886bde0cee6a`. Installed-wheel smoke, deterministic ten-artifact staging, and complete M70 release smoke passed. This factual row changes the sdist afterward, so exact integration-commit artifact identity remains delegated to hosted qualification. |
| Record-frozen scope and hygiene gate | 0 | The unchanged lock resolved 46 packages in 0.84 ms; all 313 files were format clean; Ruff and strict Pyright were clean; all 774 architecture assertions passed with 1 capability skip in 6.06 seconds; strict docs built in 1.30 seconds with only the known upstream notice; whitespace and full Git-object checking passed. The diff remains exactly four record/roadmap files, with zero credential/private-key and zero explicit development-tool identity matches. |

## M70 hosted integration-record evidence - 2026-08-12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Ready PR #163 run `31612786971` | 0 | Exact four-file DCO head `dda00757d1ee9365f2f3fbeddc0b89183585c9d2`, tree `29673a50d7bf46c7f56850117e4edd0c6f99eab8`, passed in one 36-second Linux allocation, job `94168073709`. Desktop umbrella job `94168302942` skipped with zero steps. No compatibility interpreter, software-rendering runtime, full suite, profile, graphics, example, or desktop runner executed. |
| Hosted documentation, distribution, and smoke | 0 | All 313 Python files were format clean; Ruff was clean; strict docs built in 1.19 seconds; all 775 documentation-selected architecture assertions passed in 7.19 seconds. Two builds reproduced the feature-identical 273,374-byte wheel at `18390d39f6c267fedb832e41a0b030a03838a04c9c574fc159b45e263d67e91a` and a record-updated 1,222,477-byte source archive at `aa903ca95706abac5f31b7f27ee0f8855e7b19162074c4a0fe422388f3e17c38`. Installed-wheel smoke, deterministic staging, and complete M70 release smoke passed. |
| Delayed exact-head integration review audits | 0 | Two separated audits found no issue comment, review, inline comment, or review thread. PR #163 remained ready, clean, mergeable, exact-head, exact-base, and fully checked. |
| Integration squash verification | 0 | PR #163 squash `504d5bbe7c3ee46c71023d77748d27abd3484c74` has tree `29673a50d7bf46c7f56850117e4edd0c6f99eab8`, exactly matching reviewed record head `dda00757d1ee9365f2f3fbeddc0b89183585c9d2`; its sole parent is exact feature squash `cae3454089b4f0453859360de00129399533e2d7`. GitHub reports a valid signature verified at `2026-08-12T15:34:14Z` and an exact DCO trailer. The remote branch returns 404, and the exact-tree-equivalent local integration branch was deleted. |

## M70 closeout local evidence - 2026-08-13, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Exact three-record closeout gate | 0 | All 774 architecture assertions passed with 1 local capability skip in 5.49 seconds; strict docs built in 1.28 seconds with only the known upstream Material notice; whitespace and full Git-object checking passed. The closeout changes exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md`; it changes no workflow, runtime, verifier, producer, dependency, package, test, public documentation, or roadmap surface and is excluded from hosted CI. Added/current changed content scans found zero credential/private-key or explicit development-tool identity markers. |

## M69 local development evidence - 2026-08-12, Windows, CPython 3.12

M69 starts from exact synchronized M68 closeout
`fec3df4d490d363a9ab538f6b99ec86859e7acdc`, tree
`519955303ba8638ed9847df6b0d9cb62ded25436`. The worktree was clean;
`main`, `origin/main`, and `origin/HEAD` matched; only `main` existed locally
and remotely before the neutral feature branch was created.

| Command or review | Exit | Result |
| --- | ---: | --- |
| Focused primary-source direction scan | Advisory | Python 3.12 documents encrypted-member decryption and password-bearing reads; CPython performs traditional/strong encryption handling during member-open and can include the archive member identity in its failure. PKWARE assigns traditional encryption, strong encryption, and masked header values to ZIP general-purpose bits 0, 6, and 13. The selected response is a private fail-before-read preflight, not a decryption or general archive-safety claim. |
| Initial `uv run --frozen --python 3.12 pytest -q tests/architecture/test_m69_encrypted_sample_member_preflight.py --basetemp D:\\LudoWeaveValidation\\m69\\baseline` | 1 | Seven assertions failed and one protected-surface guard passed in 0.52 seconds against exact M68 code. All three indicators reached staging; the mask/helper, producer assertion, ordering contract, RFC, and documentation were absent. |
| Focused implementation gate | 0 | Ruff formatted one new test file; both changed Python files then passed Ruff and strict Pyright. M64-M69 passed 75 assertions with 1 local symbolic-link capability skip in 0.67 seconds. Strict docs built in 1.20 seconds with only the known upstream Material notice. |
| Complete source gate | 0 | `uv lock --check` resolved the unchanged 46-package lock in 1 ms; the restored 45-package CPython 3.12 graphics environment synchronized in 5 ms. All 312 Python files were format clean; Ruff and strict Pyright reported zero findings; whitespace passed. |
| Complete CPython 3.12 suite | 0 | The full suite passed 2,304 tests with 15 skips in 120.03 seconds using an isolated D: basetemp. |
| Complete CPython 3.13 suite | 0 | The full suite passed 2,294 tests with 16 skips in 102.83 seconds using an isolated D: basetemp. |
| Initial CPython 3.14 attempts | Environment failure | The first environment recreation exhausted C: during import-cache creation and never reached tests. After moving the generated environment to D:, the next suite reached 100% but pytest could not write its final cache and exited nonzero without a valid summary. Neither attempt is counted as passing. Only the exact ignored `.venv`, completed disposable basetemps, pytest cache, and generated docs site were removed before rerun. |
| Clean CPython 3.14 rerun | 0 | With the generated environment on D:, completed basetemps pruned, and pytest's nonessential cache disabled, the full suite passed 2,294 tests with 16 skips in 104.90 seconds. The baseline CPython 3.12 graphics environment was restored afterward. |
| Architecture and release-artifact gate | 0 | All 766 selected assertions passed with 1 local symbolic-link capability skip in 5.85 seconds. |
| Real-wgpu, profiles, and vertical slices | 0 | All 10 real-wgpu tests passed in 6.78 seconds. Five-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`, 3 draws, and 16 sprites. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, 6 query matches, 5 replay batches, and passing registered tests. |
| Diagnostic M1-M4 benchmark gate | 0 | All four fresh dirty-tree artifacts validated. M1 accepted 7 workloads with 1 of 2 historical targets observed; M2 accepted 4 informational workloads with no timing targets; M3 accepted 6 workloads with 0 of 2 historical targets met; M4 accepted 3 workloads with its baseline target observed. These are diagnostic measurements, not regression, support, release, or native-admission claims. |
| Reproducible distribution and release gate | 0 | Two builds reproduced a pure 273,229-byte wheel at `bba4773ecedf1b2c749daa7e8d930da482ed040df8e7d4e25a68e4a8127d66de` and a 1,206,202-byte source archive at `22420057c1c8d7c6283666501a05f596461a3505c2ac4425bee07463caeaa3bd`. Installed-wheel smoke, deterministic ten-artifact staging, and complete release smoke passed. The wheel has 94 entries, the sdist 504 including exactly one M69 test and RFC, and the 50-member sample has no encryption indicator; no inspected archive contains native/WASM content. This factual row changes the sdist afterward, so exact commit-tree artifact identity remains delegated to hosted qualification. |
| Findings-first review | Strengthened | No implementation defect was identified. The runtime regression proved fail-before-member-read and fail-before-staging, while fail-before-exact-inventory relied only on source ordering. The test now makes inventory evaluation itself forbidden and requires every expected member identity to be absent from the error. Production code and public docs are unchanged. |
| Review-affected source and behavior gate | 0 | All 312 Python files were format clean; Ruff and strict Pyright reported zero findings. M64-M69 passed 75 assertions with 1 local capability skip in 0.64 seconds; all 766 selected architecture/release assertions passed with 1 skip in 5.41 seconds; strict docs built in 1.23 seconds with only the known upstream Material notice; whitespace passed. |
| Review-affected reproducible distribution and release gate | 0 | Two builds reproduced the feature-identical pure 273,229-byte wheel at `bba4773ecedf1b2c749daa7e8d930da482ed040df8e7d4e25a68e4a8127d66de` and a 1,207,763-byte source archive at `54cc3fd021dfc120cf51fc7d3db31a3a3054b345c7a09547d7e6982298a9a671`. Installed-wheel smoke, deterministic ten-artifact staging, and complete release smoke passed. This factual row changes the sdist afterward, so exact commit-tree artifact identity remains delegated to hosted qualification. |
| Final record, scope, hygiene, and repository gate | 0 | The unchanged lock resolved 46 packages in 0.75 ms; all 312 files were format clean; Ruff and strict Pyright were clean; all 766 architecture/release assertions passed with 1 capability skip in 5.16 seconds; strict docs built in 1.17 seconds with only the known upstream Material notice; whitespace and `git fsck --full --no-dangling` passed. The exact 14-path scope has 12 tracked edits plus the M69 RFC/test, with no diff in workflows, runtime package, benchmarks, project metadata/lock, or producer. Protected SHA-256 values remain exact. Added-content scans found zero credential/private-key and zero explicit development-tool identity markers. Only `main` plus the intended neutral feature branch exist locally; only `origin/main` exists remotely. |
| Initial ready PR #159 run `31590079286` | 0 | Exact initial DCO head `c4b772943da75b6d6886c0f66d27b925b55eac1e` passed in exactly three Linux-first allocations. Linux job `94092772430` passed in 7m10s before macOS `94094454303` and Windows `94094454317` began; they passed in 2m31s and 4m07s. This head is retained as initial evidence only and is superseded by the review correction. |
| Initial hosted static, supported-Python, and graphics gates | 0 | All 312 files were format clean; Ruff and strict Pyright were clean; strict docs built in 1.60 seconds. Linux CPython 3.12 passed 2,309 tests; Ubuntu 3.13/3.14 and macOS/Windows 3.14 each passed 2,309 tests with 1 expected skip. Every OS passed 10 real-wgpu tests, its graphics profile, Clockwork Arena, and Agent World Builder; Linux also passed the base profile. |
| Initial hosted artifacts and release smoke | 0 | Two exact-head builds reproduced a pure 273,216-byte wheel at `805a0348c76a45a302a271c0386057eaa545594bf254818a5be2d6745f062d32` and a 1,208,501-byte source archive at `176b5453c9bd933e3643bb91a48bc8b2c8be4a2f79c6cc7644a966b76c566185`. Installed-wheel smoke, deterministic ten-artifact staging, and complete release smoke passed. |
| Delayed hosted review audit | Actionable | The first issue-comment audit was empty and the generic review summary contained no inline details, but the corrected GraphQL thread query found one unresolved P2 on exact head `c4b7729`. Encryption validation shared the per-member metadata loop, so an earlier unsafe-path or metadata failure could mask a later encryption indicator and violate the stable order-independent category. Merge was stopped. |
| Review correction and order-adversarial regression | 0 | A dedicated first pass now validates all member encryption flags before initializing or running per-member metadata validation. A two-member fixture with an unsafe first name and traditional-encryption bit on the second member requires the encrypted-member category and no output. The focused M69 file passes 9 assertions in 0.37 seconds. |
| First corrected source-gate attempt | Environment failure | Sandboxed `uv lock --check` could not access the existing user uv cache and exited 1 before resolving. The approved-cache rerun resolved 46 packages, checked the 45-package graphics environment, and passed formatting, Ruff, and strict Pyright, but the subsequent focused command used three nonexistent M64/M66/M67 filenames and exited 1 without collecting tests. No focused-suite pass is claimed from either failed invocation. |
| Corrected focused, docs, and whitespace gate | 0 | With the exact tracked filenames, M64-M69 passed 76 assertions with 1 local capability skip in 0.63 seconds. All 312 files remained format clean; Ruff and strict Pyright reported zero findings; strict docs built in 1.31 seconds with only the known upstream Material notice; whitespace passed. |
| Corrected complete CPython 3.12 suite | 0 | The complete review-corrected tree passed 2,305 tests with 15 skips in 109.86 seconds using a disposable D: basetemp. The algorithm and test-only correction has no version-specific dependency; exact updated-head 3.13/3.14 qualification remains delegated to the required hosted gate rather than being inferred. |
| Corrected architecture and release-artifact gate | 0 | All 767 selected assertions passed with 1 local capability skip in 5.18 seconds. |
| Corrected reproducible distribution and release gate | 0 | Two fresh builds reproduced the feature-identical pure 273,229-byte wheel at `bba4773ecedf1b2c749daa7e8d930da482ed040df8e7d4e25a68e4a8127d66de` and a 1,208,657-byte source archive at `85d8cc5f2d9cb9ecedc763176abb428726c8eab76e4c59e3b885e03b6df3ff6f`. Installed-wheel smoke, deterministic ten-artifact staging, and complete release smoke passed. This factual row changes the sdist afterward, so exact corrected-commit artifact identity remains delegated to hosted qualification. |
| Renderer, profile, example, and benchmark applicability | Not repeated | The correction changes only private sample-release preflight plus its architecture test and factual records; no renderer, runtime package, profile, example, benchmark, workflow, dependency, producer, or version surface changed. The earlier exact feature-head results remain applicable, while the corrected head will still receive the complete hosted three-OS gate before merge. |
| Post-correction findings-first review | 0 | The five-path correction diff was reviewed for error precedence, complete-member coverage, content-silent failure, extraction side effects, scope, and stale evidence. The dedicated flag pass is bounded by the unchanged 256-member limit and precedes every per-member metadata check; the new order-adversarial runtime proof fails if an earlier unsafe member can mask a later encrypted one. No further blocking or non-blocking finding remains. |
| Corrected final record-frozen gate | 0 | The unchanged lock resolved 46 packages in 1 ms; all 312 files were format clean; Ruff and strict Pyright reported zero findings; all 767 architecture/release assertions passed with 1 capability skip in 8.85 seconds; strict docs built in 1.48 seconds with only the known upstream Material notice; whitespace and full Git-object checking passed. |
| Corrected scope and hygiene audit | 0 | The correction changes exactly the two intended Python paths plus the three neutral project records. No diff exists in either workflow, runtime package, profile, example, benchmark, project metadata/lock, or sample producer. All five protected SHA-256 values remain exact. Ninety-seven added lines produced zero credential/private-key and zero explicit development-tool identity matches. Only `main` plus the intended neutral feature branch exist locally and remotely. |

## M69 hosted feature evidence - 2026-08-12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Corrected ready PR #159 run `31591830264` | 0 | Exact DCO head `cea31f5e6b52ff8c6ba0858425266723924726a3` passed in exactly three Linux-first allocations. Linux job `94098335992` passed in 7m11s before macOS `94100037726` and Windows `94100037646` began; they passed in 2m02s and 3m59s. |
| Corrected hosted static, supported-Python, and graphics gates | 0 | All 312 Python files were format clean; Ruff and strict Pyright were clean; strict docs built in 1.54 seconds. Linux CPython 3.12 passed 2,310 tests. Ubuntu 3.13/3.14 and macOS/Windows 3.14 each passed 2,310 tests with 1 expected skip. Every OS passed 10 real-wgpu tests, its graphics profile, Clockwork Arena, and Agent World Builder; Linux also passed the base profile. |
| Corrected hosted artifacts and release smoke | 0 | Two exact-head builds reproduced a pure 273,216-byte wheel at `805a0348c76a45a302a271c0386057eaa545594bf254818a5be2d6745f062d32` and a 1,210,777-byte source archive at `9783a01b07a22423e71414b6edfa64ea922ed3bc04df31f5018244206cd74dfc`. Installed-wheel smoke, deterministic ten-artifact staging, and complete release smoke passed. |
| Review resolution and delayed audits | 0 | The P2 was answered with exact local and hosted correction evidence and resolved. Two later separated audits found no issue comment, new actionable review, or unresolved thread. PR #159 remained ready, clean, mergeable, exact-head, exact-base, and fully checked. |
| Feature squash verification | 0 | PR #159 squash `9d298f800964b4237f204ea4acc366d224bcf76f` has tree `9652eded10bb48251bd67393f93cd90ca307d1d8`, exactly matching corrected reviewed head `cea31f5e6b52ff8c6ba0858425266723924726a3`; its sole parent is exact M68 closeout `fec3df4d490d363a9ab538f6b99ec86859e7acdc`. GitHub reports a valid signature verified at `2026-08-12T14:23:14Z` and an exact DCO trailer. The remote branch returns 404, and the exact-tree-equivalent local feature branch was deleted. |

## M69 integration-record local evidence - 2026-08-13, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Exact four-file source gate | 0 | `uv lock --check` resolved the unchanged 46-package lock in 1 ms. All 312 Python files were format clean; Ruff and strict Pyright reported zero findings; all 767 selected architecture/release assertions passed with 1 capability skip in 5.76 seconds; strict docs built in 1.31 seconds with only the known upstream Material notice; whitespace and full Git-object checking passed. The diff is exactly the three neutral `.project` records plus `ROADMAP.md`, with no substantive change from verified feature squash `9d298f8`. |
| Reproducible distribution and smoke | 0 | Two builds reproduced the feature-identical pure 273,229-byte wheel at `bba4773ecedf1b2c749daa7e8d930da482ed040df8e7d4e25a68e4a8127d66de` and a 1,212,288-byte record-updated source archive at `6eaf97ad765abf4e28ca4107231cdb0861adcef05e2ab24b942bc56961922b13`. Installed-wheel smoke, deterministic ten-artifact staging, and complete M69 release smoke passed. This factual row changes the sdist afterward, so exact integration-commit artifact identity remains delegated to hosted qualification. |
| Final record-frozen and scope gate | 0 | The unchanged lock resolved 46 packages in 0.78 ms; all 312 files were format clean; Ruff and strict Pyright reported zero findings; all 767 architecture/release assertions passed with 1 capability skip in 5.21 seconds; strict docs built in 1.19 seconds with only the known upstream notice; whitespace and full Git-object checking passed. The exact four-path diff changes no workflow, runtime, verifier, producer, dependency, package, test, or public documentation beyond the roadmap evidence row; all five protected hashes remain exact, and added-content scans found zero credential/private-key or explicit development-tool identity markers. Only `main` plus the intended neutral integration branch exist locally; only `origin/main` exists remotely. |

## M69 hosted integration-record evidence - 2026-08-12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Ready PR #160 run `31607127000` | 0 | Exact four-file DCO head `7a19c9d4005992afbb4f3ee738f2d26f93515d65` passed in one 41-second Linux allocation, job `94148855154`. Desktop umbrella job `94149098753` skipped with zero steps. No compatibility interpreter, software-rendering runtime, baseline/full suite, profile, graphics, example, or desktop runner executed. |
| Hosted documentation, distribution, and smoke | 0 | All 312 Python files were format clean; Ruff was clean; strict docs built in 1.41 seconds; all 766 documentation-selected architecture assertions passed in 8.98 seconds. Two builds reproduced the feature-identical 273,216-byte wheel at `805a0348c76a45a302a271c0386057eaa545594bf254818a5be2d6745f062d32` and a record-updated 1,212,886-byte source archive at `a262564238b30683cedc5ff7e07005318f2590c0804f9bacd96fd3f765ff8de9`. Installed-wheel smoke, deterministic staging, and complete M69 release smoke passed. |
| Delayed exact-head integration review audits | 0 | Two separated audits found no issue comment, review, or review thread. PR #160 remained ready, clean, mergeable, exact-head, exact-base, and fully checked. |
| Integration squash verification | 0 | PR #160 squash `9fcd61d1a3b93801b1bfd5a56392007fa15c6e03` has tree `c5ebdd4769118ed86fb7c50f557dcdd42be87597`, exactly matching reviewed record head `7a19c9d4005992afbb4f3ee738f2d26f93515d65`; its sole parent is exact feature squash `9d298f800964b4237f204ea4acc366d224bcf76f`. GitHub reports a valid signature verified at `2026-08-12T14:32:43Z` and an exact DCO trailer. The remote branch returns 404, and the exact-tree-equivalent local branch was deleted. |

## M69 closeout local evidence - 2026-08-13, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Exact three-record closeout gate | 0 | All 765 architecture assertions passed with 1 local capability skip in 4.83 seconds; strict docs built in 1.23 seconds with only the known upstream Material notice; whitespace and full Git-object checking passed. The closeout changes exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md`; it changes no workflow, runtime, verifier, producer, dependency, package, test, public documentation, or roadmap surface and is excluded from hosted CI. Added-content scans found zero credential/private-key or explicit development-tool identity markers. Only `main` plus the intended neutral closeout branch exist locally; only `origin/main` exists remotely. |

## M68 local development evidence - 2026-08-12, Windows, CPython 3.12

M68 starts from exact synchronized M67 closeout
`ea3de73f5ef1792df729c1f271b3d84a28db1028`, tree
`feed6f892798f0030974c957fa6b5f1352c8b53c`. The worktree was clean and
`main`, `origin/main`, and `origin/HEAD` matched before the neutral feature
branch was created.

| Command or review | Exit | Result |
| --- | ---: | --- |
| Focused primary-source direction scan | Advisory | Python 3.12 `zipfile` documents seekable file-object input and archive memory/disk resource limits; OWASP recommends explicit input-file and post-decompression size limits. The selected response is a private 16 MiB regular-file parser-input boundary through one opened handle, not a general archive-safety claim. |
| Initial `uv run --frozen pytest -q tests/architecture/test_m68_bounded_sample_archive_container.py` | 1 | Six assertions failed and two guards passed in 0.34 seconds against unchanged M67 code. The limit/helper were absent, invalid metadata reached the patched parser, valid parsing supplied a path rather than an admitted handle, and source ordering was absent. Documentation and protected-surface guards passed. |
| First focused M64-M68/static gate | Corrected | All 66 inherited/new behavior assertions passed with 1 local symlink-capability skip and Ruff was clean; strict Pyright found one unnecessary test cast. Removing that cast produced a clean focused static result. |
| Corrected focused static/docs gate | 0 | Both changed Python files were already formatted; Ruff and strict Pyright reported zero findings; M64-M68 passed 66 assertions with 1 capability skip in 0.69 seconds; strict docs built in 1.12 seconds with only the known upstream Material notice; and whitespace passed. |
| Unchanged lock and complete environment | 0 | `uv lock --check` resolved the unchanged 46-package lock in 1 ms. `uv sync --frozen --all-groups --extra graphics` checked the existing 45-package CPython 3.12 environment in 2 ms. |
| Whole-tree static gate | 0 | All 311 Python files were format clean; Ruff and strict Pyright reported zero findings. |
| Pre-review supported-Python suites | 0 | Using disposable `D:\LudoWeaveValidation\m68` pytest roots, CPython 3.12.13 passed 2,295 tests with 15 skips in 108.82 seconds. CPython 3.13.13 and 3.14.5 each passed 2,285 tests with 16 skips in 101.11 and 109.92 seconds; their ten-test difference is the intentionally absent optional graphics extra. The locked CPython 3.12 graphics environment was restored. |
| Architecture and release-artifact gate | 0 | All 757 selected architecture/release-artifact assertions passed with 1 local capability skip in 7.25 seconds. |
| Real-wgpu, profiles, and vertical slices | 0 | All 10 real-wgpu tests passed in 7.62 seconds. Five-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`, 3 draws, and 16 sprites. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, 6 query matches, 5 replay batches, and passing registered tests. |
| Diagnostic M1-M4 benchmark gate | 0 | All four fresh dirty-tree artifacts validated. M1 accepted 7 workloads with 1 of 2 historical targets observed; M2 accepted 4 informational workloads with no timing targets; M3 accepted 6 workloads with 0 of 2 historical targets met; M4 accepted 3 workloads with its baseline target observed. These are diagnostic measurements, not regression, support, release, or native-admission claims. |
| Pre-review reproducible distribution and release gate | 0 | Two fresh builds reproduced a pure 273,082-byte wheel at `089c787bd156e3af5f36fa20dbab1a69e953cc913b9367d9b023e1ccb18977fe` and a 1,198,756-byte source archive at `f135564122dacca5e3cd3c10e20005a7d40e4a9eda774b00a2771bb036d23f68`. Isolated-wheel smoke, deterministic ten-artifact staging, and complete release smoke passed. The 111,168-byte 50-file sample ZIP has SHA-256 `52e3fe162b844ba2c88634871e3d2d67a9afbf42fc1cd2c74b508186f786f2b3`. The wheel has 94 entries, the sdist 502 including exactly one M68 test/RFC, and no inspected archive contains native/WASM content. |
| Findings-first review | Corrected | Descriptor-only validation could block while opening a FIFO and could surface a directory-open failure before the promised stable category. The verifier now rejects obvious non-regular/oversized path metadata before open and then authoritatively revalidates the opened descriptor. A regression proves an obvious non-regular source is rejected before `Path.open`; docs now state both checks and the remaining mutability/race nonclaim. No other finding remains. |
| Review-corrected focused gate | 0 | Both changed Python files were format/Ruff/strict-Pyright clean; M64-M68 passed 67 assertions with 1 capability skip in 0.81 seconds; strict docs built in 1.14 seconds with only the known upstream notice; and whitespace passed. |
| Review-corrected complete CPython 3.12 suite | 0 | The full suite passed 2,296 tests with 15 skips in 113.80 seconds using a fresh disposable D: basetemp. |
| Review-corrected cross-version archive contract | 0 | M64-M68 passed 67 assertions with 1 local capability skip on CPython 3.13.13 in 1.16 seconds and CPython 3.14.5 in 1.03 seconds. The locked CPython 3.12 graphics environment was restored afterward. |
| Final record-inclusive source gate | 0 | The unchanged lock resolved 46 packages in 0.81 ms; all 311 Python files were format clean; Ruff and strict Pyright reported zero findings; all 758 selected architecture/release-artifact assertions passed with 1 capability skip in 8.78 seconds; strict docs built in 1.72 seconds with only the known upstream Material notice; whitespace, protected-surface comparison, and full Git-object checking passed. No diff exists in either workflow, runtime source, benchmarks, project metadata/lock, or the sample producer. |
| Record-inclusive reproducible distribution and release gate | 0 | After removing only the three verified old M68 artifact directories, two fresh builds reproduced a pure 273,106-byte wheel at `685c3baaa66ed325c471b5deb5f3f44590eb1bbc2c177ebdd53bc39366119c22` and a 1,200,373-byte source archive at `5d1bcb8424c13145977d53484a164457911ddfeb7d0e6e972e27399708afeaeb`. Installed-wheel smoke, deterministic ten-artifact staging, and complete M68 release smoke passed. This factual row changes the sdist afterward; exact commit-tree artifact identity remains delegated to hosted qualification. |

## M68 hosted feature evidence - 2026-08-12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Ready PR #156 run `31585838550` | 0 | Exact DCO head `0fbccca248e6a00a79631ca12c2afa6e7b9acdac` passed in exactly three Linux-first allocations. Linux job `94079347124` passed in 7m34s before macOS `94081155631` and Windows `94081155687` began; they passed in 2m58s and 4m13s. |
| Hosted supported-Python and static/docs gates | 0 | Linux CPython 3.12 passed 2,301 tests. Ubuntu 3.13/3.14 and macOS/Windows 3.14 each passed 2,301 tests with 1 expected skip. All 311 Python files were format clean; Ruff and strict Pyright were clean; strict docs built in 1.75 seconds. |
| Hosted graphics, profiles, examples, distribution, and smoke | 0 | Every allocated OS passed 10 real-wgpu tests, its graphics profile, Clockwork Arena, and Agent World Builder; Linux also passed the base profile. Two exact-head builds reproduced a pure 273,092-byte wheel at `85378f6485a06a8e1496e775fa8f71b122a899bdd0731ba3d67e1eda0f06db58` and a 1,200,886-byte source archive at `d1ac76ec6d3e62be894e894a862fbde09fa0aca07b58a8277b2ea33f96fdc977`. Installed-wheel smoke, deterministic ten-artifact staging, and complete M68 release smoke passed. |
| Delayed exact-head review audits | 0 | Two separated audits found no issue comment, review, or review thread. PR #156 remained ready, clean, mergeable, exact-head, exact-base, and fully checked. |
| Feature squash verification | 0 | PR #156 squash `5bd0196128aeffcf21094d0a0c6d78b624aaf49b` has tree `7e03726ebea72d074e0404f6c8073f96e0e8cce5`, exactly matching reviewed head `0fbccca248e6a00a79631ca12c2afa6e7b9acdac`; its sole parent is exact M67 closeout `ea3de73f5ef1792df729c1f271b3d84a28db1028`. GitHub reports a valid signature verified at `2026-08-12T10:19:22Z` and an exact parsed DCO trailer. The remote and local feature branches are absent. |

## M68 integration-record local evidence - 2026-08-12, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Exact four-file source gate | 0 | `uv lock --check` resolved the unchanged 46-package lock in 2 ms. All 311 Python files were format clean; Ruff and strict Pyright reported zero findings; all 758 selected architecture/release-artifact assertions passed with 1 capability skip in 7.49 seconds; strict docs built in 1.59 seconds with only the known upstream Material notice; whitespace and exact scope passed. No substantive surface changed from verified feature squash `5bd0196`. |
| Reproducible distribution and smoke | 0 | Two builds reproduced the feature-identical pure 273,106-byte wheel at `685c3baaa66ed325c471b5deb5f3f44590eb1bbc2c177ebdd53bc39366119c22` and a 1,202,267-byte record-updated source archive at `850c09e90f17ee4de792f9f6f2d7ff48741a02300fa94b81cdf4535df151f2f8`. Installed-wheel smoke, deterministic ten-artifact staging, and complete M68 release smoke passed. This factual row changes the sdist afterward, so exact integration-commit artifact identity remains delegated to hosted qualification. |

## M68 hosted integration-record evidence - 2026-08-12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Ready PR #157 run `31587335592` | 0 | Exact four-file DCO head `cd65d1345b2725eb3be4daeb899535eacb740dee` passed in one 43-second Linux allocation; the desktop matrix umbrella skipped with zero steps. No compatibility interpreter, software graphics runtime, baseline/full-suite, profile, graphics, example, or desktop runner executed. |
| Hosted documentation, distribution, and smoke | 0 | All 311 Python files were format clean; Ruff was clean; strict docs built in 1.52 seconds; all 757 documentation-selected architecture assertions passed in 9.07 seconds. Two builds reproduced the feature-identical 273,092-byte wheel at `85378f6485a06a8e1496e775fa8f71b122a899bdd0731ba3d67e1eda0f06db58` and a record-updated 1,202,598-byte source archive at `32d390922dbfc9a62eb19fdf0ea4f35f6817a2da7c676534d6849bafbee3cc6e`. Installed-wheel smoke, deterministic staging, and complete M68 release smoke passed. |
| Delayed exact-head integration review audits | 0 | Two separated audits found no issue comment, review, or review thread. PR #157 remained ready, clean, mergeable, exact-head, exact-base, and fully checked. |
| Integration squash verification | 0 | PR #157 squash `69fe032bfa0af6513d46e7c7492ffa3a5720d163` has tree `83e765ba0fa92038aeefaaf2dcf9d2fb85eec052`, exactly matching reviewed head `cd65d1345b2725eb3be4daeb899535eacb740dee`; its sole parent is exact feature squash `5bd0196128aeffcf21094d0a0c6d78b624aaf49b`. GitHub reports a valid signature verified at `2026-08-12T10:28:06Z` and an exact parsed DCO trailer. The remote and local integration branches are absent. |

## M68 closeout local evidence - 2026-08-12, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Exact three-record closeout gate | 0 | All 756 architecture assertions passed with 1 local capability skip in 5.65 seconds; strict docs built in 1.20 seconds with only the known upstream Material notice; whitespace, exact scope, and full Git-object checking passed. The closeout changes exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md`; it changes no workflow, runtime, verifier, producer, dependency, package, test, public documentation, or roadmap surface and is excluded from hosted CI. Only `main` plus the intended closeout branch exist locally, and only `origin/main` exists remotely. |
| Closeout squash and pruning | 0 | PR #158 squash `fec3df4d490d363a9ab538f6b99ec86859e7acdc` has exact tree `519955303ba8638ed9847df6b0d9cb62ded25436`, sole parent M68 integration squash `69fe032bfa0af6513d46e7c7492ffa3a5720d163`, a valid GitHub signature verified at `2026-08-12T10:34:00Z`, and exact DCO. The remote branch returned 404, no closeout workflow run exists, every M68 branch/output was removed, `main` matched `origin/main`, no PR remained open, whitespace and full Git-object checking passed. |

## M67 local development evidence - 2026-08-12, Windows, CPython 3.12

M67 starts from exact synchronized M66 closeout
`995fdda097a418a7a0e570bb6b492d3f5609d471`, tree
`54da91c867211007156d5006512a426815a8374b`. The worktree was clean;
`main`, `origin/main`, and `origin/HEAD` matched; only `main` existed locally
and remotely; and `gh pr list --state open` returned `[]` before creating the
neutral feature branch.

| Command or review | Exit | Result |
| --- | ---: | --- |
| Focused primary-source direction scan | Advisory | Python `zipfile` warns that untrusted archives require prior inspection; OWASP recommends allowlists and pre-extraction path/expansion checks; SLSA 1.2 recommends comparing artifacts with source-defined expectations and rejecting unrecognized inputs. The selected narrow response is exact project sample inventory conformance, not a SLSA-compliance or general archive-safety claim. |
| Initial `uv run --frozen pytest -q tests/architecture/test_m67_exact_sample_bundle_inventory.py` | 1 | Five assertions failed and three guards passed in 0.33 seconds against unchanged M66 production code. No expected inventory existed; extra and missing-nested-member fixtures reached archive reads; the source-ordering contract and RFC-0050 were absent. Producer inventory, exact-valid extraction, and protected-surface guards passed. |
| First focused implementation gate | Corrected | Ruff formatting identified one test file; Ruff found three constant-attribute `setattr` calls and one non-raw regular expression; strict Pyright found the corresponding three unknown lambda parameters plus a set/frozenset comparison issue. Behavior passed 57 assertions with 1 capability skip, strict docs built in 1.11 seconds, and whitespace was clean. No complete static pass is claimed from this invocation. |
| Corrected focused static and behavior gate | 0 | After mechanical formatting, typed scoped-policy helpers, a raw regex, and a same-type set comparison, all five changed Python files were format/Ruff/strict-Pyright clean. M64-M67 passed 57 assertions with 1 local symbolic-link capability skip in 0.60 seconds. Strict docs had already passed in 1.26 seconds with only the known upstream Material notice, and whitespace was clean. |
| Whole-tree source and documentation gate | 0 | The unchanged lock resolved 46 packages in 0.92 ms and the frozen CPython 3.12 graphics environment checked 45 packages. All 310 Python files were format clean; Ruff and strict Pyright reported zero findings; all 746 architecture assertions passed with 1 local capability skip in 6.26 seconds; both release-artifact tests passed in 0.62 seconds; strict docs built in 1.31 seconds with only the known upstream Material notice; and whitespace was clean. |
| Supported-Python candidate suites | 0 | With pytest temporary repositories isolated under disposable `D:\LudoWeaveValidation\m67`, CPython 3.12.13 passed 2,286 tests with 15 expected skips in 107.53 seconds. CPython 3.13.13 and 3.14.5 each passed 2,276 tests with 16 skips in 99.07 and 105.41 seconds; their ten-test difference is the intentionally absent optional graphics extra. The locked 45-package CPython 3.12 graphics environment was restored afterward. |
| Real-wgpu, profiles, and vertical slices | 0 | All 10 real-wgpu tests passed in 7.49 seconds. Five-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`, 3 draws, and 16 sprites. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, 6 query matches, 5 replay batches, and passing registered tests. |
| Diagnostic M1-M4 benchmark gate | 0 | All four fresh dirty-tree artifacts validated. M1 accepted 7 workloads with 1 of 2 historical targets observed; M2 accepted 4 informational workloads with no timing targets; M3 accepted 6 workloads with 0 of 2 historical targets met; M4 accepted 3 workloads with its baseline target observed. These are diagnostic measurements, not regression, support, release, or native-admission claims. |
| Pre-review reproducible distribution and release gate | 0 | Two fresh confirmed-absent builds reproduced a pure 272,880-byte wheel at `dba45ae505702b2bb04e1666adce518f87239158f2e5ba3cafd19ee82c50016b` and a 1,190,493-byte source archive at `962068fd8537e13639efc0d528179911e2beeab8a0a8ccce1776a641c09ade12`. Isolated-wheel smoke, deterministic 10-artifact staging, and complete M67 release smoke passed. This factual row changes the source archive afterward; exact commit-tree artifact identity remains delegated to hosted qualification. |
| Pre-review archive inventory | 0 | The wheel contains 94 entries and no native library or WASM file. The 500-entry source archive contains the exact M67 architecture test and RFC-0050 with no native/WASM file. The staged sample ZIP contains exactly 50 files beneath one expected versioned root and no native/WASM file. |
| Findings-first review | Strengthened | Review found that the separate 49-member omission and 51-member addition cases did not independently disprove a count-only implementation. A 50-member one-for-one substitution now proves exact identity, and a patched staging constructor proves mismatch rejection precedes staging as well as member reads. The correction changes tests only; no production or runtime surface changed. No blocking or non-blocking finding remains. |
| Review-strengthened focused gate | 0 | All five changed Python files were format/Ruff/strict-Pyright clean and M64-M67 passed 58 assertions with 1 local symbolic-link capability skip in 0.75 seconds. Earlier full supported-version, graphics, profile, vertical-slice, benchmark, and artifact results remain applicable because review changed only this test. |
| Final record-frozen source gate | 0 | The unchanged lock resolved 46 packages in 0.82 ms; all 310 Python files were format clean; Ruff and strict Pyright reported zero findings; all 747 reviewed architecture assertions passed with 1 local capability skip in 6.17 seconds; both release-artifact tests passed in 0.64 seconds; strict docs built in 1.25 seconds with only the known upstream Material notice; whitespace and full Git-object checking passed. Protected workflow, producer, runtime, benchmark, dependency, lock, version, and package surfaces have no diff. |

## M67 hosted feature evidence - 2026-08-12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Ready PR #153 run `31534773135` | 0 | Exact DCO head `3cb44d412d71a930f84a1545e59f893643d68666` passed in exactly three Linux-first allocations. Linux job `93923151529` passed in 7m44s before macOS `93925267043` and Windows `93925266979` began; they passed in 3m22s and 4m15s. |
| Hosted supported-Python and graphics suites | 0 | Linux baseline passed 2,292 tests in 141.13 seconds; Ubuntu 3.13 and 3.14 each passed 2,292 with 1 expected skip in 113.96 and 120.36 seconds. macOS and Windows 3.14 each passed 2,292 with 1 skip in 133.74 and 198.13 seconds. Real-wgpu passed 10 tests on Linux in 9.00 seconds, macOS in 16.23 seconds, and Windows in 9.17 seconds. |
| Hosted profiles, examples, distribution, and smoke | 0 | Both profiles and both vertical slices passed on every allocated operating system. Two hosted builds reproduced a pure 272,867-byte wheel at `5b67653c5f4374ffc52f55eadc9d2e29fc72e8281969d6c891da3b56042475a8` and a 1,191,892-byte source archive at `79bf91855560aa26b4a2a8c6082b08b164eb22e7baece36b05397191f171bdb1`. Installed-wheel smoke, 10-artifact staging, and complete M67 release smoke passed. |
| Hosted delayed audits | 0 | Initial plus two delayed exact-head audits found no review, issue comment, review comment, or unresolved thread. PR #153 remained clean, mergeable, exact-head, exact-base, and fully green. |
| Feature squash verification | 0 | PR #153 squash `bc8a3d9a24bab5860e48af919dbeab4ca4c913f2` has tree `cd8833bbd93e11c7e7e678ee324711503a921d97`, exactly matching reviewed head `3cb44d412d71a930f84a1545e59f893643d68666`; its sole parent is exact M66 closeout `995fdda097a418a7a0e570bb6b492d3f5609d471`. GitHub reports a valid signature verified at `2026-08-11T21:03:55Z`, and the squash has an exact parsed DCO trailer. The feature branch is absent locally and remotely. |

## M67 integration-record local evidence - 2026-08-12, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Exact scope, lock, static, architecture, docs, and whitespace gate | 0 | The diff names exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md`; no implementation, workflow, producer, runtime, benchmark, dependency, or package surface differs from verified feature squash `bc8a3d9`. The unchanged lock resolved 46 packages in 0.93 ms. All 310 Python files were format clean; Ruff and strict Pyright reported zero findings; all 747 architecture assertions passed with 1 local capability skip in 6.38 seconds; both release-artifact tests passed in 0.61 seconds; strict docs built in 1.19 seconds with only the known upstream Material notice; whitespace and full Git-object checking passed. |
| Reproducible distribution and smoke | 0 | Two builds reproduced the unchanged pure 272,880-byte wheel at `dba45ae505702b2bb04e1666adce518f87239158f2e5ba3cafd19ee82c50016b` and a 1,192,787-byte record-updated source archive at `2c0341630a35ec53fc5cf35b25a8aa20741a7092ef5e4c219ece5eccc2e738e8`. Installed-wheel smoke, deterministic 10-artifact staging, and complete M67 release smoke passed. This factual row changes the source archive afterward, so exact commit-tree artifact identity remains delegated to the one-allocation hosted gate. |

## M67 hosted integration-record evidence - 2026-08-12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Ready PR #154 run `31536520514` | 0 | Exact four-document DCO head `565053e8cf0f3961f8bfbc1a54df04a604240183` passed in one 41-second Linux allocation. The desktop compatibility umbrella job `93928999570` skipped with zero steps and no runner. All 310 Python files were format clean; Ruff, strict docs, and all 748 documentation-selected architecture assertions passed. |
| Hosted reproducible distribution and smoke | 0 | Two builds reproduced the feature-identical 272,867-byte wheel at `5b67653c5f4374ffc52f55eadc9d2e29fc72e8281969d6c891da3b56042475a8` and a record-updated 1,193,131-byte source archive at `ca246f1f23225cf43e5f81a5eda1b60629f6ff47dc389d4700e7a53b97606389`. Installed-wheel smoke, deterministic staging, and complete M67 release smoke passed. |
| Review resolution and delayed audits | Resolved | Delayed review comment `3761750291` incorrectly claimed the sole integration commit lacked DCO. GitHub's PR commit endpoint returned only `565053e` with the exact authorized trailer, and local `git interpret-trailers --parse` returned the same trailer. Evidence reply `3765169173` was posted and thread `PRRT_kwDOTtqoGs6YYOGq` resolved. Two post-resolution exact-head audits found no later review, issue comment, review comment, or unresolved thread. |
| Integration squash verification | 0 | PR #154 squash `5025877d31a2bc8a9a0a1b7bb2e106869f76066f` has tree `eb532eddbd368efaaa1a896efd930727cc5b3059`, exactly matching reviewed head `565053e8cf0f3961f8bfbc1a54df04a604240183`; its sole parent is feature squash `bc8a3d9a24bab5860e48af919dbeab4ca4c913f2`. GitHub reports a valid signature verified at `2026-08-12T09:28:58Z`, and the squash has an exact parsed DCO trailer. The integration branch is absent locally and remotely. |

## M67 closeout local evidence - 2026-08-12, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Three-file closeout source gate | 0 | Exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md` differ from verified integration squash `5025877`. All 747 architecture assertions passed with 1 local capability skip in 6.04 seconds; strict docs built in 1.45 seconds with only the known upstream Material notice; whitespace and full Git-object checking passed. Workflow, runtime, verifier, producer, dependency, package, tests, public docs, and roadmap are unchanged. Existing CI path policy excludes this closeout from hosted execution. |

## M66 local development evidence - 2026-08-12, Windows, CPython 3.12

M66 starts from exact synchronized M65 closeout
`0892f4b234be5ea06d6a91f3b1f0b50a1f44eb1`, tree
`a8e028df3db9b6eb0293cd9177cedcda3367666a`. The worktree was clean;
`main`, `origin/main`, and `origin/HEAD` matched; and only `main` existed
locally and remotely before creating the neutral feature branch.

| Command or review | Exit | Result |
| --- | ---: | --- |
| Initial `uv run --frozen pytest -q tests/architecture/test_m66_atomic_sample_extraction.py` | 1 | Eight assertions failed, two guards passed, and the Windows symbolic-link capability case skipped in 0.36 seconds against unchanged M65 production code. Stream-size and incomplete-bundle failures left partial final roots; an existing directory reached archive reads; an existing file raised a host `FileExistsError`; a missing output parent was created; publish-failure injection was never reached; and staged source structure/RFC-0049 were absent. The valid final shape and protected workflow/stager/runtime/dependency/package surfaces passed. |
| Non-documentation implementation contract | 0 | `uv run --frozen pytest -q tests/architecture/test_m66_atomic_sample_extraction.py -k "not docs"` passed 9 assertions, skipped the Windows symbolic-link capability case, and deselected the documentation assertion in 0.25 seconds. Stream mismatch, incomplete bundle, existing file/directory, missing parent, injected publish failure, successful single-root publication, source ordering, and protected surfaces behaved as specified. |
| First focused static/inherited gate | 1 | Ruff reported that both changed Python files would be reformatted and the fail-fast gate stopped before lint, type checking, or inherited tests. No later pass is claimed from this invocation. |
| Corrected focused static/inherited gate | 0 | After mechanical formatting, both changed Python files were format/Ruff/strict-Pyright clean; all 46 M64-M66 archive assertions passed with 1 Windows symbolic-link capability skip in 0.46 seconds. |
| First record-inclusive source gate | 0 | The sandboxed lock probe first exited 1 because the user uv cache was inaccessible. Its approved rerun resolved the unchanged 46-package lock in 0.75 ms, and the graphics-enabled environment checked 45 packages in 3 ms. All 309 Python files were format clean; Ruff and strict Pyright reported zero findings; all 736 architecture assertions passed with 1 capability skip in 5.09 seconds; strict docs built in 1.12 seconds with only the known upstream Material notice; and whitespace was clean. |
| First CPython 3.12 suite attempt | Invalid | The drive reached zero free bytes at 91%, emitted late failures, and pytest then raised `OSError: [Errno 28]` while writing its cache. The run exited 1 without a valid test summary; no behavioral pass or failure claim is made from it. |
| Second CPython 3.12 suite attempt | Invalid | After verified generated workspace cleanup recovered about 272 MiB, the suite reached 2,265 passed and 15 skipped before the only remaining test failed while creating its deliberate 1 MiB oversized fixture with `Errno 28`. The run exited 1 and is treated as environmental evidence only. |
| Isolated CPython 3.12 suite | 0 | With pytest temporary repositories moved to verified disposable `D:\\LudoWeaveValidation\\m66\\pytest-312`, the exact candidate passed 2,266 tests with 15 expected skips in 102.03 seconds. |
| Supported-Python compatibility | 0 | The locked CPython 3.13.13 environment passed 2,266 tests with 16 expected skips in 98.41 seconds, and CPython 3.14.5 passed 2,266 with 16 skips in 103.92 seconds. Both used separate disposable `D:` pytest roots; the locked CPython 3.12.13 graphics environment was restored afterward. |
| Real-wgpu, profiles, and vertical slices | 0 | All 10 real-wgpu tests passed in 6.47 seconds. Five-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`, 3 draws, and 16 sprites. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, 6 query matches, 5 replay batches, and passing registered tests. |
| Diagnostic M1-M4 benchmark gate | 0 | All four fresh dirty-tree artifacts validated. M1 accepted 7 workloads with 1 of 2 historical targets observed; M2 accepted 4 informational workloads with no timing targets; M3 accepted 6 workloads with 0 of 2 historical targets met; M4 accepted 3 workloads with its baseline target observed. These are diagnostic measurements, not regression, support, release, or native-admission claims. |
| Pre-review reproducible distribution and release gate | 0 | The first sandboxed build exited 1 because uv cache access was denied. Approved reruns built two byte-identical pure 272,709-byte wheels at `c781d27046ee92131208802fdef6d800e1fc5fc28f6baeb4a4ef8234b0cc58f8` and 1,181,229-byte source archives at `046234a5156ae22aaac765f9263ba7ff328c6219d0e50f8a530e78a6944c8855`. Reproducibility, isolated-wheel smoke, deterministic 10-artifact staging, and complete M66 release smoke passed. |
| Findings-first review | Corrected | Correctness/security review found that `output.is_symlink()` did not reject a Windows directory junction despite the documented real-directory contract. Two review-derived assertions failed before the correction; adding `output.is_junction()` made the link-like parent fail before staging. Review also added direct mid-stream I/O cleanup and late final-root collision preservation proofs. No further blocking or non-blocking finding remained. |
| Review-strengthened focused gate | Corrected then 0 | The first strict-Pyright pass found one test-only `BinaryIO`/`IO[bytes]` return mismatch. After correcting that annotation, the test file was format/Ruff/strict-Pyright clean and all 13 M66 assertions passed with 1 local symbolic-link capability skip in 0.62 seconds. |
| Review-strengthened record-inclusive source gate | 0 | The unchanged lock resolved 46 packages in 0.74 ms; all 309 Python files were format clean; Ruff and strict Pyright reported zero findings; all 738 architecture assertions passed with 1 capability skip in 4.75 seconds; both release-artifact tests passed in 0.51 seconds; strict docs built in 1.08 seconds with only the known upstream Material notice; and whitespace was clean. |
| Final reviewed reproducible distribution and release gate | 0 | Two fresh confirmed-absent builds reproduced the unchanged pure 272,709-byte wheel at `c781d27046ee92131208802fdef6d800e1fc5fc28f6baeb4a4ef8234b0cc58f8` and a review/record-updated 1,183,308-byte source archive at `c8838b14876882c8588d5887d24087c428d3cff98fd98208ba4403fd0f16d13b`. Isolated-wheel smoke, deterministic 10-artifact staging, and complete M66 release smoke passed. This factual row changes the source archive afterward; exact commit-tree artifact identity remains delegated to hosted qualification. |
| Final reviewed archive inventory | 0 | The wheel contains 94 entries and no native library or WASM file. The 498-entry source archive contains the exact M66 architecture test and RFC-0049. The 50-entry staged sample ZIP has exactly one expected `ludoweave-samples-0.1.0a1` root. |
| Final record-frozen source gate | 0 | The unchanged lock resolved 46 packages in 0.87 ms; all 309 Python files were format clean; Ruff and strict Pyright reported zero findings; all 738 architecture assertions passed with 1 capability skip in 4.74 seconds; both release-artifact tests passed in 0.51 seconds; strict docs built in 1.20 seconds with only the known upstream Material notice; and whitespace was clean. |

## M66 hosted feature evidence - 2026-08-12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Ready PR #150 run `31529725573` | 0 | Exact DCO head `facda31545cd490187e7679d613cd9bb5149028d` passed in exactly three Linux-first allocations. Linux `93906589413` passed in 7m17s before macOS `93908604436` passed in 2m07s and Windows `93908604437` in 3m21s. |
| Hosted supported-Python and graphics suites | 0 | Linux baseline passed 2,283 tests in 122.00 seconds; Ubuntu 3.13 and 3.14 each passed 2,283 with 1 expected skip in 104.30 and 108.79 seconds. macOS and Windows 3.14 each passed 2,283 with 1 skip in 88.60 and 150.89 seconds. Real-wgpu passed 10 tests on Linux in 5.39 seconds, macOS in 7.27 seconds, and Windows in 7.47 seconds. |
| Hosted profiles, examples, distribution, and smoke | 0 | Both profiles and both vertical slices passed on every allocated operating system. Two hosted builds reproduced a pure 272,695-byte wheel at `d72a13dcecdcaa1cef53392b0c2fb6d7eba10b817894985588e3524f8f2a2874` and a 1,183,498-byte source archive at `89f1e1cd845445c3a55030c32af2f1c247d43639cd2c0eb18a47b7a8994ec360`. Installed-wheel smoke, 10-artifact staging, and complete M66 release smoke passed. |
| Hosted review resolution and delayed audits | Resolved | Review comment `3761229485` incorrectly cited commit `dd958c5`, which is absent from PR #150. GitHub's PR commit endpoint and local `origin/main..HEAD` each contained only `facda315`; its exact message and parsed trailer contain `Signed-off-by: Louijie Compo <louijie.compo@gmail.com>`. Evidence reply `3761286817` was posted and thread `PRRT_kwDOTtqoGs6YW4Bn` resolved. Two delayed audits found no later review, issue comment, review comment, or unresolved thread. |
| Feature squash verification | 0 | PR #150 squash `79593b01d670dd07fb761e493382685765d13d7a` has tree `dc776056d2cdb15c30944dbe2dae5f7c2ffb0c8e`, exactly matching reviewed head `facda31545cd490187e7679d613cd9bb5149028d`; its sole parent is exact M65 closeout `0892f4b234be5ea06d6a91f3b1f0b50a1f44eb1`. GitHub reports a valid signature verified at `2026-08-11T20:04:35Z`, and the squash has an exact parsed DCO trailer. The feature branch is absent locally and remotely. |

## M66 integration-record local evidence - 2026-08-12, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Exact scope, lock, static, architecture, docs, and whitespace gate | 0 | The diff names exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md`; no implementation/workflow/dependency surface differs from verified feature squash `79593b0`. The unchanged lock resolved 46 packages in 0.76 ms. All 309 Python files were format clean; Ruff and strict Pyright reported zero findings; all 738 architecture assertions passed with 1 capability skip in 5.10 seconds; strict docs built in 1.12 seconds with only the known upstream Material notice; and whitespace was clean. |
| Reproducible distribution and smoke | 0 | Two builds reproduced the unchanged pure 272,709-byte wheel at `c781d27046ee92131208802fdef6d800e1fc5fc28f6baeb4a4ef8234b0cc58f8` and a 1,185,006-byte record-updated source archive at `762db81c1fbffa374af536cca0b5e646f7ff9af5f432f315d936bee7fe5f4a1c`. Installed-wheel smoke, deterministic 10-artifact staging, and complete M66 release smoke passed. This factual row changes the source archive afterward, so exact commit-tree artifact identity remains delegated to the one-allocation hosted gate. |

## M66 hosted integration-record evidence - 2026-08-12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Ready PR #151 run `31531603994` | 0 | Exact four-document head `595eb77c42de31211c4d164e949cf0fa4d5db3c3` passed in one 43-second Linux allocation. The desktop compatibility umbrella skipped with zero steps. All 309 Python files were format clean; Ruff, strict docs, and all 739 documentation-selected architecture assertions passed. |
| Hosted reproducible distribution and smoke | 0 | Two builds reproduced the 272,695-byte wheel at `d72a13dcecdcaa1cef53392b0c2fb6d7eba10b817894985588e3524f8f2a2874` and the record-updated 1,185,305-byte source archive at `d9ebe95fe0a30777e0138ce1434e9c31ac21bbfb6ba4b6856740310a1b087c5f`. Installed-wheel smoke, deterministic staging, and complete M66 release smoke passed. |
| Delayed integration-record audits | 0 | Both delayed exact-head audits found no review, issue comment, or review comment. PR #151 remained clean, mergeable, exact-head, and exact-base with its Linux check successful and desktop umbrella skipped. |
| Integration squash verification | 0 | PR #151 squash `bcc91aa97d3157971eb4ba52f2430b8bb65c4ab6` has tree `8ed42b87e04ed93fb205f06878bc5f85cf26b8b5`, exactly matching reviewed head `595eb77c42de31211c4d164e949cf0fa4d5db3c3`; its sole parent is feature squash `79593b01d670dd07fb761e493382685765d13d7a`. GitHub reports a valid signature verified at `2026-08-11T20:14:33Z`, and the squash has an exact parsed DCO trailer. The integration branch is absent locally and remotely. |

## M65 local development evidence - 2026-08-12, Windows, CPython 3.12

M65 starts from exact synchronized M64 closeout
`92e706961e2ecd4e2c187a205cc045a8c6506ab9`, tree
`8df4aaa8222517d729234792d162dfc115674767`. The worktree was clean, local
`main`, `origin/main`, and `origin/HEAD` matched, only `main` remained after
remote pruning, no pull request was open, `git fsck --no-dangling` exited zero,
and no post-closeout run or check exists.

| Command or review | Exit | Result |
| --- | ---: | --- |
| Initial `pytest -q tests/architecture/test_m65_portable_sample_member_paths.py` | 1 | Sixteen assertions failed and two passed in 0.56 seconds against unchanged production code. Nonportable names extracted before later incomplete-bundle failure or reached a host path error; duplicates overwrote, case aliases merged, prefix collisions failed after writes, explicit directories created output, and the M65 constant/source/RFC contract was absent. The valid nested sample shape and protected workflow/stager/runtime/dependency/package surfaces passed. |
| First focused implementation gate | 1 | Ruff formatting reported the new M65 test file would be reformatted and the fail-fast gate stopped before lint, type checking, or behavior tests. No focused pass is claimed. |
| Corrected focused implementation gate | 0 | After mechanical formatting, both changed Python files were format clean and Ruff clean; strict Pyright reported zero findings; all 17 non-documentation M65 assertions passed with the docs case deselected in 0.26 seconds. |
| Complete documented M65 contract | 0 | Both changed Python files remained format/Ruff/strict-Pyright clean; all 18 M65 behavior, ordering, boundary, protected-surface, and documentation assertions passed in 0.23 seconds; strict docs built in 1.11 seconds with only the known upstream Material notice; and whitespace was clean. |
| Inherited architecture and release-artifact gate | 0 | All 720 architecture assertions passed in 4.97 seconds, preserving M64 bounded streaming and all earlier boundaries; both release-artifact tests passed in 0.65 seconds. |
| First record-inclusive source gate | Corrected | The unchanged lock resolved 46 packages in 0.80 ms. `uv sync --frozen --all-groups` removed the optional six-package graphics extra as designed; formatting for 308 files and Ruff then passed, but strict Pyright reported 17 missing/unknown wgpu-related imports. No complete static pass is claimed from that baseline-only environment. |
| Corrected graphics-enabled source gate | 0 | Restoring `--extra graphics` installed the exact six locked packages. All 308 files were format clean; Ruff and strict Pyright reported zero findings; all 720 architecture assertions passed in 5.24 seconds; strict docs built in 1.17 seconds with only the known upstream Material notice; and whitespace was clean. |
| Supported-Python candidate gate | 0 | The graphics-enabled candidate passed 2,260 tests with 14 expected skips on CPython 3.12.13 in 108.88 seconds, CPython 3.13.13 in 107.48 seconds, and CPython 3.14.5 in 112.99 seconds. The suites ran serially because the repository shares one temporary test root. |
| Real-wgpu, profiles, and vertical slices | 0 | After restoring the locked 45-package CPython 3.12.13 graphics environment, all ten real-wgpu tests passed in 6.73 seconds. Five-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`, three draws, and 16 sprites. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, six query matches, five replay batches, and passing registered tests. |
| Documented M1-M4 benchmark gate | 0 | All four fresh dirty-tree artifacts validated on Windows CPython 3.12.13. M1 accepted seven workloads with one of two historical targets observed; M2 accepted four informational workloads with no timing targets; M3 accepted six workloads with one of two historical targets met; M4 accepted three workloads with its baseline target observed. These measurements are diagnostic, not regression, support, release, or native-admission claims. |
| Pre-review reproducible distribution and release gate | 0 | Two fresh confirmed-absent builds reproduced a pure 272,430-byte wheel at `f563d5a7f2ab11c28404462de33454108d74e68528c65742d9417dc9736a3020` and a 1,169,917-byte source distribution at `3ae5e4f6498e1f8aaa7c01771f4c6e4203c5201707cfcb75f01d6f258b28f95b`. Isolated-wheel smoke, fresh ten-artifact staging, and complete portable-path release smoke passed. |
| Findings-first scope, security, and archive review | Strengthened | Workflows, project metadata, lockfile, sample producer, and runtime package source are byte-unchanged. The implementation confines new work to complete private release-smoke preflight and contains no credential-like value or backend/native import. Case folding follows ASCII admission; full duplicates, ancestor aliases, and file/directory prefixes are checked before writes; validated parts are reused during streaming. Review found no production defect, but added direct proof that the exact 255-character upper boundary remains admitted. |
| Review-strengthened focused and inherited gate | 0 | Both changed Python files remained format/Ruff/strict-Pyright clean; all 19 M65 assertions passed in 0.84 seconds; all 721 architecture assertions passed in 4.98 seconds. |
| First archive inventory command | Corrected | The PowerShell command used nonexistent `Select-Object -Single`, so archive paths were unset and `tar` listed nothing. The shell's later statements returned zero and the overall invocation exited zero; its reported zero-entry tables are invalid and no archive claim is made from that command. |
| Corrected archive and sample-identity inspection | 0 | The built wheel contains 94 entries and the source archive 496, with no native library, WASM, bytecode, cache, site, or dist payload. The staged sample ZIP contains 50 entries; its longest full path is 71 characters and it has zero case-insensitive duplicates or file-prefix collisions. |
| Final record-inclusive source gate | 0 | The unchanged lock resolved 46 packages in 0.88 ms and the restored CPython 3.12 graphics environment checked 45 packages in 2 ms. All 308 Python files were format clean; Ruff and strict Pyright reported zero findings; all 721 architecture assertions passed in 5.08 seconds; strict docs built in 1.12 seconds with only the known upstream Material notice; and whitespace was clean. |
| Final review-strengthened supported-Python gate | 0 | The exact reviewed candidate passed 2,261 tests with 14 expected skips on CPython 3.12.13 in 108.73 seconds, CPython 3.13.13 in 106.91 seconds, and CPython 3.14.5 in 113.21 seconds. The suites ran serially because the repository shares one temporary test root. |
| Post-review renderer/profile/example/benchmark applicability | Not repeated | Review added one direct helper-level test and updated records only; production code and runtime package source are unchanged from the candidate that passed ten real-wgpu tests, both five-repeat profiles, both vertical slices, and all four diagnostic benchmark validators. Those executed results remain applicable; no new performance claim is made. |
| Final reproducible distribution and release gate | 0 | Two fresh confirmed-absent builds reproduced a pure 272,430-byte wheel at `f563d5a7f2ab11c28404462de33454108d74e68528c65742d9417dc9736a3020` and a 1,171,921-byte source distribution at `7edac507f8d7d245d295adb216f54da8b2223a6f47b4538caf87e7e024770761`. Isolated-wheel smoke, fresh ten-artifact staging, and complete portable-path release smoke passed. This factual row changes the source archive afterward; exact commit-tree artifact identities remain delegated to hosted evidence. |
| Final record-frozen source gate | 0 | The unchanged lock resolved 46 packages in 0.86 ms; all 308 Python files were format clean; Ruff and strict Pyright reported zero findings; all 19 M65 assertions passed in 1.21 seconds; all 721 architecture assertions passed in 5.16 seconds; both release-artifact tests passed in 0.66 seconds; strict docs built in 1.14 seconds with only the known upstream Material notice; and whitespace was clean. |
| Final scope, provenance, and repository audit | 0 | A post-record architecture run passed all 721 assertions in 4.97 seconds and whitespace remained clean. The 16-path scope is confined to private release smoke, one architecture test, RFC/navigation/public/maintainer documentation, roadmap/changelog, and neutral project records. No diff exists in either workflow, `src/ludoweave`, `pyproject.toml`, `uv.lock`, or the sample producer; their protected hashes remain exact. Added-line and untracked-file scans found no credential/private-key value or explicit development-tool identity. Full Git-object checking passed with no reported corruption or dangling object. |
| Initial ready PR #147 run `31521633593` | 0 | Exact initial DCO head `fce4140dd2d1b2982a1e90091dd2b157b00e861c` passed in the unchanged three Linux-first allocations. Linux `93879809651` passed in 5m24s, then macOS `93881371543` passed in 2m50s and Windows `93881371674` in 4m05s. The run is retained as initial-head evidence only and no merge claim follows. |
| Initial hosted suites and artifacts | 0 | Linux baseline and Ubuntu 3.13/3.14 each passed 2,265 tests, with one expected compatibility skip on 3.13/3.14; macOS and Windows 3.14 each passed 2,265 with one expected skip. Real-wgpu passed ten tests on each OS; profiles and both vertical slices passed. Two hosted builds reproduced a pure 272,418-byte wheel at `197a0aae2caa411c829e0ef7371ebbd61537002470a37260e25599cab6319449` and 1,172,265-byte source archive at `eedf8445a793903b9d249ed3b31b87273736ad386c1c7b30bb11ca506267f1e5`; wheel and release smoke passed. |
| First hosted review audit | Actionable | Review comment `3760580215` identified that `ZipInfo.is_dir()` is filename-based and the earlier mode guard rejected only symbolic links. FIFO, socket, character-device, and block-device modes without a trailing slash could therefore pass preflight and be materialized as regular files, contrary to RFC-0048. Merge was stopped. |
| Reviewer-derived non-regular-mode regression | 1 | The strengthened focused file failed exactly four FIFO/socket/device cases and passed 19 existing cases in 0.45 seconds against the published head. Every invalid mode wrote `payload.bin` and reached the later incomplete-bundle error instead of the stable non-regular-member preflight failure. |
| Corrected non-regular-mode focused gate | 0 | After rejecting every explicit file type other than regular while retaining unspecified type bits, all 23 focused M65 cases passed in 0.24 seconds. |
| Explicit regular/unspecified-mode compatibility proof | 0 | The valid nested-bundle fixture now mixes common-producer entries with omitted file-type bits and one explicitly encoded regular file. The changed Python files remained format/Ruff clean, full strict Pyright reported zero findings, all 23 focused cases passed in 0.41 seconds, and all 727 architecture/release assertions passed in 6.30 seconds. |
| Corrected source/static/docs gate | 0 | Initial sandboxed lock and sync commands exited 1 because the existing user uv cache was inaccessible; approved cache-access reruns resolved the unchanged 46-package lock in 1 ms and checked the 45-package graphics environment in 2 ms. All 308 Python files were format clean; Ruff and strict Pyright reported zero findings; all 727 architecture/release assertions passed in 6.12 seconds; strict docs built in 1.17 seconds with only the known upstream Material notice. |
| Corrected supported-Python gate | 0 | The graphics-enabled corrected candidate passed 2,265 tests with 14 expected skips on CPython 3.12.13 in 108.82 seconds, CPython 3.13.13 in 106.86 seconds, and CPython 3.14.5 in 112.45 seconds. The suites ran serially because the repository shares one temporary test root. |
| Corrected real-wgpu, profile, and vertical-slice gate | 0 | After restoring the locked CPython 3.12.13 graphics environment, ten real-wgpu tests passed in 6.69 seconds. Five-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced the exact M65 local state/capture with three draws and 16 sprites; Agent World Builder reproduced the exact local state/capture/replay with six query matches and five replay batches. |
| Corrected reproducible distribution and release gate | 0 | Two fresh builds reproduced a pure 272,430-byte wheel at `f563d5a7f2ab11c28404462de33454108d74e68528c65742d9417dc9736a3020` and a 1,172,451-byte source archive at `fabf9855670bef2801fa7951a5f9c38cb737fc89a1ad037548b922ca254ea154`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed with the corrected mode guard. This factual row and the documentation clarification change the source archive afterward; exact commit-tree artifact identity remains delegated to fresh hosted evidence. |

## M65 hosted feature evidence - 2026-08-12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Corrected ready PR #147 run `31523863615` | 0 | Exact amended DCO head `9de1e2e6ea11b4058bb61b4102043273715875ee` passed in exactly three Linux-first allocations. Linux `93887270228` passed in 7m32s before macOS `93889429991` and Windows `93889429975` began; they passed in 2m09s and 4m11s. |
| Hosted supported-Python and graphics suites | 0 | Linux baseline passed 2,269 tests in 131.98 seconds; Ubuntu 3.13 and 3.14 each passed 2,269 with one expected skip in 108.76 and 111.24 seconds. macOS and Windows 3.14 each passed 2,269 with one expected skip in 88.25 and 188.27 seconds. Real-wgpu passed ten tests on Linux in 9.77 seconds, macOS in 5.36 seconds, and Windows in 8.37 seconds. |
| Hosted profiles, examples, distribution, and smoke | 0 | Both profiles and both vertical slices passed on every allocated operating system. Two builds reproduced a pure 272,473-byte wheel at `4bb773ae13a5b8f4a132ef7488b783cb0249f6e4ff7e3640016c7207872c5c87` and a 1,174,818-byte source archive at `123f08b48bf2c0eef3058024182cc1389544fd70eb361c00b30b1fba73530738`. Installed-wheel, staging, and complete corrected release smoke passed. |
| Review resolution and delayed audits | 0 | Review comment `3760580215` was answered with exact correction/testing facts and its sole thread resolved after the corrected hosted pass. The first and both delayed corrected-head audits found no later issue comment, review comment, review, or unresolved thread. PR #147 remained exact-head, clean, and mergeable with all three checks successful. |
| Feature squash verification | 0 | PR #147 squash `b01335592d0e984c6b3eb6a35d31294081cff0d5` has tree `34bfb5e87ef22e56c3414a9072cbad2e0bd3c74b`, exactly matching corrected reviewed head `9de1e2e6ea11b4058bb61b4102043273715875ee`; its sole parent is exact M64 closeout `92e706961e2ecd4e2c187a205cc045a8c6506ab9`. GitHub reports a valid signature verified at `2026-08-11T18:55:10Z` and an exact parsed DCO trailer. The remote feature branch is absent, and its exact-tree-equivalent local branch was deleted. |

## M65 integration-record local evidence - 2026-08-12, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Exact scope, lock, static, architecture, docs, and whitespace gate | 0 | The diff names exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md`; no implementation/workflow/dependency surface differs from verified feature squash `b0133559`. The unchanged lock resolved 46 packages in 0.85 ms and the graphics environment checked 45 packages in 2 ms. All 308 Python files were format clean; Ruff and strict Pyright reported zero findings; all 727 architecture/release assertions passed in 6.53 seconds; strict docs built in 1.20 seconds with only the known upstream Material notice; and whitespace was clean. |
| Reproducible distribution and smoke | 0 | Two builds reproduced a pure 272,486-byte wheel at `35fd0e84a0f9117c9d60f76430651db71d6dbab2cfaddaef8fd33389373d6f06` and a 1,175,870-byte source archive at `860ea13505418586779bc265bc671bb7da15dcf0438348fbd5e330c7965ecfd5`. Isolated-wheel smoke, deterministic ten-artifact staging, and complete corrected release smoke passed. This evidence edit changes the source archive afterward, so exact commit-tree artifact identity remains delegated to the one-allocation hosted gate. |

## M65 hosted integration-record evidence - 2026-08-12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Ready PR #148 run `31525664897` | 0 | Exact four-document head `1401a2423bdbd001c359735a365f4be14a010d60` passed in one 43-second Linux allocation. The desktop compatibility umbrella skipped with zero steps. All 308 Python files were format clean; Ruff, strict docs, and all 725 documentation-selected architecture assertions passed. |
| Hosted reproducible distribution and smoke | 0 | Two builds reproduced the 272,473-byte wheel at `4bb773ae13a5b8f4a132ef7488b783cb0249f6e4ff7e3640016c7207872c5c87` and the record-updated 1,176,061-byte source archive at `d148c700f4b09a35518cb3a61e3116088f28c4549137de85ac73b7c82d799b85`. Installed-wheel smoke, deterministic staging, and complete corrected release smoke passed. |
| Integration review surfaces | 0 | The initial audit and both delayed audits found no issue comment, review comment, review, or review thread. PR #148 remained exact-head, clean, and mergeable with the Linux check successful and desktop umbrella skipped. |
| Integration squash verification | 0 | PR #148 squash `b88090a78fdd6cb4978863e0792d7741cd07efb3` has tree `2c24ce9d68e7068d745f794a423b6d6d60d971b2`, exactly matching reviewed head `1401a2423bdbd001c359735a365f4be14a010d60`; its sole parent is feature squash `b01335592d0e984c6b3eb6a35d31294081cff0d5`. GitHub reports a valid signature verified at `2026-08-11T19:04:22Z` and exact parsed DCO trailer. The remote integration branch is absent, and its exact-tree-equivalent local branch was deleted. |
| Three-record closeout local gate | 0 | The diff names exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md`; no workflow, implementation, dependency, documentation, roadmap, or release surface differs from integration squash `b88090a`. All 727 architecture/release assertions passed in 5.51 seconds; strict docs built in 1.16 seconds with only the known upstream Material notice; whitespace and full Git-object checks passed. This project-record-only closeout requests no hosted runner. |

## M64 local development evidence - 2026-08-12, Windows, CPython 3.12

M64 starts from exact synchronized M63 closeout
`a92330c5d592eaeba69e75e25dd94d83b22d367f`, tree
`86cf786b01eb92ff39fcdbdc5464540f4b3c8eea`. Only `main` existed locally and
remotely before the milestone branch was created, no pull request was open, and
the verified M63 closeout created no run or check.

| Command or review | Exit | Result |
| --- | ---: | --- |
| Pre-implementation staged-bundle measurement | 0 | A fresh unchanged-M63 build and stage produced a 111,168-byte sample ZIP with 50 members, 379,577 total declared uncompressed bytes, and a 33,018-byte largest member. |
| Initial `pytest -q tests/architecture/test_m64_bounded_sample_bundle_extraction.py` | 1 | Seven assertions failed and the protected workflow/runtime/dependency/package guard passed in 0.44 seconds. The limit constants and RFC were absent; count, member-size, and total-size fixtures wrote before later completeness failure; and valid extraction called whole-member `ZipFile.read()`. The required-file fixture was corrected to include the existing Clockwork Arena sample before production implementation. |
| First focused M64 implementation gate | Mixed | Both files were already formatted and Ruff clean. Strict Pyright reported eight intentional private-usage diagnostics in the architecture test; the seven non-documentation behavior assertions then passed in 0.29 seconds. Because the final pytest segment returned zero, the shell invocation exited zero despite the intermediate Pyright failure; no complete static pass is claimed. |
| First fail-fast focused gate | 1 | The sandboxed invocation could not open uv's existing user cache and exited before project validation. The approved rerun found both files format clean and Ruff clean, then strict Pyright rejected the file directive because explanatory prose followed the required `reportPrivateUsage=false` value and repeated the eight private-usage findings. The fail-fast command stopped before pytest and docs; no behavior or documentation pass is claimed. |
| Corrected focused M64 contract | 0 | Both changed Python files were format clean and Ruff clean; strict Pyright reported zero findings; all eight behavior, boundary, protected-surface, and documentation assertions passed in 0.27 seconds; and strict docs built in 1.05 seconds with only the known upstream Material notice. |
| Inherited architecture and release-artifact gate | 0 | All 699 architecture and release-artifact assertions passed in 5.27 seconds, including the real source scan, synthetic boundary guards, deterministic staging, and archive-content tests. |
| Complete record-inclusive source gate | 0 | The unchanged lock resolved 46 packages in 0.88 ms and the locked graphics environment checked 45 packages in 2 ms. All 307 Python files were format clean; Ruff and strict Pyright reported zero findings; all 699 architecture/release-artifact assertions passed in 5.38 seconds; strict docs built in 1.09 seconds with only the known upstream notice; and whitespace was clean. |
| Complete supported-Python candidate gate | 0 | The graphics-enabled candidate passed 2,237 tests with 14 expected skips on CPython 3.12.13 in 108.65 seconds, CPython 3.13.13 in 106.66 seconds, and CPython 3.14.5 in 113.06 seconds. The suites ran serially because the repository shares one temporary test root. |
| Real-wgpu, profiles, and vertical slices | 0 | After restoring the locked 45-package CPython 3.12.13 graphics environment, all ten real-wgpu tests passed in 7.02 seconds. Five-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`, three draws, and 16 sprites. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, six query matches, five replay batches, and passing registered tests. |
| Documented M1-M4 benchmark gate | 0 | All four fresh dirty-tree artifacts validated on Windows CPython 3.12.13. M1 accepted seven workloads with one of two historical targets observed; M2 accepted four informational workloads with no timing targets; M3 accepted six workloads with one of two historical targets met; M4 accepted three workloads with its baseline target observed. These measurements are diagnostic, not regression, support, release, or native-admission claims. |
| Pre-review reproducible distribution and release gate | 0 | Two fresh confirmed-absent builds reproduced a pure 272,185-byte wheel at `62e015de8ce562946f6658a7727a58d194b274d7da78e75107a57cf01df48b97` and a 1,159,098-byte source distribution at `8faa4bbca23cc3439f6f4837d73fe88bd71f8c5b44de97d47b0450e36300bef9`. Isolated-wheel smoke, fresh ten-artifact staging, and the complete bounded release smoke passed. |
| Findings-first scope, security, and archive review | Strengthened | Protected workflows, project metadata, lockfile, and runtime package source are byte-unchanged. The changed production/test surface has no credential-like value or backend/native import. The wheel contains 94 entries and the source archive 494 entries, with no native, WASM, bytecode, cache, site, or dist payload. Review clarified that `zipfile` parses the central directory before the member-count check and identified that exact copied-size behavior was source-guarded but not directly exercised; the RFC now states the parser boundary and two short/long stream regressions were added. |
| First strengthened focused gate | 1 | Both changed Python files were format clean, then Ruff rejected the newly added test imports as unsorted and the fail-fast command stopped before Pyright or pytest. No strengthened static or behavior pass is claimed. |
| Corrected strengthened focused and inherited gate | 0 | Both changed Python files were format clean, Ruff clean, and strict-Pyright clean. All ten M64 assertions, including short and long streamed-size mismatches, passed in 0.87 seconds; all 701 architecture/release-artifact assertions passed in 5.31 seconds. |
| Final pre-matrix record-inclusive source gate | 0 | The unchanged lock resolved 46 packages in 0.96 ms and the locked CPython 3.12 graphics environment checked 45 packages in 2 ms. All 307 Python files were format clean; Ruff and strict Pyright reported zero findings; all 701 architecture/release-artifact assertions passed in 5.38 seconds; strict docs built in 1.12 seconds with only the known upstream notice; and whitespace was clean. |
| Final supported-Python candidate gate | 0 | The reviewed graphics-enabled candidate passed 2,239 tests with 14 expected skips on CPython 3.12.13 in 108.64 seconds, CPython 3.13.13 in 107.16 seconds, and CPython 3.14.5 in 112.73 seconds. The suites ran serially because the repository shares one temporary test root. |
| Final real-wgpu, profiles, and vertical slices | 0 | After restoring the locked 45-package CPython 3.12.13 graphics environment, all ten real-wgpu tests passed in 6.78 seconds. Both five-repeat profiles validated, and Clockwork Arena plus Agent World Builder reproduced the exact state, capture, and replay identities recorded in the pre-review row. |
| Final documented M1-M4 benchmark gate | 0 | All four fresh reviewed-candidate artifacts validated on Windows CPython 3.12.13. M1 accepted seven workloads with one of two historical targets observed; M2 accepted four informational workloads with no timing targets; M3 accepted six workloads with zero of two historical targets met; M4 accepted three workloads with its baseline target observed. These observations remain diagnostic only. |
| Final pre-publication reproducible distribution and release gate | 0 | Two fresh confirmed-absent builds reproduced a pure 272,185-byte wheel at `62e015de8ce562946f6658a7727a58d194b274d7da78e75107a57cf01df48b97` and a 1,160,326-byte source distribution at `55ac4258dca4fe83ed9a9825e6289005a9edb9653af6c66a5941f16c19f1f5e4`. Isolated-wheel smoke, fresh ten-artifact staging, and complete bounded release smoke passed. This factual row changes the packaged source archive afterward; exact commit-tree artifact identities remain delegated to hosted evidence. |
| Final documentation review | Corrected | The first lines already identified M0 through M63 as integrated, but a secondary README paragraph still said M58 through M62. It now states the verified M58-through-M63 range and describes M60-M63 without claiming M64 hosted completion. |
| Final record-frozen source gate | 0 | The unchanged lock resolved 46 packages in 0.78 ms; all 307 Python files were format clean; Ruff and strict Pyright reported zero findings; all 699 architecture assertions passed in 5.47 seconds; all ten M64 assertions passed again in 0.38 seconds; strict docs built in 1.12 seconds with only the known upstream notice; and whitespace was clean. |
| Post-record architecture and scope gate | 0 | All 699 architecture assertions passed in 4.85 seconds; whitespace was clean; and the status/diff inventory contained exactly the intended M64 records, public documentation, RFC/nav, private release-smoke implementation, and architecture-test surfaces. Untracked RFC/test files are included in the intended staging scope even though `git diff --name-only` does not list untracked paths. |
| Initial ready PR #144 CI run `31513476270` | 0 | Exact initial head `c5813633f8ff7970311cc7ab8e1159f844c056f7` passed in exactly three Linux-first allocations. Linux `93852742523` passed in 7m33s before macOS `93854944611` and Windows `93854944488` began; they passed in 2m56s and 4m28s. Linux baseline passed 2,243 tests; Ubuntu 3.13/3.14 and both desktop 3.14 suites each passed 2,243 with one expected skip. All real-wgpu, profile, vertical-slice, reproducibility, installed-wheel, staging, and release-smoke slices passed. |
| Initial hosted artifacts | 0 | Two builds reproduced a pure 272,176-byte wheel at `80a52b31109504d23a6d4fc5c5c36c9427c3f3d11ef3a2fa83362043236aedc4` and a 1,160,677-byte source archive at `d0b61cc6b97aabdf2eeb6166385dad6c1201858b5b647aee359426a9d7e9efdf`; installed-wheel and complete release smoke passed. |
| First hosted review audit | Actionable | Review identified that CPython's BZIP2/LZMA `ZipExtFile` paths decompress an input chunk without the deflate path's maximum-output argument before truncating to declared size. A forged small central-directory size could therefore bypass M64's intended memory bound. Exact managed CPython source inspection confirmed stored reads directly and deflated reads with a maximum output, while other codecs call `decompress(data)` without a limit. Merge was stopped. |
| Reviewer-derived codec regression on initial hosted head | 1 | The strengthened focused file failed exactly three assertions and passed ten in 0.48 seconds: the stored/deflated admission constant was absent, and BZIP2 plus LZMA fixtures wrote before later incomplete-bundle failure instead of failing preflight with the stable unsupported-method error. |
| First codec-correction focused gate | 1 | The fail-fast command stopped immediately because Ruff formatting reported the strengthened test would be reformatted. One file was then mechanically formatted; no static, behavior, or documentation pass is claimed from this invocation. |
| Second codec-correction focused gate | 1 | Both files were format clean, then Ruff's Yoda-condition rule rejected the direct private-module set comparison and the fail-fast command stopped before Pyright, pytest, or docs. The test now names the expected set before comparison; no complete pass is claimed. |
| Third codec-correction focused gate | 1 | Both files remained format clean, but Ruff still classified the private constant on the comparison's left as a Yoda condition. The local expected-set variable is now on the left; the command again stopped before later checks and no complete pass is claimed. |
| Corrected codec focused gate | 0 | Both changed Python files were format clean, Ruff clean, and strict-Pyright clean. All 13 M64 assertions passed in 0.31 seconds, including stored acceptance, BZIP2/LZMA preflight rejection, and the earlier count/size/streaming contracts. Strict docs built in 1.11 seconds with only the known upstream notice. |
| Strengthened codec and inherited gate | 0 | After locking codec terms into source/document structure, both files remained format/Ruff/Pyright clean; all 13 M64 assertions passed in 0.29 seconds; all 704 architecture/release-artifact assertions passed in 5.29 seconds; strict docs built in 1.12 seconds with only the known upstream notice; and whitespace was clean. |
| Complete codec-corrected source gate | 0 | The unchanged lock resolved 46 packages in 0.80 ms and the locked graphics environment checked 45 packages in 2 ms. All 307 Python files were format clean; Ruff and strict Pyright reported zero findings; all 704 architecture/release-artifact assertions passed in 5.42 seconds; strict docs built in 1.11 seconds with only the known upstream notice; and whitespace was clean. |
| Complete codec-corrected supported-Python gate | 0 | The corrected graphics-enabled candidate passed 2,242 tests with 14 expected skips on CPython 3.12.13 in 108.68 seconds, CPython 3.13.13 in 106.69 seconds, and CPython 3.14.5 in 112.70 seconds. The suites ran serially because the repository shares one temporary test root. |
| Codec-corrected real-wgpu, profiles, and vertical slices | 0 | After restoring the locked CPython 3.12.13 graphics environment, all ten real-wgpu tests passed in 6.85 seconds. Both five-repeat profiles validated; Clockwork Arena and Agent World Builder reproduced the previously recorded local state, capture, and replay identities. |
| Codec-corrected reproducible distribution and release gate | 0 | Two fresh confirmed-absent builds reproduced a pure 272,239-byte wheel at `38eb28c126aa0245744ded463c3d327423c25b99375c0a9680a7012723c4c7c0` and a 1,163,429-byte source distribution at `a2750f2411faac4e1a2aa5b72ef63b5bd9b2bdfed843e1613492594fe89dfee0`. Isolated-wheel smoke, fresh ten-artifact staging, and the corrected complete release smoke passed. The diagnostic M1-M4 benchmarks were not repeated because the correction changes only private release-smoke archive admission and documentation; their earlier reviewed-candidate results remain applicable to unchanged runtime code. |
| Final codec-correction record-inclusive source gate | 0 | The unchanged lock resolved 46 packages in 0.94 ms; all 307 Python files were format clean; Ruff and strict Pyright reported zero findings; all 704 architecture/release-artifact assertions passed in 5.84 seconds; strict docs built in 1.09 seconds with only the known upstream notice; and whitespace was clean. |

## M64 hosted feature evidence - 2026-08-12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Corrected ready PR #144 CI run `31515782370` | 0 | Exact corrected head `8b6861df891f12d194bc9b7e98b41ac8ab81f7d1` passed in exactly three Linux-first allocations. Linux `93860439338` passed in 7m13s before macOS `93862476671` and Windows `93862476577` began; they passed in 2m55s and 4m06s. |
| Hosted supported-Python and graphics suites | 0 | Linux baseline passed 2,246 tests in 127.19 seconds; Ubuntu 3.13 and 3.14 each passed 2,246 with one expected skip in 107.93 and 109.64 seconds. Windows and macOS 3.14 each passed 2,246 with one expected skip in 185.20 and 121.22 seconds. Real-wgpu passed ten tests on Linux in 13.22 seconds, Windows in 9.42 seconds, and macOS in 8.76 seconds. |
| Hosted profiles, examples, distribution, and smoke | 0 | Both profiles, Clockwork Arena, Agent World Builder, staging, installed-wheel smoke, and complete release smoke passed. Two builds reproduced a pure 272,227-byte wheel at `4eb1cb0b2524f188056c619c7e5757b41c739ff3d889f49982c026dba7a60a3b` and a 1,163,806-byte source archive at `718d719b0c0c40cf1af93aa5e5aa398fbfbdd5439de1067003deb6dba40c69b2`. |
| Corrected-head review surfaces | 0 | The first and both delayed audits found no new issue comment, review comment, or unresolved thread. The earlier BZIP2/LZMA finding remained answered and resolved; the PR stayed clean, mergeable, and exact-head with all three checks successful. |
| Feature squash verification | 0 | PR #144 squash `8399e0f94838f455ead604eceee0a17e1b2c9a91` has tree `3f46ec8c23a044a20823a7d9132906cc2efdb3fa`, exactly matching the corrected reviewed head; its sole parent is exact M63 closeout `a92330c5d592eaeba69e75e25dd94d83b22d367f`. GitHub reports a valid signature. Both source commits carry exact DCO sign-offs. The merge command passed escaped newline text in its body, which GitHub preserved literally, so the squash message is not claimed to contain a standalone parsed DCO trailer. The merged feature branch is absent remotely. |

## M64 integration-record local evidence - 2026-08-12, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Exact scope, lock, static, architecture, docs, and whitespace gate | 0 | The diff named exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md`; whitespace was clean; the unchanged lock resolved 46 packages in 0.76 ms; all 307 Python files were format clean; Ruff and strict Pyright reported zero findings; all 702 architecture assertions passed in 5.10 seconds; and strict docs built in 1.09 seconds with only the known upstream Material notice. |
| Reproducible distribution and smoke | 0 | Two builds reproduced a pure 272,239-byte wheel at `38eb28c126aa0245744ded463c3d327423c25b99375c0a9680a7012723c4c7c0` and a 1,163,698-byte source archive at `c08fb4bab14fa51c4ec1d6499e016bec2d32184e3b0b3abe1a8d1817e9830e3d`. Isolated-wheel smoke, deterministic ten-artifact staging, and complete bounded release smoke passed. This evidence edit changes the source archive afterward, so exact commit-tree artifact identities remain delegated to hosted evidence. |

## M64 hosted integration-record evidence - 2026-08-12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Ready PR #145 CI run `31517725574` | 0 | Exact four-document head `49857245d37aaf8ea1b8a0cf702897a17b3f79ab` passed in one 42-second Linux allocation. All 307 Python files were format clean; Ruff, strict docs, and all 702 architecture assertions passed. The desktop umbrella skipped with zero steps. |
| Hosted reproducible distribution and smoke | 0 | Two builds reproduced the 272,227-byte wheel at `4eb1cb0b2524f188056c619c7e5757b41c739ff3d889f49982c026dba7a60a3b` and the record-updated 1,163,996-byte source archive at `d6ed5eef92c48c40f97749ad95d69b718551bafbd1024b8ee69e8dd517bbd077`. Installed-wheel smoke, deterministic staging, and complete release smoke passed. |
| Integration review surfaces | 0 | The initial audit and two delayed audits found no issue comment, review comment, review, or review thread. The PR remained clean, mergeable, and exact-head. |
| Integration squash verification | 0 | PR #145 squash `6f3c0352420d39f9c4666101f7de3c23a52ac2d2` has tree `7fec531dd168a8ae96a074177d72c9589975264c`, exactly matching the reviewed head; its sole parent is feature squash `8399e0f94838f455ead604eceee0a17e1b2c9a91`. GitHub reports a valid signature and exact parsed DCO trailer. |
| Three-record closeout local gate | 0 | The diff named exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md`; all 702 architecture assertions passed in 5.07 seconds; and whitespace was clean. No hosted validation is requested for this project-record-only closeout. |

The pending exact three-record closeout requests no hosted runner and will
establish the clean M65 selection base after review and verified squash.

## M63 local development evidence - 2026-08-12, Windows, CPython 3.12

M63 starts from exact synchronized M62 closeout
`1cdc1b452cbe79c9e4f082acb4dd1205f4b3648f`. The worktree was clean, local
`main`, `origin/main`, and `origin/HEAD` matched, only `main` remained after
remote pruning, no pull request was open, and GitHub reported the closeout
squash signature valid with the exact reviewed tree and parsed DCO trailer.

| Command or review | Exit | Result |
| --- | ---: | --- |
| Initial `pytest -q tests/architecture/test_m63_public_release_output_confinement.py` | 1 | Ten assertions failed and the protected-surface guard passed in 0.46 seconds against unchanged M62 production code. Smoke stdout/stderr escaped on success, nonzero failure, and exception; boolean and float zero values were accepted as success; hostile comparison hooks escaped; and RFC-0046 was absent. |
| First focused M63 implementation gate | 1 | Ruff formatting/linting were clean, but strict Pyright rejected the test's annotation of pytest's non-public `CaptureResult` type and stopped before the behavior command. No focused static or behavior pass is claimed from this invocation. |
| Corrected focused M63 behavior and static gate | 0 | After returning plain `(status, stdout, stderr)` values from the helper, both changed Python files were format clean, Ruff clean, and strict-Pyright clean. All ten non-documentation assertions passed with the docs case deselected in 0.69 seconds. |
| Complete documented M63 contract | 0 | All 11 behavior, protected-surface, and documentation assertions passed in 0.24 seconds; strict docs built in 1.14 seconds with only the known upstream notice. |
| First inherited architecture gate | 1 | 685 assertions passed and three inherited literal guards failed: M45 and M46 still required the direct smoke call, while M62 required an exact stale completed-milestone string. The release-draft suite did not run after the failure. |
| First strengthened inherited gate | 1 | 687 assertions passed and one M45 ordering guard still required the direct smoke-call literal. The release-draft suite did not run after the failure. |
| Corrected inherited contract gate | 0 | After updating the remaining order guard and making the completed-milestone guards monotonic, all 688 architecture assertions passed in 4.81 seconds; the release-draft suite passed 56 tests with two expected platform-capability skips in 5.15 seconds. |
| First record-inclusive source gate | Corrected | A sandboxed lock invocation exited before project validation because uv's existing user cache was inaccessible. The approved rerun resolved the unchanged 46-package lock in 1 ms; all 306 Python files were format clean; Ruff and strict Pyright reported zero findings; all 688 architecture assertions passed in 4.82 seconds; all 11 then-current M63 assertions passed in 0.35 seconds; and strict docs built in 1.14 seconds with only the known upstream notice. |
| Complete supported-Python candidate gate | 0 | The graphics-enabled candidate passed 2,228 tests with 14 expected skips on CPython 3.12.13 in 106.11 seconds, CPython 3.13.13 in 105.77 seconds, and CPython 3.14.5 in 111.12 seconds. The suites ran serially because the repository shares one temporary test root. |
| Real-wgpu, profiles, and vertical slices | 0 | After restoring the locked 45-package CPython 3.12.13 graphics environment, all ten real-wgpu tests passed in 6.86 seconds. Five-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`, three draws, and 16 sprites. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, six query matches, five replay batches, and passing registered tests. |
| Documented M1-M4 benchmark gate | 0 | All four fresh dirty-tree artifacts validated on Windows CPython 3.12.13. M1 accepted seven workloads with one of two historical targets observed; M2 accepted four informational workloads with no timing targets; M3 accepted six workloads with zero of two historical targets met; M4 accepted three workloads with its baseline target observed. These measurements are diagnostic, not regression, support, release, or native-admission claims. |
| Pre-review reproducible distribution and release gate | 0 | Two confirmed-absent builds reproduced a pure 272,051-byte wheel at `9ecf0cc835b1cc61628e9045e593bbbe0a2ac7d36e40f672aa304926dcb86125` and a 1,149,252-byte source distribution at `578bcd2b6bc0226e483b99d54efeb9ab934cff0af2e6d80c8aab0342cdeec67c`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed. Archive review found 94 wheel entries and 492 source entries with no native, WASM, bytecode, cache, site, or dist payload. Findings-first review changed tests and records afterward, so these are not final exact-tree artifacts. |
| Reviewer-derived exception-restoration regression | Corrected | Review found that smoke exception restoration was covered but validator exception restoration was only implied. The added direct regression proves subordinate output is discarded and process streams are restored. Focused formatting, Ruff, and strict Pyright passed; all 12 M63 assertions passed in 0.80 seconds and all 689 architecture assertions passed in 4.67 seconds. The chained command then exited 1 because it named nonexistent `tests/integration/test_release_draft_workflow.py`; no release-draft result is claimed from that invocation. |
| Corrected release-draft path | 0 | The actual `tests/unit/test_release_draft_integrity.py` suite passed 56 tests with two expected platform-capability skips in 5.15 seconds. |
| Findings-first scope and security review | 0 | The retired metadata directory is absent; the then-changed surface contained no automation-identity marker, credential-like value, backend/native leakage, or whitespace error. CI, release workflow, project metadata, lockfile, and runtime package source are byte-unchanged. The review found and corrected only the exception-restoration evidence gap above. |
| First final record-inclusive source gate | 1 | Lock, graphics-environment, whole-tree formatting, Ruff, and strict Pyright passed; architecture then reported 688 passes and one metadata-hygiene failure because the two records above had newly named the retired directory literally. The command stopped before later focused, release-draft, documentation, or whitespace checks. No complete source-gate pass is claimed from this invocation. |
| Corrected final record-inclusive source gate | 0 | After removing those literal markers, the unchanged lock resolved 46 packages in 0.93 ms and the locked graphics environment checked 45 packages in 4 ms. All 306 Python files were format clean; Ruff and strict Pyright reported zero findings; all 689 architecture assertions passed in 4.85 seconds; all 12 M63 assertions passed in 0.35 seconds; the release-draft suite passed 56 tests with two expected skips in 6.10 seconds; strict docs built in 1.12 seconds with only the known upstream notice; and whitespace was clean. |
| Final complete supported-Python candidate gate | 0 | The final graphics-enabled candidate passed 2,229 tests with 14 expected skips on CPython 3.12.13 in 113.25 seconds, CPython 3.13.13 in 114.58 seconds, and CPython 3.14.5 in 120.27 seconds. The suites ran serially because the repository shares one temporary test root. |
| Final real-wgpu, profiles, and vertical slices | 0 | After restoring the locked 45-package CPython 3.12.13 graphics environment, all ten real-wgpu tests passed in 7.30 seconds. Five-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`, three draws, and 16 sprites. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, six query matches, five replay batches, and passing registered tests. |
| Final documented M1-M4 benchmark gate | 0 | All four fresh final-candidate artifacts validated on Windows CPython 3.12.13. M1 accepted seven workloads with one of two historical targets observed; M2 accepted four informational workloads with no timing targets; M3 accepted six workloads with zero of two historical targets met; M4 accepted three workloads with its baseline target observed. These observations remain diagnostic only. |
| Final pre-publication reproducible distribution and release gate | 0 | Two fresh confirmed-absent builds reproduced a pure 272,051-byte wheel at `9ecf0cc835b1cc61628e9045e593bbbe0a2ac7d36e40f672aa304926dcb86125` and a 1,150,415-byte source distribution at `3f525366eb17333665c011cfa76a658a87799f56b40f8e69fd019638ef412c29`. Isolated-wheel smoke, fresh ten-artifact staging, complete release smoke, and archive review passed. The archives contain 94 wheel and 492 source entries with no native, WASM, bytecode, cache, site, or dist payload. This factual row changes the packaged source archive afterward; exact commit-tree identities remain delegated to hosted evidence. |
| Final record-only source gate | 0 | The unchanged lock resolved 46 packages in 0.89 ms; all 306 Python files were format clean; Ruff and strict Pyright reported zero findings; all 689 architecture assertions passed in 5.66 seconds; all 12 M63 assertions passed in 0.37 seconds; strict docs built in 1.24 seconds with only the known upstream notice; and whitespace was clean. |

## M63 hosted feature evidence - 2026-08-12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Ready PR #141 CI run `31507526704` | 0 | Exact head `8fe7518efb1855c69f3f093eba921721421072ce` passed in exactly three Linux-first allocations. Linux `93832810911` passed in 7m07s before macOS `93835048148` and Windows `93835048154` began; they passed in 2m59s and 3m11s. |
| Hosted tests and vertical slices | 0 | Linux baseline passed 2,233 tests; Ubuntu 3.13 and 3.14 each passed 2,233 with one expected skip. macOS and Windows real-wgpu, graphics profiles, Clockwork Arena, and Agent World Builder passed; each desktop 3.14 suite passed 2,233 tests with one expected skip. State and replay identities remained stable; renderer capture bytes retained their documented platform dependence. |
| Hosted reproducible distribution and smoke | 0 | Two builds reproduced a pure 272,038-byte wheel at `df7348f0a9911611e1df59e91151b00320f8a4a5a86fcf97def39ac008d41b22` and a 1,151,376-byte source archive at `eb400512913e1d2cd748dc93f1c4bab26699d4878edb882e54cab2661c261cfb`. Installed-wheel staging and complete ten-artifact release smoke passed. |
| Review surfaces | 0 | The initial audit and two delayed audits found no issue comment, review comment, review, review decision, or external commit status. The PR remained clean, mergeable, and exact-head with all three checks successful. |
| Feature squash verification | 0 | PR #141 squash `e0f1dc683d5e38b69d01d342f843074470a8418a` has tree `5ba0be8a3e600963a3ced06030963edf454e07a9`, exactly matching the reviewed head; its sole parent is exact M62 closeout `1cdc1b452cbe79c9e4f082acb4dd1205f4b3648f`. GitHub reports a valid signature and the exact parsed DCO trailer. |
| Local synchronization and branch cleanup | Corrected | Local `main` fast-forwarded to the verified squash. Ordinary branch deletion correctly refused because squash integration does not preserve feature ancestry; after exact tree equality was already proven, the authorized force-delete removed only the merged local feature branch. The remote feature branch was already deleted. |
| Integration-record preparation | Corrected | The first atomic four-record patch stopped without changing a file because the workspace drive was full while the sandbox wrote its setup log. Only verified generated `.tmp`, pytest-temp, site, and dist outputs inside the workspace were removed; they are reproducible, and source/Git state remained clean. The same bounded patch then applied successfully. |
| First four-record local source gate | 1 | Exact four-file scope, lock, no-graphics sync, formatting, and Ruff passed. Strict Pyright then reported 17 expected missing/unknown optional-renderer diagnostics because the command had removed the graphics extra immediately before whole-project type checking. The command stopped before architecture, docs, and whitespace; no complete pass is claimed. |
| Corrected four-record local source gate | 0 | After restoring all six exact locked graphics packages, all 306 Python files were format clean; Ruff and strict Pyright reported zero findings; all 689 architecture assertions passed in 4.89 seconds; strict docs built in 1.01 seconds with only the known upstream notice; and whitespace was clean. |
| Four-record reproducible distribution and release gate | 0 | Two fresh builds reproduced a pure 272,051-byte wheel at `9ecf0cc835b1cc61628e9045e593bbbe0a2ac7d36e40f672aa304926dcb86125` and a 1,152,579-byte source distribution at `ba86098f1015aba3197fa11dc79459c14b26047ff5a420488b56987f140ccfc5`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed. This row changes the source archive afterward, so exact integration-head identities remain delegated to hosted evidence. |
| Final four-record source gate | 0 | Exact four-file scope passed; the unchanged lock resolved 46 packages in 0.77 ms; all 306 Python files were format clean; Ruff and strict Pyright reported zero findings; all 689 architecture assertions passed in 4.74 seconds; strict docs built in 1.06 seconds with only the known upstream notice; and whitespace was clean. |

## M63 hosted integration-record evidence - 2026-08-12

| Command or review | Exit | Result |
| --- | ---: | --- |
| Ready PR #142 CI run `31509382982` | 0 | Exact four-document head `88ec556325bfbb278232dbfafb546a066e266b63` passed in one 41-second Linux allocation. All 306 files were format clean; Ruff, strict docs, and all 689 architecture assertions passed. The desktop umbrella skipped with zero steps. |
| Hosted reproducible distribution and smoke | 0 | Two builds reproduced the 272,038-byte wheel at `df7348f0a9911611e1df59e91151b00320f8a4a5a86fcf97def39ac008d41b22` and the record-updated 1,152,973-byte source archive at `445df3aaae7877ef2aa485033f59e29da48ab96a111e869d0a47d5c77228f386`. Installed-wheel and complete release smoke passed. |
| Integration review surfaces | 0 | The initial audit and two delayed audits found no issue comment, review comment, review, or review decision. The PR remained clean, mergeable, and exact-head. |
| Integration squash verification | 0 | PR #142 squash `abc51243e5e4612f5e7f1ca20cb5eeedb6dc0a8a` has tree `86c4cbd8d24dfa3c0e81dc115d2765a273bfdb7c`, exactly matching the reviewed head; its sole parent is feature squash `e0f1dc683d5e38b69d01d342f843074470a8418a`. GitHub reports a valid signature and exact parsed DCO trailer. |
| Three-record closeout local gate | 0 | Exact three-file scope passed; all 689 architecture assertions passed in 4.87 seconds; and whitespace was clean. No hosted validation is requested for this project-record-only closeout. |

The pending three-record closeout requests no hosted runner and will establish
the exact M64 base after review and verified squash integration.

## M62 local development evidence - 2026-08-12, Windows, CPython 3.12

M62 starts from exact synchronized M61 closeout
`14f848c92021d54c9140e01b0333c0725c45145d`. The worktree was clean, local
`main`, `origin/main`, and `origin/HEAD` matched, only `main` remained after
remote pruning, no pull request was open, and GitHub reported the closeout
squash signature valid with the exact reviewed tree and parsed DCO trailer.

| Command or review | Exit | Result |
| --- | ---: | --- |
| Initial `pytest -q tests/architecture/test_m62_public_release_asset_names.py` | 1 | Fourteen assertions failed and two passed in 0.51 seconds against unchanged production code. All 11 nonportable names were accepted, case-only duplicates were accepted, the invalid existing plan reached an intentionally forbidden asset download, and RFC-0045 was absent. The representative portable names and protected-surface guard passed. |
| First focused M62 implementation gate | 1 | All 15 non-documentation assertions passed with the docs case deselected in 0.23 seconds and Ruff was clean, but formatting identified one test file and strict Pyright identified an untyped validator lambda. No focused static pass is claimed from this command. |
| Corrected focused M62 behavior and static gate | 0 | After replacing the lambda with a typed function and formatting the test, both changed Python files were formatted, Ruff clean, and strict-Pyright clean. All 15 non-documentation assertions passed with the docs case deselected in 0.22 seconds. |
| Complete documented M62 contract | 0 | All 16 behavior, protected-surface, and documentation assertions passed in 0.23 seconds; strict docs built in 1.08 seconds with only the known upstream notice. |
| First combined architecture and release-draft attempt | 1 | The two pytest processes were mistakenly launched concurrently despite the repository's shared `.pytest-tmp` root. The architecture process reported 675 passes, one substantive stale M45 literal-guard failure, and one setup error caused by the temporary-root collision. The independently completed release-draft process passed 56 tests with two platform-capability skips in 5.74 seconds. No architecture pass is claimed from this attempt. |
| Corrected sequential architecture gate | 0 | After the inherited M45 contract was strengthened to require casefolded name keys and the portable-name predicate, all 677 architecture assertions passed in 4.79 seconds. |
| Whole-tree static and documentation gate | 0 | All 305 Python files were format clean; Ruff and strict Pyright reported zero findings; strict docs built in 1.36 seconds with only the known upstream notice. |
| Complete supported-Python candidate gate | 0 | The graphics-enabled candidate passed 2,217 tests with 14 expected skips on CPython 3.12.13 in 105.33 seconds, CPython 3.13.13 in 113.10 seconds, and CPython 3.14.5 in 119.76 seconds. The suites ran serially because the repository shares one temporary test root. |
| Real-wgpu, profiles, and vertical slices | 0 | After restoring the locked CPython 3.12.13 graphics environment, all ten real-wgpu tests passed in 7.43 seconds. Five-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`, three draws, and 16 sprites. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, six query matches, five replay batches, and passing registered tests. |
| Documented M1-M4 benchmark gate | 0 | All four fresh dirty-tree artifacts validated on Windows CPython 3.12.13. M1 accepted seven workloads with one of two historical targets observed; M2 accepted four informational workloads with no timing targets; M3 accepted six workloads with zero of two historical targets met; M4 accepted three workloads with its baseline target observed. These measurements are diagnostic, not regression, support, release, or native-admission claims. |
| First record-inclusive local source gate | 0 | The unchanged lock resolved 46 packages in 0.92 ms. All 305 Python files were format clean; Ruff and strict Pyright reported zero findings; all 677 architecture assertions passed in 5.49 seconds; all 16 M62 assertions passed in 0.34 seconds; strict docs built in 1.24 seconds with only the known upstream notice. |
| Pre-review reproducible distribution and release gate | 0 | Two confirmed-absent builds reproduced a pure 271,854-byte wheel at `6687d3e57dd8781e90e0159ce6d40cdaa4297adcf306a84c618512880e498710` and a 1,141,325-byte source distribution at `e5ce56c6cbc68206615c668cc13ca90a4745f686b1e496e7f3ea5aad97c2fe2e`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed. Archive review found 94 wheel entries and 490 source entries with no native, WASM, bytecode, cache, site, or dist payload. Findings-first review changed documentation afterward, so these are not final exact-tree artifacts. |
| Reviewer-derived stale-status regression | Expected failure | The new documentation assertion failed with 15 passes because README still claimed only M0 through M59 were integrated even though M60 and M61 are complete. No corrected pass is claimed from this probe. |
| First reviewer-correction verification invocation | 1 | The command mistakenly included `README.md` in Ruff's Python-format inputs and stopped with the expected experimental-Markdown-format error before behavior or documentation checks. No pass is claimed from this invocation. |
| Corrected reviewer-status gate | 0 | The Python regression file was format clean, Ruff clean, and strict-Pyright clean. All 16 M62 assertions passed in 0.23 seconds after README stated completed M61 and the stale internal M61 closeout sentence was repaired; strict docs built in 1.12 seconds with only the known upstream notice. |
| Frozen post-review source and integrity gate | 0 | The unchanged lock resolved 46 packages in 0.89 ms. All 305 Python files were format clean; Ruff and strict Pyright reported zero findings; all 677 architecture assertions passed in 4.99 seconds; all 16 M62 assertions passed in 0.38 seconds; strict docs built in 1.11 seconds with only the known upstream notice. Whitespace and full Git-object checking passed, with only expected unreachable historical objects. Workflow, project metadata, lock, runtime package, and benchmark surfaces are unchanged. Added-line credential scanning and the current-tree tool-identity scan returned no match. |
| Frozen post-review distribution and release gate | 0 | Two new confirmed-absent builds reproduced a pure 271,887-byte wheel at `ad034f17c823a63a0b372e1f2d73d4e2e36fc1f417c7fcbeea39c3b5fae61ef1` and a 1,142,219-byte source distribution at `5cb2860add01e48285c643e84d46f86008f2f0a7be70dcb77e00c642c5f11217`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed. Archive review found 94 wheel entries and 490 source entries with no native, WASM, bytecode, cache, site, or dist payload. This factual row changes the packaged source archive afterward, so hosted exact-head artifact identity remains authoritative. |
| Findings-first scope and correctness review | 0 | No actionable M62 issue remains after the stale completion-boundary correction. The parser preserves exact portable ASCII names, rejects classic Windows device stems, trailing periods, over-255-character names, and case-only collisions before asset download/output creation with stable content-silent failure. No filesystem probing, normalization, rewriting, workflow, dependency, lock, version, runtime package/API, backend/native implementation, release authority, tag, release, or publication was added. |
| Hosted exact-head feature gate | 0 | Ready PR #138 exact head `3bb7539463e34859b5ef8a63d2ea4bc1ff4c2cb2` passed run `31501434063` in exactly three Linux-first allocations. Linux job `93812142249` passed in 7m20s before macOS `93814459679` and Windows `93814459742` began; they passed in 3m11s and 4m18s. Linux baseline passed 2,221 tests; Ubuntu CPython 3.13/3.14 and both desktop CPython 3.14 suites passed 2,221 with one expected skip. Every platform passed ten real-wgpu tests, profile smoke, Clockwork Arena, and Agent World Builder. Hosted distributions reproduced a 271,874-byte wheel (`00c026e3800aa4ab4f46adc55bc91e21a0d09a9bfecf22a0b882a3b2349f306a`) and 1,142,880-byte source distribution (`efe8f58254a38949d9ae3b170d4b8d6f369c55fe65fc6616d48011bf06b7bcde`); installed-wheel and complete ten-artifact release smoke passed. |
| Hosted review and exact-tree squash audit | 0 | Two delayed audits found zero issue comments, reviews, or threads. PR #138 was ready, `MERGEABLE/CLEAN`, exact-head/exact-base, and had exactly three successful checks. Head-pinned GitHub-verified squash `a96fac6b4fdd2eb3c0d65ede17f66cede2faa232` has tree `0bbacc706be88a4aab7ed13a444f1657db90fdb6` exactly equal to reviewed head `3bb7539463e34859b5ef8a63d2ea4bc1ff4c2cb2`, sole parent M61 closeout `14f848c92021d54c9140e01b0333c0725c45145d`, a valid signature, and standalone DCO. The first redundant local `^{tree}` command was misquoted by PowerShell and produced no valid comparison; the corrected quoted invocation proved both trees equal. The merged feature branch was deleted locally/remotely, and only synchronized `main` remained before the integration-record branch was created. |
| Four-file integration-record local gate | 0 | Exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md` changed. The unchanged lock resolved 46 packages in 0.87 ms; all 305 Python files were format clean; Ruff and strict Pyright reported zero findings; all 677 architecture assertions passed in 6.59 seconds; strict docs built in 1.50 seconds with only the known upstream notice; whitespace was clean. Two confirmed-absent builds reproduced the pure 271,887-byte wheel (`ad034f17c823a63a0b372e1f2d73d4e2e36fc1f417c7fcbeea39c3b5fae61ef1`) and 1,144,202-byte source distribution (`966586340111cf6dc79f712d0548c09c1c00cb5d5a00be12d831a60227fbce78`); isolated-wheel and complete ten-artifact release smoke passed. This factual row changes the packaged source archive afterward, so hosted integration-head identities remain authoritative. |
| Final integration-record evidence-inclusive gate | 0 | The unchanged lock resolved 46 packages in 1 ms; all 305 Python files remained format clean; Ruff and strict Pyright reported zero findings; all 677 architecture assertions passed in 7.74 seconds; strict docs built in 1.81 seconds with only the known upstream notice. Whitespace, exact four-file scope, and full Git-object checking passed, with only expected unreachable historical objects. |
| Integration-record hosted gate | 0 | PR #139 exact head `5252987bc6b1da546f49f09b9358a2735e6b34f1` passed run `31503119877` in one 41-second Linux allocation. The trusted classifier selected documentation scope; all 305 Python files were format clean, Ruff passed, strict docs built, all 677 documentation architecture assertions passed in 8.67 seconds, and reproducible build plus installed-wheel and complete release smoke passed. The exact-head 271,874-byte wheel was `00c026e3800aa4ab4f46adc55bc91e21a0d09a9bfecf22a0b882a3b2349f306a`; the 1,144,309-byte source distribution was `84f40929144a7e28f01c5a55a4e423ec370d110a704e4cbef19d9ea63ca98f09`. Desktop umbrella `93818148618` skipped with zero steps and no runner allocation. |
| Integration-record review, squash, and cleanup audit | 0 | Two delayed audits found exact head/base, `MERGEABLE/CLEAN`, one successful Linux check, one zero-step skipped umbrella, and no issue comment, review, or thread. Head-pinned GitHub-verified squash `de6ead04124b889318b5ab854d25a6b5324d05aa` has tree `baa594eb17a548482b81ef11e868ce0d4175051b` exactly equal to reviewed record head `5252987bc6b1da546f49f09b9358a2735e6b34f1`, sole parent feature squash `a96fac6b4fdd2eb3c0d65ede17f66cede2faa232`, a valid signature, and standalone DCO. Both merged working branches were deleted locally/remotely; only synchronized `main` remained before the closeout branch was created. |
| Three-file closeout prepublication audit | 0 | The unchanged lock resolved 46 packages in 0.93 ms; all 305 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 677 architecture assertions passed in 5.22 seconds; strict docs built in 1.20 seconds with only the known upstream notice. Exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md` changed; workflow, metadata, lock, runtime, tests, benchmarks, scripts, public docs, and roadmap are unchanged. Whitespace and full Git-object checking passed with only expected unreachable historical objects. `main`, `origin/main`, and the closeout parent resolve to verified integration squash `de6ead04124b889318b5ab854d25a6b5324d05aa`; only remote `main` exists. No open pull request, post-integration `main` run, tag, or GitHub release exists. |

No closeout merge is claimed yet.

## M61 local development evidence - 2026-08-11, Windows, CPython 3.12

M61 starts from exact synchronized M60 closeout
`a8fc787a7b04b4fe8ed3766167e58258aa62c8d6`. The worktree was clean, local
`main`, `origin/main`, and `origin/HEAD` matched, only `main` remained after
remote pruning, no pull request was open, and GitHub reported the closeout
squash signature valid with the exact reviewed tree and parsed DCO trailer.

| Command or review | Exit | Result |
| --- | ---: | --- |
| Initial `pytest -q tests/architecture/test_m61_public_release_root_separation.py` | 1 | Six assertions failed and two passed against unchanged production code. Both direct overlap cases, the resolved-parent-alias case, and both content-silent resolution-failure cases reached the intentionally forbidden download path. The documentation contract named the intentionally absent RFC-0044. The separate candidate-child layout and protected-surface guard passed. |
| Focused M61 behavior and boundary group | 0 | Seven non-documentation assertions passed with one documentation assertion deselected in 0.21 seconds after strict root resolution and overlap rejection were implemented. |
| Focused format, Ruff, and strict Pyright | 0 | Both changed Python files were already formatted, Ruff reported no finding, and strict Pyright reported zero diagnostics. |
| First documented M61 contract | 1 | Seven assertions passed and the documentation assertion required the ordering phrase `before validator` explicitly rather than only the combined wording `before network or validator`. Focused static checks were clean and strict docs built in 1.12 seconds. |
| Corrected complete M61 contract and strict docs | 0 | All eight M61 assertions passed in 0.20 seconds after the ordering statement was made explicit. Strict docs built in 1.06 seconds with only the known upstream notice. |
| First inherited public-release boundary selector | 4 | Pytest stopped before collection because the command guessed nonexistent `tests/unit/test_release_draft.py`; no inherited-boundary pass is claimed from that attempt. |
| Corrected M45-M61/release-draft boundary | 0 | Using actual `tests/unit/test_release_draft_integrity.py`, 346 tests passed with two platform-capability skips in 7.56 seconds. |
| Whole-tree static, architecture, and documentation gate | 0 | The unchanged lock resolved 46 packages in 0.80 ms and checked the locked 45-package graphics environment. All 304 Python files were format clean; Ruff and strict Pyright reported zero findings; all 656 architecture assertions passed in 4.95 seconds; strict docs built in 1.17 seconds with only the known upstream notice. |
| Complete supported-Python candidate gate | 0 | The graphics-enabled candidate passed 2,196 tests with 14 expected skips on CPython 3.12.13 in 104.97 seconds, CPython 3.13.13 in 103.77 seconds, and CPython 3.14.5 in 111.55 seconds. |
| Real-wgpu, profiles, and vertical slices | 0 | The locked CPython 3.12.13 graphics environment was restored with 45 packages. All ten real-wgpu tests passed in 7.55 seconds. Five-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`, three draw calls, and 16 sprites. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, six query matches, five replay batches, and passing registered tests. |
| Documented benchmark gate | 0 | M1 validated seven workloads; fixed 3,600 ticks observed its target at 35.7460 ms p95, while 10,000-entity simulation retained its miss at 132.2362 ms p95. M2 validated four target-free informational workloads. M3 validated six workloads; 10,000-sprite extraction and 10,000-wgpu submission retained misses at 24.7991 ms and 3.0809 ms p95. M4 validated three workloads; baseline observed its target at 1.8727 ms p95, while stress 4/8 recorded 2.8540/4.5200 ms p95 without targets. These are local dirty-tree observations, not regression or support claims. |
| Pre-record reproducible distribution and release gate | 0 | Two fresh builds reproduced a pure 271,671-byte wheel at `f425169be9f6e0e0f53186979206dbad4528012ee4c62152b5cb97dec0a18149` and a 1,132,009-byte source distribution at `3c059b29d95a4a65a165d470ea76491b2313d956cdd6058fca3cc553475bc8d6`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed. Archive review found 94 wheel and 488 source entries, with no native/WASM wheel member or cache/build output. This row changes the source archive afterward, so later final and hosted artifact identities remain authoritative. |
| Expanded resolver proof points | 0 | Permission and symlink-loop-style `RuntimeError` failures both retain content-silent candidate/output-root codes, and a safe resolved alias demonstrably directs the first download to the resolved output root. All 11 M61 assertions passed in 0.93 seconds; both changed Python files remained format clean, Ruff clean, and strict-Pyright clean. |
| Evidence-inclusive static, architecture, and documentation gate | 0 | The unchanged lock resolved 46 packages in 0.85 ms; all 304 Python files were format clean; Ruff and strict Pyright reported zero findings; all 659 architecture assertions passed in 4.71 seconds; strict docs built in 1.14 seconds with only the known upstream notice. |
| Final supported-Python evidence | 0 | The record-inclusive graphics-enabled CPython 3.12.13 candidate passed 2,199 tests with 14 expected skips in 112.21 seconds. The final 11 M61 assertions passed on CPython 3.13.13 in 1.25 seconds and CPython 3.14.5 in 0.57 seconds after their earlier complete 2,196-test candidate passes. |
| Pre-review record-inclusive artifact and integrity gate | 0 | After restoring the locked 45-package CPython 3.12 environment, the unchanged lock resolved 46 packages in 0.77 ms; 304-file formatting, Ruff, strict Pyright, all 659 architecture assertions in 5.46 seconds, strict docs in 1.17 seconds, whitespace, reachable Git-object checking, and protected workflow/metadata/lock/runtime comparison passed. Two builds reproduced the pure 271,671-byte wheel (`f425169be9f6e0e0f53186979206dbad4528012ee4c62152b5cb97dec0a18149`) and 1,132,688-byte source distribution (`6d81141dca6ef2acbd47208391cd5316a8e3e6b95090f6e87188ad94b170d81c`); isolated-wheel and complete ten-artifact release smoke passed. Archive review found 94 wheel and 488 source entries with no native/WASM wheel member or cache/build output. This factual row changes the source archive afterward, so exact immutable final identities are captured with commit/PR evidence. |
| Final pre-host local gate | 0 | After the last factual-record correction, the unchanged lock resolved 46 packages in 0.78 ms; 304-file formatting, Ruff, strict Pyright, 659 architecture assertions in 4.91 seconds, all 11 M61 assertions in 0.37 seconds, strict docs in 1.19 seconds, whitespace, reachable Git-object checking, and protected-surface comparison passed. Two fresh builds reproduced the pure 271,669-byte wheel (`1dcd285720be404820da10f7473788ce50ffb28845d3200dd458eefb996744ff`) and 1,133,032-byte source distribution (`5a85ffd0f8221d677db8e975537a27ab39b00591f2ed4dc7abe30085e613555f`); isolated-wheel and complete ten-artifact release smoke passed. Archive review found 94 wheel and 488 source entries with no native/WASM/cache member. |
| Initial hosted PR #135 gate | 0 | Exact head `e17476380d979e2bec891db9fdf9a8523734e8b5` passed run `31494364000` in exactly three Linux-first allocations. Linux job `93788273122` passed in 7m09s before macOS `93790316767` and Windows `93790316678` began; they passed in 3m22s and 4m11s. The Linux baseline and every 3.13/3.14 compatibility suite passed 2,203 tests, with one expected skip outside the baseline. Every platform passed ten real-graphics tests, both profiles, Clockwork Arena, and Agent World Builder. Hosted distributions reproduced a 271,655-byte wheel (`d768b69d2269a811ae99f7248f082d7912f04d3ad5a62eaf5deccb788e4ebb13`) and 1,133,019-byte source distribution (`0ff8bbdc71f67e83d3484484945667b5c26cf19bae3ce95f96afed6b6f0669fa`); wheel and release smoke passed. |
| First thread-aware review audit | 0 | The exact hosted head/base and three successful checks were confirmed. One actionable P1 thread identified that `Path.resolve()` does not promise canonical spelling on a case-insensitive POSIX filesystem, so path equality alone could miss a differently cased filesystem alias. The first hosted gate is therefore superseded and is not final-head integration authority. |
| Test-first filesystem-identity correction | 1 | Against unchanged hosted production code, both new filesystem-identity assertions reached the intentionally forbidden download and the expanded documentation contract lacked the identity/case-insensitive boundary; three assertions failed and ten passed in 0.43 seconds. |
| Focused identity implementation | 0 | After comparing the resolved output root and every ancestor to the candidate with `Path.samefile()`, all 12 non-documentation M61 assertions passed with one documentation assertion deselected in 0.23 seconds. Identity-inspection failure maps content-silently to `public_release.temp_unavailable`. |
| Corrected focused M61 and documentation gate | 0 | After aligning RFC-0044 and public architecture/security/release documentation, all 13 M61 assertions passed in 0.23 seconds. Both changed Python files were already formatted, Ruff was clean, strict Pyright reported zero diagnostics, and strict docs built in 1.09 seconds with only the known upstream notice. |
| Correction-inclusive static and supported-Python gate | 0 | The unchanged lock resolved 46 packages in 0.72 ms; all 304 Python files were format clean; Ruff and strict Pyright reported zero findings; all 661 architecture assertions passed in 6.14 seconds; strict docs built in 1.31 seconds; whitespace, object, and protected-surface checks passed. The complete graphics-enabled candidate passed 2,201 tests with 14 expected skips on CPython 3.12.13 in 113.87 seconds, CPython 3.13.13 in 110.05 seconds, and CPython 3.14.5 in 114.92 seconds. |
| Corrected-head hosted PR #135 gate | 0 | Exact corrected head `75d985f40bec2c073952172e53075ddadc8bc214` passed run `31496532379` in exactly three Linux-first allocations. Linux `93795541158` passed in 7m18s before macOS `93797741480` and Windows `93797741693` began; they passed in 3m18s and 4m05s. The Linux baseline and every 3.13/3.14 compatibility suite passed 2,205 tests, with one expected skip outside the baseline. Every platform passed ten real-graphics tests, both profiles, Clockwork Arena, and Agent World Builder. Hosted distributions reproduced a 271,706-byte wheel (`88e5b70b34896ed136ee80e268adec8e60c439c9ad3e02d38493fc3933ce27ad`) and 1,135,916-byte source distribution (`db036d8e628c5ab061ae38bcf07f3635f06c98096b86fbe9b5444644f31ded5c`); wheel and release smoke passed. |
| Corrected-head review audits | 0 | Two delayed audits confirmed exact head/base, `MERGEABLE/CLEAN`, three successful checks, no conversation comment, and only the addressed/resolved P1 thread. No new actionable review item was present. |
| Head-pinned feature integration | 0 | PR #135 squash `7feded4ed2e37157b87a7f3bb733caf96805187e` has tree `3ae8059dc5a4f61a8a3b31d245b20f0373e0ffe4` exactly equal to the reviewed corrected head, sole parent exact M60 closeout `a8fc787a7b04b4fe8ed3766167e58258aa62c8d6`, valid GitHub signature, and parsed DCO trailer. The feature branch is deleted locally/remotely; no post-feature `main` run is claimed. |
| Integration-record PR #136 gate | 0 | Exact head `d80292ab4be734093bed52d0b0435da4d8b164e6` changed exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md`. Run `31497995187` passed in one 38-second Linux allocation: 304-file formatting, Ruff, strict docs in 1.42 seconds, 661 documentation-architecture assertions in 8.53 seconds, distribution build, installed-wheel smoke, release staging, and release smoke passed. Desktop umbrella `93800638843` skipped with zero steps. |
| Integration-record review and squash | 0 | Two delayed audits found exact head/base, `MERGEABLE/CLEAN`, one successful check plus the expected skipped umbrella, and no comment, review, or thread. Head-pinned GitHub-verified squash `9d1c4d4f967e97c7c77cf3b95d82c2d57367162e` has exact reviewed tree `8da574c0f2642369a725e6eb32d3983176e38dac`, sole parent feature squash `7feded4ed2e37157b87a7f3bb733caf96805187e`, and parsed DCO. The branch is deleted locally/remotely; no post-integration `main` run is claimed. |

No closeout hosted run or check is claimed.

## M60 local development and pre-record validation - 2026-08-11

M60 starts from exact synchronized M59 closeout
`9ba74e55b5c47d5f0bd030b53ad6a35a361c5735`. The worktree was clean, local
`main`, `origin/main`, and `origin/HEAD` matched, only `main` remained after
remote pruning, no pull request was open, and GitHub reported the closeout
squash signature valid with the exact reviewed tree and DCO trailer.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 1 | The first sandboxed attempt stopped before project execution because uv's existing user cache was inaccessible. |
| Approved `uv lock --check` rerun | 0 | Resolved the unchanged 46-package lock in 0.83 ms. |
| Baseline focused M45-M58/release-draft group | 0 | 317 tests passed with two platform-capability skips in 7.19 seconds. |
| Initial `pytest -q tests/architecture/test_m60_public_release_output_paths.py` | 1 | All eight tests failed as designed: six behavior cases reached forbidden side effects, the scope fixture had one stale release-workflow hash, and RFC-0043 was absent. |
| Corrected M60 behavior/scope group | 0 | Seven selected assertions passed in 0.21 seconds; focused format, Ruff, and strict Pyright were clean. |
| First complete M60 documentation group | 1 | Seven assertions passed; the documentation contract identified one missing exact `before validator` phrase. |
| Corrected initial M60 group | 0 | Eight assertions passed in 0.19 seconds. |
| Expanded M45-M60/release-draft group | 1 | 325 tests passed with two skips; M58's inherited documentation guard identified missing `M58` wording in `MAINTAINERS.md`. |
| Corrected expanded M45-M60/release-draft group | 0 | 326 tests passed with two skips in 7.12 seconds. |
| First complete architecture suite | 1 | 645 assertions passed; M46's literal old implementation check and M59's documentation-preservation check failed. |
| Second complete architecture suite | 1 | 646 assertions passed; the remaining M59 README phrase was identified. |
| Corrected complete architecture suite | 0 | 647 assertions passed in 4.41 seconds. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Checked 45 locked packages in 2 ms. |
| Whole-tree Ruff format/check and strict Pyright | 0 | 303 Python files were format-clean; Ruff had no finding; Pyright reported zero diagnostics. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict docs built in 1.09 seconds with only the recorded upstream MkDocs Material notice. |
| CPython 3.12.13 graphics-enabled complete suite | 0 | 2,187 tests passed with 14 expected skips in 101.84 seconds. |
| CPython 3.13.13 graphics-enabled complete suite | 0 | 2,187 tests passed with 14 expected skips in 99.87 seconds. |
| CPython 3.14.5 graphics-enabled complete suite | 0 | 2,187 tests passed with 14 expected skips in 106.60 seconds. |
| `uv run --python 3.12 --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Ten real-wgpu tests passed in 6.48 seconds. |
| Five-repeat M7 base profile and validator | 0 | The versioned profile validated two workloads. |
| Five-repeat M7 graphics profile and validator | 0 | The versioned real-wgpu profile validated three workloads. |
| Clockwork Arena wgpu 30-tick slice | 0 | Deterministic arena/capture summary completed with three draw calls. |
| Agent World Builder slice | 0 | Typed-tool loop completed with committed apply/adjust receipts, six query matches, passing embedded tests, and replay evidence. |
| M1 benchmark and validator | 0 | Seven workloads validated; fixed 3,600 ticks observed its target at 35.7375 ms p95, while the 10,000-entity simulation retained its miss at 117.7404 ms p95. |
| M2 benchmark and validator | 0 | Four informational target-free workloads validated. |
| M3 benchmark and validator | 0 | Six workloads validated; 10,000-wgpu submission observed its target at 2.8034 ms p95, while 10,000-sprite extraction retained its miss at 23.3646 ms p95. |
| M4 benchmark and validator | 0 | Three workloads validated; baseline observed its target at 1.8545 ms p95, and stress 4/8 p95 values were 2.9241/4.3010 ms without targets. |
| Two `uv build --out-dir .tmp/m60-dist-*` runs | 0 | Both built the pure wheel and source distribution. |
| Distribution reproducibility validator | 0 | The 271,507-byte wheel (`03115989...e83a6`) and 1,121,988-byte sdist (`ed6904e...8b2fc`) reproduced byte-for-byte. |
| Isolated-wheel smoke | 0 | The built wheel passed the complete installed smoke. |
| Release staging and smoke | 0 | Ten artifacts staged; checksum, manifest, SPDX SBOM, sample, safe extraction, and installed-release smoke passed. |
| Final expanded M60 group after two additional regressions | 0 | Ten assertions passed in 0.74 seconds; focused format/Ruff and whole-project strict Pyright remained clean. |

The record-inclusive local candidate passes `uv lock --check` (46 packages in
0.81 ms), whole-tree format/Ruff/Pyright, 648 architecture assertions in 5.20
seconds, strict docs in 1.16 seconds, and 2,188 CPython 3.12 graphics-enabled
tests with 14 expected skips in 101.93 seconds. The final ten M60 assertions
also pass on CPython 3.13.13 in 1.08 seconds and CPython 3.14.5 in 0.55 seconds.
Two record-inclusive builds reproduce; isolated-wheel and ten-artifact release
smoke pass. Archive review finds 94 pure-wheel entries, 486 source-distribution
entries, every M60 source/test/RFC/record, and no native or WASM wheel member.
Protected workflow/metadata/lock/runtime comparison, credential/backend pattern
review, `git fsck --no-dangling`, and `git diff --check` report no finding. The
exact immutable candidate artifact hashes are recorded with commit/PR evidence
rather than embedded into the source distribution that contains this file.

The first post-record Pyright rerun exited 1 with 17 missing/unknown optional-
graphics diagnostics because the preceding CPython 3.13/3.14 focused commands
had recreated `.venv` without the graphics extra. `uv sync --frozen
--all-groups --extra graphics` installed the six locked graphics packages, and
the immediate Pyright rerun exited 0 with zero diagnostics. No source change was
made for this environment correction.

| Command or review | Exit | Result |
| --- | ---: | --- |
| Feature commit, push, and ready PR | 0 | The exact reviewed 16-path tree was DCO-signed as `836c1e14bbfe0e9bb94dbe1fc84df600279e0b23`, pushed on neutral branch `security/m60-output-path-conformance`, and published as ready PR #132 against exact M59 closeout `9ba74e55b5c47d5f0bd030b53ad6a35a361c5735`. |
| Hosted exact-head feature gate | 0 | Run `31488972656` passed exact head `836c1e14bbfe0e9bb94dbe1fc84df600279e0b23` in exactly three Linux-first allocations. Linux job `93770741704` passed in 7m25s before macOS job `93772531511` and Windows job `93772531611` began; they passed in 2m28s and 3m17s. Linux baseline passed 2,192 tests; Ubuntu CPython 3.13/3.14 and both desktop CPython 3.14 suites passed 2,192 tests with one expected skip. Every platform passed ten real-graphics tests, a valid three-workload graphics profile, Clockwork Arena, and Agent World Builder. Linux also passed the valid two-workload base profile, strict static/docs gates, reproducible build, installed-wheel smoke, and complete release smoke. |
| Hosted reproducible artifacts | 0 | Same-source builds reproduced a pure 271,493-byte wheel at `ed79ae64bbda70b105fea3eaf61fedfa175998ea55191a7127d764063579f784` and a 1,125,477-byte source distribution at `462b6659990f222fe2c06c1deca5e124fdc897ec08d4d75cde3020f919ba2aab`. This is same-source/same-job equality, not independent rebuild or publication evidence. |
| Review and exact-tree squash audit | 0 | The initial and delayed audits found PR #132 ready, exact-head/exact-base, `MERGEABLE/CLEAN`, exactly three successful checks, zero issue comments, review comments, reviews, or threads. Head-pinned GitHub-verified squash `8967bd8cfc11f1b29caadbf01da9255bd6eb4584` has tree `e17d11565f30e58b6eb705926702e257026f9b3b` exactly equal to reviewed head `836c1e14bbfe0e9bb94dbe1fc84df600279e0b23` and sole parent M59 closeout `9ba74e55b5c47d5f0bd030b53ad6a35a361c5735`. The feature source commit carries the exact maintainer DCO trailer and remains attached to PR #132. The generated squash body retained literal escaped newline text before its displayed sign-off, so no parsed-trailer claim is made for that generated commit; this signed integration record preserves the factual attestation without rewriting public history. The feature branch was deleted locally/remotely. Synchronized `main` has no post-merge run or open PR. |
| Four-file integration-record local gate | 0 | Exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md` changed. The unchanged lock resolved 46 packages in 0.84 ms and checked the locked 45-package graphics environment. All 303 Python files were format clean; Ruff and strict Pyright reported zero findings; all 648 architecture assertions passed in 5.51 seconds; strict docs built in 1.17 seconds with only the known upstream notice. Two fresh builds reproduced the pure 271,507-byte wheel (`03115989c614f5627ece94d4d794364510f0b88e1dcb65a5ddec2489a23e83a6`) and 1,127,134-byte source distribution (`00c7197ad4560c0c27c09c51eecad6d8d21b1c7215052c5040c44c725641ac21`); isolated-wheel and complete ten-artifact release smoke passed. This factual row changes the packaged source archive afterward, so exact integration-head identities remain delegated to hosted evidence. |
| Final integration-record evidence-inclusive gate | 0 | The unchanged lock resolved 46 packages in 0.76 ms; all 303 Python files remained format clean; Ruff and strict Pyright reported zero findings; all 648 architecture assertions passed in 4.77 seconds; strict docs built in 1.09 seconds with only the known upstream notice. Whitespace, exact four-file scope, and full reachable Git-object checking passed. |
| Integration-record hosted gate | 0 | PR #133 exact head `f4a41d848a9e9bfa85da2c34d09e705ad7493c87` passed run `31490571527` in one 43-second Linux allocation. The trusted classifier reported four changed paths and `classification=documentation`; all 303 Python files were format clean, Ruff passed, strict docs built in 1.53 seconds, all 648 documentation architecture assertions passed in 8.51 seconds, reproducible build plus installed-wheel and complete release smoke passed. The exact-head 271,493-byte wheel was `ed79ae64bbda70b105fea3eaf61fedfa175998ea55191a7127d764063579f784`; the 1,127,269-byte source distribution was `02d7bc6c928068e4c562b3674cfd76fbec204ab0c31cc33933d1acf0254d2a6a`. Desktop umbrella job `93776026071` skipped with zero steps and no runner allocation. |
| Integration-record review, squash, and cleanup audit | 0 | Two delayed audits found exact head/base, `MERGEABLE/CLEAN`, one successful Linux check, one zero-step skipped umbrella, and no issue comment, review comment, review, or thread. Head-pinned GitHub-verified squash `6861198cf32d04f1e802525c2327335ca1c8be86` has tree `280d9e41e4f04d73f99dc5d324ede72f8fc7a472` exactly equal to reviewed record head `f4a41d848a9e9bfa85da2c34d09e705ad7493c87`, sole parent feature squash `8967bd8cfc11f1b29caadbf01da9255bd6eb4584`, a valid signature, and a parsed DCO trailer. No post-merge `main` run was allocated; both M60 working branches were deleted locally/remotely, and no open PR or non-main remote branch exists. |
| Three-file closeout prepublication audit | 0 | The unchanged lock resolved 46 packages in 0.90 ms; all 303 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 648 architecture assertions passed in 4.68 seconds; strict docs built in 1.11 seconds with only the known upstream notice. Exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md` changed; whitespace and full reachable Git-object checks passed. `main`, `origin/main`, and `origin/HEAD` resolve to verified integration squash `6861198cf32d04f1e802525c2327335ca1c8be86`; only `main` and the intended local closeout branch exist. No remote working branch, open PR, post-integration `main` run, tag, or release exists. The first GitHub branch-list query used an invalid jq selector and exited 1 without changing state; the corrected query returned only `main`. |

No tag, release, package publication, real public release observation,
race-free filesystem guarantee, or stability promotion is claimed.

## M59 development evidence - 2026-08-11, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| M58 closeout and repository baseline audit | 0 | Exact synchronized `main`, `origin/main`, and `origin/HEAD` resolved to GitHub-verified M58 closeout `d4487565d4fda57ec05437dfcadc687d2507dafa`. PR #128 had zero checks and merged with exact reviewed tree, sole parent M58 integration squash, valid signature, and standalone DCO; neither its branch nor squash allocated a run. Only `main` existed locally/remotely and no open PR remained. |
| Current tracked-tree identity scan | Finding | The explicit maintenance-marker scan found 107 matching lines across `.project/TEST_EVIDENCE.md` (78), `.project/PROJECT_STATE.md` (25), three duplicated architecture guards, and one persistent-command actor fixture. No other tracked file matched. This establishes the bounded current-tree cleanup set without making an immutable-history erasure claim. |
| M59 tests-first tracked-tree guard | Expected failure | The new centralized architecture file failed one tracked-text assertion and passed one absent-root control in 0.28 seconds against the unchanged repository. Its failure identified exactly the two project-record files and four tests from the baseline scan. |
| First implementation-focused gate | Corrected | After descriptive record redaction, a neutral actor fixture, and consolidation of the three duplicate loops, all 56 selected inherited and M59 assertions passed in 0.70 seconds and focused strict Pyright reported zero diagnostics. The new guard itself required one formatter rewrite and one import-order correction; no format/lint pass is claimed from that initial check, and both mechanical findings were corrected. A direct current-tree scan returned no match. |
| M59 documentation-contract tests-first gate | Expected failure | Both current-tree hygiene assertions passed. The third assertion failed because the README, maintainer boundary, changelog, roadmap, accepted RFC-0042, RFC index, and MkDocs navigation had not yet recorded M59. No documentation-integrated pass is claimed from this run. |
| First documentation-integrated gate | Corrected | Ruff formatting required one rewrite in the new architecture test while Ruff and strict Pyright were otherwise clean. All 56 selected implementation assertions passed, but the documentation assertion found that the required README phrase was split across lines; strict docs still built in 1.12 seconds with only the known upstream notice. No format or focused-suite pass is claimed from this combined attempt. |
| Corrected focused implementation and documentation gate | 0 | After making the README contract phrase contiguous, all 57 selected inherited and M59 assertions passed in 0.52 seconds. The new guard remained format clean, Ruff clean, and strict-Pyright clean. |
| Whole-tree static, architecture, and documentation gate | 0 | The unchanged lock resolved 46 packages in 0.92 ms and synchronized the locked 45-package graphics environment. All 302 Python files were format clean; Ruff and strict Pyright reported zero findings; all 636 architecture assertions passed in 5.48 seconds; strict docs built in 1.12 seconds with only the known upstream notice. |
| Complete supported-Python candidate gate | 0 | The graphics-enabled candidate passed 2,176 tests with 14 expected skips on CPython 3.12.13 in 110.33 seconds, CPython 3.13.13 in 107.47 seconds, and CPython 3.14.5 in 113.21 seconds. |
| Real-wgpu, profiles, and vertical slices | 0 | The locked CPython 3.12.13 graphics environment was restored with 45 packages. All ten real-wgpu tests passed in 7.31 seconds. Five-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`, three draw calls, and 16 sprites. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d505438522850586a0eef226927b4833234e52612e413bf5e5de8c57df34b2ef`, six query matches, five replay batches, and registered tests passing. The initial restricted-cache profile invocation was blocked before producing output; only the approved fresh rerun is represented as passing. |
| Documented benchmark gate | 0 | M1 validated seven workloads with one of two recorded targets observed; M2 validated four target-free informational workloads; M3 validated six workloads with zero of two observed targets met and no target claim; M4 validated three workloads with its baseline target observed. These are local dirty-tree observations, not regression or support claims. |
| Pre-record reproducible distribution and release gate | 0 | Two confirmed-absent output directories reproduced a pure 271,295-byte wheel at SHA-256 `cdaead3b189dbbd17e9b84287dfd0316ada659bf25d888b6b1a78b8240448bb8` and a 1,112,752-byte source distribution at `79747c1f813a195dd8758ef64f8836d77e83479a661a4caded95b836fdf83c2b`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed. This factual row changes the source archive afterward, so replacement final and hosted artifact identities remain authoritative. |
| Pre-record archive and scope review | Corrected | The wheel contained 94 entries and the source distribution 484 file entries, with no native library, WASM, bytecode, cache, or encoded retired marker. Protected workflow, project-metadata, lock, runtime, benchmark, and script surfaces had no diff. Review then found two uppercase legacy instruction-name remnants in current project records that the first case-insensitive marker set did not reject. Both were descriptively redacted, the exact-case guard was added, and three focused assertions passed in 0.26 seconds with formatting, Ruff, and strict Pyright clean. No clean final-review claim is made from the pre-correction scan. |
| Final focused guard hardening | 0 | The encoded set now covers direct automation-attribution wording. The scanner checks path names and symlink targets without following links outside the repository; no tracked symlink currently exists. The matcher explicitly preserves product-facing engine-agent terminology. All four M59 assertions passed in 0.27 seconds with formatting, Ruff, and strict Pyright clean. A direct retired-marker scan returned no match; a deliberately broader search returned only legitimate engine-agent terminology. |
| First record-inclusive static attempt | Blocked | The uv lock command failed before project validation because the managed environment denied access to uv's existing user cache. No lock, sync, formatting, lint, or type-check pass is claimed from that sequence. The concurrently independent architecture and documentation commands did complete successfully. |
| Record-inclusive static, architecture, and documentation gate | 0 | With approved existing-cache access, the unchanged lock resolved 46 packages in 0.89 ms and checked the locked 45-package graphics environment. All 302 Python files were format clean; Ruff and strict Pyright reported zero findings. Independently, all 637 architecture assertions passed in 4.96 seconds and strict docs built in 1.11 seconds with only the known upstream notice. |
| Record-inclusive reproducible distribution and release gate | 0 | Two fresh confirmed-absent output directories reproduced a pure 271,295-byte wheel at SHA-256 `cdaead3b189dbbd17e9b84287dfd0316ada659bf25d888b6b1a78b8240448bb8` and a 1,114,038-byte source distribution at `e1e8ed474723ee7b5d0d79d225b9e18a4627697869ab98de7f703716f6b1422c`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed. The first archive-helper invocation was found to still target the pre-record directory, so no final-artifact audit claim is made from it; after correcting the ignored helper argument, the exact final wheel's 94 entries and source archive's 484 file entries had no native library, WASM, bytecode, cache, or encoded retired-marker hit. This row changes the source archive afterward, so hosted exact-head artifact identity remains authoritative. |
| Final evidence-inclusive local gate and findings-first review | 0 | The unchanged lock resolved 46 packages in 0.76 ms; all 302 Python files were format clean; Ruff and strict Pyright reported zero findings. The first parallel architecture/docs invocation was blocked before either command ran by restricted existing-cache access; the approved identical rerun passed all 637 architecture assertions in 4.48 seconds and built strict docs in 1.03 seconds with only the known upstream notice. Whitespace and length-bounded credential scans passed. No tracked symlink exists. Protected workflow, project-metadata, lock, runtime, benchmark, and script surfaces have no diff. Full Git-object checking passed with only expected unreachable development objects; history remains linear from exact M58 closeout, and only `main` plus the intended neutral feature branch exist. Review of every changed and added file found no actionable issue or backend/native leakage. |
| Initial hosted exact-head feature gate | Corrected | PR #129 exact head `3d7329311d326692dd725024d312b73bb420ef16` passed run `31482750494` in exactly three Linux-first allocations. Linux job `93751196748` passed in 7m27s before macOS `93752915784` and Windows `93752915830` began; they passed in 2m21s and 4m20s. Linux baseline passed 2,181 tests; Ubuntu CPython 3.13/3.14 and both desktop CPython 3.14 suites passed 2,181 tests with one expected skip. Every platform passed ten real-graphics tests, profile smoke, Clockwork Arena, and Agent World Builder. Hosted reproducibility produced a pure 271,281-byte wheel (`90d0e8daed42c217ae3fd5795feea821744c2e154f361112dbb5c6135998e28a`) and 1,114,755-byte source distribution (`1801d4c777f60c77366cabbb52eca38ca141253014387b5b3ffd4b10671ea124`); installed-wheel and complete release smoke passed. Review then found a valid dangling-symlink gap, so this initial head is not represented as merge-ready. |
| Dangling-root review regression | Expected failure | The reviewer-derived platform-independent regression simulated `exists() == False` with `is_symlink() == True` for a retired root entry and failed because no lexical root-path violation helper existed. This reproduces the P2 without requiring Windows symlink privileges. |
| First focused review-correction attempt | Blocked | The managed environment denied uv's existing user cache before formatting began. No formatter, lint, type, or test pass is claimed from that sequence. |
| Second focused review-correction attempt | Corrected | The correction was format clean and Ruff clean, but strict Pyright rejected five unknown-type diagnostics from untyped monkeypatch lambdas. No type-check or test pass is claimed from that stopped sequence; typed local functions replaced the lambdas. |
| Corrected focused review gate | 0 | The lexical root helper treats `path.exists() or path.is_symlink()` as a violation, so dangling retired root links fail closed even when ignored by Git. The focused file was format clean, Ruff clean, and strict-Pyright clean; all five assertions passed in 0.28 seconds. Corrected whole-tree and hosted exact-head validation remain pending. |
| Corrected whole-tree local gate | 0 | The unchanged lock resolved 46 packages in 0.93 ms; all 302 Python files were format clean; Ruff and strict Pyright reported zero findings; all 638 architecture assertions passed in 4.42 seconds; strict docs built in 1.02 seconds with only the known upstream notice; whitespace was clean. Corrected hosted exact-head validation remains pending. |
| Corrected hosted exact-head feature gate | 0 | PR #129 corrected head `28e80e66eb16656a998353627ef78a8fe6e4c80b` passed run `31484028669` in exactly three Linux-first allocations. Linux job `93755205753` passed in 6m05s before macOS `93756589084` and Windows `93756589057` began; they passed in 2m53s and 4m08s. Linux baseline passed 2,182 tests; Ubuntu CPython 3.13/3.14 and both desktop CPython 3.14 suites passed 2,182 tests with one expected skip. Every platform passed ten real-graphics tests, profile smoke, Clockwork Arena, and Agent World Builder. Hosted reproducibility produced a pure 271,281-byte wheel (`90d0e8daed42c217ae3fd5795feea821744c2e154f361112dbb5c6135998e28a`) and 1,116,015-byte source distribution (`5650d9a3df594799e09969f305419829b4345d6e85b8682b130b78fe926be987`); installed-wheel and complete release smoke passed. |
| Corrected review, exact-tree squash, and cleanup audit | 0 | The valid P2 was answered with exact correction evidence and its sole thread resolved. Two delayed audits found PR #129 ready, exact-head/exact-base, `MERGEABLE/CLEAN`, exactly three successful checks, zero issue comments, and no unresolved or later review activity. Head-pinned GitHub-verified squash `f12f65ab7c1f8426b0232bb4b414e48276bbad56` has tree `759107195ba7094fb78cbc25b62a5d6011dd637d` exactly equal to corrected head `28e80e66eb16656a998353627ef78a8fe6e4c80b`, sole parent M58 closeout `d4487565d4fda57ec05437dfcadc687d2507dafa`, and standalone DCO. The merged feature branch was deleted locally/remotely. Synchronized `main` has no post-merge run, open PR, or non-main remote branch. |
| Four-file integration-record local gate | 0 | Exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md` changed. The unchanged lock resolved 46 packages in 0.81 ms and checked the locked 45-package graphics environment. All 302 Python files were format clean; Ruff and strict Pyright reported zero findings; all 638 architecture assertions passed in 4.41 seconds; strict docs built in 1.02 seconds with only the known upstream notice; whitespace was clean. Two fresh confirmed-absent builds reproduced the pure 271,295-byte wheel (`cdaead3b189dbbd17e9b84287dfd0316ada659bf25d888b6b1a78b8240448bb8`) and 1,117,300-byte source distribution (`c51004adaba3c868e7a847b3f4cc910552213bd8cba52dbf4dbd9543b4839423`); isolated-wheel and complete ten-artifact release smoke passed. This factual row changes the packaged source archive afterward, so exact integration-head identities remain delegated to hosted evidence. |
| Final integration-record evidence-inclusive gate | 0 | The unchanged lock resolved 46 packages in 0.69 ms; all 302 Python files remained format clean; Ruff and strict Pyright reported zero findings; all 638 architecture assertions passed in 4.39 seconds; strict docs built in 1.00 seconds with only the known upstream notice. Whitespace, exact four-file scope, and full Git-object checking passed, with only expected unreachable development objects reported. |
| Integration-record hosted gate | 0 | PR #130 exact head `f142ceae1381c5c8c6cb15001229cfd4679ff028` passed run `31485465637` in one 42-second Linux allocation. All 302 Python files were format clean, Ruff passed, strict docs built in 1.50 seconds, all 638 documentation architecture assertions passed in 8.40 seconds, reproducible build plus installed-wheel and complete release smoke passed. The exact-head 271,281-byte wheel was `90d0e8daed42c217ae3fd5795feea821744c2e154f361112dbb5c6135998e28a`; the 1,117,495-byte source distribution was `b8c4a21345ff809e7bb078ded52daae5993f863e6f54379345cc0683a92f86be`. Desktop umbrella job `93759917789` skipped with zero steps and no runner allocation. |
| Integration-record review, squash, and cleanup audit | 0 | Two delayed audits found exact head/base, `MERGEABLE/CLEAN`, one successful Linux check, one zero-step skipped umbrella, and no issue comment, review comment, review, or thread. Head-pinned GitHub-verified squash `f6b734878738ca6408afeabb793c5cd591c0d607` has tree `da5e3b4404a9385990685467d920806b290de282` exactly equal to reviewed record head `f142ceae1381c5c8c6cb15001229cfd4679ff028`, sole parent feature squash `f12f65ab7c1f8426b0232bb4b414e48276bbad56`, a valid signature, and standalone DCO. No post-merge `main` run was allocated; both M59 working branches were deleted locally/remotely, and no non-main remote branch exists. |
| Three-file closeout prepublication audit | 0 | The unchanged lock resolved 46 packages in 0.75 ms; all 302 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 638 architecture assertions passed in 4.44 seconds; strict docs built in 1.05 seconds with only the known upstream notice. Exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md` changed; protected workflows, metadata, lock, runtime, tests, benchmarks, scripts, public docs, and roadmap are unchanged. Whitespace and full Git-object checking passed with only expected unreachable development objects reported. `main`, `origin/main`, and `origin/HEAD` resolve to verified integration squash `f6b734878738ca6408afeabb793c5cd591c0d607`; only `main` and the intended local closeout branch exist. No remote working branch, open pull request, post-integration `main` run, tag, or GitHub release exists. |

Closeout publication must allocate zero hosted runs or checks; publication
evidence follows only after those operations actually execute.

## M58 development evidence - 2026-08-10 through 2026-08-11, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| M57 closeout audit | 0 | Exact synchronized `main`, `origin/main`, and `origin/HEAD` resolved to verified M57 closeout `26826822547d6d8df6ce1bfc05d8cf728a32d505`. Only `main` existed locally/remotely; no open pull request, tag, release, closeout run/check, or post-closeout `main` run existed; full Git-object checking passed. |
| Focused inherited M47-M57 baseline | 0 | All 243 public-release assertions passed in 2.49 seconds on the exact clean M57 closeout. |
| Official Python 3.14 close-contract review | 0 | Python documents `HTTPConnection.close()` as closing the connection to the server, `HTTPResponse` as a buffered readable object, and the common I/O close/context contract as idempotent cleanup that also runs when an operation raises. RFC-0041 adopts only the public close methods and makes no broader operating-system or transport resource-leak proof. |
| M58 tests-first behavior and boundary probe | Expected failure | The new test file was format clean. Ruff found six constant-attribute access findings and strict Pyright found seven fake-constructor/access typing findings, all confined to the test harness. Against unchanged production code, all nine executed behavior and boundary assertions failed in 0.46 seconds: partial publication preceded cleanup; cleanup failures escaped raw or masked an active failure; response close failure skipped connection close; redirect continued without proven cleanup; and source ordering was wrong. The documentation assertion was intentionally deselected. |
| Implemented focused M58 behavior gate | 0 | Both changed Python files were format clean; Ruff passed; strict Pyright reported zero findings; all nine M58 behavior and frozen-boundary assertions passed in 0.28 seconds, with the documentation assertion intentionally deselected. |
| First documentation-integrated M58 gate | Corrected | Ruff and strict Pyright remained clean; strict docs built in 1.08 seconds with only the known upstream notice; whitespace was clean. Nine of ten focused assertions passed, while the documentation guard found that the contract expressed publication-after-cleanup without the required literal phrase `before partial publication`. No complete focused pass is claimed from this run; RFC-0041 now states the ordering directly. |
| First wording-correction probe | Corrected | Strict docs again built in 1.08 seconds and whitespace remained clean, but nine of ten focused assertions passed because Markdown line wrapping split the required phrase across lines. No complete focused pass is claimed; RFC-0041 now keeps `before partial publication` on one line. |
| Corrected focused implementation and documentation gate | 0 | All ten M58 behavior, boundary, and documentation assertions passed in 0.24 seconds. Focused Ruff and strict Pyright remained clean; all 253 inherited M47-M58 assertions passed together in 2.50 seconds; strict docs built in 1.09 seconds with only the known upstream notice; whitespace was clean. |
| Whole-tree static, architecture, and documentation gate | 0 | The unchanged lock resolved 46 packages and the locked CPython 3.12 graphics environment checked 45 packages. All 301 Python files were format clean; Ruff and strict Pyright reported zero findings; all 631 architecture assertions passed in 5.16 seconds; strict docs built in 1.14 seconds with only the known upstream notice; whitespace was clean. The first sandboxed lock check could not access uv's external cache and was rerun successfully with the required cache permission. |
| First CPython 3.13 invocation | Corrected | A default-extra invocation completed with 2,161 passes and 15 skips in 97.86 seconds, revealing that switching interpreters had recreated the environment without the required graphics extra. It is not acceptance evidence; the complete graphics-enabled invocation follows. |
| Complete supported-Python candidate gate | 0 | The graphics-enabled candidate passed 2,171 tests with 14 expected skips on CPython 3.12.13 in 104.90 seconds, CPython 3.13.13 in 102.33 seconds, and CPython 3.14.5 in 108.78 seconds. The suites ran serially because the repository shares one temporary test root. |
| Real-wgpu, profiles, and vertical slices | 0 | After restoring the locked 45-package CPython 3.12.13 graphics environment, all ten real-wgpu tests passed in 6.74 seconds. Five-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`, three draws, and 16 sprites. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, committed receipts, six query matches, five replay batches, and passing tests. |
| Documented M1-M4 benchmark gate | 0 | All four fresh artifact contracts validated on dirty Windows CPython 3.12.13. M1 accepted seven workloads with one of two historical targets observed; M2 accepted four informational workloads with no timing targets; M3 accepted six workloads with zero of two historical targets met; M4 accepted three workloads with its baseline target observed. These local observations are diagnostic, not regression, release, support, or native-admission claims. |
| Pre-review reproducible distribution and release gate | 0 | Two confirmed-absent builds reproduced a pure 271,289-byte wheel at SHA-256 `89b5ad458d9b78c101e72fbb618c4dc5d93451df0833cc0802b7b53856e88e79` and a 1,106,398-byte source distribution at `8c1b82b04c2bbb70968666ce986ea53064ab22d4c0d9ccf8e0bf4c8c5819c610`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed for `0.1.0a1`. Findings-first review changed the candidate afterward, so these are not final exact-tree artifacts. |
| Hostile cleanup-exception truthiness probe | Expected failure | Findings-first review added an exception subclass whose `__bool__` raises a private assertion. Against the then-current `close_error or error` selection, the regression failed in 0.80 seconds after both close attempts because selecting the first failure invoked attacker-defined truthiness. No correction pass is claimed from this probe. |
| Corrected first-cleanup-error focused gate | 0 | Explicit identity selection avoids exception truthiness. Both changed Python files were format clean; Ruff and strict Pyright reported zero findings; all 11 M58 behavior, boundary, documentation, and reviewer-derived assertions passed in 0.26 seconds. |
| Corrected whole-tree static, architecture, and documentation gate | 0 | All 301 Python files remained format clean; Ruff and strict Pyright reported zero findings; all 254 inherited M47-M58 assertions passed in 2.55 seconds; all 632 architecture assertions passed in 5.14 seconds; strict docs built in 1.14 seconds with only the known upstream notice; whitespace was clean. |
| Corrected complete supported-Python candidate gate | 0 | The graphics-enabled corrected candidate passed 2,172 tests with 14 expected skips on CPython 3.12.13 in 104.70 seconds, CPython 3.13.13 in 103.10 seconds, and CPython 3.14.5 in 108.59 seconds. The suites ran serially because the repository shares one temporary test root. |
| Corrected real-wgpu, profiles, and vertical slices | 0 | After restoring the locked 45-package CPython 3.12.13 graphics environment, all ten real-wgpu tests passed in 6.64 seconds. Five-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`, three draws, and 16 sprites. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, committed receipts, six query matches, five replay batches, and passing tests. |
| Corrected documented M1-M4 benchmark gate | 0 | All four fresh corrected-candidate artifact contracts validated on dirty Windows CPython 3.12.13. M1 accepted seven workloads with one of two historical targets observed; M2 accepted four informational workloads with no timing targets; M3 accepted six workloads with zero of two historical targets met; M4 accepted three workloads with its baseline target observed. These local observations remain diagnostic only. |
| Caller exception-context probe | Expected failure | A second findings-first regression invoked a cleanup-only failure while the caller was handling an unrelated exception. Against ambient `sys.exception()` detection, the download wrongly suppressed cleanup failure and did not raise; the regression failed in 0.78 seconds. No correction pass is claimed from this probe. |
| Corrected local-primary-failure focused gate | 0 | `_download` now tracks only failures originating within its own exchange and preserves all ordinary and control-flow failures through an explicit `BaseException` re-raise path. Both changed Python files were format clean; Ruff and strict Pyright reported zero findings; all 12 focused M58 assertions passed in 0.27 seconds. |
| Final whole-tree static, architecture, and documentation gate | 0 | The unchanged lock resolved 46 packages in 0.80 ms. All 301 Python files were format clean; Ruff and strict Pyright reported zero findings; all 255 inherited M47-M58 assertions passed in 2.56 seconds; all 633 architecture assertions passed in 5.16 seconds; strict docs built in 1.12 seconds with only the known upstream notice; whitespace was clean. |
| Final complete supported-Python candidate gate | 0 | The final graphics-enabled candidate passed 2,173 tests with 14 expected skips on CPython 3.12.13 in 105.26 seconds, CPython 3.13.13 in 111.56 seconds, and CPython 3.14.5 in 109.24 seconds. The suites ran serially because the repository shares one temporary test root. |
| Final real-wgpu, profiles, and vertical slices | 0 | After restoring the locked 45-package CPython 3.12.13 graphics environment, all ten real-wgpu tests passed in 6.96 seconds. Five-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`, three draws, and 16 sprites. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, committed receipts, six query matches, five replay batches, and passing tests. |
| Final documented M1-M4 benchmark gate | 0 | All four fresh final-candidate artifact contracts validated on dirty Windows CPython 3.12.13. M1 accepted seven workloads with one of two historical targets observed; M2 accepted four informational workloads with no timing targets; M3 accepted six workloads with zero of two historical targets met; M4 accepted three workloads with its baseline target observed. These local observations remain diagnostic only. |
| Final-record reproducible distribution and release gate | 0 | Two confirmed-absent builds reproduced a pure 271,289-byte wheel at SHA-256 `89b5ad458d9b78c101e72fbb618c4dc5d93451df0833cc0802b7b53856e88e79` and a 1,107,819-byte source distribution at `08dbcc67fe7638f0b49ec558eb22c334d732700c94deee5bc8c1958338dd65f1`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed for `0.1.0a1`. This factual row changes the source archive afterward, so hosted exact-head distribution identity remains authoritative. |
| Findings-first scope, archive, credential, identity, history, and integrity review | 0 | No actionable M58 issue remains after explicit first-error identity selection and exchange-local primary-failure tracking. The candidate changes no workflow, project metadata, lock, runtime package, benchmark, or release authority. The 94-entry wheel and 482-entry source distribution contain no retired control path, native library, WASM, bytecode, or cache payload. Added-line credential/private-key scans returned no match; root retired control paths remain absent. A full-tree identity-hygiene scan found only one pre-existing actor fixture and three pre-existing retired-path guards; M58 adds none, and a later isolated hygiene slice may remove literal legacy naming without widening this security change. History remains linear from exact M57 closeout; only `main` and the intended neutral feature branch exist; whitespace is clean; full Git-object checking passes with only expected unreachable historical objects. |
| Final record-inclusive local gate | 0 | The unchanged lock resolved 46 packages in 0.93 ms. All 301 Python files remained format clean; Ruff and strict Pyright reported zero findings; all 633 architecture assertions passed in 6.35 seconds; strict docs built in 1.45 seconds with only the known upstream notice. Whitespace and full Git-object checking passed, with only expected unreachable historical objects reported. |
| Hosted exact-head feature gate | 0 | PR #126 exact head `8bd11f0ab6575edee6a5e7b5c78e36af59e55088` passed run `31478254138` in exactly three Linux-first allocations. Linux job `93736984444` passed in 7m48s before macOS `93738860983` and Windows `93738860996` began; they passed in 2m00s and 4m01s. Linux baseline passed 2,177 tests; Ubuntu CPython 3.13/3.14 and both desktop CPython 3.14 suites passed 2,177 tests with one expected skip. Every platform passed ten real-graphics tests, profile smoke, Clockwork Arena, and Agent World Builder. Hosted reproducibility produced a pure 271,274-byte wheel (`04147c9b56fa5caf3c012172c043e4f0d1580257a0be513e8a274d0fe60d0f98`) and 1,108,291-byte sdist (`30f98c24226d4cc588f122d0623d13a6e575e5abc8396c2a428cf22509134500`); installed-wheel and complete release smoke passed. |
| Hosted review and exact-tree squash audit | 0 | Two delayed audits found zero issue comments, review comments, reviews, or threads. PR #126 was ready, `MERGEABLE/CLEAN`, exact-head/exact-base, and had exactly three successful checks. Head-pinned squash `17ea7354c80b9d140350b88cd0ae3e615f700e45` has tree `feea8788e3a1c0e34505be6e752aa7d0e721b693` exactly equal to reviewed head `8bd11f0ab6575edee6a5e7b5c78e36af59e55088`, sole parent M57 closeout `26826822547d6d8df6ce1bfc05d8cf728a32d505`, a valid GitHub signature, and standalone DCO. The merged feature branch was deleted locally/remotely. Synchronized `main` has no post-merge run or non-main remote branch. |
| Four-file integration-record local gate | 0 | The unchanged lock resolved 46 packages in 0.84 ms and checked the locked 45-package graphics environment. All 301 Python files were format clean; Ruff and strict Pyright reported zero findings; all 633 architecture assertions passed in 5.97 seconds; strict docs built in 1.20 seconds with only the known upstream notice. Whitespace and exact four-file scope checks passed. Two fresh confirmed-absent builds reproduced the pure 271,289-byte wheel (`89b5ad458d9b78c101e72fbb618c4dc5d93451df0833cc0802b7b53856e88e79`) and 1,109,609-byte sdist (`a0953800933cf64fcdaba720f0303c9ad06e6755e8b07a4467ae3a163f3289c8`); isolated-wheel and complete ten-artifact release smoke passed. This factual row changes the packaged source archive afterward, so exact integration-head identities remain delegated to hosted evidence. |
| Final integration-record evidence-inclusive gate | 0 | The unchanged lock resolved 46 packages in 0.84 ms; all 301 Python files remained format clean; Ruff and strict Pyright reported zero findings; all 633 architecture assertions passed in 5.80 seconds; strict docs built in 1.19 seconds with only the known upstream notice. Whitespace, exact four-file scope, and full Git-object checking passed, with only expected unreachable historical objects reported. |
| Integration-record hosted gate | 0 | PR #127 exact head `4a72ae994714a4c2040547c568c5d625ee4a7ab9` passed run `31479930394` in one 40-second Linux allocation. All 301 Python files were format clean, Ruff passed, strict docs built in 1.41 seconds, all 633 documentation architecture assertions passed in 8.13 seconds, reproducible build plus installed-wheel and complete release smoke passed. The exact-head 271,274-byte wheel was `04147c9b56fa5caf3c012172c043e4f0d1580257a0be513e8a274d0fe60d0f98`; the 1,109,741-byte sdist was `bbe2929eefcc98486065667902b36c8100b93cdf2c623d66d9e8888c20348257`. Desktop umbrella job `93742463489` skipped with zero steps and no runner allocation. |
| Integration-record review, squash, and cleanup audit | 0 | Two delayed audits found exact head/base, `MERGEABLE/CLEAN`, one successful Linux check, one zero-step skipped umbrella, and no issue comment, review comment, review, or thread. Head-pinned GitHub-verified squash `26ec103a2ff3da55c4f2c4a8dca506f92ca3195e` has tree `ebff30df07c5797d3f85956ea9bb3a95ba833e66` exactly equal to reviewed record head `4a72ae994714a4c2040547c568c5d625ee4a7ab9`, sole parent feature squash `17ea7354c80b9d140350b88cd0ae3e615f700e45`, a valid signature, and standalone DCO. No post-merge `main` run was allocated; both M58 working branches were deleted locally/remotely, and no non-main remote branch exists. |
| Three-file closeout prepublication audit | 0 | The unchanged lock resolved 46 packages in 0.78 ms; all 301 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 633 architecture assertions passed in 5.77 seconds; strict docs built in 1.17 seconds with only the known upstream notice. Exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md` changed; protected workflows, metadata, lock, runtime, tests, benchmarks, scripts, public docs, and roadmap are unchanged. Whitespace and full Git-object checking passed with only expected unreachable historical objects reported. `main`, `origin/main`, and `origin/HEAD` resolve to verified integration squash `26ec103a2ff3da55c4f2c4a8dca506f92ca3195e`; only `main` and the intended local closeout branch exist. No remote working branch, open pull request, post-integration `main` run, tag, or GitHub release exists. |

Closeout publication must allocate zero hosted runs or checks; publication
evidence follows only after those operations actually execute.

## M57 development evidence - 2026-08-10, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| M56 closeout audit | 0 | Exact synchronized `main`, `origin/main`, and `origin/HEAD` resolved to GitHub-verified M56 closeout `187cbfb1c857e62594e49d1cf8e7591024aff8c9`. Only `main` existed locally/remotely; no open pull request, tag, release, closeout run/check, or post-closeout `main` run existed; full Git-object checking passed. |
| Focused inherited M47-M56 baseline | 0 | All 226 public-release assertions passed in 2.29 seconds on the exact clean M56 closeout. |
| Official Python 3.14 and RFC 9112 review | 0 | Python 3.14.7 documents `HTTPResponse` as a binary buffered reader and `read(amount)` as returning the response body up to that many bytes; binary I/O produces bytes. RFC 9112 defines a message body as octets, a valid `Content-Length` as the exact expected body length, and a shorter declared body as incomplete. RFC-0040 adopts only those documented public surfaces and explicitly does not claim general completeness for unframed close-delimited bodies. |
| First M57 tests-first attempt | Corrected | Formatting and Ruff passed. The unchanged verifier produced 13 failures and one pass, exposing the intended raw type/access exceptions plus accepted malformed blocks and declared-length disagreement. The helper also reloaded the verifier after capturing its exception class, invalidating one wrapped-exception assertion. No clean tests-first count is claimed from this attempt; the helper now receives the already loaded download function. |
| Corrected M57 tests-first behavior probe | Expected failure | Against the still-unchanged verifier, 12 assertions failed and two controls passed in 0.45 seconds. Failures demonstrated raw text/boolean/access exceptions, accepted mutable buffers, memory views, absent values, blocks larger than the requested amount, short/long declared bodies, and missing declared-length enforcement after a redirect. No implementation pass is claimed from this probe. |
| Implemented focused M57 behavior gate | 0 | Both Python files were format clean; Ruff and strict Pyright reported zero findings; all 14 response-block, declared-length, stable-error, valid-short-read, and redirect behavior assertions passed in 0.31 seconds. |
| Inherited M47-M57 behavior gate | 0 | All 240 public-release behavior assertions passed together in 2.33 seconds before the documentation and boundary guards were added. |
| First documentation-integrated focused gate | Corrected | Both Python files were format clean; Ruff and strict Pyright reported zero findings. Of 242 focused assertions, 241 passed and the documentation guard found that contracts said variants of “adds no ... alternate client” rather than the explicit required phrase `no alternate client`. No complete focused or docs pass is claimed from this fail-fast sequence. The README now states that phrase directly without changing scope. |
| Corrected focused implementation and documentation gate | 0 | Both Python files were format clean; Ruff and strict Pyright reported zero findings; all 242 M47-M57 implementation, compatibility, boundary, and documentation assertions passed in 2.37 seconds; strict docs built in 1.01 seconds with only the known upstream notice; whitespace was clean. |
| Complete whole-tree static, architecture, and documentation gate | 0 | The unchanged lock resolved 46 packages and checked the locked 45-package graphics environment. All 300 Python files were format clean; Ruff and strict Pyright reported zero findings; all 620 architecture assertions passed in 4.18 seconds; strict docs built in 1.06 seconds with only the known upstream notice; whitespace was clean. |
| Complete supported-Python candidate gate | 0 | The graphics-enabled candidate passed 2,160 tests with 14 expected skips on CPython 3.12.13 in 104.69 seconds, CPython 3.13.13 in 104.61 seconds, and CPython 3.14.5 in 108.86 seconds. The suites ran serially because the repository shares one temporary test root. |
| Real-wgpu, profiles, and vertical slices | 0 | After restoring the locked 45-package CPython 3.12.13 graphics environment, all ten real-wgpu tests passed in 6.87 seconds. Three-repeat two-workload base and three-workload graphics profiles validated. An initial 30-draw Clockwork Arena run passed; the established three-draw shape then reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, committed receipts, six query matches, five replay batches, and passing tests. |
| Documented M1-M4 benchmark gate | 0 | All four fresh artifact contracts validated on dirty Windows CPython 3.12.13. M1 accepted seven workloads with one of two historical targets observed; M2 accepted four informational workloads with no timing targets; M3 accepted six workloads with zero of two historical targets met; M4 accepted three workloads with its baseline target observed. These local observations are diagnostic, not regression, release, support, or native-admission claims. |
| Hostile bytes-subclass review probe | Expected failure | Findings-first review added an exact hostile `bytes` subclass whose `__len__` raises a private runtime exception. Against the then-current `isinstance` check, that regression failed with the raw exception while 16 existing and new controls passed in 0.91 seconds. No correction pass is claimed from this probe. |
| Corrected exact-built-in-bytes focused gate | 0 | Both changed Python files were format clean; Ruff and strict Pyright reported zero findings; all 243 M47-M57 implementation, compatibility, boundary, and documentation assertions passed in 2.37 seconds; strict docs built in 1.03 seconds with only the known upstream notice; whitespace was clean. |
| Corrected whole-tree static, architecture, and documentation gate | 0 | The unchanged lock resolved 46 packages and checked the locked 45-package graphics environment. All 300 Python files were format clean; Ruff and strict Pyright reported zero findings; all 621 architecture assertions passed in 4.20 seconds; strict docs built in 1.02 seconds with only the known upstream notice; whitespace was clean. |
| Corrected complete supported-Python candidate gate | 0 | The graphics-enabled corrected candidate passed 2,161 tests with 14 expected skips on CPython 3.12.13 in 104.14 seconds, CPython 3.13.13 in 103.22 seconds, and CPython 3.14.5 in 108.44 seconds. The suites ran serially because the repository shares one temporary test root. |
| Corrected real-wgpu, profiles, and vertical slices | 0 | After restoring the locked 45-package CPython 3.12.13 graphics environment, all ten real-wgpu tests passed in 6.62 seconds. Three-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`, three draws, and 16 sprites. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, committed receipts, six query matches, five replay batches, and passing tests. |
| Corrected documented M1-M4 benchmark gate | 0 | All four fresh artifact contracts validated on dirty Windows CPython 3.12.13. M1 accepted seven workloads with one of two historical targets observed; M2 accepted four informational workloads with no timing targets; M3 accepted six workloads with zero of two historical targets met; M4 accepted three workloads with its baseline target observed. These local observations are diagnostic, not regression, release, support, or native-admission claims. |
| Pre-record reproducible distribution and release gate | 0 | Two confirmed-absent builds reproduced a pure 271,132-byte wheel at SHA-256 `60bbe7949601cf2b47d2fadb4bbf9174e8679f030195d40b54dc0c428573f669` and a 1,098,995-byte source distribution at `70d7bd8f117c5a59bc9d73d5de377554142d17e5c5788539c09cb30d45ef0297`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed for `0.1.0a1`. This factual row changes the source archive afterward, so final exact-tree artifact identities remain pending. |
| Findings-first correctness, scope, archive, credential, identity, history, and integrity review | 0 | No actionable issue remains after exact-built-in-bytes validation. The candidate is confined to 16 verifier/test/RFC/public-document/project-record paths and changes no workflow, runtime package, benchmark, project metadata, or lock. Failure ordering remains framing, status, body block, declared length, independent expected size, then publication; no private response state, raw parser, new header requirement, or unframed completeness claim was added. The 94-entry pure wheel and 480-entry source distribution contain no retired repository-control path, native library, WASM, or bytecode payload. Token-length credential/private-key and added-line identity-marker scans returned no match; `[retired control directory]`, `[retired control directory]`, `[retired control directory]`, and `[retired control file]` remain absent. History is linear from exact M56 closeout, only `main` plus the intended neutral feature branch exist, whitespace is clean, and full Git-object checking passes with only expected unreachable historical objects reported. |
| Final record-inclusive static, architecture, documentation, and integrity gate | 0 | The unchanged lock resolved 46 packages and checked the locked 45-package CPython 3.12.13 graphics environment. All 300 Python files were format clean; Ruff and strict Pyright reported zero findings; all 621 architecture assertions passed in 4.78 seconds; strict docs built in 1.06 seconds with only the known upstream notice; whitespace was clean. |
| Final record-inclusive reproducible distribution and release gate | 0 | Two new confirmed-absent output directories reproduced the pure 271,132-byte wheel at SHA-256 `60bbe7949601cf2b47d2fadb4bbf9174e8679f030195d40b54dc0c428573f669` and the 1,099,267-byte source distribution at `91a3b4e12c1542ab047fce560da8b98c9455e6618f2524e16f661861b3c8d886`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed for `0.1.0a1`. This factual row changes the source archive afterward, so hosted exact-head distribution identity remains authoritative. |
| Final evidence-inclusive local gate | 0 | The unchanged 46-package lock resolved in 0.82 ms; all 300 Python files remained format clean; Ruff and strict Pyright reported zero findings; all 621 architecture assertions passed in 4.31 seconds; strict docs built in 1.03 seconds with only the known upstream notice; whitespace and full Git-object checking passed, with only expected unreachable historical objects reported. |
| Hosted exact-head feature gate | 0 | PR #123 exact head `f7347965d7e9a78218fa08a34f76aed7d32ba67d` passed run `31332655171` in exactly three Linux-first allocations. Linux job `93293248918` passed in 5m37s before macOS `93293864546` and Windows `93293864554` began; they passed in 1m51s and 3m48s. Linux baseline passed 2,165 tests; Ubuntu CPython 3.13/3.14 and both desktop CPython 3.14 suites passed 2,165 tests with one expected skip. Every platform passed ten real-graphics tests, profile smoke, Clockwork Arena, and Agent World Builder. Hosted reproducibility produced a pure 271,119-byte wheel (`a24b3d068c351370dca59d320a15dc8148ea64bfbcf6f8540591c4aeed96be61`) and 1,099,375-byte sdist (`61add34b6732f399d772a556bf59d06816c30c794f1bd1c6a0d09905f2645602`); installed-wheel and complete release smoke passed. |
| Hosted review and exact-tree squash audit | 0 | Two delayed audits found zero issue comments, review comments, reviews, or threads. PR #123 was ready, `MERGEABLE/CLEAN`, exact-head/exact-base, and had exactly three successful checks. Head-pinned squash `800050c74530d74a72338b5d444ee4751c5ad155` has tree `44b379cdcc510ee55bbaf35dce0bc826ffadb3ab` exactly equal to reviewed head `f7347965d7e9a78218fa08a34f76aed7d32ba67d`, sole parent M56 closeout `187cbfb1c857e62594e49d1cf8e7591024aff8c9`, a valid GitHub signature, and standalone DCO. The merged feature branch was deleted locally/remotely. Synchronized `main` has no post-merge run, open pull request, non-main remote branch, tag, or release. |
| Four-file integration-record local gate | 0 | The unchanged lock resolved 46 packages in 0.81 ms and checked the locked 45-package graphics environment. All 300 Python files were format clean; Ruff and strict Pyright reported zero findings; all 621 architecture assertions passed in 4.30 seconds; strict docs built in 1.03 seconds with only the known upstream notice. Whitespace and the protected workflow/metadata/lock/runtime/test/benchmark/script/public-document surface comparison passed. Two fresh confirmed-absent builds reproduced the pure 271,132-byte wheel (`60bbe7949601cf2b47d2fadb4bbf9174e8679f030195d40b54dc0c428573f669`) and 1,100,566-byte sdist (`b5799e4176802fa2ea180599fc0009fbc4e13ed3f0bca311ce6c5d76cd089d37`); installed-wheel and complete release smoke passed. This factual row changes the packaged source archive afterward, so exact integration-head identities remain delegated to hosted evidence. |
| Final integration-record evidence-inclusive gate | 0 | The unchanged 46-package lock resolved in 0.78 ms; all 300 Python files remained format clean; Ruff and strict Pyright reported zero findings; all 621 architecture assertions passed in 4.28 seconds; strict docs built in 1.05 seconds with only the known upstream notice. Whitespace and the protected workflow/metadata/lock/runtime/test/benchmark/script/public-document surface comparison remained clean. |
| Integration-record hosted gate | 0 | PR #124 exact head `b959cad56d0c9e9b3b34d02d313ce4a6b67a9fa9` passed run `31333440409` in one 36-second Linux allocation. All 300 Python files were format clean, Ruff passed, strict docs built in 1.05 seconds, all 621 documentation architecture assertions passed in 6.60 seconds, reproducible build plus installed-wheel and complete release smoke passed. The exact-head 271,119-byte wheel was `a24b3d068c351370dca59d320a15dc8148ea64bfbcf6f8540591c4aeed96be61`; the 1,100,675-byte sdist was `b1c10ecfd5b3dedcf2cf2bf0a25f5277d1d40f76ef3da4e79292810a80a6c603`. Desktop umbrella job `93295290611` skipped with zero steps and no runner allocation. |
| Integration-record review, squash, and cleanup audit | 0 | Two delayed audits found exact head/base, `MERGEABLE/CLEAN`, one successful Linux check, one zero-step skipped umbrella, and no issue comment, review comment, review, or thread. Head-pinned GitHub-verified squash `f28d5ee6e9b1e3d65b1ff47c4574e8525cb6c85e` has tree `f8dcbfab5044a58bcfe9e1f0600ac82661d1dc8a` exactly equal to reviewed record head `b959cad56d0c9e9b3b34d02d313ce4a6b67a9fa9`, sole parent feature squash `800050c74530d74a72338b5d444ee4751c5ad155`, a valid signature, and standalone DCO. No post-merge `main` run was allocated; both M57 working branches were deleted locally/remotely, and no open pull request, non-main remote branch, tag, or release exists. |
| Three-file closeout prepublication audit | 0 | The unchanged lock resolved 46 packages in 0.77 ms; all 300 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 621 architecture assertions passed in 4.30 seconds; strict docs built in 1.05 seconds with only the known upstream notice. Exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md` changed; protected workflows, metadata, lock, runtime, tests, benchmarks, scripts, public docs, and roadmap are unchanged. Whitespace, current-added-line identity scanning, and full Git-object checking passed with only expected unreachable historical objects reported. `main`, `origin/main`, and `origin/HEAD` resolve to verified integration squash `f28d5ee6e9b1e3d65b1ff47c4574e8525cb6c85e`; only `main` and the intended local closeout branch exist. No remote working branch, open pull request, post-integration `main` run, tag, or GitHub release exists. |

Closeout publication must allocate zero hosted runs or checks; publication
evidence follows only after those operations actually execute.

## M56 development evidence - 2026-08-10, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| M55 closeout audit | 0 | Exact synchronized `main`, `origin/main`, and `origin/HEAD` resolved to verified M55 closeout `e7f700454adf1c11c80cb1ba684ed3318f7876e4`. Only `main` existed locally/remotely; no open pull request, tag, release, or post-closeout `main` run existed; full Git-object checking passed. |
| Focused inherited M47-M55 baseline | 0 | All 189 public-release assertions passed in 1.93 seconds on the exact clean M55 closeout. |
| Official Python 3.14 and RFC 9110/3986 review | 0 | Python documents `HTTPResponse.status`, the `getheaders()` pair list, URL-parser non-validation, and `urljoin()` authority replacement by an absolute second argument. RFC 9110 defines valid status integers as 100 through 599, Location as a single URI-reference, multiple-field recovery as non-interoperable, and minimum 8,000-octet support. RFC 3986 defines generic URI-reference characters, percent encoding, and relative resolution. |
| Tests-first M56 behavior probe | Expected failure | Against the unchanged verifier, 25 assertions failed, six passed, and two documentation/boundary checks were intentionally deselected. Failures demonstrated accepted float `200.0`, raw malformed-status exceptions, joined Location use, absent exact field-occurrence validation, permissive whitespace/control/backslash/non-ASCII/incomplete-percent/oversize handling, and raw invalid-IPv6 resolution failure. No implementation pass is claimed from this probe. |
| Implemented M56 behavior and boundary gate excluding documentation | 0 | Ruff passed the verifier, compatible M47-M55 fixtures, and new M56 tests. All 32 then-existing M56 behavior/boundary assertions passed in 0.48 seconds; only the documentation guard was deselected. |
| Inherited M47-M56 compatibility attempt | Corrected | 220 assertions passed, but the M55 source-order guard still searched for direct `response.status` use removed by the stricter M56 helper. No complete inherited pass is claimed. The guard now proves M55 framing still precedes the M56 status validator. |
| Corrected inherited M47-M56 behavior gate excluding documentation | 0 | All 221 assertions passed in 2.17 seconds with only the then-pending M56 documentation guard deselected. |
| Focused M47-M56 implementation and documentation gate | 0 | All 11 focused Python files were format clean; Ruff reported zero findings; all 223 focused assertions passed in 2.19 seconds, including the completed RFC/public/maintainer documentation guard; strict docs built in 1.05 seconds with only the known upstream notice; whitespace was clean. |
| First whole-tree static attempt | Corrected | The unchanged lock resolved 46 packages. `uv sync --frozen --all-groups` completed but correctly omitted the optional graphics extra, removing six graphics packages. All 299 Python files were format clean; Ruff, all 601 architecture assertions in 4.62 seconds, strict docs in 1.11 seconds, and whitespace passed. Strict Pyright stopped on five partially unknown M56 tuple values plus 17 expected missing/unknown graphics-import diagnostics. No type-check or complete static-gate pass is claimed. M56 now widens the runtime tuple explicitly to `tuple[object, ...]`, and the corrected environment includes the locked graphics extra. |
| Second whole-tree static attempt | Corrected | The six locked graphics packages were restored. Ruff, all 601 architecture assertions in 5.25 seconds, strict docs in 1.09 seconds, and whitespace passed, but formatting required one verifier rewrite and strict Pyright rejected two now-unnecessary string casts after the explicit tuple widening. No format, type-check, or complete static-gate pass is claimed. The casts are removed and the formatter is applied before the final gate. |
| Corrected whole-tree static, architecture, and documentation gate | 0 | The unchanged lock resolved 46 packages. All 299 Python files were format clean; Ruff and strict Pyright reported zero findings; all 601 architecture assertions passed in 4.83 seconds; strict docs built in 1.11 seconds with only the known upstream notice; whitespace was clean. |
| Complete supported-Python candidate gate | 0 | The graphics-enabled candidate passed 2,141 tests with 14 expected skips on CPython 3.12.13 in 104.11 seconds, CPython 3.13.13 in 102.55 seconds, and CPython 3.14.5 in 109.56 seconds. |
| Real-wgpu, profiles, and vertical slices | 0 | After restoring the locked 45-package CPython 3.12.13 graphics environment, all ten real-wgpu tests passed in 6.58 seconds. Three-repeat two-workload base and three-workload graphics M7 profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`. Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, committed apply/adjust receipts, six query matches, five replay batches, and passing registered tests. |
| Documented M1-M4 benchmark gate | 0 | All four retained artifact contracts validated. M1 accepted seven workloads with one of two historical targets observed; M2 accepted four informational workloads with no timing target; M3 accepted six workloads with zero of two historical targets met; M4 accepted three workloads with its baseline target observed. These dirty-tree local observations are not regression, release, or support claims. |
| First reproducible-build attempt inside the restricted sandbox | Blocked | `uv build --out-dir .tmp/m56-dist-first` failed before project build because the configured uv cache was outside sandbox access. No build pass is claimed from this attempt; both output directories had been confirmed absent and the same command was rerun with approved cache access. |
| Pre-record reproducible distribution and release gate | 0 | Two confirmed-absent builds reproduced a pure 270,842-byte wheel at SHA-256 `90766e19603c2e9bda56418d8f41ebbe817ef378fac968b81d5dc5dba9e2a3be` and a 1,087,149-byte source distribution at `93c86e3b89b002075a0af3f4de33c83ac27e1146979deb25e9f34f286f10ab93`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed for `0.1.0a1`. This factual row changes the source archive afterward, so final exact-tree artifact identities remain pending. |
| First archive inspection attempt | Corrected | The first PowerShell wheel inspection lacked the compression assembly and returned type/null errors, so no archive result is claimed from it. Loading the standard compression assembly corrected the inspection. |
| Findings-first correctness, scope, archive, credential, identity, history, and integrity review | 0 | Review corrected one RFC consequence that could imply a general URI syntax validator; the accepted wording now describes the bounded character and percent-escape subset. Repeat review found no actionable issue in status/framing/redirect ordering, stable errors, header occurrence, URI bounds, cross-host handling, or per-hop revalidation. The 25-path candidate changes no workflow, runtime package, benchmark, project metadata, or lock. The 94-entry pure wheel and 478-entry source distribution contain no retired repository-control path, native library, WASM, or bytecode payload. Token-length credential/private-key and current-added-line identity-marker scans returned no match; `[retired control directory]`, `[retired control directory]`, `[retired control directory]`, and `[retired control file]` remain absent. History is linear from exact M55 closeout, only `main` plus the intended neutral feature branch exist, whitespace is clean, and full Git-object checking passes. |
| Post-review focused implementation and documentation gate | 0 | All 223 M47-M56 assertions passed in 2.67 seconds after the wording correction; strict docs built in 1.05 seconds with only the known upstream notice. |
| Final record-inclusive static, architecture, documentation, and integrity gate | 0 | The unchanged lock resolved 46 packages and checked the locked 45-package graphics environment. All 299 Python files were format clean; Ruff and strict Pyright reported zero findings; all 601 architecture assertions passed in 4.77 seconds; strict docs built in 1.12 seconds with only the known upstream notice; whitespace and full Git-object checks passed. |
| Final record-inclusive reproducible distribution and release gate | 0 | Two new confirmed-absent output directories reproduced the pure 270,842-byte wheel at SHA-256 `90766e19603c2e9bda56418d8f41ebbe817ef378fac968b81d5dc5dba9e2a3be` and the 1,088,119-byte source distribution at `ff2476fbccf5b260a04d0fc98b4e3d0df33045449ef29c66795915caf1790937`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed for `0.1.0a1`. This factual row changes the source archive afterward, so hosted exact-head distribution identity remains required. |
| Final evidence-inclusive local gate | 0 | The unchanged 46-package lock resolved in 0.72 ms; all 299 Python files remained format clean; Ruff and strict Pyright reported zero findings; all 601 architecture assertions passed in 4.89 seconds; strict docs built in 1.14 seconds with only the known upstream notice. Hosted exact-head validation remains pending. |
| Initial hosted exact-head gate | Corrected | PR #120 exact head `86b2d4eaf404b15100bfc7d083fe119adc3e9f11` passed run `31328303442` in exactly three Linux-first allocations. Linux job `93282247295` passed in 7m37s before macOS `93283140177` and Windows `93283140179` began; they passed in 3m16s and 4m12s. Linux baseline passed 2,145 tests; Ubuntu CPython 3.13/3.14 and both desktop CPython 3.14 suites passed 2,145 tests with one expected skip. Every platform passed ten real-graphics tests, profile smoke, Clockwork Arena, and Agent World Builder. Hosted reproducibility produced a pure 270,827-byte wheel (`ed35ebe1208a422211bf00a185f973ce6ae0b96b2ffff302a2deb1ab2484479f`) and 1,088,361-byte sdist (`4b6fd61e733a2a1eeafd42a9e401768af920aefb9cbfbe7dc38eae84b4a620b1`); installed-wheel and complete release smoke passed. Delayed review then found bracket delimiters accepted in path/query components, so no merge or final acceptance is claimed for this head. |
| Reviewer-derived bracket tests-first reproduction | Expected failure | The unchanged implementation failed the exact `/asset[stale]` and `?token=[bad]` cases by following each malformed reference until the fake response iterator exhausted; 14 existing and new controls passed, including a valid bracketed IPv6 authority. No correction pass is claimed from this probe. |
| Targeted bracket-delimiter correction gate | 0 | All 16 exact invalid-reference and valid-control cases passed in 0.37 seconds. The correction rejects bracket delimiters in path, query, and fragment components while retaining them inside a parsed valid IPv6 authority. |
| Corrected focused, static, architecture, and documentation gate | 0 | All 226 focused M47-M56 assertions passed in 2.21 seconds. The unchanged lock resolved 46 packages; all 299 Python files were format clean; Ruff and strict Pyright reported zero findings; all 604 architecture assertions passed in 4.77 seconds; strict docs built in 1.08 seconds with only the known upstream notice. |
| Corrected complete supported-Python candidate gate | 0 | The graphics-enabled corrected candidate passed 2,144 tests with 14 expected skips on CPython 3.12.13 in 105.04 seconds, CPython 3.13.13 in 102.94 seconds, and CPython 3.14.5 in 108.83 seconds. |
| Corrected real-wgpu, profiles, and vertical slices | 0 | The locked 45-package CPython 3.12.13 graphics environment was restored. All ten real-wgpu tests passed in 6.73 seconds. Three-repeat two-workload base and three-workload graphics M7 profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, replay `sha256:d5051aa5b4a004e48f449940ec4788f8f227d4509d80f080f6371d7c9299b2ef`, committed receipts, six query matches, five replay batches, and passing tests. |
| Corrected pre-record reproducible distribution and release gate | 0 | Two fresh confirmed-absent builds reproduced a pure 270,883-byte wheel at SHA-256 `c91c9e7c6937d125f904edf6ba8047e9e1072be5ef86b23513c507475ad04133` and a 1,089,764-byte source distribution at `22b0b9519b35c2e57537300e90196fe9655077e6acc93f164ad1b0f01c2533a9`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed. This factual row changes the source archive afterward, so final exact-tree and hosted artifact identities remain pending. |
| Corrected findings-first scope, archive, credential, identity, history, and integrity review | 0 | No actionable finding remains. The correction is confined to 13 verifier/test/documentation/project-record paths and changes no workflow, runtime package, benchmark, project metadata, or lock. Component-aware bracket rejection preserves the valid IPv6 authority control and stable content-silent redirect failure. The 94-entry wheel and 478-entry source distribution contain no retired repository-control path, native library, WASM, or bytecode payload. Token-length credential/private-key and correction-added-line identity-marker scans returned no match; whitespace and full Git-object checking pass. |
| Final corrected record-inclusive static and documentation gate | 0 | The unchanged lock resolved 46 packages in 0.77 ms; all 299 Python files were format clean; Ruff and strict Pyright reported zero findings; all 604 architecture assertions passed in 5.55 seconds; strict docs built in 1.14 seconds with only the known upstream notice. |
| Final corrected record-inclusive reproducible distribution and release gate | 0 | Two new confirmed-absent output directories reproduced the pure 270,883-byte wheel at SHA-256 `c91c9e7c6937d125f904edf6ba8047e9e1072be5ef86b23513c507475ad04133` and the 1,090,241-byte source distribution at `e4f5998477c0d4b0ef6001443abe62663ef8a3520e54101ed6bcced7e4992995`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed. This factual row changes the source archive afterward, so replacement hosted exact-head artifact identity remains authoritative. |
| Corrected final evidence-inclusive local gate | 0 | The unchanged lock resolved in 0.74 ms; all 299 Python files remained format clean; Ruff and strict Pyright reported zero findings; all 604 architecture assertions passed in 4.85 seconds; strict docs built in 1.11 seconds with only the known upstream notice. |
| Corrected hosted exact-head feature gate | 0 | PR #120 exact head `35b94a42b10cbd8f75048d3200e95a4aca81fa5d` passed run `31329613114` in exactly three Linux-first allocations. Linux job `93285627958` passed in 7m22s before macOS `93286456923` and Windows `93286456914` began; they passed in 2m19s and 4m00s. Linux baseline passed 2,148 tests; Ubuntu CPython 3.13/3.14 and both desktop CPython 3.14 suites passed 2,148 tests with one expected skip. Every platform passed ten real-graphics tests, profile smoke, Clockwork Arena, and Agent World Builder. Hosted reproducibility produced a pure 270,869-byte wheel (`c09dfe4f799ecad4860d088588a547786c0a9ed8cf3cc8045f8f1eb417c31cf2`) and 1,090,506-byte sdist (`7de047cbe0b6dc5b8120795e6c1207db8a66a3f0a4372d8a69fad510a7116368`); installed-wheel and complete release smoke passed. |
| Hosted review resolution and exact-tree squash audit | 0 | The sole valid P2 review comment was answered with the correction evidence and its thread resolved. Two delayed audits found zero issue comments, exactly the original review comment plus its reply, and no unresolved thread or later review activity. PR #120 was ready, `MERGEABLE/CLEAN`, exact-head/exact-base, and had exactly three successful checks. Head-pinned squash `22c432310fae2f9ac372062cbd465cc2617fb95c` has tree `a891364113a439c08e985c925fc81a507053fb2c` exactly equal to corrected head `35b94a42b10cbd8f75048d3200e95a4aca81fa5d`, sole parent M55 closeout `e7f700454adf1c11c80cb1ba684ed3318f7876e4`, a valid GitHub signature, and standalone DCO. Fetch pruned the deleted remote feature branch; its verified local squash-source branch was then deleted. Synchronized `main` has no post-merge run, open PR, non-main remote branch, tag, or release. |
| First four-file integration-record local gate | Blocked | The restricted-cache `uv lock --check` attempt failed before project validation because uv could not initialize its existing user cache. No lock or later command in that fail-fast sequence is represented as passing. |
| Corrected four-file integration-record local gate | 0 | With approved cache access, the unchanged lock resolved 46 packages in 0.79 ms; all 299 Python files were format clean; Ruff and strict Pyright reported zero findings; all 604 architecture assertions passed in 4.23 seconds; strict docs built in 1.03 seconds with only the known upstream notice. Whitespace and the protected workflow/metadata/lock/runtime/test/benchmark/script surface comparison passed. Two fresh confirmed-absent builds reproduced the pure 270,883-byte wheel (`c91c9e7c6937d125f904edf6ba8047e9e1072be5ef86b23513c507475ad04133`) and 1,091,471-byte sdist (`f255d15f017b4a368d981effbe390ef624d18ad46d25db87589b30f34f9c9dd4`); installed-wheel and complete release smoke passed. This factual row changes the packaged source archive afterward, so exact integration-head identities remain delegated to hosted evidence. |
| Integration-record hosted gate | 0 | PR #121 exact head `db7c50009243fa7cf3bf9cd8f57afb4589dec7e7` passed run `31330464522` in one 38-second Linux allocation. All 299 Python files were format clean, Ruff passed, strict docs built in 1.40 seconds, all 604 documentation architecture assertions passed in 7.72 seconds, reproducible build plus installed-wheel and complete release smoke passed. The exact-head 270,869-byte wheel was `c09dfe4f799ecad4860d088588a547786c0a9ed8cf3cc8045f8f1eb417c31cf2`; the 1,091,735-byte sdist was `3b11cdf8917b6651bb492b9b6ad2eac4ec21922161d4bbf85bbbb8c9c8f83abc`. Desktop umbrella job `93287863357` skipped with zero steps and no runner allocation. |
| Integration-record review, squash, and cleanup audit | 0 | Two delayed audits found exact head/base, `MERGEABLE/CLEAN`, one successful Linux check, one zero-step skipped umbrella, and no issue comment, review comment, review, or thread. Head-pinned GitHub-verified squash `acc6893ef4cadf9a17c87cd578e38b7802a3ed77` has tree `69ed3d44d8eab6cfa98cb646f897a9cb295296f8` exactly equal to reviewed record head `db7c50009243fa7cf3bf9cd8f57afb4589dec7e7`, sole parent feature squash `22c432310fae2f9ac372062cbd465cc2617fb95c`, a valid signature, and standalone DCO. No post-merge `main` run was allocated; both M56 working branches were deleted locally/remotely, and no open PR, non-main remote branch, tag, or release exists. |
| Three-file closeout prepublication audit | 0 | The unchanged lock resolved 46 packages in 0.79 ms; all 299 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 604 architecture assertions passed in 4.12 seconds; strict docs built in 1.03 seconds with only the known upstream notice. Exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md` changed; protected workflows, metadata, lock, runtime, tests, benchmarks, scripts, public docs, and roadmap are unchanged. Whitespace, current-added-line identity scanning, and full Git-object checks passed. `main`, `origin/main`, and `origin/HEAD` resolve to verified integration squash `acc6893ef4cadf9a17c87cd578e38b7802a3ed77`; only `main` and the intended local closeout branch exist. No remote working branch, open pull request, post-integration `main` run, tag, or GitHub release exists. |

Closeout publication must allocate zero hosted runs or checks; publication
evidence follows only after those operations actually execute.

## M55 development evidence - 2026-08-10, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| M54 closeout audit | 0 | Exact synchronized `main`, `origin/main`, and `origin/HEAD` resolved to verified M54 closeout `aab15d601eb4402213f2e058f270237b964f1000`. Only `main` existed locally/remotely; no open pull request, tag, release, or post-closeout `main` run existed. |
| Official Python 3.14 and RFC 9112 HTTP framing review | 0 | Python documents integer response version `11` for HTTP/1.1 and `getheader()` joining repeated values with `, `. RFC 9112 defines HTTP/1.1 framing, client acceptance of chunked transfer coding, and the `Transfer-Encoding`/`Content-Length` ambiguity. RFC-0038 adopts only documented response metadata and makes no general request-smuggling claim. |
| Focused inherited M47-M54 compatibility probe | 0 | All 157 inherited public-release assertions passed in 1.83 seconds after valid response fakes exposed `version=11`; no workflow, runtime, dependency, package, or lock file changed. |
| M55 behavioral gate excluding documentation | 0 | Ruff formatted the new test and reported zero findings; all 30 HTTP/1.1 version, transfer-coding, framing ambiguity, content-length type, cause/content, redirect-ordering, and frozen-boundary assertions passed in 0.48 seconds; one documentation guard was intentionally deselected until contract documents existed. |
| Focused M47-M55 implementation and documentation gate | 0 | All ten focused Python files were format clean; Ruff reported zero findings; all 188 focused public-release assertions passed in 1.84 seconds; strict docs built in 1.03 seconds with only the known upstream notice. |
| First whole-tree gate inside the restricted sandbox | Blocked | Every uv command failed before project execution because the configured cache at `C:\Users\louij\AppData\Local\uv\cache` was outside sandbox access. The trailing whitespace check returned zero, making the combined shell status misleading; no uv pass is claimed from this attempt. |
| First approved whole-tree static attempt | Corrected | The unchanged lock resolved and all 298 Python files plus Ruff passed, but strict Pyright rejected three runtime shape checks as statically unnecessary against `HTTPResponse` annotations. No type-check or later gate pass is claimed. The documented values are now widened explicitly to `object` so hostile/malformed runtime observations remain checked without suppressing diagnostics. |
| Corrected whole-tree static, architecture, and documentation gate | 0 | The unchanged lock resolved 46 packages and checked the locked 45-package graphics environment. All 298 Python files were format clean; Ruff and strict Pyright reported zero findings; all 566 architecture assertions passed in 3.62 seconds; strict docs built in 1.02 seconds with only the known upstream notice; whitespace was clean. |
| Complete supported-Python candidate gate | 0 | The graphics-enabled candidate passed 2,106 tests with 14 expected skips on CPython 3.12.13 in 104.14 seconds, CPython 3.13.13 in 103.30 seconds, and CPython 3.14.5 in 107.70 seconds. |
| Real-wgpu, profiles, and vertical slices | 0 | The locked CPython 3.12.13 graphics environment was restored with 45 packages. All ten real-wgpu tests passed in 6.69 seconds. Three-repeat two-workload base and three-workload graphics M7 profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, with committed receipts, six query matches, five replay batches, and registered tests passing. |
| Documented benchmark gate | 0 | M1 validated seven workloads with one of two recorded targets observed; M2 validated four target-free informational workloads; M3 validated six workloads with zero of two observed targets met and no target claim; M4 validated three workloads with its baseline target observed. These are local dirty-tree observations, not regression or support claims. |
| Pre-record reproducible distribution and release gate | 0 | Two confirmed-absent output directories reproduced a pure 270,516-byte wheel at SHA-256 `71c93b0461fc982f5a1f8db6947ab17abbec6647fc0403fb0fd3dff8a3abc44f` and a 1,075,009-byte source distribution at `186ff7201ba19c935a760099ecb3b2ce0602174e526b449ca0ea9d397e2e1ae4`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed for `0.1.0a1`. This factual row changes the source archive afterward, so final exact-tree artifact identities remain pending. |
| First credential-pattern review | Corrected | The focused M47-M55 suite passed 188 assertions; workflow, release-workflow, project-metadata, and lock hashes matched the frozen M55 expectations; the wheel contained 94 entries and the source distribution 476. The credential pattern then produced one benign `ghp-import` package-name match in `uv.lock` because it accepted any characters after `ghp_`; no clean credential-scan claim is made from that attempt. |
| Corrected findings-first scope, archive, credential, identity, and integrity review | 0 | No actionable finding remains. The 24-path candidate is confined to the portable release verifier, inherited/new architecture tests, accepted RFC/public/maintainer documentation, roadmap, changelog/navigation, and neutral project records. There is no diff in either workflow, `src/ludoweave`, benchmarks, project metadata, or lock. The 94-entry wheel and 476-entry sdist contain no retired repository-control path, native library, WASM, or bytecode payload. Token-length credential/private-key and current-added-line identity-marker scans returned no match. History remains linear from exact verified M54 closeout; whitespace and full Git-object checks pass; only `main` plus the intended neutral feature branch exist. |
| Final fail-fast static, architecture, docs, distribution, and release gate | 0 | The unchanged lock resolved and checked 45 packages; all 298 Python files were format clean; Ruff and strict Pyright reported zero findings; all 566 architecture assertions passed in 3.67 seconds; strict docs built in 1.03 seconds with only the known upstream notice. Two fresh builds reproduced the pure 270,516-byte wheel at `71c93b0461fc982f5a1f8db6947ab17abbec6647fc0403fb0fd3dff8a3abc44f` and a 1,075,386-byte source distribution at `5a66309e36841423ef7565a91d210b04779ca15e9c57e984b590371d31849920`; isolated-wheel and complete ten-artifact release smoke passed. Whitespace and full Git-object checks passed. This factual row changes the source archive afterward, so hosted exact-head distribution identity remains required. |
| Final evidence-inclusive local gate | 0 | The unchanged lock resolved; all 298 Python files were format clean; Ruff and strict Pyright reported zero findings; all 566 architecture assertions passed in 3.72 seconds; strict docs built in 1.03 seconds; whitespace and full Git-object checks passed. Hosted exact-head validation remains pending. |
| Initial hosted exact-head gate | Corrected | PR #117 head `77812ae6b25635a9831b43088bd4397645fb4adf` passed run `31324078779` in exactly three Linux-first allocations: Linux `93271525836` in 7m18s, macOS `93272308757` in 2m16s, and Windows `93272308758` in 3m55s. Static, supported-Python, real-graphics, profiles, samples, reproducible build, installed-wheel, and release smoke passed. Delayed review then found that CPython normalizes other raw `HTTP/1.x` status-line tokens to public `version=11`, so the prior exact-token implication was false. No merge/pass claim is made for the original contract; correction and revalidation follow. |
| CPython status-line normalization reproduction | 0 | The locked CPython 3.12 runtime parsed a synthetic `HTTP/1.9 200 OK` status line as public `HTTPResponse.version == 11`, confirming the review finding without network access. RFC/public/maintainer contracts and tests now describe `11` as the documented HTTP/1.1-class compatibility bucket and explicitly disclaim exact raw status-line evidence. |
| First corrected-head focused gate | Corrected | Both focused Python files were format clean, then Ruff stopped on one import-order finding in the added normalization test. No Ruff, type, test, docs, or whitespace pass is claimed from this combined attempt. The import block is now sorted and the full focused gate follows. |
| Corrected-head focused implementation and documentation gate | 0 | Both focused files were format clean; Ruff and strict Pyright reported zero findings; all 189 M47-M55 assertions passed in 1.92 seconds, including the real CPython normalization fixture; strict docs built in 1.02 seconds with only the known upstream notice; whitespace was clean. |
| Corrected-head whole-tree static, architecture, and documentation gate | 0 | The unchanged lock resolved 46 packages and checked the 45-package graphics environment. All 298 Python files were format clean; Ruff and strict Pyright reported zero findings; all 567 architecture assertions passed in 3.73 seconds; strict docs built in 1.03 seconds with only the known upstream notice; whitespace was clean. |
| Corrected-head supported-Python candidate gate | 0 | The graphics-enabled corrected candidate passed 2,107 tests with 14 expected skips on CPython 3.12.13 in 103.58 seconds, CPython 3.13.13 in 103.11 seconds, and CPython 3.14.5 in 108.10 seconds. |
| Corrected-head real-wgpu, profiles, vertical slices, distribution, and release gate | 0 | The locked CPython 3.12.13 graphics environment was restored with 45 packages; all ten real-wgpu tests passed in 6.85 seconds; three-repeat base and graphics profiles validated; both vertical slices reproduced their expected state and local captures. Two confirmed-absent builds reproduced a pure 270,606-byte wheel at `c53c613517c5a275fc61f3f3831a85e35538b79499d42b419df10daa5764bf7c` and a 1,077,638-byte source distribution at `0a165da8de52f47b66f28944caf69c87db4cf0bb2fa92cd830d0bd7bf82470d6`; isolated-wheel and complete ten-artifact release smoke passed. This row changes the source archive afterward, so hosted corrected-head artifact identity remains required. |
| Corrected-head findings-first review | 0 | All 32 focused M55 assertions passed against the revised contract. Every M55 surface explicitly disclaims exact raw status-line token evidence; the correction is confined to one test, one source docstring, RFC/public/maintainer/project records, and no workflow, dependency, lock, package, or release authority. Frozen hashes remain exact, token-shaped credential and current-added-line identity-marker scans returned no match, whitespace and Git-object checks pass, and no actionable local finding remains. |
| Corrected-head final evidence-inclusive local gate | 0 | The unchanged lock resolved; all 298 Python files were format clean; Ruff and strict Pyright reported zero findings; all 567 architecture assertions passed in 3.66 seconds; strict docs built in 1.05 seconds; whitespace and full Git-object checks passed. Corrected hosted exact-head validation remains pending. |
| Feature commits, push, and ready PR | 0 | The reviewed 24-path feature was DCO-signed as `77812ae6b25635a9831b43088bd4397645fb4adf`, pushed on neutral branch `security/m55-http-response-framing`, and published as ready PR #117 against exact M54 closeout. After the valid P2, the 14-path correction was DCO-signed as `f57c28b9cc3a05ef1da830c8ad478d85d46b4a3a`, pushed, and the PR scope updated. |
| Corrected hosted exact-head feature gate | 0 | PR #117 corrected head `f57c28b9cc3a05ef1da830c8ad478d85d46b4a3a` passed run `31325192734` in exactly three Linux-first allocations. Linux job `93274316988` passed in 7m26s before macOS `93275131866` and Windows `93275131863` began; they passed in 2m44s and 2m57s. Linux baseline, Ubuntu 3.13/3.14, and both desktop 3.14 suites passed 2,111 tests, with one expected skip outside baseline. Every platform passed ten real-graphics tests, profile smoke, Clockwork Arena, and Agent World Builder. Hosted reproducibility passed for a pure 270,593-byte wheel (`4b6917302282746f301e082003a4474cef230bc77bda7a0b19d90b59a7f566af`) and 1,077,996-byte sdist (`bd8378618ca43f52ea4049ecde33eed5a8a33a40228e891a3073710221df9e26`); installed-wheel and complete ten-artifact release smoke passed. |
| Corrected review, squash, and cleanup audit | 0 | The valid P2 was answered with exact correction evidence and its sole thread resolved. Two delayed audits found exact corrected head/base, `MERGEABLE/CLEAN`, exactly three successful checks, no issue comments, and no new or unresolved thread. Head-pinned GitHub-verified squash `879de01c5e1869c6493b59f4fbd904e361f9ddb6` has tree `d14d5b30a5ecc9ec1003e249150c3ce374325f1a` exactly equal to corrected feature head, sole parent M54 closeout `aab15d601eb4402213f2e058f270237b964f1000`, and standalone DCO. No post-merge `main` run was allocated; the feature branch was deleted locally/remotely, and no tag or release was created. |
| Integration-record local gate | 0 | On the exact four-file record diff, the unchanged lock resolved; all 298 Python files remained format clean; Ruff passed; all 567 architecture assertions passed in 3.90 seconds; strict docs built in 1.02 seconds; whitespace and full Git-object checks passed. Two builds reproduced the pure 270,606-byte wheel at `c53c613517c5a275fc61f3f3831a85e35538b79499d42b419df10daa5764bf7c` and a 1,078,881-byte sdist at `edd0e59e7055259a1ff4b1dc09360ece3d6b6a9ae02b2eaa013d9f74004fc057`; installed-wheel and complete release smoke passed. This row changes the source archive, so the documentation-only hosted exact-head result is authoritative. |
| Integration-record hosted gate and review correction | Corrected | Initial PR #118 head `e7cbfe5e4da0da20db0a28a10d1e7cc95ac86d6b` passed run `31325924046` in one 38-second Linux allocation: 298-file formatting, lint, strict docs in 1.55 seconds, all 567 architecture assertions in 7.02 seconds, reproducible build, installed-wheel smoke, and release smoke passed. The 270,593-byte wheel was `4b6917302282746f301e082003a4474cef230bc77bda7a0b19d90b59a7f566af`; the 1,078,944-byte sdist was `af7714675930f76cf16f9100d8ecc16d8f7706a55163b3dae5ffa43035c08b03`. Desktop umbrella job `93276242361` skipped with zero steps. Delayed review then found one stale sentence that still called corrected feature validation pending; no merge/pass claim is made for that contradictory record, and correction evidence follows. |
| Corrected integration-record local and hosted gate | 0 | The stale sentence was corrected in DCO-signed head `ff71acdadbee98043f3d9f06fa1bb08371f89bfc`. Locally, the unchanged lock resolved; 298-file formatting, lint, all 567 architecture assertions in 3.80 seconds, strict docs in 1.05 seconds, reproducible build, installed-wheel smoke, release smoke, and whitespace passed. Replacement run `31326132049` then passed the corrected exact head in one 38-second Linux allocation: 298-file formatting, lint, strict docs in 1.09 seconds, all 567 architecture assertions in 5.77 seconds, reproducible build, installed-wheel smoke, and release smoke. The 270,593-byte wheel was `4b6917302282746f301e082003a4474cef230bc77bda7a0b19d90b59a7f566af`; the 1,078,940-byte sdist was `273db1d43231a3afd020b4e6d3829de5f2f7589865565e7edc9cf2d79077171d`. Desktop umbrella job `93276763337` skipped with zero steps and no runner allocation. |
| Integration-record review, squash, and cleanup audit | 0 | The valid stale-status finding was answered with exact correction evidence and its sole thread resolved. The delayed audit found exact corrected head/base, `MERGEABLE/CLEAN`, successful Linux documentation check, zero-step skipped umbrella, no issue comments, and no new or unresolved thread. Head-pinned GitHub-verified squash `d0a230e2329daecf4e248350289351c1e81827f6` has tree `c079de60da5e3b24e8e9b11507f012ad9fbae13e` exactly equal to the corrected record head, sole parent feature squash `879de01c5e1869c6493b59f4fbd904e361f9ddb6`, a valid GitHub signature, and standalone DCO. No post-merge `main` run was allocated; both M55 integration branches were deleted locally/remotely, and no tag or release was created. |
| Three-file closeout prepublication audit | 0 | Exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md` changed with clean whitespace. `main`, `origin/main`, and `origin/HEAD` resolve to verified integration squash `d0a230e2329daecf4e248350289351c1e81827f6`; only `main` and the intended local closeout branch exist, no remote feature/record branch or open pull request remains, no tag or GitHub release exists, no post-integration `main` run was allocated, and full Git-object checking passes. The `.project/**`-only closeout must allocate zero hosted runs or checks. |

Closeout publication evidence follows only after those operations actually
execute.

## M54 development evidence - 2026-08-10, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| M53 closeout audit | 0 | Exact synchronized `main`, `origin/main`, and `origin/HEAD` resolved to verified M53 closeout `fe585f8bd2313feac39b70cadf088c57bbb1960e`. Only `main` existed locally/remotely; no open pull request, tag, release, or post-closeout `main` run existed. |
| Official Python 3.14 and OpenSSL 3.6 TLS resumption review | 0 | Python documents `SSLSocket.session_reused` as the post-handshake reuse observation and permits client `session` assignment before a handshake. OpenSSL documents TLS 1.3 resumption through a PSK path. RFC-0037 adopts only the exact portable observation, explicitly without claiming reconstructed handshake or certificate-exchange evidence. |
| Corrected focused M47-M53 compatibility gate | 0 | All 144 inherited public-release assertions passed in 1.59 seconds after valid fake sockets exposed `session_reused=False`; no workflow, runtime, dependency, or package file changed. |
| M54 behavioral gate excluding documentation | 0 | All 12 exact-false, malformed/missing/raising observation, cause/content, ordering, redirect-independence, and frozen-boundary assertions passed in 0.32 seconds; one documentation guard was intentionally deselected until the contract documents existed. |
| Focused M47-M54 implementation and documentation gate | 0 | Ruff formatted the new M54 test and reported zero findings; all 157 focused public-release assertions passed in 1.52 seconds, including the completed documentation guard. |
| First whole-tree gate inside the restricted sandbox | Blocked | Each uv command failed before project execution because the configured cache at `C:\Users\louij\AppData\Local\uv\cache` was outside sandbox access. The trailing whitespace check returned zero, making the combined shell status misleading; no uv pass is claimed from this attempt. |
| Approved whole-tree static, architecture, and documentation gate | 0 | The unchanged lock resolved 46 packages and checked the locked 45-package graphics environment. All 297 Python files were format clean; Ruff and strict Pyright reported zero findings; all 535 architecture assertions passed in 3.34 seconds; strict docs built in 1.01 seconds with only the known upstream notice; whitespace was clean. |
| Complete supported-Python candidate gate | 0 | The graphics-enabled candidate passed 2,075 tests with 14 expected skips on CPython 3.12.13 in 104.25 seconds, CPython 3.13.13 in 102.60 seconds, and CPython 3.14.5 in 109.59 seconds. |
| Real-wgpu, profiles, and vertical slices | 0 | The locked CPython 3.12.13 graphics environment was restored with 45 packages. All ten real-wgpu tests passed in 6.82 seconds. Three-repeat two-workload base and three-workload graphics M7 profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, with committed receipts, six query matches, five replay batches, and registered tests passing. |
| Documented benchmark gate | 0 | M1 validated seven workloads with one of two recorded targets observed; M2 validated four target-free informational workloads; M3 validated six workloads with zero of two observed targets met and no target claim; M4 validated three workloads with its baseline target observed. These are local dirty-tree observations, not regression or support claims. |
| Pre-record reproducible distribution and release gate | 0 | Two fresh builds reproduced a pure 270,334-byte wheel at SHA-256 `7177e64c931ff5f7fd1a798710a750eb8cf540f5d5de672512100741b747653b` and a 1,066,620-byte source distribution at `e3013919f171bf707690ec8e43a758cb5f467790e9a30f3d491f07c39c822dec`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed for `0.1.0a1`. This factual row and subsequent navigation correction change the source archive afterward, so final exact-tree artifact identities remain pending. |
| Documentation review correction | Corrected | Findings-first review found that the RFC index stopped at RFC-0034 and the changelog stopped at M51 despite accepted M52-M53 records. The index and changelog now cover M52-M54, and the M54 documentation guard includes both surfaces. The earlier broad gates remain truthful development evidence but do not validate this correction; final recorded-tree gates follow. |
| First post-record final gate | Corrected | Formatting, Ruff, strict Pyright, 534 of 535 architecture assertions, strict docs, two-build reproducibility, isolated-wheel smoke, and release smoke completed, but the documentation guard incorrectly required the roadmap milestone token in the RFC index's descriptive RFC-0037 link. Because PowerShell continued after pytest and the last command returned zero, the combined status was misleading; no complete final-gate pass is claimed. The guard now requires `M54` only in milestone-specific documents and separately proves the exact RFC-0037 index target. |
| Corrected M54 guard gate | 0 | The focused M54 file remained format clean, Ruff reported zero findings, and all 13 M54 assertions passed in 0.42 seconds. |
| Corrected fail-fast static, architecture, docs, and distribution gate | 0 | The unchanged 46-package lock resolved in 0.73 ms; all 297 Python files were format clean; Ruff and strict Pyright reported zero findings; all 535 architecture assertions passed in 3.34 seconds; strict docs built in 1.02 seconds with only the known upstream notice; whitespace was clean. Two builds reproduced a pure 270,334-byte wheel at SHA-256 `7177e64c931ff5f7fd1a798710a750eb8cf540f5d5de672512100741b747653b` and a 1,067,491-byte source distribution at `b1df5495d15bf3edfb31fbbbcf00a750bb7bf6d1e0df2492a52550f7299139af`; isolated-wheel and complete ten-artifact release smoke passed. This factual record changes the source archive afterward, so hosted exact-head distribution identity remains required. |
| Findings-first scope, archive, history, credential, and integrity review | 0 | No actionable finding remains. The 23-path candidate is confined to the portable release verifier, inherited/new architecture tests, accepted RFC/public/maintainer documentation, roadmap, changelog/navigation, and neutral project records. There is no diff in either workflow, `src/ludoweave`, benchmarks, project metadata, or lock. The 94-entry wheel and 474-entry sdist contain no retired repository-control path, native library, WASM, or bytecode payload. Focused credential/private-key and current-surface identity-marker scans returned no match. History is linear from exact verified M53 closeout, only `main` plus the intended neutral feature branch exist, whitespace is clean, and `git fsck --full --no-dangling` passes. |
| Final record-inclusive local gate | 0 | The unchanged 46-package lock resolves; all 297 Python files are format clean; Ruff and strict Pyright report zero findings; all 535 architecture assertions and strict docs pass; whitespace and full Git-object checks pass. Hosted exact-head validation remains pending. |
| Feature commit, push, and ready PR | 0 | The exact reviewed 23-path tree was committed as DCO-signed `d5d02a38ea302c0e314f966376e267c45508d14b` on neutral branch `security/m54-tls-session-freshness`, pushed, and published as ready PR #114 against exact M53 closeout `fe585f8bd2313feac39b70cadf088c57bbb1960e`. |
| Hosted exact-head feature gate | 0 | Ready PR #114 exact head `d5d02a38ea302c0e314f966376e267c45508d14b` passed run `31321661693` in exactly three Linux-first allocations. Linux job `93265498085` passed in 6m23s before macOS `93266207090` and Windows `93266207095` began; they passed in 2m10s and 4m11s. Linux baseline passed 2,079 tests; Ubuntu CPython 3.13/3.14 and both desktop CPython 3.14 suites each passed 2,079 tests with one expected skip. Every platform passed ten real-graphics tests, profile smoke, Clockwork Arena, and Agent World Builder. Hosted reproducibility passed for a pure 270,321-byte wheel (`009b51c9ddb4606968f195a5543288c7e98114ebaec85111347addf00a5eceee`) and 1,068,001-byte sdist (`b26ff481a608d9d9777e65650f9556c2d880d7ab28c01a7a38b7c6ed7c1b17f1`); installed-wheel and complete ten-artifact release smoke passed. |
| Delayed PR review, squash, and cleanup audit | 0 | PR #114 remained ready, exact-head/exact-base, `MERGEABLE/CLEAN`, with exactly three successful checks and no review, issue comment, inline comment, or thread. Head-pinned GitHub-verified squash `c333f2b9aad98b9a55d986076fe8b09153d30762` has tree `845032b09cb2a029ac1b73bcfe7ea6c20ccbfac5` exactly equal to reviewed feature head `d5d02a38ea302c0e314f966376e267c45508d14b`, sole parent M53 closeout `fe585f8bd2313feac39b70cadf088c57bbb1960e`, and standalone DCO. No post-merge `main` run was allocated; the feature branch was deleted locally/remotely, and no tag or release was created. |
| Integration-record local gate | 0 | On the exact four-file record diff, the unchanged lock resolved 46 packages in 0.78 ms; all 297 Python files remained format clean; Ruff passed; all 535 architecture assertions passed in 3.57 seconds; strict docs built in 1.03 seconds; whitespace and full Git-object checks passed. Two builds reproduced the 270,334-byte wheel at `7177e64c931ff5f7fd1a798710a750eb8cf540f5d5de672512100741b747653b` and a 1,068,828-byte sdist at `4f5503c1b3568fc04913af270a2205164f4dd4d8688e1af53b8a50f99437c49a`; installed-wheel and complete release smoke passed. This row changes the sdist afterward, so the hosted record-head artifact identity remains authoritative. |
| Integration-record commit, push, and ready PR | 0 | The exact reviewed four-file integration record was committed as DCO-signed `baec3a2bac0c0bdd8dd4bceb66cdb6e26973538b`, pushed on neutral branch `records/m54-integration`, and published as ready PR #115 against exact feature squash `c333f2b9aad98b9a55d986076fe8b09153d30762`. |
| Hosted integration-record gate | 0 | PR #115 exact head passed run `31322470238` in one 37-second Linux allocation. All 297 Python files were format clean, Ruff passed, strict docs built in 1.43 seconds, all 535 architecture assertions passed in 6.19 seconds, reproducibility passed for the 270,321-byte wheel (`009b51c9ddb4606968f195a5543288c7e98114ebaec85111347addf00a5eceee`) and 1,068,926-byte sdist (`4d4381962a27f08dcdf479081e7be726250c03f3224c9de6f5d24bb1da62f2b0`), and installed-wheel plus complete release smoke passed. Desktop umbrella `93267534507` skipped with zero steps; no compatibility/graphics allocation ran. |
| Integration-record review, squash, and cleanup audit | 0 | PR #115 remained ready, exact-head/exact-base, `MERGEABLE/CLEAN`, and review-clean with no issue comment, inline comment, or thread. Head-pinned GitHub-verified squash `50a14e0674c4e7468faf1c8ec4490846255558ce` has tree `5976f5b63353914199a7b677490090f12c8082f3` exactly equal to reviewed record head `baec3a2bac0c0bdd8dd4bceb66cdb6e26973538b`, sole parent feature squash `c333f2b9aad98b9a55d986076fe8b09153d30762`, and standalone DCO. No post-merge `main` run was allocated; both M54 working branches were deleted locally/remotely, and no tag or release was created. |
| Closeout-record local gate | 0 | The unchanged lock resolved 46 packages in 0.78 ms; all 297 Python files were format clean; Ruff and strict Pyright reported zero findings; all 535 architecture assertions passed in 3.44 seconds; strict docs built in 1.00 second with only the known upstream notice. Exactly three `.project/**` Markdown paths changed; whitespace and full Git-object checks passed. |

## M53 development evidence - 2026-08-10, Windows, CPython 3.12

| Command or review | Exit | Result |
| --- | ---: | --- |
| M52 closeout audit | 0 | Exact synchronized `main`, `origin/main`, and `origin/HEAD` resolved to verified M52 closeout `8d69f5b265277edb95ae47ea3a0af001217a4575`. Only `main` existed locally/remotely; no open pull request, tag, release, or post-closeout `main` run existed. |
| Official Python 3.14.7 `ssl` and `http.client` review | 0 | Python documents `SSLSocket.context` as the context to which the socket is tied, `SSLSocket.server_side` as its role, `SSLContext` post-use mutation as potentially surprising, and `HTTPSConnection(context=...)` as accepting the connection's SSL options. RFC-0036 applies those standard-library surfaces without a dependency or external runtime. |
| First focused M47-M52 compatibility probe | Corrected | The selected suite reached 20 passes before eight representative failures stopped it. Existing fake sockets lacked the standard `context` attribute, so the new fail-closed binding correctly rejected them before their older intended phases. No pass is claimed for this attempt. |
| Corrected focused M47-M52 compatibility gate | 0 | All 126 selected inherited public-release assertions passed in 1.25 seconds after test sockets retained the exact injected context and `server_side=False`. |
| M53 behavioral gate excluding documentation | 0 | All 17 exact-binding, client-role, missing/raising accessor, post-handshake mutation, ordering, redirect-independence, hash-boundary, and source-order assertions passed in 0.34 seconds; one documentation guard was intentionally deselected until the contract documents existed. |
| Focused M47-M53 implementation and documentation gate | 0 | Ruff formatted the new M53 test file, then reported zero findings; strict Pyright reported zero errors, warnings, or information findings; all 144 focused public-release assertions passed in 1.38 seconds, including the completed documentation guard. |
| First whole-tree gate inside the restricted sandbox | Blocked | Every uv command failed before project execution because the configured cache at `C:\Users\louij\AppData\Local\uv\cache` was outside sandbox access. A trailing whitespace check returned zero, so the combined shell status was misleading; no uv pass is claimed from this attempt. |
| First approved whole-tree environment attempt | Corrected | Lock checking and a frozen all-group sync completed, formatting and Ruff passed, but the sync removed the optional graphics packages. Strict Pyright then reported 17 unresolved/unknown wgpu-backend findings. This was an environment-selection issue; no type-check or later gate pass is claimed from this attempt. |
| Corrected whole-tree static, architecture, and documentation gate | 0 | Restoring the locked `graphics` extra installed the six expected optional packages. All 296 Python files were format clean; Ruff and strict Pyright reported zero findings; all 522 architecture assertions passed in 3.59 seconds; strict docs built in 1.06 seconds with only the known upstream notice; whitespace was clean. |
| Complete supported-Python candidate gate | 0 | The graphics-enabled candidate passed 2,062 tests with 14 expected skips on CPython 3.12.13 in 104.51 seconds, CPython 3.13.13 in 103.11 seconds, and CPython 3.14.5 in 108.09 seconds. |
| Real-wgpu, profiles, and vertical slices | 0 | After restoring the locked 45-package CPython 3.12.13 graphics environment, all ten real-wgpu tests passed in 6.64 seconds. Three-repeat two-workload base and three-workload graphics M7 profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, with committed receipts, six query matches, five replay batches, and registered tests passing. |
| Documented benchmark gate | 0 | M1 validated seven workloads with one of two recorded targets observed; M2 validated four target-free informational workloads; M3 validated six workloads with one of two recorded targets met; M4 validated three workloads with its baseline target observed. |
| Pre-record reproducible distribution and release gate | 0 | Two fresh builds reproduced a pure 270,186-byte wheel at SHA-256 `815202e5a5e458d755c1e292ea35b8765aa3e8103bd211a9e60a4fd588fdf748` and a 1,060,257-byte source distribution at `d3dac9acd99b92aade8a7c56c8ad375af196f11ca6e39124cf846874aa77ff93`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed for `0.1.0a1`. This factual row changes the source archive afterward, so final exact-tree artifact identities remain pending. |
| Final recorded-tree static, architecture, and documentation gate | 0 | The unchanged 46-package lock resolved in 0.87 ms and the locked 45-package CPython 3.12 graphics environment checked cleanly. All 296 Python files were format clean; Ruff and strict Pyright reported zero findings; all 522 architecture assertions passed in 3.79 seconds; strict docs built in 1.02 seconds with only the known upstream notice; whitespace was clean. |
| Final record-inclusive reproducible distribution and release gate | 0 | Two new confirmed-absent output directories reproduced the pure 270,186-byte wheel at SHA-256 `815202e5a5e458d755c1e292ea35b8765aa3e8103bd211a9e60a4fd588fdf748` and the 1,060,944-byte source distribution at `cad1bc18ac5f5ffa35fd82692843a63fd4f0916ce116dbc3e138333eea579e74`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed for `0.1.0a1`. This factual row changes the source archive afterward, so hosted exact-head build evidence will be authoritative rather than the pre-row sdist hash. |
| Findings-first diff, scope, history, and integrity review | 0 | No actionable finding remained. The 19-path candidate is confined to the portable verifier, inherited/new architecture tests, accepted RFC/public-maintainer documentation, roadmap, and neutral project records. Workflows, runtime package, benchmarks, metadata, and lock are unchanged; changed additions contain no repository-visible tool identity marker or credential; no backend/native object enters a public API. History is linear from verified M52 closeout, whitespace and full Git-object checking pass, and only `main` plus the intended local feature branch exist. |
| Post-evidence consistency gate | 0 | All 296 Python files remained format clean; Ruff and strict Pyright reported zero findings; all 18 M53 assertions passed in 0.43 seconds; strict docs built in 1.00 seconds with only the known upstream notice; whitespace was clean. |
| Hosted exact-head feature gate | 0 | Ready PR #111 exact head `0b3eaad213a149fb96c138cd4eabc1d861d053e9` passed run `31319422736` in exactly three Linux-first allocations. Linux job `93259888701` passed in 7m05s before macOS `93260670456` and Windows `93260670458` began; they passed in 2m08s and 4m01s. Linux baseline and Ubuntu CPython 3.13/3.14 each passed 2,066 tests, with one expected skip on the compatibility interpreters; macOS and Windows CPython 3.14 each passed 2,066 with one expected skip. Every platform passed ten real-graphics tests, profile smoke, Clockwork Arena, and Agent World Builder. Hosted reproducibility passed for a pure 270,172-byte wheel (`055d7f53440dc3e758d5ffd6b490b9cd1dd2072cbbbdd10f2932f13601536be6`) and 1,061,506-byte sdist (`2d1b7cb7ebe49ed7c79f630a53f0a197583731b0c7761de44170b53848258549`); installed-wheel and complete ten-artifact release smoke passed. |
| Feature review, squash, and cleanup audit | 0 | PR #111 remained ready, exact-head/exact-base, `MERGEABLE/CLEAN`, and three-check green after the delayed audit found zero reviews, issue comments, inline comments, or threads. Head-pinned GitHub-verified squash `66f9d84eea57c270e9b18326348eb1ea5c4ebfa4` has tree `b036b39f9244b18d43a7f56ac8b6d463915227bd` exactly equal to reviewed feature head `0b3eaad213a149fb96c138cd4eabc1d861d053e9`, sole parent M52 closeout `8d69f5b265277edb95ae47ea3a0af001217a4575`, and standalone DCO. No post-merge `main` run was allocated; the feature branch was deleted locally/remotely, and no tag or release was created. |
| Four-file integration-record local gate | 0 | Exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md` changed. The unchanged lock resolved; all 296 Python files were format clean; Ruff and strict Pyright reported zero findings; all 522 architecture assertions passed in 3.40 seconds; strict docs built in 1.00 seconds; and whitespace was clean. Two fresh builds reproduced a pure 270,186-byte wheel (`815202e5a5e458d755c1e292ea35b8765aa3e8103bd211a9e60a4fd588fdf748`) and 1,061,777-byte sdist (`71cd9de7fe770fade2fcaec314929879834dfd92437eca04d5cfedd9db77009c`); isolated-wheel and complete ten-artifact release smoke passed. This factual row changes the source archive, so the documentation-only hosted exact-head result will be authoritative. |
| Integration-record hosted gate | 0 | Exact head `de488d1e305026f724a155bf692653cd5f8cb454` passed run `31320201771`. Linux job `93261809439` completed in 36 seconds with 296-file formatting, lint, strict docs, all 522 architecture assertions in 6.02 seconds, reproducible build, isolated-wheel smoke, and complete release smoke. The pure 270,172-byte wheel was `055d7f53440dc3e758d5ffd6b490b9cd1dd2072cbbbdd10f2932f13601536be6`; the 1,061,851-byte sdist was `ddd32b19a4fbd1361b45d3f1e7a094f5df19c88579811c6d7beaf060fbfe2492`. Desktop umbrella job `93261877229` skipped with zero steps and no runner allocation. |
| Integration-record review, squash, and cleanup audit | 0 | PR #112 remained ready, exact-head/exact-base, `MERGEABLE/CLEAN`, and review-clean with no issue comment, inline comment, or thread. Head-pinned GitHub-verified squash `9217862df30d51efa7754cc8a9300c4b05fb2426` has tree `9c1ee15d87de8045b89eef2a600525299526fe03` exactly equal to reviewed record head `de488d1e305026f724a155bf692653cd5f8cb454`, sole parent feature squash `66f9d84eea57c270e9b18326348eb1ea5c4ebfa4`, and standalone DCO. No post-merge `main` run was allocated; both M53 working branches were deleted locally/remotely, and no tag or release was created. |
| Three-file closeout prepublication audit | 0 | Exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md` changed with clean whitespace. `main`, `origin/main`, and `origin/HEAD` resolve to verified integration squash `9217862df30d51efa7754cc8a9300c4b05fb2426`; only `main` and the intended local closeout branch exist, no remote feature/record branch or open pull request remains, no tag or release exists, and no post-integration `main` run was allocated. The `.project/**`-only closeout must allocate zero hosted runs or checks. |

Closeout publication evidence follows only after those operations actually
execute.

## M52 development evidence - 2026-08-09 to 2026-08-10, Windows, CPython 3.12-3.14

| Command or review | Exit | Result |
| --- | ---: | --- |
| M51 closeout audit | 0 | Exact synchronized `main`, `origin/main`, and `origin/HEAD` resolved to verified M51 closeout `047478d0c7fb873ae94aaa6e322b5b08903ed354`. Its tree exactly matched reviewed closeout head, its sole parent was the integration-record squash, GitHub reported a valid signature, and its message carried standalone DCO. No post-closeout `main` run, open PR, local/remote non-main branch, tag, or GitHub release existed; full Git-object checking passed. |
| Official Python 3.14.7 `ssl`/`http.client` and RFC 9525 review | 0 | Python documents that `check_hostname` requires a supplied `server_hostname`, that `SSLSocket.server_hostname` retains the expected name in IDNA A-label form, and that `getpeercert(binary_form=True)` returns the peer certificate as DER bytes. RFC 9525 defines the client reference identity and server-presented certificate relationship. RFC-0035 applies those portable surfaces without adding a certificate parser, pin registry, dependency, or external runtime. |
| First focused M47-M52 implementation gate | Corrected | Ruff formatted one new test and lint passed. Strict Pyright found one test-helper annotation that excluded an intentionally malformed `server_hostname` fixture; widening only that test parameter to `object` produced the corrected static result below. The behavioral command passed 116 assertions with six documentation guards intentionally deselected in 1.23 seconds; no type-check pass is claimed for this attempt. |
| Corrected focused Ruff/strict-Pyright gate | 0 | The verifier and six M47-M52 architecture files passed Ruff; strict Pyright reported zero errors, warnings, or information findings. |
| Corrected focused M47-M52 behavioral gate | 0 | All 116 selected inherited and service-identity assertions passed with six documentation guards intentionally deselected in 1.20 seconds. |
| Service-identity findings-first correction | Corrected | Review found that Unicode case-folding could make a non-ASCII observed hostname compare equal to an ASCII reference containing `k` or `s`. The verifier now requires the observed `server_hostname` to be ASCII before case-insensitive comparison; a case-fold-equivalent regression plus missing-accessor and invalid-IDNA cases were added. One combined attempt passed 125 behavioral assertions but Ruff rejected the intentionally visible confusable character; spelling it as a Unicode escape retained the runtime case and produced a clean focused Ruff/Pyright gate. The final M52-only focused suite passed 19 assertions in 0.91 seconds. |
| Preliminary whole-tree static, architecture, docs, and scope gate | 0 | The unchanged 46-package lock resolved in 0.92 ms; all 295 Python files were format clean; Ruff and strict Pyright reported zero findings; 503 architecture assertions passed in 3.47 seconds; strict docs built in 1.11 seconds; whitespace and full Git-object checking passed. Protected workflows, runtime source, benchmarks, metadata, and lock were unchanged, and changed hunks introduced no workflow-identity marker. A later invalid-IDNA regression requires the final architecture recount recorded below. |
| Preliminary complete supported-Python gate | 0 | The graphics-enabled candidate passed 2,043 tests with 14 expected skips on CPython 3.12.13 in 135.17 seconds, CPython 3.13.13 in 106.01 seconds, and CPython 3.14.5 in 111.53 seconds. A later invalid-IDNA regression changes the final exact-tree counts, so these remain development evidence rather than the final supported-Python gate. |
| First real-wgpu and profile attempt inside the restricted sandbox | Blocked | Five uv invocations could not initialize the configured external uv cache because access to `C:\Users\louij\AppData\Local\uv\cache\sdists-v9\.git` was denied. No blocked invocation is represented as passing; the approved rerun is recorded next. |
| Approved real-wgpu and three-repeat profile gate | 0 | Ten real-wgpu tests passed in 8.17 seconds. The two-workload base and three-workload graphics M7 profiles each ran three repeats and validated against `ludoweave.profile.m7/1`. |
| Vertical-slice and documented benchmark gate | 0 | Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced committed apply/adjust receipts, six query matches, five replay batches, passing tests, and its established state/capture identities. M1 validated seven workloads with one of two recorded targets observed; M2 validated four target-free informational workloads; M3 validated six workloads with zero of two observed targets met; M4 validated three workloads with its baseline target observed. |
| Pre-record reproducible distribution and release gate | 0 | Two fresh builds reproduced a 269,970-byte wheel (`0b225a11e59c265389594f2bebcb7b169c15f85d2c201b0db40278cc256dacf2`) and 1,050,704-byte sdist (`a3b4094e95eb2529222c265e02c6ecf1da6f53c4673a1e978dd95566f168a6cb`). Isolated-wheel smoke, ten-artifact staging, and complete release smoke passed for `0.1.0a1`. The later regression and factual record change the sdist, so exact feature-head identities remain delegated to final local/hosted evidence. |
| Final recorded-tree static, architecture, documentation, and scope gate | 0 | The unchanged 46-package lock resolved in 0.98 ms; all 295 Python files were format clean; Ruff and strict Pyright reported zero findings; 504 architecture assertions passed in 3.57 seconds; strict docs built in 1.17 seconds; protected-path, whitespace, and full Git-object checks passed. A first orchestration wrapper was rejected by its JavaScript parser before any repository command ran; the simpler rerun produced the recorded project results. |
| Final recorded-tree CPython 3.12 graphics gate | 0 | CPython 3.12.13 passed 2,044 tests with 14 expected skips in 110.39 seconds. |
| Final recorded-tree CPython 3.13 graphics gate | 0 | CPython 3.13.13 recreated the environment and passed 2,044 tests with 14 expected skips in 110.90 seconds. |
| Final recorded-tree CPython 3.14 graphics gate | 0 | CPython 3.14.5 recreated the environment and passed 2,044 tests with 14 expected skips in 108.85 seconds. |
| First record-inclusive distribution build inside the restricted sandbox | Blocked | The first build could not initialize the configured external uv cache because access to `C:\Users\louij\AppData\Local\uv\cache\sdists-v9\.git` was denied. No distribution command ran to completion and no pass is claimed for this attempt; the approved cache-access build and independent repeat are recorded next. |
| Record-inclusive reproducible distribution, wheel, and release gate | 0 | Two fresh confirmed-absent output directories matched byte-for-byte: the pure 269,970-byte wheel SHA-256 was `0b225a11e59c265389594f2bebcb7b169c15f85d2c201b0db40278cc256dacf2`, and the 1,051,820-byte source distribution SHA-256 was `44f92999e63bbc5a58826db4371dd08ad9b4235cda61c74e21aa0b231ec220aa`. Isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed for `0.1.0a1`. This factual row changes the source archive afterward, so hosted exact-head build evidence remains authoritative rather than the pre-row sdist hash. |
| Final findings-first IDNA-order correction | Corrected | Review found that the invalid-IDNA regression supplied a preconnected fake socket, whereas a real `HTTPSConnection` could attempt its own IDNA conversion during connect and classify the malformed value outside M52's stable TLS boundary. The corrected verifier derives the ASCII reference hostname before connection construction and uses it for that hop; comparison against the actual socket and certificate observation remain after connected-peer confinement. The earlier full and artifact gates remain truthful development evidence but do not validate this correction; corrected focused and final gates follow. |
| Corrected focused M47-M52 and documentation gate | 0 | Ruff and strict Pyright reported zero findings for the corrected verifier and M52 regression file; all 126 focused inherited and M52 behavior assertions passed in 1.42 seconds; strict docs built in 1.06 seconds with only the known upstream notice. |
| Corrected complete supported-Python gate | 0 | The corrected graphics-enabled candidate passed 2,044 tests with 14 expected skips on CPython 3.12.13 in 104.30 seconds, CPython 3.13.13 in 102.38 seconds, and CPython 3.14.5 in 109.80 seconds. |
| Corrected reproducible distribution, wheel, and release gate | 0 | Two new confirmed-absent build directories reproduced the pure 269,970-byte wheel at `0b225a11e59c265389594f2bebcb7b169c15f85d2c201b0db40278cc256dacf2` and the 1,052,840-byte source distribution at `fb77adbe15a3934e00eac20eed48f33d47ed5fe53cbe67c5eb6d436114c93e67`. Corrected isolated-wheel smoke, fresh ten-artifact staging, and complete release smoke passed for `0.1.0a1`. This factual row changes the source archive afterward, so hosted exact-head build evidence remains authoritative rather than the pre-row sdist hash. |
| Corrected post-record static, architecture, documentation, and integrity gate | 0 | The unchanged 46-package lock resolved in 0.89 ms; all 295 Python files were format clean; Ruff and strict Pyright reported zero findings; all 504 architecture assertions passed in 5.05 seconds; strict docs built in 1.08 seconds with only the known upstream notice; whitespace and full Git-object checking passed. |
| Final findings-first scope, security, archive, and disclosure review | 0 | Review first identified and corrected the real-connection IDNA ordering gap above. Repeat review found no remaining blocking or non-blocking finding across correctness, failure mapping, ordering, ownership, redirect independence, tests, architecture, documentation, or compatibility. Changed hunks and both new files contained no workflow-identity marker or credential pattern; workflow, metadata, lock, runtime package, and benchmark paths were unchanged; executable/test changes introduced no wgpu, GLFW, NumPy, native, subprocess, or dynamic-evaluation dependency. The corrected wheel and sdist contained no `[retired control directory]`, `[retired control directory]`, `[retired control directory]`, `[retired control file]`, native-library, WASM, or bytecode payload. |
| Hosted exact-head feature gate | 0 | Ready PR #108 exact head `170db846112e27b9d11377da69784c69a6565bb4` passed run `31316474864` in exactly three Linux-first allocations: Linux `93252443745` passed in 7m02s, then macOS `93253220602` passed in 2m16s and Windows `93253220599` in 3m59s. Linux baseline passed 2,048 tests; Ubuntu CPython 3.13/3.14 and both desktop CPython 3.14 suites each passed 2,048 tests with one expected skip. Every platform passed ten real-graphics tests, profile smoke, Clockwork Arena, and Agent World Builder. Hosted reproducibility passed for a 269,957-byte wheel (`0bbdcc263fa1b28b7c0b8e29559b45b47df28b7d61a43eb23feb941d6e1e3386`) and 1,053,252-byte sdist (`ec58993d27bdfdfe06f16bd963651fb68cd04c842a50649f1e8ed675f1af4581`); installed-wheel and complete ten-artifact release smoke passed. |
| Feature review, squash, and cleanup audit | 0 | PR #108 remained ready, exact-head/exact-base, `MERGEABLE/CLEAN`, and three-check green after a delayed audit found zero reviews, issue comments, inline comments, or threads. Head-pinned GitHub-verified squash `eb083089bfff774c0df2b115428901357c9084b2` has tree `ab92b60f4e05faccc2b0059d3d9cfad6b0e0eaef` exactly equal to reviewed feature head `170db846112e27b9d11377da69784c69a6565bb4`, sole parent M51 closeout `047478d0c7fb873ae94aaa6e322b5b08903ed354`, and standalone DCO. No post-merge `main` run was allocated; the feature branch was deleted locally/remotely, and no tag or release was created. |
| Four-file integration-record local gate | 0 | Exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md` changed. The unchanged lock resolved; all 295 Python files were format clean; Ruff and strict Pyright reported zero findings; all 504 architecture assertions passed in 3.65 seconds; strict docs built in 1.06 seconds; and whitespace was clean. Two fresh builds reproduced a 269,970-byte wheel (`0b225a11e59c265389594f2bebcb7b169c15f85d2c201b0db40278cc256dacf2`) and 1,054,384-byte sdist (`457aa72b9b515fcf2e8d70b6ab588ac9f7926da9adcd2342b571d30ae3a4f5f1`); isolated-wheel and complete ten-artifact release smoke passed. This factual row changes the source archive, so the documentation-only hosted exact-head result remains authoritative. |
| Integration-record hosted gate and review correction | Corrected | Initial PR #109 head `92427931151106f7b1ce9c77c4809bf794d1f7f9` passed run `31317421319` in one 41-second Linux allocation: 295-file formatting and Ruff passed, strict docs built in 1.44 seconds, all 504 documentation architecture assertions passed in 5.65 seconds, byte-identical distributions passed, and wheel/release smoke passed. The 269,957-byte wheel was `0bbdcc263fa1b28b7c0b8e29559b45b47df28b7d61a43eb23feb941d6e1e3386`; the 1,054,460-byte sdist was `c64b433c21e6878226469175fe8133a87b0716b324d9351cce4c5b5b07768d98`. Desktop umbrella job `93254887616` skipped with zero steps. External review then found that an earlier M52 summary still called final review and hosted gates pending despite the exact evidence below it. The stale sentence is removed; this otherwise-green head will not be merged, and corrected hosted evidence follows only after it executes. |
| Corrected integration-record hosted gate | 0 | Exact head `6e36c1a77e5ca9c1ca50b272c184fab63495299c` passed run `31317666409`. Linux job `93255421358` completed in 42 seconds with 295-file formatting, lint, strict docs, 504 documentation architecture assertions in 5.99 seconds, reproducible build, isolated-wheel smoke, and complete release smoke. The reproducible 269,957-byte wheel was `0bbdcc263fa1b28b7c0b8e29559b45b47df28b7d61a43eb23feb941d6e1e3386`; the 1,055,033-byte sdist was `ca9a361a96c899eff198421fc8fc015385011b0ac89110ccdd35a3d629c357de`. Desktop umbrella job `93255511671` skipped with zero steps and no runner allocation. |
| Integration-record review, squash, and cleanup audit | 0 | The one actionable PR #109 thread is resolved after the cited contradiction was removed; no issue comment or unresolved thread remains. The PR was ready, `MERGEABLE/CLEAN`, and exact-head/exact-base with its Linux check successful and zero-step umbrella skipped. Head-pinned GitHub-verified squash `cd697ef150861c405b9e104db009a15a9db78e47` has tree `0dd8456b491f5a8f783407b1c2f237a0e7604407` exactly equal to corrected record head `6e36c1a77e5ca9c1ca50b272c184fab63495299c`, sole parent feature squash `eb083089bfff774c0df2b115428901357c9084b2`, a valid GitHub signature, and standalone DCO. No post-merge `main` run was allocated; both M52 branches were deleted locally/remotely, and no tag or release was created. |
| Three-file closeout prepublication audit | 0 | Exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md` changed with clean whitespace. `main`, `origin/main`, and `origin/HEAD` all resolved to verified integration squash `cd697ef150861c405b9e104db009a15a9db78e47`; only `main` and the intended local closeout branch existed, no remote feature/record branch or open pull request remained, no tag or GitHub release existed, no post-integration `main` run was allocated, and full Git-object checking passed. The `.project/**`-only closeout must allocate zero hosted runs or checks. |

Closeout publication evidence follows only after those commands and reviews
actually complete.

## M51 development evidence - 2026-08-09, Windows, CPython 3.12-3.14

| Command or review | Exit | Result |
| --- | ---: | --- |
| Official Python 3.14.7 `ssl` and `http.client` documentation review | 0 | Confirmed the actual negotiated semantics of `SSLSocket.version()`, `cipher()`, `compression()`, and `selected_alpn_protocol()`, and that a custom `HTTPSConnection` context owns its ALPN advertisement. RFC-0034 applies those documented surfaces without adding a foreign registry or external runtime dependency. |
| Initial focused Ruff/strict-Pyright/M45-M51 gate | 0 | Ruff formatting/lint and strict Pyright passed; 109 focused assertions passed in 1.18 seconds. A subsequent review added `NotImplementedError` to the session-accessor failure boundary, so this is development evidence rather than final-tree evidence. |
| Corrected focused/docs command using nonexistent `tests/architecture/test_m45_public_release_consumer.py` | Corrected | Ruff and strict Pyright passed and strict docs built in 1.02 seconds, but pytest reported the mistyped path and ran zero tests. The corrected command below is the behavioral evidence. |
| Corrected focused M45/M47-M51 pytest command using `test_m45_public_release_consumer_integrity.py` | 0 | 110 assertions passed in 1.10 seconds after the defensive exception correction and documentation alignment. |
| First complete static/architecture gate inside the restricted sandbox | Blocked | Seven uv commands could not initialize the configured external uv cache because access to `C:\Users\louij\AppData\Local\uv\cache\sdists-v9\.git` was denied. No blocked uv command is represented as passing; the approved rerun is recorded next. |
| Approved `uv lock --check`; graphics sync; repository format/lint; strict Pyright; architecture; strict docs; `git diff --check` | 0 | Lock resolved, 45 packages checked, 294 files format clean, Ruff and strict Pyright reported zero findings, 482 architecture assertions passed in 2.88 seconds, strict docs built in 0.98 seconds, and diff whitespace validation passed. This preceded the final ALPN behavior assertion. |
| `uv run --frozen --python 3.12 --extra graphics pytest -q` | 0 | 2,022 tests passed with 14 expected skips in 105.00 seconds. |
| `uv run --frozen --python 3.13 --extra graphics pytest -q` | 0 | CPython 3.13.13 recreated the environment; 2,022 tests passed with 14 expected skips in 104.30 seconds. |
| `uv run --frozen --python 3.14 --extra graphics pytest -q` | 0 | CPython 3.14.5 recreated the environment; 2,022 tests passed with 14 expected skips in 108.88 seconds. |
| Real-wgpu, three-repeat base/graphics profiles, Clockwork Arena, and Agent World Builder | 0 | Ten real-wgpu tests passed in 7.43 seconds; both profile contracts validated; the 30-tick arena produced state hash `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`; Agent World Builder reported committed apply/adjust receipts, six query matches, valid replay, and passing tests. |
| First repeat-build, isolated-wheel, release-stage, and release-smoke gate | 0 | Reproducibility passed for a 269,742-byte wheel (`f39f742ec64debc3943b67636299c77318dc8c500bda70b69a2c87908bb691bb`) and 1,038,637-byte sdist (`887005824abbfb80fd12c06d9d84e07e72e31f703636cbbdf16fcb4b3773e7ce`); isolated wheel and ten-artifact release smoke passed. A later test/documentation addition changes the sdist, so final-tree artifact identities are recorded separately below. |
| Documented M1-M4 benchmark/validation commands | 0 | All four benchmark documents validated. M1 recorded seven workloads with one currently observed target of two recorded; M2 validated four informational workloads without timing targets; M3 validated six workloads with two observed targets and no target claim; M4 validated three workloads with the baseline target observed. Timings remain local dirty-tree observations, not regression or support claims. |
| Corrected ALPN behavior-focused Ruff/strict-Pyright/M45-M51 gate | 0 | A behavioral fake-context assertion proves the exact one-element `http/1.1` advertisement. Ruff and strict Pyright passed; 111 focused assertions passed in 1.64 seconds. |
| Final-tree static, architecture, documentation, whitespace, and credential-pattern gate | 0 | Lock and 45-package sync checks passed; all 294 files were format clean; Ruff and strict Pyright reported zero findings; 483 architecture assertions passed in 3.02 seconds; strict docs built in 1.02 seconds; `git diff --check` passed. The only credential-pattern search hit was the pre-existing `Authorization:` negative-test literal in `test_m46_fresh_runner_consumer_rehearsal.py`; no new credential material was found. |
| Final-tree `uv run --frozen --python 3.12 --extra graphics pytest -q` | 0 | 2,023 tests passed with 14 expected skips in 106.87 seconds. |
| Final-tree `uv run --frozen --python 3.13 --extra graphics pytest -q` | 0 | CPython 3.13.13 recreated the environment; 2,023 tests passed with 14 expected skips in 105.26 seconds. |
| Final-tree `uv run --frozen --python 3.14 --extra graphics pytest -q` | 0 | CPython 3.14.5 recreated the environment; 2,023 tests passed with 14 expected skips in 111.42 seconds. |
| Candidate-tree repeat-build, isolated-wheel, release-stage, and release-smoke gate | 0 | Immediately before this factual evidence row was added, reproducibility passed for the 269,742-byte pure wheel (`f39f742ec64debc3943b67636299c77318dc8c500bda70b69a2c87908bb691bb`) and 1,040,772-byte sdist (`31bda1c14ab0ca37979ecf2835b2853a04be1dd5f94b0e50f9b3452f9b1c3cf4`). Isolated wheel smoke, ten-artifact release staging, and complete release smoke passed for `0.1.0a1`. Because this evidence file is intentionally included in the sdist, exact feature-head artifact identities are deferred to hosted pull-request evidence rather than represented by the pre-record sdist hash. |
| First post-record static gate after isolated-wheel smoke | Corrected | Formatting and Ruff passed; 483 architecture assertions and strict docs passed, but strict Pyright reported 17 missing/unknown optional-wgpu diagnostics because isolated-wheel smoke had intentionally recreated `.venv` without the graphics extra. This environment-dependent attempt is not represented as a type-check pass. |
| Corrected `uv sync --frozen --all-groups --extra graphics`; format/lint; strict Pyright; architecture; strict docs; `git diff --check` | 0 | Restored six locked graphics packages; all 294 files were format clean; Ruff and strict Pyright reported zero findings; 483 architecture assertions passed in 3.24 seconds; strict docs built in 1.06 seconds; diff whitespace validation passed. |
| PR #105 initial exact-head hosted gate and pre-merge review | Corrected | Initial head `cdd3cc8fd943861072efafed593462fac7ffc3f4` passed run `31312040824` in exactly three Linux-first allocations: Linux `93241207399` in 7m42s, macOS `93242025688` in 1m52s, and Windows `93242025672` in 3m41s. Linux baseline passed 2,027 tests; Ubuntu 3.13/3.14 and each desktop 3.14 suite passed 2,027 with one expected skip; every platform passed ten graphics tests, profile smoke, Clockwork Arena, and Agent World Builder. Hosted reproducibility passed for a 269,728-byte wheel (`9539b42da0143fb893e107eeb554dfe0229125439627f361b3b7507b9f3df989`) and 1,041,121-byte sdist (`73985ddca3423828e28ca21bbe716aacbf5dff4be0c58a51c3b65a349530ce6a`). Pre-merge review then found that an unhashable malformed version value could escape through set membership, so this otherwise-green head is not accepted or merged. |
| Review correction focused and architecture gate | 0 | The version is now required to be a string before allowed-set membership. Sequence and mapping regression cases were added; Ruff and strict Pyright passed, 113 focused M45/M47-M51 assertions passed in 1.21 seconds, and 485 architecture assertions passed in 2.99 seconds. |
| Corrected-candidate `uv run --frozen --python 3.12 --extra graphics pytest -q` | 0 | 2,025 tests passed with 14 expected skips in 106.83 seconds. |
| Corrected-candidate `uv run --frozen --python 3.13 --extra graphics pytest -q` | 0 | CPython 3.13.13 recreated the environment; 2,025 tests passed with 14 expected skips in 117.17 seconds. |
| Corrected-candidate `uv run --frozen --python 3.14 --extra graphics pytest -q` | 0 | CPython 3.14.5 recreated the environment; 2,025 tests passed with 14 expected skips in 112.22 seconds. |
| Corrected-candidate real-wgpu, three-repeat profiles, vertical slices, and static/docs gate | 0 | Ten real-wgpu tests passed in 7.26 seconds; both base and graphics profile contracts validated; Clockwork Arena retained its deterministic state hash; Agent World Builder retained committed receipts, six query matches, valid replay, and passing tests. All 294 files were format clean; Ruff and strict Pyright reported zero findings; strict docs built in 1.03 seconds; diff whitespace validation passed. |
| Corrected-candidate repeat-build, isolated-wheel, release-stage, and release-smoke gate | 0 | Immediately before this factual row was added, reproducibility passed for a 269,742-byte pure wheel (`f39f742ec64debc3943b67636299c77318dc8c500bda70b69a2c87908bb691bb`) and 1,041,876-byte sdist (`e6e0568efbb3316730f5f467f6a1876f55ab7a3e257635773fc9b9dd4a1cd27e`). Isolated-wheel smoke, ten-artifact staging, and complete release smoke passed for `0.1.0a1`. Exact corrected-head artifact identities remain delegated to hosted evidence because this record is packaged in the sdist. |
| Corrected-head PR #105 hosted gate | 0 | Exact head `a0612236aa13c2892fd95e55c2a77286d21572d4` passed run `31312987430` in exactly three Linux-first allocations: Linux `93243602979` in 7m16s, macOS `93244384980` in 2m02s, and Windows `93244384979` in 3m55s. Linux baseline passed 2,029 tests; Ubuntu 3.13/3.14 and each desktop 3.14 suite passed 2,029 with one expected skip. All platforms passed ten graphics tests, profile smoke, Clockwork Arena, and Agent World Builder. Reproducibility passed for the 269,728-byte wheel (`9539b42da0143fb893e107eeb554dfe0229125439627f361b3b7507b9f3df989`) and 1,041,948-byte sdist (`27c0604758c1d9eb391bf26a093c9c5f85396e33a6a84e4af49004bf0f1bbc5f`); installed-wheel and complete release smoke passed. |
| PR #105 review resolution and exact-tree squash audit | 0 | The initial review contributed one actionable review comment/thread and no issue comment. The corrected head made it outdated; explicit string guarding plus sequence/mapping regressions passed locally and hosted, after which the sole thread was resolved. The PR was `MERGEABLE/CLEAN` with exact corrected head/base and three successful checks. Head-pinned squash `ce4184b4ecedd9163a654cc96ae6c96086683760` has tree `c331ea93e5332b47a3df20906dfb6f6e77c6cdb3` exactly equal to corrected head `a0612236aa13c2892fd95e55c2a77286d21572d4`, sole parent M50 closeout `53f3804010f1556ecaff21a61b1e9c405a26e203`, a valid GitHub signature, and standalone DCO. A PowerShell-mangled `HEAD^{tree}` preflight token failed before the merge command, so the tree was rechecked successfully with `git show --format=%T` and `git diff --exit-code`; no post-merge `main` run was allocated. The feature branch was deleted locally/remotely. |
| Four-file integration-record local gate | 0 | Lock, formatting, Ruff, whitespace, 485 architecture assertions in 3.22 seconds, and strict docs in 1.01 seconds passed. Immediately before this factual row was added, two builds reproduced a 269,742-byte wheel (`f39f742ec64debc3943b67636299c77318dc8c500bda70b69a2c87908bb691bb`) and 1,043,170-byte sdist (`b78d827cd1319c8209611cdaffcec86fe97ca706a59300b99a116fb4fdfe4a3f`); installed-wheel and complete release smoke passed. Exact integration-head artifact identities remain delegated to hosted evidence because this record is packaged in the sdist. |
| Integration-record review correction | Corrected | Initial PR #106 head `bea144e9d0444237c08a3be6a56905f6d66b2c65` passed docs-only run `31313663654` in one Linux allocation: job `93245316725` passed in 37 seconds with 485 architecture assertions, reproducible build, isolated-wheel smoke, and complete release smoke; desktop umbrella `93245398574` skipped with zero steps. Review then found one stale sentence still claiming exact-head hosted validation was pending. The sentence was corrected; the initial otherwise-green head was not merged. A restricted-cache `uv lock --check` attempt during correction was blocked before project validation; its approved cache-access rerun resolved the unchanged 46-package lock. Formatting, Ruff, whitespace, 485 architecture assertions in 3.15 seconds, and strict docs in 1.03 seconds passed on the corrected record. |
| Corrected integration-record hosted gate | 0 | Exact head `aa94d62a06d51f635a6dce1dcbfd686a8c0ac2dd` passed run `31313847857`. Linux job `93245782842` completed in 38 seconds with lock, format, lint, strict docs, 485 documentation architecture assertions in 5.17 seconds, reproducible build, isolated-wheel smoke, and complete release smoke. The reproducible 269,728-byte wheel was `9539b42da0143fb893e107eeb554dfe0229125439627f361b3b7507b9f3df989`; the 1,043,265-byte sdist was `5b66b95d6976c88943afccf1731ee359cd82e08b9bb0d46bb779b46fc3378b40`. Desktop umbrella job `93245857571` skipped with zero steps and no runner allocation. |
| Integration-record review, squash, and cleanup audit | 0 | The one actionable PR #106 thread is resolved after the cited contradiction was removed; there is no issue comment or unresolved thread. The PR was ready, `MERGEABLE/CLEAN`, and exact-head/exact-base with its Linux check successful and zero-step umbrella skipped. Head-pinned squash `d2cc5d630b15351289008976d192232cde184afc` has tree `706324da08b466e14f77fe34eb2f1cad727eecca` exactly equal to reviewed head `aa94d62a06d51f635a6dce1dcbfd686a8c0ac2dd`, sole parent feature squash `ce4184b4ecedd9163a654cc96ae6c96086683760`, a valid GitHub signature, and standalone DCO. No post-merge `main` run was allocated. Fetch pruned the deleted remote record branch; the verified local squash-source branch was deleted. Synchronized `main`, `origin/main`, and `origin/HEAD` resolve to the squash; no open PR, tag, or GitHub release exists and `git fsck --full --no-dangling` passes. |
| Closeout-record local gate | 0 | The unchanged lock resolved 46 packages in 0.89 ms; all 294 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 485 architecture assertions passed in 3.41 seconds; and strict docs built in 1.12 seconds with only the known upstream notice. Exactly three `.project/**` Markdown paths changed; protected workflows, metadata, lock, runtime source, public docs, and roadmap are unchanged. Whitespace and full Git-object checks passed, and the changed hunks introduce no repository-visible workflow-identity term. |

Closeout-record evidence follows only after those commands actually complete.

## M50 development evidence - 2026-08-09, Windows, CPython 3.12-3.14

| Command or check | Exit | Result |
| --- | ---: | --- |
| M49 closeout audit | 0 | Exact synchronized base `f6214992b02a9ef0bc44d6a9e4e6d72dc9d33de0` is the verified M49 closeout. Only `main` existed locally/remotely and the worktree was clean. No open pull request, tag, or GitHub release existed; the prior closeout had passed full Git-object validation. |
| Current TLS direction research | 0 | Python 3.14.7 documentation states that `create_default_context()` enables TLS key logging when `SSLKEYLOGFILE` is set, `keylog_filename` writes session secrets to an append-only debug file, `PROTOCOL_TLS_CLIENT` enables certificate/hostname verification, and `minimum_version` selects the lowest permitted TLS version. RFC-0033 adopts explicit verified per-hop contexts and rejects process-environment mutation, custom pins, and workflow expansion. |
| Initial ambient-keylog probe | Inconclusive | The first `uv run --frozen --python 3.12` attempt failed before Python execution because sandboxed uv-cache access was denied. The approved rerun emitted an OpenSSL uplink diagnostic rather than the expected Python fields and left a zero-byte controlled target. That probe is not represented as a passing behavioral result; the documented behavior and deterministic M50 regression test are the accepted evidence. |
| Initial focused implementation gate | Corrected | Ruff formatting/lint passed and 90 M45/M47-M50 assertions passed in 0.96 seconds. Strict Pyright reported two `keylog_filename` stub mismatches because the runtime accepts/returns `None` while the type surface declared `str`. Removing the redundant assignment and using a defensive `getattr` invariant produced zero Pyright diagnostics and five focused M50 passes in 0.22 seconds. |
| Documentation-integrated gate | Corrected | All 293 Python files passed formatting/Ruff and strict Pyright reported zero findings. Strict docs built in 1.00 seconds with only the known upstream Material notice. The focused suite passed 91 assertions and failed one exact wording guard because RFC-0033 said `not a real public release observation` rather than `no real public release observation`; aligning the guard to the actual explicit non-claim produced the complete architecture result below. |
| `uv run --frozen ruff format --check .`; `uv run --frozen ruff check .`; `uv run --frozen pyright`; `uv run --frozen pytest -q tests/architecture`; `uv run --frozen mkdocs build --strict`; `git diff --check` | 0 | All 293 Python files were formatted, Ruff and strict Pyright reported zero findings, all 464 architecture assertions passed in 2.85 seconds, strict docs built in 1.05 seconds with only the known upstream notice, and whitespace was clean. |
| Complete supported-Python gate | 0 | The exact graphics-enabled implementation tree passed 2,004 tests with 14 expected capability/platform skips on each supported interpreter: CPython 3.12.13 in 111.40 seconds, CPython 3.13.13 in 108.61 seconds, and CPython 3.14.5 in 117.52 seconds. The suites ran serially because the repository shares one temporary test root. |
| Real-wgpu, profiles, and vertical slices | 0 | After restoring the locked 45-package CPython 3.12.13 graphics environment, all ten real-wgpu tests passed in 7.62 seconds. Three-repeat two-workload base and three-workload graphics M7 profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, with registered tests and five replay batches passing. |
| `uv lock --check` and fresh-output preflight | Corrected | The lock resolved successfully. An unrelated system `python -c` preflight could not execute because the Windows App Execution Alias is unusable; no Python result is claimed. The corrected PowerShell `Test-Path -LiteralPath` preflight confirmed both build directories and the release-candidate directory were absent. |
| Reproducible distribution, wheel, and release smoke | 0 | Two fresh builds matched byte-for-byte: the 269,516-byte universal wheel SHA-256 was `1ef5f7b95dfa2b41481ddce561652e2d51af0408416ab542cc0e1b2fafb01aaf`, and the 1,029,477-byte source distribution SHA-256 was `7df8892460c8dfbf48d5c62fd973810110d48ffbb683d9727634607951718bec`. Isolated-wheel smoke and a fresh ten-artifact release candidate passed complete smoke. The wheel had 94 entries and no script, test, benchmark, native-library, or WASM payload. Factual records change afterward, so the source digest is not represented as final commit identity; hosted exact-head build evidence remains required. |
| Findings-first local review | 0 | The complete source/test/RFC diff and changed-path list were reviewed. Protected workflow, runtime package, benchmarks, pyproject, and lock diffs were empty. Added-content scanning found no credential/private-key pattern, disallowed identity marker, or absolute user path. The explicit context is created independently per hop before connection ownership, retains system trust and M48/M49 ordering, and maps failure content-silently. `git diff --check` passed; full Git-object checking found only existing unreachable objects and no corruption. No actionable finding remained. |
| Record-inclusive final local gate | 0 | The unchanged 46-package lock resolved in 0.77 ms and the 45-package CPython 3.12 graphics environment checked in 2 ms. All 293 Python files remained formatted; Ruff and strict Pyright reported zero findings; all 464 architecture assertions passed in 3.24 seconds; strict docs built in 0.98 seconds with only the known upstream notice; whitespace and full Git-object checking passed. Two fresh record-inclusive builds matched: the 269,516-byte wheel remained `1ef5f7b95dfa2b41481ddce561652e2d51af0408416ab542cc0e1b2fafb01aaf` and the 1,031,617-byte sdist was `bc3d7a984fbfec37d111668612aeee7b553a6b712fa2c561614e6bf4c14302af`; isolated-wheel and complete release smoke passed, and the 94-entry wheel remained payload-clean. This factual row changes the source archive, so hosted exact-head build evidence remains authoritative. |
| Hosted exact-head gate | 0 | Ready PR #102 exact head `99134b6be68bb7978431710228e788250561659e` and exact M49-closeout base passed run `31309759226` in exactly three allocations. Linux `93235618328` passed in 7m43s before macOS `93236421634` and Windows `93236421636` began; they passed in 2m08s and 3m01s. Linux baseline passed 2,008 tests; Ubuntu 3.13/3.14 and both desktop 3.14 suites each passed 2,008 with one expected skip. All platforms passed ten graphics tests, profiles, Clockwork Arena, and Agent World Builder. Reproducible hosted artifacts were a 269,502-byte wheel at `64a76ea20168da3a0e5411470964277b0c920d181ba6100c271a34fe52880898` and a 1,031,790-byte sdist at `2aeaaf28921965d122633dad7f10ec3b07f70e562b26c289307d97ef0f0939da`; isolated-wheel and complete ten-artifact release smoke passed. |
| Hosted review and squash audit | Corrected | PR #102 was `MERGEABLE/CLEAN` with three successful checks and zero submitted reviews, issue comments, review comments, or review threads. An initial literal GraphQL query was mangled by PowerShell and returned a malformed-number error; the corrected typed-variable query returned exactly zero threads. GitHub-verified squash `5fb56120e1a96a0a25db96baa3836699e435611c` has reviewed tree `2ec52b638069d23aabd68af04f3ada426aab803d`, sole parent M49 closeout `f6214992b02a9ef0bc44d6a9e4e6d72dc9d33de0`, and standalone DCO. No post-merge `main` run was allocated. The explicit remote-delete command reported the ref already absent because GitHub had deleted it; pruning removed the stale remote-tracking ref. Only synchronized `main` remains locally/remotely, with healthy Git objects and no real tag or release. |
| Integration-record local gate | 0 | The four-Markdown record changed only `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md`. The lock resolved; all 293 Python files passed formatting/Ruff; strict Pyright had zero findings; all 464 architecture assertions passed in 2.93 seconds; strict docs built in 0.97 seconds with only the known upstream notice; and whitespace was clean. Two fresh distributions matched: the 269,516-byte wheel remained `1ef5f7b95dfa2b41481ddce561652e2d51af0408416ab542cc0e1b2fafb01aaf` and the 1,033,001-byte sdist was `bf9d85fe369581e757f2d31b606c17f393fdc46a7c2a92c4da0331e7bf1d4f16`; isolated-wheel and complete ten-artifact release smoke passed. This row changes the source archive, so the documentation-only hosted exact-head result remains authoritative. |
| Integration-record hosted gate | 0 | PR #103 exact head `7441e9fae142a67a9d30075ac4c28127978cc750` changed exactly four Markdown files and classified `documentation`. Run `31310482277` passed in one 40-second Linux allocation: 293-file formatting/Ruff passed, strict docs built in 1.46 seconds, all 464 architecture assertions passed in 5.10 seconds, byte-identical distributions passed, and wheel/release smoke passed. The desktop umbrella job `93237511223` had exactly zero steps and was skipped. Hosted artifacts were the unchanged 269,502-byte wheel at `64a76ea20168da3a0e5411470964277b0c920d181ba6100c271a34fe52880898` and a 1,033,178-byte sdist at `9fdd1e02e858ec09c981d9024fc13e221c98e11247d48068bfa65ca433564855`. |
| Integration-record review and squash audit | 0 | PR #103 was `MERGEABLE/CLEAN` with exact M50-feature base/head and zero submitted reviews, issue comments, review comments, or review threads. GitHub-verified squash `7764ea32645c3455fb08bfbd5a3c4e2d8cabbd47` has tree `d2ea7fe46d4a807c17f896ba0cfaa87e2f499a44` exactly equal to the reviewed head, sole parent feature squash `5fb56120e1a96a0a25db96baa3836699e435611c`, and standalone DCO. No post-merge `main` run was allocated; the branch was deleted locally/remotely and only synchronized `main` remained. |
| Closeout-record local gate | 0 | The exact diff contained only `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md`. The unchanged lock resolved in 0.80 ms; all 293 Python files passed formatting/Ruff; strict Pyright reported zero findings; all 464 architecture assertions passed in 2.78 seconds; strict docs built in 0.95 seconds with only the known upstream notice; whitespace and full Git-object checking passed. The closeout must allocate zero hosted runs/checks. |

## M49 development evidence - 2026-08-09, Windows, CPython 3.12

| Command or check | Exit | Result |
| --- | ---: | --- |
| M48 closeout audit | 0 | Zero-run PR #97 exact head `e414e61d65351f72acd408c887845e6bd4a97155` had exact M48-record base, zero run/check/review/comment/thread, and only three `.project/**` files. Squash/current M49 base `049cdbcf2769a1c2359593f642e37697d5bf7400` has sole parent M48 record squash `ee98b591abb8e8ecd37b8fa32c01acb0ce279b52`, tree `3ea3e76c4dc0b5b310df557ba92ca8ab215e18c6` exactly equal to the reviewed head, valid GitHub signature, and standalone DCO. No post-merge run was allocated; the branch was deleted locally/remotely. Only synchronized `main` remained, with no open PR, tag, or release and healthy Git objects. |
| Current peer-confinement direction | 0 | Official GitHub documentation retains direct `200` or `302` asset delivery. Python documents `getpeername()` as the actual connected remote address and `ipaddress.is_global` against IANA special-purpose reachability. Current IANA IPv4/IPv6 registries distinguish globally reachable from private, shared, loopback, link-local, documentation, benchmarking, unspecified, multicast, and reserved space. The accepted M49 direction validates the actual connected peer before HTTP transmission rather than trusting a hostname allowlist or separate DNS result. |
| Initial focused implementation gate | Corrected | Ruff formatting/lint passed. Strict Pyright first reported one partially unknown socket-peer tuple and one incompatible test override; 69 non-documentation M47-M49 assertions still passed. After typing the peer tuple and replacing the override, the next Pyright run found one stale fixture constructor and four corresponding malformed-peer cases failed. Correcting that fixture produced zero Ruff/Pyright findings and 69 passes. Expanded redirect-hop and peer-discovery coverage then produced 74 passes with the three documentation assertions intentionally deselected in 0.79 seconds. |
| Supported-version classification probe | Corrected | Two initial probe forms produced Python `SyntaxError` because Windows native-argument processing removed embedded address-string quotes; neither is represented as a classification result. The corrected uv-managed CPython 3.12.13, 3.13.13, and 3.14.5 probes returned identical `is_global` values for `192.0.0.8`, `192.0.0.9`, `64:ff9b:1::1`, `2002::1`, `2001:1::1`, `2001:db8::1`, and private/public IPv4-mapped IPv6. Each interpreter selection recreated the local environment; the final graphics-enabled 3.12 environment must be restored before broader validation. |
| Documentation-integrated focused gate | 0 | The locked CPython 3.12.13 graphics environment was restored with all 45 packages in 3.07 seconds. All 292 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 83 M45/M47-M49 response, peer, workflow-boundary, and documentation assertions passed in 1.17 seconds; strict docs built in 1.03 seconds with only the known upstream notice. |
| Complete architecture gate | 0 | The unchanged 46-package lock resolved in 0.79 ms and all 455 architecture assertions passed in 2.97 seconds. |
| Complete supported-Python gate | 0 | The exact graphics-enabled M49 tree passed 1,995 tests with 14 expected platform/capability skips on each supported interpreter: CPython 3.12.13 in 108.80 seconds, CPython 3.13.13 in 103.50 seconds, and CPython 3.14.5 in 106.63 seconds. The suites ran serially because the repository intentionally shares one temporary root. |
| Real-wgpu, profiles, and vertical slices | 0 | The locked CPython 3.12.13 graphics environment was restored with 45 packages in 3.07 seconds. All ten real-wgpu tests passed in 6.80 seconds. Three-repeat two-workload base and three-workload graphics M7 profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, with registered tests and five replay batches passing. |
| Initial distribution exercise | Corrected | The first verifier invocation exited 1 with `distribution.invalid_directory` because it compares already-built directories rather than creating output paths; no artifact result is claimed from that invocation. The corrected sequence built twice into confirmed-absent directories and matched byte-for-byte: the 269,314-byte wheel SHA-256 was `dc914e6f5f93415ddee9cfae7deec7bf5c706fdc4b6a8f0cc9ba1e16bd59879b`, and the 1,021,038-byte sdist SHA-256 was `67ac093c9ed11fd9cf78bc1816800d2039b0185ab6ce3b33d58b732a2ce95bab`. Isolated-wheel smoke and complete ten-artifact release staging/smoke passed. Because factual records change afterward, these digests are not represented as final-tree distribution evidence. |
| Final static, architecture, docs, scope, and Git gate | 0 | The unchanged 46-package lock resolved in 0.70 ms; all 292 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 455 architecture assertions passed in 2.67 seconds; strict docs built in 0.94 seconds with only the known upstream notice; whitespace and full Git-object checking passed. No diff exists in either workflow, `src/ludoweave`, `benchmarks`, `pyproject.toml`, or `uv.lock`. CI, release-workflow, pyproject, and lock SHA-256 values remain `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`, `c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5`, `42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1`, and `e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed`. |
| Final pre-publication scope, credential, identity, and repository audit | 0 | Added-line plus untracked-file scanning found zero credential/private-key patterns, zero disallowed identity patterns, and zero absolute user paths. Protected diff count was zero. Only `main` existed remotely, with no open PR, remote tag, or GitHub release. Manual findings-first review confirmed actual-peer validation precedes every HTTP request, repeats per redirect, and preserves timeout/failure taxonomy and M48 bounds. A later hosted review found the additional classification defect recorded below. |
| Final commit-candidate distribution gate | Corrected | Two confirmed-absent build directories matched byte-for-byte: the 269,314-byte universal wheel SHA-256 is `dc914e6f5f93415ddee9cfae7deec7bf5c706fdc4b6a8f0cc9ba1e16bd59879b`, and the 1,021,493-byte source distribution SHA-256 is `5ccf040a7fba848f4e4e26abe7e477a080c55657cd5179cbd136936566c13999`. Isolated-wheel smoke and a fresh ten-artifact release candidate passed complete smoke. The first inventory command used unsupported PowerShell `Select-Object -Single`, so its zero-entry output is invalid and unclaimed; the corrected exact-one-wheel audit found 94 entries and zero verifier/test/native/WASM files. Only this factual record changes afterward, so no source-archive digest is represented as final commit identity; hosted exact-head build evidence remains required. |
| Final record-inclusive recheck | 0 | All 292 Python files remained formatted; Ruff and strict Pyright reported zero findings; all 455 architecture tests passed in 2.74 seconds; strict docs built in 1.02 seconds with only the known upstream notice; whitespace and full Git-object checking passed. Only factual evidence wording changes afterward; hosted exact-head validation remains the final immutable-tree evidence. |
| Initial hosted feature gate | Corrected | Ready PR #98 exact head `c19d37f24516bbdc8bea71b521936ac7daf1f8e9` passed run `31306631901` in exactly three allocations. Linux job `93227939522` passed in 438 seconds, then macOS `93228676707` passed in 151 seconds and Windows `93228676696` in 230 seconds. Linux passed 1,999 baseline tests; Ubuntu CPython 3.13/3.14 each passed 1,999 with one skip; both desktop CPython 3.14 suites passed 1,999 with one skip; all three platforms passed ten graphics tests, profiles, and both vertical slices. Reproducible artifacts were a 269,300-byte wheel at `4d0c8951410d181730ade2103b5c19720a568eee004169de10d86659377baa1c` and a 1,022,071-byte sdist at `10082f0303e048b104115cfb1b3826abee11d69152213e624df0152e2aa114bf`; wheel and release smoke passed. Hosted review found one valid unresolved defect, so this exact head is not mergeable evidence and PR #98 will be retired unmerged. |
| Hosted reserved-peer review correction | Corrected | Hosted review demonstrated that supported CPython can classify deprecated IPv6 site-local `fec0::1` and reserved `5f00::1` as global, allowing request transmission despite M49's explicit reserved-space boundary. The predicate now rejects `is_reserved` and IPv6 `is_site_local` in addition to its existing global, multicast, and unspecified checks. Both addresses are regression inputs. All 292 files remained formatted; Ruff and strict Pyright reported zero findings; all 31 focused M49 assertions passed in 0.65 seconds. |
| Corrected supported-Python gate | Corrected | An initial uv invocation failed before execution because sandboxed cache access was denied; rerunning with approved cache access succeeded. A later `uv sync --python 3.13` was followed by an unpinned `uv run` that selected repository-default CPython 3.12; that redundant run was interrupted and no 3.13 result is claimed from it. With interpreter selection explicitly pinned for both environment and test commands, the complete corrected tree passed 1,997 tests with 14 expected skips on CPython 3.12.13 in 103.73 seconds, CPython 3.13.13 in 102.18 seconds, and CPython 3.14.5 in 107.18 seconds. |
| Corrected real-wgpu, profiles, and vertical slices | 0 | The locked CPython 3.12.13 graphics environment was restored with all 45 packages in 3.10 seconds. All ten real-wgpu tests passed in 6.54 seconds. Three-repeat two-workload base and three-workload graphics profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, with registered tests and five replay batches passing. |
| Corrected distribution gate | Corrected | The first build attempt failed before artifact creation because sandboxed uv-cache access was denied. With approved cache access, two fresh build directories matched byte-for-byte: the 269,314-byte universal wheel SHA-256 was `dc914e6f5f93415ddee9cfae7deec7bf5c706fdc4b6a8f0cc9ba1e16bd59879b`, and the 1,023,301-byte source distribution SHA-256 was `3fc26ee78cb510db4fdaccad5fe38a1058378affaed3f88efc4732d197fab357`. Isolated-wheel smoke and a fresh ten-artifact release candidate passed complete smoke. Factual records change afterward, so this source digest is not represented as final commit identity; replacement hosted exact-head build evidence remains required. |
| Corrected final static, architecture, docs, and Git gate | 0 | All 292 Python files remained formatted; Ruff and strict Pyright reported zero findings; all 457 architecture assertions passed in 3.29 seconds; strict docs built in 1.05 seconds with only the known upstream notice; whitespace and full Git-object checking passed. Only this factual record and its aligned current-state count change afterward; replacement hosted exact-head validation remains the final immutable-tree evidence. |
| Corrected hosted feature and integration audit | 0 | Ready PR #99 exact head `01c955f0256c0c6e3a34afaf317c828e439b87ca` passed run `31307775820` in exactly three allocations: Linux `93230730827` in 422 seconds, macOS `93231457896` in 143 seconds, and Windows `93231457841` in 230 seconds. Linux passed 2,001 baseline tests; Ubuntu CPython 3.13/3.14 and both desktop CPython 3.14 suites each passed 2,001 with one skip. Every platform passed ten graphics tests, profiles, Clockwork Arena, and Agent World Builder. Reproducible artifacts were a 269,300-byte wheel at `4d0c8951410d181730ade2103b5c19720a568eee004169de10d86659377baa1c` and a 1,023,424-byte sdist at `ba42cc14a628a95ef928bd9fa7e974af61b2650fd18667b3a853cd9c9a1ef374`; wheel and release smoke passed. The PR was clean and mergeable at the exact head with zero review, issue comment, review comment, or thread. GitHub-verified squash `842aedc67a7ae4584821c4d8bc96a4ed8cb334c3` has exact reviewed tree `a9755cbf65dfeba5087f5037f73bc6027c408444`, sole parent M48 closeout `049cdbcf2769a1c2359593f642e37697d5bf7400`, and standalone DCO. No post-merge `main` run was allocated; the feature branch was deleted locally/remotely and only `main` remained remotely. No real tag or release was created. |
| Integration-record local gate | 0 | The four-Markdown integration record kept all 292 Python files formatted with zero Ruff/Pyright findings; all 457 architecture assertions passed in 2.75 seconds; strict docs built in 0.94 seconds with only the known upstream notice; whitespace and full Git-object checking passed. Two fresh build directories matched byte-for-byte: the 269,314-byte wheel SHA-256 was `dc914e6f5f93415ddee9cfae7deec7bf5c706fdc4b6a8f0cc9ba1e16bd59879b`, and the 1,024,351-byte sdist SHA-256 was `91093bd49195bacbce52daf229d60ad2f8e39994be65f433e6a0bbbf9dfa57d8`. Isolated-wheel and complete ten-artifact release smoke passed. This factual row changes afterward, so its source digest is not represented as final record-commit identity; hosted exact-head evidence remains required. |
| Integration-record hosted gate | 0 | PR #100 exact head `6d04bbf9f77382b5df3c4d1a7f5d0b70496751f9` changed exactly four Markdown files and classified `documentation`. Run `31308454299` passed in exactly one 31-second Linux allocation: 292-file formatting and Ruff passed, strict docs built in 0.98 seconds, all 457 architecture tests passed in 3.53 seconds, byte-identical distributions passed, and wheel/release smoke passed. Desktop umbrella job `93232491763` was skipped with exactly zero steps. Its 269,300-byte wheel hash remained `4d0c8951410d181730ade2103b5c19720a568eee004169de10d86659377baa1c`; the factual record changed the 1,024,432-byte sdist hash to `af12d5d53c4ddcff3c9d20cf7361bbeecdf211c02c137410cf73a9b9d697e2d6`. |
| Integration-record review and squash audit | 0 | PR #100 was `MERGEABLE`/`CLEAN` with exact M49-feature base, exact validated record head, and zero review, issue comment, review comment, or thread. Squash `d6ef4fef7f42a8bd961ea549eb3deb618a0c073f` has sole parent `842aedc67a7ae4584821c4d8bc96a4ed8cb334c3`, tree `55048621e219b915879736730011393b14caf49e` exactly equal to the reviewed head, GitHub verification `valid`, and standalone DCO. No post-merge `main` run was allocated; the record branch was deleted locally/remotely and local `main` was fast-forwarded exactly. |
| Closeout-record local gate | 0 | On the exact three-`.project/**` closeout tree, the unchanged lock, 292-file formatting, Ruff, strict Pyright, all 457 architecture assertions, strict docs, whitespace, and full Git-object checking passed. The diff contained only the current-task, project-state, and factual-evidence Markdown records. |

## M48 development evidence - 2026-08-09, Windows, CPython 3.12

| Command or check | Exit | Result |
| --- | ---: | --- |
| M47 closeout audit | 0 | Zero-run PR #94 exact head `dbe4c8bc0f71e039196130e136570ecb17b1c1ca` had exact M47-record base, zero run/check/review/comment/thread, and only three `.project/**` files. Squash/current M48 base `8d8d9e4a5790d7b74ec06139d314ffdf30a4ef41` has sole parent M47 record squash `7bea262210afd5b22265fede596d2d5117b14854`, tree `05654fc19bcadbd426966844c5ae6b54c279a4c9` exactly equal to the reviewed head, valid GitHub signature, and standalone DCO. No post-merge run was allocated; the branch was deleted locally/remotely. Only synchronized `main` remained, with no open PR, tag, or release and healthy Git objects. |
| Baseline hashes and response documentation | 0 | CI, release-workflow, pyproject, and lock SHA-256 values are `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`, `c2eea00debc2cdd742ac34075f1223d33820bb103708ad986637b6f1eefb60a5`, `42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1`, and `e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed`. Current official GitHub documentation lists `200` for Get a release and `200`/`302` for Get a release asset. Current Python documentation states that blocking socket timeouts raise `TimeoutError`, which is an `OSError`. |
| Initial focused code gate | Corrected | Formatting and Ruff passed; all 27 inherited M47 tests passed. The first strict Pyright command reported five test-call diagnostics because the local `_Download` protocol omitted the new explicit `maximum_redirects` parameter even though runtime calls passed it. After correcting that test-only protocol and focused lint assertions, strict Ruff/Pyright passed and all 45 non-documentation M47/M48 assertions passed in 0.56 seconds. Documentation assertions were intentionally deselected while docs were pending. |
| Documentation-integrated focus | Corrected | Strict Ruff/Pyright and strict docs passed. The first 47-test M47/M48 run exposed two exact documentation guards: the rewritten maintainer boundary no longer contained M47's literal `cross-platform`, and RFC-0031 did not contain the exact phrase `no release mutation`. After restoring those explicit claims, all 47 tests passed in 0.53 seconds and strict docs built in 1.01 seconds. A later direct-`200` release/asset regression brought the M45/M47/M48 focus to 54 passing tests in 1.11 seconds. |
| Architecture migration | Corrected | The first complete architecture run passed 424 assertions and failed one inherited M45 source guard that still expected `_MAX_REDIRECTS`; after advancing it to `_MAX_ASSET_REDIRECTS`, the next run exposed the old dictionary-literal API-header form. Updating only those exact guards produced six passing M45 tests and all 425 then-current architecture assertions in 2.61 seconds. The later direct-`200` regression remains for final exact-tree architecture validation. |
| Final supported-Python gate | 0 | After the direct-`200` regression, the exact graphics-enabled CPython 3.12, 3.13, and 3.14 trees each passed 1,966 tests with 14 expected platform/capability skips, in 105.37, 103.85, and 109.05 seconds respectively. |
| Real-wgpu, profiles, and vertical slices | 0 | All ten real-wgpu tests passed in 7.11 seconds. The two-workload base and three-workload graphics M7 profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, with registered tests and five replay batches passing. |
| Initial distribution exercise | 0 | Before the final direct-`200` regression and factual records, two fresh build directories matched exactly: the 269,075-byte wheel SHA-256 was `5e0ffbe62e5dcdb1d495fc3359fbc3fdead3b7559b7a56dca6dc5c55883647f0`, and the 1,011,774-byte sdist SHA-256 was `52a72d5099be14db3fbe000aadf6673581e70dbe286e7db7c1b320ee077e656a`. Isolated-wheel smoke and complete ten-artifact release staging/smoke passed. Because test and record files changed afterward, no digest from this run is represented as final-tree distribution evidence. |
| Final static, architecture, docs, and Git gate | 0 | Restoring the locked graphics-enabled CPython 3.12 environment installed 45 packages in 6.72 seconds; the unchanged 46-package lock resolved in 1 ms. All 291 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 426 architecture assertions passed in 3.86 seconds; strict docs built in 0.99 seconds with only the known upstream notice; whitespace and full Git-object checking passed. |
| Final commit-candidate distribution gate | 0 | Two confirmed-absent build directories matched byte-for-byte: the 269,075-byte universal wheel SHA-256 is `5e0ffbe62e5dcdb1d495fc3359fbc3fdead3b7559b7a56dca6dc5c55883647f0`, and the 1,012,603-byte source distribution SHA-256 is `dfd1e1f70f7dca46ec1d3fcd8b88de0cbfc2b211f42b5e5dce84d4624f9aab11`. Isolated-wheel smoke passed; a fresh ten-artifact release candidate passed complete release smoke. Only this factual record changes afterward, so no source-archive digest is represented as the final commit identity; hosted exact-head build evidence remains required. |
| Hosted exact-head gate | 0 | Pull-request run `31288303182` classified 17 changed files as substantive and used exactly three allocations at head `9b5c533d1e73ee985945fa0feb7e876417ee0126`. Linux qualified first in 415 seconds, macOS then passed in 118 seconds, and Windows passed in 228 seconds; every job and non-skipped step succeeded. Linux reported zero Ruff/Pyright findings, strict docs, 1,970 baseline tests, ten graphics tests, both profiles/vertical slices, reproducible distributions, wheel/release smoke, and 1,970 tests with one skip on each of CPython 3.13 and 3.14. macOS and Windows each passed ten graphics tests, both vertical slices/profiles, and 1,970 CPython 3.14 tests with one skip. Run artifact hashes are the 269,062-byte wheel `3c7abfb19c6e1d4e82d63e69e513ff9fdbe2808c90fe74938bef57d3218a93ef` and 1,012,713-byte sdist `bc4c132512ce4e91232d4dc6be4075481763b616685308a18a603610679a919a`. |
| PR review and squash audit | 0 | Ready PR #95 had exact M47-closeout base and exact validated head, was `MERGEABLE`/`CLEAN`, and had zero review, comment, or review thread. Squash `c32ff1bf71b53278ef2ff616c2fc3cfce5cf20a3` has sole parent `8d8d9e4a5790d7b74ec06139d314ffdf30a4ef41`, tree `1986f691633d94a5b980c2be0b7e1d0b364de37e` exactly equal to the reviewed head, GitHub verification `valid`, and standalone DCO. No post-merge `main` run was allocated; the feature branch was deleted locally/remotely and local `main` was fast-forwarded exactly. |
| Integration-record local gate | Corrected | The first sandboxed `uv lock --check` exited 1 before project validation because the existing user cache was inaccessible. The approved cache-access rerun resolved the unchanged 46-package lock in 1 ms and checked the 45-package graphics environment in 3 ms; all 291 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 426 architecture tests passed in 2.55 seconds; and strict docs built in 0.98 seconds with only the known upstream notice. Whitespace and full Git-object checking passed. |
| Integration-record hosted gate | 0 | PR #96 exact head `609e0977ba879be84270c2d4fd47a8b9ad23b4c5` changed exactly four Markdown files and classified `documentation`. Run `31288912878` passed in exactly one 33-second Linux allocation: 291-file formatting and Ruff passed, strict docs built in 1.34 seconds, all 426 architecture tests passed in 3.87 seconds, byte-identical distributions passed, and wheel/release smoke passed. Desktop umbrella job `93182693323` was skipped with exactly zero steps. Its wheel hash remained `3c7abfb19c6e1d4e82d63e69e513ff9fdbe2808c90fe74938bef57d3218a93ef`; the factual record changed the sdist hash to `c76a212dcc55c73651770300b1e6f9d5762cdd844e44cb5910711c9be72101a1`. |
| Integration-record review and squash audit | 0 | PR #96 was `MERGEABLE`/`CLEAN` with exact M48-feature base, exact validated record head, and zero review, comment, or thread. Squash `ee98b591abb8e8ecd37b8fa32c01acb0ce279b52` has sole parent `c32ff1bf71b53278ef2ff616c2fc3cfce5cf20a3`, tree `bf4dc989ae014f33b89f81ef67246eb22401ea36` exactly equal to the reviewed head, GitHub verification `valid`, and standalone DCO. No post-merge `main` run was allocated; the record branch was deleted locally/remotely and local `main` was fast-forwarded exactly. |
| Closeout-record local gate | 0 | On the exact three-`.project/**` closeout tree, the unchanged 46-package lock resolved in 1 ms; all 291 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 426 architecture tests passed in 2.58 seconds; and strict docs built in 0.98 seconds with only the known upstream notice. Whitespace and full Git-object checking passed. |

## M47 development evidence - 2026-08-09, Windows, CPython 3.12

| Command or check | Exit | Result |
| --- | ---: | --- |
| M46 closeout audit | 0 | Zero-run PR #91 exact head `76f5aa6d871b1d118e56661d3f191a1cd3f758b8` had exact M46-record base, zero run/check/review/comment/thread, and only three `.project/**` files. Squash/current M47 base `2d27b139c6bf4a130ca97e7f0b518f6ebfe191c5` has sole parent M46 record squash `f6a15655b9bfe5657f15baea89d36206743a3468`, tree `1a26146a7213d21ef5930c6817a9d5ef27aa0259` exactly equal to the reviewed head, valid GitHub signature, and standalone DCO. No post-merge run was allocated; the branch was deleted locally/remotely. Only synchronized `main` remained, with no open PR, tag, or release and healthy Git objects. |
| Portable-verifier focused gate | 0 | Strict formatting, Ruff, and Pyright passed. All 39 focused M45-M47 assertions passed in 0.48 seconds, including fresh-plan creation against the real release-document validator, exact byte revalidation, aggregate-only output, credential rejection, malformed/duplicate/over-limit plan rejection, three-redirect success, fourth/non-HTTPS redirect rejection, declared/streamed size mismatch, monotonic/socket deadline failure, and exclusive hard-link finalization without clobber. |
| Final supported-Python gate | 0 | The exact hardened graphics-enabled CPython 3.12, 3.13, and 3.14 trees each passed 1,945 tests with 14 expected platform/capability skips, in 123.73, 143.78, and 143.70 seconds respectively. The earlier pre-timeout-diagnostic runs are not represented as final-tree evidence. |
| Real-wgpu, profiles, and vertical slices | 0 | All ten real-wgpu tests passed in 7.39 seconds. The two-workload base and three-workload graphics M7 profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, with registered tests and five replay batches passing. |
| Initial distribution exercise | 0 | Before the final aggregate-output/no-clobber hardening and factual records, two fresh build directories matched exactly; isolated-wheel smoke and complete ten-artifact release staging/smoke passed. Because executable and record files changed afterward, no digest from this run is represented as final-tree distribution evidence. |
| Final static, architecture, docs, and workflow gate | 0 | The unchanged lock resolved 46 packages in 1 ms; all 290 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 405 architecture assertions passed in 2.28 seconds; strict docs built in 1.00 seconds with only the known upstream notice; release YAML parsed to the exact `release`/`fresh-consumer` job set; whitespace passed. |
| Final commit-candidate distribution gate | 0 | Two confirmed-absent build directories matched byte-for-byte: the 268,878-byte universal wheel SHA-256 is `3f2ed5d17b503304a7912f39dbe01f96691f3e4f9b092653c7b602a3a0b3ac8a`, and the 1,004,290-byte source distribution SHA-256 is `f1f350662264b28059bac04333c4cf8145af8ff84c8b6f2aca0181ccfddeabec`. Isolated-wheel smoke passed; a fresh ten-artifact release candidate passed complete release smoke. The exact staged contents became sole-parent DCO commit `fdddaa986b647e68a0a027445c11547b878ad246`. |
| Hosted exact-head gate | 0 | Pull-request run `31286321895` classified 30 changed files as substantive and used exactly three allocations at head `fdddaa986b647e68a0a027445c11547b878ad246`. Linux qualified first in 440 seconds, macOS then passed in 160 seconds, and Windows passed in 235 seconds; every job and non-skipped step succeeded. Linux reported 290 formatted files, zero Ruff/Pyright diagnostics, strict docs, 1,949 baseline tests, ten graphics tests, both profiles/vertical slices, reproducible distributions, wheel/release smoke, and 1,949 tests with one skip on each of CPython 3.13 and 3.14. macOS and Windows each passed ten graphics tests, both vertical slices/profiles, and 1,949 CPython 3.14 tests with one skip. Run artifact hashes are the 268,864-byte wheel `9590418ddad07b1c89e2171ba5e99a10943fb3d65ed53f5c163b29722eaa835c` and 1,004,274-byte sdist `dfd5d3c3a7beebf9d460a165a3ab4ca21c4b738f7a6183a69a492fbd554343cf`. |
| PR review and squash audit | 0 | Ready PR #92 had exact M46-closeout base and exact validated head, was `MERGEABLE`/`CLEAN`, and had zero review, comment, or review thread. Squash `c3f5d9c4b9f21315b7ae8f113cc643f978d75746` has sole parent `2d27b139c6bf4a130ca97e7f0b518f6ebfe191c5`, tree `e222ebff0655b9d86548bab6e8d19fb79ba3afc5` exactly equal to the reviewed head, GitHub verification `valid`, and standalone DCO. No post-merge `main` run was allocated; the feature branch was deleted locally/remotely and local `main` was fast-forwarded exactly. |
| Integration-record local gate | 0 | On the four-Markdown record tree, the unchanged graphics environment checked 45 packages in 10 ms and the 46-package lock resolved in 6 ms; all 290 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 405 architecture tests passed in 2.98 seconds; and strict docs built in 1.27 seconds with only the known upstream notice. Whitespace and full Git-object checking passed. |
| Integration-record hosted gate | 0 | PR #93 exact head `19d0c9f21701acd4fa731c567d3927177374dbce` changed exactly four Markdown files and classified `documentation`. Run `31286982718` passed in exactly one 37-second Linux allocation: 290-file formatting and Ruff passed, strict docs built in 1.28 seconds, all 405 architecture tests passed in 3.64 seconds, byte-identical distributions passed, and wheel/release smoke passed. The desktop umbrella job `93177555851` was skipped with exactly zero steps. Its wheel hash remained `9590418ddad07b1c89e2171ba5e99a10943fb3d65ed53f5c163b29722eaa835c`; the factual record changed the sdist hash to `847219da5da3d93e06261d250dd8f0573d5783a046a6875bda66550f66f8ad15`. |
| Integration-record review and squash audit | 0 | PR #93 was `MERGEABLE`/`CLEAN` with exact M47-feature base, exact validated record head, and zero review, comment, or thread. Squash `7bea262210afd5b22265fede596d2d5117b14854` has sole parent `c3f5d9c4b9f21315b7ae8f113cc643f978d75746`, tree `6ebbe7af4071ce2d7a3f7539f9ef84413ed23be8` exactly equal to the reviewed head, GitHub verification `valid`, and standalone DCO. No post-merge `main` run was allocated; the record branch was deleted locally/remotely and local `main` was fast-forwarded exactly. |
| Closeout-record local gate | 0 | On the exact three-`.project/**` closeout tree, the unchanged 46-package lock resolved in 1 ms; all 290 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 405 architecture tests passed in 2.42 seconds; and strict docs built in 0.97 seconds with only the known upstream notice. Whitespace and full Git-object checking passed. |

## M46 development evidence - 2026-08-09, Windows, CPython 3.12

| Command or check | Exit | Result |
| --- | ---: | --- |
| M45 final closeout audit | 0 | Zero-run PR #88 exact head `1192c4bdb3a87efc8124424560287530f10eb9db` had zero run, check, review, comment, or thread. Final squash/current base `086f1ceb3974583ce7a2c386c67f516299c2f1dd` has sole parent M45 integration-record squash `01241e2e1eadff959d13530e1118b0ad6b686dad`, tree `65588443ddccf65d19d6b398664e4fdc76ca6710` exactly equal to the reviewed head, a valid GitHub signature, and standalone DCO. No post-merge `main` run was allocated; the branch was deleted locally/remotely. |
| Repository/history/release baseline audit | 0 | Clean local `main`, `origin/main`, and `origin/HEAD` resolved to the M45 closeout. Only `main` existed locally/remotely, no open PR, GitHub release, or remote tag existed, and full Git-object checking passed. |
| Baseline hashes and inherited release focus | 0 | CI, release-workflow, pyproject, and lock SHA-256 values were `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`, `84da9dfd05f02cbf13403d9ab266808b2ed771fa549fd26a1aad0518f3855a6f`, `42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1`, and `e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed`. The exact inherited release chain passed 147 tests with three capability skips in 14.45 seconds. |
| Initial workflow parse correction | Corrected | The system `python.exe` launcher failed before YAML parsing because its Windows logon session was unavailable. The uv-managed frozen interpreter rerun parsed `release.yml` successfully. No YAML result is claimed from the failed launcher attempt. |
| Current first-party workflow direction | 0 | Current official GitHub documentation supports dependent job outputs through `needs` and recommends upload/download artifacts for files shared between jobs in one workflow. Official `actions/download-artifact` release v8.0.1 and moving v8 tag resolve to verified commit `3e5f45b2cfb9172054b4087a40e8e0b5a5461e7c`; its action definition uses Node 24 and defaults to current-run/current-repository retrieval with digest-mismatch failure. |
| Initial workflow and shared-script integration | Mixed | Release YAML parsed with jobs `release` and `fresh-consumer`; the extracted shared Bash verifier passed Git Bash syntax. The unchanged M45 architecture suite produced two passes and five expected failures because its assertions still inspected the formerly inline workflow body and one-job topology. No M45 regression-suite pass is claimed from this run. |
| Initial M45/M46 behavior gate | Corrected | Focused format/lint and strict Pyright passed; Bash syntax passed. The first behavior run passed 12 assertions but failed three new topology assertions because the helper treated a four-space property as a new two-space job. After correcting the explicit job boundary, all 15 non-documentation M45/M46 assertions passed in 1.90 seconds. Documentation assertions were intentionally excluded while docs were pending. |
| Documentation-integrated architecture migration | Corrected | Static, typing, strict docs, release YAML, and whitespace passed. One focused command used a stale M45 filename and ran no tests. The first complete architecture run passed 362 assertions and failed 21 expected migration guards: eleven exact prior-workflow hashes, six one-job topology counts, three inherited maintainer continuity terms, and one M46 fresh-runner term. After advancing only the authorized M46 workflow topology/hash and preserving M42-M44 wording, all 383 architecture assertions passed in 4.98 seconds; the corrected M45/M46 focus passed 17 tests in 1.60 seconds. |
| Lock/environment access correction | Corrected | Initial lock and sync attempts stopped before validation because the restricted sandbox denied the existing uv user cache. Authorized retries resolved the unchanged 46-package lock in 13 ms and checked the 45-package graphics environment in 6 ms. Git Bash syntax and two-job release-workflow YAML topology passed. |
| Complete supported-Python gate | 0 | The exact graphics-enabled CPython 3.12, 3.13, and 3.14 environments each passed 1,923 tests with 14 expected platform/capability skips, in 146.19, 153.73, and 167.67 seconds respectively. Pytest processes ran serially because the repository config intentionally shares one temporary root. |
| Static, docs, and architecture gate | 0 | All 288 Python files passed format; Ruff passed with one non-fatal cache-write warning; strict Pyright reported zero diagnostics; strict docs built in 1.81 seconds with only the known upstream notice; all 383 architecture assertions passed; shell syntax, workflow YAML, and whitespace passed. |
| Initial reproducible distribution and release gate | 0 | Two confirmed-absent fresh build directories matched exactly: the 268,666-byte wheel SHA-256 was `006947130c2ab9bab93480b8b7ec0047d4d54784af19c80523d6e4bfea03764d`, and the 990,542-byte sdist SHA-256 was `9bc5bb769a3854d1a93f5a19a6e70ea789e9413e2f27fc44446a35999f5ea8d7`. Isolated-wheel smoke and complete ten-artifact release staging/smoke passed. This preceded the plan-option review correction, so final-tree distribution evidence remains separate. |
| Real-wgpu, profiles, and vertical slices | 0 | All ten real-wgpu tests passed in 11.24 seconds. The two-workload base and three-workload graphics M7 profiles validated. Clockwork Arena reproduced state `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, with registered tests and five replay batches passing. |
| Retained benchmark-contract integrity | 0 | M1 accepted seven workloads with one of two historical targets observed; M2 accepted four informational workloads with no targets; M3 accepted six graphics workloads with two targets observed and none met; M4 accepted three workloads with its baseline target observed. Dirty-tree local measurements validate unchanged contracts only and are not release evidence or new targets. |
| Plan-option review correction | Corrected | Review found that fresh mode passed nonexistent `--write-retrieval-plan` to a verifier whose exclusive-create interface is `--asset-plan`; the prior shell fixture stubbed Python and therefore could not detect parser rejection. The shell now uses the established option, and the fresh-mode regression drives the real verifier through public-document validation, exclusive two-asset plan creation, exact byte retrieval, and revalidation while stubbing only final release smoke. All 17 M45/M46 tests passed on CPython 3.12, 3.13, and 3.14; all 383 architecture assertions, strict typing, Git Bash syntax, and whitespace pass after correction. No pre-correction artifact or suite is represented as final-tree evidence. |
| Post-correction distribution gate | 0 | Two new confirmed-absent output directories matched exactly: the 268,666-byte universal wheel SHA-256 is `006947130c2ab9bab93480b8b7ec0047d4d54784af19c80523d6e4bfea03764d`, and the 992,140-byte source distribution SHA-256 is `09bfe175e342b811fe0ffa80d891680e8619416711421964c9fef571b59992b0`. Isolated-wheel smoke passed; a fresh ten-artifact candidate passed complete release smoke. Only subsequent factual `.project` record lines differ from that built source archive; hosted exact-head build evidence remains required. |
| Final implementation-tree gate | 0 | The unchanged lock resolved 46 packages in 1 ms; all 288 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 383 architecture assertions passed in 5.54 seconds; strict docs built in 1.75 seconds with only the known upstream notice; Git Bash syntax and whitespace passed. The complete CPython 3.12 graphics-enabled implementation tree passed 1,923 tests with 14 expected capability skips in 167.85 seconds. Only these subsequent factual record lines differ. |
| First hosted feature run | Blocked | Ready PR #89 exact head `bbfd68ee6b0826b47b573ede4a10910b07945aeb` classified 35 paths as substantive and allocated exactly three runners in run `31282550237`. Linux job `93166096904` passed in 5m58s before desktop allocation; Windows `93166655774` passed in 3m42s. macOS `93166655799` failed in 2m05s: 1,926 tests passed and one skipped, but the M45 reuse-mode shell regression failed because macOS Bash 3.2 reports an explicitly empty array expansion as unbound under `set -u`. The PR remains blocked and no merge is claimed. |
| Bash 3.2 portability correction | Corrected | The first local correction removed the empty array but duplicated the verifier command; the inherited M45 guard then passed 16 focused tests and failed one exact two-call-site assertion. A shared verifier function now forwards only safe positional `"$@"` arguments, create mode supplies `--asset-plan`, reuse mode supplies no extra argument, and exactly two verifier call sites remain. Focused format/lint/typing and Git Bash syntax pass; all 17 M45/M46 tests pass on CPython 3.12, 3.13, and 3.14. Corrected complete local and hosted gates remain pending. |
| Corrected complete local gate | 0 | All 288 files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 383 architecture assertions passed in 4.07 seconds; strict docs built in 1.28 seconds with only the known upstream notice; Git Bash syntax and whitespace passed. The corrected complete CPython 3.12 graphics suite passed 1,923 tests with 14 expected capability skips in 124.90 seconds. Only these subsequent factual record lines differ. |
| Corrected hosted exact-head gate | 0 | Run `31283211266` passed corrected head `7f7f865880a415bec2f1fdaffbc35426399fb0fd` after classifying 35 paths as substantive. Linux job `93167719009` passed in 7m07s before macOS `93168410366` and Windows `93168410370` were allocated; macOS passed in 2m31s and Windows in 4m24s, for exactly three allocations. Linux CPython 3.12 passed 1,927 tests; Ubuntu 3.13/3.14 and both desktop 3.14 suites each passed 1,927 with one skip. Every platform passed ten real-wgpu tests, profiles, Clockwork Arena, and Agent World Builder. Linux reproducibly built a 268,652-byte wheel at SHA-256 `a04089cbae12977bff08da2d239a15bb00248c53d4b5a2dbad9c83d74ba4a4cf` and a 993,325-byte sdist at SHA-256 `db16457f5c382f29fa9b4149c545b60eb9483ebc0b2a8d31b3d3343643ad563b`; installed-wheel and complete release smoke passed. |
| Review and squash integration audit | 0 | PR #89 exact corrected head/base was `MERGEABLE` and `CLEAN`, with no review, issue comment, review comment, or review thread. Squash `d4cb4410d1dd9f684d3b169932ea3251801d3884` has sole parent exact M45 closeout `086f1ceb3974583ce7a2c386c67f516299c2f1dd`, tree `a3774ff0846a099c2b821500a93fb3b387db2210` exactly equal to the reviewed head, a valid GitHub signature, and standalone DCO. No post-merge `main` run was allocated. Fetch confirmed remote feature deletion; local `main` fast-forwarded and the verified local feature ref was deleted. |
| Integration-record local gate | 0 | The unchanged lock resolved 46 packages in 0.95 ms; all 288 files passed format and Ruff; strict Pyright reported zero diagnostics; all 383 architecture assertions passed; strict docs built with only the known upstream notice; exactly four Markdown paths changed; whitespace and full Git-object checking passed. A fresh universal build, isolated-wheel smoke, complete ten-artifact staging, and release smoke passed. |
| Integration-record hosted gate | 0 | PR #90 exact head `4a74380f3011cbb841b89a7778cf676163cc1c28` classified four paths as documentation. Run `31283922258` allocated only Linux job `93169503776`, which passed in 36 seconds with 383 architecture tests in 3.54 seconds, strict docs, a 268,652-byte wheel at SHA-256 `a04089cbae12977bff08da2d239a15bb00248c53d4b5a2dbad9c83d74ba4a4cf`, a 994,254-byte sdist at SHA-256 `5de818b55de7657168db8331c7e0c90b5fce0cf8aae3253473ef354626de5b62`, installed-wheel smoke, and complete release smoke. Desktop umbrella job `93169560315` skipped with zero steps. No review, comment, or thread existed. |
| Integration-record squash and cleanup audit | 0 | Squash `f6a15655b9bfe5657f15baea89d36206743a3468` has sole parent feature squash `d4cb4410d1dd9f684d3b169932ea3251801d3884`, tree `41f907a4be24bead1dfdbeeb05a4dfa28893ef7e` exactly equal to the reviewed record head, valid GitHub signature, and standalone DCO. No post-merge run was allocated. Fetch confirmed remote record deletion; local `main` fast-forwarded and the verified local record ref was deleted. Only synchronized `main` remained before this closeout branch, with no open PR and healthy Git objects. |
| Closeout local gate | 0 | The unchanged lock resolved 46 packages in 1 ms; all 288 files passed format and Ruff; strict Pyright reported zero diagnostics; all 383 architecture assertions passed in 3.92 seconds; strict docs built in 1.02 seconds with only the known upstream notice; whitespace and full Git-object checking passed. The diff contained exactly `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, and `.project/TEST_EVIDENCE.md`. |

## M45 development evidence - 2026-08-09, Windows, CPython 3.12

| Command or check | Exit | Result |
| --- | ---: | --- |
| M44 final closeout audit | 0 | Zero-run PR #85 exact head `5bde66de625d92837d74ed4e6c0d650196763296` had no workflow run, check, review, comment, or thread. Squash/current base `2c5e312a97028d0b835fc174b8abb51df22ea314` has sole parent M44 integration squash `792a2e702a8331566ddc5c5bf07e449c66f30f9e`, tree `60f5850c297f0a9e34aa9e19f58623a2b403f6d0` exactly equal to the reviewed head, a valid GitHub signature, and standalone DCO trailer. No post-merge `main` run was allocated; the branch was pruned remotely and deleted locally. |
| Repository/history/release baseline audit | 0 | Clean local `main`, `origin/main`, and `origin/HEAD` resolved to the M44 closeout; only `main` existed locally/remotely, no open PR, local/remote tag, or GitHub release existed, and full Git object checking passed. |
| Baseline hashes and inherited release focus | 0 | CI SHA-256 was `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`; release workflow was `3e82735e95120ab3fcbd9d2f0b658765a2e524e808d8b64a25062e799454dfae`; pyproject and lock were `42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1` and `e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed`. The exact inherited release-chain focus passed 100 tests with three Windows capability skips in 5.48 seconds. |
| Current primary public-retrieval direction | 0 | Current official GitHub REST documentation states that the exact public release-ID and release-asset-ID endpoints can be used without authentication for public resources; the asset endpoint accepts `application/octet-stream` and may stream or redirect. Current immutable-release guidance also confirms that immutability is a separate repository setting; M45 does not change or claim it. |
| Initial workflow/architecture structure gate | Mixed | Release YAML parsed and its final step was the M45 public consumer path. Focused Ruff lint passed and strict Pyright reported zero diagnostics; 13 non-documentation M43-M45 architecture assertions passed in 0.24 seconds. Ruff format reported that the new M45 architecture file needs mechanical formatting, and documentation assertions were intentionally excluded while docs were pending. No complete initial gate pass is claimed. |
| Initial documentation-integrated focus | Mixed | After mechanical formatting, focused format/lint/strict typing, release-workflow YAML parsing, strict docs, and whitespace passed. The 109-test release/M43-M45 focus had 105 passes and three capability skips but one failure because the rewritten current maintainer boundary omitted M43's literal `retriev` continuity marker. No focused-suite pass is claimed for this run. |
| Corrected focused release-chain gate | 0 | Maintainer continuity now names the canonical M43 retrieval plan. Focused format/lint and strict Pyright passed; all 106 release-workflow/M43-M45 architecture plus release-validator tests passed with three Windows capability skips in 5.57 seconds; strict docs built in 0.94 seconds; YAML and whitespace passed. After the release-ID strengthening, the focused suite again passed 106 tests with three skips in 5.53 seconds. |
| Shell-syntax probe correction | Corrected | A sandboxed combined probe was blocked before project checks by existing uv-cache permissions and the Windows system `bash` launcher. The authorized retry passed focused tests but confirmed that system `bash` had no WSL distribution. The first Git Bash `-c` call split the multiline value and was not a valid syntax result. Piping the exact YAML-extracted step to the installed Git Bash parser then exited 0 with `M45 Bash syntax parsed with Git Bash`. |
| Initial complete architecture gate | Mixed | Lock/sync, 287-file format, Ruff, strict Pyright, strict docs, workflow YAML, and whitespace passed. Architecture produced 360 passes and 12 failures: eleven earlier admission/CI tests intentionally pinned the prior M44 release-workflow hash, while one M42 test counted all later verifier calls instead of its own step. No architecture pass is claimed for this run. |
| Corrected complete architecture gate | 0 | Historical M26-M37 exact-workflow guards now pin M45 SHA-256 `84da9dfd05f02cbf13403d9ab266808b2ed771fa549fd26a1aad0518f3855a6f`; the M42/M43/M44 tests bound their own steps. All 37 architecture files passed format and Ruff, strict Pyright reported zero diagnostics, and all 372 architecture tests passed in 2.24 seconds. |
| Complete CPython 3.12 graphics suite | 0 | The exact frozen graphics environment passed 1,912 tests with 14 expected platform/capability skips in 109.25 seconds. |
| Complete cross-version compatibility gate | 0 | Exact frozen non-graphics CPython 3.13 passed 1,902 tests with 15 expected skips in 97.36 seconds. CPython 3.14 passed the same counts in 102.87 seconds. Exact CPython 3.12 plus the 45-package graphics environment was restored. |
| Real-wgpu, profile, and vertical-slice gate | 0 | All ten real-wgpu tests passed in 7.71 seconds; the two-workload base and three-workload graphics M7 profiles validated. Clockwork Arena reproduced state hash `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, with registered tests and five replay batches passing. |
| Fresh reproducible distribution and release gate | 0 | Three M45 output paths were confirmed absent. Two same-source builds matched exactly: the 268,458-byte wheel SHA-256 is `01cbd4bb5d9693ffd6289d513c6bba1d56f71db4863383b50f653597a9cd4775`; the 978,884-byte sdist SHA-256 is `1b6ee70e8c03d680c0d637755aec6d4164e65b70b4ae9f8612738dd9685b3738`. Isolated-wheel smoke and complete ten-artifact release staging/smoke passed. |
| Documented benchmark integrity | 0 | M1 validation accepted seven workloads with one of two historical targets observed; M2 accepted four informational workloads with no targets; M3 accepted six graphics workloads with two targets observed and none met; M4 accepted three workloads with its baseline target observed. These dirty-tree local measurements validate unchanged evidence contracts; they are not release results or new targets. |
| Synthetic public-shell execution correction | Corrected | The first cross-platform shell regression invoked extracted workflow text without GitHub Actions' `-e -o pipefail` wrapper and let the system curl path win over a file stub; the intentionally nonexistent request produced an empty asset while later commands masked the failure. No pass is claimed. The corrected regression uses shell functions, the exact fail-fast/pipefail flags, and a one-asset canonical plan; it proves two credential-free bounded curl invocations, exact bytes/no leftover partial, two validator calls, and one release-smoke call. Focused format/lint/strict typing passed and all seven M45 architecture tests passed in 0.50 seconds. |
| Corrected synthetic public-shell cross-version gate | 0 | The seven M45 architecture tests, including exact extracted-shell execution under GitHub Actions' fail-fast/pipefail flags, passed on CPython 3.12 in 0.50 seconds, CPython 3.13 in 0.85 seconds, and CPython 3.14 in 0.89 seconds. This is deterministic local fixture evidence, not a real release request. |
| Final recorded-tree static and architecture gate | 0 | The unchanged lock resolved 46 packages in 0.82 ms; all 287 Python files passed Ruff format and lint; strict Pyright reported zero diagnostics; all 373 architecture tests passed in 3.13 seconds; strict docs built in 0.95 seconds; the exact extracted Bash step parsed under Git Bash; workflow YAML and whitespace passed. |
| Final recorded-tree complete suite | 0 | The complete exact CPython 3.12 graphics-enabled suite passed 1,913 tests with 14 expected platform/capability skips in 109.16 seconds. |
| Final scope, credential, identity, and Git-object audit | 0 | No diff exists in the pull-request CI workflow, runtime source, `pyproject.toml`, `uv.lock`, or benchmarks. CI, release-workflow, pyproject, and lock SHA-256 values are respectively `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`, `84da9dfd05f02cbf13403d9ab266808b2ed771fa549fd26a1aad0518f3855a6f`, `42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1`, and `e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed`. New additions contain no repository-visible tooling identity terms or credential values; full Git object checking passed. No remaining local review finding was identified. |
| Post-record exact-tree gate | Corrected | The first `uv lock --check` attempt exited 1 before lock evaluation because the restricted sandbox denied access to uv's existing user cache; the approved cache-access rerun resolved the unchanged 46-package lock in 0.80 ms. All 287 Python files passed formatting, Ruff passed, strict Pyright reported zero diagnostics, all 373 architecture tests passed in 3.31 seconds, strict docs built in 1.05 seconds, and whitespace passed. |
| Staged-inventory reproducibility and release gate | 0 | The exact 29-path staged inventory had no whitespace error. Two fresh builds matched exactly: the 268,458-byte wheel SHA-256 is `01cbd4bb5d9693ffd6289d513c6bba1d56f71db4863383b50f653597a9cd4775`, and the 981,484-byte source distribution SHA-256 is `ed3df9ff0627943c6e2baa689e1faa6e83a4181aa6a9b9f695ad9c87ff7267bc`. Isolated-wheel smoke passed; complete ten-artifact staging and release smoke passed. |
| Final precommit history and publication audit | 0 | After `git fetch --prune origin`, branch `HEAD`, local `main`, `origin/main`, `origin/HEAD`, and the merge base all resolved to exact M44 closeout `2c5e312a97028d0b835fc174b8abb51df22ea314`; no commit existed on the feature branch yet. The only local branches were `main` and the intended M45 branch, and the only remote branch was `origin/main`. GitHub reported `main` as default, no open pull request, no release, and no remote tag. |
| Feature publication | 0 | DCO-signed commit `51e5a600c89fbecf09a9addb47e8e2a1729b0081` has exact parent M44 closeout, tree `5f9368d215038b76cc8afb104cf6bcb444a04801`, and the reviewed 29-path inventory. Neutral branch `release/m45-public-consumer-verification` was pushed and ready PR #86 opened against exact `main` base. |
| Hosted exact-head gate | 0 | Run `31279830471` passed exact head `51e5a600c89fbecf09a9addb47e8e2a1729b0081` after classifying 29 paths as substantive. Linux job `93159242419` passed in 6m58s before desktops were allocated; macOS `93159945457` passed in 2m07s and Windows `93159945447` in 4m01s, for exactly three allocations. Linux CPython 3.12 passed 1,917 tests; Ubuntu 3.13/3.14 and both desktop 3.14 suites each passed 1,917 tests with one expected skip. Every platform passed ten real-wgpu tests, profiles, Clockwork Arena, and Agent World Builder. Linux reproducibly built a 268,444-byte wheel at SHA-256 `eacfbec422b2e83daf20e964b407c28abe12298969997d1baeb06a0f75cbcdee` and a 981,813-byte sdist at SHA-256 `020098dced75b6114863cbbc4b300d1ef357e5643465ea85cd69b44e509499a9`; installed-wheel and complete release smoke passed. |
| Review and squash integration audit | 0 | GitHub reported PR #86 `MERGEABLE` and `CLEAN`, with no review, issue comment, review comment, or thread. Squash `471da6efe908463ed8f6744272bd372548cb3345` has sole parent exact M44 closeout `2c5e312a97028d0b835fc174b8abb51df22ea314`, tree `5f9368d215038b76cc8afb104cf6bcb444a04801` exactly equal to the reviewed head, a valid GitHub signature, and a standalone DCO trailer. No post-merge `main` run was allocated. Two read-only local tree queries initially left PowerShell revision braces unquoted and misparsed; corrected quoted queries and literal tree diff both passed. |
| Post-merge cleanup baseline | Corrected | Fetch confirmed remote feature deletion and advanced `origin/main` to the verified squash. Local `main` fast-forwarded cleanly. Ordinary `git branch -d` correctly refused because squash integration does not preserve the feature commit as an ancestor; after exact tree equality was proven, the explicitly authorized force deletion removed only that local feature ref. Before this record branch, synchronized `main` was the sole local/remote branch. |
| Integration-record local gate | 0 | The unchanged lock resolved 46 packages in 1 ms; all 287 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 373 architecture tests passed in 4.68 seconds; strict docs built in 1.80 seconds; exactly four Markdown paths changed; whitespace and full Git-object checking passed. A fresh universal build, isolated-wheel smoke, complete ten-artifact staging, and release smoke also passed. |
| Integration-record hosted gate | 0 | PR #87 exact head `13dcd951226430cb660ddf98ad0bd9c66f4633a5` classified four paths as documentation. Run `31280561142` allocated only Linux job `93161042021`, which passed in 38 seconds with 373 architecture tests in 3.26 seconds, strict docs, a 268,444-byte wheel at SHA-256 `eacfbec422b2e83daf20e964b407c28abe12298969997d1baeb06a0f75cbcdee`, a 982,837-byte sdist at SHA-256 `649fada4a8aa79257548a6b537f0942233642722b179af0c18c6eb90073ccc82`, isolated-wheel smoke, and complete release smoke. Desktop umbrella job `93161106180` skipped with zero steps and no runner allocation. The first GraphQL review-thread query had a brace syntax error; the corrected query returned zero threads. |
| Integration-record squash and cleanup audit | 0 | PR #87 was `MERGEABLE` and `CLEAN`, with no review, issue comment, review comment, or thread. Squash `01241e2e1eadff959d13530e1118b0ad6b686dad` has sole parent feature squash `471da6efe908463ed8f6744272bd372548cb3345`, tree `e2c25c9ab29d9caeb28cb50fd47bdf05220ece96` exactly equal to the reviewed record head, a valid GitHub signature, and standalone DCO. No post-merge `main` run was allocated. Fetch confirmed remote branch deletion; local `main` fast-forwarded and the verified local record branch was deleted. Before this closeout branch, clean synchronized `main` was the sole local/remote branch, no PR was open, and full Git-object checking passed. |
| Closeout-record local gate | 0 | The unchanged lock resolved 46 packages in 10 ms; all 287 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 373 architecture tests passed in 4.03 seconds; strict docs built in 1.70 seconds; exactly three `.project/**` Markdown paths changed; whitespace and full Git-object checking passed. |

## M44 development evidence - 2026-08-09, Windows, CPython 3.12

| Command or check | Exit | Result |
| --- | ---: | --- |
| M43 final closeout audit | 0 | Zero-run PR #82 exact head `59ecb5b53890b6dcdc10328ca8d59b8b8ff5507d` changed exactly three `.project` Markdown paths and had no run, check, review, comment, or thread. Squash/current base `0b3b9eb982a67eee1833f3a8f920671f8ffd006b` has sole parent M43 integration squash `deab03fd1f01c3baea8c55494ec1205f53495417`, exact reviewed tree `34bec1410bb96d85172c19238d6eed382f9e0caf`, a valid GitHub signature, and standalone DCO trailer. No post-merge `main` run was allocated. |
| Repository/history/release baseline audit | Mixed | Clean synchronized `main` began at the M43 closeout, only `main` existed locally/remotely, no open PR, tag, or GitHub release existed, and full Git object checking passed. The first `gh release list` JSON query requested unsupported `url` and failed; the corrected supported-field query returned `[]`. No release absence claim relies on the failed query. |
| Baseline hashes and inherited release focus | 0 | CI SHA-256 was `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`; release workflow was `a5c7ff3f80010cad2712592daf32327b80122b8473cee720fe066bbb3eb06e06`; pyproject and lock were `42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1` and `e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed`; the M43 verifier was `3915994bf9369a47da11d95dd86da7e500458509a970f1e6d948eafc2a71a72f`. The exact inherited M38-M43/release test command passed 86 tests with two capability skips in 5.25 seconds. |
| Current primary attestation direction | 0 | Official GitHub documentation and installed GitHub CLI 2.95.0 help expose SLSA v1 and SPDX 2.3 predicate verification plus exact repository, signer workflow/digest, source ref/digest, GitHub OIDC issuer, hosted-runner denial, and candidate-limit flags. The documented trust boundary states that attestation verification proves subject provenance/identity, not artifact security. |
| Initial verifier static gate | Mixed | `uv run --frozen ruff format --check scripts\\verify_release_attestations.py` reported that one file required formatting. Focused Ruff lint passed and strict Pyright reported zero diagnostics. Ruff then formatted the file. No initial format pass is claimed. |
| Initial focused behavior gate | Mixed | After adding adversarial tests, Ruff found one constant-attribute `getattr`, strict Pyright found two private-test-helper accesses, and pytest passed 28 tests with one capability skip but failed two wheel-cardinality fixtures because Windows `Path` collation did not match the protocol's case-sensitive basename order. No initial focused gate pass is claimed. |
| Corrected focused verifier gate | 0 | The test fixture now sorts explicitly by basename and uses typed module-level wrappers. Focused Ruff passed, strict Pyright reported zero diagnostics, and all 30 exact-policy, plan/directory-bound, wheel-cardinality, child-failure, timeout, unavailable-command, and content-confidentiality tests passed with one Windows symlink-capability skip in 0.36 seconds. |
| Initial workflow/documentation integration gate | Mixed | Focused Ruff, strict Pyright, release-workflow YAML parsing, whitespace, and strict docs passed. The combined release suite passed 63 tests with one capability skip and exposed two stale architecture assumptions: the current maintainer boundary no longer named inherited M42 literally, and the new ordering guard used a non-existent attestation step label. No combined-suite pass is claimed. |
| Corrected workflow/documentation integration gate | 0 | Documentation continuity now names M42/M43 explicitly and the guard uses exact pinned workflow labels. Focused format/lint and strict Pyright passed, strict docs built in 0.98 seconds with only the known upstream notice, and all 65 release/attestation tests passed with one Windows symlink-capability skip in 0.53 seconds. |
| Complete lock/static/architecture gate | Corrected | The first lock check was blocked before validation by managed-cache permissions. Its authorized retry resolved the unchanged 46-package lock in 1 ms, and exact frozen CPython 3.12 graphics sync checked 45 packages. All 286 Python files passed formatting, Ruff passed, strict Pyright reported zero diagnostics, all 366 architecture tests passed in 2.19 seconds, and whitespace passed. |
| Pre-review complete CPython 3.12 graphics suite | 0 | The exact frozen graphics environment passed 1,905 tests with 14 expected platform/capability skips in 102.86 seconds. A later focused success-output regression is separately validated below. |
| Real-wgpu, profile, and vertical-slice gate | 0 | All ten real-wgpu tests passed in 5.93 seconds; the two-workload base and three-workload graphics M7 profiles validated. Clockwork Arena reproduced state hash `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, with registered tests and five replay batches passing. |
| Complete cross-version compatibility gate | 0 | Exact frozen non-graphics CPython 3.13 passed 1,895 tests with 15 expected skips in 93.56 seconds. CPython 3.14 passed the same counts in 99.06 seconds. Exact CPython 3.12 plus the 45-package graphics environment was restored. |
| Fresh reproducible distribution and release gate | Corrected | The first build attempt was blocked before building by managed-cache permissions. Authorized fresh builds in two confirmed-absent directories then matched exactly: the 268,208-byte wheel SHA-256 is `e3f9f6655d52cc00173b4d1a0e4dfb32250d06a57cb8718b955e9076caa0ac71`; the 969,261-byte sdist SHA-256 is `58399ff571ab77e16703f5ce9f72e5e0f611fe6edd72c3243a6672657dd9362a`. Installed-wheel smoke and complete ten-artifact release staging/smoke passed. The 94-entry wheel contains no native file or release verifier; the 453-entry sdist contains the exact M44 verifier, RFC, unit test, and architecture test. |
| Documented benchmark integrity | 0 | The M1 validator accepted seven workloads with one of two historical targets observed; M2 accepted four informational workloads with no targets; M3 accepted six graphics workloads with two targets observed and none met; and M4 accepted three workloads with its baseline target observed. These dirty-tree local measurements are validation observations, not release evidence or new performance targets. |
| Success-output confidentiality strengthening | 0 | A direct CLI-success regression now proves that only protocol, status, and three aggregate counts are emitted and that tag, commit, paths, predicate labels, and artifact identities remain absent. Focused Ruff and strict Pyright passed; all 36 M44 unit/architecture tests passed with one capability skip in 1.28 seconds. |
| Protected-surface and archive audit | 0 | No diff exists against exact base in pull-request CI, runtime source, benchmarks, pyproject, or lock. Final CI/release/pyproject/lock SHA-256 values are `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`, `3e82735e95120ab3fcbd9d2f0b658765a2e524e808d8b64a25062e799454dfae`, `42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1`, and `e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed`; verifier SHA-256 is `780d08eb107787d67e40d6f7ce95bb68fa95626d812abfbc2103314d6a672a27`. Diff scans found no credential value. |
| Final recorded-tree static, docs, architecture, and suite gate | 0 | All 286 Python files passed formatting; Ruff passed; strict Pyright reported zero diagnostics; all 366 architecture tests passed in 2.18 seconds; strict docs built in 1.00 seconds with only the known upstream notice; whitespace passed; and the complete exact CPython 3.12 graphics suite passed 1,906 tests with 14 expected skips in 101.66 seconds. |
| Final review-record gate | 0 | After recording the complete evidence and removing an unnecessary tool-name phrase from repository-visible records, all 286 files passed format and Ruff, strict Pyright reported zero diagnostics, all 397 architecture plus M44 unit tests passed with one capability skip in 2.83 seconds, strict docs built in 0.94 seconds with only the known upstream notice, whitespace passed, and a neutral-path diff scan returned no match. |
| DCO feature commit and ready PR | 0 | Exact 30-path reviewed index became DCO-signed commit `494ae4f32209c8e679633d528bb63cf4b1093800`, with sole parent exact M43 closeout and tree `623014f83b2196e838bc5b51cc4a80a84d35c0c5`. The neutral branch was pushed and ready PR #83 was created against unchanged exact base `0b3b9eb982a67eee1833f3a8f920671f8ffd006b`. A supplementary unquoted PowerShell `HEAD^{tree}` spelling was mangled and produced no usable result; its quoted retry returned the exact commit tree and no repository change occurred. |
| Hosted exact-head gate | 0 | Run `31277236908` passed exact head `494ae4f32209c8e679633d528bb63cf4b1093800` and exact base in exactly three allocations. The trusted-base classifier admitted 30 substantive paths. Linux job `93152711778` passed in 7m04s before macOS `93153426050` and Windows `93153426045` started; macOS passed in 2m35s and Windows in 3m50s. |
| Hosted behavior and artifacts | 0 | Linux baseline passed 1,910 tests; Ubuntu CPython 3.13/3.14 and Windows/macOS CPython 3.14 each passed 1,910 tests with one expected skip. All three platforms passed ten real-wgpu tests, profiles, Clockwork Arena, and Agent World Builder. Reproducible builds reported a 268,194-byte wheel SHA-256 `b03925afeaf20ead351c62103a4a706840d6a685d919942445e47ae9934bb821` and a 970,729-byte sdist SHA-256 `6f661ec47c4526bb39f525579e0d9d666c5903188eb47d520944556df43f94fe`; installed-wheel and complete release smoke passed. |
| Thread-inspection correction | Corrected | The previously used installed review-helper path was absent, so no result is claimed from that invocation. Direct authenticated PR/review/GraphQL reads then found one current unresolved P1 thread and no conversation comment or additional thread. |
| Predicate-URI review resolution | 0 | The P1 claimed that `sbom-path` used unversioned `https://spdx.dev/Document`. Exact pinned `actions/attest` commit `1e69f48acb82d1966a394da916b4c1698aa569d6` instead reads `SPDX-2.3`, extracts `2.3`, and emits `https://spdx.dev/Document/v2.3`; current official GitHub verification documentation specifies the same URI. The evidence was posted, thread `PRRT_kwDOTtqoGs6Xgla0` was resolved, and a final re-fetch found no unresolved thread or conversation comment. No code change or extra hosted run was warranted. |
| PR #83 squash integration audit | 0 | PR #83 was ready, `MERGEABLE`/`CLEAN`, exact-head/exact-base, and had all three checks successful before merge. Squash `781ca0d1692b309ca3dd7ea9ca8dc6af88f77b09` has sole parent exact M43 closeout, tree `623014f83b2196e838bc5b51cc4a80a84d35c0c5` exactly equal to the reviewed head, a valid GitHub signature, and standalone maintainer DCO trailer. No post-merge `main` run was allocated. Fetch pruned the deleted remote feature branch; local `main` was fast-forwarded and the local feature branch was deleted only after tree equality was proven. Only clean synchronized `main` remained before this record branch. |
| Integration-record local gate | 0 | The unchanged lock resolved 46 packages in 0.75 ms; all 286 files passed format and Ruff; strict Pyright reported zero diagnostics; all 366 architecture tests passed in 2.45 seconds; strict docs built in 1.05 seconds with only the known upstream notice; whitespace and Git objects passed. Confirmed-absent output paths then received a fresh universal wheel/sdist and complete ten-artifact release candidate; isolated-wheel and release smoke passed. Exactly four Markdown paths changed. |
| Integration-record hosted gate | 0 | Ready PR #84 exact head `66c58256790127db727c8cc87741d95f6c9a5612` and base `781ca0d1692b309ca3dd7ea9ca8dc6af88f77b09` classified exactly four changed paths as documentation. Run `31278008212` allocated only Linux job `93154643908`, which passed in 30 seconds with the unchanged lock, format, lint, strict docs, all 366 architecture tests, reproducible universal build, installed-wheel smoke, and complete release smoke. Desktop umbrella job `93154696963` skipped with zero steps. The PR had no review, comment, or thread. |
| Integration-record squash and cleanup audit | 0 | PR #84 squash-integrated as `792a2e702a8331566ddc5c5bf07e449c66f30f9e`; its sole parent is feature squash `781ca0d1692b309ca3dd7ea9ca8dc6af88f77b09`, tree `028e40887910df3562c891fdfd816cdacc663115` exactly equals the reviewed record head, GitHub reports `verified=true` and `reason=valid`, and the message contains a standalone DCO trailer. No post-merge `main` run was allocated. Fetch pruned the deleted remote record branch, and the local squash-source branch was deleted after tree equality was proven. Only synchronized `main` remained before this closeout branch. |
| Closeout-record local gate | 0 | Exactly three `.project` Markdown paths changed; protected workflows, metadata, lock, runtime source, docs, and roadmap are unchanged. Whitespace and full Git-object checks passed, and the current three-file record contains no repository-visible workflow-identity term. |

## M43 development evidence - 2026-08-09, Windows, CPython 3.12

| Command or check | Exit | Result |
| --- | ---: | --- |
| M42 final closeout audit | 0 | Zero-run PR #79 exact head `8407499326f2c55118c7a28735224c9e4cd18723` changed only three `.project` paths and had no check, run, review, comment, or thread. Squash `2ed26ebc5e5a388a02ddd1ae0fd8114f4c3e1e79` has sole parent `35aa6c46f0d128f66535d75dff342f0b7f6bcdeb`; tree `664d67c43daa42eb8bd02ab0c52d04bad294ff6b` exactly equals the reviewed head; GitHub reports `verified=true`, `reason=valid`; and the message has a standalone DCO trailer. No post-merge `main` run was allocated. The branch was pruned remotely and deleted locally. |
| Repository/history/release baseline audit | 0 | Clean local `main`, `origin/main`, and `origin/HEAD` all resolved to `2ed26ebc5e5a388a02ddd1ae0fd8114f4c3e1e79`; only `main` existed locally/remotely, no open pull request, local/remote tag, or GitHub release existed, and `git fsck --full --no-dangling` passed. |
| Baseline hashes and release focus | 0 | CI SHA-256 was `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`; release workflow was `a15921df77a64c51889d8d6353cce7e5f6924b38396a5b84bd39c5a5accbfefe`; M42 verifier was `901b0538c0c69468d0dfea797f58a72fdccf0fbb657f7484f5fa41b3385174f3`; pyproject and lock were `42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1` and `e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed`. All 46 inherited validator/M42 tests passed with two Windows symlink-capability skips in 3.97 seconds. |
| Current primary retrieval direction | 0 | Official GitHub REST documentation states that a numeric release asset ID can return binary content with `Accept: application/octet-stream`, directly or through a redirect, using existing contents access. The exact IDs in the already verified published document therefore support authenticated byte retrieval without another job, runner, action, permission, dependency, or publication authority. |
| Initial M43 behavior gate | Mixed | Ruff lint and strict Pyright passed. The format check reported one verifier file requiring mechanical formatting, and the first behavior run passed 52 tests with two Windows symlink-capability skips while exposing two stale test fixtures: expected JSON order differed from canonical plan order and the synthetic extra asset lacked its newly required ID. No complete behavior or format pass is claimed. |
| Corrected M43 behavior gate | 0 | Ruff mechanically formatted one file. Focused formatting, lint, and strict Pyright passed; all 54 plan, state, ID, asset, confidentiality, and no-clobber behavior tests passed with two Windows symlink-capability skips in 4.89 seconds. |
| Initial workflow-integrated gate | Mixed | Lint and strict Pyright passed, and all 63 focused behavior/M42/M43 architecture tests passed with two capability skips in 4.89 seconds. The formatting command incorrectly included the YAML workflow in Ruff's Python inputs, so Ruff rejected the non-Python file and also reported one new Python architecture file requiring formatting. No integrated format pass is claimed. |
| Corrected workflow-integrated gate | 0 | Ruff mechanically formatted the one Python architecture file. Four focused Python files then passed formatting, lint, and strict Pyright; the release workflow parsed as YAML; and all 63 focused tests passed with two Windows symlink-capability skips in 4.88 seconds. |
| Initial documentation-integrated gate | Mixed | All 283 Python files passed Ruff formatting and lint, strict Pyright reported zero errors, the release workflow parsed as YAML, and MkDocs 0.91 strict documentation passed. The focused suite passed 64 tests with two Windows symlink-capability skips and exposed one over-specific M43 RFC assertion that required four boundary nouns to appear as one literal phrase even though the RFC stated each boundary independently. No complete focused-test pass is claimed. |
| Corrected documentation-integrated gate | 0 | The M43 documentation guard was narrowed to check each bounded hosted-resource term independently. All 283 Python files passed formatting and lint, strict Pyright reported zero errors, the release workflow parsed as YAML, MkDocs 0.91 strict documentation passed, all 65 focused tests passed with two Windows symlink-capability skips in 4.99 seconds, and whitespace validation passed. |
| Initial complete architecture migration | Mixed | The complete architecture suite passed 349 tests and failed 12 guards in 2.09 seconds. Eleven historical M26-M34/M36-M37 guards rejected the intentional release-workflow SHA-256 change from `a15921df77a64c51889d8d6353cce7e5f6924b38396a5b84bd39c5a5accbfefe` to `4fd17754f739c0a65635802209531f7c17096e533e35eb403f0a2df738e24fd2`; the M41 live verifier guard still required protocol v3 rather than v4. No unexpected architecture failure occurred, and no complete architecture pass is claimed. |
| Corrected complete architecture suite | 0 | The eleven historical workflow guards were advanced only to exact M43 release-workflow SHA-256 `4fd17754f739c0a65635802209531f7c17096e533e35eb403f0a2df738e24fd2`, and the M41 live verifier guard was advanced only to protocol v4. All 361 architecture tests passed in 2.12 seconds. |
| Initial complete lock/environment gate | 1 | `uv lock --check` and `uv sync --frozen --all-groups --extra graphics` each stopped before validation because the restricted sandbox denied uv access to its managed user cache. No lock or environment pass is claimed from these attempts. |
| Corrected complete lock/environment gate | 0 | With managed-cache access permitted, `uv lock --check` resolved the unchanged 46-package lock and exact frozen graphics sync checked 45 installed packages. |
| Complete static and documentation gate | 0 | All 283 Python files passed Ruff formatting, Ruff lint passed, strict Pyright reported zero diagnostics, and MkDocs 0.91 built the complete strict documentation in 0.97 seconds with only the known upstream MkDocs 2.0 notice. |
| Complete CPython 3.12 graphics suite | 0 | The complete exact frozen environment passed 1,869 tests with 13 expected platform/capability skips in 101.30 seconds. |
| Real-wgpu, profile, and vertical-slice gate | 0 | All ten real-wgpu integration tests passed in 6.17 seconds; the two-workload base and three-workload graphics M7 profiles validated. Clockwork Arena reproduced state hash `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`, with all registered tests and five replay batches passing. |
| Complete cross-version compatibility gate | 0 | Exact frozen non-graphics CPython 3.13 passed 1,859 tests with 14 expected skips in 92.46 seconds. Exact CPython 3.14 passed the same counts in 98.53 seconds. |
| Restored baseline environment | 0 | Exact CPython 3.12 plus the frozen 45-package graphics environment was restored before packaging and final validation. |
| Pre-review reproducible distribution and release gate | 0 | Six named M43 output paths were confirmed absent before use. Two fresh same-source builds matched exactly: the 267,920-byte wheel SHA-256 was `1568bb7f9b3b029b758a0a33256d9a005964336fd6d3f6c63a0150b403af1713`; the 952,976-byte sdist SHA-256 was `47184fd81a0d7f6eaf92843c5352291510054063cfbd52797e9ac01360503527`. Installed-wheel smoke and complete ten-artifact release staging/smoke passed. This gate preceded the review-only shell-bound correction and added local round-trip test, so final-tree distribution validation remains separately required. |
| Exact-ID local retrieval round-trip regression | 0 | A new success-path regression consumed the canonical ID/name plan, materialized every named byte by its planned ID, and reverified the retrieved directory against the same published document. Focused formatting, Ruff, strict Pyright, and all 56 validator tests passed with two Windows symlink-capability skips in 5.93 seconds. |
| Findings-first bounded-ID correction | 0 | Review found that workflow defense in depth rejected zero and nonnumeric IDs but did not independently enforce the RFC's canonical positive 63-bit bound. The shell boundary now rejects leading zeroes, more than 19 digits, values above `9223372036854775807`, and a 33rd request. Final release-workflow SHA-256 is `874f40f4edc0abe5f455d7cc001a7a3e2a94f8bbb38c21ff75ac628662126aac`; historical live guards were advanced to that exact value. All 283 files passed format and Ruff, strict Pyright reported zero diagnostics, all 70 focused tests passed with two capability skips in 5.16 seconds, all 361 architecture tests passed in 2.39 seconds, and strict docs built in 0.91 seconds. |
| Initial shell-boundary diagnostic | 1 | The unqualified Windows `bash` alias attempted to start the sandbox-denied WSL service, so it could not evaluate the condition. No shell-syntax pass is claimed from that diagnostic. |
| Corrected shell-boundary diagnostic | 0 | Explicit Git Bash executed the exact canonical/63-bit ID conditions: IDs `1` and `9223372036854775807` passed; `0`, `01`, `9223372036854775808`, and the 20-digit value `10000000000000000000` failed. |
| Final-tree reproducible distribution and release gate | 0 | Three final-tree output paths were confirmed absent before use. Two fresh same-source builds matched exactly: the 267,920-byte wheel SHA-256 is `1568bb7f9b3b029b758a0a33256d9a005964336fd6d3f6c63a0150b403af1713`; the 953,858-byte sdist SHA-256 is `d112d0fb245388243b942a39438158a327063238b838f86f718fe79bcaf6f1f7`. Installed-wheel smoke and complete ten-artifact release staging/smoke passed. |
| Final reviewed implementation-tree suite | 0 | The complete exact CPython 3.12 graphics-enabled suite passed 1,870 tests with 13 expected platform/capability skips in 101.10 seconds. |
| Initial verifier transport scan | Corrected | An over-broad lexical pattern matched the `eval(` suffix inside the type name `ReleaseAssetRetrieval(`. Inspection confirmed it was not an evaluation call; the corrected token/import-boundary scan returned no match. |
| Final scope, credential, archive, identity, YAML, and Git-object audit | 0 | No diff exists in runtime source, `pyproject.toml`, `uv.lock`, or the pull-request CI workflow. Exact SHA-256 values are CI `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`, release workflow `874f40f4edc0abe5f455d7cc001a7a3e2a94f8bbb38c21ff75ac628662126aac`, pyproject `42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1`, lock `e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed`, and verifier `0248b6153512ad9024415001a81d4dd5fe91404cfe3d2665ba39537908e02320`. The release YAML parsed, credential/private-key and corrected verifier transport/evaluation scans found no match, whitespace passed, retired workflow-marker paths remain absent with no new marker added by the diff, and `git fsck --full --no-dangling` passed. The 94-entry wheel contains no native/WASM or release verifier file; the 50-entry sample bundle remains complete; the 449-entry sdist contains exactly one verifier, M43 RFC, and M43 architecture test. Only `main` plus the intended local M43 feature branch exist, with only `origin/main` remote. No remaining blocking or non-blocking review finding was identified. |
| Final record-aware gate | 0 | The unchanged lock resolved 46 packages in 0.82 ms; all 283 files passed format and Ruff, strict Pyright reported zero diagnostics, all 361 architecture tests passed in 2.63 seconds, and strict docs built in 0.97 seconds with only the known upstream notice. |
| Initial Git staging attempt | 1 | The restricted sandbox denied creation of `.git/index.lock`; no staging or commit occurred. With repository-write permission, all intended M43 paths staged and DCO-signed commit `56069b26d5d416e864c6eb9689a5dbf40e93e1fb` was created with exact parent `2ed26ebc5e5a388a02ddd1ae0fd8114f4c3e1e79` and tree `58207d1754bf6fa550f3088725255887aa632f55`. |
| Initial feature publication | 0 | Branch `release/m43-asset-retrieval-integrity` was pushed and ready PR #80 was created against exact `main` base `2ed26ebc5e5a388a02ddd1ae0fd8114f4c3e1e79`. |
| Initial hosted exact-head gate | Blocked by review | Run `31273727767` passed exact head `56069b26d5d416e864c6eb9689a5dbf40e93e1fb` in exactly three allocations: Linux job `93143827271` in 5m58s, macOS `93144479696` in 2m45s, and Windows `93144479700` in 3m38s. Classification was 32 changed paths and substantive. Linux baseline and Ubuntu 3.13/3.14 plus both desktop 3.14 suites each passed 1,873 tests; compatibility suites had one expected skip. All platforms passed ten real-wgpu tests, profiling, and both samples. Hosted reproducibility reported a 267,906-byte wheel SHA-256 `b36bf6eebeb8173d04c9dba1c96d166f0294aab0d36804c07523be2cb2fd71c1` and 954,433-byte sdist SHA-256 `26fed671d05278284813eeb40d1ee5d13c2be6c9592c1e53d9a15eef7251ffdf`; installed-wheel and release smoke passed. One unresolved P2 review correctly identified unbounded disk consumption before post-download validation, so this head is not merge-approved. |
| Thread-aware review inspection | Corrected | An initial GraphQL query was malformed by PowerShell around the hyphenated repository name. The bundled helper could not use the unusable system Python launcher, then its first uv-managed run encountered Windows legacy-output decoding. With `PYTHONUTF8=1`, it reported exactly one unresolved, current P2 thread `PRRT_kwDOTtqoGs6XgHH9` at `.github/workflows/release.yml`; no conversation comment or second thread existed. |
| P2 bounded-response correction | In progress | The verified plan now carries expected bytes. The workflow revalidates 0..256-MiB sizes, enforces the 512-MiB expected-total cap, streams only expected bytes plus one through `head -c`, rejects non-exact `wc -c`, and retains exclusive partial/final paths plus complete rehashing. This adds no runner, action, permission, dependency, trigger, or release authority. The workflow SHA-256 advances to `a5c7ff3f80010cad2712592daf32327b80122b8473cee720fe066bbb3eb06e06`. |
| Bounded-stream shell probe | Corrected | The first inline Bash command had a quoting parse failure. Two explicit Git Bash attempts then could not locate `head` under the inherited Windows path. A repository-ignored probe with `/usr/bin:/bin` set explicitly passed: 0 and 256-MiB size bounds were accepted; leading-zero, over-limit, and ten-digit sizes were rejected; exact and short streams were distinguished; a long producer stopped after six bytes with nonzero `pipefail`; and the exact 512-MiB total boundary passed while one byte over failed. |
| Focused P2 correction gate | 0 | One verifier file was mechanically formatted after the first format check. All 283 files then passed format and Ruff, strict Pyright reported zero diagnostics, all 70 focused tests passed with two Windows symlink-capability skips in 5.11 seconds, all 361 architecture tests passed in 2.09 seconds, strict docs built in 0.91 seconds, and the release YAML parsed. |
| Complete corrected-head suite | 0 | The exact CPython 3.12 graphics-enabled suite passed 1,870 tests with 13 expected platform/capability skips in 101.11 seconds. |
| Corrected-head reproducible distribution and release gate | 0 | Three fresh output paths were confirmed absent. Two same-source builds matched exactly: the unchanged 267,920-byte wheel SHA-256 is `1568bb7f9b3b029b758a0a33256d9a005964336fd6d3f6c63a0150b403af1713`; the 956,357-byte sdist SHA-256 is `92342f9b8b13212a11949f2949c40f9a267432c1cb72318cb54987c90d972a63`. Installed-wheel smoke and complete ten-artifact release staging/smoke passed. |
| Corrected-head scope and security audit | 0 | No correction diff exists in runtime source, `pyproject.toml`, `uv.lock`, or pull-request CI. Exact SHA-256 values are CI `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`, release workflow `a5c7ff3f80010cad2712592daf32327b80122b8473cee720fe066bbb3eb06e06`, pyproject `42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1`, lock `e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed`, and verifier `3915994bf9369a47da11d95dd86da7e500458509a970f1e6d948eafc2a71a72f`. Credential/private-key scanning found no match, whitespace passed, and full Git-object checking passed. No remaining local blocking or non-blocking finding was identified. |
| Final correction record-aware gate | 0 | The unchanged lock resolved 46 packages in 0.85 ms; all 283 files passed format and Ruff, strict Pyright reported zero diagnostics, all 361 architecture tests passed in 2.71 seconds, and strict docs built in 1.03 seconds with only the known upstream notice. |
| Initial corrected-hosted evidence retrieval | 1 | Three parallel `gh` reads were denied network access by the restricted sandbox before GitHub returned data. No hosted result was inferred from those failures; approved identical reads supplied the evidence below. |
| Corrected PR #80 hosted gate | 0 | Run `31274622529` passed exact corrected head `3a5004217598c82eca5b8286442e7d8a502642b1` and exact base `2ed26ebc5e5a388a02ddd1ae0fd8114f4c3e1e79`. The trusted-base classifier reported 32 paths and `substantive`. Exactly three allocations ran: Linux job `93146100921` passed in 7m13s before macOS `93146830451` and Windows `93146830453` started; macOS passed in 1m48s and Windows in 3m53s. |
| Corrected hosted behavior and artifacts | 0 | The Linux baseline passed 1,873 tests; Ubuntu CPython 3.13/3.14 and macOS/Windows CPython 3.14 each passed 1,873 with one expected skip. All platforms passed ten real-wgpu tests, profiling, Clockwork Arena, and Agent World Builder. Reproducible builds reported a 267,906-byte wheel SHA-256 `b36bf6eebeb8173d04c9dba1c96d166f0294aab0d36804c07523be2cb2fd71c1` and a 956,605-byte sdist SHA-256 `2064aa70d5b8cdfef41f9a36b49689cd38e89e0b3a5780000a9d742e8b8a2982`; installed-wheel smoke and complete ten-artifact release smoke passed. |
| Final thread-aware review audit | 0 | The helper re-fetch found the sole P2 thread outdated after correction. A reply linked exact correction commit `3a5004217598c82eca5b8286442e7d8a502642b1`, bounded-stream semantics, and corrected hosted run `31274622529`; GraphQL then reported thread `PRRT_kwDOTtqoGs6XgHH9` resolved. A final re-fetch found no unresolved thread or new conversation comment. GitHub reported exact head/base, all three checks successful, `MERGEABLE`, and `CLEAN`. |
| PR #80 squash integration audit | 0 | PR #80 merged at `2026-08-08T19:44:48Z` as squash `8b7038cc203cead16d1dd88c746b584b6d0c37ca`. Its sole parent is exact M42 closeout `2ed26ebc5e5a388a02ddd1ae0fd8114f4c3e1e79`; tree `6c5ed36a8454a3ab16fec82152df13038c41ce84` exactly equals the reviewed corrected head; GitHub reports `verified=true`, `reason=valid`; and the message contains a standalone maintainer DCO trailer. No `main` run was allocated. The remote feature branch was deleted by the merge, the local feature branch was deleted after fast-forwarding `main`, and remote pruning left only synchronized `main` before this record branch. Full Git object checking reported only expected unreachable historical objects and no corruption error. |
| Integration-record local gate | 0 | The unchanged lock resolved 46 packages in 0.86 ms; all 283 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 361 architecture tests passed in 2.15 seconds; and strict docs built in 0.91 seconds with only the known upstream notice. Confirmed-absent `.tmp/m43-integration-dist` and `.tmp/m43-integration-release` paths then received a universal wheel/sdist and complete ten-artifact candidate; isolated-wheel and release smoke passed. Exactly four Markdown paths changed. |
| Final integration-record gate | 0 | On the recorded tree, the unchanged lock resolved 46 packages in 0.77 ms; all 283 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 361 architecture tests passed in 2.04 seconds; and strict docs built in 0.91 seconds. Exactly four Markdown paths changed, whitespace and full Git-object checks passed, and `[retired control directory]`, `[retired control directory]`, `[retired control directory]`, and `[retired control file]` remained absent. |
| Integration-record hosted gate | 0 | PR #81 exact head `3350a8eb59fae09cd0764a400540d0d51722866e` classified four paths as `documentation`. Run `31275425828` allocated only Linux job `93148087116`, which passed in 33 seconds: lock, documentation environment, formatting, Ruff, strict docs, all 361 architecture tests in 3.08 seconds, two universal builds, isolated-wheel smoke, release staging, and complete release smoke. Desktop umbrella job `93148143924` skipped with zero steps and no runner; substantive type/full-suite, compatibility, graphics, profile, and vertical-slice steps did not run. |
| Integration-record review, squash, and cleanup | 0 | Immediately before merge, GitHub reported PR #81 exact base `8b7038cc203cead16d1dd88c746b584b6d0c37ca`, exact head `3350a8eb59fae09cd0764a400540d0d51722866e`, `MERGEABLE`, `CLEAN`, one successful Linux check, one skipped zero-step desktop umbrella, and no review, comment, or thread. Squash `deab03fd1f01c3baea8c55494ec1205f53495417` has sole parent the feature squash, exact reviewed tree `0725d4a05a2033b868e44b050d58023b4cdb61e3`, a valid GitHub signature, and standalone DCO trailer. No post-merge `main` run was allocated. The branch was deleted remotely, then locally after fast-forwarding `main`; remote pruning left only `main` before this closeout branch. |
| Closeout-record local gate | 0 | The unchanged lock resolved 46 packages in 0.79 ms; all 283 Python files passed formatting and Ruff; strict Pyright reported zero diagnostics; all 361 architecture tests passed in 2.03 seconds; and strict docs built in 0.88 seconds with only the known upstream notice. Exactly three `.project` Markdown paths changed, whitespace and full Git-object checks passed, and `[retired control directory]`, `[retired control directory]`, `[retired control directory]`, and `[retired control file]` remained absent. |

## M42 development evidence - 2026-08-09, Windows, CPython 3.12

| Command or check | Exit | Result |
| --- | ---: | --- |
| M41 final closeout audit | 0 | Zero-run PR #76 exact head `5d891d0bfa030ff8387d9c384fafa4aa81abbdf8` changed only three `.project` paths and had no check, run, review, comment, or thread. Squash `0dec2254a9d9483b27d158aaad108340e9c94e28` has sole parent `b05dbda471edf2ac14c5e0b6bf4bd75aaf23f252`; tree `a028eb0492019b42658045bf112ca2fcafd211b4` exactly equals the reviewed head; GitHub reports `verified=true`, `reason=valid`; and the message has a standalone DCO trailer. No post-merge `main` run was allocated. The branch was pruned remotely and deleted locally. |
| Repository/history/release baseline audit | 0 | Clean local `main`, `origin/main`, and `origin/HEAD` all resolved to `0dec2254a9d9483b27d158aaad108340e9c94e28`; only `main` existed locally/remotely, no open pull request, local/remote tag, or GitHub release existed, and `git fsck --full --no-dangling` passed. |
| Baseline hashes and release focus | 0 | CI SHA-256 was `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`; release workflow was `3983cd82f0201fcac8fe2156f77715e1136998781b428c60a192b3f3a3522871`; M41 verifier was `b34ef5fd37a428561cb294c4673da6adffb5ace43025f68359af689258ec4a35`; pyproject and lock were `42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1` and `e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed`. All 37 inherited validator/workflow tests passed with two Windows symlink-capability skips in 2.88 seconds. |
| Current primary publication direction | 0 | Official GitHub CLI documentation identifies `gh release edit --draft=false` as the draft publication transition. The versioned release API exposes draft/prerelease state, publication time, immutable state, body, and assets. The existing exact release ID therefore supports one same-ID postpublication read without a new permission, job, runner, action, dependency, or publication authority. |
| Initial M42 behavior gate | Mixed | Ruff lint and strict Pyright passed, and all 39 explicit draft/published-state behavior tests passed with two Windows symlink-capability skips in 3.72 seconds. The format check reported that the two changed files required mechanical formatting, so no initial format pass is claimed. |
| Corrected M42 behavior gate | 0 | Ruff mechanically formatted the two files. Focused format and strict Pyright passed; a strengthened calendrical timestamp check initially produced one Ruff `UP017` alias finding while tests/type checking remained green, then passed after using `datetime.UTC`. All 39 behavior tests passed with two capability skips in 3.81 seconds. |
| Workflow-integrated gate | Corrected | The first combined run passed Ruff and strict Pyright plus 48 behavior/workflow tests, while two M41 architecture assertions correctly rejected the intentional workflow hash and protocol changes. After removing the obsolete unchanged-workflow assertion, advancing the live protocol guard, and adding M42 same-ID/state/topology coverage, focused formatting/lint/type checking passed and all 54 tests passed with two Windows symlink-capability skips in 3.90 seconds. |
| Complete architecture hash migration | Corrected | The first complete architecture run passed 345 tests but 11 historical M26-M34/M36-M37 guards rejected the intentional release-workflow hash change. Every affected guard was advanced to the exact M42 workflow SHA-256 `a15921df77a64c51889d8d6353cce7e5f6924b38396a5b84bd39c5a5accbfefe`; no CI, runtime, metadata, or lock guard changed. Whole-tree formatting/lint, strict Pyright, and strict docs then passed; all 395 validator plus architecture tests passed with two Windows symlink-capability skips in 5.87 seconds, and whitespace passed. |
| Findings-first published-boundary strengthening | 0 | Review generalized draft-only error wording for the published invocation, proved that success emits neither publication timestamp nor immutable state, added published notes/asset drift regressions with content-silent failures, and guarded the second verifier/API request against mutation, deletion, clobber, or tag-based lookup. Focused format/lint/strict typing passed and all 57 release-integrity tests passed with two Windows symlink-capability skips in 4.02 seconds. No remaining blocking or non-blocking review finding was identified. |
| Complete M42 CPython 3.12 quality gate | 0 | The unchanged lock resolved 46 packages, exact frozen graphics sync checked 45 packages, whole-tree formatting reported 282 files, Ruff passed, strict Pyright reported zero diagnostics, strict docs built in 0.88 seconds, all 397 validator plus complete architecture tests passed with two Windows symlink-capability skips in 5.74 seconds, whitespace passed, and the complete suite passed 1,850 tests with 13 expected skips in 100.33 seconds. |
| Real-wgpu, profile, and vertical-slice gate | 0 | All ten real-wgpu integration tests passed in 6.23 seconds; the two-workload base and three-workload graphics M7 profiles validated; Clockwork Arena reproduced state hash `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`; all five replay batches/tests passed. |
| Complete cross-version compatibility gate | 0 | Exact frozen non-graphics CPython 3.13 passed 1,840 tests with 14 expected skips in 92.16 seconds. Exact CPython 3.14 passed the same counts in 97.07 seconds. Exact CPython 3.12 plus the graphics extra was then restored. |
| Fresh reproducible distribution and release gate | 0 | Five output paths were confirmed absent before use. Two fresh same-source builds matched exactly: the 267,707-byte wheel SHA-256 is `6957bcc95af86ae36832549615e4324a32a86bbb9669af87de9f6318617536d5`; the 942,424-byte sdist SHA-256 is `84c2f28f610745ee0bbc3a497b2a0bb2678b7f6e233627a41beba394c3df90ad`. Installed-wheel smoke, complete ten-artifact staging/release smoke, and source-archive M42 inventory passed. Exact staged synthetic documents passed protocol `/3` for mutable draft, mutable published prerelease, and immutable published prerelease state without emitting timestamps or immutable policy. |
| Scope, credential, archive, and Git-object audit | 0 | No diff exists in the pull-request CI workflow, runtime source, pyproject, or lock. CI, release workflow, pyproject, and lock SHA-256 values are `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`, `a15921df77a64c51889d8d6353cce7e5f6924b38396a5b84bd39c5a5accbfefe`, `42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1`, and `e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed`. Credential/private-key scanning found no value; the validator contains no eval, exec, subprocess, shell, requests, urllib, socket, or HTTP client; the wheel contains no verifier/native object; `[retired control directory]` is absent; and full Git object checking passed. |
| Final recorded-tree static and architecture gate | 0 | The unchanged lock resolved 46 packages in 0.83 ms; whole-tree formatting reported 282 files, Ruff passed, strict Pyright reported zero diagnostics, strict docs built in 0.94 seconds, all 397 validator plus complete architecture tests passed with two Windows symlink-capability skips in 6.87 seconds, the changed release workflow parsed as YAML, CI/runtime/metadata/lock scope and whitespace passed, and full Git object checking remained clean. |
| Hosted exact-head gate | 0 | Ready PR #77 run `31271273535` passed exact head `45cd04e627f44400e8bd3adcbeeaf1756160f745` in exactly three allocations. Linux job `93137568146` passed in 6m54s, Windows `93138322832` in 3m39s, and macOS `93138322836` in 1m59s. Ubuntu CPython 3.12 passed 1,853 tests; Ubuntu 3.13/3.14 and both desktop 3.14 suites each passed 1,853 tests with one expected skip. All platforms passed ten real-wgpu tests, graphics profiling, and both deterministic samples. Hosted reproducibility reported a 267,693-byte wheel SHA-256 `9a9881ce0fa918e1652b2be8019aede5b2e4c4c403565cc5eb570db8454101d7` and a 943,096-byte sdist SHA-256 `370278b63994c913c74c7675e2ed02f2ca17cf3023ff26f96b64cf44faf26fc0`; installed-wheel and complete ten-artifact release smoke passed. |
| Review and squash integration audit | 0 | Immediately before merge, PR #77 was ready, `MERGEABLE`/`CLEAN`, exact-base/exact-head, all three checks successful, and had zero review, issue comment, review comment, or review thread. Squash `28dd9d7e282ec85c06b71ed340f3cfcea379d6be` has sole parent exact M41 closeout `0dec2254a9d9483b27d158aaad108340e9c94e28`; tree `7e65795a6b44de7b3ff393128274eda207c58dc3` exactly equals reviewed head; GitHub reports `verified=true`, `reason=valid`; and the message has a standalone DCO trailer. No post-merge `main` run was allocated. |
| Post-merge cleanup baseline | 0 | Fetch pruned the deleted remote feature branch. The exact reviewed tree was proven before the local squash-source branch was force-deleted. Clean local `main`, `origin/main`, and `origin/HEAD` resolve to the M42 squash, and only `main` remained locally/remotely before the integration-record branch was created. |
| Integration-record sandbox gate | Mixed | Strict docs built in 0.95 seconds and all 356 architecture tests passed in 2.34 seconds. The concurrently requested static commands did not execute because the managed filesystem sandbox denied uv access to its existing user cache, so no pass is claimed for that first static batch. |
| Corrected integration-record local gate | 0 | With the required read access to the existing uv cache, the unchanged lock resolved 46 packages in 0.79 ms, whole-tree formatting reported 282 files, Ruff passed, and strict Pyright reported zero diagnostics. The four-path documentation scope and whitespace checks passed. |
| Final integration-record gate | 0 | The unchanged lock resolved 46 packages in 0.85 ms; whole-tree formatting reported 282 files, Ruff passed, strict Pyright reported zero diagnostics, strict docs built in 0.89 seconds, and all 356 architecture tests passed in 2.02 seconds. Exactly four Markdown paths changed, whitespace and full Git object checking passed, and `[retired control directory]` remained absent. |
| Integration-record hosted gate | 0 | PR #78 exact head `b08c4ff57c2d995fdce73f2e835f2ca3a8075a70` classified four changed paths as documentation. Run `31271986168` allocated only Linux job `93139403348`, which passed in 33 seconds with 356 architecture tests, universal build, installed-wheel smoke, and complete release smoke. Desktop umbrella job `93139476046` skipped with zero steps and no runner. The PR had no review, issue comment, review comment, or thread. |
| Integration-record squash and cleanup audit | 0 | PR #78 squash-integrated as `35aa6c46f0d128f66535d75dff342f0b7f6bcdeb`; its sole parent is feature squash `28dd9d7e282ec85c06b71ed340f3cfcea379d6be`, tree `fbdb7c0caf0ec1db7c0c331309c92e1abc66d5f5` exactly equals the reviewed record head, GitHub reports `verified=true` and `reason=valid`, and the message contains a standalone DCO trailer. No post-merge `main` run was allocated. Fetch pruned the deleted remote record branch and the local branch was force-deleted only after equality was established. Only clean synchronized `main` remains. |
| Redundant local tree spelling | 1 | A supplementary `rev-parse` spelling was mangled by PowerShell and failed, so no evidence is claimed from it. The authenticated feature-head and squash-commit API documents independently reported the same exact tree used by the successful integration audit. |
| Closeout-record local gate | 0 | The unchanged lock resolved 46 packages in 0.91 ms; whole-tree formatting reported 282 files, Ruff passed, strict Pyright reported zero diagnostics, strict docs built in 0.89 seconds, and all 356 architecture tests passed in 2.01 seconds. Exactly three `.project` Markdown paths changed, whitespace and full Git object checking passed, and `[retired control directory]` remained absent. |

## M41 development evidence - 2026-08-09, Windows, CPython 3.12

| Command or check | Exit | Result |
| --- | ---: | --- |
| M40 final closeout audit | 0 | Zero-run PR #73 exact head `e1b07f781096370fa3b6f820bc80dc1d4c585279` changed only three `.project` paths and had no check, run, review, comment, or thread. Squash `9983e0da88b6aef999d26498cc6438f0b3c5927b` has sole parent `67d03d41430dc24bf81a894752b3641de8e521ed`; tree `d76b9a348690d6a35af774755cdc4a836240069a` exactly equals the reviewed head; GitHub reports `verified=true`, `reason=valid`; and the message has a standalone DCO trailer. No post-merge `main` run was allocated. The branch was pruned remotely and deleted locally. |
| Repository/history/release baseline audit | 0 | Clean local `main`, `origin/main`, and `origin/HEAD` all resolved to `9983e0da88b6aef999d26498cc6438f0b3c5927b`; only `main` existed locally/remotely, no PR, local/remote tag, or GitHub release existed, and `git fsck --full --no-dangling` passed. `[retired control file]` is absent; `MAINTAINERS.md` is authoritative. |
| Baseline hashes and release focus | 0 | CI SHA-256 was `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`; release workflow was `3983cd82f0201fcac8fe2156f77715e1136998781b428c60a192b3f3a3522871`; M40 verifier was `f618eeb897ba8a9b48fb01cb79ca8f8337453053610656102adef5abc7a5f141`; pyproject and lock were `42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1` and `e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed`. All 25 inherited validator/M40/workflow tests passed with one Windows symlink-capability skip in 2.30 seconds. |
| Current primary release-notes direction | 0 | Official GitHub CLI documentation states that `--notes-file` reads release notes from a file, and the versioned REST release schema exposes the source notes as `body`. The existing authenticated draft document therefore supports an exact local/source-body comparison without another API call, permission, workflow step, or runner allocation. |
| Initial M41 behavior gate | Mixed | Focused formatting, Ruff, and strict Pyright passed. The first behavior run exposed Windows text-mode LF/CRLF normalization in the test fixture, causing valid synthetic drafts to mismatch, and pytest derived an overlong temporary path from the oversized byte parameter. No behavior-suite pass is claimed from that run. |
| Corrected focused M41 gate | 0 | The fixture now writes/reads exact UTF-8 bytes and uses bounded explicit case IDs. Focused formatting/lint passed, strict Pyright reported zero diagnostics, and all 26 exact-body, malformed-state, bounded-notes, asset, and pathological-JSON tests passed with one Windows symlink-capability skip in 2.80 seconds. |
| Corrected documentation-integrated gate | 0 | Whole-tree formatting reported 281 files, Ruff passed, focused strict Pyright reported zero diagnostics, strict docs built in 0.94 seconds, all 37 draft-integrity and M41 architecture tests passed with one Windows symlink-capability skip in 2.98 seconds, and whitespace passed. The preceding integrated test run had one documentation-coverage assertion that accepted `release notes` but not the repository's hyphenated `release-notes`; the corrected assertion requires both words independently. |
| Failure-output confidentiality regression | 0 | Focused formatting/lint passed, strict Pyright reported zero diagnostics, and all 30 draft-integrity plus M41 architecture tests passed with one Windows symlink-capability skip in 2.87 seconds. Remote notes-drift cases now explicitly prove that neither expected nor substituted note text is emitted in structured failure output. |
| Complete M41 CPython 3.12 quality gate | 0 | The unchanged lock resolved 46 packages, exact frozen graphics sync restored 45 packages, whole-tree formatting reported 281 files, Ruff passed, strict Pyright reported zero diagnostics, strict docs built in 0.86 seconds, all 377 validator plus complete architecture tests passed with one Windows symlink-capability skip in 4.69 seconds, and the complete suite passed 1,830 tests with 12 expected skips in 98.93 seconds. |
| Real-wgpu, profile, and vertical-slice gate | 0 | All ten real-wgpu integration tests passed in 6.10 seconds; the two-workload base and three-workload graphics M7 profiles validated; Clockwork Arena reproduced state hash `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`; all five replay batches/tests passed. |
| Complete cross-version compatibility gate | 0 | Exact frozen non-graphics CPython 3.13 passed 1,820 tests with 13 expected skips in 90.63 seconds. Exact CPython 3.14 passed the same counts in 96.42 seconds. Exact CPython 3.12 plus the graphics extra was then restored. |
| First fresh distribution and synthetic-draft gate | Mixed | Two fresh builds were byte-reproducible, installed-wheel smoke and complete ten-artifact release smoke passed. A temporary inline Python fixture command was mangled by PowerShell quoting, exited 1 before producing the document, and the verifier correctly rejected the absent document. The same fixture generated through an explicit ignored temporary helper then passed protocol `/2`; no pass is claimed for the failed one-liner. |
| Findings-first notes-member correction | Corrected | Review found that a symlink substituted specifically for `RELEASE_NOTES.md` failed safely but used the generic asset-entry code because asset scanning ran first. Notes validation now precedes asset scanning, so every invalid notes member uses `release_draft.invalid_notes`; a capability-aware symlink regression covers the correction. Focused format/lint/strict typing passed with 30 tests and two Windows symlink-capability skips in 3.61 seconds. |
| Corrected complete architecture and suite gate | 0 | All 377 validator plus complete architecture tests passed with two Windows symlink-capability skips in 4.95 seconds. The complete exact CPython 3.12 graphics suite then passed 1,830 tests with 13 expected skips in 98.95 seconds. |
| Corrected fresh distribution and release gate | 0 | Three final output paths were confirmed absent before use. Two fresh same-source builds matched exactly: the 267,535-byte wheel SHA-256 is `7a33fd4d3224db7f1a8fb790a6bcbfa694c3b7312a3a43c75e82d9577c4e968c`; the 933,796-byte sdist SHA-256 is `891a004f3762761c6e2a1871f5e0d0b59a6730c635138d7e8250d4b32891b592`. Installed-wheel smoke, complete ten-artifact staging/release smoke, source-archive M41 inventory, and exact staged synthetic-draft notes-and-assets verification under protocol `/2` passed. |
| Scope, credential, archive, and Git-object audit | 0 | Both workflow hashes remain exact baseline values, and no diff exists in either workflow, `src/ludoweave`, `pyproject.toml`, or `uv.lock`. Credential/private-key scanning found no value, and the validator contains no eval, exec, subprocess, shell, requests, urllib, socket, or HTTP client. The wheel contains no verifier or native object; the sdist contains the M41 verifier, RFC, unit tests, and architecture test. `[retired control directory]` is absent, whitespace passed, and `git fsck --full --no-dangling` passed. No remaining blocking or non-blocking review finding was identified. |
| Final recorded-tree static and architecture gate | 0 | The unchanged lock resolved 46 packages in 0.83 ms; whole-tree formatting reported 281 files, Ruff passed, strict Pyright reported zero diagnostics, strict docs built in 0.89 seconds, all 377 validator plus complete architecture tests passed with two Windows symlink-capability skips in 5.10 seconds, whitespace and scope-boundary checks passed, and full Git object checking remained clean. |
| Hosted exact-head gate | 0 | Ready PR #74 run `31269399211` passed exact head `ec051d4fd2da80235da1a94642158ebe384cb2b0` in exactly three allocations. Linux job `93132713018` passed in 6m55s, Windows `93133449986` in 2m44s, and macOS `93133449993` in 2m12s. Classification reported 18 changed paths and `substantive`. Ubuntu CPython 3.12 passed 1,833 tests; Ubuntu 3.13/3.14 and both desktop 3.14 suites each passed 1,833 tests with one expected skip. All platforms passed ten real-wgpu tests, graphics profiling, and both deterministic samples. Hosted reproducibility reported a 267,521-byte wheel SHA-256 `5f74478b0516e15ae3e0caa841f6b125f19f742efba290b8f0c0c031ab65ce68` and a 934,831-byte sdist SHA-256 `426080ee88d0ce9c040a053e3258e8cd74f6f4602b78b90cec0df9ad8eed700f`; installed-wheel and complete release smoke passed. |
| Review and squash integration audit | 0 | Immediately before merge, PR #74 was ready, `MERGEABLE`/`CLEAN`, exact-base/exact-head, all three checks successful, and had zero review, issue comment, review comment, review, or review thread. Squash `89a641559c246e971869a3ae06a878de81bffcee` has sole parent exact M40 closeout `9983e0da88b6aef999d26498cc6438f0b3c5927b`; tree `6446826ee0b35c02dcebc78b9fad3f55caaca0c5` exactly equals reviewed head; GitHub reports `verified=true`, `reason=valid`; and the message has a standalone DCO trailer. No post-merge `main` run was allocated. |
| Post-merge cleanup baseline | 0 | The merge had already deleted the remote feature branch, so a redundant explicit deletion correctly reported that the ref did not exist; fetch pruned the stale tracking ref. The exact reviewed tree was proven before local branch deletion. Clean local `main`, `origin/main`, and `origin/HEAD` resolve to the M41 squash, and only `main` remains locally/remotely. |
| Integration-record local gate | 0 | The unchanged lock resolved 46 packages in 0.78 ms; whole-tree formatting reported 281 files, Ruff passed, strict Pyright reported zero diagnostics, strict docs built in 0.88 seconds, all 351 architecture tests passed in 2.06 seconds, the four-path documentation boundary and whitespace passed, and full Git object checking remained clean. |
| Integration-record hosted gate | 0 | PR #75 exact head `d967624c618e433beda1052a7715872b0f256540` classified four changed paths as documentation. Run `31270041957` allocated only Linux job `93134330478`, which passed in 33 seconds with 351 architecture tests, universal build, installed-wheel smoke, and complete release smoke. Desktop umbrella job `93134392069` skipped with zero steps and no runner. The PR had no review, comment, or thread. |
| Integration-record squash and cleanup audit | 0 | PR #75 squash-integrated as `b05dbda471edf2ac14c5e0b6bf4bd75aaf23f252`; its sole parent is feature squash `89a641559c246e971869a3ae06a878de81bffcee`, tree `b4750863c6500602982853f75faca3c2a11e4e1f` exactly equals the reviewed record head, GitHub reports `verified=true` and `reason=valid`, and the message contains a standalone DCO trailer. No post-merge `main` run was allocated. GitHub had already deleted the remote record branch; its stale tracking ref was pruned and the local branch was deleted after tree equality was proven. Only clean synchronized `main` remains. |

## M40 development evidence - 2026-08-09, Windows, CPython 3.12

| Command or check | Exit | Result |
| --- | ---: | --- |
| M39 final closeout audit | 0 | Zero-run PR #70 exact head `4d31f46008bf5efd7475a9b432226748e484d891` changed only three `.project` paths, allocated no workflow run, and had no review, comment, or thread. Squash `49fba13477890bf6bf1c9e6a645e669b3a69492f` has sole parent `166dcb2dc619dbc721207eece273c0fd9437f9ff`; tree `46df243de9b6f9f773723412af2580fe8682f27a` exactly equals the reviewed head; GitHub reports `verified=true`, `reason=valid`; and the message has a standalone DCO trailer. No post-merge `main` run was allocated. The branch was pruned remotely and deleted locally. |
| Repository/history/release baseline audit | 0 | Clean local `main`, `origin/main`, and `origin/HEAD` all resolved to `49fba13477890bf6bf1c9e6a645e669b3a69492f`; only `main` existed locally/remotely, no PR, local/remote tag, or GitHub release existed, and `git fsck --full --no-dangling` passed. A read-only administrative query reported immutable releases `enabled=false`, `enforced_by_owner=false`; M40 does not change that setting. |
| Baseline lock and release focus | 0 | The unchanged lock resolved 46 packages in 0.84 ms; all 30 inherited release-artifact, release-ref, release-workflow, M38, and M39 tests passed in 6.67 seconds. Baseline CI SHA-256 was `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`; release workflow was `fd18b22b4363f183bc986bd013db7a139502f93d103725f429a62219f9ce61ca`; pyproject and lock remained `42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1` and `e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed`. |
| Current primary draft-release direction | 0 | Official GitHub documentation recommends draft/attach/publish ordering for immutable-release compatibility; the CLI documents that asset-bearing `gh release create` already uses separate internal draft/upload/publish calls; and the REST release schema reports each asset's uploaded state, byte size, and `sha256:` digest. M40 exposes that ordering so repository-owned validation can compare the authenticated draft with local staging before publication, without enabling immutable releases. |
| Initial draft-validator gate | Mixed | Focused formatting and Ruff passed. Strict Pyright reported three partially unknown list-value diagnostics in the untyped JSON asset array. Seventeen tests passed and one capability test skipped, but the success test used platform-dependent `Path` ordering and failed. No initial type or test-suite pass is claimed. |
| Corrected draft-validator gate | 0 | The JSON array is explicitly narrowed to `list[object]`, and expected output sorts by basename like the validator. Focused formatting/lint passed, strict Pyright reported zero diagnostics, and 18 behavior/adversarial tests passed with one Windows symlink-capability skip in 2.34 seconds. |
| First integrated workflow gate | Mixed | Focused Ruff lint and strict Pyright passed, the release workflow parsed as YAML, and all 33 draft-validator/release-workflow/M38-M40 tests passed with one capability skip in 2.24 seconds. The new M40 architecture file required mechanical Ruff formatting, so no initial format pass is claimed. |
| Corrected integrated workflow gate | 0 | Ruff mechanically formatted the architecture file. Focused format/lint and strict Pyright then passed, and all 33 behavior/workflow/M38-M40 architecture tests passed with one Windows symlink-capability skip in 2.25 seconds. |
| Documentation-integrated gate | 0 | Whole-tree formatting reported 280 files, Ruff passed, focused strict Pyright reported zero diagnostics, strict docs built in 0.91 seconds, all 365 draft-validator plus complete architecture tests passed with one Windows symlink-capability skip in 4.09 seconds, both workflows parsed as YAML, and whitespace passed. |
| Findings-first exact-draft correction | Corrected | Review found that GitHub documents `GET /releases/tags/{tag}` as a published-release endpoint, so it cannot be trusted to return the private draft being verified. The workflow now resolves the explicit draft's numeric database ID through authenticated `gh release view`, rejects an empty/non-decimal ID, and fetches the exact release by ID through the pinned REST API. Architecture coverage forbids the published-by-tag endpoint. No runner, action, permission, dependency, trigger, or publication boundary changed. |
| Corrected post-review focus | 0 | Whole-tree formatting and Ruff passed, focused strict Pyright reported zero diagnostics, the release workflow parsed as YAML, all 34 draft-validator/release-workflow/M38-M40 tests passed with one Windows symlink-capability skip in 2.31 seconds, and whitespace passed. Final release-workflow SHA-256 at this gate is `3983cd82f0201fcac8fe2156f77715e1136998781b428c60a192b3f3a3522871`. |
| Complete M40 CPython 3.12 quality gate | 0 | The unchanged lock resolved 46 packages, exact frozen graphics sync restored 45 packages, whole-tree formatting reported 280 files, Ruff passed, strict Pyright reported zero diagnostics, strict docs built in 0.89 seconds, all 365 validator plus complete architecture tests passed with one Windows symlink-capability skip in 4.45 seconds, and the complete suite passed 1,818 tests with 12 expected skips in 101.99 seconds. |
| Real-wgpu, profile, and vertical-slice gate | 0 | All ten real-wgpu integration tests passed in 6.07 seconds; the two-workload base and three-workload graphics M7 profiles validated; Clockwork Arena reproduced state hash `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`; all five replay batches/tests passed. |
| Complete cross-version compatibility gate | 0 | Exact frozen non-graphics CPython 3.13 passed 1,808 tests with 13 expected skips in 93.40 seconds. Exact CPython 3.14 passed the same counts in 98.05 seconds. Exact CPython 3.12 plus the graphics extra was then restored. |
| Fresh reproducible distribution and release gate | 0 | Three output paths were confirmed absent before use. Two fresh same-source builds matched exactly: the 267,351-byte wheel SHA-256 is `a1a7cf55d515d80481d84d7e48452b43ba4395c3643157f0eb7d2d12c5244a10`; the 925,549-byte sdist SHA-256 is `3e3023e9d74173bce63713c12090d3796e18c00da5137436cc2cd8f18ce82bf7`. Installed-wheel smoke passed, ten artifacts totaling 1,324,128 bytes were staged, complete release smoke passed, and the M40 verifier accepted a synthetic uploaded draft carrying the exact staged names, sizes, and SHA-256 digests. |
| Scope, archive, credential, and Git-object audit | 0 | No diff exists in `src/ludoweave`, `pyproject.toml`, `uv.lock`, or the pull-request CI workflow. The wheel contains only Python/package metadata and no new script or native object; the sdist contains the M40 verifier, RFC, unit tests, and architecture test. Credential-value scanning found no credential/private-key material; the verifier contains no eval, exec, subprocess, shell, socket, request, URL, or network client. Both workflows parsed as YAML, `[retired control directory]` is absent, whitespace passed, and `git fsck --full --no-dangling` passed. CI SHA-256 remains `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`; release workflow is `3983cd82f0201fcac8fe2156f77715e1136998781b428c60a192b3f3a3522871`. |
| Final recorded-tree static and architecture gate | 0 | The unchanged lock resolved 46 packages in 0.78 ms; whole-tree formatting reported 280 files, Ruff passed, strict Pyright reported zero diagnostics, strict docs built in 1.05 seconds, all 365 validator plus complete architecture tests passed with one Windows symlink-capability skip in 6.16 seconds, both workflows parsed as YAML, and whitespace passed. |
| Final recorded-tree complete suite | 0 | The complete exact CPython 3.12 graphics implementation-tree suite passed 1,818 tests with 12 expected skips in 101.70 seconds. |
| Hosted exact-head gate on initial implementation commit | Review finding | Pull request #71 run `31266763465` passed exact head `d3184c06df974ffecf61c55f78f44fb32edae466` in exactly three allocations: Linux job `93126055035` in 6m41s, Windows job `93126750452` in 2m55s, and macOS job `93126750459` in 2m56s. Review then identified that `json.loads` can raise `RecursionError` for pathological nesting or `ValueError` for an integer beyond Python's digit limit; neither was converted into the promised structured failure. No merge is claimed for this head. |
| Corrected pathological-JSON gate | 0 | The parser now preserves intentional duplicate-key failures while converting Unicode, recursion-depth, integer-digit-limit, and ordinary JSON value failures into stable `release_draft.invalid_document` results. Regression cases cover 2,000 nested arrays and a 10,000-digit integer. Focused format/lint/strict typing passed with 25 tests and one Windows symlink skip in 2.81 seconds. Whole-tree formatting reported 280 files, Ruff passed, strict Pyright reported zero diagnostics, strict docs built in 0.95 seconds, all 365 validator plus architecture tests passed with one skip in 4.83 seconds, whitespace passed, and the complete Python 3.12 graphics suite passed 1,818 tests with 12 expected skips in 101.40 seconds. |
| Corrected exact-commit distribution and release gate | 0 | Correction commit `967147b3bbc83414d0ce303845975dea0c4e9d26` has a standalone DCO trailer and a clean tree. Two fresh builds matched exactly: the 267,351-byte wheel SHA-256 is `a1a7cf55d515d80481d84d7e48452b43ba4395c3643157f0eb7d2d12c5244a10`; the 926,814-byte sdist SHA-256 is `34f9100147df9ee565ca2bdd07a8510ad0a900d62d5825a14b0fdcd4f14770d6`. Installed-wheel smoke, complete ten-artifact staging/release smoke, and exact staged synthetic-draft verification all passed. |
| Corrected hosted exact-head gate | 0 | Pull request #71 run `31267396755` passed exact corrected head `967147b3bbc83414d0ce303845975dea0c4e9d26` in exactly three allocations. Linux job `93127664106` passed in 6m43s, macOS job `93128354404` in 2m51s, and Windows job `93128354399` in 3m35s. Classifier output was 31 changed paths and `substantive`. Hosted reproducibility reported a 267,339-byte wheel SHA-256 `108e7387b4b8d98c20f1a9b5a38dd246e8d7b3f14b07ae787167331c4b9001cc` and a 926,797-byte sdist SHA-256 `9364d694b7ef02b4f1b22e79958e98a9d1d6acc7279c167d9b540d4ab00891ec`; installed-wheel and ten-artifact release smoke passed. Ubuntu CPython 3.13 and 3.14 each passed 1,820 tests with one expected skip. |
| Review resolution and squash integration audit | 0 | The one actionable review thread was answered with the exact correction and resolved; final audit reported one resolved/outdated thread with two comments and no unresolved thread. PR #71 squash-integrated as `e9d9850e11f572a1d4ddc78d06c79b23a5584f87`; its sole parent is exact M39 closeout `49fba13477890bf6bf1c9e6a645e669b3a69492f`, tree `974b790ab2d925562185c2c18707f3878b0e7bdd` exactly equals the corrected reviewed head, GitHub reports `verified=true` and `reason=valid`, and the message contains a standalone DCO trailer. No post-merge `main` run was allocated. |
| Post-merge cleanup baseline | 0 | The feature branch was deleted remotely by the merge and locally after tree equality was proven. Clean local `main`, `origin/main`, and `origin/HEAD` all resolve to the M40 squash; only `main` exists locally/remotely, no PR, local/remote tag, or GitHub release exists, and `git fsck --full --no-dangling` passes. |
| Integration-record local gate | 0 | Whole-tree formatting reported 280 files, Ruff passed, strict Pyright reported zero diagnostics, strict docs built in 0.94 seconds, all 347 architecture tests passed in 2.65 seconds, and whitespace passed for the four-path documentation record. |
| Integration-record hosted gate | 0 | Pull request #72 exact head `bf3ca2a02b4699e7fe3ab80e4fb92bb983ceb43a` classified four changed paths as documentation. Run `31268048294` allocated only Linux job `93129285124`, which passed in 35 seconds; desktop umbrella job `93129362731` skipped with zero steps and no runner. The PR had no review, comment, or thread. |
| Integration-record squash and cleanup audit | 0 | PR #72 squash-integrated as `67d03d41430dc24bf81a894752b3641de8e521ed`; its sole parent is feature squash `e9d9850e11f572a1d4ddc78d06c79b23a5584f87`, tree `896461bbfd43975ca1ee49962409d9b38695c10f` exactly equals the reviewed record head, GitHub reports `verified=true` and `reason=valid`, and the message contains a standalone DCO trailer. No post-merge `main` run was allocated. The record branch was deleted locally/remotely; before the closeout branch, only clean synchronized `main` remained and full Git object checking passed. |

## M39 development evidence - 2026-08-09, Windows, CPython 3.12

| Command or check | Exit | Result |
| --- | ---: | --- |
| Repository/history/release baseline audit | 0 | Clean synchronized `main`, `origin/main`, and `origin/HEAD` at `185e206d6b9c1e97512e289bcba84701dc29c147`; only `main` existed locally/remotely, no PR or issue was open, no local/remote tag existed, all M38 branches were deleted, and `git fsck --full --no-dangling` passed. |
| Baseline lock and release focus | 0 | The unchanged lock resolved 46 packages in 0.89 ms; all ten inherited release-workflow, release-artifact, and M38 boundary tests passed in 0.66 seconds. Baseline CI SHA-256 was `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`; release workflow was `fa6c60642946cc0350f3d2fb78d6918efc4a1ba6f27b54de9f53de3a156c85ae`; pyproject and lock remained `42a7363b8b86a9fb875e48f4e07a071d90e8b1a7ce11865414b17b20adaa2ab1` and `e2c7b4c801e59dba77a6c0cc6efc45e27d0baa466d17c2e5ed76c0dd27ea11ed`. |
| Current primary release-ref direction | 0 | Official Git documentation distinguishes signed/annotated release tags from lightweight labels. GitHub documents that `gh release create --verify-tag` checks only remote tag existence, its Git-tag API exposes annotated objects and signature-verification state, Actions tag-push `GITHUB_SHA` is the tip commit, and checkout requires `fetch-depth: 0` for all history/tags. The M39 disposition is GitHub signature verification plus independent local identity/ancestry checks inside the existing tag job. |
| Initial verifier behavior and static gate | Mixed | Ruff formatting and lint passed and all 15 valid/adversarial tests passed in 4.83 seconds. Strict Pyright reported one unknown dictionary-key type in the JSON object validator, so no initial type pass is claimed. |
| Corrected verifier focused gate | 0 | The JSON object validator now narrows untyped dictionaries before checking keys; local tag failures preserve a specific reason code; and the `origin/main` ref is SHA-validated instead of compared with itself. Format/lint passed, strict Pyright reported zero diagnostics, and all 15 tests passed in 5.18 seconds. |
| First integrated workflow gate | 0 | The release workflow YAML parsed; focused format/lint and strict Pyright passed; all 23 verifier, release-workflow, and M38 boundary tests passed in 4.95 seconds. |
| First documentation-integrated gate | Mixed | Whole-tree formatting and Ruff passed, strict docs built in 0.95 seconds, all 28 focused tests passed in 5.66 seconds, and whitespace passed. Whole-project Pyright alone reported 17 missing/unknown optional graphics imports because the M38 documentation closeout had intentionally removed the six graphics-extra packages. No whole-project type pass is claimed from that environment. |
| Corrected graphics environment and complete architecture gate | 0 | Frozen graphics sync restored the six exact optional packages. Whole-project strict Pyright then reported zero diagnostics. Whole-tree formatting reported 277 files, Ruff passed, strict docs built in 0.94 seconds, all 359 release-ref unit plus complete architecture tests passed in 7.96 seconds, and whitespace passed. At this gate CI SHA-256 remained `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`; release workflow was `e702c085466b79cadcaa3ef1fa37d4374aea672c045f870091a4e2e6ab72225e`. |
| Complete M39 CPython 3.12 quality gate | 0 | The unchanged lock resolved 46 packages, exact graphics sync checked 45 packages, whole-tree formatting reported 277 files, Ruff passed, strict Pyright reported zero diagnostics, and the complete suite passed 1,796 tests with 11 expected skips in 111.13 seconds. |
| Fresh distribution and release gate | 0 | Strict docs built in 0.94 seconds. Confirmed-absent output directories received two matching builds: the 267,124-byte wheel SHA-256 is `c0cae9269d9f75d84b991e00adaddf929a89d148a46064aad14077eb427edee7`; the 904,583-byte sdist SHA-256 is `ceecf76d0166bc92accb87c03348ba2fcf8cce73522b6215700cbabb1a23917d`. Installed-wheel smoke, complete ten-artifact staging/release smoke, workflow YAML parsing, and whitespace passed. |
| Real-wgpu, profile, and vertical-slice gate | 0 | All ten wgpu integration tests passed in 6.79 seconds; the two-workload base and three-workload graphics M7 profiles validated; Clockwork Arena reproduced state hash `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`. |
| Complete cross-version compatibility gate | 0 | Exact frozen non-graphics CPython 3.13 passed 1,786 tests with 12 expected skips in 94.41 seconds. Exact CPython 3.14 passed the same counts in 100.56 seconds. |
| Findings-first early-sync correction | Corrected | Review found that the pre-sync version/ref steps still used `uv run`, which may synchronize a fresh project environment before the tag is admitted. Both standard-library checks now use setup Python directly, and the architecture test forbids `uv run` in the ref step. No runner, action, permission, dependency, lock, or behavior boundary changed. |
| Findings-first trusted-verifier correction | Corrected | A second review found that executing the not-yet-admitted tag checkout's verifier needlessly trusted the candidate ref. The workflow now materializes `scripts/verify_release_ref.py` from fetched `origin/main` and executes that runner-temporary copy. RFC, architecture, release, and security docs explicitly preserve the remaining operational limit: an already-authorized actor able to replace the workflow itself is outside this self-check. |
| Corrected findings focus | 0 | Exact CPython 3.12 plus the 45-package graphics environment was restored. Whole-tree formatting, Ruff, and strict Pyright passed; all 23 verifier/current release-workflow/M39 architecture tests passed in 6.30 seconds; release YAML parsed; and whitespace passed. Final release-workflow SHA-256 is `fd18b22b4363f183bc986bd013db7a139502f93d103725f429a62219f9ce61ca`. |
| Final post-review static and architecture gate | 0 | The unchanged lock resolved 46 packages in 1 ms; whole-tree formatting reported 277 files, Ruff passed, strict Pyright reported zero diagnostics, strict docs built in 0.89 seconds, all 359 verifier plus complete architecture tests passed in 9.46 seconds, both workflows parsed as YAML, and whitespace passed. |
| Final post-review complete suite | 0 | The complete exact CPython 3.12 implementation-tree suite passed 1,796 tests with 11 expected skips in 99.26 seconds. |
| Post-review distribution and release gate | 0 | Three output paths were confirmed absent before use. Two fresh builds matched: the 267,124-byte wheel SHA-256 is `c0cae9269d9f75d84b991e00adaddf929a89d148a46064aad14077eb427edee7`; the 906,375-byte sdist SHA-256 is `3644ca467290f8dbe681e494fdb71d53241f2f7a853204df621ca05fde231112`. Installed-wheel smoke, complete ten-artifact staging/release smoke, and whitespace passed. The subsequently appended factual evidence rows are Markdown-only and are not claimed as part of that archive identity. |
| Scope, archive, credential, and Git-object audit | 0 | No diff exists in `src/ludoweave`, `pyproject.toml`, `uv.lock`, or the CI workflow. The 94-entry wheel has no native/WASM file. The 439-entry sdist contains the M39 verifier, RFC, unit tests, and architecture tests. Credential-pattern scanning matched only expected workflow token-context vocabulary and found no credential value/private key; the verifier contains no eval, shell subprocess, socket, request, or URL client. Whitespace and `git fsck --full --no-dangling` passed. |
| Exact committed-tree distribution/release smoke | 0 | Feature commit `f71d8ddbf816873cf9af8ea6538112ff0e75553e` built a 267,124-byte wheel at SHA-256 `c0cae9269d9f75d84b991e00adaddf929a89d148a46064aad14077eb427edee7` and a 906,696-byte sdist at SHA-256 `23ca5d525dd0ea193e66f3cce9a0ccae74a43d6ba2f0653afa709eabcc561b4c`; installed-wheel and complete ten-artifact release smoke passed. Trusted-base classification reported 31 changed paths, `classification=substantive`, and `substantive=true`. |
| Hosted exact-head gate | 0 | Pull request #68 run `31264314307` passed exact head `f71d8ddbf816873cf9af8ea6538112ff0e75553e` in exactly three allocations. Linux job `93119879683` passed in 6m43s before macOS/Windows began; macOS `93120568487` passed in 2m33s and Windows `93120568501` in 3m30s. Linux passed the full baseline, graphics/profile/sample, distribution, installed-wheel, release-candidate, and CPython 3.13/3.14 gates. Its build reported a 267,110-byte wheel at SHA-256 `b09d2727d39ae8b750f6aa9f13035cad34477d287eab07eb5ee52341221cd02a` and a 906,680-byte sdist at SHA-256 `ef6e4fbf6f05d664a0311249c46106b0001b949a16373025dec171e60cca4314`; staging reported ten artifacts and release smoke passed. |
| Hosted review and squash audit | 0 | PR #68 was clean and mergeable with three passing checks, no review decision, review, comment, or review thread. Squash `4e30b4bf3b911270ab4e1bd117d49ca0d090a0a7` has sole parent `185e206d6b9c1e97512e289bcba84701dc29c147`; tree `e08a1956e1b6ec9005b1455c5020ee716f6fbdef` exactly equals the reviewed feature tree. GitHub reports signature verification `verified=true`, `reason=valid`; the message contains a standalone DCO trailer. No post-merge `main` run was allocated. The feature branch was pruned remotely and deleted locally after exact-tree comparison. |
| First integration-record documentation lane | Environment-blocked | The managed filesystem sandbox denied access to uv's existing user cache before any lock, sync, formatting, lint, docs, or test command ran. No quality pass is claimed from that invocation; the final `git diff --check` command produced no finding. |
| Approved integration-record documentation lane | 0 | The unchanged lock resolved 46 packages; docs-only sync removed the six graphics-extra packages; whole-tree formatting reported 277 files, Ruff passed, strict docs built in 0.92 seconds, all 343 architecture tests passed in 2.28 seconds, and whitespace passed. |
| Final integration-record documentation lane | 0 | Against the final four-path record content before this factual row, the unchanged lock resolved 46 packages, exact docs sync checked 39 packages, whole-tree formatting reported 277 files, Ruff passed, strict docs built in 0.91 seconds, all 343 architecture tests passed in 1.99 seconds, and whitespace passed. This appended Markdown-only evidence row is not claimed as part of that exact invocation. |
| Hosted public integration-record gate | 0 | PR #69 exact head `774180c7cb87739e83a36b0bcb4571aded18b017` passed run `31265044941`. Trusted-base classification reported four paths and `classification=documentation`. The only runner allocation was Linux job `93121720961`, which passed in 33 seconds including lock, formatting, lint, strict docs, all architecture tests, distribution build, installed-wheel smoke, ten-artifact staging, and release smoke. Desktop umbrella `93121781802` was skipped with zero steps and no matrix runner. |
| Public integration-record review and squash audit | 0 | PR #69 was clean and mergeable with its Linux check passing, desktop umbrella skipped, and no review decision, review, comment, or review thread. Squash `166dcb2dc619dbc721207eece273c0fd9437f9ff` has sole parent `4e30b4bf3b911270ab4e1bd117d49ca0d090a0a7`; tree `1071165a0bf41397dfbeee38b09eee606299686e` exactly equals the reviewed record tree. GitHub reports signature verification `verified=true`, `reason=valid`; the message contains a standalone DCO trailer. No post-merge `main` run was allocated, and the record branch was pruned remotely and deleted locally. |
| Pre-closeout clean-main audit | 0 | Clean local `main`, `origin/main`, and `origin/HEAD` all resolved to `166dcb2dc619dbc721207eece273c0fd9437f9ff`; only `main` existed locally and remotely, no pull request was open, and `git fsck --full --no-dangling` passed before the `.project`-only closeout branch was created. |

## M38 development evidence - 2026-08-08 to 2026-08-09, Windows, CPython 3.12

| Command or check | Exit | Result |
| --- | ---: | --- |
| Repository/history/hosted baseline audit | 0 | Clean synchronized `main`, `origin/main`, and `origin/HEAD` at `3578da64b2686cd8d63340aeb1eed30f5c4cb761`; only `main` existed locally/remotely, no PR or issue was open, all M37 branches were deleted, and `git fsck --full --no-dangling` passed. |
| Baseline lock and release/CI focus | 0 | The unchanged lock resolved 46 packages in 0.88 ms; all 17 inherited release-artifact, release-workflow, M36, and M37 architecture tests passed in 0.80 seconds. |
| Two independent clean-source builds | 0 | Fresh `.tmp/m38-repro-a` and `.tmp/m38-repro-b` each received one universal wheel and sdist. Both wheels are 266,543 bytes with SHA-256 `bccd986ef625342167f45a49d9d7837fd9137c97ec796026d2cb546b659b2eed`; both sdists are 882,315 bytes with SHA-256 `12a61a083cce7bbe318f9ff12c3d0cd9a55bf50f1ee5eb7c8c32c6cda58dbdaa`. |
| Current primary packaging direction | 0 | Official Hatch documentation states that supported build targets are reproducible by default, use `SOURCE_DATE_EPOCH` when set, and otherwise use an unchanging default. GitHub documents attestations as provenance that binds artifacts to build identity. The M38 disposition is to enforce byte equality without changing the existing attestation boundary. |
| Initial verifier focused gate | Mixed | Ruff lint and strict focused Pyright passed. Ruff formatting required one mechanical reformat. Seven of nine tests passed; two assertions incorrectly expected sdist-before-wheel ordering and a cross-directory name mismatch before per-directory completeness validation. No initial format or test-suite pass is claimed. |
| Corrected verifier focused gate | 0 | Ruff formatted the verifier, lint and strict focused Pyright passed, and all nine valid/mismatch/directory/artifact-name tests passed in 0.84 seconds. |
| Real-artifact verifier invocation | 0 | The new verifier emitted `ludoweave.distribution-reproducibility/1`, `status=pass`, and the exact two baseline artifact sizes/SHA-256 identities. |
| First combined workflow/release/architecture gate | Mixed | Formatting and Ruff lint passed; all 349 verifier, release, and architecture tests passed in 3.17 seconds. Whole-project Pyright reported 17 missing/unknown optional graphics imports because M37's documentation-lane validation had intentionally removed the graphics extra. No whole-project type pass is claimed from this environment. |
| Corrected strict typing environment and gate | 0 | Frozen graphics sync restored the six exact optional packages; whole-project strict Pyright then reported zero errors, warnings, or information findings. |
| First documentation-integrated gate | Mixed | Ruff lint, strict Pyright, strict docs, YAML parsing, and whitespace passed; 349 focused tests passed with one Windows symlink-capability skip. The M38 architecture file still required formatting and its RFC assertion expected an absent exact `same-source` term, so no format or focused-suite pass is claimed. |
| Second documentation-integrated gate | Mixed | Mechanical formatting, whole-tree format/lint, strict Pyright, and strict docs passed; 349 focused tests again passed with the symlink skip, but a second prose assertion did not normalize a wrapped `no additional runner allocation` phrase. No focused-suite pass is claimed from this invocation. |
| Corrected documentation focus | 0 | The assertion now normalizes Markdown whitespace; all 14 verifier/M38 architecture tests passed with one Windows symlink-capability skip in 1.10 seconds, and focused format/lint passed. |
| Complete M38 local quality gate | 0 | The unchanged lock resolved 46 packages, exact graphics sync checked 45 packages, whole-tree formatting reported 274 files, Ruff passed, strict Pyright reported zero diagnostics, the complete suite passed 1,774 tests with ten expected skips in 95.85 seconds, strict docs built in 0.94 seconds, and whitespace passed. |
| First final artifact command group | Mixed | Both requested output paths were absent; the primary `uv build` wrote the current pair into shared `dist`, but the verifier correctly rejected that directory because it also retained an older `0.1.0.dev0` pair. Installed-wheel smoke, fresh ten-artifact staging, and release smoke passed, but no complete reproducibility/artifact gate is claimed from this layout. |
| Corrected dedicated-directory artifact gate | 0 | Three fresh output paths were confirmed absent. Independent `.tmp/m38-corrected-first` and `-second` builds matched exactly: the 266,811-byte wheel SHA-256 is `1831f7cb5c1a5cca9a79f8352a46c999ba61ce7c910389d49d22d50b3c5953c7`; the 890,594-byte sdist SHA-256 is `943206b2c1de8e59c9428ed6a4b660554995a1ffa63f9f82e86797eeb99f3c03`. Installed-wheel smoke, fresh ten-artifact staging, and complete release smoke passed from the verified primary directory. CI/release workflows now use two dedicated fresh directories and never compare or publish from shared `dist`. |
| Final archive and focused boundary audit | Mixed | The wheel has 94 entries and no native/WASM file; the 435-entry sdist contains the verifier, RFC-0021, and both new test modules. All 350 verifier/release/architecture tests passed with one symlink-capability skip in 3.53 seconds; Ruff lint, strict Pyright, strict docs, and whitespace passed. The M38 architecture file needed one final mechanical format, so no format pass is claimed from this invocation. |
| Corrected final static and affected boundary gate | 0 | The final file was formatted; whole-tree formatting reported 274 files, Ruff passed, strict Pyright reported zero diagnostics, all 29 affected M36-M38 workflow/verifier tests passed with one Windows symlink-capability skip in 0.99 seconds, and whitespace passed. Final CI SHA-256 is `258216325687f59fda44763f875000ef91a5790098ae8b92b2207436dab95946`; release-workflow SHA-256 is `fa6c60642946cc0350f3d2fb78d6918efc4a1ba6f27b54de9f53de3a156c85ae`. |
| Final post-documentation gate | 0 | The unchanged lock resolved 46 packages in 0.95 ms; whole-tree formatting reported 274 files, Ruff passed, strict Pyright reported zero diagnostics, all 350 verifier/release/architecture tests passed with one Windows symlink-capability skip in 3.06 seconds, strict docs built in 0.91 seconds, both workflows and MkDocs configuration parsed as YAML, and whitespace passed. |
| Final cross-version-name regression gate | 0 | A distinct but individually valid second artifact version now proves cross-directory name comparison fails closed. Focused format/lint, whole-project strict Pyright, and all 351 verifier/release/architecture tests passed with the one Windows symlink-capability skip in 3.14 seconds; whitespace passed. |
| Post-review verifier hardening and final focused gate | 0 | Review added structured directory-enumeration failure and rejected an empty normalized package-version identity. The unchanged lock resolved 46 packages in 0.69 ms; whole-tree formatting reported 274 files, Ruff passed, strict Pyright reported zero diagnostics, all 352 verifier/release/architecture tests passed with the Windows symlink-capability skip in 3.21 seconds, strict docs built in 0.89 seconds, workflow/MkDocs YAML parsed, whitespace passed, and `git fsck --full --no-dangling` passed. |
| Exact reviewed-tree artifact gate | 0 | Three final output paths were confirmed absent. Independent `.tmp/m38-reviewed-first` and `-second` builds matched exactly: the 266,811-byte wheel SHA-256 is `1831f7cb5c1a5cca9a79f8352a46c999ba61ce7c910389d49d22d50b3c5953c7`; the 891,956-byte sdist SHA-256 is `1b8f98bdafa35ecff381a4939522c67db2e1ab00875654044402d2323b215c69`. Installed-wheel smoke, fresh ten-artifact staging, and complete release smoke passed. The 94-entry wheel contains no native/WASM file; the 435-entry sdist contains the verifier, RFC-0021, and both new test modules. |
| First exact committed classifier invocation | 1 | A guessed full head SHA was not an object, so Git rejected the three-dot comparison and the classifier failed closed. No classification is claimed from that command. The corrected exact-base/exact-head invocation classified all 32 feature paths as `substantive=true`. |
| Initial PR #65 hosted run `31261251937` | 0 | Exact initial head `0974fdaec59d76140b0a099d734ddf2abbf92abf` passed exactly three allocations: Linux in 6m48s, Windows in 3m22s, and macOS in 1m50s. The hosted verifier passed same-source byte equality. This result predates the review correction and is retained as development evidence, not the final accepted gate. |
| PR #65 review correction | Corrected | Review found that a supported symlink loop raises `RuntimeError` from `Path.resolve(strict=True)`, escaping the versioned JSON boundary. The verifier now treats `OSError` and `RuntimeError` as `distribution.invalid_directory`. Focused format/lint and strict Pyright passed; the unit file passed 11 tests with two Windows symlink-capability skips, and the combined unit/M38 architecture gate passed 16 tests with those two skips. DCO commit `4f3db7446c842df4f36d7cc8f8321a89bbe5997f` changed only the exception boundary and its regression. |
| Corrected PR #65 hosted run `31261807768` | 0 | Exact final head `4f3db7446c842df4f36d7cc8f8321a89bbe5997f` passed exactly three allocations. Linux passed every classification, lock, format, lint, type, docs, complete CPython 3.12/3.13/3.14, graphics, profiling, vertical-slice, two-build comparison, wheel, staging, and release-smoke step in 6m50s. Only then were macOS and Windows allocated; all their graphics/example/3.14 steps passed in 1m59s and 3m44s. |
| Hosted reproducibility protocol | 0 | Linux emitted `ludoweave.distribution-reproducibility/1` with `status=pass`. Each same-source build produced a 266,797-byte `ludoweave-0.1.0a1-py3-none-any.whl` at SHA-256 `6c43bb79ed5de115ee645f1c8a9b4e8338f364c5bb1f53e08cde58e82e9afe06` and an 892,185-byte `ludoweave-0.1.0a1.tar.gz` at SHA-256 `8f21585819f76f289887a6194e44bcf06b72497d70d13451326cc778e48e4f8a`. This is same-source/same-job equality only, not cross-platform, hermetic, independently rebuilt, provenance, or publication evidence. |
| Final PR #65 review and DCO audit | 0 | GitHub reported exact base `3578da64b2686cd8d63340aeb1eed30f5c4cb761`, exact head `4f3db7446c842df4f36d7cc8f8321a89bbe5997f`, `MERGEABLE`, and `CLEAN`. Both source commits contain exact maintainer DCO trailers. The sole review thread is resolved and outdated; no unresolved thread remains. |
| PR #65 squash integration audit | 0 | PR #65 merged at `2026-08-08T14:35:07Z` as GitHub-signature-verified squash `9f6ca61ccb1f9b7e0796e5cc60c7dd38e6af99d7`, with sole parent exact base and tree `1a96d02b8b23410732fc7ac746179459a14d3f44` exactly equal to the corrected feature head. The squash has a parsed DCO trailer. An initial unquoted PowerShell `^{tree}` invocation was mangled and failed without changing state; the corrected quoted tree comparison passed. The feature branch is deleted locally and remotely. |
| Post-merge CI quota audit | 0 | `gh run list --branch main` contained no run for squash `9f6ca61ccb1f9b7e0796e5cc60c7dd38e6af99d7`; the latest listed main run remained pre-M34 run `31226750474`. The PR-only workflow therefore allocated no redundant post-merge runner. |
| First local documentation-record gate | Not executed | Every uv-backed command was blocked before project execution because the sandbox could not read the existing managed uv cache. PowerShell continued through the semicolon-separated group and the final standalone whitespace check returned zero; no lock, sync, static, docs, architecture, build, reproducibility, wheel, or release pass is claimed from that group. |
| Corrected local documentation-record gate | 0 | With approved access to the existing cache, the unchanged lock resolved 46 packages, the no-graphics environment removed six optional packages, whole-tree formatting reported 274 files, Ruff passed, strict docs built in 0.95 seconds, and all 339 architecture tests passed in 2.13 seconds. Two fresh builds matched: the 266,811-byte wheel SHA-256 is `1831f7cb5c1a5cca9a79f8352a46c999ba61ce7c910389d49d22d50b3c5953c7`; the 893,458-byte sdist SHA-256 is `ec5b1300ec7d707c94899e16739b96a7ebf71e8e38ade3b15cf2c9ca7cfa0203`. Isolated-wheel and complete ten-artifact release smoke passed, as did whitespace. |

## M38 documentation-only hosted proof and closeout - 2026-08-09

| Command or check | Exit | Result |
| --- | ---: | --- |
| First committed record-classifier invocation | 2 | The invocation omitted the required `--github-output` argument, so argument validation exited before classification. No result is claimed from that attempt. |
| Corrected committed record-classifier invocation | 0 | Against exact base `9f6ca61ccb1f9b7e0796e5cc60c7dd38e6af99d7` and head `d4d02bb8dae9f0524f923f40bfa338e99c0db09a`, the trusted classifier reported four paths, `classification=documentation`, and `substantive=false`. The paths were `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md`. |
| PR #66 documentation-lane hosted proof | 0 | Run `31262609814` passed exact head `d4d02bb8dae9f0524f923f40bfa338e99c0db09a`. Linux job `93115649996` passed trusted classification, lock, no-graphics sync, format, lint, strict docs, 339 architecture tests, two-build comparison, installed wheel, staging, and release smoke in 32 seconds. All substantive-only steps skipped. |
| Desktop quota proof | 0 | GitHub skipped desktop matrix umbrella `93115706948` in zero seconds before matrix expansion. It had no checkout, setup, test, or other runner step and allocated no Windows/macOS runner. Exactly one hosted allocation was consumed by the record PR. |
| Final PR #66 review audit | 0 | GitHub reported exact base `9f6ca61ccb1f9b7e0796e5cc60c7dd38e6af99d7`, exact head `d4d02bb8dae9f0524f923f40bfa338e99c0db09a`, `MERGEABLE`, and `CLEAN`, with one successful Linux check, one skipped desktop umbrella, and no comment, review, or review thread. The record commit contains the exact maintainer DCO trailer. |
| PR #66 squash integration audit | 0 | PR #66 merged at `2026-08-08T14:43:34Z` as GitHub-signature-verified squash `42046d521242147cc5ed56874238d25de9870316`, with sole parent exact feature squash and tree `0776afee4c20884240cd4828095ac3b03ae46423` exactly equal to the reviewed record head. The squash has a parsed DCO trailer. The remote and local record branches were deleted. |
| Final main-run quota audit | 0 | `gh run list --branch main` contained no run for record squash `42046d521242147cc5ed56874238d25de9870316`; the latest listed main run remained pre-M34 run `31226750474`. Both M38 merges therefore consumed no redundant main runner. |

## M37 development evidence - 2026-08-08, Windows, CPython 3.12

| Command | Exit | Result |
| --- | ---: | --- |
| Repository/history/hosted baseline audit | 0 | Clean synchronized `main`, `origin/main`, and `origin/HEAD` at `46ef98447706c94763a236841a38c2dbb5b444ca`; only `main` existed locally/remotely, no PR was open, M36 branches were deleted, and `git fsck --full --no-dangling` passed. M36 run `31232803658` passed exactly three allocations; both verified M36 squash commits are integrated. |
| First `uv lock --check` | 1 | The sandbox could not initialize the existing managed uv cache. No lock pass is claimed. |
| Corrected `uv lock --check` | 0 | With approved access to the existing managed cache, the unchanged lock resolved 46 packages in 0.74 ms. |
| Focused workflow baseline | 0 | All 34 inherited M34-M36 workflow/release boundary tests passed in 1.41 seconds. |
| Current official GitHub direction scan | 0 | Official GitHub documentation states that conditionally skipped jobs report success, `needs` gates dependent jobs, path-skipped workflows can leave required checks pending, and Actions metrics expose job/runtime usage. The advisory disposition is trusted-base in-workflow qualification; no project authority came from the sources. |
| Initial classifier behavior gate | Mixed | All 25 classifier tests passed in 0.47 seconds and Ruff lint passed. Formatting check required two mechanical reformats; strict Pyright found one redundant test cast. No initial formatting/type pass is claimed. |
| Corrected classifier static and behavior gate | 0 | Both classifier/test files were formatted; Ruff passed; strict Pyright reported zero diagnostics; the 25 classifier tests plus nine inherited M36/release tests passed, 34 total, in 0.49 seconds. |
| First combined workflow/docs gate | Mixed | All 65 focused M34-M37 workflow/release/classifier tests passed in 0.73 seconds; Ruff lint, strict Pyright, strict docs, YAML parsing, and whitespace passed. The new M37 architecture file still required Ruff formatting, so no combined format pass is claimed. |
| Corrected combined workflow/docs gate | 0 | All three M37 Python files were formatted; Ruff and strict Pyright passed; all 65 focused tests passed in 0.71 seconds; whitespace remained clean. |
| Documentation-only environment transition and first lock | Mixed | Frozen all-group sync removed the six optional graphics packages. Formatting reported 271 files, Ruff lint passed, strict docs built in 0.91 seconds, all 334 architecture tests passed in 1.93 seconds, and whitespace passed. The sandboxed lock check could not read the managed cache, so no lock pass is claimed from that attempt. |
| Corrected documentation-only gate | 0 | The approved identical lock check resolved 46 packages in 0.79 ms. The universal wheel/sdist built, isolated-wheel smoke passed, confirmed-absent `.tmp/m37-docs-lane` received ten artifacts, and complete release smoke passed without graphics installed. |
| Initial substantive static and focused gate | Mixed | Managed CPython 3.13/3.14 were present. Formatting reported 271 files, Ruff and strict Pyright passed, strict docs built, YAML parsed, all 65 focused tests passed in 0.81 seconds, and whitespace passed. The sandboxed lock check was cache-blocked; its approved identical retry resolved 46 packages in 0.80 ms. |
| Initial complete substantive suites | 0 | With the exact 3.12 graphics environment, 1,755 tests passed with nine skips in 92.24 seconds. Exact frozen environment replacement then passed 1,745 tests with ten skips on CPython 3.13 in 82.32 seconds and the same counts on CPython 3.14 in 87.18 seconds. |
| Graphics, profile, and vertical-slice gate | 0 | Restored the exact 45-package CPython 3.12 graphics environment; all ten real-wgpu tests passed in 9.46 seconds; two-workload base and three-workload graphics M7 profiles validated; Clockwork Arena and Agent World Builder reproduced their M36 state/capture hashes. The universal build, isolated wheel, and confirmed-absent ten-artifact `.tmp/m37-substantive-final` release candidate passed. |
| Findings-first executable-doc correction | Corrected | Review found that admitting every `docs/**` path plus `mkdocs.yml` could let a candidate add an executable MkDocs hook under the smaller gate. The classifier now admits only Markdown below `docs/`/`.project`, treats `mkdocs.yml` and non-Markdown inputs as substantive, and restricts issue forms to Markdown/YAML. The first correction gate passed 36 tests, Ruff, strict Pyright, strict docs, and whitespace, but the architecture test required formatting; no corrected format pass is claimed from that attempt. |
| Final corrected static and focused gate | 0 | Whole-tree formatting reported 271 files, Ruff passed, strict Pyright reported zero diagnostics, strict docs built in 0.94 seconds, all 70 focused M34-M37 workflow/release/classifier tests passed in 0.76 seconds, and whitespace passed. |
| Final corrected cross-version tests | 0 | The complete final 3.12 suite passed 1,760 tests with nine skips in 93.38 seconds. The focused hardened classifier/boundary gate passed 36 tests on CPython 3.13 in 1.20 seconds and CPython 3.14 in 0.88 seconds after their earlier complete-suite passes. |
| Final corrected artifact gate | 0 | Restored exact CPython 3.12 plus graphics, rebuilt the universal wheel/sdist, passed isolated-wheel smoke, staged ten artifacts in confirmed-absent `.tmp/m37-reviewed-final`, and passed complete release smoke. The wheel contains 94 entries and no native/WASM file; the 431-entry sdist contains the M37 classifier, RFC, unit tests, and architecture tests. |
| Final static, scope, package, credential, identity, and Git-object audit | 0 | The unchanged 46-package lock resolved in 0.96 ms; whole-tree formatting reported 271 files; Ruff and strict Pyright passed; strict docs built in 1.00 second; all 70 focused tests passed in 1.14 seconds; YAML and whitespace passed. No diff exists in `src`, `benchmarks`, `pyproject.toml`, `uv.lock`, or `release.yml`. CI SHA-256 is `e162010dddab856dd0621957b88efaec6ab20bc6cace1116a842226da4431223`; release SHA-256 remains `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`; lock SHA-256 remains `e2c7b4c801e59dba77a6c0cc6efc45e27d0ba466d17c2e5ed76c0dd27ea11ed`. Credential vocabulary matched only the maintainer checklist; no value pattern was found. New/changed public surfaces contain no retired workflow-marker or non-neutral branch reference; `[retired control directory]`, `[retired control directory]`, `[retired control directory]`, and `[retired control file]` remain absent. `git fsck --full --no-dangling` passed. |

## M37 feature review, correction, hosted validation, and integration - 2026-08-08

| Command or check | Exit | Result |
| --- | ---: | --- |
| Initial PR #62 hosted run `31258685192` | 0 | Exact implementation head `a7db2b88d8394cf2f3a0b73388234daa669de25f` passed three allocations: Linux in 6m36s, Windows in 3m06s, and macOS in 1m45s. Desktop jobs were allocated only after Linux passed. This result predates the review correction and is retained as development evidence, not the accepted final hosted gate. |
| PR #62 review-thread audit | Finding | The automated review identified a real P2 quota defect: the classifier admitted uppercase `.github/PULL_REQUEST_TEMPLATE.md` while the repository tracks lowercase `.github/pull_request_template.md`. The thread URL is retained by PR #62. |
| First focused correction command | Mixed | Ruff formatting and lint passed and strict Pyright reported zero diagnostics. Pytest exited before collection because two requested architecture filenames do not exist; no test pass is claimed for that invocation. |
| Corrected focused command | 0 | `uv run --frozen pytest -q tests/unit/test_ci_change_classifier.py tests/architecture/test_m37_ci_change_qualification.py tests/architecture/test_m36_ci_runner_consolidation.py tests/architecture/test_release_workflow.py` passed all 45 tests in 0.57 seconds. `git diff --check` passed, and DCO commit `8214227c99831310546147977bf354b5ae956bce` changed only the allowlist and matching test fixture. |
| Corrected PR #62 hosted run `31259200818` | 0 | Exact final head `8214227c99831310546147977bf354b5ae956bce` passed. Linux ran every substantive qualification, static, docs, baseline 3.12, Ubuntu 3.13/3.14, graphics, profiling, vertical-slice, build, wheel, and release step in 6m48s. Only after Linux succeeded did Windows and macOS start; they passed their graphics, vertical-slice, and CPython 3.14 steps in 3m40s and 2m45s. Exactly three runner allocations occurred. |
| Final PR #62 review and DCO audit | 0 | GitHub reported exact base `46ef98447706c94763a236841a38c2dbb5b444ca`, exact head `8214227c99831310546147977bf354b5ae956bce`, `MERGEABLE`, and `CLEAN`. Both feature commits contain exact maintainer DCO trailers. The sole review thread is outdated and resolved; no unresolved thread remains. |
| PR #62 squash integration audit | 0 | Squash `407226beae36182d237e32866a86ce19bb93c691` has sole parent `46ef98447706c94763a236841a38c2dbb5b444ca`, exact reviewed tree `91e5b30136febbb5f25a05f36453e03fe6536b4a`, a valid GitHub signature, and a parsed DCO trailer. The feature PR is merged, its local/remote branch is deleted, synchronized main contains the squash, no main-branch run was allocated, and only `main` remained before this record branch. |
| PowerShell-safe squash tree rerun | 0 | An initial unquoted caret/braced tree expression was mangled by PowerShell and produced an ambiguous-revision error. The corrected `git show -s --format=%T` comparison reported `91e5b30136febbb5f25a05f36453e03fe6536b4a` for both reviewed head and squash; their direct diff is empty. |
| First local record-gate command group | 1 | Each uv-backed command was blocked before project execution because the sandbox could not read the existing managed uv cache. No lock, sync, format, lint, docs, or architecture-test pass is claimed from this invocation. |
| Corrected local documentation gate | 0 | With approved access to the existing cache, the unchanged lock resolved 46 packages, the no-graphics all-groups environment removed six optional graphics packages, Ruff formatting reported 271 already-formatted files, Ruff lint passed, strict docs built in 0.98 seconds, all 334 architecture tests passed in 1.93 seconds, and `git diff --check` passed. |
| Local record artifact gate | 0 | `uv build` produced the universal wheel and sdist; isolated-wheel smoke passed; confirmed-absent `.tmp/m37-record-local` received the complete ten-artifact staged candidate; and checksums, manifest, SBOM, safe sample extraction, isolated installation, and bundled evidence release smoke passed. |

At publication, the public M37 integration record was explicitly treated as a
pending documentation-only acceptance fixture. No one-allocation hosted result
or desktop conditional-skip result was claimed before it completed.

## M37 documentation-only hosted proof and closeout - 2026-08-08

| Command or check | Exit | Result |
| --- | ---: | --- |
| First committed record-classifier invocation | 1 | The command used a guessed full head SHA rather than the actual commit SHA. Git rejected the three-dot expression, the classifier failed closed, and no output file or classification was produced. |
| Corrected committed record-classifier invocation | 0 | Against exact base `407226beae36182d237e32866a86ce19bb93c691` and head `06fc5d53b01706b10ceb67f4f6f2f310f2d0b6c6`, the unchanged trusted classifier reported four paths, `classification=documentation`, and `substantive=false`. The paths were `.project/CURRENT_TASK.md`, `.project/PROJECT_STATE.md`, `.project/TEST_EVIDENCE.md`, and `ROADMAP.md`. |
| PR #63 hosted run `31259908552` | 0 | Exact head `06fc5d53b01706b10ceb67f4f6f2f310f2d0b6c6` completed successfully. Linux was the only runner allocation and passed in 32 seconds: trusted classification, unchanged lock, no-graphics docs sync, formatting, lint, strict docs, all architecture tests, universal build, isolated-wheel smoke, release staging, and complete release smoke. Type/full compatibility, graphics, profiles, and vertical slices were correctly skipped for documentation-only scope. |
| PR #63 desktop-allocation audit | 0 | GitHub evaluated the desktop condition before expanding the two-entry matrix. One matrix-umbrella check concluded `skipped` with no steps; no Windows or macOS runner was allocated. This is the hosted representation of both desktop entries being excluded, not two separately expanded skipped checks. |
| Final PR #63 review audit | 0 | GitHub reported exact base `407226beae36182d237e32866a86ce19bb93c691`, exact head `06fc5d53b01706b10ceb67f4f6f2f310f2d0b6c6`, `MERGEABLE`, and `CLEAN`; the pull request had no comments, reviews, or review threads. |
| PR #63 squash integration audit | 0 | Squash `7434f310c86dd9acf6c61ff01c1a5f2dfcdffe31` has sole parent `407226beae36182d237e32866a86ce19bb93c691`, exact reviewed tree `9dc7f0bc50b7b5b8309405ce491978f3ef39cbe4`, a valid GitHub signature, and a parsed DCO trailer. The record PR is merged, its branch is deleted locally/remotely, synchronized main contains the squash, no main-branch run was allocated, and only main remained before this `.project` closeout branch. |

M37 is complete. The two accepted hosted feature runs consumed three runner
allocations for the substantive correction and one for the public
documentation fixture. The final `.project/**` closeout record is excluded by
the existing pull-request path filter and is expected to consume zero hosted
allocations; no run result is pre-claimed here.

## M36 development evidence - 2026-08-08, Windows, CPython 3.12

| Command | Exit | Result |
| --- | ---: | --- |
| Repository/history/hosted baseline audit | 0 | Clean synchronized `main`, `origin/main`, and `origin/HEAD` at `ba9125389ab2b2b760ca7115b5b1b03c447f4190`; only `main` existed locally/remotely, no PR was open, both M35 branches were deleted, and `git fsck --full --no-dangling` passed. |
| M35 hosted topology/timing audit | 0 | Corrected run `31231410432` passed eight allocations: one Ubuntu 3.12 quality/distribution slice, Ubuntu 3.13/3.14 and Windows/macOS 3.14 compatibility slices, and Ubuntu/Windows/macOS 3.12 graphics slices. Checkout and setup executed in every allocation. |
| Focused workflow baseline | 0 | All 25 inherited M34/M35 workflow-boundary tests passed in 0.64 seconds. |
| First `uv lock --check` | 1 | The sandbox could not initialize the existing user uv cache. No lock pass is claimed. |
| Corrected `uv lock --check` | 0 | Using the existing managed cache, the unchanged lock resolved 46 packages. |
| Local Python availability probe | 0 | uv found CPython 3.12 in the project environment and managed CPython 3.13/3.14 interpreters. |
| `git switch -c maintenance/m36-ci-runner-consolidation` | 0 | Created the neutral M36 branch from exact clean base `ba9125389ab2b2b760ca7115b5b1b03c447f4190`. |
| First workflow/docs gate | Mixed | Ruff, strict docs, and whitespace passed; 30 of 31 focused tests passed. The single failure was a prose assertion expecting `five fewer runner allocations` contiguously while README inserted `That is` before the phrase. No focused-suite pass is claimed. |
| Corrected initial workflow/docs gate | 0 | The aligned README wording passed all 31 focused M34-M36 workflow/docs tests in 0.36 seconds. |
| CPython 3.12 graphics environment and smoke | 0 | The frozen all-group graphics sync checked 45 packages; `uv python install 3.13 3.14` confirmed managed compatibility interpreters; all ten real-wgpu tests passed in 6.95 seconds. |
| First sequential CPython 3.13 full test | 1 | The environment transition completed, then 1,713 tests passed with ten expected skips and one failure in 92.97 seconds. `test_release_workflow` still parsed the superseded `verify/tests/graphics` job names. No 3.13 pass is claimed. |
| Corrected CPython 3.13 gate | 0 | The release-workflow architecture test now validates the Linux/desktop topology. Ruff and 34 focused workflow/release tests passed; the complete CPython 3.13 suite passed 1,714 tests with ten expected skips in 93.40 seconds. |
| Sequential CPython 3.14 gate | 0 | The exact frozen environment replacement completed and the complete CPython 3.14 suite passed 1,714 tests with ten expected skips in 101.78 seconds. |
| Restored CPython 3.12 complete suite | 0 | Restored the exact 45-package graphics environment; the complete suite passed 1,724 tests with nine expected skips in 105.48 seconds. |
| Distribution, graphics, profile, and vertical-slice gate | 0 | Built the universal wheel and sdist; isolated-wheel smoke passed; confirmed-absent `.tmp/release-candidate-m36-reviewed` received ten artifacts and release smoke passed; ten real-wgpu tests passed in 6.60 seconds; base and graphics profile artifacts validated; and both deterministic vertical slices reproduced their M35 hashes. |
| Findings-first fail-early refinement | 0 | Operational review moved managed 3.13/3.14 installation immediately after uv setup so interpreter availability fails before expensive quality/build/graphics work. Architecture regressions fix that ordering. Final 268-file formatting, Ruff, strict Pyright, strict docs, YAML parsing, 34 focused tests, and whitespace passed. |
| Scope, workflow, archive, credential, identity, and Git-object audit | 0 | No diff exists in `src/ludoweave`, `benchmarks`, `pyproject.toml`, `uv.lock`, or `release.yml`; the release-workflow SHA-256 remains `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`. Final CI SHA-256 is `ab4d4e5e71e733abfccc20b35944e90dcf9c5cf6dba433f3bdf62a999a1d5fa7`. The 94-entry wheel has no native/WASM payload. Credential-pattern matches were expected test/service vocabulary only; `[retired control directory]`, `[retired control directory]`, `[retired control directory]`, and `[retired control file]` remain absent; `git fsck --full --no-dangling` passed. |
| Final implementation-tree `uv run --frozen pytest -q` | 0 | The complete CPython 3.12 suite passed 1,724 tests with nine expected skips in 106.27 seconds after the fail-early refinement. Only these factual `.project/**` evidence rows were added afterward. Hosted proof remains pending. |
| DCO feature commit and ready PR | 0 | DCO-signed commit `38589bbe6b4c688b581bc972f0ba1e4e39d5cd93`, exact tree `39d29fa863fee46665bf02856f4d9657068b573f`, was pushed and published as ready PR #60 against exact base `ba9125389ab2b2b760ca7115b5b1b03c447f4190`. |
| Hosted consolidation and review audit | 0 | Pull-request run `31232803658` passed exactly three allocations on the exact feature head: Linux quality/compatibility/graphics/distribution in 6m36s, Windows graphics/3.14 compatibility in 3m32s, and macOS graphics/3.14 compatibility in 2m16s. Step-level inspection confirmed every retained slice passed. GitHub reported PR #60 `MERGEABLE` and `CLEAN`, with no top-level comment, review, or review thread. This proves allocation consolidation and retained coverage; it does not claim a billed-minute reduction. |
| PR #60 squash integration audit | 0 | The first merge command was rejected before execution because its proposed DCO identity did not match the configured repository identity; no merge occurred. The corrected command used the exact configured author identity. PR #60 then merged at `2026-08-08T01:38:33Z` as GitHub-signature-verified DCO commit `0b8b39052d79ee9c8a2f909f8ac70045adf5a785`, with sole parent exact base and tree `39d29fa863fee46665bf02856f4d9657068b573f`, exactly equal to the feature tree. The feature branch was deleted locally and remotely. |
| Post-merge CI quota and repository audit | 0 | `gh run list --branch main` listed no run for M36 merge commit `0b8b39052d79ee9c8a2f909f8ac70045adf5a785`; the latest main run remained successful pre-M34 run `31226750474`. No pull request remained open, only synchronized `main` existed locally/remotely before this records branch, the worktree was clean, and full object connectivity inspection reported only expected unreachable historical objects with no corruption error. |

## M35 development evidence - 2026-08-08, Windows, CPython 3.12

| Command | Exit | Result |
| --- | ---: | --- |
| Repository/history/hosted baseline audit | 0 | Clean synchronized `main`, `origin/main`, and `origin/HEAD` at `277de9052e768a5f70d32f1a2f67ec9f93353723`; only `main` existed locally/remotely, no PR was open, `git fsck --full --no-dangling` passed, GitHub reported no branch protection, and M34 pull-request run `31229138742` passed all eight essential jobs. No M34 post-merge or `.project/**`-record run existed. |
| Focused inherited baseline | 0 | 154 existing plugin, installed render/agent/WorldStore conformance, release-artifact, and boundary tests passed in 3.54 seconds. |
| Initial M35 evaluator gate | Mixed | The initial 207-byte empty manifest had SHA-256 `1eb9bcfeec623b25b1c90497bf8f25fb73544082f5e882d64fe69183e3ce21c6`. Ruff passed; strict Pyright reported four redundant test casts; 73 of 74 evaluator tests passed because one direct evaluator assertion expected a JSON list rather than the internal tuple. No type or focused-suite pass is claimed. |
| Corrected initial evaluator gate | 0 | After test-only corrections, formatting and Ruff passed, strict Pyright reported zero diagnostics, and all 74 evaluator tests passed in 2.21 seconds. |
| Reviewed-census contract hardening | 0 | Added an explicit complete project-accepted submission-census review assertion. The final exact empty manifest is 250 bytes with SHA-256 `adee8c68b5d89923ee2682162eb24cd9542a4601b1ff6fb901709ebcc0066767`. |
| First combined architecture/conformance selector | 4 | Ruff, strict Pyright, strict docs, and whitespace passed, but stale M12/M17/M18 architecture filenames caused pytest to collect no tests. No focused-test pass is claimed. |
| Corrected architecture/conformance gate | Corrected | The first actual focused run passed 159 of 160 tests; one RFC did not yet contain the literal milestone identity used by the documentation-boundary test. The single corrected test then exposed an overly brittle support-matrix phrase assertion. After documentation and test-language alignment, all 160 M35, M12, M17-M19, release-artifact, and installed-conformance tests passed in 4.74 seconds. |
| Findings-first public-evidence correction | 0 | Review found that reserved non-public domains and non-wheel HTTPS paths could satisfy the claimed public-wheel locator shape. The validator now rejects RFC-reserved/local/IP authorities and requires `.whl` paths for both implementation and LudoWeave artifacts. Ruff and strict Pyright passed; all 91 focused evaluator/architecture regressions passed in 2.26 seconds. No other pre-publication code, privacy, architecture, or CI-operability finding was identified. |
| First `uv sync --frozen --all-groups --extra graphics` | 2 | The sandbox could not open the existing user uv cache. No environment-sync pass is claimed from this attempt. |
| Corrected `uv sync --frozen --all-groups --extra graphics` | 0 | Using the existing managed cache, uv checked 45 installed packages. |
| First `uv lock --check` | 2 | The sandbox could not open the existing user uv cache. No lock pass is claimed from this attempt. |
| Corrected `uv lock --check` | 0 | The unchanged lock resolved 46 packages. |
| Complete static/docs gate | 0 | `uv run --frozen ruff format --check .` reported 267 files formatted; Ruff passed; strict Pyright reported zero diagnostics; strict MkDocs built in 0.88 seconds with only the known upstream Material notice; and `git diff --check` passed. |
| `uv run --frozen pytest -q` | 0 | 1,716 tests passed with nine expected platform-capability skips in 114.15 seconds. |
| First `uv build` | 2 | The sandbox could not open the existing user uv cache. No build pass is claimed from this attempt. |
| Corrected `uv build` and installed-wheel smoke | 0 | Built `ludoweave-0.1.0a1.tar.gz` and universal `ludoweave-0.1.0a1-py3-none-any.whl`; `uv run --frozen python scripts/smoke_wheel.py dist` passed, including exact installed M35 evidence. |
| Fresh release stage and smoke | 0 | Confirmed `.tmp/release-candidate-m35-reviewed` absent, staged ten deterministic artifacts, and passed checksum, manifest, SBOM, safe-extraction, isolated-installation, and bundled M35 evidence smoke. |
| Real-wgpu and profiling gates | 0 | All ten wgpu integration tests passed in 6.45 seconds. The two-workload base and three-workload graphics M7 profile artifacts both validated under `ludoweave.profile.m7/1`. |
| Deterministic vertical slices | 0 | Clockwork Arena reproduced state hash `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`. |
| Scope, archive, credential, identity, and Git-object audit | 0 | No diff exists in `src/ludoweave`, `benchmarks`, `pyproject.toml`, `uv.lock`, or either workflow. CI SHA-256 remains `3ca17d0e1fad70cd898c90451701ba6733ecfb5235d5c03d898fc9c75bf5871d`; release SHA-256 remains `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`. The 94-entry wheel has no native/WASM file; the 50-entry sample bundle contains the M35 evaluator and exact manifest. Credential-pattern matches were expected command/service vocabulary only; no credential value was found. `[retired control directory]`, `[retired control directory]`, `[retired control directory]`, and `[retired control file]` remain absent, and `git fsck --full --no-dangling` passed. Hosted validation remains pending. |
| DCO feature commit and ready PR | 0 | DCO-signed commit `74da3c169552c658528b3cfeb64ca2f11ae613d0` was pushed and published as ready PR #58 against exact base `277de9052e768a5f70d32f1a2f67ec9f93353723`. One PowerShell audit command misparsed unquoted `^{tree}` syntax and made no repository change; its quoted retry verified the tree and clean worktree. |
| Initial hosted run `31231040437` | Corrected | All eight essential jobs passed on exact head `74da3c169552c658528b3cfeb64ca2f11ae613d0`, but automated review correctly found that the generic identifier grammar disagreed with all three installed conformance runners. IDs without a separator could be admitted and valid underscore IDs could be rejected. No merge-ready claim is made for this head. |
| Review-requested adapter-ID correction | 0 | Implementation and adapter identities now use the exact shared M17-M19 grammar `[a-z][a-z0-9]*(?:[._-][a-z0-9]+){1,15}` and remain equal. Regressions prove underscore admission and separator-free rejection. All 100 focused admission/installed-conformance tests passed in 3.62 seconds; 267-file formatting, Ruff, strict Pyright, whitespace, and strict docs passed; the complete suite passed 1,718 tests with nine skips in 101.99 seconds; all ten real-wgpu tests passed in 6.45 seconds; the rebuilt universal wheel, isolated smoke, and a fresh ten-artifact release candidate passed. Corrected hosted validation remains pending. |
| Corrected hosted validation and review closure | 0 | Pull-request run `31231410432` passed all eight jobs on exact final head `fb0d887eed80a2d96c4b3348d950df371e58db56`: quality/tests/distribution; Ubuntu CPython 3.13/3.14; Windows and macOS CPython 3.14; and Ubuntu/Windows/macOS real graphics. The exact correction evidence was posted to P2 thread `PRRT_kwDOTtqoGs6XbLNk`, which is resolved. GitHub reported PR #58 `MERGEABLE` and `CLEAN`, with no top-level comment and eight successful completed checks. |
| PR #58 squash integration audit | 0 | PR #58 merged at `2026-08-08T01:00:02Z` as GitHub-signature-verified commit `603403967e333342c5ff72222ea3567d3252fd6f`, with sole parent exact base `277de9052e768a5f70d32f1a2f67ec9f93353723` and tree `59c049ebdb957818aba2252c74d5b5f8ef9cb72f`, exactly equal to final feature head `fb0d887eed80a2d96c4b3348d950df371e58db56`. The squash body has a valid standalone `Signed-off-by` trailer. The feature branch was deleted locally and remotely. |
| Post-merge CI quota audit | 0 | `gh run list --branch main` listed no run for M35 merge commit `603403967e333342c5ff72222ea3567d3252fd6f`; the latest main run remained successful pre-M34 run `31226750474`, confirming that the PR-only workflow did not duplicate the validated tree. No pull request remained open, only `main` existed locally/remotely, the worktree was clean, and `git fsck --full --no-dangling` passed. |

## M34 development evidence - 2026-08-08, Windows, CPython 3.12

| Command | Exit | Result |
| --- | ---: | --- |
| Repository/history/hosted baseline audit | 0 | Clean synchronized `main`, `origin/main`, and `origin/HEAD` at `d12c30a02782c0ebf892e27c5daf6e9fec1c93ee`; only `main` existed locally/remotely, no PR was open, `git fsck --full --no-dangling` passed, GitHub reported no branch protection, and post-M33 main run `31226750474` passed all eight jobs. The first sandboxed GitHub query was network-blocked; the read-only escalated query succeeded. |
| First focused baseline attempt | 2 | Repository and Git-object checks completed, but sandboxed uv could not open the existing user cache. No test pass is claimed from this attempt. |
| Corrected focused baseline and branch creation | 0 | 47 inherited agent-service, agent-conformance, and M33 architecture tests passed in 0.91 seconds; created neutral branch `evidence/m34-agent-tool-recovery` from the exact base. |
| M34 manifest identity probe | 0 | Exact 195-byte empty reviewed manifest SHA-256 is `e952c045b039055e8439069cf88176b6ac1d2ad7de49a94d39b2737e5d06e1d5`. |
| First evaluator/static gate | Mixed | Ruff passed. Strict Pyright found three unnecessary casts, and 51 of 53 evaluator tests passed; two test fixtures did not actually violate canonical order or reach the call-limit gate. No typing or focused-test pass is claimed. The casts and test inputs were corrected without runtime relaxation. |
| Corrected evaluator/static gate | 0 | Ruff passed, strict Pyright reported zero diagnostics, and all 53 evaluator tests passed in 1.08 seconds. |
| First public-contract/docs gate | Mixed | Formatting and Ruff passed; strict Pyright reported zero diagnostics; 142 of 144 focused tests passed. Two M34 architecture assertions used the wrong textual spelling for the existing 3.12 setup key and one lowercase RFC phrase. Strict docs and whitespace passed. No focused-suite pass is claimed. |
| Corrected public-contract gate | 0 | Formatting/Ruff/strict Pyright passed; all 144 evaluator, M27-M34 architecture, and release-artifact tests passed in 1.83 seconds; strict docs built in 0.86 seconds with only the known upstream Material notice; whitespace passed. |
| Findings-first privacy correction | 0 | Review found that consented sanitized evidence was documented but not an explicit schema gate. Per-window and per-call `privacy_and_consent_reviewed` requirements and adversarial tests were added. Ruff, strict Pyright, 70 focused tests, strict docs, and whitespace passed. No remaining code or CI finding was identified; PR-only CI still assumes the documented PR maintenance process because `main` is currently unprotected. |
| First complete static command group | Mixed | Lock resolution, 263-file format check, Ruff, strict docs, and whitespace passed. The command mistakenly used `uv sync --frozen --all-groups` without the documented `--extra graphics`, which removed six optional packages; strict Pyright then reported 17 expected unresolved/unknown wgpu diagnostics. No complete static pass is claimed; repository documentation was already correct. |
| Corrected complete lock/static/docs gate | 0 | `uv sync --frozen --all-groups --extra graphics` restored the six exact locked graphics packages; all 263 Python files were formatted, Ruff passed, strict Pyright reported zero diagnostics, strict docs built in 0.88 seconds with only the known upstream notice, and whitespace passed. The lock remained 46 packages. |
| `uv run --frozen pytest -q` | 0 | 1,624 tests passed with nine expected platform-capability skips in 96.49 seconds. |
| `uv build` and installed-wheel smoke | 0 | Built `ludoweave-0.1.0a1.tar.gz` and universal `ludoweave-0.1.0a1-py3-none-any.whl`; isolated no-dependency wheel smoke passed with exact M34 evidence. |
| Fresh release stage and smoke | 0 | Confirmed `.tmp/release-candidate-m34-reviewed` absent, staged ten deterministic artifacts, and passed checksum, manifest, SBOM, safe-extraction, isolated-installation, and bundled M34 evidence smoke. |
| Real-wgpu and vertical-slice gate | 0 | All ten wgpu integration tests passed in 6.89 seconds; the three-workload M7 graphics profile validated; Clockwork Arena reproduced state hash `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder reproduced state `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`. |
| Scope, archive, credential, identity, and Git-object audit | 0 | No diff exists in `src/ludoweave`, `benchmarks`, `pyproject.toml`, `uv.lock`, or the release workflow. CI hash is `3ca17d0e1fad70cd898c90451701ba6733ecfb5235d5c03d898fc9c75bf5871d`; release hash remains `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`. The 94-entry wheel has no native/WASM file. The 48-entry sample bundle contains the M34 evaluator and manifest. Focused credential-pattern scanning returned no match; `[retired control directory]`, `[retired control directory]`, `[retired control directory]`, and `[retired control file]` remain absent; whitespace and `git fsck --full --no-dangling` passed. |
| DCO feature commit and ready PR | 0 | DCO-signed commit `1b10e021651b2320addf40f56fc9597953585771` was pushed and published as ready PR #56 against exact base `d12c30a02782c0ebf892e27c5daf6e9fec1c93ee`. |
| Initial hosted run `31228373123` | 1 | All three graphics jobs and Windows CPython 3.14 compatibility passed. Quality/distribution, Ubuntu CPython 3.13/3.14, and macOS CPython 3.14 each failed only `test_missing_manifest_error_is_path_free`: POSIX rendered the chained `FileNotFoundError` traceback with the deliberately missing path. Quality completed 1,622 other tests. No hosted pass is claimed for this head. |
| Initial correction selector | 4 | Focused formatting and Ruff passed, but pytest used a nonexistent architecture-test filename and collected no tests. No focused-test pass is claimed from that invocation. |
| Corrected CLI gate | 0 | The CLI catches the expected outer `RuntimeError`, emits one sanitized stderr line, and returns 1 while direct evaluator callers retain the chained cause. The regression additionally forbids `Traceback`; the correct focused selector passed 68 tests, strict Pyright reported zero diagnostics, strict docs built, and the complete suite passed 1,624 tests with nine skips. The rebuilt wheel and a fresh ten-artifact release candidate passed isolated smoke. |
| Delayed-review excessive-nesting regression | Corrected | Review correctly found that sufficiently deep JSON could raise an undocumented `RecursionError`. The first new adversarial test failed because this CPython parsed 2,000 nested arrays and the later recursive depth walk exhausted recursion; no pass is claimed from that run. The guarded validation now normalizes exhaustion from either parsing or the depth walk, while preserving the explicit nesting-limit error. |
| Final corrected local gate | 0 | All 69 focused M34 evaluator/architecture tests passed in 1.11 seconds. The unchanged 46-package lock resolved; all 263 Python files were formatted; Ruff and strict Pyright passed; strict docs built in 0.91 seconds with only the known upstream Material notice; whitespace passed; and the complete suite passed 1,625 tests with nine expected skips in 95.23 seconds. `uv build` rebuilt the universal wheel and sdist; isolated-wheel smoke passed; confirmed-absent `.tmp/m34-final-correction` received ten artifacts; and full release smoke passed. Corrected hosted validation remains pending. |
| Corrected hosted validation and review closure | 0 | Pull-request run `31229138742` passed all eight jobs on exact corrected head `600f71a416f0df46af68e63d28a2711893ec4675`: quality/tests/distribution; Ubuntu CPython 3.13/3.14; Windows and macOS CPython 3.14; and Ubuntu/Windows/macOS real graphics. The excessive-nesting finding was acknowledged with exact local evidence and its sole thread resolved. GitHub reported PR #56 `MERGEABLE` and `CLEAN`, with zero top-level comments and eight successful completed checks. |
| PR #56 squash integration audit | 0 | PR #56 merged at `2026-08-08T00:10:05Z` as GitHub-signature-verified commit `a0d80851821b569156979d8d2ae0e473cea768f9`, with sole parent exact base `d12c30a02782c0ebf892e27c5daf6e9fec1c93ee` and tree `b7fa900adfdf73e30aa1cb6a27b2f23dbc953227`, exactly equal to the corrected feature head. Both source commits carry valid DCO trailers. The generated squash body retained literal escaped newline text before its displayed sign-off, so no parsed-trailer claim is made for that generated commit; this signed integration record preserves the explicit attestation without rewriting public history. The feature branch was deleted locally and remotely. |
| Post-merge CI quota audit | 0 | `gh run list --branch main` listed no run for M34 merge commit `a0d80851821b569156979d8d2ae0e473cea768f9`; latest main run remained successful pre-M34 run `31226750474`, confirming removal of the redundant push trigger. |
| Records-only PR quota audit | 0 | Ready PR #57 targets exact `main` commit `a0d80851821b569156979d8d2ae0e473cea768f9` from DCO-signed record head `f39316958cfd875f22e2cf57275feefd2761ab57`. GitHub reported it `MERGEABLE` and `CLEAN` with an empty status-check rollup, and `gh run list --branch records/m34-integration` returned an empty list. The `.project/**` path filter therefore consumed no hosted runner for this factual record. |

## M33 development evidence - 2026-08-08, Windows, CPython 3.12

| Command | Exit | Result |
| --- | ---: | --- |
| M32 integration baseline audit | 0 | Clean synchronized `main`, `origin/main`, and `origin/HEAD` at `60ddf57216d1054ac44df8d834756312c3864e3e`; only `main` existed locally/remotely. The sandbox blocked the GitHub API open-PR query, so no remote PR-state result is claimed. |
| First focused baseline attempt | 4 | `uv lock --check` resolved the unchanged 46-package lock, but stale benchmark-test filenames caused pytest to collect no tests. No test pass is claimed. |
| Corrected focused baseline | 0 | 86 inherited M32, benchmark-validator, release-artifact, and release-workflow tests passed with one graphics-capability skip in 5.10 seconds. |
| `git switch -c evidence/m33-benchmark-regression-rate` | 0 | Created the neutral M33 branch from exact integrated base. |
| M33 manifest identity probe | 0 | Exact 199-byte empty reviewed manifest SHA-256 is `720ae794e2a4ba76303196cd43d6ba0f3b21f81cffd4fa8584f526e2a0d48dca`. |
| Initial evaluator/static gate | Mixed | Ruff passed and the evaluator emitted exact path-free `not-ready` evidence; all 44 evaluator tests passed in 1.07 seconds. Strict Pyright found only two redundant test casts, which were corrected; no type pass is claimed from this group. |
| Corrected evaluator/artifact gate | 0 | Eight touched Python files were formatted; Ruff passed; strict Pyright reported zero diagnostics; 57 evaluator, architecture, and release-artifact tests passed in 1.48 seconds. |
| First public-contract/docs gate | Mixed | Formatting and Ruff passed; strict MkDocs built in 1.03 seconds with only the known upstream notice; whitespace passed; 57 of 58 focused tests passed, with one documentation assertion failing only because a required phrase crossed a Markdown line wrap. No focused-suite pass is claimed. The assertion was corrected and later passed. |
| Corrected public-contract gate | 0 | Eight touched Python files were formatted; Ruff passed; strict Pyright reported zero diagnostics; 58 evaluator, architecture, and release-artifact tests passed in 1.41 seconds; strict docs built in 0.84 seconds with only the known upstream notice; whitespace passed. |
| Shared runner-profile review correction | 0 | Findings-first review found that a frozen controlled runner profile should be reusable across comparisons. Global uniqueness now applies to result/timing artifacts rather than shared runner-profile evidence; an explicit regression proves reuse. Ruff, strict Pyright, whitespace, and all 59 focused tests passed in 1.47 seconds. No remaining blocking or non-blocking review finding was identified. |
| Complete lock/static/docs gate | 0 | The unchanged lock resolved 46 packages in 1 ms; frozen sync checked 45 packages in 4 ms; all 259 Python files were formatted; Ruff passed; strict Pyright reported zero diagnostics; strict docs built in 0.84 seconds with only the known upstream notice; whitespace passed. |
| First complete suite | 1 | 1,555 tests passed with nine expected platform-capability skips in 95.23 seconds, but one inherited M32 architecture assertion failed because README wording shortened `empty reviewed execution manifest`. No complete-suite pass is claimed. Runtime behavior did not fail. |
| Restored M32/M33 contract gate | 0 | The exact inherited M32 phrase was restored; all 70 M32/M33 architecture and evaluator tests passed in 1.46 seconds; whitespace passed. |
| Corrected complete suite | 0 | All 1,556 tests passed with nine expected platform-capability skips in 95.10 seconds. |
| Pure build and installed-wheel smoke | 0 | `uv build` produced `ludoweave-0.1.0a1.tar.gz` and universal `ludoweave-0.1.0a1-py3-none-any.whl`; isolated no-dependency wheel smoke passed with exact M33 evidence. |
| Fresh release stage and smoke | 0 | Confirmed `.tmp/release-candidate-m33-reviewed` absent, staged ten deterministic artifacts, and passed checksum, manifest, SBOM, safe-extraction, isolated-installation, and bundled M33 evidence smoke. |
| Documented M1/M2/M4 benchmark integrity | 0 | All three benchmark commands and validators completed. M1 recorded one of two historical absolute targets observed; M2 validated four informational workloads with no targets; M4 validated three workloads with its baseline target observed. Dirty-tree local results are not admitted M33 comparison evidence. |
| Documented M3 and M7 integrity | 0 | The graphics M3 benchmark/validator recorded six workloads and both historical targets, with zero met. Base and graphics M7 cProfile documents validated two and three diagnostic workloads respectively. These local outputs are not admitted M33 timing comparisons. |
| Real-wgpu regression and vertical slices | 0 | All ten real-wgpu integration tests passed in 7.86 seconds. Clockwork Arena completed 30 ticks with three draws, 16 sprites, state hash `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, and capture `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`. Agent World Builder passed registered tests with five replay batches, state hash `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`, and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`. |
| Artifact, scope, history, and credential audit | 0 | Protected `.github`, metadata, lock, `src/ludoweave`, and `benchmarks` surfaces are unchanged from exact base. CI/release workflow SHA-256 values remain `06a5e07918c83fc8de61e6746cb344f865b6421d81f554d79f4455d3718a3b21` and `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`; whitespace and `git fsck --full --no-dangling` passed. The 94-entry wheel and 46-entry sample bundle contain no native/WASM artifact; the sample bundle contains the exact 33,018-byte evaluator and 199-byte manifest. Focused credential-pattern scanning returned no match; retired `[retired control directory]`, `[retired control directory]`, `[retired control directory]`, and `[retired control file]` paths remain absent. GitHub reported no open PR. |
| Final post-record gate | 0 | The unchanged lock resolved 46 packages in 0.89 ms; all 259 files were formatted; Ruff passed; strict Pyright reported zero diagnostics; all 344 architecture, M33 evaluator, and release-artifact tests passed in 3.32 seconds; strict docs built in 0.88 seconds with only the known upstream notice; whitespace and exact-base protected-surface comparison passed. |
| DCO feature commit, ready PR, and hosted validation | 0 | Commit `3bd7e17eed26028592cb39d37e77e15c6f4371f1` was DCO-signed, pushed, and published as ready PR #54 against exact base `60ddf57216d1054ac44df8d834756312c3864e3e`. Hosted run `31225942698` passed all eight essential jobs: quality/tests/distribution; Ubuntu CPython 3.13/3.14; Windows and macOS CPython 3.14; and Ubuntu/Windows/macOS graphics smoke. |
| Hosted review and merge audit | 0 | GitHub reported exact PR head/base, all eight successful completed checks, `MERGEABLE`/`CLEAN`, no top-level comment, no review, and no review thread. |
| PR #54 squash integration verification | 0 | PR #54 merged at `2026-08-07T23:07:51Z` as GitHub-verified commit `0993c73b3290809ef4e0c36d64d39e5ee5891a9b`. Its sole parent is exact base `60ddf57216d1054ac44df8d834756312c3864e3e`; tree `0db61d87fed781f3cc6ffbeac1b3743f32a81ca2` exactly equals feature-head tree; literal diff and object-integrity checks passed; and the squash message retains the DCO trailer. |
| Feature-branch cleanup | 0 | Local `main` fast-forwarded to the verified squash commit. The exact `evidence/m33-benchmark-regression-rate` branch was deleted remotely and locally after tree verification. Fetch/prune, branch audit, and GitHub PR audit found only synchronized `main` and no open PR. |
| Documentation-only integration-record gate | 0 | All 12 M33 architecture tests passed in 0.41 seconds; strict docs built in 0.84 seconds with only the known upstream notice; whitespace and protected runtime/workflow/metadata comparison against integrated `main` passed; focused credential-pattern scanning returned no match. The record changes only `ROADMAP.md` and three neutral `.project` files. |
| Initial integration-record hosted review | Corrected | Run `31226304397` passed all eight essential jobs, but hosted review correctly found that the record claimed only `main` remained while the record branch/PR itself was still pending. The current-task and project-state text now distinguish the deleted feature branch from pending record PR #55; no merge is claimed for the record head. |

The current empty manifest and synthetic populated fixtures prove evaluator
mechanics only. They are not controlled benchmark runs, historical comparison
evidence, a measured regression rate, a zero-regression result, a performance
claim, or native-code authorization.

## M32 development evidence - 2026-08-08, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| M31 feature/state integration and cleanup verification | 0 | PR #50 is merged as verified `8adb8d46d0ce13ea3687856ae53e899e98dc42a6`; no-CI PR #51 is merged as verified `b4de1d115ddb620ecddccab84637c0e66cfad9fd`; both exact feature/record trees and parents were verified; both temporary branches were deleted locally and remotely; no open PR remained; and only synchronized `main` remained. |
| M32 design selection | 0 | The authoritative design specification orders replay-divergence rate in CI immediately after issue-response and PR-review time. M32 was bounded to strict offline measurement admission with non-execution preservation and no telemetry, GitHub lookup, workflow, runtime, replay, or API change. |
| Exact M32 base and workflow identity audit | 0 | `HEAD`, `main`, `origin/main`, and `origin/HEAD` all resolved to `b4de1d115ddb620ecddccab84637c0e66cfad9fd`; the worktree was clean, only `main` existed locally/remotely, no PR was open, `git fsck --full --no-dangling` passed, and CI/release SHA-256 values remained `06a5e07918c83fc8de61e6746cb344f865b6421d81f554d79f4455d3718a3b21` and `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`. |
| First sandboxed uv lock attempt | 1 | uv was denied access to existing user-cache metadata before project execution. No lock result is claimed from this attempt. |
| Corrected host-cache lock and inherited baseline | 0 | The unchanged lock resolved 46 packages in 0.80 ms; 65 M31 evaluator, architecture, release-artifact, and release-workflow tests passed with one Windows symlink-capability skip in 1.44 seconds. |
| `git switch -c evidence/m32-replay-divergence-rate` | 0 | Created the neutral M32 branch from the exact integrated base. |
| M32 manifest identity probe | 0 | The reviewed replay-divergence-rate manifest is exactly 175 bytes with SHA-256 `cff8a32428ac8dcd18029be4f70e9d359b4c9d70fd411ffe2f36d35704d68aa7` and contains zero evaluation windows. |
| Initial M32 evaluator/static group | Mixed | The evaluator emitted the exact path-free `not-ready` report. Ruff lint passed, but formatting reported two files and strict Pyright found two local tuple-variable type errors. No complete static pass is claimed from this group. |
| Corrected evaluator format/static group | 0 | The tuple variables were made role-specific, the locked formatter reformatted both files, and repeated formatting, Ruff, and strict Pyright checks passed with zero diagnostics. |
| First M32 adversarial focused gate | Mixed | All 51 evaluator/validator tests passed with one Windows symlink-capability skip and strict Pyright passed, but Ruff rejected four intentionally full-width timestamp digits. No Ruff pass is claimed from this group. The literal was escaped without changing its tested value. |
| Corrected M32 evaluator/architecture/artifact/docs gate | 0 | All 68 evaluator, architecture, release-artifact, and release-workflow tests passed with one Windows symlink-capability skip in 1.54 seconds; eight changed Python files were formatted; Ruff passed; strict Pyright reported zero diagnostics; strict docs built in 0.84 seconds with only the known upstream notice; and whitespace passed. |
| First complete M32 gate | Mixed | `uv lock --check`, `uv sync --frozen --all-groups`, 255-file formatting, Ruff, strict docs, and whitespace passed. The sync intentionally removed six optional graphics packages; the immediately following Pyright run therefore reported 17 missing graphics imports. The full suite ran 1,487 successful tests with ten skips and one failure because M32 README wording displaced an exact inherited M31 documentation assertion. No complete type or test pass is claimed from this group. |
| Corrected dependency/static/documentation gate | 0 | `uv sync --frozen --all-groups --extra graphics` restored the six exact locked graphics packages; strict Pyright reported zero diagnostics; 23 M31/M32 architecture tests passed; strict docs built in 0.84 seconds with only the known upstream notice; and whitespace passed after retaining the exact M31 README contract. |
| Corrected pre-review complete suite | 0 | All 1,498 tests passed with nine Windows/platform-capability skips in 102.29 seconds. |
| Pre-review distribution and graphics gate | 0 | `uv build`, isolated-wheel smoke, fresh ten-artifact release staging/smoke, and ten unchanged real-wgpu integration tests all passed. Clockwork Arena completed 3,600 ticks on real wgpu with state hash `sha256:4243defe548ba6e36b6bec93b45f266d2ad48e74c24efc2856d3f7c6197a3b6e` and capture `b795305972071922d2efb563dee15a7faccb1cecbe9e170adf8d49b8a1686f86`; Agent World Builder passed five replay batches and its tests with state hash `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7` and capture `sha256:8e8cf5d6cbf1a73ecba00269c63125816db208b090a59d3fdba4ead5d6c31850`. |
| Findings-first review and correction | Corrected | Review found two blockers: case-source validation accepted encoded/query/fragment-bearing pseudo-paths, and documentation did not fix eligibility before outcomes to exclude intentionally divergent fixtures and verification-disabled diagnostics. Exact path-character validation plus three regressions now reject the malformed URLs; RFC/docs/maintainer boundaries now define eligibility before outcomes while retaining actual eligible-case divergences. No blocking or non-blocking finding remains. |
| Corrected focused review gate | 0 | The first focused rerun passed Ruff and strict Pyright but had one architecture documentation assertion mismatch and one formatter request; no complete focused pass is claimed. After correcting the line-wrap-insensitive phrase and applying the locked formatter, 68 tests passed with one Windows symlink-capability skip in 1.85 seconds, all 255 files were formatted, Ruff passed, and strict docs built in 1.11 seconds with only the known upstream notice. |
| Final reviewed lock/static/repository gate | 0 | The unchanged lock resolved 46 packages in 15 ms; strict Pyright reported zero diagnostics; whitespace, exact protected-surface comparison against `b4de1d115ddb620ecddccab84637c0e66cfad9fd`, and `git fsck --full --no-dangling` passed. CI and release workflow SHA-256 values remain exact. |
| Final reviewed complete suite | 0 | All 1,498 tests passed with nine expected platform-capability skips in 163.56 seconds. |
| Final reviewed distribution gate | 0 | `uv build` produced `ludoweave-0.1.0a1.tar.gz` and universal `ludoweave-0.1.0a1-py3-none-any.whl`; isolated-wheel smoke passed; the confirmed-absent `.tmp/release-candidate-m32-reviewed` target staged ten artifacts; and complete release smoke passed. |
| Artifact, scope, and credential audit | 0 | The wheel contains 94 entries and no native/WASM file; the sample bundle contains 44 entries including `replay_divergence_rate_readiness.py` and `assets/replay_divergence_rate.json`, with no native/WASM file. The manifest remains 175 bytes at exact reviewed SHA-256. Protected `.github`, metadata, lock, and `src/ludoweave` surfaces are unchanged. Focused credential-pattern scanning found no plausible credential, and retired `[retired control directory]`, `[retired control directory]`, `[retired control directory]`, and `[retired control file]` paths remain absent. |
| Initial hosted validation and review | Corrected | Ready PR #52 exact implementation head `7046e59eb4840e6df492c886ce78baf4ad51cd95` passed all eight unchanged essential jobs in run `31194645068`. Hosted review then correctly found that the evaluator required nonexistent `world.replay.divergence` while the runtime emits stable `world.replay.diverged`, which would reject authentic divergent evidence. No merge or final hosted pass is claimed for that head. The evaluator, synthetic fixture, docs, task contract, and architecture regression now use and pin the runtime code. |
| Post-hosted-review correction gate | 0 | The first focused correction run passed 80 replay/M32 tests with one Windows symlink-capability skip, Ruff lint, and strict Pyright, while formatting requested one architecture-test layout update; no complete format pass is claimed from that run. After applying the locked formatter, all 255 files were formatted; strict docs built in 0.83 seconds; the unchanged 46-package lock resolved in 1 ms; protected-surface and whitespace checks passed; and all 1,499 tests passed with nine platform-capability skips in 100.02 seconds. `uv build`, isolated-wheel smoke, confirmed-absent fresh ten-artifact staging, and complete release smoke all passed. Corrected hosted validation remains pending. |
| Corrected hosted validation and review closure | 0 | Ready PR #52 exact corrected head `f6f574c2e9b54341e77d1b9ba2d9268bffe5439a` passed all eight unchanged essential jobs in run `31195402467`: quality/tests/distribution; Ubuntu CPython 3.13/3.14; Windows and macOS CPython 3.14; and Ubuntu/Windows/macOS real graphics. The sole review thread was replied to, resolved, and became outdated; no top-level comment or unresolved thread remained. GitHub reported the PR `MERGEABLE` and `CLEAN`. |
| PR #52 squash integration and cleanup | 0 | PR #52 merged at `2026-08-07T16:03:46Z` as commit `36e8d9ed65a619569f3620b2431d977a1fb80a58`, with sole parent `b4de1d115ddb620ecddccab84637c0e66cfad9fd`, exact feature tree `e185e24861b74fe11325b7188026af29a9618926`, DCO trailer, and GitHub-valid signature verified at `2026-08-07T16:03:50Z`. A local signature query could not access the sandboxed GPG keyring, so no local verification is claimed; GitHub API verification supplied the recorded result. The first read-only PowerShell tree query interpreted unquoted revision braces incorrectly; the quoted rerun returned the exact tree and parent. Local `main` fast-forwarded to the squash commit, object integrity passed, and the M32 feature branch was deleted locally and remotely after exact tree comparison. |
| Documentation-only integration record gate | 0 | Thirteen M32 architecture tests passed in 0.49 seconds; strict docs built in 1.08 seconds with only the known upstream notice; whitespace and protected `.github`/metadata/lock/runtime comparison against integrated `main` passed; and the focused credential-pattern scan returned no match. The record changes only `ROADMAP.md` and three neutral `.project` files. |

The current empty manifest and synthetic populated fixtures prove evaluator
mechanics only. They are not a historical CI replay cohort, workflow run,
measured rate, zero-divergence result, reliability claim, or release gate.
The implementation is reviewed, locally and hosted validated, exact-tree
squash-integrated, and cleaned up. Only this factual integration-record PR
remains pending; no tag, release, package publication, measured rate,
reliability result, or release gate is claimed.

## M31 development evidence - 2026-08-08, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| M30 feature/state integration and cleanup verification | 0 | PR #48 is merged as verified `675713d15a20a38233b80580e5aa773dc7a8684c`; no-CI PR #49 is merged as verified `22dc58df8b0c4d17c3619d83e37c6d0ee6184441`; both exact feature/record trees and parents were verified; both temporary branches were deleted locally and remotely; no open PR remained; and only synchronized `main` remained. |
| M31 design selection | 0 | The authoritative design specification orders issue-response and PR-review time immediately after installation success. M31 was bounded to strict offline measurement admission with pending-item preservation and no SLA, telemetry, networking, or runtime/API change. |
| Exact M31 base and workflow identity audit | 0 | `HEAD`, `main`, `origin/main`, and `origin/HEAD` all resolved to `22dc58df8b0c4d17c3619d83e37c6d0ee6184441`; the worktree was clean, `git fsck --full --no-dangling` passed, and CI/release SHA-256 values remained `06a5e07918c83fc8de61e6746cb344f865b6421d81f554d79f4455d3718a3b21` and `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`. |
| First sandboxed uv baseline attempt | Mixed | Repository identity, object integrity, and workflow hashing completed, but both uv commands were denied access to the existing user cache. No lock or test pass is claimed from this attempt. |
| Corrected host-cache lock and inherited baseline | 0 | The unchanged lock resolved 46 packages in 0.69 ms; 59 M30 evaluator, architecture, release-artifact, and release-workflow tests passed with one Windows symlink-capability skip in 2.08 seconds. |
| `git switch -c evidence/m31-response-review-latency` | 0 | Created the neutral M31 branch from the exact integrated base. |
| M31 manifest identity probe | 0 | The reviewed response/review-latency manifest is exactly 199 bytes with SHA-256 `bc40bbcc1636229fa2c78aed5f71854d1221fd3c0d33169edc1321dd07e69d4f` and contains zero measurement windows. |
| Initial M31 evaluator/static group | Mixed | The evaluator emitted the exact path-free `not-ready` report. Ruff found two UTC-alias style issues and strict Pyright found seven local type issues. No static pass is claimed from this group. |
| Corrected evaluator format/static group | 0 | The first corrected check still reported two files requiring formatting while Ruff lint and strict Pyright passed and the evaluator remained exact. The locked formatter then reformatted both files; the repeated format, Ruff, and strict Pyright checks passed with zero diagnostics. |
| First M31 adversarial focused gate | 1 | Strict Pyright passed and 46 tests passed with one Windows symlink-capability skip, but three test fixtures failed and Ruff rejected a raw full-width-digit literal. No focused-suite or Ruff pass is claimed. The fixtures were corrected without changing the evaluated contract. |
| Corrected M31 adversarial focused gate | 0 | Ruff and strict Pyright passed; all 49 evaluator/validator tests passed with one Windows symlink-capability skip in 1.01 seconds. |
| Initial source/wheel/release artifact wiring gate | 0 | Ruff and strict Pyright passed; all 51 evaluator and release-artifact tests passed with one Windows symlink-capability skip in 1.37 seconds. |
| First architecture/evaluator/artifact/docs gate | Mixed | 61 tests passed with one Windows symlink-capability skip, but one architecture assertion required the literal `no SLA` while the roadmap used the stronger contextual statement `no latency aggregate or SLA is claimed`. No focused-suite pass is claimed. Strict docs still built in 0.97 seconds and whitespace passed. |
| Corrected architecture/evaluator/artifact/docs gate | 0 | The assertion now checks each document's actual explicit non-claim. Ruff and strict Pyright passed; all 62 tests passed with one Windows symlink-capability skip in 1.44 seconds; strict docs built in 0.83 seconds with only the known upstream notice; and whitespace passed. |
| Findings-first M31 review | 0 | Review found no remaining blocking or non-blocking issue. It verified pending-item preservation, complete-cohort/manual-review boundaries, aggregate suppression before exact manifest/history admission, canonical project-only locators, timestamp/latency agreement, path-free failures, privacy limits, installed artifact wiring, and unchanged runtime/workflow scope. |
| Complete lock/static/docs gate | 0 | The unchanged lock resolved 46 packages in 1 ms; frozen sync checked 45 packages in 3 ms; all 251 Python files were formatted; Ruff passed; strict Pyright reported zero diagnostics; strict docs built in 0.81 seconds with only the known upstream notice; and whitespace passed. |
| `uv run --frozen pytest -q` | 0 | The exact reviewed tree passed 1,435 tests with eight Windows capability skips in 90.68 seconds. |
| `uv build` and `scripts/smoke_wheel.py dist` | 0 | Built the pure `0.1.0a1` source archive and universal wheel; isolated no-dependency installed-wheel smoke passed with exact M31 evidence. |
| Fresh M31 release staging and `scripts/smoke_release.py` | 0 | Staged ten deterministic artifacts and passed checksum, manifest, SBOM, safe-extraction, isolated-installation, and bundled M31 evidence smoke. |
| Real-wgpu regression and vertical slices | 0 | All ten real-wgpu tests passed in 6.83 seconds. Clockwork Arena reproduced state hash `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture SHA-256 `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder completed its typed loop with five replay batches and passing registered tests. |
| First final artifact/security audit | Mixed | Manifest/workflow hashes, protected scope, whitespace, object integrity, credential scan, and neutral-path checks passed, but incorrect PowerShell archive path syntax made the archive counts invalid. No archive-content pass is claimed from this attempt. |
| Corrected archive-content audit | 0 | The unchanged 94-entry wheel contains zero native/WASM files. The 42-entry sample bundle contains the exact M31 evaluator and manifest paths. |
| Final post-record static/focused/docs/scope gate | 0 | All 251 Python files were formatted; Ruff passed; strict Pyright reported zero diagnostics; all 62 focused tests passed with one Windows symlink-capability skip in 1.53 seconds; strict docs built in 0.78 seconds with only the known upstream notice; whitespace, exact-base protected-surface comparison, and the neutral repository-path audit passed. |
| DCO feature commit, ready PR, and initial hosted validation | 0 | DCO-signed feature commit `95f193779d2895ea48584e0bc589bd94d6b58ff7` was pushed and published as ready PR #50 against exact base `22dc58df8b0c4d17c3619d83e37c6d0ee6184441`; GitHub Actions run `31189729885` passed all eight essential jobs on that exact head. |
| Hosted review of the initial PR head | Mixed | GitHub reported the PR `MERGEABLE` and `CLEAN` with eight successful checks, but its automated review correctly found that `observed_through == opened_before` was admitted even though the contract requires post-window observation. No final review or integration pass is claimed for the initial head. |
| Post-review focused/static/docs gate | 0 | Admission now requires `observed_through > opened_before`, equality has an explicit regression, and the RFC/public admission text says the cutoff is strictly after closure. All 60 focused tests passed with one Windows symlink-capability skip in 1.15 seconds; focused Ruff formatting/linting and strict Pyright passed; and strict docs built in 0.91 seconds with only the known upstream notice. |
| Post-review complete static and test gate | 0 | All 251 Python files were formatted; Ruff passed; strict Pyright reported zero diagnostics; and the complete suite passed 1,435 tests with eight Windows capability skips in 91.83 seconds. |
| Post-review pure build, installed-wheel smoke, and fresh release smoke | 0 | `uv build` rebuilt the pure `0.1.0a1` source archive and universal wheel; isolated no-dependency wheel smoke passed; a confirmed-absent target staged ten deterministic artifacts; and the complete release smoke passed. |
| Corrected-head publication and hosted validation | 0 | DCO-signed correction commit `dd4058b71439b5bade9d091831ba5453a51db35c` was pushed to PR #50; run `31190559197` passed all eight essential jobs on that exact head: quality/tests/distribution, Ubuntu CPython 3.13 and 3.14, Windows CPython 3.14, macOS CPython 3.14, and graphics smoke on Ubuntu, Windows, and macOS. |
| Final hosted review and merge audit | 0 | The valid finding was acknowledged and its thread resolved. GitHub reported the sole thread resolved and outdated, zero top-level comments, eight successful completed checks, exact base `22dc58df8b0c4d17c3619d83e37c6d0ee6184441`, exact head `dd4058b71439b5bade9d091831ba5453a51db35c`, and PR #50 `MERGEABLE` and `CLEAN`. |
| PR #50 squash integration verification | 0 | PR #50 merged at 2026-08-07T15:05:08Z as GitHub-verified commit `8adb8d46d0ce13ea3687856ae53e899e98dc42a6`. Its tree `2ec80742556e62b34dc9275fd0b268a484e9eace` exactly equals the corrected feature-head tree, its sole parent is exact M31 base `22dc58df8b0c4d17c3619d83e37c6d0ee6184441`, literal `git diff --exit-code` found no tree difference, and `git fsck --full --no-dangling` passed. |
| M31 feature-branch cleanup | 0 | GitHub deleted the remote feature branch; fetch/prune confirmed it absent. Normal local safe deletion correctly refused because a squash merge does not make feature commits ancestors; after exact tree/parent verification, the single named local feature branch was force-deleted. No open PR remained, and synchronized `main` became the base of `records/m31-integration`. |
| State-record focused architecture gate | 0 | All 11 M31 public-contract architecture tests passed in 0.50 seconds. |
| State-record strict documentation and scope gate | 0 | Strict MkDocs built in 0.81 seconds with only the known upstream notice; `git diff --check` passed; and the diff contained only `ROADMAP.md` plus the three neutral `.project` records. |

The current empty manifest and synthetic populated fixtures prove evaluator
mechanics only. They are not people, issue responses, pull-request reviews,
maintainer work, responsiveness, support, service levels, or project history.
Documentation/architecture validation, the post-review full local gate,
findings-first review, artifact audit, corrected-head hosted validation, review
reread, exact squash integration, and feature-branch cleanup are complete. No
benchmark was run because M31 changes no runtime/performance path and defines no
timing target.

## M30 development evidence - 2026-08-07, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| M29 feature/state integration and cleanup verification | 0 | PR #46 is merged as verified `fc969a981ecdbbf842477f46486e29277119e05b`; no-CI PR #47 is merged as verified `c88b166a39a793c91741bfa762af5627a87c53b4`; both exact feature/record trees and parents were verified; both temporary branches were deleted locally and remotely; no open PR remained; and only synchronized `main` remained. |
| Exact M30 base and workflow identity audit | 0 | `HEAD`, `main`, `origin/main`, `origin/HEAD`, and the merge base all resolved to `c88b166a39a793c91741bfa762af5627a87c53b4`; the worktree was clean, `git fsck --full --no-dangling` passed, and CI/release SHA-256 values remained `06a5e07918c83fc8de61e6746cb344f865b6421d81f554d79f4455d3718a3b21` and `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`. |
| `git switch -c evidence/m30-installation-matrix-readiness` | 0 | Created the neutral M30 branch from the exact integrated base. |
| `uv lock --check` | 0 | The unchanged lock resolved 46 packages in 0.84 ms. |
| Inherited M29/artifact baseline | 0 | 61 contributor-retention, architecture, release-artifact, and release-workflow tests passed with one Windows symlink-capability skip in 2.20 seconds. |
| M30 manifest identity probe | 0 | The reviewed installation-matrix manifest is exactly 462 bytes with SHA-256 `7c05813a7304e8ff44a009ada37c8e60ff545baec633852fc332e46bdfe03c90` and contains zero installation records. |
| Initial M30 evaluator/static group | Mixed | The evaluator emitted the exact path-free `not-ready` report. Ruff passed, while strict Pyright found six local annotation issues in the new evaluator. No Pyright pass is claimed from this group. The annotations were corrected before tests were added. |
| Initial M30 evaluator regression suite | 0 | Ruff and strict Pyright passed; 41 evaluator tests passed with one Windows symlink-capability skip in 2.93 seconds. |
| Initial source/wheel/release artifact wiring gate | 0 | Ruff and strict Pyright passed; 43 evaluator and release-artifact tests passed with one Windows symlink-capability skip in 2.04 seconds. |
| First combined evaluator/architecture/artifact gate | 1 | 53 tests passed with one skip, but the public-contract architecture test found that the README non-claim did not explicitly name the empty installation-matrix manifest. Strict docs still built in 0.89 seconds. No focused-suite pass is claimed. |
| Second combined evaluator/architecture/artifact gate | 1 | 53 tests passed with one skip, but the RFC's equivalent non-claim was line-wrapped across the exact architecture phrase. Strict docs still built in 0.83 seconds. No focused-suite pass is claimed. |
| Corrected focused/static/docs gate | 0 | All 53 evaluator, architecture, and release-artifact tests passed with one Windows symlink-capability skip in 2.07 seconds; Ruff passed; strict Pyright reported zero diagnostics; strict docs built in 0.80 seconds with only the known upstream notice; and `git diff --check` passed. |
| Complete static/documentation gate | 0 | The unchanged 46-package lock resolved, frozen sync checked 45 packages, all 247 Python files were formatted, Ruff passed, strict Pyright reported zero diagnostics, strict docs built in 0.81 seconds with only the known upstream notice, and whitespace passed. |
| First `uv run --frozen pytest -q` | 1 | 1,371 tests passed with seven Windows capability skips, but one M28 architecture contract failed because the updated README status had omitted M28's exact empty sample-game manifest non-claim. No complete-suite pass is claimed from this run. |
| Corrected M28-M30 public-contract group and complete suite | 0 | All 30 M28-M30 architecture tests passed in 0.50 seconds; the complete suite then passed 1,372 tests with seven Windows capability skips in 93.53 seconds. |
| `uv build` and `scripts/smoke_wheel.py dist` | 0 | Built the pure `0.1.0a1` source archive and universal wheel; isolated no-dependency wheel smoke passed with exact M30 evidence. |
| Fresh M30 release staging and `scripts/smoke_release.py` | 0 | Staged ten deterministic artifacts and passed checksum, manifest, SBOM, safe-extraction, isolated-installation, and bundled M30 evidence smoke. |
| Real-wgpu regression and vertical slices | 0 | All ten real-wgpu tests passed in 6.82 seconds. Clockwork Arena reproduced state hash `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture SHA-256 `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder completed its typed loop with five replay batches and passing registered tests. |
| Findings-first M30 review | Mixed | Review found that the synthetic future record used the release-page path instead of GitHub's canonical asset-download path, lacked a public validation-job locator, allowed noncanonical record ordering, and accepted impossible calendar dates. No final-reviewed pass is claimed from the pre-review tree. |
| Corrected findings-first focused/static/docs gate | 0 | Canonical download/validation URLs, unique validation evidence, required environment order, and calendar dates are enforced. All 56 focused tests passed with one Windows symlink-capability skip in 2.22 seconds; Ruff passed; strict Pyright reported zero diagnostics; strict docs built in 0.83 seconds with only the known upstream notice; and whitespace passed. |
| Final post-review lock/static/docs gate | 0 | The unchanged 46-package lock resolved in 0.80 ms; frozen sync checked 45 packages; all 247 Python files were formatted; Ruff passed; strict Pyright reported zero diagnostics; strict docs built in 0.78 seconds with only the known upstream notice; and whitespace passed. |
| Final post-review `uv run --frozen pytest -q` | 0 | The exact reviewed tree passed 1,375 tests with seven Windows capability skips in 92.88 seconds. |
| Final `uv build` and `scripts/smoke_wheel.py dist` | 0 | The pure `0.1.0a1` source archive and universal wheel rebuilt; isolated no-dependency installed-wheel smoke passed with exact M30 evidence. |
| Final release staging and `scripts/smoke_release.py` | 0 | A fresh ten-artifact candidate passed checksum, manifest, SBOM, safe-extraction, isolated-installation, and bundled M30 evidence smoke. |
| Final protected-surface, credential, object, and artifact audit | 0 | `git diff --check`, exact-base protected diff, and `git fsck --full --no-dangling` passed. Workflow hashes remain unchanged; the exact 462-byte manifest hash remains pinned; no targeted credential pattern appeared; the 94-entry wheel contains no native/WASM file; and the 40-entry sample bundle contains the exact M30 evaluator and manifest paths. |
| DCO commit, ready PR, and exact hosted head | 0 | DCO-signed feature commit `576dd070b547bef853ee47ece4c928b4e9962a7d` was pushed on the neutral M30 branch and published as ready PR #48 against exact base `c88b166a39a793c91741bfa762af5627a87c53b4`. |
| GitHub Actions run `31186083454` | 0 | The exact feature head passed all eight essential jobs: quality/tests/distribution; Ubuntu CPython 3.13 and 3.14; Windows CPython 3.14; macOS CPython 3.14; and graphics smoke on Ubuntu, Windows, and macOS. |
| Final hosted review and check audit | 0 | GitHub reported zero reviews, zero review threads, and eight successful completed checks on PR #48. |
| PR #48 squash integration verification | 0 | PR #48 merged at 2026-08-07T14:12:10Z as GitHub-verified commit `675713d15a20a38233b80580e5aa773dc7a8684c`. Its tree `6c421ece852d822270f3de1e9ece9c7cc1568678` exactly equals the feature-head tree, its sole parent is exact M30 base `c88b166a39a793c91741bfa762af5627a87c53b4`, `git diff --exit-code` found no tree difference, and `git fsck --full --no-dangling` passed. |
| M30 feature-branch cleanup | 0 | GitHub deleted the merged remote feature branch; fetch/prune showed no remote feature branch; the exact verified local feature branch was deleted after tree comparison; and synchronized `main` became the base of neutral state-record branch `records/m30-integration`. |
| State-record focused architecture gate | 0 | All ten M30 public-contract architecture tests passed in 0.28 seconds. |
| State-record strict documentation and scope gate | 0 | Strict MkDocs built in 0.86 seconds with only the known upstream notice; `git diff --check` passed; and the diff contained only `ROADMAP.md` plus the three neutral `.project` records. |

No benchmark was run because M30 changes no runtime or performance path and
makes no performance claim. The final review found no remaining runtime/API,
format, dependency, lock, version, workflow/CI-topology, backend/native/WASM,
networking, telemetry, provider, credential, private-data, path-leakage, or
stale-documentation change. Ready-PR publication, hosted validation, review
reread, exact squash integration, and feature-branch cleanup are complete.

The current empty manifest and synthetic populated fixtures prove evaluator
mechanics only. They are not releases, users, installations, clean machines,
publication, support evidence, or external adoption. Full local validation and
review are complete; the current result remains an evidence-only non-claim.

## M29 Python 3.14 hosted correction - 2026-08-07

Ready PR #46 initially preserved five successful essential jobs: the Ubuntu
3.12 quality/distribution job, Ubuntu 3.13 compatibility, and the Ubuntu,
macOS, and Windows graphics jobs. Run `31181308306` failed only its Ubuntu,
macOS, and Windows Python 3.14 compatibility jobs. Each failure was the same
`test_retention_manifest_rejects_excessive_json_nesting` expectation: CPython
3.14 accepted the 10,000-level array and the evaluator then rejected its root
as a non-object, while the regression expected a decoder error. No hosted pass
is claimed for those three jobs from that run.

The correction enforces a parser-independent 16-level object/array nesting
limit over the already byte-bounded manifest. Its linear scanner ignores JSON
string contents and escapes, and the standard parser remains authoritative for
JSON syntax. Boundary and escaped-string regressions cover those semantics.

| Command | Exit | Result |
| --- | ---: | --- |
| Local reproduction on CPython 3.14.5 before correction | 1 | The single excessive-nesting regression reproduced the hosted failure: the evaluator reported that the manifest must be an object instead of the expected invalid-JSON error. No pass is claimed. |
| Focused CPython 3.12 evaluator and architecture suite | 0 | 56 tests passed with one Windows symlink-capability skip in 5.27 seconds. |
| Focused Ruff and Pyright checks | 0 | Ruff reported no lint finding and Pyright reported zero errors, warnings, or information findings. |
| `uv run --isolated --frozen --python 3.14 pytest -q tests/integration/test_external_contributor_retention_readiness.py tests/architecture/test_m29_contributor_retention_boundary.py` | 0 | 56 tests passed with one Windows symlink-capability skip in 2.28 seconds. |
| First combined lock/sync/static/docs gate in the managed sandbox | 1 | Every uv command stopped before project execution because the sandbox denied access to existing user-cache metadata. No pass is claimed from this invocation; `git diff --check` produced no finding. |
| Authorized lock, frozen sync, formatting, lint, type, docs, and whitespace gate | 0 | The unchanged 46-package lock resolved; 45 installed packages were checked; all 243 Python files were formatted; Ruff passed; Pyright reported zero diagnostics; strict docs built with only the known upstream MkDocs Material notice; and `git diff --check` passed. |
| `uv run --frozen pytest -q` on CPython 3.12.13 | 0 | The complete suite passed 1,321 tests with six Windows capability skips in 101.76 seconds. |
| `uv run --isolated --frozen --python 3.14 pytest -q` on CPython 3.14.5 | 0 | The complete compatibility suite passed 1,311 tests with seven platform/version capability skips in 95.59 seconds. |
| `uv build` | 0 | Built the pure `ludoweave-0.1.0a1` source archive and universal wheel. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency installed-wheel smoke passed. |
| Fresh release staging and `scripts/smoke_release.py` | 0 | Staged ten deterministic artifacts and passed release-bundle smoke for `0.1.0a1`. |
| GitHub Actions correction run `31183032073` | 0 | All eight essential jobs passed on exact DCO-signed head `897a3db5b0901835c6929eda5f94ed1774afac16`: quality/tests/distribution; Ubuntu 3.13; Ubuntu, macOS, and Windows 3.14; and graphics smoke on all three operating systems. |
| Final PR #46 review and mergeability audit | 0 | GitHub reported `MERGEABLE` and `CLEAN`; no review thread or actionable finding remained. One old general comment cited a nonexistent commit, while both actual PR commits contain valid DCO trailers. |
| PR #46 squash integration | 0 | GitHub squash-integrated the exact corrected tree as verified commit `fc969a981ecdbbf842477f46486e29277119e05b` with sole parent `e4125bf31a751473d2af4fecc05a9744d551063c` and tree `d98c25f156aaeee863ff8dc88b00355daa921d2e`, identical to the final feature head. |
| Post-merge synchronization and branch cleanup | 0 | Local `main`, `origin/main`, and `origin/HEAD` synchronized at the verified squash commit; the obsolete M29 feature branch was deleted locally and remotely; `git fsck --full --no-dangling` passed. |
| Integration-record focused gate | 0 | All ten M29 architecture tests passed in 0.25 seconds; strict docs built in 0.76 seconds with only the known upstream notice; whitespace passed; and the record changes no workflow, metadata, lock, runtime, example, script, or test file. |

The correction changes only the bounded offline M29 evaluator, its tests, and
the matching public boundary documentation. M29 is fully integrated.

## M29 development evidence - 2026-08-07, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| M28 feature/state integration and branch-cleanup verification | 0 | PR #44 is merged as verified `90d58a4567e7c7eaff90a28a7c59f2453b6d4538`; no-CI PR #45 is merged as verified `e4125bf31a751473d2af4fecc05a9744d551063c`; local and remote M28 branches were deleted after both PRs merged, no open PR remained, and only synchronized `main` remained locally and remotely. |
| Exact M29 base and workflow identity audit | 0 | `HEAD`, `main`, `origin/main`, and `origin/HEAD` all resolved to `e4125bf31a751473d2af4fecc05a9744d551063c`; the worktree was clean, `git fsck --full --no-dangling` passed, and CI/release SHA-256 values remained `06a5e07918c83fc8de61e6746cb344f865b6421d81f554d79f4455d3718a3b21` and `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`. |
| `git switch -c evidence/m29-contributor-retention-readiness` | 0 | Created the neutral-named M29 branch from the exact integrated base. |
| First `uv lock --check` in the managed sandbox | 1 | uv failed before project execution because the sandbox denied access to existing user-cache metadata; no lock pass is claimed from this attempt. |
| `uv lock --check` with approved cache access | 0 | The unchanged lock resolved 46 packages in 0.74 ms. |
| Focused M27/M28/adoption-artifact baseline | 0 | 114 contributor-rehearsal, sample-game, architecture, and release-artifact tests passed with two Windows symlink-capability skips in 3.93 seconds. |
| M29 manifest identity probe | 0 | The reviewed contributor-retention manifest is exactly 274 bytes with SHA-256 `61785ec165e9f9a7c1025c37f7b714d6fa42b2c7081145a0f843395a325b36ee` and contains zero retention records. |
| Initial M29 evaluator report | 0 | The source evaluator emitted exact path-free `not-ready` evidence with zero retained contributors, zero return contributions, and reason `retained-external-contributor-absent`. |
| Initial M29 formatting, Ruff, and integration suite | 0 | Ruff formatted one of three files, lint passed, and all 39 initial fail-closed integration tests passed with one Windows symlink-capability skip in 1.83 seconds. |

Synthetic populated retention records prove evaluator mechanics only. They are
not people, contributions, issues, pull requests, feedback, retention,
adoption, project history, or popularity evidence.

## M29 final local validation and review - 2026-08-07, Windows, CPython 3.12.13

Findings-first review identified that GitHub login case could otherwise make
one public identity appear as two contributors. The evaluator now canonicalizes
logins case-insensitively before uniqueness and history checks. Regressions also
prove that `star_count` is rejected at both manifest and record levels rather
than treated as retention evidence.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Approved cache-access run checked 45 installed packages in 3 ms. |
| `uv run --frozen ruff format --check .` | 0 | All 243 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | No lint findings. |
| `uv run --frozen pyright` | 0 | Zero errors, warnings, or information findings. |
| Focused M27-M29 evaluator, architecture, and artifact suite | 0 | The corrected suite passed 146 tests with three Windows symlink-capability skips in 5.58 seconds. |
| First `uv run --frozen pytest -q` | 1 | 1,316 tests passed with six skips, but one M28 architecture contract failed because M29's README status sentence had replaced M28's exact empty-sample-manifest non-claim. No full-suite pass is claimed from this run. |
| Corrected M28/M29 documentation-contract check | 0 | Both retained non-claims are explicit; all 20 M28/M29 architecture tests passed in 0.41 seconds. |
| Corrected `uv run --frozen pytest -q` | 0 | The complete suite passed 1,317 tests with six Windows symlink-capability skips in 88.85 seconds. |
| `uv run --frozen mkdocs build --strict` after correction | 0 | Strict documentation built in 0.81 seconds with only the known upstream MkDocs Material/MkDocs 2.0 informational warning. |
| Final post-record formatting, Ruff, Pyright, focused tests, strict docs, and complete tests | 0 | All 243 Python files remained formatted; Ruff passed; Pyright reported zero diagnostics; 54 focused M29/artifact tests passed with one Windows symlink-capability skip in 2.43 seconds; strict docs built in 0.91 seconds with the known upstream warning; and 1,317 complete tests passed with six skips in 91.43 seconds. |
| `uv build` | 0 | Approved cache-access run built `ludoweave-0.1.0a1.tar.gz` and the universal pure-Python wheel. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency wheel installation passed all inherited smoke plus exact M29 zero-retention evidence. |
| Fresh M29 release staging and `scripts/smoke_release.py` | 0 | Staged a deterministic ten-artifact candidate and passed checksum, manifest, SBOM, safe-extraction, isolated-installation, and bundled M29 evidence smoke. |
| Documented M1-M4 benchmark generators and validators | 0 | All retained schemas validated. M1's 3,600-tick p95 was 57.287 ms and observed its 12-second target; its 10,000-entity simulation p95 was 175.1282 ms and missed 4 ms. M2's four target-free p95 values were 38.0544, 17.2453, 18.8606, and 248.891 ms. M3 extraction/submission p95 values were 26.9649/3.0528 ms and both missed 3 ms. M4 baseline p95 was 2.0168 ms and observed 16.666667 ms; stress 4/8 p95 values were 3.0014/4.2406 ms with no targets. |
| Five-repeat base and graphics M7 profile generators and validators | 0 | The two-workload base and three-workload graphics artifacts validated; timings remain diagnostic only. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | All ten unchanged real-wgpu integration tests passed in 6.98 seconds. |
| Clockwork Arena and Agent World Builder real-wgpu vertical slices | 0 | Clockwork Arena completed 30 ticks and three draws with state hash `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859` and capture SHA-256 `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; Agent World Builder committed its typed loop, passed registered tests, and recorded five replay batches. |
| Final whitespace, protected-surface, object, and artifact inventory audit | 0 | `git diff --check`, exact-base protected diff, and `git fsck --full --no-dangling` passed. Workflow hashes remain unchanged; the exact 274-byte manifest hash remains pinned; the 94-entry wheel contains no native/WASM file; and the 38-entry sample bundle contains both M29 evidence files. |
| Targeted credential-pattern `rg` scan | 1 | Expected no-match exit: no private-key, GitHub-token, AWS-key, or generic `sk-` credential pattern appeared in the changed evidence/documentation surfaces. |
| First ASCII/nesting hardening gate | Mixed | Ruff correctly rejected a confusable Unicode digit in a test literal, and the 1,100-level nesting fixture parsed to a non-object instead of exercising the intended decoder failure. No pass is claimed from this attempt. The fixture now uses escaped Unicode and 10,000 nesting levels within the byte cap. |
| First post-migration `uv lock --check` in the managed sandbox | 1 | uv again failed before project execution because access to existing user-cache metadata was denied; no lock pass is claimed from this attempt. |
| Final `uv lock --check` with approved cache access | 0 | The unchanged 46-package lock resolved in 0.92 ms. |
| Final `uv sync --frozen --all-groups --extra graphics` | 0 | The frozen environment checked 45 packages in 3 ms. |
| Final formatting, Ruff, Pyright, and strict docs after the repository-convention migration | 0 | All 243 Python files were formatted; Ruff passed; Pyright reported zero diagnostics; strict docs built in 0.97 seconds with only the known upstream warning. |
| First focused M28/M29 command after migration | 4 | A stale architecture-test filename caused pytest collection to stop with no tests run. No pass is claimed from this invocation. |
| Corrected focused M28/M29 and artifact suite | 0 | 111 tests passed with two Windows symlink-capability skips in 4.16 seconds. |
| Final `uv run --frozen pytest -q` | 0 | The exact final tree passed 1,319 tests with six Windows symlink-capability skips in 98.88 seconds. |
| Final `uv build` and `scripts/smoke_wheel.py dist` | 0 | The pure `0.1.0a1` sdist and universal wheel built; isolated wheel smoke passed. |
| Exact documented release staging and smoke | 0 | A fresh `.tmp/release-candidate` contained ten deterministic artifacts, and complete release smoke passed. |
| Final documented M1-M4 generators and validators | 0 | All schemas validated. M1 fixed-step p95 was 46.5708 ms and observed its target; simulation p95 was 195.7832 ms and missed 4 ms. M2's target-free p95 values were 44.8821, 17.0150, 23.1025, and 259.5819 ms. M3 extraction/submission p95 values were 28.0267/4.0673 ms and both missed 3 ms. M4 baseline p95 was 2.5603 ms and observed its target; stress 4/8 p95 values were 3.8675/4.7666 ms with no targets. |
| Final documented M7 base and graphics profile generators and validators | 0 | The two-workload base and three-workload graphics profile artifacts validated; timings remain diagnostic only. |
| Neutral repository-convention inspection | 0 | `[retired control directory]` and `[retired control file]` are absent from the working tree; maintenance guidance is `MAINTAINERS.md`, current records live under `.project/`, and current references resolve to those paths. Historical branch names remain only where required for factual Git/test evidence; no history was rewritten. |
| Final remote-history refresh and graph audit | 0 | `git fetch origin --prune` completed; `HEAD`, `main`, `origin/main`, `origin/HEAD`, and the merge base all remained exact `e4125bf31a751473d2af4fecc05a9744d551063c`, with zero commits on either side. The graph is linear through the verified M28 integration record, `git fsck --full --no-dangling` passed, and only local `main` plus the neutral M29 branch and remote `main` exist. |
| Final protected-surface and workflow/manifest identity audit | 0 | The staged diff against the exact base is empty for `.github`, `pyproject.toml`, `uv.lock`, and `src/ludoweave`. CI, release, and M29 manifest SHA-256 values remain exact `06a5e07918c83fc8de61e6746cb344f865b6421d81f554d79f4455d3718a3b21`, `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`, and `61785ec165e9f9a7c1025c37f7b714d6fa42b2c7081145a0f843395a325b36ee`. |
| First final credential scan invocation | 1 | The pattern began with hyphens and was interpreted as an `rg` option, so the scan did not execute and no clean result is claimed from that attempt. |
| Corrected credential and development-provenance phrase scans | 1 | Expected no-match exits: no targeted private-key/token/access-key pattern and no explicit development-agent phrase appeared in the reviewed current tree. Product-facing software-agent terminology remains because agent operability is an engine requirement. |
| First artifact inventory probe | 1 | PowerShell had not loaded the ZIP filesystem assembly, so no artifact-count result is claimed from that attempt. |
| Corrected artifact inventory probe | 0 | After explicitly loading the read-only ZIP assembly, the wheel contained 94 entries and zero native/WASM libraries; the 38-entry sample bundle contained the exact M29 evaluator and manifest paths. |
| Final post-review `uv run --frozen mkdocs build --strict` | 0 | Strict docs rebuilt in 0.77 seconds with only the known upstream warning after the last wording edits. |

The final scope review found no runtime/public-export, persistent-format,
dependency, lock, version, workflow, CI-topology, backend/native/WASM,
networking, telemetry, provider, credential, private-data, or stale-documentation
change. The separately authorized maintenance-path migration changes no
authorship or milestone semantics. M1 simulation and both M3 targets remain
recorded misses and authorize no native code or scope expansion. Subsequent
correction, hosted validation, review, and integration evidence is recorded in
the M29 correction section above.

## M28 development evidence - 2026-08-07, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| M27 feature/state integration verification and branch preparation | 0 | PR #42 squash-integrated exact final M27 evidence head `349dc3b78dcae2b1c725ed3dc8e5e646ca3d3ac1` as GitHub-verified `ff1c81f8aaa96245706586096f400a5fb03bdd04`; no-CI PR #43 integrated the exact five-file state tree as GitHub-verified `17401eb32be30862496bbe02366d886a60752fb3`; local `main`, `origin/main`, and `origin/HEAD` matched with a clean worktree, and `git fsck --full --no-dangling` exited 0. |
| `git switch -c [historical branch name redacted]` | 0 | Created M28 from exact integrated `main` commit `17401eb32be30862496bbe02366d886a60752fb3`. |
| First `uv lock --check` in the managed sandbox | 1 | uv failed before project execution because the sandbox denied access to existing user-cache metadata; no lock pass is claimed from this attempt. |
| `uv lock --check` with approved cache access | 0 | The unchanged lock resolved 46 packages in 0.83 ms. |
| Focused M25/M27/adoption-artifact baseline | 0 | 94 external-feedback, contributor-rehearsal, architecture, and release-artifact tests passed with two Windows symlink-capability skips in 4.75 seconds. |
| M28 manifest identity probe | 0 | The reviewed external sample-game manifest is exactly 280 bytes with SHA-256 `ecdd0be75e42f047037c6799205786079274eb6d73d788f81e1061acc82008dd` and contains zero sample-game records. |
| Initial M28 formatting | 0 | Ruff reformatted three of eight changed Python files; five were already formatted. |
| Initial M28 Ruff, Pyright, focused tests, and report group | Mixed | Ruff passed and the exact sanitized report was `not-ready`. Pyright found one unnecessary Boolean cast. The focused suite passed 51 tests with one Windows symlink-capability skip but failed its single documentation-contract test because the M28 public docs had not yet been added. No Pyright or focused-suite pass is claimed from this group. |
| First corrected focused/static/docs gate | 0 | After the type correction and public documentation landed, Ruff passed, Pyright reported zero diagnostics, 52 focused tests passed with one Windows symlink-capability skip in 2.22 seconds, and strict docs built in 0.81 seconds. |
| Findings-first hardening gate | Mixed | Review added explicit independence, provenance, and outcome attestations plus cross-role artifact and evidence-locator uniqueness. Ruff, Pyright, and strict docs passed, but the first 65-record count-cap regression reached the 65,536-byte limit before the record-count limit. No focused-suite pass is claimed from this group. |
| Corrected focused M28 suite | 0 | The executable record cap was set to 32; all 56 evaluator, validator, boundary, artifact, and release tests passed with one Windows symlink-capability skip in 2.18 seconds. |

Synthetic populated sample-game records prove evaluator mechanics only. They
are not authors, games, users, repositories, feedback, adoption, project
history, releases, or compatibility evidence.

## M28 final local validation and review - 2026-08-07, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Approved cache-access run resolved the unchanged 46-package lock in 0.90 ms. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Approved cache-access run checked 45 installed packages in 3 ms. |
| First combined static command | Interrupted | The combined shell was interrupted before producing conclusive results; no pass is claimed from it. Every check was rerun separately below. |
| `uv run --frozen ruff format --check .` | 0 | All 239 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | No lint findings. |
| `uv run --frozen pyright` | 0 | Zero errors, warnings, or information findings. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built in 0.86 seconds with only the known upstream MkDocs Material/MkDocs 2.0 informational warning. |
| `uv run --frozen pytest -q` | 0 | 1,264 tests passed with five Windows symlink-capability skips in 92.09 seconds. |
| First sandboxed `uv build` | 1 | uv could not access existing user-cache metadata before project execution; no build pass is claimed from this attempt. |
| `uv build` with approved cache access | 0 | Built `ludoweave-0.1.0a1.tar.gz` and the universal pure-Python wheel. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency wheel installation passed all inherited smoke and exact M28 empty-manifest evidence. |
| Fresh M28 release staging and `scripts/smoke_release.py` | 0 | Staged a deterministic ten-artifact candidate and passed checksum, manifest, SBOM, safe-extraction, isolated-installation, and bundled M28 evidence smoke. |
| M28 report and exact validator | 0 | The source evaluator emitted the exact sanitized `not-ready` document with zero games and reason `external-sample-game-absent`; the installed evidence validator accepted it. |
| Documented M1-M4 benchmark generators and validators | 0 | All retained schemas validated. M1 observed only the 3,600-tick target; its 10,000-entity simulation p95 was 127.2239 ms against 4 ms. M2 retained four target-free observations. M3 extraction/submission p95 values were 26.7673/3.3518 ms and both missed their 3 ms starting targets. M4 baseline p95 was 1.9282 ms and observed its 16.666667 ms target; stress 4/8 p95 values were 3.0410/4.4781 ms with no targets. |
| Five-repeat base and graphics M7 profile generators and validators | 0 | The two-workload base and three-workload graphics artifacts validated; timings remain diagnostic only. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | All ten unchanged real-wgpu integration tests passed in 6.88 seconds. |
| `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 30 --renderer wgpu --render-every 10` | 0 | Offscreen wgpu completed 30 ticks, three draws, 16 sprites, state hash `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`, and capture SHA-256 `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`. |
| `uv run --frozen --extra graphics python examples/agent_world_builder.py` | 0 | The typed-tool loop committed create/adjust work, completed three ticks, captured 320x180 RGBA8, passed registered tests, and recorded five replay batches. |
| Final whitespace, protected-surface, Git-object, identity, and artifact inventory audit | 0 | `git diff --check`, exact-base protected diff, and `git fsck --full --no-dangling` passed. CI/release workflow hashes remain `06a5e07918c83fc8de61e6746cb344f865b6421d81f554d79f4455d3718a3b21` and `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`; the exact 280-byte manifest hash remains pinned; the 94-entry wheel contains no native file; and the 36-entry sample bundle contains both M28 evidence files. |
| Final post-record formatting, Ruff, Pyright, focused tests, strict docs, and complete tests | 0 | All 239 Python files remained formatted; Ruff passed; Pyright reported zero diagnostics; 56 focused tests passed with one Windows symlink-capability skip in 2.39 seconds; strict docs built in 0.84 seconds with the known upstream warning; and 1,264 complete tests passed with five skips in 92.90 seconds. |

The findings-first review found no remaining scope, credential, privacy,
backend/native/WASM leakage, dependency-direction, wall-clock, history,
packaging, or stale-documentation issue. M28 changes no runtime source, public
API/export, persistent format, protocol, operation, dependency, lock, package
version, stability label, workflow, CI topology, tag, release, publication,
provider, network surface, or external fact. M1 simulation and both M3 targets
remain recorded misses and authorize no acceleration. At this local-validation
stage, ready-PR publication, hosted validation, thread-aware review, and squash
integration had not yet been executed; the later sections record their results.

## M28 hosted validation and review correction - PR #44

Ready PR #44 targets exact base
`17401eb32be30862496bbe02366d886a60752fb3`. Its DCO-signed implementation
head is `a1898a81218ae5674fd0347018c6062a5537f359` with tree
`7768d74ce536ce0c5201af804248dd01c9bac0b7` and that base as its sole parent.

GitHub Actions run `31175906134` executed the exact implementation head and
passed all eight unchanged essential jobs: quality/tests/distribution, Ubuntu
CPython 3.13, Ubuntu/macOS/Windows CPython 3.14, and real graphics on Ubuntu,
macOS, and Windows. No additional workflow, job, or matrix was created.

Thread-aware review found two valid P2 issues on that head. An unreviewed
custom manifest could expose nonzero game and author aggregates even though
its gate remained false. A syntactically safe HTTPS evidence locator did not
have to contain an immutable record identity. The correction exposes record-
derived counts, versions, scopes, outcomes, and presence only after the exact
manifest digest and complete mandatory history are admitted. It also requires
the locator path to contain the exact revision or one recorded source,
execution, or review digest.

| Correction command | Exit | Result |
| --- | ---: | --- |
| First review-correction static/focused/docs group | Mixed | Ruff formatting and lint, Pyright, and strict docs passed, but two duplicate-identity regressions failed because their fixtures did not yet preserve the new locator-identity invariant. No focused-suite pass is claimed from this group. |
| First corrected duplicate-fixture group | Mixed | All 57 focused tests passed with one Windows symlink-capability skip, and Ruff lint passed, but the leading format check reported one test file would be reformatted. No format pass is claimed from this group. |
| Final post-review format, Ruff, Pyright, focused tests, strict docs, report, and validator | 0 | All 239 Python files were formatted; Ruff passed; Pyright reported zero diagnostics; 57 focused tests passed with one skip in 2.19 seconds; strict docs built in 0.81 seconds with the known upstream warning; and the exact zero-game `not-ready` report and validator passed. The first sandboxed report rerun failed only on denied uv cache access; the approved rerun supplied the recorded report pass. |
| `uv run --frozen pytest -q` | 0 | The corrected complete suite passed 1,265 tests with five Windows symlink-capability skips in 88.39 seconds. |
| Corrected `uv build`, isolated wheel smoke, fresh release staging, and release smoke | 0 | Rebuilt the pure `0.1.0a1` sdist/wheel, passed isolated wheel smoke, staged a fresh ten-artifact candidate, and passed complete release smoke with the corrected bundled M28 evaluator. |

The correction changes only the M28 evaluator, regressions, readiness guide,
RFC, and factual `[retired control directory]` state. It does not widen scope or change runtime source,
public APIs/exports, persistent formats, dependencies, lock, version, workflow,
CI topology, tag, release, publication, provider, network behavior, or current
zero-adoption result.

Correction commit `36130c8a3d0923a7330ee2c9e287c11c2a52594c` is DCO-signed,
has tree `3e0fa65789beefb4dcb8a00489fe732b7124ca01`, and follows the
implementation commit directly. GitHub Actions run `31176729893` executed that
exact correction head from `2026-08-07T12:05:20Z` through
`2026-08-07T12:08:35Z` and passed all eight unchanged essential jobs. Its
quality job passed the lock, formatting, Ruff, Pyright, strict docs, full tests,
base profile smoke, pure build, isolated wheel smoke, deterministic release
staging, and release smoke. All four compatibility jobs and all three real-
graphics jobs passed.

GitHub reports ready PR #44 `MERGEABLE` and `CLEAN` against exact base
`17401eb32be30862496bbe02366d886a60752fb3`. The final thread-aware reread
reports both original P2 threads outdated after the adjacent corrections. The
current logic and regressions expose no unreviewed aggregates and reject a
locator without the exact revision or one recorded artifact digest. No new
review submission, comment, thread, or actionable finding exists. Neither
thread was replied to or manually resolved. The factual CI-skipping evidence
commit `c383a4f143fd8682059a89ff6b645104a6b4332d` has tree
`2f5ebf96af70741deb8d2b7d18ffa6d84effc494` and created no third workflow
run.

## M28 main integration - 2026-08-07

PR #44 squash-integrated exact final evidence head
`c383a4f143fd8682059a89ff6b645104a6b4332d` into `main` as commit
`90d58a4567e7c7eaff90a28a7c59f2453b6d4538` at `2026-08-07T12:11:14Z`.
GitHub reports a valid verification at `2026-08-07T12:11:19Z`. The squash
commit's sole parent is exact assigned base
`17401eb32be30862496bbe02366d886a60752fb3`; its tree is
`2f5ebf96af70741deb8d2b7d18ffa6d84effc494`, exactly matching the final PR
head, and its message retains `Signed-off-by: Louijie Compo
<louijie.compo@gmail.com>`. PR #44 is `MERGED`. Local `main`, `origin/main`,
and `origin/HEAD` were synchronized to the verified squash commit before the
documentation-only integration record was created.

| Integration-record command | Exit | Result |
| --- | ---: | --- |
| `gh pr view 44` and branch-scoped `gh run list` | 0 | PR #44 is merged from exact head `c383a4f143fd8682059a89ff6b645104a6b4332d` into exact base `17401eb32be30862496bbe02366d886a60752fb3` as `90d58a4567e7c7eaff90a28a7c59f2453b6d4538`; the branch has exactly the two successful CI runs `31175906134` and `31176729893`, so the final `[skip ci]` commit created no third run. |
| Local `git show`/`rev-parse` and GitHub commit API verification | 0 | The squash commit has the assigned base as its sole parent, exact final tree `2f5ebf96af70741deb8d2b7d18ffa6d84effc494`, retained DCO trailer, and valid GitHub verification. |
| `uv run --frozen mkdocs build --strict` | 0 | The six-file factual integration record built in 0.81 seconds with only the known upstream MkDocs Material/MkDocs 2.0 informational warning. |
| `git diff --check` | 0 | No whitespace errors. |
| `git diff --exit-code 90d58a4567e7c7eaff90a28a7c59f2453b6d4538 -- .github pyproject.toml uv.lock src/ludoweave` | 0 | Workflows, package metadata, lock, and all runtime source are unchanged. |
| `git fsck --full --no-dangling` | 0 | Repository object connectivity is clean with no dangling objects reported. |

## M27 development evidence - 2026-08-07, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| M26 feature/state integration verification and branch preparation | 0 | PR #40 squash-integrated the exact final M26 tree as GitHub-verified `a62d28e8c36d9a590e7ad7e7a9e8b49266dcbdde`; zero-run PR #41 integrated its exact five-file state tree as GitHub-verified `c1c3be08f7f75d90e7d1b517adbc30d56902ece4`; local `main` was clean and synchronized. |
| `git switch -c [historical branch name redacted]` | 0 | Created M27 from exact integrated `main` commit `c1c3be08f7f75d90e7d1b517adbc30d56902ece4`. |
| Initial contributor-document inspection | 1 | The inspection read `CONTRIBUTING.md` and related public templates but also requested nonexistent `docs/contributor-walkthrough.md`. No content is claimed from that path; the actual guide `docs/first-contribution.md` was located and read next. |
| `uv lock --check` | 0 | The unchanged lock resolved 46 packages in 0.82 ms. |
| Focused prior release/M25/M26 baseline | 0 | 64 tests passed with two Windows symlink-capability skips in 3.73 seconds. |
| M27 manifest identity probe | 0 | The reviewed external-contributor rehearsal manifest is exactly 270 bytes with SHA-256 `ecb959e90a0033b4dbe3dcfe8a48db1c1eea915e0ef2840510969b9e25cdb9c7` and contains zero rehearsal records. |
| Initial M27 format, Ruff, Pyright, focused tests, report, and whitespace group | 0 | Four files were reformatted; Ruff passed; Pyright reported zero diagnostics; 51 tests passed with one Windows symlink-capability skip in 1.74 seconds; the exact sanitized report was `not-ready`; and whitespace checks passed. |
| First artifact-wiring format, Ruff, Pyright, and focused test group | Mixed | Two files were reformatted; Pyright reported zero diagnostics and 53 tests passed with one Windows symlink-capability skip in 2.02 seconds, but Ruff reported import-order findings in both smoke scripts. The combined shell ended 0 because later commands succeeded, so no Ruff pass is claimed. |
| Corrected artifact-wiring Ruff group | 0 | Ruff mechanically sorted the two import blocks; both files were already formatted and Ruff then passed. |
| Findings-first hardening gate | 0 | Cross-role reuse of head/merge and patch/feedback identities plus duplicate JSON fields now fail closed; Ruff passed, Pyright reported zero diagnostics, 59 focused tests passed with one Windows symlink-capability skip in 2.03 seconds, strict docs built in 0.70 seconds, and whitespace passed. |

Synthetic populated rehearsal records prove evaluator mechanics only. They are
not contributors, public issues, pull requests, feedback, usability research,
adoption, project history, releases, or stability evidence.

## M27 final local validation - 2026-08-07, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| First combined lock/sync/static/test/docs gate in the managed sandbox | Mixed | All seven uv invocations failed before project execution because the sandbox denied access to existing user-cache metadata. The final whitespace command succeeded, making the combined shell exit 0; no uv check pass is claimed from this attempt. |
| Complete lock/sync/static/test/docs gate with approved cache access | 0 | The unchanged lock resolved 46 packages in 0.86 ms; 45 installed packages were checked; all 235 Python files were formatted; Ruff passed; Pyright reported zero diagnostics; 1,210 tests passed in 81.04 seconds with four Windows symlink-capability skips; and strict docs built in 0.72 seconds with the known upstream Material warning. |
| `uv build` | 0 | Built the `0.1.0a1` source distribution and pure `py3-none-any` wheel. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated installed-wheel smoke passed, including the explicit M27 reviewed-manifest evidence path. |
| Fresh M27 release staging and `scripts/smoke_release.py` | 0 | Staged the deterministic ten-artifact candidate and passed isolated release smoke, including the bundled M27 evaluator and empty reviewed manifest. |
| Documented M1-M4 benchmark generators and validators | 0 | All retained contracts validated; M1 observed one of two targets, M2 has no timing target, the M3 validator reported one of two targets met in this diagnostic run, and M4 observed its baseline target. These are inherited observations, not M27 performance claims. |
| Five-repeat base and graphics M7 profile generators and validators | 0 | The two-workload base and three-workload graphics artifacts validated; timings remain diagnostic only. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | All ten unchanged real-wgpu integration tests passed in 5.74 seconds. |
| Graphics vertical-slice commands | 0 | Thirty-tick wgpu Clockwork Arena and Agent World Builder completed with their expected deterministic structured summaries. |
| First combined final-report/scope/credential/artifact audit command | 1 | PowerShell rejected the command before execution because a quoted credential-pattern expression was unterminated. No audit result is claimed from this attempt. |
| Corrected current-report and Git scope/history audit | 0 | The exact sanitized report is `not-ready` with zero records and reason `external-contributor-rehearsal-absent`; runtime source, both workflows, project metadata, and lock are unchanged; whitespace and `git fsck --full --no-dangling` passed; the only retained “no external-contributor study” match is the deliberate current non-claim. |
| Credential-pattern, identity, and artifact inventory audit | 0 | Broad credential matches are deliberate security/sanitization text and tests only; CI/release workflow hashes remain `06a5e07918c83fc8de61e6746cb344f865b6421d81f554d79f4455d3718a3b21` and `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`; the exact manifest hash remains reviewed; the 94-entry wheel contains zero `.pyd`, `.so`, `.dll`, or `.dylib`; and the 34-entry sample bundle contains both M27 files. |

The final local review found no remaining scope, credential, backend/native
leakage, dependency-direction, wall-clock, packaging, privacy, history, or
stale-documentation finding. M27 adds no runtime source, public export,
persistent format, protocol, dependency, lock, version, workflow job, network
activity, telemetry, external fact, tag, release, or publication.

## M27 initial hosted failure and local correction - PR #42

Ready PR #42 targets exact base
`c1c3be08f7f75d90e7d1b517adbc30d56902ece4` from DCO-signed implementation
commit `c622ff534ba93639b9dae7fe3ce603a123709792`. Initial GitHub Actions run
`31118834216` exposed one project defect and one independent infrastructure
failure:

- Ubuntu CPython 3.13 and 3.14 each ran the complete tests and failed only
  `test_public_contributor_path_is_complete_but_claims_no_external_study`.
  The M27 test referenced `.github/PULL_REQUEST_TEMPLATE.md`, but the exact
  tracked path is lowercase `.github/pull_request_template.md`; Windows local
  validation could not expose the case-sensitive lookup defect.
- Windows graphics failed during runner setup before checkout. GitHub reported
  `Service Unavailable` and `Failed to resolve action download info`; no
  repository command ran.
- macOS graphics passed every graphics/provider/profile/sample step.

The M27 architecture test now uses the exact tracked lowercase filename. The
already-failed run was cancelled so its remaining queued jobs would not consume
quota. No workflow or production behavior changed. Corrected local and hosted
validation remain pending; no pass is claimed for run `31118834216`.

| Corrected case-sensitive path gate | Exit | Result |
| --- | ---: | --- |
| Ruff format/check, Pyright, focused tests, strict docs, and whitespace | 0 | The exact test file was formatted and Ruff-clean; Pyright reported zero diagnostics; 59 focused tests passed with one Windows symlink-capability skip in 2.00 seconds; strict docs built in 0.72 seconds; and whitespace passed. |

## M27 corrected hosted validation - PR #42

Corrected GitHub Actions run `31119640551` targets exact DCO-signed head
`f9e779d83a82795ad68cff22c424b6e94ef13703`. Attempt 1 completed graphics on
Ubuntu and Windows plus macOS CPython 3.14 successfully. GitHub's critical
Actions outage then caused quality/distribution and Ubuntu 3.13/3.14 plus
Windows 3.14 to fail during action download before checkout; macOS graphics
never received a runner and was cancelled. GitHub subsequently marked the
incident resolved and Actions operational. No repository failure is claimed
for those five affected jobs.

Exactly one failed-job-only rerun created attempt 2. It preserved the three
successful attempt-1 jobs and reran only the five affected jobs. Attempt 2
concluded `success` at `2026-08-07T10:40:14Z`; the effective run contains all
eight unchanged essential jobs as successes:

- quality, tests, and distribution passed in 2 minutes 34 seconds, including
  lock, formatting, Ruff, Pyright, strict docs, 1,210 baseline tests, profiling
  smoke, pure build, isolated-wheel smoke, release staging, and release smoke;
- compatibility passed on Ubuntu CPython 3.13 and 3.14, Windows CPython 3.14,
  and macOS CPython 3.14; and
- graphics/provider/profile/Clockwork Arena/Agent World Builder smoke passed
  on Ubuntu, Windows, and macOS.

`gh pr checks 42 --repo xsparc/ludoweave-engine` reported all eight checks as
`pass`. The workflow files remain unchanged. This validates M27's installed and
cross-platform paths; it does not establish an actual external contributor,
independent rehearsal, usability, adoption, release, publication, stability
promotion, or any inherited missed performance target.

After recording the hosted facts, `uv run --frozen mkdocs build --strict`,
`git diff --check`, and the protected-surface comparison against the exact M27
base all exited 0. The strict docs build completed in 0.88 seconds with only
the recorded upstream Material warning; `.github`, project metadata, lock, and
runtime source remain unchanged.

## M27 main integration - 2026-08-07

Final evidence head `349dc3b78dcae2b1c725ed3dc8e5e646ca3d3ac1` used `[skip ci]`.
`gh run list` returned only corrected run `31119640551` and initial cancelled
run `31118834216`; no workflow run was created for the evidence commit. GitHub
reported ready PR #42 as `MERGEABLE` and `CLEAN` at that exact head and exact
base `c1c3be08f7f75d90e7d1b517adbc30d56902ece4`. Local and GitHub history
inspection confirmed that all three branch commits contain a DCO
`Signed-off-by` trailer.

The final thread-aware reread found one unresolved, non-outdated automated
comment anchored to `[retired control file]`. It alleged missing DCO on
`b8dcedce82bb6da786297dd5a0942e4019f4df6e`, which is GitHub's ephemeral PR
test-merge commit and is absent from the exact three-commit branch history.
The comment therefore does not identify a branch defect; it was neither
answered nor manually resolved.

PR #42 was squash-merged at `2026-08-07T10:44:26Z`. GitHub reports merge
commit `ff1c81f8aaa96245706586096f400a5fb03bdd04`, sole parent
`c1c3be08f7f75d90e7d1b517adbc30d56902ece4`, tree
`f957c2e40eec5bd2d70cc274079ea334d6a34cc3`, valid signature verified at
`2026-08-07T10:44:31Z`, and the DCO trailer. `git rev-parse` returned the same
tree for final feature head and squash commit, and `git diff --exit-code`
between them exited 0. Local `main` then fast-forwarded cleanly to the verified
squash commit and matched `origin/main`.

This five-file integration record passes `uv run --frozen mkdocs build
--strict`, `git diff --check`, and the protected-surface comparison against
`origin/main`; all exited 0. The docs build completed in 0.73 seconds with only
the recorded upstream Material warning.

## M26 development evidence - 2026-08-07, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| M25 feature/state integration verification and branch preparation | 0 | PR #38 squash-integrated exact final M25 tree `fcaa7b11a4aa8d1c87e57a810db16682cf9f00e6` as GitHub-verified `9ec6eeaaed40fefeb64d738d4eaaf3f7a9c4009b`; zero-run PR #39 integrated its exact state tree as GitHub-verified `0de919a699dee6b10b6fef9ba2cdce5e3c0f2e62`; local `main` was clean and synchronized. |
| `git switch -c [historical branch name redacted]` | 0 | Created M26 from exact integrated `main` commit `0de919a699dee6b10b6fef9ba2cdce5e3c0f2e62`. |
| Initial release-policy scope probe | 1 | Relevant RFC/policy/workflow searches and RFC-0003 read succeeded, but the final `Get-Content docs/release.md` failed because that file does not exist. No content is claimed from it; the actual guide is `docs/release-process.md` and was read next. |
| `uv lock --check` | 0 | The unchanged lock resolved 46 packages in 0.91 ms. |
| Focused release/stability baseline | 0 | 61 release-workflow, artifact, command-stability, cross-version, external-feedback, and API-stability tests passed with one Windows symlink-capability skip in 5.90 seconds. |
| M26 manifest and workflow identity probes | 0 | The reviewed release-channel manifest is exactly 278 bytes with SHA-256 `f23b4314696384ad288b86c63bc101606f1aa9f323c4fb186486d8c74915ec41`; the unchanged release workflow SHA-256 is `d1d61988e48e752d1d100f4ac3ad4df9508590dba6e87bd0344d9101aa5e5dd8`. |
| First M26 focused format, Ruff, Pyright, tests, and report group | Mixed | Two files were reformatted. Ruff alone exited 1 on B905/RUF007 for a successive-pair `zip`; Pyright reported zero diagnostics, 35 tests passed with one Windows symlink-capability skip in 1.66 seconds, and the sanitized current report was `not-ready`. The combined shell ended 0 only because later commands succeeded, so no Ruff pass is claimed. |
| Focused gate after simplifying the unique-version order check | 0 | All four files were formatted, Ruff passed, Pyright reported zero diagnostics, and 35 tests passed with one Windows symlink-capability skip in 1.65 seconds. |
| M26 artifact-wiring static and focused test group | 0 | Four artifact files were already formatted, Ruff and Pyright were clean, and 37 tests passed with one Windows symlink-capability skip in 2.00 seconds. |
| Post-hardening focused static/docs group | 0 | Canonical project-tag URL, explicit non-draft/non-prerelease status, unique publication identity, and exact public-policy checks were added; Ruff passed, Pyright reported zero diagnostics, strict docs built in 0.73 seconds, and whitespace checks passed. |
| First post-hardening focused pytest command | 1 | Pytest rejected the nonexistent path `tests/integration/test_release_workflow.py` and ran zero tests. The actual module was located at `tests/architecture/test_release_workflow.py`; no test result is claimed from this attempt. |
| Corrected post-hardening focused pytest command | 0 | 46 release-channel, artifact, and release-workflow tests passed with one Windows symlink-capability skip in 2.00 seconds. |

The synthetic canonical-shaped project-tag URLs identify nonexistent releases
and prove only evaluator mechanics. They are not tags, publications, support
commitments, release history, a deprecation channel, or stability promotion.

## M26 final local validation - 2026-08-07, Windows, CPython 3.12.13

Findings-first review added exact canonical project-tag URL enforcement,
explicit non-draft/non-prerelease state, publication-identity uniqueness, and
matching regressions. A later documentation audit corrected the stale README
milestone status and described M25/M26 without changing runtime behavior.

| Command | Exit | Result |
| --- | ---: | --- |
| First combined `uv lock --check` and `uv sync --frozen --all-groups --extra graphics` in the managed sandbox | 1 | Both uv commands failed before project execution because the sandbox denied access to existing user-cache metadata; no lock or sync pass is claimed from this attempt. |
| `uv lock --check` and `uv sync --frozen --all-groups --extra graphics` with approved cache access | 0 | The unchanged lock resolved 46 packages in 0.71 ms and 45 installed packages were checked. |
| Complete formatting, Ruff, Pyright, strict docs, and whitespace group | 0 | All 231 Python files were formatted, Ruff passed, Pyright reported zero diagnostics, strict docs built in 0.73 seconds with the known upstream Material warning, and `git diff --check` passed. |
| `uv run --frozen pytest -q` | 0 | 1,152 tests passed in 79.27 seconds; three Windows symlink-capability probes skipped because link creation was unavailable. |
| First `uv build` in the managed sandbox | 1 | uv could not access its existing user cache, so no build result is claimed from this attempt. |
| `uv build` with approved cache access | 0 | Built the `0.1.0a1` source distribution and pure `py3-none-any` wheel. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated installed-wheel smoke passed, including the explicit M26 source-manifest evidence path. |
| Fresh M26 release staging and `scripts/smoke_release.py` | 0 | Staged the deterministic ten-artifact candidate and passed isolated release smoke, including the bundled empty reviewed release-channel manifest. |
| Documented M1-M4 benchmark generators and validators | 0 | All four retained artifact contracts validated; M1 observed one of two targets, M2 has no timing target, M3 observed zero of two targets, and M4 observed its baseline target. These are inherited observations, not M26 claims. |
| Five-repeat base and graphics M7 profile generators and validators | 0 | The two-workload base and three-workload graphics artifacts validated; timings remain diagnostic only. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | All 10 unchanged real-wgpu integration tests passed in 6.24 seconds. |
| Graphics vertical-slice commands | 0 | Thirty-tick wgpu Clockwork Arena and Agent World Builder completed with their expected deterministic structured summaries. |
| Current M26 report execution | 0 | The exact sanitized report is `not-ready`, has zero release records and feature lines, and retains reason `supported-feature-release-channel-absent`. |
| Protected-scope, manifest, credential-pattern, artifact, history, and Git-object audit | 0 | Runtime source, workflows, metadata, dependency lock, M24/M25 reviewed manifests, and the release workflow remain unchanged; the M26 manifest hash is exact; the 94-entry wheel has no `.pyd`, `.so`, `.dll`, or `.dylib`; the 32-entry sample bundle contains both M26 files; broad credential matches are deliberate sanitization text/tests only; `HEAD` and its merge-base with `main` are exact assigned base; and `git fsck --full --no-dangling` passed. |
| Final post-documentation formatting, Ruff, Pyright, strict docs, tests, and whitespace recheck | 0 | All 231 Python files remained formatted; Ruff passed; Pyright reported zero diagnostics; strict docs built in 0.75 seconds with the known upstream Material warning; 1,152 tests passed with three Windows symlink-capability skips in 79.11 seconds; and `git diff --check` passed. |

The implementation commit and hosted evidence are recorded below.

## M26 hosted validation and initial thread-aware review - PR #40

Ready PR #40 targets exact base
`0de919a699dee6b10b6fef9ba2cdce5e3c0f2e62` from DCO-signed implementation
commit `835ac2b2f3dd8bfe5a31fe9f880a43555e86fd34`. Its sole GitHub Actions run
`31115252696` completed successfully across the unchanged eight-job topology:

| Job | Result |
| --- | --- |
| Quality, tests, and distribution | Passed formatting, Ruff, Pyright, strict docs, non-provider tests, base profile, pure build, installed-wheel smoke, release staging, and release smoke. |
| Compatibility - Ubuntu 3.13 | Passed. |
| Compatibility - Ubuntu 3.14 | Passed. |
| Compatibility - Windows 3.14 | Passed. |
| Compatibility - macOS 3.14 | Passed. |
| Graphics smoke - Ubuntu | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |
| Graphics smoke - Windows | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |
| Graphics smoke - macOS | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |

GitHub reports PR #40 open, ready, `MERGEABLE`, and `CLEAN`, with the exact
head/base above and all eight checks successful. The first GraphQL thread-aware
read returned no issue comment, review, or inline review thread.

This hosted pass does not establish a supported release, recurring channel,
support promise, cross-version execution, external consumer feedback,
stability promotion, tag, GitHub release, or PyPI publication. DCO-signed
factual evidence commit `3ac2b0786d588ab844978703a01d692c282927cb`
used `[skip ci]`, was pushed, and created no additional run.

## M26 delayed-review correction - PR #40

At `2026-08-06T15:22:47Z`, delayed automated review of implementation commit
`835ac2b2f3dd8bfe5a31fe9f880a43555e86fd34` added one unresolved, non-outdated
P2 thread: a future reviewer could pin a nonempty manifest digest without
updating the empty mandatory prefix, so append-only history would remain
vacuously true.

The correction requires a reviewed manifest's complete identity sequence to
equal the executable mandatory prefix. An unreviewed append-only candidate may
still show preserved prior history, but it cannot satisfy the gate. The
synthetic true-gate and patch-cadence tests now pin both the digest and complete
prefix, and a dedicated regression proves digest-only pinning fails with
`historical-release-record-missing`.

| Command | Exit | Result |
| --- | ---: | --- |
| First correction Ruff, Pyright, focused tests, strict docs, and whitespace group | Mixed | Ruff and Pyright passed, strict docs built in 0.76 seconds, and whitespace passed. The focused suite ran 47 tests with one Windows symlink skip but one patch-cadence assertion failed because that fixture intentionally pinned only the digest after the new guard; no focused test pass is claimed. |
| Corrected focused Ruff, Pyright, tests, strict docs, and whitespace group | 0 | Ruff passed, Pyright reported zero diagnostics, 47 tests passed with one Windows symlink-capability skip in 2.07 seconds, strict docs built in 0.77 seconds, and whitespace passed. |
| Corrected `uv lock --check` and complete static/docs gate | 0 | The unchanged lock resolved 46 packages; all 231 Python files were formatted; Ruff passed; Pyright reported zero diagnostics; strict docs built in 0.75 seconds; and whitespace passed. |
| Corrected `uv run --frozen pytest -q` | 0 | 1,153 tests passed in 79.01 seconds; the three Windows symlink-capability probes skipped. |
| Corrected pure build, isolated wheel smoke, fresh release staging, and release smoke | 0 | The pure wheel/sdist rebuilt; installed-wheel M26 evidence passed; a fresh ten-artifact release candidate executed the bundled corrected evaluator successfully. |
| First combined corrected-report and scope audit group | Mixed | The report command alone failed before execution because the sandbox denied uv user-cache access. Subsequent whitespace, protected-scope, status, and Git-object checks ran successfully; no report pass is claimed from this attempt. |
| Corrected report with approved cache access | 0 | The exact sanitized current report remains `not-ready` with zero releases and reason `supported-feature-release-channel-absent`. |

No reply or manual resolution was performed on the review thread. A DCO-signed
correction commit, one necessary corrected hosted run, final thread-aware
reread, and squash integration remain pending.

## M26 corrected hosted validation and final thread-aware reread - PR #40

DCO-signed correction commit
`ad73e641605ee1622e8168a73183f9987d9f9254` was pushed once. Corrected
GitHub Actions run `31116147333` passed the quality/distribution job, all four
compatibility jobs, and Linux/macOS graphics on its first attempt. Its Windows
graphics job failed entirely during runner setup: GitHub reported `Service
Unavailable` and then `Internal Server Error` while resolving action-download
information. Checkout and every repository command were never reached.

Only that failed job was rerun. Run attempt 2 completed successfully: Windows
graphics checked out the exact corrected head and passed the locked graphics
install, ten real-wgpu tests, graphics profile, Clockwork Arena, and Agent World
Builder. GitHub now reports corrected run `31116147333` successful with all
eight status checks successful.

`gh run list` returns exactly two M26 branch runs: initial successful run
`31115252696` on implementation commit
`835ac2b2f3dd8bfe5a31fe9f880a43555e86fd34` and corrected successful run
`31116147333` on exact correction head above. The earlier factual evidence
commit used `[skip ci]` and created no additional run.

PR #40 is open, ready, `MERGEABLE`, and `CLEAN` against exact assigned base
`0de919a699dee6b10b6fef9ba2cdce5e3c0f2e62`. The final GraphQL thread-aware
reread returns the original P2 thread unresolved but outdated. The corrected
gate requires the complete reviewed identity sequence to equal the mandatory
prefix, and the dedicated digest-only regression passes. No finding remains
actionable. No reply or manual thread resolution was performed.

The successful corrected checks do not establish a supported release,
recurring channel, support promise, cross-version execution, external consumer
feedback, stability promotion, tag, GitHub release, or PyPI publication. A
final CI-skipping factual evidence commit and squash integration remain.

## M26 main integration - 2026-08-07

Ready PR #40 was squash-merged at `2026-08-06T15:40:42Z`. GitHub reports merged
commit `a62d28e8c36d9a590e7ad7e7a9e8b49266dcbdde` with sole parent
`0de919a699dee6b10b6fef9ba2cdce5e3c0f2e62`, tree
`e1f39a9c5d2bc81f76b45288225b27a7c782bf50`, DCO sign-off, and valid GitHub
verification at `2026-08-06T15:40:46Z`. The tree exactly matches final feature
evidence head `ac8dd43e6b93bc89af1f5dd1821948e4860ac88b`; the milestone branch is
retained for audit history.

GitHub lists only initial successful run `31115252696` and necessary corrected
run `31116147333` for the milestone branch. The corrected run's first attempt
had a GitHub action-download setup outage on Windows graphics before checkout;
its failed-job-only second attempt passed. Both factual evidence commits used
`[skip ci]` and created no additional run.

Integration changes no runtime source, API/export, protocol, workflow,
dependency, lock, version, support promise, external fact, tag, release, or
publication. Local `main` fast-forwarded cleanly to the verified squash commit;
quoted tree probes, sole-parent inspection, DCO message inspection, and
`git fsck --full --no-dangling` passed.

The integration-record branch changes exactly `[retired control directory]/CURRENT_TASK.md`,
`[retired control directory]/PROJECT_STATE.md`, `[retired control directory]/TEST_EVIDENCE.md`, `[retired control file]`, and `ROADMAP.md`.
Strict docs built in 0.72 seconds with the known upstream Material warning;
whitespace, exact scope, and Git-object checks passed. The state commit and PR
must use `[skip ci]` and create no Actions run.

## M25 development evidence - 2026-08-07, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| M24 feature/state integration verification and branch preparation | 0 | PR #36 squash-integrated the exact corrected M24 tree as GitHub-verified `b7b16697d28410567cbddf8eb962c7e6c9e664b8`; zero-run PR #37 integrated its exact state tree as GitHub-verified `680e90dd8f9377fece23c43bd9f07ca9d76297de`; local `main` was clean and synchronized before branch creation. |
| `git switch -c [historical branch name redacted]` | 0 | Created M25 from exact integrated `main` commit `680e90dd8f9377fece23c43bd9f07ca9d76297de`. |
| `uv lock --check` | 0 | The unchanged lock resolved 46 packages in 0.88 ms. |
| Focused M20/M24/release baseline | 0 | 45 tests passed in 4.40 seconds. |
| M25 manifest identity probe | 0 | The reviewed feedback manifest is exactly 283 bytes with SHA-256 `b113444f60946461ec6774e2c278b9e82e7d80e08a37450b6cc153e5c5c1500e` and contains zero feedback records. |
| First M25 format, Ruff, Pyright, example, integration, and architecture group | 0 | Two files were reformatted; Ruff passed; Pyright reported zero diagnostics; the sanitized current report was `not-ready`; and 29 strict-evidence, synthetic-gate, history, malformed-record, boundary, and scope tests passed in 1.96 seconds. |

The synthetic `.invalid` consumer proves only evaluator behavior. It is not an
external consumer, feedback artifact, adoption result, release, or stability
promotion. Full docs, repository, wheel/release, graphics/profile, review, and
hosted validation remain pending.

## M25 final local validation - 2026-08-07, Windows, CPython 3.12.13

Findings-first review identified that CLI path normalization dereferenced an
explicit symlink before the documented symlink rejection. The correction keeps
the selected path intact for the bounded reader and also rejects credential-
bearing, local-host, Unicode, and backslash HTTPS locator forms. The focused
post-correction gate passed 35 tests with one Windows symlink-capability skip in
2.23 seconds; Ruff and strict Pyright remained clean.

| Command | Exit | Result |
| --- | ---: | --- |
| First combined lock/sync/static gate in the managed sandbox | 1 | uv could not open its existing user-cache metadata; all five uv invocations failed before project execution, so no pass is claimed for this attempt. |
| `uv lock --check` and `uv sync --frozen --all-groups --extra graphics` with approved cache access | 0 | The unchanged lock resolved 46 packages and 45 installed packages were checked. |
| `uv run --frozen ruff format --check .` | 0 | All 227 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All checks passed. |
| `uv run --frozen pyright` | 0 | Zero errors, warnings, or information messages. |
| `uv run --frozen pytest -q` | 0 | 1,109 tests passed in 79.58 seconds; the inherited Windows symlink-capability probe and the new explicit-manifest symlink probe skipped because link creation was unavailable. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built in 0.69 seconds; Material printed its known upstream MkDocs 2.0 warning. |
| `uv build` | 0 | Built the `0.1.0a1` source distribution and pure `py3-none-any` wheel. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated installed-wheel smoke passed, including the explicit M25 source-manifest evidence path. |
| Fresh M25 release staging and `scripts/smoke_release.py` | 0 | Staged the deterministic ten-artifact candidate and passed isolated release smoke, including the bundled empty reviewed feedback manifest. |
| Documented M1-M4 benchmark artifact generators and validators | 0 | All four retained artifact contracts validated; M1 observed one of two targets, M2 has no timing target, M3 observed zero of two targets, and the M4 baseline target was observed. These are inherited observations, not M25 claims. |
| Five-repeat base and graphics M7 profile generators and validators | 0 | The two-workload base and three-workload graphics artifacts validated. Timings remain diagnostic only. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | All 10 unchanged real-wgpu integration tests passed in 6.31 seconds. |
| Graphics vertical-slice commands | 0 | Thirty-tick wgpu Clockwork Arena and Agent World Builder completed with their expected deterministic structured summaries. |
| Scope, whitespace, credential-pattern, Git-object, and stale-reference audit | 0 | Runtime source, workflow, metadata, lock, immutable M21 receipt fixtures, and M24 corpus are unchanged; `git diff --check` and `git fsck --full --no-dangling` passed. Broad credential-pattern results were existing tests/code identifiers or deliberate sanitization fixtures; no new credential value is present. |
| Final static/docs, ancestry, and wheel inventory recheck | 0 | Formatting, Ruff, strict Pyright, strict docs, whitespace, and Git object checks passed; `HEAD` and its merge-base with `main` were exact assigned base `680e90dd8f9377fece23c43bd9f07ca9d76297de`; the current pure wheel contains 94 entries and zero `.pyd`, `.so`, `.dll`, or `.dylib` entries. |

The final audit found no remaining scope, credential, backend/native leakage,
dependency-direction, wall-clock, packaging, or stale-documentation finding.
M25 adds no runtime source, public export, protocol, dependency, lock, version,
workflow job, network activity, telemetry, stability promotion, external fact,
tag, release, or publication. Commit, ready PR, hosted validation, delayed
thread-aware review, and squash integration remain pending.

## M25 hosted validation and initial thread-aware review - PR #38

Ready PR #38 targets exact base
`680e90dd8f9377fece23c43bd9f07ca9d76297de` from DCO-signed implementation
commit `9667e020c2213d415072b7c7efbd880f6b58abfa`. GitHub Actions run
`31111498136` completed successfully across the unchanged eight-job topology:

| Job | Result |
| --- | --- |
| Quality, tests, and distribution | Passed formatting, Ruff, Pyright, strict docs, non-provider tests, base profile, pure build, installed-wheel smoke, release staging, and release smoke. |
| Compatibility - Ubuntu 3.13 | Passed. |
| Compatibility - Ubuntu 3.14 | Passed. |
| Compatibility - Windows 3.14 | Passed. |
| Compatibility - macOS 3.14 | Passed. |
| Graphics smoke - Ubuntu | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |
| Graphics smoke - Windows | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |
| Graphics smoke - macOS | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |

`gh run list` returned exactly that one run for the M25 branch. GitHub reports
PR #38 open, ready, `MERGEABLE`, and `CLEAN`, with the exact head and base
above and all eight checks successful. The first GraphQL thread-aware read
returned no issue comment, review, or inline review thread.

This hosted pass does not establish an external consumer, feedback, adoption,
cross-version release history, supported release channel, stability promotion,
tag, GitHub release, or PyPI publication. A CI-skipping factual evidence commit,
delayed thread-aware reread, and squash integration remain.

## M25 delayed-review correction - PR #38

At `2026-08-06T14:39:01Z`, delayed automated review of implementation commit
`9667e020c2213d415072b7c7efbd880f6b58abfa` added one unresolved, non-outdated
P2 thread: numeric authorities such as loopback or link-local IPs passed the
future HTTPS locator syntax gate. The finding is valid because a later pinned
manifest could otherwise produce a true gate from a non-public authority.

The correction requires the authority's final DNS-style label to contain an
alphabetic character, while the existing label/ASCII/credential/port checks
continue to reject IPv6 literals and malformed hosts. Exact regressions reject
`127.0.0.1` and `169.254.169.254`. Documentation now states the non-IP
authority boundary.

| Command | Exit | Result |
| --- | ---: | --- |
| Focused correction format, Ruff, Pyright, integration/architecture/release tests, and strict docs | 0 | Files were already formatted; Ruff passed; Pyright reported zero diagnostics; 37 tests passed with one Windows symlink-capability skip in 2.30 seconds; strict docs built in 0.70 seconds. |
| Corrected `uv lock --check` and complete static gate | 0 | The unchanged 46-package lock, all 227-file formatting, Ruff, and strict Pyright passed. |
| Corrected `uv run --frozen pytest -q` | 0 | 1,111 tests passed in 78.06 seconds; the two Windows symlink-capability probes skipped. |
| Corrected strict docs, pure build, isolated wheel smoke, and fresh release smoke | 0 | Strict docs built in 0.70 seconds; the pure wheel/sdist built; installed-wheel evidence passed; and a fresh ten-artifact release candidate executed the bundled M25 evidence successfully. |
| Corrected protected-scope, whitespace, and Git-object audit | 0 | Runtime source, workflow, metadata, lock, and the exact reviewed empty manifest remain unchanged; `git diff --check` and `git fsck --full --no-dangling` passed. |

No reply or manual resolution was performed on the review thread. A DCO-signed
correction commit, one necessary corrected hosted run, final thread-aware
reread, and squash integration remain.

## M25 corrected hosted validation and final thread-aware reread - PR #38

DCO-signed correction commit
`90ed57e360765cf7f2d0973e41b8f8ec06dc4b50` was pushed once. GitHub Actions
run `31112342328` completed successfully across all eight unchanged essential
jobs: quality/tests/distribution; Ubuntu 3.13 and 3.14; Windows 3.14; macOS
3.14; and real graphics on Ubuntu, Windows, and macOS.

`gh run list` returned exactly two M25 branch runs: initial successful run
`31111498136` on implementation commit
`9667e020c2213d415072b7c7efbd880f6b58abfa` and necessary successful
correction run `31112342328` on exact corrected head above. PR #38 is open,
ready, `MERGEABLE`, and `CLEAN` against exact assigned base
`680e90dd8f9377fece23c43bd9f07ca9d76297de`, with all corrected-head checks
successful.

The final GraphQL thread-aware reread returned no issue comment and one review
with its original inline P2 thread. The thread remains unresolved and non-
outdated because the same conditional anchor persists at line 306. The anchored
code now requires an alphabetic DNS-style top-level label, rejecting the exact
numeric IP examples named by review, and dedicated loopback/link-local
regressions pass. No finding remains actionable. No reply or manual thread
resolution was performed.

The successful corrected checks do not establish an external consumer,
feedback, adoption, cross-version release history, supported release channel,
stability promotion, tag, GitHub release, or PyPI publication. A final
CI-skipping factual evidence commit and squash integration remain.

## M25 main integration - 2026-08-07

Ready PR #38 was squash-merged at `2026-08-06T14:49:28Z`. GitHub reports merged
commit `9ec6eeaaed40fefeb64d738d4eaaf3f7a9c4009b` with sole parent
`680e90dd8f9377fece23c43bd9f07ca9d76297de`, tree
`fcaa7b11a4aa8d1c87e57a810db16682cf9f00e6`, DCO sign-off, and valid GitHub
verification at `2026-08-06T14:49:33Z`. The tree exactly matches final feature
evidence head `d0866967832fe80a49942184e1ab81d3c426a478`; the milestone branch
is retained for audit history.

The first combined post-merge command omitted PowerShell-safe quoting around
two `^{tree}` revision expressions. PowerShell rewrote those two arguments and
both `git rev-parse` subcommands emitted fatal ambiguous-revision errors; no
tree result is claimed from them. The same tree probes were rerun with quoted
revisions and exited 0, returning exact matching tree
`fcaa7b11a4aa8d1c87e57a810db16682cf9f00e6` for final feature head and
`origin/main`. The remaining fetch, commit metadata, and GitHub verification
steps in the first command completed successfully.

GitHub lists only initial successful run `31111498136` and necessary successful
correction run `31112342328` for the milestone branch; both factual evidence
commits used `[skip ci]` and created no additional run. Integration changes no
runtime source, API/export, protocol, workflow, dependency, lock, version,
stability label, or reviewed-manifest byte. No tag, GitHub release, PyPI
publication, actual external feedback, adoption, certification, cross-version
release history, supported release channel, or stability promotion is claimed.

After `git fetch origin main`, local `main` fast-forwarded cleanly from assigned
base to verified squash commit `9ec6eeaaed40fefeb64d738d4eaaf3f7a9c4009b`.
`[historical branch name redacted]` was created from that exact commit for this factual
record. Strict docs, whitespace, scope, Git-object, commit/tree, zero-extra-run,
and review-state checks precede its CI-skipping publication.

## M24 development evidence - 2026-08-06, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| M23 feature/integration PR verification, `git fetch`, fast-forward, and `git fsck --full --no-dangling` | 0 | PR #34 squash was GitHub-verified as exact-tree commit `2f7152565d369225dbf69055b7d42a4c80f46d1a`; zero-run PR #35 integrated its exact-tree state record as GitHub-verified `55c7a72337913303b6b1f6bd31edbca7ff28683b`; local `main` was clean and synchronized. |
| M24 branch creation | 128 | The first sandboxed `git switch -c` could not create the Git ref lock; no branch was created. The same command was rerun with approved repository-metadata access. |
| `git switch -c [historical branch name redacted]` | 0 | Created M24 from exact integrated `main` commit `55c7a72337913303b6b1f6bd31edbca7ff28683b`. |
| M21 manifest identity probe | 0 | Preserved source manifest remained exactly 762 bytes with SHA-256 `ed3f1040294376fafce523e129897ce756d785b2f6d90c54335ad5f8abb84ac3`. |
| `uv lock --check` | 0 | Baseline lock remained current; 46 packages resolved in 0.76 ms. |
| Focused receipt corpus/reader/policy/architecture baseline | 0 | 71 tests passed in 4.05 seconds. |
| First M24 format/Ruff/Pyright/example group | 0 | The new example was formatted, Ruff passed, Pyright reported zero diagnostics, and one sanitized `not-ready` report printed with both missing-gate reasons. |
| First M24 integration/architecture group | 0 | 19 exact-evidence, tamper, safe-path, synthetic future-gate, import-boundary, and scope tests passed in 1.77 seconds. |
| M24 artifact-wiring static and focused test group | 0 | Four artifact files were already formatted, Ruff and Pyright were clean, and 21 tests passed in 2.19 seconds. |

The synthetic `0.1.0a2` test proves only gate logic. It is not a package build,
supported release, cross-version history, external consumer result, or preview
promotion. Full docs, repository, wheel/release, provider, and review validation
remain pending.

## M24 final local validation - 2026-08-06, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| Expanded M21-M24 format/Ruff/Pyright/receipt/artifact/docs group | 0 | All 223 Python files were formatted, Ruff and Pyright were clean, 92 focused tests passed in 5.78 seconds, and strict docs built in 0.67 seconds. |
| First M24 `uv build`, isolated wheel smoke, fresh release staging/smoke | 0 | Built the pure wheel/sdist; installed-wheel evidence passed; fresh 10-artifact release candidate included and executed the exact preserved corpus; release smoke passed. |
| `uv run --frozen pytest -q` before final review hardening | 0 | 1,072 tests passed in 81.59 seconds; one existing Windows symlink-capability test skipped. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | 10 unchanged real-wgpu integration tests passed in 6.35 seconds. |
| Hosted graphics vertical-slice commands | 0 | Thirty-tick wgpu Clockwork Arena and Agent World Builder completed with their expected deterministic structured summaries. |
| Base and graphics M7 profile contract smokes | 0 | Two-workload base and three-workload graphics artifacts validated with one repeat. Timing remains diagnostic only. |
| Final `uv lock --check`, Ruff format/check, Pyright, and strict MkDocs | 0 | Lock resolved 46 packages in 0.80 ms; 223 files were formatted; Ruff passed; Pyright reported zero diagnostics; docs built in 0.72 seconds. |
| Final `uv run --frozen pytest -q` | 0 | 1,074 tests passed in 78.93 seconds; one existing Windows symlink-capability test skipped. |
| Final `uv build` and isolated wheel/release smoke using `.tmp/release-candidate-m24-review-final` | 0 | Fresh absent target produced the pure wheel/sdist and deterministic 10-artifact release candidate; both isolated smokes passed. |

Findings-first review identified three issues before publication. A pre-stat
followed by `read_bytes()` left a local change-between-check/read window;
bounded streaming, child-directory confinement, and symlink rejection replace
it. A caller-selected manifest could otherwise self-declare future release
records; the exact reviewed corpus SHA-256 is now pinned by executable evidence
and the strict validator, with a negative arbitrary-manifest regression.
Finally, manifest byte bounds alone did not cap child work or declared receipt
size; source manifests, fixtures, receipts, and supported-release records now
have explicit caps and exact release-version coverage. The final 26-test
hardening group passes in 2.42 seconds. No runtime, dependency, lock, package-
version, workflow, or CI-topology change is included.

Final strict MkDocs rebuilt in 0.67 seconds, `git diff --check` and
`git fsck --full --no-dangling` exited 0, changed/new-file credential-assignment
and trailing-whitespace scans matched nothing, and the scope diff remained
empty for `src/`, `.github/`, `pyproject.toml`, `uv.lock`, and the immutable
`tests/fixtures/receipt_v1` corpus.

## M24 hosted validation and initial thread-aware review - PR #36

Ready PR #36 targets exact base
`55c7a72337913303b6b1f6bd31edbca7ff28683b` from DCO-signed implementation
commit `e590d482246d122120c011969b47f79f9680efa2`. GitHub Actions pull-request
run `31107800179` executed that exact head from `2026-08-06T13:50:00Z` through
`2026-08-06T13:52:57Z` and concluded `success` across the unchanged eight-job
topology:

| Hosted job | Result |
| --- | --- |
| Quality, tests, and distribution - Ubuntu, Python 3.12 | Passed lock verification, formatting, Ruff, strict Pyright, strict docs, baseline tests, base profile smoke, pure build, isolated wheel smoke, release staging, and isolated release smoke. |
| Compatibility - Ubuntu, Python 3.13 | Passed. |
| Compatibility - Ubuntu, Python 3.14 | Passed. |
| Compatibility - Windows, Python 3.14 | Passed. |
| Compatibility - macOS, Python 3.14 | Passed. |
| Graphics smoke - Ubuntu | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |
| Graphics smoke - Windows | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |
| Graphics smoke - macOS | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |

`gh run list` returned exactly that one run for the M24 branch. After completion,
GitHub reported PR #36 open, ready, `MERGEABLE`, and `CLEAN`, with exact head
and base above and all eight checks `SUCCESS`. The first GraphQL thread-aware
read returned no issue comment, review, or inline review thread. No workflow or
job topology changed. This evidence does not claim actual cross-version package
history, supported release records, external consumer feedback, stability
promotion, tag, GitHub release, or PyPI publication. Final delayed-review reread
and squash integration remain.

## M24 delayed-review correction - PR #36

At `2026-08-06T13:54:48Z`, delayed automated review of implementation commit
`e590d482246d122120c011969b47f79f9680efa2` added one unresolved, non-outdated
P1 thread. The finding was valid: changing only the reviewed whole-manifest
digest could allow a future source list to replace the M21 entry, contradicting
RFC-0007's append-only rule. No reply or manual thread resolution was
performed.

The correction adds executable frozen prefixes for exact source-manifest and
supported-release identities, makes their preservation an independent gate,
and reports `historical-corpus-entry-missing` when it fails. A new regression
pins a synthetic future manifest with complete release coverage after replacing
the `receipt_v1` directory identity; every other gate becomes true while the
history gate and overall admission remain false.

| Command | Exit | Result |
| --- | ---: | --- |
| Focused format, Ruff, Pyright, installed example, and M24/release tests | 0 | One file was reformatted; Ruff passed, Pyright reported zero diagnostics, the report included `historical_entries_preserved: true`, and 28 focused tests passed in 2.66 seconds. |
| First correction `uv lock --check` | 1 | The managed sandbox denied access to uv's existing user cache before project execution; no lock pass is claimed for this attempt. |
| Approved `uv lock --check` rerun | 0 | The unchanged lock resolved 46 packages in 0.77 ms. |
| `uv run --frozen ruff format --check .` | 0 | All 223 Python files were formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, and 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 1,076 tests passed in 81.42 seconds; one existing Windows symlink-capability test skipped. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict docs built in 0.75 seconds with only the recorded upstream Material/MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built the pure `ludoweave-0.1.0a1` source distribution and universal wheel. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated installed-wheel smoke passed with the corrected exact report. |
| Fresh release staging and `smoke_release.py` at `.tmp/release-candidate-m24-review-correction` | 0 | The target was confirmed absent, ten artifacts were staged, and isolated release smoke passed for `0.1.0a1`. |

After synchronizing the correction record, strict MkDocs rebuilt in 0.70
seconds, `git diff --check` and `git fsck --full --no-dangling` exited 0, and
the focused credential-assignment scan returned no match. The first scope query
exited 1 because it mistakenly included the intentionally new M24 admission
manifest in a comparison to the pre-M24 base; it showed only that expected
addition. Corrected checks compare protected runtime/workflow/metadata/lock and
the immutable M21 corpus to the assigned base, and the M24 admission-manifest
bytes to prior evidence head `bebae10b8c9e1b663e0555bdc941ede9be8d0a12`;
both exited 0.

The correction changes no runtime source, public API/export, protocol,
dependency, lock, package version, workflow, or CI topology. Correction commit,
push, one necessary hosted run, final thread-aware reread, and squash integration
remain.

## M24 corrected hosted validation and final thread-aware reread - PR #36

DCO-signed correction commit
`b393d6857f0a60c5d124fdeb25b3779c8f9dab86` was pushed once. GitHub Actions
pull-request run `31108924069` executed that exact head from
`2026-08-06T14:03:36Z` through `2026-08-06T14:06:16Z` and concluded `success`.
All eight unchanged essential jobs passed:

| Hosted job | Result |
| --- | --- |
| Quality, tests, and distribution - Ubuntu, Python 3.12 | Passed lock, formatting, Ruff, strict Pyright, strict docs, baseline tests, base profile smoke, pure build, isolated wheel smoke, release staging, and isolated release smoke. |
| Compatibility - Ubuntu, Python 3.13 | Passed. |
| Compatibility - Ubuntu, Python 3.14 | Passed. |
| Compatibility - Windows, Python 3.14 | Passed. |
| Compatibility - macOS, Python 3.14 | Passed. |
| Graphics smoke - Ubuntu | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |
| Graphics smoke - Windows | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |
| Graphics smoke - macOS | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |

GitHub lists exactly two M24 branch runs: initial successful run `31107800179`
on the implementation commit and necessary successful correction run
`31108924069`. PR #36 is open, ready, `MERGEABLE`, and `CLEAN` at the exact
correction head above and assigned base
`55c7a72337913303b6b1f6bd31edbca7ff28683b`; all eight final checks are
`SUCCESS`.

Final GraphQL thread-aware reread found no new issue comment, review, or thread.
The original P1 discussion remains unresolved and non-outdated because its loop
anchor persists at the shifted line. Current adjacent code freezes the exact
M21 source prefix and the accepted-release prefix, independently gates their
preservation, and the new test proves even a newly pinned replacement corpus
cannot satisfy admission. The requested condition is therefore present and no
finding remains actionable. No reply or manual thread resolution was performed.

The successful hosted checks do not establish real cross-version release
history, supported-release evidence, external feedback, stability promotion,
tag, GitHub release, or PyPI publication. The final documentation-only evidence
commit used `[skip ci]` and created no additional run; integration is recorded
below.

## M24 main integration - 2026-08-06

Ready PR #36 was squash-merged at `2026-08-06T14:08:37Z`. GitHub reports merged
commit `b7b16697d28410567cbddf8eb962c7e6c9e664b8` with sole parent
`55c7a72337913303b6b1f6bd31edbca7ff28683b`, exact tree
`fa3c455ccd9722c666cc07cae325f1b50e37ddc7`, a valid GitHub signature verified
at `2026-08-06T14:08:40Z`, and the DCO trailer. The tree exactly matches final
evidence head `1a8bd6f19f656eb5c4a0d6bd90f057a69bddbc34` on retained branch
`[historical branch name redacted]`; literal tree comparison and
`git diff --exit-code` reported no difference.

GitHub still lists exactly the initial successful run `31107800179` and the one
necessary successful correction run `31108924069` for the milestone branch;
both final evidence commits used `[skip ci]` and created no additional run.
Integration changes no runtime source, API/export, protocol, workflow,
dependency, lock, version, stability label, immutable M21 receipt byte, or M24
admission-manifest byte. No tag, GitHub release, PyPI publication, actual cross-
version history, supported release record, external feedback, certification, or
stability promotion is claimed.

After `git fetch --prune origin`, local `main` fast-forwarded to the verified
squash commit and matched `origin/main` with a clean worktree. Full repository
connectivity passed `git fsck --full --no-dangling`. Documentation-only branch
`[historical branch name redacted]` was created from that exact clean commit; it adds no
subsequent milestone work.

On the documentation-only integration branch, strict MkDocs built in 0.70
seconds, `git diff --check`, the non-state-surface comparison to `main`, and
`git fsck --full --no-dangling` exited 0. `git diff --name-only main` listed
exactly `[retired control directory]/CURRENT_TASK.md`, `[retired control directory]/PROJECT_STATE.md`, `[retired control directory]/TEST_EVIDENCE.md`,
`[retired control file]`, and `ROADMAP.md`. The focused credential-assignment scan returned
no match.

## M23 development evidence - 2026-08-06, Windows, CPython 3.12

| Command | Exit | Result |
| --- | ---: | --- |
| `git status --short --branch`, recent history, and `git rev-parse HEAD` | 0 | Baseline was clean synchronized `main` at `415859e19d9d29caa1168fabc96def509897b056`. |
| `uv lock --check` | 0 | Baseline lock remained current; 46 packages resolved in 0.87 ms. |
| Focused receipt/reader/transaction/stability/architecture baseline | 0 | 84 tests passed in 2.21 seconds. |
| First focused format/Ruff/Pyright/example group | 1 | Formatting changed one new file and Ruff/Pyright passed, but the example failed before reporting evidence because postponed annotations exposed component fields as strings. No example pass is claimed. |
| Second focused format/Ruff/Pyright/example group | 1 | Static checks passed, but the example correctly exposed that `world.transaction.nontransactional_operation` is wrapped as the `cause_code` of top-level `world.transaction.apply_failed`. No example pass is claimed. |
| Corrected focused format/Ruff/Pyright/example group | 0 | Both files were formatted, Ruff and Pyright were clean, and the exact sanitized M23 JSON report printed successfully. |
| Focused M23 integration and architecture gate | 0 | 17 repeatability, exact-policy, tamper, import-boundary, dependency, and synthetic forbidden-import tests passed in 1.83 seconds. |
| Expanded M23/readiness/release static and test group | 0 | 11 files were formatted; Ruff and strict Pyright were clean; 28 tests passed in 3.80 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.66 seconds with Material's upstream MkDocs 2.0 informational warning. |

The correction freezes only six current top-level transaction rejection codes.
The nontransactional-operation identity remains visible as a nested diagnostic
detail in existing runtime behavior, but M23 does not reinterpret that detail
as a top-level code or change runtime source. Full validation follows after
artifact wiring.

## M23 final local validation - 2026-08-06, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| Expanded repository-wide format/Ruff/Pyright, M20-M23/release/architecture group, and strict docs | 0 | 219 files were formatted, Ruff and Pyright were clean, 228 tests passed in 7.68 seconds, and docs built in 0.66 seconds. |
| `uv build` | 0 | Built pure `ludoweave-0.1.0a1-py3-none-any.whl` and source distribution. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated installed-wheel smoke passed, including exact M23 receipt-semantic evidence and readiness schema `/4`. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/release-candidate-m23-development` | 0 | Staged the complete deterministic 10-artifact release candidate with the M23 sample, SPDX SBOM, manifest, and checksums. |
| `uv run --frozen python scripts/smoke_release.py .tmp/release-candidate-m23-development` | 0 | Isolated release smoke passed for `0.1.0a1`, including bundled M23 evidence. |
| Direct installed unknown-operation diagnostic probe | 0 | The built-in transaction service returned top-level `world.transaction.validation_failed` with nested `cause_code` `world.unknown_operation`, confirming the frozen top-level classification. |
| Strengthened M23 architecture/integration group | 0 | 18 exact contract, direct-code-literal coverage, installed evidence, and boundary tests passed in 1.90 seconds. |
| `uv lock --check` | 0 | Lockfile remained current; 46 packages resolved in 0.68 ms. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Locked baseline plus graphics environment checked 45 packages in 2 ms. |
| `uv run --frozen ruff format --check .` | 0 | All 219 Python files were formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 1,048 tests passed in 77.67 seconds; one existing Windows symlink-capability test skipped. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | 10 unchanged real-wgpu integration tests passed in 6.52 seconds. |
| Hosted graphics vertical-slice commands | 0 | Thirty-tick wgpu Clockwork Arena and Agent World Builder completed with their expected deterministic structured summaries. |
| M1 benchmark plus validator | 0 | Seven workloads validated; fixed-tick target observed, simulation-tick target not observed. |
| M2 benchmark plus validator | 0 | Four informational workloads validated with no timing targets. |
| M3 benchmark plus validator | 0 | Six workloads validated; neither of two recorded targets was met. |
| M4 benchmark plus validator | 0 | Three workloads validated; baseline target observed. |
| M7 base and graphics profile runners plus validators | 0 | Two-workload base and three-workload graphics artifacts validated with five repeats. |

The M1 simulation and both M3 target misses are recorded without a performance
pass claim. They do not authorize native acceleration. The implementation
changes no file under `src/`, `.github/`, `pyproject.toml`, or `uv.lock`; the
release remains pure Python and the eight essential hosted jobs remain
unchanged.

Findings-first review inspected changed behavior, current transaction/receipt
call sites, status invariants, error wrapping, exact fixture/evidence matching,
security/privacy, compatibility, resource ownership, tests, release smoke,
architecture boundaries, and documentation state. It found no blocking or
non-blocking defect and no open question. The optional `[retired control directory]/tasks.json` and
`[retired control directory]/ledger.md` inputs named by the review role do not exist, so no shared-
workflow acceptance claim is made; the repository's `[retired control directory]` task, accepted RFCs,
and `[retired control file]` contract supplied the authoritative criteria. Final strict MkDocs
then exited 0 in 0.67 seconds, `git diff --check` exited 0, the new-file
credential-assignment scan matched nothing, and the scope check reported no
change under `src/`, `.github/`, `pyproject.toml`, or `uv.lock`.

## M23 initial hosted validation and delayed review - PR #34

Ready PR #34 targets exact base
`415859e19d9d29caa1168fabc96def509897b056` from DCO-signed implementation
commit `a6dc30ec62d91b1f6640db2c23797967f2aefefe`. GitHub Actions run
`31104052702`, triggered once by the pull request, completed successfully on
2026-08-06 across the unchanged eight-job topology:

| Hosted job | Result |
| --- | --- |
| Quality, tests, and distribution - Ubuntu, Python 3.12 | Passed lock, formatting, Ruff, strict Pyright, strict docs, baseline tests, base profile smoke, pure build, isolated wheel smoke, release staging, and isolated release smoke. |
| Compatibility - Ubuntu, Python 3.13 | Passed. |
| Compatibility - Ubuntu, Python 3.14 | Passed. |
| Compatibility - Windows, Python 3.14 | Passed. |
| Compatibility - macOS, Python 3.14 | Passed. |
| Graphics smoke - Ubuntu | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |
| Graphics smoke - Windows | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |
| Graphics smoke - macOS | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |

After the run, PR #34 was open, ready, `MERGEABLE`, and `CLEAN`; all eight
status checks were `SUCCESS`. The first thread-aware read returned no review
material. A later read after the `[skip ci]` evidence commit found an automated
review of the implementation head with two valid unresolved P1 findings:

1. the frozen diagnostic list identified codes but did not bind each code to a
   stable meaning and executable rejection scenario; and
2. the example checked semantic-diff field shapes but did not compare the full
   generated values and declared ordering across every change family.

No reply or manual thread resolution was performed. A correction and one
necessary follow-up run are required; the initial successful run is not claimed
as final review closure. No workflow or job topology changed. No cross-version,
external-adoption, stability-promotion, release, or publication claim is made.

## M23 review correction local validation - 2026-08-06, Windows, CPython 3.12.13

The correction adds a normative code/meaning/scenario record for all six
top-level diagnostics and an exact full complex-diff value oracle covering
created, destroyed, changed, component add/remove/change, resource, allocator,
epoch, and tick fields. The fixture is exactly 6,286 bytes with SHA-256
`f724a189e1ca23b6bc2637e1037d897bda4fa6dd3eda701ff5d538882a633619`.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen python examples/receipt_semantic_compatibility.py` | 0 | Emitted the sanitized report with six exact code/meaning/scenario cases and `complex_diff_exact: true`. |
| `uv run --frozen pytest -q tests/integration/test_receipt_semantic_compatibility.py tests/architecture/test_m23_receipt_semantic_boundary.py` | 0 | 20 exact-evidence, tamper, literal-fixture, and boundary tests passed in 2.35 seconds. |
| Focused Ruff and Pyright correction checks | 0 | Ruff passed and Pyright reported 0 errors, 0 warnings, and 0 information messages. |
| First repository-wide uv quality invocation | 1 | The managed sandbox denied access to uv's existing user cache before all five commands ran; no quality pass is claimed for this attempt. |
| `uv lock --check` | 0 | Lockfile remained current; 46 packages resolved in 0.81 ms. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Locked baseline plus graphics environment checked 45 packages in 2 ms. |
| `uv run --frozen ruff format --check .` | 0 | All 219 Python files were formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 1,050 tests passed in 76.89 seconds; one existing Windows symlink-capability test skipped. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built in 0.70 seconds with Material's upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built pure `ludoweave-0.1.0a1-py3-none-any.whl` and source distribution. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated installed-wheel smoke passed with corrected exact M23 evidence. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/release-candidate-m23-review-final` | 0 | Fresh absent target staged the complete deterministic 10-artifact release candidate. |
| `uv run --frozen python scripts/smoke_release.py .tmp/release-candidate-m23-review-final` | 0 | Isolated release smoke passed for `0.1.0a1` with corrected bundled evidence. |

The correction changes no file under `src/`, `.github/`, `pyproject.toml`, or
`uv.lock`. The earlier real-wgpu, graphics vertical-slice, and M1-M4/M7
benchmark/profile evidence remains applicable because no runtime, graphics,
benchmark, or profile file changed. After synchronizing the factual state
records, strict MkDocs rebuilt successfully in 0.66 seconds, `git diff --check`
exited 0, the added-line credential-assignment scan matched nothing, and the
scope diff remained empty for `src/`, `.github/`, `pyproject.toml`, and
`uv.lock`.

## M23 corrected hosted validation and thread-aware reread - PR #34

DCO-signed correction commit
`4eb61cd49542b0a4753629f31ebe80229c7d45b8` was pushed once. GitHub Actions
run `31105197045` completed successfully on 2026-08-06 across the unchanged
eight-job topology:

| Hosted job | Result |
| --- | --- |
| Quality, tests, and distribution - Ubuntu, Python 3.12 | Passed lock, formatting, Ruff, strict Pyright, strict docs, baseline tests, base profile smoke, pure build, isolated wheel smoke, release staging, and isolated release smoke. |
| Compatibility - Ubuntu, Python 3.13 | Passed. |
| Compatibility - Ubuntu, Python 3.14 | Passed. |
| Compatibility - Windows, Python 3.14 | Passed. |
| Compatibility - macOS, Python 3.14 | Passed. |
| Graphics smoke - Ubuntu | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |
| Graphics smoke - Windows | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |
| Graphics smoke - macOS | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |

After completion, PR #34 was open, ready, `MERGEABLE`, and `CLEAN`; all eight
status checks were `SUCCESS`, exact head was the correction commit, and exact
base remained `415859e19d9d29caa1168fabc96def509897b056`. The branch had exactly
two CI runs: initial successful run `31104052702` on the implementation commit
and corrected successful run `31105197045`.

The thread-aware GraphQL reread returned the same two review discussions. Both
remain marked unresolved and non-outdated because their original anchor lines
still exist: the code-list thread is anchored at fixture line 142 with the new
per-code definitions beginning at line 150, and the shallow-shape thread is
anchored at example line 315 with the new exact full-diff assertion at line 316.
The current code, fixture-literal guards, installed example, strict validator,
tamper tests, full local gate, wheel/release smokes, and hosted run directly
satisfy both requested changes. Neither review text describes a current defect.
No reply or manual resolution was performed, and no new review finding appeared.

## M23 main integration - 2026-08-06

PR #34 squash-integrated final evidence head
`eacb0153d8ac6e5f65d4d52f02c493bf9a891219` into `main` as commit
`2f7152565d369225dbf69055b7d42a4c80f46d1a`. Read-only verification found:

- the squash commit's sole parent is exact assigned base
  `415859e19d9d29caa1168fabc96def509897b056`;
- the final branch head and squash commit have exact tree
  `6ba709c29688041992bef75a2a83831275ff32db`;
- the commit contains the contributor DCO sign-off and GitHub reports
  verification `valid` with `verified: true`;
- local `main`, `origin/main`, and the PR merge commit all resolved to
  `2f7152565d369225dbf69055b7d42a4c80f46d1a` after a fast-forward; and
- the feature branch was retained for audit history.

Immediately before merge, PR #34 was open, ready, `MERGEABLE`, and `CLEAN`;
its base and head were the exact assigned and final evidence commits. The
branch listed exactly two completed successful Actions runs, `31104052702` and
`31105197045`; the final `[skip ci]` evidence commit created no third run. The
two review discussions retained unresolved/non-outdated GitHub metadata but
their current adjacent definitions and exact-diff assertion satisfied both
findings, as recorded above. No tag, release, publication, runtime source,
dependency, lock, version, workflow, or subsequent-milestone work is included.

On `[historical branch name redacted]`, `uv run --frozen mkdocs build --strict`
exited 0 and built documentation in 0.70 seconds with Material's upstream
informational warning. `git diff --check` and
`git fsck --full --no-dangling` exited 0 with no output. The diff contains
only `[retired control directory]` state, `[retired control file]`, and `ROADMAP.md`.

## M22 development evidence — 2026-08-06, Windows, CPython 3.12

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Baseline lock remained current; 46 packages resolved in 0.75 ms. |
| Inherited focused command/transaction/stability/API/release tests | 0 | 165 tests passed in 3.43 seconds. |
| `uv run --frozen pytest -q` | 0 | Inherited full suite passed 1,015 tests in 80.65 seconds with one existing Windows symlink-capability skip. |
| `uv run --frozen python examples/operation_argument_compatibility.py` | 0 | All seven valid built-in v1 operations committed; missing-required and unexpected-field cases rejected with `world.transaction.validation_failed`; one sanitized schema `/1` report printed. |
| `uv run --frozen pytest -q tests/integration/test_operation_argument_compatibility.py` | 0 | 7 installed evidence and tamper tests passed in 1.49 seconds. |
| M22 integration plus architecture tests | 0 | 15 tests passed in 1.63 seconds. |
| Focused M22/M20/release test group after artifact wiring | 0 | 34 tests passed in 3.50 seconds. |
| First repository-wide Ruff check | 1 | Three simplification findings in the new example/architecture test were reported and corrected; no lint pass is claimed for this attempt. |
| First repository-wide Pyright run | 0 | 0 errors, 0 warnings, 0 information messages. |
| First M22 strict MkDocs build | 0 | Documentation built successfully in 0.66 seconds with Material's upstream MkDocs 2.0 informational warning. |

The first sandboxed uv invocation after adding M22 evidence exited 1 before
pytest ran because the managed sandbox denied access to uv's user cache. The
same test commands were rerun with approved cache access and passed; no test
pass is claimed for the failed attempt. Final full-suite, docs, build, wheel,
release, graphics, benchmark/profile, and diff evidence follows. Hosted
hosted evidence is recorded below.

## M22 final local validation — 2026-08-06, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current; 46 packages resolved in 1 ms. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Locked baseline plus graphics environment checked 45 packages in 2 ms. |
| `uv run --frozen ruff format --check .` | 0 | All 215 Python files were formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed after the recorded first-pass corrections. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 1,030 tests passed in 71.59 seconds; one existing Windows symlink-capability test skipped. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.64 seconds with Material's upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built pure `ludoweave-0.1.0a1-py3-none-any.whl` and source distribution. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated installed-wheel smoke passed, including exact M22 operation-argument evidence. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/release-candidate-m22-final` | 0 | Staged the complete deterministic 10-artifact release candidate with sample bundle and SPDX SBOM. |
| `uv run --frozen python scripts/smoke_release.py .tmp/release-candidate-m22-final` | 0 | Isolated release smoke passed for `0.1.0a1`, including bundled M22 evidence. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | 10 real-wgpu integration tests passed in 5.79 seconds. |
| Hosted graphics vertical-slice commands | 0 | Thirty-tick wgpu Clockwork Arena and Agent World Builder completed with their expected structured summaries. |
| M1 benchmark plus validator | 0 | Seven workloads validated; fixed-tick target observed, simulation-tick target not observed. |
| M2 benchmark plus validator | 0 | Four informational workloads validated with no timing targets. |
| M3 benchmark plus validator | 0 | Six workloads validated; neither of two recorded targets was met. |
| M4 benchmark plus validator | 0 | Three workloads validated; baseline target observed. |
| M7 base and graphics profile runners plus validators | 0 | Two-workload base and three-workload graphics artifacts validated. |
| `git diff --check` | 0 | No whitespace errors. |
| First sandboxed `git add --all` | 128 | The filesystem sandbox denied creation of `.git/index.lock`; no path was staged. The operation was rerun with approved repository-metadata access. |

The M1 simulation and both M3 target misses are recorded without a performance
pass claim. They do not authorize native acceleration. Repository review found
no change under `src/`, `.github/`, `pyproject.toml`, or `uv.lock`; no credential
assignment matched; and the M22 evidence import scan found no ambient,
provider, filesystem, process, or network dependency.

## M22 hosted validation — PR #32

Ready PR #32 targets `main` from `[historical branch name redacted]` at
DCO-signed implementation commit
`f1a89ad460467039f966ed37955144840cd96a12`. GitHub Actions run
`31100821087`, triggered by that pull request, completed successfully on
2026-08-06. It validates the original implementation head; the review
correction below requires one follow-up run because it changes installed
evidence and artifact smoke.

| Hosted job | Result |
| --- | --- |
| Quality, tests, and distribution — Ubuntu, Python 3.12 | Passed lock, formatting, Ruff, strict Pyright, strict docs, baseline tests, base profile smoke, pure build, isolated wheel smoke, release staging, and isolated release smoke. |
| Compatibility — Ubuntu, Python 3.13 | Passed. |
| Compatibility — Ubuntu, Python 3.14 | Passed. |
| Compatibility — Windows, Python 3.14 | Passed. |
| Compatibility — macOS, Python 3.14 | Passed. |
| Graphics smoke — Ubuntu | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |
| Graphics smoke — Windows | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |
| Graphics smoke — macOS | Passed real-wgpu tests, graphics profile smoke, Clockwork Arena, and Agent World Builder. |

No additional CI job or workflow change was introduced. No cross-version,
external-adoption, stability-promotion, release, or publication claim is made.

### Automated review correction

The thread-aware PR review inspection found one unresolved P2 claiming that
dataclass defaults might fill omitted persistent component fields. Source
inspection confirmed `ComponentRegistry.migrate()` calls exact current-field
validation before construction, so omission is rejected even when the Python
field has a default. The contract and installed evidence now state and exercise
that behavior explicitly instead of weakening the rule.

The first focused post-review group exited 1 after 23 tests passed because the
intentional fixture edit changed its frozen byte size and digest. The checker
reported actual size 2,926 and SHA-256
`11ec4b9d9805dc509f18a52e8c0defd50136a475e216ae88fbe6bae68fb27001`;
those exact values are now recorded and the group is rerun below. The initial
failure is not reported as a pass.

| Corrected review gate | Exit | Result |
| --- | ---: | --- |
| Ruff format/check and strict Pyright | 0 | 215 files formatted; no Ruff or Pyright findings. |
| Corrected focused compatibility/architecture/stability/release group | 0 | 26 tests passed in 3.62 seconds. |
| `uv run --frozen pytest -q` | 0 | 1,030 tests passed in 71.15 seconds; the existing Windows symlink-capability test skipped. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.64 seconds with the upstream informational warning. |
| `uv build` and installed-wheel smoke | 0 | Pure wheel/sdist built and the installed evidence passed. |
| Fresh ten-artifact release staging and smoke | 0 | `.tmp/release-candidate-m22-review-final` staged and passed, including the corrected bundled evidence. |
| `git diff --check` | 0 | No whitespace errors. |

The correction changes no runtime source or contract. A necessary second
hosted run was quota-conscious evidence for the reviewed final artifact rather
than a new CI job.

## M22 final hosted validation and review closure — PR #32

DCO-signed correction commit
`cf3ae540e71cda128837ea698f5f175a7abf2fc4` triggered necessary follow-up
GitHub Actions run `31101607485`. All eight unchanged essential jobs passed:
complete Ubuntu quality/test/docs/build/wheel/release, Ubuntu 3.13/3.14,
Windows 3.14, macOS 3.14, and real graphics on Ubuntu/Windows/macOS.

The required thread-aware review reread returned no conversation comments and
one review thread with `isOutdated: true`, no current line anchor, and no other
actionable thread. Its original claim is covered by the exact frozen rule,
installed default-omission rejection, docs, focused regression, full suite,
artifact smoke, and final hosted run. No GitHub reply or manual resolution was
performed.

The branch has two CI runs total: the original complete implementation run
`31100821087` and the necessary review-correction run `31101607485`. Both
passed. No workflow or job topology changed.

## M22 main integration - 2026-08-06

PR #32 squash-integrated final evidence head
`a5a49dcca277f28bb3e6097f37d5418d5d3c2c9d` into `main` as commit
`8a4d288c4edf55d0299828b8edee1bd1885884d9`. Read-only verification found:

- the squash commit's sole parent is exact assigned base
  `291dfb3fd6895a2fdac7a2f0016bb181f0e5bca4`;
- the final branch head and squash commit have exact tree
  `f513bec716d1735cc47a6aab862bca0f5f770af9`;
- the commit contains the contributor DCO sign-off and GitHub reports
  verification `valid` with `verified: true`;
- local `main`, `origin/main`, and the PR merge commit all resolve to
  `8a4d288c4edf55d0299828b8edee1bd1885884d9` after a fast-forward; and
- `git fsck --full --no-dangling` exited 0 with no output.

Immediately before merge, PR #32 was open, ready, `MERGEABLE`, and `CLEAN`;
its base was the exact assigned commit. The branch listed exactly two completed
successful Actions runs, `31100821087` and `31101607485`. The feature branch
was retained for audit history. No tag, release, publication, runtime source,
dependency, lock, version, workflow, or M23 work is included.

On the integration-record branch, `uv run --frozen mkdocs build --strict`
exited 0 and built the documentation in 0.64 seconds with Material's upstream
informational warning. `git diff --check` exited 0 with no whitespace errors;
the diff contains only `[retired control directory]` state, `[retired control file]`, and `ROADMAP.md`.

## Baseline — 2026-08-04

| Command | Exit | Result |
| --- | ---: | --- |
| `git status --short --branch` | 0 | Clean `main` tracking `origin/main`; only the initial README and LICENSE were tracked. |
| `uv run --no-project python --version` | 0 | CPython 3.14.5 executed through uv; no project existed. |
| `uv run --no-project python -m pytest -q` | 1 | Baseline could not run because pytest was not installed. |
| `uv run --no-project python scripts/agent_workflow.py status` | 1 | Optional workflow helper was absent from the initial repository. |

## Development feedback retained

The first focused quality pass was not clean and was not reported as passing:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen ruff format --check .` | 1 | One file required formatting. |
| `uv run --frozen ruff check .` | 1 | Three lint findings were reported and corrected. |
| `uv run --frozen pyright` | 1 | Nineteen strict-type findings were reported and corrected. |
| `uv run --frozen pytest -q` | 1 | 38 tests passed; one setup error came from denied access to pytest's user temp directory. Test temporaries were moved to the workspace. |

The independent review later reproduced two relative-import forms that bypassed the architecture checker. Relative parent imports and sibling-alias imports are now resolved to absolute module names, regression fixtures cover both forms, and all affected checks were rerun.

## Final local validation — Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile is current; 39 packages resolved. |
| `uv sync --frozen --all-groups` | 0 | Locked environment checked successfully with 39 packages. |
| `uv run --frozen ruff format --check .` | 0 | 26 Python files already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 44 tests passed in 0.96 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully; Material printed its upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated wheel install passed console version, JSON doctor, and three-tick headless example checks. |
| `git diff --check` | 0 | No whitespace errors after LF normalization. |

## Executable acceptance evidence

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen ludoweave --version` | 0 | Printed `ludoweave 0.1.0.dev0`. |
| `uv run --frozen ludoweave doctor` | 0 | JSON schema `ludoweave.doctor/1`; Python, monotonic clock, and null renderer all reported `ok`. |
| `uv run --frozen python examples/hello_headless.py --ticks 120` | 0 | Printed JSON with 120 ticks, 120 frames, null renderer, closed final state, and 2,000,000,000 virtual nanoseconds. |
| GitHub YAML parse check | 0 | Parsed all four workflow/template YAML files. |
| Banned-import source scan | 1 | No `wgpu`, `glfw`, `numpy`, or `rust` imports matched; ripgrep uses exit 1 for no matches. |
| Credential-pattern scan | 1 | No key/password/secret/private-key assignment patterns matched; ripgrep uses exit 1 for no matches. |

## Review evidence

- Wheel contents contain only `ludoweave`, `py.typed`, distribution metadata, CLI entry point, LICENSE, and NOTICE.
- Package metadata reports Apache-2.0, Python `>=3.12,<3.15`, and no runtime `Requires-Dist` entries.
- CI actions use full commit SHAs, workflow permissions are `contents: read`, and checkout credential persistence is disabled.
- Independent review found relative parent/sibling import checker bypasses and stale state files as blockers. Both bypass forms have regression coverage; these state files now reflect executed evidence.
- No GitHub-hosted matrix job has run yet, so cross-platform CI is not claimed as passing.

## M1-01 final local validation — 2026-08-05, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current with 39 packages resolved. |
| `uv sync --frozen --all-groups` | 0 | Existing locked environment checked successfully with 39 packages. |
| `uv run --frozen pytest -q tests/unit/test_entity_allocator.py tests/architecture/test_import_boundaries.py` | 0 | 21 focused allocator and architecture tests passed. |
| `uv run --frozen ruff format --check .` | 0 | 30 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 61 tests passed in 1.64 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully; Material printed its documented upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated wheel checks passed version, doctor, entity generation/staleness, and the headless example. |
| `git diff --check` | 0 | No whitespace errors. |

Independent review found that plain prefix matching allowed `ludoweave.ecs_tools` through the ECS dependency rule. All package-boundary checks now require exact module names or dot-delimited children, a synthetic near-prefix regression is present, and the reviewer independently reran the 21 focused tests with no remaining blocker.

## M1-02 final local validation — 2026-08-05, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current with 39 packages resolved. |
| `uv sync --frozen --all-groups` | 0 | Existing locked environment checked successfully with 39 packages. |
| `uv run --frozen pytest -q tests/unit/test_component_schema.py tests/property/test_component_migrations.py tests/architecture/test_import_boundaries.py` | 0 | 48 focused component, migration, property, and architecture tests passed. |
| `uv run --frozen ruff format --check .` | 0 | 33 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 103 tests passed in 1.75 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully; Material printed its documented upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated wheel checks passed version, doctor, entity generations, explicit component registration, forward migration, and the headless example. |
| `git diff --check` | 0 | No whitespace errors. |
| Banned-import source scan | 1 | No `wgpu`, `glfw`, `numpy`, or `rust` import matched; ripgrep uses exit 1 for no matches. |
| Credential-pattern scan | 1 | No credential-assignment pattern matched; ripgrep uses exit 1 for no matches. |
| Global-registry source scan | 1 | No `ComponentRegistry` instance exists in package source; ripgrep uses exit 1 for no matches. |

Independent architecture and quality design reviews recommended explicit UUID identity, no global registration, immutable registries, a narrow canonical scalar domain, and complete adjacent migrations; ADR-0003 records the decision. Independent code review found no runtime/API defect. Its state-drift blockers were the stale derived-ID wording and missing completion evidence; both are corrected here.

## M1-03 final local validation — 2026-08-05, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current with 39 packages resolved. |
| `uv sync --frozen --all-groups` | 0 | Frozen environment checked successfully with 39 packages. |
| `uv run --frozen ruff format --check .` | 0 | 39 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q tests\unit\test_world_storage.py tests\conformance\test_world_conformance.py tests\property\test_world_model.py tests\architecture\test_import_boundaries.py` | 0 | 47 focused storage, conformance, state-machine property, and architecture tests passed in 1.13 seconds. |
| `uv run --frozen pytest -q` | 0 | 144 tests passed in 2.53 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully; Material printed its documented upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts\smoke_wheel.py dist` | 0 | Isolated wheel passed version, doctor, allocator, schema migration, copy-safe world add/patch/get/remove, destroy/reuse, stale-handle, and headless example checks. |
| `git diff --check` | 0 | No whitespace errors. |
| Banned-import source scan | 1 | No `wgpu`, `glfw`, `numpy`, or `rust` import matched source, tests, or scripts; ripgrep uses exit 1 for no matches. |
| Credential-pattern scan | 1 | No credential-assignment pattern matched outside excluded generated/dependency paths; ripgrep uses exit 1 for no matches. |
| ECS wall-clock/random scan | 1 | No wall-clock or random source matched `src/ludoweave/ecs`; ripgrep uses exit 1 for no matches. |
| Dynamic-evaluation scan | 1 | No `eval()` or `exec()` call matched package source; ripgrep uses exit 1 for no matches. |
| ECS backend-leakage scan | 1 | No render, wgpu, GLFW, or NumPy reference matched ECS source; ripgrep uses exit 1 for no matches. |
| `uv run --frozen python -m zipfile -l dist\ludoweave-0.1.0.dev0-py3-none-any.whl` | 0 | Wheel contains the typed `ludoweave` package including ECS modules, distribution metadata, CLI entry point, LICENSE, and NOTICE. |

Independent architecture and quality reviews established the copy boundary, epoch contract, swap-removal checks, and independent dictionary oracle before implementation. Findings-first code review then reproduced raw missing-slot errors, a side-effecting getter time-of-check/time-of-use alias defect, an omitted protocol clone declaration, incomplete clone coverage, and a bypassable reference-import guard. All were corrected with regressions. The reviewer reran 47 focused tests with clean Ruff and strict Pyright and accepted M1-03 with no implementation blocker.

GitHub-hosted Windows/macOS/Linux and Python 3.13/3.14 jobs have not run for these changes. No cross-platform pass claim is made.

## M1-06 and complete-M1 final local validation — 2026-08-05, Windows, CPython 3.12.13 GIL build

The first sandboxed `uv lock --check` invocation exited 1 because the managed sandbox denied access to uv's user cache. The same command was rerun with approved cache access and exited successfully; this was an environment permission failure, not a lockfile failure.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current; 39 packages resolved in 0.72 milliseconds. |
| `uv sync --frozen --all-groups` | 0 | Frozen environment checked successfully with 39 packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | 60 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 303 tests passed in 2.78 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.31 seconds; Material printed its documented upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated wheel smoke passed version, doctor, M1 ECS/resource/schedule operations, the M0 headless example, and the fixed-step world example. |
| `uv run --frozen python benchmarks/benchmark_m1.py --samples 30 --seed 1 --json-out .tmp/m1-benchmark.json` | 0 | Recorded 30 raw samples for all seven versioned M1 workloads with sanitized Windows/AMD64/CPython 3.12.13 release-GIL metadata and a dirty-worktree commit reference. |
| `uv run --frozen python benchmarks/validate_m1_results.py .tmp/m1-benchmark.json` | 0 | Exact artifact schema, parameters, distributions, metadata, and both target records validated; one of two local engineering targets was observed. |
| `git diff --check` | 0 | No whitespace errors. |
| Banned native/backend import scan | 1 | No `wgpu`, `glfw`, `numpy`, or `rust` import matched source, tests, examples, scripts, or benchmarks; ripgrep uses exit 1 for no matches. |
| Credential-assignment scan | 1 | No API key, access token, client secret, password, or private-key assignment pattern matched outside excluded generated/dependency/artifact paths; ripgrep uses exit 1 for no matches. |
| ECS wall-clock/random scan | 1 | No wall-clock, performance timer, or global random use matched `src/ludoweave/ecs`; ripgrep uses exit 1 for no matches. |
| Dynamic-evaluation scan | 1 | No `eval()` or `exec()` call matched package source; ripgrep uses exit 1 for no matches. |
| Application/core concrete-backend scan | 1 | No concrete render backend, wgpu, GLFW, or NumPy reference matched application, ECS, or core source; ripgrep uses exit 1 for no matches. |
| `uv run --frozen python -m zipfile -l dist\ludoweave-0.1.0.dev0-py3-none-any.whl` | 0 | Wheel contains only the typed `ludoweave` package, distribution/entry-point metadata, LICENSE, and NOTICE; benchmarks, tests, docs, credentials, and native artifacts are absent. |

### Final M1 benchmark observations

All durations are nearest-rank distributions from the final 30 retained samples; setup is excluded as documented for operation-specific workloads.

| Workload | p50 | p95 | p99 | Local target observation |
| --- | ---: | ---: | ---: | --- |
| Entity create/destroy/reuse, 10,000 entities | 28.3294 ms | 36.3653 ms | 37.1018 ms | No target assigned. |
| Read query, 10,000 entities/two components | 96.8505 ms | 129.7374 ms | 132.6638 ms | No target assigned. |
| Writable query, 10,000 entities/two components | 148.5815 ms | 194.5107 ms | 202.5685 ms | No target assigned. |
| Scheduler plan, seeded 100-system DAG | 4.1550 ms | 4.6828 ms | 4.8285 ms | No target assigned. |
| Staged flush, 1,000 two-component spawn commands | 41.0282 ms | 56.0997 ms | 60.7698 ms | No target assigned. |
| Fixed-step headless run, 3,600 ticks | 22.7571 ms | 26.8523 ms | 29.0085 ms | Observed p95 ≤ 12 seconds (at least 5× simulated real time). |
| Representative application tick, 10,000 entities | 166.5203 ms | 196.8800 ms | 217.7976 ms | **Not observed:** p95 < 4 ms. |

The benchmark miss is recorded without a performance pass claim. It authorizes profiling and pure-Python algorithm work only; no Rust, PyO3, Cython, NumPy storage, or native build requirement was added.

### Independent review closure

Findings-first review reproduced and drove regressions for forged schedule execution, incomplete flush diagnostics, noncanonical resource failure ordering, hostile input objects/mappings, BaseException query-lease leakage, unmodeled entity-set reads/writes, writable engine-owned input, exact bool/float and signed-zero equality, protocol/runtime surface mismatch, and underspecified benchmark validation/metadata. Canonical plan revalidation, exact input signatures, BaseException-safe cleanup, restricted M1 structural operations, exact public protocols, hostile-source wrapping, exact benchmark schemas, tamper tests, and GIL/free-threaded metadata resolve those findings. The reviewer independently reran 130 focused tests, the 303-test full suite, Ruff format/lint, strict Pyright, a minimal benchmark, and the official 30-sample artifact validator, then accepted M1-06 with no remaining blocking or non-blocking code finding.

### Hosted CI — PR #1

The first PR run (`30936335552`) failed before checkout on every job because the planned `actions/checkout` v6.0.2 SHA `de0fac2e4500dabe0009e8f65f754d05d2b0f7a6` does not exist upstream. The official tag API resolved v6.0.2 to `de0fac2e4500dabe0009e67214ff5f5447ce83dd`; `astral-sh/setup-uv` v8.1.0 independently resolved to the already configured `08807647e7069bb48b6ef5acd8ec9567f424441b`. The three checkout references were corrected without changing workflow privileges or credential persistence.

GitHub Actions run `30936533105` then completed successfully:

| Hosted job | Result |
| --- | --- |
| Quality and documentation — Ubuntu, Python 3.12 | Passed formatting, lint, strict Pyright, lock verification, and strict MkDocs build. |
| Tests — Ubuntu, Python 3.12/3.13/3.14 | All three matrix jobs passed. |
| Tests — Windows, Python 3.12/3.14 | Both matrix jobs passed. |
| Tests — macOS, Python 3.12/3.14 | Both matrix jobs passed. |
| Installed wheel — Ubuntu/Windows/macOS, Python 3.12 | All three build and isolated-wheel smoke jobs passed. |

Some successful jobs emitted non-fatal setup-uv cache-reservation annotations because another matrix job created the same cache first. No test, build, documentation, or wheel-smoke step failed in the corrected run.

## M1-05 final local validation — 2026-08-05, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current; 39 packages resolved in 0.80 milliseconds. |
| `uv sync --frozen --all-groups` | 0 | Frozen environment checked successfully with 39 packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | 49 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q tests/unit/test_resources.py tests/unit/test_schedule.py tests/property/test_schedule_graph.py tests/architecture/test_import_boundaries.py` | 0 | 47 focused resource, scheduler, generated graph property, and architecture tests passed in 0.45 seconds. |
| `uv run --frozen pytest -q` | 0 | 219 tests passed in 2.26 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.28 seconds; Material printed its documented upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated wheel passed version, doctor, allocator/schema/world/query/command checks, copy-owned typed resource isolation, deterministic scheduled ordering, and the headless example. |
| `git diff --check` | 0 | No whitespace errors. |
| Banned-import source scan | 1 | No `wgpu`, `glfw`, `numpy`, or `rust` import matched source, tests, or scripts; ripgrep uses exit 1 for no matches. |
| Credential-pattern scan | 1 | No credential-assignment pattern matched outside excluded generated/dependency paths; ripgrep uses exit 1 for no matches. |
| ECS wall-clock/random scan | 1 | No wall-clock or random source matched `src/ludoweave/ecs`; ripgrep uses exit 1 for no matches. |
| Dynamic-evaluation scan | 1 | No `eval()` or `exec()` call matched package source; ripgrep uses exit 1 for no matches. |
| ECS backend-leakage scan | 1 | No render, wgpu, GLFW, or NumPy import matched ECS source; ripgrep uses exit 1 for no matches. |

Independent architecture and quality reviews established the explicit resource identity/copy boundary, fixed phases, same-phase conflict ambiguity rule, serial-only planner, and deterministic graph diagnostics before implementation. Findings-first code review reproduced a canonical-state mutation risk from misbehaving resource adapters, D0 component eligibility bypass, raw signature-inspection exception, class-member declaration ambiguity, stale public/state documentation, and missing after-only/write-write regressions. The accepted contract now explicitly trusts adapters that treat input as read-only, deterministic plans reject D0 components, signature failures are structured and chained, only strict module-level functions are accepted, and focused regressions cover the ordering relationships. The reviewer independently reran focused tests, Ruff, and strict Pyright and accepted M1-05 with no remaining runtime, API, architecture, test, or scope blocker.

GitHub-hosted Windows/macOS/Linux and Python 3.13/3.14 jobs have not run for these changes. No cross-platform pass claim is made.

## M1-04 final local validation — 2026-08-05, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current with 39 packages resolved. |
| `uv sync --frozen --all-groups` | 0 | Frozen environment checked successfully with 39 packages. |
| `uv run --frozen ruff format --check .` | 0 | 44 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q tests/unit/test_query.py tests/unit/test_commands.py tests/conformance/test_query_commands_conformance.py tests/property/test_world_model.py tests/architecture/test_import_boundaries.py` | 0 | 52 focused query, command, conformance, state-machine property, and architecture tests passed in 1.12 seconds. |
| `uv run --frozen pytest -q` | 0 | 185 tests passed in 2.16 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully; Material printed its documented upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated wheel passed version, doctor, allocator/schema/world checks, stable include/exclude/changed query, writable query close, buffered-operation invisibility, atomic flush, deferred-token resolution, and the headless example. |
| `git diff --check` | 0 | No whitespace errors. |
| Banned-import source scan | 1 | No `wgpu`, `glfw`, `numpy`, or `rust` import matched source, tests, or scripts; ripgrep uses exit 1 for no matches. |
| Credential-pattern scan | 1 | No credential-assignment pattern matched outside excluded generated/dependency paths; ripgrep uses exit 1 for no matches. |
| ECS wall-clock/random scan | 1 | No wall-clock or random source matched `src/ludoweave/ecs`; ripgrep uses exit 1 for no matches. |
| Dynamic-evaluation scan | 1 | No `eval()` or `exec()` call matched package source; ripgrep uses exit 1 for no matches. |
| ECS backend-leakage scan | 1 | No render, wgpu, GLFW, or NumPy import matched ECS source; ripgrep uses exit 1 for no matches. |
| `uv run --frozen python -m zipfile -l dist\ludoweave-0.1.0.dev0-py3-none-any.whl` | 0 | Wheel contains the typed package including query/command modules, distribution metadata, CLI entry point, LICENSE, and NOTICE; no generated docs, tests, backend-native objects, or credentials are packaged. |

Independent architecture and quality reviews established cursor ownership, row-atomic writeback, mutation-guard precedence, buffer rollback, exact token identity, reference independence, and the M2 boundary before implementation. Findings-first code review then reproduced a value-equal deferred-token forgery and signed-zero change-detection loss, and identified five-plus query typing, frozen-write documentation, plan-driver coverage, and failed-queue wording gaps. Identity-only tokens, float-hex signatures, variadic fallback typing, focused regressions, and corrected documentation resolve every finding. The reviewer independently reran all gates and reported no remaining runtime, API, or architecture blocker.

GitHub-hosted Windows/macOS/Linux and Python 3.13/3.14 jobs have not run for these changes. No cross-platform pass claim is made.
## M2-01 full local validation — 2026-08-05, Windows, CPython 3.12

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen ruff format --check .` | 0 | 66 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 334 tests passed in 3.16 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.30 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `git diff --check` | 0 | No whitespace errors. |

The new focused canonical-command/architecture suite reported 45 passing tests
in 0.50 seconds before the full gate. This evidence establishes M2-01 only; no
atomic apply, receipt, snapshot, replay, or CLI pass claim is made yet.

## M2-02 full local validation — 2026-08-05, Windows, CPython 3.12

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen ruff format --check .` | 0 | 73 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 351 tests passed in 3.44 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.31 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `git diff --check` | 0 | No whitespace errors. |

Focused M2-02 transaction and generated reference-model tests passed before the
full gate. They cover stale-hash rejection, invalid-middle rollback, dry-run,
resource and tick staging, BaseException escape, allocator churn, limits,
thread ownership, and production/reference authority hashes. This is not yet a
receipt, snapshot, replay, CLI, package-build, or hosted-platform pass claim.

## M2-03 full local validation — 2026-08-05, Windows, CPython 3.12

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen ruff format --check .` | 0 | 76 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 357 tests passed in 3.36 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.31 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `git diff --check` | 0 | No whitespace errors. |

Focused receipt/diff tests passed before the full gate. They cover exact net
created/destroyed/changed entities, component field and row-epoch changes,
spawn-then-destroy audit behavior, dry-run/commit equivalence, canonical
rejected receipts, resource/tick changes, and pre-adoption receipt/diff limits.
This is not yet snapshot, replay, CLI, package-build, or hosted-platform
evidence.

## M2-04 full local validation — 2026-08-05, Windows, CPython 3.12

The first sandboxed combined gate could not initialize uv's user cache and did
not execute the uv-managed checks. The rerun used approved cache access. Its
first full pytest execution found a missing reference-model error whitelist
entry; that architecture-test defect was corrected, and the complete gate was
rerun from the beginning.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current; 39 packages resolved in 0.70 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | 80 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 373 tests passed in 3.64 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.33 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `git diff --check` | 0 | No whitespace errors. |

Focused random/snapshot tests reported 16 passes before the final full gate.
Coverage includes independent repeatable named streams, exact random
checkpoint continuation, allocator churn and future allocation, change epochs,
byte-identical round trips, resource/component migrations, malformed and
hash-mismatched payloads, semantic limits, invalid resource/random state, and
active-query atomic-load rejection. This is not yet replay, branch, CLI,
package-build, wheel-smoke, or hosted-platform evidence.

## M2-05 local validation — 2026-08-05, Windows, CPython 3.12.13

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen ruff format --check .` | 0 | 82 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 381 tests passed in 3.74 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.33 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `git diff --check` | 0 | No whitespace errors. |

This evidence covers self-contained replay, checkpoints, hash divergence,
immutable parent-bound branches, and repeated replay. Later independent review
required additional one-tick branch-boundary and composition corrections, so
the final M2 evidence supersedes this slice result.

## M2 final review-candidate source gate — 2026-08-05, Windows, CPython 3.12.13

Review-driven fixes added exact command equality and operation dispatch,
exhaustive resource roles, detached session views, project-bound snapshots,
excluded-resource preservation, strict checkpoint/schema invariants, one-tick
replay boundaries, bounded handle reads, and stronger architecture guards.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen ruff format --check .` | 0 | 88 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 430 tests passed, 1 skipped in 8.46 seconds. The skip is the Windows symlink-capability test for an account that cannot create file symlinks. |

This is source-gate evidence for the review candidate, not the final M2
artifact/benchmark/hosted-platform claim. Documentation, build, wheel smoke,
benchmark validation, scans, independent resnapshot, and hosted CI remain to be
recorded after they execute on the final cut.

## M2 final local validation — 2026-08-05, Windows, CPython 3.12.13

The first full pytest attempt on the final review cut reported six failures
because an established component-version error-message regex no longer matched.
The signed-64 validation behavior was correct; stable wording was restored and
the complete gate below was rerun. No pass is claimed for that failed attempt.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile remained current; 39 packages resolved in 0.74 milliseconds. |
| `uv sync --frozen --all-groups` | 0 | Frozen environment checked 39 packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | 88 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 444 tests passed and one Windows symlink-capability test skipped in 8.15 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built in 0.36 seconds; Material printed its documented upstream MkDocs 2.0 warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated installed-wheel version, doctor, headless, command, receipt, snapshot, replay, branch, and diff workflow smoke passed. |
| `uv run --frozen python benchmarks/benchmark_m2.py --samples 30 --seed 1 --json-out .tmp/m2-benchmark.json` | 0 | Recorded 30 retained samples after three warmups for all four versioned informational workloads. |
| `uv run --frozen python benchmarks/validate_m2_results.py .tmp/m2-benchmark.json` | 0 | Validated four informational M2 workloads with no timing targets. |
| `git diff --check` | 0 | No whitespace errors. |
| `git diff --cached --check` | 0 | The complete staged 61-file milestone diff has no whitespace errors. |
| Credential-pattern scan | 1 | No private-key, AWS key, GitHub token, or Slack token pattern matched project files; ripgrep uses exit 1 for no matches. |
| Backend/native import scan | 1 | No wgpu, GLFW, NumPy, Rust, Box2D, or MCP import matched source, tests, examples, benchmarks, or scripts; ripgrep uses exit 1 for no matches. |
| Wheel content listing | 0 | Pure-Python wheel contains only the typed `ludoweave` package, distribution metadata, entry point, LICENSE, and NOTICE; no tests, generated docs, native objects, or credentials are packaged. |

The final 30-sample local duration p50/p95 values were 30.2751/33.7076 ms
for canonical 100-command round trips, 13.9896/16.9751 ms for atomic
100-command apply, 17.1209/18.0412 ms for 1,000-entity snapshot round trips,
and 216.5521/271.2240 ms for verified 100-batch replay. These are local
profiling observations, not timing targets or cross-platform performance claims.

Independent final code/security review reran Ruff, Pyright, the complete test
suite, strict documentation, a minimal benchmark/validator, and diff checks. It
reported no remaining P0, P1, or P2 actionable finding. Trusted author codecs,
migrations, and tick executors plus a trusted/quiescent local project tree remain
documented boundaries. Hosted M2 CI has not yet run, so no new hosted-platform
claim is made.

## M2 hosted validation — GitHub Actions run 30947073913

The DCO-signed M2 commit `6bf3f99e94e30e4204af221064331e4b01c487dc`
was pushed to `[historical branch name redacted]` and published as stacked
pull request #2 against the open M1 branch. The resulting least-privilege CI
run completed successfully:

| Hosted job | Result |
| --- | --- |
| Quality and documentation — Ubuntu, Python 3.12 | Passed lock, formatting, lint, strict Pyright, and strict MkDocs gates. |
| Tests — Ubuntu, Python 3.12/3.13/3.14 | All three matrix jobs passed. |
| Tests — Windows, Python 3.12/3.14 | Both matrix jobs passed. |
| Tests — macOS, Python 3.12/3.14 | Both matrix jobs passed. |
| Installed wheel — Ubuntu/Windows/macOS, Python 3.12 | All three build and isolated installed-wheel workflow smoke jobs passed. |

All 11 jobs in run `30947073913` passed. This supplies the cross-platform M2
evidence that was deliberately not claimed by the local gate.

## M3 local validation — 2026-08-05, Windows, CPython 3.12.13

Development-focused renderer checks reached 51 passes, then the graphics-enabled
full suite reached 484 passes and one existing Windows symlink-capability skip.
The final cut added the rotated-camera regression and produced the complete gate
below. An earlier real offscreen clear exposed wgpu-py 0.32's Windows queue
callback ABI mismatch; the exact adapter now contains and documents the native
device-poll workaround. The failing attempt raised typed
`render.device_lost`; no pass was claimed for it.

The first graphics-free `uv sync` attempt could not open uv's managed user cache
inside the filesystem sandbox and did not execute tests. The approved rerun
completed and removed `cffi`, `glfw`, `numpy`, `pycparser`, `rendercanvas`, and
`wgpu`, proving the optional dependency boundary:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv sync --frozen --all-groups` | 0 | Removed six graphics/provider packages from the base environment. |
| `uv run --frozen pytest -q` | 0 | 479 tests passed and two tests skipped: the Windows symlink capability and graphics-extra module capability. |

The real window composition was also executed outside the sandbox:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen --extra graphics python examples/hello_sprite.py --width 16 --height 8 --window` | 0 | Created the rendercanvas/GLFW surface, submitted one draw with two sprite instances, completed the fence, emitted the versioned JSON summary, and closed. |

The final local gate used the locked graphics extra:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile resolved 46 packages in 0.70 milliseconds. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Frozen environment checked 45 packages in 2 milliseconds. |
| `uv run --frozen --extra graphics ruff format --check .` | 0 | 105 Python files were already formatted. |
| `uv run --frozen --extra graphics ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen --extra graphics pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen --extra graphics pytest -q` | 0 | 485 tests passed and one Windows symlink-capability test skipped in 13.72 seconds. This includes five real offscreen wgpu/example tests. |
| `uv run --frozen --extra graphics mkdocs build --strict` | 0 | Documentation built in 0.36 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and pure `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen --extra graphics python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency wheel smoke passed version, doctor, M0-M2 workflows, package/render imports, and structured missing-graphics diagnostics. |
| `uv run --frozen --extra graphics python benchmarks/benchmark_m3.py --samples 30 --output .tmp/m3-benchmark-final.json` | 0 | Recorded 30 retained samples after three warmups for all six M3 workloads. |
| `uv run --frozen --extra graphics python benchmarks/validate_m3_results.py .tmp/m3-benchmark-final.json` | 0 | Validated all workload schemas, distributions, exact dependency versions, sanitized metadata, one-draw invariants, and two target observations; zero targets were met. |
| `git diff --check` | 0 | No whitespace errors in the tracked diff. |

The final Windows/CPython 3.12.13 local duration observations were:

| Workload | p50 | p95 | p99 | Draws | 3 ms target |
| --- | ---: | ---: | ---: | ---: | --- |
| Extraction/packing, 1,000 sprites | 3.2777 ms | 3.6115 ms | 4.1763 ms | 1 | Not assigned |
| Extraction/packing, 10,000 sprites | 35.4460 ms | 41.9722 ms | 51.8362 ms | 1 | Not observed |
| Null submission, 1,000 sprites | 0.0081 ms | 0.0124 ms | 0.0465 ms | 1 | Not assigned |
| Null submission, 10,000 sprites | 0.0077 ms | 0.0084 ms | 0.0085 ms | 1 | Not assigned |
| wgpu CPU submission, 1,000 sprites | 0.5095 ms | 0.8001 ms | 0.8055 ms | 1 | Not assigned |
| wgpu CPU submission, 10,000 sprites | 5.3753 ms | 6.5363 ms | 6.9215 ms | 1 | Not observed |

The misses are recorded performance risks, not compatibility failures, target
passes, cross-platform claims, or authorization for native acceleration.

A separate final audit found no credential/private-key pattern. The backend
import scan found only the three expected wgpu/rendercanvas imports inside
`ludoweave.render.backends.wgpu`; no NumPy, MCP, Box2D, Rust/PyO3, or arbitrary
evaluation import/call entered source/examples/benchmarks/scripts. The wheel
listing contains only the typed package, metadata, entry point, LICENSE, and
NOTICE; it contains no native objects, tests, generated docs, or credentials.
## M3 hosted validation — GitHub Actions runs 30951328011 and 30993554807

The DCO-signed M3 implementation commit
`230687b16dfc02a8d2762af66f6bf2db4ef87f21` was pushed to
`[historical branch name redacted]` and published as stacked PR #3 against the
M2 branch. Initial run `30951328011` was not green and is not reported as a
pass: all base test and wheel jobs plus Windows/macOS graphics passed, while
strict Pyright failed because the quality job had not installed optional
provider packages and Ubuntu graphics failed with the typed
`render.adapter_unavailable` outcome because the runner had no usable graphics
driver.

Correction commit `6e6cea0bd80450a4d5b59cc1ff2e9f27a4195a92`
installs the already locked `graphics` extra in the quality job and installs
`libvulkan1` plus `mesa-vulkan-drivers` only on the Ubuntu graphics runner.
Local strict Pyright remained green before publication. Corrected run
`30993554807` then completed successfully:

| Hosted job | Result |
| --- | --- |
| Quality and documentation — Ubuntu, Python 3.12 | Passed lock, formatting, lint, strict Pyright with the optional adapter installed, and strict MkDocs. |
| Tests — Ubuntu, Python 3.12/3.13/3.14 | All three base jobs passed without the graphics extra. |
| Tests — Windows, Python 3.12/3.14 | Both base jobs passed. |
| Tests — macOS, Python 3.12/3.14 | Both base jobs passed. |
| Installed wheel — Ubuntu/Windows/macOS, Python 3.12 | All three pure-wheel/no-dependency workflow smokes passed. |
| Graphics smoke — Ubuntu/Windows/macOS, Python 3.12 | All three real clear, instanced sprite, capture, resize/minimize, and loss fixtures passed; Ubuntu used the explicitly provisioned Mesa Vulkan software runtime. |

All 14 jobs in run `30993554807` passed. This supplies the cross-platform M3
evidence that was deliberately not claimed by the local gate.

## M4 final local validation — 2026-08-05, Windows, CPython 3.12.13

Focused input, asset, audio, collision, and architecture tests passed 73 tests.
The Clockwork Arena integration suite passed four tests in 28.70 seconds,
including the exact 3,600-tick fixture, an independently recorded 3,600-tick
input replay with the same state hash, replay checkpoints, and presentation
nonmutation.

The real renderer compositions were executed with the locked graphics extra:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 30 --renderer wgpu --render-every 10` | 0 | Offscreen wgpu submitted three draws containing 16 total sprite instances. The capture SHA-256 was `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`; the exact final state hash was `sha256:c8cd6e3d7706e22003e11ccaf8e63b72627c364d42e6e1889c377d562cd3c859`. |
| `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 10 --renderer wgpu --window --interactive` | 0 | The GLFW window path processed platform input, submitted 10 draws containing 40 total sprite instances, and closed with state hash `sha256:8dec596fd7492b86e30a4c00409ce447c515548b79005a544ef8a2af8bd39fa6`. |

The complete local quality and package gate then passed:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile resolved 46 packages in 0.72 milliseconds. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Frozen environment checked 45 packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | 125 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 516 tests passed and one existing Windows symlink-capability test skipped in 45.39 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.44 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and pure `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency installed-wheel smoke passed version, doctor, existing workflows, and M4 Arena/audio/collision checks outside the source tree. |
| `uv run --frozen python benchmarks/benchmark_m4.py --samples 300 --warmups 60 --output .tmp/m4-benchmark.json` | 0 | Recorded 300 retained samples after 60 warmups at stress levels 1, 4, and 8 with fixed seed, raw durations, final metrics, and state hashes. |
| `uv run --frozen python benchmarks/validate_m4_results.py .tmp/m4-benchmark.json` | 0 | Validated artifact schema, sample distributions, metadata, workload integrity, and all three final summaries; the baseline target observation was true. |
| `git diff --check` | 0 | No whitespace errors in the complete tracked diff. |

The final M4 benchmark retained 300 samples after 60 warmups for each workload.
Its artifact validator returned
`{"baseline_target_observed":true,"schema":"ludoweave.benchmark.m4/1","valid":true,"workloads":3}`.

| Workload | p50 | p95 | p99 | Target |
| --- | ---: | ---: | ---: | --- |
| Clockwork Arena, stress 1 | 1.5228 ms | 2.1228 ms | 2.5898 ms | p95 < 16.666667 ms observed |
| Clockwork Arena, stress 4 | 2.1822 ms | 3.5029 ms | 4.3358 ms | Not assigned |
| Clockwork Arena, stress 8 | 2.6362 ms | 4.8371 ms | 5.7986 ms | Not assigned |

The exact 3,600-tick fixture records 35 enemies spawned, three destroyed, 300
score, 360 shots, 12 waves, 12 remaining player health, and state hash
`sha256:4243defe548ba6e36b6bec93b45f266d2ad48e74c24efc2856d3f7c6197a3b6e`.
Architecture, credential, dynamic-evaluation, native/backend, Box2D, MCP,
network, and editor scans found no unapproved dependency or capability. Wheel
inspection found the new assets, audio, collision, platform, and sample modules
as pure Python, with no provider objects, tests, docs, or native artifacts.
M4 hosted CI has not yet run, so no cross-platform M4 pass is claimed here.

## M4 hosted validation — GitHub Actions run 30996905660

The DCO-signed M4 implementation commit
`e46bceec62fb20886fbb705149b07d083f4a46de` was pushed to
`[historical branch name redacted]` and published as stacked pull request #4 against the
validated M3 branch. The resulting least-privilege CI run completed
successfully:

| Hosted job | Result |
| --- | --- |
| Quality and documentation — Ubuntu, Python 3.12 | Passed lock, formatting, lint, strict Pyright with the optional graphics adapter installed, and strict MkDocs gates. |
| Tests — Ubuntu, Python 3.12/3.13/3.14 | All three base matrix jobs passed. |
| Tests — Windows, Python 3.12/3.14 | Both base matrix jobs passed. |
| Tests — macOS, Python 3.12/3.14 | Both base matrix jobs passed. |
| Installed wheel — Ubuntu/Windows/macOS, Python 3.12 | All three pure-wheel/no-dependency workflow smokes passed, including the installed M4 Arena/audio/collision checks. |
| Graphics smoke — Ubuntu/Windows/macOS, Python 3.12 | All three real graphics fixtures and the Clockwork Arena wgpu vertical-slice command passed; Ubuntu used the explicitly provisioned Mesa Vulkan software runtime. |

All 14 jobs in run `30996905660` passed. This supplies the cross-platform M4
evidence that was deliberately not claimed by the local gate.

## M5 final local validation — 2026-08-05, Windows, CPython 3.12.13

Focused service, MCP, CLI, architecture, and real graphics tests were run while
the slice was developed. One initial rate-window assertion exposed an incorrect
zero-time threshold and one initial sample composition exposed postponed
component annotations; both attempts failed and were corrected before any pass
was claimed. The final audit also found that successful-result redaction covered
tokens/passwords but not API-key and authorization-shaped fields explicitly;
the redactor and regression test were strengthened, then the entire gate was
rerun on the exact final tree.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Lockfile resolved 46 packages in 0.76 milliseconds. No dependency change was required. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Frozen environment checked 45 packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | All 137 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 545 tests passed and one existing Windows symlink-capability test skipped in 51.70 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Final documentation built successfully in 0.47 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0.dev0.tar.gz` and pure `ludoweave-0.1.0.dev0-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency wheel smoke passed existing workflows plus installed `agent` receipt equivalence, MCP stdio lifecycle/discovery, and the full Agent World Builder loop with a provider-neutral fake capture. |
| `uv run --frozen --extra graphics python examples/agent_world_builder.py` | 0 | The real wgpu composition created six entities, committed create/adjust transactions and three ticks, captured 320x180 RGBA8, passed all registered checks, and recorded five replay batches. Final state hash: `sha256:ad940fab4c432f3c67f5e217f9c7f7460c28973f21ac2f85feb74d9666346be7`; replay hash: `sha256:95d9c87ecd826c1bf33b72ded0779fff02488c08c169735f6c3083638eb45893`. |
| `git diff --check` | 0 | No whitespace errors in the complete tracked diff. |

The final source scan found no credential/private-key literal; matches were
policy text, redaction fixtures, or existing token terminology. Agent source
contains no evaluation primitive. The MCP adapter contains no socket, HTTP, or
network-framework import. Provider imports remain confined to
`ludoweave.render.backends.wgpu`; the sample selects that adapter only at its
composition root. Wheel inspection found only pure Python package files,
metadata, the console entry point, LICENSE, and NOTICE—no native objects, tests,
generated docs, credentials, or mandatory graphics dependency.

Hosted M5 CI had not yet run at the time of the local gate, so that section made
no cross-platform claim.

## M5 hosted validation — GitHub Actions run 30999777517

The DCO-signed M5 implementation commit
`b85bfcd13c56d6ffcfc292823c6e0be33c78f945` was pushed to
`[historical branch name redacted]` and published as stacked pull request #5 against the
validated M4 branch. The resulting least-privilege CI run completed
successfully:

| Hosted job | Result |
| --- | --- |
| Quality and documentation — Ubuntu, Python 3.12 | Passed lock, formatting, lint, strict Pyright with the optional graphics adapter installed, and strict MkDocs gates. |
| Tests — Ubuntu, Python 3.12/3.13/3.14 | All three base matrix jobs passed. |
| Tests — Windows, Python 3.12/3.14 | Both base matrix jobs passed. |
| Tests — macOS, Python 3.12/3.14 | Both base matrix jobs passed. |
| Installed wheel — Ubuntu/Windows/macOS, Python 3.12 | All three pure-wheel/no-dependency smokes passed, including installed agent receipt, MCP stdio, and Agent World Builder checks. |
| Graphics smoke — Ubuntu/Windows/macOS, Python 3.12 | All three real graphics fixtures and the Agent World Builder wgpu composition passed; Ubuntu used the explicitly provisioned Mesa Vulkan software runtime. |

All 14 jobs in run `30999777517` passed. This supplies the cross-platform M5
evidence that was deliberately not claimed by the local gate.

## M6 final local validation — 2026-08-05, Windows, CPython 3.12.13

Focused development checks first passed the deterministic artifact, API
metadata, and release-workflow contracts: five release/workflow tests passed,
two API-stability tests passed, strict Pyright reported no findings, and the
dependency-free `examples/alpha_acceptance.py` returned status `ok` with four
engine ticks, 120 Arena ticks, three agent ticks, five replay batches, and all
registered agent tests passing.

The first default-sandbox invocations of `uv lock --check`, `uv sync`, and
`uv build` each exited 1 because the sandbox could not open uv's managed user
cache. The exact commands were rerun with access to that existing cache and
passed. This was an execution-environment restriction, not recorded as a
project pass.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Final rerun resolved 46 packages in 0.77 milliseconds. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Final frozen rerun checked 45 packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | All 143 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 552 tests passed and one existing Windows symlink-capability test skipped in 45.79 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.44 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and pure `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency installed-wheel version, doctor, M0-M5 workflow, agent, MCP, and sample checks passed outside the source tree. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/release-candidate-final --tag v0.1.0a1` | 0 | Staged ten files: wheel, sdist, fixed-timestamp sample ZIP, LICENSE, NOTICE, optional-dependency notices, release notes, manifest, SPDX SBOM, and exact checksum inventory. |
| `uv run --frozen python scripts/smoke_release.py .tmp/release-candidate-final` | 0 | Exact checksum and manifest coverage, SBOM identity, required notices, safe sample extraction, isolated wheel install, CLI/doctor, and bundled headless examples passed for `0.1.0a1`. |
| `git diff --check` | 0 | No whitespace errors in the complete tracked diff before the factual evidence update. |

Wheel inspection found only the typed pure-Python `ludoweave` package,
distribution metadata, console entry point, LICENSE, and NOTICE. The sample ZIP
contains the eight documented example files plus the Clockwork Arena asset,
all beneath one versioned directory with fixed timestamps. A credential-prefix
scan found no key/token/private-key material. Provider imports remain confined
to `ludoweave.render.backends.wgpu`; no Rust, PyO3, Box2D, new networking,
editor, native object, or mandatory runtime dependency was introduced.

No M6 benchmark was run because the milestone changes distribution,
compatibility metadata, documentation, and community workflow rather than a
performance-sensitive runtime path. No new timing claim is made. At the time
of this local section, hosted M6 CI had not run, so no cross-platform result was
claimed there.

## M6 hosted validation — GitHub Actions run 31002365370

The DCO-signed M6 implementation commit
`84cc318c7c14ccbd2efbda6b61e19cec7c375612` was pushed to
`[historical branch name redacted]` and published as stacked pull request #6 against
the validated M5 branch. The least-privilege CI run completed successfully:

| Hosted job | Result |
| --- | --- |
| Quality and documentation — Ubuntu, Python 3.12 | Passed lock, formatting, lint, strict Pyright with the optional adapter installed, and strict MkDocs. |
| Tests — Ubuntu, Python 3.12/3.13/3.14 | All three jobs passed. |
| Tests — Windows, Python 3.12/3.14 | Both jobs passed. |
| Tests — macOS, Python 3.12/3.14 | Both jobs passed. |
| Installed release candidate — Ubuntu/Windows/macOS, Python 3.12 | All three built the pure wheel/sdist, passed installed-wheel smoke, staged the 10-file candidate, and passed checksum/manifest/SBOM/notice/bundled-sample smoke. |
| Graphics smoke — Ubuntu/Windows/macOS, Python 3.12 | All three real graphics fixtures, Clockwork Arena wgpu run, and Agent World Builder loop passed; Ubuntu used the explicitly provisioned Mesa Vulkan software runtime. |

All 14 jobs passed. Six jobs printed non-failing setup-uv annotations because a
parallel job had already reserved the same cache key; no validation step or
job failed. This supplies the cross-platform M6 artifact evidence deliberately
not claimed by the local-only section.

## M7 final local validation — 2026-08-05, Windows, CPython 3.12.13

M7 profiles the inherited M1/M3 target misses and decides whether the first
Rust/PyO3 kernel satisfies the project admission gate. The decision is a
deferral: no native source, build tool, artifact, dependency, storage object,
or public API was added.

Development feedback was retained rather than reported as a pass:

- The initial profiler quality check exited 1: two new files required Ruff
  formatting and strict Pyright reported 11 `pstats`/unknown-container findings.
  A typed protocol view and explicit container narrowing resolved them.
- The first base-profile command in the default sandbox exited 1 because uv
  could not open its existing user cache. The authorized rerun generated the
  artifact, but its validator exited 1 on the profiler's `python.~` built-in
  record. Built-ins and raw memory-address text are now normalized; the exact
  base and graphics artifacts then validated.
- The first new extraction regressions had two incorrect detail-container
  assertions and four corresponding Pyright findings; they were corrected to
  inspect the immutable detail pairs as a mapping before the focused pass.
- One focused pytest invocation named a nonexistent property-test path and
  exited before collection; the corrected real query/reference/property set
  passed 20 tests.
- The first sprite-packer quality command reported one Ruff import-order
  finding. The mechanical import fix was applied before the final gate.

The final executed command evidence is:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Resolved the existing 46-package lock in 0.76 milliseconds; no dependency changed. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Checked the locked 45-package environment in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | All 148 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 564 tests passed and one existing Windows symlink-capability test skipped in 46.11 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.45 seconds; Material printed its upstream MkDocs 2.0 informational warning. |
| `uv run --frozen python -m benchmarks.profile_m7 --repeats 5 --output .tmp/m7-profile-base-final.json` | 0 | Recorded the exact 10,000-entity simulation and 10,000-sprite extraction/packing profiles under `ludoweave.profile.m7/1`. |
| `uv run --frozen python -m benchmarks.validate_m7_profile .tmp/m7-profile-base-final.json` | 0 | Validated both base workload identities, parameters, invariants, calls, sanitized metadata, and canonical hotspot order. |
| `uv run --frozen --extra graphics python -m benchmarks.profile_m7 --repeats 5 --include-wgpu --output .tmp/m7-profile-graphics-final.json` | 0 | Recorded the two base workloads plus exact 10,000-sprite wgpu CPU submission with engine-owned capabilities. |
| `uv run --frozen python -m benchmarks.validate_m7_profile .tmp/m7-profile-graphics-final.json` | 0 | Validated all three graphics-profile workloads and sanitization contracts. |
| `uv run --frozen python benchmarks/benchmark_m1.py --samples 30 --seed 1 --json-out .tmp/m7-m1-benchmark-final.json` | 0 | Recorded 30 retained samples for all seven M1 workloads after three warmups. |
| `uv run --frozen python benchmarks/validate_m1_results.py .tmp/m7-m1-benchmark-final.json` | 0 | Validated seven workloads and two target records; only the 3,600-tick headless target was observed. |
| `uv run --frozen --extra graphics python benchmarks/benchmark_m3.py --samples 30 --output .tmp/m7-m3-benchmark-final.json` | 0 | Recorded 30 retained samples for all six M3 workloads after three warmups. |
| `uv run --frozen --extra graphics python benchmarks/validate_m3_results.py .tmp/m7-m3-benchmark-final.json` | 0 | Validated six workloads and two target records; neither 10,000-sprite target was observed. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and pure `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency installed-wheel smoke passed outside the source tree. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m7-release-candidate-final` | 0 | Staged the complete 10-file alpha candidate with deterministic sample ZIP, manifest, SPDX SBOM, notices, and checksums. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m7-release-candidate-final` | 0 | Release checksum/manifest/SBOM/notices/sample extraction, isolated install, CLI, doctor, and bundled M0-M5 scenario smoke passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Six real wgpu clear/sprite/capture/resize/loss tests passed in 5.56 seconds. |
| `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 30 --renderer wgpu --render-every 10` | 0 | Offscreen wgpu run completed 30 ticks with three draws and 16 submitted sprite instances. |
| `uv run --frozen --extra graphics python examples/agent_world_builder.py` | 0 | The typed-tool loop committed create/adjust work, completed three ticks, captured 320×180 RGBA8, passed registered tests, and recorded five replay batches. |
| `git diff --check` | 0 | No whitespace errors remained after the factual state update. |

### M7 final local performance observations

| Workload | p50 | p95 | p99 | Target observation |
| --- | ---: | ---: | ---: | --- |
| 10,000-entity simulation tick | 130.1806 ms | 144.0474 ms | 150.6699 ms | `< 4 ms`: not observed |
| 10,000-sprite extraction/packing | 20.8641 ms | 30.6902 ms | 31.4777 ms | `< 3 ms`: not observed |
| 10,000-sprite wgpu CPU submission | 2.8678 ms | 5.1918 ms | 5.2584 ms | `< 3 ms`: not observed |

Against the earlier same-machine records, those p95 values are lower by
26.83%, 26.88%, and 20.57%, respectively. They remain local observations and
are not cross-platform timing claims. Profiler totals include instrumentation
overhead and are not benchmark/frame durations.

The five-repeat graphics profile attributes overlapping cumulative time as
follows: simulation `_open_query` about 55% and component preparation about
47%; extraction interpolation/record construction about 42% and packing about
8%; wgpu submission packing about 86%. The strongest narrow-looking candidate
still reads nested Python objects and cannot release the GIL without a prior
scalar-buffer conversion. RFC-0001 records the missing build, owner, buffer,
GIL, cross-platform, and conformance fields and defers native acceleration.

The final repository/wheel audit found no Cargo manifest, Rust source, direct
NumPy/PyO3/Rust import, credential/private-key literal, native artifact, or new
mandatory dependency. Provider imports remain confined to the existing exact
wgpu adapter. The wheel contains only the typed pure-Python package,
distribution metadata/entry point, LICENSE, and NOTICE. Hosted M7 CI had not
run at the time of this local section, so no cross-platform result is claimed.

## M7 hosted validation — GitHub Actions run 31005165849

The DCO-signed M7 implementation commit
`b14e6c5581e2ca797adc9d71e46d460b941005b8` was pushed to
`[historical branch name redacted]` and published as stacked pull request #7
against the validated M6 branch. The least-privilege pull-request run completed
successfully:

| Hosted job | Result |
| --- | --- |
| Quality and documentation — Ubuntu, Python 3.12 | Passed lock, formatting, lint, strict Pyright, strict MkDocs, and the exact base profiling-contract smoke. |
| Tests — Ubuntu, Python 3.12/3.13/3.14 | All three base matrix jobs passed. |
| Tests — Windows, Python 3.12/3.14 | Both base matrix jobs passed. |
| Tests — macOS, Python 3.12/3.14 | Both base matrix jobs passed. |
| Installed release candidate — Ubuntu/Windows/macOS, Python 3.12 | All three built the pure wheel/sdist, passed installed-wheel smoke, staged the complete candidate, and passed release smoke. |
| Graphics smoke — Ubuntu/Windows/macOS, Python 3.12 | All three passed real clear/sprite/capture/resize/loss tests, exact wgpu profiling-contract smoke, Clockwork Arena, and Agent World Builder; Ubuntu used Mesa Vulkan. |

All 14 jobs passed. Run `31005165849` completed with conclusion `success` for
head `b14e6c5581e2ca797adc9d71e46d460b941005b8`. GitHub reports PR #7 open,
mergeable, and `CLEAN` against `[historical branch name redacted]`. The hosted
profiling steps validate portable execution and artifact contracts only; they
do not create uncontrolled cross-platform timing claims.

Before the hosted-evidence commit, `uv run --frozen mkdocs build --strict` and
`git diff --check` both exited 0; documentation built in 0.55 seconds with only
the already-recorded upstream Material/MkDocs 2.0 informational warning.

## M8 final local validation — 2026-08-05, Windows, CPython 3.12.13

This executed gate was superseded after independent review found three
blocking adapter defects: production window focus was not translated, a GLFW
C-level query error could be mistaken for disconnection, and an unavailable
trigger axis could become a false half press. Its results remain factual
historical evidence but are not the final M8 acceptance evidence.

M8 adds provider-neutral standardized gamepad input and decides whether an
SDL3 adapter is mature enough for the supported alpha baseline. ADR-0023
defers SDL3: the current SDL-listed Python binding is Beta and downloads native
binaries on first use by default, while the already-pinned GLFW dependency
supplies bounded standardized state without a new dependency.

Development feedback was retained rather than reported as a pass:

- The first focused Ruff invocation exited 1 on one export ordering and one
  import ordering finding; Ruff's deterministic fixes resolved both.
- The first focused gamepad test run reported 47 passes and one failure because
  structured error details are immutable pairs rather than a mapping; the
  assertion now copies them through `dict()`.
- The first strict Pyright run after that correction reported two protocol
  return-variance findings in the fake provider; exact `Sequence` annotations
  resolved them.
- A later format check exited 1 on one architecture-test layout and the file
  was formatted before the final gate.
- The first default-sandbox `uv lock --check` and `uv build` invocations each
  exited 1 because the sandbox could not open uv's existing user cache. The
  exact commands were rerun with access to that cache and passed. This was an
  execution-environment restriction, not a project failure.

The final executed command evidence is:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Authorized rerun resolved the unchanged 46-package lock in 1 millisecond. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Checked all 45 locked environment packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | All 149 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 589 tests passed and one existing Windows symlink-capability test skipped in 48.24 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.53 seconds with only the already-recorded upstream Material/MkDocs 2.0 informational warning. |
| `uv build` | 0 | Authorized rerun built `ludoweave-0.1.0a1.tar.gz` and pure `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | The isolated no-dependency installed-wheel smoke passed, including typed gamepad events, deadzone mapping, and Null-provider lifecycle. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m8-release-candidate-local` | 0 | Staged the complete 10-file `ludoweave.release-stage/1` alpha candidate. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m8-release-candidate-local` | 0 | Checksum, manifest, SPDX SBOM, notice, sample, isolated install, CLI, doctor, and bundled workflow smoke passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Eight real wgpu tests passed, including the provider-free device result and a real GLFW null-platform gamepad poll. |
| `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 30 --renderer wgpu --render-every 10` | 0 | Offscreen wgpu completed 30 ticks, three draws, 16 sprite instances, and deterministic state/capture hashes. |
| `uv run --frozen --extra graphics python examples/agent_world_builder.py` | 0 | The typed-tool loop committed create/adjust work, completed three ticks, captured 320×180 RGBA8, passed registered tests, and recorded five replay batches. |
| `uv run --frozen python examples/alpha_acceptance.py` | 0 | The dependency-free acceptance composition returned `status: ok` with four engine ticks, 120 Arena ticks, three agent ticks, and five replay batches. |
| `git diff --check` | 0 | No whitespace errors existed before the factual state/evidence update. |

The final source scan found no introduced credential value, SDL/PySDL3 import,
native artifact, or new dependency. The only provider imports remain inside
`ludoweave.render.backends.wgpu`; architecture fixtures now reject SDL and
PySDL3 imports as well as the existing banned roots. Gamepad events carry only
bounded slots, engine enums, booleans, and normalized floats. Provider names,
GUIDs, timestamps, native objects, and hardware capabilities remain outside
canonical state and public values.

No M8 benchmark was run because polling is bounded to 16 logical slots and the
milestone adds input contracts/adapter translation rather than a frame-scale
simulation or extraction workload. No timing claim is made. Hosted M8 CI has
not run, so no cross-platform M8 pass is claimed here.

## M8 corrected final local validation — 2026-08-05, Windows, CPython 3.12.13

The review-blocking focus, provider-error, and trigger-neutrality defects were
corrected before publication. GLFW focus transitions are prepended during
production surface draining, gamepad and focus queries clear and check the
calling-thread GLFW error state, and GLFW emits only its unambiguous buttons
and four stick axes. The public provider contract retains trigger events for a
future provider that can distinguish capability and neutral state safely.

Development feedback in the corrected pass was retained:

- The first focused Ruff check exited 1 for an import-order finding and one
  stale internal protocol name. Ruff organized the imports and the cast now
  uses `_GlfwGamepadApi`.
- The first strict Pyright pass after adding the focus fake exited 1 with five
  invariant protocol-constant findings. Explicit `ClassVar[int]` annotations
  resolved them.
- The default-sandbox `uv lock --check` and
  `uv sync --frozen --all-groups --extra graphics` commands exited 1 because
  uv's existing user cache was inaccessible. The exact commands passed when
  rerun with authorized cache access; no lock or dependency changed.

The corrected final executed command evidence is:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Authorized rerun resolved the unchanged 46-package lock in 0.72 milliseconds. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Authorized rerun checked all 45 locked environment packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | All 149 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, and 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 594 tests passed and one existing Windows symlink-capability test skipped in 45.16 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.53 seconds with only the already-recorded upstream Material/MkDocs 2.0 informational warning. |
| `uv build` | 0 | Authorized run built `ludoweave-0.1.0a1.tar.gz` and `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | The isolated no-dependency installed-wheel smoke passed, including the M8 gamepad contract. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m8-release-candidate-corrected` | 0 | Staged the complete 10-file `ludoweave.release-stage/1` candidate. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m8-release-candidate-corrected` | 0 | Checksum, manifest, SPDX SBOM, notice, sample, isolated install, CLI, doctor, and bundled workflow smoke passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Eight real wgpu tests passed, including provider-free and real GLFW null-platform gamepad polling. |
| `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 30 --renderer wgpu --render-every 10` | 0 | Offscreen wgpu completed 30 ticks, three draws, 16 sprite instances, and deterministic state/capture hashes. |
| `uv run --frozen --extra graphics python examples/agent_world_builder.py` | 0 | The typed-tool loop committed create/adjust work, completed three ticks, captured 320×180 RGBA8, passed registered tests, and recorded five replay batches. |
| `uv run --frozen python examples/alpha_acceptance.py` | 0 | The dependency-free acceptance composition returned `status: ok` with four engine ticks, 120 Arena ticks, three agent ticks, and five replay batches. |
| PowerShell wheel ZIP inventory | 0 | The built wheel contained 79 entries and zero `.pyd`, `.so`, `.dll`, or `.dylib` entries. |
| `git diff --check` | 0 | No whitespace errors existed after final evidence reconciliation. |

Repeat independent review executed 113 focused unit/architecture tests, two
real gamepad integration selections, Ruff formatting/linting, Pyright, and
`git diff --check`; all passed. It also reproduced an uninitialized pinned
GLFW query becoming structured `platform.gamepad_provider_failure` code 65537.
The reviewer found no remaining blocker, provider/native leakage, credential
exposure, authority violation, dependency drift, or lifecycle/concurrency
regression and recommended M8 for commit and PR.

No M8 benchmark was run and no performance statement is made.

## M8 hosted validation — 2026-08-05

Commit `2a654e03005481d61c6cbeb054b31e260b960659` was pushed to
`[historical branch name redacted]` and published as ready PR #9 against
`main`. GitHub reported the PR mergeable. Actions run `31012696753` completed
successfully with all 14 jobs passing:

- quality and strict documentation;
- Ubuntu CPython 3.12, 3.13, and 3.14;
- Windows CPython 3.12 and 3.14;
- macOS CPython 3.12 and 3.14;
- isolated installed-wheel smoke on Ubuntu, Windows, and macOS; and
- real graphics/gamepad smoke on Ubuntu, Windows, and macOS.

The hosted result validates execution and artifact contracts, not controller
hardware coverage or a performance target. PR #9 remains open and no merge,
tag, release, or package publication is claimed.

## M9 local validation — 2026-08-06, Windows, CPython 3.12.13

M9 evaluates `box2d-python==0.1.2` as an isolated candidate and does not add it
to project metadata, the uv lock, the package, or release dependencies. Primary
package evidence shows an early-development CFFI preview with partial Box2D
v3.0 functionality, no source distribution, CPython 3.12/3.13 wheels only,
macOS ARM64 wheels only, and no Trusted Publishing upload. Official Box2D is
now 3.1.0 and documents cross-platform determinism beginning in 3.1; that claim
is not attributed to this partial v3.0 community binding.

Development feedback is retained rather than reported as a pass:

- An initial CPython 3.12 candidate command used the tuple-position call shown
  on the PyPI example and exited 1 because the installed wheel required two
  position arguments. The corrected isolated call stepped successfully and
  also tolerated repeated `destroy()`.
- The first focused Ruff check found import ordering, a mutable test class
  attribute, and a missing exception import. These were corrected.
- The first focused pytest collection failed because the repository's
  `scripts` directory is not an import package. The test now invokes the real
  script in an isolated subprocess with a fake distribution instead of changing
  project import behavior.
- The first focused Pyright pass found two unsafe `object`-to-float conversions.
  The probe now explicitly validates finite numeric position values.
- A default-sandbox base-environment probe could not open uv's existing cache.
  The authorized exact rerun produced the expected structured `unavailable`
  document with child exit 2 and did not install the candidate.
- Independent review found that distribution metadata and the imported module
  were not yet linked, allowing a shadow `box2d.py` to be misattributed to
  version 0.1.2. The probe now matches the resolved module to the
  distribution's installed-file inventory before import, checks identity again
  after import, fails closed without paths, and has a shadow-module regression.
  It also requires at least one observed position change.

Candidate probe evidence:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv run --no-project --python 3.12 --with box2d-python==0.1.2 python scripts/probe_box2d_candidate.py --iterations 25 --steps 120` | 0 | Windows CPython 3.12.13 completed 25 single-thread create/step/double-destroy repetitions; exact traces matched with SHA-256 `c9e299e715c5f7a3654d7c5794d75347d765cc029b7991d4c8066dfaf7abdfc5`. |
| `uv run --no-project --python 3.13 --with box2d-python==0.1.2 python scripts/probe_box2d_candidate.py --iterations 25 --steps 120` | 0 | Windows CPython 3.13.13 produced the same exact bounded trace digest. |
| `uv run --no-project --python 3.14 --with box2d-python==0.1.2 python scripts/probe_box2d_candidate.py --iterations 25 --steps 120` | 1 | Resolution failed: the release has no matching `cp314` wheel and publishes only `cp312`/`cp313` ABI wheels. The probe did not run. |
| `uv run --frozen python scripts/probe_box2d_candidate.py --iterations 2 --steps 1` | 2 | The locked base environment emitted sanitized schema `ludoweave.evaluation.box2d/1` with status `unavailable`, confirming Box2D is not installed. |

The full executed repository gate is:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Resolved the unchanged 46-package lock in 0.73 milliseconds. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Checked all 45 locked environment packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | All 151 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, and 0 information messages. |
| `uv run --frozen pytest -q` | 0 | The ownership-corrected final run reported 606 tests passed and one existing Windows symlink-capability test skipped in 46.57 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Documentation built successfully in 0.55 seconds with only the known upstream Material/MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and the pure `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency installed-wheel smoke passed. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m9-release-candidate-reviewed-20260806` | 0 | The final post-review build staged the complete 10-file `ludoweave.release-stage/1` candidate. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m9-release-candidate-reviewed-20260806` | 0 | The final post-review checksum, manifest, SPDX SBOM, notice, sample, isolated install, CLI, doctor, and bundled workflow smoke passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Eight real wgpu/GLFW integration tests passed. |
| `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 30 --renderer wgpu --render-every 10` | 0 | Offscreen wgpu completed 30 ticks, three draws, 16 sprite instances, and deterministic state/capture hashes. |
| `uv run --frozen --extra graphics python examples/agent_world_builder.py` | 0 | The typed-tool loop committed create/adjust work, completed three ticks, captured 320×180 RGBA8, passed registered tests, and recorded five replay batches. |
| `uv run --frozen python examples/alpha_acceptance.py` | 0 | The dependency-free acceptance composition returned `status: ok` with four engine ticks, 120 Arena ticks, three agent ticks, and five replay batches. |
| PowerShell wheel ZIP inventory | 0 | The built wheel contained 79 entries and zero `.pyd`, `.so`, `.dll`, or `.dylib` entries. |
| Runtime dependency scan | 1 | No case-insensitive Box2D name matched `src`, `pyproject.toml`, or `uv.lock`; ripgrep exit 1 means no matches. |
| Credential-pattern scan | 1 | No private-key header or simple credential assignment matched the reviewed M9 repository surfaces; ripgrep exit 1 means no matches. |
| `git diff --check` | 0 | No whitespace errors existed before factual evidence reconciliation. |

The Windows traces establish only bounded same-binary headless/lifecycle smoke.
No performance benchmark, cross-platform determinism, rollback, snapshot,
contact-order, GIL-release, thread-safety, free-threaded, or provider-support
claim is made.

Independent review initially blocked sign-off because metadata identity did not
prove ownership of the imported top-level module. After correction, repeat
review ran 54 focused tests, Ruff formatting/linting, strict Pyright,
`git diff --check`, the runtime/dependency scan, and an actual CPython 3.12
candidate probe. It verified the pre-import installed-file ownership check,
post-import identity check, structured broken-install behavior, and
non-executing shadow-module regression; no blocker remained and the reviewer
recommended M9 for final sign-off. Hosted M9 CI had not run at that point.

## M9 hosted validation — 2026-08-06

DCO-signed implementation commit
`8b429aaf07684651f6d538419701c049ee55fc4f` was pushed to
`[historical branch name redacted]` and published as ready stacked PR #10 against
the hosted-validated M8 branch. GitHub Actions run `31015885190` completed with
conclusion `success`; all 14 jobs passed:

- quality, lock, formatting, lint, strict Pyright, strict documentation, and
  base profiling-contract smoke on Ubuntu CPython 3.12;
- tests on Ubuntu CPython 3.12, 3.13, and 3.14;
- tests on Windows and macOS CPython 3.12 and 3.14;
- pure build, isolated wheel smoke, complete release staging, and release smoke
  on Ubuntu, Windows, and macOS; and
- real graphics/gamepad, profiling-contract, Clockwork Arena, and Agent World
  Builder smoke on Ubuntu, Windows, and macOS.

GitHub reports PR #10 open, ready, mergeable, and `CLEAN` against
`[historical branch name redacted]`, whose exact base is
`187ad4503a40325a1e334da3cb4078969e2e043b`. The hosted result validates project
execution and artifact contracts; it does not install the deferred candidate,
exercise controller hardware, or create Box2D performance/cross-platform
determinism claims. No merge, tag, release, or package publication occurred.

## M10 final local validation - 2026-08-06, Windows, CPython 3.12.13

M10 adds one finite headless semantic inspector over an owned local MCP child.
It introduces no runtime dependency, listener, arbitrary process command,
editor, second world store, native code, or release publication.

Development and review feedback is retained rather than reported as a pass:

- The first focused Ruff run found one set-comparison simplification and the
  first focused Pyright run found 19 strict typing issues in decoded JSON.
  Both were corrected before focused tests.
- After the CI job consolidation, the existing release-workflow architecture
  test failed because it still required three redundant wheel jobs. The test
  now asserts one complete distribution gate, the reduced compatibility
  matrix, and retained three-OS graphics coverage.
- Independent review blocked publication on four trust-boundary defects:
  inherited cwd/`PYTHONPATH` could shadow the child package, dash-prefixed
  project names could become child options, a top-level tick result could omit
  a valid receipt, and stream decode/read errors escaped structured handling.
  The child now uses `-I`, binds variable options with `=`, places the project
  after `--`, requires exactly one committed receipt with exact hash/tick
  continuity, and translates Unicode/I/O/closed-stream failures. Source and
  installed-wheel adversarial regressions cover every correction.
- During the adversarial correction pass, one import-order finding and three
  strict typing findings were corrected. The repeat focused gate then passed.
- Final CI review found that the consolidated baseline would duplicate real
  wgpu execution without the dedicated Linux job's Mesa/Vulkan installation.
  Baseline pytest now excludes exactly `test_wgpu_render.py`; the three-OS
  graphics matrix remains its sole gate. Architecture assertions now protect
  least privilege, pins, timeouts, caching, no credential persistence,
  fail-fast policy, cancellation, matrix size, and distribution commands.
- A default-sandbox `uv lock --check` attempt exited 1 because access to uv's
  existing user cache was denied. The approved exact rerun exited 0; this was
  an environment permission failure, not a lock failure.

Final executed repository gate:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | The unchanged lock resolved 46 packages in 0.79 milliseconds. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | The locked environment checked 45 packages in 2 milliseconds. |
| `uv run --frozen ruff format --check .` | 0 | All 154 Python files were formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, and 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 642 tests passed and one existing Windows symlink-capability test skipped in 49.09 seconds. |
| `uv run --frozen pytest -q --ignore=tests/integration/test_wgpu_render.py` | 0 | The exact consolidated baseline command passed 634 non-provider tests with one skip in 52.39 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | The final documentation build completed in 0.48 seconds with only the known Material/MkDocs 2.0 informational warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency installation passed all inherited smoke plus M10 bootstrap/tick receipts and proved a cwd-shadowed `ludoweave` package was not executed. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m10-release-candidate-final-reviewed-20260806` | 0 | Staged the complete 10-file `ludoweave.release-stage/1` candidate. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m10-release-candidate-final-reviewed-20260806` | 0 | Checksum, manifest, SPDX SBOM, notices, sample bundle, isolated install, CLI, doctor, and bundled workflow smoke passed. |
| `uv run --frozen python -m benchmarks.profile_m7 --repeats 1 --output .tmp/m10-profile-base.json` plus validator | 0 | The retained two-workload base profiling contract validated. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Eight real wgpu/GLFW integration tests passed in 5.51 seconds. |
| `uv run --frozen --extra graphics python -m benchmarks.profile_m7 --repeats 1 --include-wgpu --output .tmp/m10-profile-graphics.json` plus validator | 0 | The retained three-workload graphics profiling contract validated. |
| `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 30 --renderer wgpu --render-every 10` | 0 | Offscreen wgpu completed 30 ticks, three draws, 16 sprites, and the expected deterministic state/capture hashes. |
| `uv run --frozen --extra graphics python examples/agent_world_builder.py` | 0 | The typed-tool loop committed create/adjust work, completed three ticks, captured 320x180 RGBA8, passed registered tests, and recorded five replay batches. |
| `uv run --frozen python examples/alpha_acceptance.py` | 0 | Dependency-free acceptance returned `status: ok` with four engine ticks, 120 Arena ticks, three agent ticks, and five replay batches. |
| CI workflow YAML parse and quota contract | 0 | The workflow parsed with exactly eight jobs: one complete baseline, four compatibility, and three graphics jobs. Five focused release/workflow tests passed. |
| Wheel ZIP/metadata inventory | 0 | The wheel contains 80 entries, zero native entries, no mandatory runtime dependency, and only the three exact optional graphics requirements. |
| Local stdio network-import scan | 1 | No network-module import matched the inspector or MCP adapter; ripgrep exit 1 means no matches. |
| Local stdio dynamic-evaluation scan | 1 | No `eval`, `exec`, or `__import__` call matched the inspector or MCP adapter; ripgrep exit 1 means no matches. |
| Deferred-provider scan | 1 | No Box2D or SDL3 binding name matched package source, project metadata, or the lock; ripgrep exit 1 means no matches. |
| Credential-assignment scan | 1 | No credential assignment matched the reviewed M10 source, tests, scripts, docs, or workflow; ripgrep exit 1 means no matches. |
| `git diff --check` | 0 | No whitespace errors. |

The final focused inspector, architecture, and trust-boundary suite reported 81
passes. Repeat independent review reran that suite, Ruff, strict Pyright, and
diff checks, found no remaining implementation blocker, and approved the
corrected M10 head. The exact quota-conscious baseline and separately gated
graphics commands were then executed locally after CI review.

M10 has no benchmark or performance threshold. The retained M7 profiling
commands validate artifact behavior only; no timing result or performance pass
is claimed. Before PR publication, hosted M10 CI had not run and no M10
cross-platform or hosted pass was claimed.

## M10 hosted validation - 2026-08-06

DCO-signed implementation commit
`2e60b3f1c4884dba71df5f23b779bc49187d68c6` was pushed to
`[historical branch name redacted]` and published as ready stacked PR #11
against exact final M9 head
`22bc2de9f8450f60fe483bd4fea10a86702d2f0f`. GitHub Actions run
`31020096463` completed with conclusion `success`; all eight jobs passed:

- the Ubuntu CPython 3.12 quality/test/distribution job passed lock,
  formatting, lint, strict Pyright, strict docs, 634-test baseline, base profile
  contract, pure build, isolated wheel smoke, release staging, and release
  smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profile contract, Clockwork Arena, and Agent World
  Builder passed on Ubuntu software Vulkan, Windows, and macOS.

GitHub reports PR #11 open, ready, mergeable, and `CLEAN` against
`[historical branch name redacted]`. This is the first run of the consolidated
eight-job topology; it replaces the former 14-job topology without dropping a
supported Python version, desktop operating system, complete distribution
gate, or real three-OS graphics gate. No merge, tag, release, or package
publication occurred.

## M11 focused development validation - 2026-08-06

Environment: Windows, uv-managed CPython 3.12.13. M11 is based on exact M10
evidence head `bae799900671481cfd6f03fe502dea95b2c7f96c` and is not yet
published. No hosted or milestone-complete claim is made.

- `uv run --frozen ruff format src/ludoweave/presentation src/ludoweave/audio examples/rich_2d_showcase.py scripts/smoke_wheel.py scripts/release_artifacts.py scripts/smoke_release.py tests`
  exited 0; 76 files were already formatted.
- `uv run --frozen ruff check src/ludoweave/presentation src/ludoweave/audio examples/rich_2d_showcase.py scripts/smoke_wheel.py scripts/release_artifacts.py scripts/smoke_release.py tests/unit/test_presentation.py tests/unit/test_audio.py tests/integration/test_rich_2d_showcase.py tests/architecture`
  exited 0 with `All checks passed!`.
- `uv run --frozen pyright src/ludoweave/presentation src/ludoweave/audio examples/rich_2d_showcase.py scripts/smoke_wheel.py scripts/release_artifacts.py scripts/smoke_release.py tests/unit/test_presentation.py tests/unit/test_audio.py tests/integration/test_rich_2d_showcase.py`
  exited 0 with zero errors, warnings, or information diagnostics.
- `uv run --frozen pytest -q tests/unit/test_presentation.py tests/unit/test_audio.py tests/integration/test_rich_2d_showcase.py tests/architecture`
  exited 0 with 76 passing tests in 1.40 seconds.

An earlier focused run exposed three lint defaults, one tuple return-type
annotation, and an incorrect newly authored particle digest fixture; a second
integration run corrected its expected lifetime count from eight to ten. Those
development failures are not pass evidence. The corrected commands above are
the current focused evidence. Full suite, strict docs, distribution/release,
graphics, independent review, and hosted validation remain pending.

## M11 final reviewed local validation - 2026-08-06

Environment: Windows, uv-managed CPython 3.12.13 with the exact locked graphics
extra. Base: `bae799900671481cfd6f03fe502dea95b2c7f96c`. Branch:
`[historical branch name redacted]`.

The final independently reviewed command sequence produced these results:

- `uv lock --check` exited 0; the 46-package lock was unchanged.
- `uv sync --frozen --all-groups --extra graphics` exited 0; 45 packages were
  checked.
- `uv run --frozen ruff format --check .` exited 0; 164 Python files were
  already formatted.
- `uv run --frozen ruff check .` exited 0 with `All checks passed!`.
- `uv run --frozen pyright` exited 0 with zero errors, warnings, or information
  diagnostics.
- `uv run --frozen pytest -q` exited 0 with 663 passing tests and one existing
  Windows symlink-capability skip in 46.37 seconds.
- `uv run --frozen mkdocs build --strict` exited 0 in 0.47 seconds. Material for
  MkDocs emitted its existing upstream MkDocs 2.0 informational warning.
- `uv build` exited 0 and rebuilt
  `dist/ludoweave-0.1.0a1.tar.gz` plus the universal
  `dist/ludoweave-0.1.0a1-py3-none-any.whl` from the sdist.
- `uv run --frozen python scripts/smoke_wheel.py dist` exited 0 with
  `wheel smoke passed: ludoweave-0.1.0a1-py3-none-any.whl`. The isolated
  no-dependency environment ran CLI/doctor, inherited scenarios, inspector,
  agent builder, and the M11 rich-2D example.
- `uv run --frozen python scripts/release_artifacts.py dist .tmp/m11-release-candidate-reviewed-20260806`
  exited 0 with protocol `ludoweave.release-stage/1`, version `0.1.0a1`, ten
  artifacts, the sample bundle, and SPDX SBOM.
- `uv run --frozen python scripts/smoke_release.py .tmp/m11-release-candidate-reviewed-20260806`
  exited 0 with `release smoke passed: ludoweave 0.1.0a1`; the extracted
  versioned bundle ran `rich_2d_showcase.py` from the installed wheel.
- `git diff --check` exited 0.

Additional retained-gate execution:

- `uv run --frozen python -m benchmarks.profile_m7 --repeats 1 --output .tmp/m11-profile-base.json`
  and its validator exited 0 with schema `ludoweave.profile.m7/1`, two valid
  workloads.
- `uv run --frozen --extra graphics python -m benchmarks.profile_m7 --repeats 1 --include-wgpu --output .tmp/m11-profile-graphics.json`
  and its validator exited 0 with the same schema and three valid workloads.
  These validate inherited artifact contracts only; M11 assigns no timing
  target and makes no performance claim.
- `uv run --frozen pytest -q tests/integration/test_wgpu_render.py` exited 0
  with nine passes in 5.52 seconds, including M11 animation/text/tile/particle
  extraction through the real provider.
- `uv run --frozen --extra graphics python examples/clockwork_arena.py --ticks 30 --renderer wgpu --render-every 10`
  exited 0 with 30 ticks, three draws, 16 sprites, and capture SHA-256
  `05fc014f471d5094f08c8151c650530a6f61016e7b38ee6908306f0ba0b2e906`.
- `uv run --frozen --extra graphics python examples/agent_world_builder.py`
  exited 0 with committed apply/adjust status, six query matches, three ticks,
  five replay batches, and passing registered tests.
- `uv run --frozen python examples/alpha_acceptance.py` exited 0 with protocol
  `ludoweave.sample.alpha_acceptance/1` and status `ok`.
- `uv run --frozen python examples/rich_2d_showcase.py --ticks 6` exited 0 with
  schema `ludoweave.example.rich_2d/1`, animation frame 0, audio gain 0.2, nine
  glyphs, ten particles, 20 sprite instances, eight tile instances, two draw
  calls, and particle digest
  `d3bb0b7050ec5f841de9f0b12997c9e9f4bdeb88f6a14024cd4554103beaa546`.

Artifact and scope audit:

- the wheel contains 87 entries, including all seven
  `ludoweave/presentation` files and zero `.pyd`, `.so`, `.dll`, `.dylib`,
  `.a`, or `.lib` entries;
- metadata has no mandatory `Requires-Dist`; only the unchanged exact graphics
  extra (`glfw`, `rendercanvas[glfw]`, `wgpu`) is present;
- the final release sample ZIP contains `rich_2d_showcase.py`;
- `.github/workflows/ci.yml` is unchanged, so the eight-job essential topology
  remains the only pull-request gate;
- focused scans found no M11 native/provider imports, presentation clock/global
  RNG/thread/network imports, high-confidence credentials, or new-file trailing
  whitespace; and architecture tests passed.

Independent findings-first review initially identified unreachable maximum
tile coordinates, unbounded/quadratic layer traversal, unbounded public
sequence freezing, missing runtime parent-bus fader propagation, particle
work/state bounds, and Ruff generic syntax. The fixes add edge, infinite-
iterator, work-budget, state-lifetime, canonical-order, and nested-gain
regressions. Final re-review reported no blocking, non-blocking, or open finding:
format and Ruff passed, Pyright reported zero, 78 focused tests and 58
architecture/API tests passed, provider isolation and deterministic showcase
passed, and diff/credential checks were clean. One parallel review invocation
collided with the root process on shared `.pytest-tmp` and produced 55 setup
errors; the isolated rerun passed all 78, so that collision is not pass
evidence.

An initial sandboxed full-gate attempt could not read the existing uv user
cache and therefore produced no check evidence. The exact approved reruns above
completed successfully. At this local-gate stage no M11 hosted, cross-platform,
merge, tag, release, or package-publication claim was made.

## M11 hosted validation - 2026-08-06

Ready stacked PR #12 targets `[historical branch name redacted]` from
`[historical branch name redacted]`. GitHub Actions pull-request run `31024155710`
executed signed implementation commit
`aca6d93165a52d88451e8e06d5f1aa8d2e323f1d` and completed successfully from
`2026-08-05T16:12:36Z` through `2026-08-05T16:14:40Z`.

All eight essential jobs concluded `success`:

- `Quality, tests, and distribution` on Ubuntu with CPython 3.12 ran the
  lockfile, formatting, Ruff, Pyright, strict documentation, baseline tests,
  base profiling-contract smoke, sdist/wheel build, isolated-wheel smoke,
  release staging, and release smoke gates.
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14;
- real graphics smoke passed on Ubuntu, Windows, and macOS, including inherited
  clear/sprite/capture/resize/loss/gamepad coverage, graphics profiling,
  Clockwork Arena, and Agent World Builder.

The workflow file was unchanged by M11. This run is the only hosted run created
for the implementation commit. It validates the supported cross-platform
matrix and distribution/provider contracts; it does not merge PR #12, publish
a package, create a tag or release, or admit any deferred provider/native work.

## M12 final reviewed local validation - 2026-08-06

Environment: Windows 11, uv-managed CPython 3.12.13 with the exact locked
graphics extra. Base and current pre-commit `HEAD`:
`840a8b06d461fa1d5e649911b22f5995154728a7`. Branch:
`[historical branch name redacted]`.

The complete independently reviewed command sequence produced these results:

- The first sandboxed `uv lock --check` attempt exited 1 because the workspace
  sandbox denied access to uv's existing user cache. The approved exact rerun
  exited 0 and resolved the unchanged 46-package lock.
- `uv sync --frozen --all-groups --extra graphics` exited 0 and checked 45
  packages.
- `uv run --frozen ruff format --check .` exited 0; 170 Python files were
  already formatted.
- `uv run --frozen ruff check .` exited 0 with `All checks passed!`.
- `uv run --frozen pyright` exited 0 with zero errors, warnings, or information
  diagnostics.
- `uv run --frozen pytest -q` exited 0 with 741 passing tests and one existing
  Windows symlink-capability skip in 47.87 seconds.
- `uv run --frozen mkdocs build --strict` exited 0 in 0.50 seconds. Material for
  MkDocs emitted its existing upstream MkDocs 2.0 informational warning.
- `uv build` exited 0 and rebuilt
  `dist/ludoweave-0.1.0a1.tar.gz` plus the universal
  `dist/ludoweave-0.1.0a1-py3-none-any.whl` from the sdist.
- `uv run --frozen python scripts/smoke_wheel.py dist` exited 0 with
  `wheel smoke passed: ludoweave-0.1.0a1-py3-none-any.whl`; the isolated wheel
  check included the explicit M12 manifest and path-free compatible report.
- `uv run --frozen python scripts/release_artifacts.py dist .tmp/m12-release-candidate-final-reviewed-20260806`
  exited 0 with protocol `ludoweave.release-stage/1`, version `0.1.0a1`, ten
  artifacts, the versioned sample bundle, and SPDX SBOM.
- `uv run --frozen python scripts/smoke_release.py .tmp/m12-release-candidate-final-reviewed-20260806`
  exited 0 with `release smoke passed: ludoweave 0.1.0a1`; the extracted bundle
  checked `example.plugin.json` through the isolated installed wheel.
- `git diff --check` exited 0.

Provider and example acceptance:

- `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py`
  exited 0 with nine passes in 5.53 seconds.
- Null and real-wgpu `examples/clockwork_arena.py --ticks 600` runs both exited
  0 with the same authoritative state hash
  `sha256:b7a77c7fa0f0bab668245723719a4e57c00f5f821b4df8cf013dcf9aaaf34c70`;
  the wgpu run completed 600 draws and produced an offscreen capture.
- `uv run --frozen --extra graphics python examples/agent_world_builder.py`
  exited 0 with committed apply/adjust status, six query matches, three ticks,
  five replay batches, and passing registered tests.
- `uv run --frozen python examples/alpha_acceptance.py` exited 0 with protocol
  `ludoweave.sample.alpha_acceptance/1` and status `ok`.
- `uv run --frozen python examples/rich_2d_showcase.py --ticks 6` exited 0 with
  schema `ludoweave.example.rich_2d/1`, nine glyphs, ten particles, 20 sprite
  instances, eight tile instances, and two draw calls.
- `uv run --frozen ludoweave plugin check examples/example.plugin.json` exited
  0 with canonical protocol `ludoweave.plugin-check/1`, one compatible plugin,
  no issues or path, and manifest-set fingerprint
  `sha256:c2ed00ea4153e92aec46c5e80d22324656fe4009903c638544faa48cba9d24a2`.

Every benchmark/profile command in the README quality suite was also rerun
against uniquely named M12 artifacts and its validator exited 0:

- M1 recorded seven workloads. The fixed 3,600-tick p95 was 35,648,600 ns and
  observed its headless target; the 10,000-entity simulation p95 was
  118,236,300 ns and did not observe its inherited 4 ms target. The validator
  reported one of two recorded targets observed.
- M2 validated four informational workloads with no timing targets.
- M3 validated six workloads with zero of its two inherited timing targets
  observed.
- M4 validated three workloads; the baseline p95 was 1,824,800 ns and observed
  its 16,666,667 ns target.
- The five-repeat M7 base and real-wgpu profile artifacts validated with two
  and three workloads respectively. Profile timing is diagnostic only.

Artifact, scope, and history audit:

- the wheel contains 91 entries, including four `ludoweave/plugins` files and
  zero `.pyd`, `.so`, `.dll`, `.dylib`, `.a`, or `.lib` entries;
- wheel metadata has no mandatory dependency; its only `Requires-Dist` entries
  are the unchanged exact `graphics` extra for GLFW, rendercanvas, and wgpu;
- credential-assignment and plugin backend/discovery/evaluation/filesystem
  scans found no matches; ripgrep exit 1 means no matches;
- the CI workflow, `pyproject.toml`, and `uv.lock` are unchanged, retaining the
  eight essential hosted jobs and pure-Python package contract; and
- `HEAD`, local M11, and remote-tracking M11 all resolved to
  `840a8b06d461fa1d5e649911b22f5995154728a7` before the M12 commit. Merge-base
  matched exactly and the pre-commit left/right count was `0 0`, so the stack
  contains no missing or unrelated commit.

Independent findings-first review reproduced and drove regressions for bounded
cycle diagnostics, canonical detail/report limits, exact error types and
protocol values, mixed-key and pre-bound mapping validation, exact plugin
identities, deterministic immutable decision state, path-free diagnostics,
explicit import/global-state/I/O/evaluation architecture rules, and sanitized
CLI parsing before file I/O. Final re-review reported no blocking or
non-blocking finding; its corrected focused plugin/CLI/architecture/API/release
suite passed 138 tests, with clean Ruff, Pyright, strict docs, diff, and
isolated CLI checks.

At this stage no M12 hosted or cross-platform pass, merge, tag, release, package
publication, discovery/loading/execution, provider admission, networking,
editor/GUI, deferred Box2D/SDL3 adapter, or native-code claim is made.

## M12 hosted validation - 2026-08-06

Ready stacked PR #13 targets `[historical branch name redacted]` from
`[historical branch name redacted]`. Its one DCO-signed implementation
commit is `e1f6e3cd8572d20a4f0a5c62a96b9aa52a986b38`; GitHub reports the PR open,
ready, mergeable, and `CLEAN` against exact final M11 evidence head
`840a8b06d461fa1d5e649911b22f5995154728a7`.

GitHub Actions pull-request run `31028863469` executed the implementation
commit from `2026-08-05T17:11:37Z` through `2026-08-05T17:13:23Z` and concluded
`success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profiling
  contract, sdist/wheel build, isolated-wheel smoke including the explicit
  plugin manifest, release staging, and complete release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file was unchanged by M12. This is the only hosted run created for
the implementation commit. It validates the supported cross-platform,
distribution, and provider contracts; it does not merge PR #13, publish a
package, create a tag or release, load plugin code, admit a provider, or
authorize any deferred networking/editor/native work.

## M13 final reviewed local validation - 2026-08-06

Environment: Windows 11, uv-managed CPython 3.12.13 with the exact locked
graphics extra. Base and current pre-commit `HEAD`:
`7cb834c7b5e84e1b1a945905a68b947b3a4bdd3f`. Branch:
`[historical branch name redacted]`.

The complete post-review command sequence produced these results:

- The first sandboxed `uv lock --check` / `uv sync --frozen --all-groups
  --extra graphics` attempt exited 1 because the workspace sandbox denied
  access to uv's existing user cache. The approved exact rerun exited 0:
  `uv lock --check` resolved the unchanged 46-package lock and sync checked 45
  packages. An initial sandboxed `uv build` had the same cache denial; its
  approved exact rerun and final post-review rebuild both exited 0.
- `uv run --frozen ruff format --check .` exited 0; all 174 Python files were
  already formatted.
- `uv run --frozen ruff check .` exited 0 with `All checks passed!`.
- `uv run --frozen pyright` exited 0 with zero errors, warnings, or information
  diagnostics.
- `uv run --frozen mkdocs build --strict` exited 0 in 0.51 seconds. Material
  for MkDocs emitted its existing upstream MkDocs 2.0 informational warning.
- `uv run --frozen pytest -q` exited 0 with 793 passing tests and one existing
  Windows symlink-capability skip in 60.05 seconds.
- `uv build` exited 0 and rebuilt
  `dist/ludoweave-0.1.0a1.tar.gz` plus the universal
  `dist/ludoweave-0.1.0a1-py3-none-any.whl` from the sdist.
- `uv run --frozen python scripts/smoke_wheel.py dist` exited 0 with
  `wheel smoke passed: ludoweave-0.1.0a1-py3-none-any.whl`; the isolated wheel
  ran the M13 24/12 readiness proof and required deferred/no-transport gates.
- `uv run --frozen python scripts/release_artifacts.py dist
  .tmp/m13-release-candidate-final-20260806` exited 0 with protocol
  `ludoweave.release-stage/1`, version `0.1.0a1`, ten artifacts, the versioned
  sample bundle, and SPDX SBOM.
- `uv run --frozen python scripts/smoke_release.py
  .tmp/m13-release-candidate-final-20260806` exited 0 with
  `release smoke passed: ludoweave 0.1.0a1`; the isolated installed wheel ran
  the bundled readiness example.
- `git diff --check` exited 0.

M13 evidence and provider acceptance:

- `uv run --frozen python examples/rollback_readiness.py --ticks 120
  --branch-tick 60 --output .tmp/m13-readiness-final.json` exited 0 with schema
  `ludoweave.evaluation.rollback-readiness/1`, status `deferred`, no transport,
  120 parent batches/121 verified checkpoints, 60 child batches/61 verified
  checkpoints, immutable parent timeline hash
  `sha256:c4650d3173a0b62eb9e65e1a49f8e90fa90c9268b56ab9000fb75b096ec0e515`,
  parent final hash
  `sha256:9d4b4f5e81ed1ac487f83ae742ce41cfb27f2a0da652a43c33c74e5571cd3026`,
  and repeatable corrected final hash
  `sha256:2708c1bb1df45adaca0eb095242f12b96837493e2bd06cd8a3c78b45742af7b2`.
  The informational canonical sizes were 2,793 snapshot bytes, 95,118 parent
  timeline bytes, and 51,160 child timeline bytes; M13 defines no timing or
  bandwidth target.
- `uv run --frozen python scripts/validate_rollback_readiness.py
  .tmp/m13-readiness-final.json` exited 0 with
  `rollback readiness evidence valid`.
- The final hostile integration/architecture/release focus exited 0 with 54
  passes in 13.01 seconds. It covers direct-call work bounds, exact checkpoint
  counts, root/nested duplicate JSON, non-finite numbers, non-regular and
  oversized files, exact root types/version, Boolean/integer ambiguity,
  hashes/counts/metrics, false admission, and closed import/member aliases.
- `uv run --frozen --extra graphics pytest -q
  tests/integration/test_wgpu_render.py` exited 0 with nine passes in 5.65
  seconds.
- Clockwork Arena wgpu, Agent World Builder, alpha acceptance, rich-2D
  showcase, and the path-free compatible example plugin check all exited 0.

Every benchmark/profile command in the README quality suite was also rerun
against uniquely named M13 artifacts and its validator exited 0:

- M1 recorded seven workloads. The fixed 3,600-tick p95 was 35,707,100 ns and
  observed its headless target; the 10,000-entity simulation p95 was
  136,388,500 ns and did not observe its inherited 4 ms target. The validator
  reported one of two recorded targets observed.
- M2 validated four informational workloads with no timing targets.
- M3 validated six workloads. The 10,000-sprite extraction p95 was 24,154,400
  ns and missed its inherited target; the wgpu submit p95 was 2,747,400 ns and
  observed its target. One of two recorded targets was observed.
- M4 validated three workloads; the baseline p95 was 1,840,000 ns and observed
  its 16,666,667 ns target.
- The five-repeat M7 base and real-wgpu profile artifacts validated with two
  and three workloads respectively. Profile timing is diagnostic only.

Artifact, scope, and history audit:

- the wheel contains 91 entries and zero `.pyd`, `.so`, `.dll`, or `.dylib`
  entries;
- wheel metadata has no mandatory dependency; its only `Requires-Dist` entries
  are the unchanged exact `graphics` extra for GLFW, rendercanvas, and wgpu;
- `.github/workflows/ci.yml`, `pyproject.toml`, `uv.lock`, and all `src/` files
  are unchanged from the exact M12 base, retaining the eight essential jobs,
  persistent formats, public Python surfaces, and pure-Python package contract;
- focused secret-assignment and network/provider import scans found no match;
  ripgrep exit 1 means no matches; and
- merge-base equals exact M12 head
  `7cb834c7b5e84e1b1a945905a68b947b3a4bdd3f` and the pre-commit left/right
  count was `0 0`, so no unrelated commit entered the stack.

Independent hostile review reproduced and drove fixes for pre-read byte caps,
regular-file pre/post-open checks, canonical duplicate/non-finite JSON,
version/path spoofing, exact Boolean/integer/count types, direct-call work
bounds, complete parent/child checkpoint verification, closed exact
module/member import allowlists, and dynamic-builtin aliases. Final review
reported no blocking or non-blocking finding. It independently passed Ruff,
Pyright, strict docs, 54 focused tests, a generated/validated 24/12 artifact,
and the advertised maximum 600/300 proof in 19.1 seconds with deferred and
no-transport gates. Diff and secret scans were clean.

At this stage no M13 hosted or cross-platform pass, merge, tag, release,
package publication, socket/listener, peer authority, live rollback service,
network protocol, persistent-format change, editor/GUI, 3D, provider adapter,
or native-code claim is made.

## M13 hosted validation - 2026-08-06

Ready stacked PR #14 targets `[historical branch name redacted]` from
`[historical branch name redacted]`. Its one DCO-signed implementation
commit is `ba62b650191cfb982100692e7ec694da318956ae`; GitHub reports the PR open,
ready, mergeable, and `CLEAN` against exact final M12 evidence head
`7cb834c7b5e84e1b1a945905a68b947b3a4bdd3f`.

GitHub Actions pull-request run `31031590206` executed the implementation
commit from `2026-08-05T17:46:38Z` through `2026-08-05T17:48:41Z` and concluded
`success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profiling
  contract, sdist/wheel build, isolated-wheel smoke including the M13
  readiness proof, release staging, and complete release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file was unchanged by M13. This is the only hosted run created for
the implementation commit. It validates the supported cross-platform,
distribution, and provider contracts; it does not merge PR #14, publish a
package, create a tag or release, or authorize sockets, remote authority, live
rollback, a network protocol, editor/GUI, 3D, provider/native work, or a
persistent-format change.

## M14 final local validation - 2026-08-06

M14 was evaluated on Windows 11 with uv-managed CPython 3.12.13. It changes
repository evidence, tests, and documentation only. Its installed JSON confirms
the exact 47-name public render export list, orthographic `Camera2D` fields and
matrix, canonical sprite `(layer, z, entity)` ordering, the tile layer field,
color-only descriptors, 2D limits, and the seven existing world operations.
All nine constrained-3D admission gates are false.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | The existing lock resolved 46 packages and remained current. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | The existing frozen environment checked 45 packages. |
| `uv run --frozen ruff format --check .` | 0 | All 178 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, and 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 809 tests passed and one existing Windows symlink-capability test skipped in 69.68 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built in 0.51 seconds; Material emitted its documented upstream MkDocs 2.0 warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and the universal `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency wheel install passed the exact M14 installed-surface document plus the inherited public smokes. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m14-release-candidate-r2` | 0 | Staged the complete deterministic ten-artifact candidate including the M14 sample. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m14-release-candidate-r2` | 0 | Checksums, manifest, SBOM, installed wheel, and every bundled sample including exact M14 evidence passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Nine real-wgpu integration tests passed in 5.51 seconds. |
| `git diff --check` | 0 | No whitespace errors. |

Every inherited benchmark/profile command in the README quality suite ran
against uniquely named M14 artifacts and its validator exited 0:

- M1 validated seven workloads. Fixed 3,600-tick p95 was 35,706,500 ns and
  observed its target; 10,000-entity simulation p95 was 128,658,700 ns and did
  not observe the inherited 4 ms target. One of two targets was observed.
- M2 validated four informational workloads with no timing targets.
- M3 validated six workloads. The 10,000-sprite extraction p95 was 28,468,500
  ns and missed its inherited target; real-wgpu 10,000-instance submission p95
  was 2,835,700 ns and observed its target. One of two targets was observed.
- M4 validated three workloads; baseline p95 was 1,877,900 ns and observed its
  16,666,667 ns target.
- Five-repeat M7 base and real-wgpu profile artifacts validated with two and
  three workloads respectively. Profile timing remains diagnostic only.

Artifact, scope, history, and independent-review evidence:

- the wheel contains 91 entries and zero `.pyd`, `.so`, `.dll`, or `.dylib`
  entries; metadata retains Apache-2.0, Python `>=3.12,<3.15`, no mandatory
  dependency, and only the unchanged exact `graphics` extra;
- `.github/workflows/ci.yml`, `pyproject.toml`, `uv.lock`, and all `src/` files
  are byte-unchanged from exact M13 evidence head
  `48f8f296113e3f2794bae7f4c67997d433e4dd36`;
- merge-base equals that exact M13 head and the pre-commit left/right count was
  `0 0`; focused credential assignment scanning returned no matches (ripgrep
  exit 1); and
- independent hostile review first blocked positive layered-2D evidence,
  exact artifact validation, and closed import/export guards. After correction,
  it independently reproduced lock/static/full-test/docs/build/wheel/release
  success, rejected tampered sorting/version/export/gate documents, found no
  credential match, and approved with no remaining finding.

At this stage no M14 hosted/cross-platform pass, merge, tag, release, package
publication, runtime/public/persistent-format change, 3D feature, provider
dependency, or new performance-target claim is made.

## M14 hosted validation - 2026-08-06

Ready stacked PR #15 targets `[historical branch name redacted]` from
`[historical branch name redacted]`. Its DCO-signed implementation commit is
`47443046834eb423be977973775f80494161533d`. GitHub reports the PR open,
ready, mergeable, and `CLEAN` against exact final M13 evidence head
`48f8f296113e3f2794bae7f4c67997d433e4dd36`.

GitHub Actions pull-request run `31033924254` executed the implementation
commit from `2026-08-05T18:16:06Z` through `2026-08-05T18:18:37Z` and
concluded `success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profile smoke,
  sdist/wheel build, exact isolated-wheel M14 evidence, release staging, and
  complete release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file was unchanged by M14, and the branch has exactly this one
pull-request CI run for the implementation commit. Hosted evidence confirms
the supported installed/cross-platform/provider contracts; it does not merge
PR #15, publish a package, create a tag or release, add 3D runtime behavior,
change a public/persistent contract, or admit a new dependency/provider.

## M8-M14 main integration - 2026-08-06

Direct-main integration PR #16 used exact base
`0237b2bfb11c6032d030dada639c7dbe439e5089` and final M14 evidence head
`02426805a11712030b3082ec349696d6d94aca50`. The pre-merge audit found 14
linear commits, zero merge commits, and DCO sign-off in all 14. The M8-M14
implementation runs `31012696753`, `31015885190`, `31020096463`,
`31024155710`, `31028863469`, `31031590206`, and `31033924254` were all
re-queried from GitHub and reported completed `success`.

PR #16 was open, ready, `MERGEABLE`, and `CLEAN`. Its final evidence head
contained `[skip ci]`, so opening the integration PR created no redundant
matrix. The user-authorized squash merge completed at
`2026-08-05T18:22:37Z` as GitHub-verified main commit
`2c62c8ed9c4ced6292260f6b8c84b1f069de1eaa`. Its tree
`137a1870b0dd9034ad935b253a13186f6c7cc913` exactly equals the validated M14
head tree. The squash message includes the DCO sign-off and all seven hosted
run IDs.

Stacked PRs #9-#15 were closed as superseded after the exact-tree check;
branches were retained. The integration creates no tag, release, package
publication, new runtime/provider behavior, or additional Actions run.

## M15 final local validation - 2026-08-06

M15 was evaluated on Windows 11 with uv-managed CPython 3.12.13. It changes
repository evidence, tests, and documentation only. Its deterministic installed
document derives the exact four-name root export surface, empty tools exports,
the exact 20-name all-experimental agent surface, twelve tools, seven world
operations, command/transaction/receipt/agent/inspector/MCP revisions, and
inspector configuration/read-only facts. It also executes one ephemeral
six-command write-enabled agent transaction and verifies a committed v1
receipt, six committed outcomes, pre/post/authority hash continuity, unchanged
tick count, and six resulting entities. All twelve editor-admission gates
remain false.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | The existing lock resolved 46 packages and remained current. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | The existing frozen environment checked 45 packages. |
| `uv run --frozen ruff format --check .` | 0 | All 182 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, and 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 834 tests passed and one existing Windows symlink-capability test skipped in 62.59 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built in 0.52 seconds; Material emitted its documented upstream MkDocs 2.0 warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and the universal `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | The isolated no-dependency wheel install passed the exact M15 installed document plus inherited public smokes. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m15-release-candidate-r2` | 0 | Staged the complete deterministic ten-artifact candidate including the M15 sample. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m15-release-candidate-r2` | 0 | Checksums, manifest, SBOM, installed wheel, and every bundled sample including exact M15 evidence passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Nine real-wgpu integration tests passed in 5.59 seconds. |
| `git diff --check` | 0 | No whitespace errors. |

The first sandboxed attempt to start the complete uv gate could not access the
user-managed uv cache and therefore ran no check; the authorized rerun above
completed successfully. The corrected focused review suite reported 120 passes,
clean Ruff/Pyright, and strict docs before the final full gate.

Every inherited README benchmark/profile command ran against uniquely named
M15 artifacts and its validator exited 0:

- M1 validated seven workloads. Fixed 3,600-tick p95 was 35,317,100 ns and
  observed its target; 10,000-entity simulation p95 was 158,073,300 ns and did
  not observe the inherited 4 ms target. One of two targets was observed.
- M2 validated four informational workloads with no timing targets.
- M3 validated six workloads. The 10,000-sprite extraction p95 was 24,263,200
  ns and real-wgpu 10,000-instance submission p95 was 3,057,200 ns; neither
  observed its inherited target in this local run. Zero of two targets was
  observed.
- M4 validated three workloads; baseline p95 was 1,885,700 ns and observed its
  16,666,667 ns target.
- Five-repeat M7 base and real-wgpu profile artifacts validated with two and
  three workloads respectively. Profile timing remains diagnostic only.

Artifact, scope, history, and independent-review evidence:

- the exact alpha wheel contains 91 entries and zero `.pyd`, `.so`, `.dll`, or
  `.dylib` entries;
- `.github/workflows/ci.yml`, `pyproject.toml`, `uv.lock`, and all `src/` files
  are byte-unchanged from exact base
  `bfea67d2d922e8c591224d18f56c14d572d7f7da`;
- merge-base equals that exact base and the pre-commit left/right count is
  `0 0`; deferred-interface import and credential-assignment scans found no
  match; and
- independent review initially blocked hard-coded inspector-public status,
  shallow agent stability evidence, non-executed receipt claims, narrow root
  export/dependency guards, formatting, and stale roadmap/state text. After
  correction, the reviewer independently reproduced 120 focused and 834 full
  passes, static/docs/build/wheel/release success, protected scope, history,
  and credential scans and approved with no remaining finding.

At this stage no M15 commit, hosted/cross-platform pass, PR, merge, tag,
release, package publication, runtime/public/persistent-format change,
GUI/editor implementation, toolkit/dependency, or new performance-target claim
is made.

## M15 hosted validation - 2026-08-06

Ready PR #19 targets `main` from `[historical branch name redacted]`. Before
the evidence-only follow-up, GitHub reported exact base
`bfea67d2d922e8c591224d18f56c14d572d7f7da`, implementation head
`7e85570056dde3678aaeee13eee4036067876d8c`, `MERGEABLE`, and `CLEAN`. The
implementation history contains one DCO-signed commit.

GitHub Actions pull-request run `31036925179` executed that implementation
commit from `2026-08-05T18:54:18Z` through `2026-08-05T18:56:30Z` and
concluded `success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profile smoke,
  sdist/wheel build, exact isolated-wheel M15 evidence, release staging, and
  complete release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file is unchanged, and this is the only hosted run created for
the implementation commit. Hosted evidence confirms the supported installed,
cross-platform, and provider contracts; it does not publish a package, create
a tag or release, add a GUI/editor/runtime API, promote the experimental agent
surface, change a persistent format, or admit a new dependency/provider.

## M16 final local validation - 2026-08-06

M16 was evaluated on Windows 11 with uv-managed CPython 3.12.13. It changes
repository evidence, tests, release-sample composition, and documentation only.
The deterministic installed document records the complete exact three-entry
optional-graphics `Requires-Dist` set, exact root/plugin exports and preview
stability, ten inert manifest fields, eight capability labels, typed rejection
of six representative executable fields, no WASM runtime requirement, no
public guest-execution export, and fifteen false admission gates. It compiles
or executes no guest.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | The existing lock resolved 46 packages and remained current. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | The existing frozen environment checked 45 packages. |
| `uv run --frozen ruff format --check .` | 0 | All 186 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | All lint checks passed. |
| `uv run --frozen pyright` | 0 | 0 errors, 0 warnings, and 0 information messages. |
| `uv run --frozen pytest -q` | 0 | 870 tests passed and one existing Windows symlink-capability test skipped in 65.04 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built in 0.55 seconds; Material emitted its documented upstream MkDocs 2.0 warning. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and the universal `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | The isolated no-dependency wheel install passed the exact M16 installed document plus inherited public smokes. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m16-release-candidate-reviewed-20260806` | 0 | Staged the complete deterministic ten-artifact candidate including the M16 sample. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m16-release-candidate-reviewed-20260806` | 0 | Checksums, manifest, SBOM, installed wheel, and every bundled sample including exact M16 evidence passed. |
| `uv run --frozen pytest -q tests/integration/test_wgpu_render.py` | 0 | Nine real-wgpu integration tests passed in 5.62 seconds. |
| `uv run --frozen python examples/wasm_mod_security_decision.py` | 0 | Emitted the exact deferred `ludoweave.evaluation.wasm-mod-security/1` document. |
| `git diff --check` | 0 | No whitespace errors. |

The first sandboxed `uv lock --check` and two sandboxed `uv build` attempts
could not open the user-managed uv cache and exited 1 before completing those
checks. Their explicitly authorized reruns above exited 0. The first strict
docs attempt found two links outside the documentation tree; the links were
corrected and both final and independent strict builds passed.

Every inherited README benchmark/profile command ran against uniquely named
M16 artifacts and its validator exited 0:

- M1 validated seven workloads. Fixed 3,600-tick p95 was 36,551,800 ns and
  observed its target; 10,000-entity simulation p95 was 123,939,400 ns and did
  not observe the inherited 4 ms target. One of two targets was observed.
- M2 validated four informational workloads with no timing targets.
- M3 validated six workloads. The 10,000-sprite extraction p95 was 24,013,300
  ns and real-wgpu 10,000-instance submission p95 was 3,172,000 ns; neither
  observed its inherited target in this local run. Zero of two targets was
  observed.
- M4 validated three workloads; baseline p95 was 1,817,500 ns and observed its
  16,666,667 ns target.
- Five-repeat M7 base and real-wgpu profile artifacts validated with two and
  three workloads respectively. Profile timing remains diagnostic only.

Artifact, scope, history, and independent-review evidence:

- the exact alpha wheel contains 91 entries and zero `.pyd`, `.so`, `.dll`,
  `.dylib`, WASM runtime, or WASI entries;
- `.github/workflows/ci.yml`, `pyproject.toml`, `uv.lock`, the version, and all
  `src/` files are byte-unchanged from exact base
  `c013dad38b1b64f0f4ccddc19681d643f6414427`; the eight-job CI topology is
  unchanged;
- explicit, dynamic, and named-module fixtures prove the WASM runtime guard,
  including the reproduced `webassembly_runtime.py` bypass; unknown and
  malformed installed requirement fixtures fail before evidence success; and
- independent review initially blocked blacklist-only requirement evidence,
  the named-module bypass, missing residual risk, and inaccurate current-flow
  wording. After correction, the reviewer ran
  `uv run --frozen pytest -q tests/architecture/test_import_boundaries.py tests/architecture/test_m16_wasm_boundary.py tests/integration/test_wasm_mod_security_decision.py tests/unit/test_release_artifacts.py tests/architecture/test_release_workflow.py`
  with 140 passes in 3.30 seconds, independently reproduced clean focused
  Ruff/Pyright, strict docs, offline build, wheel/release smoke, exact evidence,
  protected scope, and diff checks, and approved with no remaining finding.

At this stage no M16 commit, hosted/cross-platform pass, PR, merge, tag,
release, package publication, runtime/public/persistent-format change,
executable mod, WASI/host-call surface, dependency, or new performance-target
claim is made.

## M16 hosted validation - 2026-08-06

Ready PR #20 targets `main` from
`[historical branch name redacted]`. Before the evidence-only follow-up,
GitHub reported exact base `c013dad38b1b64f0f4ccddc19681d643f6414427`,
implementation head `bcaf78fbc78bda8a13a95e397ab15d003dd4a6ce`,
`MERGEABLE`, and `CLEAN`. The implementation history contains one DCO-signed
commit.

GitHub Actions pull-request run `31039403209` executed that implementation
commit from `2026-08-05T19:26:18Z` through `2026-08-05T19:28:52Z` and
concluded `success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profile smoke,
  sdist/wheel build, exact isolated-wheel M16 evidence, release staging, and
  complete release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file is unchanged, and this is the only hosted run created for
the implementation commit. Hosted evidence confirms the supported installed,
cross-platform, and provider contracts; it does not publish a package, create
a tag or release, add an executable mod/runtime/WASI/host-call surface, change
a public or persistent contract, or admit a new dependency/provider.

## M16 main integration - 2026-08-06

PR #20 used exact base `c013dad38b1b64f0f4ccddc19681d643f6414427`
and final evidence head `808e48a5cb2727c8e1f4d7e896c4f8c7d41bfe1a`.
The two-commit branch history contains a DCO trailer on both commits. The final
evidence commit contains `[skip ci]`, and GitHub lists only implementation run
`31039403209` for the branch.

The user-authorized squash merge completed at `2026-08-05T19:31:34Z` as
GitHub-verified main commit `e2bd57c057c0c16861953c0702b2012c4cabfe90`
with verification reason `valid`. Its sole parent is the exact base, its DCO
trailer is a real commit-message trailer, and tree
`05367be9bd85014fe6c70995ac1a69a39f90ef1e` exactly equals the final M16
branch tree. The milestone branch is retained.

The integration creates no tag, release, package publication, executable mod,
runtime/provider/dependency behavior, or additional Actions run. The
authoritative post-alpha sequence ends with M16 item 10; no M17 milestone or
acceptance criteria are assigned by the current plan.

## M17 installed render-device conformance - local final gate - 2026-08-06

M17 was subsequently assigned from the design plan's longer-term metric for
third-party adapters/plugins passing conformance. Branch
`[historical branch name redacted]` started from exact clean synchronized
`main` commit `27d2ee9d1f7f75dacc17568650f00ce833ef4fce` (`main...origin/main`
left/right count `0 0`). The bounded slice is one experimental installed
`RenderDevice` baseline over an explicitly supplied trusted factory. It adds
no adapter discovery/loading/installation, provider dependency, plugin field,
canonical/persistent world state, version change, or CI job.

Final Windows local gate used uv-managed CPython 3.12.13:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Resolved the unchanged 46-package lock. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Checked the locked 45-package environment. |
| `uv run --frozen ruff format --check .` | 0 | All 191 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | No lint findings. |
| `uv run --frozen pyright` | 0 | Zero errors, warnings, or information findings. |
| `uv run --frozen pytest -q` | 0 | 895 passed and one existing Windows symlink-capability test skipped in 64.75 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built; the upstream Material MkDocs-2 warning remained informational. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and universal `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | The isolated no-dependency wheel passed all inherited flows plus the nine-check Null render-device profile. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m17-release-candidate-final-reviewed` | 0 | Staged the complete deterministic ten-artifact candidate including the updated sample bundle. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m17-release-candidate-final-reviewed` | 0 | Exact checksums/manifest/SBOM/notices, safe extraction, isolated install, inherited samples, and bundled Null conformance passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | All 10 real-wgpu tests passed in 5.87 seconds, including the shared baseline. |
| `uv run --frozen --extra graphics python examples/render_device_conformance.py --backend wgpu` | 0 | Protocol `ludoweave.render-device-conformance/1`, profile `render-device-baseline/1`, adapter `wgpu`, all nine checks `pass`. |
| `uv run --frozen pytest -q tests/unit/test_render_device_conformance.py tests/architecture/test_m17_conformance_boundary.py tests/architecture/test_import_boundaries.py` | 0 | 121 focused success, failure-sanitization, lifecycle, explicit-factory, and dependency-boundary tests passed. |

Artifact inspection found 92 wheel entries, including
`ludoweave/render/conformance.py`, and zero `.pyd`, `.so`, `.dll`, `.dylib`,
or `.wasm` entries. Installed metadata retains no mandatory requirement and
the exact existing graphics extra only:

- `glfw==2.10.2; extra == 'graphics'`;
- `rendercanvas[glfw]==2.7.2; extra == 'graphics'`; and
- `wgpu==0.32.0; extra == 'graphics'`.

The protected `.github/workflows/ci.yml`, `pyproject.toml`, `uv.lock`, package
version, and package-root exports are unchanged. M14's installed render-export
fingerprint was updated from 47 to the exact 53-name surface by adding only the
two conformance constants, status enum, two frozen report records, and runner;
its layered-2D facts and every 3D admission gate remain unchanged.

All documented benchmark/profile validation contracts were executed on the
dirty M17 working tree and validated:

- M1: seven workloads; fixed-step p95 `54,750,000 ns` observed its target,
  while 10,000-entity simulation p95 `126,505,000 ns` missed; 1 of 2 recorded
  targets observed.
- M2: four informational workloads validated with no timing threshold.
- M3: six workloads; 10,000-sprite extraction p95 `24,179,800 ns` and wgpu
  submission p95 `3,735,200 ns` both missed; 0 of 2 targets observed.
- M4: baseline p95 `1,863,200 ns` observed its target; two stress workloads
  remained informational.
- M7: five-repeat base profile with two workloads and graphics profile with
  three workloads both validated under `ludoweave.profile.m7/1`.

Two sandboxed command attempts failed before executing project code because
the managed sandbox denied uv cache access at
`C:\Users\louij\AppData\Local\uv\cache`; the same commands were rerun with
approved cache access and passed as recorded above. One earlier wheel smoke
correctly failed after the additive public render exports changed M14's exact
installed-surface fixture. The fixture was updated to the six exact M17 names,
then focused M14/M15/M16 tests, final wheel smoke, and final release smoke all
passed. No product failure remains unresolved.

## M17 hosted validation - 2026-08-06

Ready PR #22 targets `main` from
`[historical branch name redacted]`. GitHub reported exact base
`27d2ee9d1f7f75dacc17568650f00ce833ef4fce`, implementation head
`8e592f329424719214239bf97bd85dad9c9c5928`, `MERGEABLE`, and `CLEAN`. The
implementation history contains one DCO-signed commit.

GitHub Actions pull-request run `31042903689` executed that implementation
commit from `2026-08-05T20:11:26Z` through `2026-08-05T20:13:48Z` and
concluded `success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profile smoke,
  sdist/wheel build, installed-wheel smoke, release staging, and complete
  release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file is unchanged, and this is the only hosted run created for
the implementation commit. Hosted evidence validates supported installed,
cross-platform, and existing-provider behavior; it does not certify or admit
third-party code, count project-owned adapters as independent adoption,
publish a package, create a tag or release, add discovery/loading/install
behavior, change a public or persistent format, or claim the locally missed
M1/M3 performance targets passed.

After recording these hosted facts, `uv run --frozen mkdocs build --strict`
exited 0 in 0.58 seconds with only the documented upstream Material MkDocs-2
warning, and `git diff --check` exited 0.

## M17 main integration - 2026-08-06

PR #22 used exact base `27d2ee9d1f7f75dacc17568650f00ce833ef4fce`
and final evidence head `148600cdaf9c419fbf552c68f833e0d55655731f`.
The two-commit branch history contains a DCO trailer on both commits. The final
evidence commit contains `[skip ci]`; GitHub lists only implementation run
`31042903689` for the branch.

The user-authorized squash merge completed at `2026-08-05T20:17:17Z` as
GitHub-verified `main` commit
`610261c8450afc3d7db6ebb2b0425a1829737aec` with verification reason `valid`.
Its sole parent is the exact base, its DCO trailer is a real commit-message
trailer, and tree `1e82568a463c62d0a1cf988b67eea09885ec50e3`
exactly equals the final M17 branch tree. The milestone branch is retained.

The first local tree comparison used unquoted PowerShell revision braces and
failed before comparing with an encoded-argument parsing error. The corrected
quoted `git rev-parse "HEAD^{tree}"` and
`git rev-parse "origin/main^{tree}"` commands both returned the exact tree
above, and `git diff --exit-code HEAD origin/main` exited 0.

The integration creates no tag, release, package publication, adapter
discovery/loading/installation, provider admission, dependency, workflow
change, or additional Actions run. Project-owned Null/wgpu conformance remains
reference evidence and does not increase independent third-party adoption.

On the integration-evidence branch,
`uv run --frozen mkdocs build --strict` exited 0 in 0.56 seconds with only the
documented upstream Material MkDocs-2 warning, and `git diff --check` exited 0.

PR #23 then squash-integrated the M17 repository-state evidence into `main` as
GitHub-verified commit `ed65b12fa02f672113eac5939a0f616079fee44a` without a
new Actions run. The retained M18 branch starts from that exact synchronized
commit.

## M18 installed agent-tool conformance - local final gate - 2026-08-06

Branch `[historical branch name redacted]` started from exact clean synchronized
`main` commit `ed65b12fa02f672113eac5939a0f616079fee44a`. The bounded slice is
one experimental installed 12-tool agent-service baseline over an explicitly
supplied trusted factory. It adds no discovery, dynamic import, installation,
subprocess, network transport, provider, plugin field, dependency, lock,
version, persistent format, canonical state, package-root export, or CI job.

Final Windows local gate used uv-managed CPython 3.12.13:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Resolved the unchanged 46-package lock. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Checked the locked 45-package environment. |
| `uv run --frozen ruff format --check .` | 0 | All 196 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | No lint findings. |
| `uv run --frozen pyright` | 0 | Zero errors, warnings, or information findings. |
| `uv run --frozen pytest -q` | 0 | 925 tests passed and one existing Windows symlink-capability test skipped in 66.24 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built; the upstream Material MkDocs-2 warning remained informational. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and universal `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | The isolated no-dependency wheel passed inherited flows plus the exact 12-check direct agent-service profile. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m18-release-candidate-final-20260806-b` | 0 | Staged the complete deterministic ten-artifact candidate including the M18 sample. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m18-release-candidate-final-20260806-b` | 0 | Checksums, manifest, SBOM, notices, safe extraction, isolated install, inherited samples, and bundled agent conformance passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | All 10 existing real-wgpu integration tests passed in 5.80 seconds. |
| `uv run --frozen pytest -q tests/unit/test_agent_tool_conformance.py tests/architecture/test_m18_agent_conformance_boundary.py tests/integration/test_agent_tool_conformance_example.py tests/unit/test_release_artifacts.py tests/integration/test_visual_editor_decision.py tests/architecture/test_release_workflow.py tests/architecture/test_import_boundaries.py` | 0 | 145 focused success, adversarial-sanitization, receipt/atomicity, lifecycle, explicit-factory, release, and dependency-boundary tests passed in 3.91 seconds. |
| `git diff --check` | 0 | No whitespace errors. |
| `git fsck --no-dangling` | 0 | Repository object/connectivity check reported no issue. |

Artifact inspection found 93 wheel entries, including
`ludoweave/agent/conformance.py`, and no `.pyd`, `.so`, `.dll`, `.dylib`, or
`.wasm` entry. Metadata retains Python `>=3.12,<3.15`, no mandatory
requirement, and only the exact existing optional graphics requirements:

- `glfw==2.10.2; extra == 'graphics'`;
- `rendercanvas[glfw]==2.7.2; extra == 'graphics'`; and
- `wgpu==0.32.0; extra == 'graphics'`.

The protected `.github/workflows/ci.yml`, `pyproject.toml`, `uv.lock`, package
version, and package-root exports are unchanged. Source scans found no
credential assignment, discovery/process/network import or call, or backend/
native dependency in the conformance runtime/example. The M15 exact installed
agent-export fingerprint was updated only with the seven experimental M18
names; its visual-editor decision and admission gates are unchanged.

All documented benchmark/profile validation contracts were executed on the
dirty M18 working tree and validated:

- M1: seven workloads; fixed-step p95 `39,482,100 ns` observed its target,
  while 10,000-entity simulation p95 `122,772,500 ns` missed; 1 of 2 recorded
  targets observed.
- M2: four informational workloads validated with no timing threshold.
- M3: six workloads; 10,000-sprite extraction p95 `23,673,400 ns` and wgpu
  submission p95 `3,437,400 ns` both missed; 0 of 2 targets observed.
- M4: baseline p95 `1,821,000 ns` observed its target; two stress workloads
  remained informational.
- M7: five-repeat base profile with two workloads and graphics profile with
  three workloads both validated under `ludoweave.profile.m7/1`.

Development checks first exposed import/export sorting, one unnecessary cast,
and one unknown-result type issue; all were corrected and the focused/full
static gates were rerun clean. Skeptical review then strengthened exact receipt
identity/outcome validation, invalid-factory cleanup, control-flow cleanup
during close, and nested forbidden-import fixtures before the final gate.
One sandboxed `uv build` attempt exited 1 before project execution because
access to uv's user cache was denied; the approved rerun and all final artifact
commands above exited 0. No product failure remains unresolved.

History review before publication reports `HEAD`, local `main`, `origin/main`,
and the merge base at exact commit
`ed65b12fa02f672113eac5939a0f616079fee44a`, with left/right count `0 0` and
the intended linear squash-integrated milestone history. At this stage no M18
commit, hosted/cross-platform pass, PR, merge, tag, release, or package
publication is claimed.

## M18 hosted validation - 2026-08-06

Ready PR #24 targets `main` from
`[historical branch name redacted]`. GitHub reported exact base
`ed65b12fa02f672113eac5939a0f616079fee44a`, DCO-signed implementation head
`c4dde705393eebb7c99af428745e9383750f6b4d`, `MERGEABLE`, and `CLEAN` after
checks completed.

GitHub Actions pull-request run `31046172544` executed that implementation
commit from `2026-08-05T20:52:57Z` through `2026-08-05T20:55:24Z` and
concluded `success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profile smoke,
  sdist/wheel build, installed-wheel smoke, release staging, and complete
  release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file is unchanged, and this is the only hosted run created for
the implementation commit. Hosted evidence validates the supported installed,
cross-platform, and existing-provider contracts. It does not discover, admit,
certify, or count third-party adapter code; establish real-agent manual-
recovery rates; publish a package; create a tag or release; add a transport,
listener, provider, dependency, or CI job; or claim the locally missed M1/M3
performance targets passed.

## M18 main integration - 2026-08-06

PR #24 used exact base `ed65b12fa02f672113eac5939a0f616079fee44a`
and final evidence head `cb617be0f678528fadc82877ec6910e42c6daf6b`.
The two-commit branch history contains a DCO trailer on both commits. The final
evidence commit contains `[skip ci]`, and GitHub lists only implementation run
`31046172544` for the branch.

The user-authorized squash merge completed at `2026-08-05T20:57:29Z` as
GitHub-verified `main` commit
`1000d362432f19c912edf51c67e29c79bf444443` with verification reason `valid`.
Its sole parent is the exact base, its DCO trailer is a real commit-message
trailer, and tree `1b6676ca7c1a6aaa223057a35e0c95242f4e9462`
exactly equals the final M18 branch tree. The milestone branch is retained.

The integration creates no tag, release, package publication, adapter
discovery/loading/installation, transport, provider admission, dependency,
workflow change, or additional Actions run. Project-owned direct-service
conformance remains reference evidence and does not increase independently
authored adapter adoption or establish real-agent manual-recovery rates.

## M19 installed WorldStore conformance - local final gate - 2026-08-06

Branch `[historical branch name redacted]` starts from exact clean synchronized
`main` commit `4076f3d7ac0c0a82834a1c98dcb36426ba67ac5e`, with local `main`,
`origin/main`, both merge bases, and `HEAD` initially equal and left/right count
`0 0`. The bounded slice adds one experimental installed ten-check profile over
an explicit trusted `factory(ComponentRegistry)`. It adds no discovery, dynamic
import, installation, subprocess, network operation, backend, database,
external-resource lifecycle, native/archetype/NumPy storage, persistent format,
plugin field, dependency, lock, version, package-root export, or CI job.

Final hardened Windows gate used uv-managed CPython 3.12.13:

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Resolved the unchanged 46-package lock. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Checked the locked 45-package environment. |
| `uv run --frozen ruff format --check .` | 0 | All 201 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | No lint findings. |
| `uv run --frozen pyright` | 0 | Zero errors, warnings, or information findings. |
| `uv run --frozen pytest -q` | 0 | 955 tests passed and one existing Windows symlink-capability test skipped in 73.37 seconds. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built in 0.80 seconds; the upstream Material MkDocs-2 warning remained informational. |
| `uv build` | 0 | Built `ludoweave-0.1.0a1.tar.gz` and universal `ludoweave-0.1.0a1-py3-none-any.whl`. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | The isolated no-dependency wheel passed all inherited flows plus both ten-check built-in WorldStore profiles. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/release-candidate` | 0 | Staged the complete deterministic ten-artifact candidate including `world_store_conformance.py`. |
| `uv run --frozen python scripts/smoke_release.py .tmp/release-candidate` | 0 | Checksums, manifest, SBOM, notices, safe extraction, isolated install, inherited samples, and bundled production/reference WorldStore conformance passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | All ten existing real-wgpu integration tests passed in 7.05 seconds. |
| `uv run --frozen pytest -q tests/unit/test_world_store_conformance.py tests/architecture/test_m19_world_store_conformance_boundary.py tests/integration/test_world_store_conformance_example.py tests/unit/test_release_artifacts.py tests/conformance tests/architecture/test_import_boundaries.py tests/architecture/test_api_stability.py` | 0 | 149 focused success, adversarial-sanitization, epoch/copy/query/command/clone, explicit-factory, release, API, and dependency-boundary tests passed in 2.02 seconds. |
| `git diff --check` | 0 | No whitespace errors. |
| `git fsck --no-dangling` | 0 | Repository object/connectivity check reported no issue. |

The final wheel contains 94 entries including exactly one
`ludoweave/ecs/conformance.py`, and no `.pyd`, `.so`, `.dll`, `.dylib`, or
`.wasm` entry. Metadata retains Python `>=3.12,<3.15`, no mandatory
requirement, and only the exact existing optional graphics requirements:

- `glfw==2.10.2; extra == 'graphics'`;
- `rendercanvas[glfw]==2.7.2; extra == 'graphics'`; and
- `wgpu==0.32.0; extra == 'graphics'`.

The protected `.github/workflows`, `pyproject.toml`, `uv.lock`, package version,
and package-root exports are unchanged from the exact base. The sample bundle
contains one project-owned `world_store_conformance.py`. Source scans found no
credential assignment or wall-clock/random use; the only broad discovery/
process/network scan match was the runtime docstring explicitly stating that
subprocess and network operations are absent. AST tests reject discovery,
private storage, concrete reference, filesystem, process, network, NumPy, and
SQLite imports and prove nested forbidden imports are detected.

All documented benchmark/profile contracts were executed on the dirty M19
working tree and validated:

- M1: seven workloads; fixed-step p95 `36,282,500 ns` observed its target,
  while 10,000-entity simulation p95 `164,496,800 ns` missed; one of two
  recorded targets observed.
- M2: four informational workloads validated with no timing threshold.
- M3: six workloads; 10,000-sprite extraction p95 `26,171,800 ns` and wgpu
  submission p95 `3,465,100 ns` both missed; zero of two targets observed.
- M4: baseline p95 `2,019,400 ns` observed its target; two stress workloads
  remained informational.
- M7: five-repeat base profile with two workloads and graphics profile with
  three workloads both validated under `ludoweave.profile.m7/1`.

Development validation first exposed postponed component annotations in the
fixture, import/export ordering, one unnecessary cast, and two incorrect
adversarial-test assumptions; all were corrected before the complete gate.
Findings-first final review then added exact property-shape checks, adapter-stage
control-flow propagation coverage, and precise direct-import architecture
wording. The complete static, 955-test, installed-wheel, and release gates were
rerun on that hardened tree with no remaining finding.

Initial sandboxed `uv lock --check`, `uv sync`, and `uv build` invocations each
exited 1 before project execution because access to uv's existing user cache
was denied. Approved cache-access reruns and every final command above exited
0; these were environment-permission failures, not lock, sync, or build
failures. No M19 hosted/cross-platform pass, PR, merge, tag, release, package
publication, certification, or independently authored adapter adoption is
claimed at this stage.

## M19 hosted validation - 2026-08-06

Ready PR #26 targets `main` from
`[historical branch name redacted]`. GitHub reported exact base
`4076f3d7ac0c0a82834a1c98dcb36426ba67ac5e`, DCO-signed implementation head
`1da692a693c1f92e10b676c2d4539354ce3ff59f`, `MERGEABLE`, and `CLEAN` after
checks completed.

GitHub Actions pull-request run `31092244573` executed that implementation
commit from `2026-08-06T10:11:30Z` through `2026-08-06T10:14:03Z` and
concluded `success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profile smoke,
  sdist/wheel build, installed-wheel smoke, release staging, and complete
  release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file is unchanged, and GitHub lists this as the only hosted run
for the M19 branch. Hosted evidence validates supported installed,
cross-platform, and existing-provider contracts. It does not discover, admit,
certify, or count third-party storage implementations; establish persistence,
external-resource lifecycle, free-threaded safety, or maintenance readiness;
publish a package; create a tag or release; add a backend, dependency, format,
or CI job; or claim the locally missed M1/M3 performance targets passed.

## M19 main integration - 2026-08-06

Ready PR #26 was squash-merged at `2026-08-06T10:17:52Z`. GitHub reports
merged commit `1a7219e540d8f4cb3c1f60ff12981513c6860ef9` with sole parent
`4076f3d7ac0c0a82834a1c98dcb36426ba67ac5e`, exact tree
`7fcd614fdde76daf1807f27dbe78ec306a501cc3`, a valid GitHub signature, and the
DCO trailer. The tree exactly matches final evidence head
`b93ca591f7063a1500cf105e6b0496b33573c69a` on retained branch
`[historical branch name redacted]`; `git diff --exit-code` reported no
difference between those trees.

GitHub still lists only successful run `31092244573` for the milestone branch;
the documentation-only hosted-evidence commit used `[skip ci]` and created no
second run. Integration changes no runtime, public API, workflow, dependency,
lock, package version, benchmark target, format, or release artifact. No tag,
GitHub release, PyPI publication, provider discovery/admission/certification,
or independently authored WorldStore adoption is claimed.

## M20 baseline and initial evidence - 2026-08-06

M20 starts from exact clean synchronized `main` commit
`2fdeccd697f09f3e165130eb8564a6c585d472d2` on branch
`[historical branch name redacted]`.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Approved cache-access rerun resolved 46 packages in 0.84 ms. |
| `uv run --frozen pytest -q tests/unit/test_canonical_json.py tests/unit/test_persistent_command_schema.py tests/unit/test_transactions.py tests/unit/test_receipts.py tests/unit/test_agent_tool_conformance.py tests/integration/test_agent_cli.py tests/architecture/test_api_stability.py` | 0 | 91 focused baseline tests passed in 1.52 seconds. |
| `uv run --frozen pytest -q` | 0 | 955 tests passed with one existing Windows symlink-capability skip in 72.22 seconds. |
| `uv run --frozen python examples/command_receipt_stability_decision.py` | 0 | The initial versioned installed evidence confirmed the current boundary and returned deferred `retain-experimental-command-receipt`. |
| `uv run --frozen pytest -q tests/integration/test_command_receipt_stability_decision.py tests/architecture/test_m20_command_receipt_stability_boundary.py` | 0 | 16 exact-evidence, tamper, stability-drift, argument, dependency, and nested-import boundary tests passed in 2.05 seconds. |

The first sandboxed `uv lock --check` attempt exited 1 before project execution
because uv could not access its existing user cache. The approved cache-access
rerun above is the project result. At this stage the complete static, full,
documentation, build, isolated-wheel, release, provider, benchmark/profile, and
findings-first review gates remain pending. No hosted M20 run, PR, merge, tag,
release, package publication, stability promotion, cross-version compatibility,
or external consumer/adoption evidence is claimed.

## M20 final local validation and review - 2026-08-06

The final reviewed tree remains based on exact `main` commit
`2fdeccd697f09f3e165130eb8564a6c585d472d2`. M20 changes no file under
`.github`, `src/ludoweave`, `pyproject.toml`, or `uv.lock`.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Approved cache-access rerun checked 45 packages. |
| `uv run --frozen ruff format --check .` | 0 | All 205 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | No lint findings. |
| `uv run --frozen pyright` | 0 | Zero errors, warnings, or information findings. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built; only the upstream MkDocs Material/MkDocs 2.0 informational warning was emitted. |
| `uv run --frozen pytest -q tests/integration/test_command_receipt_stability_decision.py tests/architecture/test_m20_command_receipt_stability_boundary.py tests/unit/test_release_artifacts.py tests/unit/test_canonical_json.py tests/unit/test_persistent_command_schema.py tests/unit/test_transactions.py tests/unit/test_receipts.py tests/unit/test_agent_tool_conformance.py tests/integration/test_agent_cli.py tests/architecture/test_api_stability.py tests/architecture/test_import_boundaries.py tests/architecture/test_release_workflow.py` | 0 | 211 expanded evidence, canonical transaction/receipt, agent, artifact, and architecture tests passed in 4.24 seconds. |
| `uv run --frozen pytest -q` | 0 | 972 tests passed with one existing Windows symlink-capability skip in 73.99 seconds. |
| `uv build` | 0 | Approved cache-access final build produced `ludoweave-0.1.0a1.tar.gz` and the universal pure-Python wheel. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | The isolated no-dependency installed-wheel workflow, including M20 evidence validation, passed. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m20-release-final` | 0 | A fresh complete ten-artifact release directory was staged. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m20-release-final` | 0 | Checksums, manifest, SPDX SBOM, installed wheel, and all sample-bundle evidence passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Ten real-wgpu integration tests passed in 6.29 seconds. |
| `git diff --check` | 0 | No whitespace errors. |
| `git diff --exit-code main -- .github pyproject.toml uv.lock src/ludoweave` | 0 | Workflow, metadata, lock, and runtime package trees are unchanged. |
| `git fsck --no-dangling` | 0 | Repository object connectivity is clean with no dangling objects reported. |

The M20 evidence runs twice byte-for-byte identically in its integration test.
Its exact validator rejects value and JSON-type drift, arguments, and an
unrecorded stability promotion. The source, isolated wheel, and deterministic
sample-bundle paths all return deferred
`retain-experimental-command-receipt`. The final wheel contains 94 entries,
declares only the existing optional graphics extra, contains no native/WASM
file, and the release sample ZIP contains
`command_receipt_stability_decision.py`.

All inherited documented performance artifacts validate:

- M1's 3,600-tick p95 was 42.0198 ms and observed its 12-second target; the
  10,000-entity simulation p95 was 125.6192 ms and missed the 4 ms target.
- M2's four target-free informational p50/p95 observations were
  31.8993/35.7171 ms for canonical 100-command round trips,
  14.2993/15.8356 ms for atomic 100-command apply, 18.0485/19.5923 ms for
  1,000-entity snapshot round trips, and 210.5091/229.5513 ms for verified
  100-batch replay.
- M3's 10,000-sprite extraction p95 was 26.2983 ms and real-wgpu submission
  p95 was 3.1636 ms; both missed their 3 ms starting targets.
- M4's baseline Clockwork Arena p95 was 2.1096 ms and observed its 16.666667
  ms target. Stress 4/8 p95 values were 3.0000/4.4796 ms with no targets.
- Five-repeat M7 base and graphics profiling artifacts validated with two and
  three workloads respectively. These are call-profile contracts, not timing
  targets.

Development evidence is retained rather than rewritten as a false clean first
attempt. Initial sandboxed `uv lock --check`, `uv sync`, and `uv build` calls
exited 1 before project execution because uv's existing user cache was denied;
approved cache-access reruns exited 0. The first evidence composition omitted
the explicit capture provider required by the M18 profile and was corrected.
The first Ruff pass found two smoke-script import-order issues and passed after
correction. Findings-first review identified that exact-name import checks
would miss forbidden submodules; prefix matching and a nested wgpu fixture now
cover that case, and the focused boundary suite passes 17 tests in 2.05
seconds.

The final scope/credential/backend review found no new credential assignment,
ambient time/random/environment/path input, native/WASM/backend leakage,
runtime/public API change, dependency change, workflow change, stale link, or
unsupported pass claim. No hosted M20 run, PR, merge, tag, release, package
publication, cross-version compatibility, external adoption, or stability
promotion is claimed at this stage.

After recording the final evidence, one post-record gate reran `uv lock
--check`, Ruff format/check, Pyright, strict MkDocs, the 17 M20 integration and
architecture tests, and `git diff --check` in sequence. Every command exited 0;
the focused tests passed in 2.07 seconds. A fresh `git fetch --prune origin`
then confirmed local `main`, `origin/main`, the M20 merge base, and branch HEAD
all share exact base `2fdeccd697f09f3e165130eb8564a6c585d472d2`; the reviewed
history is linear and GitHub reports `main` as the default branch.

## M20 hosted validation - 2026-08-06

Ready PR #28 targets `main` from
`[historical branch name redacted]`. GitHub reports exact base
`2fdeccd697f09f3e165130eb8564a6c585d472d2`, DCO-signed implementation head
`d96d132da5ee847d6e86645be5e87a1e4aa5e89e`, `MERGEABLE`, and `CLEAN` after
checks completed.

GitHub Actions pull-request run `31095009029` executed that implementation
commit from `2026-08-06T10:52:55Z` through `2026-08-06T10:55:33Z` and
concluded `success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` on Ubuntu CPython 3.12 passed lock,
  formatting, Ruff, Pyright, strict docs, baseline tests, base profile smoke,
  sdist/wheel build, installed-wheel smoke, release staging, and complete
  release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file is unchanged, and GitHub lists this as the only hosted run
for the M20 branch. Hosted evidence confirms supported installed and cross-
platform same-version behavior. It does not establish cross-version
compatibility, external consumer adoption, a public receipt reader, a
deprecation-capable release channel, stability promotion, certification, tag,
release, or package publication; add a runtime/API/schema/dependency/version/CI
change; or claim the locally missed M1/M3 performance targets passed. PR #28
has not yet been merged at this stage.

## M21 main integration - 2026-08-06

Ready PR #30 was squash-merged at `2026-08-06T11:50:27Z`. GitHub reports
merged commit `6bfb56555cafc93a7312f64465ea15cd7c450e79` with sole parent
`feed793e94c345fac4b146c358a68264ef6e5f62`, exact tree
`ea3f410fac31d7a32faee4e697c4fb0941b657df`, a valid GitHub signature verified
at `2026-08-06T11:50:31Z`, and the DCO trailer. The tree exactly matches final
evidence head `4e378756b2a1733de28e7160ac2d6d72921f3e4a` on retained branch
`[historical branch name redacted]`; literal tree comparison reported no
difference.

GitHub still lists only successful run `31098563810` for the milestone branch;
the documentation-only hosted-evidence commit used `[skip ci]` and created no
second run. Integration changes no receipt protocol/field, command, operation,
stability label, workflow, dependency, lock, package version, backend, storage,
benchmark target, root export, or release artifact. No tag, GitHub release,
PyPI publication, cross-version compatibility, receipt authenticity, external
consumer adoption, certification, or stability promotion is claimed.

After `git fetch --prune origin`, local `main` fast-forwarded to the verified
squash commit and matched `origin/main` with a clean worktree. The retained M21
branch remains available for audit history.

After adding this hosted record, `uv run --frozen mkdocs build --strict` and
`git diff --check` both exited 0; the documentation build emitted only the
recorded upstream MkDocs Material/MkDocs 2.0 informational warning.

## M20 main integration - 2026-08-06

Ready PR #28 was squash-merged at `2026-08-06T10:58:12Z`. GitHub reports
merged commit `d166ef86bf25526d9d7715f63263d3cac6db78d4` with sole parent
`2fdeccd697f09f3e165130eb8564a6c585d472d2`, exact tree
`c3e2dc1224f530fb483d1b9684ff55329bf9557b`, a valid GitHub signature verified
at `2026-08-06T10:58:16Z`, and the DCO trailer. The tree exactly matches final
evidence head `d04561184996fac507071ad9e7dd0ef9c5e3cb7c` on retained branch
`[historical branch name redacted]`; corrected literal-revision
`git rev-parse` checks and `git diff --exit-code` reported equal trees and no
difference.

GitHub still lists only successful run `31095009029` for the milestone branch;
the documentation-only hosted-evidence commit used `[skip ci]` and created no
second run. The first read-only tree query left PowerShell revision braces
unquoted and was parsed incorrectly, producing fatal ambiguous-revision output;
the quoted rerun above exited 0 and is the recorded result. Integration changes
no runtime, public API, protocol, stability label, workflow, dependency, lock,
package version, benchmark target, format, or release artifact. No tag, GitHub
release, PyPI publication, cross-version compatibility, external consumer
adoption, public receipt reader, or stability promotion is claimed.

The documentation-only integration record passes `uv run --frozen mkdocs
build --strict`, `git diff --check`, and the protected-surface comparison
`git diff --exit-code origin/main -- .github pyproject.toml uv.lock
src/ludoweave`; all exited 0. The docs build emitted only the recorded upstream
MkDocs Material/MkDocs 2.0 informational warning.

## M21 baseline and development evidence - 2026-08-06

M21 starts from exact clean synchronized `main` commit
`feed793e94c345fac4b146c358a68264ef6e5f62` on branch
`[historical branch name redacted]`. The branch was created before any M21
change and the initial history inspection showed that commit as local `main`,
`origin/main`, `origin/HEAD`, and the feature-branch base.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Resolved the unchanged 46-package lock in 0.71 ms. |
| `uv run --frozen pytest -q tests/unit/test_receipts.py tests/unit/test_persistent_command_schema.py tests/unit/test_canonical_json.py tests/architecture/test_api_stability.py tests/architecture/test_import_boundaries.py tests/unit/test_release_artifacts.py` | 0 | 138 focused baseline tests passed in 1.70 seconds. |
| `uv run --frozen pytest -q` | 0 | The inherited suite passed 972 tests with one existing Windows symlink-capability skip in 69.25 seconds. |
| Corrected reader unit/static group | 0 | 26 reader tests passed in 0.41 seconds; Ruff and Pyright reported no finding for the group. |
| Corrected fixture/reader group | 0 | 24 exact corpus, round-trip, limit, and compatibility tests passed in 0.39 seconds; focused Ruff and Pyright reported no finding. |
| Corrected installed/release group | 0 | 34 deterministic example, validator, isolated-artifact integration, and release-registration tests passed in 2.22 seconds; focused static checks were clean. |
| Combined M20/M21 focused group | 0 | 58 tests passed in 3.46 seconds. Ruff was clean after one mechanical import-order correction; Pyright then identified one frozen-value mutation in a test helper, which was corrected. The combined post-correction gate remains pending. |
| `uv run --frozen ruff check <M20/M21 changed Python files>` | 0 | Corrected focused files passed all Ruff checks. |
| `uv run --frozen pyright` | 0 | Corrected complete project reported zero errors, warnings, or information findings. |
| `uv run --frozen pytest -q tests/unit/test_receipt_reader.py tests/integration/test_receipt_v1_compatibility_corpus.py tests/integration/test_receipt_reader_example.py tests/integration/test_command_receipt_stability_decision.py tests/architecture/test_m21_receipt_reader_boundary.py tests/architecture/test_m20_command_receipt_stability_boundary.py tests/unit/test_release_artifacts.py` | 0 | 60 corrected M20/M21 reader, fixture, evidence, release, and architecture tests passed in 4.10 seconds. |

Development evidence is retained rather than rewritten as a clean first pass.
The first reader unit run had one failing noncanonical-input test because the
test used Python `False` inside handwritten JSON; replacing it with
`json.dumps()` corrected the fixture. Early Ruff findings were import/export
ordering only. Early Pyright findings identified one generic uniqueness helper
type and one inferred example-report return type; both received explicit types.
The installed example emitted the intended deterministic sanitized report
before its static report annotation was corrected. The final helper correction
routes the attempted frozen-field mutation through `setattr` so Pyright can
type-check the architecture test while runtime immutability remains exercised.

At this stage no complete M21 static/full/docs/distribution/graphics/benchmark
gate, final findings-first review, hosted run, PR, merge, tag, release, package
publication, stability promotion, external adoption, or cross-version
compatibility result is claimed.

## M21 final local validation and review - 2026-08-06

The final reviewed tree remains based on exact synchronized `main` commit
`feed793e94c345fac4b146c358a68264ef6e5f62`. M21 changes no file under
`.github`, `pyproject.toml`, `uv.lock`, or `src/ludoweave/__init__.py`.

| Command | Exit | Result |
| --- | ---: | --- |
| `uv lock --check` | 0 | Approved cache-access rerun resolved the unchanged 46-package lock in 0.76 ms. |
| `uv sync --frozen --all-groups --extra graphics` | 0 | Approved cache-access rerun checked 45 packages. |
| `uv run --frozen ruff format --check .` | 0 | All 211 Python files were already formatted. |
| `uv run --frozen ruff check .` | 0 | No lint findings. |
| `uv run --frozen pyright` | 0 | Zero errors, warnings, or information findings. |
| `uv run --frozen mkdocs build --strict` | 0 | Strict documentation built after correcting one out-of-tree RFC link; only the upstream MkDocs Material/MkDocs 2.0 informational warning remained. |
| `uv run --frozen pytest -q tests/unit/test_receipt_reader.py tests/integration/test_receipt_v1_compatibility_corpus.py tests/integration/test_receipt_reader_example.py tests/integration/test_command_receipt_stability_decision.py tests/architecture/test_m21_receipt_reader_boundary.py tests/architecture/test_m20_command_receipt_stability_boundary.py tests/unit/test_release_artifacts.py tests/unit/test_canonical_json.py tests/unit/test_persistent_command_schema.py tests/unit/test_transactions.py tests/unit/test_receipts.py tests/unit/test_agent_tool_conformance.py tests/integration/test_agent_cli.py tests/architecture/test_api_stability.py tests/architecture/test_import_boundaries.py tests/architecture/test_release_workflow.py` | 0 | 255 expanded reader, compatibility-fixture, canonical transaction/receipt, agent, release, and architecture tests passed in 5.60 seconds. |
| `uv run --frozen pytest -q` | 0 | 1,015 tests passed with one existing Windows symlink-capability skip in 69.87 seconds. |
| `uv build` | 0 | Approved cache-access rerun built `ludoweave-0.1.0a1.tar.gz` and the universal pure-Python wheel. |
| `uv run --frozen python scripts/smoke_wheel.py dist` | 0 | Isolated no-dependency installation passed all inherited smoke plus both M20 `/2` and M21 receipt-reader evidence. |
| `uv run --frozen python scripts/release_artifacts.py dist .tmp/m21-release-final` | 0 | Staged a fresh complete ten-artifact candidate with a 20-file sample bundle. |
| `uv run --frozen python scripts/smoke_release.py .tmp/m21-release-final` | 0 | Checksums, manifest, SPDX SBOM, safe extraction, isolated installation, and all bundled evidence including `receipt_reader.py` passed. |
| `uv run --frozen --extra graphics pytest -q tests/integration/test_wgpu_render.py` | 0 | Ten unchanged real-wgpu integration tests passed in 5.83 seconds. |
| `git diff --check` | 0 | No whitespace errors. |
| `git diff --exit-code main -- .github pyproject.toml uv.lock src/ludoweave/__init__.py` | 0 | Workflow, metadata, lock, package version, and root package exports are unchanged. |
| `git fsck --no-dangling` | 0 | Repository object connectivity is clean with no dangling objects reported. |

The inherited performance evidence was regenerated and validated on dirty
Windows/uv-managed CPython 3.12.13 without changing any target. M1's 3,600-tick
p95 was 36.1046 ms and observed its 12-second target; the 10,000-entity
simulation p95 was 118.5788 ms and missed its 4 ms target. M2's four
target-free p50/p95 observations were 29.9931/32.9317 ms for canonical
100-command round trips, 13.8005/16.0934 ms for atomic apply, 17.7123/19.1362
ms for 1,000-entity snapshot round trips, and 199.1210/223.4890 ms for verified
100-batch replay. M3's 10,000-sprite extraction p95 was 25.6030 ms and real-
wgpu submission p95 was 3.0072 ms; both missed their 3 ms starting targets.
M4's baseline p95 was 1.8156 ms and observed its 16.666667 ms target; stress
4/8 p95 values were 2.9891/4.2398 ms with no targets. Five-repeat M7 base and
graphics profiles validated with two and three workloads. No local miss
authorizes native, WASM, dependency, or scope expansion.

Findings-first review corrected four reader-boundary defects before the final
gate: mapping input now enforces encoded `max_bytes`; canonical limit failures
retain causes and map to the typed oversized code; very long numeric entity
identities cannot escape through CPython integer-conversion limits; and changed
component epochs must advance. Nested allocator/epoch objects now fail exact-
field checks before member decoding. New regressions exercise every correction.
The review also confirmed detached inputs, exact status/hash/tick/diff
relationships, experimental-only focused exports, no world mutation or
provider access, and deterministic sanitized evidence.

Development failures remain factual: initial sandboxed lock, sync, and build
attempts exited 1 before project execution because uv's existing user cache was
inaccessible; approved cache-access reruns passed. The first full strict-docs
run exited 1 for an RFC link outside the MkDocs tree and passed after the link
targeted the in-site API-status page. A read-only PowerShell tree query again
interpreted unquoted revision braces, produced ambiguous-revision output, and
passed when the revisions were quoted.

The final scope/security/package review found no new credential assignment,
ambient time/random/environment/path input, backend/native/WASM leakage,
workflow/dependency/lock/version/root-export change, stale link, or unsupported
pass claim. The wheel has 94 entries, only the existing optional exact graphics
requirements, and no native or WASM file. The frozen fixtures and manifest have
exact checked byte sizes/hashes and explicitly claim only
`single-version-baseline`. No hosted M21 run, PR, merge, tag, GitHub release,
PyPI publication, stability promotion, external adoption, certification, or
cross-version compatibility is claimed at this stage.

## M21 hosted validation - 2026-08-06

Ready PR #30 targets `main` from `[historical branch name redacted]`. GitHub
reports exact base `feed793e94c345fac4b146c358a68264ef6e5f62`, DCO-signed
implementation head `cec339be07318a7c1586bb3405e8f9b1904859f5`, `MERGEABLE`,
and `CLEAN` after checks completed.

GitHub Actions pull-request run `31098563810` executed that implementation
commit from `2026-08-06T11:45:38Z` through `2026-08-06T11:48:05Z` and
concluded `success`. All eight unchanged essential jobs passed:

- `Quality, tests, and distribution` passed lock verification, formatting,
  Ruff, Pyright, strict docs, baseline tests, base profile smoke, sdist/wheel
  build, isolated-wheel smoke, release staging, and complete release smoke;
- compatibility tests passed on Ubuntu CPython 3.13 and 3.14, Windows CPython
  3.14, and macOS CPython 3.14; and
- real graphics, graphics profiling, Clockwork Arena, and Agent World Builder
  passed on Ubuntu software Vulkan, Windows, and macOS.

The workflow file is unchanged, and `gh run list` returned only run
`31098563810` for the M21 branch. Hosted evidence confirms the supported
installed same-version reader behavior and packaging paths. It does not prove
cross-version compatibility, authenticate receipt provenance, establish
external consumer adoption, promote stability, certify a provider, authorize
native acceleration, or create a tag, release, or package publication. PR #30
has not yet been merged at this stage.
