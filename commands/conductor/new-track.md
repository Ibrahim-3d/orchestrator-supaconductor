---
name: new-track
description: "Create a new development track with spec, plan, and metadata - interactive workflow"
arguments:
  - name: description
    description: "Brief description of what you want to build"
    required: false
user_invocable: true
---

# /conductor:new-track — Create New Track

Interactive workflow to create a new development track with specification, implementation plan, and metadata.

## Usage

```bash
/conductor:new-track
/conductor:new-track "Add Stripe payment integration"
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
├── plan.md         # Implementation plan (created after spec)
└── metadata.json   # Track configuration
```

### Step 4: Generate spec.md

Write a comprehensive spec including:
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

### Step 6: Register in tracks.md

Add entry to `conductor/tracks.md`:

```markdown
| Track ID | Name | Type | Status | Created |
|----------|------|------|--------|---------|
| my-feature_20260216 | My Feature | feature | new | 2026-02-16 |
```

### Step 7: Confirm and Proceed

Show the user:
- Track ID and location
- Spec summary (3-5 bullet points)
- Estimated complexity
- Next step: Run `/conductor:implement` to start

## Track Types

| Type | When to Use |
|------|-------------|
| `feature` | New user-facing functionality |
| `bugfix` | Fixing existing broken behavior |
| `refactor` | Improving code without changing behavior |
| `infrastructure` | DevOps, CI/CD, tooling, dependencies |

## Example Output

```
## New Track Created

**Track**: stripe-payment-integration_20260216
**Location**: conductor/tracks/stripe-payment-integration_20260216/

**Spec Summary**:
- Add Stripe Checkout for one-time purchases
- Support card payments in 10+ currencies
- Webhook handling for payment confirmation
- Update user tier on successful payment
- Email receipt after purchase

**Type**: feature
**Complexity**: Medium (estimated 8-12 tasks)
**Superpowers**: Enabled ✓

**Files Created**:
- conductor/tracks/stripe-payment-integration_20260216/spec.md
- conductor/tracks/stripe-payment-integration_20260216/metadata.json

**Next Step**: Run `/conductor:implement` to start the Evaluate-Loop
```

## Related

- `/conductor:implement` — Run the evaluate-loop on this track
- `/conductor:status` — Check track status
- `/go` — Shorthand that creates track + starts implement automatically
