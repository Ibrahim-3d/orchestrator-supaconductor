# SupaConductor Roadmap

SupaConductor is actively maintained. This roadmap communicates direction, not guaranteed dates.

## Now — stabilize the v3.7.x line

- Restore a reliable GitHub release pipeline and public release history.
- Keep plugin, marketplace, README, and license metadata synchronized.
- Add repository validation for JSON, skill/command frontmatter, Bash hooks, version alignment, and license alignment.
- Triage user-reported issues so resolved bugs do not remain visibly open.
- Investigate model-routing behavior reported in [#11](https://github.com/Ibrahim-3d/orchestrator-supaconductor/issues/11).

## Next

- Give users clearer control over model inheritance/routing without losing the Opus/Sonnet role split.
- Improve release and installation verification across fresh Claude Code environments.
- Expand contributor documentation and externally actionable issues.
- Validate the new Codex, Cursor, Antigravity, Windsurf, and GitHub Copilot adapters against fresh host installs and tighten any host-specific behavior gaps.

## Under consideration

- Additional safety/enforcement integrations where they materially improve the core orchestration workflow.
- A maintained GitHub Project with Roadmap, In Progress, Next Release, and Shipped views.

## Shipped

- Cross-platform adapter architecture for Codex, Cursor, Google Antigravity, Windsurf/Cascade, and GitHub Copilot, generated from the same canonical skills/commands/agents as the Claude Code plugin (addresses the portability direction behind [#2](https://github.com/Ibrahim-3d/orchestrator-supaconductor/issues/2)).

See [GitHub Releases](https://github.com/Ibrahim-3d/orchestrator-supaconductor/releases) for published versions and [CHANGELOG.md](CHANGELOG.md) for the full history.

## How to influence the roadmap

- Use [Discussions](https://github.com/Ibrahim-3d/orchestrator-supaconductor/discussions) for ideas, questions, and broader product feedback.
- Use [Issues](https://github.com/Ibrahim-3d/orchestrator-supaconductor/issues) for reproducible bugs and scoped actionable work.
- Open a pull request for a concrete improvement that fits the current direction.

Items can move, change scope, or be dropped as coding-agent hosts and their plugin APIs evolve.
