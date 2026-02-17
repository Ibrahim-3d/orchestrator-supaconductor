# Development Workflow — Conductor v3

---

## MANDATORY RULES

1. **ALWAYS update `plan.md`** — After completing ANY task, phase, or sub-task, the agent MUST update the track's `plan.md` to reflect what was done. This prevents the next agent/session from re-doing completed work or misunderstanding scope.
2. **ALWAYS follow the Evaluate-Loop** — Every track uses the Plan → Evaluate → Execute → Evaluate → Fix loop described below. No exceptions.
3. **NEVER mark a track complete** without running the Evaluate step and confirming all criteria pass.
4. **ALWAYS sync business docs** — After any track that makes product/pricing/model decisions, run the Business Doc Sync Checklist (Step 5.5) before marking complete.
5. **ALWAYS run tests after code changes** — After ANY code changes, run your project's test suite to verify nothing is broken. Do NOT commit code with failing tests. Fix failing tests before proceeding.

---

## Evaluate-Loop Development Process

This is the **core workflow** for every track. It prevents misalignment, redundant work, and scope drift by embedding evaluation checkpoints at every stage.

### The Loop

```
┌──────────────────────────────────────────────────────────────┐
│                                                              │
│   1. PLAN ──► 2. EVALUATE PLAN ──► 3. EXECUTE                │
│                                        │                     │
│                                        ▼                     │
│                                   4. EVALUATE                 │
│                                    EXECUTION                  │
│                                        │                     │
│                              ┌─────────┴──────────┐          │
│                              │                    │          │
│                          PASS ✅              FAIL ❌        │
│                              │                    │          │
│                              ▼                    ▼          │
│                      5.5 BUSINESS         6. FIX PLAN        │
│                       DOC SYNC                │              │
│                              │                └──► 3         │
│                              ▼              (loop back)      │
│                        5. COMPLETE                           │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Agent Dispatch Table

Each step is handled by a dedicated agent skill. The `conductor-orchestrator` coordinates dispatch.

**Superpower-Enhanced Tracks** (with `superpower_enhanced: true` flag):

| Step | Agent Skill | Supporting Skills | Input | Output |
|------|-------------|-------------------|-------|--------|
| 1. Plan | `superpowers:writing-plans` | `context-loader`, `context-driven-development` | `spec.md`, `tracks.md` | `plan.md` with tasks + DAG |
| 2. Evaluate Plan | `loop-plan-evaluator` | `plan-critiquer` | `plan.md`, `spec.md`, `tracks.md` | PASS/FAIL verdict |
| 3. Execute | `superpowers:executing-plans` | `track-manager` | `plan.md` tasks | Code + updated `plan.md` |
| 4. Evaluate Execution | `loop-execution-evaluator` | Specialized evaluators (see below) | `plan.md`, `spec.md`, codebase | PASS/FAIL verdict |
| 5. Fix | `superpowers:systematic-debugging` | `track-manager` | Evaluation report | Fix tasks + code |
| 5.5 Business Doc Sync | `business-docs-sync` | `track-manager` | Evaluation PASS + decision log | Updated docs |
| Brainstorm | `superpowers:brainstorming` | N/A | Decision context | Options + recommendation |
| Orchestrator | `conductor-orchestrator` | `context-loader` | Track state | Agent dispatch |

**Legacy Tracks** (without `superpower_enhanced` flag):

| Step | Agent Skill | Supporting Skills | Input | Output |
|------|-------------|-------------------|-------|--------|
| 1. Plan | `loop-planner` | `context-loader`, `context-driven-development` | `spec.md`, `tracks.md` | `plan.md` with tasks |
| 2. Evaluate Plan | `loop-plan-evaluator` | `plan-critiquer` | `plan.md`, `spec.md`, `tracks.md` | PASS/FAIL verdict |
| 3. Execute | `loop-executor` | `track-manager` | `plan.md` tasks | Code + updated `plan.md` |
| 4. Evaluate Execution | `loop-execution-evaluator` | Specialized evaluators (see below) | `plan.md`, `spec.md`, codebase | PASS/FAIL verdict |
| 5. Fix | `loop-fixer` | `track-manager` | Evaluation report | Fix tasks + code |
| 5.5 Business Doc Sync | `business-docs-sync` | `track-manager` | Evaluation PASS + decision log | Updated docs |
| Orchestrator | `conductor-orchestrator` | `context-loader` | Track state | Agent dispatch |

**Note:** The orchestrator automatically detects which system to use based on the `superpower_enhanced` flag in `metadata.json`. New tracks default to superpowers.

### Specialized Evaluators (Step 4)

The `loop-execution-evaluator` is a **dispatcher** — it determines the track type and invokes the correct specialized evaluator:

| Evaluator | Track Type | What It Checks |
|-----------|-----------|----------------|
| `eval-ui-ux` | Screens, design system, components | Design tokens, visual consistency, responsive, component states, a11y |
| `eval-code-quality` | Features, infrastructure, refactors | Build, type safety, code patterns, error handling, dead code, tests |
| `eval-integration` | APIs, databases, third-party services | API contracts, auth flows, data persistence, error recovery, env config |
| `eval-business-logic` | Core logic, state management, pricing | Product rules, feature correctness, edge cases, state transitions, data flow |

**Multi-type tracks** get multiple evaluators. All must PASS for the track to pass.

---

## Superpower Integration (v3.1)

### Overview

The Conductor system has been enhanced with **Superpowers** — battle-tested Claude Code skills that provide superior planning, execution, and debugging patterns. The system maintains full backward compatibility through an opt-in migration model.

### Superpowers vs Legacy Loop Agents

| Capability | Superpowers | Legacy Loop Agents |
|------------|-------------|-------------------|
| **Planning** | `superpowers:writing-plans` | `loop-planner` |
| **Execution** | `superpowers:executing-plans` | `loop-executor` |
| **Debugging** | `superpowers:systematic-debugging` | `loop-fixer` |
| **Brainstorming** | `superpowers:brainstorming` | N/A (new capability) |
| **Pattern Quality** | Production-proven | Custom implementation |
| **Resumption** | Built-in via parameters | Manual state tracking |
| **Progress Tracking** | Checkpoint protocol | Basic status updates |

### How It Works

1. **Detection:** The `conductor-orchestrator` reads `metadata.json` and checks for the `superpower_enhanced: true` flag
2. **Dispatch:** If flag is present, orchestrator invokes superpowers with standardized parameters; otherwise uses legacy loop agents
3. **Parameter Passing:** Superpowers receive track context via CLI parameters:
   ```bash
   /superpowers:writing-plans \
     --spec='conductor/tracks/{track-id}/spec.md' \
     --output-dir='conductor/tracks/{track-id}/' \
     --track-id='{track-id}' \
     --metadata='conductor/tracks/{track-id}/metadata.json'
   ```
4. **State Synchronization:** Superpowers update `metadata.json` checkpoints at key execution points
5. **Evaluation:** Same evaluators work with both systems

### Migration Path

**New Tracks:** Automatically use superpowers (orchestrator sets `superpower_enhanced: true` on creation)

**Existing Tracks:**
- Opt-in migration via adding `superpower_enhanced: true` to `metadata.json`
- Safe to migrate at clean checkpoints (step status NOT `IN_PROGRESS`)
- Rollback supported by removing the flag

### Parameter Schema

Each superpower has a standardized parameter set:

**superpowers:writing-plans:**
- `--spec` (required) - Path to spec.md
- `--output-dir` (required) - Where to write plan.md
- `--context-files` (optional) - Additional context files
- `--track-id` (required) - Track identifier
- `--metadata` (required) - Path to metadata.json for checkpoint updates
- `--format` (optional) - Output format (default: markdown)
- `--include-dag` (optional) - Include dependency graph (default: true)

**superpowers:executing-plans:**
- `--plan` (required) - Path to plan.md
- `--track-dir` (required) - Track directory
- `--metadata` (required) - Path to metadata.json
- `--track-id` (required) - Track identifier
- `--mode` (optional) - Execution mode (sequential/parallel, default: parallel)
- `--resume-from` (optional) - Resume from specific task (e.g., "2.3")

**superpowers:systematic-debugging:**
- `--failures` (required) - Path to evaluation-report.md
- `--track-dir` (required) - Track directory
- `--metadata` (required) - Path to metadata.json
- `--track-id` (required) - Track identifier
- `--max-attempts` (optional) - Max retry attempts (default: 3)

**superpowers:brainstorming:**
- `--context` (required) - Decision context description
- `--output-dir` (required) - Where to write options/recommendation
- `--track-id` (required) - Track identifier
- `--options-count` (optional) - Number of options to generate (default: 3)

### Checkpoint Protocol

Superpowers update `metadata.json` at these points:

1. **On Start:** Set checkpoint status to `IN_PROGRESS` with timestamp
2. **During Execution:** Update progress fields (tasks completed, current task, etc.)
3. **On Completion:** Set status to `PASSED` or `FAILED`, record output files

**Checkpoint Structure:**
```json
{
  "checkpoints": {
    "PLAN": {
      "status": "PASSED",
      "started_at": "2026-02-13T12:00:00Z",
      "completed_at": "2026-02-13T12:15:00Z",
      "agent": "superpowers:writing-plans",
      "progress": {
        "current_phase": 5,
        "total_phases": 5,
        "tasks_completed": 35,
        "tasks_total": 35
      },
      "output_files": ["plan.md"],
      "notes": "Plan generated with 5 phases, 35 tasks, DAG included",
      "last_updated": "2026-02-13T12:15:00Z"
    }
  }
}
```

---

### Step-by-Step

#### Step 1: PLAN
- Read the track's `spec.md` to understand requirements
- Read `tracks.md` to check what's already been completed (prevents overlap)
- Create or review the track's `plan.md` with specific tasks
- Each task must have clear acceptance criteria
- Identify dependencies on other tracks

#### Step 2: EVALUATE PLAN
Before writing any code, verify the plan:

| Check | Question |
|-------|----------|
| **Scope** | Does the plan match what `spec.md` asks for? Nothing more, nothing less? |
| **Overlap** | Does any task duplicate work already completed in another track? |
| **Dependencies** | Are all prerequisite tasks/tracks complete? |
| **Feasibility** | Can each task be completed with the current codebase state? |
| **Clarity** | Would a new agent session understand exactly what to do from `plan.md` alone? |

If any check fails → return FAIL → Conductor dispatches planner to revise.

#### Step 3: EXECUTE
- Work through tasks in `plan.md` sequentially
- Mark each task `[~]` when starting, `[x]` when done
- **Update `plan.md` after every completed task** (mandatory)
- **Run tests after completing each task** to catch regressions early
- Commit at logical checkpoints

#### Step 4: EVALUATE EXECUTION
After completing all tasks, run the evaluator:

| Check | Criteria |
|-------|----------|
| **Tests Pass** | Test suite runs with zero failures |
| **Deliverables** | Every deliverable in `spec.md` exists and is functional |
| **Alignment** | Implementation matches what was planned (no scope drift) |
| **No Regressions** | Existing features still work (build passes, no console errors) |
| **plan.md Updated** | All tasks marked `[x]` with accurate descriptions of what was done |
| **No Leftover Work** | No tasks were skipped or left incomplete |

#### Step 5.5: BUSINESS DOC SYNC

After evaluation passes but before marking complete, check whether the track made any product, pricing, or model decisions that affect business documents:

1. **Check for business-impacting changes** — Did this track change pricing, model strategy, deliverables, personas, or revenue assumptions?

2. **If YES** — Run the Business Doc Sync Checklist:
   - Update affected documentation tiers
   - Log the decision in `conductor/decision-log.md`
   - Commit: `docs: sync business docs — [description of what changed]`

3. **If NO** — Skip this step and proceed to Step 5 (COMPLETE).

#### Step 5: COMPLETE (All Checks Pass)
- Generate Phase Completion Report (see template below)
- Update `tracks.md` to mark track as complete
- Commit with message: `docs: complete [TRACK-NAME] - evaluation passed`

#### Step 6: FIX
When any evaluation check fails:
- Parse the evaluator's failure report
- Create specific fix tasks in `plan.md`
- Execute the fixes
- Hand back to the evaluator for re-check
- Max 3 fix cycles before escalating to user
- Repeat until all checks pass

### Applying the Loop to Different Track Types

**Feature Track:**
```
PLAN: Define tasks for implementation
EVALUATE PLAN: Verify tasks match spec, no overlap
EXECUTE: Build the features
EVALUATE: Test functionality, verify all deliverables work
FIX: Any broken features → fix → re-evaluate
COMPLETE: When evaluation passes
```

**UI Track:**
```
PLAN: Define which screens to build and their components
EVALUATE PLAN: Verify screens match requirements
EXECUTE: Build the screens
EVALUATE: Visual check, responsive check, accessibility
FIX: Misaligned screens → fix → re-evaluate
COMPLETE: When evaluation passes
```

**Integration Track:**
```
PLAN: Define schema, API routes, auth flow
EVALUATE PLAN: Verify against tech requirements
EXECUTE: Implement integrations
EVALUATE: Test auth flow, data persistence, error handling end-to-end
FIX: Any broken flows → fix → re-evaluate
COMPLETE: When evaluation passes
```

### plan.md Update Requirements

After EVERY task completion, the agent MUST update the track's `plan.md`:

```markdown
# Before
- [ ] Task 3: Build signup form component

# After (immediately upon completion)
- [x] Task 3: Build signup form component <!-- commit: abc1234 -->
  - Created src/components/auth/signup-form.tsx
  - Added form validation (email, password min 8 chars)
  - Integrated with mock API client
```

This ensures:
1. The next agent session knows exactly what's been done
2. No work gets repeated
3. The evaluate step has clear data to check against

---

## Metadata v3 State Machine

The Evaluate-Loop uses **metadata.json v3** for explicit state tracking with **parallel execution support** and **Board of Directors deliberation**.

### Loop State Structure

Each track's `metadata.json` contains a `loop_state` object:

```json
{
  "version": 2,
  "track_id": "feature-name_20260131",
  "status": "in_progress",

  "loop_state": {
    "current_step": "EXECUTE",
    "step_status": "IN_PROGRESS",
    "step_started_at": "2026-01-31T12:00:00Z",
    "fix_cycle_count": 0,
    "max_fix_cycles": 3,

    "checkpoints": {
      "PLAN": { "status": "PASSED", "completed_at": "...", "agent": "loop-planner" },
      "EVALUATE_PLAN": { "status": "PASSED", "verdict": "PASS" },
      "EXECUTE": {
        "status": "IN_PROGRESS",
        "tasks_completed": 5,
        "tasks_total": 12,
        "last_task": "Task 2.3",
        "last_commit": "abc1234"
      },
      "EVALUATE_EXECUTION": { "status": "NOT_STARTED" },
      "FIX": { "status": "NOT_STARTED" },
      "BUSINESS_SYNC": { "status": "NOT_STARTED", "required": false }
    }
  },

  "lead_consultations": [],
  "discovered_work": [],
  "blockers": []
}
```

### Step Status Values

| Status | Meaning |
|--------|---------|
| `NOT_STARTED` | Step hasn't begun |
| `IN_PROGRESS` | Agent currently running |
| `PASSED` | Step completed successfully |
| `FAILED` | Step failed, needs fix/revision |
| `BLOCKED` | External dependency preventing progress |
| `SKIPPED` | Step not applicable for this track |

### State Machine Transitions

| Current Step | Step Status | Next Action |
|--------------|-------------|-------------|
| `PLAN` | `NOT_STARTED` | Dispatch planner |
| `PLAN` | `IN_PROGRESS` | Resume planner |
| `PLAN` | `PASSED` | Advance to `EVALUATE_PLAN` |
| `EVALUATE_PLAN` | `NOT_STARTED` | Dispatch plan evaluator |
| `EVALUATE_PLAN` | `PASSED` | Advance to `EXECUTE` |
| `EVALUATE_PLAN` | `FAILED` | Go back to `PLAN` |
| `EXECUTE` | `NOT_STARTED` | Dispatch executor |
| `EXECUTE` | `IN_PROGRESS` | Resume executor from `last_task` |
| `EXECUTE` | `PASSED` | Advance to `EVALUATE_EXECUTION` |
| `EVALUATE_EXECUTION` | `NOT_STARTED` | Dispatch execution evaluator |
| `EVALUATE_EXECUTION` | `PASSED` | Check `business_sync_required` → `BUSINESS_SYNC` or `COMPLETE` |
| `EVALUATE_EXECUTION` | `FAILED` | Advance to `FIX` |
| `FIX` | `NOT_STARTED` | Check `fix_cycle_count` → dispatch fixer or escalate |
| `FIX` | `PASSED` | Go back to `EVALUATE_EXECUTION` |
| `BUSINESS_SYNC` | `PASSED` | Advance to `COMPLETE` |
| `COMPLETE` | — | Mark track complete, report success |
| Any | `BLOCKED` | Check blockers, escalate to user |

### Checkpoint Update Protocol

Each loop agent MUST update `metadata.json` at key points:

1. **On Start**: Set `checkpoints.[STEP].status = "IN_PROGRESS"` with timestamp
2. **During Execution**: Update progress fields (e.g., `tasks_completed`, `last_task`)
3. **On Completion**: Set status to `PASSED` or `FAILED`, advance `current_step`

This enables exact resumption if the orchestrator is interrupted.

### Resumption Protocol

When the orchestrator starts or resumes:

1. Read `metadata.json` → get `loop_state.current_step` and `step_status`
2. For `IN_PROGRESS` steps, check checkpoint data (e.g., `EXECUTE.last_task`)
3. Resume agent from that exact point — no re-work of completed items
4. For `PASSED` steps, advance to next step in state machine
5. For `FAILED` steps, follow failure path (FIX cycle or back to PLAN)

---

## Parallel Execution System (v3)

Version 3 of the orchestrator enables **parallel task execution** via specialized worker agents that coordinate through a shared message bus.

### When Parallel Execution Applies

Parallel execution is used when:
- Plan contains a `dag:` block with `parallel_groups`
- DAG validation passed in EVALUATE_PLAN
- Track has 3+ tasks that can run concurrently

### The DAG (Directed Acyclic Graph)

Plans now include explicit dependency graphs:

```yaml
dag:
  nodes:
    - id: "1.1"
      name: "Create data store"
      type: "code"
      files: ["src/stores/data-store.ts"]
      depends_on: []
      phase: 1
    - id: "1.2"
      name: "Build resolver"
      type: "code"
      files: ["src/lib/resolver.ts"]
      depends_on: []
      phase: 1
    - id: "1.3"
      name: "Wire together"
      type: "code"
      files: ["src/stores/data-store.ts"]
      depends_on: ["1.1", "1.2"]
      phase: 1

  parallel_groups:
    - id: "pg-1"
      tasks: ["1.1", "1.2"]
      conflict_free: true
    - id: "pg-2"
      tasks: ["1.3"]
      conflict_free: true
```

### Parallel Groups

Tasks are grouped by topological level:
- **conflict_free: true** — No shared files, can run without coordination
- **conflict_free: false** — Shared resources require file locking

### Worker Agents

Workers are **ephemeral agents** created from templates:

| Template | Specialization |
|----------|---------------|
| `code-worker.template.md` | TDD focus, code patterns |
| `ui-worker.template.md` | Design system, accessibility |
| `integration-worker.template.md` | API contracts, error handling |
| `test-worker.template.md` | Coverage targets, test patterns |

Workers are created by `agent-factory`, dispatched via parallel Task calls, and cleaned up after completion.

### Message Bus

Workers coordinate via file-based message queue:

```
conductor/tracks/{track}/.message-bus/
├── queue.jsonl           # All messages (append-only)
├── locks.json            # File locks for coordination
├── worker-status.json    # Worker heartbeats
├── events/               # Signal files for polling
└── board/                # Board deliberation sessions
```

**Message Types:**
| Type | Purpose |
|------|---------|
| `PROGRESS` | Task progress update |
| `TASK_COMPLETE` | Unblocks dependent tasks |
| `TASK_FAILED` | Triggers fix cycle |
| `FILE_LOCK` / `FILE_UNLOCK` | Coordinate shared files |
| `BLOCKED` | Waiting on dependency |

### Worker Protocol

1. **On Start**: Check message bus for dependency completions
2. **Before Modifying Files**: Acquire lock via `locks.json`
3. **During Execution**: Post `PROGRESS` every 5 minutes
4. **On Completion**: Release locks, post `TASK_COMPLETE`
5. **On Failure**: Release locks, post `TASK_FAILED`

### Failure Isolation

One worker failure doesn't block independent tasks:
- Failed task's dependents are paused
- Other parallel tasks continue
- Orchestrator attempts retry (max 2)
- After 3 failures, escalates to user

### Deadlock Detection

Monitor detects circular waits:
- 30-minute lock timeout with auto-release
- Wait-for graph analysis
- Automatic victim selection (oldest worker)

---

## Board of Directors (v3)

The Board of Directors is a **5-member expert deliberation system** that provides multi-perspective review at key checkpoints.

### The Board

| Director | Domain | Evaluates |
|----------|--------|-----------|
| **CA** - Chief Architect | Technical | System design, patterns, scalability, tech debt |
| **CPO** - Chief Product Officer | Product | User value, market fit, scope |
| **CSO** - Chief Security Officer | Security | Vulnerabilities, compliance, data protection |
| **COO** - Chief Operations Officer | Execution | Feasibility, timeline, resources, deployment |
| **CXO** - Chief Experience Officer | Experience | UX/UI, accessibility, user journey |

### When Board is Invoked

| Checkpoint | Condition | Board Type |
|------------|-----------|------------|
| EVALUATE_PLAN | Major track (arch/integ/infra, 5+ tasks, P0) | Full meeting |
| EVALUATE_EXECUTION | Always | Quick review |
| PRE_LAUNCH | Production deploy | Security + Ops deep dive |
| CONFLICT | Evaluators disagree | Tie-breaker |

### Deliberation Protocol

**Phase 1: ASSESS (Parallel)**
- All 5 directors evaluate proposal independently
- Each posts `BOARD_ASSESS` to message bus

**Phase 2: DISCUSS (3 Rounds)**
- Directors read others' assessments
- Challenge, agree, or clarify via `BOARD_DISCUSS`
- Max 3 discussion rounds

**Phase 3: VOTE**
- Each director posts `BOARD_VOTE`
- Includes confidence level (0-1) and conditions

**Phase 4: RESOLVE**
- Orchestrator aggregates votes
- Posts `BOARD_RESOLVE` with final verdict

### Resolution Rules

| Votes | Resolution |
|-------|------------|
| 5-0 or 4-1 APPROVE | **APPROVED** |
| 3-2 APPROVE | **APPROVED WITH REVIEW** |
| 3-2 REJECT | **REJECTED** |
| 4-1 or 5-0 REJECT | **REJECTED** |
| Tie | **ESCALATE** to user |

### Board Session Tracking

Sessions are stored in metadata:

```json
{
  "board_sessions": [
    {
      "session_id": "board-20260201-123456",
      "checkpoint": "EVALUATE_PLAN",
      "verdict": "APPROVED",
      "vote_summary": {
        "CA": "APPROVE",
        "CPO": "APPROVE",
        "CSO": "APPROVE",
        "COO": "APPROVE",
        "CXO": "APPROVE"
      },
      "conditions": [
        "Add caching layer (CA)",
        "Security audit before launch (CSO)"
      ],
      "timestamp": "2026-02-01T12:00:00Z"
    }
  ]
}
```

### Board Commands

- `/board-meeting [proposal]` — Full 4-phase deliberation
- `/board-review [proposal]` — Quick assessment (no discussion)

---

## V3 Evaluate-Loop Diagram

```
                              TRACK START
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │    KNOWLEDGE MANAGER     │
                    │    (Load patterns)       │
                    └────────────┬─────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PLAN (with DAG)                                 │
│  Planner generates plan.md with explicit dependency graph                   │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EVALUATE_PLAN + BOARD MEETING                             │
│                                                                              │
│  1. DAG Validation (cycles, conflicts)                                       │
│  2. Standard checks (scope, overlap, deps, quality)                          │
│  3. For MAJOR tracks → invoke /board-meeting                                │
│     - All 5 directors ASSESS in parallel                                    │
│     - Directors DISCUSS via message bus                                     │
│     - Directors VOTE with confidence                                        │
│     - RESOLVE → APPROVED / REJECTED / CONDITIONS                            │
│                                                                              │
│  PASS → Continue   |   FAIL → Back to PLAN with conditions                  │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PARALLEL_EXECUTE                                     │
│                                                                              │
│  For each parallel_group in DAG:                                            │
│    1. agent-factory creates specialized workers                             │
│    2. Dispatch via parallel Task(run_in_background=true)                   │
│    3. Workers coordinate via message bus:                                    │
│       - FILE_LOCK / FILE_UNLOCK for shared files                           │
│       - PROGRESS updates every 5 min                                        │
│       - TASK_COMPLETE / TASK_FAILED when done                              │
│    4. Monitor for completion, handle failures                               │
│    5. Cleanup ephemeral workers                                              │
│                                                                              │
│  PASS → Continue   |   PARTIAL_FAIL → Isolate + Continue                    │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                 EVALUATE_EXECUTION + BOARD REVIEW                            │
│                                                                              │
│  1. Specialized evaluators (UI, Code, Integration, Business)                │
│  2. Quick board review (no discussion)                                       │
│  3. Verify board conditions from EVALUATE_PLAN                              │
│                                                                              │
│  PASS → BUSINESS_SYNC? → COMPLETE                                           │
│  FAIL → FIX (with specific failures)                                        │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                              ┌────┴────┐
                              │         │
                         PASS ▼    FAIL ▼
                    ┌──────────┐  ┌──────────┐
                    │BUSINESS  │  │   FIX    │
                    │  SYNC    │  │ (max 3x) │
                    └────┬─────┘  └────┬─────┘
                         │             │
                         ▼             │
                    ┌──────────┐       │
                    │ COMPLETE │◄──────┘
                    └────┬─────┘
                         │
                         ▼
                    ┌──────────────────────────┐
                    │   RETROSPECTIVE AGENT    │
                    │   + Cleanup workers      │
                    └──────────────────────────┘
```

---

## Lead Engineer Consultation System

The orchestrator minimizes user friction by consulting specialized "Lead Engineer" agents for decisions within their authority.

### Lead Engineer Roster

| Lead | Domain | Skill Path |
|------|--------|------------|
| **Architecture Lead** | Patterns, component organization, ADRs | `skills/leads/architecture-lead/` |
| **Product Lead** | Scope interpretation, requirements, copy | `skills/leads/product-lead/` |
| **Tech Lead** | Implementation approach, dependencies | `skills/leads/tech-lead/` |
| **QA Lead** | Test strategy, coverage thresholds | `skills/leads/qa-lead/` |

### Consultation Flow

```
Orchestrator encounters question
        │
        ▼
  ┌─────────────┐
  │ Check Authority Matrix │
  └──────┬──────┘
         │
    USER_ONLY? ──────► Escalate to user
         │
    LEAD_CONSULT? ──► Dispatch lead agent
         │                   │
         │            ┌──────┴──────┐
         │            │             │
         │        Decided      ESCALATE
         │            │             │
         │      Log decision   To user
         │      Continue loop
         │
    ORCHESTRATOR? ──► Decide autonomously
```

### Authority Matrix Quick Reference

**Always Escalate to User (USER_ONLY):**
- Budget changes >$50/month
- Add/remove features from spec
- Breaking API changes
- Dependencies >50KB
- Coverage below minimum threshold
- Security/production data changes
- Pricing/business model changes

**Lead Can Decide (LEAD_CONSULT):**
- Architecture: Apply existing patterns, component organization, additive schema changes
- Product: Interpret ambiguous spec, task ordering, error message copy
- Tech: Implementation approach, runtime deps <50KB, any devDependencies
- QA: Coverage thresholds, test type selection, mock strategy

**Full Matrix:** `conductor/authority-matrix.md`

### Lead Response Format

Leads return structured decisions:

```json
{
  "lead": "architecture",
  "decision_made": true,
  "decision": "Use API routes for consistency",
  "reasoning": "Matches existing pattern",
  "authority_used": "TECH_CHOICE",
  "escalate_to": null
}
```

All consultations are logged in `metadata.json → lead_consultations[]` for audit trail.

---

## Escalation Triggers

The orchestrator stops and escalates to user when:

1. **Fix cycle limit** — 3 failed EVALUATE → FIX cycles
2. **USER_ONLY decision** — From authority matrix
3. **Lead escalated** — Lead returned `escalate_to: "user"`
4. **Blocker detected** — External dependency blocking progress
5. **Max iterations** — Safety limit of 50 loop iterations reached

---

## Development Approach

### Trunk-Based Development

- Commit directly to `main` branch
- Small, frequent commits
- Each commit should be deployable
- Feature flags for incomplete features (if needed)

### Commit Message Format

```
type: brief description

[optional body with more detail]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring
- `style`: Formatting, no logic change
- `docs`: Documentation
- `chore`: Build, config, dependencies

### Task Status Markers

```markdown
- [ ] Task: Not started
- [~] Task: In progress
- [x] Task: Completed <!-- commit-sha --> (add summary of what was done)
- [!] Task: Blocked (add note explaining why)
```

---

## Phase Completion Verification Protocol

### Purpose
Before marking any phase as complete in Conductor, this protocol ensures all deliverables meet quality standards and acceptance criteria.

### Verification Steps

1. **Deliverables Check**
   - All deliverables listed in the track's `spec.md` are present
   - Each deliverable matches its acceptance criteria
   - No placeholder or incomplete content

2. **Quality Gates**
   - All relevant quality gates have passed
   - No console errors or warnings

3. **Testing Verification**
   - Unit tests pass for new/modified code
   - Integration tests pass (if applicable)
   - Manual testing completed per checklist

4. **Documentation**
   - Code is documented where non-obvious
   - README updated if public APIs changed

5. **Sign-off**
   - Self-review completed
   - Changes committed with proper message format
   - Track status updated in `tracks.md`

### Phase Completion Template

```markdown
## Phase [X] Completion Report

**Phase:** [Phase Name]
**Date:** [YYYY-MM-DD]
**Status:** Complete

### Deliverables
- [x] Deliverable 1 - [link or description]
- [x] Deliverable 2 - [link or description]

### Quality Gates Passed
- [x] Gate 1
- [x] Gate 2

### Tests
- Unit: X passing
- Integration: X passing
- E2E: X passing

### Notes
[Any relevant notes or caveats]
```
