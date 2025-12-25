#!/bin/bash
# Remind Claude to update MASTER_PLAN.md when starting tasks

cat << 'EOF'
<user-prompt-submit-hook>
REMINDER: When starting work on any task, feature, or bug fix:
1. Check docs/MASTER_PLAN.md for existing tracking
2. Add a new entry with proper ID (TASK-XXX, BUG-XXX, etc.) if not tracked
3. Update status of existing items as work progresses
4. Mark items complete when finished
</user-prompt-submit-hook>
EOF
