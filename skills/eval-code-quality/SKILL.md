---
name: eval-code-quality
description: "Specialized code quality evaluator for the Evaluate-Loop. Use this for evaluating code implementation tracks where the deliverable is functional code — features, API routes, state management, utilities. Checks build integrity, type safety, code patterns, error handling, dead code, imports, test coverage, and naming conventions. Dispatched by loop-execution-evaluator when track type is 'feature', 'refactor', or 'infrastructure'. Triggered by: 'evaluate code', 'code review', 'quality check', 'build check'."
---

# Code Quality Evaluator Agent

Specialized evaluator for tracks whose deliverables are functional code — features, state management, utilities, API routes.

## When This Evaluator Is Used

Dispatched by `loop-execution-evaluator` when the track is one of:
- Feature implementation (e.g., user authentication, data processing)
- Infrastructure/utility work
- Refactoring tracks
- State management (Zustand, hooks)

## Inputs Required

1. Track's `spec.md` and `plan.md`
2. Changed files (from plan.md task summaries or git diff)
3. `tsconfig.json` — TypeScript config
4. `package.json` — dependencies and scripts
5. Existing test files (if any)

## Evaluation Passes (6 checks)

### Pass 1: Build Integrity

```bash
npm run build    # Must exit 0
npx tsc --noEmit # Must exit 0 (no type errors)
```

```markdown
### Build: PASS ✅ / FAIL ❌
- Build status: [success / X errors]
- Type check: [clean / X type errors]
- Errors: [list if any]
```

### Pass 2: Type Safety

| Check | What to Look For |
|-------|-----------------|
| No `any` types | Explicit typing on all exports, function params, return types |
| Generic usage | API responses typed with `ApiResponse<T>` |
| Null safety | Optional chaining (`?.`) or null checks where data may be absent |
| Type exports | Shared types in `src/types/`, not inline |
| Interface consistency | Types match spec/product.md schema |

```markdown
### Type Safety: PASS ✅ / FAIL ❌
- `any` usage: [count] — [list files:lines]
- Missing types: [list untyped exports]
- Null safety issues: [list]
```

### Pass 3: Code Patterns & State Management

| Check | What to Look For |
|-------|-----------------|
| File structure | Files in correct directories per component architecture |
| Naming | kebab-case files, PascalCase components, `{Component}Props` |
| Imports | No circular imports, no unused imports |
| DRY | No significant code duplication (>10 lines repeated) |
| Single responsibility | Functions/components do one thing |
| Module boundaries | Feature code in feature dirs, shared code in `ui/` or `lib/` |
| **State sync** | **Every client state mutation has corresponding API endpoint** |
| **Optimistic updates** | **Rollback logic present on API failure** |
| **Source of truth** | **Server (DB) is source of truth, client is cache** |

**State Sync Anti-Patterns to Flag:**

```typescript
// ❌ BAD: State updated without API persistence
const toggleLock = (id) => {
  set({ assets: { ...assets, [id]: { locked: true } } });
  // No API call!
}

// ✅ GOOD: Optimistic update with API sync
const toggleLock = async (id) => {
  const prev = assets;
  set({ assets: { ...assets, [id]: { locked: true } } }); // Optimistic
  try {
    await fetch(`/api/assets/${id}`, {
      method: 'PATCH',
      body: JSON.stringify({ locked: true })
    });
  } catch (err) {
    set({ assets: prev }); // Rollback
    throw err;
  }
}
```

```markdown
### Code Patterns & State Sync: PASS ✅ / FAIL ❌
- Naming violations: [list]
- Unused imports: [list files]
- Duplication found: [describe]
- **State mutations without API: [count] — [list]**
- **Missing rollback logic: [count] — [list]**
- **API endpoints without client updates: [count] — [list]**
```

### Pass 4: Error Handling

| Check | What to Look For |
|-------|-----------------|
| API calls | try/catch or error handling on all async operations |
| User feedback | Toast/inline error shown to user on failure |
| Null data | Empty states handled (no data, loading, error) |
| Edge cases | Invalid input, network failure, timeout |
| No silent failures | Errors not swallowed without user notification |

```markdown
### Error Handling: PASS ✅ / FAIL ❌
- Unhandled async: [list functions]
- Missing user feedback: [list scenarios]
- Silent failures: [list]
```

### Pass 5: Dead Code & Cleanup

| Check | What to Look For |
|-------|-----------------|
| Unused exports | Functions/components exported but never imported |
| Commented code | Large blocks of commented-out code (should be deleted) |
| Unused files | Files that exist but aren't imported anywhere |
| TODO/FIXME | Unresolved TODO comments |
| Console logs | `console.log` left in production code |

```markdown
### Dead Code: PASS ✅ / FAIL ❌
- Unused exports: [list]
- Console logs: [list files:lines]
- TODOs: [list]
```

### Pass 6: Test Coverage (when applicable)

| Check | Target |
|-------|--------|
| Overall coverage | 70% |
| Business logic | 90% |
| API routes | 80% |
| Utility functions | 80% |

```markdown
### Tests: PASS ✅ / FAIL ❌ / ⚠️ NOT CONFIGURED
- Coverage: [X]% overall
- Business logic: [X]%
- Untested critical paths: [list]
```

## Verdict Template

```markdown
## Code Quality Evaluation Report

**Track**: [track-id]
**Evaluator**: eval-code-quality
**Date**: [YYYY-MM-DD]
**Files Evaluated**: [count]

### Results
| Pass | Status | Issues |
|------|--------|--------|
| 1. Build | PASS/FAIL | [details] |
| 2. Type Safety | PASS/FAIL | [count] issues |
| 3. Code Patterns | PASS/FAIL | [count] issues |
| 4. Error Handling | PASS/FAIL | [count] issues |
| 5. Dead Code | PASS/FAIL | [count] issues |
| 6. Tests | PASS/FAIL/N/A | [coverage] |

### Verdict: PASS ✅ / FAIL ❌
[If FAIL, list specific fix actions for loop-fixer]
```

## Handoff

- **PASS** → Return to `loop-execution-evaluator` → Conductor marks complete
- **FAIL** → Return to `loop-execution-evaluator` → Conductor dispatches `loop-fixer`
