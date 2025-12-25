#!/bin/bash
#
# Hook: Validate MASTER_PLAN.md Task ID Format
# Triggers on Edit/Write to docs/MASTER_PLAN.md
# Ensures all task items have proper IDs (TASK-, BUG-, ROAD-, IDEA-, ISSUE-)
#

set -euo pipefail

# Read JSON input from stdin
INPUT=$(cat)

# Extract file path from tool input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

# Only validate MASTER_PLAN.md edits
if [[ "$FILE_PATH" != *"MASTER_PLAN.md" ]]; then
  exit 0
fi

# Extract the new content being written
NEW_CONTENT=$(echo "$INPUT" | jq -r '.tool_input.content // .tool_input.new_string // ""')

# If no content (e.g., reading file), skip validation
if [[ -z "$NEW_CONTENT" ]]; then
  exit 0
fi

# Define valid ID patterns
VALID_PREFIXES="TASK|BUG|ROAD|IDEA|ISSUE"

# Check for table rows that should have IDs but don't
# Look for markdown table rows in sections that should have IDs
ERRORS=""

# Check Roadmap section - tables should have ID column
if echo "$NEW_CONTENT" | grep -q "## Roadmap"; then
  # Check if Near-term table rows have IDs
  if echo "$NEW_CONTENT" | grep -E "^\| [^|]+\| [^|]+\| P[1-3]" | grep -vE "^\| ($VALID_PREFIXES)-[0-9]+" | grep -vE "^\| ~~($VALID_PREFIXES)-[0-9]+~~" | grep -vE "^\| ID " | head -1 | grep -q .; then
    ERRORS="$ERRORS\n- Roadmap table rows missing IDs (should be ROAD-XXX)"
  fi
fi

# Check Smart Group Bugs section
if echo "$NEW_CONTENT" | grep -q "### Smart Group Bugs"; then
  if echo "$NEW_CONTENT" | grep -E "^\| Bug [0-9]+" | grep -vE "^\| ($VALID_PREFIXES)-[0-9]+" | head -1 | grep -q .; then
    ERRORS="$ERRORS\n- Bug table rows should use BUG-XXX IDs, not 'Bug X:' format"
  fi
fi

# Check Known Issues section
if echo "$NEW_CONTENT" | grep -q "## Known Issues"; then
  if echo "$NEW_CONTENT" | grep -E "^\| \*\*[^|]+\*\*" | grep -vE "^\| ($VALID_PREFIXES)-[0-9]+" | grep -vE "^\| ID " | head -1 | grep -q .; then
    ERRORS="$ERRORS\n- Known Issues table rows missing IDs (should be ISSUE-XXX)"
  fi
fi

# Check Active Work section for task headers
if echo "$NEW_CONTENT" | grep -q "## Active Work"; then
  # Active work section headers should have TASK-XXX prefix
  if echo "$NEW_CONTENT" | grep -E "^### [A-Z][a-z]+" | grep -v "### TASK-" | grep -v "### Smart Group" | grep -v "### Calendar Issues" | grep -v "### Phases" | head -1 | grep -q .; then
    ERRORS="$ERRORS\n- Active Work section headers should use format: ### TASK-XXX: Title"
  fi
fi

# If errors found, output warning but don't block (exit 0 with additionalContext)
if [[ -n "$ERRORS" ]]; then
  # Output JSON with warning context
  cat << EOF
{
  "additionalContext": "WARNING: MASTER_PLAN.md format issues detected:$ERRORS\n\nPlease ensure all items have proper IDs:\n- TASK-XXX for active work\n- BUG-XXX for bugs\n- ROAD-XXX for roadmap items\n- IDEA-XXX for ideas\n- ISSUE-XXX for known issues"
}
EOF
fi

exit 0
