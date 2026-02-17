---
name: loop-fixer
description: "Fix issues found by evaluation. Evaluate-Loop Step 5."
arguments:
  - name: track_id
    description: "The track ID to fix"
    required: true
user_invocable: true
---

# /loop-fixer — Fix Evaluation Failures

Evaluate-Loop Step 5: Address issues found during evaluation.

## Usage

```bash
/loop-fixer <track-id>
```

## Your Task

You ARE the loop-fixer agent. Fix the issues from the evaluation report.

1. **Read failure list** from `plan.md` evaluation report
2. **Check error registry**: `conductor/knowledge/errors.json` for known fixes
3. **For each issue**:
   - Understand the root cause
   - Implement the minimal fix (no scope creep)
   - Verify it addresses the issue
   - Commit with descriptive message
4. **Add Fix Phase to plan.md**
5. **Log new errors** to `errors.json` if discovered
6. **Update metadata.json**:
   - Set `current_step = "EVALUATE_EXECUTION"`
   - Set `step_status = "NOT_STARTED"`

## Plan.md Fix Phase Format

```markdown
## Fix Phase (Cycle 1)

### Fix 1: Button contrast
- [x] Updated button background to #1a1a1a <!-- def5678 -->
  - Contrast now 7.2:1

### Fix 2: Test coverage
- [x] Added tests for edge cases <!-- ghi9012 -->
  - Coverage now 74%
```

## Commit Format

```
fix(track-id): Fix 1 - Button contrast issue

- Updated button background to #1a1a1a
- Contrast ratio now 7.2:1 (was 3.2:1)

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Escalation

If this is fix cycle 3+, stop and report to user:

```markdown
## Orchestrator Paused — User Input Required

**Track**: {track_id}
**Reason**: Fix cycle exceeded 3 iterations

**Recurring Issues**:
1. [List issues that keep failing]

What would you like to do?
```

## Output

```
FIXES APPLIED: X
COMMITS: def5678, ghi9012, ...
VERDICT: PASS
```

## Message Bus

```bash
echo "PASS" > .message-bus/events/FIX_COMPLETE_{track_id}.event
```

## Reference

Full agent instructions: `.claude/agents/loop-fixer.md`
