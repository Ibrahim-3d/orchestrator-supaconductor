#!/usr/bin/env python3
"""Repository-level consistency checks for SupaConductor."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def load_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{path.relative_to(ROOT)}: invalid JSON: {exc}")
        return None


# All committed JSON should parse.
for path in ROOT.rglob("*.json"):
    if ".git" not in path.parts:
        load_json(path)

plugin = load_json(ROOT / ".claude-plugin" / "plugin.json") or {}
portable_plugin = load_json(ROOT / "plugin.json") or {}
codex_plugin = load_json(ROOT / ".codex-plugin" / "plugin.json") or {}
marketplace = load_json(ROOT / ".claude-plugin" / "marketplace.json") or {}
manifest = load_json(ROOT / ".release-please-manifest.json") or {}

plugin_entry = next(
    (p for p in marketplace.get("plugins", []) if p.get("name") == "orchestrator-supaconductor"),
    {},
)

expected_license = "AGPL-3.0"
for name, value in {
    "Claude plugin.json": plugin.get("license"),
    "portable plugin.json": portable_plugin.get("license"),
    "marketplace plugin": plugin_entry.get("license"),
}.items():
    if value != expected_license:
        fail(f"{name}: license must be {expected_license!r}, found {value!r}")

versions = {
    "Claude plugin.json": plugin.get("version"),
    "portable plugin.json": portable_plugin.get("version"),
    "Codex overlay": codex_plugin.get("version"),
    "marketplace root": marketplace.get("version"),
    "marketplace plugin": plugin_entry.get("version"),
    "release manifest": manifest.get("."),
}
if None in versions.values() or len(set(versions.values())) != 1:
    fail("version mismatch: " + ", ".join(f"{k}={v!r}" for k, v in versions.items()))


def frontmatter(path: Path, require_description: bool) -> None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail(f"{path.relative_to(ROOT)}: missing YAML frontmatter")
        return
    end = text.find("\n---", 4)
    if end < 0:
        fail(f"{path.relative_to(ROOT)}: unterminated YAML frontmatter")
        return
    meta = text[4:end]
    if not re.search(r"(?m)^name:\s*\S", meta):
        fail(f"{path.relative_to(ROOT)}: missing frontmatter name")
    if require_description and not re.search(r"(?m)^description:\s*\S", meta):
        fail(f"{path.relative_to(ROOT)}: missing frontmatter description")


for path in sorted((ROOT / "skills").rglob("SKILL.md")):
    frontmatter(path, require_description=True)

for directory in ("agents", "commands"):
    for path in sorted((ROOT / directory).rglob("*.md")):
        frontmatter(path, require_description=False)

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for stale in (
    "license-MIT",
    "MIT — see [LICENSE]",
    "blob/main/LICENSE",
    "/install Ibrahim-3d/orchestrator-supaconductor",
):
    if stale in readme:
        fail(f"README.md: stale public metadata/instruction found: {stale!r}")

if portable_plugin.get("$schema") != "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json":
    fail("plugin.json: missing or invalid Agent Plugins schema")

for required_path in (
    ROOT / ".codex-plugin" / "plugin.json",
    ROOT / "docs" / "platform-support.md",
    ROOT / "scripts" / "build-platform-adapters.py",
):
    if not required_path.exists():
        fail(f"missing cross-platform integration file: {required_path.relative_to(ROOT)}")

required_readme_links = ("ROADMAP.md", "CONTRIBUTING.md", "SUPPORT.md", "docs/platform-support.md")
for link in required_readme_links:
    if link not in readme:
        fail(f"README.md: missing public navigation link to {link}")

if errors:
    print("Repository validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)

print(f"Repository validation passed. Version: {plugin.get('version')}; license: {expected_license}")
