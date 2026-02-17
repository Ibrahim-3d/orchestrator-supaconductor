# Authority Matrix — Lead Engineer Consultation System

This document defines the decision authority levels for the Conductor orchestrator and its Lead Engineer consultation system.

## Authority Levels

| Level | Description | Decision Maker |
|-------|-------------|----------------|
| **USER_ONLY** | High-impact decisions requiring explicit user approval | User |
| **LEAD_CONSULT** | Decisions within lead's domain expertise and guardrails | Lead Engineer Agent |
| **ORCHESTRATOR** | Routine decisions following established conventions | Orchestrator (autonomous) |

## Decision Matrix

### Budget & Cost

| Decision | Authority | Lead | Guardrails |
|----------|-----------|------|------------|
| Cost increase >$50/month | USER_ONLY | — | Always escalate |
| New paid API integration | USER_ONLY | — | Always escalate |
| Cost increase <$50/month | LEAD_CONSULT | Tech | Document in decision log |
| Cost optimization (same features) | LEAD_CONSULT | Tech | Document savings |

### Scope & Features

| Decision | Authority | Lead | Guardrails |
|----------|-----------|------|------------|
| Add feature to spec | USER_ONLY | — | Always escalate |
| Remove feature from spec | USER_ONLY | — | Always escalate |
| Defer spec requirement to future track | USER_ONLY | — | Always escalate |
| Change deliverable definition | USER_ONLY | — | Always escalate |
| Interpret ambiguous spec | LEAD_CONSULT | Product | Must cite spec section |
| Task prioritization within phase | LEAD_CONSULT | Product | Same phase only |
| Edge case handling approach | LEAD_CONSULT | Product | Within spec intent |
| Default value selection | LEAD_CONSULT | Product | Reasonable defaults |

### Architecture & Patterns

| Decision | Authority | Lead | Guardrails |
|----------|-----------|------|------------|
| New architectural pattern (not in codebase) | USER_ONLY | — | Always escalate |
| Breaking change to public API | USER_ONLY | — | Always escalate |
| Cross-track architectural change | USER_ONLY | — | Always escalate |
| Apply existing codebase pattern | LEAD_CONSULT | Architecture | Document precedent |
| Component folder organization | LEAD_CONSULT | Architecture | Follow conventions |
| API route vs server action | LEAD_CONSULT | Architecture | Cite existing pattern |
| Data flow architecture | LEAD_CONSULT | Architecture | Match established patterns |
| Database schema (additive) | LEAD_CONSULT | Architecture | Document rationale |
| Database schema (breaking) | USER_ONLY | — | Always escalate |
| Module boundary decisions | ORCHESTRATOR | — | Follow conventions |

### Dependencies

| Decision | Authority | Lead | Guardrails |
|----------|-----------|------|------------|
| Add runtime dependency >50KB gzipped | USER_ONLY | — | Always escalate |
| Remove any dependency | USER_ONLY | — | Could break features |
| Major version upgrade | USER_ONLY | — | Breaking changes risk |
| Add runtime dependency <50KB gzipped | LEAD_CONSULT | Tech | Document size & reasoning |
| Add devDependency (any size) | ORCHESTRATOR | — | No runtime impact |

### Quality & Testing

| Decision | Authority | Lead | Guardrails |
|----------|-----------|------|------------|
| Skip business logic tests | USER_ONLY | — | Critical code must be tested |
| Coverage below minimum threshold | USER_ONLY | — | Minimum threshold enforced |
| Skip security-related tests | USER_ONLY | — | Security risk |
| Accept known failing tests | USER_ONLY | — | Tech debt decision |
| Coverage threshold adjustments | LEAD_CONSULT | QA | Within acceptable range |
| Test type selection | LEAD_CONSULT | QA | Standard approaches |
| Mock strategy | LEAD_CONSULT | QA | Consistent patterns |
| Test file organization | ORCHESTRATOR | — | Follow existing pattern |

### Business & Pricing

| Decision | Authority | Lead | Guardrails |
|----------|-----------|------|------------|
| Pricing tier changes | USER_ONLY | — | Revenue impact |
| Feature tier assignment | USER_ONLY | — | Business model |
| Persona changes | USER_ONLY | — | Product direction |
| User journey changes | USER_ONLY | — | Product direction |

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
USER_ONLY   LEAD_CONSULT  ORCHESTRATOR
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
    │     ▼          │      │
    │   Log to       │      │
    │  metadata      │      │
    │     │          │      │
    │     ▼          │      │
    │  Continue      │      │
    │   loop         │      │
    │     │          │      │
    ▼     │          ▼      ▼
┌───────────────────────────────┐
│ Escalate to User / Decide     │
│ Autonomously / Continue       │
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
  "escalate_to": "user | cto-advisor",
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
      "escalated_to": "user",
      "escalation_reason": "Adding templates would be a scope expansion"
    }
  ]
}
```

---

## Escalation Triggers

The orchestrator immediately escalates to user (no lead consultation) when:

1. **Fix cycle limit exceeded** — 3 failed EVALUATE → FIX cycles
2. **Blocker detected** — External dependency blocking progress
3. **Explicit USER_ONLY decision** — From this matrix
4. **Multiple leads disagree** — Cannot resolve precedence
5. **Security concern** — Any security-related change
6. **Production data impact** — Migrations affecting live data

---

## Quick Reference Card

### Always Escalate to User
- Budget >$50/month
- Add/remove features from spec
- Breaking API changes
- Dependencies >50KB
- Coverage below minimum threshold
- Security/production data

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
