---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks autonomously to completion.

**Core principle:** Execution behavior depends on `conductor/config.json` → `"mode"`:
- **`"agentic"`**: Autonomous execution — never stop for human feedback. Resolve all issues by consulting lead agents or best-judgment.
- **`"human-in-the-loop"`**: Stop at blockers and report to user. Wait for feedback between batches of 3 tasks.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## The Process

### Step 1: Load and Review Plan
1. read_file plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns:
   - **`"agentic"` mode**: Resolve autonomously — consult lead agents (Architecture Lead, Tech Lead) via subagent dispatch. NEVER ask the user.
   - **`"human-in-the-loop"` mode**: Raise concerns with the user before starting.
4. Create TodoWrite and proceed

### Step 2: Execute Tasks (Mode-Dependent)

**`"agentic"` mode** — Execute ALL tasks sequentially without stopping:

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. If verification fails: attempt fix autonomously (max 3 retries per task), log the issue, continue to next task
5. Mark as completed

**`"human-in-the-loop"` mode** — Execute in batches of 3 tasks, then pause:

For each batch (3 tasks at a time):
1. Mark tasks as in_progress
2. Follow each step exactly
3. Run verifications as specified
4. If verification fails: STOP and ask the user for help before continuing
5. After each batch completes: report progress, say "Ready for feedback.", and wait before proceeding to next batch

### Step 3: Report Progress
After tasks complete:
- Show what was implemented
- Show verification output
- **`"agentic"` mode**: Show any autonomous decisions made; **do NOT wait for feedback — proceed to completion**
- **`"human-in-the-loop"` mode**: Say "Ready for feedback." and wait

### Step 5: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use supaconductor:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## Blocker Resolution (Mode-Dependent)

**If mode = `"agentic"`**: Resolve all blockers autonomously. NEVER stop.
**If mode = `"human-in-the-loop"`**: STOP and ask the user for help on any blocker.

### Agentic Mode Resolutions:

- **Missing dependency** → Install it if safe (<50KB), or skip the task and log the blocker
- **Test fails** → Attempt fix (max 3 retries), then log failure and continue with remaining tasks
- **Instruction unclear** → Spawn a Plan subagent to interpret based on codebase context, or consult Product Lead
- **Plan has critical gaps** → Consult Architecture Lead via subagent to fill gaps autonomously
- **Verification fails repeatedly** → Log the issue with details, mark task as `completed-with-warnings`, continue

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Fundamental approach is failing (>50% of tasks failing) — re-plan autonomously
- Architecture Lead subagent recommends a different approach

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- **`"agentic"` mode**: Execute ALL tasks without stopping — resolve blockers autonomously, log all decisions
- **`"human-in-the-loop"` mode**: Execute in batches of 3 — stop at blockers and ask the user, wait for feedback between batches
- Never start implementation on main/master branch — use feature branches

## Conductor Integration (Autonomous Mode)

When invoked with `--plan`, `--track-dir`, and `--metadata` parameters (from Conductor orchestrator):
- read_file plan from `--plan` path
- **`"agentic"` mode**: Execute ALL tasks without stopping — run autonomously
- **`"human-in-the-loop"` mode**: Execute in batches of 3 — stop at blockers, wait for user feedback between batches
- After each task: use replace tool to mark `[x]` in plan.md with commit SHA
- After all tasks: update `--metadata` checkpoint to `EXECUTE: PASSED`
- Return concise verdict: `{"verdict": "PASS", "tasks_completed": N}`
- If `--resume-from` is provided, skip tasks before that task ID

When these parameters are absent, fall back to the standalone mode-aware workflow above.

## Integration

**Required workflow skills:**
- **supaconductor:using-git-worktrees** - REQUIRED: Set up isolated workspace before starting
- **supaconductor:writing-plans** - Creates the plan this skill executes
- **supaconductor:finishing-a-development-branch** - Complete development after all tasks

