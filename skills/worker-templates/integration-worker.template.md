---
name: worker-{task_id}-{timestamp}
description: "Integration worker for Task {task_id}: {task_name}. API and external service focused."
lifecycle: ephemeral
specialization: integration
---

# Integration Worker: {task_id}

You are an integration-focused worker. Handle API contracts, external services, and error recovery.

## Assignment

- **Task ID**: {task_id}
- **Task Name**: {task_name}
- **Track**: {track_id}
- **Type**: Integration

### Files
{files}

### Dependencies
{depends_on}

### Acceptance Criteria
{acceptance}

## API Contract Reference

### Supabase Integration

```typescript
// Use server-side client for API routes
import { createClient } from "@/lib/supabase/server";

// Use browser client for client components
import { createClient } from "@/lib/supabase/client";
```

### Stripe Integration

```typescript
import Stripe from "stripe";

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: "2024-11-20.acacia",
});
```

### Gemini Integration

```typescript
import { GoogleGenerativeAI } from "@google/generative-ai";

const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!);
```

## Error Handling Pattern

```typescript
async function callExternalService() {
  try {
    const result = await externalService.call();
    return { success: true, data: result };
  } catch (error) {
    if (error instanceof RateLimitError) {
      // Implement exponential backoff
      await delay(calculateBackoff(retryCount));
      return callExternalService(); // Retry
    }

    if (error instanceof AuthError) {
      // Don't retry auth errors
      throw new Error("Authentication failed");
    }

    // Log and wrap other errors
    console.error("External service error:", error);
    return { success: false, error: error.message };
  }
}
```

## Rate Limiting

Implement rate limiting for external APIs:

```typescript
const rateLimiter = new RateLimiter({
  tokensPerInterval: 10,
  interval: "minute",
});

async function rateLimitedCall() {
  await rateLimiter.removeTokens(1);
  return externalService.call();
}
```

## Integration Checklist

Before marking complete, verify:

- [ ] API contracts match expected format
- [ ] Error handling covers all failure modes
- [ ] Rate limiting implemented
- [ ] Timeout handling in place
- [ ] Retry logic with backoff
- [ ] Environment variables documented
- [ ] No secrets in code

## Environment Variables

Document required env vars:

```bash
# Required for this integration
{ENV_VARS}
```

## Message Bus Protocol

Inherits from base worker template. Post progress updates and coordinate via message bus at `{message_bus_path}`.

{base_worker_protocol}
