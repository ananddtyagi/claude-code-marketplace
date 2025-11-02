# Plugin Schema Specification

This document defines the expected schema for all plugins in the marketplace.

## Directory Structure

Each plugin must follow this structure:

```
plugin-name/
├── .claude-plugin/           # Required: Metadata directory
│   └── plugin.json          # Required: Plugin manifest
├── commands/                 # Optional: Command definitions
│   ├── command1.md
│   └── command2.md
├── agents/                   # Optional: Agent definitions
│   ├── agent1.md
│   └── agent2.md
├── skills/                   # Optional: Agent Skills
│   ├── skill-name/
│   │   └── SKILL.md
│   └── another-skill/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Optional: Hook configurations
│   ├── hooks.json           # Main hook config
│   └── additional-hooks.json
├── .mcp.json                # Optional: MCP server definitions
├── scripts/                 # Optional: Hook and utility scripts
│   ├── script1.sh
│   └── script2.py
├── LICENSE                  # Optional: License file
├── CHANGELOG.md             # Optional: Version history
└── README.md                # Optional: Documentation
```

## Required Files

### `.claude-plugin/plugin.json`

The plugin manifest file is **required** for all plugins. It must contain valid JSON with the following structure:

#### Required Fields

- **`name`** (string): Plugin identifier (kebab-case recommended)
- **`version`** (string): Semantic version (e.g., "1.2.0")
- **`description`** (string): Brief description of the plugin

#### Optional Fields

- **`author`** (object): Author information
  - `name` (string, required): Author's name
  - `email` (string, optional): Author's email
  - `url` (string, optional): Author's website or GitHub profile
- **`homepage`** (string): Plugin documentation URL
- **`repository`** (string): Git repository URL
- **`license`** (string): License identifier (e.g., "MIT", "Apache-2.0")
- **`keywords`** (array of strings): Searchable keywords
- **`commands`** (string or array of strings): Custom command locations
- **`agents`** (string): Custom agent directory location
- **`hooks`** (string): Custom hook configuration file location
- **`mcpServers`** (string): Custom MCP server configuration file location

#### Example `plugin.json`

**Minimal:**
```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "A simple plugin for Claude Code"
}
```

**Complete:**
```json
{
  "name": "enterprise-plugin",
  "version": "1.2.0",
  "description": "Enterprise-grade development plugin",
  "author": {
    "name": "Jane Developer",
    "email": "jane@example.com",
    "url": "https://github.com/janedev"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/janedev/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "security", "compliance"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json"
}
```

## Optional Directories

### `commands/`

Contains command definition files (`.md` format). Each file defines a custom slash command.

### `agents/`

Contains agent definition files (`.md` format). Each file defines a specialized AI agent.

### `skills/`

Contains skill directories. Each skill directory should have:
- `SKILL.md` - Skill definition
- Optional subdirectories for scripts and resources

### `hooks/`

Contains hook configuration files (`.json` format). Hooks define event-driven automation.

### `scripts/`

Contains scripts used by hooks or for plugin utilities. Can be any executable format (.sh, .py, .js, etc.).

## Optional Files

### `.mcp.json`

Defines Model Context Protocol server configurations. Must be valid JSON.

### `LICENSE`

License file for the plugin.

### `CHANGELOG.md`

Version history and release notes.

### `README.md`

Plugin documentation and usage instructions.

## Validation

### Automated Validation

The repository includes automated validation that runs on every commit:

1. **Schema Validation** (`scripts/validate-plugin-schema.py`)
   - Verifies required files exist
   - Validates `plugin.json` structure and field types
   - Checks JSON syntax in all `.json` files
   - Validates directory structure

2. **Marketplace Sync** (`scripts/validate-marketplace-sync.py`)
   - Ensures marketplace documentation is updated when plugins change
   - Checks that README.md and plugins.md reference existing plugins

### Running Validation Locally

```bash
# Validate plugin schemas
python3 scripts/validate-plugin-schema.py

# Validate marketplace sync
python3 scripts/validate-marketplace-sync.py
```

### Common Validation Errors

1. **Missing `plugin.json`**
   ```
   Error: Missing required file: .claude-plugin/plugin.json
   ```
   Solution: Create the `.claude-plugin/` directory and add a `plugin.json` file.

2. **Invalid `plugin.json` structure**
   ```
   Error: plugin.json missing required fields: name, version
   ```
   Solution: Ensure all required fields are present.

3. **Invalid author field**
   ```
   Error: plugin.json 'author' must be an object
   ```
   Solution: Use the proper author object format with at least a `name` field.

4. **Invalid JSON syntax**
   ```
   Error: Invalid JSON in plugin.json: Expecting ',' delimiter
   ```
   Solution: Fix JSON syntax errors (trailing commas, missing quotes, etc.).

## Best Practices

1. **Use semantic versioning** for the `version` field
2. **Include descriptive keywords** for better discoverability
3. **Provide author information** for attribution and support
4. **Link to repository** for open-source contributions
5. **Document your plugin** with a README.md
6. **Track changes** with CHANGELOG.md
7. **Use clear names** that describe the plugin's purpose
8. **Keep descriptions concise** but informative

## Migration Guide

If you have an existing plugin without `plugin.json`, create it:

```bash
cd plugins/your-plugin
mkdir -p .claude-plugin
cat > .claude-plugin/plugin.json << 'EOF'
{
  "name": "your-plugin",
  "version": "1.0.0",
  "description": "Your plugin description",
  "author": {
    "name": "Your Name"
  }
}
EOF
```

## CI/CD Integration

The validation runs automatically via GitHub Actions on:
- Push to main/master branch
- Pull requests to main/master branch
- Changes in the `plugins/` directory

The workflow:
- Checks out the code
- Sets up Python 3.11
- Runs schema validation
- Runs marketplace sync validation

Failed validation will block PR merges.


