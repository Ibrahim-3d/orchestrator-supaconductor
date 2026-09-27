# Platform Support

SupaConductor keeps one canonical source of truth in `skills/`, `commands/`, and `agents/`. Platform packages are generated from those sources so support does not fork into manually maintained copies.

## Compatibility matrix

| Host | Integration | Commands | Skills | Specialized agents | Notes |
|---|---|---:|---:|---:|---|
| Claude Code | Native Claude plugin | Native slash commands | Native | Native | Existing reference implementation |
| OpenAI Codex / ChatGPT desktop | Agent Plugins package | Generated command-skills | Native Agent Skills | Orchestration via skills / host agents | Root `plugin.json` follows Agent Plugins; release ZIP adds command aliases |
| Cursor | Native Cursor plugin package | Native commands | Native | Native custom agents | Generated package normalizes Claude-specific frontmatter |
| Google Antigravity | Native Antigravity plugin package | Generated command-skills | Native | Native custom subagents | Uses Antigravity's plugin schema and subagent tool names |
| Windsurf / Cascade | Workspace package | Native slash workflows | Native Agent Skills | Inline/host delegation fallback | Every command becomes a short workflow backed by a generated skill |
| GitHub Copilot | Repository customization package | Prompt files (`/name`) | Native Agent Skills | Native custom agents | VS Code/IDE agent mode, Copilot CLI, and supported cloud-agent surfaces |

The hosts do not expose identical APIs. The adapter targets the strongest native primitive each platform actually supports rather than claiming false one-to-one API parity.

## Build every adapter

```bash
python3 scripts/build-platform-adapters.py
```

Generated packages:

```text
dist/platforms/
├── codex/orchestrator-supaconductor/
├── cursor/orchestrator-supaconductor/
├── antigravity/orchestrator-supaconductor/
├── windsurf/orchestrator-supaconductor/
└── copilot/orchestrator-supaconductor/
```

CI runs the same generator with `--check`, so a new command or agent cannot silently disappear from an adapter.

## Installation

### Claude Code

```text
/plugin marketplace add Ibrahim-3d/orchestrator-supaconductor
/plugin install orchestrator-supaconductor@ibrahim-plugins
```

### Codex

The repository now has a root Agent Plugins manifest (`plugin.json`) plus a `.codex-plugin/plugin.json` compatibility overlay. For full command aliases, build/download the Codex adapter and add it to a Codex personal or repository plugin marketplace.

### Cursor

Build/download the Cursor adapter and copy its `orchestrator-supaconductor` directory into:

```text
~/.cursor/plugins/local/orchestrator-supaconductor
```

Reload Cursor. The generated Cursor manifest registers normalized skills, agents, and commands.

### Antigravity

Workspace:

```text
<project>/.agents/plugins/orchestrator-supaconductor/
```

Global:

```text
~/.gemini/config/plugins/orchestrator-supaconductor/
```

The generated package contains Antigravity's manifest, Agent Skills, command-skills, and converted custom subagents.

### Windsurf

Merge the generated adapter's `.windsurf/` directory into the target project. Commands become slash workflows such as `/go`, `/status`, and `/board-review`; each is backed by the complete generated command-skill.

### GitHub Copilot

Merge the generated adapter's `.github/` directory into the target repository:

```text
.github/
├── skills/
├── agents/
└── prompts/
```

Prompt files are slash-invoked in supported IDEs, while Agent Skills and custom agents are available across the Copilot surfaces that support them.

## Release artifacts

Published releases build and attach:

- `supaconductor-codex.zip`
- `supaconductor-cursor.zip`
- `supaconductor-antigravity.zip`
- `supaconductor-windsurf.zip`
- `supaconductor-copilot.zip`

Do not hand-edit generated output. Change the canonical skill, command, or agent and regenerate.
