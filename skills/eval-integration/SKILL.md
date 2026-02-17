---
name: eval-integration
description: "Specialized integration evaluator for the Evaluate-Loop. Use this for evaluating tracks that integrate external services — Supabase auth/DB, Stripe payments, Gemini API, third-party APIs. Checks API contracts, auth flows, data persistence, error recovery, environment config, and end-to-end flow integrity. Dispatched by loop-execution-evaluator when track type is 'integration', 'auth', 'payments', or 'api'. Triggered by: 'evaluate integration', 'test auth flow', 'check API', 'verify payments'."
---

# Integration Evaluator Agent

Specialized evaluator for tracks that integrate external services — Supabase, Stripe, Gemini, or any third-party API.

## When This Evaluator Is Used

Dispatched by `loop-execution-evaluator` when the track involves:
- Authentication or database integration
- Payment processing integration
- AI/ML API integration
- Any external API connection

## Inputs Required

1. Track's `spec.md` and `plan.md`
2. Environment config (`.env.example`, env variable documentation)
3. API client code (`src/lib/`)
4. Database schema (if Supabase)
5. Webhook handlers (if Stripe)

## Evaluation Passes (6 checks)

### Pass 1: API Contract Verification

| Check | What to Look For |
|-------|-----------------|
| Request shapes | API calls send correct payload structure |
| Response handling | Responses parsed with correct types |
| Error responses | 4xx/5xx errors handled with user-friendly messaging |
| Rate limits | Rate limit handling present (retry, backoff, queue) |
| Timeout | Reasonable timeout set on API calls |
| Auth headers | Bearer token / API key sent correctly |

```markdown
### API Contracts: PASS ✅ / FAIL ❌
- Endpoints verified: [count]
- Missing error handling: [list]
- Type mismatches: [list]
```

### Pass 2: Authentication Flow

| Check | What to Look For |
|-------|-----------------|
| Sign up | Creates user, stores token, redirects to dashboard |
| Sign in | Validates credentials, stores token, redirects |
| Sign out | Clears token, redirects to home |
| Token refresh | Handles expired tokens (refresh or re-auth) |
| Protected routes | Unauthenticated users redirected to login |
| OAuth | Third-party login flow (if applicable) |

```markdown
### Auth Flow: PASS ✅ / FAIL ❌
- Flows tested: [sign up / sign in / sign out / token refresh]
- Broken flows: [list]
- Token handling: [correct / issues]
```

### Pass 3: Data Persistence & Schema Hygiene

**CRUD Operations:**

| Check | What to Look For |
|-------|-----------------|
| Create | Data saved correctly to database/storage |
| Read | Data retrieved and rendered correctly |
| Update | Changes persisted on save |
| Delete | Records removed, UI reflects deletion |
| Relationships | Foreign keys / joins working correctly |
| Storage | File uploads stored and retrievable (if applicable) |

**Database Schema Quality (MANDATORY for all new tables/migrations):**

| Check | Requirement | Why |
|-------|-------------|-----|
| Timestamps | `created_at`, `updated_at` on ALL mutable tables | Debugging, audit trail, cache invalidation |
| Primary keys | UUID with default OR auto-increment | Data uniqueness |
| Foreign keys | Explicit cascade rules (`on delete cascade`) | Prevent orphaned data |
| Indexes | Index ALL foreign keys | Query performance |
| Null constraints | New columns nullable OR have defaults | Backward compatibility |
| Unique constraints | Composite uniques where needed | Data integrity |
| Version history | JSONB column for flexible history | Schema evolution |

**Schema Anti-Patterns to Flag:**

```sql
-- ❌ BAD: No timestamps
create table brands (
  id uuid primary key,
  name text
);

-- ✅ GOOD: Complete schema
create table brands (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  created_at timestamptz default now() not null,
  updated_at timestamptz default now() not null
);

-- ❌ BAD: Foreign key without cascade
brand_id uuid references brands(id)

-- ✅ GOOD: Explicit cascade
brand_id uuid references brands(id) on delete cascade not null

-- ❌ BAD: New required column (breaks existing data)
alter table assets add column image_url text not null;

-- ✅ GOOD: Nullable or has default
alter table assets add column locked boolean default false;
```

```markdown
### Data Persistence & Schema: PASS ✅ / FAIL ❌
- CRUD operations: [which work / which fail]
- Data integrity: [any corruption or loss]
- Storage: [files accessible / issues]
- **Tables missing timestamps: [count] — [list]**
- **Foreign keys without indexes: [count] — [list]**
- **Migrations without defaults: [count] — [list]**
- **Orphaned data risk: [YES/NO — describe]**
```

### Pass 4: Error Recovery

| Check | What to Look For |
|-------|-----------------|
| Network failure | Offline/timeout → user sees error, can retry |
| Invalid data | Malformed responses → graceful fallback |
| Auth failure | Expired token → redirect to login, not crash |
| Payment failure | Declined card → clear message, can retry |
| API down | Service unavailable → error state, not blank screen |
| Partial failure | One API fails, others still work |

```markdown
### Error Recovery: PASS ✅ / FAIL ❌
- Scenarios tested: [list]
- Unhandled failures: [list]
- User messaging: [clear / missing]
```

### Pass 5: Environment Configuration

| Check | What to Look For |
|-------|-----------------|
| `.env.example` | All required variables documented |
| No secrets in code | No API keys, tokens, or passwords in source files |
| Environment switching | Dev/staging/prod configs separate |
| Missing vars | App handles missing env vars gracefully (error, not crash) |

```markdown
### Environment: PASS ✅ / FAIL ❌
- Variables documented: [YES/NO]
- Secrets in code: [NONE / list files with exposed secrets]
- Missing var handling: [graceful / crashes]
```

### Pass 6: End-to-End Flow

Walk through the complete user journey that involves this integration:

| Flow | Steps to Verify |
|------|----------------|
| Auth flow | Landing → Sign Up → Verify → Dashboard |
| Payment flow | Select plan → Checkout → Payment → Confirmation |
| Generation flow | Form → Generate → View → Download |

```markdown
### E2E Flow: PASS ✅ / FAIL ❌
- Flow tested: [describe]
- Steps completed: [X]/[Y]
- Broken at step: [which step, if any]
```

## Verdict Template

```markdown
## Integration Evaluation Report

**Track**: [track-id]
**Evaluator**: eval-integration
**Date**: [YYYY-MM-DD]
**Service**: [Supabase/Stripe/Gemini/etc.]

### Results
| Pass | Status | Issues |
|------|--------|--------|
| 1. API Contracts | PASS/FAIL | [details] |
| 2. Auth Flow | PASS/FAIL | [details] |
| 3. Data Persistence | PASS/FAIL | [details] |
| 4. Error Recovery | PASS/FAIL | [details] |
| 5. Environment | PASS/FAIL | [details] |
| 6. E2E Flow | PASS/FAIL | [details] |

### Verdict: PASS ✅ / FAIL ❌
[If FAIL, list specific fix actions for loop-fixer]
```

## Handoff

- **PASS** → Return to `loop-execution-evaluator` → Conductor marks complete
- **FAIL** → Return to `loop-execution-evaluator` → Conductor dispatches `loop-fixer`
