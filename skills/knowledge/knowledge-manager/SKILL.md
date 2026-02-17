---
name: knowledge-manager
description: "Loads relevant patterns and known errors before track planning. Searches conductor/knowledge/ for solutions we've used before and errors we've encountered. Injects findings into the planner prompt to prevent reinventing solutions and repeating mistakes. Triggered automatically by orchestrator before PLAN step."
---

# Knowledge Manager — Pre-Planning Intelligence

Searches the knowledge base for relevant patterns and errors before a track begins, injecting institutional memory into the planning process.

## When This Runs

**Automatically** — The orchestrator calls this agent BEFORE dispatching the `loop-planner` for any track.

## Inputs

1. **Track spec.md** — To understand what the track is about
2. **Track type** — From metadata.json (feature, UI, integration, etc.)
3. **Keywords** — Extracted from spec (e.g., "auth", "Supabase", "form", "state")

## Workflow

### 1. Extract Keywords from Spec

Read the track's `spec.md` and extract relevant keywords:

```typescript
const keywords = extractKeywords(spec);
// Example: ["authentication", "Supabase", "login", "signup", "OAuth"]
```

Keywords come from:
- Section headings
- Technical terms
- Integration names (Supabase, Stripe, Gemini)
- Component types (form, modal, grid, etc.)
- Pattern names (state management, API routes, etc.)

### 2. Search Pattern Library

Search `conductor/knowledge/patterns.md` for matching patterns:

```markdown
## Relevant Patterns Found

### Pattern: Supabase Client Singleton
**Category**: Integration
**Relevance**: Track mentions Supabase auth
**Summary**: Use singleton pattern with server/client separation
**Key Code**:
```tsx
// lib/supabase/server.ts
export const createClient = async () => { /* ... */ };
```

### Pattern: Server Actions with Error Handling
**Category**: API
**Relevance**: Track implements auth actions
**Summary**: Wrap all server actions with try/catch and typed responses
```

### 3. Search Error Registry

Search `conductor/knowledge/errors.json` for errors related to this track type:

```markdown
## Known Errors to Watch For

### Error: Hydration Mismatch (err-003)
**Pattern**: "Hydration failed because the initial UI does not match"
**Context**: Auth state can differ between server and client
**Prevention**: Wrap auth-dependent UI in useEffect or client component

### Error: NEXT_REDIRECT in try/catch (err-004)
**Pattern**: "NEXT_REDIRECT"
**Context**: Server actions with redirect after login
**Prevention**: Re-throw NEXT_REDIRECT errors or move redirect outside try/catch
```

### 4. Generate Knowledge Brief

Output a knowledge brief that gets injected into the planner's prompt:

```markdown
# Knowledge Brief for [Track ID]

## Relevant Patterns (Apply These)

1. **Supabase Client Singleton** — Use separate server/client clients
2. **Server Actions with Error Handling** — Typed responses with try/catch

## Known Errors (Avoid These)

1. **Hydration Mismatch** — Don't render auth-dependent UI on server
2. **NEXT_REDIRECT** — Handle redirect() specially in try/catch

## Previous Similar Work

- Track `auth-flow_20260115` implemented similar auth flow
- See `conductor/tracks/auth-flow_20260115/plan.md` for reference

## Recommendations

- Consider using the existing auth patterns from previous track
- Watch for SSR/client hydration issues with auth state
```

## Output Format

The Knowledge Manager returns a structured brief:

```json
{
  "patterns_found": [
    {
      "name": "Supabase Client Singleton",
      "category": "Integration",
      "relevance": "high",
      "summary": "...",
      "code_snippet": "..."
    }
  ],
  "errors_to_watch": [
    {
      "id": "err-003",
      "pattern": "Hydration mismatch",
      "prevention": "..."
    }
  ],
  "similar_tracks": [
    {
      "track_id": "auth-flow_20260115",
      "relevance": "Implemented OAuth flow"
    }
  ],
  "recommendations": [
    "Reuse auth patterns from previous track",
    "Watch for hydration issues"
  ]
}
```

## Integration with Orchestrator

The orchestrator injects this brief into the planner's dispatch:

```typescript
// In conductor-orchestrator
async function dispatchPlanner(trackId: string) {
  // 1. Run Knowledge Manager first
  const knowledgeBrief = await Task({
    subagent_type: "general-purpose",
    description: "Load knowledge for track",
    prompt: `You are the knowledge-manager agent.

      Track: ${trackId}
      Spec: ${specContent}

      Search conductor/knowledge/patterns.md and errors.json.
      Return a knowledge brief with relevant patterns and errors.`
  });

  // 2. Dispatch planner WITH knowledge brief
  await Task({
    subagent_type: "general-purpose",
    description: "Create track plan",
    prompt: `You are the loop-planner agent.

      ${knowledgeBrief.output}

      Create plan.md using the patterns above where applicable.
      Avoid the known errors listed.`
  });
}
```

## Search Strategies

### By Category
Match track type to pattern/error categories:
- UI track → Search "UI", "component", "styling" patterns
- Integration track → Search "Integration", "API", "Supabase", "Stripe" patterns
- Feature track → Search "State", "API", "Testing" patterns

### By Keyword
Fuzzy match keywords from spec against pattern descriptions and error contexts.

### By Recency
Prioritize patterns from recent tracks (more likely to be relevant to current codebase state).

## Maintaining the Knowledge Base

The Knowledge Manager is read-only. Writing to the knowledge base is done by:
- **Retrospective Agent** — After track completion
- **Fixer Agent** — When discovering new error patterns

## No Matches Found

If no relevant patterns or errors are found, return:

```json
{
  "patterns_found": [],
  "errors_to_watch": [],
  "similar_tracks": [],
  "recommendations": ["No prior patterns found. Document solutions discovered in this track."]
}
```

This is fine — it means we're doing something new. The retrospective will capture learnings after.
