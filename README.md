<p align="center">
  <strong>Conductor Superpowers</strong>
</p>

<p align="center">
  Multi-agent orchestration system for <a href="https://docs.anthropic.com/en/docs/claude-code">Claude Code</a> with parallel execution, automated quality gates, and a 5-member Board of Directors.
</p>

<p align="center">
  <a href="#installation">Installation</a> &bull;
  <a href="#quick-start">Quick Start</a> &bull;
  <a href="#how-it-works">How It Works</a> &bull;
  <a href="#commands">Commands</a> &bull;
  <a href="#architecture">Architecture</a> &bull;
  <a href="#license">License</a>
</p>

---

## What is this?

Conductor Superpowers is a **Claude Code plugin** that turns Claude into a structured engineering team. Instead of ad-hoc coding, it organizes work into tracks with specs, plans, parallel execution, and automated evaluation — like having a project manager, architect, and QA team built into your CLI.

**One command. Full automation.**

```
/go Add user authentication with OAuth
```

What happens behind the scenes:
1. Creates a specification from your goal
2. Generates a dependency-aware execution plan (DAG)
3. Evaluates the plan for scope, overlap, and feasibility
4. Executes tasks in parallel where possible
5. Evaluates results (code quality, UI/UX, integrations, business logic)
6. Fixes any issues automatically
7. Reports completion

## What's Included

| Component | Count | Description |
|-----------|------:|-------------|
| **Agents** | 16 | Orchestrator, loop agents, board directors, executive advisors, workers |
| **Skills** | 42 | Planning, execution, evaluation, debugging, TDD, code review, and more |
| **Commands** | 22 | `/go`, `/conductor`, `/board-meeting`, `/cto-advisor`, and more |
| **Evaluators** | 4 | UI/UX, Code Quality, Integration, Business Logic |
| **Board of Directors** | 5 | Chief Architect, CPO, CSO, COO, CXO |
| **Lead Engineers** | 4 | Architecture, Product, Tech, QA |

Bundles [superpowers](https://github.com/obra/superpowers) v4.3.0 (MIT) — no external dependencies needed.

## Installation

### Option 1: Clone directly (recommended)

```bash
git clone https://github.com/Ibrahim-3d/conductor-superpowers.git ~/.claude/plugins/conductor-superpowers
```

### Option 2: Manual download

Download the latest release and extract to `~/.claude/plugins/conductor-superpowers/`.

### Verify installation

Start a new Claude Code session. You should see the superpowers skills load and the `/conductor` command become available.

## Quick Start

### Initialize Conductor in your project

```bash
/conductor setup
```

This creates a `conductor/` directory with track registry, workflow docs, and knowledge base.

### Start building

```bash
/go <describe what you want to build>
```

Examples:

```bash
/go Add Stripe payment integration with webhooks
/go Fix the login bug where users get logged out after refresh
/go Build a dashboard with real-time analytics charts
/go Refactor the database layer to use connection pooling
```

### More control

```bash
/conductor status          # See all tracks and progress
/conductor implement       # Continue work on current track
/conductor new-track       # Create a track manually
/phase-review              # Run quality gate evaluation
```

## How It Works

### The Evaluate-Loop

Every track follows a rigorous cycle:

```
        +--------+     +-----------+     +---------+     +----------+
   +--->|  PLAN  |---->| EVAL PLAN |---->| EXECUTE |---->| EVAL EXEC|---+
   |    +--------+     +-----------+     +---------+     +----------+   |
   |         ^              |                                  |        |
   |         |            FAIL                               PASS     FAIL
   |         |              |                                  |        |
   |         +--------------+                                  v        |
   |                                                    +-----------+   |
   |                                                    | COMPLETE  |   |
   |                                                    +-----------+   |
   |                                                                    |
   |    +-------+                                                       |
   +----| FIX   |<-----------------------------------------------------+
        +-------+
```

- **Plan** — Generates implementation steps with dependency graph (DAG)
- **Evaluate Plan** — Checks scope, overlap with existing tracks, feasibility
- **Execute** — Implements code, runs tests, updates progress
- **Evaluate Execution** — Dispatches specialized evaluators (UI/UX, code quality, integration, business logic)
- **Fix** — Addresses failures, loops back to evaluation (max 3 cycles)

### Parallel Execution

Tasks without dependencies run simultaneously:

```
Task 1: Create database schema ──────┐
Task 2: Build API endpoints ─────────┼──> Task 5: Integration tests
Task 3: Design UI components ────────┘
Task 4: Write unit tests (independent) ──> Done
```

### Board of Directors

For major decisions, a 5-member board deliberates:

| Director | Domain | Focus |
|----------|--------|-------|
| **Chief Architect (CA)** | Technical | System design, patterns, scalability, tech debt |
| **Chief Product Officer (CPO)** | Product | User value, market fit, scope discipline |
| **Chief Security Officer (CSO)** | Security | Vulnerabilities, compliance, data protection |
| **Chief Operations Officer (COO)** | Operations | Feasibility, timeline, resources, deployment |
| **Chief Experience Officer (CXO)** | Experience | UX/UI, accessibility, user journey |

```bash
/board-meeting Should we migrate from REST to GraphQL?
/board-review Add real-time notifications via WebSocket
```

## Commands

### Core

| Command | Description |
|---------|-------------|
| `/go <goal>` | State your goal — Conductor handles everything |
| `/conductor status` | View all tracks and current progress |
| `/conductor implement` | Run the Evaluate-Loop on current track |
| `/conductor new-track` | Create a new track with spec and plan |
| `/conductor setup` | Initialize Conductor in a project |

### Quality & Review

| Command | Description |
|---------|-------------|
| `/phase-review` | Post-execution quality gate |
| `/cto-advisor` | CTO-level architecture review |
| `/board-meeting <topic>` | Full board deliberation (4 phases) |
| `/board-review <topic>` | Quick board assessment |
| `/ui-audit` | UI/UX accessibility audit |

### Advisors

| Command | Description |
|---------|-------------|
| `/ceo` | Strategic business advice |
| `/cmo` | Marketing strategy guidance |
| `/cto` | Technical architecture guidance |
| `/ux-designer` | UX strategy and design guidance |

### Superpowers (Bundled)

| Command | Description |
|---------|-------------|
| `/write-plan` | Create a plan using superpowers patterns |
| `/execute-plan` | Execute a plan using superpowers patterns |
| `/brainstorm` | Creative problem-solving session |

## Architecture

### Directory Structure

```
conductor-superpowers/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── agents/                       # 16 agent definitions
│   ├── conductor-orchestrator.md # Master loop coordinator
│   ├── loop-planner.md          # Plan creation
│   ├── loop-executor.md         # Code implementation
│   ├── loop-fixer.md            # Issue resolution
│   ├── loop-plan-evaluator.md   # Plan validation
│   ├── loop-execution-evaluator.md # Execution validation
│   ├── board-meeting.md         # Board coordinator
│   ├── code-reviewer.md         # Code review (superpowers)
│   ├── parallel-dispatcher.md   # Parallel task dispatch
│   ├── task-worker.md           # Ephemeral task executor
│   └── ...                      # Executive advisors (CEO, CMO, CTO, UX)
├── commands/                     # 22 slash commands
├── skills/                       # 42 skills
│   ├── conductor-orchestrator/   # Core loop orchestration
│   ├── writing-plans/            # Plan creation (superpowers)
│   ├── executing-plans/          # Plan execution (superpowers)
│   ├── systematic-debugging/     # Debugging (superpowers)
│   ├── eval-ui-ux/              # UI/UX evaluator
│   ├── eval-code-quality/       # Code quality evaluator
│   ├── eval-integration/        # Integration evaluator
│   ├── eval-business-logic/     # Business logic evaluator
│   ├── board-of-directors/      # Board deliberation system
│   │   └── directors/           # 5 director profiles
│   ├── leads/                   # 4 lead engineer roles
│   ├── parallel-dispatch/       # DAG-based parallel execution
│   ├── message-bus/             # Inter-agent communication
│   ├── worker-templates/        # 5 worker templates
│   └── ...                      # 25+ more skills
├── hooks/                        # Session hooks
├── lib/                          # Utility scripts
├── docs/                         # Workflow and authority docs
├── scripts/                      # Setup script
└── LICENSES/                     # Third-party license files
```

### Track Structure (per project)

When you run `/conductor setup`, it creates:

```
your-project/
└── conductor/
    ├── tracks.md               # Track registry
    ├── workflow.md             # Process documentation
    ├── authority-matrix.md     # Decision boundaries
    ├── decision-log.md         # Architectural decisions
    ├── knowledge/
    │   └── patterns.md         # Learned patterns
    └── tracks/                 # Individual tracks
        └── feature-name/
            ├── spec.md         # Requirements
            ├── plan.md         # Implementation plan + DAG
            └── metadata.json   # State machine + config
```

## Project-Specific Skills

Conductor handles orchestration. Your project handles domain knowledge. Keep project-specific skills in your project's `.claude/skills/`:

```
your-project/.claude/skills/
├── product-rules/SKILL.md       # Business logic, personas
├── api-patterns/SKILL.md        # API conventions
├── design-system/SKILL.md       # Design tokens, components
└── testing-standards/SKILL.md   # Coverage targets, test patterns
```

The orchestrator loads both plugin skills and project skills automatically.

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- Git

## Third-Party

This plugin bundles [superpowers](https://github.com/obra/superpowers) v4.3.0 by [Jesse Vincent](https://github.com/obra), licensed under MIT. See [LICENSES/superpowers-MIT](LICENSES/superpowers-MIT).

## License

MIT - see [LICENSE](LICENSE)
