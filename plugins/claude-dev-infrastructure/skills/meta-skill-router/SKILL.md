# Meta Skill Router

**Purpose**: Intelligent skill routing and management system for automated skill selection and execution.

## 🧠 **Core Functionality**
- Analyze user requests and route to appropriate skills
- Maintain skill dependency relationships
- Optimize skill selection based on context
- Provide progressive disclosure for complex operations

## 🎯 **Routing Logic**
- **Pattern Recognition**: Identify intent from natural language
- **Skill Mapping**: Match requests to available skills
- **Priority Scoring**: Rank skills by relevance and success probability
- **Chain Building**: Create multi-skill execution plans

## 🔗 **Integration Features**
- Auto-discovery of new skills
- Learning system for improved routing
- Quality gates and validation
- Performance monitoring

## 📊 **Management Capabilities**
- Skill registry management
- Health monitoring and diagnostics
- Usage analytics and reporting
- Conflict resolution between skills

## 🛠️ **Tools Included**
- `router-logic.ts`: Core routing engine
- `skill-discovery.ts`: Automated skill detection
- `learning-system.ts`: Adaptive routing improvement
- `quality-gates.md`: Validation framework

## ⚡ **Execution Modes**
- **Auto**: Fully automated skill selection
- **Assisted**: User-guided skill choice
- **Manual**: Direct skill invocation
- **Batch**: Multi-skill workflow execution

## 🎭 **Triggers**
- Natural language request analysis
- Code pattern detection
- Performance issue identification
- User intent classification

---

**Usage**: Automatically routes requests to the most appropriate skill based on context, user intent, and available capabilities.

---

## MANDATORY USER VERIFICATION REQUIREMENT

### Policy: No Fix Claims Without User Confirmation

**CRITICAL**: Before claiming ANY issue, bug, or problem is "fixed", "resolved", "working", or "complete", the following verification protocol is MANDATORY:

#### Step 1: Technical Verification
- Run all relevant tests (build, type-check, unit tests)
- Verify no console errors
- Take screenshots/evidence of the fix

#### Step 2: User Verification Request
**REQUIRED**: Use the `AskUserQuestion` tool to explicitly ask the user to verify the fix:

```
"I've implemented [description of fix]. Before I mark this as complete, please verify:
1. [Specific thing to check #1]
2. [Specific thing to check #2]
3. Does this fix the issue you were experiencing?

Please confirm the fix works as expected, or let me know what's still not working."
```

#### Step 3: Wait for User Confirmation
- **DO NOT** proceed with claims of success until user responds
- **DO NOT** mark tasks as "completed" without user confirmation
- **DO NOT** use phrases like "fixed", "resolved", "working" without user verification

#### Step 4: Handle User Feedback
- If user confirms: Document the fix and mark as complete
- If user reports issues: Continue debugging, repeat verification cycle

### Prohibited Actions (Without User Verification)
- Claiming a bug is "fixed"
- Stating functionality is "working"
- Marking issues as "resolved"
- Declaring features as "complete"
- Any success claims about fixes

### Required Evidence Before User Verification Request
1. Technical tests passing
2. Visual confirmation via Playwright/screenshots
3. Specific test scenarios executed
4. Clear description of what was changed

**Remember: The user is the final authority on whether something is fixed. No exceptions.**
