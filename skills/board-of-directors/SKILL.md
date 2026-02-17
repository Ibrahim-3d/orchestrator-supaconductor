---
name: board-of-directors
description: "Simulate a 5-member expert board deliberation for major decisions. Use when evaluating plans, architecture choices, feature designs, or any decision requiring multi-perspective expert analysis. Triggers: 'board review', 'get expert opinions', 'board meeting', 'director evaluation', 'consensus review'."
---

# Board of Directors Simulation

Simulates a 5-member expert board that deliberates, debates, and reaches consensus on major decisions. Each director brings domain expertise and can challenge other directors' opinions.

## The Board

| Role | Domain | Evaluates |
|------|--------|-----------|
| **Chief Architect (CA)** | Technical | System design, patterns, scalability, tech debt, code quality |
| **Chief Product Officer (CPO)** | Product | User value, market fit, feature priority, scope, usability |
| **Chief Security Officer (CSO)** | Security | Vulnerabilities, compliance, data protection, risk assessment |
| **Chief Operations Officer (COO)** | Execution | Feasibility, timeline, resources, process, deployment |
| **Chief Experience Officer (CXO)** | Experience | UX/UI, accessibility, user journey, design consistency |

## When to Invoke the Board

- **Track Planning** — Before starting major tracks
- **Architecture Decisions** — ADRs, system design choices
- **Feature Evaluation** — New feature proposals
- **Risk Assessment** — Security or operational concerns
- **Conflict Resolution** — When leads disagree

## Deliberation Protocol

### Phase 1: Individual Assessment (Parallel)

Each director reviews the proposal independently:

```
DISPATCH via Task tool (all 5 in parallel):
  - CA: Evaluate technical aspects
  - CPO: Evaluate product aspects
  - CSO: Evaluate security aspects
  - COO: Evaluate operational aspects
  - CXO: Evaluate experience aspects
```

Each director outputs:
```json
{
  "director": "CA",
  "verdict": "APPROVE" | "CONCERNS" | "REJECT",
  "score": 1-10,
  "key_points": ["..."],
  "concerns": ["..."],
  "questions_for_board": ["Question for CPO about...", "Challenge to COO on..."]
}
```

### Phase 2: Board Discussion (Sequential via Message Bus)

Directors respond to each other's questions and challenges:

```
MESSAGE BUS: conductor/tracks/{track}/.message-bus/board/

1. Post all Phase 1 assessments to board/assessments.json
2. Each director reads others' assessments
3. Directors post rebuttals/responses to board/discussion.jsonl
4. Max 3 rounds of discussion
```

Discussion message format:
```json
{
  "from": "CA",
  "to": "CPO",
  "type": "CHALLENGE" | "AGREE" | "QUESTION" | "CLARIFY",
  "message": "Regarding your concern about scope...",
  "changes_my_verdict": true | false
}
```

### Phase 3: Final Vote

After discussion, each director casts final vote:

```json
{
  "director": "CA",
  "final_verdict": "APPROVE" | "REJECT",
  "confidence": 0.0-1.0,
  "conditions": ["Must add rate limiting", "Needs load testing"],
  "dissent_noted": false
}
```

### Phase 4: Board Resolution

Aggregate votes and produce board decision:

| Scenario | Resolution |
|----------|------------|
| 5-0 or 4-1 APPROVE | **APPROVED** — Proceed with any conditions noted |
| 3-2 APPROVE | **APPROVED WITH REVIEW** — Proceed but schedule follow-up |
| 3-2 REJECT | **REJECTED** — Address major concerns first |
| 4-1 or 5-0 REJECT | **REJECTED** — Significant rework needed |
| 2-2-1 (tie with abstain) | **ESCALATE** — User makes final call |

## Orchestrator Integration

### Invoke Board from Conductor

```typescript
async function invokeBoardReview(proposal: string, context: object) {
  // 1. Initialize board message bus
  await initBoardMessageBus(trackId);

  // 2. Phase 1: Parallel assessment
  const assessments = await Promise.all([
    Task({
      description: "CA board assessment",
      prompt: `You are the Chief Architect on the Board of Directors.

        PROPOSAL: ${proposal}
        CONTEXT: ${JSON.stringify(context)}

        Follow the directors/chief-architect.md profile.

        Output your assessment as JSON.`
    }),
    Task({ description: "CPO board assessment", ... }),
    Task({ description: "CSO board assessment", ... }),
    Task({ description: "COO board assessment", ... }),
    Task({ description: "CXO board assessment", ... })
  ]);

  // 3. Phase 2: Discussion rounds
  await runBoardDiscussion(assessments, maxRounds: 3);

  // 4. Phase 3: Final vote
  const votes = await collectFinalVotes();

  // 5. Phase 4: Resolution
  return aggregateBoardDecision(votes);
}
```

### Board Output Format

```markdown
## Board of Directors Resolution

**Proposal**: [Brief description]
**Session**: [timestamp]
**Verdict**: APPROVED | APPROVED WITH REVIEW | REJECTED | ESCALATE

### Vote Summary
| Director | Vote | Confidence | Key Condition |
|----------|------|------------|---------------|
| CA | APPROVE | 0.9 | Add caching layer |
| CPO | APPROVE | 0.8 | Validate with usability check |
| CSO | CONCERNS→APPROVE | 0.7 | Security audit before launch |
| COO | APPROVE | 0.85 | Need 2-week buffer |
| CXO | APPROVE | 0.95 | Accessibility is solid |

**Final: 5-0 APPROVE**

### Conditions for Approval
1. Add caching layer for API responses (CA)
2. Complete security audit before production (CSO)
3. Buffer timeline by 2 weeks (COO)

### Discussion Highlights
- CA challenged CPO on scope creep → CPO agreed to defer Phase 2
- CSO raised auth concern → CA proposed token rotation solution
- CXO praised accessibility approach, no concerns

### Dissenting Opinions
None recorded.

---
*Board session complete. Proceed with implementation.*
```

## Director Skills

Each director has specialized evaluation criteria. See:

- `directors/chief-architect.md` — Technical excellence
- `directors/chief-product-officer.md` — Product value
- `directors/chief-security-officer.md` — Security posture
- `directors/chief-operations-officer.md` — Execution reality
- `directors/chief-experience-officer.md` — User experience

## Quick Invocation

For rapid board review without full deliberation:

```markdown
/board-review [proposal]

Returns: Quick assessment from each director (no discussion phase)
```

For full deliberation:

```markdown
/board-meeting [proposal]

Returns: Full 4-phase deliberation with discussion
```

## Integration with Evaluate-Loop

The board can be invoked at key checkpoints:

| Checkpoint | Board Involvement |
|------------|-------------------|
| EVALUATE_PLAN | Full board meeting for major tracks |
| EVALUATE_EXECUTION | Quick review for implementation quality |
| Pre-Launch | Security + Operations deep dive |
| Post-Mortem | All directors analyze what went wrong |

## Message Bus Structure

```
.message-bus/board/
├── session-{timestamp}.json    # Session metadata
├── assessments.json            # Phase 1 outputs
├── discussion.jsonl            # Phase 2 messages
├── votes.json                  # Phase 3 final votes
└── resolution.md               # Phase 4 board decision
```
