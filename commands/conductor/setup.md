---
name: setup
description: "Initialize the Conductor environment in a new project - creates conductor/ directory structure"
user_invocable: true
---

# /conductor:setup — Initialize Conductor Environment

Set up the Conductor workflow system in a new project. Creates the directory structure, registry files, and documentation needed to start using tracks.

## Usage

```bash
/conductor:setup
```

## What It Creates

```
conductor/
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

### 3. Create tracks.md

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

### 4. Create index.md

```markdown
# Project Status

**Last Updated**: YYYY-MM-DD

## Current Focus
(no active tracks)

## Recent Completions
(none)

## System Health
- Conductor v3 initialized
- Superpowers: enabled
```

### 5. Create decision-log.md

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

### 6. Create knowledge/patterns.md

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

### 7. Create knowledge/errors.json

```json
{
  "version": 1,
  "errors": []
}
```

### 8. Create workflow.md Link/Copy

Copy or reference the Conductor workflow documentation from the plugin's `docs/workflow.md`.

## Confirmation Output

```
## Conductor Initialized

**Location**: conductor/
**Files Created**: 6 files, 2 directories

**Next Steps**:
1. Run `/conductor:new-track` to create your first development track
2. Or run `/go <your goal>` to create and start a track automatically

**Quick Start**:
/go Add user authentication
```

## Re-initialization

If conductor/ already exists:
```
## Conductor Already Initialized

**Status**: Active
**Tracks**: 3 active, 7 complete
**Last Activity**: 2026-02-16

Run `/conductor:status` to see current state.
```

## Related

- `/conductor:new-track` — Create your first track
- `/go` — Start working immediately
- `conductor/workflow.md` — Full process documentation
