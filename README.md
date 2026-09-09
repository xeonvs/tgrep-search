# tgrep Search Skill

A public, instruction-only skill for efficient and safe local source-tree search
with [microsoft/tgrep](https://github.com/microsoft/tgrep). It helps an agent
choose an inexpensive one-off scan, a bounded local index, a managed search
server, or an exact current-filesystem scan.

The package contains no `tgrep` binary, automatic installer, hook, MCP server,
telemetry, local index, credentials, or personal data. It does not alter a
repository unless an agent is separately authorized to create an ignored local
index.

## Install

After the initial public release, use the shared
[`xeonvs-engineering`](https://github.com/xeonvs/xeonvs-engineering) catalog:

```bash
# Codex
codex plugin marketplace add xeonvs/xeonvs-engineering
codex plugin add tgrep-search@xeonvs-engineering

# Claude Code
claude plugin marketplace add xeonvs/xeonvs-engineering
claude plugin install tgrep-search@xeonvs-engineering
```

Claude Code invokes the installed skill as `/tgrep-search:tgrep-search`.
OpenCode and other agents that support standard skill folders can use the
canonical `skill/tgrep-search/` directory in a native `.opencode/skills/`,
`.agents/skills/`, or `.claude/skills/` location. This project does not claim a
separate OpenCode marketplace.

## Maintainers

- `skill/tgrep-search/` is the canonical source.
- `plugins/tgrep-search/` is the self-contained marketplace package; its skill
  bytes must equal the canonical source.
- `scripts/build_plugin.py --check` and
  `scripts/validate_public_package.py` are offline release gates.
