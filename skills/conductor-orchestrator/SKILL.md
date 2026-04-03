---
name: conductor-orchestrator
description: "Master coordinator for the Evaluate-Loop workflow v3. Supports GOAL-DRIVEN entry, PARALLEL execution via worker agents, BOARD OF DIRECTORS deliberation, and message bus coordination. Dispatches specialized workers dynamically, monitors via message bus, aggregates results. Uses metadata.json v3 for parallel state tracking. Use when: '/go <goal>', '/conductor implement', 'start track', 'run the loop', 'orchestrate', 'automate track'."
---

# Conductor Orchestrator — Parallel Multi-Agent Coordinator (v3)

The master coordinator that runs the Evaluate-Loop for any track. Version 3 adds **goal-driven entry**, **parallel execution** via worker agents, **Board of Directors deliberation**, and **message bus coordination**.

---

## Mode Configuration Protocol

**FIRST ACTION: Read `conductor/config.json` to determine operating mode.**

```typescript
const config = await readJSON('conductor/config.json').catch(() => ({ mode: 'agentic' }));
const MODE = config.mode; // "agentic" | "human-in-the-loop"
const MAX_FIX_CYCLES = config.max_fix_cycles || 5;
```

| Mode | Behavior |
|------|----------|
| `"agentic"` | Fully autonomous. Resolve all decisions via leads, board, or best-judgment. Never ask user. |
| `"human-in-the-loop"` | Pause at key decision points. Ask user for ambiguity, blockers, fix limits, HIGH_IMPACT decisions. |

**All decision points below check `MODE` before acting.** If config.json doesn't exist, default to `"agentic"`.

---

## Goal-Driven Entry (`/go`)

The simplest entry point. User states their goal, the system handles everything.

### Usage

```bash
/go Add Stripe payment integration
/go Fix the login bug
/go Build an admin dashboard
```

### Goal Processing Flow

```typescript
async function processGoal(userGoal: string) {
  // 1. GOAL ANALYSIS
  const analysis = await analyzeGoal(userGoal);
  /*
    Returns:
    - intent: "feature" | "bugfix" | "refactor" | "research"
    - keywords: ["stripe", "payment", "checkout"]
    - complexity: "minor" | "moderate" | "major"
    - technical: boolean
  */

  // 2. CHECK EXISTING TRACKS
  const existingTrack = await findMatchingTrack(analysis.keywords);

  if (existingTrack) {
    // Resume existing track
    console.log(`Found existing track: ${existingTrack.id}`);
    return resumeOrchestration(existingTrack.id);
  }

  // 3. CREATE NEW TRACK
  const trackId = await createTrackFromGoal(userGoal, analysis);
  /*
    Creates:
    - conductor/tracks/{trackId}/
    - conductor/tracks/{trackId}/spec.md (generated from goal)
    - conductor/tracks/{trackId}/metadata.json (v3)
  */

  // 4. RUN FULL LOOP
  return runOrchestrationLoop(trackId);
}
```

### Goal Analysis

```typescript
async function analyzeGoal(goal: string) {
  // Use context-explorer to understand codebase
  const codebaseContext = await Task({
    subagent_type: "Explore",
    description: "Understand codebase for goal",
    prompt: `Analyze codebase to understand context for: "${goal}"

      Return:
      1. Related files/components
      2. Existing patterns to follow
      3. Dependencies needed
      4. Potential conflicts with existing code`
  });

  // Classify goal
  const intent = classifyIntent(goal);
  const keywords = extractKeywords(goal);
  const complexity = estimateComplexity(goal, codebaseContext);
  const technical = isTechnicalGoal(goal);

  return { intent, keywords, complexity, technical, codebaseContext };
}

function classifyIntent(goal: string): string {
  const lowerGoal = goal.toLowerCase();

  if (lowerGoal.match(/fix|bug|error|broken|crash|issue/)) return "bugfix";
  if (lowerGoal.match(/refactor|clean|optimize|improve|simplify/)) return "refactor";
  if (lowerGoal.match(/research|investigate|analyze|understand/)) return "research";
  return "feature";
}
```

### Track Matching

```typescript
async function findMatchingTrack(keywords: string[]): Track | null {
  const tracks = await readTracksFile();

  // Check in-progress tracks first
  const inProgress = tracks.filter(t =>
    t.status === 'IN_PROGRESS' || t.status === 'in_progress'
  );

  for (const track of inProgress) {
    const trackKeywords = extractKeywords(track.name + ' ' + track.description);
    const overlap = keywords.filter(k => trackKeywords.includes(k));

    if (overlap.length >= 2) {
      return track; // Good match
    }
  }

  // Check planned tracks
  const planned = tracks.filter(t =>
    t.status === 'NOT_STARTED' || t.status === 'planned'
  );

  for (const track of planned) {
    const trackKeywords = extractKeywords(track.name + ' ' + track.description);
    const overlap = keywords.filter(k => trackKeywords.includes(k));

    if (overlap.length >= 2) {
      return track;
    }
  }

  return null; // No match, create new track
}
```

### Spec Generation from Goal

```typescript
async function generateSpecFromGoal(goal: string, analysis: GoalAnalysis): string {
  const spec = await Task({
    subagent_type: "Plan",
    description: "Generate spec from goal",
    prompt: `Generate a specification document for this goal:

      GOAL: "${goal}"

      CODEBASE CONTEXT:
      ${analysis.codebaseContext}

      Create spec.md with:
      1. Overview - what we're building/fixing
      2. Requirements - specific deliverables
      3. Acceptance Criteria - how to verify it works
      4. Dependencies - what this needs
      5. Out of Scope - what we're NOT doing

      Be specific and actionable. Use the codebase context to identify:
      - Existing patterns to follow
      - Files that will be modified
      - Tests that need to pass

      Format as markdown.`
  });

  return spec.output;
}
```

### Goal Resolution (Mode-Dependent)

```typescript
// If goal is ambiguous, check mode
if (analysis.ambiguous) {
  if (MODE === 'human-in-the-loop') {
    // HUMAN MODE: Ask user to pick interpretation
    return ask_user({
      questions: [{
        question: "I need clarification on your goal. Which do you mean?",
        header: "Clarify",
        options: analysis.interpretations.map(i => ({
          label: i.summary, description: i.detail
        })),
        multiSelect: false
      }]
    });
  }
  // AGENTIC MODE: Resolve autonomously — NEVER ask the user
  // Spawn a Plan subagent to pick the best interpretation
  const resolution = await Task({
    subagent_type: "Plan",
    description: "Resolve ambiguous goal",
    prompt: `The user's goal "${userGoal}" has multiple interpretations:
      ${analysis.interpretations.map(i => `- ${i.summary}: ${i.detail}`).join('\n')}

      Analyze the codebase context and pick the BEST interpretation.
      Consider: existing code patterns, project structure, recent git history.
      Return JSON: {"chosen": "<interpretation summary>", "reasoning": "<why>"}`
  });
  // Use the resolved interpretation and continue
  analysis = { ...analysis, ambiguous: false, resolvedGoal: resolution.chosen };
}

// If multiple tracks match, check mode
if (matchingTracks.length > 1) {
  if (MODE === 'human-in-the-loop') {
    // HUMAN MODE: Ask user which track
    return ask_user({
      questions: [{
        question: "This goal matches multiple existing tracks. Which one?",
        header: "Track",
        options: matchingTracks.map(t => ({
          label: t.name, description: `Status: ${t.status}`
        })),
        multiSelect: false
      }]
    });
  }
  // AGENTIC MODE: Pick the most relevant one — NEVER ask the user
  // Pick the track with the highest keyword overlap and most recent activity
  const bestMatch = matchingTracks.sort((a, b) => {
    const aOverlap = keywords.filter(k => a.name.toLowerCase().includes(k)).length;
    const bOverlap = keywords.filter(k => b.name.toLowerCase().includes(k)).length;
    if (bOverlap !== aOverlap) return bOverlap - aOverlap;
    return new Date(b.updated_at) - new Date(a.updated_at); // Most recent
  })[0];
  console.log(`Auto-selected track: ${bestMatch.id} (best keyword match)`);
  return resumeOrchestration(bestMatch.id);
}
```

---

## Key Changes in v3

### From v2
1. **Metadata-based state detection** — Reads `loop_state.current_step` from metadata.json
2. **Lead Engineer consultation** — Consults specialized leads for decisions
3. **Resumption support** — Exact state recovery if interrupted
4. **Explicit checkpoints** — Each step writes state to metadata.json
5. **Learning Layer** — Knowledge Manager + Retrospective Agent

### New in v3
6. **Parallel Execution** — Multiple workers execute DAG tasks simultaneously
7. **Board of Directors** — 5-member expert deliberation at checkpoints
8. **Message Bus** — Inter-agent coordination via file-based queue
9. **Worker Pool** — Dynamic worker creation/cleanup via agent-factory
10. **DAG-Aware Planning** — Plans include explicit dependency graphs
11. **Failure Isolation** — One worker failure doesn't block independent tasks

---

## State Detection (New v2 Protocol)

### Primary: read_file metadata.json

```typescript
async function detectCurrentStep(trackId: string) {
  const metadataPath = `conductor/tracks/${trackId}/metadata.json`;
  const metadata = await readJSON(metadataPath);

  // Migrate v1 to v2 if needed
  if (!metadata.version || metadata.version < 2) {
    metadata = await migrateToV2(trackId, metadata);
    await writeJSON(metadataPath, metadata);
  }

  const { current_step, step_status } = metadata.loop_state;

  return { current_step, step_status, metadata };
}
```

### State Machine Logic (v3)

| Current Step | Step Status | Next Action |
|--------------|-------------|-------------|
| `PLAN` | `NOT_STARTED` | Dispatch `loop-planner` (with DAG generation) |
| `PLAN` | `IN_PROGRESS` | Resume `loop-planner` |
| `PLAN` | `PASSED` | Advance to `EVALUATE_PLAN` |
| `EVALUATE_PLAN` | `NOT_STARTED` | Dispatch `loop-plan-evaluator` + DAG validation |
| `EVALUATE_PLAN` | `BOARD_REVIEW` | Invoke Board (full or collapsed) |
| `EVALUATE_PLAN` | `PASSED` | Advance to `PARALLEL_EXECUTE` |
| `EVALUATE_PLAN` | `FAILED` | Increment `plan_revision_count`; if ≥ max (3) → `completeWithWarnings`; else back to `PLAN` |
| `PARALLEL_EXECUTE` | `NOT_STARTED` | **NEW**: Initialize message bus, dispatch parallel workers |
| `PARALLEL_EXECUTE` | `IN_PROGRESS` | Monitor workers via message bus |
| `PARALLEL_EXECUTE` | `PASSED` | Advance to `EVALUATE_EXECUTION` |
| `PARALLEL_EXECUTE` | `PARTIAL_FAIL` | Handle failures, continue independent tasks |
| `EVALUATE_EXECUTION` | `NOT_STARTED` | Dispatch evaluators + quick board review |
| `EVALUATE_EXECUTION` | `PASSED` | Check `business_sync_required` → `BUSINESS_SYNC` or `COMPLETE` |
| `EVALUATE_EXECUTION` | `FAILED` | Advance to `FIX` |
| `FIX` | `NOT_STARTED` | Check `fix_cycle_count` → dispatch `loop-fixer` or escalate |
| `FIX` | `IN_PROGRESS` | Resume `loop-fixer` |
| `FIX` | `PASSED` | Go back to `EVALUATE_EXECUTION` |
| `BUSINESS_SYNC` | `NOT_STARTED` | Dispatch `business-docs-sync` |
| `BUSINESS_SYNC` | `PASSED` | Advance to `COMPLETE` |
| `COMPLETE` | — | Run retrospective, cleanup workers, report success |
| Any | `BLOCKED` | Log blockers, skip blocked tasks, continue with unblocked work |
| Any | `ESCALATE` | Route to Board of Directors for autonomous resolution |

---

## Lead Engineer Consultation System

### When to Consult Leads

Before escalating a decision to user, consult the appropriate Lead Engineer:

| Question Category | Lead to Consult | Skill Path |
|-------------------|-----------------|------------|
| Architecture, patterns, component organization | Architecture Lead | `${CLAUDE_PLUGIN_ROOT}/skills/leads/architecture-lead/SKILL.md` |
| Scope interpretation, requirements, copy | Product Lead | `${CLAUDE_PLUGIN_ROOT}/skills/leads/product-lead/SKILL.md` |
| Implementation, dependencies, tooling | Tech Lead | `${CLAUDE_PLUGIN_ROOT}/skills/leads/tech-lead/SKILL.md` |
| Testing, coverage, quality gates | QA Lead | `${CLAUDE_PLUGIN_ROOT}/skills/leads/qa-lead/SKILL.md` |

### Consultation Flow

```typescript
async function handleDecision(question: Question) {
  // 1. Check Authority Matrix
  const authority = lookupAuthority(question.category);

  // 2. HIGH_IMPACT decisions: check mode
  if (authority === 'HIGH_IMPACT') {
    if (MODE === 'human-in-the-loop') {
      return escalateToUser(question); // HUMAN MODE: ask user
    }
    return escalateToBoard(question); // AGENTIC MODE: board decides
  }

  // 3. LEAD_CONSULT decisions go to appropriate lead
  if (authority === 'LEAD_CONSULT') {
    const lead = getLeadForCategory(question.category);

    // Dispatch lead agent via Task tool
    const response = await Task({
      subagent_type: "general-purpose",
      description: `Consult ${lead} lead`,
      prompt: `You are the ${lead}-lead agent.

        Question: ${question.text}
        Context: ${question.context}

        Follow the ${lead}-lead skill instructions.

        Output your decision in JSON format:
        {
          "lead": "${lead}",
          "decision_made": true/false,
          "decision": "...",
          "reasoning": "...",
          "authority_used": "...",
          "escalate_to": null | "board" | "cto-advisor",
          "escalation_reason": "..."
        }`
    });

    const result = parseLeadResponse(response.output);

    // Log consultation to metadata
    await logConsultation(trackId, result);

    if (result.decision_made) {
      return result.decision;
    }

    // Lead escalated - route to Board of Directors for autonomous resolution (NEVER to user)
    return escalateToBoard({ question: question.text, context: result.escalation_reason });
  }

  // 4. ORCHESTRATOR decisions are made autonomously
  return makeAutonomousDecision(question);
}
```

### Authority Matrix Reference

See `conductor/authority-matrix.md` for the complete decision matrix.

**Quick Reference — High-Impact (Board Decides Autonomously):**
- Budget changes >$50/month → Board evaluates cost/benefit
- Add/remove features from spec → Board assesses scope impact
- Breaking API changes → Board reviews migration path
- Dependencies >50KB → Board evaluates alternatives
- Coverage below 70% → Board decides acceptable threshold
- Security/production data changes → Board reviews risk

**Quick Reference — Lead Can Decide:**
- Architecture: Patterns (existing), component org, schema (additive)
- Product: Spec interpretation, copy, task order
- Tech: Dependencies <50KB, implementation approach
- QA: Coverage 70-90%, test types, mocks

---

## Agent Dispatch Protocol

### Dispatch with Metadata Updates

Each agent dispatch includes instructions to update metadata.json:

```typescript
// Example: Dispatching executor with resumption
Task({
  subagent_type: "general-purpose",
  description: "Execute track tasks",
  prompt: `You are the loop-executor agent for track ${trackId}.

    METADATA STATE:
    - Current step: EXECUTE
    - Tasks completed: ${metadata.loop_state.checkpoints.EXECUTE.tasks_completed}
    - Last task: ${metadata.loop_state.checkpoints.EXECUTE.last_task}
    - Resume from: Next [ ] task after "${lastTask}"

    Your task:
    1. read_file conductor/tracks/${trackId}/plan.md
    2. Skip all [x] tasks - they are already done
    3. Find first [ ] task after "${lastTask}"
    4. Implement following loop-executor skill
    5. After EACH task completion:
       - Mark [x] in plan.md with commit SHA
       - Update metadata.json checkpoints.EXECUTE:
         - tasks_completed++
         - last_task = "Task X.Y"
         - last_commit = "sha"
    6. Continue until all tasks complete

    MANDATORY: Update metadata.json after every task for resumption support.`
})
```

### Agent Roster (v3) — with Model Allocation

**Use Opus for planning/strategy, Sonnet for execution/implementation.** This saves tokens while maintaining quality.

| Step | Agent | Skill | Model | Rationale |
|------|-------|-------|-------|-----------|
| PRE-PLAN | Knowledge Manager | `knowledge-manager` | **sonnet** | Data retrieval |
| PLAN | Planner | `loop-planner` | **opus** | Strategic planning requires deep thinking |
| EVALUATE_PLAN | Plan Evaluator | `loop-plan-evaluator` | **opus** | Architectural judgment |
| EVALUATE_PLAN | **Board** | `board-of-directors` | **opus** | Nuanced deliberation |
| PARALLEL_EXECUTE | **Workers** | `worker-templates/*` | **sonnet** | Procedural code execution |
| EVALUATE_EXECUTION | Exec Evaluator | `loop-execution-evaluator` | **sonnet** | Checklist-based evaluation |
| FIX | Fixer | `loop-fixer` | **sonnet** | Follows evaluation report |
| BUSINESS_SYNC | Biz Doc Sync | `business-docs-sync` | **sonnet** | Document updates |
| POST-COMPLETE | Retrospective | `retrospective-agent` | **sonnet** | Pattern extraction |

---

## Parallel Execution Engine (v3)

### When to Use Parallel Execution

Parallel execution is used when:
- Plan contains `dag:` block with `parallel_groups`
- DAG validation passed in EVALUATE_PLAN
- Track has 3+ tasks that can run concurrently

### PARALLEL_EXECUTE Step

```typescript
async function stepParallelExecute(trackId: string, metadata: dict) {
  // 1. Initialize message bus
  const busPath = await initMessageBus(`conductor/tracks/${trackId}`);

  // 2. Parse DAG from plan.md
  const dag = await parseDagFromPlan(trackId);

  // 3. Import parallel dispatch utilities
  const { execute_parallel_phase } = require('parallel-dispatch');

  // 4. Execute all parallel groups
  const result = await execute_parallel_phase(dag, trackId, busPath, metadata);

  // 5. Update metadata with results
  metadata.loop_state.parallel_state = {
    total_workers_spawned: result.workers_spawned,
    completed_workers: result.all_tasks_completed.length,
    failed_workers: Object.keys(result.failed_tasks).length,
    parallel_groups_completed: result.parallel_groups_executed
  };

  // 6. Determine next step
  if (result.success) {
    return { next_step: 'EVALUATE_EXECUTION', status: 'PASSED' };
  } else if (result.escalate) {
    return { next_step: 'ESCALATE', reason: result.escalate_reason };
  } else {
    return { next_step: 'FIX', failures: result.failed_tasks };
  }
}
```

### Worker Dispatch via Task Tool

Workers are dispatched using parallel Task calls:

```typescript
// Dispatch 3 workers in parallel (single message, multiple tool calls)
await Promise.all([
  Task({
    subagent_type: "general-purpose",
    description: "Execute Task 1.1: Create store",
    prompt: workerPrompts["1.1"],
    run_in_background: true
  }),
  Task({
    subagent_type: "general-purpose",
    description: "Execute Task 1.2: Build resolver",
    prompt: workerPrompts["1.2"],
    run_in_background: true
  }),
  Task({
    subagent_type: "general-purpose",
    description: "Execute Task 1.3: Add validation",
    prompt: workerPrompts["1.3"],
    run_in_background: true
  })
]);
```

### Worker Monitoring

Monitor workers via message bus polling:

```typescript
async function monitorWorkers(busPath: string, taskIds: string[]) {
  const pending = new Set(taskIds);
  const completed = new Set();
  const failed = {};

  while (pending.size > 0) {
    // Check for completions
    for (const taskId of pending) {
      const eventFile = `${busPath}/events/TASK_COMPLETE_${taskId}.event`;
      if (await exists(eventFile)) {
        pending.delete(taskId);
        completed.add(taskId);
      }

      const failFile = `${busPath}/events/TASK_FAILED_${taskId}.event`;
      if (await exists(failFile)) {
        pending.delete(taskId);
        failed[taskId] = await getFailureReason(busPath, taskId);
      }
    }

    // Check for stale workers
    const stale = await checkStaleWorkers(busPath, thresholdMinutes=10);
    for (const worker of stale) {
      if (pending.has(worker.task_id)) {
        failed[worker.task_id] = `Stale: no heartbeat for ${worker.minutes_stale}m`;
        pending.delete(worker.task_id);
      }
    }

    await sleep(5000);
  }

  return { completed: [...completed], failed };
}
```

---

## Board of Directors Integration (v3)

### When to Invoke the Board

The full multi-agent Board (5 parallel Opus calls + discussion rounds) is reserved for **genuinely high-stakes** decisions. Routine evaluation uses a single structured Opus call ("collapsed board") that delivers comparable depth at ~1/10th the cost.

| Checkpoint | Condition | Review Type |
|------------|-----------|-------------|
| EVALUATE_PLAN | Production deploy, security architecture change, breaking API, data-loss migration | Full meeting (5 agents) |
| EVALUATE_PLAN | All other tracks | Collapsed board (1 Opus call) |
| EVALUATE_EXECUTION | board_conditions exist from EVALUATE_PLAN | Verify conditions only |
| CONFLICT | Evaluators disagree with no clear resolution | Full meeting (5 agents) |

```typescript
function isHighStakesTrack(metadata: dict, planContent: string): boolean {
  const highStakesSignals = [
    /production.deploy|prod\s+release/i,
    /security\s+architect|auth\s+overhaul|oauth\s+migration/i,
    /breaking\s+(api|change)|remove.*endpoint|rename.*field/i,
    /data.*migration|schema.*drop|column.*drop|irreversible/i,
  ];
  const combined = `${metadata.spec_summary || ''} ${planContent}`;
  return highStakesSignals.some(re => re.test(combined));
}
```

### Invoking Board at EVALUATE_PLAN

```typescript
async function evaluatePlanWithBoard(trackId: string, metadata: dict) {
  // 1. Run standard plan evaluation
  const evalResult = await dispatchPlanEvaluator(trackId);
  const planContent = await readFile(`conductor/tracks/${trackId}/plan.md`);

  // 2. Choose review type based on stakes
  let boardResult: dict;
  if (isHighStakesTrack(metadata, planContent)) {
    // Full multi-agent deliberation for genuinely high-stakes decisions
    boardResult = await invokeBoardMeeting(
      busPath: `conductor/tracks/${trackId}/.message-bus`,
      checkpoint: "EVALUATE_PLAN",
      proposal: planContent,
      context: { spec: metadata.spec_summary, dag: evalResult.dag }
    );
  } else {
    // Collapsed board: single structured Opus call (routine tracks)
    boardResult = await collapsedBoardEval(planContent, metadata.spec_summary);
  }

  // 3. Store session record
  metadata.loop_state.board_sessions = metadata.loop_state.board_sessions || [];
  metadata.loop_state.board_sessions.push({
    checkpoint: "EVALUATE_PLAN",
    review_type: isHighStakesTrack(metadata, planContent) ? "full" : "collapsed",
    verdict: boardResult.verdict,
    conditions: boardResult.conditions,
    timestamp: new Date().toISOString()
  });

  // 4. Handle verdict
  if (boardResult.verdict === "REJECTED") {
    return {
      next_step: "PLAN",
      status: "FAILED",
      reason: "Board rejected plan",
      conditions: boardResult.conditions
    };
  }

  // Carry forward conditions for EVALUATE_EXECUTION
  metadata.board_conditions = boardResult.conditions;
  return { next_step: "PARALLEL_EXECUTE", status: "PASSED" };
}
```

### Collapsed Board Evaluation (Single Opus Call)

For all non-high-stakes tracks, replace the 10+ Opus call board with one structured call:

```typescript
async function collapsedBoardEval(planContent: string, specSummary: string): Promise<dict> {
  const result = await Task({
    subagent_type: "general-purpose",
    model: "opus",
    description: "Multi-lens plan evaluation",
    prompt: `Evaluate this implementation plan from 5 perspectives.
For each lens give: verdict (APPROVE/REJECT/CONCERN), score 1-10, up to 3 conditions.

SPEC: ${specSummary}

PLAN:
${planContent}

Lenses: technical_architecture | product_value | security_risk | operational_feasibility | ux_impact

Output strictly as JSON:
{
  "lenses": {
    "technical_architecture": {"verdict": "APPROVE|REJECT|CONCERN", "score": 0, "conditions": []},
    "product_value":          {"verdict": "APPROVE|REJECT|CONCERN", "score": 0, "conditions": []},
    "security_risk":          {"verdict": "APPROVE|REJECT|CONCERN", "score": 0, "conditions": []},
    "operational_feasibility":{"verdict": "APPROVE|REJECT|CONCERN", "score": 0, "conditions": []},
    "ux_impact":              {"verdict": "APPROVE|REJECT|CONCERN", "score": 0, "conditions": []}
  },
  "verdict": "APPROVED|REJECTED|CONDITIONS",
  "blocking_conditions": [],
  "advisory_conditions": []
}`
  });

  const parsed = JSON.parse(result.output);
  const rejectCount = Object.values(parsed.lenses).filter((l: any) => l.verdict === "REJECT").length;

  return {
    verdict: rejectCount >= 2 ? "REJECTED" : (parsed.blocking_conditions.length > 0 ? "CONDITIONS" : "APPROVED"),
    conditions: [...parsed.blocking_conditions, ...parsed.advisory_conditions]
  };
}
```

### Board Condition Verification at EVALUATE_EXECUTION

```typescript
async function evaluateExecutionWithBoard(trackId: string, metadata: dict) {
  // 1. Run specialized evaluators
  const evalResults = await dispatchSpecializedEvaluators(trackId);

  // 2. Verify board conditions from EVALUATE_PLAN (if any)
  if (metadata.board_conditions?.length > 0) {
    const conditionsMet = await verifyBoardConditions(
      metadata.board_conditions,
      evalResults
    );
    if (!conditionsMet.all_met) {
      return {
        next_step: "FIX",
        status: "FAILED",
        reason: `Board conditions not met: ${conditionsMet.unmet.join(", ")}`
      };
    }
  }

  return evalResults.all_passed
    ? { next_step: "BUSINESS_SYNC", status: "PASSED" }
    : { next_step: "FIX", status: "FAILED" };
}
```

---

## V3 State Machine Diagram

```
                              TRACK START
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │    KNOWLEDGE MANAGER     │
                    │    (Load patterns)       │
                    └────────────┬─────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PLAN (with DAG)                                 │
│  loop-planner generates plan.md with explicit dependency graph              │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    EVALUATE_PLAN + BOARD MEETING                             │
│                                                                              │
│  1. DAG Validation (cycles, conflicts)                                       │
│  2. Standard checks (scope, overlap, deps, quality)                          │
│  3. For MAJOR tracks → invoke /board-meeting                                │
│     ┌──────────────────────────────────────────────────────────────────┐    │
│     │  BOARD DELIBERATION                                               │    │
│     │  Phase 1: All 5 directors ASSESS in parallel                      │    │
│     │  Phase 2: Directors DISCUSS via message bus                       │    │
│     │  Phase 3: Directors VOTE                                          │    │
│     │  Phase 4: RESOLVE → APPROVED / REJECTED / CONDITIONS              │    │
│     └──────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  PASS → Continue   |   FAIL → Back to PLAN with conditions                  │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PARALLEL_EXECUTE                                     │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        MESSAGE BUS                                   │    │
│  │  queue.jsonl | locks.json | worker-status.json | events/            │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
│  For each parallel_group in DAG:                                            │
│    1. agent-factory creates specialized workers                             │
│    2. Dispatch via parallel Task(run_in_background=true)                   │
│    3. Workers coordinate via message bus:                                    │
│       - FILE_LOCK / FILE_UNLOCK for shared files                           │
│       - PROGRESS updates every 5 min                                        │
│       - TASK_COMPLETE / TASK_FAILED when done                              │
│    4. Monitor for completion, handle failures                               │
│    5. Cleanup ephemeral workers                                              │
│                                                                              │
│  ┌──────┐ ┌──────┐ ┌──────┐                                                 │
│  │Worker│ │Worker│ │Worker│  (max 5 concurrent)                            │
│  │ 1.1  │ │ 1.2  │ │ 1.3  │                                                 │
│  └──┬───┘ └──┬───┘ └──┬───┘                                                 │
│     └────────┴────────┘                                                      │
│              │                                                               │
│  PASS → Continue   |   PARTIAL_FAIL → Isolate + Continue                    │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                 EVALUATE_EXECUTION + BOARD REVIEW                            │
│                                                                              │
│  1. Specialized evaluators (UI, Code, Integration, Business)                │
│  2. Quick board review (no discussion)                                       │
│  3. Verify board conditions from EVALUATE_PLAN                              │
│                                                                              │
│  PASS → BUSINESS_SYNC? → COMPLETE                                           │
│  FAIL → FIX (with specific failures)                                        │
└──────────────────────────────────┬──────────────────────────────────────────┘
                                   │
                              ┌────┴────┐
                              │         │
                         PASS ▼    FAIL ▼
                    ┌──────────┐  ┌──────────┐
                    │BUSINESS  │  │   FIX    │
                    │  SYNC    │  │ (max 3x) │
                    └────┬─────┘  └────┬─────┘
                         │             │
                         ▼             │
                    ┌──────────┐       │
                    │ COMPLETE │◄──────┘
                    │          │   (after fix passes)
                    └────┬─────┘
                         │
                         ▼
                    ┌──────────────────────────┐
                    │   RETROSPECTIVE AGENT    │
                    │   + Cleanup workers      │
                    └──────────────────────────┘
```

---

## Resumption Protocol

When orchestrator starts, it resumes from exact state:

```typescript
async function resumeOrchestration(trackId: string) {
  const { current_step, step_status, metadata } = await detectCurrentStep(trackId);

  // Reconcile plan.md checkboxes with metadata before resuming EXECUTE
  if (current_step === 'PARALLEL_EXECUTE' || current_step === 'EXECUTE') {
    await reconcileProgress(trackId);
  }

  switch (step_status) {
    case 'NOT_STARTED':
      // Start the step fresh
      return dispatchAgent(current_step, metadata);

    case 'IN_PROGRESS':
      // Resume the step with checkpoint data
      const checkpoint = metadata.loop_state.checkpoints[current_step];
      return resumeAgent(current_step, checkpoint);

    case 'PASSED':
      // Move to next step
      const nextStep = getNextStep(current_step, 'PASS');
      await updateMetadata(trackId, { current_step: nextStep, step_status: 'NOT_STARTED' });
      return dispatchAgent(nextStep, metadata);

    case 'FAILED':
      // Handle based on which step failed
      if (current_step === 'EVALUATE_PLAN') {
        // Guard against infinite PLAN→EVALUATE_PLAN loops
        const revisionCount = (metadata.loop_state.plan_revision_count || 0) + 1;
        const maxRevisions = config.max_plan_revisions || 3;
        if (revisionCount >= maxRevisions) {
          await logAutonomousDecision(trackId, 'plan_revision_limit',
            `Plan revision limit (${maxRevisions}) reached — completing with warnings`);
          return completeWithWarnings(trackId);
        }
        await updateMetadata(trackId, {
          current_step: 'PLAN',
          step_status: 'NOT_STARTED',
          loop_state: {
            ...metadata.loop_state,
            plan_revision_count: revisionCount
          }
        });
        return dispatchAgent('PLAN', metadata);
      }
      if (current_step === 'EVALUATE_EXECUTION') {
        // Check fix cycle limit
        if (metadata.loop_state.fix_cycle_count >= 5) {
          // NEVER escalate to user — complete with warnings
          await logAutonomousDecision(trackId, 'fix_limit_reached', 'Completed with unresolved issues after 5 fix cycles');
          return completeWithWarnings(trackId);
        }
        await updateMetadata(trackId, {
          current_step: 'FIX',
          step_status: 'NOT_STARTED',
          fix_cycle_count: metadata.loop_state.fix_cycle_count + 1
        });
        return dispatchAgent('FIX', metadata);
      }

    case 'BLOCKED':
      // Check if blocker is resolved
      const activeBlockers = metadata.blockers.filter(b => b.status === 'ACTIVE');
      if (activeBlockers.length > 0) {
        // NEVER escalate to user — log blocker and skip blocked tasks
        await logAutonomousDecision(trackId, 'blocker_skipped', `Skipped blocked tasks: ${activeBlockers[0].description}`);
        await skipBlockedTasks(trackId, activeBlockers);
      }
      // Blocker resolved, continue
      await updateMetadata(trackId, { step_status: 'NOT_STARTED' });
      return dispatchAgent(current_step, metadata);
  }
}
```

### Resumption by Step

| Step | Resumption Data | Action |
|------|-----------------|--------|
| PLAN | `checkpoints.PLAN.plan_version` | Re-run planner if revising |
| EXECUTE | `checkpoints.EXECUTE.last_task` | Skip completed tasks, continue from next |
| FIX | `checkpoints.FIX.fixes_remaining` | Continue with remaining fixes |

---

## The Full Loop (Automated)

```
┌─────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATOR                             │
│                                                                 │
│  1. read_file metadata.json → detect current_step + step_status      │
│  2. Dispatch appropriate agent via Task tool                    │
│  3. Agent updates metadata.json checkpoints                     │
│  4. Agent returns → orchestrator reads new state                │
│  5. Continue to next step or handle failure                     │
│  6. Loop until COMPLETE or escalation needed                    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

PLAN ──► EVALUATE_PLAN ──► EXECUTE ──► EVALUATE_EXECUTION
  ▲            │                              │
  │        FAIL → back                   PASS → BUSINESS_SYNC? → COMPLETE
  │                                      FAIL → FIX
  │                                             │
  └─────────────────────────────────────────────┘
                    (after fix, re-evaluate)
```

---

## Resolution Triggers (Mode-Dependent)

**Behavior depends on `conductor/config.json` → `mode`:**
- **`"agentic"`**: All situations resolved autonomously. Never stops.
- **`"human-in-the-loop"`**: Pauses at each trigger below and asks the user.

1. **Fix cycle limit (5 cycles)** → Complete track with warnings, log unresolved issues
2. **Plan revision limit (3 revisions)** → Complete track with warnings, log board conditions
3. **HIGH_IMPACT decision** → Route to Board of Directors for autonomous deliberation
4. **Lead escalated** → Lead returned `escalate_to: "board"` → route to Board of Directors
5. **Blocker detected** → Log blocker, skip blocked tasks, continue with unblocked work
6. **Max iterations (50)** → Complete track with warnings, log all progress

### Progress Logging Format

```json
{
  "autonomous_decisions": [
    {
      "timestamp": "...",
      "type": "fix_limit_reached|blocker_skipped|board_decided|ambiguity_resolved",
      "context": "What was happening",
      "decision": "What was decided",
      "reasoning": "Why this was chosen"
    }
  ]
}
```

---

## Autonomous Resolution Utility Functions

These utility functions implement the autonomous resolution patterns. They operate on metadata.json:

### `logAutonomousDecision(trackId, type, reasoning)`

Append a decision record to the `autonomous_decisions` array in metadata.json:
```json
{
  "timestamp": "{ISO timestamp}",
  "type": "ambiguity_resolved|blocker_skipped|board_decided|fix_limit_reached|completed_with_warnings",
  "context": "{current_step at time of decision}",
  "decision": "{what was decided}",
  "reasoning": "{why this was chosen}"
}
```

### `escalateToBoard(question)`

Dispatch a board meeting for autonomous resolution:
1. Spawn: `claude --print --model opus "/orchestrator-supaconductor:board-meeting {question}"`
2. Parse board verdict (APPROVED / REJECTED)
3. If APPROVED → continue with board conditions as constraints
4. If REJECTED → re-plan incorporating all board feedback
5. Log board decision via `logAutonomousDecision()`

### `skipBlockedTasks(trackId, activeBlockers)`

Skip blocked tasks and continue with unblocked work:
1. Read plan.md and mark blocked tasks as `[~] SKIPPED`
2. Add each blocker to metadata.json `"blockers"` array with description and timestamp
3. Continue executing the next unblocked task in DAG order

### `completeWithWarnings(trackId)`

Complete the track with warnings instead of blocking:
1. Update metadata.json: `current_step = "COMPLETE"`, `step_status = "PASSED_WITH_WARNINGS"`
2. Add `"warnings"` array to metadata with unresolved issues
3. Update tracks.md — mark track as "Done (with warnings)"
4. Log via `logAutonomousDecision("completed_with_warnings", ...)`
5. Output summary report listing all warnings

### `reconcileProgress(trackId)`

Reconcile `plan.md` checkbox markers with `metadata.json` task count on resumption.
plan.md is the ground truth — if the counts diverge, update metadata to match:

```typescript
async function reconcileProgress(trackId: string) {
  const planPath = `conductor/tracks/${trackId}/plan.md`;
  const metaPath = `conductor/tracks/${trackId}/metadata.json`;
  const metadata = await readJSON(metaPath);

  const completedInMeta = metadata.loop_state.checkpoints?.EXECUTE?.tasks_completed || 0;
  const planMtime = await getFileMtime(planPath);
  const metaMtime = await getFileMtime(metaPath);

  // Skip reconciliation if metadata was written after plan.md (already in sync)
  if (metaMtime >= planMtime && completedInMeta > 0) {
    return;
  }

  const plan = await readFile(planPath);
  // Match both '- [x]' and '* [x]' (case-insensitive) to handle markdown variants
  const completedInPlan = (plan.match(/^[*-] \[[xX]\]/gm) || []).length;

  if (completedInPlan !== completedInMeta) {
    metadata.loop_state.checkpoints = metadata.loop_state.checkpoints || {};
    metadata.loop_state.checkpoints.EXECUTE = metadata.loop_state.checkpoints.EXECUTE || {};
    metadata.loop_state.checkpoints.EXECUTE.tasks_completed = completedInPlan;
    await writeJSON(metaPath, metadata);
    console.warn(`[reconcile] plan.md=${completedInPlan} vs metadata=${completedInMeta} — metadata updated`);
  }
}
```

---

## Track Completion Protocol

When `current_step` reaches `COMPLETE`:

1. **Update metadata.json**
```json
{
  "status": "complete",
  "completed_at": "[timestamp]",
  "loop_state": {
    "current_step": "COMPLETE",
    "step_status": "PASSED"
  }
}
```

2. **Update tracks.md** — Move track to "Done" table with date

3. **Update conductor/index.md** — Update current status

4. **Commit** — `docs: complete [track-id] - evaluation passed`

5. **Report to user**

6. **Run Retrospective** (after completion commit):
   Dispatch agent: "read_file conductor/tracks/{trackId}/plan.md and git log.
   Extract reusable patterns → append to conductor/knowledge/patterns.md
   Extract error fixes → append to conductor/knowledge/errors.json
   Create files if they don't exist."
```markdown
## Track Complete

**Track**: [track-id]
**Phases**: [count] completed
**Tasks**: [count] completed
**Evaluation**: PASS — all checks passed
**Lead Consultations**: [count] decisions made autonomously
**Commits**: [list of key commits]

**Next track**: [suggest from tracks.md]
```

---

## CTO Advisor Integration

For **technical tracks**, automatically include CTO review during EVALUATE_PLAN:

```typescript
// Detect if track is technical
const technicalKeywords = [
  'architecture', 'system design', 'integration', 'API', 'database',
  'schema', 'migration', 'infrastructure', 'scalability', 'performance',
  'security', 'authentication', 'authorization', 'deployment'
];

const isTechnical = technicalKeywords.some(keyword =>
  spec.toLowerCase().includes(keyword) || plan.toLowerCase().includes(keyword)
);

if (isTechnical) {
  // Include CTO review in plan evaluation
  dispatchPrompt += `
    This is a TECHNICAL track. Your evaluation must include:
    1. Standard plan checks (scope, overlap, dependencies, clarity)
    2. CTO technical review using cto-plan-reviewer skill

    Both must PASS for plan evaluation to pass.`;
}
```

---

## Learning Layer Integration

The orchestrator integrates the Knowledge Layer for continuous learning:

### Pre-Planning: Knowledge Manager

**BEFORE** dispatching the planner, run Knowledge Manager to load relevant patterns. The brief is **capped at 500 tokens** (top-3 most relevant patterns) to prevent unbounded growth as the knowledge base accumulates:

```typescript
async function dispatchPlannerWithKnowledge(trackId: string) {
  // 1. Run Knowledge Manager with bounded retrieval
  const knowledgeBrief = await Task({
    subagent_type: "general-purpose",
    description: "Load knowledge for track",
    prompt: `You are the knowledge-manager agent.

      Track: ${trackId}
      Spec: ${await readFile(`conductor/tracks/${trackId}/spec.md`)}

      1. Extract the top 5 keywords from the spec
      2. Score each pattern in conductor/knowledge/patterns.md by keyword overlap count
      3. Return ONLY the top 3 highest-scoring patterns (skip patterns with score 0)
      4. Score each entry in conductor/knowledge/errors.json by keyword overlap
      5. Return ONLY the top 3 highest-scoring errors (skip score-0 entries)
      6. Cap total output at 500 tokens — truncate lower-priority entries if needed

      Follow ${CLAUDE_PLUGIN_ROOT}/skills/knowledge/knowledge-manager/SKILL.md`
  });

  // 2. Dispatch planner WITH bounded knowledge brief
  await Task({
    subagent_type: "general-purpose",
    description: "Create track plan",
    prompt: `You are the loop-planner agent for track ${trackId}.

      ## KNOWLEDGE BRIEF (top-3 relevant patterns/errors, max 500 tokens)
      ${knowledgeBrief.output}

      ## YOUR TASK
      Create plan.md using the patterns above where applicable.
      Avoid the known errors listed.

      Follow ${CLAUDE_PLUGIN_ROOT}/skills/loop-planner/SKILL.md`
  });
}
```

### Post-Completion: Retrospective Agent

**AFTER** a track reaches COMPLETE, run Retrospective Agent to extract learnings:

```typescript
async function runPostCompletionRetrospective(trackId: string) {
  await Task({
    subagent_type: "general-purpose",
    description: "Run track retrospective",
    prompt: `You are the retrospective-agent.

      Track: ${trackId}

      1. read_file conductor/tracks/${trackId}/plan.md (all tasks and fix cycles)
      2. read_file conductor/tracks/${trackId}/metadata.json (fix counts, consultations)
      3. Analyze: What worked? What failed? What patterns emerged?
      4. Update conductor/knowledge/patterns.md with new reusable solutions
      5. Update conductor/knowledge/errors.json with new error patterns
      6. write_file retrospective to conductor/tracks/${trackId}/retrospective.md
      7. Propose skill improvements if workflow issues found

      Follow ${CLAUDE_PLUGIN_ROOT}/skills/knowledge/retrospective-agent/SKILL.md`
  });
}
```

### Updated State Machine with Learning

```
                              TRACK START
                                   │
                                   ▼
                    ┌──────────────────────────┐
                    │    KNOWLEDGE MANAGER     │  ◄── NEW: Load patterns & errors
                    │    (Pre-planning intel)  │
                    └────────────┬─────────────┘
                                 │
                                 ▼
PLAN ──► EVALUATE_PLAN ──► EXECUTE ──► EVALUATE_EXECUTION
  ▲            │                              │
  │        FAIL → back                   PASS → BUSINESS_SYNC? → COMPLETE
  │                                      FAIL → FIX                  │
  │                                             │                    │
  └─────────────────────────────────────────────┘                    │
                                                                     ▼
                                                    ┌──────────────────────────┐
                                                    │   RETROSPECTIVE AGENT    │  ◄── NEW
                                                    │   (Extract learnings)    │
                                                    └────────────┬─────────────┘
                                                                 │
                                                                 ▼
                                                    ┌──────────────────────────┐
                                                    │    KNOWLEDGE BASE        │
                                                    │  patterns.md + errors.json│
                                                    └──────────────────────────┘
                                                                 │
                                                                 ▼
                                                          NEXT TRACK
                                                    (now smarter than before)
```

### Knowledge Layer Files

| File | Purpose | Updated By |
|------|---------|------------|
| `conductor/knowledge/patterns.md` | Reusable solutions | Retrospective Agent |
| `conductor/knowledge/errors.json` | Error → Fix registry | Retrospective Agent, Fixer |
| `conductor/tracks/[id]/retrospective.md` | Track-specific learnings | Retrospective Agent |

### Fixer Integration with Error Registry

The loop-fixer also uses the error registry:

```typescript
// In loop-fixer, before attempting a fix
async function findKnownSolution(errorMessage: string) {
  const errors = JSON.parse(await readFile('conductor/knowledge/errors.json'));

  for (const error of errors.errors) {
    if (new RegExp(error.pattern, 'i').test(errorMessage)) {
      return {
        found: true,
        solution: error.solution,
        code_fix: error.code_fix
      };
    }
  }

  return { found: false };
}

// After fixing a new error, log it
async function logNewError(pattern, solution, trackId) {
  const errors = JSON.parse(await readFile('conductor/knowledge/errors.json'));
  errors.errors.push({
    id: `err-${String(errors.errors.length + 1).padStart(3, '0')}`,
    pattern,
    solution,
    discovered_in: trackId,
    last_seen: new Date().toISOString().split('T')[0]
  });
  await writeFile('conductor/knowledge/errors.json', JSON.stringify(errors, null, 2));
}
```

---

## Quick Reference

### Starting a Track

```
User: /conductor implement

Orchestrator:
1. read_file conductor/tracks.md → get active track
2. read_file conductor/tracks/[track]/metadata.json → get loop_state
3. Determine current step and status
4. Dispatch appropriate agent
5. Loop until complete
```

### State Locations

| Data | Location | Purpose |
|------|----------|---------|
| Loop state | `metadata.json → loop_state` | Primary state machine |
| Task progress | `plan.md` markers | Human-readable progress |
| Lead decisions | `metadata.json → lead_consultations` | Decision audit trail |
| Blockers | `metadata.json → blockers` | Escalation tracking |
| Authority rules | `conductor/authority-matrix.md` | Decision boundaries |

### Files Modified by Orchestrator

- `conductor/tracks/[track]/metadata.json` — State updates
- `conductor/tracks.md` — Completion tracking
- `conductor/index.md` — Current status

