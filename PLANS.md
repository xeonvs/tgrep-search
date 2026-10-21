# Execution Plans

plan_schema_version: 2

Use this file for active, blocked, ready-for-closure, or recently completed
execution work. Preserve the repository's completed release record below.

## Recently Completed

- [x] 2026-09-13: Completed Search Without Mandatory Setup.
- [x] 2026-09-12: Completed tgrep Search 1.0.2 Node 24 Release Actions.
- [x] 2026-09-12: Completed tgrep Search 1.0.2 Plugin Brand Icon.

## Active Plan: Integrate tgrep 1.2.4 And Release tgrep-search 1.1.0

Status: active
Owner: root
Last Updated: 2026-10-21

### Goal

Publish accurate tgrep 1.2.4 guidance as tgrep-search 1.1.0, import its unchanged released bundle into xeonvs-engineering 1.0.12, and verify native local plugin and Homebrew binary updates.

### Plan Origin

plan_mode_approved

### Requested Scope

Correct ordinary search/index/server guidance; add an optional managed-v2 reference; validate behavior in disposable fixtures; release source and catalog; update local Codex, Claude Code, and tgrep installations.

### Requirement Traceability

| Requirement | Complete outcome | Source | Work queue | Acceptance or validation | Status |
| --- | --- | --- | --- | --- | --- |
| REQ-001 | Accurate ordinary search, freshness, hidden coverage, traversal, filters, errors and storage guidance | approved plan | WQ-01, WQ-02 | CLI parity and scenario checks against 1.2.4 | done |
| REQ-002 | Optional concise managed-v2 lifecycle reference, without default activation or copied protocol | approved shared-mode decision | WQ-01, WQ-02 | source review and two-worktree smoke | done |
| REQ-003 | Validated immutable tgrep-search 1.1.0 release | approved full-cycle decision | WQ-03 | package parity, unit/skill/privacy/security checks, reviewed PR and release asset readback | pending |
| REQ-004 | Unmodified source import and marketplace 1.0.12 release; other plugin unchanged | approved full-cycle decision | WQ-04 | native sync, provenance/hash, catalog tests and release readback | pending |
| REQ-005 | Homebrew tgrep 1.2.4 and enabled native local tgrep-search 1.1.0 installations | approved full-cycle decision | WQ-02, WQ-05 | binary version, active paths, enabled state and released-byte parity | pending |
| REQ-006 | Reviewed complete outcome and checked lifecycle closure in both repositories | approved plan | WQ-06 | aggregate review, reconciled plans, checked compact closure | pending |
| REQ-007 | Current stable pinned GitHub Actions and applicable project dependencies | user addition 2026-10-21 | WQ-07 | official release/pin verification, package tests and CI | done |

### Explicit Non-Goals

- Change engineering-workflow, install upstream MCP/hooks, ship binaries/indexes, build an installer or orchestration layer, enable shared mode by default, rename existing indexes, or create ongoing monitoring.

### Constraints

- Preserve historical plan records, existing tags, icons, invocation policy, and unrelated installations/configuration.
- Canonical source is skill/tgrep-search; generated plugin skill bytes must match it exactly.
- Publication, merge, release and requested local updates are explicitly authorized by the approved implementation request. Privacy/security gates remain mandatory before every push.
- Root owns shared state, versions, integration and acceptance. Keep transient logs in protected task-owned temporary storage; do not publish machine paths or raw secrets.

### Inputs And Sources

- User-approved implementation plan and answers: full release/local-update cycle; optional short managed-v2 route.
- https://github.com/microsoft/tgrep/releases/tag/v1.2.4
- https://github.com/microsoft/tgrep/compare/v1.2.3...v1.2.4
- https://github.com/microsoft/tgrep/blob/v1.2.4/README.md
- https://github.com/microsoft/tgrep/blob/v1.2.4/AGENTS.md
- https://github.com/microsoft/tgrep/blob/v1.2.4/SHARED_WORKTREE_INDEXES.md
- https://github.com/xeonvs/tgrep-search and https://github.com/xeonvs/xeonvs-engineering

### User Decisions And Answers

- Full cycle includes binary, both native clients, source release and marketplace release.
- Shared worktree receives a short opt-in route/reference, not an automatic integration.
- 2026-10-21 addition: update Actions and applicable dependencies in both released repositories; do not modify the unchanged engineering-workflow bundle.

### Completed Baseline State

- [x] WQ-00 — Clean source and catalog checkouts inspected; current source tag 1.0.3, catalog 1.0.11, both local clients enabled at 1.0.3; local tgrep 1.2.3. Upstream stable is 1.2.4; Homebrew upstream formula already points to 1.2.4. Planned versions unoccupied.

### Current Work Queue

- [x] WQ-07 — Audit/update Actions and applicable dependencies for REQ-007 before source publication. `done`
- [x] WQ-01 — Implement REQ-001, REQ-002 and update all active version owners to 1.1.0. `done`
- [x] WQ-02 — Upgrade Homebrew tgrep; run ordinary behavior matrix and bounded shared smoke for REQ-001, REQ-002, REQ-005. `done`
- [ ] WQ-03 — Review, validate, publish source release and verify assets for REQ-003. `in_progress`
- [ ] WQ-04 — Native sync, review exact import, validate and release catalog for REQ-004. `pending`
- [ ] WQ-05 — Update native local plugins and verify active installation parity for REQ-005. `pending`
- [ ] WQ-06 — Aggregate review, requirement reconciliation and canonical closure for REQ-006. `pending`

### Locked Decisions

- Use tgrep-search 1.1.0 for added optional managed guidance and catalog 1.0.12; recheck refs before publishing, never move a tag.
- Keep rg/no-setup default for small searches. Exact disk scans still respect eligibility/ignore/size policies and are not atomic snapshots.
- Reuse explicitly selected .tgrep-index storage; upstream default is .tgrep. No automatic migration.
- Keep binary managed by Homebrew; update marketplace-managed plugins natively, never write their caches directly.

### Verification

- WQ-01/02: ordinary scans/index/server including initial fallback, hidden/ignored files, stale edits, explicit files, filters, JSON and exit 0/1/2; compare rg and no-index where semantics align.
- WQ-02: two disposable worktrees, managed policy/ownership/attach/query/detach and supervised process cleanup; no background process survives.
- WQ-03: unittest discovery, build_plugin --check, validate_public_package, skill quick validator, semantic review, public-tree scanner, redacted Gitleaks tree/all reachable refs, CI and checksummed release assets.
- WQ-04: unittest discovery, validate_catalog, sync_upstreams --verify-recorded, exact bundle/provenance and unchanged engineering-workflow; security gates, CI and release assets.
- WQ-05/06: native list/status, installed-byte comparison, final aggregate diff review, plan fidelity and lifecycle closure.

### Latest Validation Results

- 2026-10-21: Homebrew upgraded tgrep to 1.2.4; prior Cellar/cache version was removed by Homebrew's normal cleanup and remains reinstallable through Homebrew.
- 2026-10-21: six offline package tests, build parity, public-package validator, skill quick validator, Claude plugin validation and whole-public-tree privacy scan passed. PyYAML was initially missing from system Python; the skill validator passed in a task-owned temporary virtual environment with PyYAML 6.0.3, without changing project dependencies.
- 2026-10-21: independent read-only forward evaluation found no reportable issues in one-off, repeated/hidden/post-edit, single-server/traversal and managed-worktree scenarios. Documentation link check found no errors; existing HTML logo syntax is not parsed by that checker.
- 2026-10-21: 12/12 package and CLI tests pass on tgrep 1.2.4 / Python 3.15.0, including actual server transport, partial-result exit 2 and Unix backslash names. APFS rejects invalid UTF-8 filenames at creation; that subcase runs only on filesystems supporting it. Missing-binary mode cleanly skips six optional CLI cases.
- 2026-10-21: official v1.2.4 qualification managed_smoke passed on the installed binary: two worktrees, owner proof, generation reuse, scan parity, migration/replay, detach and cleanup; no owned processes/fixtures survive. Evidence source is microsoft/tgrep commit 0be7a76e8ad6636b64cb2cf17173badecf8a8176, scripts/qualification/qualify.py managed_smoke (364-537); inspected before execution and root-reviewed.
- 2026-10-21: official stable Action refs verified: checkout v7.0.1 and action-gh-release v3.0.3 already current; setup-python updated to v7.0.0 (5fda3b95a4ea91299a34e894583c3862153e4b97), Node 24. CI Python upgraded to stable 3.15, available in actions/python-versions; no third-party runtime/project Python dependencies exist. Both repositories' updated tests pass.
- Root corrected server test coverage before acceptance; privacy scan initially flagged synthetic marker variable names, which were renamed without changing or weakening the scanner. Final public-tree scan passes. No release published yet.

### Risks And Recovery

- Stale indexes/readiness can yield incomplete absence claims: document exact-scan boundary and test changed files.
- Managed lifecycle is complex: keep opt-in, use official policy/protocol, bounded fixture processes with finally cleanup; stop on unsupported contract rather than invent ownership.
- Release/sync/native failure: inspect terminal state before retry, retain prior installation and immutable release; never force tags or bypass failed gates.
- Historical PLANS sections are retained verbatim outside this active plan; lifecycle closure must preserve them.

### Resume Point

- WQ-03: review final source slice, run final pre-push gates, create/merge the validated PR and publish immutable v1.1.0.

### Plan Fidelity Check

- [x] Every agreed outcome has a requirement ID.
- [x] Every source URL is preserved.
- [x] Every user answer and locked decision is preserved.
- [x] No requirement was silently narrowed or removed.
- [x] The queue covers every requirement ID.
- [x] Validation covers every acceptance criterion.
- [x] Non-goals do not contradict requested scope.
- [x] The resume point names the first unfinished queue item.
- [x] This plan is not a compressed rewrite of a more detailed approved plan.

### Reconciliation Check

- [x] Baseline state and authorized scope agree with current observations.
- [ ] Final plan, statuses, validation, working trees and related catalog state agree.
- [ ] Completed sections contain no stale active work.

### Closure Gate

- [ ] Every in-scope requirement and queue item is terminal.
- [ ] Applicable validation is current for final content.
- [ ] Review feedback, omissions, backlog and indexes are reconciled.
- [ ] Resume Point contains no future in-scope work.
- [ ] Compact disposition preserves existing historical records atomically.

### Post-Close Delivery

- Source release, catalog release and requested local updates remain WQ-03 through WQ-05 until actually verified. Final closure-only commit/PR delivery may follow canonical closure without changing runtime artifacts.

### Handoff Notes

- No current blocker. Follow the first unfinished queue item; do not reconstruct the execution transcript.

## Active Work

### tgrep-search 1.0.1 — initial public skill release and publication-workflow correction

- **Status:** completed
- **Release classification:** initial public release
- **Target:** publish an instruction-only, self-contained `tgrep-search` plugin
  for Codex and Claude Code. The same canonical `SKILL.md` remains directly
  installable by OpenCode and other agents that discover standard skill folders.
- **Scope:** platform-neutral canonical skill; generated dual-plugin package;
  public README; deterministic package and privacy validation; Draft review;
  immutable GitHub release; compact release readback. The prior `v1.0.0` tag is retained as an unpublished failed attempt; its workflow could not resolve a pinned third-party action, so it is never retargeted or represented as a release.
- **Non-goals:** bundle a `tgrep` binary; automatically install software; add a
  wrapper, hook, MCP server, telemetry, credentials, user-machine configuration,
  or marketplace catalog content.
- **Security boundary:** package only public instructions and metadata. It must
  contain no local paths, secrets, personal data, indexes, generated caches or
  private repository references.

| ID | State | Work and acceptance evidence |
| --- | --- | --- |
| TS-01 | done | Canonical skill and byte-identical Codex/Claude bundle are present. |
| TS-02 | done | Offline package, manifest and public-content validation passes. |
| TS-03 | done | Exact-head self-review, hosted validation and protected merge completed in PR #1. |
| TS-04 | done | Protected PR #2 corrected the action pin; signed `v1.0.1` published successfully with archive and `SHA256SUMS` readback. `v1.0.0` remains an unpublished failed tag. |

## Completion

**Completed 2026-09-09.** Protected PR #2 corrected the release action pin. The
immutable public GitHub release [`v1.0.1`](https://github.com/xeonvs/tgrep-search/releases/tag/v1.0.1)
was published from commit `e316614144d14efb7bdf63f49ff820a12bdedc84`; its
archive and `SHA256SUMS` were read back. The earlier `v1.0.0` tag remains an
unpublished failed attempt and was neither moved nor reused.

The separate `xeonvs-engineering` catalog may now reference the released package
without changing the skill scope.
