# Changelog

## [3.3.0] - 2026-02-19

### Fixed

- **Board decisions now persist to files** — Board meetings write `resolution.md` and `session-{timestamp}.json` to the message bus after every deliberation. Decisions survive across sessions instead of disappearing after the conversation ends.

- **Superpowers skills aligned with Conductor paths** — `writing-plans` and `executing-plans` skills now have explicit Conductor Integration sections. When the orchestrator invokes them with `--output-dir`, `--spec`, `--plan` parameters, they write to the correct track directory instead of `docs/plans/`. Standalone usage still works as before.

- **Executing-plans autonomous mode** — When invoked by the Conductor orchestrator, `executing-plans` now runs all tasks continuously without stopping for human feedback between batches of 3. The batch-and-review workflow remains available for standalone use.

- **Context flooding mitigation** — Added "Concise Agent Returns" rule to the orchestrator: all dispatched agents must write detailed output to files and return only a one-line JSON verdict. Added Output Protocol sections to `loop-execution-evaluator`, `loop-executor`, `task-worker`, and `parallel-dispatcher` agents.

- **task-worker can now spawn sub-agents** — Added `Task` tool to task-worker's toolset and a Parallel Decomposition section for complex tasks with 3+ independent sub-components.

- **Context-loader enforcement rules** — Added mandatory size checks (>500KB partial read, >1MB skip entirely), tier limits (stop after Tier 1-3), no loading completed tracks, and a 15-file maximum per context load.

### Added

- **Knowledge layer documentation** — Added `docs/parameter-schema.md` (superpower invocation parameters) and `docs/checkpoint-protocol.md` (how superpowers update metadata.json for state tracking and resumption).

- **Retrospective dispatch at track completion** — Orchestrator now runs a retrospective agent after completing a track, extracting reusable patterns to `conductor/knowledge/patterns.md` and error fixes to `conductor/knowledge/errors.json`.

### Changed

- Version bump to 3.3.0
