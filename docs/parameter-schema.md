# Parameter Schema for SupaConductor Orchestration

**Purpose**: Define the standardized parameter format for invoking SupaConductor's bundled superpower skills from the orchestrator.

## Overview

SupaConductor's enhanced loop agents (Planner, Executor, Fixer) are powered by the bundled superpowers toolkit. They are invoked via the Claude CLI with specific parameters that configure them to write directly to SupaConductor's track structure. This document defines the parameter schema for each superpower type.

## Common Parameters

All SupaConductor superpower skills accept these common parameters:

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `--track-id` | string | Yes | Track identifier | `orchestrator-supaconductor-track_20260213` |
| `--metadata` | string | Yes | Path to `metadata.json` | `conductor/tracks/auth_2026/metadata.json` |

## Skill-Specific Schemas

### writing-plans

Used by the Planner agent when `superpower_enhanced: true` is set in track metadata.

```bash
claude --print "/orchestrator-supaconductor:writing-plans \
  --spec='conductor/tracks/{trackId}/spec.md' \
  --output-dir='conductor/tracks/{trackId}/' \
  --context-files='conductor/tech-stack.md,conductor/workflow.md,conductor/product.md' \
  --track-id='{trackId}' \
  --metadata='conductor/tracks/{trackId}/metadata.json' \
  --format='markdown' \
  --include-dag=true"
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--spec` | string | Yes | Path to specification file |
| `--output-dir` | string | Yes | Where to save `plan.md` |
| `--context-files` | string | Yes | Comma-separated context files |
| `--include-dag` | boolean | No | Whether to include dependency graph |

### executing-plans

Used by the Executor agent when `superpower_enhanced: true` is set in track metadata.

```bash
claude --print "/orchestrator-supaconductor:executing-plans \
  --plan='conductor/tracks/{trackId}/plan.md' \
  --track-dir='conductor/tracks/{trackId}/' \
  --metadata='conductor/tracks/{trackId}/metadata.json' \
  --track-id='{trackId}' \
  --mode='parallel'"
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--plan` | string | Yes | Path to `plan.md` to execute |
| `--track-dir` | string | Yes | Track directory for artifacts |
| `--mode` | string | No | Execution mode (`sequential` or `parallel`) |
| `--resume-from` | string | No | Task ID to resume execution from |

### systematic-debugging

Used by the Fixer agent when `superpower_enhanced: true` is set in track metadata.

```bash
claude --print "/orchestrator-supaconductor:systematic-debugging \
  --failures='conductor/tracks/{trackId}/evaluation-report.md' \
  --track-dir='conductor/tracks/{trackId}/' \
  --metadata='conductor/tracks/{trackId}/metadata.json' \
  --track-id='{trackId}' \
  --max-attempts=3"
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--failures` | string | Yes | Path to report containing failures |
| `--track-dir` | string | Yes | Track directory for artifacts |
| `--max-attempts` | integer | No | Max fix attempts before escalation |

### brainstorming

Used for architectural and creative tracks.

```bash
claude --print "/orchestrator-supaconductor:brainstorming \
  --context='Architectural decision for {trackId}' \
  --output-dir='conductor/tracks/{trackId}/brainstorm/' \
  --track-id='{trackId}' \
  --options-count=3"
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `--context` | string | Yes | Problem statement or context |
| `--output-dir` | string | Yes | Where to save brainstorming artifacts |
| `--options-count` | integer | No | Number of options to generate |

## Validation

All SupaConductor superpower skills MUST:
1. Validate required paths exist before execution.
2. Update the track's `metadata.json` checkpoint upon completion (PASS or FAIL).
3. Follow the [checkpoint-protocol.md](checkpoint-protocol.md) for progress tracking.
