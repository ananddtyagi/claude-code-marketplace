---
description: Update the CLAUDE.md file to reflect major changes in the codebase
---

# Update CLAUDE.md Command

You should update the `CLAUDE.md` or `.claude/CLAUDE.md` file to reflect recent major changes in the codebase.

## Purpose

The CLAUDE.md file serves as a high-level guide for Claude Code (and other AI assistants) to understand:
- Project structure and organization
- Key architectural decisions
- Important conventions and patterns
- Where to find things
- What to watch out for

## When to Update

Update CLAUDE.md after:
- Major refactoring or restructuring
- New features or modules added
- Changes to architecture or patterns
- Updates to dependencies or tooling
- Changes to conventions or standards
- New directories or significant file moves

## What to Include

### 1. Project Overview
- Brief description of what the project does
- Tech stack and key dependencies
- Development setup instructions

### 2. Architecture & Structure
```markdown
## Project Structure

- `/src` - Main application code
  - `/components` - React components
  - `/services` - Business logic and API calls
  - `/utils` - Helper functions
  - `/types` - TypeScript type definitions
- `/tests` - Test files
- `/docs` - Documentation
- `/scripts` - Build and utility scripts
```

### 3. Key Patterns & Conventions
- Code organization patterns
- Naming conventions
- State management approach
- Error handling patterns
- Testing strategies

### 4. Important Notes
- Gotchas or common pitfalls
- Performance considerations
- Security requirements
- Browser/platform support
- Third-party integrations

### 5. Development Workflow
- How to run locally
- How to run tests
- How to build
- How to deploy
- Branch strategy

## Format Example

```markdown
# Project Name

## Overview
Brief description of the project and its purpose.

## Tech Stack
- Framework/Language
- Key libraries and tools
- Database
- Infrastructure

## Project Structure
[Detailed structure as shown above]

## Architecture
Describe the high-level architecture:
- Frontend architecture (React, state management)
- Backend architecture (API structure, services)
- Database design
- External integrations

## Key Conventions
- File naming: kebab-case for components, camelCase for utilities
- Component structure: Functional components with hooks
- State management: Redux Toolkit for global state
- Styling: CSS Modules with BEM naming
- Testing: Jest + React Testing Library

## Important Notes
- Authentication uses JWT tokens stored in httpOnly cookies
- API rate limiting is 100 requests per minute
- Image uploads are handled by AWS S3
- Background jobs use Bull queue with Redis

## Development
```bash
# Install dependencies
npm install

# Run locally
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

## Where to Find Things
- API endpoints: `/src/routes`
- Database models: `/src/models`
- Authentication logic: `/src/middleware/auth.js`
- Email templates: `/src/templates/email`

## Common Tasks
- Adding a new API endpoint: Create route in `/src/routes`, add controller in `/src/controllers`
- Adding a new database table: Create migration in `/migrations`, add model in `/src/models`
- Adding a new React page: Create component in `/src/pages`, add route in `/src/App.js`
```

## Your Task

1. **Locate the CLAUDE.md file** (or create it if it doesn't exist)
   - Check for `CLAUDE.md` or `.claude/CLAUDE.md`
   - If neither exists, create `.claude/CLAUDE.md`

2. **Review recent changes**
   - Look at git history for major changes
   - Review current project structure
   - Note any new patterns or conventions

3. **Update the file**
   - Add new sections for new features/modules
   - Update structure diagrams
   - Document new conventions or patterns
   - Update any outdated information
   - Add notes about recent major changes

4. **Keep it concise but comprehensive**
   - Focus on what's important for understanding the codebase
   - Don't duplicate documentation that exists elsewhere (link to it)
   - Highlight things that aren't obvious from the code alone

## Remember

- CLAUDE.md is a living document - it should evolve with the codebase
- Focus on information that helps understand the big picture
- Be specific enough to be useful, but high-level enough to stay relevant
- Update it proactively, not just when asked
- Think about what would help someone (or AI) new to the codebase get oriented quickly

