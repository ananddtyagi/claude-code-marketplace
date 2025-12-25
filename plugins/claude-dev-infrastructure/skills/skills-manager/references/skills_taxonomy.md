# Skills Taxonomy Framework

Comprehensive categorization system for Claude Code skills to ensure consistent organization and analysis.

## Primary Categories

### 1. Meta Skills
**Purpose**: Skills that manage other skills or the Claude Code ecosystem itself
**Characteristics**: High-level, system-wide impact, rarely directly user-facing
**Examples**:
- `skill-creator-doctor` - Creates and manages other skills
- `skills-manager` - Audits and consolidates skills
- `mapping-manager` - Maintains skill documentation mapping

**Protection Level**: CRITICAL (Never auto-delete or modify)

### 2. Debug Skills
**Purpose**: Identify, analyze, and fix issues in code and systems
**Characteristics**: Problem-solving focused, reactive, diagnostic
**Examples**:
- `dev-debugging` - General debugging workflows
- `vue-debugging` - Vue.js specific debugging
- `dev-debug-reactivity` - Reactivity system debugging
- `canvas-debug` - Canvas interaction debugging

**Protection Level**: HIGH (Essential for development workflow)

### 3. Create Skills
**Purpose**: Generate new code, components, or functionality
**Characteristics**: Generative, constructive, creative
**Examples**:
- `dev-vue` - Vue component creation
- `component-generator` - UI component generation
- `api-generator` - API endpoint creation
- `template-creator` - Template and scaffold generation

**Protection Level**: MEDIUM (Valuable but can be consolidated)

### 4. Fix Skills
**Purpose**: Repair, maintain, or optimize existing code
**Characteristics**: Corrective, maintenance-focused, optimization
**Examples**:
- `dev-fix-timer` - Timer functionality fixes
- `pinia-fixer` - Pinia state management fixes
- `performance-optimizer` - Performance issue resolution
- `security-hardener` - Security vulnerability fixes

**Protection Level**: HIGH (Critical for code maintenance)

### 5. Test Skills
**Purpose**: Validate, verify, or test code and functionality
**Characteristics**: Validation-focused, quality assurance, testing workflows
**Examples**:
- `qa-testing` - Quality assurance testing
- `e2e-tester` - End-to-end testing
- `unit-test-generator` - Unit test creation
- `validation-tester` - Input validation testing

**Protection Level**: MEDIUM (Important for quality but can be consolidated)

### 6. Analyze Skills
**Purpose**: Analyze code, systems, or data for insights
**Characteristics**: Analytical, informative, reporting
**Examples**:
- `comprehensive-system-analyzer` - Full system analysis
- `performance-profiler` - Performance analysis
- `code-analyzer` - Code quality analysis
- `dependency-analyzer` - Dependency relationship analysis

**Protection Level**: MEDIUM (Valuable insights but can be specialized)

### 7. Optimize Skills
**Purpose**: Improve performance, efficiency, or resource usage
**Characteristics**: Performance-focused, optimization, enhancement
**Examples**:
- `dev-optimize-performance` - General performance optimization
- `memory-optimizer` - Memory usage optimization
- `bundle-optimizer` - Build bundle optimization
- `query-optimizer` - Database query optimization

**Protection Level**: MEDIUM (Important but can be merged with fix skills)

### 8. Documentation Skills
**Purpose**: Create, manage, or improve documentation
**Characteristics**: Documentation-focused, content management, communication
**Examples**:
- `smart-doc-manager` - Documentation management
- `api-docs-generator` - API documentation creation
- `readme-generator` - README file generation
- `tech-writer` - Technical writing assistance

**Protection Level**: MEDIUM (Valuable but often specialized)

### 9. Workflow Skills
**Purpose**: Automate or improve development workflows
**Characteristics**: Process automation, workflow optimization, efficiency
**Examples**:
- `git-workflow-helper` - Git workflow assistance
- `ci-cd-manager` - CI/CD pipeline management
- `deployment-automation` - Deployment workflow automation
- `release-manager` - Release process management

**Protection Level**: HIGH (Essential for development productivity)

### 10. Tools Skills
**Purpose:** Provide specific tool functionality or integrations
**Characteristics**: Tool-specific, integration-focused, utility
**Examples**:
- `storybook-manager` - Storybook management
- `docker-helper` - Docker container management
- `database-migrator` - Database migration assistance
- `package-manager` - Package dependency management

**Protection Level**: LOW (Tool-specific, can be consolidated)

## Secondary Classification Dimensions

### Technology Domain
**Frontend**: Skills related to client-side development
- Vue.js, React, Angular, Svelte
- CSS, Styling, UI/UX
- Component frameworks, State management

**Backend**: Skills related to server-side development
- Node.js, Python, Java, Go, Rust
- API development, Microservices
- Database integration

**DevOps**: Skills related to operations and deployment
- Docker, Kubernetes, CI/CD
- Infrastructure as Code
- Monitoring and logging

**Testing**: Skills related to testing and quality assurance
- Unit testing, Integration testing
- E2E testing, Performance testing
- Test automation

### Scope Level
**General**: Broad, technology-agnostic skills
- General debugging, Performance optimization
- Code analysis, Documentation
- Workflow automation

**Specific**: Technology or domain-specific skills
- Vue debugging, React components
- Python testing, Node.js optimization
- Docker containerization

### Complexity Level
**Simple**: Single-focus, straightforward operations
- Basic debugging, Simple fixes
- Template generation, Basic documentation

**Complex**: Multi-step, intricate workflows
- System analysis, Performance optimization
- Complex debugging, Advanced automation

**Advanced**: Expert-level, specialized knowledge
- Security hardening, Advanced optimization
- Complex system architecture, Specialized tooling

## Skill Relationship Patterns

### Hierarchical Relationships
- **Parent Skills**: Broad capabilities that encompass more specific skills
- **Child Skills**: Specialized implementations of parent capabilities

### Complementary Relationships
- **Sequencing**: Skills that work well in sequence (debug → fix → test)
- **Parallel**: Skills that can be used together for comprehensive coverage

### Overlapping Relationships
- **Functional Overlap**: Skills with similar capabilities but different approaches
- **Domain Overlap**: Skills that work in the same technology domain
- **Scope Overlap**: Skills with overlapping problem spaces

## Classification Algorithm

### Automatic Categorization
```python
def categorize_skill(skill_metadata):
    """Automatically categorize a skill based on metadata"""

    # Extract keywords from name, description, capabilities
    keywords = extract_keywords(skill_metadata)

    # Category scoring based on keyword matches
    category_scores = {}
    for category, category_keywords in CATEGORY_KEYWORDS.items():
        score = len(set(keywords) & set(category_keywords))
        category_scores[category] = score

    # Technology domain classification
    tech_domain = classify_technology_domain(keywords)

    # Complexity assessment
    complexity = assess_complexity(skill_metadata, keywords)

    # Scope determination
    scope = determine_scope(keywords, skill_metadata)

    return SkillCategory(
        primary=primary_category,
        domain=tech_domain,
        complexity=complexity,
        scope=scope,
        confidence=calculate_confidence(category_scores)
    )
```

### Keyword Mapping
```python
CATEGORY_KEYWORDS = {
    'debug': ['debug', 'fix', 'error', 'issue', 'problem', 'troubleshoot', 'diagnose'],
    'create': ['create', 'build', 'generate', 'make', 'develop', 'implement', 'scaffold'],
    'fix': ['fix', 'repair', 'patch', 'resolve', 'correct', 'optimize', 'improve'],
    'test': ['test', 'testing', 'validate', 'verify', 'check', 'assert', 'quality'],
    'analyze': ['analyze', 'analysis', 'audit', 'review', 'inspect', 'examine', 'report'],
    'optimize': ['optimize', 'performance', 'speed', 'efficiency', 'improve', 'enhance'],
    'documentation': ['documentation', 'docs', 'readme', 'guide', 'manual', 'reference'],
    'workflow': ['workflow', 'automation', 'process', 'pipeline', 'cicd', 'deploy'],
    'meta': ['skill', 'claude', 'code', 'management', 'orchestration']
}
```

## Usage Guidelines

### For Skill Creation
1. **Choose Primary Category**: Select the most appropriate primary category
2. **Identify Technology Domain**: Specify the relevant technology stack
3. **Assess Complexity**: Determine the skill's complexity level
4. **Define Scope**: Clarify if the skill is general or specific
5. **Set Protection Level**: Based on importance and uniqueness

### For Skill Analysis
1. **Apply Consistent Taxonomy**: Use the same classification criteria for all skills
2. **Identify Relationships**: Map out how skills relate to each other
3. **Detect Overlaps**: Find skills with similar capabilities
4. **Assess Necessity**: Evaluate skills based on usage and relevance
5. **Plan Consolidation**: Group related skills for potential merging

### For Skill Management
1. **Maintain Balance**: Ensure good coverage across all categories
2. **Protect Critical Skills**: Safeguard essential meta and debug skills
3. **Consolidate Overlap**: Merge skills with high capability overlap
4. **Archive Unused**: Move low-value, unused skills to archive
5. **Optimize Organization**: Maintain clear, logical skill structure

## Evolution and Adaptation

The taxonomy should evolve as:
- New technologies emerge
- Development practices change
- User needs evolve
- Skill capabilities expand

Regular taxonomy reviews ensure:
- Relevance to current development practices
- Adequate coverage of new technologies
- Consistent classification standards
- Optimal skill organization

This framework provides the foundation for intelligent skill management, ensuring your Claude Code skills remain organized, relevant, and efficient over time.