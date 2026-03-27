---
name: new-track
description: "Create a new development track with spec, plan, and metadata"
model: sonnet
arguments:
  - name: new-track
    description: "Brief description of what you want to build"
    required: false
user_invocable: true
---

# /orchestrator-supaconductor:new-track — Create New Track

Interactive workflow to create a new development track with specification, implementation plan, and metadata.

## Usage

```bash
/orchestrator-supaconductor:new-track
/orchestrator-supaconductor:new-track "Add Stripe payment integration"
```

## Your Task

Guide the user through creating a new track:

### Step 1: Gather Requirements

If `$ARGUMENTS` provided, use it as the track goal.
If not, ask: "What would you like to build or fix?"

### Step 2: Generate Track Name

Create a kebab-case slug from the goal:
- "Add Stripe payment integration" → `stripe-payment-integration`
- "Fix login bug" → `fix-login-bug`
- "Build analytics dashboard" → `analytics-dashboard`

### Step 3: Create Directory Structure

```
conductor/tracks/{track-name}_{YYYYMMDD}/
├── spec.md         # Requirements and acceptance criteria
├── plan.md         # Implementation plan (generated in Step 6)
└── metadata.json   # Track configuration
```

### Step 4: Generate spec.md

write_file a comprehensive spec including:
- **Goal**: What success looks like
- **Requirements**: Specific features and behaviors
- **Acceptance Criteria**: Verifiable conditions for completion
- **Out of Scope**: What NOT to build (prevents scope creep)
- **Technical Notes**: Architecture guidance, patterns to follow

### Step 5: Create metadata.json

```json
{
  "version": 3,
  "track_id": "{track-name}_{YYYYMMDD}",
  "name": "Human-readable Track Name",
  "type": "feature | bugfix | refactor | infrastructure",
  "status": "new",
  "superpower_enhanced": true,
  "created_at": "YYYY-MM-DD",
  "loop_state": {
    "current_step": "NOT_STARTED",
    "step_status": "NOT_STARTED",
    "fix_cycle_count": 0
  }
}
```

**Note:** Always set `superpower_enhanced: true` for new tracks — they use the superior superpowers agents by default.

### Step 6: Generate plan.md

**Invoke the loop-planner to create the implementation plan:**

1. Read the spec.md you just created
2. Read project context: `conductor/product.md`, `conductor/tech-stack.md` (if they exist)
3. Check `conductor/tracks.md` for completed work (avoid overlap)
4. Generate `conductor/tracks/{track_id}/plan.md` with:
   - Phased tasks with `[ ]` checkboxes
   - Bite-sized TDD steps (write failing test → implement → verify → commit)
   - DAG section for parallel execution
   - Clear acceptance criteria per task
   - Exact file paths and code
5. Update `metadata.json`:
   - Set `loop_state.current_step` = `"EVALUATE_PLAN"`
   - Set `loop_state.checkpoints.PLAN.status` = `"PASSED"`

### Step 7: Register in tracks.md

Add entry to `conductor/tracks.md`:

```markdown
| Track ID | Name | Type | Status | Created |
|----------|------|------|--------|---------|
| my-feature_20260216 | My Feature | feature | planned | 2026-02-16 |
```

### Step 8: Final Announcement and HALT

Show the user:
- Track ID and location
- Spec summary (3-5 bullet points)
- Plan summary (number of phases, tasks, estimated complexity)
- Files created (spec.md, plan.md, metadata.json)

```
## New Track Created

**Track**: {track_id}
**Location**: conductor/tracks/{track_id}/

**Spec Summary**:
- ...

**Plan Summary**:
- {N} phases, {M} tasks
- Estimated complexity: S/M/L/XL

**Files Created**:
- conductor/tracks/{track_id}/spec.md
- conductor/tracks/{track_id}/plan.md
- conductor/tracks/{track_id}/metadata.json

### What To Do Next (display to user — DO NOT execute)
- `/orchestrator-supaconductor:implement` — start the Evaluate-Loop
- `/orchestrator-supaconductor:go` — shorthand to start immediately
```

**CRITICAL: STOP HERE. Do NOT proceed to execute the plan. Do NOT invoke `/implement` or `/go`. Return control to the user.**

## Track Types

| Type | When to Use |
|------|-------------|
| `feature` | New user-facing functionality |
| `bugfix` | Fixing existing broken behavior |
| `refactor` | Improving code without changing behavior |
| `infrastructure` | DevOps, CI/CD, tooling, dependencies |

## Related

- `/orchestrator-supaconductor:implement` — Run the evaluate-loop on this track
- `/orchestrator-supaconductor:status` — Check track status
- `/orchestrator-supaconductor:go` — Shorthand that creates track + starts implement automatically
- `/orchestrator-supaconductor:close-track` — Close a completed track

