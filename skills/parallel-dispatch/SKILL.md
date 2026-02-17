---
name: parallel-dispatch
description: "Parallel execution engine for dispatching worker agents. Used by conductor-orchestrator to spawn multiple workers simultaneously from DAG parallel groups. Handles dispatch, monitoring, aggregation, and failure recovery."
---

# Parallel Dispatch Protocol

Engine for executing DAG tasks in parallel using worker agents.

## Core Concepts

### Parallel Groups
Tasks from the DAG that can execute simultaneously:
- Same topological level (no dependencies between them)
- Either conflict-free (no shared files) or with coordination strategy

### Worker Pool
Maximum 5 concurrent workers to prevent context overflow:
- Each worker is an ephemeral agent created by agent-factory
- Workers coordinate via message bus
- 30-minute timeout with heartbeat monitoring

## Dispatch Protocol

### 1. Parse DAG for Parallel Groups

```python
def get_executable_parallel_groups(dag: dict, completed: set) -> list:
    """
    Get parallel groups that are ready to execute.
    A group is ready if all dependencies are completed.
    """
    ready_groups = []

    for pg in dag.get("parallel_groups", []):
        # Check if all tasks in group have met dependencies
        all_ready = True
        for task_id in pg["tasks"]:
            task = next((n for n in dag["nodes"] if n["id"] == task_id), None)
            if not task:
                continue

            # Check if all dependencies completed
            for dep in task.get("depends_on", []):
                if dep not in completed:
                    all_ready = False
                    break

            if not all_ready:
                break

        if all_ready:
            # Check no tasks in group are already completed
            if not any(t in completed for t in pg["tasks"]):
                ready_groups.append(pg)

    return ready_groups
```

### 2. Create Workers for Parallel Group

```python
def dispatch_parallel_group(
    parallel_group: dict,
    dag: dict,
    track_id: str,
    bus_path: str
) -> list:
    """
    Dispatch all workers for a parallel group.
    Returns list of dispatched worker handles.
    """
    from agent_factory import create_workers_for_parallel_group, dispatch_workers

    # 1. Create worker agents
    workers = create_workers_for_parallel_group(
        parallel_group, dag, track_id, bus_path
    )

    # 2. Check pool capacity
    active_workers = count_active_workers(bus_path)
    if active_workers + len(workers) > 5:
        # Split into batches
        batch_size = 5 - active_workers
        workers = workers[:batch_size]

    # 3. Dispatch workers via parallel Task calls
    handles = dispatch_workers(workers)

    # 4. Log dispatch
    for worker in workers:
        post_message(bus_path, "WORKER_DISPATCHED", "orchestrator", {
            "worker_id": worker["worker_id"],
            "task_id": worker["task_id"],
            "parallel_group": parallel_group["id"]
        })

    return handles
```

### 3. Monitor Worker Progress

```python
async def monitor_parallel_group(
    parallel_group: dict,
    workers: list,
    bus_path: str,
    timeout_minutes: int = 60
) -> dict:
    """
    Monitor workers until all complete or fail.
    Returns aggregated results.
    """
    import asyncio
    from datetime import datetime, timedelta

    start_time = datetime.utcnow()
    timeout = timedelta(minutes=timeout_minutes)
    pending_tasks = set(pg["tasks"] for pg in [parallel_group])
    completed_tasks = set()
    failed_tasks = {}

    while pending_tasks and (datetime.utcnow() - start_time) < timeout:
        # Check for completions
        for task_id in list(pending_tasks):
            event_file = f"{bus_path}/events/TASK_COMPLETE_{task_id}.event"
            if os.path.exists(event_file):
                pending_tasks.remove(task_id)
                completed_tasks.add(task_id)
                # Get completion details
                msgs = read_messages(bus_path, msg_type="TASK_COMPLETE")
                for msg in msgs:
                    if msg["payload"]["task_id"] == task_id:
                        # Log success
                        break

        # Check for failures
        for task_id in list(pending_tasks):
            event_file = f"{bus_path}/events/TASK_FAILED_{task_id}.event"
            if os.path.exists(event_file):
                pending_tasks.remove(task_id)
                # Get failure details
                msgs = read_messages(bus_path, msg_type="TASK_FAILED")
                for msg in msgs:
                    if msg["payload"]["task_id"] == task_id:
                        failed_tasks[task_id] = msg["payload"]["error"]
                        break

        # Check for stale workers (no heartbeat)
        stale = check_stale_workers(bus_path, threshold_minutes=10)
        for stale_worker in stale:
            task_id = stale_worker["task_id"]
            if task_id in pending_tasks:
                failed_tasks[task_id] = f"Worker stale: no heartbeat for {stale_worker['minutes_stale']} min"
                pending_tasks.remove(task_id)

        # Check for deadlocks
        deadlock_cycle = detect_deadlock(bus_path)
        if deadlock_cycle:
            for worker_id in deadlock_cycle:
                # Find task for this worker
                status = get_worker_status(bus_path, worker_id)
                if status and status["task_id"] in pending_tasks:
                    failed_tasks[status["task_id"]] = f"Deadlock detected in cycle: {deadlock_cycle}"
                    pending_tasks.remove(status["task_id"])

        await asyncio.sleep(5)

    # Handle timeout
    for task_id in pending_tasks:
        failed_tasks[task_id] = "Timeout: task did not complete within time limit"

    return {
        "completed": list(completed_tasks),
        "failed": failed_tasks,
        "success": len(failed_tasks) == 0
    }
```

## Failure Handling

### Failure Isolation

When one worker fails, isolate the failure:

```python
def handle_worker_failure(
    failed_task_id: str,
    dag: dict,
    bus_path: str
) -> dict:
    """
    Handle a failed worker. Isolate failure and continue with independent tasks.
    Returns impact analysis.
    """

    # 1. Find tasks that depend on the failed task
    blocked_tasks = []
    for node in dag["nodes"]:
        if failed_task_id in node.get("depends_on", []):
            blocked_tasks.append(node["id"])

    # 2. Recursively find all downstream tasks
    def find_all_downstream(task_id, visited=None):
        if visited is None:
            visited = set()
        if task_id in visited:
            return []
        visited.add(task_id)

        downstream = []
        for node in dag["nodes"]:
            if task_id in node.get("depends_on", []):
                downstream.append(node["id"])
                downstream.extend(find_all_downstream(node["id"], visited))
        return downstream

    all_blocked = set(blocked_tasks)
    for task in blocked_tasks:
        all_blocked.update(find_all_downstream(task))

    # 3. Mark blocked tasks
    for task_id in all_blocked:
        post_message(bus_path, "TASK_BLOCKED", "orchestrator", {
            "task_id": task_id,
            "blocked_by": failed_task_id,
            "reason": "Upstream task failed"
        })

    # 4. Find tasks that can still proceed
    all_tasks = set(n["id"] for n in dag["nodes"])
    can_proceed = all_tasks - all_blocked - {failed_task_id}

    return {
        "failed_task": failed_task_id,
        "blocked_tasks": list(all_blocked),
        "can_proceed": list(can_proceed),
        "needs_fix": True
    }
```

### Recovery Strategy

```python
def attempt_recovery(
    failure_result: dict,
    dag: dict,
    track_id: str,
    bus_path: str,
    max_retries: int = 2
) -> dict:
    """
    Attempt to recover from failure.
    """
    failed_task = failure_result["failed_task"]

    # 1. Check retry count
    retry_key = f"retry_{failed_task}"
    retries = get_coordination_log_count(bus_path, retry_key)

    if retries >= max_retries:
        return {
            "action": "ESCALATE",
            "reason": f"Task {failed_task} failed {retries} times, needs manual intervention"
        }

    # 2. Log retry attempt
    log_coordination(bus_path, {
        "type": retry_key,
        "attempt": retries + 1,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    })

    # 3. Re-dispatch failed task
    task = next((n for n in dag["nodes"] if n["id"] == failed_task), None)
    if task:
        worker = create_worker_agent(task, track_id, bus_path)
        dispatch_workers([worker])

        return {
            "action": "RETRY",
            "task": failed_task,
            "attempt": retries + 1
        }

    return {"action": "SKIP", "reason": "Task not found in DAG"}
```

## Deadlock Detection & Resolution

```python
def resolve_deadlock(
    deadlock_cycle: list,
    bus_path: str
) -> dict:
    """
    Resolve a detected deadlock by releasing locks from oldest worker.
    """
    if not deadlock_cycle:
        return {"resolved": True, "action": "none"}

    # Find oldest worker in cycle (longest waiting)
    oldest_worker = None
    oldest_time = None

    for worker_id in deadlock_cycle:
        status = get_worker_status(bus_path, worker_id)
        if status:
            started = datetime.fromisoformat(status.get("started_at", "").replace("Z", ""))
            if oldest_time is None or started < oldest_time:
                oldest_time = started
                oldest_worker = worker_id

    if oldest_worker:
        # Release all locks held by this worker
        release_all_locks_for_worker(bus_path, oldest_worker)

        # Post resolution message
        post_message(bus_path, "DEADLOCK_RESOLVED", "orchestrator", {
            "cycle": deadlock_cycle,
            "victim": oldest_worker,
            "action": "released_locks"
        })

        return {
            "resolved": True,
            "action": "released_locks",
            "victim": oldest_worker
        }

    return {"resolved": False, "action": "manual_intervention_needed"}
```

## Aggregating Results

```python
def aggregate_parallel_group_results(
    parallel_group: dict,
    bus_path: str
) -> dict:
    """
    Aggregate results from completed parallel group.
    """
    results = {
        "parallel_group_id": parallel_group["id"],
        "tasks": {},
        "files_modified": [],
        "commits": []
    }

    for task_id in parallel_group["tasks"]:
        # Get completion message
        msgs = read_messages(bus_path, msg_type="TASK_COMPLETE")
        for msg in msgs:
            if msg["payload"]["task_id"] == task_id:
                results["tasks"][task_id] = {
                    "status": "completed",
                    "commit_sha": msg["payload"].get("commit_sha"),
                    "files": msg["payload"].get("files_modified", [])
                }
                results["files_modified"].extend(msg["payload"].get("files_modified", []))
                if msg["payload"].get("commit_sha"):
                    results["commits"].append(msg["payload"]["commit_sha"])
                break
        else:
            # Check for failure
            fail_msgs = read_messages(bus_path, msg_type="TASK_FAILED")
            for msg in fail_msgs:
                if msg["payload"]["task_id"] == task_id:
                    results["tasks"][task_id] = {
                        "status": "failed",
                        "error": msg["payload"].get("error")
                    }
                    break

    results["all_succeeded"] = all(
        t.get("status") == "completed"
        for t in results["tasks"].values()
    )

    return results
```

## Full Parallel Execution Loop

```python
async def execute_parallel_phase(
    dag: dict,
    track_id: str,
    bus_path: str,
    metadata: dict
) -> dict:
    """
    Execute all parallel groups from a DAG phase.
    Main entry point for parallel execution.
    """
    completed_tasks = set(metadata.get("completed_tasks", []))
    phase_results = {
        "parallel_groups_executed": [],
        "all_tasks_completed": [],
        "failed_tasks": {},
        "success": True
    }

    while True:
        # Get next ready parallel groups
        ready_groups = get_executable_parallel_groups(dag, completed_tasks)

        if not ready_groups:
            # No more groups to execute
            break

        for pg in ready_groups:
            # Skip if all tasks already completed
            if all(t in completed_tasks for t in pg["tasks"]):
                continue

            # Dispatch workers
            workers = dispatch_parallel_group(pg, dag, track_id, bus_path)

            # Monitor until completion
            result = await monitor_parallel_group(pg, workers, bus_path)

            # Update completed set
            completed_tasks.update(result["completed"])
            phase_results["all_tasks_completed"].extend(result["completed"])

            # Handle failures
            if result["failed"]:
                phase_results["failed_tasks"].update(result["failed"])
                phase_results["success"] = False

                # Attempt recovery or continue with independent tasks
                for failed_task, error in result["failed"].items():
                    impact = handle_worker_failure(failed_task, dag, bus_path)
                    recovery = attempt_recovery(impact, dag, track_id, bus_path)

                    if recovery["action"] == "ESCALATE":
                        phase_results["escalate"] = True
                        phase_results["escalate_reason"] = recovery["reason"]

            phase_results["parallel_groups_executed"].append(pg["id"])

            # Cleanup workers
            for worker in workers:
                cleanup_worker(worker["worker_id"])

        # Update metadata
        metadata["parallel_state"]["parallel_groups_completed"].extend(
            [pg["id"] for pg in ready_groups]
        )
        save_metadata(track_id, metadata)

    return phase_results
```

## Usage in Orchestrator

```python
# In conductor-orchestrator PARALLEL_EXECUTE step:

async def step_parallel_execute(track_id: str, metadata: dict):
    # 1. Parse DAG from plan.md
    dag = parse_dag_from_plan(track_id)

    # 2. Initialize message bus
    bus_path = init_message_bus(f"conductor/tracks/{track_id}")

    # 3. Execute all parallel groups
    result = await execute_parallel_phase(dag, track_id, bus_path, metadata)

    # 4. Update metadata
    metadata["loop_state"]["parallel_state"]["total_workers_spawned"] = ...
    metadata["loop_state"]["parallel_state"]["completed_workers"] = len(result["all_tasks_completed"])
    metadata["loop_state"]["parallel_state"]["failed_workers"] = len(result["failed_tasks"])

    # 5. Determine next step
    if result["success"]:
        return "EVALUATE_EXECUTION"
    elif result.get("escalate"):
        return "ESCALATE_TO_USER"
    else:
        return "FIX"
```

## Worker Coordination Patterns

### File Lock Coordination

For parallel groups with shared files:

```python
# Worker before modifying shared file:
if not acquire_lock(bus_path, "src/shared/file.ts", worker_id):
    # Post blocked message and wait
    post_message(bus_path, "BLOCKED", worker_id, {
        "task_id": task_id,
        "waiting_for": "FILE_UNLOCK_src/shared/file.ts",
        "resource": "src/shared/file.ts"
    })

    # Poll for unlock
    if wait_for_event(bus_path, "FILE_UNLOCK_*.event", timeout=300):
        # Retry lock
        acquire_lock(bus_path, "src/shared/file.ts", worker_id)
```

### Dependency Notification

Workers notify dependents when complete:

```python
# Worker on completion:
unblocked_tasks = find_tasks_unblocked_by(task_id, dag)

post_message(bus_path, "TASK_COMPLETE", worker_id, {
    "task_id": task_id,
    "commit_sha": commit_sha,
    "files_modified": files,
    "unblocks": unblocked_tasks
})

# Create event files for each unblocked task
for unblocked in unblocked_tasks:
    Path(f"{bus_path}/events/DEP_READY_{unblocked}.event").touch()
```
