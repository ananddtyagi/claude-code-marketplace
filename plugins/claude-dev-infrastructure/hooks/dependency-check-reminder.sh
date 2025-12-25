#!/bin/bash
# Dependency check reminder hook
# Reminds Claude to check the Task Dependency Index before starting work

echo "DEPENDENCY CHECK: Before starting work on any MASTER_PLAN task:"
echo "1. Check Task Dependency Index in docs/MASTER_PLAN.md (Active Work section)"
echo "2. Verify no file conflicts with IN_PROGRESS tasks"
echo "3. Check if task depends on incomplete work"
echo "4. Update Status column when starting/completing tasks"
