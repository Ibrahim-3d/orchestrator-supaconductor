#!/bin/bash
# Conductor Superpowers — Project Initialization Script
# Usage: bash ~/.claude/plugins/conductor-superpowers/scripts/setup.sh [project-dir]
#
# Creates the conductor/ directory structure in your project.

set -euo pipefail

PROJECT_DIR="${1:-.}"

echo "Initializing Conductor in: $PROJECT_DIR"

# Create directory structure
mkdir -p "$PROJECT_DIR/conductor/tracks"
mkdir -p "$PROJECT_DIR/conductor/knowledge"

# Create tracks.md if it doesn't exist
if [ ! -f "$PROJECT_DIR/conductor/tracks.md" ]; then
  cat > "$PROJECT_DIR/conductor/tracks.md" << 'TRACKS_EOF'
# Track Registry

## Active Tracks

| Track ID | Name | Status | Priority | Started |
|----------|------|--------|----------|---------|
| — | — | — | — | — |

## Completed Tracks

| Track ID | Name | Completed | Summary |
|----------|------|-----------|---------|
| — | — | — | — |

---

*Updated by Conductor orchestrator. Do not edit manually.*
TRACKS_EOF
  echo "  Created conductor/tracks.md"
fi

# Create decision-log.md if it doesn't exist
if [ ! -f "$PROJECT_DIR/conductor/decision-log.md" ]; then
  cat > "$PROJECT_DIR/conductor/decision-log.md" << 'DECISION_EOF'
# Decision Log

All product, pricing, architecture, and model decisions are logged here for audit trail and business document synchronization.

## Decisions

| Date | Track | Decision | Category | Impact | Logged By |
|------|-------|----------|----------|--------|-----------|
| — | — | — | — | — | — |

---

*Entries added automatically by business-docs-sync and lead consultations.*
DECISION_EOF
  echo "  Created conductor/decision-log.md"
fi

# Create knowledge/patterns.md if it doesn't exist
if [ ! -f "$PROJECT_DIR/conductor/knowledge/patterns.md" ]; then
  cat > "$PROJECT_DIR/conductor/knowledge/patterns.md" << 'PATTERNS_EOF'
# Project Knowledge — Patterns & Conventions

This file captures learned patterns, conventions, and best practices discovered during development. Updated by the Knowledge Manager and Retrospective Agent.

## Architecture Patterns

*No patterns recorded yet.*

## Code Conventions

*No conventions recorded yet.*

## Common Pitfalls

*No pitfalls recorded yet.*

---

*Updated automatically by Conductor knowledge agents.*
PATTERNS_EOF
  echo "  Created conductor/knowledge/patterns.md"
fi

# Copy workflow docs if they don't exist
PLUGIN_DIR="$(cd "$(dirname "$0")/.." && pwd)"

if [ ! -f "$PROJECT_DIR/conductor/workflow.md" ]; then
  if [ -f "$PLUGIN_DIR/docs/workflow.md" ]; then
    cp "$PLUGIN_DIR/docs/workflow.md" "$PROJECT_DIR/conductor/workflow.md"
    echo "  Copied conductor/workflow.md"
  fi
fi

if [ ! -f "$PROJECT_DIR/conductor/authority-matrix.md" ]; then
  if [ -f "$PLUGIN_DIR/docs/authority-matrix.md" ]; then
    cp "$PLUGIN_DIR/docs/authority-matrix.md" "$PROJECT_DIR/conductor/authority-matrix.md"
    echo "  Copied conductor/authority-matrix.md"
  fi
fi

echo ""
echo "Conductor initialized successfully!"
echo ""
echo "Next steps:"
echo "  1. Use /go <your goal> to start working"
echo "  2. Or /conductor new-track to create a track manually"
echo "  3. Run /conductor status to see current state"
