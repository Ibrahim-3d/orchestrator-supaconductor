# Business Document Sync Strategy

Ensures all business strategy, pricing, and product documents stay synchronized when product decisions change during any track execution or evaluation.

## When to Use This Skill

- After ANY track completion that changes pricing, model strategy, or business decisions
- After ANY evaluation that produces product decisions or action items
- During `loop-executor` Step 3 when a task modifies business-impacting logic
- During `loop-execution-evaluator` Step 4 as part of the structural checks
- When creating new tracks that depend on business context (pricing, GTM, personas, model strategy)

## The Problem This Solves

Projects accumulate business strategy documents across multiple locations:
- Conductor root docs
- Strategy and planning tracks
- Agent skills
- JSON data files (pricing, config)
- Research tracks

When a product decision is made (e.g., adding a new pricing tier, changing the model strategy), these documents become stale unless explicitly synced. The next agent session reads outdated info and makes wrong decisions.

## Business Document Registry

### Tier 1: Source of Truth (MUST be updated first)

These are the canonical documents. When a decision changes, update these FIRST:

| Document | Location | Contains | Update When |
|----------|----------|----------|-------------|
| **product.md** | `conductor/product.md` | PRD, deliverables, pricing tiers, personas, user stories | Any product feature/pricing change |
| **business-strategy.md** | `conductor/business-strategy.md` | GTM, revenue projections, break-even, moat, risk register | Pricing, cost structure, or competitive position changes |
| **tech-stack.md** | `conductor/tech-stack.md` | Architecture, model strategy, API integrations, cost projections | Technology decisions, model changes, new integrations |
| **Data files** | `src/data/pricing.json` (or equivalent) | UI pricing tiers, features, comparison data | Any pricing change (tiers, features, price points) |

### Tier 2: Derived Documents (Update to match Tier 1)

These documents derive from Tier 1 and must stay consistent:

| Document | Location | Derives From | Update When |
|----------|----------|--------------|-------------|
| **product-roadmap.md** | `conductor/product-roadmap.md` | product.md, business-strategy.md | Roadmap phases, pricing evolution, or track structure changes |
| **product-guidelines.md** | `conductor/product-guidelines.md` | product.md | UI copy, paywall text, pricing display rules |
| **prompts.md** | `conductor/prompts.md` | product.md, tech-stack.md | Asset changes, model changes, prompt strategy |
| **screen-map.md** | `conductor/screen-map.md` | product.md | New screens, changed user flows |

### Tier 3: Skills (Update to match Tier 1 + Tier 2)

Agent skills must reflect current decisions so agents make correct choices:

| Skill | Location | Reflects | Update When |
|-------|----------|----------|-------------|
| **Product knowledge skill** | `.claude/skills/*/SKILL.md` | product.md, pricing model, personas | Product rules, pricing tiers, personas change |
| **Integration skills** | `.claude/skills/*/SKILL.md` | tech-stack.md, API docs | SDK patterns, model strategy, cost data, API changes |

### Tier 4: Strategy Archives (Reference only — do NOT update)

Historical research outputs capture decisions AT THE TIME they were made and should NOT be retroactively edited.

**Exception:** If a Tier 4 document is the ONLY place a specific decision is documented, add a "Superseded" note at the top pointing to the updated Tier 1 doc.

## Sync Trigger Events

### Automatic Triggers (Built into Evaluate-Loop)

| Event | What Triggers | Sync Action |
|-------|---------------|-------------|
| **Track Completion** | Any track marked COMPLETE | Run Business Doc Sync Checklist (Step 5.5) |
| **Evaluation Complete** | Any evaluation with product decisions | Run Business Doc Sync Checklist (Step 5.5) |
| **Pricing Change** | Price point, tier, or feature list changes | Update Tier 1-3 pricing sections |
| **Model Strategy Change** | AI model, SDK, or cost structure changes | Update tech-stack.md, skills, cost projections |
| **New Package/Tier Added** | New pricing tier or product bundle | Update ALL Tier 1-3 pricing sections |

### Manual Triggers

| Trigger | When |
|---------|------|
| `/conductor sync-docs` | User explicitly requests doc sync |
| Discovered during planning | Agent notices stale data while reading docs |

## Business Doc Sync Checklist

Run this checklist whenever a sync trigger fires. Check each item and update if stale:

```markdown
## Business Doc Sync Checklist

**Trigger:** [Describe what changed — e.g., "Added new pricing tier"]
**Date:** [YYYY-MM-DD]

### Tier 1: Source of Truth
- [ ] `conductor/product.md` — Pricing section reflects current tiers and features
- [ ] `conductor/business-strategy.md` — Revenue projections use current pricing; cost analysis uses current model costs
- [ ] `conductor/tech-stack.md` — Model strategy, SDK references, and cost projections are current
- [ ] Data files — UI pricing data matches product.md tiers

### Tier 2: Derived Documents
- [ ] `conductor/product-roadmap.md` — Phase pricing and track descriptions are current
- [ ] `conductor/product-guidelines.md` — Paywall copy, pricing display rules match current tiers
- [ ] `conductor/prompts.md` — Prompt strategy aligns with current model capabilities
- [ ] `conductor/screen-map.md` — Screen list includes any new tier-related screens

### Tier 3: Skills
- [ ] Product knowledge skill — Pricing model, tech stack table, personas current
- [ ] Integration skills — SDK patterns, model names, cost data current

### Verification
- [ ] No document references a price point that doesn't match `product.md`
- [ ] No document references a model name that doesn't match `tech-stack.md`
- [ ] No skill references an SDK pattern that doesn't match the actual codebase
- [ ] Data file tier count and features match `product.md` tier count and features
```

## Sync Execution Protocol

### Step 1: Identify What Changed
Read the trigger source (evaluation report, track completion, user instruction) and extract:
- **Decision**: What was decided?
- **Impact**: Which documents does this affect?
- **Scope**: Tier 1 only? Tier 1-2? Tier 1-3?

### Step 2: Update Tier 1 First
Always update the source of truth documents first. This prevents cascading inconsistencies.

### Step 3: Cascade to Tier 2
Update derived documents to match the new Tier 1 state.

### Step 4: Update Tier 3 Skills
Update agent skills so future sessions use correct data.

### Step 5: Verify Consistency
Run the sync checklist above and confirm all items pass.

### Step 6: Commit
```
docs: sync business docs — [brief description of what changed]
```

## Decision Changelog

Track all product decisions that trigger syncs. This lives in `conductor/decision-log.md`:

```markdown
| Date | Decision | Source | Documents Updated | Commit |
|------|----------|--------|-------------------|--------|
| 2026-01-28 | Added premium pricing tier | Track evaluation | product.md, tech-stack.md, business-strategy.md, pricing data, skills | abc1234 |
```

## Integration with Evaluate-Loop

This skill integrates into the existing Evaluate-Loop as **Step 5.5: Business Doc Sync**:

```
PLAN → EVALUATE PLAN → EXECUTE → EVALUATE EXECUTION
                                       │
                                  PASS → 5.5 BUSINESS DOC SYNC → COMPLETE
                                  FAIL → FIX → re-EXECUTE → re-EVALUATE
```

**Step 5.5** runs AFTER evaluation passes but BEFORE marking the track complete. It ensures that any product decisions made during the track are propagated to all documents before the next track begins.

The `loop-execution-evaluator` checks for business doc staleness as part of its structural checks. If business-impacting changes were made but docs weren't synced, evaluation returns FAIL with a "Business docs out of sync" finding.

## Related Documentation

- `conductor/workflow.md` — Evaluate-Loop process (Step 5.5 integration)
- `conductor/decision-log.md` — Chronological decision history
- `conductor/product.md` — Tier 1 source of truth (product)
- `conductor/business-strategy.md` — Tier 1 source of truth (business)
- `conductor/tech-stack.md` — Tier 1 source of truth (technology)
