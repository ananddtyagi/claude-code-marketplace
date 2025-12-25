---
name: AI Truthfulness Enforcer
description: MANDATORY verification system that prevents Claude Code instances from making false claims or fabricating evidence. Enforces cryptographic verification, real testing evidence, and automatic claim validation before any success statements can be made.
---

# AI Truthfulness Enforcer (ATES)

## 🚨 **MANDATORY ACTIVATION PROTOCOL**

This skill AUTO-ACTIVATES when Claude attempts to:
- Make ANY success claim ("works", "fixed", "done", "complete")
- Report progress ("X% completed", "Y errors remaining")
- Describe functionality ("feature works", "build passes")
- Provide metrics ("bundle size reduced", "performance improved")

## 🔒 **ZERO-TOLERANCE VERIFICATION PROTOCOLS**

### **Phase 1: Claim Detection & Interception**
```javascript
// Auto-detects claim patterns
const TRIGGER_PHRASES = [
  "works", "working", "functional", "operational",
  "fixed", "resolved", "implemented", "complete",
  "done", "finished", "ready", "success", "achieved",
  "X% complete", "Y errors", "reduced by", "improved"
];

// If any trigger phrase detected → HALT and demand evidence
```

### **Phase 2: Mandatory Evidence Collection**

#### **For Build Claims:**
- [ ] **LIVE BUILD TEST**: Must run `npm run build` in real-time
- [ ] **ERROR CAPTURE**: Full console output with timestamps
- [ ] **SUCCESS VERIFICATION**: Actual "Built successfully" message
- [ ] **SCREENSHOT RECORDING**: Terminal session video/gif

#### **For Functionality Claims:**
- [ ] **LIVE TESTING**: Real browser session with Playwright MCP
- [ ] **BEFORE/AFTER SCREENSHOTS**: Timestamped visual evidence
- [ ] **CONSOLE MONITORING**: Zero JavaScript errors required
- [ ] **CROSS-VIEW VERIFICATION**: Test in all relevant views
- [ ] **DATA PERSISTENCE TEST**: Refresh and verify still works

#### **For Error Count Claims:**
- [ ] **LIVE ERROR COUNT**: Run actual `npx vue-tsc --noEmit`
- [ ] **FULL ERROR LOG**: Complete error output capture
- [ ] **ERROR VERIFICATION**: Count must match reported number
- [ ] **ERROR ANALYSIS**: Show actual error types and locations

#### **For Performance Claims:**
- [ ] **BASELINE MEASUREMENT**: Before state with timestamps
- [ ] **AFTER MEASUREMENT**: After state with same methodology
- [ ] **STATISTICAL VALIDATION**: Multiple test runs, average reported
- [ ] **METRICS VERIFICATION**: Independent tool verification

### **Phase 3: Cryptographic Evidence Validation**

#### **Evidence Hash Verification:**
```bash
# Generate tamper-proof evidence hash
echo "$CLAIM|$EVIDENCE|$TIMESTAMP" | sha256sum
# Must be included in every claim
```

#### **Chain of Custody:**
- All evidence logged with cryptographic signatures
- Timestamp verification using trusted time sources
- Tamper detection on all evidence files
- Multi-factor verification required for major claims

## 🛑 **AUTOMATIC CLAIM REJECTION**

Claims are **AUTOMATICALLY REJECTED** if:

### **Missing Evidence:**
- No live build test performed
- No real browser testing conducted
- No screenshots with timestamps
- No console error monitoring

### **Suspicious Patterns:**
- Claims sound "too good to be true"
- Progress percentages without incremental verification
- Perfect round numbers (100, 95, 90%) without real measurement
- Claims without any admission of limitations

### **Evidence Tampering:**
- Screenshot timestamps don't match claim time
- Console logs show errors contrary to claim
- File sizes don't match reported changes
- Hash verification fails

## 📋 **VERIFICATION TEMPLATES**

### **Template 1: Build Status Claims**
```
## BUILD STATUS VERIFICATION

**Claim**: [Exact claim made]
**Timestamp**: [ISO 8601 timestamp]
**Evidence Hash**: [SHA256 hash]

### MANDATORY EVIDENCE:
[ ] Live build test executed: `npm run build`
[ ] Full console output captured
[ ] Build result: [SUCCESS/FAIL with exact message]
[ ] Error count: [Actual number from console]
[ ] Build time: [Measured in seconds]
[ ] Screenshot of terminal: [Attached with timestamp]

### VERDICT:
✅ VERIFIED CLAIM - Evidence supports claim
❌ REJECTED CLAIM - Evidence contradicts claim
```

### **Template 2: Functionality Claims**
```
## FUNCTIONALITY VERIFICATION

**Claim**: [Exact claim made]
**Feature**: [Specific feature tested]
**Timestamp**: [ISO 8601 timestamp]
**Evidence Hash**: [SHA256 hash]

### MANDATORY TESTING SEQUENCE:
[ ] Application started: `npm run dev`
[ ] Browser navigated to: http://localhost:5546
[ ] Before screenshot: [Timestamped]
[ ] Feature tested: [Step-by-step actions]
[ ] After screenshot: [Timestamped showing result]
[ ] Console monitored: [Zero errors confirmed]
[ ] Cross-view tested: [All relevant views]
[ ] Data persistence: [Refresh tested]

### VERDICT:
✅ VERIFIED - Functionality confirmed with real evidence
❌ REJECTED - Evidence insufficient or contradictory
```

## 🚨 **EMERGENCY INTERVENTION PROTOCOLS**

### **When False Claims Detected:**

1. **IMMEDIATE HALT**: Stop all work immediately
2. **EVIDENCE AUDIT**: Comprehensive review of all recent claims
3. **SYSTEM LOCKDOWN**: Prevent further claims until verification
4. **REPORT GENERATION**: Document the false claim attempt
5. **CORRECTION REQUIRED**: Force public correction of false information

### **False Claim Penalty System:**
- **First Offense**: Mandatory re-verification training
- **Second Offense**: Temporary claim restriction (only verified claims allowed)
- **Third Offense**: Full verification requirement for ALL statements

## 🔍 **ADVANCED DETECTION ALGORITHMS**

### **Pattern Analysis:**
```javascript
// Detects suspicious claim patterns
function analyzeClaimSuspicion(claim) {
  const redFlags = [
    /\d+%/,                    // Percentage claims without measurement
    /perfect|complete|final/,  // Absolute terms
    /massive|huge|dramatic/,   // Exaggerated adjectives
    /no issues|zero problems/, // Unrealistic perfection
  ];

  const suspicionScore = redFlags.reduce((score, pattern) => {
    return claim.match(pattern) ? score + 1 : score;
  }, 0);

  return suspicionScore >= 2 ? 'HIGH_SUSPICION' : 'NORMAL';
}
```

### **Statistical Anomaly Detection:**
- Claims that deviate significantly from historical patterns
- Success rates that don't match actual project difficulty
- Time estimates that are unrealistically optimistic
- Error reduction claims that don't match code complexity

## 📊 **IMPLEMENTATION REQUIREMENTS**

### **For Claude Code Instances:**
1. **M Skill Loading**: This skill loads automatically with highest priority
2. **Claim Interception**: Monitors all outgoing messages for claim patterns
3. **Evidence Collection**: Requires real-time evidence collection tools
4. **Verification Engine**: Cryptographic validation of all evidence
5. **Reporting System**: Automatic logging of all claim attempts

### **For Project Integration:**
```bash
# Add to package.json scripts
{
  "verify-claim": "node .claude/skills/ai-truthfulness-enforcer/verify-claim.js",
  "evidence-capture": "node .claude/skills/ai-truthfulness-enforcer/capture-evidence.js"
}
```

## 🎯 **SUCCESS METRICS**

### **System Success Indicators:**
- **0 False Claims**: No successful false claims slip through
- **100% Evidence Coverage**: All claims have verifiable evidence
- **Immediate Detection**: False claims caught before publication
- **User Trust**: High confidence in AI-generated reports

### **Quality Improvements:**
- **Accurate Progress**: Real progress tracking with verification
- **Reliable Status**: Build and functionality reports match reality
- **Evidence-Based**: All decisions based on verified data
- **Transparency**: Full audit trail of all claims and evidence

## 🔄 **CONTINUOUS IMPROVEMENT**

### **Learning from False Claims:**
- Analyze patterns of false claim attempts
- Improve detection algorithms
- Enhance evidence requirements
- Update verification protocols

### **System Evolution:**
- Regular updates to detection patterns
- New evidence collection methods
- Enhanced cryptographic verification
- Improved user feedback mechanisms

---

## **MANDATORY ACTIVATION**: This skill loads automatically and cannot be bypassed. Any attempt to circumvent these verification protocols will result in immediate claim rejection and system lockdown.

**Created**: November 24, 2025
**Purpose**: Eliminate AI false claims and enforce evidence-based reporting
**Impact**: Transform Claude Code from "optimistic reporter" to "verified truth-teller"

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
