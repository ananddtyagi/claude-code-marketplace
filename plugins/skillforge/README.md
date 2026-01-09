# SkillForge

Complete AI development toolkit for Claude Code with 78 skills, 20 agents, 12 commands, and 92 hooks.

## Installation

```bash
/plugin install skillforge@cc-marketplace
```

Or install directly from GitHub:

```bash
git clone https://github.com/yonatangross/skillforge-claude-plugin .claude
```

## Features

### Skills (78)

| Category | Skills |
|----------|--------|
| **AI/LLM** | agent-loops, embeddings, function-calling, llm-streaming, llm-evaluation, rag-retrieval, reranking-patterns, prompt-caching, ollama-local |
| **Backend** | api-design-framework, clean-architecture, caching-strategies, rate-limiting, background-jobs, api-versioning, fastapi-advanced |
| **Frontend** | react-server-components-framework, design-system-starter, type-safety-validation, motion-animation-patterns, performance-optimization |
| **Security** | owasp-top-10, auth-patterns, input-validation, llm-safety-patterns, security-scanning |
| **Testing** | unit-testing, integration-testing, e2e-testing, msw-mocking, vcr-http-recording, test-data-management, llm-testing |
| **Architecture** | system-design-interrogation, brainstorming, context-engineering, resilience-patterns |
| **DevOps** | devops-deployment, observability-monitoring, edge-computing-patterns, github-cli |
| **LangGraph** | langgraph-state, langgraph-routing, langgraph-checkpoints, langgraph-human-in-loop, langgraph-supervisor, langgraph-parallel |

### Agents (20)

**Product Thinking (6)**
- `product-strategist` - Value proposition, business alignment
- `requirements-translator` - PRDs, user stories, acceptance criteria
- `prioritization-analyst` - RICE/ICE/WSJF scoring, backlog ranking
- `ux-researcher` - Personas, user journeys, validation
- `market-intelligence` - Competitive analysis, TAM/SAM/SOM
- `business-case-builder` - ROI, cost-benefit analysis

**Technical Implementation (14)**
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
- `metrics-architect` - OKRs, KPIs, instrumentation
- `security-layer-auditor` - Defense-in-depth verification
- `system-design-reviewer` - Architecture review

### Commands (12)

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
| `/configure` | Configure SkillForge bundles and settings |
| `/status` | Show current configuration status |

### Hooks (92)

Security-hardened hooks for:
- **Lifecycle**: Session start/end, context initialization
- **Permission**: Auto-approval for safe operations
- **Pre-tool**: File guards, git branch protection, bash validation
- **Post-tool**: Audit logging, metrics, error tracking
- **Notifications**: Desktop and sound alerts
- **Stop**: Quality gates, subagent validation

## Key Features

- **Progressive Loading**: Token-efficient skill loading via capabilities.json (Tier 1-4)
- **LangGraph 1.0**: Multi-agent workflows with checkpointing and human-in-the-loop
- **Security-First**: OWASP Top 10, defense-in-depth, LLM safety patterns
- **Production-Ready**: Patterns for FastAPI, React 19, PostgreSQL/pgvector
- **CC 2.1.2 Compliant**: All hooks tested and compliant

## Repository

https://github.com/yonatangross/skillforge-claude-plugin

## Author

[Yonatan Gross](https://github.com/yonatangross)

## License

MIT