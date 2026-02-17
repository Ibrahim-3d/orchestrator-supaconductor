---
name: loop-executor
description: "Implement tasks from the plan. Evaluate-Loop Step 3."
arguments:
  - name: track_id
    description: "The track ID to execute"
    required: true
user_invocable: true
---

# /loop-executor — Execute Plan Tasks

Evaluate-Loop Step 3: Implement the tasks defined in the plan.

## Usage

```bash
/loop-executor <track-id>
```

## Your Task

You ARE the loop-executor agent. Implement each pending task:

1. **Read plan.md**: Find all `[ ]` tasks (pending), skip `[x]` tasks (done)
2. **For each task**:
   - Read task description and acceptance criteria
   - Read existing files mentioned in the task
   - Implement the code changes following project patterns
   - Run verification (`npm run build`, `npm run typecheck`)
   - Create git commit with descriptive message
   - **Immediately mark `[x]` in plan.md with commit SHA**
   - Update `metadata.json` checkpoint

3. **After all tasks**:
   - Set `current_step = "EVALUATE_EXECUTION"`
   - Set `step_status = "NOT_STARTED"`

## Commit Format

```
feat(track-id): Task 1.1 - Create base component

- Created src/components/foo.tsx
- Added TypeScript types

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Plan.md Update Format

```markdown
- [x] Task 1.1: Create base component <!-- abc1234 -->
  - Created src/components/foo.tsx
  - Added TypeScript types
```

## Output

```
TASKS COMPLETED: X/Y
COMMITS: abc1234, def5678, ...
VERDICT: PASS
```

## Message Bus

```bash
echo "PASS" > .message-bus/events/EXECUTE_COMPLETE_{track_id}.event
```

## Reference

Full agent instructions: `.claude/agents/loop-executor.md`
