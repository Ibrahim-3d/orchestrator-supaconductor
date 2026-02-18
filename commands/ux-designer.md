---
name: ux-designer
description: Get UX strategy and design guidance from an expert UX Designer with 30 years of user experience and product design experience
arguments:
  - name: question
    description: Your design question or topic to discuss
    required: false
user_invocable: true
---

# UX Designer Advisor Command

Invoke the UX Designer advisor agent for user experience and design guidance.

## Instructions

Use the Task tool to spawn the `ux-designer` agent:

```
Task:
  subagent_type: "ux-designer"
  description: "UX design advice"
  prompt: "<user's question or 'Start a consultation session'>"
```

## Behavior

1. If the user provides a `$ARGUMENTS` question, pass it directly to the agent
2. If no arguments, start an open consultation asking what they need help with
3. The agent is **advisory only** - it will NOT modify any code or files
4. It can read project files to understand context when relevant

## Example Usage

```
/ux-designer How should I structure the navigation?
/ux-designer Review this user flow for pain points
/ux-designer What's the best pattern for this form?
/ux-designer
```

## What to Pass to the Agent

**Prompt for the Task tool:**

If `$ARGUMENTS` is provided:
> The user is asking for UX design advisory help with: $ARGUMENTS
>
> Provide design guidance based on your 30 years of user experience design expertise. Ask clarifying questions if needed before giving advice.

If no arguments:
> Start a UX design consultation session. Introduce yourself briefly and ask what design challenge the user would like to discuss today.
