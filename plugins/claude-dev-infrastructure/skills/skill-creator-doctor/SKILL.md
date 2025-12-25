---
name: skill-creator-doctor
description: Create, repair, maintain, and consolidate skills. This skill should be used when users want to create new skills, fix broken skills that won't load, diagnose skill system issues, maintain skill health, or consolidate duplicate/obsolete skills. Automatically detects and repairs common skill loading problems including missing registry entries, metadata format issues, and structural problems. Provides comprehensive skill ecosystem management including duplicate detection, merge workflows, and archival processes.
license: Complete terms in LICENSE.txt
---

# Skill Creator Doctor

This skill provides comprehensive skill lifecycle management: creation, repair, and maintenance.

## About Skills

Skills are modular, self-contained packages that extend Claude's capabilities by providing
specialized knowledge, workflows, and tools. Think of them as "onboarding guides" for specific
domains or tasks—they transform Claude from a general-purpose agent into a specialized agent
equipped with procedural knowledge that no model can fully possess.

### What Skills Provide

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats or APIs
3. Domain expertise - Company-specific knowledge, schemas, business logic
4. Bundled resources - Scripts, references, and assets for complex and repetitive tasks

### Anatomy of a Skill

Every skill consists of a required SKILL.md file and optional bundled resources:

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter metadata (required)
│   │   ├── name: (required)
│   │   └── description: (required)
│   └── Markdown instructions (required)
└── Bundled Resources (optional)
    ├── scripts/          - Executable code (Python/Bash/etc.)
    ├── references/       - Documentation intended to be loaded into context as needed
    └── assets/           - Files used in output (templates, icons, fonts, etc.)
```

#### SKILL.md (required)

**Metadata Quality:** The `name` and `description` in YAML frontmatter determine when Claude will use the skill. Be specific about what the skill does and when to use it. Use the third-person (e.g. "This skill should be used when..." instead of "Use this skill when...").

#### Bundled Resources (optional)

##### Scripts (`scripts/`)

Executable code (Python/Bash/etc.) for tasks that require deterministic reliability or are repeatedly rewritten.

- **When to include**: When the same code is being rewritten repeatedly or deterministic reliability is needed
- **Example**: `scripts/rotate_pdf.py` for PDF rotation tasks
- **Benefits**: Token efficient, deterministic, may be executed without loading into context
- **Note**: Scripts may still need to be read by Claude for patching or environment-specific adjustments

##### References (`references/`)

Documentation and reference material intended to be loaded as needed into context to inform Claude's process and thinking.

- **When to include**: For documentation that Claude should reference while working
- **Examples**: `references/finance.md` for financial schemas, `references/mnda.md` for company NDA template, `references/policies.md` for company policies, `references/api_docs.md` for API specifications
- **Use cases**: Database schemas, API documentation, domain knowledge, company policies, detailed workflow guides
- **Benefits**: Keeps SKILL.md lean, loaded only when Claude determines it's needed
- **Best practice**: If files are large (>10k words), include grep search patterns in SKILL.md
- **Avoid duplication**: Information should live in either SKILL.md or references files, not both. Prefer references files for detailed information unless it's truly core to the skill—this keeps SKILL.md lean while making information discoverable without hogging the context window. Keep only essential procedural instructions and workflow guidance in SKILL.md; move detailed reference material, schemas, and examples to references files.

##### Assets (`assets/`)

Files not intended to be loaded into context, but rather used within the output Claude produces.

- **When to include**: When the skill needs files that will be used in the final output
- **Examples**: `assets/logo.png` for brand assets, `assets/slides.pptx` for PowerPoint templates, `assets/frontend-template/` for HTML/React boilerplate, `assets/font.ttf` for typography
- **Use cases**: Templates, images, icons, boilerplate code, fonts, sample documents that get copied or modified
- **Benefits**: Separates output resources from documentation, enables Claude to use files without loading them into context

### Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently:

1. **Metadata (name + description)** - Always in context (~100 words)
2. **SKILL.md body** - When skill triggers (<5k words)
3. **Bundled resources** - As needed by Claude (Unlimited*)

*Unlimited because scripts can be executed without reading into context window.

## Skill Creation Process

To create a skill, follow the "Skill Creation Process" in order, skipping steps only if there is a clear reason why they are not applicable.

### Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood. It remains valuable even when working with an existing skill.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building an image-editor skill, relevant questions include:

- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"
- "What would a user say that should trigger this skill?"

To avoid overwhelming users, avoid asking too many questions in a single message. Start with the most important questions and follow up as needed for better effectiveness.

Conclude this step when there is a clear sense of the functionality the skill should support.

### Step 2: Planning the Reusable Skill Contents

To turn concrete examples into an effective skill, analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

Example: When building a `pdf-editor` skill to handle queries like "Help me rotate this PDF," the analysis shows:

1. Rotating a PDF requires re-writing the same code each time
2. A `scripts/rotate_pdf.py` script would be helpful to store in the skill

Example: When designing a `frontend-webapp-builder` skill for queries like "Build me a todo app" or "Build me a dashboard to track my steps," the analysis shows:

1. Writing a frontend webapp requires the same boilerplate HTML/React each time
2. An `assets/hello-world/` template containing the boilerplate HTML/React project files would be helpful to store in the skill

Example: When building a `big-query` skill to handle queries like "How many users have logged in today?" the analysis shows:

1. Querying BigQuery requires re-discovering the table schemas and relationships each time
2. A `references/schema.md` file documenting the table schemas would be helpful to store in the skill

To establish the skill's contents, analyze each concrete example to create a list of the reusable resources to include: scripts, references, and assets.

### Step 3: Initializing the Skill

At this point, it is time to actually create the skill.

Skip this step only if the skill being developed already exists, and iteration or packaging is needed. In this case, continue to the next step.

When creating a new skill from scratch, always run the `init_skill.py` script. The script conveniently generates a new template skill directory that automatically includes everything a skill requires, making the skill creation process much more efficient and reliable.

Usage:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script:

- Creates the skill directory at the specified path
- Generates a SKILL.md template with proper frontmatter and TODO placeholders
- Creates example resource directories: `scripts/`, `references/`, and `assets/`
- Adds example files in each directory that can be customized or deleted

After initialization, customize or remove the generated SKILL.md and example files as needed.

### Step 4: Edit the Skill

When editing the (newly-generated or existing) skill, remember that the skill is being created for another instance of Claude to use. Focus on including information that would be beneficial and non-obvious to Claude. Consider what procedural knowledge, domain-specific details, or reusable assets would help another Claude instance execute these tasks more effectively.

#### Start with Reusable Skill Contents

To begin implementation, start with the reusable resources identified above: `scripts/`, `references/`, and `assets/` files. Note that this step may require user input. For example, when implementing a `brand-guidelines` skill, the user may need to provide brand assets or templates to store in `assets/`, or documentation to store in `references/`.

Also, delete any example files and directories not needed for the skill. The initialization script creates example files in `scripts/`, `references/`, and `assets/` to demonstrate structure, but most skills won't need all of them.

#### Update SKILL.md

**Writing Style:** Write the entire skill using **imperative/infinitive form** (verb-first instructions), not second person. Use objective, instructional language (e.g., "To accomplish X, do Y" rather than "You should do X" or "If you need to do X"). This maintains consistency and clarity for AI consumption.

To complete SKILL.md, answer the following questions:

1. What is the purpose of the skill, in a few sentences?
2. When should the skill be used?
3. In practice, how should Claude use the skill? All reusable skill contents developed above should be referenced so that Claude knows how to use them.

### Step 5: Packaging a Skill

Once the skill is ready, it should be packaged into a distributable zip file that gets shared with the user. The packaging process automatically validates the skill first to ensure it meets all requirements:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Optional output directory specification:

```bash
scripts/package_skill.py <path/to/skill-folder> ./dist
```

The packaging script will:

1. **Validate** the skill automatically, checking:
   - YAML frontmatter format and required fields
   - Skill naming conventions and directory structure
   - Description completeness and quality
   - File organization and resource references

2. **Package** the skill if validation passes, creating a zip file named after the skill (e.g., `my-skill.zip`) that includes all files and maintains the proper directory structure for distribution.

If validation fails, the script will report the errors and exit without creating a package. Fix any validation errors and run the packaging command again.

### Step 6: Iterate

After testing the skill, users may request improvements. Often this happens right after using the skill, with fresh context of how the skill performed.

**Iteration workflow:**
1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again

## Skill Repair & Maintenance

### When Skills Break

Skills can fail to load due to various issues. Common symptoms include:
- **"Unknown skill" errors** when trying to activate a skill
- **Missing registry entries** in skills.json
- **Invalid metadata format** in SKILL.md frontmatter
- **Structural problems** with missing directories or files

### Automated Skill Repair

Use the built-in repair functionality to automatically diagnose and fix common issues:

```bash
# Repair a specific skill
scripts/repair_skill.py <skill-name>

# Diagnose without repairing
scripts/repair_skill.py --diagnose <skill-name>

# List all skills with issues
scripts/repair_skill.py --list-issues
```

### Common Repair Scenarios

#### Scenario 1: Skill Not Found in Registry
**Problem**: "Error: Unknown skill: my-skill-name"
**Solution**: The repair script automatically adds missing skills to the skills.json registry with proper metadata extracted from SKILL.md.

#### Scenario 2: Invalid Frontmatter Format
**Problem**: YAML parsing errors or missing required fields
**Solution**: The repair script fixes frontmatter format, adds missing required fields (name, description), and ensures proper YAML structure.

#### Scenario 3: Missing Skill Structure
**Problem**: Missing SKILL.md or required directories
**Solution**: The repair script identifies structural issues and provides guidance for fixing them.

#### Scenario 4: Category Not Defined
**Problem**: Skill references undefined category in registry
**Solution**: The repair script adds missing category definitions to skills.json.

### Manual Registry Fixes

For advanced users, skills.json can be manually edited:

```json
{
  "skills": {
    "my-skill": {
      "name": "My Skill Display Name",
      "category": "create",
      "triggers": ["using my skill", "activate my skill"],
      "keywords": ["my", "skill", "automation"],
      "activation_count": 0,
      "last_used": null,
      "related_skills": ["skill-creator-doctor"],
      "description": "Skill description for discovery"
    }
  },
  "categories": {
    "create": {
      "description": "Skills for building new components and features",
      "color": "#45B7D1"
    }
  }
}
```

### Skill Health Monitoring

Regular maintenance ensures skills remain functional:

```bash
# Validate a single skill
python scripts/quick_validate.py <path/to/skill>

# Comprehensive system health check
scripts/repair_skill.py --list-issues
```

### Prevention Best Practices

1. **Always validate skills** after creation with the packaging script
2. **Test skill loading** immediately after creation or modification
3. **Use consistent naming** between directory names and registry entries
4. **Maintain proper YAML format** in SKILL.md frontmatter
5. **Update registry entries** when modifying skill metadata

### Real-World Example: ts-foundation-restorer

The ts-foundation-restorer skill was successfully repaired using this system:

**Issue**: Skill existed in filesystem but wasn't discoverable
**Root Cause**: Missing registry entry in skills.json
**Solution**: Added proper registry entry with metadata extracted from SKILL.md
**Result**: Skill became discoverable and functional

This demonstrates how the repair system can quickly resolve skill loading failures without manual intervention.

## Advanced Troubleshooting Guide

### Understanding Claude Code Skill Discovery

Claude Code uses a **declarative, prompt-based system** for skill discovery. The system scans skills from multiple locations and loads metadata into the system prompt. Claude decides when to invoke skills based on textual descriptions—there's no algorithmic matching at the code level.

### Critical YAML Frontmatter Requirements

The most common cause of "Unknown skill" errors is **YAML frontmatter validation failures**.

**Required Fields:**
- `name`: Must use **lowercase letters, numbers, and hyphens only** (kebab-case), max 64 characters
- `description`: Brief description (max 1024 characters)

**Correct Format:**
```yaml
---
name: my-skill-name
description: Brief description of what the skill does and when to use it
---
```

**Common Validation Failures:**

❌ **Title Case**: `name: My Skill Name`
❌ **snake_case**: `name: my_skill_name`
❌ **camelCase**: `name: mySkillName`
❌ **Underscores**: `name: my_skill_name`
❌ **XML tags**: `<name>my-skill</name>`
❌ **Reserved words**: Names containing "anthropic", "claude"

### Systematic Troubleshooting Process

#### 1. Validate YAML Frontmatter Format

Check for common issues:

```bash
# View the frontmatter
cat .claude/skills/my-skill/SKILL.md | head -n 15

# Common issues to look for:
# - Missing opening or closing ---
# - Tabs instead of spaces (use spaces only)
# - Unquoted strings with special characters
# - Extra spaces or hidden characters
```

#### 2. Check for Hidden Characters and Encoding

Even if YAML looks correct, hidden characters can cause parsing failures:

```bash
# Check for hidden characters
cat -A .claude/skills/my-skill/SKILL.md | head -n 15

# Verify UTF-8 encoding
file .claude/skills/my-skill/SKILL.md
```

#### 3. Verify File Structure

Ensure the directory structure is correct:

```
.claude/skills/my-skill/
└── SKILL.md  (required, exact capitalization)
```

The file **must** be named `SKILL.md` (all caps).

#### 4. Clear Claude Code Cache

Claude Code maintains caches that may not refresh after skill modifications:

```bash
# Option 1: Use /clear command (may not fully clear skill cache)
# In Claude Code session, type:
/clear

# Option 2: Completely restart Claude Code (recommended)
# Exit current session and restart:
claude
```

For persistent cache issues:
- Quit Claude Code completely
- Clear cache directories (if they exist):
  - macOS: `~/Library/Caches/Claude/`
  - Clear any residual temp files
- Restart Claude Code

#### 5. Test with Minimal Skill

Create a test skill to isolate the issue:

```bash
mkdir -p .claude/skills/test-skill
cat > .claude/skills/test-skill/SKILL.md << 'EOF'
---
name: test-skill
description: Simple test skill for validation
---

# Test Skill

This is a test skill.
EOF
```

Restart Claude Code and test if the minimal skill works.

### Known Issues and Limitations

#### 1. SDK vs CLI Behavior

Skills may not load correctly when using the Claude Agent SDK compared to the standalone CLI. If you're using the SDK, this is a known issue where skills are not auto-discovered despite correct configuration.

#### 2. Skill System Cache Inconsistencies

- The `/clear` command may not fully clear skill-related caches
- Skills added or modified during a session may require a **complete restart** to be recognized
- Some users report skills only load after exiting and restarting Claude Code entirely

#### 3. Frontmatter Parser Strictness

The frontmatter parser is extremely strict and may reject files that appear valid. The parser specifically checks for:
- Exact YAML syntax (no tabs, proper spacing)
- Kebab-case naming convention
- Absence of reserved words
- No XML tags or special characters in metadata

### Advanced Debugging Techniques

#### 1. Compare Working vs Broken Skills

Since some skills work correctly, compare their frontmatter format exactly:

```bash
# View working skill
cat .claude/skills/working-skill/SKILL.md | head -n 15

# View broken skill
cat .claude/skills/broken-skill/SKILL.md | head -n 15

# Look for differences in:
# - Spacing (tabs vs spaces)
# - Line endings (CRLF vs LF)
# - Character encoding
# - YAML structure
```

#### 2. Check Claude Code Logs

View logs to see specific skill loading errors:

- **macOS**: `~/Library/Logs/Claude/`
- **Linux**: Check terminal output with `--verbose` flag
- Look for parsing errors or skill validation failures

### Recommended Solution Path

Based on troubleshooting experience, follow these steps in order:

1. **Recreate the SKILL.md file** with guaranteed-clean formatting:
   - Copy the content to a new file
   - Ensure name uses only lowercase letters, numbers, and hyphens
   - Use spaces (not tabs) for indentation
   - Save with UTF-8 encoding, Unix line endings (LF)

2. **Verify the exact name format**:
   ```yaml
   ---
   name: my-skill-name
   description: Your description here
   ---
   ```

3. **Completely restart Claude Code**:
   - Exit the current session
   - Close all terminal windows
   - Start fresh with `claude`

4. **Test skill recognition**:
   - Ask: "List all available Skills"
   - Check if your skill appears

5. **If still failing**, try renaming the skill:
   - Change to something simpler: `my-skill` or `skill-fix`
   - Sometimes shorter names work better

### Why Some Skills Work and Others Don't

The inconsistency you're experiencing (some skills load, others don't with identical formats) suggests:

1. **Subtle formatting differences** invisible to the eye (tabs vs spaces, line endings)
2. **Character encoding issues** in the specific file
3. **Cache corruption** for that particular skill
4. **Name validation edge case**

The fact that renaming doesn't help suggests the issue is likely in the file content itself (encoding, hidden characters, or YAML structure) rather than the name.

## Skill Consolidation & Optimization

Manage growing skill collections by identifying duplicates, resolving conflicts, merging similar skills, and archiving obsolete skills. This ensures your skill ecosystem remains efficient, maintainable, and free of redundancy.

### When to Use

- **Managing growing skill collections** (10+ skills)
- **Suspecting duplicate/overlapping skills** with similar purposes
- **Changing technology stacks** (e.g., migrating from MongoDB to PostgreSQL)
- **Removing deprecated features** or outdated workflows
- **Similar names/triggers/keywords** causing activation confusion
- **Wanting to optimize the skill ecosystem** for better organization

### Core Workflows

#### Workflow 1: Scan & Inventory
Build comprehensive inventory of all skills with usage statistics and metadata.

```bash
# Generate skill inventory
python scripts/scan_skills.py --output skill_inventory.json
```

**What it does:**
- Scans all skills in skills/ directory
- Extracts metadata: name, description, category, triggers, keywords
- Reads usage stats from config/skills.json
- Analyzes bundled resources: scripts, references, assets
- Outputs structured JSON with summary statistics

**Output includes:**
- Skill metadata and purpose
- Activation counts and last used dates
- Resource analysis (scripts, references, assets)
- Category distribution
- Usage patterns and trends

#### Workflow 2: Analyze Similarity
Identify merge candidates, trigger conflicts, and obsolete skills.

```bash
# Analyze for consolidation opportunities
python scripts/analyze_similarity.py --inventory skill_inventory.json --threshold 0.65

# Custom threshold
python scripts/analyze_similarity.py --inventory skill_inventory.json --threshold 0.80
```

**Similarity Detection Methods:**

1. **Keyword/Trigger Overlap** (Jaccard Similarity)
   - J(A,B) = |A ∩ B| / |A ∪ B|
   - Identifies skills with shared triggers (conflicts)
   - Detects >50% trigger overlap

2. **Content Similarity**
   - Compares skill descriptions and metadata
   - Analyzes semantic similarity
   - Identifies complementary workflows

3. **Category Matching**
   - Skills in same category have higher consolidation likelihood
   - Groups related domain-specific skills

4. **Usage Statistics**
   - Identifies unused skills (activation_count = 0)
   - Finds outdated skills (last_used > 6 months)
   - Prioritizes based on usage patterns

**Outputs:**
- `skill_consolidation_report.md` (human-readable recommendations)
- `skill_analysis.json` (detailed analysis data)
- Priority categorization: High (>80%), Medium (65-80%), Review (<65%)

#### Workflow 3: Review Consolidation Report
Analyze the generated report and make informed decisions.

```bash
# Open the generated report
cat skill_consolidation_report.md

# Key sections to review:
# - High Priority Merge Candidates (>80% similarity)
# - Trigger Conflicts (ambiguous activations)
# - Obsolete Skills (unused or outdated)
# - Medium Priority Candidates (65-80% similarity)
```

**Decision Criteria:**

**Merge When:**
- 80%+ similarity with overlapping functionality
- Trigger conflicts causing ambiguous activation
- Complementary workflows in same domain
- One skill rarely used, fits naturally in another

**Archive When:**
- Never used (activation_count = 0)
- Not used in 6+ months
- Tech stack changed (old technology references)
- Features removed from project

#### Workflow 4: Execute Skill Merges
Safely merge similar skills while preserving functionality.

**Natural Language Commands:**
```
"Merge task-creator and task-manager based on the consolidation report"
"Combine these duplicate Vue debugging skills"
"Merge skill-a into skill-b, keep skill-b as primary"
```

**Merge Process:**
1. **Analyze both skills** - Read SKILL.md files completely
2. **Identify unique content** - Find different/valuable content in each
3. **Create unified SKILL.md** - Preserve all unique functionality
4. **Combine metadata** - Merge triggers, keywords, related_skills
5. **Copy bundled resources** - Move scripts/references/assets to primary skill
6. **Update registry** - Modify config/skills.json with merged metadata
7. **Archive secondary skill** - Move to skills/archive/ with documentation
8. **Validate merged skill** - Ensure it loads and functions correctly
9. **Report completion** - List merged triggers/keywords and changes

**Registry Updates:**
```json
{
  "merged_from": ["task-creator", "task-editor"],
  "activation_count": 37,  // Sum of both skills
  "triggers": ["create task", "edit task", "manage tasks", "task operations"],
  "last_used": "2025-11-13"  // Most recent date
}
```

#### Workflow 5: Archive/Remove Obsolete Skills
Clean up unused or outdated skills safely.

**Natural Language Commands:**
```
"Archive old-mongodb-helper skill, we migrated to PostgreSQL"
"Remove unused-experimental-skill, it was never activated"
"Archive all skills related to deprecated feature X"
```

**Archive Process:**
1. **Create archive directory** - `skills/archive/[skill-name]archived[date]/`
2. **Move skill** - Relocate entire skill directory
3. **Create ARCHIVED.md** - Document reason, date, and restoration instructions
4. **Update registry** - Remove skill entry from config/skills.json
5. **Update references** - Remove from related_skills in other skills
6. **Update archive index** - Add to skills/archive/ARCHIVE_INDEX.md

**ARCHIVED.md Template:**
```markdown
# Archived: [skill-name]

**Archive Date:** 2025-11-13
**Reason:** [Archive reason]
**Original Description:** [Skill description]

## Archive Reason
[Detailed explanation of why skill was archived]

## Restoration Instructions
To restore this skill:
1. Move directory from `archive/` back to `skills/`
2. Add entry to `config/skills.json`
3. Update any related_skills references
4. Test skill loading

## Related Skills
[List of skills that referenced this skill]
```

### Natural Language Interface

Use consolidation features through natural conversation:

**Analysis Commands:**
- "Scan my skills and find duplicates"
- "Analyze my skills for consolidation opportunities"
- "Find skills I haven't used in 6 months"
- "Check for trigger conflicts in my skills"
- "What consolidation opportunities do I have?"

**Action Commands:**
- "Merge [skill-a] and [skill-b]"
- "Archive [old-skill] because [reason]"
- "Combine these Vue debugging skills"
- "We migrated from MongoDB to PostgreSQL, clean up old skills"
- "Fix the trigger conflicts for 'create task'"

### Examples

#### Example 1: Duplicate Skills
```
User: "I created task-creator and later task-manager. Are they duplicates?"

Claude analyzes:
- task-creator: "Create new tasks" (triggers: ["create task", "new task"], activations: 25)
- task-manager: "Create, edit, delete tasks" (triggers: ["manage tasks", "create task"], activations: 12)

Finding: 87% similar (overlapping triggers, similar purpose)

Recommendation: Merge into task-manager (more used, broader scope)

Execution:
- Merges both skills into task-manager
- Archives task-creator
- Updates registry with merged_from field
- Reports completion with consolidated triggers
```

#### Example 2: Tech Stack Migration
```
User: "We migrated from MongoDB to PostgreSQL. Which skills should I clean up?"

Claude:
- Scans all skills
- Finds: mongodb-helper, mongo-query-builder, mongodb-schema
- Recommends: Archive all three, update database-helper to focus on PostgreSQL

Execution:
- Archives MongoDB skills with proper documentation
- Updates database-helper with PostgreSQL-specific content
- Removes MongoDB skills from registry
- Updates related_skills references
```

#### Example 3: Trigger Conflicts
```
User: "Check for trigger conflicts"

Claude finds:
- "create task" used by: task-creator, task-manager, project-tasks

Recommendation:
- task-creator: Change to "create new task", "add task"
- task-manager: Keep "manage tasks", "organize tasks"
- project-tasks: Change to "create project task", "add to project"

Execution:
- Updates triggers in each skill's registry entry
- Validates no conflicts remain
- Reports updated trigger mappings
```

### Best Practices

#### Naming Consolidated Skills
- Use broader names: `task-creator` + `task-editor` → `task-manager`
- Use domain + action pattern: `[domain]-[action]`
- Avoid vague names: "helper", "utils"
- Keep names under 64 characters with kebab-case

#### Maintenance Schedule
- **Monthly (5 minutes):** Quick scan for obvious duplicates
- **Quarterly (30-60 minutes):** Full analysis and consolidation
- **After major changes:** Tech stack migration, feature removal

#### Quality Assurance
- Always test merged skills before archiving originals
- Keep archive documentation thorough
- Validate registry consistency after changes
- Test skill loading after major consolidation

### Implementation Scripts

#### scan_skills.py
Scans skills directory and extracts comprehensive inventory including metadata, usage statistics, bundled resources analysis, and emoji assignments.

#### analyze_similarity.py
Analyzes skill inventory using multiple similarity detection methods to identify merge candidates, trigger conflicts, and obsolete skills. Generates detailed consolidation reports with emoji-enhanced displays.

#### assign_emoji.py
Comprehensive emoji management utility for skills. Supports custom emoji assignment, conflict detection, category-based defaults, and batch operations. Integrates with both registry and SKILL.md frontmatter.

### References

- `references/skill-consolidation-guide.md` - Quick start guide with examples
- `skill_consolidation_report.md` - Generated analysis report
- `skill_analysis.json` - Detailed analysis data

## Skill Emoji Management

Manage visual identification of skills through custom emoji assignment. Emojis appear during skill activation and execution, providing instant recognition of active skills and better user experience.

### When to Use Emoji Management

- **Visual Skill Identification**: Make skills instantly recognizable during activation
- **Category Organization**: Use consistent emojis for skill categories (🐛 debug, ⚡ create, 🔧 fix)
- **Custom Branding**: Assign specific emojis to important or frequently used skills
- **Folder Organization**: Align folder names with registry emoji assignments
- **Team Consistency**: Standardize emoji usage across team skill collections

### Emoji Assignment Workflow

#### Workflow 1: Individual Skill Emoji Assignment

**Natural Language Commands:**
```
"Assign 🎨 emoji to ui-design skill"
"Set custom emoji for vue-debugging to 🐛"
"Give the database-helper skill the 🗃️ emoji"
```

**Script Execution:**
```bash
# Assign specific emoji to skill
python scripts/assign_emoji.py --skill vue-debugging --emoji "🐛"

# The system will:
# 1. Validate emoji character
# 2. Check for conflicts with other skills
# 3. Update skills.json registry
# 4. Update SKILL.md frontmatter
# 5. Report success or conflicts
```

#### Workflow 2: Category-Based Emoji Assignment

**Natural Language Commands:**
```
"Assign 🐛 emoji to all debug skills"
"Set ⚡ emoji for create category skills"
"Apply default emojis to all skills in fix category"
```

**Script Execution:**
```bash
# Assign emoji to entire category
python scripts/assign_emoji.py --category debug --emoji "🐛"

# System will:
# 1. Find all skills in the category
# 2. Check for emoji conflicts
# 3. Update all skills in category
# 4. Handle conflicts with user confirmation
```

#### Workflow 3: Automatic Emoji Assignment

**Natural Language Commands:**
```
"Auto-assign default emojis to all skills"
"Apply category-based emojis to skills without custom assignments"
"Set up emoji defaults for my entire skill collection"
```

**Script Execution:**
```bash
# Auto-assign based on categories
python scripts/assign_emoji.py --auto-assign

# System will:
# 1. Identify skills without emojis
# 2. Apply category default emojis
# 3. Handle conflicts intelligently
# 4. Report assignments and any conflicts
```

#### Workflow 4: Emoji Conflict Resolution

**Natural Language Commands:**
```
"Check for emoji conflicts in my skills"
"Show me which skills have duplicate emojis"
"Suggest alternative emojis for conflicting skills"
```

**Script Execution:**
```bash
# List all emoji assignments and conflicts
python scripts/assign_emoji.py --list

# The system will:
# 1. Show all emoji assignments
# 2. Highlight conflicts (multiple skills with same emoji)
# 3. List skills without emojis
# 4. Provide suggestions for resolution
```

#### Workflow 5: Emoji Suggestions

**Natural Language Commands:**
```
"Suggest emojis for my new skill"
"What emoji would work best for api-integration skill?"
"Recommend emojis based on my skill description"
```

**Script Execution:**
```bash
# Get emoji suggestions for a skill
python scripts/assign_emoji.py --suggest skill-name

# System will:
# 1. Analyze skill name, category, and description
# 2. Suggest relevant emojis based on keywords
# 3. Check for conflicts with existing assignments
# 4. Provide context for each suggestion
```

### Emoji Category Defaults

The system includes built-in emoji defaults for common skill categories:

```json
{
  "emoji_defaults": {
    "debug": "🐛",      // Bug fixing and troubleshooting
    "create": "⚡",     // Building and creating
    "fix": "🔧",        // Maintenance and repair
    "optimize": "🚀",   // Performance and optimization
    "test": "🧪",      // Testing and validation
    "analyze": "📊",    // Analysis and reporting
    "implement": "🛠️",  // Implementation and development
    "specialized": "⭐", // Specialized functionality
    "meta": "🎯",       // Meta-skills and management
    "emergency": "🚨",   // Emergency and critical issues
    "default": "⚙️"     // Generic fallback
  }
}
```

### Folder Name Integration

Use the **skill-folder-emoji-updater** skill to synchronize folder names with registry assignments:

**Natural Language Commands:**
```
"Update all skill folders to match their registry emojis"
"Add 🐛 emoji to all debug skill folders"
"Make sure my skill folders have emoji prefixes"
```

**Script Execution:**
```bash
# Update all folders to match registry
python ../skill-folder-emoji-updater/scripts/update_folder_emojis.py --all

# Update specific category folders
python ../skill-folder-emoji-updater/scripts/update_folder_emojis.py --category debug

# Dry run to see what would change
python ../skill-folder-emoji-updater/scripts/update_folder_emojis.py --all --dry-run
```

### Natural Language Interface

**Emoji Assignment:**
- "Assign 🎨 emoji to ui-design skill"
- "Give vue-debugging the 🐛 emoji"
- "Set custom emoji for task-manager"

**Category Management:**
- "Apply bug emoji to all debug skills"
- "Use lightning bolt for create category"
- "Set default emojis for my skills"

**Conflict Resolution:**
- "Check for emoji conflicts"
- "Show me skills with duplicate emojis"
- "Fix emoji conflicts automatically"

**Folder Integration:**
- "Update skill folders with emojis"
- "Sync folder names with registry"
- "Add emoji prefixes to all skill folders"

**Discovery and Analysis:**
- "Suggest emoji for my new skill"
- "List all emoji assignments"
- "Show which skills need emojis"

### Examples

#### Example 1: Individual Skill Assignment
```
User: "Assign 🎨 emoji to ui-design skill"

System:
✅ Assigned emoji 🎨 to skill: ui-design
✅ Updated skills.json registry
✅ Updated SKILL.md frontmatter
✅ Updated display name: 🎨 UI Design

Natural Language Usage:
- "🎨 Using ui-design skill for component styling"
- "🎨 UI Design skill activated for layout fixes"
```

#### Example 2: Category Assignment
```
User: "Assign 🐛 emoji to all debug skills"

System:
⚠️ Emoji conflicts detected for 🐛:
   - component-debugger (existing)
   - vue-debugger (existing)

Continue anyway? (y/N): y

✅ Assigned emoji 🐛 to 5 skills in category 'debug'
   - api-debugger → 🐛 API Debugger
   - performance-debug → 🐛 Performance Debug
   - state-debugger → 🐛 State Debugger
   - render-debug → 🐛 Render Debug
   - memory-debug → 🐛 Memory Debug
```

#### Example 3: Folder Integration
```
User: "Update all skill folders to match their registry emojis"

System:
📋 Would rename 8 skill folders:
   🐛 vue-debugging (from: vue-debugging)
   ⚡ task-creator (from: task-creator)
   🔧 pinia-fixer (from: pinia-fixer)
   📊 analytics (from: analytics)
   ...

Apply changes? (y/N): y

✅ Updated 8 skill folders with emojis
```

### Technical Implementation

#### Registry Storage
```json
{
  "skills": {
    "vue-debugging": {
      "name": "Vue Debugging",
      "emoji": "🐛",
      "display_name": "🐛 Vue Debugging",
      "category": "debug"
    }
  }
}
```

#### Frontmatter Integration
```yaml
---
name: vue-debugging
emoji: "🐛"
description: Debug Vue.js applications
---
```

#### Validation Features
- **Emoji Validation**: Ensures only valid Unicode emojis
- **Conflict Detection**: Identifies duplicate emoji assignments
- **Category Consistency**: Maintains logical emoji-category relationships
- **Cross-Reference Sync**: Keeps registry and SKILL.md aligned

### Best Practices

#### Emoji Selection Guidelines
1. **Relevance**: Choose emojis that relate to skill purpose
2. **Category Consistency**: Use category defaults when possible
3. **Uniqueness**: Avoid duplicate emojis within the same category
4. **Clarity**: Use well-recognized emojis (🐛, ⚡, 🔧, etc.)
5. **Accessibility**: Ensure emojis render correctly across platforms

#### Assignment Workflow
1. **Check existing assignments** to avoid conflicts
2. **Consider category** defaults first
3. **Test emoji** before widespread assignment
4. **Update both registry** and frontmatter
5. **Verify skill loading** after changes

#### Maintenance Schedule
- **Monthly**: Review new skills for emoji assignment
- **Quarterly**: Check for emoji conflicts and consistency
- **After skill creation**: Assign emoji as part of creation process
- **During consolidation**: Preserve or update emojis for merged skills

### Integration with Skill Ecosystem

**Works With:**
- **skill-creator-doctor**: For emoji assignment and management
- **skill-folder-emoji-updater**: For folder name synchronization
- **skill consolidation system**: Emoji-enhanced reports and displays
- **skills.json registry**: Central storage for emoji assignments

**Enhanced Features:**
- **Visual skill identification** during activation
- **Category-based organization** through consistent emojis
- **Folder visual organization** matching registry
- **Conflict prevention** through detection and resolution

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
