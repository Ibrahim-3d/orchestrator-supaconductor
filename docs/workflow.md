# SupaConductor Evaluate-Loop Workflow

This document defines the automated **Evaluate-Loop** — the core process SupaConductor uses to manage development tracks from conception to completion.

## The 5-Step Cycle

Every development track in SupaConductor follows this cycle:

```
1. PLAN → 2. EVALUATE PLAN → 3. EXECUTE → 4. EVALUATE EXECUTION → 5. FIX (if failed)
```

The loop runs autonomously, managing state through `metadata.json` and delegating tasks to specialized agents.

### Step 1: PLAN

**Input**: `spec.md` (requirements)
**Agent**: `supaconductor:writing-plans` (Superpower-enhanced)
**Process**:
- Analyze requirements in `spec.md`.
- Generate a task-by-task implementation plan in `plan.md`.
- Build a Dependency Graph (DAG) for parallel execution.
- Update `metadata.json` checkpoint to `PLAN: PASSED`.

**Output**: `plan.md` (complete with task IDs and dependencies).

### Step 2: EVALUATE PLAN

**Input**: `plan.md`
**Agent**: `supaconductor:loop-plan-evaluator`
**Process**:
- Check for technical feasibility and scope discipline.
- Check for overlap with other active tracks in `tracks.md`.
- Ensure tasks meet the "bite-sized" granularity standard.
- Flag risks for user attention.

**Verdict**:
- `PASS`: Advance to Step 3.
- `FAIL`: Return to Step 1 for re-planning (based on evaluator feedback).

### Step 3: EXECUTE

**Input**: `plan.md` + track metadata
**Agent**: `supaconductor:executing-plans` (Superpower-enhanced)
**Process**:
- Parse the plan's DAG for parallelizable tasks.
- Dispatch workers to implement code changes task-by-task.
- Follow TDD patterns where applicable.
- Update `metadata.json` checkpoint after EACH task with commit SHAs.

**Output**: Implementation commits and updated `plan.md` with task statuses.

### Step 4: EVALUATE EXECUTION (Quality Gate)

**Input**: Implementation changes + `plan.md`
**Agent**: `supaconductor:loop-execution-evaluator`
**Process**:
- Dispatch specialized evaluators for deep verification:
  - `eval-ui-ux`: Audit for accessibility, design system, and user experience.
  - `eval-code-quality`: Audit for patterns, DRY/YAGNI, and readability.
  - `eval-integration`: Audit for API compatibility and system-wide side effects.
  - `eval-business-logic`: Verify all acceptance criteria from `spec.md` are met.
- Compile a consolidated `evaluation-report.md`.

**Verdict**:
- `PASS`: Advance to completion protocol.
- `FAIL`: Advance to Step 5 (FIX).

### Step 5: FIX

**Input**: `evaluation-report.md` with failure list
**Agent**: `supaconductor:systematic-debugging` (Superpower-enhanced)
**Process**:
- Perform root-cause analysis for each failure in the report.
- Propose and implement fixes sequentially.
- Verify fixes before committing.
- Increment `fix_cycle_count` in metadata.

**Output**: Fix commits and updated metadata. Advance to Step 4 for re-evaluation.

---

## State Management

The orchestrator manages the loop state in `conductor/tracks/{trackId}/metadata.json`:

```json
{
  "loop_state": {
    "current_step": "EXECUTE",
    "step_status": "IN_PROGRESS",
    "fix_cycle_count": 0,
    "max_fix_cycles": 5,
    "superpower_enhanced": true
  }
}
```

- **`current_step`**: The active phase of the loop.
- **`step_status`**: `NOT_STARTED`, `IN_PROGRESS`, `PASSED`, `FAILED`, `BLOCKED`.
- **`fix_cycle_count`**: Increments after each failed evaluation. Max 5 cycles before completing with warnings.

## Resolution Protocol (Mode-Dependent)

The orchestrator's behavior at decision points depends on `conductor/config.json` → `"mode"`:

### Mode: `"agentic"` (default)

Fully autonomous — never pauses for user input:

1. **`fix_cycle_count` exceeds `max_fix_cycles`** → Mark track as `completed-with-warnings`. Log unresolved issues in metadata.
2. **Agent returns `BLOCKED` status** → Log blocker. Skip blocked tasks. Continue with unblocked tasks.
3. **Board deliberations reach a tie** → Chief Architect (CA) casts the tiebreaking vote.
4. **Track duration exceeds safety limit (50 iterations)** → Complete track with warnings.

### Mode: `"human-in-the-loop"`

Pauses and requests user input at decision points:

1. **`fix_cycle_count` exceeds 3** → Pause. Present recurring issues. Ask user for direction.
2. **Agent returns `BLOCKED` status** → Pause. Report blocker. Ask user for resolution.
3. **Board deliberations reach a deadlock** → Pause. Present board feedback. Ask user to decide.
4. **Track duration exceeds safety limit** → Pause. Report progress. Ask user to continue or abort.
5. **Goal is ambiguous** → Pause. Present interpretations. Ask user to pick.
6. **HIGH_IMPACT decision needed** → Pause. Present options. Ask user to decide.

### Switching Modes

Edit `conductor/config.json`:
```json
{ "mode": "agentic" }        // fully autonomous (default)
{ "mode": "human-in-the-loop" }  // pauses at decision points
```

## Resumption Protocol

SupaConductor is designed for intermittent connectivity and long-running sessions. If a session is interrupted:
1. Orchestrator reads `metadata.json`.
2. Identifies the last active step and checkpoint.
3. Dispatches the appropriate agent with a `resume_from` flag if necessary.
4. Execution continues from the last-recorded stable state.
