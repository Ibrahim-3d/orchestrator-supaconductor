---
name: writing-plans
description: Use when you have a spec or requirements for a multi-step task, before touching code
---

# Writing Plans

## Overview

Write comprehensive implementation plans assuming the engineer has zero context for our codebase and questionable taste. Document everything they need to know: which files to touch for each task, code, testing, docs they might need to check, how to test it. Give them the whole plan as bite-sized tasks. DRY. YAGNI. TDD. Frequent commits.

Assume they are a skilled developer, but know almost nothing about our toolset or problem domain. Assume they don't know good test design very well.

**Announce at start:** "I'm using the writing-plans skill to create the implementation plan."

**Save plans to:** The active conductor track directory: `conductor/tracks/{track_id}/plan.md`
If no conductor track exists, create one first using the `/orchestrator-supaconductor:new-track` flow.

## Bite-Sized Task Granularity

**Each step is one action (2-5 minutes):**
- "Write the failing test" - step
- "Run it to make sure it fails" - step
- "Implement the minimal code to make the test pass" - step
- "Run the tests and make sure they pass" - step
- "Commit" - step

## Plan Document Header

**Every plan MUST start with this header:**

```markdown
# [Feature Name] Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use orchestrator-supaconductor:executing-plans to implement this plan task-by-task.

**Goal:** [One sentence describing what this builds]

**Architecture:** [2-3 sentences about approach]

**Tech Stack:** [Key technologies/libraries]

---
```

## Task Structure

````markdown
### Task N: [Component Name]

**Files:**
- Create: `exact/path/to/file.py`
- Modify: `exact/path/to/existing.py:123-145`
- Test: `tests/exact/path/to/test.py`

**Step 1: Write the failing test**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**Step 2: Run test to verify it fails**

Run: `pytest tests/path/test.py::test_name -v`
Expected: FAIL with "function not defined"

**Step 3: Write minimal implementation**

```python
def function(input):
    return expected
```

**Step 4: Run test to verify it passes**

Run: `pytest tests/path/test.py::test_name -v`
Expected: PASS

**Step 5: Commit**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: add specific feature"
```
````

## Remember
- Exact file paths always
- Complete code in plan (not "add validation")
- Exact commands with expected output
- Reference relevant skills with @ syntax
- DRY, YAGNI, TDD, frequent commits

## Conductor Integration

This skill is part of the Conductor workflow. All plans are saved to the active track directory.

**When invoked by the Conductor orchestrator** (with `--track-dir` and `--spec` parameters):
- Read spec from `--spec` path
- Read project context from `conductor/product.md`, `conductor/tech-stack.md`
- Save plan to `{--track-dir}/plan.md`
- Include DAG section for parallel execution
- Update track's `metadata.json` checkpoint to `PLAN: PASSED`
- Return control to orchestrator — do NOT start execution

**When invoked standalone** (no parameters):
- Look for the active track in `conductor/tracks.md`
- Read its `spec.md` for requirements
- Save plan to `conductor/tracks/{track_id}/plan.md`
- Update track's `metadata.json` checkpoint to `PLAN: PASSED`
- After saving, announce the plan summary and HALT — do NOT start execution
- The user should run `/orchestrator-supaconductor:implement` or `/orchestrator-supaconductor:go` to execute

