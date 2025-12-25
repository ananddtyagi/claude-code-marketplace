# CLAUDE.md Template

# {{PROJECT_NAME}} - Claude Code Development Guide

> This file provides guidance to Claude Code when working with this codebase.
> Last Updated: {{DATE}}

---

## Project Overview

**{{PROJECT_NAME}}** is {{PROJECT_DESCRIPTION}}.

### Current Status

| Component | Status | Notes |
|-----------|--------|-------|
| Core | ✅ Working | Main functionality operational |
| Tests | ⚠️ Partial | Some tests need updating |
| Docs | 🔄 In Progress | Documentation being written |

**Full Tracking**: See `docs/MASTER_PLAN.md` for:
- Active work (TASK-XXX)
- Bug tracking (BUG-XXX)
- Roadmap items (ROAD-XXX)
- Known issues (ISSUE-XXX)

---

## Technology Stack

### Core
- **Language**: {{PRIMARY_LANGUAGE}}
- **Framework**: {{FRAMEWORK}}
- **Build Tool**: {{BUILD_TOOL}}

### Testing
- **Unit Tests**: {{TEST_FRAMEWORK}}
- **E2E Tests**: {{E2E_FRAMEWORK}}

### Development
- **Linting**: {{LINTER}}
- **Formatting**: {{FORMATTER}}

---

## Development Commands

```bash
# Install dependencies
{{INSTALL_COMMAND}}

# Start development server
{{DEV_COMMAND}}

# Build for production
{{BUILD_COMMAND}}

# Run tests
{{TEST_COMMAND}}

# Lint code
{{LINT_COMMAND}}
```

---

## Project Architecture

```
{{PROJECT_ROOT}}/
├── src/                    # Source code
│   ├── components/         # UI components
│   ├── views/              # Page views
│   ├── stores/             # State management
│   ├── composables/        # Reusable logic
│   └── utils/              # Utility functions
├── tests/                  # Test files
├── docs/                   # Documentation
│   └── MASTER_PLAN.md      # Project tracking
└── CLAUDE.md               # This file
```

---

## Key Development Rules

### MUST Follow
1. **Test Before Claiming Success** - Visual/automated verification is mandatory
2. **Use Established Patterns** - Follow existing code conventions
3. **Type Safety** - All new code must have proper types
4. **Update Documentation** - Keep MASTER_PLAN.md current

### Best Practices
1. Follow existing code patterns
2. Write tests for new functionality
3. Document complex logic
4. Keep functions small and focused

---

## Task Tracking

### MASTER_PLAN.md Integration

All work items must be tracked in `docs/MASTER_PLAN.md` with proper IDs:

| Prefix | Usage | Example |
|--------|-------|---------|
| `TASK-XXX` | Active features/tasks | `TASK-001: New Feature` |
| `BUG-XXX` | Bug fixes | `BUG-001: Fix login issue` |
| `ROAD-XXX` | Roadmap items | `ROAD-001: Future feature` |
| `IDEA-XXX` | Ideas to consider | `IDEA-001: Concept` |
| `ISSUE-XXX` | Known issues | `ISSUE-001: Limitation` |

### Task Format
```markdown
### TASK-XXX: Task Title (STATUS)

**Priority**: P2-MEDIUM

- [ ] Step 1
- [ ] Step 2
- [ ] Step 3
```

---

## Common Issues & Solutions

### Issue 1: {{COMMON_ISSUE_1}}
**Solution**: {{SOLUTION_1}}

### Issue 2: {{COMMON_ISSUE_2}}
**Solution**: {{SOLUTION_2}}

---

## File Organization

### When Adding New Features
1. Add components to appropriate directories
2. Create tests alongside implementation
3. Update documentation as needed
4. Track progress in MASTER_PLAN.md

### Naming Conventions
- **Components**: PascalCase (`MyComponent.vue`)
- **Functions**: camelCase (`myFunction`)
- **Constants**: UPPER_SNAKE_CASE (`MY_CONSTANT`)
- **Files**: Depends on type (see existing patterns)

---

## Development Workflow

### 1. Starting New Work
1. Check MASTER_PLAN.md for task dependencies
2. Create/update task entry with status
3. Implement following existing patterns
4. Test thoroughly

### 2. Completing Work
1. Verify all tests pass
2. Update MASTER_PLAN.md status
3. Document any new patterns in CLAUDE.md
4. Create SOP if complex debugging was needed

---

## Port Configuration

| Service | Port | Command |
|---------|------|---------|
| Dev Server | {{DEV_PORT}} | `{{DEV_COMMAND}}` |
| Test Server | {{TEST_PORT}} | `{{TEST_COMMAND}}` |

---

## Environment Variables

```env
# Required
{{REQUIRED_ENV_VARS}}

# Optional
{{OPTIONAL_ENV_VARS}}
```

---

## Contact & Resources

- **Repository**: {{REPO_URL}}
- **Documentation**: {{DOCS_URL}}
- **Issue Tracker**: {{ISSUES_URL}}

---

**Version**: 1.0.0
**Framework**: {{FRAMEWORK}} {{FRAMEWORK_VERSION}}
