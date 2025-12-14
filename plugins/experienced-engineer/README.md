# Experienced Engineer Plugin

A comprehensive Claude Code plugin that provides specialized engineering subagents and productivity commands to help software teams work more efficiently.

## Overview

The Experienced Engineer plugin gives you instant access to specialized expert agents covering all major roles in a software engineering team. Whether you need help with API design, security review, performance optimization, or testing strategies, this plugin has you covered.

## Features

### 🤖 Specialized Subagents

Access expert-level guidance from 10 specialized engineering roles:

- **API Architect** - Design robust, scalable APIs with REST, GraphQL, and proper versioning
- **Security Specialist** - Identify vulnerabilities and implement secure coding practices
- **Code Quality Reviewer** - Maintain high code quality with SOLID principles and clean code
- **UX/UI Designer** - Create intuitive, accessible interfaces with great user experience
- **Database Architect** - Design efficient schemas and optimize database performance
- **Performance Engineer** - Identify bottlenecks and optimize application performance
- **DevOps Engineer** - Set up CI/CD, infrastructure as code, and deployment automation
- **Testing Specialist** - Implement comprehensive testing strategies and automation
- **Documentation Writer** - Create clear, comprehensive technical documentation
- **Tech Lead** - Get architectural guidance and technical leadership insights

### ⚡ Productivity Commands

#### `/code-explain`
Deep dive into your codebase to answer questions and explain functionality:
- "How does authentication work?"
- "What does this function do?"
- "Where is the payment processing implemented?"

Get thorough explanations with code snippets, execution flow, and architectural context.

#### `/update-claude`
Automatically update your `CLAUDE.md` file to reflect major changes in the codebase. This command helps keep your project documentation current so Claude (and your team) always has an up-to-date understanding of your architecture.

### 🎣 Smart Hooks

**Auto-Documentation Hook**: Automatically prompts to update `CLAUDE.md` after detecting significant code changes (50+ lines modified). This ensures your project documentation stays in sync with major refactoring or feature additions.

## Installation

### From Marketplace

```bash
# Add the marketplace (if not already added)
/plugin marketplace add cc-marketplace

# Install the plugin
/plugin install experienced-engineer@cc-marketplace
```

### Local Development

```bash
# Add local marketplace
/plugin marketplace add /path/to/cc-marketplace

# Install plugin
/plugin install experienced-engineer@cc-marketplace
```

## Usage

### Using Subagents

Access any specialist agent through the `/agent` command:

```bash
# Get API design review
/agent api-architect

# Security code review
/agent security-specialist

# Performance optimization suggestions
/agent performance-engineer
```

Or use the interactive agent selector:

```bash
/agents
```

Then select the specialist you need.

### Using Commands

#### Code Explanation

```bash
# Ask about any part of your codebase
/code-explain How does the authentication middleware work?

# Get detailed explanations
/code-explain Where is the database connection pool configured?
```

#### Documentation Updates

```bash
# Manually trigger CLAUDE.md update
/update-claude
```

Or let the auto-hook prompt you after major changes!

## Use Cases

### 🔍 Code Review
- Run security reviews with the **Security Specialist**
- Get code quality feedback from the **Code Quality Reviewer**
- Check API design with the **API Architect**

### 🏗️ Architecture Planning
- Consult the **Tech Lead** for architectural decisions
- Design database schemas with the **Database Architect**
- Plan infrastructure with the **DevOps Engineer**

### 🚀 Performance & Optimization
- Profile and optimize with the **Performance Engineer**
- Review database queries with the **Database Architect**
- Optimize frontend rendering with the **UX/UI Designer**

### 📝 Documentation & Testing
- Write comprehensive tests with the **Testing Specialist**
- Create clear documentation with the **Documentation Writer**
- Keep CLAUDE.md updated automatically

### 🎨 Frontend & UX
- Review UI/UX with the **UX/UI Designer**
- Check accessibility compliance
- Optimize user flows and interactions

## Plugin Structure

```
experienced-engineer/
├── .claude-plugin/
│   └── plugin.json              # Plugin manifest
├── agents/
│   ├── api-architect.md         # API design expert
│   ├── security-specialist.md   # Security review expert
│   ├── code-quality-reviewer.md # Code quality expert
│   ├── ux-ui-designer.md        # UX/UI design expert
│   ├── database-architect.md    # Database design expert
│   ├── performance-engineer.md  # Performance optimization expert
│   ├── devops-engineer.md       # DevOps & infrastructure expert
│   ├── testing-specialist.md    # Testing strategy expert
│   ├── documentation-writer.md  # Documentation expert
│   └── tech-lead.md             # Technical leadership expert
├── commands/
│   ├── code-explain.md          # Code explanation command
│   └── update-claude.md         # CLAUDE.md update command
├── hooks/
│   └── hooks.json               # Auto-documentation hook
└── README.md                    # This file
```

## Tips for Best Results

1. **Be Specific**: When consulting agents, provide context about what you're working on
2. **Combine Agents**: Use multiple specialists for comprehensive reviews
3. **Use Code Explain**: Before making changes, use `/code-explain` to understand existing code
4. **Keep Docs Updated**: Let the auto-hook update your CLAUDE.md regularly
5. **Iterative Consulting**: Ask follow-up questions to dive deeper

## Examples

### Example 1: API Design Review

```bash
/agent api-architect
"Review the REST API endpoints in /src/routes/users.js and suggest improvements"
```

### Example 2: Security Audit

```bash
/agent security-specialist
"Review authentication implementation in /src/middleware/auth.js for vulnerabilities"
```

### Example 3: Understanding Complex Code

```bash
/code-explain How does the payment processing workflow handle retries and failures?
```

### Example 4: Performance Investigation

```bash
/agent performance-engineer
"The dashboard page loads slowly. Help identify bottlenecks and optimization opportunities."
```

## Contributing

Found a way to improve these agents? Suggestions for new specialists? Contributions are welcome!

## License

MIT

## Version

1.0.0

---

**Made with ❤️ for engineering teams who want to move fast without breaking things.**

