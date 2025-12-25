#!/bin/bash
# Hook: Check for existing npm scripts before using manual serve commands

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command being executed
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // ""')

# Only check for serve-like commands
if ! echo "$COMMAND" | grep -qE "(npx serve|python.*http\.server)"; then
  exit 0
fi

# Check if package.json exists
PKG_JSON="${CLAUDE_PROJECT_DIR}/package.json"
if [[ ! -f "$PKG_JSON" ]]; then
  exit 0
fi

# Find scripts that might be related (contain 'serve' or related ports)
SCRIPTS=$(grep -E '"[^"]+": *".*serve|:60[0-9]{2}|:55[0-9]{2}' "$PKG_JSON" 2>/dev/null | head -5)

if [[ -n "$SCRIPTS" ]]; then
  echo "CHECK PACKAGE.JSON FIRST: Found existing serve-related scripts:"
  echo "$SCRIPTS" | sed 's/^/  /'
  echo "Use 'npm run <script>' instead of manual npx serve commands."
fi

exit 0
