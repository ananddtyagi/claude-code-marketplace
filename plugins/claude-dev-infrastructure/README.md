# Claude Dev Infrastructure Plugin

A comprehensive development infrastructure plugin for Claude Code projects. Provides battle-tested skills, hooks, templates, and standards extracted from real-world projects.

## Components

| Component | Count | Description |
|-----------|-------|-------------|
| **Skills** | 11 | Stack-agnostic AI skills for architecture, debugging, documentation |
| **Hooks** | 11 | Pre/post-tool hooks for task locking, reminders, automation |
| **Templates** | 5 | Project scaffolding templates (MASTER_PLAN, CLAUDE.md, SOP) |
| **Standards** | 5 | Quality and process standards documents |
| **Dev Manager** | 1 | Kanban dashboard with MASTER_PLAN.md integration |

## Quick Start

```bash
# 1. Clone or copy this plugin
cp -r ~/claude-plugins/claude-dev-infrastructure /path/to/your/project/.claude-plugin

# 2. Or use the setup script for selective installation
./init/setup.sh /path/to/your/project

# 3. Start the dev manager (optional)
cd dev-manager
npm install
npm start
```

## Skills Included

### Architecture & Planning
- **chief-architect** - Strategic development orchestrator
- **master-plan-manager** - MASTER_PLAN.md management
- **meta-skill-router** - Intelligent skill selection

### Quality Assurance
- **ai-truthfulness-enforcer** - Prevents false success claims
- **qa-testing** - Mandatory testing protocols

### Documentation
- **document-sync** - Keep docs synchronized with code
- **skill-creator-doctor** - Create and repair skills

### Safety & Organization
- **data-safety-auditor** - Data safety auditing
- **safe-project-organizer** - Safe file organization
- **crisis-debugging-advisor** - Emergency debugging guidance
- **skills-manager** - Skill consolidation and management

## Hooks Included

### Task Coordination (Multi-Instance)
- `task-lock-enforcer.sh` - Prevents concurrent task editing
- `session-lock-awareness.sh` - Shows active locks at session start
- `session-lock-release.sh` - Releases locks at session end

### Automation
- `auto-sync-task-status.sh` - Syncs task status changes
- `master-plan-reminder.sh` - Reminds about MASTER_PLAN updates
- `check-npm-scripts.sh` - Validates npm scripts

### Debugging
- `task-disappearance-helper.sh` - Tracks mysterious data loss

## Templates

| Template | Purpose |
|----------|---------|
| `MASTER_PLAN.template.md` | Project tracking with task IDs |
| `CLAUDE.template.md` | Claude Code project guidance |
| `SOP.template.md` | Standard Operating Procedure format |
| `settings.template.json` | Claude Code settings with hooks |
| `skill-template.md` | Skill creation template |

## Dev Manager

A Node.js dashboard that:
- Parses MASTER_PLAN.md into a Kanban board
- Supports drag-and-drop task status changes
- Live syncs changes back to MASTER_PLAN.md
- Provides SSE for real-time updates

```bash
cd dev-manager
DEV_MANAGER_ROOT=/your/project npm start
# Opens at http://localhost:6010
```

## Standards Documents

- `development-quality.md` - Code quality requirements
- `documentation-sync.md` - Documentation synchronization rules
- `session-handoff.md` - Multi-session handoff protocols
- `testing-requirements.md` - Testing before claiming success
- `user-verification-protocol.md` - User verification requirements

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CLAUDE_PROJECT_DIR` | Project root for hooks | Auto-detected |
| `DEV_MANAGER_PORT` | Dev manager port | 6010 |
| `DEV_MANAGER_ROOT` | Project root for dev-manager | Current directory |

### Claude Code Settings

Add to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "command": ".claude/hooks/task-lock-enforcer.sh"
      }
    ],
    "SessionStart": [
      {
        "command": ".claude/hooks/session-lock-awareness.sh"
      }
    ]
  }
}
```

## Directory Structure

```
claude-dev-infrastructure/
├── .claude-plugin/
│   └── plugin.json          # Plugin manifest
├── skills/                   # 11 AI skills
│   ├── chief-architect/
│   ├── master-plan-manager/
│   └── ...
├── hooks/                    # 11 shell scripts
│   ├── task-lock-enforcer.sh
│   └── ...
├── templates/                # 5 templates
│   ├── MASTER_PLAN.template.md
│   └── ...
├── standards/                # 5 standards docs
│   └── ...
├── dev-manager/              # Dashboard server
│   ├── server.js
│   ├── package.json
│   └── kanban/
├── init/
│   └── setup.sh             # Installation script
└── README.md
```

## License

MIT

## Credits

Extracted from the Pomo-Flow project's development infrastructure.
