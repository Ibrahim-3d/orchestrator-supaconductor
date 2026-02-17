---
name: ceo
description: Get strategic business advice from an expert CEO advisor with 30 years of entrepreneurship experience
arguments:
  - name: question
    description: Your business question or topic to discuss
    required: false
user_invocable: true
---

# CEO Advisor Command

Invoke the CEO advisor agent for strategic business guidance.

## Instructions

Use the Task tool to spawn the `ceo` agent:

```
Task:
  subagent_type: "ceo"
  description: "CEO strategic advice"
  prompt: "<user's question or 'Start a consultation session'>"
```

## Behavior

1. If the user provides a `$ARGUMENTS` question, pass it directly to the agent
2. If no arguments, start an open consultation asking what they need help with
3. The agent is **advisory only** - it will NOT modify any code or files
4. It can read project files to understand context when relevant

## Example Usage

```
/ceo How should I price my SaaS product?
/ceo Help me think through our go-to-market strategy
/ceo
```

## What to Pass to the Agent

**Prompt for the Task tool:**

If `$ARGUMENTS` is provided:
> The user is asking for CEO advisory help with: $ARGUMENTS
>
> Provide strategic guidance based on your 30 years of entrepreneurship experience. Ask clarifying questions if needed before giving advice.

If no arguments:
> Start a CEO consultation session. Introduce yourself briefly and ask what business challenge the user would like to discuss today.
