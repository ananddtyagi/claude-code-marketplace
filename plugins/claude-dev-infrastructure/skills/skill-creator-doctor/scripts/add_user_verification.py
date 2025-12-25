#!/usr/bin/env python3
"""
Add mandatory user verification policy to all skills.

This script adds a standardized "User Verification Required" section to every
SKILL.md file, requiring explicit user confirmation before any issue can be
claimed as "fixed".
"""

import os
import sys
from pathlib import Path

# The mandatory user verification policy to add to all skills
USER_VERIFICATION_POLICY = """
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
"""

def find_skill_files(base_path: str) -> list[Path]:
    """Find all SKILL.md files in the skills directory."""
    base = Path(base_path)
    skill_files = []

    for item in base.iterdir():
        if item.is_dir() and not item.name.startswith('.'):
            skill_md = item / "SKILL.md"
            if skill_md.exists():
                skill_files.append(skill_md)

    return skill_files

def has_verification_section(content: str) -> bool:
    """Check if the skill already has the verification section."""
    return "MANDATORY USER VERIFICATION REQUIREMENT" in content

def add_verification_policy(skill_file: Path) -> tuple[bool, str]:
    """Add the verification policy to a skill file if not present."""
    try:
        content = skill_file.read_text(encoding='utf-8')

        if has_verification_section(content):
            return False, f"Already has verification section: {skill_file}"

        # Add the policy at the end of the file
        updated_content = content.rstrip() + "\n" + USER_VERIFICATION_POLICY

        skill_file.write_text(updated_content, encoding='utf-8')
        return True, f"Added verification policy to: {skill_file}"

    except Exception as e:
        return False, f"Error processing {skill_file}: {e}"

def main():
    # Default skills directory
    skills_dir = "/home/noam/my-projects/Development/My-Dev/Productivity/pomo-flow/.claude/skills"

    if len(sys.argv) > 1:
        skills_dir = sys.argv[1]

    print(f"Scanning skills directory: {skills_dir}")
    print("=" * 60)

    skill_files = find_skill_files(skills_dir)
    print(f"Found {len(skill_files)} skill files")
    print()

    added = 0
    skipped = 0
    errors = 0

    for skill_file in sorted(skill_files):
        success, message = add_verification_policy(skill_file)
        print(message)

        if success:
            added += 1
        elif "Already has" in message:
            skipped += 1
        else:
            errors += 1

    print()
    print("=" * 60)
    print(f"Summary:")
    print(f"  Added verification policy: {added}")
    print(f"  Already had policy (skipped): {skipped}")
    print(f"  Errors: {errors}")
    print(f"  Total processed: {len(skill_files)}")

if __name__ == "__main__":
    main()
