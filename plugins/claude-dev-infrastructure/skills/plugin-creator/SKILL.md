---
name: plugin-creator
description: Create, validate, and publish Claude Code plugins and marketplaces. Use this skill when building plugins with commands, agents, hooks, MCP servers, or skills.
---

# Claude Code Plugin Creator

## Overview

This skill provides comprehensive guidance for creating Claude Code plugins following the official Anthropic format (as of December 2025).

## Plugin Architecture

A Claude Code plugin can contain any combination of:
- **Commands**: Custom slash commands (`/mycommand`)
- **Agents**: Specialized AI subagents for specific tasks
- **Hooks**: Pre/post tool execution behaviors
- **MCP Servers**: Model Context Protocol integrations
- **Skills**: Domain-specific knowledge packages

## Directory Structure

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json          # REQUIRED - Plugin manifest
├── commands/                 # Optional - Slash commands
│   └── my-command.md
├── agents/                   # Optional - Subagents
│   └── my-agent.md
├── hooks/                    # Optional - Hook definitions
│   └── hooks.json
├── skills/                   # Optional - Bundled skills
│   └── my-skill/
│       └── SKILL.md
├── mcp/                      # Optional - MCP server configs
└── README.md
```

## Plugin Manifest (plugin.json)

The `.claude-plugin/plugin.json` file is **required**. Here's the complete schema:

```json
{
  "$schema": "https://anthropic.com/claude-code/plugin.schema.json",
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "Clear description of what this plugin does",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "license": "MIT",
  "commands": [
    {
      "name": "mycommand",
      "description": "What this command does",
      "source": "./commands/my-command.md"
    }
  ],
  "agents": [
    {
      "name": "my-agent",
      "description": "What this agent specializes in",
      "source": "./agents/my-agent.md"
    }
  ],
  "hooks": {
    "source": "./hooks/hooks.json"
  },
  "skills": [
    "./skills/my-skill"
  ],
  "mcp_servers": [
    {
      "name": "my-mcp",
      "command": "npx",
      "args": ["my-mcp-server"]
    }
  ]
}
```

## Creating Commands

Commands are markdown files with YAML frontmatter:

```markdown
---
name: deploy
description: Deploy the application to production
---

# Deploy Command

When the user runs /deploy, perform these steps:

1. Run the build process
2. Run all tests
3. Create a deployment package
4. Upload to the configured target

## Usage Examples

- `/deploy` - Deploy to default environment
- `/deploy staging` - Deploy to staging
- `/deploy production --skip-tests` - Deploy to production (use carefully)
```

## Creating Agents

Agents are specialized subagents with focused capabilities:

```markdown
---
name: security-reviewer
description: Reviews code for security vulnerabilities
model: sonnet
tools:
  - Read
  - Grep
  - Glob
---

# Security Review Agent

You are a security expert focused on identifying vulnerabilities.

## Your Responsibilities

1. Scan for OWASP Top 10 vulnerabilities
2. Identify hardcoded secrets
3. Check for input validation issues
4. Review authentication/authorization logic

## Output Format

Provide findings as:
- CRITICAL: Immediate security risk
- HIGH: Should fix before deployment
- MEDIUM: Fix in next sprint
- LOW: Consider improving
```

## Creating Skills

Skills use the official Agent Skills format:

```markdown
---
name: my-skill
description: What this skill teaches Claude to do
---

# My Skill Name

## When to Use

Use this skill when the user needs help with [specific task].

## Instructions

1. Step one
2. Step two
3. Step three

## Examples

### Example 1: Basic Usage
[Concrete example]

### Example 2: Advanced Usage
[Another example]

## Best Practices

- Practice 1
- Practice 2
```

## Creating Hooks

Hooks are defined in `hooks.json`:

```json
{
  "hooks": [
    {
      "event": "PreToolUse",
      "matcher": "Edit|Write",
      "command": ".claude-plugin/hooks/security-check.sh"
    },
    {
      "event": "PostToolUse",
      "matcher": "Bash",
      "command": ".claude-plugin/hooks/log-commands.sh"
    }
  ]
}
```

Hook events:
- `PreToolUse` - Before a tool executes
- `PostToolUse` - After a tool completes
- `SessionStart` - When a Claude Code session begins
- `SessionEnd` - When a session ends

## Creating a Marketplace

To distribute multiple plugins, create a marketplace:

```
my-marketplace/
├── .claude-plugin/
│   └── marketplace.json
└── plugins/
    ├── plugin-a/
    │   └── .claude-plugin/
    │       └── plugin.json
    └── plugin-b/
        └── .claude-plugin/
            └── plugin.json
```

### marketplace.json

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "my-marketplace",
  "version": "1.0.0",
  "description": "Collection of productivity plugins",
  "owner": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "plugins": [
    {
      "name": "plugin-a",
      "description": "What plugin A does",
      "source": "./plugins/plugin-a",
      "category": "development",
      "tags": ["productivity", "automation"]
    },
    {
      "name": "plugin-b",
      "description": "What plugin B does",
      "source": "./plugins/plugin-b",
      "category": "productivity"
    }
  ]
}
```

### Plugin Categories

Official categories:
- `development` - Developer tools
- `productivity` - Workflow automation
- `security` - Security tools
- `learning` - Educational content
- `testing` - Test automation
- `database` - Database tools
- `design` - UI/UX tools
- `monitoring` - Observability
- `deployment` - CI/CD tools

## Testing Plugins

### Local Testing

```bash
# Install from local path
/plugin install /path/to/my-plugin

# Or add as local marketplace
/plugin marketplace add /path/to/my-marketplace
/plugin install my-plugin@my-marketplace

# List installed plugins
/plugin list

# Enable/disable
/plugin enable my-plugin
/plugin disable my-plugin

# Uninstall
/plugin uninstall my-plugin
```

### Validation Checklist

Before publishing, verify:

- [ ] `plugin.json` is valid JSON
- [ ] All `source` paths exist
- [ ] Commands have name + description
- [ ] Agents specify required tools
- [ ] Hook scripts are executable
- [ ] Skills have proper YAML frontmatter
- [ ] README.md explains usage

## Publishing to a Marketplace

### Option 1: Create Your Own Marketplace

1. Create a GitHub repository
2. Add `.claude-plugin/marketplace.json`
3. Add plugin directories
4. Users install via:
   ```
   /plugin marketplace add your-username/your-repo
   /plugin install plugin-name@your-repo
   ```

### Option 2: Submit to Community Marketplaces

Popular community marketplaces:
- [cc-marketplace](https://github.com/ananddtyagi/claude-code-marketplace)
- [claude-plugins.dev](https://claude-plugins.dev)

Submit via:
- Pull request to the marketplace repo
- Or their submission forms

### Option 3: Anthropic's Official Marketplace

The [anthropics/claude-code](https://github.com/anthropics/claude-code) repo contains official plugins. To add:
1. Fork the repository
2. Add your plugin under `plugins/`
3. Update `marketplace.json`
4. Submit a pull request

## Best Practices

### Plugin Design

1. **Single Responsibility**: Each plugin should do one thing well
2. **Clear Descriptions**: Users should understand purpose from description
3. **Sensible Defaults**: Work out-of-the-box with minimal config
4. **Version Semantics**: Use semver (1.0.0, 1.1.0, 2.0.0)

### Security

1. **Minimal Permissions**: Only request tools you need
2. **No Secrets in Code**: Use environment variables
3. **Audit Hook Scripts**: Review all shell scripts for safety
4. **Document Risks**: Explain what your plugin does

### Documentation

1. **README.md**: Always include installation and usage
2. **Examples**: Show concrete use cases
3. **Changelog**: Track version changes
4. **License**: Specify usage terms (MIT recommended)

## Quick Start Template

Run this to scaffold a new plugin:

```bash
mkdir my-plugin && cd my-plugin
mkdir -p .claude-plugin commands agents skills

cat > .claude-plugin/plugin.json << 'EOF'
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "My awesome Claude Code plugin",
  "author": {
    "name": "Your Name"
  },
  "commands": []
}
EOF

cat > README.md << 'EOF'
# My Plugin

Description of your plugin.

## Installation

```
/plugin install /path/to/my-plugin
```

## Usage

Describe how to use your plugin.
EOF

echo "Plugin scaffolded! Edit .claude-plugin/plugin.json to add commands/agents."
```

## References

- [Claude Code Plugin Docs](https://code.claude.com/docs/en/plugins)
- [Creating Marketplaces](https://code.claude.com/docs/en/plugin-marketplaces)
- [Agent Skills Spec](https://agentskills.io)
- [Anthropic Skills Repo](https://github.com/anthropics/skills)
- [Official Plugins](https://github.com/anthropics/claude-code/tree/main/plugins)
