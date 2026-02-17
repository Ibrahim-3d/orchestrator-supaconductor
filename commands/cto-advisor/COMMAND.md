# /cto-advisor

Run CTO-level technical review of the current execution plan. Uses the `cto-advisor` skill to evaluate architecture decisions, tech debt implications, technology choices, and engineering excellence.

## When to Use

Run this command to get technical leadership guidance on:
- **Architecture decisions** — evaluating system design patterns, component boundaries
- **Technology selection** — choosing libraries, frameworks, services
- **Technical debt** — assessing debt introduction and mitigation strategies
- **Engineering metrics** — validating against DORA metrics and quality standards
- **Integration planning** — reviewing API design, vendor dependencies
- **Infrastructure changes** — evaluating scalability, performance, monitoring
- **Security review** — checking authentication, authorization, OWASP compliance

## Usage

```bash
# Review current track's plan
/cto-advisor

# Or manually specify track
/cto-advisor TRACK-001-core-feature
```

## What It Does

The command invokes the `cto-plan-reviewer` skill, which:

1. **Loads Context**
   - Reads track's `plan.md` and `spec.md`
   - Loads `conductor/tech-stack.md` for current technology decisions
   - Loads `conductor/product.md` for product constraints
   - Scans codebase for existing architecture patterns

2. **Applies CTO Advisor Frameworks**
   - **Architecture Review** — ADR templates, system design criteria, technology standards
   - **Tech Debt Assessment** — Debt analyzer, 40/25/15 allocation strategy, red flags
   - **Technology Evaluation** — 4-week evaluation framework, vendor management, cost analysis
   - **Engineering Excellence** — DORA metrics (deployment frequency, lead time, MTTR, CFR), quality metrics (test coverage >80%)
   - **Team & Process** — Execution feasibility, knowledge distribution, documentation needs

3. **Generates Technical Review Report**
   - Architecture assessment with specific recommendations
   - Tech debt analysis with severity and mitigation plan
   - Technology evaluation with alternatives and lock-in risk
   - Engineering excellence checklist (testing, performance, security, observability)
   - Team & process fit analysis
   - Red flags from CTO advisor checklist
   - DORA metrics impact assessment
   - Actionable recommendations (must-fix, should-consider, nice-to-have)
   - Final verdict: PASS / PASS WITH CONDITIONS / FAIL

## Output Format

```markdown
## CTO Technical Review Report

**Track**: TRACK-001-core-feature
**Reviewer**: cto-plan-reviewer (using cto-advisor frameworks)
**Date**: YYYY-MM-DD

### Architecture Assessment

#### Design Decisions
- [x] Architecture pattern: Zustand store with React hooks — appropriate for client-side state
- [ ] CONCERN: No error boundary strategy for API failures
- Recommendation: Add React Error Boundaries around critical components

#### System Design
- [x] Component boundaries clear and well-defined
- [x] Separation of concerns maintained (state/UI/API separated)
- [ ] CONCERN: Tight coupling between generation and state management
- Recommendation: Extract state to separate store slice for independent evolution

### Tech Debt Analysis

#### Debt Introduction: LOW
- Debt items introduced:
  1. Mock client for development — Severity: Low — Justification: Needed for parallel frontend work
  2. Hardcoded templates — Severity: Medium — Justification: Will be moved to database in Phase 2

#### Mitigation Plan
- [x] Debt paydown plan documented in plan.md Phase 2
- [x] Capacity allocated: 15% in maintenance sprints — Aligns with cto-advisor 40/25/15 strategy

### Technology Evaluation

#### New Dependencies
| Library/Service | Necessity | Alternatives Considered | Lock-in Risk | Cost Impact |
|----------------|-----------|------------------------|--------------|-------------|
| API Service | High | Alternative A, Alternative B | Medium | $X/request |
| Utility Lib | High | alt-lib-1, alt-lib-2 | Low | None (open source) |
| State Manager | Medium | Redux, Jotai, Context API | Low | None (easy to migrate) |

#### Integration Assessment
- API design: Well-structured with proper error types
- Error handling: Good — includes retry logic and user-friendly messages
- Retry logic: Present with exponential backoff
- Cost monitoring: Missing — Add API usage tracking before production

### Engineering Excellence

#### Testing Strategy: ADEQUATE
- Coverage targets: 70% overall, 90% business logic — Meets cto-advisor 80% threshold for critical paths
- TDD applicability: High for core logic
- Test types planned: Unit (core logic), Integration (store), E2E (full flow)
- Recommendation: Add E2E test for complete end-to-end flow

#### Performance Criteria: DEFINED
- Load requirements: Defined per use case
- Optimization strategy: Lazy loading, caching where appropriate

#### Security Review: PASS
- OWASP top 10 considered: Yes
- Input validation: In place
- Auth patterns: Appropriate for current phase

#### Observability: BASIC
- Monitoring: Missing — Add analytics
- Logging: Present — Console logs for key steps
- Alerting: Not applicable for Phase 1
- Recommendation: Add structured logging for production debugging

### Team & Process

#### Execution Feasibility: HIGH
- Team capability match: Good
- Knowledge distribution: Acceptable, documentation present
- Onboarding impact: Low — clear component structure and naming

#### Documentation Plan: ADEQUATE
- Technical docs needed: Key integration guides
- ADR required: No (decisions documented in architecture doc)
- Onboarding docs: Present in project docs

### Red Flags

**X red flag(s) found:**
- [List any red flags with actions]

### DORA Metrics Impact Assessment

| Metric | Current Target | Impact of Plan | Assessment |
|--------|---------------|----------------|------------|
| Deployment Frequency | >1/day | Positive | Trunk-based dev enables continuous deployment |
| Lead Time | <1 day | Neutral | Feature complexity appropriate for daily deployment |
| MTTR | <1 hour | Positive | Error boundaries and fallbacks reduce recovery time |
| Change Failure Rate | <15% | Positive | TDD on critical paths reduces defects |

### Recommendations

#### Must Fix (Blocking Issues)
1. [List blocking issues]

#### Should Consider (Improvements)
1. [List improvements]

#### Nice to Have (Enhancements)
1. [List enhancements]

### Verdict

**Technical Review**: PASS | PASS WITH CONDITIONS | FAIL

**Rationale**: [Assessment summary]

---

**Next Steps**:
1. Executor should address "Must Fix" items during implementation
2. Track these conditions in plan.md under "Technical Review Conditions"
3. Verify conditions met during Step 4 (Evaluate Execution)
```

## Integration with Conductor

This command is automatically invoked by the conductor during plan evaluation for technical tracks:

```
/conductor implement
  → detects technical track (keywords: architecture, API, database, etc.)
  → dispatches loop-plan-evaluator
    → invokes /cto-advisor automatically
  → aggregates standard checks + CTO review
  → PASS/FAIL verdict
```

You can also run it manually at any time to get CTO-level guidance on the current plan.

## When CTO Review is Automatic

The conductor automatically includes CTO review when the track's `spec.md` or `plan.md` contains these keywords:

**Technical Keywords:**
- architecture, system design, integration, API, database, schema, migration
- infrastructure, scalability, performance, security
- authentication, authorization, deployment, monitoring, logging
- vendor, technology selection, framework, library

**If unsure whether your track needs CTO review**, run it manually. It's better to over-review than under-review critical technical decisions.

## Manual vs Automatic

### Automatic (Recommended)
```bash
/conductor implement
# CTO review runs automatically for technical tracks during plan evaluation
```

### Manual (When Needed)
```bash
# Get CTO review anytime
/cto-advisor

# Review specific track
/cto-advisor TRACK-002-integration

# Get architecture guidance before planning
/cto-advisor
```

## CTO Advisor Frameworks Used

The command leverages these frameworks from the `cto-advisor` skill:

### 1. Architecture Decision Records (ADRs)
- Template for documenting technical decisions
- Context, options, decision, consequences format
- Ensures decisions are traceable and justified

### 2. Technology Evaluation Framework
- 4-week evaluation process (requirements → research → evaluation → decision)
- Vendor assessment criteria (SLA, cost, lock-in risk)
- Alternatives comparison matrix

### 3. Tech Debt Strategy
- 40/25/15 capacity allocation (Critical/High/Medium debt)
- Red flags checklist (increasing debt, vendor lock-in, security vulnerabilities)
- Mitigation planning requirements

### 4. DORA Metrics
- Deployment Frequency target: >1/day
- Lead Time for Changes: <1 day
- Mean Time to Recovery: <1 hour
- Change Failure Rate: <15%

### 5. Engineering Metrics
- Test Coverage: >80% (70% overall, 90% business logic)
- Code Review: 100% of changes
- Technical Debt: <10% of capacity

### 6. System Design Review Criteria
- Component boundaries and separation of concerns
- Scalability and performance characteristics
- Error handling and resilience patterns
- Observability and debugging support

## Example: Before/After CTO Review

### Before CTO Review
```markdown
# Plan (incomplete technical thinking)

## Phase 1: Add Stripe Integration
- [ ] Install Stripe SDK
- [ ] Create checkout page
- [ ] Add webhook handler
- [ ] Update database with payment status
```

### After CTO Review
```markdown
# Plan (enhanced with CTO guidance)

## Phase 1: Add Stripe Integration

### Technical Review Conditions
- [!] Add webhook signature verification (Security — prevents unauthorized payments)
- [!] Add idempotency keys (Reliability — prevents duplicate charges)
- [!] Add webhook retry logic with exponential backoff (Resilience — handles temporary failures)
- [!] Add Stripe event logging for audit trail (Observability — debugging and compliance)
- [!] Document webhook failure recovery process in runbook (Operations — incident response)

## Tasks
- [ ] Install Stripe SDK (v11.x — latest stable)
- [ ] Create checkout page
  - Acceptance: Stripe Checkout redirects to success/cancel URLs
  - Security: No card details stored client-side
- [ ] Add webhook handler at /api/webhooks/stripe
  - Acceptance: Verifies signature, handles checkout.session.completed
  - Resilience: Idempotent (can handle duplicate events)
  - Observability: Logs all events to structured logger
- [ ] Update database with payment status
  - Acceptance: Transaction recorded, user tier updated
  - Consistency: Atomic transaction (payment + tier update)
- [ ] Add webhook failure recovery cron job
  - Acceptance: Polls Stripe for missed events every 1 hour
  - Resilience: Handles extended webhook downtime
```

**Key Improvements from CTO Review:**
1. Security hardening (webhook verification, no client-side card storage)
2. Resilience patterns (idempotency, retry logic, recovery cron)
3. Observability (structured logging, audit trail)
4. Operational readiness (failure recovery documented)
5. Specific version and acceptance criteria

## Related

- `.claude/skills/cto-plan-reviewer/SKILL.md` — Full CTO review agent documentation
- `.claude/skills/cto-advisor/SKILL.md` — Core CTO advisor frameworks and tools
- `/conductor implement` — Automated loop that includes CTO review
- `conductor/workflow.md` — Evaluate-Loop process
