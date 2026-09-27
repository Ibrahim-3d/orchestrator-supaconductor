# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.9.0](https://github.com/Ibrahim-3d/orchestrator-supaconductor/compare/v3.8.0...v3.9.0) (2026-09-27)


### Features

* add configurable mode — agentic vs human-in-the-loop ([d01b784](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/d01b784f7386482fec1c658c13d6d42824fba252))
* add explicit model declarations to all 32 commands ([1be4d2c](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/1be4d2c0b5a1a876183becad213a21856a9de73d))
* add multi-agent platform adapters ([#24](https://github.com/Ibrahim-3d/orchestrator-supaconductor/issues/24)) ([ce8a31a](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/ce8a31ade4c2aee11c54f315f1cac7c9d0871c4f))
* bundle superpowers v4.3.0 (MIT) — fully self-contained plugin ([f6fef93](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/f6fef937893df306c48ce98eb863d418f9a49526))
* enforce opus for planning, sonnet for execution — optimize token usage ([cb94862](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/cb948620d87a1d6c982c95d7561805a72cc5705d))
* enhance /setup to analyze project, generate PRD, and populate development sprint ([4e4a681](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/4e4a681f98273b1b35e61d5ad3305797b323fef8))
* initial Conductor Superpowers plugin v3.1.0 ([9cad9a5](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/9cad9a5cf800d8c7a310b9215701f7e7e553adbb))
* make entire plugin fully agentic — never ask user questions ([244240d](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/244240dc75997e9642de412800522fb6ed5d31ea))
* rebrand to supaconductor and standardize tool/command structure ([c37221c](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/c37221c6508622674792e0a4f1e8103b47c0f1ae))
* rewrite /setup as full interactive project initialization ([bfd8bf9](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/bfd8bf975d48c851ff1d3740b7134164965f3dfe))


### Bug Fixes

* add missing name: fields and create 2 missing command wrappers ([6d5a2f3](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/6d5a2f3d6c78cf91d46ef7929e69a023bb244fa9))
* add YAML frontmatter to business-docs-sync skill ([e2e1afb](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/e2e1afbe9e23475a416b555c1c1c137aab71f137))
* add YAML frontmatter to business-docs-sync skill ([d14f966](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/d14f9664a85ab2ebfa1c362ff83e23c108e3a22d))
* address all 5 code review issues ([72941b1](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/72941b1127b324db09089262d173a6d40aac9167))
* address community feedback — board persistence, context flooding, autonomous mode (v3.3.0) ([1d4af1a](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/1d4af1ae14f4ec2f680402be98d2a05f0084ea20))
* align marketplace license metadata with AGPL-3.0 ([2b98179](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/2b9817986be905b1fc446baed2febb00b1419357))
* align plugin license metadata with AGPL-3.0 ([aafcf64](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/aafcf6405f7e141ded023f8c2957f5482baebc3f))
* align public install release and license story ([df1c682](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/df1c682a40663f0c321002333d31e801f4ee74c9))
* bootstrap missing v3.7.0 release history ([653cfd9](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/653cfd9f5bd239f697d5668f63c4380f4f52a57c))
* bootstrap missing v3.7.0 release history ([91b3e81](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/91b3e815fc93a23e4f0ab44748068c97f943a293))
* cache session update checks portably ([08e73fc](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/08e73fc9c6adea799041fdb2f769cc76da900fe1))
* create bootstrap release tag without git identity ([f803d58](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/f803d58f6f80cb0a8fff437782da1c9c4f11f5ee))
* declare all board-meeting runtime tools ([e9b4302](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/e9b4302f8af531d303084db1f97d4f3fd5462af4))
* flatten command structure and fix slash command registration ([0399626](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/03996260a4c44053720f6ba7cfaa59c30cf0079b))
* implement all agentic workflow review improvements ([71c1818](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/71c1818b7a4fa99b3658707a52bb5642ec5a971c))
* make executing-plans and finishing-a-development-branch mode-aware ([87e3ef5](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/87e3ef52be17ac4d1ef8ad14370d94d9051f40c6))
* make release announcements run from release workflow ([95ef345](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/95ef345e2b4f6e8a52101ea30ba2219c777ea278))
* make SupaConductor public repo release-ready ([b8d2f3f](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/b8d2f3f377ef0d8b856d7f6625666ee15ca8fb84))
* make v3.7.0 release bootstrap non-interactive ([090119d](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/090119d1cec9987f53f3a0d7bec920c214559c19))
* marketplace.json author field must be object, not string ([54cef1f](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/54cef1f86d545cdb563bf9d6dd9b315c613c5420))
* move UI/UX audit report template out of commands/ ([b8fdde3](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/b8fdde3d27b3d9e471677f1bd1039c8f7687be25))
* move UI/UX audit report template out of commands/ to docs/ ([c94e52f](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/c94e52f34fe13d4d58bc1c8212ab2d2da0414102))
* prevent setup command from auto-executing tracks after planning ([3739dcf](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/3739dcff98c3d0b9aaf225a7c9727952d1449468))
* publish releases without Actions PR permission ([#26](https://github.com/Ibrahim-3d/orchestrator-supaconductor/issues/26)) ([76c9b10](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/76c9b10023238a6c0f58d4ebffc4e2ebfdf6c5e5))
* remove reddit replies from repo, update outdated README diagrams ([7517221](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/7517221a1b6d718ead6ae5dadceae5cabe4a4a9a))
* remove stale marketplace update instructions ([55bb937](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/55bb937b644644831195420d23e2e846d5e5f00e))
* remove unrecognized bundledDependencies from plugin.json ([3e9d8db](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/3e9d8dbe29915257a99438637a417049ddf0e02b))
* rename marketplace to avoid recursive cache on Windows ([8629d17](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/8629d17c5d4fb13ae6dbe5b2b94ffd37ce6694f6))
* resolve 6 dead endpoints found during pressure testing ([1e44dbb](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/1e44dbba357237d5e8fd37090fe23c10117efcb6))
* resolve PR [#12](https://github.com/Ibrahim-3d/orchestrator-supaconductor/issues/12) and [#15](https://github.com/Ibrahim-3d/orchestrator-supaconductor/issues/15) correctly ([14fbbc5](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/14fbbc58916ce87c73f30111e018d058f9da190e))
* restructure commands to flat format for proper Claude Code plugin standard ([4058a43](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/4058a435e67370821a0acd5c88a887e09484d4df))
* use qualified marketplace update instructions ([90443ff](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/90443ffc6ad7d94c882676ce70d8d861b4e049ef))
* use simple release strategy for non-node plugin ([8a3f8e9](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/8a3f8e9ab58958da9a6cde01973e31ab11c4695e))


### Documentation

* add contributor workflow ([b7cd331](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/b7cd331cf859e446d6ae79047af3fbdd9b1ea202))
* add FAQ section covering token usage, tool compatibility, and cost ([47f6dce](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/47f6dce5fbe057873968b6f29dbe40404a176043))
* add marketplace install option, fix command names to /conductor:subcommand format ([a983683](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/a983683808dfc698cd665b8c272a60c32ba5c24e))
* add README, LICENSE, and .gitignore for public release ([0fb35bf](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/0fb35bf396f313345a36d6b77cc0bdf999e002a7))
* add security reporting policy ([5f090b1](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/5f090b1b96a672519734361fe4eaeb41fca20431))
* clean up reddit replies for easy copy-paste ([6525d87](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/6525d877c43f641d40bf86e6154b4e073d54caf8))
* curate v3.7.1 release notes ([bf834a9](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/bf834a953815e62cbc7b8f9184ec44543bde667c))
* define support routes ([f3dd4ec](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/f3dd4ec03ae0ec118c1b8f13c499af3d07257275))
* publish project roadmap ([875d027](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/875d0277fdab7265c40ede10087be49ad6605ca7))
* redesign README with generated diagrams and visual architecture ([26d88c9](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/26d88c9fc47d6faf8e568d09049c4c4dda71bd69))
* rewrite README for non-tech users, add changelog automation and GitHub config ([bba7d45](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/bba7d45eb3c2357570a9cfe8b6981a9a7fbddc9a))
* rewrite reddit replies — simpler, first-time responses ([7b6c9ee](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/7b6c9eecf8b854ae43d28f688dbe5ce08f00cddb))
* update install command with new marketplace name ([0d4a6c8](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/0d4a6c80ddf5661a878fbbb3dcd6aad5e7e3aa72))


### Maintenance

* add pull request template ([f7af47a](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/f7af47aca37358acdde98510bc8605617b9f6e96))
* add structured bug report form ([cf43465](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/cf43465cb59d54c3571dfff644a7844f94c6fff1))
* bump to v3.7.0, update README/CHANGELOG, add release automation ([8909816](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/8909816d3181bb84f65f0214ae89ab9a432deb24))
* **master:** release 3.7.1 ([3bdea29](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/3bdea29e78c54681b13bbf1d19edfe358df9c70c))
* **master:** release 3.8.0 ([16b06f8](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/16b06f81b6edc74f5c2dc8013b3d3b76d147c72e))
* **master:** release 3.8.0 ([#25](https://github.com/Ibrahim-3d/orchestrator-supaconductor/issues/25)) ([ccca566](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/ccca5660761e282354c38e20756a8c39094fb2c8))
* release v3.7.1 ([1aa382b](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/1aa382b54cab411c1379967a73380e53d4af85ab))
* remove one-time release bootstrap ([778ea1c](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/778ea1c3fb9c725f2ed3776919886d1b798da825))
* remove one-time release bootstrap ([82d7d47](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/82d7d47aafe50f614067a65b6e0ec8d0189c26ed))
* remove unreachable duplicate release announcement workflow ([8fe28c0](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/8fe28c0ee13329fe5063a48faf300e24ec810237))
* rename to conductor-orchestrator-superpowers ([82fa663](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/82fa663716a44ae641f7e23f86a8e88ee0a0cf8e))
* route support and ideas to discussions ([5bd3d4b](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/5bd3d4b6130b7c0abe188203baf0ef03d8a2af5e))


### Tests

* add lightweight repository quality CI ([4ebafda](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/4ebafda52e74718a0332cd3608c8e6e03b6f5347))
* add repository consistency validator ([8aaefab](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/8aaefab8692cda1d0db0e5123f2f208169d63552))

## [3.8.0](https://github.com/Ibrahim-3d/orchestrator-supaconductor/compare/v3.7.1...v3.8.0) (2026-09-27)


### Features

* add multi-agent platform adapters ([#24](https://github.com/Ibrahim-3d/orchestrator-supaconductor/issues/24)) ([ce8a31a](https://github.com/Ibrahim-3d/orchestrator-supaconductor/commit/ce8a31ade4c2aee11c54f315f1cac7c9d0871c4f))

## [3.7.1](https://github.com/Ibrahim-3d/orchestrator-supaconductor/compare/v3.7.0...v3.7.1) - 2026-09-27

### Public release & installation

- **Restored the GitHub release story** — established the real v3.7.0 baseline so tags, Releases, update checks, and future release automation have a valid starting point.
- **Corrected Claude Code marketplace installation and update commands** — README and session update guidance now use the current marketplace-qualified workflow.
- **Aligned licensing** — README, plugin metadata, marketplace metadata, and the repository license now consistently report AGPL-3.0.

### Bug Fixes

- **Board meeting runtime tools** — declare both `run_shell_command` and `Task`, matching the tools the agent actually uses.
- **Session update checks** — cache successful GitHub release checks for 24 hours, respect `XDG_CACHE_HOME`, and remove the invalid `find -quiet` path that prevented caching.
- **Business docs skill discovery** — add the missing skill frontmatter so `business-docs-sync` can be discovered correctly.
- **UI audit template placement** — move the non-invocable report template out of the command discovery surface.

### Repository experience

- Added a public roadmap plus contribution, support, and security guidance.
- Added a structured bug-report form and clearer Issues vs Discussions routing.
- Added a pull-request template and repository quality CI for JSON, version/license consistency, frontmatter, and Bash syntax.
- Repaired Release Please for this non-Node Claude Code plugin and integrated release announcements into the release workflow.

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
