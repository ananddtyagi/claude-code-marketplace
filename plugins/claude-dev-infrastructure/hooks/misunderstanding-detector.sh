#!/bin/bash
# Detect when user indicates Claude misunderstood and force clarification

# Read the user's message from stdin
USER_MESSAGE=$(cat)

# Check for misunderstanding patterns (case-insensitive)
if echo "$USER_MESSAGE" | grep -qiE "(you (didn.?t|don.?t) understand|that.?s not what I (meant|asked)|misunderstood|no,? I (meant|said)|wrong|incorrect|not what I (wanted|asked|meant)|try again|let me clarify|I said|you missed|you got it wrong)"; then
  cat << 'EOF'
<user-prompt-submit-hook>
MISUNDERSTANDING DETECTED - MANDATORY CLARIFICATION REQUIRED

The user has indicated you may have misunderstood their request.
You MUST:
1. Use the AskUserQuestion tool IMMEDIATELY to clarify what the user actually wants
2. DO NOT proceed with any implementation until clarification is received
3. DO NOT apologize extensively - focus on asking specific clarifying questions
4. Present 2-4 options that might match what the user intended
5. Include an "Other" option so user can explain in their own words

Example clarification:
- "What specific aspect did I misunderstand?"
- "Which of these interpretations matches your intent?"
- "What should I focus on instead?"
</user-prompt-submit-hook>
EOF
fi
