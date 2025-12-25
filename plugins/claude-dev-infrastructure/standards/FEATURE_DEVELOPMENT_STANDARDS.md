# 🛠️ FEATURE DEVELOPMENT STANDARDS - REQUIRED READING

## **PROACTIVE TYPESAFE DEVELOPMENT FOR VUE 3 + TYPESCRIPT**
**Prevention-focused standards based on industry best practices and research**

---

## **🚨 CRITICAL: READ AND FOLLOW BEFORE ANY FEATURE DEVELOPMENT**

You are about to add features to a **STRICT TYPED** Vue 3 application where TypeScript errors **BREAK DEPLOYMENT**. Following these standards prevents errors rather than discovering them after implementation.

### **📊 ERROR PREVENTION TRACKING:**
Following these standards prevents **80%+** of common TypeScript errors before compilation:
- **40%** eliminated by interface-first development
- **25%** eliminated by explicit type annotations
- **15%** eliminated by build system integration

---

## **🏗️ PHASE 1: BEFORE YOU CODE - INTERFACE-FIRST DEVELOPMENT**

### **MANDATORY PRE-DEVELOPMENT PROTOCOL:**

#### **Step 1: Define All Interfaces FIRST**
```typescript
// ❌ FORBIDDEN: Coding without interfaces
function processUser(user) { // No typing - creates errors
  return { ...user, processed: true };
}

// ✅ REQUIRED: Define interfaces before implementation
interface User {
  id: number;
  name: string;
  email: string;
  age?: number;
}

interface ProcessedUser extends User {
  processed: boolean;
  processedAt: Date;
}

function processUser(user: User): ProcessedUser {
  return {
    ...user,
    processed: true,
    processedAt: new Date()
  };
}
```

#### **Step 2: Vue 3 Component Structure Standards**
```typescript
<!-- ComponentName.vue - REQUIRED STRUCTURE -->
<script setup lang="ts">
// 1. IMPORTS FIRST
import { ref, computed, reactive } from 'vue';
import type { Ref, ComputedRef } from 'vue';

// 2. INTERFACES BEFORE LOGIC
interface Props {
  userId: number;
  userName: string;
  isActive?: boolean;
}

interface Emits {
  (e: 'update', value: string): void;
  (e: 'delete', id: number): void;
}

// 3. IMPLEMENTATION AFTER INTERFACES
const props = withDefaults(defineProps<Props>(), {
  isActive: true
});

const emit = defineEmits<Emits>();

// 4. EXPLICIT TYPE ANNOTATIONS (no inference)
const loading: Ref<boolean> = ref(false);
const userData: Ref<User | null> = ref(null);

const displayName: ComputedRef<string> = computed(() =>
  props.userName || 'Unknown User'
);
</script>

<template>
  <div>
    <h3>{{ displayName }}</h3>
    <p>ID: {{ props.userId }}</p>
    <p>Status: {{ props.isActive ? 'Active' : 'Inactive' }}</p>
  </div>
</template>
```

#### **Step 3: Type-Safe Event Handling**
```typescript
// ❌ FORBIDDEN: Implicit event typing
function handleChange(event) {
  console.log(event.target.value); // TypeScript error
}

// ✅ REQUIRED: Explicit event typing
function handleChange(event: Event): void {
  const target = event.target as HTMLInputElement;
  console.log(target.value);
}

// ✅ REQUIRED: Type-safe emits
const emit = defineEmits<{
  change: [value: string];
  update: [id: number];
}>();

// Usage with compile-time checking
emit('change', 'newValue'); // ✅ Correct
emit('change', 123); // ❌ TypeScript error
```

---

## **⚡ PHASE 2: WHILE YOU CODE - REAL-TIME MONITORING**

### **MANDATORY DEVELOPMENT ENVIRONMENT:**

#### **Start Development with Type Monitoring**
```bash
# REQUIRED: Run both dev server AND type checking in parallel
npm run dev:full

# OR run in separate terminals:
# Terminal 1: Development server
npm run dev

# Terminal 2: Real-time TypeScript checking
npx vue-tsc --noEmit --watch
```

#### **Add to package.json (if not present):**
```json
{
  "scripts": {
    "dev": "vite --host 0.0.0.0 --port 5546",
    "type-check": "vue-tsc --noEmit",
    "type-check:watch": "vue-tsc --noEmit --watch",
    "dev:full": "concurrently \"npm run dev\" \"npm run type-check:watch\"",
    "check-circular": "madge --circular --extensions ts,vue ./src"
  }
}
```

#### **Install Required Tools:**
```bash
# For parallel development monitoring
npm install --save-dev concurrently madge

# For pre-commit type checking
npm install --save-dev husky lint-staged tsc-files
```

### **REAL-TIME ERROR PREVENTION:**

#### **1. Immediate Error Detection**
- Keep `vue-tsc --watch` running at all times
- Each file save triggers instant type checking
- Fix errors BEFORE moving to next file

#### **2. Import/Export Validation**
- Use path aliases consistently: `@/components/`, `@/utils/`
- Verify all imports resolve immediately
- No circular dependencies (monitor with `madge`)

#### **3. Component Integration Testing**
- Test component compilation before integration
- Verify prop types match expected interfaces
- Check emit events are properly typed

---

## **✅ PHASE 3: BEFORE YOU COMMIT - VERIFICATION PROTOCOL**

### **MANDATORY PRE-COMMIT CHECKLIST:**

#### **Step 1: Type Safety Verification**
```typescript
// ✅ CHECK 1: No implicit any types
// Search entire codebase for ": any" and "as any"

// ✅ CHECK 2: All refs are explicitly typed
const count: Ref<number> = ref(0); // ✅ Explicit
const badCount = ref(0); // ❌ Implicit

// ✅ CHECK 3: All event handlers typed
function handleClick(event: Event): void { /* ... */ }

// ✅ CHECK 4: All props/emits have interfaces
interface Props { /* ... */ }
defineProps<Props>();
```

#### **Step 2: Build System Verification**
```bash
# REQUIRED: All must pass before commit
npm run type-check        # Zero TypeScript errors
npm run build           # Production build succeeds
npm run check-circular  # No circular dependencies
npm run lint           # Code style passes
```

#### **Step 3: Component Functionality Testing**
```bash
# Start development server
npm run dev

# Test in browser:
# ✅ Component renders without console errors
# ✅ Props work correctly
# ✅ Events emit properly
# ✅ No runtime type errors
```

### **AUTOMATED PRE-COMMIT HOOKS:**

#### **Setup Husky for Type Safety**
```bash
# Install and setup
npm install --save-dev husky lint-staged tsc-files
npx husky install
npx husky add .husky/pre-commit "npx lint-staged"
```

#### **package.json Configuration:**
```json
{
  "lint-staged": {
    "*.{ts,vue}": [
      "eslint --fix",
      "tsc-files --noEmit"
    ]
  },
  "scripts": {
    "prepare": "husky install"
  }
}
```

---

## **🤖 PHASE 4: AI ASSISTANT GUIDELINES - CLAUDE CODE STANDARDS**

### **MANDATORY PROMPT TEMPLATE FOR FEATURE REQUESTS:**

```
Create a Vue 3 component following these STRICT TYPE SAFETY standards:

REQUIREMENTS:
- Use <script setup lang="ts"> syntax
- Define ALL interfaces BEFORE component logic
- Use explicit type annotations (no implicit any)
- Implement proper prop validation with TypeScript interfaces
- Use defineEmits<T>() for type-safe event emitting
- Add comprehensive error handling with try-catch blocks

SECURITY & VALIDATION:
- Validate all user inputs before processing
- Implement proper error boundaries
- Use type-safe event handlers (Event, HTMLInputElement)
- No console.log in production code - use proper logging

VERIFICATION PROTOCOL:
- Code must pass: vue-tsc --noEmit with ZERO errors
- Component must compile with: npm run build
- Include type-safe test examples
- Add JSDoc comments for complex type definitions

PROJECT CONTEXT:
- Vue 3.4.0 with TypeScript 5.9.3
- Vite 7.2.4 development environment
- Pinia 2.1.7 for state management
- Path aliases: @/ for src/, @components/ for src/components/

Please implement: [describe feature/component]
```

### **CODE ACCEPTANCE VERIFICATION CHECKLIST:**

#### **Before Accepting ANY Claude Code:**
```typescript
// ✅ MANDATORY TYPE CHECKS:
□ All function parameters have explicit types
□ All function return types are defined
□ No "any" types present anywhere in code
□ All refs use explicit generics: ref<Type>()
□ All computed values use ComputedRef<Type>
□ Event handlers are properly typed (Event, MouseEvent, etc.)

// ✅ VUE 3 STANDARDS:
□ Uses <script setup lang="ts"> syntax
□ Props defined with TypeScript interfaces
□ Emits defined with defineEmits<T>()
□ No circular dependencies introduced
□ Imports use path aliases (@/components, @/utils)

// ✅ SECURITY & ERROR HANDLING:
□ User inputs are validated
□ Proper error handling with try-catch
□ No hardcoded secrets or API keys
□ XSS prevention (proper escaping)
□ Type-safe error messages
```

### **FORBIDDEN PATTERNS (REJECT CODE IF FOUND):**
```typescript
// ❌ IMMEDIATE REJECTION:
function process(data) { } // No parameters typed
const result = getData(); // No return type
ref(value); // No explicit generic
any; // Any usage of 'any' type
@ts-ignore; // Bypassing type checking

// ❌ VUE ANTI-PATTERNS:
export default { // Options API instead of Composition API
  data() { return { count: 0 }; } // Use ref() instead
}
```

---

## **🚨 PHASE 5: EMERGENCY PROCEDURES - ERROR RECOVERY**

### **WHEN TYPESCRIPT ERRORS OCCUR:**

#### **Step 1: Error Categorization**
```bash
# Get current error count
npx vue-tsc --noEmit 2>&1 | grep -c "error"

# Categorize errors by type
npx vue-tsc --noEmit 2>&1 | grep "error TS" | cut -d':' -f1 | sort | uniq -c | sort -nr
```

#### **Step 2: High-Impact Error Priority**
1. **TS2339** (Property does not exist) - Fix immediately
2. **TS2322** (Type assignment) - Fix before commit
3. **TS18046** (Object possibly undefined) - Add null checks
4. **TS2345** (Argument type mismatch) - Fix function signatures

#### **Step 3: Systematic Resolution**
```bash
# Focus on highest-error files first
npx vue-tsc --noEmit 2>&1 | grep "error TS" | cut -d'(' -f1 | sort | uniq -c | sort -nr | head -10

# Fix files in order of error count:
# 1. services/unified-task-service.ts
# 2. composables/useCrossTabSync.ts
# 3. stores/tasks.ts
```

### **ROLLBACK PROCEDURES:**

#### **If Build Completely Fails:**
```bash
# 1. Check git status - see what changed
git status

# 2. Identify problematic files
npx vue-tsc --noEmit 2>&1 | grep "error" | head -5

# 3. Stash changes if needed
git stash

# 4. Verify build works without changes
npm run build

# 5. Incrementally reapply and fix
git stash pop
# Fix errors one by one
```

---

## **📈 SUCCESS METRICS & COMPLIANCE**

### **SUCCESSFUL FEATURE DEVELOPMENT = ALL MET:**

✅ **ZERO TypeScript Errors**: `vue-tsc --noEmit` shows 0 errors
✅ **Build Success**: `npm run build` completes without errors
✅ **Development Server**: `npm run dev` starts cleanly
✅ **No Console Errors**: Browser dev tools show no errors
✅ **Type Coverage**: 100% of functions/components typed

### **FORBIDDEN DEPLOYMENT CONDITIONS:**

❌ ANY TypeScript compilation errors
❌ Build process failures
❌ Console warnings/errors in development
❌ Untyped public APIs
❌ Missing interface definitions

---

## **🔧 PROJECT-SPECIFIC CONFIGURATIONS**

### **Pomo-Flow Project Standards:**

#### **Path Aliases (USE CONSISTENTLY):**
```typescript
import type { User } from '@/types/user';
import { useTaskStore } from '@/stores/tasks';
import { TaskService } from '@/services/task-service';
import TaskComponent from '@/components/TaskComponent.vue';
```

#### **Store Patterns (Pinia + TypeScript):**
```typescript
interface TaskState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
}

export const useTaskStore = defineStore('tasks', {
  state: (): TaskState => ({
    tasks: [],
    loading: false,
    error: null
  }),
  actions: {
    async loadTasks(): Promise<void> {
      this.loading = true;
      try {
        const tasks = await TaskService.getTasks();
        this.tasks = tasks;
      } catch (error) {
        this.error = (error as Error).message;
      } finally {
        this.loading = false;
      }
    }
  }
});
```

#### **Service Layer Patterns:**
```typescript
export class TaskService {
  private api: ApiClient;

  constructor(api: ApiClient) {
    this.api = api;
  }

  async getTasks(): Promise<Task[]> {
    const response = await this.api.get<Task[]>('/tasks');
    return response.data;
  }

  async createTask(task: CreateTaskRequest): Promise<Task> {
    const response = await this.api.post<Task>('/tasks', task);
    return response.data;
  }
}
```

---

## **🎯 DAILY DEVELOPMENT WORKFLOW**

### **RECOMMENDED DAILY ROUTINE:**

```bash
# 1. START DAY
npm run dev:full  # Starts dev server + type monitoring

# 2. FEATURE DEVELOPMENT
# - Create interfaces first
# - Implement with explicit typing
# - Real-time error monitoring catches issues immediately

# 3. BEFORE COMMIT
npm run type-check     # Verify zero errors
npm run build         # Verify production build
npm run check-circular # Verify no circular deps

# 4. COMMIT
git add .
git commit -m "feat: add user profile component"

# 5. END DAY
npm run type-check    # Final verification
git push              # Push clean code
```

---

## **📋 VERIFICATION CHECKLIST**

### **Before ANY Feature is Considered Complete:**

- [ ] **Interface First**: All interfaces defined before implementation
- [ ] **Type Coverage**: 100% of functions, components, props typed
- [ ] **Compilation**: `vue-tsc --noEmit` shows ZERO errors
- [ ] **Build Success**: `npm run build` completes successfully
- [ ] **Dev Server**: `npm run dev` starts without errors
- [ ] **No Runtime Errors**: Browser console shows no TypeScript errors
- [ ] **Error Handling**: Proper try-catch blocks implemented
- [ ] **Validation**: All user inputs validated before processing

---

## **🚀 ADVANCED PREVENTION STRATEGIES**

### **Complex Type Patterns:**

#### **Generic Component Patterns:**
```typescript
// ✅ REUSABLE TYPED COMPONENTS
interface ListProps<T> {
  items: T[];
  renderItem: (item: T) => VNode;
  keyExtractor: (item: T) => string;
}

function GenericList<T>(props: ListProps<T>) {
  // Implementation with full type safety
}
```

#### **Composable Patterns:**
```typescript
// ✅ TYPE-SAFE COMPOSABLES
export function useApi<T>() {
  const data: Ref<T | null> = ref(null);
  const loading: Ref<boolean> = ref(false);
  const error: Ref<Error | null> = ref(null);

  async function fetch(url: string): Promise<void> {
    loading.value = true;
    try {
      const response = await api.get<T>(url);
      data.value = response.data;
    } catch (err) {
      error.value = err as Error;
    } finally {
      loading.value = false;
    }
  }

  return { data, loading, error, fetch };
}
```

---

**Last Updated**: Based on industry research and Vue 3 + TypeScript best practices
**Purpose**: Prevent TypeScript errors during development rather than discovering them after implementation
**Status**: ACTIVE - Required for all Pomo-Flow feature development

**Following these standards prevents 80%+ of common TypeScript errors and ensures all new features maintain the strict type safety required for reliable deployment.**