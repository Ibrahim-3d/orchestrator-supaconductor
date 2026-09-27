# Contributing to SupaConductor

Contributions that improve reliability, interoperability, documentation, and the Evaluate-Loop are welcome.

## Before opening an issue

Use the right public surface:

- **Questions, ideas, and broad feature proposals:** [GitHub Discussions](https://github.com/Ibrahim-3d/orchestrator-supaconductor/discussions)
- **Reproducible bugs and scoped actionable work:** [GitHub Issues](https://github.com/Ibrahim-3d/orchestrator-supaconductor/issues)
- **Security vulnerabilities:** follow [SECURITY.md](SECURITY.md); do not publish exploit details in a public issue.

## Development setup

Clone the repository and load it directly in Claude Code:

```bash
git clone https://github.com/Ibrahim-3d/orchestrator-supaconductor.git
cd orchestrator-supaconductor
claude --plugin-dir .
```

Run the repository checks before submitting:

```bash
python3 scripts/validate-repo.py
find hooks scripts -type f -name '*.sh' -print0 | xargs -0 -r -n1 bash -n
```

You can also validate the Claude Code plugin package itself:

```bash
claude plugin validate .
```

## Pull requests

Keep pull requests focused. A useful PR should include:

1. **Problem** — what is broken, missing, or unnecessarily costly.
2. **Change** — what the PR changes.
3. **Validation** — how you verified the behavior.
4. **Compatibility** — any effect on Claude Code versions, platforms, commands, or existing tracks.

For behavior changes, update user-facing documentation in the same PR when necessary.

## Commit messages

The release pipeline uses Conventional Commit prefixes:

- `fix:` — bug fix; normally a patch release.
- `feat:` — new user-visible capability; normally a minor release.
- `docs:` — documentation only.
- `refactor:`, `perf:`, `test:`, `chore:` — maintenance categories.

Use `!` or a `BREAKING CHANGE:` footer only for genuine breaking changes.

## Project conventions

- Skills live under `skills/<skill-name>/SKILL.md` and require YAML frontmatter with `name` and `description`.
- Agents and commands require valid frontmatter and should declare the tools they actually use.
- Keep README claims, plugin metadata, marketplace metadata, release notes, and actual behavior synchronized.
- Do not introduce a second source of truth for roadmap or release state.
