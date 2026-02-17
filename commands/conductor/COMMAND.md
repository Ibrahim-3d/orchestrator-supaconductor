# /conductor

Automated Evaluate-Loop workflow manager. Automatically detects the current step, dispatches the appropriate agent, reads the result, and continues to the next step until the track is complete or requires user intervention.

## Commands

```bash
/conductor implement          # Run the full Evaluate-Loop automatically
/conductor status            # Show current track status and next step
/conductor new-track         # Create a new track with spec and plan
/conductor setup             # Initialize conductor environment
```

## How /conductor implement Works

This command fully automates the Evaluate-Loop workflow:

```
PLAN → EVALUATE PLAN → EXECUTE → EVALUATE EXECUTION
                                       │
                                  PASS → 5.5 BUSINESS DOC SYNC → COMPLETE
                                  FAIL → FIX → re-EXECUTE → re-EVALUATE (loop)
```

### Automated Flow

1. **Detect Current Step** — Read `plan.md` state to determine where we are in the loop
2. **Dispatch Agent** — Call the appropriate agent skill using the Task tool
3. **Read Result** — Parse agent output for PASS/FAIL verdict
4. **Next Step** — Automatically dispatch next agent or mark complete
5. **Repeat** — Continue until track complete or blocker requires user input

### Step Detection Logic

The command reads the track's `plan.md` and `metadata.json` to determine the current state:

| State | Condition | Action |
|-------|-----------|--------|
| **No plan** | `plan.md` doesn't exist or has no tasks | Invoke **conductor-orchestrator** → dispatches planner (superpower or legacy based on flag) |
| **Plan exists, not evaluated** | Tasks exist but no "Plan Evaluation Report" | Invoke **conductor-orchestrator** → dispatches plan evaluator (includes CTO review for technical tracks) |
| **Plan evaluated FAIL** | Evaluation report says FAIL | Invoke **conductor-orchestrator** → dispatches planner to revise |
| **Plan evaluated PASS, tasks pending** | Has `[ ]` tasks | Invoke **conductor-orchestrator** → dispatches executor (superpower or legacy) |
| **All tasks done, not evaluated** | All `[x]`, no "Execution Evaluation Report" | Invoke **conductor-orchestrator** → dispatches execution evaluator |
| **Execution evaluated FAIL** | Report says FAIL with fix list | Invoke **conductor-orchestrator** → dispatches fixer (superpower or legacy) |
| **Execution evaluated PASS** | All checks passed | Run Step 5.5 Business Doc Sync (if needed) → Mark complete |
| **Fix in progress** | Fix Phase tasks exist with `[ ]` | Invoke **conductor-orchestrator** → dispatches fixer to continue |

**Superpower vs Legacy:**
- The **conductor-orchestrator** checks `metadata.json` for `superpower_enhanced: true`
- **If true (new tracks):** Uses `superpowers:writing-plans`, `superpowers:executing-plans`, `superpowers:systematic-debugging`
- **If false/missing (legacy):** Uses `loop-planner`, `loop-executor`, `loop-fixer`
- Both systems are fully supported and work with the same evaluators and quality gates

### Agent Dispatch via Task Tool

The command uses the Task tool to launch specialized agents:

```typescript
// Example: Dispatching the planner agent
Task({
  subagent_type: "Plan",
  description: "Create execution plan",
  prompt: "Create a detailed execution plan for track [track-id]. Read spec.md, check tracks.md for overlap, and produce plan.md with phased tasks."
})

// Example: Dispatching the executor agent
Task({
  subagent_type: "general-purpose",
  description: "Execute track tasks",
  prompt: "Execute tasks from plan.md for track [track-id]. Use the loop-executor skill. Update plan.md after every task. Commit at checkpoints."
})
```

### CTO Advisor Integration

For technical tracks (architecture, integrations, infrastructure), the plan evaluation step automatically includes CTO technical review:

```
Plan created → loop-plan-evaluator dispatches:
  1. Standard plan checks (scope, overlap, dependencies, clarity)
  2. cto-plan-reviewer (for technical tracks) → uses cto-advisor skill
  3. Aggregate results → PASS/FAIL
```

**Technical track detection keywords:**
architecture, system design, integration, API, database, schema, migration, infrastructure, scalability, performance, security, authentication, deployment, monitoring, vendor, technology selection

### Manual CTO Review

You can also manually invoke the CTO advisor at any time:

```bash
# From user prompt
claude /cto-advisor
```

This launches the `cto-plan-reviewer` skill which uses the full `cto-advisor` framework to review the current plan.

## Automatic vs Manual Mode

### Automatic Mode (Recommended)

```bash
/conductor implement
```

Runs continuously until:
- Track is complete
- Fix cycle exceeds 3 iterations
- Blocker prevents task completion
- User intervention required

### Manual Mode (Step-by-Step)

For more control, run agents individually:

```bash
/loop-planner           # Step 1: Create plan
/loop-plan-evaluator    # Step 2: Evaluate plan (includes CTO review for technical tracks)
/loop-executor          # Step 3: Execute tasks
/loop-execution-evaluator  # Step 4: Evaluate execution
/loop-fixer             # Step 5: Fix failures
```

## Status Command

```bash
/conductor status
```

Shows:
- Current track being worked on
- Current step in the Evaluate-Loop
- Tasks completed vs remaining
- Last agent run and result
- Next recommended action

**Example output:**
```
## Conductor Status

**Active Track**: TRACK-001-core-feature
**Current Step**: Execute (Step 3)
**Tasks**: 8/12 completed
**Last Agent**: loop-executor (2 tasks completed)
**Next Action**: Continue execution (4 tasks remaining)

Run `/conductor implement` to continue automatically
```

## New Track Command

```bash
/conductor new-track
```

Interactive workflow to create a new track:
1. Track name and description
2. Generate `spec.md` from requirements
3. Create `plan.md` using superpowers:writing-plans (or loop-planner for legacy)
4. Set up `metadata.json` with `superpower_enhanced: true` (new tracks use superpowers by default)
5. Ready to start implementation

**New tracks automatically use superpowers for superior planning, execution, and debugging patterns.** The orchestrator detects the `superpower_enhanced` flag and dispatches the correct agents.

## Setup Command

```bash
/conductor setup
```

Initializes the conductor environment:
- Creates `conductor/` directory structure
- Creates `tracks.md` registry
- Creates `index.md` status file
- Creates `workflow.md` process documentation
- Creates `decision-log.md` for business decisions

## Escalation & User Intervention

The automatic loop will pause and request user input when:

1. **Fix Cycle Limit** — 3 fix iterations without passing evaluation
2. **Scope Change Needed** — Discovered work requires spec revision
3. **Blocker** — Task cannot complete due to external dependency
4. **Ambiguous Requirement** — Spec unclear, needs clarification
5. **Critical Decision** — Architecture or business decision required

**User will see:**
```
Automatic loop paused — user intervention required

**Reason**: Fix cycle exceeded 3 iterations
**Track**: TRACK-001-core-feature
**Issue**: Dependency resolution tests failing after 3 fix attempts

**Options**:
1. Review the implementation manually
2. Revise the spec to clarify requirements
3. Skip this task and continue with others

What would you like to do?
```

## Track Completion Protocol

When execution evaluation returns PASS:

1. **Check Business Doc Sync** — If evaluation flagged business-impacting changes:
   - Run Step 5.5: Execute Business Doc Sync Checklist
   - Update Tier 1-3 documents
   - Log decisions in `conductor/decision-log.md`
   - Commit: `docs: sync business docs — [description]`

2. **Mark Track Complete**:
   - Update `tracks.md` — mark track complete with date
   - Update `conductor/index.md` — update current status
   - Update track's `metadata.json` — set status to "complete"
   - Commit: `docs: complete [TRACK-NAME] - evaluation passed`

3. **Report to User**:
   ```
   Track Complete

   **Track**: TRACK-001-core-feature
   **Phases**: 3 completed
   **Tasks**: 12 completed
   **Evaluation**: PASS — all checks passed
   **Commits**: 15 commits
   **Business Docs Synced**: Yes (updated relevant docs)

   **Next track suggestion**: TRACK-002-next-feature
   ```

## Command Implementation Details

### For Claude Code CLI

This command should be implemented as:

```typescript
// .claude/commands/conductor/index.ts

import { spawnAgent } from '@claude/agent-sdk';
import { readFile, writeFile } from 'fs/promises';

export async function conductorImplementCommand(args: string[]) {
  // 1. Detect active track
  const tracks = await readTracksFile();
  const activeTrack = tracks.find(t => t.status === 'in-progress');

  if (!activeTrack) {
    return 'No active track. Run /conductor new-track first.';
  }

  // 2. Loop until complete or blocked
  let maxIterations = 50; // Safety limit
  let iteration = 0;

  while (iteration < maxIterations) {
    // 3. Detect current step
    const currentStep = await detectCurrentStep(activeTrack);

    // 4. Dispatch agent
    const agent = getAgentForStep(currentStep);
    const result = await spawnAgent(agent.type, agent.prompt);

    // 5. Check result
    if (result.status === 'complete') {
      await markTrackComplete(activeTrack);
      return `Track ${activeTrack.id} complete!`;
    }

    if (result.status === 'blocked') {
      return `Blocked: ${result.message}`;
    }

    if (result.status === 'needs-user-input') {
      return `User input required: ${result.message}`;
    }

    // 6. Continue to next step
    iteration++;
  }

  return 'Max iterations reached. Please review manually.';
}

async function detectCurrentStep(track: Track): Promise<Step> {
  const planMd = await readFile(`conductor/tracks/${track.id}/plan.md`, 'utf-8');

  // Detection logic (see table above)
  if (!planMd || planMd.length < 100) {
    return 'PLAN';
  }

  if (!planMd.includes('Plan Evaluation Report')) {
    return 'EVALUATE_PLAN';
  }

  if (planMd.includes('Plan Evaluation: FAIL')) {
    return 'PLAN'; // Revise
  }

  const hasPendingTasks = /- \[ \]/.test(planMd);
  if (hasPendingTasks) {
    return 'EXECUTE';
  }

  if (!planMd.includes('Execution Evaluation Report')) {
    return 'EVALUATE_EXECUTION';
  }

  if (planMd.includes('Execution Evaluation: FAIL')) {
    return 'FIX';
  }

  // All checks passed
  return 'COMPLETE';
}

function getAgentForStep(step: Step): AgentConfig {
  const agents = {
    PLAN: {
      type: 'Plan',
      prompt: 'Use loop-planner skill to create execution plan...'
    },
    EVALUATE_PLAN: {
      type: 'general-purpose',
      prompt: 'Use loop-plan-evaluator skill to verify plan...'
    },
    EXECUTE: {
      type: 'general-purpose',
      prompt: 'Use loop-executor skill to implement tasks...'
    },
    EVALUATE_EXECUTION: {
      type: 'general-purpose',
      prompt: 'Use loop-execution-evaluator skill to verify implementation...'
    },
    FIX: {
      type: 'general-purpose',
      prompt: 'Use loop-fixer skill to address failures...'
    }
  };

  return agents[step];
}
```

## Usage Examples

### Start a new track and run it to completion

```bash
# Create track
/conductor new-track

# User provides: "Add Stripe payment integration"
# Planner creates spec.md and plan.md

# Run automatically
/conductor implement

# Output: Loops through all steps automatically
# PLAN → EVALUATE (with CTO review) → EXECUTE → EVALUATE → COMPLETE
```

### Resume interrupted work

```bash
# Check where we are
/conductor status

# Output: "Step 3: Execute — 5/10 tasks completed"

# Continue automatically
/conductor implement

# Picks up where it left off, completes remaining tasks
```

### Review technical plan manually

```bash
# User wants CTO review before execution
/conductor new-track
# ... spec created, plan created

# Manual CTO review
claude /cto-advisor

# CTO review runs, provides recommendations

# Continue with implementation
/conductor implement
```

## Related Documentation

- `conductor/workflow.md` — Evaluate-Loop process details
- `.claude/skills/conductor-orchestrator/SKILL.md` — Orchestrator skill
- `.claude/skills/cto-plan-reviewer/SKILL.md` — CTO technical review
- `CLAUDE.md` — Mandatory agent rules
