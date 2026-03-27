#!/usr/bin/env bash
# SessionStart hook for SupaConductor plugin

set -euo pipefail

# Determine plugin root directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PLUGIN_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# ── Version detection ────────────────────────────────────────────────
# Read current version from plugin.json
LOCAL_VERSION=""
PLUGIN_JSON="${PLUGIN_ROOT}/.claude-plugin/plugin.json"
if [ -f "$PLUGIN_JSON" ]; then
    # Extract version using lightweight parsing (no jq dependency)
    LOCAL_VERSION=$(sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$PLUGIN_JSON" | head -1)
fi
LOCAL_VERSION="${LOCAL_VERSION:-unknown}"

# Check for latest release on GitHub (non-blocking, 3s timeout)
REPO="Ibrahim-3d/orchestrator-supaconductor"
update_message=""
if command -v curl &>/dev/null; then
    latest_tag=$(curl -s --max-time 3 \
        "https://api.github.com/repos/${REPO}/releases/latest" 2>/dev/null \
        | sed -n 's/.*"tag_name"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' \
        | sed 's/^v//' | head -1) || true

    if [ -n "$latest_tag" ] && [ "$latest_tag" != "$LOCAL_VERSION" ]; then
        update_message="\\n\\n**UPDATE AVAILABLE:** SupaConductor v${latest_tag} is available (you have v${LOCAL_VERSION}). Tell the user: A new version of SupaConductor is available (v${latest_tag}). Update with: claude plugin update orchestrator-supaconductor"
    fi
fi

# ── Legacy skills directory check ────────────────────────────────────
warning_message=""
legacy_skills_dir="${HOME}/.config/supaconductor/skills"
if [ -d "$legacy_skills_dir" ]; then
    warning_message="\n\n<important-reminder>IN YOUR FIRST REPLY AFTER SEEING THIS MESSAGE YOU MUST TELL THE USER:⚠️ **WARNING:** SupaConductor now uses Claude Code's skills system. Custom skills in ~/.config/supaconductor/skills will not be read. Move custom skills to ~/.claude/skills instead. To make this message go away, remove ~/.config/supaconductor/skills</important-reminder>"
fi

# Read using-supaconductor content
using_supaconductor_content=$(cat "${PLUGIN_ROOT}/skills/using-supaconductor/SKILL.md" 2>&1 || echo "Error reading using-supaconductor skill")

# Escape string for JSON embedding using bash parameter substitution.
# Each ${s//old/new} is a single C-level pass - orders of magnitude
# faster than the character-by-character loop this replaces.
escape_for_json() {
    local s="$1"
    s="${s//\\/\\\\}"
    s="${s//\"/\\\"}"
    s="${s//$'\n'/\\n}"
    s="${s//$'\r'/\\r}"
    s="${s//$'\t'/\\t}"
    printf '%s' "$s"
}

using_supaconductor_escaped=$(escape_for_json "$using_supaconductor_content")
warning_escaped=$(escape_for_json "$warning_message")
update_escaped=$(escape_for_json "$update_message")

# Output context injection as JSON
cat <<EOF
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "<EXTREMELY_IMPORTANT>\nYou have SupaConductor v${LOCAL_VERSION}.\n\n**Below is the full content of your 'orchestrator-supaconductor:using-supaconductor' skill - your introduction to using skills. For all other skills, use the 'Skill' tool:**\n\n${using_supaconductor_escaped}\n\n${warning_escaped}${update_escaped}\n</EXTREMELY_IMPORTANT>"
  }
}
EOF

exit 0
