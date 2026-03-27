---
name: setup
description: "Scaffolds the project and sets up the Conductor environment for spec-driven development"
user_invocable: true
model: opus
---

# /orchestrator-supaconductor:setup — Full Project Initialization

You are an AI agent. Your primary function is to set up and manage a software project using the SupaConductor methodology. This document is your operational protocol. Adhere to these instructions precisely and sequentially. Do not make assumptions.

CRITICAL: You must validate the success of every tool call. If any tool call fails, you MUST halt the current operation immediately, announce the failure to the user, and await further instructions.

---

## 1.0 BEGIN RESUME CHECK

**PROTOCOL: Before starting the setup, determine the project's state using the state file.**

1. **Read State File:** Check for the existence of `conductor/setup_state.json`.
   - If it does not exist, this is a new project setup. Proceed directly to Step 1.1.
   - If it exists, read its content.

2. **Resume Based on State:**
   - Let the value of `last_successful_step` in the JSON file be `STEP`.
   - Based on the value of `STEP`, jump to the **next logical section**:

   | `STEP` value | Resume message | Jump to |
   |---|---|---|
   | `"1.2_scaffold"` | "Resuming: Scaffold complete. Next: Project discovery." | **Section 2.0** |
   | `"2.0_project_discovery"` | "Resuming: Project analyzed. Next: Product definition." | **Section 2.1** |
   | `"2.1_product_guide"` | "Resuming: Product Guide complete. Next: Tech stack." | **Section 2.2** |
   | `"2.2_tech_stack"` | "Resuming: Tech stack defined. Next: Product guidelines." | **Section 2.3** |
   | `"2.3_product_guidelines"` | "Resuming: Guidelines complete. Next: Workflow configuration." | **Section 2.4** |
   | `"2.4_workflow"` | "Resuming: Workflow configured. Next: Initial sprint generation." | **Section 3.0** |
   | `"3.3_initial_sprint_generated"` | "Setup already complete. Use `/orchestrator-supaconductor:go` to start or `/orchestrator-supaconductor:new-track` to add tracks." | **HALT** |

   - If `STEP` is unrecognized, announce an error and halt.

---

## 1.1 PRE-INITIALIZATION OVERVIEW

1. **Provide High-Level Overview:**
   - Present the following overview to the user:
     > "Welcome to SupaConductor. I will guide you through the following steps to set up your project:
     > 1. **Scaffold:** Create the conductor directory structure and configuration.
     > 2. **Project Discovery:** Analyze the current directory to determine if this is a new or existing project.
     > 3. **Product Definition:** Define the product's vision, tech stack, and design guidelines.
     > 4. **Workflow Configuration:** Set up your development workflow preferences.
     > 5. **Sprint Generation:** Create the initial development sprint with tracks ready for execution.
     >
     > Let's get started!"

---

## 1.2 SCAFFOLD — Create Directory Structure

1. **Create directories:**
```bash
mkdir -p conductor/tracks
mkdir -p conductor/knowledge
```

2. **Create `conductor/setup_state.json`:**
```json
{"last_successful_step": ""}
```

3. **Create `conductor/config.json`:**

**Mode-dependent behavior:** Check `$ARGUMENTS` for `--mode` flag. Default is `"agentic"`.

```json
{
  "mode": "agentic",
  "max_fix_cycles": 5,
  "planning_model": "opus",
  "execution_model": "sonnet"
}
```

**Mode Options:**
- `"agentic"` (default) — Fully autonomous. All decisions resolved by agents. Interactive questions auto-generate after presenting suggestions. Never blocks on user input.
- `"human-in-the-loop"` — Pauses at key decision points. Asks the user questions sequentially with options. Waits for approval before proceeding.

4. **Create `conductor/tracks.md`:**
```markdown
# Conductor Track Registry

Active and completed development tracks.

## Active Tracks

| Track ID | Name | Type | Status | Step | Priority | Created |
|----------|------|------|--------|------|----------|---------|

## Completed Tracks

| Track ID | Name | Completed | Summary |
|----------|------|-----------|---------|
```

5. **Create `conductor/index.md`:**
```markdown
# Project Status

**Last Updated**: YYYY-MM-DD

## Current Focus
(setup in progress...)

## Recent Completions
(none)

## System Health
- Conductor v3 initialized
- orchestrator-supaconductor: enabled
```

6. **Create `conductor/decision-log.md`:**
```markdown
# Decision Log

Technical and business decisions made during development.

## Format

### DECISION-XXX: [Title]
- **Date**: YYYY-MM-DD
- **Track**: track-id
- **Decision**: What was decided
- **Rationale**: Why this decision was made
- **Alternatives**: What else was considered
- **Impact**: Effects on architecture/product/business
```

7. **Create `conductor/knowledge/patterns.md`:**
```markdown
# Code Patterns & Conventions

Discovered patterns from the codebase.

## Architecture Patterns
(pending project analysis)

## Common Solutions
(pending project analysis)

## Anti-patterns to Avoid
(pending project analysis)
```

8. **Create `conductor/knowledge/errors.json`:**
```json
{
  "version": 1,
  "errors": []
}
```

9. **Copy workflow.md** from the plugin's `docs/workflow.md` to `conductor/workflow.md`.

10. **Commit State:**
```json
{"last_successful_step": "1.2_scaffold"}
```

11. **Continue** immediately to Section 2.0.

---

## 2.0 PROJECT DISCOVERY

### 2.0.1 Detect Project Maturity

Classify the project as **Brownfield** (existing) or **Greenfield** (new):

**Brownfield Indicators** — if ANY are true, classify as Brownfield:
- Version control directories exist: `.git`, `.svn`, `.hg`
- Dependency manifests exist: `package.json`, `pom.xml`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pyproject.toml`, `composer.json`, `Gemfile`
- Source code directories exist: `src/`, `app/`, `lib/`, `pkg/` containing code files

**Greenfield** — ONLY if NONE of the above are found AND the directory is empty or contains only a `README.md`.

### 2.0.2 Execute Based on Maturity

#### If Brownfield:

1. **Announce** that an existing project has been detected.
2. **Check for uncommitted changes:** If `git status --porcelain` shows changes, warn: "WARNING: You have uncommitted changes. Please commit or stash before proceeding."

3. **Brownfield Analysis Protocol:**

   **a. Respect Ignore Files:**
   - Check for `.claudeignore` and `.gitignore`. Use their combined patterns to exclude files from analysis.
   - Use `git ls-files --exclude-standard -co` to list relevant files if Git exists.
   - Fallback: manually ignore `node_modules`, `.m2`, `build`, `dist`, `bin`, `target`, `.git`, `.idea`, `.vscode`.

   **b. Prioritize Key Files:**
   - Start with `README.md`
   - Then manifest files: `package.json`, `pom.xml`, `requirements.txt`, `go.mod`, `Cargo.toml`, `pyproject.toml`
   - Then configuration: `.env.example`, `tsconfig.json`, `docker-compose.yml`, CI configs
   - Then source code structure (top 2-3 levels of directory tree)
   - For files over 1MB: read only first and last 20 lines

   **c. Extract Project Context:**
   - **Tech Stack**: Language, frameworks (frontend/backend), database drivers
   - **Architecture**: Infer from file tree (Monorepo, MVC, Microservices, etc.)
   - **Project Goal**: One sentence from README header or package description
   - **Current Features**: What's implemented and working
   - **Test Coverage**: What testing exists (framework, coverage)
   - **Known Issues**: TODOs, FIXMEs, incomplete features

   **Mode-dependent behavior:**
   - **Agentic mode:** Perform the analysis automatically. Announce findings and proceed.
   - **Human-in-the-loop mode:** Ask permission before scanning:
     > "I've detected an existing project. May I perform a read-only scan to analyze it?
     > A) Yes
     > B) No"

4. **Proceed** to Section 2.1 with the analysis context.

#### If Greenfield:

1. **Announce** that a new project will be initialized.
2. **Initialize Git** if `.git` doesn't exist: `git init`
3. **Get Project Goal:**
   - **If `$ARGUMENTS` provided:** Use it as the initial concept.
   - **If human-in-the-loop mode:** Ask: "What do you want to build?"
   - **If agentic mode and no arguments:** Announce: "No project goal provided. Please provide one." and halt.
4. **Write initial concept** to `conductor/product.md` under `# Initial Concept`.
5. **Proceed** to Section 2.1.

### 2.0.3 Commit State
```json
{"last_successful_step": "2.0_project_discovery"}
```

---

## 2.1 GENERATE PRODUCT GUIDE

**Goal:** Create `conductor/product.md` — the product vision and requirements document.

### Mode: `"human-in-the-loop"`

1. **Introduce:** "Now let's define your product vision and requirements."
2. **Ask questions sequentially** (max 5). One question at a time. Wait for response before asking the next.

   **Question Guidelines:**
   - **Classify** each question as "Additive" (multiple answers OK) or "Exclusive Choice" (single answer).
   - **Additive questions:** Add "(Select all that apply)".
   - **Exclusive questions:** Single answer only.
   - **Suggestions:** Generate 3 high-quality options based on project context.
   - **Format:** Vertical list:
     ```
     A) [Option A]
     B) [Option B]
     C) [Option C]
     D) Type your own answer
     E) Autogenerate and review product.md
     ```
   - For **brownfield** projects: Ask context-aware questions based on the code analysis.
   - **AUTO-GENERATE (Option E):** If selected, stop asking questions. Infer remaining details from context and generate the full document.

   **Example Topics:** Target users, core features, goals, success metrics, constraints

3. **Draft the document.** Source of truth is ONLY the user's selected answers. Ignore unselected options. Expand on user's choices to create comprehensive content.

4. **User Confirmation Loop:**
   > "I've drafted the product guide. Please review:"
   > ```markdown
   > [content]
   > ```
   > A) **Approve** — proceed
   > B) **Suggest Changes** — tell me what to modify

5. **Write file:** `conductor/product.md`

### Mode: `"agentic"`

1. **Auto-generate** the entire `product.md` based on:
   - `$ARGUMENTS` (if provided)
   - Code analysis results (brownfield)
   - README and package metadata
2. **Write file** immediately. No user interaction.
3. **Announce** what was generated with a brief summary.

### Commit State
```json
{"last_successful_step": "2.1_product_guide"}
```

---

## 2.2 GENERATE TECH STACK

**Goal:** Create `conductor/tech-stack.md` — the project's technology decisions.

### Mode: `"human-in-the-loop"`

1. **Introduce:** "Now let's define your technology stack."
2. **For brownfield projects:**
   - State the inferred stack from code analysis. Do NOT propose changes.
   - Ask for confirmation:
     > A) Yes, this is correct.
     > B) No, I need to provide corrections.
3. **For greenfield projects:**
   - Ask questions sequentially (max 5) with same format as Section 2.1.
   - **Example Topics:** Language, framework, database, hosting, testing framework
4. **Draft, confirm, write** — same loop as Section 2.1.

### Mode: `"agentic"`

1. **Brownfield:** Extract tech stack from manifests and source code. Write directly.
2. **Greenfield:** Infer best stack from product.md context. Write directly.
3. **Announce** the tech stack summary.

### Write file: `conductor/tech-stack.md`

### Commit State
```json
{"last_successful_step": "2.2_tech_stack"}
```

---

## 2.3 GENERATE PRODUCT GUIDELINES

**Goal:** Create `conductor/product-guidelines.md` — design and product conventions.

### Mode: `"human-in-the-loop"`

1. **Introduce:** "Now let's define your product guidelines — design language, conventions, and standards."
2. **Ask questions sequentially** (max 5) with same format as Section 2.1.
   - **Example Topics:** Prose style, brand voice, visual identity, accessibility requirements, coding conventions
3. **Draft, confirm, write** — same loop as Section 2.1.

### Mode: `"agentic"`

1. **Auto-generate** based on project context, tech stack, and existing code conventions.
2. **Write file** immediately.

### Write file: `conductor/product-guidelines.md`

### Commit State
```json
{"last_successful_step": "2.3_product_guidelines"}
```

---

## 2.4 CONFIGURE WORKFLOW

**Goal:** Customize `conductor/workflow.md` with project-specific preferences.

### Mode: `"human-in-the-loop"`

1. **Present default workflow:**
   > "The default workflow includes:
   > - Evaluate-Loop (PLAN → EVALUATE → EXECUTE → EVALUATE → FIX)
   > - Test-driven development where applicable
   > - Commit after every task
   > - Max 5 fix cycles before escalation
   >
   > Would you like to customize?
   > A) Use defaults (Recommended)
   > B) Customize"

2. **If Customize (Option B):**
   - **Q1:** "Required test coverage?" — A) 80% (Recommended) B) Type your own
   - **Q2:** "Commit frequency?" — A) After each task (Recommended) B) After each phase
   - **Q3:** "Max fix cycles before escalation?" — A) 5 (Recommended) B) 3 C) Type your own

3. **Update** `conductor/workflow.md` with customizations.

### Mode: `"agentic"`

1. **Use defaults.** No customization needed.

### Commit State
```json
{"last_successful_step": "2.4_workflow"}
```

---

## 3.0 INITIAL SPRINT GENERATION

**PROTOCOL: Generate a comprehensive development sprint with tracks based on everything gathered so far.**

### 3.1 Generate PRD (Product Requirements Document)

Create `conductor/prd.md` — this is the master planning document that synthesizes everything from Phase 2.

**Content structure:**

```markdown
# Product Requirements Document

**Project**: {project name}
**Generated**: YYYY-MM-DD
**Source**: Project analysis + product definition

## 1. Product Overview

### Vision
{from product.md}

### Current State
{from project analysis — what exists today}

### Tech Stack
{from tech-stack.md}

## 2. Architecture Overview

{from code analysis — entry points, key modules, data flow}

## 3. Current Features
{bulleted list of what's implemented — brownfield only}

## 4. Requirements & User Stories
{from product.md — synthesized into actionable requirements}

## 5. Gaps & Opportunities
{prioritized list}
- 🔴 Critical — blocks core functionality
- 🟡 Important — significant improvement
- 🟢 Nice-to-have — quality of life

## 6. Development Sprint

### Sprint Goal
{1 sentence}

### Tracks (ordered by priority and dependency)

| # | Track | Type | Priority | Depends On | Est. Complexity |
|---|-------|------|----------|------------|-----------------|
| 1 | ... | ... | 🔴 | — | S/M/L/XL |

### Dependency Graph
{show execution order}

## 7. Quality Baseline
- Test Coverage: {estimated}
- Known Issues: {count}
- Technical Debt: {assessment}
```

### 3.2 Propose Initial Sprint

**Mode-dependent behavior:**

#### Human-in-the-loop:

1. **Present the sprint proposal:**
   > "Based on the project analysis, I propose the following initial sprint with {N} tracks:"
   >
   > | # | Track | Type | Priority |
   > |---|-------|------|----------|
   > | 1 | ... | ... | ... |
   >
   > "How would you like to proceed?
   > A) Approve this sprint
   > B) Suggest changes
   > C) Start with just the first track"

2. **Iterate** based on user feedback.

#### Agentic:

1. **Auto-generate** the sprint. Announce what was created and proceed.

### 3.3 Create Track Artifacts

For EACH track in the approved sprint:

1. **Generate Track ID:** `{kebab-case-slug}_{YYYYMMDD}` (e.g., `add-auth-flow_20260327`)

2. **Create track directory:**
```
conductor/tracks/{track_id}/
├── spec.md
├── metadata.json
└── (plan.md will be generated during /orchestrator-supaconductor:go)
```

3. **Generate `spec.md`:**
```markdown
# Track Spec: {Track Name}

## Goal
{What success looks like}

## Requirements
{Specific deliverables}

## Acceptance Criteria
{Verifiable conditions for completion}

## Out of Scope
{What NOT to build — prevents scope creep}

## Technical Notes
{Architecture guidance, files to modify, patterns to follow}

## Dependencies
{Which other tracks must complete first}
```

4. **Create `metadata.json`:**
```json
{
  "version": 3,
  "track_id": "{track_id}",
  "name": "Human-readable Track Name",
  "type": "feature | bugfix | refactor | infrastructure",
  "status": "new",
  "priority": "critical | important | nice-to-have",
  "superpower_enhanced": true,
  "created_at": "YYYY-MM-DD",
  "depends_on": [],
  "sprint_order": 1,
  "loop_state": {
    "current_step": "NOT_STARTED",
    "step_status": "NOT_STARTED",
    "fix_cycle_count": 0
  }
}
```

5. **Register in `conductor/tracks.md`:**
Add each track to the Active Tracks table.

### 3.4 Update Project Files

1. **Update `conductor/index.md`:**
```markdown
# Project Status

**Last Updated**: YYYY-MM-DD
**Project**: {project name}

## Current Focus
Sprint: {sprint goal}
Next Track: {first track by priority/dependency order}

## Sprint Overview
- **Total Tracks**: {count}
- **Critical**: {count} | **Important**: {count} | **Nice-to-have**: {count}

## Track Summary
1. {track name} — {one-line description} [new]
2. {track name} — {one-line description} [new]

## System Health
- Conductor v3 initialized
- orchestrator-supaconductor: enabled
- PRD: generated
- Sprint: {N} tracks
```

2. **Populate `conductor/knowledge/patterns.md`** with actual patterns discovered during analysis:
```markdown
# Code Patterns & Conventions

## Architecture Patterns
{actual patterns found}

## Common Solutions
{actual solutions found}

## Naming Conventions
{actual conventions}

## Anti-patterns to Avoid
{any anti-patterns noticed}
```

### 3.5 Commit State
```json
{"last_successful_step": "3.3_initial_sprint_generated"}
```

---

## 4.0 FINALIZATION

### 4.1 Save Conductor Files

Add and commit all files:
```bash
git add conductor/
git commit -m "conductor(setup): Initialize SupaConductor with PRD and development sprint"
```

### 4.2 Final Announcement

```
## SupaConductor Fully Initialized

**Location**: conductor/
**Mode**: {mode} ({description})

### What Was Created

**Project Foundation:**
- conductor/product.md          — Product vision & requirements
- conductor/tech-stack.md       — Technology decisions
- conductor/product-guidelines.md — Design & product conventions
- conductor/workflow.md         — Development workflow configuration

**Sprint Planning:**
- conductor/prd.md              — Product Requirements Document
- {N} development tracks in conductor/tracks/
- Each track has spec.md + metadata.json

**Knowledge Base:**
- conductor/knowledge/patterns.md — Discovered code patterns
- conductor/knowledge/errors.json — Error tracking (empty)
- conductor/decision-log.md      — Decision history

### Sprint Overview

| # | Track | Type | Priority |
|---|-------|------|----------|
| 1 | ... | ... | 🔴 |
| 2 | ... | ... | 🟡 |
...

### Next Steps
Run `/orchestrator-supaconductor:go` to start executing the first track.
Or run `/orchestrator-supaconductor:go <specific goal>` to jump to a specific track.
```

---

## Re-initialization

If setup has already completed (`last_successful_step` is `"3.3_initial_sprint_generated"`):

```
## SupaConductor Already Initialized

**Status**: Active
**Tracks**: {N} active, {N} complete
**PRD**: conductor/prd.md
**Last Activity**: YYYY-MM-DD

Run `/orchestrator-supaconductor:status` to see current state.
Run `/orchestrator-supaconductor:new-track` to add a new track.
Run `/orchestrator-supaconductor:go` to start executing.
```

---

## Related

- `/orchestrator-supaconductor:go` — Start executing tracks
- `/orchestrator-supaconductor:new-track` — Add a track manually
- `/orchestrator-supaconductor:implement` — Run evaluate-loop on existing track
- `/orchestrator-supaconductor:status` — Check progress
- `conductor/prd.md` — Full product requirements document
- `conductor/workflow.md` — Full process documentation
