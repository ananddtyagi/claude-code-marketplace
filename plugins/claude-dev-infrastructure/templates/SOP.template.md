# SOP Template: {{ISSUE_TITLE}}

**Created**: {{DATE}}
**Last Updated**: {{DATE}}
**Status**: Active
**Related Tasks**: {{TASK_IDS}}

---

## Quick Reference

| Aspect | Details |
|--------|---------|
| **Problem** | Brief description of what went wrong |
| **Root Cause** | The underlying technical issue |
| **Solution** | High-level fix description |
| **Prevention** | How to avoid in future |

---

## 1. Issue Summary

### What Happened
Describe the observable symptoms or behavior that indicated something was wrong.

### Impact
- **Affected Areas**: List components/features affected
- **Severity**: Critical / High / Medium / Low
- **User Impact**: How users experienced the issue

---

## 2. Root Cause Analysis

### Technical Investigation

**Initial Hypothesis**:
What was initially suspected.

**Investigation Steps**:
1. Step 1: What was checked
2. Step 2: What was found
3. Step 3: How root cause was identified

**Root Cause**:
The actual technical reason for the issue.

### Code Evidence

**File**: `src/path/to/file.ts`
```typescript
// The problematic code
const example = problematicFunction()
```

**Why This Caused the Issue**:
Explanation of why this code caused the problem.

---

## 3. Solution Implementation

### Fix Overview

| File | Change Type | Description |
|------|-------------|-------------|
| `src/file1.ts` | Modified | Description of change |
| `src/file2.vue` | Added | New functionality |

### Fix Details

#### Fix 1: Description

**File**: `src/path/to/file.ts`

**Before**:
```typescript
// Old code
const oldImplementation = badApproach()
```

**After**:
```typescript
// Fixed code
const fixedImplementation = correctApproach()
```

**Why This Works**:
Explanation of why the fix resolves the issue.

---

## 4. Verification Steps

### Manual Testing
1. [ ] Test scenario 1
2. [ ] Test scenario 2
3. [ ] Test edge case

### Automated Tests
```bash
# Run relevant tests
npm run test:specific-area
```

### Visual Verification
- [ ] Verify in browser
- [ ] Check console for errors
- [ ] Confirm expected behavior

---

## 5. Rollback Procedure

### If Issues Arise

```bash
# Revert the changes
git revert {{COMMIT_HASH}}

# Or restore specific files
git checkout {{PREVIOUS_COMMIT}} -- src/affected/files.ts
```

### Rollback Verification
1. Confirm application builds
2. Verify original behavior restored
3. Document any data implications

---

## 6. Prevention Measures

### Code Guidelines
- Guideline 1 to prevent recurrence
- Guideline 2 for similar scenarios

### Testing Requirements
- Test type 1 to catch this issue
- Test type 2 for edge cases

### Documentation Updates
- [ ] Update CLAUDE.md if new pattern
- [ ] Add to common issues section
- [ ] Create skill if complex debugging needed

---

## 7. References

### Related Files
- `src/related/file1.ts` - Description
- `src/related/file2.vue` - Description

### Related Documentation
- [Link to relevant docs](#)
- [External reference](#)

### Related Issues
- BUG-XXX: Related bug
- TASK-XXX: Related task

---

## Appendix

### Debug Commands Used
```bash
# Commands that helped diagnose
command1
command2
```

### Console Output
```
Relevant console output or logs
```

### Screenshots
(Add screenshots if applicable)
