# Conductor Superpowers Plugin v3.2

Parallel multi-agent orchestration with Evaluate-Loop, Board of Directors, and bundled Superpowers skills for Claude Code.

## What is Conductor?

Conductor is a structured workflow system that organizes development work into **tracks** and **phases**, with detailed specifications, step-by-step implementation plans, and automated quality gates. It provides:

- **Evaluate-Loop** — Plan → Evaluate Plan → Execute → Evaluate Execution → Fix cycle
- **16 Specialized Agents** — Orchestrator, planners, executors, evaluators, fixers, code reviewer
- **Board of Directors** — 5-member expert deliberation system (CA, CPO, CSO, COO, CXO)
- **Parallel Execution** — DAG-based task parallelization with worker agents
- **Lead Engineer System** — Architecture, Product, Tech, QA leads for autonomous decisions
- **Bundled Superpowers** — Battle-tested skills for planning, execution, debugging, TDD, code review

## Quick Start

### 1. Install the Plugin

The plugin should be installed at `~/.claude/plugins/conductor-superpowers/`.

### 2. Initialize a Project

Run the setup script to create the `conductor/` directory in your project:

```bash
bash ~/.claude/plugins/conductor-superpowers/scripts/setup.sh
```

Or use the `/conductor setup` command in Claude Code.

### 3. Start Working

The simplest way to use Conductor:

```bash
/go <your goal>
```

Examples:
```bash
/go Add Stripe payment integration
/go Fix the login bug where users get logged out
/go Build a dashboard with analytics
/go Refactor the auth system to use JWT
```

### 4. What Happens

1. System analyzes your goal and checks for matching tracks
2. Creates a new track if needed (spec + plan with DAG)
3. Evaluates the plan (with Board of Directors for major tracks)
4. Executes tasks in parallel where possible
5. Evaluates results and fixes issues automatically
6. Reports completion

## Commands

### Conductor Commands

| Command | Description |
|---------|-------------|
| `/go <goal>` | Main entry point — state your goal, Conductor handles the rest |
| `/conductor status` | View current progress across all tracks |
| `/conductor new-track` | Create a new development track |
| `/conductor implement` | Run the automated Evaluate-Loop |
| `/conductor setup` | Initialize Conductor in a new project |
| `/phase-review` | Run post-execution quality gate |
| `/board-meeting [proposal]` | Full 4-phase board deliberation |
| `/board-review [proposal]` | Quick board assessment |
| `/cto-advisor` | CTO-level technical review |
| `/ceo`, `/cmo`, `/cto`, `/ux-designer` | Executive advisor consultations |

### Superpowers Commands (Bundled)

| Command | Description |
|---------|-------------|
| `/write-plan` | Create an implementation plan using superpowers patterns |
| `/execute-plan` | Execute a plan using superpowers patterns |
| `/brainstorm` | Brainstorm approaches to a problem |

## Track Structure

Each track lives in `conductor/tracks/[track-name]/`:

```
track-name/
├── spec.md          # Product spec and requirements
├── plan.md          # Implementation plan with tasks + DAG
├── metadata.json    # Track configuration, state machine, board sessions
└── ...              # Additional track artifacts
```

## Architecture

### Evaluate-Loop

```
PLAN → EVALUATE PLAN → EXECUTE → EVALUATE EXECUTION
                                       │
                                  PASS → BUSINESS DOC SYNC → COMPLETE
                                  FAIL → FIX → re-EXECUTE → re-EVALUATE (loop)
```

### Agent System

- **Orchestrator** — Detects track state, dispatches agents, manages loop
- **Loop Agents** — Planner, Executor, Fixer (legacy or Superpowers-enhanced)
- **Evaluators** — Plan evaluator, Execution evaluator (dispatches to specialized: UI/UX, Code Quality, Integration, Business Logic)
- **Board** — 5 directors with ASSESS → DISCUSS → VOTE → RESOLVE protocol
- **Leads** — Architecture, Product, Tech, QA for autonomous decisions
- **Workers** — Ephemeral parallel task executors
- **Code Reviewer** — Superpowers code review agent

### Bundled Superpowers Skills

This plugin bundles [obra/superpowers](https://github.com/obra/superpowers) v4.3.0 (MIT License). These skills are used by the Conductor orchestrator for enhanced planning, execution, and debugging:

| Skill | Purpose |
|-------|---------|
| `writing-plans` | Superior plan creation with DAG structure |
| `executing-plans` | Plan execution with built-in TDD and debugging |
| `systematic-debugging` | Structured root-cause analysis and fixes |
| `brainstorming` | Creative problem-solving and decision-making |
| `test-driven-development` | TDD workflow patterns |
| `subagent-driven-development` | Multi-agent task execution |
| `dispatching-parallel-agents` | Parallel agent coordination |
| `verification-before-completion` | Pre-completion quality checks |
| `requesting-code-review` | Code review workflow |
| `receiving-code-review` | Handling review feedback |
| `using-git-worktrees` | Git worktree workflows |
| `finishing-a-development-branch` | Branch completion workflow |
| `writing-skills` | Creating new Claude Code skills |
| `using-superpowers` | Skills system introduction |

New tracks use Superpowers by default. Legacy tracks fall back to the built-in loop agents.

## Documentation

- [Evaluate-Loop Workflow](workflow.md) — Full process documentation
- [Authority Matrix](authority-matrix.md) — Lead Engineer decision boundaries

## Project-Specific Skills

Conductor is designed to work alongside project-specific skills. Keep project-specific knowledge in your project's `.claude/skills/` directory:

- Product rules, personas, and domain knowledge
- Framework-specific patterns (e.g., Next.js, Rails)
- Design system tokens and conventions
- API integration specifics

The generic orchestration (this plugin) handles the workflow; your project skills handle the domain knowledge.

## Third-Party Licenses

This plugin bundles the following third-party software:

### Superpowers (v4.3.0)

- **Author:** Jesse Vincent (jesse@fsck.com)
- **License:** MIT
- **Repository:** https://github.com/obra/superpowers
- **License file:** [LICENSES/superpowers-MIT](../LICENSES/superpowers-MIT)

## License

MIT
