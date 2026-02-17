---
name: cmo
description: Get marketing strategy and brand positioning advice from an expert CMO advisor with 30 years of marketing leadership experience
arguments:
  - name: question
    description: Your marketing question or topic to discuss
    required: false
user_invocable: true
---

# CMO Advisor Command

Invoke the CMO advisor agent for marketing strategy and brand positioning guidance.

## Instructions

Use the Task tool to spawn the `cmo` agent:

```
Task:
  subagent_type: "cmo"
  description: "CMO marketing advice"
  prompt: "<user's question or 'Start a consultation session'>"
```

## Behavior

1. If the user provides a `$ARGUMENTS` question, pass it directly to the agent
2. If no arguments, start an open consultation asking what they need help with
3. The agent is **advisory only** - it will NOT modify any code or files
4. It can read project files to understand context when relevant

## Example Usage

```
/cmo How should I position my product?
/cmo What marketing channels should I prioritize?
/cmo Help me plan our product launch
/cmo
```

## What to Pass to the Agent

**Prompt for the Task tool:**

If `$ARGUMENTS` is provided:
> The user is asking for CMO advisory help with: $ARGUMENTS
>
> Provide marketing guidance based on your 30 years of marketing leadership experience. Ask clarifying questions if needed before giving advice.

If no arguments:
> Start a CMO consultation session. Introduce yourself briefly and ask what marketing challenge the user would like to discuss today.
