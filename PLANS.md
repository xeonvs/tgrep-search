# Execution Plans

## Active Work

### tgrep-search 1.0.0 — initial public skill release

- **Status:** active
- **Release classification:** initial public release
- **Target:** publish an instruction-only, self-contained `tgrep-search` plugin
  for Codex and Claude Code. The same canonical `SKILL.md` remains directly
  installable by OpenCode and other agents that discover standard skill folders.
- **Scope:** platform-neutral canonical skill; generated dual-plugin package;
  public README; deterministic package and privacy validation; Draft review;
  immutable GitHub release; compact release readback.
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
| TS-03 | active | Exact-head self-review, hosted validation and protected merge remain. |
| TS-04 | queued | Publish immutable `v1.0.0` and confirm tag/release assets with one compact readback. |

## Completion

Complete after the immutable public GitHub release `v1.0.0` exists and a
minimal readback confirms the tag, release, and its assets. The separate
`xeonvs-engineering` catalog is created only after this release and references
this package without changing its scope.
