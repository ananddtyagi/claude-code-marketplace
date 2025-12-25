#!/bin/bash
#
# Hook: Auto-sync Task Status in MASTER_PLAN.md
# Triggers on Edit/Write to source files
# Matches edited files against Task Dependency Index and updates status
#

set -euo pipefail

MASTER_PLAN="$CLAUDE_PROJECT_DIR/docs/MASTER_PLAN.md"

# Read JSON input from stdin
INPUT=$(cat)

# Extract file path from tool input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // ""')

# Skip if no file path or if editing MASTER_PLAN.md itself (avoid loops)
if [[ -z "$FILE_PATH" ]] || [[ "$FILE_PATH" == *"MASTER_PLAN.md" ]]; then
  exit 0
fi

# Skip non-source files (configs, tests, etc. that don't indicate active work)
if [[ "$FILE_PATH" == *".json" ]] || [[ "$FILE_PATH" == *".md" ]] || [[ "$FILE_PATH" == *".sh" ]]; then
  exit 0
fi

# Get just the filename for matching
FILENAME=$(basename "$FILE_PATH")

# Check if MASTER_PLAN.md exists
if [[ ! -f "$MASTER_PLAN" ]]; then
  exit 0
fi

# Extract Task Dependency Index section and find matching task
# Format: | TASK-XXX | Status | Primary Files | ...
MATCHING_TASK=""
CURRENT_STATUS=""

while IFS= read -r line; do
  # Skip non-table rows and header rows
  if [[ ! "$line" =~ ^\|.*TASK-[0-9]+ ]]; then
    continue
  fi

  # Extract task ID (handle strikethrough)
  TASK_ID=$(echo "$line" | grep -oE '(~~)?TASK-[0-9]+(~~)?' | head -1 | tr -d '~')

  # Skip done tasks (strikethrough)
  if [[ "$line" =~ ~~TASK-[0-9]+~~ ]]; then
    continue
  fi

  # Extract primary files column (3rd column)
  PRIMARY_FILES=$(echo "$line" | cut -d'|' -f4 | tr -d '`' | xargs)

  # Extract current status (2nd column after ID)
  CURRENT_STATUS=$(echo "$line" | cut -d'|' -f3 | xargs)

  # Check if edited file matches any pattern in Primary Files
  # Handle patterns like: tasks.ts, *.stories.ts, src/stores/*.ts
  for pattern in $(echo "$PRIMARY_FILES" | tr ',' ' '); do
    pattern=$(echo "$pattern" | xargs)  # trim

    # Direct filename match
    if [[ "$FILENAME" == "$pattern" ]]; then
      MATCHING_TASK="$TASK_ID"
      break 2
    fi

    # Glob pattern match (e.g., *.stories.ts)
    if [[ "$pattern" == *"*"* ]]; then
      # Convert glob to regex
      REGEX=$(echo "$pattern" | sed 's/\./\\./g' | sed 's/\*/.*/g')
      if echo "$FILENAME" | grep -qE "^$REGEX$"; then
        MATCHING_TASK="$TASK_ID"
        break 2
      fi
      # Also check full path
      if echo "$FILE_PATH" | grep -qE "$REGEX"; then
        MATCHING_TASK="$TASK_ID"
        break 2
      fi
    fi
  done
done < "$MASTER_PLAN"

# If no matching task found, exit silently
if [[ -z "$MATCHING_TASK" ]]; then
  exit 0
fi

# If task is already IN_PROGRESS, DONE, or special status (MONITORING), no update needed
if [[ "$CURRENT_STATUS" == "IN_PROGRESS" ]] || [[ "$CURRENT_STATUS" == *"DONE"* ]] || [[ "$CURRENT_STATUS" == *"✅"* ]] || [[ "$CURRENT_STATUS" == *"MONITORING"* ]] || [[ "$CURRENT_STATUS" == *"👀"* ]]; then
  exit 0
fi

# Update the task status to IN_PROGRESS
# Use sed to update the status column for this specific task
sed -i "s/| $MATCHING_TASK | [^|]* |/| $MATCHING_TASK | IN_PROGRESS |/" "$MASTER_PLAN"

# Output context message
cat << EOF
{
  "additionalContext": "AUTO-SYNC: Updated $MATCHING_TASK status to IN_PROGRESS (editing $FILENAME)"
}
EOF

exit 0
