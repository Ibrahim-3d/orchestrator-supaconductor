# Checkpoint Protocol for Superpowers

**Purpose**: Define how superpowers update metadata.json checkpoints during execution for state tracking and resumption.

**Version**: 1.0
**Created**: 2026-02-13

---

## Overview

Superpowers must update `metadata.json` at key points during execution to enable:
1. **Progress Tracking** - Orchestrator knows what's happening
2. **Resumption** - Can resume from exact checkpoint after interruption
3. **Failure Recovery** - Clear record of what succeeded/failed
4. **Audit Trail** - Complete history of execution

---

## Checkpoint Update Points

### When to Update

Superpowers MUST update checkpoints at these points:

| Event | Update Type | Checkpoint Status |
|-------|-------------|-------------------|
| **Start** | Initial | `IN_PROGRESS` |
| **During Execution** | Progress | `IN_PROGRESS` (with progress data) |
| **On Success** | Completion | `PASSED` |
| **On Failure** | Completion | `FAILED` |
| **On Block** | Completion | `BLOCKED` |

---

## Checkpoint Data Structure

### Full Checkpoint Format

```json
{
  "loop_state": {
    "current_step": "PLAN",
    "step_status": "IN_PROGRESS",
    "step_started_at": "2026-02-13T12:00:00Z",
    "fix_cycle_count": 0,
    "max_fix_cycles": 3,

    "checkpoints": {
      "PLAN": {
        "status": "IN_PROGRESS",
        "started_at": "2026-02-13T12:00:00Z",
        "completed_at": null,
        "agent": "superpowers:writing-plans",
        "progress": {
          "current_phase": 2,
          "total_phases": 5,
          "current_task": "Designing parameter schema",
          "tasks_completed": 5,
          "tasks_total": 35
        },
        "output_files": [],
        "notes": "",
        "last_updated": "2026-02-13T12:05:00Z"
      }
    }
  }
}
```

### Required Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `status` | string | Yes | `NOT_STARTED`, `IN_PROGRESS`, `PASSED`, `FAILED`, `BLOCKED` |
| `started_at` | ISO timestamp | Yes | When step started |
| `completed_at` | ISO timestamp | No | When step completed (null if in progress) |
| `agent` | string | Yes | Which superpower is executing |
| `progress` | object | No | Progress data (for IN_PROGRESS) |
| `output_files` | array | No | Files created/modified |
| `notes` | string | No | Brief summary or error message |
| `last_updated` | ISO timestamp | Yes | Last checkpoint update |

---

## Update Protocol for Each Superpower

### superpowers:writing-plans

**Checkpoint Key**: `PLAN`

1. **On Start**: Set status `IN_PROGRESS`, record agent and timestamp
2. **During Execution** (every 5 minutes): Update progress with current phase/task
3. **On Completion**: Set status `PASSED`, record output_files and notes

### superpowers:executing-plans

**Checkpoint Key**: `EXECUTE`

1. **On Start**: Set status `IN_PROGRESS`, record tasks_total
2. **After Each Task**: Update tasks_completed, last_task, last_commit
3. **On Completion**: Set status `PASSED`, record total tasks and commits

### superpowers:systematic-debugging

**Checkpoint Key**: `FIX`

1. **On Start**: Set status `IN_PROGRESS`, record issues_total
2. **During Fixing**: Update issues_fixed, current_issue
3. **On Completion**: Set status `PASSED`, record fix summary

### superpowers:brainstorming

**Checkpoint Key**: `BRAINSTORM`

1. **On Start**: Set status `IN_PROGRESS`
2. **On Completion**: Set status `PASSED`, record output_files

---

## Error Handling

### On Failure

Update checkpoint with failure details in the `notes` field:

```json
{
  "status": "FAILED",
  "notes": "ERROR: Missing required spec.md file at conductor/tracks/{track-id}/spec.md"
}
```

### On Interruption

Checkpoint preserves exact state for resumption. The orchestrator can resume with `--resume-from` parameter using the `last_task` value from the checkpoint.

---

## File Locking

To prevent race conditions with concurrent metadata updates:

```bash
# Acquire lock
lockfile="${track_dir}/.metadata.lock"
while ! mkdir "$lockfile" 2>/dev/null; do
  sleep 0.1
done

# Update metadata
# ... (update code here)

# Release lock
rmdir "$lockfile"
```
