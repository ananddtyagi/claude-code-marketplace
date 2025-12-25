# Dev Manager

Development management dashboard for Claude Code projects with Kanban board and MASTER_PLAN.md integration.

## Quick Start

```bash
# Navigate to dev-manager directory
cd dev-manager

# Install dependencies
npm install

# Start server (default port 6010)
npm start

# Or with custom configuration
DEV_MANAGER_ROOT=/path/to/your/project DEV_MANAGER_PORT=8080 npm start
```

Open http://localhost:6010 (or your custom port)

## Features

| Feature | Description |
|---------|-------------|
| **Kanban Board** | Visual task tracking synced with MASTER_PLAN.md |
| **Live Sync** | Real-time updates when MASTER_PLAN.md changes |
| **Task Editing** | Edit tasks directly from the UI |
| **Drag & Drop** | Move tasks between columns |

## Configuration

Environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DEV_MANAGER_ROOT` | Project root directory | Current directory |
| `DEV_MANAGER_PORT` | Server port | 6010 |

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/master-plan` | GET | Get MASTER_PLAN.md content |
| `/api/task/:id` | POST | Update task property |
| `/api/task/:id/status` | POST | Update task status |
| `/api/task/:id/move` | POST | Move task between columns |
| `/api/events` | GET | SSE endpoint for live updates |

## Integration

The dev-manager expects a `docs/MASTER_PLAN.md` file in your project root with the standard task tracking format:

```markdown
### TASK-XXX: Task Title (STATUS)

**Priority**: P2-MEDIUM

- [ ] Step 1
- [x] Step 2
```

See `templates/MASTER_PLAN.template.md` for the full format.
