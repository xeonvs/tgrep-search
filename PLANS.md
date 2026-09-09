# Execution Plans

## Active Work

### tgrep-search 1.0.1 — initial public skill release and publication-workflow correction

- **Status:** active
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
| TS-04 | active | Correct the invalid immutable release-action SHA through a protected PR, publish immutable `v1.0.1`, and confirm tag/release assets with one compact readback. |

## Completion

Complete after the immutable public GitHub release `v1.0.1` exists and a
minimal readback confirms the tag, release, and its assets. `v1.0.0` remains an
unpublished tag whose release job failed before asset creation; it is not moved or
reused. The separate
`xeonvs-engineering` catalog is created only after this release and references
this package without changing its scope.
