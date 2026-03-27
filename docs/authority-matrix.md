# Authority Matrix — Lead Engineer Consultation System

This document defines the decision authority levels for the Conductor orchestrator and its Lead Engineer consultation system.

## Authority Levels

| Level | Description | Decision Maker |
|-------|-------------|----------------|
| **HIGH_IMPACT** | High-impact decisions resolved by Board of Directors deliberation | Board of Directors (autonomous) |
| **LEAD_CONSULT** | Decisions within lead's domain expertise and guardrails | Lead Engineer Agent (autonomous) |
| **ORCHESTRATOR** | Routine decisions following established conventions | Orchestrator (autonomous) |

> **IMPORTANT:** No decision level requires user input. The system is fully autonomous. All decisions are logged in metadata.json for post-completion review.

## Decision Matrix

### Budget & Cost

| Decision | Authority | Lead | Guardrails |
|----------|-----------|------|------------|
| Cost increase >$50/month | HIGH_IMPACT | — | Board decides |
| New paid API integration | HIGH_IMPACT | — | Board decides |
| Cost increase <$50/month | LEAD_CONSULT | Tech | Document in decision log |
| Cost optimization (same features) | LEAD_CONSULT | Tech | Document savings |

### Scope & Features

| Decision | Authority | Lead | Guardrails |
|----------|-----------|------|------------|
| Add feature to spec | HIGH_IMPACT | — | Board decides |
| Remove feature from spec | HIGH_IMPACT | — | Board decides |
| Defer spec requirement to future track | HIGH_IMPACT | — | Board decides |
| Change deliverable definition | HIGH_IMPACT | — | Board decides |
| Interpret ambiguous spec | LEAD_CONSULT | Product | Must cite spec section |
| Task prioritization within phase | LEAD_CONSULT | Product | Same phase only |
| Edge case handling approach | LEAD_CONSULT | Product | Within spec intent |
| Default value selection | LEAD_CONSULT | Product | Reasonable defaults |

### Architecture & Patterns

| Decision | Authority | Lead | Guardrails |
|----------|-----------|------|------------|
| New architectural pattern (not in codebase) | HIGH_IMPACT | — | Board decides |
| Breaking change to public API | HIGH_IMPACT | — | Board decides |
| Cross-track architectural change | HIGH_IMPACT | — | Board decides |
| Apply existing codebase pattern | LEAD_CONSULT | Architecture | Document precedent |
| Component folder organization | LEAD_CONSULT | Architecture | Follow conventions |
| API route vs server action | LEAD_CONSULT | Architecture | Cite existing pattern |
| Data flow architecture | LEAD_CONSULT | Architecture | Match established patterns |
| Database schema (additive) | LEAD_CONSULT | Architecture | Document rationale |
| Database schema (breaking) | HIGH_IMPACT | — | Board decides |
| Module boundary decisions | ORCHESTRATOR | — | Follow conventions |

### Dependencies

| Decision | Authority | Lead | Guardrails |
|----------|-----------|------|------------|
| Add runtime dependency >50KB gzipped | HIGH_IMPACT | — | Board decides |
| Remove any dependency | HIGH_IMPACT | — | Could break features |
| Major version upgrade | HIGH_IMPACT | — | Breaking changes risk |
| Add runtime dependency <50KB gzipped | LEAD_CONSULT | Tech | Document size & reasoning |
| Add devDependency (any size) | ORCHESTRATOR | — | No runtime impact |

### Quality & Testing

| Decision | Authority | Lead | Guardrails |
|----------|-----------|------|------------|
| Skip business logic tests | HIGH_IMPACT | — | Critical code must be tested |
| Coverage below minimum threshold | HIGH_IMPACT | — | Minimum threshold enforced |
| Skip security-related tests | HIGH_IMPACT | — | Security risk |
| Accept known failing tests | HIGH_IMPACT | — | Tech debt decision |
| Coverage threshold adjustments | LEAD_CONSULT | QA | Within acceptable range |
| Test type selection | LEAD_CONSULT | QA | Standard approaches |
| Mock strategy | LEAD_CONSULT | QA | Consistent patterns |
| Test file organization | ORCHESTRATOR | — | Follow existing pattern |

### Business & Pricing

| Decision | Authority | Lead | Guardrails |
|----------|-----------|------|------------|
| Pricing tier changes | HIGH_IMPACT | — | Revenue impact |
| Feature tier assignment | HIGH_IMPACT | — | Business model |
| Persona changes | HIGH_IMPACT | — | Product direction |
| User journey changes | HIGH_IMPACT | — | Product direction |

### Implementation Details

| Decision | Authority | Lead | Guardrails |
|----------|-----------|------|------------|
| Implementation approach | LEAD_CONSULT | Tech | Maintainable code |
| Type definitions | LEAD_CONSULT | Tech | Best practices |
| Hook composition | LEAD_CONSULT | Tech | Framework patterns |
| Error message copy | LEAD_CONSULT | Product | Clear, user-friendly |
| Loading state text | LEAD_CONSULT | Product | Clear, user-friendly |
| Variable naming | ORCHESTRATOR | — | Match codebase style |
| File naming | ORCHESTRATOR | — | Follow conventions |

---

## Lead Engineer Skills

| Lead | Skill Path | Primary Domain |
|------|------------|----------------|
| Architecture Lead | `skills/leads/architecture-lead/SKILL.md` | System design, patterns, ADRs |
| Product Lead | `skills/leads/product-lead/SKILL.md` | Scope, requirements, UX copy |
| Tech Lead | `skills/leads/tech-lead/SKILL.md` | Implementation, dependencies |
| QA Lead | `skills/leads/qa-lead/SKILL.md` | Testing, coverage, quality |

---

## Consultation Flow

```
Orchestrator encounters decision
        │
        ▼
┌───────────────────────────────┐
│ Look up decision in matrix    │
└───────────────┬───────────────┘
                │
    ┌───────────┼───────────┐
    │           │           │
    ▼           ▼           ▼
HIGH_IMPACT LEAD_CONSULT  ORCHESTRATOR
    │           │           │
    │           ▼           │
    │    ┌──────────────┐   │
    │    │ Dispatch to  │   │
    │    │ appropriate  │   │
    │    │ Lead agent   │   │
    │    └──────┬───────┘   │
    │           │           │
    │     ┌─────┴─────┐     │
    │     │           │     │
    │     ▼           ▼     │
    │  Decision    ESCALATE │
    │  Made          │      │
    │     │          │      │
    │     ▼          ▼      │
    │   Log to    Route to  │
    │  metadata    Board    │
    │     │          │      │
    │     ▼          ▼      │
    │  Continue   Board     │
    │   loop     Decides    │
    │     │          │      │
    ▼     │          ▼      ▼
┌───────────────────────────────┐
│ Board Decides Autonomously /  │
│ Lead Decides / Orchestrator   │
│ Decides — NEVER asks user     │
└───────────────────────────────┘
```

---

## Lead Response Format

### When Decision Made

```json
{
  "lead": "architecture | product | tech | qa",
  "decision_made": true,
  "decision": "The specific decision made",
  "reasoning": "Why this decision was made, citing precedent or guidelines",
  "authority_used": "CATEGORY from matrix",
  "precedent": "Reference to existing pattern if applicable",
  "escalate_to": null,
  "escalation_reason": null
}
```

### When Escalation Required

```json
{
  "lead": "architecture | product | tech | qa",
  "decision_made": false,
  "decision": null,
  "reasoning": "Why this is outside lead's authority",
  "authority_used": null,
  "escalate_to": "board | cto-advisor",
  "escalation_reason": "Specific reason for escalation with context"
}
```

---

## Logging Consultations

All lead consultations are logged to the track's `metadata.json`:

```json
{
  "lead_consultations": [
    {
      "timestamp": "2026-01-31T14:30:00Z",
      "lead": "tech",
      "question": "Which date formatting library should we use?",
      "decision_made": true,
      "decision": "Use date-fns (8KB gzipped)",
      "reasoning": "Under 50KB threshold, tree-shakeable",
      "authority_used": "DEPENDENCY_SMALL",
      "escalated_to": null
    },
    {
      "timestamp": "2026-01-31T15:00:00Z",
      "lead": "product",
      "question": "Should we add templates feature?",
      "decision_made": false,
      "decision": null,
      "reasoning": "Not in current spec",
      "authority_used": null,
      "escalated_to": "board",
      "escalation_reason": "Adding templates would be a scope expansion"
    }
  ]
}
```

---

## High-Impact Triggers (Board Resolution)

The orchestrator routes these to the Board of Directors for autonomous resolution (NEVER to the user):

1. **Fix cycle limit exceeded** — 5 failed EVALUATE → FIX cycles → Board decides: alternative approach or complete with warnings
2. **Blocker detected** — External dependency blocking → Board decides: skip, workaround, or log for review
3. **HIGH_IMPACT decision** — From this matrix → Board deliberates with all 5 directors
4. **Multiple leads disagree** — Cannot resolve precedence → Board acts as tiebreaker
5. **Security concern** — CSO (Chief Security Officer) on the Board evaluates risk and decides
6. **Production data impact** — Board assesses migration safety with all directors weighing in

---

## Quick Reference Card

### Board Decides Autonomously (High-Impact)
- Budget >$50/month → Board evaluates cost/benefit
- Add/remove features from spec → Board assesses scope impact
- Breaking API changes → Board reviews migration path
- Dependencies >50KB → Board evaluates alternatives
- Coverage below minimum threshold → Board decides acceptable threshold
- Security/production data → CSO leads Board review

### Lead Can Decide
- Architecture: Patterns (existing), component org, schema (additive)
- Product: Spec interpretation, copy, task order
- Tech: Dependencies <50KB, implementation, types
- QA: Coverage thresholds, test types, mocks

### Orchestrator Decides Autonomously
- File/variable naming
- devDependencies
- Task markers
- Following established conventions
