---
name: safe-project-organizer
description: Safely analyze and reorganize project structure with multi-stage validation, dry-run previews, and explicit user confirmation. Use when projects need cleanup, standardization, or better organization.
---

# Safe Project Organizer

## Overview

This skill enables Claude Code to analyze project structure and suggest safe organizational improvements like moving files, removing unused directories, and restructuring folders. It prioritizes safety through multi-stage validation, dry-run previews, and explicit user confirmation.

## Core Safety Principles

### 1. Read-Only Analysis Phase
- All analysis operations are read-only
- No modifications occur during scanning
- Complete project snapshot before any changes

### 2. Dry-Run Validation
- All operations preview changes before execution
- Show exact file paths being affected
- Calculate impact metrics (files moved, deleted, created)

### 3. Explicit User Confirmation
- Require confirmation for each operation category
- Display detailed change summary
- Allow selective approval of suggestions

### 4. Atomic Operations with Rollback
- Each operation is reversible
- Create backup references before modifications
- Maintain operation log for audit trail

### 5. Protected File Patterns
Never modify files matching these patterns:
- `.git/`, `.svn/`, `.hg/` (version control)
- `node_modules/`, `vendor/`, `venv/`, `.venv/` (dependencies)
- `.env*`, `secrets.*`, `credentials.*` (sensitive data)
- `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml` (lock files)
- `dist/`, `build/`, `.next/`, `.nuxt/` (build artifacts)

## When to Use This Skill

Use this skill when you encounter any of these scenarios:

**Project Cleanup:**
- "My project root is messy with too many files"
- "I have empty directories that should be cleaned up"
- "Documentation files are scattered everywhere"

**Standardization:**
- "This project doesn't follow standard directory structure"
- "Source files are mixed with config files in root"
- "I need to organize files by type for better maintainability"

**Migration Preparation:**
- "I'm about to hand off this project and need to clean it up"
- "This codebase needs better organization before adding new features"
- "I want to standardize the project structure"

**Safety Concerns:**
- "I'm nervous about accidentally breaking something"
- "I need to see exactly what will change before making changes"
- "I want a safe way to reorganize without losing data"

## Safe Usage Workflow

### Step 1: Initial Scan (Read-Only)
Execute the project organizer script with `--scan` flag:

```bash
python3 scripts/project_organizer.py /path/to/project --scan
```

**What it does:**
- Scans entire project structure
- Identifies file types, counts, sizes
- Detects empty directories
- Lists protected files
- **No modifications made**

**Example Output:**
```
🔍 Scanning project: /path/to/project
📋 This is a READ-ONLY scan. No changes will be made.

✅ Scan complete!
   📁 Directories: 24
   📄 Files: 156
   🔒 Protected items: 42
   📂 Empty directories: 3
```

### Step 2: Generate Suggestions (Still Read-Only)
Use `--analyze` flag to generate organizational suggestions:

```bash
python3 scripts/project_organizer.py /path/to/project --analyze
```

**What it does:**
- Performs full analysis
- Generates organizational suggestions
- Displays suggestion count
- **Still no modifications**

### Step 3: Preview Changes (Detailed Review)
Use `--preview` flag to see exactly what will change:

```bash
python3 scripts/project_organizer.py /path/to/project --preview
```

**What it does:**
- Shows detailed preview of ALL suggestions
- Groups by action type (move, delete, create)
- Displays risk levels (🟢 low, 🟡 medium, 🔴 high)
- Shows safety checks for each operation
- Lists exact file paths affected
- **Zero modifications**

**Example Preview Output:**
```
📋 PREVIEW MODE - No changes will be made
============================================================

📊 Total Suggestions: 8

🎯 By Action:
   MOVE: 5
   DELETE: 2
   CREATE_DIR: 1

⚠️  By Risk Level:
   🟢 LOW: 6
   🟡 MEDIUM: 2

📝 Detailed Suggestions:

MOVE Operations (5):
1. 🟢 Documentation/config files organized in docs/ directory
   FROM: CONTRIBUTING.md
   TO:   docs/CONTRIBUTING.md
   Safety Checks:
      ✓ File is not a primary config
      ✓ No imports reference this file path
      ✓ Not in protected patterns

DELETE Operations (2):
1. 🟢 Empty directory with no files or subdirectories
   PATH: old_backup/temp
   Safety Checks:
      ✓ Directory is empty
      ✓ Not a protected path
      ✓ No version control markers
```

### Step 4: Dry Run (Simulation Only)
Use `--execute` flag for dry-run simulation:

```bash
python3 scripts/project_organizer.py /path/to/project --execute
```

**What it does:**
- Simulates ALL operations
- Shows what WOULD happen
- Validates all safety checks
- Reports success/failure/skipped
- **No actual changes made**

### Step 5: Real Execution (Requires Confirmation)
Use `--execute-real` flag only after thorough review:

```bash
python3 scripts/project_organizer.py /path/to/project --execute-real
```

**What it does:**
- Prompts for explicit confirmation
- Executes approved changes
- Creates audit log (`.project_organizer.log`)
- Shows real-time progress
- **Actually modifies project**

**Confirmation Prompt:**
```
⚠️  WARNING: This will make REAL changes. Type 'yes' to confirm: yes
```

## Operation Types and Safety

### Move Operations
**Low Risk (🟢):**
- Moving documentation files to `docs/`
- Moving config files to `config/`
- Moving scripts to `scripts/`

**Medium Risk (🟡):**
- Grouping source files by type
- Creating organizational directories

**Safety Checks Performed:**
- Source file exists and is accessible
- Source is not in protected patterns
- Destination doesn't already exist
- Parent directories can be created safely

### Delete Operations
**Low Risk (🟢):**
- Removing truly empty directories
- Deleting temporary files

**Safety Checks Performed:**
- Target exists
- Directory is completely empty
- Not a protected path
- No version control markers

### Create Directory Operations
**Low Risk (🟢):**
- Creating standard directories (`src/`, `docs/`, `tests/`)
- Creating organizational structure

**Safety Checks Performed:**
- Target doesn't already exist
- No naming conflicts
- Standard directory pattern
- Parent directories can be created

## Protected File Patterns

The skill automatically protects these paths from modification:

### Version Control
- `.git/`, `.git/**`
- `.svn/`, `.svn/**`
- `.hg/`, `.hg/**`

### Dependencies
- `node_modules/`, `node_modules/**`
- `vendor/`, `vendor/**`
- `venv/`, `venv/**`
- `.venv/`, `.venv/**`

### Build Artifacts
- `dist/`, `dist/**`
- `build/`, `build/**`
- `.next/`, `.next/**`
- `.nuxt/`, `.nuxt/**`
- `out/`, `out/**`

### Sensitive Data
- `.env*`
- `secrets.*`
- `credentials.*`

### Lock Files
- `package-lock.json`
- `yarn.lock`
- `pnpm-lock.yaml`
- `Gemfile.lock`
- `Pipfile.lock`
- `poetry.lock`

### Cache Files
- `__pycache__/`, `__pycache__/**`

## Best Practices

### Before Running the Skill
1. **Commit Changes**: Ensure all current work is committed to version control
2. **Backup Important Files**: Have a recent backup or git stash available
3. **Review Project**: Understand what files and directories are important
4. **Test Access**: Verify you have necessary permissions

### During Execution
1. **Always Start with Scan**: Begin with `--scan` to understand the project
2. **Review Suggestions Carefully**: Look through all generated suggestions
3. **Use Preview Mode**: Always use `--preview` before any execution
4. **Test with Dry Run**: Use `--execute` to simulate changes safely

### After Execution
1. **Verify Project Works**: Test that your project still builds/runs correctly
2. **Review Operation Log**: Check `.project_organizer.log` for what was changed
3. **Commit Separately**: Commit organizational changes separately from functional changes
4. **Update Documentation**: Update any documentation that references old file paths

### Safety Checklist
Before using `--execute-real`, verify:
- [ ] Project is committed to version control
- [ ] All suggestions reviewed in preview mode
- [ ] Dry run completed successfully
- [ ] No critical files are being moved
- [ ] Build/test processes still work
- [ ] Team members notified if shared project

## Error Handling and Troubleshooting

### Common Issues

**Permission Denied:**
- Ensure you have write permissions
- Check file ownership
- May need appropriate privileges

**Path Protected:**
- Review protected patterns
- Confirm the path should be modified
- Adjust patterns if needed

**Changes Not Appearing:**
- Verify you used `--execute-real` (not just `--execute`)
- Check the operation log
- Confirm "yes" was entered at confirmation prompt

### Recovery Options

**Git Recovery:**
```bash
git status                    # See what changed
git checkout -- .            # Restore all changes
git reset --hard HEAD        # Full reset to last commit
```

**Operation Log Review:**
```bash
cat .project_organizer.log    # Review detailed operation log
```

## Customization

### Adding Custom Protected Patterns
Edit the `PROTECTED_PATTERNS` list in the script:
```python
PROTECTED_PATTERNS = [
    # Existing patterns...
    'my_important_dir/**',    # Custom protection
    '*.critical',             # Protect critical files
]
```

### Custom Organization Rules
Edit `MOVABLE_ROOT_FILES` dictionary:
```python
MOVABLE_ROOT_FILES = {
    'assets': ['*.png', '*.jpg', '*.svg'],  # Move images to assets/
    'data': ['*.csv', '*.json', '*.xml'],   # Move data files
}
```

### Custom Safety Validators
Extend the `SafeProjectOrganizer` class:
```python
def _custom_safety_check(self, path: Path) -> bool:
    """Your custom safety logic"""
    # Return True if safe, False if should be protected
    return True
```

## Integration with Claude Code

### As a Skill Tool
This skill integrates naturally with Claude Code's workflow:

1. **User Request**: "Organize my project structure"
2. **Skill Activation**: Safe Project Organizer loads
3. **Sequential Execution**: Follows the 5-step workflow automatically
4. **User Confirmation**: Confirms each step before proceeding
5. **Safety Validation**: All operations include safety checks

### Example User Interactions

**Simple Cleanup:**
```
User: "My project root is messy, can you help organize it?"
Claude: [Uses skill to scan and suggest safe improvements]
```

**Targeted Organization:**
```
User: "I have too many documentation files scattered around"
Claude: [Uses skill to identify and suggest grouping docs/ folder]
```

**Pre-Migration Cleanup:**
```
User: "I need to clean up before handing this project to another team"
Claude: [Uses skill for comprehensive safe reorganization]
```

## Resources

### scripts/
- `project_organizer.py` - The main safe project organizer script with comprehensive safety features

The script includes:
- Multi-phase analysis and execution
- Protected pattern detection
- Risk level classification
- Comprehensive safety checks
- Audit trail generation
- Rollback information preservation

This script can be executed independently of Claude Code for manual project organization tasks.

---

**Safety Guarantee**: This skill never modifies files without explicit confirmation, always previews changes, and includes comprehensive safety checks to protect important project data.

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
