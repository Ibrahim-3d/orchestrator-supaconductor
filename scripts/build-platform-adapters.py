#!/usr/bin/env python3
"""Build native SupaConductor packages for non-Claude coding-agent hosts.

Canonical source remains this repository's skills/, commands/, and agents/ trees.
Adapters are generated so platform copies cannot drift from the Claude Code plugin.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def strip_frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return text.strip()
    end = text.find("\n---", 4)
    if end < 0:
        return text.strip()
    return text[end + 4 :].lstrip("\n").strip()


def read_meta(text: str, fallback_name: str) -> tuple[str, str]:
    name = fallback_name
    description = f"Run the SupaConductor {fallback_name} workflow."
    if not text.startswith("---\n"):
        return name, description
    end = text.find("\n---", 4)
    if end < 0:
        return name, description
    front = text[4:end]
    m = re.search(r"(?m)^name:\s*[\"']?([^\n\"']+)", front)
    if m:
        name = m.group(1).strip()
    m = re.search(r"(?m)^description:\s*[\"']?([^\n\"']+)", front)
    if m and m.group(1).strip() not in {"|", ">"}:
        description = m.group(1).strip().rstrip("\"'")
    return name, description


def portable_body(text: str) -> str:
    body = strip_frontmatter(text)
    replacements = {
        "read_file": "read the file",
        "write_file": "write the file",
        "grep_search": "search the workspace",
        "run_shell_command": "run a shell command",
        "google_web_search": "search the web",
        "web_fetch": "fetch the web page",
        "Task calls": "subagent invocations",
        "Task call": "subagent invocation",
        "Task(": "delegate(",
    }
    for old, new in replacements.items():
        body = body.replace(old, new)
    body = body.replace("the conductor-orchestrator agent", "the `conductor-orchestrator` skill or equivalent orchestrator")
    return body


def command_skill(command_path: Path) -> str:
    raw = command_path.read_text(encoding="utf-8")
    name, description = read_meta(raw, command_path.stem)
    body = portable_body(raw)
    fallback = ""
    agent_path = ROOT / "agents" / f"{name}.md"
    if agent_path.exists():
        fallback = (
            "\n\n## Inline fallback when this host cannot invoke a named subagent\n\n"
            "Execute the following role instructions in the current agent context while preserving the command's scope:\n\n"
            + portable_body(agent_path.read_text(encoding="utf-8"))
        )
    safe_desc = description.replace("\"", "'")[:500]
    return f'''---\nname: supaconductor-command-{name}\ndescription: "{safe_desc}"\n---\n\n# SupaConductor command: /{name}\n\nThis skill is the portable equivalent of Claude Code's `/orchestrator-supaconductor:{name}` command. Treat the user's text after the skill/command name as `$ARGUMENTS`. Follow the protocol below as authoritative.\n\n{body}{fallback}\n'''


def normalized_cursor_file(source: Path) -> str:
    raw = source.read_text(encoding="utf-8")
    name, description = read_meta(raw, source.stem)
    safe_desc = description.replace("\"", "'")[:500]
    return f'''---\nname: {name}\ndescription: "{safe_desc}"\n---\n\n{portable_body(raw)}\n'''


def antigravity_tools(raw: str) -> list[str]:
    tools: list[str] = []
    mapping = [
        (("read_file",), "view_file"),
        (("write_file", "replace"), "replace_file_content"),
        (("grep_search", "glob"), "grep_search"),
        (("run_shell_command",), "run_command"),
        (("Task",), "invoke_subagent"),
    ]
    for needles, tool in mapping:
        if any(n in raw for n in needles) and tool not in tools:
            tools.append(tool)
    return tools or ["view_file", "grep_search"]


def normalized_antigravity_agent(source: Path) -> str:
    raw = source.read_text(encoding="utf-8")
    name, description = read_meta(raw, source.stem)
    safe_desc = description.replace("\"", "'")[:500]
    tool_lines = "\n".join(f"  - {tool}" for tool in antigravity_tools(raw))
    body = portable_body(raw).replace("delegate(", "invoke_subagent(")
    return f'''---\nname: {name}\ndescription: "{safe_desc}"\ntools:\n{tool_lines}\nmainAgent: false\nsubagent: true\nmodel: inherit\ncommandExecutionPolicy: sandbox\n---\n\n{body}\n'''


def copy_canonical_skills(dst: Path) -> None:
    shutil.copytree(ROOT / "skills", dst / "skills", dirs_exist_ok=True)
    for command in sorted((ROOT / "commands").glob("*.md")):
        skill_dir = dst / "skills" / f"supaconductor-command-{command.stem}"
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(command_skill(command), encoding="utf-8")


def build_codex(base: Path) -> None:
    dst = base / "codex" / "orchestrator-supaconductor"
    dst.mkdir(parents=True, exist_ok=True)
    copy_canonical_skills(dst)
    shutil.copy2(ROOT / "plugin.json", dst / "plugin.json")
    codex_dir = dst / ".codex-plugin"
    codex_dir.mkdir(exist_ok=True)
    shutil.copy2(ROOT / ".codex-plugin" / "plugin.json", codex_dir / "plugin.json")
    shutil.copytree(ROOT / "assets", dst / "assets", dirs_exist_ok=True)


def build_cursor(base: Path) -> None:
    dst = base / "cursor" / "orchestrator-supaconductor"
    dst.mkdir(parents=True, exist_ok=True)
    copy_canonical_skills(dst)
    (dst / "commands").mkdir(exist_ok=True)
    for path in sorted((ROOT / "commands").glob("*.md")):
        (dst / "commands" / path.name).write_text(normalized_cursor_file(path), encoding="utf-8")
    (dst / "agents").mkdir(exist_ok=True)
    for path in sorted((ROOT / "agents").glob("*.md")):
        (dst / "agents" / path.name).write_text(normalized_cursor_file(path), encoding="utf-8")
    manifest_dir = dst / ".cursor-plugin"
    manifest_dir.mkdir(exist_ok=True)
    version = json.loads((ROOT / "plugin.json").read_text(encoding="utf-8"))["version"]
    manifest = {
        "name": "orchestrator-supaconductor",
        "version": version,
        "description": "SupaConductor multi-agent engineering orchestration for Cursor.",
        "author": {"name": "Ibrahim"},
        "homepage": "https://github.com/Ibrahim-3d/orchestrator-supaconductor",
        "repository": "https://github.com/Ibrahim-3d/orchestrator-supaconductor",
        "license": "AGPL-3.0",
        "keywords": ["orchestration", "multi-agent", "planning", "evaluation", "tdd"],
        "skills": "skills",
        "agents": "agents",
        "commands": "commands",
    }
    (manifest_dir / "plugin.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def build_antigravity(base: Path) -> None:
    dst = base / "antigravity" / "orchestrator-supaconductor"
    dst.mkdir(parents=True, exist_ok=True)
    copy_canonical_skills(dst)
    (dst / "agents").mkdir(exist_ok=True)
    for path in sorted((ROOT / "agents").glob("*.md")):
        (dst / "agents" / path.name).write_text(normalized_antigravity_agent(path), encoding="utf-8")
    manifest = {
        "$schema": "https://antigravity.google/schemas/v1/plugin.json",
        "name": "orchestrator-supaconductor",
        "description": "SupaConductor multi-agent engineering orchestration with skills and custom subagents.",
    }
    (dst / "plugin.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def build_copilot(base: Path) -> None:
    dst = base / "copilot" / "orchestrator-supaconductor"
    skill_root = dst / ".github"
    copy_canonical_skills(skill_root)
    prompt_dir = dst / ".github" / "prompts"
    prompt_dir.mkdir(parents=True, exist_ok=True)
    for command in sorted((ROOT / "commands").glob("*.md")):
        (prompt_dir / f"{command.stem}.prompt.md").write_text(command_skill(command), encoding="utf-8")
    agent_dir = dst / ".github" / "agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    for path in sorted((ROOT / "agents").glob("*.md")):
        (agent_dir / path.name).write_text(normalized_cursor_file(path), encoding="utf-8")


def build_windsurf(base: Path) -> None:
    dst = base / "windsurf" / "orchestrator-supaconductor"
    skill_root = dst / ".windsurf"
    copy_canonical_skills(skill_root)
    workflow_dir = skill_root / "workflows"
    workflow_dir.mkdir(parents=True, exist_ok=True)
    for command in sorted((ROOT / "commands").glob("*.md")):
        raw = command.read_text(encoding="utf-8")
        name, description = read_meta(raw, command.stem)
        safe_desc = description.replace("\"", "'")[:500]
        workflow = f'''---\ndescription: "{safe_desc}"\n---\n\n# SupaConductor /{name}\n\nInvoke the `supaconductor-command-{name}` Agent Skill and follow it as the authoritative workflow. Treat text after `/{name}` as the workflow arguments. If automatic skill loading does not occur, read `.windsurf/skills/supaconductor-command-{name}/SKILL.md` and follow it directly.\n'''
        (workflow_dir / f"{name}.md").write_text(workflow, encoding="utf-8")


def validate_build(base: Path) -> None:
    source_commands = len(list((ROOT / "commands").glob("*.md")))
    source_agents = len(list((ROOT / "agents").glob("*.md")))
    source_skills = len(list((ROOT / "skills").rglob("SKILL.md")))

    checks = {
        "codex command skills": len(list((base / "codex/orchestrator-supaconductor/skills").glob("supaconductor-command-*/SKILL.md"))),
        "cursor commands": len(list((base / "cursor/orchestrator-supaconductor/commands").glob("*.md"))),
        "cursor agents": len(list((base / "cursor/orchestrator-supaconductor/agents").glob("*.md"))),
        "antigravity agents": len(list((base / "antigravity/orchestrator-supaconductor/agents").glob("*.md"))),
        "windsurf workflows": len(list((base / "windsurf/orchestrator-supaconductor/.windsurf/workflows").glob("*.md"))),
        "copilot prompts": len(list((base / "copilot/orchestrator-supaconductor/.github/prompts").glob("*.prompt.md"))),
        "copilot agents": len(list((base / "copilot/orchestrator-supaconductor/.github/agents").glob("*.md"))),
    }
    expected = {
        "codex command skills": source_commands,
        "cursor commands": source_commands,
        "cursor agents": source_agents,
        "antigravity agents": source_agents,
        "windsurf workflows": source_commands,
        "copilot prompts": source_commands,
        "copilot agents": source_agents,
    }
    problems = [f"{k}: expected {expected[k]}, got {v}" for k, v in checks.items() if v != expected[k]]
    for platform in ("codex", "cursor", "antigravity", "windsurf", "copilot"):
        root = base / platform / "orchestrator-supaconductor"
        if not root.exists():
            problems.append(f"missing package: {platform}")
    if source_skills < 1:
        problems.append("no canonical Agent Skills found")
    if problems:
        raise SystemExit("Adapter validation failed:\n - " + "\n - ".join(problems))
    print(f"Platform adapters validated: {source_commands} commands, {source_agents} agents, {source_skills} canonical skills")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "platforms")
    parser.add_argument("--check", action="store_true", help="build in a temp directory and validate without keeping artifacts")
    args = parser.parse_args()

    if args.check:
        with tempfile.TemporaryDirectory(prefix="supaconductor-adapters-") as tmp:
            base = Path(tmp)
            build_codex(base)
            build_cursor(base)
            build_antigravity(base)
            build_windsurf(base)
            build_copilot(base)
            validate_build(base)
        return

    base = args.output.resolve()
    if base.exists():
        shutil.rmtree(base)
    base.mkdir(parents=True, exist_ok=True)
    build_codex(base)
    build_cursor(base)
    build_antigravity(base)
    build_windsurf(base)
    build_copilot(base)
    validate_build(base)
    print(f"Built platform adapters at {base}")


if __name__ == "__main__":
    main()
