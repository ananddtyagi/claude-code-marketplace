#!/usr/bin/env node

/**
 * Crisis Debugging Advisor Skill
 *
 * This skill helps developers who feel stuck with countless app issues
 * and AI tools claiming false success while reality shows broken functionality.
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

// Import smart file path resolver for proper file organization
import { getSmartPath } from '../../../scripts/file-path-resolver.cjs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

class CrisisDebuggingAdvisor {
  constructor() {
    this.projectRoot = process.cwd();
    // Use smart file paths to prevent root directory clutter
    this.realityCheckPath = getSmartPath('emergency', 'reality-check.md');
    this.crisisLogPath = getSmartPath('emergency', 'crisis-log.md');
  }

  async run(args) {
    const command = args[0];

    console.log('\n🚨 Crisis Debugging Advisor');
    console.log('============================\n');
    console.log('For developers feeling stuck with broken apps and AI false success claims\n');

    switch (command) {
      case 'assess':
        await this.situationAssessment();
        break;
      case 'reality-check':
        await this.createRealityCheck();
        break;
      case 'isolate':
        await this.binarySearchDebug();
        break;
      case 'rebuild':
        await this.groundUpReconstruction();
        break;
      case 'protocol':
        await this.establishVerificationProtocol();
        break;
      case 'emergency':
        await this.emergencyRecovery();
        break;
      default:
        await this.showMenu();
    }
  }

  async showMenu() {
    console.log('Available Commands:\n');
    console.log('  assess         - Complete situation assessment and reality check');
    console.log('  reality-check  - Create reality check matrix');
    console.log('  isolate        - Binary search debugging to isolate root cause');
    console.log('  rebuild        - Ground-up reconstruction from working foundation');
    console.log('  protocol       - Establish AI verification protocol');
    console.log('  emergency      - Emergency recovery procedures');
    console.log('\nUsage: node index.js <command>\n');

    console.log('🔍 Quick Start:');
    console.log('1. Run "node index.js assess" for complete analysis');
    console.log('2. Follow the systematic debugging framework');
    console.log('3. Remember: Manual verification ALWAYS trumps AI claims');
    console.log('\n💡 Remember: If it doesn\'t work in browser, it\'s broken. Period.');
  }

  async situationAssessment() {
    console.log('📊 Phase 1: Situation Assessment & Reality Check\n');
    console.log('Let\'s establish what actually works vs. what AI claims works...\n');

    // Create reality check
    await this.createRealityCheck();

    console.log('🔍 Next Steps:');
    console.log('1. Open your browser at http://localhost:5546');
    console.log('2. Test each item in REALITY_CHECK.md manually');
    console.log('3. Mark actual working vs. broken features');
    console.log('4. Run "node index.js isolate" to find root cause');

    console.log('\n⚠️  CRITICAL REMINDER:');
    console.log('Do not trust AI success claims. Only trust manual browser testing.');
  }

  async createRealityCheck() {
    console.log('📋 Creating Reality Check Matrix...\n');

    const realityCheckTemplate = `# Reality Check Matrix
*Created: ${new Date().toISOString()}*
*Purpose: Establish ground truth of what actually works vs AI claims*

## Core Functionality Status
### App Foundation
- [ ] App loads without white screen or crashes
- [ ] No console errors in browser dev tools
- [ ] Vue app mounts successfully (#app element exists)
- [ ] Basic routing works (can navigate between views)

### Essential Features
- [ ] Task creation works (BoardView)
- [ ] Task editing works
- [ ] Task deletion works
- [ ] Data persistence works (IndexedDB/LocalForage)
- [ ] Timer functionality works
- [ ] Canvas interactions work (drag/drop)

### State Management
- [ ] Pinia stores are accessible
- [ ] Tasks store loads data correctly
- [ ] Canvas store state updates properly
- [ ] Timer store maintains session state
- [ ] UI store responds to changes

## AI Claim vs Reality Test
*Document recent AI suggestions and whether they actually work*

| AI Claim | Manual Test Result | Evidence |
|----------|-------------------|----------|
| "Fixed task creation" | [ ] Actually works | Screenshots/console logs |
| "Implemented canvas fixes" | [ ] Actually works | Screenshots/console logs |
| "Resolved state issues" | [ ] Actually works | Screenshots/console logs |

## Console Errors Checklist
### JavaScript Errors
- [ ] No "Uncaught TypeError" messages
- [ ] No "Cannot read property" errors
- [ ] No "Failed to resolve module" errors
- [ ] No async/await unhandled rejections

### Vue/Vite Errors
- [ ] No "Failed to resolve component" errors
- [ ] No "Property does not exist" errors
- [ ] No hydration mismatch errors
- [ ] No router warnings

## Performance Issues
- [ ] App loads within 3 seconds
- [ ] No memory leaks (monitor in DevTools)
- [ ] No excessive re-renders (Vue DevTools)
- [ ] No blocked main thread tasks

## Visual Regression
- [ ] UI elements render correctly
- [ ] No CSS layout issues
- [ ] Responsive design works
- [ ] Dark/light mode switching works

## Testing Evidence
### Screenshots Required
- [ ] App home page screenshot
- [ ] Browser console screenshot
- [ ] Vue DevTools screenshot
- [ ] Network tab screenshot (failed requests)

### Manual Test Videos
- [ ] Task creation workflow
- [ ] Canvas interaction workflow
- [ ] Navigation workflow

## Summary Assessment
### Current State
- Working Features: [Count] / [Total]
- Broken Features: [Count] / [Total]
- Overall App Status: [BROKEN / PARTIALLY WORKING / MOSTLY WORKING]

### Critical Path Issues
1. [Most critical issue preventing app usage]
2. [Second most critical issue]
3. [Third most critical issue]

### Next Priority Action
- [ ] Fix critical issue #1
- [ ] Run binary search debugging
- [ ] Start ground-up reconstruction
- [ ] Emergency recovery procedures

---
*Remember: Manual browser testing is ground truth. AI claims are hypotheses.*
`;

    fs.writeFileSync(this.realityCheckPath, realityCheckTemplate);
    console.log(`✅ Created: ${this.realityCheckPath}`);
    console.log('\n📝 Fill out this matrix with REAL testing results.');
    console.log('🔍 Be honest about what works vs. what AI claims works.');

    console.log('\n🚀 Quick Testing Commands:');
    console.log('npm run dev          # Start development server');
    console.log('Open browser         # Test manually in Chrome/Firefox');
    console.log('F12 → Console       # Check for errors');
    console.log('Vue DevTools        # Inspect component tree');
  }

  async binarySearchDebug() {
    console.log('🔍 Phase 2: Binary Search Debugging\n');
    console.log('Systematically isolating the root cause...\n');

    // Check if we have git history
    const hasGit = fs.existsSync(path.join(this.projectRoot, '.git'));

    if (hasGit) {
      console.log('📊 Git-based Binary Search:');
      console.log('This approach helps isolate the exact commit that broke functionality.\n');

      const gitBisectInstructions = `# Git Bisect Instructions
# Run these commands to find the breaking commit:

git bisect start
git bisect bad HEAD  # Current version is broken
git bisect good v1.0-stable  # Last known good tag (adjust as needed)

# Git will checkout commits for testing
# For each checkout:
npm run dev
# Test manually in browser
# If working: git bisect good
# If broken: git bisect bad

# Continue until Git identifies the problematic commit
git bisect reset  # End bisect when done
`;

      console.log(gitBisectInstructions);
    }

    console.log('🧪 Component-based Binary Search:');
    console.log('If git history isn\'t available, test components systematically:\n');

    const componentTestTemplate = `# Component Isolation Testing

## Test in Order (stop when you find the broken layer)

### Layer 1: Core App
- [ ] Remove all components, test basic Vue app mounting
- Test: Create blank app.vue with just <div>App Loaded</div>

### Layer 2: Basic Stores
- [ ] Test with simplest Pinia store possible
- Test: Create counter store with basic increment/decrement

### Layer 3: Static Components
- [ ] Add components without dynamic functionality
- Test: Static components with hardcoded data

### Layer 4: Basic Interactions
- [ ] Add simple click handlers and state changes
- Test: Button clicks that update simple state

### Layer 5: Complex Features
- [ ] Add task management, canvas, timer features
- Test: Full feature functionality

### Layer 6: Integrations
- [ ] Add IndexedDB, router, and third-party integrations
- Test: Full app functionality

## Isolation Code Template

### 1. Minimal App Test
\`\`\`vue
<!-- src/App.vue -->
<template>
  <div>App Loaded Successfully</div>
</template>

<script setup>
// Nothing else - pure minimal test
</script>
\`\`\`

### 2. Basic Store Test
\`\`\`javascript
// src/stores/test-store.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useTestStore = defineStore('test', () => {
  const count = ref(0)

  const increment = () => count.value++
  const decrement = () => count.value--

  return { count, increment, decrement }
})
\`\`\`

### 3. Simple Component Test
\`\`\`vue
<!-- src/components/TestComponent.vue -->
<template>
  <div>
    <h2>Test Component</h2>
    <p>Count: {{ testStore.count }}</p>
    <button @click="testStore.increment">+</button>
    <button @click="testStore.decrement">-</button>
  </div>
</template>

<script setup>
import { useTestStore } from '@/stores/test-store'
const testStore = useTestStore()
</script>
\`\`\`
`;

    fs.writeFileSync(getSmartPath('analysis', 'component-isolation-test.md'), componentTestTemplate);
    console.log('✅ Created: COMPONENT_ISOLATION_TEST.md');

    console.log('\n🎯 Binary Search Strategy:');
    console.log('1. Test Layer 1 (minimal app) - if broken, the issue is in core setup');
    console.log('2. If Layer 1 works, test Layer 2 (basic stores)');
    console.log('3. Continue testing layers until you find the breaking point');
    console.log('4. Focus debugging efforts on the broken layer only');

    console.log('\n⏱️  Expected Time: 2-4 hours for systematic isolation');
  }

  async groundUpReconstruction() {
    console.log('🔧 Phase 3: Ground-Up Reconstruction\n');
    console.log('Building from working foundation, verifying each layer...\n');

    const reconstructionInstructions = `# Ground-Up Reconstruction Guide

## Create Recovery Directory
\`\`\`bash
mkdir crisis-recovery
cd crisis-recovery
\`\`\`

## Step 1: Copy Essential Files Only
\`\`\`bash
# Copy package.json (minimal dependencies)
cp ../package.json .

# Copy vite.config.js (remove custom plugins for now)
cp ../vite.config.js .

# Create minimal index.html
cat > index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
  <title>Crisis Recovery App</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.js"></script>
</body>
</html>
EOF

# Create src directory and basic files
mkdir -p src
\`\`\`

## Step 2: Minimal Working App
Create these files in crisis-recovery/src/:

### main.js
\`\`\`javascript
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
\`\`\`

### App.vue
\`\`\`vue
<template>
  <div class="app">
    <h1>Crisis Recovery App</h1>
    <p>Step 1: Basic app mounting</p>
  </div>
</template>

<script setup>
console.log('App mounted successfully')
</script>

<style>
.app {
  padding: 20px;
  font-family: Arial, sans-serif;
}
</style>
\`\`\`

## Step 3: Test Foundation
\`\`\`bash
npm install
npm run dev
\`\`\`

**If this works, you have a solid foundation. If not, the issue is in:**
- Node.js version compatibility
- Package dependencies
- Vite configuration
- Environment setup

## Step 4: Incremental Layer Addition

### Add Basic Routing (if needed)
\`\`\`bash
npm install vue-router@4
\`\`\`

### Add Pinia (if needed)
\`\`\`bash
npm install pinia
\`\`\`

### Add Features One by One
1. [ ] Basic routing
2. [ ] Simple Pinia store (counter)
3. [ ] Basic components
4. [ ] Task management features
5. [ ] Canvas functionality
6. [ ] Timer features
7. [ ] Data persistence
8. [ ] Advanced features

## Verification Protocol for Each Step
Before adding the next feature, verify:
1. [ ] No console errors
2. [ ] App loads and is interactive
3. [ ] Previous features still work
4. [ ] New feature works as expected

## Rollback Strategy
If a feature breaks everything:
\`\`\`bash
git add .
git commit -m "Add [feature name]"
git tag -a "step-[number]" -m "[feature name] working"
\`\`\`

If next feature breaks:
\`\`\`bash
git reset --hard step-[previous-number]
\`\`\`

## Migration Strategy
Once you have a working foundation:
1. Copy original components one by one
2. Test each component individually
3. Fix issues before copying next component
4. Maintain working state at all times

## Success Criteria
The reconstruction is successful when:
1. All core features work without errors
2. Performance is acceptable
3. Data persistence works
4. User interactions work correctly
5. No console errors or warnings

## Time Expectation
- Foundation setup: 1-2 hours
- Feature reconstruction: 4-6 hours
- Testing and validation: 2-3 hours
- Total: 7-11 hours
`;

    fs.writeFileSync(getSmartPath('emergency', 'reconstruction-guide.md'), reconstructionInstructions);
    console.log('✅ Created: RECONSTRUCTION_GUIDE.md');

    console.log('\n🏗️  Reconstruction Strategy:');
    console.log('1. Create minimal working app in separate directory');
    console.log('2. Add features incrementally, testing each layer');
    console.log('3. Never add a new feature until current layer works perfectly');
    console.log('4. Commit/tag working states for easy rollback');

    console.log('\n⚠️  Critical Rules:');
    console.log('- Do NOT copy broken code to recovery directory');
    console.log('- Test EVERYTHING manually before proceeding');
    console.log('- One feature at a time, no exceptions');
    console.log('- If unsure, test more before proceeding');
  }

  async establishVerificationProtocol() {
    console.log('🤝 Phase 4: AI Trust Rebuilding & Verification Protocol\n');
    console.log('Establishing systematic AI verification workflow...\n');

    const verificationProtocol = `# AI Verification Protocol (AVP)

## Golden Rule: Reality-First Verification
**Manual browser testing ALWAYS trumps AI claims**
**If it doesn\'t work in browser, it\'s broken. Period.**

## Pre-Implementation Checklist
Before accepting ANY AI suggestion:

### 1. Success Criteria Definition
\`\`\`markdown
## Feature: [Feature Name]
### Success Criteria:
- [ ] Specific, measurable outcome
- [ ] User can complete [specific task]
- [ ] No console errors during workflow
- [ ] Data persists correctly
- [ ] Performance acceptable (< 3 seconds)

### Test Steps:
1. Navigate to [specific page/component]
2. Click [specific element]
3. Perform [specific action]
4. Verify [specific result]

### Acceptance Criteria:
✅ All test steps pass
✅ Manual verification in browser
✅ No regression in existing features
\`\`\`

### 2. Risk Assessment
- [ ] What could break if this is wrong?
- [ ] How easily can we rollback if needed?
- [ ] What's the blast radius if this fails?

### 3. Implementation Scope
- [ ] Is this a small, isolated change?
- [ ] Does this affect core functionality?
- [ ] Can we test this in isolation?

## Implementation Verification

### Step 1: Isolated Testing
\`\`\`javascript
// Create test component for isolated verification
const TestFeature = {
  template: \`
    <div class="test-feature">
      <h3>Testing: {{ featureName }}</h3>
      <button @click="testFeature">Test Now</button>
      <div v-if="testResult" class="result">
        Result: {{ testResult }}
      </div>
      <div v-if="error" class="error">
        Error: {{ error }}
      </div>
    </div>
  \`,

  setup() {
    const featureName = ref('New Feature')
    const testResult = ref(null)
    const error = ref(null)

    const testFeature = async () => {
      try {
        // Test the new feature in isolation
        const result = await testNewFeature()
        testResult.value = 'SUCCESS: ' + result
        error.value = null
      } catch (e) {
        error.value = e.message
        testResult.value = null
      }
    }

    return { featureName, testResult, error, testFeature }
  }
}
\`\`\`

### Step 2: Integration Testing
- [ ] Feature works in isolation
- [ ] Feature works with existing components
- [ ] No performance degradation
- [ ] No console errors
- [ ] Existing features still work

### Step 3: User Workflow Testing
- [ ] Complete user journey works
- [ ] Edge cases handled properly
- [ ] Error states are user-friendly
- [ ] Loading states work correctly

## Post-Implementation Validation

### Browser Testing Checklist
- [ ] Chrome/Chromium: Works
- [ ] Firefox: Works
- [ ] Safari (if applicable): Works
- [ ] Mobile Chrome: Works
- [ ] Mobile Safari: Works

### Performance Testing
- [ ] Initial load < 3 seconds
- [ ] Feature interaction < 1 second
- [ ] No memory leaks
- [ ] No excessive re-renders

### Error Handling Testing
- [ ] Network failures handled gracefully
- [ ] Invalid input handled properly
- [ ] Edge cases don\'t crash app
- [ ] Error messages are user-friendly

## Communication Template with AI

### When Requesting Changes:
\`\`\`
CONTEXT: I'm implementing changes following AI Verification Protocol.

CURRENT STATUS:
- Working: [List confirmed working features]
- Last Test Results: [Summarize recent testing]

REQUESTED CHANGE:
- Feature: [Specific feature name]
- Success Criteria: [What must work for this to be successful]
- Test Plan: [How I will verify this works]
- Constraints: [Any limitations or requirements]

VERIFICATION REQUIREMENTS:
1. I will test this manually in browser before accepting
2. I need step-by-step implementation, not wholesale changes
3. If uncertain, please provide multiple approaches with trade-offs
4. Include rollback instructions if needed
\`\`\`

### When Reporting Issues:
\`\`\`
ISSUE REPORT:
Feature: [Feature name]
Environment: [Browser, OS, versions]

STEPS TO REPRODUCE:
1. [Exact step 1]
2. [Exact step 2]
3. [Exact step 3]

EXPECTED RESULT:
[What should happen]

ACTUAL RESULT:
[What actually happens]

CONSOLE OUTPUT:
[Paste exact console errors]

ADDITIONAL CONTEXT:
[Relevant screenshots, videos, or observations]
\`\`\`

## Trust Rebuilding Metrics

Track these metrics to rebuild trust in AI assistance:

### Success Rate Tracking
\`\`\`markdown
## Week of [Date]
- AI Suggestions: [Count]
- Successfully Implemented: [Count]
- Failed Implementation: [Count]
- Success Rate: [Percentage]

### Failed Implementations Analysis:
1. [Reason for failure] - [How to prevent]
2. [Reason for failure] - [How to prevent]
3. [Reason for failure] - [How to prevent]
\`\`\`

### Quality Improvements:
- Better success criteria definition
- More thorough pre-testing
- Smaller, incremental changes
- Better communication of requirements

## Red Flags to Watch For

### AI Suggestions That Require Extra Scrutiny:
- Claims about "fixing everything" without specific details
- Wholesale rewrites of working code
- Suggestions without rollback plans
- Claims about performance improvements without metrics
- Complex solutions to simple problems

### When to Pause and Verify:
- Any suggestion involving core app architecture
- Changes to data persistence layer
- Modifications to routing or state management
- Claims about security improvements
- Major dependency updates

## Emergency Stop Criteria

STOP immediately and seek manual help if:
- AI suggests breaking working functionality
- Multiple consecutive failures occur
- Suggestions become increasingly complex
- You cannot verify the suggestion independently
- The app becomes completely broken

---

Remember: AI tools are assistants, not authorities. Your manual testing and verification are what matter most.
`;

    fs.writeFileSync(getSmartPath('verification', 'ai-verification-protocol.md'), verificationProtocol);
    console.log('✅ Created: AI_VERIFICATION_PROTOCOL.md');

    console.log('\n🔐 Verification Protocol Established:');
    console.log('1. Define success criteria BEFORE implementing');
    console.log('2. Test in isolation BEFORE integration');
    console.log('3. Manual browser verification is REQUIRED');
    console.log('4. Document failures to prevent recurrence');

    console.log('\n📊 Trust Rebuilding Takes Time:');
    console.log('- Start with small, low-risk changes');
    console.log('- Verify everything manually');
    console.log('- Track success rates over time');
    console.log('- Build confidence gradually');
  }

  async emergencyRecovery() {
    console.log('🚨 Emergency Recovery Procedures\n');
    console.log('For when the app is completely broken and you need immediate help...\n');

    const emergencyProcedures = `# Emergency Recovery Procedures

## STOP! Don't Panic, Follow This Systematically

### Immediate Actions (First 5 Minutes)

1. **STOP MAKING CHANGES**
   - Close your editor
   - Step away from keyboard
   - Take 3 deep breaths

2. **ASSESS THE DAMAGE**
   - What was the last thing that worked?
   - What specific change broke it?
   - Can you access the app at all?

3. **CREATE SAFE SPACE**
   - Open browser incognito mode
   - Clear all cache and storage
   - Test in a clean environment

## Emergency Procedure A: Quick Rollback

### If You Have Git History
\`\`\`bash
# Check recent commits
git log --oneline -10

# Find last working commit (look for "working" or "stable" in message)
git checkout [commit-hash]

# Test immediately
npm run dev
# Open browser and test basic functionality

# If working, create emergency branch
git checkout -b emergency-recovery
git add .
git commit -m "Emergency rollback to working state"
\`\`\`

### If You Don't Have Git History
\`\`\`bash
# Check if you have any backups
find . -name "*.backup" -o -name "*backup*" -o -name "*.bak"

# Look for recently deleted files in trash
# Check if you have any copies in other directories

# If no backups available, proceed to Emergency Procedure B
\`\`\`

## Emergency Procedure B: Safe Mode Recovery

### Create Emergency Recovery Directory
\`\`\`bash
# Create completely fresh start
mkdir emergency-recovery
cd emergency-recovery

# Initialize new project
npm init -y

# Install ONLY essential dependencies
npm install vue@latest pinia@latest @vitejs/plugin-vue vite

# Create minimal working app
mkdir -p src
\`\`\`

### Emergency App Files

#### package.json (minimal)
\`\`\`json
{
  "name": "emergency-recovery",
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build"
  },
  "dependencies": {
    "vue": "^3.4.0",
    "pinia": "^2.1.0"
  },
  "devDependencies": {
    "@vitejs/plugin-vue": "^5.0.0",
    "vite": "^5.0.0"
  }
}
\`\`\`

#### vite.config.js
\`\`\`javascript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000  // Different port to avoid conflicts
  }
})
\`\`\`

#### index.html
\`\`\`html
<!DOCTYPE html>
<html>
<head>
  <title>Emergency Recovery</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="/src/main.js"></script>
</body>
</html>
\`\`\`

#### src/main.js
\`\`\`javascript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.mount('#app')
\`\`\`

#### src/App.vue
\`\`\`vue
<template>
  <div class="emergency-app">
    <h1>🚨 Emergency Recovery Mode</h1>
    <div class="status">
      <h2>System Status: {{ systemStatus }}</h2>
      <p>Last Checked: {{ lastChecked }}</p>
    </div>

    <div class="tests">
      <h3>Basic Tests:</h3>
      <button @click="testVueMounting">Test Vue Mounting</button>
      <button @click="testPiniaStore">Test Pinia Store</button>
      <button @click="testReactivity">Test Reactivity</button>

      <div class="results">
        <div v-for="result in testResults" :key="result.name"
             :class="['result', result.success ? 'success' : 'error']">
          {{ result.name }}: {{ result.success ? '✅ PASS' : '❌ FAIL' }}
          <span v-if="result.error" class="error-message">{{ result.error }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useEmergencyStore } from './stores/emergency'

const emergencyStore = useEmergencyStore()
const systemStatus = ref('Checking...')
const lastChecked = ref(new Date().toLocaleTimeString())
const testResults = ref([])

const addResult = (name, success, error = null) => {
  testResults.value.unshift({ name, success, error })
  lastChecked.value = new Date().toLocaleTimeString()

  if (testResults.value.every(r => r.success)) {
    systemStatus.value = '✅ ALL SYSTEMS OPERATIONAL'
  } else {
    systemStatus.value = '⚠️ SYSTEMS DEGRADED'
  }
}

const testVueMounting = () => {
  try {
    const testElement = document.createElement('div')
    document.body.appendChild(testElement)
    document.body.removeChild(testElement)
    addResult('Vue Mounting', true)
  } catch (error) {
    addResult('Vue Mounting', false, error.message)
  }
}

const testPiniaStore = () => {
  try {
    const testValue = emergencyStore.testCounter
    emergencyStore.increment()
    const newValue = emergencyStore.testCounter
    addResult('Pinia Store', newValue === testValue + 1)
  } catch (error) {
    addResult('Pinia Store', false, error.message)
  }
}

const testReactivity = () => {
  try {
    const testRef = ref(0)
    testRef.value = 1
    addResult('Vue Reactivity', testRef.value === 1)
  } catch (error) {
    addResult('Vue Reactivity', false, error.message)
  }
}

onMounted(() => {
  // Run basic tests on mount
  setTimeout(() => {
    testVueMounting()
    testPiniaStore()
    testReactivity()
  }, 1000)
})
</script>

<style>
.emergency-app {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.status {
  background: #f0f0f0;
  padding: 15px;
  border-radius: 5px;
  margin: 20px 0;
}

.tests {
  background: #fafafa;
  padding: 20px;
  border-radius: 5px;
}

.tests button {
  margin: 5px;
  padding: 10px 15px;
  background: #007acc;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.results {
  margin-top: 20px;
}

.result {
  padding: 10px;
  margin: 5px 0;
  border-radius: 3px;
}

.result.success {
  background: #d4edda;
  color: #155724;
}

.result.error {
  background: #f8d7da;
  color: #721c24;
}

.error-message {
  display: block;
  font-size: 0.9em;
  margin-top: 5px;
}
</style>
\`\`\`

#### src/stores/emergency.js
\`\`\`javascript
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useEmergencyStore = defineStore('emergency', () => {
  const testCounter = ref(0)

  const increment = () => testCounter.value++
  const decrement = () => testCounter.value--

  return { testCounter, increment, decrement }
})
\`\`\`

### Test Emergency Recovery
\`\`\`bash
npm run dev
# Open browser to http://localhost:3000
# Click each test button
# Verify all tests pass
\`\`\`

## Emergency Procedure C: Professional Help

### When to Call for Help
- Emergency recovery fails
- You don't understand what broke
- Time pressure is extreme
- Core functionality is completely broken

### Prepare Emergency Information
\`\`\`markdown
# EMERGENCY HELP REQUEST

## What Happened:
- Last working state: [Description]
- What broke: [Specific description]
- Recent changes: [List]
- Error messages: [Paste exact errors]

## What I've Tried:
- [ ] Emergency rollback
- [ ] Safe mode recovery
- [ ] Component isolation
- [ ] Binary search debugging

## Project Details:
- Framework: Vue 3.4.0
- State Management: Pinia
- Build Tool: Vite
- Browser: [Version]
- Node.js: [Version]

## Urgency Level:
- [ ] Critical - Production down
- [ ] High - Development blocked
- [ ] Medium - Feature broken
- [ ] Low - Minor issue
\`\`\`

## Post-Emergency Prevention

### Once You Have a Working Foundation
1. **Set up proper git workflow**
   - Commit working states frequently
   - Tag stable versions
   - Use feature branches

2. **Implement testing**
   - Unit tests for core functionality
   - Integration tests for workflows
   - Manual testing checklists

3. **Establish backup procedures**
   - Regular code backups
   - Database backups
   - Configuration backups

4. **Improve development process**
   - Smaller, incremental changes
   - Better communication with AI
   - More thorough testing

---

Remember: Taking 30 minutes to follow emergency procedures systematically is faster than hours of panicked debugging.
`;

    fs.writeFileSync(getSmartPath('emergency', 'emergency-recovery.md'), emergencyProcedures);
    console.log('✅ Created: EMERGENCY_RECOVERY.md');

    console.log('\n🚨 Emergency Recovery Launched:');
    console.log('1. STOP making changes immediately');
    console.log('2. Follow procedures systematically');
    console.log('3. Create emergency recovery directory');
    console.log('4. Test basic functionality first');
    console.log('5. Rebuild from solid foundation');

    console.log('\n🆘 Critical Contacts:');
    console.log('- Documentation: Read all created .md files');
    console.log('- Community: Stack Overflow, Vue Discord, Reddit');
    console.log('- Professional: Consider paid help if time-critical');

    console.log('\n⏱️  Emergency Timeline:');
    console.log('- Assessment: 15 minutes');
    console.log('- Emergency rollback: 30 minutes');
    console.log('- Safe mode recovery: 1 hour');
    console.log('- Basic functionality: 2-3 hours');
  }

  async logCrisisEvent(issue, severity = 'medium') {
    const logEntry = {
      timestamp: new Date().toISOString(),
      issue,
      severity,
      resolution: null
    };

    let crisisLog = [];
    if (fs.existsSync(this.crisisLogPath)) {
      const content = fs.readFileSync(this.crisisLogPath, 'utf8');
      // Simple parsing - in real implementation, would be more robust
      try {
        crisisLog = JSON.parse(content);
      } catch (e) {
        crisisLog = [];
      }
    }

    crisisLog.push(logEntry);
    fs.writeFileSync(this.crisisLogPath, JSON.stringify(crisisLog, null, 2));
  }
}

// CLI Entry Point
const advisor = new CrisisDebuggingAdvisor();
advisor.run(process.argv.slice(2)).catch(console.error);

export default CrisisDebuggingAdvisor;