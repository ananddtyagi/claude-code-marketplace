# MASTER_PLAN.md Template

# {{PROJECT_NAME}} - Master Development Plan

> **Purpose**: Central tracking document for all project work items, ideas, bugs, and roadmap
> **Last Updated**: {{DATE}}
> **Project Status**: {{STATUS}}

---

## Quick Navigation

| Section | Description |
|---------|-------------|
| [Task Dependency Index](#task-dependency-index) | Prevent multi-instance conflicts |
| [Active Work](#active-work) | Current tasks being worked on |
| [Bug Tracking](#bug-tracking) | Known bugs and fixes |
| [Roadmap](#roadmap) | Planned features by priority |
| [Ideas](#ideas) | Feature ideas to consider |
| [Known Issues](#known-issues) | Documented limitations |
| [Completed Work](#completed-work) | Archive of finished items |

---

## Task Dependency Index

> **Purpose**: Prevent multiple Claude Code instances from editing the same files simultaneously

| Task ID | Status | Primary Files | Depends On |
|---------|--------|---------------|------------|
| TASK-001 | TODO | `src/example.ts` | - |

**Status Legend**: `TODO` | `IN_PROGRESS` | `REVIEW` | `DONE`

---

## Active Work

### TASK-001: Example Feature (TODO)

**Description**: Brief description of what this task accomplishes.

**Priority**: P2-MEDIUM

**Files to Modify**:
- `src/example.ts` - Main implementation
- `src/components/Example.vue` - UI component

**Implementation Steps**:
- [ ] Step 1: Research and planning
- [ ] Step 2: Implementation
- [ ] Step 3: Testing
- [ ] Step 4: Documentation

**Rollback Command**:
```bash
git checkout HEAD~1 -- src/example.ts src/components/Example.vue
```

---

## Bug Tracking

| ID | Bug | Severity | Status | Notes |
|----|-----|----------|--------|-------|
| BUG-001 | Example bug description | P2 | 🔄 IN PROGRESS | Investigating root cause |

### BUG-001: Example Bug (🔄 IN PROGRESS)

**Symptoms**: Description of what's wrong.

**Steps to Reproduce**:
1. Step 1
2. Step 2
3. Observe the bug

**Root Cause**: (To be determined)

**Fix**: (To be implemented)

---

## Roadmap

### Priority Legend
- **P0**: Critical - Must fix immediately
- **P1**: High - Next sprint
- **P2**: Medium - This quarter
- **P3**: Low - Nice to have

| ID | Feature | Priority | Status | Notes |
|----|---------|----------|--------|-------|
| ROAD-001 | Example feature | P2 | TODO | Planned for next release |

---

## Ideas

> Add new ideas here. Use `IDEA-XXX` format.

| ID | Idea | Category | Added |
|----|------|----------|-------|
| IDEA-001 | Example idea description | Enhancement | {{DATE}} |

---

## Known Issues

> Document known limitations and workarounds.

| ID | Issue | Workaround | Status |
|----|-------|------------|--------|
| ISSUE-001 | Example known issue | Workaround description | Acknowledged |

---

## Completed Work

> Archive of completed tasks. Move items here when done.

### ~~TASK-000~~: Setup Project (✅ DONE)
- Completed: {{DATE}}
- Summary: Initial project setup and configuration

---

## Formatting Guide for AI/Automation

### Task Header Format
```markdown
### TASK-XXX: Task Title (STATUS)
### ~~TASK-XXX~~: Completed Task Title (✅ DONE)
```

### Status Keywords (for parser detection)
| Status | Keywords |
|--------|----------|
| Done | `DONE`, `COMPLETE`, `✅`, `~~strikethrough~~` |
| In Progress | `IN PROGRESS`, `IN_PROGRESS`, `🔄`, `ACTIVE` |
| Review | `REVIEW`, `MONITORING`, `👀` |
| Todo | Default (no keyword) |

### Progress via Subtasks
```markdown
- [x] Completed step ✅
- [ ] Pending step
```

### Priority Format
- In header: `(P1)`, `(HIGH)`, `(P2-MEDIUM)`
- Or as line: `**Priority**: P1-HIGH`
