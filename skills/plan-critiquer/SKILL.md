---
name: plan-critiquer
description: Harshly critique strategic documents (validation reports, competitive analyses, business plans) to identify blind spots, challenge assumptions, expose weaknesses, and generate Conductor-aligned action plans. Use when you need brutal honesty, "red team" analysis, or want to stress-test your thinking before execution. Applies multiple analytical frameworks (pre-mortem, assumption hunting, competitive gaps, market dynamics) and synthesizes findings into executive summaries with specific, actionable recommendations mapped to Conductor context artifacts.
---

# Plan Critiquer - Strategic Red Team Analysis

This skill provides **harsh, unfiltered critique** of strategic documents to expose blind spots, challenge assumptions, and strengthen your plans before execution. Think of this as your personal "devil's advocate" that will **brutally honest** about weaknesses, risks, and gaps in your thinking.

## Core Philosophy

**Be merciless, not merciful.** The goal is to find every possible flaw, weakness, and blind spot **before** you invest time and money. A harsh critique now saves catastrophic failure later.

**Key Principles:**
1. **Assume failure first** - Start from "this will fail" and work backward
2. **Challenge everything** - No assumption is sacred
3. **Seek disconfirming evidence** - Look for what contradicts the plan
4. **Think like competitors** - How would they exploit your weaknesses?
5. **Be specific** - Vague concerns are useless; actionable insights are gold

## When to Use This Skill

- After completing market validation or competitive analysis
- Before committing significant resources to a plan
- When you need to stress-test strategic assumptions
- Before presenting to investors, stakeholders, or team
- When you feel "too confident" about a plan (overconfidence bias check)
- After receiving positive feedback (to balance optimism with realism)

## Workflow

### Step 1: Identify and Read Input Documents

The user will provide one or more strategic documents to critique. Common types:
- Validation reports
- Competitive analyses
- Business plans
- Market research summaries
- Product roadmaps
- Go-to-market strategies

Read all provided documents completely to understand the full context.

### Step 2: Load Critique Framework

Read `references/critique_framework.md` - this contains the multi-pass analytical framework with specific questions and techniques for identifying blind spots.

### Step 3: Apply Critique Framework (Multi-Pass Analysis)

Systematically apply **all passes** from the framework:

**Pass 1: Gut Check**
- Does the narrative make sense?
- Are there obvious holes or inconsistencies?
- Does it inspire confidence or raise red flags?

**Pass 2: Assumption Hunting**
- Identify the 5-10 most critical assumptions
- Challenge each: "What if this is wrong?"
- Assess evidence strength for each assumption
- Identify assumptions that are unverified or weakly supported

**Pass 3: Pre-Mortem (Imagine Failure)**
- Assume the project failed spectacularly in 6 months
- Brainstorm all possible failure reasons (internal + external)
- Categorize and prioritize failure modes
- Identify which failures are preventable vs. uncontrollable

**Pass 4: Competitive & Market Blind Spots**
- Unaddressed competitors (direct, indirect, emerging)
- Customer perspective gaps (are we solving their problem?)
- Market dynamics not considered (regulatory, technological, social trends)
- Differentiation weaknesses (how easy to copy? how defensible?)

**Pass 5: Synthesis**
- Consolidate findings across all passes
- Identify patterns and themes
- Prioritize by impact and likelihood
- Generate specific, actionable recommendations

### Step 4: Generate Critique Report

Create a comprehensive critique report with the following structure:

#### Executive Summary (2-4 paragraphs)
- **Overall Assessment:** GO / GO WITH CAUTION / STOP (with brief rationale)
- **Critical Risks:** Top 3 deal-breaker risks that could kill the project
- **Key Blind Spots:** Top 3 areas where thinking is incomplete or flawed
- **Recommended Actions:** High-level next steps to address findings

#### Detailed Critique & Blind Spots

Organize findings by category:

**Strategic Concerns**
- Vision/positioning weaknesses
- Market opportunity gaps
- Competitive positioning flaws
- Business model vulnerabilities

**Assumption Gaps**
- Unverified assumptions with high impact
- Weak evidence for critical beliefs
- Optimistic projections without validation
- Hidden dependencies

**Competitive/Market Oversights**
- Unaddressed competitors or substitutes
- Market dynamics not considered
- Customer objections not addressed
- Differentiation weaknesses

**Execution Risks**
- Resource constraints
- Timeline unrealism
- Capability gaps
- Dependency risks

For each finding:
- **State the concern clearly**
- **Explain the impact** (what happens if this is wrong?)
- **Assess likelihood** (how probable is this risk?)
- **Provide evidence** (what makes you think this?)

### Step 5: Create Conductor-Aligned Action Plan

Generate a **prioritized, specific action plan** that maps recommendations to Conductor context artifacts.

For each action item:
1. **Priority:** HIGH / MEDIUM / LOW
2. **Action:** Specific, measurable task (not vague like "research more")
3. **Rationale:** Why this matters (link to critique finding)
4. **Conductor Artifact:** Which file(s) to update (`product.md`, `tech-stack.md`, `workflow.md`, etc.)
5. **Success Criteria:** How to know when this is complete
6. **Timeline:** Suggested timeframe (days/weeks)

**Conductor Artifact Mapping Guidelines:**

- **`product.md`** - Update for: vision changes, feature prioritization, target user refinements, success metrics
- **`product-guidelines.md`** - Update for: messaging, positioning, brand voice, terminology
- **`tech-stack.md`** - Update for: technology choices, dependencies, infrastructure, scalability concerns
- **`workflow.md`** - Update for: development practices, quality gates, validation processes, risk mitigation steps
- **`tracks.md`** - Create new tracks for: validation experiments, research tasks, prototypes, risk mitigation projects
- **New track (spec.md + plan.md)** - For substantial work requiring phased execution

### Step 6: Write Output File

Save the critique report as a markdown file in the project root with a descriptive name:
- `[ProjectName]_Critique_Report_[Date].md`

### Step 7: Inform User

Provide a brief summary of:
- Overall assessment (GO / GO WITH CAUTION / STOP)
- Number of critical risks identified
- Number of action items generated
- Location of full report
- Recommended immediate next steps (top 1-3 actions)

## Critique Quality Standards

A good critique is:

- **Specific** - "API costs could exceed revenue at scale" not "costs might be high"
- **Evidence-based** - References data, comparisons, or logical reasoning
- **Actionable** - Leads to clear next steps, not just complaints
- **Prioritized** - Distinguishes critical from nice-to-have
- **Balanced** - Acknowledges strengths while focusing on weaknesses
- **Harsh but constructive** - Brutal honesty with path to improvement

A bad critique is:

- **Vague** - "This might not work"
- **Unsupported** - Opinions without reasoning
- **Unconstructive** - Problems without solutions
- **Unfocused** - Everything is equally important
- **Overly positive** - Ignores real risks to be nice
- **Destructive** - Tears down without building up

## Advanced Techniques

### Devil's Advocate Prompts

When analyzing, actively ask:
- "What would a skeptical investor say?"
- "How would my toughest competitor attack this?"
- "What would make me abandon this in 6 months?"
- "What am I not seeing because I want this to succeed?"
- "What would a domain expert immediately spot as naive?"

### Second-Order Thinking

Don't just identify risks - think through consequences:
- "If X happens, then Y, which causes Z..."
- "This mitigation creates a new risk of..."
- "Solving this problem might make that problem worse..."

### Competitive Response Modeling

For each competitive advantage claimed:
- "How would the top competitor respond if we succeed?"
- "What prevents them from copying this in 3 months?"
- "Do they have resources/brand to crush us even if we're better?"

### Customer Psychology

Challenge solution-fit from user perspective:
- "Would I actually pay for this?"
- "What friction would stop me from buying?"
- "What objections would I have?"
- "What alternatives would I consider first?"

## Integration with Conductor Workflow & Evaluate-Loop

This skill supports the Conductor methodology at two levels:

### Strategic Level (Context → Spec transition)
1. **Context Phase:** Establish project context
2. **Validation Phase:** Conduct market research, competitive analysis
3. **CRITIQUE PHASE (This Skill):** Red team the validation findings
4. **Context Update Phase:** Refine context artifacts based on critique
5. **Spec Phase:** Define requirements for validated work

### Execution Level (Evaluate-Loop support)
The `loop-plan-evaluator` agent uses this skill's critique framework for deep plan analysis when a plan needs strategic scrutiny beyond standard scope/overlap checks.

**Loop Agent Integration:**
- `loop-plan-evaluator` → may invoke plan-critiquer for strategic-level plan review
- `loop-execution-evaluator` → may invoke plan-critiquer for post-mortem analysis

**The critique acts as a quality gate** - don't proceed to spec/plan until critical blind spots are addressed.

## Output Template

The skill uses `assets/critique_template.md` as the base structure. Customize sections as needed for the specific documents being critiqued, but maintain the core structure:

1. Executive Summary
2. Detailed Critique & Blind Spots (by category)
3. Action Plan (prioritized, Conductor-mapped)
4. Appendix (supporting analysis, data, references)

## Tips for Maximum Value

1. **Provide context:** Share related documents (product.md, previous plans) so critique can spot inconsistencies
2. **Be open to harsh feedback:** The more brutal, the more valuable
3. **Act on findings:** A critique without action is wasted effort
4. **Iterate:** Critique → Update → Critique again for high-stakes decisions
5. **Time-box:** Don't let perfect critique delay necessary action - set a deadline
