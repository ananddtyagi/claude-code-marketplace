# Version Pill - Claude Code Plugin

Project management for AI-native development. Manage roadmaps, tasks, releases, and context directly from Claude Code.

## Quick Install

```bash
# Add the Version Pill marketplace
/plugin marketplace add jimmyharika/versionpill-claude-plugin

# Install the plugin
/plugin install versionpill
```

## Setup

1. Sign up at [versionpill.com](https://versionpill.com)
2. Go to **Settings → API Keys**
3. Create a new API key
4. Set your environment variable:
   ```bash
   export VERSIONPILL_API_KEY=your_key_here
   ```

## Security

- **API keys are never stored in this plugin** - they're read from your environment
- All API calls go through `mcp.versionpill.com` over HTTPS
- Your key is passed via environment variable, never hardcoded
- Rate limiting and authentication handled server-side

## Features

### 65 Project Management Tools

| Category | Tools |
|----------|-------|
| Tasks | create, list, update, move, start, complete |
| Releases | plan, create, publish with auto-semver |
| Context | AI context docs, skills, decisions |
| Sync | Two-way sync with your repo |
| Search | Semantic search across everything |

### Slash Commands

- `/vp` - Quick access to all Version Pill features
- `/vp-sync` - Sync context to/from your codebase
- `/vp-release` - Plan and create releases

### Two-Way Repo Sync

Push your roadmap to your codebase:
```
sync_to_repo({ projectId: "my-project", repoPath: "/path/to/repo" })
```

Creates:
```
.versionpill/
├── CONTEXT.md    # Project context
├── DECISIONS.md  # Architecture decisions
├── TASKS.md      # Current tasks
└── SKILLS/       # Reusable prompts
```

Import your existing docs:
```
sync_from_repo({ projectId: "my-project", repoPath: "/path/to/repo" })
```

Imports: `CLAUDE.md`, `.cursorrules`, `.github/copilot-instructions.md`

## Why Version Pill?

**Stop repeating yourself to every AI tool.**

Your project context lives in one place. Claude Code, Cursor, Windsurf - they all read from the same source of truth.

- One source of truth for all AI tools
- Zero context loss between sessions
- 65 tools, one API
- Sub-50ms responses with edge caching

## Links

- [Website](https://versionpill.com)
- [API Documentation](https://versionpill.com/docs)
