---
name: loop-planner
description: "Create execution plan from specification. Evaluate-Loop Step 1."
arguments:
  - name: track_id
    description: "The track ID to create a plan for"
    required: true
user_invocable: true
---

# /loop-planner — Create Execution Plan

Evaluate-Loop Step 1: Create a detailed, phased execution plan from the track's specification.

## Usage

```bash
/loop-planner <track-id>
```

## Your Task

You ARE the loop-planner agent. Execute the planning process directly:

1. **Read the spec**: `conductor/tracks/{track_id}/spec.md`
2. **Check for overlap**: Read `conductor/tracks.md` for completed work
3. **Create plan.md** with:
   - Phased tasks with `[ ]` checkboxes
   - DAG section for parallel execution
   - Clear acceptance criteria per task
4. **Update metadata.json**:
   - Set `current_step = "EVALUATE_PLAN"`
   - Set `step_status = "NOT_STARTED"`

## Output

When complete, output:
```
PLAN CREATED: conductor/tracks/{track_id}/plan.md
TASKS: {count} tasks in {phase_count} phases
VERDICT: PASS
```

## Message Bus (for orchestrator coordination)

After completion, write event file:
```bash
echo "PASS" > .message-bus/events/PLAN_COMPLETE_{track_id}.event
```

## Reference

Full agent instructions: `.claude/agents/loop-planner.md`
