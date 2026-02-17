---
name: eval-business-logic
description: "Specialized business logic evaluator for the Evaluate-Loop. Use this for evaluating tracks that implement core product logic — pipelines, dependency resolution, state machines, pricing/tier enforcement, packaging. Checks feature correctness against product rules, edge cases, state transitions, data flow, and user journey completeness. Dispatched by loop-execution-evaluator when track type is 'business-logic', 'generator', or 'core-feature'. Triggered by: 'evaluate logic', 'test business rules', 'verify business rules', 'check feature'."
---

# Business Logic Evaluator Agent

Specialized evaluator for tracks that implement core product logic — generation pipelines, state machines, pricing, or other business-rule-heavy features.

## When This Evaluator Is Used

Dispatched by `loop-execution-evaluator` when the track involves:
- Core product pipeline logic
- State machine or workflow systems
- Pricing tier enforcement
- Dependency resolution between deliverables
- Download or packaging features

## Inputs Required

1. Track's `spec.md` and `plan.md`
2. `conductor/product.md` — product rules (deliverables, tiers, dependencies)
3. Project-specific pipeline/prompt configurations (if applicable)
4. Data definition files (e.g., asset definitions, feature configs)
5. Implementation code being evaluated

## Evaluation Passes (6 checks)

### Pass 1: Product Rules Compliance

Check against rules defined in `conductor/product.md`:

| Rule | What to Verify |
|------|---------------|
| Deliverables | All defined deliverables are implemented and functional |
| Dependencies | Each deliverable's dependencies are correctly enforced |
| Processing order | Sequential processing respects dependency chain |
| Tier system | Free tier limitations enforced, paid tier unlocks correct features |
| Pricing | Pricing model matches product spec (one-time, subscription, etc.) |
| State rules | State transitions (e.g., lock/unlock, draft/publish) propagate correctly |

```markdown
### Product Rules: PASS / FAIL
- Rules checked: [count]
- Violations: [list rule: actual behavior]
- Deliverables functional: [X]/[total]
```

### Pass 2: Feature Correctness

For each feature in the spec, verify it works correctly:

| Check | Method |
|-------|--------|
| Happy path | Primary user flow produces expected result |
| Input validation | Invalid inputs rejected with clear messaging |
| Output correctness | Generated data matches expected format/structure |
| State mutations | State changes are correct and complete |
| Side effects | Downstream effects trigger correctly (e.g., dependency propagation) |

```markdown
### Feature Correctness: PASS / FAIL
- Features tested: [count]
- Correct: [count]
- Failures: [describe each]
```

### Pass 3: Edge Cases

| Scenario | What to Verify |
|----------|---------------|
| Empty state | First-time user with no data |
| Boundary values | Max input length, empty inputs, special characters |
| Concurrent operations | What happens if user triggers 2 operations at once |
| Network failure mid-operation | Partial state handled correctly |
| Re-processing | Re-running an operation on existing data prompts confirmation if needed |
| All items locked/finalized | UI reflects that no further changes are possible |
| Tier limits | Exceeding free tier limit shows upgrade prompt |

```markdown
### Edge Cases: PASS / FAIL
- Scenarios checked: [count]
- Unhandled: [list]
- User impact: [describe]
```

### Pass 4: State Transitions

Verify state machine correctness for your project's state model. Example pattern:

| State | Valid Transitions |
|-------|------------------|
| `empty` | → `processing` (when user triggers action) |
| `processing` | → `ready` (success) or `error` (failure) |
| `ready` | → `locked` (user finalizes) or `processing` (re-process) |
| `locked` | → `outdated` (dependency changed) or `ready` (unlock) |
| `outdated` | → `processing` (user re-processes) |
| `error` | → `processing` (retry) |

Adapt the state table above to match your project's actual states.

```markdown
### State Transitions: PASS / FAIL
- States implemented: [list]
- Invalid transitions possible: [list]
- Missing transitions: [list]
```

### Pass 5: Data Flow

| Check | What to Verify |
|-------|---------------|
| Input → Processing | User form data correctly feeds into processing pipeline |
| Processing → Output | Results stored/displayed correctly |
| Output → Persistence | Results saved to store/database |
| Cross-component | Data shared correctly between components |
| Stale data | No stale renders after state changes |

```markdown
### Data Flow: PASS / FAIL
- Flow verified: [input → output]
- Stale data issues: [describe]
- Data loss points: [list]
```

### Pass 6: User Journey Completeness

Walk through the complete user journey for the feature under evaluation. Example structure:

```
1. User provides input (form, selection, etc.)
2. System processes input
3. User reviews output
4. User can lock/finalize results
5. System handles dependencies between outputs
6. User views all deliverables
7. User can export/download results
8. User can re-process any unlocked item
9. Locked items show "outdated" if dependencies change
```

Adapt the journey steps above to match your project's actual user flow.

```markdown
### User Journey: PASS / FAIL
- Steps completed: [X]/[total]
- Broken at step: [which]
- User experience: [smooth / friction at: describe]
```

## Verdict Template

```markdown
## Business Logic Evaluation Report

**Track**: [track-id]
**Evaluator**: eval-business-logic
**Date**: [YYYY-MM-DD]

### Results
| Pass | Status | Issues |
|------|--------|--------|
| 1. Product Rules | PASS/FAIL | [details] |
| 2. Feature Correctness | PASS/FAIL | [details] |
| 3. Edge Cases | PASS/FAIL | [details] |
| 4. State Transitions | PASS/FAIL | [details] |
| 5. Data Flow | PASS/FAIL | [details] |
| 6. User Journey | PASS/FAIL | [details] |

### Verdict: PASS / FAIL
[If FAIL, list specific fix actions for loop-fixer]
```

## Handoff

- **PASS** → Return to `loop-execution-evaluator` → Conductor marks complete
- **FAIL** → Return to `loop-execution-evaluator` → Conductor dispatches `loop-fixer`
