# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.3.1] - 2026-03-12

### Features

- Rebrand to SupaConductor and standardize tool/command structure

### Bug Fixes

- Flatten command structure and fix slash command registration
- Rename marketplace to avoid recursive cache on Windows
- Remove reddit replies from repo, update outdated README diagrams

### Documentation

- Update install command with new marketplace name

## [3.3.0] - 2026-02-19

### Bug Fixes

- **Board decisions now persist to files** — Board meetings write `resolution.md` and `session-{timestamp}.json` to the message bus after every deliberation. Decisions survive across sessions instead of disappearing after the conversation ends.
- **Superpowers skills aligned with Conductor paths** — `writing-plans` and `executing-plans` skills now have explicit Conductor Integration sections. When the orchestrator invokes them with `--output-dir`, `--spec`, `--plan` parameters, they write to the correct track directory instead of `docs/plans/`. Standalone usage still works as before.
- **Executing-plans autonomous mode** — When invoked by the Conductor orchestrator, `executing-plans` now runs all tasks continuously without stopping for human feedback between batches of 3. The batch-and-review workflow remains available for standalone use.
- **Context flooding mitigation** — Added "Concise Agent Returns" rule to the orchestrator: all dispatched agents must write detailed output to files and return only a one-line JSON verdict. Added Output Protocol sections to `loop-execution-evaluator`, `loop-executor`, `task-worker`, and `parallel-dispatcher` agents.
- **task-worker can now spawn sub-agents** — Added `Task` tool to task-worker's toolset and a Parallel Decomposition section for complex tasks with 3+ independent sub-components.
- **Context-loader enforcement rules** — Added mandatory size checks (>500KB partial read, >1MB skip entirely), tier limits (stop after Tier 1-3), no loading completed tracks, and a 15-file maximum per context load.
- marketplace.json author field must be object, not string
- Remove unrecognized bundledDependencies from plugin.json
- Restructure commands to flat format for proper Claude Code plugin standard

### Features

- **Knowledge layer documentation** — Added `docs/parameter-schema.md` (superpower invocation parameters) and `docs/checkpoint-protocol.md` (how superpowers update metadata.json for state tracking and resumption).
- **Retrospective dispatch at track completion** — Orchestrator now runs a retrospective agent after completing a track, extracting reusable patterns to `conductor/knowledge/patterns.md` and error fixes to `conductor/knowledge/errors.json`.

### Documentation

- Redesign README with generated diagrams and visual architecture
- Add FAQ section covering token usage, tool compatibility, and cost
- Add marketplace install option, fix command names to /conductor:subcommand format

## [3.1.0] - 2026-02-17

### Features

- Initial Conductor Superpowers plugin
- Bundle superpowers v4.3.0 (MIT) — fully self-contained plugin

### Documentation

- Add README, LICENSE, and .gitignore for public release
