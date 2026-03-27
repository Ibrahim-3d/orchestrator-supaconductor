---
name: implement
description: "Run the full Evaluate-Loop automatically from current track state to completion"
arguments:
  - name: implement
    description: "Optional track ID (defaults to active track)"
    required: false
user_invocable: true
---

# /supaconductor:implement — Automated Evaluate-Loop

Fully automates the Evaluate-Loop workflow. Detects current step, dispatches the correct agent, reads the result, and continues until the track is complete. **Runs fully autonomously — never stops to ask the user questions.**

## Usage

```bash
/supaconductor:implement
/supaconductor:implement my-track-id
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
- **If true (new tracks):** Uses `supaconductor:writing-plans`, `supaconductor:executing-plans`, `supaconductor:systematic-debugging`
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

Uses the run_shell_command to spawn specialized agents:

```typescript
run_shell_command(claude --print "/supaconductor:...")
```

## Autonomous Resolution

**The loop NEVER pauses for user input.** All blockers are resolved autonomously:

1. **Fix Cycle Limit** — Extends to 5 attempts with alternative approaches, then completes with warnings
2. **Scope Change Needed** — Lead agents (Product, Architecture) autonomously adjust scope within spec intent
3. **Blocker** — Logs blocker, skips blocked tasks, continues with unblocked work
4. **Ambiguous Requirement** — Product Lead interprets based on spec and codebase context
5. **Critical Decision** — Board of Directors deliberates and decides autonomously

## Track Completion Protocol

When execution evaluation returns PASS:

1. **Check Business Doc Sync** — If evaluation flagged business-impacting changes, sync docs
2. **Mark Track Complete** — Update `tracks.md`, `metadata.json`, `conductor/index.md`
3. **Report to User** — Summary of phases, tasks, commits

## Example

```bash
# Start a new track and run to completion
/supaconductor:new-track
# ... track created ...
/supaconductor:implement
# → PLAN → EVALUATE (with CTO review) → EXECUTE → EVALUATE → COMPLETE

# Resume interrupted work
/supaconductor:status  # See where we are
/supaconductor:implement  # Continue automatically
```

## Related

- `/supaconductor:status` — Check current track progress
- `/supaconductor:new-track` — Create track manually
- `/supaconductor:go` — Single entry point (creates track + runs implement)
- `conductor/workflow.md` — Full evaluate-loop documentation

