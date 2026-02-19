# Reddit Replies

Post: r/ClaudeCode — "I mixed Conductor + Superpowers + Orchestrator in one system"

---

## Reply to u/ultrathink-art

> "A Board that forgets last week's decision is just noise"

Yeah good point, I think we had an issue with that so I went and fixed it. Board decisions now get saved to actual files (`resolution.md` + a JSON session log) after every meeting. So they stick around between sessions instead of disappearing.

Also added a retrospective step that saves patterns and error fixes to a knowledge folder after each track finishes, so the system actually learns from past work now.

Thanks for bringing it up!

---

## Reply to u/Narrow-Belt-5030

> "Does yours manage the context window without human intervention?"

Yeah it does — each step runs in its own isolated session so context doesn't pile up in the main one. There's also a context-loader that only reads what's needed (project files first, then track files, skips anything too big).

I did tighten it up though — added hard limits like skipping files over 1MB, capping at 15 files per load, and making agents return short summaries instead of full reports back to the orchestrator. Should keep things a lot leaner now.

---

## Reply to u/Fit-Palpitation-7427

> "I need everything auto, not only after the discuss phase"

That's what `/go` does — you give it a goal and it handles everything end to end. No stopping between steps.

I did notice the execution part could pause for feedback in some cases when it shouldn't have, so I fixed that. Now when the orchestrator runs it, it goes through all tasks without stopping. It only pauses if something is actually broken or ambiguous.

---

## Reply to u/thurn2

> "Have you run into problems with subagents being unable to spawn their own subagents? And agent teams flooding the context window with pointless notifications?"

Good questions — on the sub-subagent thing, yeah workers can spawn their own sub-workers now. I made sure that's properly set up.

On context flooding — agents talk to each other through files (message bus), not through the conversation, so that part is clean. But I also added a rule where agents only return a short one-line summary to the orchestrator instead of dumping their full output. The details go into files that the orchestrator reads when it needs them.

---

## Reply to u/semmy_t

> "This is very nice, thank you for sharing :)"

Thanks! Just pushed some updates based on feedback from this thread. Let me know how it goes if you try it out!

---

## Reply to u/b0307

> "99% weekly usage consumed for minor decision of vibe coded orchestration"

Fair point — it does use more API calls than doing things manually since each step is its own session. That's the tradeoff for having structure and quality checks built in.

That said, skills only load when they're actually used (not all 40+ at once), and each agent runs in isolation so your main session stays light. If you're on a tight budget, you can use the individual commands (`/brainstorm`, `/board-review`, etc.) without running the full loop.

---

## Reply to u/vollpo

> "The new --auto flag runs through after the discuss phase, no more babysitting"

Yep exactly — `/go` runs the whole thing autonomously. It only stops if something is genuinely ambiguous or if the fix cycle fails 3 times. Otherwise it handles plan, execute, evaluate, fix all on its own.

---

## Reply to u/marky125

> "I've been using Zeroshot - how would you say it compares?"

Haven't used Zeroshot so I can't really compare fairly. The main things this does differently are persistent project context (specs, plans, track history survive across sessions), an evaluate-fix loop that catches issues automatically, and a Board of Directors for bigger architecture decisions.

If Zeroshot is working for you, the question is whether you need those extra layers. This is more for bigger features where you want automated review built in.

---

## Reply to u/fredagainbutagain

> "i found GSD... i wasn't getting anything done?"

Haha yeah I get that. The difference here is `/go` is just one command — you don't need to learn the whole system to use it. Give it a goal and it figures out the rest. The individual pieces are there if you want more control but they're not required.

---

## Reply to u/xRedStaRx

> "I made a fork in codex as well"

Nice! Would love to see how you adapted it. The whole thing is just markdown files so it should translate well to other tools. Happy to link your fork from the README if you want to share it.
