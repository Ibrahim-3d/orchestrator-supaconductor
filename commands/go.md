---
name: go
description: "The single entry point to the Conductor system - state your goal and everything is handled automatically"
arguments:
  - name: goal
    description: "Your goal — what you want to build, fix, or change"
    required: false
user_invocable: true
---

# /go — Goal-Driven Entry Point

**The single entry point to the entire Conductor system.**

Just state your goal. The system handles everything else.

## Usage

```
/go <your goal>
```

## Examples

```
/go Add Stripe payment integration
/go Fix the login bug where users get logged out
/go Build a dashboard with analytics
/go Refactor the API layer to use caching
```

## Your Task

You ARE the `/go` entry point. When invoked, follow this process:

### 1. Goal Analysis

Parse the user's goal from `$ARGUMENTS`:
- Identify the type (feature, bugfix, refactor, etc.)
- Estimate complexity
- Extract key requirements

If no arguments provided, check for an active track in `conductor/tracks.md` and resume it. If no active track exists, ask the user what they want to work on.

### 2. Track Detection

Check `conductor/tracks.md` for matching existing tracks:
- If match found: Resume that track from its current state
- If no match: Create a new track

### 3. For New Tracks

1. Create track directory: `conductor/tracks/{goal-slug}_{date}/`
2. Generate `spec.md` from the goal
3. Generate `plan.md` with DAG
4. Create `metadata.json` with v3 schema **AND** set `superpower_enhanced: true` (new tracks use superpowers by default)

**Example metadata.json:**
```json
{
  "version": 3,
  "track_id": "goal-slug_20260213",
  "type": "feature",
  "status": "new",
  "superpower_enhanced": true,
  "loop_state": {
    "current_step": "NOT_STARTED",
    "step_status": "NOT_STARTED"
  }
}
```

### 4. Run the Evaluate-Loop

Invoke the conductor-orchestrator agent to run the full evaluate-loop:

```
Use the conductor-orchestrator agent to run the evaluate-loop for this track.
```

The orchestrator will:
- Detect current step from metadata
- Check `superpower_enhanced` flag to determine which agents to use:
  - **If true (new tracks):** Dispatch superpowers (superpowers:writing-plans, superpowers:executing-plans, superpowers:systematic-debugging)
  - **If false/missing (legacy):** Dispatch legacy loop agents (loop-planner, loop-executor, loop-fixer)
- Monitor progress and handle failures
- Complete the track or escalate if blocked

## Escalation Points

Stop and ask user when:
- Goal is ambiguous
- Multiple interpretations possible
- Scope conflicts with existing tracks
- Board rejects the plan
- Fix cycle exceeds 3 iterations

## Resume Existing Work

```
/go                    # Continues the active track
/go continue           # Same as above
```

## What Happens End-to-End

```
User: /go Add a hello world API

1. Goal Analysis → type: feature, complexity: small
2. Track Detection → no existing match
3. Create Track → conductor/tracks/add-hello-world-api_20260216/
   - spec.md generated
   - plan.md generated with DAG
   - metadata.json created
4. Evaluate-Loop begins:
   PLAN → EVALUATE PLAN → EXECUTE → EVALUATE EXECUTION
                                          │
                                     PASS → COMPLETE
                                     FAIL → FIX → re-EVALUATE (loop)
5. Track marked complete
6. Report delivered to user
```

## Related

- `/conductor implement` — Run evaluate-loop on existing track
- `/conductor status` — Check current track progress
- `/conductor new-track` — Create track manually (more control)
- `conductor/workflow.md` — Full evaluate-loop documentation
