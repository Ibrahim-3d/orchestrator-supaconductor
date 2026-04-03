# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.7.0] - 2026-04-03

### Features

- **Board of Directors fast-path** — Routine tracks now use a single structured Opus call (`collapsedBoardEval`) that evaluates all 5 board perspectives (architecture, product, security, operations, UX) at ~1/10th the cost of the full multi-agent deliberation. Full 5-agent board is reserved for genuinely high-stakes decisions: production deploys, security architecture changes, breaking API changes, and data-loss migrations.
- **Plan revision loop guard** — Added `plan_revision_count` tracking with a configurable limit (default 3, set via `max_plan_revisions` in `conductor/config.json`). Prevents infinite PLAN→EVALUATE_PLAN cycles when a board or evaluator repeatedly rejects a plan. At the limit the track completes with warnings instead of looping forever.
- **Execution state reconciliation on resume** — New `reconcileProgress()` utility reconciles `plan.md` `[x]` checkboxes against `metadata.json` `tasks_completed` before resuming an interrupted execution. Treats plan.md as the source of truth and uses file modification timestamps to skip the check when already in sync. Prevents completed tasks from being re-executed or skipped after a session crash.

### Bug Fixes

- **Atomic file lock for message bus** — `acquire_lock` previously used a non-atomic check-then-write pattern (TOCTOU race). Replaced with `fcntl.flock(LOCK_EX | LOCK_NB)` on a dedicated `.lock_mutex` file (opened in append mode to avoid truncation). Two parallel workers can no longer simultaneously acquire the same lock. `init-bus.py` now creates the mutex file during bus initialization.
- **Bounded knowledge injection** — Knowledge Manager now scores each pattern and error entry by keyword overlap with the track spec, returns only the top-3 highest-scoring matches, and caps total output at 500 tokens. Prevents unbounded context growth as the `conductor/knowledge/` base accumulates across many completed tracks.

### Maintenance

- Remove redundant "Red Flags", "Common Rationalizations", and "Real-World Impact" sections from `systematic-debugging` skill. The procedural guidance in The Iron Law and the Four Phases already covers all cases. (297 → 246 lines)
- Correct the Evaluate-Loop table in README: the Fix step allows up to 5 fix cycles and up to 3 plan revisions (not "max 3 cycles" as previously stated).

## [3.6.0] - 2026-03-27

### Features

- **New `/plan-sprint` command** — Takes a list of features and creates fully planned tracks in parallel. Spawns one agent per track for concurrent spec + plan generation. Analyzes inter-track dependencies and priority ordering.
- **`/new-track` now generates plan.md** — Tracks are created with spec, plan, AND metadata in one step. Calls loop-planner internally so tracks are immediately ready for execution.
- **TDD bite-sized task format in loop-planner** — Plans now include exact file paths, complete code, failing test → implement → verify → commit steps. Inspired by the writing-plans skill.

### Refactoring

- **Unified planning system around conductor tracks** — All superpowers skills (`writing-plans`, `brainstorming`, `subagent-driven-development`, `requesting-code-review`) now save artifacts to `conductor/tracks/{track_id}/` instead of the old `docs/plans/` path. Eliminates the two-system fragmentation.
- **`writing-plans` no longer auto-executes** — Saves plan to track dir and HALTs. Execution is a separate user action via `/implement` or `/go`.

## [3.5.0] - 2026-03-27

### Features

- **New `/close-track` command** — Single command to finalize a track: runs quality gate, updates metadata.json/tracks.md/index.md, commits conductor state, and delegates git branch handling. Supports `--force` flag for abandoned tracks.

### Bug Fixes

- **Prevent `/setup` from auto-executing tracks** — Setup command now has explicit HALT boundary and scope constraint so it stops after scaffolding and planning instead of proceeding to execute tracks

## [3.4.0] - 2026-03-27

### Features

- **Rewrite /setup as full interactive project initialization** — /setup now analyzes the project, generates a PRD, and populates a full development sprint automatically
- **Configurable mode — agentic vs human-in-the-loop** — Users can switch between fully autonomous operation and step-by-step collaboration
- **Fully agentic plugin** — All commands now run autonomously without prompting the user for questions mid-execution
- **Explicit model declarations on all 32 commands** — Opus for planning, Sonnet for execution to optimize token usage and cost
- **Version detection on session start** — Claude now detects the running SupaConductor version and checks for available updates via GitHub

### Bug Fixes

- **Mode-aware executing-plans and finishing-a-development-branch** — These skills now respect the configured agentic/human-in-the-loop mode
- **Add missing name: fields and create 2 missing command wrappers** — Fixed registration gaps found during testing
- **Resolve 6 dead endpoints found during pressure testing** — Eliminated broken references across the plugin

### Documentation

- Rewrite README for non-tech users with clearer onboarding
- Add changelog automation via release-please and GitHub Actions config

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
