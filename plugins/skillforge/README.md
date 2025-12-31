# SkillForge

Complete AI development toolkit for Claude Code with 33 skills, 12 agents, 10 commands, and 27 hooks.

## Installation

```bash
/plugin install skillforge@cc-marketplace
```

Or install directly from GitHub:

```bash
git clone https://github.com/yonatangross/skillforge-claude-plugin .claude
```

## Features

### Skills (33)

| Category | Skills |
|----------|--------|
| **AI/LLM** | ai-native-development, langgraph-workflows, llm-caching-patterns, llm-safety-patterns, langfuse-observability, pgvector-search |
| **Backend** | api-design-framework, database-schema-designer, streaming-api-patterns, resilience-patterns |
| **Frontend** | react-server-components-framework, design-system-starter, type-safety-validation, performance-optimization |
| **Security** | security-checklist, defense-in-depth |
| **Testing** | testing-strategy-builder, webapp-testing, evidence-verification |
| **Architecture** | architecture-decision-record, system-design-interrogation, brainstorming |
| **DevOps** | devops-deployment, observability-monitoring, edge-computing-patterns |
| **Data** | golden-dataset-management, golden-dataset-curation, golden-dataset-validation |

### Agents (12)

- `backend-system-architect` - API design, database schemas, microservices
- `frontend-ui-developer` - React 19, TypeScript, accessibility
- `database-engineer` - PostgreSQL, pgvector, migrations
- `llm-integrator` - LLM APIs, prompt engineering, streaming
- `workflow-architect` - LangGraph, multi-agent systems
- `security-auditor` - OWASP, vulnerability scanning
- `code-quality-reviewer` - Code review, linting, type checking
- `test-generator` - Unit/integration/E2E tests
- `debug-investigator` - Root cause analysis
- `data-pipeline-engineer` - Embeddings, ETL, vector indexing
- `rapid-ui-designer` - UI/UX, wireframing, prototyping
- `ux-researcher` - User research, personas, journey mapping

### Commands (10)

| Command | Description |
|---------|-------------|
| `/implement` | Full-power feature implementation with parallel subagents |
| `/explore` | Deep codebase exploration |
| `/verify` | Comprehensive feature verification |
| `/commit` | Smart commit with validation |
| `/create-pr` | Create PR with auto-generated description |
| `/review-pr` | Comprehensive PR review |
| `/fix-issue` | Fix GitHub issue with parallel analysis |
| `/run-tests` | Comprehensive test execution |
| `/add-golden` | Add documents to golden dataset |
| `/brainstorm` | Multi-perspective idea exploration |

### Hooks (27)

Security-hardened hooks for:
- Lifecycle events (session start/end)
- Pre-tool validation (file guards, git protection)
- Post-tool auditing (metrics, error tracking)
- Notifications (desktop, sound)

## Key Features

- **Progressive Loading**: Token-efficient skill loading via capabilities.json
- **LangGraph 1.0**: Multi-agent workflows with checkpointing
- **Security-First**: OWASP Top 10, defense-in-depth, LLM safety
- **Production-Ready**: Patterns for FastAPI, React 19, PostgreSQL/pgvector

## Repository

https://github.com/yonatangross/skillforge-claude-plugin

## Author

[Yonatan Gross](https://github.com/yonatangross)

## License

MIT
