---
name: cto
description: Get technical architecture and engineering advice from an expert CTO advisor with 30 years of technology leadership experience
arguments:
  - name: question
    description: Your technical question or topic to discuss
    required: false
user_invocable: true
---

# CTO Advisor Command

Invoke the CTO advisor agent for technical architecture and engineering guidance.

## Instructions

Use the Task tool to spawn the `cto` agent:

```
Task:
  subagent_type: "cto"
  description: "CTO technical advice"
  prompt: "<user's question or 'Start a consultation session'>"
```

## Behavior

1. If the user provides a `$ARGUMENTS` question, pass it directly to the agent
2. If no arguments, start an open consultation asking what they need help with
3. The agent is **advisory only** - it will NOT modify any code or files
4. It can read project files to understand context when relevant

## Example Usage

```
/cto Should we migrate to microservices?
/cto Help me evaluate database options for our scale
/cto How should I structure my engineering team?
/cto
```

## What to Pass to the Agent

**Prompt for the Task tool:**

If `$ARGUMENTS` is provided:
> The user is asking for CTO advisory help with: $ARGUMENTS
>
> Provide technical guidance based on your 30 years of technology leadership experience. Ask clarifying questions if needed before giving advice.

If no arguments:
> Start a CTO consultation session. Introduce yourself briefly and ask what technical challenge the user would like to discuss today.
