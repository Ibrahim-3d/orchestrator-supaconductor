---
name: plan-sprint
description: "Create multiple tracks from a list of features — generates spec, plan, and metadata for each track in parallel"
user_invocable: true
model: opus
arguments:
  - name: features
    description: "Comma-separated or numbered list of features to create tracks for"
    required: false
---

# /orchestrator-supaconductor:plan-sprint — Batch Track Creation

Take a list of features and create fully planned tracks for each one. Spawns parallel agents for independent track creation.

**SCOPE BOUNDARY: This command creates tracks with specs and plans. It does NOT execute any tracks. After all tracks are created, it returns control to the user.**

## Your Task

### Step 1: Gather the Feature List

**If `$ARGUMENTS` provided:** Parse the feature list from arguments.

Supported formats:
```
# Comma-separated
/plan-sprint "User auth with Google OAuth, Dashboard with analytics, Stripe billing"

# Numbered list
/plan-sprint "1. User auth with Google OAuth 2. Dashboard with analytics 3. Stripe billing"

# Natural language
/plan-sprint "I need auth, a dashboard, and payments"
```

**If no arguments provided:**

Check `conductor/config.json` for mode:

- **Agentic mode:** Announce "No features provided. Please provide a feature list." and HALT.
- **Human-in-the-loop mode:** Ask the user:
  > "What features do you want to build? List them out (comma-separated or numbered):"

### Step 2: Parse and Validate Features

1. Extract individual features from the input.
2. For each feature, generate:
   - A kebab-case track slug (e.g., "User auth with Google OAuth" → `google-oauth-auth`)
   - A human-readable track name
   - A track type (`feature`, `bugfix`, `refactor`, `infrastructure`)
3. Present the parsed list to confirm:

```
## Sprint Plan: {N} Tracks

| # | Track ID | Name | Type |
|---|----------|------|------|
| 1 | google-oauth-auth_20260327 | Google OAuth Authentication | feature |
| 2 | analytics-dashboard_20260327 | Analytics Dashboard | feature |
| 3 | stripe-billing_20260327 | Stripe Billing Integration | feature |
```

**Mode-dependent behavior:**
- **Agentic mode:** Announce the plan and proceed immediately.
- **Human-in-the-loop mode:** Ask for confirmation:
  > A) Approve — create all tracks
  > B) Modify — change the list
  > C) Cancel

### Step 3: Determine Dependencies

Analyze the feature list for natural dependencies:
- Auth typically comes before features that need user context
- Data models before UI that displays them
- Infrastructure before features that depend on it

Generate a priority and dependency order:

```
## Dependency Order

1. google-oauth-auth (no dependencies) — Priority: critical
2. analytics-dashboard (depends on: auth) — Priority: important
3. stripe-billing (depends on: auth) — Priority: important
```

### Step 4: Create Tracks in Parallel

**Spawn one agent per track** using the Agent tool with `subagent_type: "general-purpose"`.

Each agent receives this prompt:

```
You are creating a conductor track. Follow these steps exactly:

1. Create directory: conductor/tracks/{track_id}/
2. Create spec.md with:
   - Goal: {feature description}
   - Requirements: Infer from the feature name and project context
   - Acceptance Criteria: Verifiable conditions
   - Out of Scope: Prevent scope creep
   - Technical Notes: Based on conductor/tech-stack.md
   - Dependencies: {depends_on list}
3. Create metadata.json with version 3 format, status "new", priority "{priority}"
4. Create plan.md with:
   - Phased tasks with [ ] checkboxes
   - Bite-sized TDD steps (write failing test → implement → verify → commit)
   - DAG section for parallel execution
   - Exact file paths and complete code
   - Clear acceptance criteria per task
5. Update metadata.json loop_state to PLAN: PASSED

Read these files for context before generating:
- conductor/product.md (if exists)
- conductor/tech-stack.md (if exists)
- conductor/tracks.md (to avoid overlap with existing tracks)

Do NOT execute any code. Only create the track files.
Return a one-line summary: "CREATED: {track_id} — {N} phases, {M} tasks"
```

**Launch all independent tracks in parallel.** Tracks that depend on others can still be created in parallel — dependencies only matter during execution, not planning.

### Step 5: Register All Tracks

After all agents complete, update `conductor/tracks.md`:

Add all tracks to the Active Tracks table in dependency/priority order:

```markdown
## Active Tracks

| Track ID | Name | Type | Status | Step | Priority | Created |
|----------|------|------|--------|------|----------|---------|
| google-oauth-auth_20260327 | Google OAuth Authentication | feature | planned | EVALUATE_PLAN | critical | 2026-03-27 |
| analytics-dashboard_20260327 | Analytics Dashboard | feature | planned | EVALUATE_PLAN | important | 2026-03-27 |
| stripe-billing_20260327 | Stripe Billing Integration | feature | planned | EVALUATE_PLAN | important | 2026-03-27 |
```

### Step 6: Update PRD (if exists)

If `conductor/prd.md` exists, append a new sprint section:

```markdown
## Sprint: {date}

### Sprint Goal
{inferred from the feature list}

### Tracks (ordered by priority and dependency)

| # | Track | Type | Priority | Depends On | Est. Complexity |
|---|-------|------|----------|------------|-----------------|
| 1 | ... | ... | critical | — | M |
```

### Step 7: Update index.md

Update `conductor/index.md` with the new sprint info.

### Step 8: Commit

```bash
git add conductor/tracks/ conductor/tracks.md conductor/index.md conductor/prd.md
git commit -m "conductor(plan-sprint): create {N} tracks — {brief summary}"
```

### Step 9: Final Announcement and HALT

```
## Sprint Planned: {N} Tracks Created

| # | Track | Type | Priority | Tasks | Phases |
|---|-------|------|----------|-------|--------|
| 1 | google-oauth-auth_20260327 | feature | critical | 12 | 3 |
| 2 | analytics-dashboard_20260327 | feature | important | 8 | 2 |
| 3 | stripe-billing_20260327 | feature | important | 15 | 4 |

**Dependency Order**: auth → dashboard, billing (parallel)

**Files Created**:
- {N} track directories in conductor/tracks/
- Each with spec.md + plan.md + metadata.json

### What To Do Next (display to user — DO NOT execute)
- `/orchestrator-supaconductor:go` — start executing the first track
- `/orchestrator-supaconductor:implement {track_id}` — start a specific track
- `/orchestrator-supaconductor:status` — see the full sprint overview
```

### Step 10: HALT — Sprint Planned

**CRITICAL: STOP HERE. Do NOT proceed further. Do NOT invoke any other skills, commands, or tools after this point.**

The `/plan-sprint` command is ONLY responsible for creating tracks. Execution is a separate user action. You must:
1. Display the Final Announcement above
2. Return control to the user
3. **Do NOT** run `/go` or `/implement` or any execution skill
4. **Do NOT** start building any features

---

## Related

- `/orchestrator-supaconductor:new-track` — Create a single track
- `/orchestrator-supaconductor:go` — Start executing the first track
- `/orchestrator-supaconductor:implement` — Run the evaluate-loop on a specific track
- `/orchestrator-supaconductor:close-track` — Close a completed track
- `/orchestrator-supaconductor:status` — See sprint overview
