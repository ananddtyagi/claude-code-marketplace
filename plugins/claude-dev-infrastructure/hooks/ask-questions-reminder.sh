#!/bin/bash
# Remind Claude to use AskUserQuestion tool instead of inline questions

cat << 'EOF'
<user-prompt-submit-hook>
QUESTION TOOL REMINDER: When you need to ask the user a question:
1. ALWAYS use the AskUserQuestion tool - NEVER ask questions inline in your response
2. The AskUserQuestion tool provides a better UX with structured options
3. Use it for: clarifications, preferences, decisions, implementation choices
4. After asking, WAIT for user response before proceeding
</user-prompt-submit-hook>
EOF
