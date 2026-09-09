# Execution Plans

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
