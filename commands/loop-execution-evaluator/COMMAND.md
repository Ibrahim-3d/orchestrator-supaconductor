---
name: loop-execution-evaluator
description: "Verify implementation quality. Evaluate-Loop Step 4."
arguments:
  - name: track_id
    description: "The track ID to evaluate"
    required: true
user_invocable: true
---

# /loop-execution-evaluator — Evaluate Implementation

Evaluate-Loop Step 4: Verify the implementation meets quality standards.

## Usage

```bash
/loop-execution-evaluator <track-id>
```

## Your Task

You ARE the loop-execution-evaluator agent. Run quality checks based on track type.

### Determine Track Type

Read `spec.md` for keywords:
- UI keywords → Apply UI/UX checks
- Feature keywords → Apply code quality checks
- Integration keywords → Apply integration checks
- Business logic keywords → Apply business logic checks

### UI/UX Checks (8 Passes)

1. Design tokens used correctly
2. Visual consistency across screens
3. Layout structure (header, footer, container)
4. Responsive breakpoints work
5. Component states complete (hover, focus, disabled, loading)
6. Animations and transitions
7. Accessibility baseline (labels, alt text, focus)
8. Usability check (copy quality, no jargon)

### Code Quality Checks (6 Passes)

1. `npm run build` passes
2. `npm run typecheck` passes (no `any` types)
3. Code patterns followed (naming, imports, DRY)
4. Error handling present
5. Dead code removed (no unused exports, console.logs)
6. Test coverage meets targets (70% overall, 90% business logic)

### Integration Checks

- API contracts match expected schema
- Auth flows work correctly
- Data persists to database
- Error recovery handles failures

### Business Logic Checks

- Product rules enforced correctly
- Edge cases handled
- State transitions are correct

## Output

Append evaluation report to `plan.md`:

```markdown
## Execution Evaluation Report

**Track**: {track_id}
**Date**: YYYY-MM-DD

| Evaluator | Status |
|-----------|--------|
| UI/UX | PASS |
| Code Quality | PASS |
| Integration | N/A |
| Business Logic | PASS |

### Verdict: PASS
```

Update `metadata.json`:
- On PASS: `current_step = "COMPLETE"`, `step_status = "PASSED"`
- On FAIL: `current_step = "FIX"`, `step_status = "NOT_STARTED"`, increment `fix_cycle_count`

## Fix Cycle Limit

If `fix_cycle_count >= 3`, escalate to user instead of continuing.

## Message Bus

```bash
echo "PASS" > .message-bus/events/EXEC_EVAL_COMPLETE_{track_id}.event
# or
echo "FAIL" > .message-bus/events/EXEC_EVAL_COMPLETE_{track_id}.event
```

## Reference

Full agent instructions: `.claude/agents/loop-execution-evaluator.md`
