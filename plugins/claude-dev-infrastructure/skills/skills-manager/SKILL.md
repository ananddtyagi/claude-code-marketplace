---
name: skills-manager
description: Universal consolidation & audit skill for Claude Code skills. Analyzes project state, detects redundancies, and safely manages skills with backup, confirmations, and rollback capabilities. Never assumes without verifying actual code and usage patterns.
---

# Skills Manager Skill - Universal Consolidation & Audit for Claude Code

**A meta-skill to audit, consolidate, archive, or remove Claude Code skills by referencing actual project state, structure, and usage needs. Safeguards the integrity of your skillset with verification-first approach.**

## Core Safety Principle

**NEVER ASSUME - ALWAYS VERIFY**

This skill MUST analyze your actual project state, codebase, and usage patterns before making any decisions about skills. It verifies system reality, validates usage data, and applies conservative safety thresholds before suggesting any changes.

---

## When to Use This Skill

Use this skill when you need to:

- **Audit skills effectiveness** - Analyze which skills are actually used vs unused
- **Consolidate redundant skills** - Merge overlapping or duplicate capabilities
- **Archive obsolete skills** - Safely move outdated skills to archive with rollback
- **Optimize skill organization** - Restructure skills based on project needs and relevance
- **Maintain skill hygiene** - Regular cleanup to keep skillset efficient and relevant

**Critical:** This skill prioritizes safety over automation. All destructive actions require explicit user confirmation and have rollback capabilities.

---

## Activation Commands

### Commands
```bash
/skills-audit                    # Run full analysis, generate reports, no changes
/skills-consolidate             # Execute consolidation after user review and approval
/skills-merge <skill1> <skill2>  # Interactive merge assistance for two skills
/skills-archive <skill-name>    # Safely archive a skill with backup
/skills-config                  # View or update configuration settings
```

### Triggers
Natural language patterns that activate this skill:

- "Audit my Claude Code skills"
- "Find redundant or unused skills"
- "Consolidate my skills collection"
- "Clean up my skills directory"
- "Archive old skills I don't use"
- "Optimize my skill organization"
- "Which skills should I keep or remove?"

---

## Phase 1: System State & Skills Inventory (MANDATORY First Step)

### 1.1 Detect Project Type & Tech Stack

**Objective:** Build accurate understanding of your actual project.

**Process:**

#### Parse Dependency Files
```bash
# Find all dependency files
find . -name "package.json" -o -name "requirements.txt" -o -name "pom.xml" \
  -o -name "go.mod" -o -name "Cargo.toml" -o -name "composer.json" \
  -o -name "Gemfile" -o -name "build.gradle"

# Extract technologies
if [ -f "package.json" ]; then
  echo "Node.js project detected"
  cat package.json | jq -r '.dependencies, .devDependencies | keys[]' | head -20
fi

if [ -f "requirements.txt" ]; then
  echo "Python project detected"
  grep -v "^#" requirements.txt | cut -d'=' -f1 | head -20
fi
```

#### Map Project Structure
```bash
# Analyze directory structure
echo "=== Project Structure Analysis ==="
for dir in src lib app components services docs k8s docker; do
  if [ -d "$dir" ]; then
    file_count=$(find "$dir" -type f | wc -l)
    echo "$dir/ - $file_count files"
  fi
done

# Identify key file types
echo "=== File Type Distribution ==="
find . -type f -name "*.ts" -o -name "*.js" -o -name "*.py" -o -name "*.go" -o -name "*.rs" | \
  cut -d'.' -f3 | sort | uniq -c | sort -nr
```

**Output Format:**
```json
{
  "system_reality": {
    "project_type": "Vue.js TypeScript Application",
    "primary_technologies": ["Vue 3", "TypeScript", "Vite", "Pinia"],
    "databases": ["IndexedDB", "LocalStorage"],
    "frameworks": ["Vue.js", "Tailwind CSS"],
    "build_tools": ["Vite", "ESLint", "TypeScript"],
    "directory_structure": {
      "src/": "234 files",
      "components/": "45 files",
      "docs/": "12 files"
    }
  },
  "relevance_domains": ["frontend", "vue.js", "typescript", "pinia", "productivity"]
}
```

### 1.2 Inventory All Current Skills

**Objective:** Complete catalog of all skills with metadata.

**Process:**

```bash
# Scan skills directory
echo "=== Skills Inventory ==="
for skill in .claude/skills/*.md; do
  if [ -f "$skill" ]; then
    skill_name=$(basename "$skill" .md)
    skill_size=$(wc -l < "$skill")
    last_modified=$(git log -1 --format="%ci" "$skill" 2>/dev/null || echo "unknown")
    echo "✅ $skill_name - $skill_size lines - last: $last_modified"
  fi
done
```

**Extract Metadata from Each Skill:**
```python
def extract_skill_metadata(skill_file):
    """Extract key metadata from skill markdown file"""
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract YAML frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if frontmatter_match:
        try:
            import yaml
            metadata = yaml.safe_load(frontmatter_match.group(1))
        except:
            metadata = {}
    else:
        metadata = {}

    # Extract capabilities from content
    capabilities = []
    if 'Capabilities:' in content:
        cap_section = re.search(r'Capabilities:(.*?)(?:\n##|\Z)', content, re.DOTALL)
        if cap_section:
            capabilities = re.findall(r'[-*]\s*(.+)', cap_section.group(1))

    # Extract activation triggers
    triggers = []
    if 'triggers' in metadata:
        if isinstance(metadata['triggers'], list):
            triggers = metadata['triggers']
        elif isinstance(metadata['triggers'], str):
            triggers = [metadata['triggers']]

    return {
        'name': metadata.get('name', skill_file.stem),
        'description': metadata.get('description', ''),
        'category': metadata.get('category', 'general'),
        'triggers': triggers,
        'capabilities': capabilities,
        'file_size': len(content),
        'last_modified': get_git_last_modified(skill_file)
    }
```

### 1.3 Analyze Usage Patterns

**Objective:** Understand which skills are actually being used.

**Process:**

#### Analyze Git History for Skill References
```bash
# Search git history for skill mentions
echo "=== Skill Usage Analysis (Last 90 Days) ==="
since_date=$(date -d "90 days ago" --iso-8601)

for skill in .claude/skills/*.md; do
  skill_name=$(basename "$skill" .md)

  # Count commits mentioning this skill
  commit_count=$(git log --since="$since_date" --grep="$skill_name" --oneline | wc -l)

  # Count file mentions in commit messages
  message_count=$(git log --since="$since_date" --all --grep="$skill_name" --oneline | wc -l)

  total_usage=$((commit_count + message_count))

  if [ $total_usage -gt 0 ]; then
    echo "📊 $skill_name - $total_usage uses in last 90 days"
  else
    echo "⚠️  $skill_name - No recent usage detected"
  fi
done
```

#### Analyze Skill Dependencies
```python
def analyze_skill_dependencies(skills_dir):
    """Analyze how skills reference each other"""
    dependencies = {}

    for skill_file in Path(skills_dir).glob("*.md"):
        skill_name = skill_file.stem
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find references to other skills
        skill_references = re.findall(r'\b([a-z][a-z0-9-]*)\b', content.lower())

        # Filter to actual skill names
        other_skills = [f.stem for f in Path(skills_dir).glob("*.md") if f.stem != skill_name]
        referenced_skills = [ref for ref in skill_references if ref in other_skills]

        if referenced_skills:
            dependencies[skill_name] = referenced_skills

    return dependencies
```

**Output Format:**
```json
{
  "skills_inventory": {
    "total_skills": 47,
    "categories": {
      "debug": 12,
      "create": 8,
      "fix": 15,
      "optimize": 5,
      "meta": 7
    },
    "usage_stats": {
      "vue-debugging": {"uses_90_days": 23, "last_used": "2025-11-20"},
      "pinia-fixer": {"uses_90_days": 15, "last_used": "2025-11-18"},
      "old-deprecated-skill": {"uses_90_days": 0, "last_used": "2024-06-01"}
    },
    "dependencies": {
      "vue-debugging": ["dev-vue"],
      "comprehensive-system-analyzer": ["qa-testing", "dev-debugging"]
    }
  }
}
```

---

## Phase 2: Skills Necessity & Redundancy Assessment

### 2.1 Necessity Scoring

**Objective:** Rank skills by importance and relevance to current project.

**Scoring Algorithm:**

```python
def calculate_necessity_score(skill_data, project_reality, usage_stats):
    """Calculate necessity score for a skill (0-100)"""

    score = 0

    # Base score from recent usage (40 points max)
    usage = usage_stats.get(skill_data['name'], {})
    recent_uses = usage.get('uses_90_days', 0)
    usage_score = min(recent_uses * 2, 40)  # 2 points per use, max 40
    score += usage_score

    # Project relevance score (30 points max)
    skill_domains = extract_domains(skill_data['description'], skill_data['capabilities'])
    project_domains = project_reality.get('relevance_domains', [])

    domain_overlap = len(set(skill_domains) & set(project_domains))
    relevance_score = min(domain_overlap * 10, 30)  # 10 points per matching domain
    score += relevance_score

    # Category importance score (20 points max)
    important_categories = ['debug', 'create', 'fix']
    if skill_data['category'] in important_categories:
        score += 20
    elif skill_data['category'] in ['optimize', 'analyze']:
        score += 15
    else:
        score += 10

    # Dependency score (10 points max)
    if skill_data['name'] in usage_stats.get('dependencies', {}):
        dependent_count = len(usage_stats['dependencies'][skill_data['name']])
        dependency_score = min(dependent_count * 2, 10)
        score += dependency_score

    return min(score, 100)
```

### 2.2 Redundancy Detection

**Objective:** Find overlapping or duplicate skills.

**Analysis Methods:**

#### Capability Overlap Analysis
```python
def analyze_capability_overlap(skill1_data, skill2_data):
    """Calculate overlap between two skills based on capabilities and triggers"""

    # Extract keywords from descriptions and capabilities
    def extract_keywords(text):
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        stop_words = {'the', 'and', 'for', 'with', 'can', 'will', 'use', 'from', 'have', 'this', 'that'}
        return [w for w in words if w not in stop_words]

    # Combine text sources
    skill1_text = f"{skill1_data['description']} {' '.join(skill1_data['capabilities'])} {' '.join(skill1_data['triggers'])}"
    skill2_text = f"{skill2_data['description']} {' '.join(skill2_data['capabilities'])} {' '.join(skill2_data['triggers'])}"

    # Extract keywords
    skill1_keywords = set(extract_keywords(skill1_text))
    skill2_keywords = set(extract_keywords(skill2_text))

    # Calculate Jaccard similarity
    if not skill1_keywords and not skill2_keywords:
        return 0.0

    intersection = len(skill1_keywords & skill2_keywords)
    union = len(skill1_keywords | skill2_keywords)

    return intersection / union if union > 0 else 0.0
```

#### Trigger Conflict Analysis
```python
def analyze_trigger_conflicts(all_skills):
    """Find skills with overlapping activation triggers"""

    trigger_map = defaultdict(list)

    for skill_name, skill_data in all_skills.items():
        for trigger in skill_data['triggers']:
            # Normalize trigger text
            normalized_trigger = trigger.lower().strip()
            trigger_map[normalized_trigger].append(skill_name)

    conflicts = []
    for trigger, skills in trigger_map.items():
        if len(skills) > 1:
            conflicts.append({
                'trigger': trigger,
                'conflicting_skills': skills,
                'conflict_type': 'exact_match'
            })

    return conflicts
```

**Output Format:**
```json
{
  "necessity_scores": {
    "vue-debugging": 85,
    "pinia-fixer": 72,
    "comprehensive-system-analyzer": 68,
    "old-unused-skill": 15
  },
  "redundancy_analysis": {
    "overlapping_skills": [
      {
        "skill1": "component-debugger",
        "skill2": "vue-component-debugger",
        "similarity": 0.87,
        "shared_capabilities": ["debug Vue components", "fix reactivity issues"],
        "recommendation": "Consider merging"
      }
    ],
    "trigger_conflicts": [
      {
        "trigger": "fix vue component",
        "conflicting_skills": ["vue-debugger", "component-debugger", "reactivity-fixer"],
        "recommendation": "Refine trigger specificity"
      }
    ]
  },
  "consolidation_candidates": {
    "merge_candidates": [
      {
        "primary_skill": "vue-debugging",
        "merge_with": ["component-debugger", "reactivity-fixer"],
        "confidence": 0.92,
        "risk": "low"
      }
    ],
    "archive_candidates": [
      {
        "skill": "old-deprecated-skill",
        "reason": "No usage in 180+ days, obsolete capabilities",
        "confidence": 0.98,
        "risk": "low"
      }
    ]
  }
}
```

---

## Phase 3: Consolidation Planning & User Review

### 3.1 Consolidation Rules Engine

**Merge Rules:**
- High similarity (≥85%) + low usage overlap → Candidate for merge
- Complementary capabilities (≤70% similarity) → Keep separate
- One skill significantly more used → Keep active, merge other into it

**Archive Rules:**
- No usage in 180+ days → Archive candidate
- Obsolete technology references → Archive candidate
- Superseded by newer skill → Archive older version

**Deletion Rules:**
- Exact duplicate (100% similarity) → Delete after merge
- Broken/unloadable skill → Delete with backup
- User explicitly marked as obsolete → Delete with confirmation

### 3.2 Generate Consolidation Plan

**Plan Structure:**
```markdown
# Skills Consolidation Plan
**Generated:** 2025-11-23 15:30 IST
**Conservatism Level:** balanced
**Total Skills Analyzed:** 47

---

## Executive Summary

- **High Priority Actions:** 5 skills (3 merges, 2 archives)
- **Medium Priority Actions:** 8 skills (4 merges, 4 archives)
- **Low Priority Actions:** 3 skills (review needed)
- **Protected Skills:** 12 (will not be modified)

**Estimated Impact:** Reduce skills from 47 to 32 (32% reduction)

---

## High Priority Actions

### 1. Merge Vue Debugging Skills
**Action:** Merge `component-debugger` + `reactivity-fixer` → `vue-debugging`

**Rationale:**
- 92% capability overlap
- `vue-debugging` has 3x more usage
- All triggers can be consolidated
- Low risk (complementary, not conflicting)

**Risk Assessment:** LOW
- Backup will be created
- All functionality preserved
- Rollback available via git revert

**User Confirmation Required:** ⚠️ YES

### 2. Archive Obsolete Skills
**Action:** Archive `old-webpack-configurator`

**Rationale:**
- No usage in 210+ days
- References obsolete webpack v3
- Modern skills cover same functionality better

**Risk Assessment:** LOW
- Moved to `skills-archive/` directory
- Preserved in git history
- Can be restored if needed

**User Confirmation Required:** ⚠️ YES

---

## Protected Skills (Will NOT be modified)

- `skill-creator-doctor` - Meta skill, critical for system
- `dev-debugging` - Core debugging functionality
- `basic-coding` - Fundamental capability
- `git-workflow-helper` - Essential for development workflow

---

## Execution Plan

1. **Pre-execution Backup**: Create `.claude/skills-backup-YYYYMMDD/`
2. **Create Branch**: `skills/consolidation-YYYYMMDD`
3. **Batch 1**: Archive obsolete skills (low risk)
4. **Batch 2**: Merge overlapping skills (medium risk)
5. **Batch 3**: Update references and triggers
6. **Validation**: Test all skill activations
7. **Cleanup**: Remove placeholder files

**Rollback Instructions:**
```bash
# Complete rollback
git checkout main
git branch -D skills/consolidation-YYYYMMDD
cp -r .claude/skills-backup-YYYYMMDD/* .claude/skills/

# Partial rollback (batch-specific)
git revert <commit-hash>
```
```

### 3.3 User Confirmation Process

**Interactive Confirmation Flow:**

```python
def get_user_confirmation(action_details):
    """Get explicit user confirmation for each action"""

    print(f"\n=== Action Review ===")
    print(f"Type: {action_details['type']}")
    print(f"Skills: {action_details['skills']}")
    print(f"Risk Level: {action_details['risk'].upper()}")
    print(f"Rationale: {action_details['rationale']}")

    if action_details['risk'] == 'high':
        print(f"\n⚠️  HIGH RISK ACTION")
        print(f"This action {action_details['warning']}")

        response = input(f"\nProceed with {action_details['type']}? (Type 'YES' to confirm): ")
        return response == 'YES'

    else:
        print(f"\nRisk: {action_details['risk']}")
        response = input(f"Proceed with {action_details['type']}? (y/n): ")
        return response.lower() in ['y', 'yes']
```

---

## Phase 4: Safe Execution Workflow

### 4.1 Pre-Execution Validation

**Safety Checklist:**
```bash
echo "=== Pre-Execution Safety Checklist ==="

# Check git status
if [ -n "$(git status --porcelain)" ]; then
  echo "❌ Working directory not clean. Please commit or stash changes."
  exit 1
fi

# Create backup
BACKUP_DIR=".claude/skills-backup-$(date +%Y%m%d-%H%M%S)"
if [ ! -d "$BACKUP_DIR" ]; then
  echo "📦 Creating backup..."
  cp -r .claude/skills "$BACKUP_DIR/"
  echo "✅ Backup created: $BACKUP_DIR"
fi

# Create working branch
BRANCH="skills/consolidation-$(date +%Y%m%d-%H%M%S)"
git checkout -b "$BRANCH"
echo "✅ Working on branch: $BRANCH"

# Validate skills can still load
echo "🔍 Validating current skill integrity..."
# Add skill loading validation here
```

### 4.2 Stepwise Execution

#### Batch 1: Archive Operations (Low Risk)
```bash
echo "=== Batch 1: Archiving Obsolete Skills ==="

for skill in "${ARCHIVE_CANDIDATES[@]}"; do
  echo "Archiving: $skill"

  # Create archive directory if needed
  mkdir -p .claude/skills-archive

  # Move skill with git history
  git mv ".claude/skills/$skill.md" ".claude/skills-archive/$skill.md"

  # Create ARCHIVED.md note
  cat > ".claude/skills-archive/$skill.md" << EOF
# Archived: $skill

**Archive Date:** $(date -Iseconds)
**Reason:** ${ARCHIVE_REASONS[$skill]}

## Archive Reason
${ARCHIVE_DETAILS[$skill]}

## Restoration Instructions
To restore this skill:
1. Move from skills-archive/ back to skills/
2. Update .claude/config/skills.json if needed
3. Test skill loading
EOF

  echo "✅ Archived: $skill"
done

git commit -m "skills: archive obsolete skills

- Archived ${#ARCHIVE_CANDIDATES[@]} obsolete skills
- Moved to skills-archive/ directory
- Preserved git history and metadata

Skills archived:
$(printf '  - %s\n' "${ARCHIVE_CANDIDATES[@]}")
"
```

#### Batch 2: Merge Operations (Medium Risk)
```bash
echo "=== Batch 2: Merging Overlapping Skills ==="

for merge_group in "${MERGE_CANDIDATES[@]}"; do
  IFS='|' read -r primary_skill merge_skills <<< "$merge_group"

  echo "Merging into: $primary_skill"
  echo "From: $merge_skills"

  # Get user confirmation for this merge
  echo "About to merge skills into $primary_skill"
  echo "This will combine capabilities and update triggers"

  read -p "Proceed with merge? (y/n): " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Perform merge operation
    python3 .claude/skills/skills-manager/scripts/merge_skills.py \
      --primary "$primary_skill" \
      --secondary $merge_skills

    # Remove merged skills
    for skill in $merge_skills; do
      git mv ".claude/skills/$skill.md" ".claude/skills-archive/merged-$skill.md"
    done

    echo "✅ Merge completed: $primary_skill"
  else
    echo "⏭️  Skipping merge: $primary_skill"
  fi
done

git commit -m "skills: merge overlapping skills

Consolidated skills with high capability overlap:
- Combined complementary capabilities
- Updated triggers to prevent conflicts
- Preserved all unique functionality
- Archived merged originals for reference"
```

### 4.3 Post-Execution Validation

```bash
echo "=== Post-Execution Validation ==="

# Validate all skills can load
echo "🔍 Testing skill loading..."
load_errors=0
for skill in .claude/skills/*.md; do
  if [ -f "$skill" ]; then
    # Test skill syntax/loading
    if ! python3 -c "
import yaml
import re
with open('$skill', 'r') as f:
    content = f.read()
# Basic validation
frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
if not frontmatter_match:
    exit(1)
" 2>/dev/null; then
      echo "❌ Skill validation failed: $(basename "$skill")"
      load_errors=$((load_errors + 1))
    fi
  fi
done

if [ $load_errors -eq 0 ]; then
  echo "✅ All skills validated successfully"
else
  echo "❌ $load_errors skills have validation errors"
  echo "Please review and fix before continuing"
fi

# Test registry consistency
echo "🔍 Validating registry consistency..."
python3 .claude/skills/skills-manager/scripts/validate_registry.py

echo "=== Consolidation Complete ==="
echo "Branch: $BRANCH"
echo "Backup: $BACKUP_DIR"
echo ""
echo "Next steps:"
echo "1. Review changes: git log --oneline -10"
echo "2. Test skill functionality"
echo "3. Create PR: gh pr create --fill"
echo "4. Merge after approval"
echo ""
echo "Rollback if needed:"
echo "  git checkout main && git branch -D $BRANCH"
echo "  cp -r $BACKUP_DIR/* .claude/skills/"
```

---

## Safety & Rollback Features

### 5.1 Backup Strategy

**Automatic Backups:**
```bash
# Pre-execution backup
BACKUP_DIR=".claude/skills-backup-$(date +%Y%m%d-%H%M%S)"
cp -r .claude/skills "$BACKUP_DIR/"

# Git stash backup
git stash push -u -m "Pre-consolidation skills state"

# Registry backup
cp .claude/config/skills.json "$BACKUP_DIR/skills-backup.json"
```

### 5.2 Rollback Procedures

**Complete Rollback:**
```bash
# Method 1: Git branch deletion
git checkout main
git branch -D skills/consolidation-YYYYMMDD

# Method 2: Restore from backup
rm -rf .claude/skills
cp -r .claude/skills-backup-YYYYMMDD/skills .claude/skills/
git add .claude/skills/
git commit -m "Rollback: restore skills from backup"
```

**Selective Rollback:**
```bash
# Rollback specific commits
git revert <commit-hash>

# Restore specific skills from backup
cp .claude/skills-backup-YYYYMMDD/skills/specific-skill.md .claude/skills/
```

### 5.3 Risk Mitigation

**Risk Levels:**
- **LOW**: Archive operations (preserves data, reversible)
- **MEDIUM**: Merge operations (requires careful validation)
- **HIGH**: Delete operations (requires explicit "YES" confirmation)

**Protected Categories:**
- Meta skills (skill-creator-doctor, skills-manager)
- Core debugging skills (dev-debugging, dev-fix-timer)
- Fundamental workflow skills (git-workflow-helper, basic-coding)

---

## Configuration

### Configuration File
```yaml
# .claude/skills-manager-config.yml
conservatism_level: balanced  # Options: aggressive, balanced, conservative

protected_skills:
  - skill-creator-doctor
  - skills-manager
  - dev-debugging
  - basic-coding
  - git-workflow-helper
  - file-operations

risk_settings:
  max_deletion_risk: medium    # disallow high-risk deletion without manual confirmation
  merge_threshold: 0.7         # 70% overlap required for merge suggestion
  archive_instead_of_delete: true
  require_confirmation_for:
    - delete
    - merge
    - modify_protected

usage_analysis:
  usage_window_days: 90        # Analyze skill activations from last 90 days
  inactive_threshold: 180      # Days without usage before considering archive
  high_usage_threshold: 20     # Uses per 90 days = high usage

redundancy_detection:
  capability_similarity_threshold: 0.8
  trigger_conflict_detection: true
  semantic_analysis_enabled: true

output:
  generate_reports: true
  create_backup: true
  verbose_logging: false
```

### Runtime Configuration Updates
```bash
# Update conservatism level
/skills-config --conservatism conservative

# Add protected skill
/skills-config --protect new-important-skill

# Adjust thresholds
/skills-config --merge-threshold 0.85
```

---

## Usage Examples

### Example 1: Full Skills Audit
```
User: "/skills-audit"

System Response:
🔍 Running comprehensive skills audit...

=== System Analysis ===
Project: Vue.js TypeScript Application
Key Technologies: Vue 3, TypeScript, Pinia, Tailwind CSS
Relevance Domains: frontend, vue.js, typescript, productivity

=== Skills Inventory ===
Total Skills: 47
Categories: debug(12), create(8), fix(15), optimize(5), meta(7)

=== Usage Analysis ===
High Usage (20+): vue-debugging(23), dev-fix-timer(18)
Medium Usage (5-19): pinia-fixer(15), component-debugger(12)
Low Usage (1-4): old-webpack-configurator(1)
No Usage: legacy-skill(0), obsolete-helper(0)

=== Recommendations ===
5 skills ready for consolidation
3 skills candidates for archival
2 potential trigger conflicts identified

Generated detailed report: .claude/skills-audit-report-20251123.md
```

### Example 2: Safe Consolidation
```
User: "/skills-consolidate"

System Response:
📋 Skills Consolidation Plan Generated

=== Executive Summary ===
- Current skills: 47 → Proposed: 32 (32% reduction)
- High priority actions: 5 (3 merges, 2 archives)
- Risk level: Medium (with backups available)

=== Proposed Actions ===

1. MERGE: component-debugger + vue-component-debugger → vue-debugging
   Similarity: 92% | Usage: vue-debugging 3x higher | Risk: LOW
   Rationale: High capability overlap, vue-debugging more actively used

2. ARCHIVE: old-webpack-configurator
   Last used: 210+ days ago | Obsolete webpack v3 references | Risk: LOW
   Rationale: No recent usage, superseded by modern tools

=== Protected Skills (Will NOT be modified) ===
- skill-creator-doctor (meta-skill)
- dev-debugging (core functionality)
- basic-coding (fundamental capability)

=== Safety Measures ===
✅ Backup will be created: .claude/skills-backup-20251123/
✅ Working branch: skills/consolidation-20251123
✅ Rollback available via git revert or backup restore

Proceed with consolidation? (y/n/view details):
```

### Example 3: Selective Skill Merge
```
User: "/skills-merge react-component-builder ui-generator"

System Response:
🔍 Analyzing skills for merge...

=== Skill Analysis ===
react-component-builder:
- Capabilities: Build React components, TypeScript support
- Usage: 8 times in last 90 days
- Last used: 2025-11-15

ui-generator:
- Capabilities: Generate UI components, styling options
- Usage: 5 times in last 90 days
- Last used: 2025-11-10

=== Similarity Analysis ===
Capability Overlap: 76%
Shared Features: Component generation, TypeScript support
Unique Features:
  - react-component-builder: React-specific hooks
  - ui-generator: Multiple styling frameworks

=== Merge Recommendation ===
Confidence: 82% | Risk: MEDIUM
Proposed Name: component-generator
Strategy: Combine capabilities with React-specific options

Proceed with merge? (y/n/customize):
```

---

## Resources

### scripts/
Automation tools for skills management:

- **analyze_skills.py** - Complete skills analysis and inventory
- **detect_redundancies.py** - Find overlapping and duplicate skills
- **merge_skills.py** - Safe skill merging with conflict resolution
- **archive_skills.py** - Automated archival with metadata preservation
- **validate_registry.py** - Ensure skills.json consistency
- **backup_manager.py** - Create and manage skill backups

### references/
Detailed guides and reference materials:

- **skills_taxonomy.md** - Comprehensive skill categorization framework
- **merge_best_practices.md** - Guidelines for combining skills effectively
- **rollback_procedures.md** - Emergency recovery and rollback instructions
- **usage_analytics.md** - Methods for tracking skill utilization

These resources provide the technical implementation details for the workflows described above, enabling systematic and safe skills management with full audit trails and recovery capabilities.

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
