---
name: dev-setup
description: Initialize a new project with Claude dev infrastructure (templates, hooks, skills)
---

# /dev-setup Command

Initialize a project with Claude Code development infrastructure.

## Usage

```
/dev-setup                    # Setup in current directory
/dev-setup /path/to/project   # Setup in specified directory
/dev-setup --minimal          # Install only essential components
```

## What Gets Installed

### Full Installation (default)
- `.claude/skills/` - 12 AI development skills
- `.claude/hooks/` - Task coordination hooks
- `.claude/settings.json` - Hook configuration
- `docs/MASTER_PLAN.md` - Task tracking template
- `CLAUDE.md` - Project guidance for Claude Code

### Minimal Installation (--minimal)
- `.claude/hooks/` - Essential task-lock hooks only
- `docs/MASTER_PLAN.md` - Task tracking template
- `CLAUDE.md` - Project guidance

## Implementation

When the user runs `/dev-setup`:

1. **Check target directory**
   - If path provided, use that directory
   - Otherwise use current working directory
   - Create directory if it doesn't exist

2. **Create .claude directory structure**
   ```bash
   mkdir -p .claude/skills .claude/hooks .claude/locks docs
   ```

3. **Copy components based on mode**
   - Full: Copy all skills, hooks, templates
   - Minimal: Copy essential hooks and templates only

4. **Generate project files from templates**
   - Replace `{{PROJECT_NAME}}` with directory name
   - Replace `{{DATE}}` with current date
   - Don't overwrite existing files

5. **Configure hooks in .claude/settings.json**
   ```json
   {
     "hooks": {
       "PreToolUse": [{"matcher": "Edit|Write", "command": ".claude/hooks/task-lock-enforcer.sh"}],
       "SessionStart": [{"command": ".claude/hooks/session-lock-awareness.sh"}],
       "SessionEnd": [{"command": ".claude/hooks/session-lock-release.sh"}]
     }
   }
   ```

6. **Report results**
   - List what was installed
   - Show next steps
   - Mention dev-manager if applicable

## Example Output

```
✅ Dev infrastructure initialized!

Installed:
  - 12 AI skills in .claude/skills/
  - 4 hooks in .claude/hooks/
  - MASTER_PLAN.md template
  - CLAUDE.md project guidance

Next steps:
  1. Edit CLAUDE.md for your project
  2. Add tasks to docs/MASTER_PLAN.md
  3. Run /dev-manager to start the Kanban dashboard
```
