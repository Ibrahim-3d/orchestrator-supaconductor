# Checkpoint Protocol for SupaConductor Orchestration

**Purpose**: Define how SupaConductor's enhanced loop agents (powered by superpowers) update `metadata.json` checkpoints during execution for state tracking and resumption.

## Overview

SupaConductor agents must update `metadata.json` at key points during execution to enable:
1. **State Persistence**: Knowing exactly which step and task is currently active.
2. **Resumption**: Restarting execution from the exact last-completed task after a crash or user pause.
3. **Loop Control**: The master orchestrator uses these checkpoints to decide the next step in the Evaluate-Loop.

## Checkpoint Update Format

Agents MUST update the `loop_state.checkpoints` object in the track's `metadata.json`.

### On Start

```json
{
  "loop_state": {
    "current_step": "EXECUTE",
    "step_status": "IN_PROGRESS",
    "step_started_at": "[ISO timestamp]",
    "checkpoints": {
      "EXECUTE": {
        "status": "IN_PROGRESS",
        "started_at": "[ISO timestamp]",
        "agent": "supaconductor:executing-plans",
        "tasks_completed": 0,
        "tasks_total": 10
      }
    }
  }
}
```

### After Each Task (for EXECUTE step)

```json
{
  "loop_state": {
    "checkpoints": {
      "EXECUTE": {
        "status": "IN_PROGRESS",
        "tasks_completed": 3,
        "last_task": "Task 1.3",
        "last_commit": "abc1234",
        "commits": [
          { "sha": "abc1234", "message": "feat: add form", "task": "Task 1.3" }
        ]
      }
    }
  }
}
```

### On Completion (PASS)

```json
{
  "loop_state": {
    "current_step": "EVALUATE_EXECUTION",
    "step_status": "NOT_STARTED",
    "checkpoints": {
      "EXECUTE": {
        "status": "PASSED",
        "completed_at": "[ISO timestamp]",
        "tasks_completed": 10,
        "last_task": "Task 3.2",
        "last_commit": "def5678"
      }
    }
  }
}
```

### On Failure (FAIL)

```json
{
  "loop_state": {
    "step_status": "FAILED",
    "checkpoints": {
      "EXECUTE": {
        "status": "FAILED",
        "completed_at": "[ISO timestamp]",
        "error": "Timeout during build step",
        "notes": "Build failed on task 2.1 due to missing dependency"
      }
    }
  }
}
```

## Mandatory Checkpoints per Step

| Step | Agent | Mandatory Updates |
|------|-------|-------------------|
| `PLAN` | `supaconductor:writing-plans` | `status`, `completed_at`, `tasks_total` |
| `EXECUTE` | `supaconductor:executing-plans` | `status`, `tasks_completed`, `last_task`, `last_commit`, `commits` |
| `FIX` | `supaconductor:systematic-debugging` | `status`, `completed_at`, `fixes_applied` |
| `BRAINSTORM` | `supaconductor:brainstorming` | `status`, `completed_at`, `options_generated` |

## Update Protocol for Agents

1. **Read Current State**: At startup, the agent reads `metadata.json` to check for an existing checkpoint and `resume_from` parameters.
2. **Atomic Write**: Agents should use atomic write operations or proper file locking to prevent `metadata.json` corruption.
3. **Immediate Write**: Checkpoints must be written IMMEDIATELY after each task/milestone, not batched at the end.
4. **Advance State**: On successful completion, the agent is responsible for advancing `current_step` to the NEXT logical step (e.g., from `EXECUTE` to `EVALUATE_EXECUTION`) and resetting `step_status` to `NOT_STARTED`.
