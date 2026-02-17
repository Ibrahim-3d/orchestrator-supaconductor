---
name: parallel-dispatcher
description: "Dispatch multiple task-workers in parallel based on DAG dependencies."
arguments:
  - name: track_id
    description: "The track ID to execute in parallel"
    required: true
user_invocable: true
---

# /parallel-dispatcher — Parallel Task Execution

Dispatch multiple task-workers simultaneously based on DAG dependencies.

## Usage

```bash
/parallel-dispatcher <track-id>
```

## Your Task

You ARE the parallel-dispatcher agent. Coordinate parallel execution.

### 1. Parse DAG from Plan

Read `conductor/tracks/{track_id}/plan.md` and extract the DAG section.

### 2. Initialize Message Bus

```bash
mkdir -p .message-bus/events
echo "{}" > .message-bus/locks.json
echo "{}" > .message-bus/worker-status.json
```

### 3. Find Ready Tasks

Tasks are ready when all their `depends_on` tasks are complete.

### 4. Dispatch Workers in Parallel

Spawn multiple Claude sessions for conflict-free tasks:

```bash
# Spawn parallel workers (max 5 concurrent)
claude --print "/task-worker {track_id} 1.1" &
claude --print "/task-worker {track_id} 1.2" &
claude --print "/task-worker {track_id} 2.1" &

# Wait for batch to complete
wait
```

### 5. Monitor Progress

```bash
# Check for completion events
ls .message-bus/events/TASK_COMPLETE_*.event
ls .message-bus/events/TASK_FAILED_*.event
```

### 6. Handle Failures

- Isolate failed tasks
- Continue with unblocked tasks
- Mark failed tasks for FIX step

### 7. Repeat Until Done

Find next batch of ready tasks and dispatch.

## Worker Pool Limits

- Maximum 5 concurrent workers
- 30-minute timeout per worker
- Heartbeat required every 5 minutes

## Output

```
PARALLEL EXECUTION COMPLETE
WORKERS SPAWNED: X
TASKS COMPLETED: Y
TASKS FAILED: Z
```

## State Update

After all parallel groups complete:
- Set `current_step = "EVALUATE_EXECUTION"`
- Set `step_status = "NOT_STARTED"`

## Message Bus

```bash
echo "PASS" > .message-bus/events/PARALLEL_COMPLETE_{track_id}.event
```

## Reference

Full agent instructions: `.claude/agents/parallel-dispatcher.md`
