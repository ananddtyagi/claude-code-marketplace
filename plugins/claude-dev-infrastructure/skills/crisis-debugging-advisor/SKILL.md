# Crisis Debugging Advisor

**Category**: Development Strategy & Debugging Methodology
**Target Users**: Developers feeling stuck with countless app issues and AI false success claims
**Primary Goal**: Systematic approach to regain control when AI assistants claim success but reality shows broken functionality

## When to Use This Skill

Use this advisor when you experience:
- ✅ **"Claude Code keeps claiming success but everything is still broken"**
- ✅ **Feeling overwhelmed with countless issues that make the app unusable**
- ✅ **AI tools reporting success while manual testing shows failures**
- ✅ **Not knowing what your next step should be**
- ✅ **App completely broken after AI-assisted development**
- ✅ **Loss of trust in AI-generated solutions**
- ✅ **Complex Vue.js/React application state management issues**

## Core Philosophy: Reality-First Verification

**Golden Rule**: **Manual verification ALWAYS trumps AI claims. If it doesn't work in browser, it's broken. Period.**

This skill implements the **Reality-First Verification Protocol (RFVP)**:
1. **AI suggestions are hypotheses, not facts**
2. **Browser testing is ground truth**
3. **Systematic verification over blind trust**
4. **Incremental validation over wholesale changes**

## The 4-Phase Crisis Debugging Framework

### Phase 1: Situation Assessment & Reality Check (15-30 minutes)

**Objective**: Establish ground truth of what actually works vs. what's broken

```bash
# Step 1: Create a Reality Check Matrix
# Create this file manually in your project root:
REALITY_CHECK.md

# Structure:
## Core Functionality Status
- [ ] App loads without console errors
- [ ] Basic task creation works
- [ ] Data persistence (IndexedDB) works
- [ ] Navigation between views works
- [ ] Timer functionality works
- [ ] Canvas interactions work

## AI Claim vs Reality Test
- [ ] AI: "Fixed X" → Manual Test: [ ] Actually works
- [ ] AI: "Implemented Y" → Manual Test: [ ] Actually works
```

**Immediate Actions**:
1. **Open browser dev tools** - Clear all errors first
2. **Test ONE core feature** - Pick the most critical functionality
3. **Document exact failure points** - Not "broken" but "task creation fails at step 3"
4. **Take screenshots** - Visual evidence of failures

### Phase 2: Binary Search Debugging (2-4 hours)

**Objective**: Systematically isolate the root cause using divide-and-conquer

**Binary Search Protocol**:
1. **Identify last known working state** (git tag, backup, or memory)
2. **List all major changes since then**
3. **Test changes in chunks** (half at a time)
4. **Continue halving until problem isolated**

```bash
# Implementation Example:
git log --oneline -20  # List last 20 changes
# Test changes 1-10: npm run dev + manual test
# If broken: test changes 1-5
# If working: test changes 6-10
# Continue until single problematic commit identified
```

**Vue.js Specific Binary Search**:
1. **Test stores in isolation** - Disable Pinia stores one by one
2. **Test components in isolation** - Comment out components systematically
3. **Test composables** - Remove custom composables progressively
4. **Test routes** - Disable routes one by one

### Phase 3: Ground-Up Reconstruction (4-8 hours)

**Objective**: Build from a working foundation, verifying each layer

**Layer-by-Layer Verification**:
```javascript
// Layer 1: Core App Bootstrap
const coreAppTest = {
  test: "Does Vue app mount without errors?",
  verify: () => {
    // Remove all components, just test app mounting
    createApp(App).mount('#app')
  }
}

// Layer 2: Basic State Management
const storeTest = {
  test: "Does basic Pinia store work?",
  verify: () => {
    // Test simplest store with basic counter
    const testStore = defineStore('test', () => {
      const count = ref(0)
      return { count }
    })
  }
}

// Layer 3: Basic Component
const componentTest = {
  test: "Does simplest component render?",
  verify: () => {
    // Test component with just <div>Hello World</div>
  }
}
```

**Reconstruction Order**:
1. **Blank Vue app** - Just mounting, no features
2. **Basic routing** - Single static route
3. **Simplest Pinia store** - Basic counter or boolean
4. **One basic component** - Static content only
5. **Add complexity incrementally** - One feature at a time

### Phase 4: AI Trust Rebuilding & New Protocol (Ongoing)

**Objective**: Establish systematic AI verification workflow

**AI Verification Protocol**:
```
FOR EACH AI SUGGESTION:
1. AI provides code change
2. BEFORE implementing: Create success test criteria
3. Implement change
4. MANUAL verification in browser
5. IF works: Accept and document
6. IF fails: Reject and report back to AI with exact failure
```

**Success Test Criteria Template**:
```javascript
// Before accepting AI suggestion:
const successCriteria = {
  feature: "Task Creation",
  steps: [
    "Navigate to BoardView",
    "Click 'Add Task' button",
    "Type 'Test Task'",
    "Press Enter",
    "Task appears in list"
  ],
  expectedResults: [
    "No console errors",
    "Task persists on refresh",
    "Task appears in correct swimlane"
  ]
}
```

## Crisis Debugging Toolset

### Essential Verification Scripts

Create these in your project for systematic testing:

**1. Core Functionality Test** (`test-core.js`):
```javascript
// Run in browser console to test basic functionality
const coreTests = {
  testAppMount: () => {
    return document.querySelector('#app') !== null
  },
  testNoConsoleErrors: () => {
    // Monitor console for 30 seconds
    return console.errorCount === 0
  },
  testBasicStore: () => {
    // Test if Pinia stores are accessible
    try {
      const store = useTaskStore()
      return store !== undefined
    } catch {
      return false
    }
  }
}
```

**2. Store State Validator** (`validate-stores.js`):
```javascript
// Run to validate all store states
const validateStores = () => {
  const stores = ['tasks', 'canvas', 'timer', 'ui']
  const results = {}

  stores.forEach(storeName => {
    try {
      const store = useStore(storeName)
      results[storeName] = {
        accessible: true,
        hasData: Object.keys(store.$state).length > 0,
        errors: null
      }
    } catch (error) {
      results[storeName] = {
        accessible: false,
        hasData: false,
        errors: error.message
      }
    }
  })

  return results
}
```

### Debugging Environment Setup

**Browser DevTools Configuration**:
1. **Console Panel**: Clear all errors first
2. **Network Panel**: Monitor failed API/IndexedDB calls
3. **Vue DevTools**: Install and inspect component tree
4. **Performance Panel**: Check for memory leaks/freezes

**Essential Browser Extensions**:
- Vue DevTools (for Vue.js apps)
- React DevTools (for React apps)
- Redux DevTools (if using Redux)
- IndexedDB Viewer (Chrome extension)

## Common Crisis Patterns & Solutions

### Pattern 1: "AI Claims Success, But App Won't Load"

**Root Causes**:
- Syntax errors in AI-generated code
- Missing imports/dependencies
- Broken component references

**Debugging Steps**:
1. **Check browser console** for syntax errors
2. **Validate imports** - all referenced files exist
3. **Test component mounting** - comment out AI components
4. **Rollback to working version** and implement manually

### Pattern 2: "State Management Completely Broken"

**Root Causes**:
- Conflicting store mutations
- Broken reactivity chains
- IndexedDB corruption

**Debugging Steps**:
1. **Clear browser storage** (IndexedDB, localStorage)
2. **Test stores in isolation** - disable all but one
3. **Check Pinia DevTools** for state anomalies
4. **Reset to default store state** manually

### Pattern 3: "Canvas/Interactive Elements Dead"

**Root Causes**:
- Event handler conflicts
- CSS z-index issues
- Vue Flow integration problems

**Debugging Steps**:
1. **Test basic click events** on simple elements
2. **Check CSS for pointer-events: none**
3. **Isolate canvas component** - remove all other elements
4. **Test Vue Flow basic functionality** without custom logic

### Pattern 4: "Performance Degraded to Unusable"

**Root Causes**:
- Memory leaks from AI code
- Inefficient re-renders
- Large data handling issues

**Debugging Steps**:
1. **Performance tab** - identify bottlenecks
2. **Memory tab** - check for leaks
3. **Profile component updates** - Vue DevTools
4. **Test with smaller datasets**

## Emergency Recovery Procedures

### Procedure 1: Safe Mode Development

When app is completely broken:

```bash
# 1. Create minimal working version
mkdir crisis-recovery
cd crisis-recovery

# 2. Copy only essential files
# - package.json
# - vite.config.js (minimal)
# - index.html (minimal)
# - src/main.ts (basic Vue setup)
# - src/App.vue (empty template)

# 3. Build incrementally
# Start with blank app, add one feature at a time
```

### Procedure 2: Git Bisect for Problem Isolation

```bash
# Start binary search through git history
git bisect start
git bisect bad HEAD  # Current version is broken
git bisect good v1.0-stable  # Last known good version

# Git will checkout a commit for testing
npm run dev
# Test manually
git bisect good  # or git bisect bad

# Continue until problem commit is identified
```

### Procedure 3: Component Isolation Testing

```vue
<!-- Create TestComponent.vue for isolation -->
<template>
  <div class="test-component">
    <h2>Component Test: {{ componentName }}</h2>
    <button @click="testClick">Test Click</button>
    <p>Clicks: {{ clickCount }}</p>
    <p v-if="error" class="error">Error: {{ error }}</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  componentName: String
})

const clickCount = ref(0)
const error = ref(null)

const testClick = () => {
  try {
    clickCount.value++
    // Add component-specific test logic here
  } catch (e) {
    error.value = e.message
  }
}
</script>
```

## Communication Protocol with AI Tools

### When Reporting Issues to AI:

**Bad Report**: "The app is broken"
**Good Report**:
```
ISSUE REPORT:
- Feature: Task creation in BoardView
- Steps to Reproduce:
  1. Navigate to BoardView
  2. Click "Add Task" button
  3. Type "Test Task"
  4. Press Enter
- Expected Result: Task appears in "Planned" swimlane
- Actual Result: Button click does nothing, no console errors
- Browser Console: [Paste exact console output]
- Environment: Chrome 120, Vue 3.4.0, Pinia 2.1.0
```

### When Requesting AI Assistance:

**Template**:
```
CONTEXT: I'm in a crisis debugging situation. Previous AI suggestions claimed success but functionality is still broken.

CURRENT STATUS:
- Working: [List what actually works]
- Broken: [List what's broken with specific failures]
- Last Working Version: [git tag or description]
- Recent Changes: [List recent modifications]

REQUESTED ACTION:
- [Specific, measurable request]
- Success Criteria: [How I'll verify it works]
- Verification Plan: [How I'll test before accepting]

CONSTRAINTS:
- I will manually verify in browser before accepting
- I need incremental changes, not wholesale rewrites
- If you're uncertain, please say so rather than guessing
```

## Prevention Strategies

### 1. Trust-but-Verify Development

- **Never accept AI claims at face value**
- **Always create success criteria before implementing**
- **Test manually in browser every single change**
- **Maintain a working baseline at all times**

### 2. Incremental Feature Development

- **One feature at a time, fully tested**
- **Commit after each working feature**
- **Tag releases with descriptive names**
- **Maintain rollback capability**

### 3. Automated Verification Setup

```javascript
// Create automated smoke tests
const smokeTests = {
  testBasicFunctionality: async () => {
    // Test core app functionality
    await page.goto('http://localhost:5546')
    await expect(page.locator('#app')).toBeVisible()
    await expect(page.locator('[data-testid="task-create"]')).toBeVisible()
  },

  testDataPersistence: async () => {
    // Test that data saves and loads
    await page.fill('[data-testid="task-input"]', 'Test Task')
    await page.press('[data-testid="task-input"]', 'Enter')
    await page.reload()
    await expect(page.locator('text=Test Task')).toBeVisible()
  }
}
```

## Quick Reference: Crisis Action Plan

**When Everything Feels Broken**:

1. **STOP** - Don't make more changes
2. **BREATHE** - This is solvable with systematic approach
3. **ASSESS** - Use Reality Check Matrix (30 minutes)
4. **ISOLATE** - Binary search through recent changes (2 hours)
5. **REBUILD** - Start from working foundation (4-8 hours)
6. **VERIFY** - Every change manually tested
7. **PREVENT** - Implement trust-but-verify protocol

**Remember**: Your manual testing is the ground truth. AI tools are assistants, not authorities. If it doesn't work in the browser, it's broken - regardless of what AI claims.

---

**Created by**: Crisis Debugging Research Team
**Based on**: Systematic debugging methodologies, AI verification protocols, and real-world crisis recovery scenarios
**Last Updated**: 2025-11-09

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
