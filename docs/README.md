# Conductor Superpowers Plugin v3.1

Parallel multi-agent orchestration with Evaluate-Loop, Board of Directors, and Superpowers integration for Claude Code.

## What is Conductor?

Conductor is a structured workflow system that organizes development work into **tracks** and **phases**, with detailed specifications, step-by-step implementation plans, and automated quality gates. It provides:

- **Evaluate-Loop** — Plan → Evaluate Plan → Execute → Evaluate Execution → Fix cycle
- **14 Specialized Agents** — Orchestrator, planners, executors, evaluators, fixers
- **Board of Directors** — 5-member expert deliberation system (CA, CPO, CSO, COO, CXO)
- **Parallel Execution** — DAG-based task parallelization with worker agents
- **Lead Engineer System** — Architecture, Product, Tech, QA leads for autonomous decisions
- **Superpowers Integration** — Battle-tested Claude Code skills for planning, execution, debugging

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

### Superpowers Integration

New tracks use Superpowers by default:
- `superpowers:writing-plans` instead of `loop-planner`
- `superpowers:executing-plans` instead of `loop-executor`
- `superpowers:systematic-debugging` instead of `loop-fixer`
- `superpowers:brainstorming` for decision-making

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

## License

MIT
