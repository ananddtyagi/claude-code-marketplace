#!/bin/bash
#
# Hook: Session Lock Awareness (SessionStart)
# Purpose: Inform Claude about existing task locks at session start
# This helps prevent suggesting tasks that are already being worked on
#

set -euo pipefail

LOCKS_DIR="${CLAUDE_PROJECT_DIR}/.claude/locks"
MASTER_PLAN="${CLAUDE_PROJECT_DIR}/docs/MASTER_PLAN.md"
LOCK_EXPIRY_HOURS=4

# Ensure locks directory exists
mkdir -p "$LOCKS_DIR"

# Read JSON input
INPUT=$(cat)
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // ""')

# Clean up stale locks
current_time=$(date +%s)
expiry_seconds=$((LOCK_EXPIRY_HOURS * 3600))

while IFS= read -r -d '' lock_file; do
  if [[ -f "$lock_file" ]]; then
    lock_time=$(jq -r '.timestamp // 0' "$lock_file" 2>/dev/null || echo "0")
    age=$((current_time - lock_time))
    if [[ $age -gt $expiry_seconds ]]; then
      rm -f "$lock_file"
    fi
  fi
done < <(find "$LOCKS_DIR" -maxdepth 1 -name "*.lock" -print0 2>/dev/null)

# Check for active locks from other sessions
ACTIVE_LOCKS=""
while IFS= read -r -d '' lock_file; do
  if [[ -f "$lock_file" ]]; then
    locked_session=$(jq -r '.session_id // ""' "$lock_file" 2>/dev/null || echo "")
    task_id=$(jq -r '.task_id // ""' "$lock_file" 2>/dev/null || echo "")
    locked_at=$(jq -r '.locked_at // "unknown"' "$lock_file" 2>/dev/null || echo "unknown")

    if [[ -n "$locked_session" ]] && [[ "$locked_session" != "$SESSION_ID" ]]; then
      ACTIVE_LOCKS="${ACTIVE_LOCKS}  - $task_id (locked at $locked_at by session ${locked_session:0:8}...)\n"
    fi
  fi
done < <(find "$LOCKS_DIR" -maxdepth 1 -name "*.lock" -print0 2>/dev/null)

if [[ -n "$ACTIVE_LOCKS" ]]; then
  cat << EOF
ACTIVE TASK LOCKS DETECTED:
The following tasks are currently being worked on by other Claude Code sessions:
$(echo -e "$ACTIVE_LOCKS")
IMPORTANT: Do NOT suggest or start work on these tasks. They will be blocked.
Check docs/MASTER_PLAN.md for alternative tasks without conflicts.
EOF
else
  echo "TASK LOCKS: No active locks from other sessions. All tasks available."
fi

exit 0
