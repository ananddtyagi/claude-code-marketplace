#!/bin/bash
# Conditional hook: Only triggers when user asks about disappearing tasks

# Read user prompt from stdin
USER_PROMPT=$(cat)

# Check if prompt mentions disappearing/missing tasks (case insensitive)
if echo "$USER_PROMPT" | grep -iE "(task|tasks).*(disappear|missing|gone|vanish|lost)|where.*(task|tasks).*go|(disappear|missing|gone|vanish|lost).*(task|tasks)" > /dev/null 2>&1; then
    cat << 'EOF'
<user-prompt-submit-hook>
TASK DISAPPEARANCE DEBUGGING:

A logger exists at `src/utils/taskDisappearanceLogger.ts` to track this issue.

Quick commands (run in browser console):
- `window.taskLogger.getDisappearedTasks()` - Check if any tasks disappeared
- `window.taskLogger.printSummary()` - See logging summary
- `window.taskLogger.exportLogs()` - Export for analysis

The logger is currently auto-enabled on app startup.

For full instructions, use the `dev-debug-data-loss` skill.
Related: BUG-020, TASK-022, TASK-024
</user-prompt-submit-hook>
EOF
fi
