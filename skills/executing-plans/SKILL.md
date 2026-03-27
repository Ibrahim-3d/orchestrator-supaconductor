---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks autonomously to completion.

**Core principle:** Autonomous execution — never stop for human feedback. Resolve all issues by consulting lead agents or making best-judgment calls.

**Announce at start:** "I'm using the executing-plans skill to implement this plan."

## The Process

### Step 1: Load and Review Plan
1. read_file plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Resolve them autonomously — consult lead agents (Architecture Lead, Tech Lead) via subagent dispatch. NEVER ask the user.
4. Create TodoWrite and proceed

### Step 2: Execute All Tasks
**Execute ALL tasks sequentially — do NOT batch or wait for feedback.**

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. If verification fails: attempt fix autonomously (max 3 retries per task), log the issue, continue to next task
5. Mark as completed

### Step 3: Report Progress
After all tasks complete:
- Show what was implemented
- Show verification output
- Show any autonomous decisions made
- **Do NOT wait for feedback — proceed to completion**

### Step 5: Complete Development

After all tasks complete and verified:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use supaconductor:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## Autonomous Blocker Resolution

**NEVER stop to ask the user for help.** Resolve all blockers autonomously:

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
- Execute ALL tasks without stopping — no batching, no waiting
- Resolve blockers autonomously — never ask the user
- Log all autonomous decisions for post-completion review
- Never start implementation on main/master branch — use feature branches

## Conductor Integration (Autonomous Mode)

When invoked with `--plan`, `--track-dir`, and `--metadata` parameters (from Conductor orchestrator):
- read_file plan from `--plan` path
- Execute ALL tasks (not batches of 3) — run autonomously
- Do NOT stop for human feedback between batches
- After each task: use replace tool to mark `[x]` in plan.md with commit SHA
- After all tasks: update `--metadata` checkpoint to `EXECUTE: PASSED`
- Return concise verdict: `{"verdict": "PASS", "tasks_completed": N}`
- If `--resume-from` is provided, skip tasks before that task ID

When these parameters are absent, fall back to the standalone batch workflow above.

## Integration

**Required workflow skills:**
- **supaconductor:using-git-worktrees** - REQUIRED: Set up isolated workspace before starting
- **supaconductor:writing-plans** - Creates the plan this skill executes
- **supaconductor:finishing-a-development-branch** - Complete development after all tasks

