---
name: setup
description: "Initialize the Conductor environment, analyze the project, generate a PRD, and populate development tracks"
user_invocable: true
model: opus
---

# /supaconductor:setup — Full Project Initialization

Set up the Conductor workflow system **and** populate it with a real development plan. This is a 2-phase command:

- **Phase 1**: Create the conductor directory structure and configuration files
- **Phase 2**: Analyze the project, generate a PRD, and create an initial development sprint with tracks

## Usage

```bash
/supaconductor:setup
/supaconductor:setup <high-level project goal>
```

If a goal is provided via `$ARGUMENTS`, use it as the project vision. If not, infer the project's purpose from the codebase.

---

## Phase 1: Scaffold

### 1. Check if Already Initialized

If `conductor/` directory already exists with a `prd.md`, show current status and ask if the user wants to re-analyze. Do NOT recreate scaffold files that already exist.

If `conductor/` exists but has NO `prd.md` (scaffold-only state from a previous incomplete setup), skip to Phase 2.

### 2. Create Directory Structure

```bash
mkdir -p conductor/tracks
mkdir -p conductor/knowledge
```

### 3. Create config.json

```json
{
  "mode": "agentic",
  "max_fix_cycles": 5,
  "planning_model": "opus",
  "execution_model": "sonnet"
}
```

**Mode Options:**
- `"agentic"` (default) — Fully autonomous. Never stops for user input. All decisions resolved by agents, leads, and board.
- `"human-in-the-loop"` — Stops at key decision points to ask the user. Pauses on ambiguity, blockers, fix limits, and high-impact decisions.

**Model Options:**
- `"planning_model"` — Model used for plan creation, evaluation, brainstorming, board meetings, and advisory agents.
- `"execution_model"` — Model used for code execution, fixing, task workers, and operational commands.

### 4. Create tracks.md

```markdown
# Conductor Track Registry

Active and completed development tracks.

## Active Tracks

| Track ID | Name | Type | Status | Step | Created |
|----------|------|------|--------|------|---------|

## Completed Tracks

| Track ID | Name | Completed | Summary |
|----------|------|-----------|---------|
```

### 5. Create index.md

```markdown
# Project Status

**Last Updated**: YYYY-MM-DD

## Current Focus
(analyzing project...)

## Recent Completions
(none)

## System Health
- Conductor v3 initialized
- supaconductor: enabled
```

### 6. Create decision-log.md

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

### 7. Create knowledge/patterns.md

```markdown
# Code Patterns & Conventions

Discovered patterns from the codebase.

## Architecture Patterns
(add as discovered)

## Common Solutions
(add as discovered)

## Anti-patterns to Avoid
(add as discovered)
```

### 8. Create knowledge/errors.json

```json
{
  "version": 1,
  "errors": []
}
```

### 9. Create workflow.md Link/Copy

Copy or reference the Conductor workflow documentation from the plugin's `docs/workflow.md`.

---

## Phase 2: Project Analysis & Sprint Population

**This is the critical phase that turns empty scaffold into actionable development plans.**

### 10. Deep Project Analysis

Thoroughly analyze the project by reading:
- **README.md** (or similar) — project purpose, goals, setup instructions
- **package.json / pyproject.toml / Cargo.toml / go.mod** — dependencies, scripts, project metadata
- **Existing source code structure** — architecture patterns, entry points, key modules
- **Configuration files** — `.env.example`, `tsconfig.json`, `docker-compose.yml`, etc.
- **Test files** — what's tested, test framework, coverage gaps
- **Git history** (last 20 commits) — recent activity, active development areas
- **Any existing docs, specs, or guides** — domain knowledge, design docs
- **CI/CD config** — `.github/workflows/`, `Makefile`, build scripts

Build a mental model of:
- What the project IS (purpose, domain, users)
- What the project HAS (current features, architecture, tech stack)
- What the project NEEDS (gaps, TODOs, incomplete features, bugs)
- What the project's QUALITY is (test coverage, code health, technical debt)

### 11. Generate PRD (Product Requirements Document)

Create `conductor/prd.md` with a comprehensive PRD:

```markdown
# Product Requirements Document

**Project**: {project name}
**Generated**: YYYY-MM-DD
**Source**: Automated analysis of codebase

## 1. Product Overview

### Vision
{1-2 sentence project vision inferred from codebase}

### Current State
{Summary of what exists today — features, architecture, tech stack}

### Tech Stack
- **Runtime**: {e.g., Node.js 20, Python 3.12}
- **Framework**: {e.g., Next.js 14, FastAPI}
- **Database**: {e.g., PostgreSQL, MongoDB}
- **Key Dependencies**: {top 5-8 notable dependencies}

## 2. Architecture Overview

{Brief description of the codebase architecture — entry points, key modules, data flow}

```
{ASCII directory tree of key directories, max 3 levels deep}
```

## 3. Current Features (What Exists)

{Bulleted list of features that are currently implemented and working}

## 4. Gaps & Opportunities (What's Needed)

{Bulleted list of gaps, TODOs, incomplete features, missing tests, technical debt}

Prioritize by:
- 🔴 Critical — blocks core functionality
- 🟡 Important — significant improvement
- 🟢 Nice-to-have — quality of life

## 5. Development Sprint

### Sprint Goal
{1 sentence describing the sprint focus}

### Tracks (ordered by priority and dependency)

| # | Track | Type | Priority | Depends On | Est. Complexity |
|---|-------|------|----------|------------|-----------------|
| 1 | {track name} | feature/bugfix/refactor/infra | 🔴/🟡/🟢 | — | S/M/L/XL |
| 2 | {track name} | ... | ... | #1 | ... |
| ... | ... | ... | ... | ... | ... |

### Dependency Graph
{Show which tracks depend on which, so execution order is clear}

## 6. Quality Baseline

- **Test Coverage**: {estimated or measured}
- **Known Issues**: {count and severity}
- **Technical Debt**: {brief assessment}
```

### 12. Create Development Tracks

For each track identified in the PRD's Sprint section, create the track:

1. Create track directory: `conductor/tracks/{track-slug}_{YYYYMMDD}/`
2. Generate `spec.md` with:
   - **Goal**: What success looks like for this track
   - **Requirements**: Specific deliverables
   - **Acceptance Criteria**: How to verify completion
   - **Out of Scope**: Boundaries to prevent scope creep
   - **Technical Notes**: Architecture guidance, files to modify, patterns to follow
   - **Dependencies**: Which other tracks must complete first
3. Create `metadata.json`:
```json
{
  "version": 3,
  "track_id": "{track-slug}_{YYYYMMDD}",
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

### 13. Populate Track Registry

Update `conductor/tracks.md` with ALL created tracks:

```markdown
## Active Tracks

| Track ID | Name | Type | Status | Step | Priority | Created |
|----------|------|------|--------|------|----------|---------|
| track-1_20260327 | Track One | feature | new | NOT_STARTED | 🔴 | 2026-03-27 |
| track-2_20260327 | Track Two | bugfix | new | NOT_STARTED | 🟡 | 2026-03-27 |
```

### 14. Update index.md

Update `conductor/index.md` with the populated project status:

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
- **Estimated Effort**: {S/M/L/XL overall}

## Track Summary
1. {track name} — {one-line description} [{status}]
2. {track name} — {one-line description} [{status}]
...

## System Health
- Conductor v3 initialized
- supaconductor: enabled
- PRD: generated
- Sprint: populated with {N} tracks
```

### 15. Update knowledge/patterns.md

Populate with actual patterns discovered during analysis:

```markdown
# Code Patterns & Conventions

Discovered patterns from the codebase.

## Architecture Patterns
{actual patterns found — e.g., "MVC with service layer", "Feature-based folder structure"}

## Common Solutions
{actual solutions found — e.g., "Auth via JWT middleware", "State management via Zustand"}

## Naming Conventions
{actual conventions — e.g., "Components: PascalCase, utils: camelCase"}

## Anti-patterns to Avoid
{any anti-patterns noticed during analysis}
```

---

## Confirmation Output

```
## Conductor Fully Initialized

**Location**: conductor/
**Mode**: agentic (fully autonomous)

### Phase 1: Scaffold ✓
- 7 config files created
- 2 directories created

### Phase 2: Project Analysis ✓
- PRD generated: conductor/prd.md
- {N} development tracks created
- Sprint populated and ordered by priority/dependency
- Code patterns documented

### Sprint Overview
| # | Track | Type | Priority |
|---|-------|------|----------|
| 1 | ... | ... | 🔴 |
| 2 | ... | ... | 🟡 |
...

### Ready to Go
Run `/supaconductor:go` to start executing the first track.
Or run `/supaconductor:go <specific goal>` to jump to a specific track.
```

## Re-initialization

If conductor/ already exists with prd.md:
```
## Conductor Already Initialized

**Status**: Active
**Tracks**: 3 active, 7 complete
**Last Activity**: 2026-02-16
**PRD**: conductor/prd.md

Run `/supaconductor:status` to see current state.
Run `/supaconductor:setup --refresh` to re-analyze the project and update the PRD.
```

## Related

- `/supaconductor:go` — Start executing tracks
- `/supaconductor:new-track` — Add a track manually
- `/supaconductor:status` — Check progress
- `conductor/prd.md` — Full product requirements document
- `conductor/workflow.md` — Full process documentation
