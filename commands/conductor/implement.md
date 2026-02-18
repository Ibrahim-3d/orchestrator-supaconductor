---
name: implement
description: "Run the full Evaluate-Loop automatically from current track state to completion"
arguments:
  - name: track_id
    description: "Optional track ID (defaults to active track)"
    required: false
user_invocable: true
---

# /conductor:implement — Automated Evaluate-Loop

Fully automates the Evaluate-Loop workflow. Detects current step, dispatches the correct agent, reads the result, and continues until the track is complete or requires user intervention.

## Usage

```bash
/conductor:implement
/conductor:implement my-track-id
```

## Automated Flow

```
PLAN → EVALUATE PLAN → EXECUTE → EVALUATE EXECUTION
                                       │
                                  PASS → 5.5 BUSINESS DOC SYNC → COMPLETE
                                  FAIL → FIX → re-EXECUTE → re-EVALUATE (loop)
```

## Step Detection Logic

| State | Condition | Action |
|-------|-----------|--------|
| **No plan** | `plan.md` doesn't exist or has no tasks | Dispatch planner (superpowers or legacy) |
| **Plan exists, not evaluated** | Tasks exist but no "Plan Evaluation Report" | Dispatch plan evaluator (includes CTO review for technical tracks) |
| **Plan evaluated FAIL** | Report says FAIL | Dispatch planner to revise |
| **Plan evaluated PASS, tasks pending** | Has `[ ]` tasks | Dispatch executor (superpowers or legacy) |
| **All tasks done, not evaluated** | All `[x]`, no "Execution Evaluation Report" | Dispatch execution evaluator |
| **Execution evaluated FAIL** | Report says FAIL with fix list | Dispatch fixer (superpowers or legacy) |
| **Execution evaluated PASS** | All checks passed | Run Step 5.5 Business Doc Sync → Mark complete |

## Superpower vs Legacy Detection

The orchestrator checks `metadata.json` for `superpower_enhanced: true`:
- **If true (new tracks):** Uses `superpowers:writing-plans`, `superpowers:executing-plans`, `superpowers:systematic-debugging`
- **If false/missing (legacy):** Uses `loop-planner`, `loop-executor`, `loop-fixer`

Both systems use the same evaluators and quality gates.

## CTO Advisor Integration

For technical tracks (architecture, integrations, infrastructure, APIs, databases), plan evaluation automatically includes CTO technical review:

```
Plan created → loop-plan-evaluator dispatches:
  1. Standard plan checks (scope, overlap, dependencies, clarity)
  2. cto-plan-reviewer (for technical tracks)
  3. Aggregate results → PASS/FAIL
```

**Technical track keywords:** architecture, system design, integration, API, database, schema, migration, infrastructure, scalability, performance, security, authentication, deployment, monitoring

## Agent Dispatch

Uses the Task tool to spawn specialized agents:

```typescript
Task({
  subagent_type: "conductor-orchestrator",
  description: "Run evaluate-loop",
  prompt: "Continue the evaluate-loop for track [track-id]. Check metadata.json for current step and dispatch the correct agent."
})
```

## Automatic Stops

The loop pauses and asks for user input when:
1. **Fix Cycle Limit** — 3 fix iterations without passing
2. **Scope Change Needed** — Discovered work requires spec revision
3. **Blocker** — Task cannot complete due to external dependency
4. **Ambiguous Requirement** — Spec unclear, needs clarification
5. **Critical Decision** — Architecture or business decision required

## Track Completion Protocol

When execution evaluation returns PASS:

1. **Check Business Doc Sync** — If evaluation flagged business-impacting changes, sync docs
2. **Mark Track Complete** — Update `tracks.md`, `metadata.json`, `conductor/index.md`
3. **Report to User** — Summary of phases, tasks, commits

## Example

```bash
# Start a new track and run to completion
/conductor:new-track
# ... track created ...
/conductor:implement
# → PLAN → EVALUATE (with CTO review) → EXECUTE → EVALUATE → COMPLETE

# Resume interrupted work
/conductor:status  # See where we are
/conductor:implement  # Continue automatically
```

## Related

- `/conductor:status` — Check current track progress
- `/conductor:new-track` — Create track manually
- `/go` — Single entry point (creates track + runs implement)
- `conductor/workflow.md` — Full evaluate-loop documentation
