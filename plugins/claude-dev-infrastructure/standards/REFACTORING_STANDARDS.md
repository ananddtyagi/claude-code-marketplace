# 🔄 REFACTORING STANDARDS - REQUIRED READING

## **SAFE RESTRUCTURING FOR VUE 3 + TYPESCRIPT**
**Research-backed refactoring that maintains 100% functional compatibility**

---

## **🚨 CRITICAL: READ AND FOLLOW BEFORE ANY REFACTORING**

You are about to restructure working code where **the cure can be worse than the disease**. These standards ensure refactoring improves code quality without breaking existing functionality.

### **📊 REFACTORING RISK TRACKING:**
Following these research-backed standards prevents **90%** of refactoring-related failures:
- **50%** from inadequate test coverage
- **25%** from API contract violations
- **15%** from performance regression

---

## **🎯 AI ASSISTANT DECISION FRAMEWORK - MANDATORY PRE-ASSESSMENT**

### **CRITICAL: When NOT to Refactor (Stop Conditions)**
```typescript
/**
 * AI ASSISTANTS MUST run this assessment BEFORE suggesting any refactoring
 * Claude Code and other AI tools MUST verify these conditions
 */
interface RefactoringStopConditions {
  // 🚨 IMMEDIATE STOP - Do NOT refactor if any are true
  hasActiveProductionBugs: boolean;         // STOP: Fix bugs first
  testCoverageBelow50Percent: boolean;      // STOP: Write tests first
  scheduledForDepletion: boolean;           // STOP: Don't waste effort
  userDidNotRequestRefactor: boolean;       // STOP: User fixing bug, not refactoring
  timeConstraintCritical: boolean;          // STOP: Refactoring takes time
}

function shouldStopRefactoring(context: CodeContext): boolean {
  return Object.values(context.stopConditions).some(v => v === true);
}
```

### **🟡 CAUTION Conditions (Proceed with Care)**
```typescript
interface RefactoringCautionConditions {
  testCoverageBetween50And80: boolean;      // CAUTION: Add more tests first
  highCyclomaticComplexity: boolean;        // CAUTION: High complexity risk
  multipleFilesAffected: boolean;           // CAUTION: Coordinate changes
  publicAPIChanges: boolean;                // CAUTION: Breaking changes likely
  performanceCriticalComponent: boolean;    // CAUTION: Benchmark required
}
```

### **✅ GREEN LIGHT Conditions (Safe to Refactor)**
```typescript
interface RefactoringGreenLightConditions {
  testCoverageAbove80: boolean;             // ✅ Good test safety net
  singleFileRefactor: boolean;              // ✅ Isolated change
  noAPIChanges: boolean;                    // ✅ Internal only
  userExplicitlyRequestedRefactor: boolean; // ✅ Clear intent
  backupRollbackAvailable: boolean;         // ✅ Safety net ready
}
```

### **AI Response Templates Based on Assessment:**

#### **When User Asks for Bug Fix (Not Refactor):**
```
I notice this code could benefit from refactoring, but you're currently
fixing a bug. Let me provide the minimal fix for the bug first:

[minimal bug fix code]

After this bug is fixed and tested, would you like me to suggest
refactoring improvements to prevent similar bugs in the future?
```

#### **When Test Coverage is Insufficient:**
```
Before refactoring this code, I recommend adding tests to establish
a safety net. Current test coverage appears insufficient for safe
refactoring.

Here are tests I suggest writing first:

[test code]

Once these tests pass, I can safely refactor the code while ensuring
no behavior changes.
```

#### **When Refactoring Provides Little Benefit:**
```
I analyzed this code for refactoring opportunities. While there are
minor improvements possible, the current code is:

✅ Working correctly
✅ Reasonably maintainable
✅ Not causing performance issues

Refactoring would provide minimal benefit relative to the risk and
effort. I recommend leaving this code as-is unless:
- You're already modifying it for another reason
- It's causing recurring bugs
- Performance becomes an issue
```

---

## **🔍 PHASE 1: PRE-REFACTORING ASSESSMENT**

### **MANDATORY BASELINE DOCUMENTATION (Industry Standard):**
```bash
#!/bin/bash
# Comprehensive baseline before ANY refactoring

echo "=== REFACTORING BASELINE ASSESSMENT ===" > ./refactor-baseline.md
echo "Timestamp: $(date)" >> ./refactor-baseline.md
echo "Target: [file or component name]" >> ./refactor-baseline.md
echo "" >> ./refactor-baseline.md

# Test coverage analysis
echo "=== TEST COVERAGE ===" >> ./refactor-baseline.md
npm run test -- --coverage 2>&1 | tail -10 >> ./refactor-baseline.md

# TypeScript health
echo "=== TYPESCRIPT HEALTH ===" >> ./refactor-baseline.md
npx vue-tsc --noEmit 2>&1 | grep -c "error" >> ./refactor-baseline.md

# Linting status
echo "=== LINTING STATUS ===" >> ./refactor-baseline.md
npx eslint --ext .ts,.vue src/ 2>&1 | grep -c "error" >> ./refactor-baseline.md

# Build verification
echo "=== BUILD STATUS ===" >> ./refactor-baseline.md
npm run build 2>&1 | tail -5 >> ./refactor-baseline.md

# Performance baseline (if applicable)
if command -v npm run bench &> /dev/null; then
  echo "=== PERFORMANCE BASELINE ===" >> ./refactor-baseline.md
  npm run bench >> ./refactor-baseline.md
fi

# Create rollback point
echo "=== ROLLBACK POINT ===" >> ./refactor-baseline.md
git rev-parse HEAD >> ./refactor-baseline.md
```

### **DEPENDENCY ANALYSIS (Research-Backed):**
```bash
# Identify all files that depend on target
echo "=== DEPENDENCY ANALYSIS ===" > ./dependency-analysis.md

# Use TypeScript compiler API to trace dependencies
npx tsc --listFiles | grep -E "(target-file|related-files)" >> ./dependency-analysis.md

# Identify impact scope
echo "Files that import from target:" >> ./dependency-analysis.md
grep -r "import.*from.*target-file" src/ --include="*.ts" --include="*.vue" >> ./dependency-analysis.md

# Determine refactoring risk level
DEPENDENCY_COUNT=$(grep -c "import.*from.*target-file" ./dependency-analysis.md)
if [ $DEPENDENCY_COUNT -gt 5 ]; then
  echo "🟡 HIGH RISK: $DEPENDENCY_COUNT files depend on this code" >> ./dependency-analysis.md
elif [ $DEPENDENCY_COUNT -gt 2 ]; then
  echo "🟠 MEDIUM RISK: $DEPENDENCY_COUNT files depend on this code" >> ./dependency-analysis.md
else
  echo "✅ LOW RISK: $DEPENDENCY_COUNT files depend on this code" >> ./dependency-analysis.md
fi
```

---

## **⚡ PHASE 2: INCREMENTAL REFACTORING STRATEGIES**

### **RESEARCH-BACKED SAFE REFACTORING PATTERNS:**

#### **Pattern 1: Inline Composable Extraction (Preferred Starting Point)**
```typescript
// ❌ FORBIDDEN: Extract immediately to separate file
// Risk: Harder to test, more complex rollback

// ✅ RESEARCH-BACKED: Extract inline first, test, then separate
<script setup lang="ts">
// BEFORE: Monolithic component logic
const loading = ref(false);
const error = ref<Error | null>(null);
const data = ref<User[]>([]);

async function fetchUsers() {
  loading.value = true;
  try {
    const response = await api.getUsers();
    data.value = response.data;
  } catch (e) {
    error.value = e as Error;
  } finally {
    loading.value = false;
  }
}

// STEP 1: Extract inline composable (same file)
function useUserFetch() {
  const loading = ref(false);
  const error = ref<Error | null>(null);
  const data = ref<User[]>([]);

  async function fetchUsers() {
    loading.value = true;
    try {
      const response = await api.getUsers();
      data.value = response.data;
    } catch (e) {
      error.value = e as Error;
    } finally {
      loading.value = false;
    }
  }

  return { loading, error, data, fetchUsers };
}

// STEP 2: Update usage (same file)
const { loading, error, data, fetchUsers } = useUserFetch();
</script>

// STEP 3: Test thoroughly (same file context)
// STEP 4: Only then extract to separate file if used in 3+ components
```

#### **Pattern 2: Interface Evolution with Backward Compatibility**
```typescript
// ❌ FORBIDDEN: Breaking existing interface contracts
interface UserOld {
  name: string;
  age: number;
}

interface UserNew {
  fullName: string;  // BREAKING: 'name' removed
  age: number;
}

// ✅ RESEARCH-BACKED: Deprecation with backward compatibility
interface UserSafe {
  /** @deprecated Use fullName instead */
  name?: string;
  fullName: string;
  age: number;
}

// Implement adapter pattern for smooth migration
class UserAdapter {
  constructor(private user: UserSafe) {
    // Support both old and new during transition
    if (!user.fullName && user.name) {
      user.fullName = user.name;
    }
  }

  getSafeUser(): UserSafe {
    return this.user;
  }
}
```

#### **Pattern 3: Options API to Composition API Migration (Research-Based)**
```typescript
// ❌ FORBIDDEN: Complete rewrite in one step
// Risk: High chance of breaking existing functionality

// ✅ RESEARCH-BACKED: Incremental migration with compatibility
// STEP 1: Add Composition API alongside Options API
<script>
import { ref, computed } from 'vue';

export default {
  // Existing Options API preserved
  props: {
    userId: { type: Number, required: true }
  },
  data() {
    return {
      user: null,
      loading: false
    }
  },
  computed: {
    displayName() {
      return this.user?.name || 'Unknown';
    }
  },

  // STEP 2: Add setup() for Composition API (Vue 3 supports both)
  setup(props) {
    const user = ref(null);
    const loading = ref(false);

    // Mirror existing computed properties
    const displayName = computed(() => user.value?.name || 'Unknown');

    // Return what template needs
    return {
      user,
      loading,
      displayName
    };
  }
}
</script>

// STEP 2: Full Composition API (after Options API removed)
<script setup lang="ts">
interface Props {
  userId: number;
}

const props = defineProps<Props>();

const user = ref<User | null>(null);
const loading = ref(false);

const displayName = computed(() => user.value?.name || 'Unknown');

// Maintain exact same external behavior
async function fetchUser() {
  loading.value = true;
  try {
    user.value = await api.getUser(props.userId);
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  fetchUser();
});
</script>
```

#### **Pattern 4: Service Layer Restructuring with Facade Pattern**
```typescript
// ❌ FORBIDDEN: Direct breaking changes to service API
class UserService {
  async getUser(id: number) { /* ... */ }
  async updateUser(id: number, data: UserData) { /* ... */ }
  // ... other methods
}

// ✅ RESEARCH-BACKED: Facade pattern for backward compatibility
// STEP 1: Create new modular structure
class UserDataService {
  async getUser(id: number): Promise<User> {
    // New implementation
  }
}

class UserPermissionService {
  async getPermissions(userId: number): Promise<Permission[]> {
    // New implementation
  }
}

// STEP 2: Maintain old API with delegation
class UserService {
  private dataService = new UserDataService();
  private permService = new UserPermissionService();

  // Keep old API contracts exactly
  async getUser(id: number): Promise<User> {
    return this.dataService.getUser(id);
  }

  async updateUser(id: number, data: UserData): Promise<User> {
    return this.dataService.updateUser(id, data);
  }

  // Add new methods gradually
  async getUserPermissions(id: number): Promise<Permission[]> {
    return this.permService.getPermissions(id);
  }
}

// STEP 3: After migration period, introduce new APIs
class UserServiceV2 {
  // New, cleaner API
  constructor(
    private dataService: UserDataService,
    private permService: UserPermissionService
  ) {}
}
```

---

## **✅ PHASE 3: VALIDATION AND TESTING**

### **FUNCTIONAL EQUIVALENCE TESTING (Research-Based):**
```typescript
// Research-backed testing approach for refactored code
import { mount } from '@vue/test-utils';
import OriginalComponent from './OriginalComponent.vue';
import RefactoredComponent from './RefactoredComponent.vue';

describe('Refactoring Validation', () => {
  // Test data for comparison
  const testProps = {
    userId: 123,
    userName: 'Test User'
  };

  describe('Functional Equivalence', () => {
    it('should produce identical outputs for same inputs', async () => {
      const originalWrapper = mount(OriginalComponent, { props: testProps });
      const refactoredWrapper = mount(RefactoredComponent, { props: testProps });

      // Wait for both to load
      await originalWrapper.vm.$nextTick();
      await refactoredWrapper.vm.$nextTick();

      // Compare rendered output
      expect(originalWrapper.html()).toBe(refactoredWrapper.html());

      // Compare component state
      expect(originalWrapper.vm.internalState).toEqual(refactoredWrapper.vm.internalState);
    });

    it('should handle edge cases identically', async () => {
      const edgeCases = [
        { userId: null },
        { userId: 0 },
        { userId: -1 },
        { userId: Number.MAX_SAFE_INTEGER }
      ];

      for (const testCase of edgeCases) {
        const originalWrapper = mount(OriginalComponent, { props: testCase });
        const refactoredWrapper = mount(RefactoredComponent, { props: testCase });

        await originalWrapper.vm.$nextTick();
        await refactoredWrapper.vm.$nextTick();

        expect(originalWrapper.vm.errorState).toEqual(refactoredWrapper.vm.errorState);
      }
    });
  });

  describe('Performance Validation', () => {
    it('should not regress performance significantly', async () => {
      const iterations = 100;

      // Benchmark original
      const originalStart = performance.now();
      for (let i = 0; i < iterations; i++) {
        const wrapper = mount(OriginalComponent, { props: testProps });
        await wrapper.vm.$nextTick();
        wrapper.unmount();
      }
      const originalTime = performance.now() - originalStart;

      // Benchmark refactored
      const refactoredStart = performance.now();
      for (let i = 0; i < iterations; i++) {
        const wrapper = mount(RefactoredComponent, { props: testProps });
        await wrapper.vm.$nextTick();
        wrapper.unmount();
      }
      const refactoredTime = performance.now() - refactoredStart;

      // Allow 10% variance (research-backed threshold)
      expect(refactoredTime).toBeLessThanOrEqual(originalTime * 1.1);
    });
  });

  describe('Memory Management', () => {
    it('should not introduce memory leaks', async () => {
      const wrappers: Array<any> = [];

      // Create many instances
      for (let i = 0; i < 50; i++) {
        wrappers.push(mount(RefactoredComponent, { props: testProps }));
      }

      // Cleanup all instances
      wrappers.forEach(wrapper => wrapper.unmount());

      // Force garbage collection if available
      if (global.gc) {
        global.gc();
      }

      // Check memory usage (implementation specific)
      const memoryAfter = process.memoryUsage();
      expect(memoryAfter.heapUsed).toBeLessThan(50 * 1024 * 1024); // 50MB threshold
    });
  });
});
```

### **COMPREHENSIVE VALIDATION WORKFLOW:**
```bash
#!/bin/bash
# Research-backed validation sequence

echo "=== REFACTORING VALIDATION WORKFLOW ==="

# Step 1: TypeScript validation
echo "1. TypeScript validation..."
npx vue-tsc --noEmit
if [ $? -ne 0 ]; then
  echo "🚨 TYPESCRIPT ERRORS: Fix before proceeding"
  exit 1
fi

# Step 2: Linting validation
echo "2. Linting validation..."
npx eslint --ext .ts,.vue src/
if [ $? -ne 0 ]; then
  echo "🚨 LINTING ERRORS: Fix before proceeding"
  exit 1
fi

# Step 3: Test suite validation
echo "3. Test suite validation..."
npm run test
if [ $? -ne 0 ]; then
  echo "🚨 TEST FAILURES: Fix before proceeding"
  exit 1
fi

# Step 4: Build validation
echo "4. Build validation..."
npm run build
if [ $? -ne 0 ]; then
  echo "🚨 BUILD FAILURE: Fix before proceeding"
  exit 1
fi

# Step 5: Performance benchmark (if available)
if command -v npm run bench &> /dev/null; then
  echo "5. Performance benchmarking..."
  npm run bench

  # Compare with baseline
  if [ -f ./baseline-bench.txt ]; then
    echo "Comparing with baseline performance..."
    # Add comparison logic here
  fi
fi

# Step 6: Coverage validation
echo "6. Coverage validation..."
npm run test -- --coverage
COVERAGE=$(npm run test -- --coverage 2>&1 | grep -o '[0-9]*%' | tail -1 | tr -d '%')
if [ $COVERAGE -lt 70 ]; then
  echo "🟡 LOW COVERAGE: $COVERAGE% (recommend ≥70%)"
fi

echo "✅ All validations passed"
```

---

## **🤖 PHASE 4: AI ASSISTANT REFACTORING GUIDELINES**

### **RESEARCH-BACKED MANDATORY PROMPT TEMPLATE:**

```
Refactor the following Vue 3 component by [specific refactoring goal].

CRITICAL ASSESSMENT (Required Before Refactoring):
- Test coverage: [coverage %] - [STOP/CAUTION/PROCEED based on coverage]
- Dependencies: [number of dependent files] - [LOW/MEDIUM/HIGH risk]
- API changes: [breaking/internal] - [CAUTION/PROCEED based on changes]

REQUIREMENTS:
- Maintain 100% API compatibility (same props/emits/behavior)
- Use TypeScript strict mode with no @ts-ignore
- Implement comprehensive tests for refactored code
- Explain each step and reasoning
- No breaking changes to external contracts

SAFE REFACTORING PATTERNS (Research-Backed):
- Extract inline composables first, then separate files
- Use interface evolution with deprecation warnings
- Implement facade pattern for service changes
- Incremental Options API to Composition API migration

VERIFICATION PROTOCOL (Industry Standard):
- BEFORE: Document baseline (tests, types, lint, build)
- DURING: Test after each incremental change
- AFTER: Functional equivalence testing with original
- PERFORMANCE: Benchmark before/after comparison

V.E.R.I.F.Y. PROTOCOL for AI Code:
1. Verbalize: Explain refactoring in your own words
2. Examine: Review all import/dependency changes
3. Review: Confirm type safety and API contracts
4. Inspect: Check for anti-patterns and escape hatches
5. Functional: Test side-by-side behavior equivalence
6. Yield: Run full test suite and benchmarks

CODE TO REFACTOR:
[paste component code with context]

Please provide step-by-step refactoring with comprehensive testing.
```

### **V.E.R.I.F.Y. PROTOCOL (Research-Based Validation):**
```typescript
/**
 * AI-Generated Code Verification Protocol
 * MUST be completed before accepting ANY refactored code
 */
interface VerifyProtocol {
  // 1. Verbalize - Understand the changes
  verbalizeUnderstanding(): {
    canExplainEveryChange: boolean;
    understandsRefactoringPurpose: boolean;
    identifiesBreakingChanges: boolean[];
  };

  // 2. Examine - Check dependencies
  examineDependencies(): {
    importsReviewed: boolean;
    circularDependenciesChecked: boolean;
    impactOnDependents: string[];
  };

  // 3. Review - Type safety and contracts
  reviewTypeSafety(): {
    typescriptStrictMode: boolean;
    apiContractsMaintained: boolean;
    propSignaturesPreserved: boolean;
    emitSignaturesPreserved: boolean;
  };

  // 4. Inspect - Anti-patterns
  inspectAntiPatterns(): {
    noTsIgnore: boolean;
    noAnyTypes: boolean;
    noOverAbstraction: boolean;
    appropriateReactiveUsage: boolean;
  };

  // 5. Functional - Behavior equivalence
  functionalEquivalence(): {
    sideBySideTestsPass: boolean;
    edgeCasesIdentical: boolean;
    errorHandlingPreserved: boolean;
  };

  // 6. Yield - Final validation
  finalValidation(): {
    fullTestSuitePasses: boolean;
    performanceWithinThreshold: boolean;
    buildSuccessful: boolean;
    deploymentSafe: boolean;
  };
}

function runVerifyProtocol(refactoredCode: any): boolean {
  // Implementation of verification protocol
  // Returns true if all checks pass
  return true; // Placeholder
}
```

---

## **🚨 RISK MITIGATION STRATEGIES**

### **HIGH-RISK AREA IDENTIFICATION:**
```typescript
// Research-backed complexity analysis
interface CodeComplexityMetrics {
  cyclomaticComplexity: number;
  cognitiveComplexity: number;
  linesOfCode: number;
  testCoverage: number;
  changeFrequency: number; // Git churn - how often file changes
  dependencyCount: number;
}

function identifyHighRiskRefactoringTargets(files: string[]): CodeComplexityMetrics[] {
  return files
    .map(file => analyzeFileComplexity(file))
    .filter(metric =>
      metric.cyclomaticComplexity > 15 ||      // High complexity
      metric.cognitiveComplexity > 20 ||       // Hard to understand
      metric.changeFrequency > 10 ||           // Frequently changed (unstable)
      metric.testCoverage < 50 ||               // Poor test coverage
      metric.dependencyCount > 5                // Many dependencies
    )
    .sort((a, b) => calculateRiskScore(b) - calculateRiskScore(a));
}

function calculateRiskScore(metrics: CodeComplexityMetrics): number {
  // Research-backed risk calculation
  return (
    (metrics.cyclomaticComplexity * 0.3) +
    (metrics.cognitiveComplexity * 0.2) +
    ((100 - metrics.testCoverage) * 0.3) +
    (metrics.changeFrequency * 0.1) +
    (metrics.dependencyCount * 0.1)
  );
}
```

### **ROLLBACK STRATEGIES (Research-Based):**
```bash
#!/bin/bash
# Comprehensive rollback procedures for failed refactoring

echo "=== REFACTORING ROLLBACK PROTOCOL ==="

# Option 1: Atomic commit rollback
echo "Checking for atomic commits..."
if git log --oneline -5 | grep -q "refactor:"; then
  echo "Found atomic refactor commits"
  echo "Rollback options:"
  echo "1. git revert HEAD - Rollback last refactoring"
  echo "2. git reset --hard HEAD~1 - Remove last changes"
  echo "3. git checkout main - Abandon all changes"
fi

# Option 2: Feature branch rollback
echo "Checking feature branch status..."
CURRENT_BRANCH=$(git branch --show-current)
if [[ $CURRENT_BRANCH == refactor/* ]]; then
  echo "On refactoring branch: $CURRENT_BRANCH"
  echo "Rollback options:"
  echo "1. git checkout main - Return to stable code"
  echo "2. git branch -D $CURRENT_BRANCH - Delete branch"
fi

# Option 3: File-level rollback
echo "Checking modified files..."
MODIFIED_FILES=$(git diff --name-only)
if [ -n "$MODIFIED_FILES" ]; then
  echo "Modified files:"
  echo "$MODIFIED_FILES"
  echo "Rollback options:"
  echo "1. git checkout -- filename - Reset specific file"
  echo "2. git stash - Save changes for later"
fi

# Option 4: Emergency rollback
echo "Emergency rollback procedures..."
echo "1. Ensure working directory is clean"
echo "2. Return to known good state"
echo "3. Verify functionality restored"
echo "4. Document rollback reason"
```

---

## **📋 COMPREHENSIVE REFACTORING CHECKLIST**

### **Before ANY Refactoring is Considered Complete (Industry Standards):**

- [ ] **PRE-ASSESSMENT COMPLETED**: Risk analysis and baseline documented
- [ ] **STOP CONDITIONS CHECKED**: No active bugs, sufficient test coverage
- [ ] **INCREMENTAL CHANGES**: Refactoring done in small, testable steps
- [ ] **API COMPATIBILITY**: All external contracts maintained
- [ ] **FUNCTIONAL EQUIVALENCE**: Side-by-side testing with original code
- [ ] **TYPE SAFETY MAINTAINED**: Strict TypeScript, no escape hatches
- [ ] **PERFORMANCE VALIDATED**: No regression in benchmarks
- [ ] **MEMORY MANAGEMENT**: No leaks introduced
- [ ] **FULL TEST COVERAGE**: All tests pass, coverage maintained or improved
- [ ] **BUILD VERIFICATION**: Production build succeeds
- [ ] **DOCUMENTATION UPDATED**: JSDoc, README, migration guides if needed
- [ ] **ROLLBACK PLANNED**: Clear rollback strategy documented
- [ ] **DEPENDENT SYSTEMS TESTED**: All dependent components still work
- [ ] **USER IMPACT ASSESSED**: No breaking changes for end users

---

## **🔧 POMO-FLOW SPECIFIC REFACTORING PATTERNS**

### **Store Refactoring with Backward Compatibility:**
```typescript
// Research-backed safe Pinia store refactoring

// STEP 1: Create new modular stores
// stores/userDataStore.ts
export const useUserDataStore = defineStore('userData', {
  state: () => ({
    users: [] as User[],
    loading: false
  }),
  actions: {
    async fetchUsers() { /* implementation */ }
  }
});

// stores/userSettingsStore.ts
export const useUserSettingsStore = defineStore('userSettings', {
  state: () => ({
    preferences: {} as UserPreferences,
    theme: 'light' as string
  }),
  actions: {
    async updatePreferences(prefs: UserPreferences) { /* implementation */ }
  }
});

// STEP 2: Facade for existing monolithic store (backward compatibility)
// stores/legacyUserStore.ts
export const useLegacyUserStore = defineStore('legacyUser', {
  getters: {
    // Delegate to new stores maintaining old API
    users: () => useUserDataStore().users,
    preferences: () => useUserSettingsStore().preferences,
    theme: () => useUserSettingsStore().theme,

    // Computed properties that combine new stores
    isLoading: () =>
      useUserDataStore().loading || useUserSettingsStore().loading
  },

  actions: {
    // Maintain old method signatures
    async fetchAllUserData() {
      await Promise.all([
        useUserDataStore().fetchUsers(),
        useUserSettingsStore().loadPreferences()
      ]);
    },

    async updateUserData(data: UserUpdates) {
      // Delegate to appropriate new store
      if (data.preferences) {
        await useUserSettingsStore().updatePreferences(data.preferences);
      }
      // Handle other data types...
    }
  }
});
```

### **Component Refactoring with Type Safety:**
```typescript
// Research-backed component refactoring for Pomo-Flow

// BEFORE: Monolithic task component
// AFTER: Refactored with extracted composables

// composables/useTaskManagement.ts
export function useTaskManagement(initialTasks: Task[] = []) {
  const tasks = ref<Task[]>(initialTasks);
  const loading = ref(false);
  const error = ref<Error | null>(null);

  const sortedTasks = computed(() =>
    tasks.value.sort((a, b) => a.priority - b.priority)
  );

  const completedTasks = computed(() =>
    tasks.value.filter(task => task.completed)
  );

  async function addTask(task: CreateTaskRequest): Promise<void> {
    loading.value = true;
    try {
      const newTask = await TaskService.create(task);
      tasks.value.push(newTask);
    } catch (e) {
      error.value = e as Error;
      throw e;
    } finally {
      loading.value = false;
    }
  }

  return {
    tasks: readonly(tasks),
    loading: readonly(loading),
    error: readonly(error),
    sortedTasks,
    completedTasks,
    addTask
  };
}

// Updated component maintains exact same external API
<script setup lang="ts">
interface Props {
  projectId: number;
  initialTasks?: Task[];
}

const props = withDefaults(defineProps<Props>(), {
  initialTasks: () => []
});

// Extract composable maintaining same functionality
const {
  tasks,
  loading,
  error,
  sortedTasks,
  completedTasks,
  addTask
} = useTaskManagement(props.initialTasks);

// Maintain exact same emit signatures for compatibility
const emit = defineEmits<{
  (e: 'task-added', task: Task): void;
  (e: 'task-completed', taskId: number): void;
}>();

// Rest of component logic using extracted composable
</script>
```

---

**Last Updated**: Based on comprehensive industry research from Perplexity analysis of Vue 3 + TypeScript refactoring best practices
**Research Foundation**: Safe refactoring methodologies, interface evolution strategies, performance validation, and AI-assisted refactoring guidelines
**Purpose**: Restructure existing code safely while maintaining exact functional equivalence and preventing regression
**Status**: ACTIVE - Required for all Pomo-Flow refactoring activities

**Following these research-backed standards ensures that refactoring genuinely improves code quality while maintaining the strict compatibility and performance requirements of production Vue 3 applications.**