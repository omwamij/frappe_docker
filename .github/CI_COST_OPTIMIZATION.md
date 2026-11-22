# CI execution cost increment - 2026-10-24

## Scope and acceptance

Base revision: `46b2643e4ca23fb8ca26c4441e4f3ddedcb70cce`. Isolated branch `codex/ci-cost-optimization-20261024`; user active checkout preserved. This is a CI-only increment, not a production release.

Parent Stable/Lint PR-only cancellation and bounded runner jobs; reusable build has timeout only to avoid cancelling its parent/sibling versions. All three maintained versions, architecture tests and publish predicates remain. Inactive workflows remain untouched.

## Verification and limits

- `actionlint -shellcheck= -pyflakes=`: passes workflow/action expressions; shellcheck/pyflakes executables were not used.
- `python -m unittest discover -s .github/tests -p test_ci_contract.py`: safety-contract checks pass (SACCO instead uses `node --test tools/ci-workflow.test.mjs`).
- `git diff --check`: passes.
- Separate read-only AGENT REVIEW found a FATCA rename-selection defect and reusable Frappe concurrency collision; both were corrected and rechecked. This is agent review, not independent certification.
- Application/browser/container suites remain unchanged but were not executed locally for this CI-only change. Hosted qualification is pending.
- Hosted CI, actual before/after runner/storage cost and deployed behavior remain unverified until the PR runs. No measured savings claimed. No merges, deployment, live signing, billing changes or test-disablement performed.

## Qualification phases

| ID         | Owner            | Acceptance                                                                                                                                            | State                                                   |
| ---------- | ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| CI-COST-01 | Engineering      | Preserve distinct commands, validate workflow/scope/gate contracts; isolate changes                                                                   | Implemented/local checks passed subject to limits above |
| CI-COST-02 | QA/maintainer    | Hosted selected jobs pass; compare docs/UI/shared/lock/workflow paths and runner seconds; inspect required-check names before adopting a renamed gate | Open                                                    |
| CI-COST-03 | Human maintainer | Review exact PR revision and authorize merge; record resulting main CI                                                                                | Open                                                    |

## Deferred optimizations

Artifact-transfer reuse, broad test removal and production deployment cancellation are not introduced. Further test profiling/BuildKit cache changes require measured inputs; the separate SQLite/PostgreSQL, restore, financial, fuzz and compatibility gates are not duplicates. Use job result selection rather than skipping required workflows. For new final-gate names, repository maintainers must reconcile required-status configuration; this task does not change branch protection.

Recovery: revert this CI-only commit or close its draft PR. No data migration or customer-site action is required.

## Failed image qualification repair

The selected official frappev16.53.0 pyproject requiresPython>=3.14,<3.15 and package.json requiresNode>=24; selected erpnextv16.52.1 requiresPython>=3.14. Updated only v16 inputs to official publishedPython3.14.9-slim-bookworm andNode24.20.0. Earlier major runtime inputs remain unchanged.

S3 backup tests failed because minio/minio is no longer publicly pullable; official Quay pulls returned401 and the archived binary endpoint returned410. Preserve the realS3 backup test by building its isolated fixture from official MinIO release RELEASE.2025-10-15T17-29-55Z, commit9e49d5e7a648f00e26f2246f4dc28e6b07f8c84a. The image is job-local and unpublished, with no host ports; all backup assertions remain. Pinned officialGo1.26.10 compiler, CGOdisabled, revision readback and license included. Modern ROOT_USER/ROOT_PASSWORD env names preserve synthetic fixture credentials. No production image recipe, app source or publication predicate changed.

Four focused fixture/runtime contracts and original CI safety test pass locally; actionlint and pinned formatting pass. Docker unavailable locally, so source compilation, all6 variant builds, actualS3 backup integration and runtime qualification remain pending hosted CI. Source-build overhead replaces unavailable external binaries; no new cost saving is claimed for this repair.
