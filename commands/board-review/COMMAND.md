---
name: board-review
description: "Quick board review - get expert opinions from 5 directors without full deliberation"
arguments:
  - name: proposal
    type: string
    description: "The proposal, plan, or decision to review"
    required: false
---

# /board-review — Quick Expert Assessment

Run a quick assessment from the 5-member Board of Directors. Each director provides their expert opinion in parallel, without the discussion phase.

## Usage

```
/board-review [proposal or leave blank to review current track]
```

## Workflow

1. **Load Proposal** — From argument or current track's plan.md
2. **Parallel Assessment** — All 5 directors evaluate simultaneously
3. **Aggregate Results** — Combine verdicts into summary

## Directors

| Director | Domain |
|----------|--------|
| **CA** - Chief Architect | Technical design, scalability, patterns |
| **CPO** - Chief Product Officer | User value, market fit, scope |
| **CSO** - Chief Security Officer | Security, compliance, risk |
| **COO** - Chief Operations Officer | Feasibility, timeline, resources |
| **CXO** - Chief Experience Officer | UX/UI, accessibility, design |

## Execution

```typescript
// Dispatch all 5 directors in parallel
const assessments = await Promise.all([
  Task({
    subagent_type: "general-purpose",
    description: "CA board assessment",
    prompt: `You are the Chief Architect.
      Proposal: ${proposal}
      Follow .claude/skills/board-of-directors/directors/chief-architect.md
      Output JSON assessment.`
  }),
  // ... CPO, CSO, COO, CXO
]);
```

## Output Format

```markdown
## Quick Board Review

**Proposal**: [summary]

| Director | Verdict | Score | Top Concern |
|----------|---------|-------|-------------|
| CA | APPROVE | 8/10 | Query performance |
| CPO | APPROVE | 9/10 | None |
| CSO | CONCERNS | 6/10 | Rate limiting missing |
| COO | APPROVE | 7/10 | Timeline tight |
| CXO | APPROVE | 8/10 | Minor a11y issues |

**Quick Verdict**: 4-1 APPROVE with conditions

**Key Conditions**:
1. Add rate limiting (CSO)
2. Add query caching (CA)
```
