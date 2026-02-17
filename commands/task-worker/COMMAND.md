---
name: task-worker
description: "Execute a single task from the plan. Used for parallel execution."
arguments:
  - name: track_id
    description: "The track ID"
    required: true
  - name: task_id
    description: "The specific task ID to execute (e.g., 1.1, 2.3)"
    required: true
user_invocable: true
---

# /task-worker — Execute Single Task

Ephemeral worker for executing a single task. Used by parallel-dispatcher for concurrent execution.

## Usage

```bash
/task-worker <track-id> <task-id>
```

## Your Task

You ARE a task-worker agent. Execute ONLY the specified task.

1. **Register with message bus**:
   ```bash
   # Update worker-status.json
   ```

2. **Read task from plan.md**: Find task matching `{task_id}`

3. **Acquire file locks** if modifying shared files:
   - Check `.message-bus/locks.json`
   - Add lock for files you'll modify

4. **Implement the task**:
   - Read existing code first
   - Follow project patterns
   - Write tests if applicable
   - Commit changes

5. **Post heartbeat** every 5 minutes (for long tasks)

6. **Release locks** after completion

7. **Post completion event**:
   ```bash
   echo "{commit_sha}" > .message-bus/events/TASK_COMPLETE_{task_id}.event
   # or on failure:
   echo "{error_message}" > .message-bus/events/TASK_FAILED_{task_id}.event
   ```

## Commit Format

```
feat(track-id): Task {task_id} - {task_name}

- {change 1}
- {change 2}

Worker: worker-{task_id}-{timestamp}
Co-Authored-By: Claude <noreply@anthropic.com>
```

## Update plan.md

Mark your task complete:
```markdown
- [x] Task {task_id}: {name} <!-- {commit_sha} -->
  - {summary of changes}
```

## Output

```
TASK COMPLETE: {task_id}
COMMIT: {sha}
FILES: {list of files modified}
```

## Reference

Full agent instructions: `.claude/agents/task-worker.md`
