---
name: dev-manager
description: Start the visual Kanban dashboard for MASTER_PLAN.md tracking
---

# /dev-manager Command

Start the visual Kanban dashboard that syncs with your MASTER_PLAN.md.

## Usage

```
/dev-manager              # Start on default port (6010)
/dev-manager 8080         # Start on custom port
/dev-manager stop         # Stop running server
/dev-manager status       # Check if server is running
```

## What It Does

The dev-manager is a Node.js server that:

1. **Parses MASTER_PLAN.md** into a visual Kanban board
2. **Live syncs changes** - edits in the board update MASTER_PLAN.md
3. **Watches for file changes** - external edits refresh the UI
4. **Provides a REST API** for task status updates

## Implementation

When the user runs `/dev-manager`:

1. **Check if dev-manager exists**
   ```bash
   if [ ! -d "dev-manager" ]; then
     echo "dev-manager not found. Run /dev-setup first."
     exit 1
   fi
   ```

2. **Install dependencies if needed**
   ```bash
   cd dev-manager
   if [ ! -d "node_modules" ]; then
     npm install
   fi
   ```

3. **Start the server**
   ```bash
   DEV_MANAGER_ROOT="$(pwd)/.." node server.js &
   ```

4. **Report status**
   ```
   ✅ Dev Manager running!

   Dashboard: http://localhost:6010
   API: http://localhost:6010/api/master-plan

   The dashboard syncs with docs/MASTER_PLAN.md
   Press Ctrl+C to stop.
   ```

## For `/dev-manager stop`:

1. Find the running process
   ```bash
   pkill -f "node.*dev-manager.*server.js"
   ```

2. Confirm termination
   ```
   ✅ Dev Manager stopped.
   ```

## For `/dev-manager status`:

1. Check if process is running
   ```bash
   pgrep -f "node.*dev-manager.*server.js"
   ```

2. Report status
   ```
   Dev Manager is running on port 6010
   PID: 12345
   ```
   or
   ```
   Dev Manager is not running.
   ```

## Dashboard Features

- **Kanban columns**: To Do, In Progress, Review, Done
- **Drag & drop**: Move tasks between columns
- **Task editing**: Click to edit title, priority, status
- **Live refresh**: Auto-updates when MASTER_PLAN.md changes
- **Progress bars**: Visual progress from checkbox completion
