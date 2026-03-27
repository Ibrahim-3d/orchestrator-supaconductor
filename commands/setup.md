---
name: setup
description: "Initialize the Conductor environment in a new project - creates conductor/ directory structure"
user_invocable: true
model: sonnet
---

# /supaconductor:setup — Initialize Conductor Environment

Set up the Conductor workflow system in a new project. Creates the directory structure, registry files, and documentation needed to start using tracks.

## Usage

```bash
/supaconductor:setup
```

## What It Creates

```
conductor/
├── config.json         # Project-level SupaConductor configuration
├── tracks.md           # Track registry (list of all tracks)
├── index.md            # Current project status overview
├── workflow.md         # Evaluate-Loop process documentation
├── decision-log.md     # Business and technical decision history
├── knowledge/
│   ├── patterns.md     # Discovered code patterns and conventions
│   └── errors.json     # Known errors and their fixes
└── tracks/             # Individual track directories (created per-track)
```

## Your Task

### 1. Check if Already Initialized

If `conductor/` directory exists, show current status instead of reinitializing.

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
| (none yet) | | | | | |

## Completed Tracks

| Track ID | Name | Completed | Summary |
|----------|------|-----------|---------|
| (none yet) | | | |
```

### 5. Create index.md

```markdown
# Project Status

**Last Updated**: YYYY-MM-DD

## Current Focus
(no active tracks)

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

## Confirmation Output

```
## Conductor Initialized

**Location**: conductor/
**Files Created**: 7 files, 2 directories
**Mode**: agentic (fully autonomous)
**To switch modes**: Edit `conductor/config.json` → set `"mode": "human-in-the-loop"`

**Next Steps**:
1. Run `/supaconductor:new-track` to create your first development track
2. Or run `/supaconductor:go <your goal>` to create and start a track automatically

**Quick Start**:
/supaconductor:go Add user authentication
```

## Re-initialization

If conductor/ already exists:
```
## Conductor Already Initialized

**Status**: Active
**Tracks**: 3 active, 7 complete
**Last Activity**: 2026-02-16

Run `/supaconductor:status` to see current state.
```

## Related

- `/supaconductor:new-track` — Create your first track
- `/supaconductor:go` — Start working immediately
- `conductor/workflow.md` — Full process documentation

