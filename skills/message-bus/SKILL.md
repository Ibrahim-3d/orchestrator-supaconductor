---
name: message-bus
description: "File-based message queue for inter-agent coordination. Used by workers AND board directors to communicate. Provides: progress updates, task completion signals, file locking, board deliberation. Core infrastructure for parallel execution."
---

# Message Bus -- Inter-Agent Communication Protocol

File-based message queue enabling workers and board directors to coordinate via shared state.

## Directory Structure

```
conductor/tracks/{track}/.message-bus/
├── queue.jsonl           # Append-only message log (all messages)
├── locks.json            # Current file locks
├── worker-status.json    # Worker heartbeats and states
├── events/               # Signal files for polling
│   ├── TASK_COMPLETE_1.1.event
│   └── FILE_UNLOCK_*.event
└── board/                # Board deliberation sessions
    ├── session-{ts}.json # Session metadata
    ├── assessments.json  # Director assessments (Phase 1)
    ├── discussion.jsonl  # Discussion messages (Phase 2)
    └── votes.json        # Final votes (Phase 3)
```

## Message Types

### Worker Messages

| Type | Purpose | Payload |
|------|---------|---------|
| `PROGRESS` | Task progress update | `{ task_id, progress_pct, current_subtask }` |
| `TASK_COMPLETE` | Task finished | `{ task_id, commit_sha, files_modified, unblocks[] }` |
| `TASK_FAILED` | Task failed | `{ task_id, error, stack_trace }` |
| `FILE_LOCK` | Acquire file lock | `{ filepath, lock_type, expires_at }` |
| `FILE_UNLOCK` | Release file lock | `{ filepath }` |
| `BLOCKED` | Waiting on dependency | `{ task_id, waiting_for, resource }` |

### Board Messages

| Type | Purpose | Payload |
|------|---------|---------|
| `BOARD_ASSESS` | Director assessment | `{ director, verdict, score, concerns[], recommendations[] }` |
| `BOARD_DISCUSS` | Discussion message | `{ from, to, type, message, changes_my_verdict }` |
| `BOARD_VOTE` | Final vote | `{ director, final_verdict, confidence, conditions[] }` |
| `BOARD_RESOLVE` | Aggregated decision | `{ verdict, vote_summary, conditions[], dissent[] }` |

## Message Format

All messages follow this structure:

```json
{
  "id": "msg-{uuid}",
  "type": "PROGRESS | TASK_COMPLETE | BOARD_ASSESS | ...",
  "source": "worker-1.1-xxx | CA | orchestrator",
  "timestamp": "2026-02-01T12:00:00Z",
  "payload": { ... }
}
```

## Worker Protocol

### Posting Messages

```python
def post_message(bus_path: str, msg_type: str, source: str, payload: dict):
    message = {
        "id": f"msg-{uuid4()}",
        "type": msg_type,
        "source": source,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "payload": payload
    }

    # Append to queue (atomic via file locking)
    with open(f"{bus_path}/queue.jsonl", "a") as f:
        f.write(json.dumps(message) + "\n")

    # Create event file for polling
    if msg_type in ["TASK_COMPLETE", "FILE_UNLOCK", "BOARD_RESOLVE"]:
        event_file = f"{bus_path}/events/{msg_type}_{payload.get('task_id', 'all')}.event"
        Path(event_file).touch()
```

### Reading Messages

```python
def read_messages(bus_path: str, since: str = None, msg_type: str = None) -> list:
    messages = []
    with open(f"{bus_path}/queue.jsonl", "r") as f:
        for line in f:
            msg = json.loads(line)
            if since and msg["timestamp"] < since:
                continue
            if msg_type and msg["type"] != msg_type:
                continue
            messages.append(msg)
    return messages
```

### Polling for Events

```python
def wait_for_event(bus_path: str, event_pattern: str, timeout: int = 300) -> bool:
    """Wait for event file to appear. Returns True if found, False if timeout."""
    import glob
    import time

    start = time.time()
    while time.time() - start < timeout:
        matches = glob.glob(f"{bus_path}/events/{event_pattern}")
        if matches:
            return True
        time.sleep(1)
    return False
```

## File Lock Protocol

### Acquiring Locks

```python
def acquire_lock(bus_path: str, filepath: str, worker_id: str) -> bool:
    locks_file = f"{bus_path}/locks.json"

    # Read current locks
    locks = json.load(open(locks_file)) if os.path.exists(locks_file) else {}

    # Check if already locked
    if filepath in locks:
        existing = locks[filepath]
        # Check if expired (30 min timeout)
        if datetime.fromisoformat(existing["expires_at"]) > datetime.utcnow():
            if existing["worker_id"] != worker_id:
                return False  # Locked by another worker

    # Acquire lock
    locks[filepath] = {
        "worker_id": worker_id,
        "acquired_at": datetime.utcnow().isoformat() + "Z",
        "expires_at": (datetime.utcnow() + timedelta(minutes=30)).isoformat() + "Z"
    }

    with open(locks_file, "w") as f:
        json.dump(locks, f, indent=2)

    # Post lock message
    post_message(bus_path, "FILE_LOCK", worker_id, {"filepath": filepath})
    return True
```

### Releasing Locks

```python
def release_lock(bus_path: str, filepath: str, worker_id: str):
    locks_file = f"{bus_path}/locks.json"
    locks = json.load(open(locks_file)) if os.path.exists(locks_file) else {}

    if filepath in locks and locks[filepath]["worker_id"] == worker_id:
        del locks[filepath]
        with open(locks_file, "w") as f:
            json.dump(locks, f, indent=2)

        # Post unlock message and event
        post_message(bus_path, "FILE_UNLOCK", worker_id, {"filepath": filepath})
```

## Worker Status Heartbeat

Workers post heartbeats every 5 minutes:

```python
def update_worker_status(bus_path: str, worker_id: str, task_id: str, status: str, progress: int):
    status_file = f"{bus_path}/worker-status.json"
    statuses = json.load(open(status_file)) if os.path.exists(status_file) else {}

    statuses[worker_id] = {
        "task_id": task_id,
        "status": status,  # "RUNNING" | "COMPLETE" | "FAILED" | "BLOCKED"
        "progress_pct": progress,
        "last_heartbeat": datetime.utcnow().isoformat() + "Z"
    }

    with open(status_file, "w") as f:
        json.dump(statuses, f, indent=2)
```

## Board Deliberation Protocol

### Phase 1: Assessment

Each director posts their assessment:

```python
def post_board_assessment(bus_path: str, director: str, assessment: dict):
    board_path = f"{bus_path}/board"

    # Read existing assessments
    assess_file = f"{board_path}/assessments.json"
    assessments = json.load(open(assess_file)) if os.path.exists(assess_file) else {}

    # Add this director's assessment
    assessments[director] = assessment

    with open(assess_file, "w") as f:
        json.dump(assessments, f, indent=2)

    # Post to main queue too
    post_message(bus_path, "BOARD_ASSESS", director, assessment)
```

### Phase 2: Discussion

Directors respond to each other:

```python
def post_board_discussion(bus_path: str, from_dir: str, to_dir: str,
                          msg_type: str, message: str, changes_verdict: bool):
    board_path = f"{bus_path}/board"

    discussion_msg = {
        "from": from_dir,
        "to": to_dir,
        "type": msg_type,  # "CHALLENGE" | "AGREE" | "QUESTION" | "CLARIFY"
        "message": message,
        "changes_my_verdict": changes_verdict,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    # Append to discussion log
    with open(f"{board_path}/discussion.jsonl", "a") as f:
        f.write(json.dumps(discussion_msg) + "\n")

    # Post to main queue
    post_message(bus_path, "BOARD_DISCUSS", from_dir, discussion_msg)
```

### Phase 3: Voting

Directors cast final votes:

```python
def post_board_vote(bus_path: str, director: str, verdict: str,
                    confidence: float, conditions: list):
    board_path = f"{bus_path}/board"

    votes_file = f"{board_path}/votes.json"
    votes = json.load(open(votes_file)) if os.path.exists(votes_file) else {}

    votes[director] = {
        "final_verdict": verdict,  # "APPROVE" | "REJECT"
        "confidence": confidence,  # 0.0 - 1.0
        "conditions": conditions,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    with open(votes_file, "w") as f:
        json.dump(votes, f, indent=2)

    post_message(bus_path, "BOARD_VOTE", director, votes[director])
```

### Phase 4: Resolution

Orchestrator aggregates votes:

```python
def resolve_board_vote(bus_path: str) -> dict:
    board_path = f"{bus_path}/board"
    votes = json.load(open(f"{board_path}/votes.json"))

    approve_count = sum(1 for v in votes.values() if v["final_verdict"] == "APPROVE")
    reject_count = len(votes) - approve_count

    # Determine verdict
    if approve_count >= 4:
        verdict = "APPROVED"
    elif approve_count == 3:
        verdict = "APPROVED_WITH_REVIEW"
    elif reject_count >= 4:
        verdict = "REJECTED"
    elif reject_count == 3:
        verdict = "REJECTED"
    else:
        verdict = "ESCALATE"

    # Collect conditions
    all_conditions = []
    for director, vote in votes.items():
        for cond in vote.get("conditions", []):
            all_conditions.append(f"{cond} ({director})")

    resolution = {
        "verdict": verdict,
        "vote_summary": {d: v["final_verdict"] for d, v in votes.items()},
        "conditions": all_conditions,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

    # Post resolution
    post_message(bus_path, "BOARD_RESOLVE", "orchestrator", resolution)

    # Create event file
    Path(f"{bus_path}/events/BOARD_RESOLVE.event").touch()

    return resolution
```

## Deadlock Detection

Monitor for circular waits:

```python
def detect_deadlock(bus_path: str) -> list:
    """Returns list of workers in deadlock cycle, or empty if none."""
    status_file = f"{bus_path}/worker-status.json"
    locks_file = f"{bus_path}/locks.json"

    statuses = json.load(open(status_file)) if os.path.exists(status_file) else {}
    locks = json.load(open(locks_file)) if os.path.exists(locks_file) else {}

    # Build wait-for graph
    # worker -> worker it's waiting for
    wait_for = {}

    # Find blocked workers
    blocked_msgs = read_messages(bus_path, msg_type="BLOCKED")
    for msg in blocked_msgs:
        blocker = msg["payload"].get("waiting_for")
        if blocker:
            wait_for[msg["source"]] = blocker

    # Detect cycles using DFS
    def find_cycle(start, visited, path):
        if start in path:
            return path[path.index(start):]
        if start in visited:
            return []
        visited.add(start)
        path.append(start)
        if start in wait_for:
            cycle = find_cycle(wait_for[start], visited, path)
            if cycle:
                return cycle
        path.pop()
        return []

    visited = set()
    for worker in wait_for:
        cycle = find_cycle(worker, visited, [])
        if cycle:
            return cycle

    return []
```

## Initialization

Initialize message bus for a track:

```python
def init_message_bus(track_path: str):
    bus_path = f"{track_path}/.message-bus"

    # Create directories
    os.makedirs(bus_path, exist_ok=True)
    os.makedirs(f"{bus_path}/events", exist_ok=True)
    os.makedirs(f"{bus_path}/board", exist_ok=True)

    # Initialize files
    Path(f"{bus_path}/queue.jsonl").touch()

    with open(f"{bus_path}/locks.json", "w") as f:
        json.dump({}, f)

    with open(f"{bus_path}/worker-status.json", "w") as f:
        json.dump({}, f)

    with open(f"{bus_path}/board/assessments.json", "w") as f:
        json.dump({}, f)

    with open(f"{bus_path}/board/votes.json", "w") as f:
        json.dump({}, f)

    Path(f"{bus_path}/board/discussion.jsonl").touch()
```

## Usage in Worker Agents

```markdown
## Worker Protocol

1. **On Start**:
   - Read message bus for TASK_COMPLETE events of dependencies
   - Verify all dependencies are met
   - Update worker-status.json with RUNNING

2. **Before Modifying Files**:
   - Call acquire_lock() for each file
   - If lock fails, post BLOCKED message and wait

3. **During Execution**:
   - Post PROGRESS every 5 minutes
   - Update worker-status.json heartbeat

4. **On Completion**:
   - Release all file locks
   - Post TASK_COMPLETE with commit SHA and files modified
   - Update worker-status.json with COMPLETE

5. **On Failure**:
   - Release all file locks
   - Post TASK_FAILED with error details
   - Update worker-status.json with FAILED
```

## Usage in Board Deliberation

```markdown
## Board Protocol

1. **Phase 1 (ASSESS)**:
   - All 5 directors read proposal
   - Each posts BOARD_ASSESS to assessments.json
   - Wait for all 5 assessments

2. **Phase 2 (DISCUSS)** -- 3 rounds:
   - Directors read others' assessments
   - Post BOARD_DISCUSS messages
   - Respond to challenges and questions

3. **Phase 3 (VOTE)**:
   - Each director posts BOARD_VOTE
   - Include confidence level and conditions

4. **Phase 4 (RESOLVE)**:
   - Orchestrator calls resolve_board_vote()
   - Posts BOARD_RESOLVE
   - Creates event file for completion
```

## Board Session Management

### Creating a Board Session

```python
def create_board_session(bus_path: str, checkpoint: str, proposal: dict) -> str:
    """Initialize a new board session for deliberation."""
    board_path = f"{bus_path}/board"
    session_id = f"board-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

    session = {
        "session_id": session_id,
        "checkpoint": checkpoint,  # "EVALUATE_PLAN" | "EVALUATE_EXECUTION" | "PRE_LAUNCH"
        "status": "ASSESSING",
        "proposal": proposal,
        "directors": ["CA", "CPO", "CSO", "COO", "CXO"],
        "started_at": datetime.utcnow().isoformat() + "Z",
        "phases": {
            "assess": {"status": "IN_PROGRESS", "complete": 0, "of": 5},
            "discuss": {"status": "NOT_STARTED", "rounds": 0, "max_rounds": 3},
            "vote": {"status": "NOT_STARTED", "complete": 0, "of": 5},
            "resolve": {"status": "NOT_STARTED"}
        }
    }

    # Clear previous session data
    with open(f"{board_path}/assessments.json", "w") as f:
        json.dump({}, f, indent=2)
    with open(f"{board_path}/votes.json", "w") as f:
        json.dump({}, f, indent=2)
    Path(f"{board_path}/discussion.jsonl").write_text("")

    # Save session metadata
    with open(f"{board_path}/session-{session_id}.json", "w") as f:
        json.dump(session, f, indent=2)

    return session_id
```

### Checking Phase Completion

```python
def check_board_phase_complete(bus_path: str, session_id: str) -> dict:
    """Check if current board phase is complete and advance if ready."""
    board_path = f"{bus_path}/board"
    session_file = f"{board_path}/session-{session_id}.json"
    session = json.load(open(session_file))

    assessments = json.load(open(f"{board_path}/assessments.json"))
    votes = json.load(open(f"{board_path}/votes.json"))
    discussions = []
    with open(f"{board_path}/discussion.jsonl") as f:
        discussions = [json.loads(l) for l in f if l.strip()]

    result = {"phase": session["status"], "complete": False, "can_advance": False}

    if session["status"] == "ASSESSING":
        session["phases"]["assess"]["complete"] = len(assessments)
        if len(assessments) >= 5:
            result["complete"] = True
            result["can_advance"] = True
            result["next_phase"] = "DISCUSSING"

    elif session["status"] == "DISCUSSING":
        current_round = session["phases"]["discuss"]["rounds"]
        if current_round >= 3:
            result["complete"] = True
            result["can_advance"] = True
            result["next_phase"] = "VOTING"

    elif session["status"] == "VOTING":
        session["phases"]["vote"]["complete"] = len(votes)
        if len(votes) >= 5:
            result["complete"] = True
            result["can_advance"] = True
            result["next_phase"] = "RESOLVING"

    # Save updated session
    with open(session_file, "w") as f:
        json.dump(session, f, indent=2)

    return result
```

### Advancing Board Phase

```python
def advance_board_phase(bus_path: str, session_id: str) -> str:
    """Advance to next deliberation phase."""
    board_path = f"{bus_path}/board"
    session_file = f"{board_path}/session-{session_id}.json"
    session = json.load(open(session_file))

    transitions = {
        "ASSESSING": "DISCUSSING",
        "DISCUSSING": "VOTING",
        "VOTING": "RESOLVING",
        "RESOLVING": "COMPLETE"
    }

    current = session["status"]
    next_phase = transitions.get(current, current)

    session["status"] = next_phase
    session["phases"][next_phase.lower().replace("ing", "")]["status"] = "IN_PROGRESS"

    with open(session_file, "w") as f:
        json.dump(session, f, indent=2)

    return next_phase
```

## Orchestrator Board Integration

### Invoking Board from Orchestrator

```python
async def invoke_board_meeting(
    bus_path: str,
    checkpoint: str,
    proposal: str,
    context: dict
) -> dict:
    """
    Full 4-phase board deliberation.
    Called by orchestrator at EVALUATE_PLAN or EVALUATE_EXECUTION checkpoints.
    """

    # 1. Create session
    session_id = create_board_session(bus_path, checkpoint, {
        "proposal": proposal,
        "context": context
    })

    # 2. Phase 1: ASSESS -- Dispatch all directors in parallel
    director_prompts = {
        "CA": f"Evaluate technical aspects: {proposal}",
        "CPO": f"Evaluate product value: {proposal}",
        "CSO": f"Evaluate security posture: {proposal}",
        "COO": f"Evaluate operational feasibility: {proposal}",
        "CXO": f"Evaluate user experience: {proposal}"
    }

    # Dispatch via parallel Task calls (see agent-factory)
    assessments = await dispatch_board_directors(director_prompts, bus_path)

    # Wait for all assessments
    while check_board_phase_complete(bus_path, session_id)["complete"] == False:
        await asyncio.sleep(5)
    advance_board_phase(bus_path, session_id)

    # 3. Phase 2: DISCUSS -- 3 rounds
    for round_num in range(3):
        await run_discussion_round(bus_path, session_id, round_num)

    advance_board_phase(bus_path, session_id)

    # 4. Phase 3: VOTE -- All directors vote
    await dispatch_final_votes(bus_path, session_id)

    while check_board_phase_complete(bus_path, session_id)["complete"] == False:
        await asyncio.sleep(5)
    advance_board_phase(bus_path, session_id)

    # 5. Phase 4: RESOLVE
    resolution = resolve_board_vote(bus_path)

    return {
        "session_id": session_id,
        "verdict": resolution["verdict"],
        "votes": resolution["vote_summary"],
        "conditions": resolution["conditions"]
    }
```

### Quick Board Review (No Discussion)

```python
async def invoke_board_review(bus_path: str, proposal: str) -> dict:
    """
    Quick board review -- Phase 1 only, no discussion.
    Used for execution quality checks or low-stakes decisions.
    """

    session_id = create_board_session(bus_path, "QUICK_REVIEW", {
        "proposal": proposal,
        "quick_mode": True
    })

    # Dispatch all directors
    await dispatch_board_directors(proposal, bus_path)

    # Wait for assessments
    while check_board_phase_complete(bus_path, session_id)["complete"] == False:
        await asyncio.sleep(5)

    # Aggregate assessments directly (skip discussion and vote)
    board_path = f"{bus_path}/board"
    assessments = json.load(open(f"{board_path}/assessments.json"))

    approve_count = sum(1 for a in assessments.values()
                       if a["verdict"] in ["APPROVE", "CONCERNS"])
    reject_count = len(assessments) - approve_count

    return {
        "session_id": session_id,
        "verdict": "APPROVED" if approve_count >= 3 else "REJECTED",
        "assessments": assessments,
        "consensus": approve_count >= 4
    }
```

## Event-Driven Director Polling

Directors can poll for messages addressed to them:

```python
def get_messages_for_director(bus_path: str, director: str) -> list:
    """Get all discussion messages addressed to this director."""
    board_path = f"{bus_path}/board"

    messages = []
    with open(f"{board_path}/discussion.jsonl") as f:
        for line in f:
            if line.strip():
                msg = json.loads(line)
                if msg["to"] == director or msg["to"] == "ALL":
                    messages.append(msg)

    return messages
```

## Board Session Files

```
.message-bus/board/
├── session-board-20260201120000.json  # Active session metadata
├── assessments.json                    # Phase 1: Director assessments
│   {
│     "CA": { "verdict": "APPROVE", "score": 8, "concerns": [...] },
│     "CPO": { "verdict": "CONCERNS", "score": 7, "concerns": [...] },
│     ...
│   }
├── discussion.jsonl                    # Phase 2: Discussion log
│   {"from": "CA", "to": "CPO", "type": "CHALLENGE", "message": "..."}
│   {"from": "CPO", "to": "CA", "type": "CLARIFY", "message": "..."}
├── votes.json                          # Phase 3: Final votes
│   {
│     "CA": { "final_verdict": "APPROVE", "confidence": 0.9 },
│     ...
│   }
└── resolution.md                       # Phase 4: Board decision
```
