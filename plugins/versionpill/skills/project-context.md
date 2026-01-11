# Project Context Skill

Get comprehensive project context from Version Pill to understand:
- Project overview and goals
- Tech stack and conventions
- Current tasks in progress
- Recent decisions and learnings

## Usage

At the start of any session, call:
```
get_ai_context(projectId)
```

This returns everything you need to understand the project and start working effectively.

## What's Included

1. **Context Docs** - Global and project-specific context (like CLAUDE.md)
2. **Active Work** - Tasks currently in progress
3. **Priorities** - What should be worked on next
4. **Decisions** - Architecture Decision Records (ADRs)
5. **Tech Stack** - Languages, frameworks, conventions

## Best Practices

- Call `get_ai_context` at session start
- Use `start_task` before working on a task
- Use `complete_task` when done (logs learnings)
- Use `brain_dump` to sync discoveries back
