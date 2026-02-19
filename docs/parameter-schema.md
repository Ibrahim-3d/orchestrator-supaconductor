# Superpower Parameter Schema

**Purpose**: Define the standardized parameter format for invoking superpowers from Conductor orchestrator.

**Version**: 1.0
**Created**: 2026-02-13

---

## Overview

Superpowers are invoked via the Claude CLI with specific parameters that configure them to write directly to Conductor's track structure. This document defines the parameter schema for each superpower type.

---

## Common Parameters

All superpowers accept these common parameters:

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `--track-id` | string | Yes | Track identifier | `conductor-superpowers_20260213` |
| `--track-dir` | path | Yes | Track directory path | `conductor/tracks/{track-id}/` |
| `--metadata` | path | Yes | Metadata.json path for state tracking | `conductor/tracks/{track-id}/metadata.json` |

---

## Superpower-Specific Parameters

### 1. superpowers:writing-plans

**Purpose**: Generate implementation plan from specification.

**Invocation Pattern**:
```bash
claude --print "/superpowers:writing-plans \
  --spec=<path> \
  --output-dir=<path> \
  --context-files=<paths> \
  --track-id=<id> \
  --metadata=<path>"
```

**Parameters**:

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `--spec` | path | Yes | Path to spec.md file | `conductor/tracks/{track-id}/spec.md` |
| `--output-dir` | path | Yes | Where to write plan.md | `conductor/tracks/{track-id}/` |
| `--context-files` | csv-paths | Yes | Project context files (comma-separated) | `conductor/tech-stack.md,conductor/workflow.md,conductor/product.md` |
| `--format` | string | No | Output format (default: markdown) | `markdown` |
| `--include-dag` | boolean | No | Include DAG for parallel execution | `true` |

**Output Files**:
- `{output-dir}/plan.md` - Implementation plan with phases and tasks
- `{metadata}` - Updated with checkpoint: `checkpoints.PLAN.status = "PASSED"`

---

### 2. superpowers:executing-plans

**Purpose**: Execute tasks from implementation plan.

**Invocation Pattern**:
```bash
claude --print "/superpowers:executing-plans \
  --plan=<path> \
  --track-dir=<path> \
  --metadata=<path> \
  --track-id=<id> \
  --resume-from=<task-id>"
```

**Parameters**:

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `--plan` | path | Yes | Path to plan.md file | `conductor/tracks/{track-id}/plan.md` |
| `--track-dir` | path | Yes | Track directory for file operations | `conductor/tracks/{track-id}/` |
| `--metadata` | path | Yes | Metadata.json for checkpoint updates | `conductor/tracks/{track-id}/metadata.json` |
| `--resume-from` | task-id | No | Task ID to resume from (for interruptions) | `2.3` |
| `--mode` | string | No | Execution mode: `sequential` or `parallel` | `parallel` |

**Output Files**:
- Code changes across the codebase
- `{plan}` - Updated with completion markers `[x]` and commit SHAs
- `{metadata}` - Updated with checkpoint: `checkpoints.EXECUTE.status = "PASSED"`

---

### 3. superpowers:systematic-debugging

**Purpose**: Fix failures identified by evaluation.

**Invocation Pattern**:
```bash
claude --print "/superpowers:systematic-debugging \
  --failures=<path> \
  --track-dir=<path> \
  --metadata=<path> \
  --track-id=<id>"
```

**Parameters**:

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `--failures` | path | Yes | Evaluation report with failure details | `conductor/tracks/{track-id}/evaluation-report.md` |
| `--track-dir` | path | Yes | Track directory for fixes | `conductor/tracks/{track-id}/` |
| `--metadata` | path | Yes | Metadata.json for checkpoint updates | `conductor/tracks/{track-id}/metadata.json` |
| `--max-attempts` | number | No | Max fix attempts before escalating | `3` |

**Output Files**:
- Code fixes across the codebase
- `{track-dir}/fix-log.md` - Log of fixes applied
- `{metadata}` - Updated with checkpoint: `checkpoints.FIX.status = "PASSED"`

---

### 4. superpowers:brainstorming

**Purpose**: Generate structured options for creative/architectural decisions.

**Invocation Pattern**:
```bash
claude --print "/superpowers:brainstorming \
  --context=<description> \
  --output-dir=<path> \
  --track-id=<id>"
```

**Parameters**:

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `--context` | string | Yes | Decision context description | `Architectural decision for {track-id}` |
| `--output-dir` | path | Yes | Where to write brainstorm results | `conductor/tracks/{track-id}/brainstorm/` |
| `--track-id` | string | Yes | Track identifier | `conductor-superpowers_20260213` |
| `--options-count` | number | No | Number of options to generate | `3` |

**Output Files**:
- `{output-dir}/options.md` - Structured options with pros/cons
- `{output-dir}/recommendation.md` - Recommended approach

---

## State Synchronization

All superpowers must update metadata.json during execution. See [checkpoint-protocol.md](checkpoint-protocol.md) for the full checkpoint update format.

### Checkpoint Update Format

```json
{
  "loop_state": {
    "checkpoints": {
      "PLAN": {
        "status": "PASSED",
        "completed_at": "2026-02-13T12:00:00Z",
        "agent": "superpowers:writing-plans",
        "output_files": ["plan.md"],
        "notes": "Plan generated with 5 phases, 35 tasks"
      }
    }
  }
}
```

---

## Error Handling

### Exit Codes

| Code | Meaning | Action |
|------|---------|--------|
| 0 | Success | Continue to next step |
| 1 | Generic failure | Log error, update metadata to FAILED |
| 2 | Missing required parameter | Escalate to user |
| 3 | File not found | Escalate to user |
| 4 | Blocked by dependency | Update metadata to BLOCKED |

---

## Path Resolution

All paths should be relative to the project root:

```bash
# Correct
--spec='conductor/tracks/track-name_20260213/spec.md'

# Incorrect
--spec='/absolute/path/to/conductor/tracks/track-name_20260213/spec.md'
```
