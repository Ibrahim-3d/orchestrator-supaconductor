---
name: conductor-status
description: "Show current track status, loop step, tasks completed, and next action"
user_invocable: true
model: sonnet
---

# /conductor:status — Current Project Status

Display the current progress across all tracks and the active evaluate-loop state.

## Usage

```bash
/conductor:status
```

## What It Shows

- **Active Track** — Which track is currently in progress
- **Current Step** — Where in the Evaluate-Loop we are
- **Tasks** — Completed vs remaining count
- **Last Agent** — Which agent ran last and its result
- **Next Action** — What to run next

## Your Task

Read the following files to generate the status report:

1. **`conductor/tracks.md`** — List of all tracks and their statuses
2. **Active track's `metadata.json`** — Current loop step and state
3. **Active track's `plan.md`** — Task completion progress

## Output Format

```
## Conductor Status

**Active Track**: my-feature-implementation
**Current Step**: Execute (Step 3 of 5)
**Tasks**: 8/12 completed (4 remaining)
**Last Agent**: loop-executor (2 tasks completed, commit abc1234)
**Superpower Enhanced**: Yes
**Fix Cycles**: 0

### Pending Tasks
- [ ] Task 2.3: Add error handling
- [ ] Task 2.4: Write unit tests
- [ ] Task 3.1: Update documentation
- [ ] Task 3.2: Final integration check

### Next Action
Run `/conductor:implement` to continue automatically

---
**Other Tracks**:
- ✅ auth-system (complete)
- ⏸️ payment-integration (not started)
```

## Status Indicators

| Symbol | Meaning |
|--------|---------|
| ✅ | Complete |
| 🔄 | In Progress |
| ⏸️ | Not Started |
| ❌ | Failed / Blocked |

## Loop Step Reference

| Step | Name | Description |
|------|------|-------------|
| 1 | PLAN | Creating execution plan |
| 2 | EVALUATE_PLAN | Validating plan quality |
| 2a | CTO_REVIEW | Technical architecture review |
| 3 | EXECUTE | Implementing code changes |
| 4 | EVALUATE_EXECUTION | Quality checking implementation |
| 5 | FIX | Addressing evaluation failures |
| 5.5 | BUSINESS_DOC_SYNC | Syncing business documents |
| ✅ | COMPLETE | Track finished |

## Related

- `/conductor:implement` — Continue the evaluate-loop
- `/conductor:new-track` — Start a new track
- `/orchestrator-supaconductor:go` — Quick start with goal statement
