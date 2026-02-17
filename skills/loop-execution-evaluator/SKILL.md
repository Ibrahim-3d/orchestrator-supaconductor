---
name: loop-execution-evaluator
description: "Evaluate-Loop Step 4: EVALUATE EXECUTION. This is the dispatcher agent — it determines the track type and invokes the correct specialized evaluator. Does NOT run a generic checklist. Instead dispatches to: eval-ui-ux (screens/design), eval-code-quality (features/infrastructure), eval-integration (APIs/auth/payments), eval-business-logic (generator/rules/state). Triggered by: 'evaluate execution', 'review implementation', 'check build', '/phase-review'. Always runs after loop-executor."
---

# Loop Execution Evaluator — Step 4: Dispatcher

This agent does NOT evaluate directly. It determines the track type and dispatches the correct specialized evaluator.

## Why Specialized Evaluators?

Different track types need fundamentally different checks:
- A **UI track** needs design system adherence, visual consistency, responsive checks
- A **feature track** needs build integrity, type safety, code patterns
- An **integration track** needs API contracts, auth flows, error recovery
- A **business logic track** needs product rules, edge cases, state transitions

A generic checklist misses critical issues specific to each type.

## Dispatch Logic

Read the track's `metadata.json` and `spec.md` to determine the track type, then dispatch:

| Track Type | Keywords in spec/metadata | Evaluator |
|-----------|--------------------------|-----------|
| UI / Design | "screen", "component", "design system", "layout", "visual", "UI shell" | `eval-ui-ux` |
| Feature / Code | "implement", "feature", "refactor", "infrastructure", "hook", "store" | `eval-code-quality` |
| Integration | "Supabase", "Stripe", "Gemini", "API", "auth", "database", "webhook" | `eval-integration` |
| Business Logic | "generation", "lock", "dependency", "pricing", "tier", "pipeline", "download" | `eval-business-logic` |

### Multi-Type Tracks

Some tracks need multiple evaluators. For example:
- A generator logic track → `eval-business-logic` + `eval-code-quality`
- An auth/DB integration track → `eval-integration` + `eval-code-quality`
- A UI shell track → `eval-ui-ux` only

When multiple evaluators apply, run them all. The track passes only if ALL evaluators pass.

## Dispatch Workflow

```
1. Read track metadata.json + spec.md
2. Determine track type(s)
3. Dispatch evaluator(s):
   → eval-ui-ux         (if UI track)
   → eval-code-quality   (if code/feature track)
   → eval-integration    (if integration track)
   → eval-business-logic (if logic track)
4. Collect results from all dispatched evaluators
5. Aggregate into final verdict
```

## Structural Checks (Always Run)

Regardless of track type, always verify these baseline checks:

| Check | Method |
|-------|--------|
| plan.md updated | All completed tasks marked `[x]` with commit SHA and summary |
| Scope alignment | No unplanned work added without documentation |
| No skipped tasks | All `[ ]` tasks either completed or documented as intentionally deferred |
| Build passes | `npm run build` exits 0 |
| Business docs in sync | If track made pricing/model/business decisions, verify docs are flagged for Step 5.5 sync |

### Business Doc Sync Check

If the track made any business-impacting changes, verify:
1. The executor's summary includes `Business Doc Sync Required: Yes`
2. Affected documents are listed
3. This flags the Conductor to run Step 5.5 (Business Doc Sync) before marking complete

**What counts as business-impacting:**
- Pricing tier, price point, or feature list changes
- AI model, SDK, or cost structure changes
- New package or product tier additions
- Asset pipeline changes (add/remove/modify assets)
- Persona, GTM, or revenue assumption changes

See `.claude/skills/business-docs-sync/SKILL.md` for the full registry.

## Aggregated Verdict

```markdown
## Execution Evaluation Report

**Track**: [track-id]
**Evaluator**: loop-execution-evaluator (dispatcher)
**Date**: [YYYY-MM-DD]

### Evaluators Dispatched
| Evaluator | Reason | Verdict |
|-----------|--------|---------|
| eval-ui-ux | Track builds P0 screens | PASS ✅ / FAIL ❌ |
| eval-code-quality | Track implements features | PASS ✅ / FAIL ❌ |

### Structural Checks
- plan.md updated: YES / NO
- Scope alignment: YES / NO
- Build passes: YES / NO
- Business doc sync needed: YES / NO (if YES, list affected docs)

### Final Verdict: PASS ✅ / FAIL ❌
All evaluators must PASS for the track to pass.

[If FAIL, aggregate all fix actions from all evaluators]
```

## Metadata Checkpoint Updates

The execution evaluator MUST update the track's `metadata.json` at key points:

### On Start
```json
{
  "loop_state": {
    "current_step": "EVALUATE_EXECUTION",
    "step_status": "IN_PROGRESS",
    "step_started_at": "[ISO timestamp]",
    "checkpoints": {
      "EVALUATE_EXECUTION": {
        "status": "IN_PROGRESS",
        "started_at": "[ISO timestamp]",
        "agent": "loop-execution-evaluator"
      }
    }
  }
}
```

### On PASS
```json
{
  "loop_state": {
    "current_step": "BUSINESS_SYNC",
    "step_status": "NOT_STARTED",
    "checkpoints": {
      "EVALUATE_EXECUTION": {
        "status": "PASSED",
        "completed_at": "[ISO timestamp]",
        "verdict": "PASS",
        "evaluators_run": [
          { "evaluator": "eval-code-quality", "verdict": "PASS", "issues": [] },
          { "evaluator": "eval-business-logic", "verdict": "PASS", "issues": [] }
        ],
        "business_sync_required": true
      },
      "BUSINESS_SYNC": {
        "status": "NOT_STARTED",
        "required": true
      }
    }
  }
}
```

### On FAIL
```json
{
  "loop_state": {
    "current_step": "FIX",
    "step_status": "NOT_STARTED",
    "checkpoints": {
      "EVALUATE_EXECUTION": {
        "status": "FAILED",
        "completed_at": "[ISO timestamp]",
        "verdict": "FAIL",
        "evaluators_run": [
          { "evaluator": "eval-code-quality", "verdict": "PASS", "issues": [] },
          { "evaluator": "eval-business-logic", "verdict": "FAIL", "issues": ["Business rule violation found"] }
        ],
        "failure_items": [
          "Fix business rule enforcement in resolver",
          "Add test coverage for edge case"
        ]
      },
      "FIX": {
        "status": "NOT_STARTED",
        "cycle": 1
      }
    }
  }
}
```

### Update Protocol
1. Read current `metadata.json`
2. Update `loop_state.checkpoints.EVALUATE_EXECUTION` with results
3. If PASS + business sync needed: Set `current_step` to `BUSINESS_SYNC`
4. If PASS + no sync needed: Set `current_step` to `COMPLETE`
5. If FAIL: Set `current_step` to `FIX`, increment `fix_cycle_count` in loop_state
6. Write back to `metadata.json`

## Handoff

- **ALL PASS + No Business Doc Sync** → Conductor marks track complete (Step 5)
- **ALL PASS + Business Doc Sync Needed** → Conductor runs Step 5.5 (Business Doc Sync) before marking complete
- **ANY FAIL** → Conductor dispatches `loop-fixer` with combined fix list
