#!/bin/bash
#
# Hook: Session Lock Release (SessionEnd)
# Purpose: Release all task locks held by this session when it ends
# This ensures locks don't persist after a session closes
#

set -euo pipefail

LOCKS_DIR="${CLAUDE_PROJECT_DIR}/.claude/locks"

# Ensure locks directory exists
mkdir -p "$LOCKS_DIR"

# Read JSON input
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""')

if [[ -z "$SESSION_ID" ]]; then
  exit 0
fi

# Release all locks owned by this session
RELEASED=""
while IFS= read -r -d '' lock_file; do
  if [[ -f "$lock_file" ]]; then
    locked_session=$(jq -r '.session_id // ""' "$lock_file" 2>/dev/null || echo "")
    task_id=$(jq -r '.task_id // ""' "$lock_file" 2>/dev/null || echo "")

    if [[ "$locked_session" == "$SESSION_ID" ]]; then
      rm -f "$lock_file"
      RELEASED="${RELEASED}$task_id "
    fi
  fi
done < <(find "$LOCKS_DIR" -maxdepth 1 -name "*.lock" -print0 2>/dev/null)

if [[ -n "$RELEASED" ]]; then
  echo "LOCKS RELEASED: $RELEASED"
fi

exit 0
