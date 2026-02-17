---
name: loop-plan-evaluator
description: "Validate execution plan against spec. Evaluate-Loop Step 2."
arguments:
  - name: track_id
    description: "The track ID to evaluate"
    required: true
user_invocable: true
---

# /loop-plan-evaluator — Validate Execution Plan

Evaluate-Loop Step 2: Verify the execution plan is valid before implementation begins.

## Usage

```bash
/loop-plan-evaluator <track-id>
```

## Your Task

You ARE the loop-plan-evaluator agent. Execute the 6 validation passes:

### Pass 1: Scope Alignment
Every task must trace to a spec requirement.

### Pass 2: Overlap Detection
Check for duplicate work with existing tracks in `conductor/tracks.md`.

### Pass 3: Dependency Check
All `depends_on` references must be valid task IDs, no circular deps.

### Pass 4: Task Quality
Each task has: clear description, specific file paths, verifiable acceptance criteria.

### Pass 5: DAG Validation
No cycles, unique IDs, parallel groups don't have file conflicts.

### Pass 6: Board Review (Major Tracks)
If 5+ tasks or architectural changes, spawn board review:
```bash
claude --print "/board-review"
```

## Output

Append evaluation report to `plan.md`:

```markdown
## Plan Evaluation Report

| Check | Status |
|-------|--------|
| Scope Alignment | PASS |
| Overlap Detection | PASS |
| Dependencies | PASS |
| Task Quality | PASS |
| DAG Valid | PASS |
| Board Review | N/A |

### Verdict: PASS
```

Update `metadata.json`:
- On PASS: `current_step = "EXECUTE"`, `step_status = "NOT_STARTED"`
- On FAIL: `current_step = "PLAN"`, `step_status = "NOT_STARTED"`

## Message Bus

```bash
echo "PASS" > .message-bus/events/PLAN_EVAL_COMPLETE_{track_id}.event
# or
echo "FAIL" > .message-bus/events/PLAN_EVAL_COMPLETE_{track_id}.event
```

## Reference

Full agent instructions: `.claude/agents/loop-plan-evaluator.md`
