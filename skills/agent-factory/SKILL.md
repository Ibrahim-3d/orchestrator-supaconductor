---
name: agent-factory
description: "Creates specialized worker agents dynamically from templates. Use when orchestrator needs to spawn task-specific workers for parallel execution. Handles agent lifecycle: create -> execute -> cleanup."
---

# Agent Factory -- Dynamic Worker Creation

Creates ephemeral worker agents from templates, specializing them based on task type.

## Worker Creation Flow

```
Task from DAG -> Determine Type -> Select Template -> Substitute Placeholders -> Spawn Worker
```

## Template Selection

| Task Type | Template | Specialization |
|-----------|----------|---------------|
| `code` | `code-worker.template.md` | TDD, code patterns, tests |
| `ui` | `ui-worker.template.md` | Design system, accessibility |
| `integration` | `integration-worker.template.md` | API contracts, error handling |
| `test` | `test-worker.template.md` | Coverage targets, test patterns |
| `docs` | `task-worker.template.md` | Base template |
| `config` | `task-worker.template.md` | Base template |

## CreateWorkerAgent Procedure

```python
def create_worker_agent(task: dict, track_id: str, message_bus_path: str) -> dict:
    """
    Create a specialized worker agent for a task.

    Args:
        task: Task node from DAG (id, name, type, files, depends_on, acceptance)
        track_id: Current track identifier
        message_bus_path: Path to message bus directory

    Returns:
        dict with worker_id, skill_path, prompt
    """

    # 1. Generate unique worker ID
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    worker_id = f"worker-{task['id']}-{timestamp}"

    # 2. Select template based on task type
    task_type = task.get('type', 'code')
    template_map = {
        'code': 'code-worker.template.md',
        'ui': 'ui-worker.template.md',
        'integration': 'integration-worker.template.md',
        'test': 'test-worker.template.md',
    }
    template_name = template_map.get(task_type, 'task-worker.template.md')
    template_path = f".claude/skills/worker-templates/{template_name}"

    # 3. Read template
    template = read_file(template_path)

    # 4. Prepare substitution values
    substitutions = {
        '{task_id}': task['id'],
        '{task_name}': task['name'],
        '{track_id}': track_id,
        '{phase}': str(task.get('phase', 1)),
        '{files}': format_list(task.get('files', [])),
        '{depends_on}': format_list(task.get('depends_on', [])),
        '{acceptance}': task.get('acceptance', 'Complete the task as specified'),
        '{message_bus_path}': message_bus_path,
        '{timestamp}': timestamp,
        '{worker_id}': worker_id,
        '{unblocks}': format_list(find_unblocked_tasks(task['id'])),
    }

    # 5. Substitute placeholders
    worker_skill = template
    for placeholder, value in substitutions.items():
        worker_skill = worker_skill.replace(placeholder, value)

    # 6. Add task-specific instructions
    if task.get('task_instructions'):
        worker_skill = worker_skill.replace(
            '{task_instructions}',
            task['task_instructions']
        )
    else:
        worker_skill = worker_skill.replace(
            '{task_instructions}',
            f"Implement: {task['name']}\n\nAcceptance: {task.get('acceptance', 'N/A')}"
        )

    # 7. Add base protocol
    base_protocol = read_file(".claude/skills/worker-templates/task-worker.template.md")
    base_protocol_section = extract_section(base_protocol, "## Execution Protocol")
    worker_skill = worker_skill.replace('{base_worker_protocol}', base_protocol_section)

    # 8. Create worker skill directory (ephemeral)
    worker_skill_path = f".claude/skills/workers/{worker_id}/SKILL.md"
    os.makedirs(os.path.dirname(worker_skill_path), exist_ok=True)
    write_file(worker_skill_path, worker_skill)

    # 9. Generate dispatch prompt
    dispatch_prompt = f"""You are worker agent {worker_id}.

Your task: {task['name']} (Task {task['id']})

MESSAGE BUS: {message_bus_path}

Follow your worker skill instructions at: {worker_skill_path}

Protocol:
1. Check dependencies via message bus
2. Acquire file locks before modifying
3. Post progress every 5 min
4. Post TASK_COMPLETE when done

Execute autonomously. Do NOT wait for user input."""

    return {
        'worker_id': worker_id,
        'skill_path': worker_skill_path,
        'prompt': dispatch_prompt,
        'task_id': task['id'],
        'task_type': task_type
    }
```

## Batch Worker Creation

For parallel groups, create all workers at once:

```python
def create_workers_for_parallel_group(
    parallel_group: dict,
    dag: dict,
    track_id: str,
    message_bus_path: str
) -> list:
    """
    Create workers for all tasks in a parallel group.

    Args:
        parallel_group: Parallel group definition (id, tasks, conflict_free)
        dag: Full DAG with all task nodes
        track_id: Current track identifier
        message_bus_path: Path to message bus

    Returns:
        List of worker definitions ready for dispatch
    """

    workers = []

    for task_id in parallel_group['tasks']:
        # Find task in DAG
        task = next((n for n in dag['nodes'] if n['id'] == task_id), None)
        if not task:
            continue

        # Create worker
        worker = create_worker_agent(task, track_id, message_bus_path)

        # Add coordination info if not conflict-free
        if not parallel_group.get('conflict_free', True):
            worker['requires_coordination'] = True
            worker['shared_resources'] = parallel_group.get('shared_resources', [])

        workers.append(worker)

    return workers
```

## Worker Dispatch

Dispatch workers via parallel Task calls:

```python
def dispatch_workers(workers: list) -> list:
    """
    Dispatch multiple workers in parallel using Task tool.

    Returns list of Task call results.
    """

    # Create Task calls for all workers
    task_calls = []
    for worker in workers:
        task_calls.append({
            'subagent_type': 'general-purpose',
            'description': f"Execute {worker['task_id']}: {worker.get('task_name', 'task')}",
            'prompt': worker['prompt'],
            'run_in_background': True  # Run in background for true parallelism
        })

    # Dispatch all at once (Claude Code handles parallel calls)
    results = []
    for call in task_calls:
        result = Task(**call)
        results.append(result)

    return results
```

## Worker Cleanup

After task completion, cleanup worker artifacts:

```python
def cleanup_worker(worker_id: str):
    """
    Remove ephemeral worker skill directory.
    Called by orchestrator after worker reports completion.
    """

    worker_skill_path = f".claude/skills/workers/{worker_id}"

    if os.path.exists(worker_skill_path):
        shutil.rmtree(worker_skill_path)

    # Log cleanup
    print(f"Cleaned up worker: {worker_id}")
```

## Cleanup All Workers

After parallel group completes:

```python
def cleanup_parallel_group_workers(parallel_group_id: str, workers: list):
    """
    Cleanup all workers from a completed parallel group.
    """

    for worker in workers:
        cleanup_worker(worker['worker_id'])

    # Remove workers directory if empty
    workers_dir = ".claude/skills/workers"
    if os.path.exists(workers_dir) and not os.listdir(workers_dir):
        os.rmdir(workers_dir)
```

## Helper Functions

```python
def format_list(items: list) -> str:
    """Format list for template substitution."""
    if not items:
        return "None"
    return "\n".join(f"- {item}" for item in items)


def find_unblocked_tasks(task_id: str, dag: dict) -> list:
    """Find tasks that will be unblocked when task_id completes."""
    unblocked = []
    for node in dag.get('nodes', []):
        if task_id in node.get('depends_on', []):
            # Check if this is the only remaining dependency
            remaining_deps = [d for d in node['depends_on'] if d != task_id]
            if not remaining_deps:
                unblocked.append(node['id'])
    return unblocked


def extract_section(content: str, section_header: str) -> str:
    """Extract a section from markdown content."""
    lines = content.split('\n')
    in_section = False
    section_lines = []

    for line in lines:
        if line.startswith(section_header):
            in_section = True
            continue
        elif in_section and line.startswith('## '):
            break
        elif in_section:
            section_lines.append(line)

    return '\n'.join(section_lines).strip()
```

## Integration with Orchestrator

The orchestrator calls the agent factory during PARALLEL_EXECUTE:

```python
# In conductor-orchestrator

async def execute_parallel_phase(phase: Phase, dag: dict):
    # 1. Get parallel groups for this phase
    parallel_groups = [
        pg for pg in dag.get('parallel_groups', [])
        if all(task_in_phase(t, phase) for t in pg['tasks'])
    ]

    for pg in parallel_groups:
        # 2. Create workers via agent factory
        workers = create_workers_for_parallel_group(
            pg, dag, track_id, message_bus_path
        )

        # 3. Dispatch workers in parallel
        results = dispatch_workers(workers)

        # 4. Monitor message bus for completion
        await wait_for_group_completion(pg, message_bus_path)

        # 5. Cleanup workers
        cleanup_parallel_group_workers(pg['id'], workers)
```

## Worker Lifecycle

```
+---------------------------------------------------------------+
|                      WORKER LIFECYCLE                          |
|                                                                |
|  1. CREATE                                                     |
|     Agent Factory -> Template -> Substitution -> Skill Dir     |
|                                                                |
|  2. DISPATCH                                                   |
|     Orchestrator -> Task(prompt, run_in_background) -> Worker  |
|                                                                |
|  3. EXECUTE                                                    |
|     Worker -> Check Deps -> Lock Files -> Implement -> Commit  |
|                                                                |
|  4. REPORT                                                     |
|     Worker -> Message Bus -> TASK_COMPLETE/TASK_FAILED         |
|                                                                |
|  5. CLEANUP                                                    |
|     Orchestrator -> cleanup_worker() -> Remove Skill Dir       |
|                                                                |
+---------------------------------------------------------------+
```

## Error Handling

```python
def handle_worker_failure(worker: dict, error: str, message_bus_path: str):
    """
    Handle worker failure gracefully.

    1. Post failure to message bus
    2. Release any held locks
    3. Cleanup worker artifacts
    4. Notify orchestrator
    """

    # Post failure message
    post_message(message_bus_path, "TASK_FAILED", worker['worker_id'], {
        "task_id": worker['task_id'],
        "error": error
    })

    # Release all locks held by this worker
    release_all_locks_for_worker(message_bus_path, worker['worker_id'])

    # Cleanup worker
    cleanup_worker(worker['worker_id'])
```
