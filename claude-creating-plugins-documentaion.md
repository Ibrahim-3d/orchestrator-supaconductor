> ## Documentation Index

> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt

> Use this file to discover all available pages before exploring further.



\# Create plugins



> Create custom plugins to extend Claude Code with skills, agents, hooks, and MCP servers.



Plugins let you extend Claude Code with custom functionality that can be shared across projects and teams. This guide covers creating your own plugins with skills, agents, hooks, and MCP servers.



Looking to install existing plugins? See \[Discover and install plugins](/en/discover-plugins). For complete technical specifications, see \[Plugins reference](/en/plugins-reference).



\## When to use plugins vs standalone configuration



Claude Code supports two ways to add custom skills, agents, and hooks:



| Approach                                                    | Skill names          | Best for                                                                                        |

| :---------------------------------------------------------- | :------------------- | :---------------------------------------------------------------------------------------------- |

| \*\*Standalone\*\* (`.claude/` directory)                       | `/hello`             | Personal workflows, project-specific customizations, quick experiments                          |

| \*\*Plugins\*\* (directories with `.claude-plugin/plugin.json`) | `/plugin-name:hello` | Sharing with teammates, distributing to community, versioned releases, reusable across projects |



\*\*Use standalone configuration when\*\*:



\* You're customizing Claude Code for a single project

\* The configuration is personal and doesn't need to be shared

\* You're experimenting with skills or hooks before packaging them

\* You want short skill names like `/hello` or `/deploy`



\*\*Use plugins when\*\*:



\* You want to share functionality with your team or community

\* You need the same skills/agents across multiple projects

\* You want version control and easy updates for your extensions

\* You're distributing through a marketplace

\* You're okay with namespaced skills like `/my-plugin:hello` (namespacing prevents conflicts between plugins)



<Tip>

&#x20; Start with standalone configuration in `.claude/` for quick iteration, then \[convert to a plugin](#convert-existing-configurations-to-plugins) when you're ready to share.

</Tip>



\## Quickstart



This quickstart walks you through creating a plugin with a custom skill. You'll create a manifest (the configuration file that defines your plugin), add a skill, and test it locally using the `--plugin-dir` flag.



\### Prerequisites



\* Claude Code \[installed and authenticated](/en/quickstart#step-1-install-claude-code)

\* Claude Code version 1.0.33 or later (run `claude --version` to check)



<Note>

&#x20; If you don't see the `/plugin` command, update Claude Code to the latest version. See \[Troubleshooting](/en/troubleshooting) for upgrade instructions.

</Note>



\### Create your first plugin



<Steps>

&#x20; <Step title="Create the plugin directory">

&#x20;   Every plugin lives in its own directory containing a manifest and your skills, agents, or hooks. Create one now:



&#x20;   ```bash  theme={null}

&#x20;   mkdir my-first-plugin

&#x20;   ```

&#x20; </Step>



&#x20; <Step title="Create the plugin manifest">

&#x20;   The manifest file at `.claude-plugin/plugin.json` defines your plugin's identity: its name, description, and version. Claude Code uses this metadata to display your plugin in the plugin manager.



&#x20;   Create the `.claude-plugin` directory inside your plugin folder:



&#x20;   ```bash  theme={null}

&#x20;   mkdir my-first-plugin/.claude-plugin

&#x20;   ```



&#x20;   Then create `my-first-plugin/.claude-plugin/plugin.json` with this content:



&#x20;   ```json my-first-plugin/.claude-plugin/plugin.json theme={null}

&#x20;   {

&#x20;   "name": "my-first-plugin",

&#x20;   "description": "A greeting plugin to learn the basics",

&#x20;   "version": "1.0.0",

&#x20;   "author": {

&#x20;   "name": "Your Name"

&#x20;   }

&#x20;   }

&#x20;   ```



&#x20;   | Field         | Purpose                                                                                                |

&#x20;   | :------------ | :----------------------------------------------------------------------------------------------------- |

&#x20;   | `name`        | Unique identifier and skill namespace. Skills are prefixed with this (e.g., `/my-first-plugin:hello`). |

&#x20;   | `description` | Shown in the plugin manager when browsing or installing plugins.                                       |

&#x20;   | `version`     | Track releases using \[semantic versioning](/en/plugins-reference#version-management).                  |

&#x20;   | `author`      | Optional. Helpful for attribution.                                                                     |



&#x20;   For additional fields like `homepage`, `repository`, and `license`, see the \[full manifest schema](/en/plugins-reference#plugin-manifest-schema).

&#x20; </Step>



&#x20; <Step title="Add a skill">

&#x20;   Skills live in the `skills/` directory. Each skill is a folder containing a `SKILL.md` file. The folder name becomes the skill name, prefixed with the plugin's namespace (`hello/` in a plugin named `my-first-plugin` creates `/my-first-plugin:hello`).



&#x20;   Create a skill directory in your plugin folder:



&#x20;   ```bash  theme={null}

&#x20;   mkdir -p my-first-plugin/skills/hello

&#x20;   ```



&#x20;   Then create `my-first-plugin/skills/hello/SKILL.md` with this content:



&#x20;   ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}

&#x20;   ---

&#x20;   description: Greet the user with a friendly message

&#x20;   disable-model-invocation: true

&#x20;   ---



&#x20;   Greet the user warmly and ask how you can help them today.

&#x20;   ```

&#x20; </Step>



&#x20; <Step title="Test your plugin">

&#x20;   Run Claude Code with the `--plugin-dir` flag to load your plugin:



&#x20;   ```bash  theme={null}

&#x20;   claude --plugin-dir ./my-first-plugin

&#x20;   ```



&#x20;   Once Claude Code starts, try your new skill:



&#x20;   ```shell  theme={null}

&#x20;   /my-first-plugin:hello

&#x20;   ```



&#x20;   You'll see Claude respond with a greeting. Run `/help` to see your skill listed under the plugin namespace.



&#x20;   <Note>

&#x20;     \*\*Why namespacing?\*\* Plugin skills are always namespaced (like `/greet:hello`) to prevent conflicts when multiple plugins have skills with the same name.



&#x20;     To change the namespace prefix, update the `name` field in `plugin.json`.

&#x20;   </Note>

&#x20; </Step>



&#x20; <Step title="Add skill arguments">

&#x20;   Make your skill dynamic by accepting user input. The `$ARGUMENTS` placeholder captures any text the user provides after the skill name.



&#x20;   Update your `SKILL.md` file:



&#x20;   ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}

&#x20;   ---

&#x20;   description: Greet the user with a personalized message

&#x20;   ---



&#x20;   # Hello Skill



&#x20;   Greet the user named "$ARGUMENTS" warmly and ask how you can help them today. Make the greeting personal and encouraging.

&#x20;   ```



&#x20;   Run `/reload-plugins` to pick up the changes, then try the skill with your name:



&#x20;   ```shell  theme={null}

&#x20;   /my-first-plugin:hello Alex

&#x20;   ```



&#x20;   Claude will greet you by name. For more on passing arguments to skills, see \[Skills](/en/skills#pass-arguments-to-skills).

&#x20; </Step>

</Steps>



You've successfully created and tested a plugin with these key components:



\* \*\*Plugin manifest\*\* (`.claude-plugin/plugin.json`): describes your plugin's metadata

\* \*\*Skills directory\*\* (`skills/`): contains your custom skills

\* \*\*Skill arguments\*\* (`$ARGUMENTS`): captures user input for dynamic behavior



<Tip>

&#x20; The `--plugin-dir` flag is useful for development and testing. When you're ready to share your plugin with others, see \[Create and distribute a plugin marketplace](/en/plugin-marketplaces).

</Tip>



\## Plugin structure overview



You've created a plugin with a skill, but plugins can include much more: custom agents, hooks, MCP servers, and LSP servers.



<Warning>

&#x20; \*\*Common mistake\*\*: Don't put `commands/`, `agents/`, `skills/`, or `hooks/` inside the `.claude-plugin/` directory. Only `plugin.json` goes inside `.claude-plugin/`. All other directories must be at the plugin root level.

</Warning>



| Directory         | Location    | Purpose                                                                        |

| :---------------- | :---------- | :----------------------------------------------------------------------------- |

| `.claude-plugin/` | Plugin root | Contains `plugin.json` manifest (optional if components use default locations) |

| `commands/`       | Plugin root | Skills as Markdown files                                                       |

| `agents/`         | Plugin root | Custom agent definitions                                                       |

| `skills/`         | Plugin root | Agent Skills with `SKILL.md` files                                             |

| `hooks/`          | Plugin root | Event handlers in `hooks.json`                                                 |

| `.mcp.json`       | Plugin root | MCP server configurations                                                      |

| `.lsp.json`       | Plugin root | LSP server configurations for code intelligence                                |

| `settings.json`   | Plugin root | Default \[settings](/en/settings) applied when the plugin is enabled            |



<Note>

&#x20; \*\*Next steps\*\*: Ready to add more features? Jump to \[Develop more complex plugins](#develop-more-complex-plugins) to add agents, hooks, MCP servers, and LSP servers. For complete technical specifications of all plugin components, see \[Plugins reference](/en/plugins-reference).

</Note>



\## Develop more complex plugins



Once you're comfortable with basic plugins, you can create more sophisticated extensions.



\### Add Skills to your plugin



Plugins can include \[Agent Skills](/en/skills) to extend Claude's capabilities. Skills are model-invoked: Claude automatically uses them based on the task context.



Add a `skills/` directory at your plugin root with Skill folders containing `SKILL.md` files:



```text  theme={null}

my-plugin/

├── .claude-plugin/

│   └── plugin.json

└── skills/

&#x20;   └── code-review/

&#x20;       └── SKILL.md

```



Each `SKILL.md` needs frontmatter with `name` and `description` fields, followed by instructions:



```yaml  theme={null}

\---

name: code-review

description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.

\---



When reviewing code, check for:

1\. Code organization and structure

2\. Error handling

3\. Security concerns

4\. Test coverage

```



After installing the plugin, run `/reload-plugins` to load the Skills. For complete Skill authoring guidance including progressive disclosure and tool restrictions, see \[Agent Skills](/en/skills).



\### Add LSP servers to your plugin



<Tip>

&#x20; For common languages like TypeScript, Python, and Rust, install the pre-built LSP plugins from the official marketplace. Create custom LSP plugins only when you need support for languages not already covered.

</Tip>



LSP (Language Server Protocol) plugins give Claude real-time code intelligence. If you need to support a language that doesn't have an official LSP plugin, you can create your own by adding an `.lsp.json` file to your plugin:



```json .lsp.json theme={null}

{

&#x20; "go": {

&#x20;   "command": "gopls",

&#x20;   "args": \["serve"],

&#x20;   "extensionToLanguage": {

&#x20;     ".go": "go"

&#x20;   }

&#x20; }

}

```



Users installing your plugin must have the language server binary installed on their machine.



For complete LSP configuration options, see \[LSP servers](/en/plugins-reference#lsp-servers).



\### Ship default settings with your plugin



Plugins can include a `settings.json` file at the plugin root to apply default configuration when the plugin is enabled. Currently, only the `agent` key is supported.



Setting `agent` activates one of the plugin's \[custom agents](/en/sub-agents) as the main thread, applying its system prompt, tool restrictions, and model. This lets a plugin change how Claude Code behaves by default when enabled.



```json settings.json theme={null}

{

&#x20; "agent": "security-reviewer"

}

```



This example activates the `security-reviewer` agent defined in the plugin's `agents/` directory. Settings from `settings.json` take priority over `settings` declared in `plugin.json`. Unknown keys are silently ignored.



\### Organize complex plugins



For plugins with many components, organize your directory structure by functionality. For complete directory layouts and organization patterns, see \[Plugin directory structure](/en/plugins-reference#plugin-directory-structure).



\### Test your plugins locally



Use the `--plugin-dir` flag to test plugins during development. This loads your plugin directly without requiring installation.



```bash  theme={null}

claude --plugin-dir ./my-plugin

```



As you make changes to your plugin, run `/reload-plugins` to pick up the updates without restarting. Changes to LSP server configuration still require a full restart. Test your plugin components:



\* Try your skills with `/plugin-name:skill-name`

\* Check that agents appear in `/agents`

\* Verify hooks work as expected



<Tip>

&#x20; You can load multiple plugins at once by specifying the flag multiple times:



&#x20; ```bash  theme={null}

&#x20; claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two

&#x20; ```

</Tip>



\### Debug plugin issues



If your plugin isn't working as expected:



1\. \*\*Check the structure\*\*: Ensure your directories are at the plugin root, not inside `.claude-plugin/`

2\. \*\*Test components individually\*\*: Check each command, agent, and hook separately

3\. \*\*Use validation and debugging tools\*\*: See \[Debugging and development tools](/en/plugins-reference#debugging-and-development-tools) for CLI commands and troubleshooting techniques



\### Share your plugins



When your plugin is ready to share:



1\. \*\*Add documentation\*\*: Include a `README.md` with installation and usage instructions

2\. \*\*Version your plugin\*\*: Use \[semantic versioning](/en/plugins-reference#version-management) in your `plugin.json`

3\. \*\*Create or use a marketplace\*\*: Distribute through \[plugin marketplaces](/en/plugin-marketplaces) for installation

4\. \*\*Test with others\*\*: Have team members test the plugin before wider distribution



Once your plugin is in a marketplace, others can install it using the instructions in \[Discover and install plugins](/en/discover-plugins).



\### Submit your plugin to the official marketplace



To submit a plugin to the official Anthropic marketplace, use one of the in-app submission forms:



\* \*\*Claude.ai\*\*: \[claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)

\* \*\*Console\*\*: \[platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)



<Note>

&#x20; For complete technical specifications, debugging techniques, and distribution strategies, see \[Plugins reference](/en/plugins-reference).

</Note>



\## Convert existing configurations to plugins



If you already have skills or hooks in your `.claude/` directory, you can convert them into a plugin for easier sharing and distribution.



\### Migration steps



<Steps>

&#x20; <Step title="Create the plugin structure">

&#x20;   Create a new plugin directory:



&#x20;   ```bash  theme={null}

&#x20;   mkdir -p my-plugin/.claude-plugin

&#x20;   ```



&#x20;   Create the manifest file at `my-plugin/.claude-plugin/plugin.json`:



&#x20;   ```json my-plugin/.claude-plugin/plugin.json theme={null}

&#x20;   {

&#x20;     "name": "my-plugin",

&#x20;     "description": "Migrated from standalone configuration",

&#x20;     "version": "1.0.0"

&#x20;   }

&#x20;   ```

&#x20; </Step>



&#x20; <Step title="Copy your existing files">

&#x20;   Copy your existing configurations to the plugin directory:



&#x20;   ```bash  theme={null}

&#x20;   # Copy commands

&#x20;   cp -r .claude/commands my-plugin/



&#x20;   # Copy agents (if any)

&#x20;   cp -r .claude/agents my-plugin/



&#x20;   # Copy skills (if any)

&#x20;   cp -r .claude/skills my-plugin/

&#x20;   ```

&#x20; </Step>



&#x20; <Step title="Migrate hooks">

&#x20;   If you have hooks in your settings, create a hooks directory:



&#x20;   ```bash  theme={null}

&#x20;   mkdir my-plugin/hooks

&#x20;   ```



&#x20;   Create `my-plugin/hooks/hooks.json` with your hooks configuration. Copy the `hooks` object from your `.claude/settings.json` or `settings.local.json`, since the format is the same. The command receives hook input as JSON on stdin, so use `jq` to extract the file path:



&#x20;   ```json my-plugin/hooks/hooks.json theme={null}

&#x20;   {

&#x20;     "hooks": {

&#x20;       "PostToolUse": \[

&#x20;         {

&#x20;           "matcher": "Write|Edit",

&#x20;           "hooks": \[{ "type": "command", "command": "jq -r '.tool\_input.file\_path' | xargs npm run lint:fix" }]

&#x20;         }

&#x20;       ]

&#x20;     }

&#x20;   }

&#x20;   ```

&#x20; </Step>



&#x20; <Step title="Test your migrated plugin">

&#x20;   Load your plugin to verify everything works:



&#x20;   ```bash  theme={null}

&#x20;   claude --plugin-dir ./my-plugin

&#x20;   ```



&#x20;   Test each component: run your commands, check agents appear in `/agents`, and verify hooks trigger correctly.

&#x20; </Step>

</Steps>



\### What changes when migrating



| Standalone (`.claude/`)       | Plugin                           |

| :---------------------------- | :------------------------------- |

| Only available in one project | Can be shared via marketplaces   |

| Files in `.claude/commands/`  | Files in `plugin-name/commands/` |

| Hooks in `settings.json`      | Hooks in `hooks/hooks.json`      |

| Must manually copy to share   | Install with `/plugin install`   |



<Note>

&#x20; After migrating, you can remove the original files from `.claude/` to avoid duplicates. The plugin version will take precedence when loaded.

</Note>



\## Next steps



Now that you understand Claude Code's plugin system, here are suggested paths for different goals:



\### For plugin users



\* \[Discover and install plugins](/en/discover-plugins): browse marketplaces and install plugins

\* \[Configure team marketplaces](/en/discover-plugins#configure-team-marketplaces): set up repository-level plugins for your team



\### For plugin developers



\* \[Create and distribute a marketplace](/en/plugin-marketplaces): package and share your plugins

\* \[Plugins reference](/en/plugins-reference): complete technical specifications

\* Dive deeper into specific plugin components:

&#x20; \* \[Skills](/en/skills): skill development details

&#x20; \* \[Subagents](/en/sub-agents): agent configuration and capabilities

&#x20; \* \[Hooks](/en/hooks): event handling and automation

&#x20; \* \[MCP](/en/mcp): external tool integration



