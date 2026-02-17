# /phase-review

Run the **Evaluate Execution** step of the Evaluate-Loop workflow. This is the mandatory quality gate before marking any track or phase complete.

## When to Use

Run this command:
- After finishing all tasks in a track/phase (Step 4 of the Evaluate-Loop)
- Before marking anything as complete in `tracks.md`
- When you want to verify alignment between plan and execution

## What It Does

1. Reads the current track's `spec.md` and `plan.md`
2. Runs the full post-execution evaluation checklist
3. Identifies misalignment between plan and execution
4. Checks all deliverables are present and functional
5. Runs usability check on user-facing changes
6. Checks build passes with no console errors
7. Generates a Phase Completion Report with PASS/FAIL verdict

## Usage

```bash
/phase-review
```

Or with a specific track:

```bash
/phase-review TRACK-001-feature-implementation
```

## Evaluation Checklist

The command verifies all checks from the Evaluate-Loop:

### 1. Deliverables Check
- [ ] All deliverables from `spec.md` are present
- [ ] Each deliverable matches acceptance criteria
- [ ] No placeholder or incomplete content

### 2. Alignment Check (Prevents Scope Drift)
- [ ] Implementation matches what `plan.md` described
- [ ] No unplanned work was added without documentation
- [ ] No planned work was skipped
- [ ] `plan.md` is fully updated with `[x]` markers and summaries

### 3. Quality Gates
- [ ] Usability check applied to user-facing changes
- [ ] No console errors or warnings
- [ ] Build completes successfully

### 4. Regression Check
- [ ] Existing features still work
- [ ] No broken imports or dead references
- [ ] Pages render without errors

### 5. Testing (when applicable)
- [ ] Unit tests pass
- [ ] Coverage meets thresholds:
  - Overall: 70%
  - Business logic: 90%
  - API routes: 80%
- [ ] Manual testing completed per `workflow.md` checklist

### 6. Documentation
- [ ] Code documented where non-obvious
- [ ] `plan.md` fully updated with task completion summaries
- [ ] Track ready for next session to pick up without confusion

## Output Format

The command generates a completion report:

```markdown
## Phase Completion Report

**Track**: [Track Name]
**Date**: [YYYY-MM-DD]
**Evaluation**: PASS | FAIL

### Deliverables
- [x] Deliverable 1 - src/components/auth/signup-form.tsx
- [x] Deliverable 2 - src/lib/api-client.ts
- [ ] Deliverable 3 - MISSING: src/hooks/useFeature.ts

### Alignment
- [x] All planned tasks executed
- [ ] DRIFT: Design system was rebuilt (not in plan)

### Quality Gates
- [x] Usability check (3 UI changes reviewed)
- [x] No console errors
- [x] Build successful

### Issues Found
1. [Issue description and severity]

### Verdict
PASS — Ready to mark complete
  OR
FAIL — Fix required before completion
  - Fix 1: [description]
  - Fix 2: [description]
```

## What Happens After

### If PASS
1. Mark track complete in `tracks.md`
2. Update `conductor/index.md` current status
3. Commit: `docs: complete [TRACK-NAME] - evaluation passed`

### If FAIL
1. Create fix tasks in `plan.md`
2. Execute the fixes (Step 3 of the Evaluate-Loop)
3. Re-run `/phase-review` (loop back to Step 4)
4. Repeat until PASS

## Related

- `conductor/workflow.md` — Evaluate-Loop Process (primary reference)
- `CLAUDE.md` — Mandatory Agent Rules
- `/conductor status` — See current track status
- `/conductor implement` — Execute track tasks
