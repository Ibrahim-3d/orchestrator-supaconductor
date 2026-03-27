---
name: close-track
description: "Close a completed track — run quality gate, update conductor state, commit, and optionally handle the git branch"
user_invocable: true
model: sonnet
arguments:
  - name: track_id
    description: "Track ID to close (defaults to the active track from tracks.md)"
    required: false
  - name: "--force"
    description: "Skip quality gate — use for abandoned or superseded tracks"
    required: false
---

# /orchestrator-supaconductor:close-track — Close a Completed Track

The single command to finalize a track. Runs the quality gate, updates all conductor state, commits, and optionally handles the git branch.

**SCOPE BOUNDARY: This command closes ONE track. It does NOT start the next track. After closing, it returns control to the user.**

## Your Task

### Step 1: Resolve Target Track

1. **If `$ARGUMENTS` contains a track ID:** Use that track.
2. **If no track ID provided:** Read `conductor/tracks.md` and find the track with status `in_progress` or `executing`.
   - If exactly one active track: use it.
   - If multiple active tracks: list them and ask the user which one to close.
   - If no active tracks: announce "No active tracks to close." and HALT.
3. **Read the track's files:**
   - `conductor/tracks/{track_id}/metadata.json`
   - `conductor/tracks/{track_id}/spec.md`
   - `conductor/tracks/{track_id}/plan.md`

### Step 2: Quality Gate

**If `--force` flag is present:** Skip to Step 3. Announce: "Force-closing track — skipping quality gate."

**Otherwise:**

1. **Check if phase-review already passed:** Read `metadata.json` → `loop_state.checkpoints.EVALUATE_EXECUTION`.
   - If `status` is `"PASSED"`: announce "Quality gate already passed. Proceeding to close." → Skip to Step 3.
   - If `status` is anything else: run the quality gate.

2. **Run quality gate** — execute the phase-review evaluation checklist:
   - Read `spec.md` → verify all deliverables exist
   - Read `plan.md` → verify all tasks are `[x]`
   - Check build passes (if applicable)
   - Check for regressions

3. **If quality gate FAILS:**
   - Display the failure report with specific issues
   - **Agentic mode:** Announce "Quality gate failed. Fix the issues and re-run `/close-track`." and HALT.
   - **Human-in-the-loop mode:** Present options:
     ```
     Quality gate failed. What would you like to do?
     A) Fix the issues now (I'll create fix tasks)
     B) Force-close anyway (skip quality gate)
     C) Cancel — keep track open
     ```
   - If A: Create fix tasks in plan.md, announce them, and HALT (user runs fixes then re-runs `/close-track`).
   - If B: Proceed to Step 3.
   - If C: HALT.

4. **If quality gate PASSES:** Continue to Step 3.

### Step 3: Update Conductor State

Perform ALL of the following updates:

#### 3a. Update `metadata.json`

```json
{
  "status": "complete",
  "completed_at": "YYYY-MM-DDTHH:MM:SSZ",
  "loop_state": {
    "current_step": "COMPLETE",
    "step_status": "COMPLETE"
  }
}
```

Keep all other fields. Only update `status`, `completed_at`, and `loop_state.current_step`/`step_status`.

#### 3b. Update `tracks.md`

1. **Remove** the track's row from the `## Active Tracks` table.
2. **Add** a row to the `## Completed Tracks` table:

```markdown
| {track_id} | {track_name} | {today's date} | {one-line summary from spec.md goal} |
```

#### 3c. Update `index.md`

1. Update `**Last Updated**` to today's date.
2. Move the track from `## Current Focus` to `## Recent Completions`.
3. If there are remaining active tracks, update `## Current Focus` to show the next one.
4. If no remaining active tracks, set `## Current Focus` to "(no active tracks)".

### Step 4: Commit Conductor Files

```bash
git add conductor/tracks/{track_id}/metadata.json
git add conductor/tracks.md
git add conductor/index.md
git commit -m "conductor(close): complete track {track_id}"
```

### Step 5: Handle Git Branch (Mode-Dependent)

**Check if on a feature branch:**

```bash
git branch --show-current
```

- If on `main` or `master`: Skip this step — no branch to handle.
- If on a feature branch: Invoke the `finishing-a-development-branch` skill to handle push/PR/merge.

### Step 6: Final Announcement

```
## Track Closed

**Track**: {track_id}
**Name**: {track_name}
**Status**: Complete
**Quality Gate**: PASSED (or SKIPPED with --force)
**Completed**: {today's date}

### Summary
{one-line summary from spec.md}

### What To Do Next (display to user — DO NOT execute)
- `/orchestrator-supaconductor:go` — start the next track
- `/orchestrator-supaconductor:status` — see remaining tracks
- `/orchestrator-supaconductor:new-track` — add a new track
```

### Step 7: HALT — Track Closed

**CRITICAL: STOP HERE. Do NOT proceed further. Do NOT invoke any other skills, commands, or tools after this point.**

The `/close-track` command is ONLY responsible for closing ONE track. Starting the next track is a separate user action. You must:
1. Display the Final Announcement above
2. Return control to the user
3. **Do NOT** run `/go` or start executing the next track
4. **Do NOT** invoke any execution skills

---

## Quick Reference

| Flag | Effect |
|------|--------|
| (no args) | Closes the active track with quality gate |
| `{track_id}` | Closes a specific track |
| `--force` | Skips quality gate (for abandoned/superseded tracks) |

## Related

- `/orchestrator-supaconductor:phase-review` — Run quality gate standalone
- `/orchestrator-supaconductor:finishing-a-development-branch` — Handle git branch separately
- `/orchestrator-supaconductor:status` — See current track state
- `/orchestrator-supaconductor:go` — Start the next track
