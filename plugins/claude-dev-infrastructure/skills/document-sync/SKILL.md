---
name: document-sync
description: A robust skill that analyzes your app's actual codebase, tech stack, configuration, and architecture to ensure ALL documentation is current and accurate. It never assumes—always verifies and compares the live system with every documentation file to detect code-doc drift and generate actionable updates.
---

# Document Sync Skill for Claude Code

## Overview

This skill provides comprehensive documentation synchronization by analyzing your actual codebase, tech stack, configuration, and architecture to ensure all documentation remains current and accurate. It operates on a "verify, never assume" principle, performing end-to-end comparisons against real code and dependencies to detect documentation drift automatically.

## Core Principles

- **Verify, Never Assume:** Documentation is only updated after end-to-end comparison against real, current code and dependencies
- **Deep System Introspection:** Checks languages, frameworks, APIs, DBs, config, code patterns, and deployment targets
- **Doc Trust Score:** Every doc gets a trust rating based on evidence found in the codebase and config files

## Quick Start

**Natural Language Commands:**
- "Run document sync analysis on my project"
- "Update docs so every API route matches the code"
- "Check if any doc mentions features no longer in the app"
- "List undocumented config variables"

**Slash Commands:**
- `/docs-sync` — Runs analysis and outputs a complete report on outdated/inaccurate sections
- `/docs-update-strict` — Suggests only changes verified by found code/config evidence
- `/docs-rewrite-missing` — Fills gaps for undocumented features based on live source
- `/docs-patch-pr` — Makes all doc changes as a PR, zero surprises

## Operation Workflow

### Phase 1: Full System Scan

Execute the system scanning script to analyze your codebase:

```bash
# Run comprehensive system scan
python3 .claude/skills/document-sync/scripts/system_scan.py
```

This phase automatically:
1. **Tech Stack Detection** - Parse `package.json`, `requirements.txt`, `pom.xml`, etc. for frameworks, DBs, and build tools
2. **Project Structure Analysis** - Map `src/`, `lib/`, `app/`, and `config/` directories for real usage
3. **Architecture Detection** - Identify data flows, auth methods, sync strategies, and cloud/on-prem deployment

**Key Outputs:** `system_state.json` and `code_features_report.md`

### Phase 2: Documentation Verification

Execute the documentation verification script:

```bash
# Verify all documentation against code
python3 .claude/skills/document-sync/scripts/verify_docs.py
```

This phase:
1. **Docs Content Inventory** - List all Markdown, docs/, and README files
2. **Technical Validation** - Cross-reference each doc claim with real code/config
3. **Relevance & Quality Scoring** - Rate every doc: current, needs update, obsolete, or missing

**Key Outputs:** `doc_verification_report.md` and `docs_update_plan.md`

### Phase 3: Automated or Assisted Document Updating

Based on the verification results, choose your update approach:

```bash
# Dry run - see what would change
python3 .claude/skills/document-sync/scripts/update_docs.py --mode=dry-run

# Suggest mode - get suggestions for review
python3 .claude/skills/document-sync/scripts/update_docs.py --mode=suggest

# Auto-update with backups
python3 .claude/skills/document-sync/scripts/update_docs.py --mode=auto-update
```

## Configuration

Create `.claude/document-sync-skill.yml` in your project root:

```yaml
mode: suggest  # suggest | dry-run | auto-update
protected_docs:
  - README.md
  - docs/security.md
review_required_for:
  - section removal
  - breaking doc changes
output_reports:
  - doc_verification_report.md
  - docs_update_plan.md
```

## Safety & Controls

- **Never deletes or rewrites without firm code evidence**
- **Always creates a diff and backup before change**
- **User sets conservatism level:** dry-run, suggest-only, or auto-update
- **All changes are traceable—committed separately with actionable summaries**

## Output Examples

**doc_verification_report.md**

| Doc Section         | Status     | Evidence Found                   | Action        |
|---------------------|------------|----------------------------------|---------------|
| `/docs/api.md` GET `/users`   | Current    | Endpoint in code (src/routes/)    | Keep          |
| `/docs/db-setup.md` PouchDB   | Outdated   | No mention in codebase            | Remove/Update |
| `/README.md` Feature X        | Missing    | Found in `src/feature-x.ts`       | Add details   |

**docs_update_plan.md**

- Remove obsolete DB doc: `/docs/db-setup.md` (no longer in code)
- Add section to `/README.md` for unlisted Feature X
- Rewrite `/docs/config.md` section on env vars (now using `.env.local`)
- Confirm all code-blocks in `/docs/usage.md` still run

## Resources

This skill includes specialized scripts and references for comprehensive document synchronization:

### scripts/
- **system_scan.py** - Comprehensive codebase analysis and tech stack detection
- **verify_docs.py** - Documentation verification and validation against code
- **update_docs.py** - Automated document updating with safety controls

### references/
- **tech_detection_patterns.md** - Patterns for identifying frameworks and technologies
- **doc_validation_rules.md** - Rules for validating documentation accuracy
- **update_templates.md** - Templates for common documentation updates

### assets/
- **report_templates/** - Markdown templates for verification and update reports
- **config_schemas/** - JSON schemas for configuration validation

## Safety Checklist

- [ ] Full project scan completed
- [ ] All doc claims matched to real code/config
- [ ] Backups created before overwriting docs
- [ ] No deletions/rewrites without clear code evidence
- [ ] All updates and removals require user review
- [ ] All code examples in docs validated with real source

## Success Metrics

- 100% doc claims match code/config truth
- 0 obsolete/incorrect references in doc set
- All new features in code are documented within 2 days
- Doc update effort reduced by >60% for every release

---

## MANDATORY USER VERIFICATION REQUIREMENT

### Policy: No Fix Claims Without User Confirmation

**CRITICAL**: Before claiming ANY issue, bug, or problem is "fixed", "resolved", "working", or "complete", the following verification protocol is MANDATORY:

#### Step 1: Technical Verification
- Run all relevant tests (build, type-check, unit tests)
- Verify no console errors
- Take screenshots/evidence of the fix

#### Step 2: User Verification Request
**REQUIRED**: Use the `AskUserQuestion` tool to explicitly ask the user to verify the fix:

```
"I've implemented [description of fix]. Before I mark this as complete, please verify:
1. [Specific thing to check #1]
2. [Specific thing to check #2]
3. Does this fix the issue you were experiencing?

Please confirm the fix works as expected, or let me know what's still not working."
```

#### Step 3: Wait for User Confirmation
- **DO NOT** proceed with claims of success until user responds
- **DO NOT** mark tasks as "completed" without user confirmation
- **DO NOT** use phrases like "fixed", "resolved", "working" without user verification

#### Step 4: Handle User Feedback
- If user confirms: Document the fix and mark as complete
- If user reports issues: Continue debugging, repeat verification cycle

### Prohibited Actions (Without User Verification)
- Claiming a bug is "fixed"
- Stating functionality is "working"
- Marking issues as "resolved"
- Declaring features as "complete"
- Any success claims about fixes

### Required Evidence Before User Verification Request
1. Technical tests passing
2. Visual confirmation via Playwright/screenshots
3. Specific test scenarios executed
4. Clear description of what was changed

**Remember: The user is the final authority on whether something is fixed. No exceptions.**
