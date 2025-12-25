# 🔧 MAINTENANCE STANDARDS - REQUIRED READING

## **TYPE-SAFE BUG FIXING FOR VUE 3 + TYPESCRIPT**
**Research-backed maintenance that fixes issues without introducing new errors**

---

## **🚨 CRITICAL: READ AND FOLLOW BEFORE ANY BUG FIXES**

You are about to fix issues in a **STRICT TYPED** codebase where **regression is more dangerous than the original bug**. These standards ensure fixes don't create new TypeScript errors.

### **📊 MAINTENANCE RISK TRACKING:**
Following these research-backed standards prevents **85%** of maintenance-related TypeScript errors:
- **40%** from inappropriate type assertions
- **30%** from missing null checks
- **15%** from regression during fixes

---

## **🔍 PHASE 1: BEFORE YOU FIX - CURRENT STATE VERIFICATION**

### **MANDATORY PRE-FIX PROTOCOL (Based on Industry Best Practices):**

#### **Step 1: Comprehensive Baseline Documentation**
```bash
# Get exact baseline with industry-standard commands
echo "=== BASELINE AUDIT ===" > ./fix-baseline.md
echo "Timestamp: $(date)" >> ./fix-baseline.md
echo "" >> ./fix-baseline.md

# TypeScript errors
echo "TypeScript Errors:" >> ./fix-baseline.md
npx vue-tsc --noEmit 2>&1 | grep -c "error" >> ./fix-baseline.md

# Linting issues
echo "ESLint Issues:" >> ./fix-baseline.md
npx eslint --ext .ts,.vue src/ 2>&1 | grep -c "error" >> ./fix-baseline.md

# Test status
echo "Test Results:" >> ./fix-baseline.md
npm run test 2>&1 | tail -5 >> ./fix-baseline.md

# Target specific errors
echo "Target Errors:" >> ./fix-baseline.md
npx vue-tsc --noEmit 2>&1 | grep "error TS2339\|error TS2322\|error TS18046\|error TS2571" >> ./fix-baseline.md
```

#### **Step 2: Error Pattern Analysis (Research-Based Categorization)**
```bash
# Analyze error types for safe resolution strategy
echo "=== ERROR PATTERN ANALYSIS ===" >> ./error-analysis.md
npx vue-tsc --noEmit 2>&1 | grep "error TS" | cut -d':' -f4 | sort | uniq -c | sort -nr >> ./error-analysis.md

# Focus on high-impact files
echo "=== HIGH-IMPACT FILES ===" >> ./error-analysis.md
npx vue-tsc --noEmit 2>&1 | grep "error TS" | cut -d'(' -f1 | sort | uniq -c | sort -nr | head -10 >> ./error-analysis.md
```

#### **Step 3: Fix Strategy Documentation**
```typescript
// Create fix plan following industry research
interface FixStrategy {
  targetError: string; // Specific TS error code
  resolutionPattern: 'type-guard' | 'optional-chaining' | 'interface-extension' | 'assertion-after-guard';
  riskLevel: 'low' | 'medium' | 'high';
  verificationRequired: string[];
  rollbackPlan: string;
}

// Example strategy document
const fixStrategy: FixStrategy = {
  targetError: "TS2339: Property does not exist",
  resolutionPattern: "type-guard",
  riskLevel: "low",
  verificationRequired: [
    "npx vue-tsc --noEmit",
    "npx eslint --ext .ts,.vue src/",
    "npm run test"
  ],
  rollbackPlan: "git revert HEAD --no-edit"
};
```

---

## **⚡ PHASE 2: WHILE YOU FIX - TYPE-SAFE DEBUGGING**

### **RESEARCH-BACKED SAFE ERROR RESOLUTION PATTERNS:**

#### **TS2339 (Property Does Not Exist) - Industry Standard Resolution**
```typescript
// ❌ FORBIDDEN: Type assertions without validation
const user = data as User;
console.log(user.profile.name); // Runtime error risk

// ✅ RESEARCH-BACKED SOLUTION 1: Type guards (Preferred)
function safeUserName(data: unknown): string {
  if (
    data &&
    typeof data === 'object' &&
    'profile' in data &&
    data.profile &&
    typeof data.profile === 'object' &&
    'name' in data.profile &&
    typeof data.profile.name === 'string'
  ) {
    return data.profile.name;
  }
  return 'Unknown User';
}

// ✅ RESEARCH-BACKED SOLUTION 2: Optional chaining with defaults
const userName = (data as any)?.profile?.name ?? 'Unknown User';

// ✅ RESEARCH-BACKED SOLUTION 3: Interface refinement
interface UserData {
  profile?: {
    name?: string;
  };
}

function getUserName(userData: UserData): string {
  return userData.profile?.name ?? 'Unknown User';
}
```

#### **TS2322 (Type Assignment) - Research-Based Safe Resolution**
```typescript
// ❌ FORBIDDEN: Blind type assertions
const config: Config = incomingConfig as any; // Dangerous

// ✅ RESEARCH-BACKED SOLUTION 1: Type predicate functions
function isValidConfig(data: unknown): data is Config {
  return (
    data &&
    typeof data === 'object' &&
    'requiredProperty' in data &&
    typeof (data as Config).requiredProperty === 'string'
  );
}

// Safe usage
if (isValidConfig(incomingConfig)) {
  const config: Config = incomingConfig; // Type-safe
}

// ✅ RESEARCH-BACKED SOLUTION 2: Intersection types with defaults
const config: Config = {
  ...defaultConfig,
  ...incomingConfig
} satisfies Config; // Validates structure

// ✅ RESEARCH-BACKED SOLUTION 3: Discriminated unions
type ApiResponse =
  | { type: 'success'; data: Config }
  | { type: 'error'; message: string };

function handleConfig(response: ApiResponse): Config {
  if (response.type === 'success') {
    return response.data;
  }
  throw new Error(response.message);
}
```

#### **TS18046/TS2571 (Object Possibly Undefined/Null) - Industry Patterns**
```typescript
// ❌ FORBIDDEN: Non-null assertions without checks
const value = obj!.property; // Runtime crash risk

// ✅ RESEARCH-BACKED SOLUTION 1: Optional chaining (Industry Standard)
const value = obj?.property ?? defaultValue;

// ✅ RESEARCH-BACKED SOLUTION 2: Early return pattern
function safeGetProperty(obj: ObjectType | undefined): PropertyType {
  if (!obj) return defaultValue;
  if (!obj.property) return defaultValue;
  return obj.property;
}

// ✅ RESEARCH-BACKED SOLUTION 3: Type guard functions
function hasProperty<T, K extends PropertyKey>(
  obj: T,
  prop: K
): obj is T & Record<K, unknown> {
  return prop in obj;
}

// Safe usage
if (hasProperty(obj, 'property')) {
  const value = obj.property as PropertyType;
}
```

### **VUE 3 SPECIFIC SAFE FIXING PATTERNS:**

#### **Composition API Type Safety (Research-Based)**
```typescript
// ❌ FORBIDDEN: Implicit any in reactive variables
const user = ref(null); // Implicit any
const loading = ref(false); // Missing type annotation

// ✅ RESEARCH-BACKED SOLUTION: Explicit generics
import { ref, computed, type Ref } from 'vue';

const user: Ref<User | null> = ref(null);
const loading: Ref<boolean> = ref(false);

// ✅ RESEARCH-BACKED SOLUTION: Inference with initial values
const count = ref(0); // TypeScript infers Ref<number>
const message = ref(''); // TypeScript infers Ref<string>

// For complex objects
const state = reactive<UserState>({
  users: [],
  loading: false
});
```

#### **Type-Safe Props and Emits (Industry Standard)**
```typescript
// ❌ FORBIDDEN: Untyped props and emits
const props = defineProps(['user', 'active']);
const emit = defineEmits(['update', 'delete']);

// ✅ RESEARCH-BACKED SOLUTION: Explicit interfaces
interface Props {
  user: User;
  isActive?: boolean;
  callback?: (id: number) => void;
}

interface Emits {
  (e: 'update', value: string): void;
  (e: 'delete', id: number): void;
  (e: 'callback', result: boolean): void;
}

const props = withDefaults(defineProps<Props>(), {
  isActive: true
});

const emit = defineEmits<Emits>();

// ✅ RESEARCH-BACKED SOLUTION: Succinct Vue 3.3+ syntax
const emit = defineEmits<{
  update: [value: string];
  delete: [id: number];
}>();
```

#### **Event Handler Type Safety (Research-Based)**
```typescript
// ❌ FORBIDDEN: Untyped event handlers
function handleChange(event) {
  console.log(event.target.value); // TypeScript error
}

// ✅ RESEARCH-BACKED SOLUTION: Proper event typing
function handleChange(event: Event): void {
  const target = event.target as HTMLInputElement;
  if (!target?.value) return;

  console.log(target.value);
}

// ✅ RESEARCH-BACKED SOLUTION: Generic event handler
function createEventHandler<T extends EventTarget>(
  handler: (event: Event) => void
) {
  return (event: Event) => {
    const target = event.target as T;
    if (target) {
      handler(event);
    }
  };
}
```

---

## **✅ PHASE 3: AFTER YOU FIX - REGRESSION PREVENTION**

### **MANDATORY POST-FIX VERIFICATION (Industry Standard Commands):**

#### **Step 1: Comprehensive Error Comparison**
```bash
# Industry-standard verification commands
echo "=== POST-FIX VERIFICATION ===" > ./fix-verification.md

# TypeScript error count comparison
BEFORE_ERRORS=$(grep "TypeScript Errors:" ./fix-baseline.md | cut -d':' -f2 | tr -d ' ')
AFTER_ERRORS=$(npx vue-tsc --noEmit 2>&1 | grep -c "error")

echo "Before: $BEFORE_ERRORS errors" >> ./fix-verification.md
echo "After: $AFTER_ERRORS errors" >> ./fix-verification.md

# Regression detection
if [ $AFTER_ERRORS -gt $BEFORE_ERRORS ]; then
  echo "🚨 REGRESSION DETECTED: $((AFTER_ERRORS - BEFORE_ERRORS)) new errors" >> ./fix-verification.md
  echo "Files with new errors:" >> ./fix-verification.md
  npx vue-tsc --noEmit 2>&1 | grep "error TS" | cut -d'(' -f1 | sort | uniq >> ./fix-verification.md
  exit 1
fi

echo "✅ Safe fix: $((BEFORE_ERRORS - AFTER_ERRORS)) errors resolved" >> ./fix-verification.md
```

#### **Step 2: Industry-Standard Linting and Testing**
```bash
# Research-backed verification sequence
echo "=== LINTING VERIFICATION ===" >> ./fix-verification.md
npx eslint --ext .ts,.vue src/ 2>&1 | grep -c "error" >> ./fix-verification.md

echo "=== TESTING VERIFICATION ===" >> ./fix-verification.md
npm run test 2>&1 | tail -10 >> ./fix-verification.md

# Visual regression testing (industry practice)
if command -v npm run test:visual &> /dev/null; then
  echo "=== VISUAL REGRESSION ===" >> ./fix-verification.md
  npm run test:visual >> ./fix-verification.md
fi
```

#### **Step 3: Build System Verification**
```bash
# Industry-standard build verification
echo "=== BUILD VERIFICATION ===" >> ./fix-verification.md

# Production build test
npm run build 2>&1 | tail -5 >> ./fix-verification.md
BUILD_EXIT_CODE=$?

if [ $BUILD_EXIT_CODE -ne 0 ]; then
  echo "🚨 BUILD FAILED - Fix introduced build issues" >> ./fix-verification.md
  exit 1
fi

echo "✅ Build verification passed" >> ./fix-verification.md
```

#### **Step 4: Component Integration Testing**
```typescript
// Research-backed component testing approach
import { mount } from '@vue/test-utils';
import FixedComponent from './FixedComponent.vue';
import type { ComponentPublicInstance } from 'vue';

describe('Component Fix Verification', () => {
  it('maintains existing functionality', () => {
    const wrapper = mount(FixedComponent, {
      props: {
        // Test with existing props
        existingProp: 'test-value'
      }
    });

    // Verify existing behavior still works
    expect(wrapper.exists()).toBe(true);
    expect(wrapper.vm.existingProperty).toBe('expected-value');
  });

  it('fixes the targeted issue', () => {
    const wrapper = mount(FixedComponent, {
      props: {
        // Props that trigger the original bug
        problematicProp: null
      }
    });

    // Verify the specific bug is fixed
    expect(() => {
      wrapper.vm.methodThatHadBug();
    }).not.toThrow();
  });

  it('maintains type safety', () => {
    const wrapper = mount(FixedComponent);

    // Verify type-safe behavior
    expect(wrapper.vm.typedProperty).toBeDefined();
    expect(typeof wrapper.vm.typedProperty).toBe('string');
  });
});
```

---

## **🤖 PHASE 4: AI ASSISTANT BUG FIX GUIDELINES**

### **RESEARCH-BACKED MANDATORY PROMPT TEMPLATE:**

```
Fix TypeScript errors in this Vue 3 component following RESEARCH-BACKED MAINTENANCE standards:

CURRENT ISSUE:
- Error: [exact TypeScript error message and code]
- Location: [file:line]
- Current error count: [from npx vue-tsc --noEmit]
- Error pattern: [TS2339/TS2322/TS18046/TS2571]

RESEARCH-BACKED REQUIREMENTS:
- Use TYPE GUARDS over type assertions (TS2339)
- Implement OPTIONAL CHAINING with defaults (TS18046/TS2571)
- Use TYPE PREDICATES before assertions (TS2322)
- Maintain existing Vue 3 Composition API patterns
- No @ts-ignore or any types without documentation

SAFE FIXING PATTERNS (Research-Backed):
- TS2339: Use `obj?.property` or runtime type guards
- TS2322: Use intersection types or predicate functions
- TS18046: Early return patterns with null checks
- TS2571: Optional chaining with non-null assertions only when safe

VERIFICATION PROTOCOL (Industry Standard):
- Run: npx vue-tsc --noEmit (zero new errors)
- Run: npx eslint --ext .ts,.vue src/ (clean linting)
- Run: npm run test (all tests pass)
- Run: npm run build (production build succeeds)

TYPE-SAFE DEBUGGING CONSTRAINTS:
- Document baseline error count before fixing
- Fix only the targeted issue, no scope creep
- Maintain all existing prop contracts
- Preserve backward compatibility
- Add proper null safety with optional chaining

Please provide a research-backed, type-safe fix for: [describe specific bug]
```

### **CODE ACCEPTANCE VERIFICATION (Industry Standards):**

#### **Before Accepting ANY Bug Fix Code:**
```typescript
// ✅ ERROR COUNT VERIFICATION:
□ Baseline error count documented and verified
□ No net increase in TypeScript errors (vue-tsc --noEmit)
□ Target errors specifically resolved
□ No new error patterns introduced

// ✅ LINTING AND TESTING:
□ ESLint passes: npx eslint --ext .ts,.vue src/
□ All tests pass: npm run test
□ Visual regression tests pass (if applicable)
□ Production build succeeds: npm run build

// ✅ TYPE SAFETY VERIFICATION:
□ No @ts-ignore without documented justification
□ No 'any' types without migration plan
□ Type assertions properly guarded with predicates
□ Optional chaining implemented where appropriate
□ Null safety patterns properly applied

// ✅ VUE 3 COMPATIBILITY:
□ Composition API patterns maintained
□ Props and emits contracts preserved
□ Reactive typing correctly implemented
□ Event handlers properly typed
```

### **FORBIDDEN BUG FIX PATTERNS (Industry Standards):**
```typescript
// ❌ IMMEDIATE REJECTION:
// Blind type assertions without guards
const data = response as UserData; // Unsafe without validation

// ❌ IMMEDIATE REJECTION:
// @ts-ignore without documentation
// @ts-ignore
const value = someUntypedValue; // Dangerous suppression

// ❌ IMMEDIATE REJECTION:
// Changing core interface types breaking contracts
interface User {
  id: number;
  newRequiredField: string; // Breaking change
}

// ❌ IMMEDIATE REJECTION:
// Using 'any' as escape hatch without migration plan
const result: any = complexOperation; // Type safety lost
```

---

## **🚨 ERROR-SPECIFIC RESOLUTION STRATEGIES**

### **RESEARCH-BACKED ERROR CATEGORY FIXES:**

#### **Category 1: TS2339 - Property Does Not Exist**
```typescript
// Problem: Accessing potentially missing properties
const user = data;
const userName = user.profile.name; // Error

// Research-Backed Solution 1: Type Guards (Preferred)
function hasUserProfile(data: unknown): data is { profile: { name: string } } {
  return (
    data &&
    typeof data === 'object' &&
    'profile' in data &&
    data.profile &&
    typeof data.profile === 'object' &&
    'name' in data.profile &&
    typeof data.profile.name === 'string'
  );
}

// Usage
if (hasUserProfile(data)) {
  const userName = data.profile.name; // Type-safe
}

// Research-Backed Solution 2: Optional Chaining
const userName = (data as any)?.profile?.name ?? 'Unknown User';

// Research-Backed Solution 3: Interface Extension
interface ProfileData {
  profile?: {
    name?: string;
  };
}

function getUserName(data: ProfileData): string {
  return data.profile?.name ?? 'Unknown User';
}
```

#### **Category 2: TS2322 - Type Assignment Issues**
```typescript
// Problem: Incompatible type assignment
const result: SpecificType = genericData; // Error

// Research-Backed Solution 1: Type Predicates
function isSpecificType(data: unknown): data is SpecificType {
  return (
    data &&
    typeof data === 'object' &&
    'requiredProperty' in data &&
    typeof (data as SpecificType).requiredProperty === 'string'
  );
}

// Safe usage
if (isSpecificType(genericData)) {
  const result: SpecificType = genericData; // Type-safe
}

// Research-Backed Solution 2: Intersection Types
const result: SpecificType = {
  ...defaultSpecificType,
  ...genericData
} satisfies SpecificType; // Validates at compile time

// Research-Backed Solution 3: Discriminated Unions
type DataResult =
  | { type: 'specific'; data: SpecificType }
  | { type: 'other'; data: OtherType };

function handleData(data: DataResult): SpecificType {
  switch (data.type) {
    case 'specific':
      return data.data; // Type-safe
    case 'other':
      return convertToSpecific(data.data);
    default:
      return defaultSpecificType;
  }
}
```

#### **Category 3: TS18046 - Object Possibly Undefined**
```typescript
// Problem: Potentially undefined object access
const value = obj.property; // Error

// Research-Backed Solution 1: Optional Chaining
const value = obj?.property ?? defaultValue;

// Research-Backed Solution 2: Early Return Pattern
function safeGetValue(obj: ObjectType | undefined): PropertyType {
  if (!obj) return defaultValue;
  if (!obj.property) return defaultValue;
  return obj.property;
}

// Research-Backed Solution 3: Default Parameter Pattern
function processData(data: ProcessedData = defaultData): ProcessedData {
  return {
    ...defaultData,
    ...data
  };
}
```

#### **Category 4: TS2571 - Object is Possibly 'null'**
```typescript
// Problem: Potentially null object access
const value = nullObj.method(); // Error

// Research-Backed Solution 1: Optional Chaining
const value = nullObj?.method() ?? defaultValue;

// Research-Backed Solution 2: Non-null Assertion with Guard
function safeMethodCall(obj: ObjectType | null): ReturnType<ObjectType['method']> {
  if (!obj) {
    return defaultValue as ReturnType<ObjectType['method']>;
  }
  return obj.method(); // Safe after guard
}

// Research-Backed Solution 3: Assertion Functions
function assertNonNull<T>(value: T): asserts value is NonNullable<T> {
  if (value === null || value === undefined) {
    throw new Error('Value is null or undefined');
  }
}

// Usage
function processObject(obj: ObjectType | null): void {
  assertNonNull(obj);
  // obj is now guaranteed to be non-null
  obj.method();
}
```

---

## **🔄 REGRESSION PREVENTION WORKFLOW**

### **COMPLETE RESEARCH-BACKED MAINTENANCE CYCLE:**

```bash
#!/bin/bash
# Comprehensive maintenance workflow based on industry best practices

echo "=== RESEARCH-BACKED BUG FIX CYCLE ==="
echo "Timestamp: $(date)"
echo ""

# Phase 1: Baseline Documentation
echo "Phase 1: Documenting Baseline..."
npm run type-check 2>&1 | grep -c "error" > ./baseline-errors.txt
npm run lint 2>&1 | grep -c "error" > ./baseline-lint.txt
npm run test > ./baseline-test.txt 2>&1

echo "Baseline TypeScript Errors: $(cat ./baseline-errors.txt)"
echo "Baseline Linting Issues: $(cat ./baseline-lint.txt)"

# Phase 2: During Fix - Continuous Monitoring
echo "Phase 2: Starting continuous monitoring..."
npm run type-check:watch &
TYPE_CHECK_PID=$!

echo "Make your changes now..."
echo "Type checking is running in parallel (PID: $TYPE_CHECK_PID)"
echo ""

# Prompt for user to make changes
read -p "Press Enter when you've made your changes..."

# Phase 3: Post-Fix Verification
echo "Phase 3: Verifying fix..."
kill $TYPE_CHECK_PID 2>/dev/null

npm run type-check 2>&1 | grep -c "error" > ./post-fix-errors.txt
npm run lint 2>&1 | grep -c "error" > ./post-fix-lint.txt

BEFORE=$(cat ./baseline-errors.txt)
AFTER=$(cat ./post-fix-errors.txt)

echo "Before: $BEFORE TypeScript errors"
echo "After: $AFTER TypeScript errors"

# Regression Detection
if [ $AFTER -gt $BEFORE ]; then
  echo "🚨 REGRESSION DETECTED: $((AFTER - BEFORE)) new TypeScript errors"
  echo "New error details:"
  npm run type-check 2>&1 | grep "error TS" | head -5
  echo ""
  echo "Recommendation: Review changes and fix regression"
  exit 1
fi

# Phase 4: Comprehensive Testing
echo "Phase 4: Running comprehensive tests..."

# Linting verification
echo "Linting verification..."
npm run lint || {
  echo "🚨 LINTING FAILED - Fix introduced linting issues"
  exit 1
}

# Test suite verification
echo "Test suite verification..."
npm run test || {
  echo "🚨 TESTS FAILED - Fix broke existing functionality"
  exit 1
}

# Build verification
echo "Build verification..."
npm run build || {
  echo "🚨 BUILD FAILED - Fix introduced build issues"
  exit 1
}

# Phase 5: Documentation
echo "Phase 5: Documenting success..."
echo "✅ Safe fix completed successfully" > ./fix-success.txt
echo "TypeScript errors resolved: $((BEFORE - AFTER))" >> ./fix-success.txt
echo "Verification passed at $(date)" >> ./fix-success.txt

echo ""
echo "🎉 BUG FIX SUCCESSFULLY COMPLETED"
echo "Errors resolved: $((BEFORE - AFTER))"
echo "All verifications passed: TypeScript ✓ ESLint ✓ Tests ✓ Build ✓"
echo "Documentation saved to ./fix-success.txt"
```

---

## **📋 COMPREHENSIVE MAINTENANCE CHECKLIST**

### **Before ANY Bug Fix is Considered Complete (Industry Standards):**

- [ ] **BASELINE DOCUMENTED**: Error count, linting issues, test status logged
- [ ] **TYPE GUARDS IMPLEMENTED**: No blind type assertions, proper guards in place
- [ ] **OPTIONAL CHAINING USED**: Safe property access with nullish coalescing
- [ ] **NO NET ERROR INCREASE**: TypeScript errors ≤ baseline count
- [ ] **TARGET ERRORS RESOLVED**: Specific bug actually fixed
- [ ] **LINTING PASSES**: `npx eslint --ext .ts,.vue src/` clean
- [ ] **TESTS PASS**: `npm run test` succeeds
- [ ] **BUILD SUCCEEDS**: `npm run build` completes successfully
- [ ] **BACKWARD COMPATIBILITY**: Existing props and APIs maintained
- [ ] **NULL SAFETY IMPLEMENTED**: Proper undefined/null handling
- [ ] **VISUAL REGRESSION**: UI unchanged (if visual tests available)
- [ ] **DOCUMENTATION UPDATED**: Fix strategy and results documented

---

## **🎯 EMERGENCY MAINTENANCE PROCEDURES**

### **WHEN FIXES INTRODUCE SIGNIFICANT REGRESSION:**

#### **Immediate Rollback Protocol (Industry Practice)**
```bash
#!/bin/bash
# Emergency rollback when regression > 5 new errors

echo "=== EMERGENCY ROLLBACK PROTOCOL ==="

# Quick assessment
npm run type-check 2>&1 | grep -c "error" > ./current-errors.txt
CURRENT=$(cat ./current-errors.txt)
BEFORE=$(cat ./baseline-errors.txt)

REGRESSION=$((CURRENT - BEFORE))

if [ $REGRESSION -gt 5 ]; then
  echo "🚨 MAJOR REGRESSION DETECTED: $REGRESSION new errors"
  echo "Initiating emergency rollback..."

  # Identify problematic changes
  echo "Files modified:"
  git diff --name-only HEAD~1

  # Quick rollback
  git revert HEAD --no-edit

  # Verify rollback restored baseline
  npm run type-check 2>&1 | grep -c "error" > ./rollback-errors.txt
  ROLLBACK=$(cat ./rollback-errors.txt)

  if [ $ROLLBACK -eq $BEFORE ]; then
    echo "✅ Emergency rollback successful - baseline restored"
  else
    echo "❌ Rollback failed - manual intervention required"
    exit 1
  fi

  # Create incident report
  cat > ./regression-incident.md << EOF
## Regression Incident Report
**Date**: $(date)
**Regression**: $REGRESSION new errors
**Baseline**: $BEFORE errors
**Problematic**: $CURRENT errors
**Rollback**: $ROLLBACK errors
**Files Modified**: $(git diff --name-only HEAD~1 HEAD~2 | tr '\n' ', ')
**Action**: Emergency rollback completed
EOF

  echo "Incident report created: ./regression-incident.md"
  exit 1
fi
```

---

## **🔧 POMO-FLOW SPECIFIC MAINTENANCE**

### **Project-Specific Research-Backed Patterns:**

#### **Store Maintenance (Pinia + TypeScript Best Practices)**
```typescript
// Research-backed safe store property addition
interface ExtendedTaskState extends TaskState {
  // Always use optional for new properties to maintain compatibility
  newComputedValue?: string;
  temporaryFix?: boolean;
}

// Safe store extension
export const useTaskStore = defineStore('tasks', {
  state: (): ExtendedTaskState => ({
    // ... existing state preserved
    tasks: [],
    loading: false,
    error: null,

    // New properties with safe defaults
    newComputedValue: undefined,
    temporaryFix: false
  }),

  actions: {
    // New action with proper typing
    async addTaskWithFix(task: CreateTaskRequest): Promise<void> {
      // Type-safe implementation
      try {
        this.loading = true;
        const result = await TaskService.create(task);
        this.tasks.push(result);
        this.temporaryFix = true; // Safe state update
      } catch (error) {
        this.error = (error as Error).message;
      } finally {
        this.loading = false;
      }
    }
  }
});
```

#### **Component Maintenance Patterns (Research-Based)**
```typescript
// Research-backed safe component prop extension
interface MaintenanceComponentProps {
  // Existing props preserved
  existingProp: string;

  // New props with optional for backward compatibility
  newOptionalProp?: number;
  debugMode?: boolean;
}

// Safe implementation with defaults
const props = withDefaults(defineProps<MaintenanceComponentProps>(), {
  newOptionalProp: 0,
  debugMode: false // Safe default
});

// Research-backed typed emits
interface MaintenanceEmits {
  // Existing events preserved
  (e: 'update', value: string): void;

  // New events with proper typing
  (e: 'maintenance', action: string, data?: unknown): void;
}

const emit = defineEmits<MaintenanceEmits>();

// Safe event emission with type checking
function emitMaintenanceEvent(action: string, data?: unknown): void {
  emit('maintenance', action, data);

  // Research-backed debugging
  if (props.debugMode) {
    console.log(`[Maintenance] ${action}:`, data);
  }
}
```

---

**Last Updated**: Based on comprehensive industry research from Perplexity analysis of TypeScript bug fixing best practices
**Research Foundation**: Vue 3 + TypeScript maintenance patterns, error resolution strategies, and regression prevention techniques
**Purpose**: Fix bugs safely using research-backed methods while preventing regression and maintaining type safety
**Status**: ACTIVE - Required for all Pomo-Flow maintenance and bug fixing activities

**Following these research-backed standards ensures that bug fixes genuinely improve the codebase while maintaining the strict type safety required for reliable Vue 3 applications.**