---
name: track-manager
description: Manage Conductor tracks, phases, and tasks. Use when working with track status, updating task markers, or navigating between tracks. Enforces the Evaluate-Loop workflow.
---

# Track Manager Skill

Manage the lifecycle of Conductor tracks including status updates, task completion, and phase transitions. All operations follow the **Evaluate-Loop** process defined in `conductor/workflow.md`.

## MANDATORY: Evaluate-Loop Integration

Every track operation must follow the Evaluate-Loop:

```
PLAN → EVALUATE PLAN → EXECUTE → EVALUATE EXECUTION → COMPLETE/FIX
```

**Key rules:**
1. **ALWAYS update `plan.md`** after completing any task (prevents duplicate work across sessions)
2. **ALWAYS evaluate** before marking anything complete
3. **NEVER skip** the pre-execution plan evaluation

## Trigger Conditions

Use this skill when:

- Checking track status or progress
- Marking tasks as complete
- Transitioning between phases
- Running pre/post execution evaluations
- User mentions: "track status", "mark complete", "next task", "update plan", "evaluate"

## Track Structure

```
conductor/
├── tracks.md           # Master track list
├── authority-matrix.md # Lead Engineer decision boundaries
├── schemas/
│   └── track-metadata.v2.json  # Metadata schema definition
└── tracks/
    └── <track_id>/
        ├── spec.md         # Requirements
        ├── plan.md         # Phased tasks (MUST be kept updated)
        └── metadata.json   # v2 status with loop_state
```

## Metadata v2 Protocol

All tracks use the v2 metadata schema with explicit loop state tracking.

### Creating a New Track

Initialize `metadata.json` with v2 structure:

```json
{
  "version": 2,
  "track_id": "feature-name_20260131",
  "type": "feature",
  "status": "new",
  "created_at": "2026-01-31T00:00:00Z",
  "updated_at": "2026-01-31T00:00:00Z",

  "loop_state": {
    "current_step": "PLAN",
    "step_status": "NOT_STARTED",
    "fix_cycle_count": 0,
    "max_fix_cycles": 3,
    "checkpoints": {
      "PLAN": { "status": "NOT_STARTED" },
      "EVALUATE_PLAN": { "status": "NOT_STARTED" },
      "EXECUTE": { "status": "NOT_STARTED" },
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

### Updating Loop State

When a step completes, update the checkpoint:

```json
{
  "loop_state": {
    "current_step": "EXECUTE",
    "step_status": "IN_PROGRESS",
    "checkpoints": {
      "PLAN": {
        "status": "PASSED",
        "completed_at": "2026-01-31T10:00:00Z",
        "agent": "loop-planner"
      },
      "EVALUATE_PLAN": {
        "status": "PASSED",
        "completed_at": "2026-01-31T10:30:00Z",
        "verdict": "PASS"
      },
      "EXECUTE": {
        "status": "IN_PROGRESS",
        "started_at": "2026-01-31T11:00:00Z",
        "tasks_completed": 3,
        "tasks_total": 10,
        "last_task": "Task 1.3"
      }
    }
  }
}
```

### Migrating v1 to v2

If a track has v1 metadata (no `version` field or `loop_state`):

1. Read current metadata fields
2. Infer loop state from plan.md content
3. Add v2 structure with inferred values
4. Write back to metadata.json

## Task Status Markers

| Marker | Status      | Description           |
| ------ | ----------- | --------------------- |
| `[ ]`  | Pending     | Not started           |
| `[~]`  | In Progress | Currently working     |
| `[x]`  | Completed   | Done (add commit SHA + summary) |
| `[!]`  | Blocked     | Add note explaining why |

## Workflow Operations

### Before Starting ANY Work

1. Read `tracks.md` to see what's already complete
2. Read the track's `plan.md` to see what tasks are done vs pending
3. Read `spec.md` to understand requirements
4. **Evaluate the plan** — verify scope matches spec, no overlap with completed tracks

### Start a Task

```markdown
# Before
- [ ] Implement user authentication

# After (mark in progress)
- [~] Implement user authentication
```

### Complete a Task (MANDATORY: update plan.md immediately)

```markdown
# After completion (add commit SHA + summary of what was done)
- [x] Implement user authentication <!-- abc1234 -->
  - Created src/components/auth/signup-form.tsx
  - Added email/password validation
  - Integrated with mock API client
```

### Update tracks.md

When completing a phase, update `conductor/tracks.md`:

```markdown
## Active Tracks

| Track ID | Type    | Status      | Progress  |
| -------- | ------- | ----------- | --------- |
| auth-001 | feature | in_progress | Phase 2/3 |
```

## Phase Transition Rules

1. All tasks in phase must be `[x]` before moving to next phase
2. **Run post-execution evaluation** (see Evaluate-Loop in `conductor/workflow.md`)
3. If evaluation fails → create fix tasks → execute → re-evaluate (loop)
4. If evaluation passes → update `metadata.json` with completion timestamp
5. Create commit for phase completion
6. Update `tracks.md` progress column
7. Update `conductor/index.md` current status

## Post-Execution Evaluation Checklist

Before marking a track complete, verify:

| Check | Question |
|-------|----------|
| **Deliverables** | Every deliverable in `spec.md` exists and is functional? |
| **Alignment** | Implementation matches what was planned (no scope drift)? |
| **No Regressions** | Build passes? No console errors? Existing features work? |
| **Quality** | Usability check passes on all user-facing copy? |
| **plan.md Updated** | All tasks marked `[x]` with summaries? |
| **No Leftover** | No tasks skipped or left incomplete? |

## Response Format

After track operations:

```
## Track Update

**Track**: [track_id]
**Operation**: [started/completed/updated/evaluated]
**Phase**: [phase number] - [phase name]
**Progress**: [completed]/[total] tasks
**Evaluation**: [PASS / FAIL - describe issues]
**Next**: [next task description]
```
