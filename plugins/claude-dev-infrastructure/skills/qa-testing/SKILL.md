---
name: Comprehensive Testing & Verification
description: MASTER Vue.js application testing with strict enforcement of verification protocols. Systematically test functionality with Playwright, validate bug fixes, verify features work, and enforce zero-tolerance policies for false success claims. MANDATORY testing with visual evidence before any deployment or functionality claims.
---

# Comprehensive Testing

## Instructions

### Mandatory Testing Protocol
ALWAYS follow this sequence before claiming any feature works:

1. **Environment Setup**
   - Navigate to http://localhost:5546
   - Wait for app container to load
   - Verify stores are loaded
   - Check for initial console errors

2. **Real Data Verification**
   - Confirm tasks are loaded (not demo content)
   - Verify tasks have real properties (ids, titles, dates)
   - Check no placeholder/demo data exists

3. **Playwright MCP Testing**
   - Test functionality in browser
   - Verify visual feedback works correctly
   - Monitor for console errors
   - Confirm state synchronization across views

4. **Cross-View Validation**
   - Test sidebar ↔ calendar ↔ kanban sync
   - Verify state changes reflect everywhere
   - Test data persistence after refresh

### Zero Tolerance Rules
- **NO console errors** allowed (zero tolerance)
- **NO demo content** - must use real data
- **NO assumptions** - must verify visually
- **NO shortcuts** - complete testing required

### Critical Validation Checklist
- [ ] Real tasks loaded (not demo content)
- [ ] Zero console errors
- [ ] Visual confirmation in Playwright MCP
- [ ] State synchronized across all views
- [ ] Data persists after page refresh
- [ ] All interactions work as expected

### Test Examples
```javascript
// Test task creation
await page.click('[data-testid="quick-add-task"]')
await page.fill('[data-testid="task-title-input"]', 'Test Task')
await page.click('[data-testid="save-task"]')
await expect(page.locator('[data-testid="sidebar-task"]:has-text("Test Task")')).toBeVisible()

// Test calendar drag-drop
const sidebarTask = page.locator('[data-testid="sidebar-task"]').first()
const timeSlot = page.locator('[data-testid="time-slot"]').first()
await sidebarTask.dragTo(timeSlot)
await expect(page.locator('[data-testid="calendar-event"]')).toBeVisible()
```

## Strict Verification Protocols (Integrated from qa-verify & testing-enforcer)

### 🚫 ZERO TOLERANCE POLICY

**NEVER claim functionality works without mandatory testing evidence.** Every success declaration requires:

#### MANDATORY Verification Sequence
**Phase 1: Baseline Verification**
1. **Start Application**: Run `npm run dev`
2. **Verify Server Running**: Check dev server starts successfully
3. **Verify Build Works**: Run `npm run build` - must pass without errors
4. **Take Baseline Screenshot**: Use Playwright MCP to capture initial state

**Phase 2: Change Implementation**
1. **Make ONE Change**: Only one small change at a time
2. **Immediate Build Test**: Run `npm run build` after every single change
3. **Fix Build Errors**: If build fails, fix before proceeding
4. **Check Console**: Monitor for any console errors

**Phase 3: Functional Testing**
1. **Navigate to Application**: Use Playwright MCP to go to the running app
2. **Take Screenshot**: Capture state before testing
3. **Test the Specific Feature**: Only test what was changed
4. **Take After Screenshot**: Capture state after testing
5. **Check Console**: Ensure no errors during testing

**Phase 4: Cross-View Verification**
1. **Test in Multiple Views**: Verify changes work across different app views
2. **Test Data Persistence**: Refresh page and verify changes persist
3. **Test Related Features**: Ensure no regression in related functionality

### 🎯 ENFORCEMENT TRIGGERS

#### Monitored Claim Patterns
The system automatically detects when you claim:
- "works", "working", "functional"
- "done", "complete", "finished"
- "ready", "production-ready", "deployable"
- "success", "successful", "achieved"
- "fixed", "resolved", "implemented"
- "verified", "confirmed", "validated"

#### Required Evidence for Claims
**For UI Changes:**
- ✅ Playwright MCP test results (pass/fail)
- ✅ Visual screenshots (before/after)
- ✅ Console error monitoring (clean)
- ✅ Cross-view compatibility (verified)
- ✅ Data persistence (confirmed)

**For Performance Claims:**
- ✅ Benchmark measurements (before/after)
- ✅ Memory usage analysis
- ✅ Load time measurements
- ✅ Resource utilization data

**For Bug Fixes:**
- ✅ Reproduction case (before fix)
- ✅ Test scenario (after fix)
- ✅ Regression testing (related features)
- ✅ Edge case validation

### 📋 TESTING CHECKLIST

#### Before Claiming ANY Feature Works:
- [ ] **Application starts**: `npm run dev` succeeds
- [ ] **Build passes**: `npm run build` no errors
- [ ] **Real data present**: No demo/placeholder data
- [ ] **Visual test passed**: Playwright MCP confirms
- [ ] **Console clean**: No JavaScript errors
- [ ] **Cross-view tested**: Works in all relevant views
- [ ] **Data persists**: Survives page refresh
- [ ] **Regressions checked**: Related features still work
- [ ] **Screenshots captured**: Before/after evidence
- [ ] **Test results documented**: Pass/fail evidence recorded

#### Automatic Claim Detection:
When the system detects a success claim without evidence:
1. **HALT**: Stop the workflow
2. **REQUEST**: Demand specific testing evidence
3. **GUIDE**: Provide exact testing steps required
4. **VERIFY**: Confirm evidence meets standards
5. **APPROVE**: Only then allow claim to stand

### 🔍 Evidence Collection Templates

#### UI Feature Testing Template
```javascript
// Evidence Collection Template
const evidenceCollection = {
  featureName: "Feature Name",
  claimDate: new Date().toISOString(),
  testingEnvironment: {
    url: "http://localhost:5546",
    browser: "chromium",
    viewport: "1280x720"
  },
  tests: [
    {
      description: "Test specific functionality",
      expectedResult: "Expected outcome",
      actualResult: "Actual outcome",
      status: "PASS/FAIL",
      screenshot: "path/to/screenshot.png",
      evidence: "Detailed test results"
    }
  ],
  verification: {
    buildPassed: true,
    consoleClean: true,
    crossViewTested: true,
    dataPersists: true,
    noRegressions: true
  }
}
```

---

This comprehensive testing skill ensures rigorous validation that features actually work with real data, verifiable evidence, and zero tolerance for false success claims. **All claims must be backed by mandatory testing evidence before being accepted.**

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
