---
name: board-meeting
description: "Full board deliberation with discussion rounds - directors debate and reach consensus"
arguments:
  - name: proposal
    type: string
    description: "The proposal, plan, or decision to deliberate on"
    required: false
user_invocable: true
---

# /board-meeting — Full Board Deliberation

Run a complete 4-phase board meeting with the 5-member Board of Directors. Directors assess, discuss, debate, and vote to reach consensus.

## Usage

```
/board-meeting [proposal or leave blank to review current track]
```

## The 4 Phases

### Phase 1: Individual Assessment (Parallel)
All 5 directors evaluate the proposal independently and simultaneously.

### Phase 2: Board Discussion (3 Rounds)
Directors respond to each other's concerns and questions via message bus.

### Phase 3: Final Vote
Each director casts their final vote with confidence level.

### Phase 4: Board Resolution
Aggregate votes and produce official board decision.

## Directors

| Director | Domain | Focus |
|----------|--------|-------|
| **CA** | Technical | System design, patterns, scalability |
| **CPO** | Product | User value, scope, usability check |
| **CSO** | Security | Vulnerabilities, compliance, risk |
| **COO** | Operations | Feasibility, timeline, resources |
| **CXO** | Experience | UX/UI, accessibility, journey |

## Resolution Rules

| Votes | Resolution |
|-------|------------|
| 5-0 or 4-1 APPROVE | **APPROVED** |
| 3-2 APPROVE | **APPROVED WITH REVIEW** |
| 3-2 REJECT | **REJECTED** |
| 4-1 or 5-0 REJECT | **REJECTED** |
| Tie/Deadlock | **ESCALATE** to user |

## Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 1: ASSESS                          │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐              │
│  │  CA  │ │ CPO  │ │ CSO  │ │ COO  │ │ CXO  │  (parallel)  │
│  └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘              │
│     └────────┴────────┴────────┴────────┘                   │
│                       │                                      │
│                       ▼                                      │
│              ┌─────────────────┐                            │
│              │  MESSAGE BUS    │                            │
│              └────────┬────────┘                            │
│                       │                                      │
├───────────────────────┼─────────────────────────────────────┤
│                    PHASE 2: DISCUSS                         │
│                       │                                      │
│     Round 1: Initial responses to concerns                  │
│     Round 2: Rebuttals and clarifications                   │
│     Round 3: Final positions                                │
│                       │                                      │
├───────────────────────┼─────────────────────────────────────┤
│                    PHASE 3: VOTE                            │
│                       │                                      │
│  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐              │
│  │ VOTE │ │ VOTE │ │ VOTE │ │ VOTE │ │ VOTE │              │
│  └──────┘ └──────┘ └──────┘ └──────┘ └──────┘              │
│                       │                                      │
├───────────────────────┼─────────────────────────────────────┤
│                    PHASE 4: RESOLVE                         │
│                       │                                      │
│              ┌─────────────────┐                            │
│              │    DECISION     │                            │
│              │  + Conditions   │                            │
│              │  + Dissent log  │                            │
│              └─────────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

## Output Format

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
| CSO | CONCERNS→APPROVE | 0.7 | Security audit first |
| COO | APPROVE | 0.85 | 2-week buffer |
| CXO | APPROVE | 0.95 | A11y is solid |

**Final: 5-0 APPROVE**

### Conditions for Approval
1. Add caching layer for API responses (CA)
2. Complete security audit before production (CSO)
3. Buffer timeline by 2 weeks (COO)

### Discussion Highlights
- CA challenged CPO on scope → CPO agreed to defer Phase 2
- CSO raised auth concern → CA proposed JWT rotation
- CXO praised accessibility approach

### Dissenting Opinions
None recorded.

---
*Board session complete. Proceed with implementation.*
```

## When to Use

- **Major Track Planning** — Before starting significant features
- **Architecture Decisions** — ADRs, system design choices
- **Risk Assessment** — Security or operational concerns
- **Conflict Resolution** — When stakeholders disagree
- **Go/No-Go Decisions** — Launch readiness, major releases
