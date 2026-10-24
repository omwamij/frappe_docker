# CI execution cost increment — 2026-10-24

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

| ID | Owner | Acceptance | State |
|---|---|---|---|
| CI-COST-01 | Engineering | Preserve distinct commands, validate workflow/scope/gate contracts; isolate changes | Implemented/local checks passed subject to limits above |
| CI-COST-02 | QA/maintainer | Hosted selected jobs pass; compare docs/UI/shared/lock/workflow paths and runner seconds; inspect required-check names before adopting a renamed gate | Open |
| CI-COST-03 | Human maintainer | Review exact PR revision and authorize merge; record resulting main CI | Open |

## Deferred optimizations

Artifact-transfer reuse, broad test removal and production deployment cancellation are not introduced. Further test profiling/BuildKit cache changes require measured inputs; the separate SQLite/PostgreSQL, restore, financial, fuzz and compatibility gates are not duplicates. Use job result selection rather than skipping required workflows. For new final-gate names, repository maintainers must reconcile required-status configuration; this task does not change branch protection.

Recovery: revert this CI-only commit or close its draft PR. No data migration or customer-site action is required.
