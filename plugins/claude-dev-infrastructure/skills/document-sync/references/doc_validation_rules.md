# Documentation Validation Rules

This reference document defines the rules and criteria used by the Document Sync skill to validate documentation against the actual codebase.

## Validation Categories

### 1. API Endpoint Validation

#### High Severity Issues
**Missing API Endpoints:**
- **Rule**: Documentation mentions API endpoints that don't exist in code
- **Detection**: Compare documented endpoints with detected route definitions
- **Evidence**: System scan of route files, Express/Flask route patterns
- **Impact**: Developer confusion, failed API calls
- **Priority**: High

**Incorrect HTTP Methods:**
- **Rule**: Documented HTTP method doesn't match implementation
- **Detection**: Verify method (GET/POST/PUT/DELETE) against route definition
- **Evidence**: Route handler analysis
- **Impact**: API method not allowed errors
- **Priority**: High

#### Medium Severity Issues
**Missing Response Examples:**
- **Rule**: API documentation lacks response examples
- **Detection**: Check for code blocks showing response format
- **Evidence**: Absence of JSON/JSON response examples
- **Impact**: Integration difficulties
- **Priority**: Medium

**Missing Request Parameters:**
- **Rule**: API endpoints documented without parameter details
- **Detection**: Check for parameter documentation
- **Evidence**: Missing parameter tables or descriptions
- **Impact**: API usage errors
- **Priority**: Medium

### 2. Framework and Technology Validation

#### Medium Severity Issues
**Framework Mismatch:**
- **Rule**: Documentation claims framework usage not detected in code
- **Detection**: Compare documented frameworks with package.json imports
- **Evidence**: Package analysis, import statements
- **Impact**: Incorrect setup expectations
- **Priority**: Medium

**Version Inconsistencies:**
- **Rule**: Documented framework versions don't match installed versions
- **Detection**: Compare version numbers in docs vs package files
- **Evidence**: Version string analysis
- **Impact**: Compatibility issues
- **Priority**: Medium

#### Low Severity Issues
**Deprecated Technology References:**
- **Rule**: Documentation mentions deprecated or outdated technologies
- **Detection**: Check for known deprecated frameworks/libraries
- **Evidence**: Technology deprecation databases
- **Impact**: Security risks, maintenance burden
- **Priority**: Low

### 3. File Reference Validation

#### High Severity Issues
**Broken File Links:**
- **Rule**: Documentation references files that don't exist
- **Detection**: Verify file paths exist in project structure
- **Evidence**: File system checks
- **Impact**: Documentation frustration
- **Priority**: High

**Incorrect Import Paths:**
- **Rule**: Code examples use incorrect import paths
- **Detection**: Check if import paths resolve to actual files
- **Evidence**: Path resolution analysis
- **Impact**: Import errors in tutorials
- **Priority**: High

#### Medium Severity Issues
**Outdated File Structure:**
- **Rule**: Documentation shows project structure that has changed
- **Detection**: Compare documented directory structure with actual
- **Evidence**: Directory tree analysis
- **Impact**: Developer navigation confusion
- **Priority**: Medium

### 4. Configuration Validation

#### Medium Severity Issues
**Missing Environment Variables:**
- **Rule**: Documentation doesn't list required environment variables
- **Detection**: Scan code for `process.env` or equivalent patterns
- **Evidence**: Environment variable usage analysis
- **Impact**: Configuration errors
- **Priority**: Medium

**Incorrect Configuration Values:**
- **Rule**: Documentation shows wrong default values or ranges
- **Detection**: Compare with config files or source code defaults
- **Evidence**: Configuration file analysis
- **Impact**: Misconfigured applications
- **Priority**: Medium

#### Low Severity Issues
**Configuration File Location:**
- **Rule**: Documentation points to wrong configuration file locations
- **Detection**: Verify config file paths exist
- **Evidence**: File system checks
- **Impact**: Setup frustration
- **Priority**: Low

### 5. Code Example Validation

#### High Severity Issues
**Syntax Errors:**
- **Rule**: Code examples contain syntax errors
- **Detection**: Parse code examples for syntax validity
- **Evidence**: Syntax parsing, linting tools
- **Impact**: Copy-paste errors
- **Priority**: High

**Runtime Errors:**
- **Rule**: Code examples fail when executed
- **Detection**: Execute code examples in sandbox when possible
- **Evidence**: Execution results, error messages
- **Impact**: Non-functional examples
- **Priority**: High

#### Medium Severity Issues
**Outdated API Usage:**
- **Rule**: Code examples use deprecated API methods
- **Detection**: Check API methods against current version
- **Evidence**: API deprecation analysis
- **Impact**: Broken code after updates
- **Priority**: Medium

**Missing Dependencies:**
- **Rule**: Code examples require unmentioned dependencies
- **Detection**: Analyze imports and compare with documented requirements
- **Evidence**: Import analysis vs documented dependencies
- **Impact**: Import errors
- **Priority**: Medium

#### Low Severity Issues
**Poor Code Style:**
- **Rule**: Code examples don't follow project style guidelines
- **Detection**: Check against linting rules
- **Evidence**: Linter output
- **Impact**: Inconsistent code style
- **Priority**: Low

### 6. Feature Completeness Validation

#### Medium Severity Issues
**Undocumented Features:**
- **Rule**: Codebase has features not mentioned in documentation
- **Detection**: Compare detected features with documented ones
- **Evidence**: Feature extraction analysis
- **Impact**: Hidden functionality
- **Priority**: Medium

**Over-Documented Features:**
- **Rule**: Documentation mentions removed or non-existent features
- **Detection**: Verify documented features exist in codebase
- **Evidence**: Code search for feature implementations
- **Impact**: User confusion
- **Priority**: Medium

#### Low Severity Issues
**Missing Feature Details:**
- **Rule**: Features mentioned but poorly explained
- **Detection**: Analyze documentation depth for documented features
- **Evidence**: Documentation length and detail analysis
- **Impact**: Underutilized features
- **Priority**: Low

## Trust Score Calculation

### Scoring Algorithm
The trust score is calculated using a weighted average of validation results:

```
Trust Score = (API_Weight × API_Score +
              Tech_Weight × Tech_Score +
              File_Weight × File_Score +
              Config_Weight × Config_Score +
              Code_Weight × Code_Score +
              Feature_Weight × Feature_Score)
```

### Weight Distribution
- **API Validation**: 30% (critical functionality)
- **Code Examples**: 25% (practical usage)
- **File References**: 20% (navigation)
- **Configuration**: 10% (setup)
- **Technology Claims**: 10% (context)
- **Feature Completeness**: 5% (comprehensiveness)

### Score Categories
- **80-100%**: High Trust - Documentation is reliable
- **60-79%**: Medium Trust - Documentation mostly reliable with some issues
- **40-59%**: Low Trust - Documentation needs significant updates
- **0-39%**: Very Low Trust - Documentation is unreliable

## Validation Process

### Phase 1: Content Extraction
1. **Parse Documentation Files**
   - Extract API endpoints from markdown code blocks
   - Identify framework mentions
   - Parse configuration variables
   - Extract file references
   - Analyze code examples

2. **Content Classification**
   - Categorize extracted content by type
   - Assign confidence scores based on extraction method
   - Detect duplicate or conflicting information

### Phase 2: Evidence Gathering
1. **Codebase Analysis**
   - Scan for API route definitions
   - Analyze import statements and dependencies
   - Extract configuration patterns
   - Identify file structure

2. **Cross-Reference**
   - Match documented claims with code evidence
   - Identify gaps and conflicts
   - Generate evidence matrix

### Phase 3: Validation Execution
1. **Rule Application**
   - Apply validation rules to each claim
   - Generate issue reports with severity levels
   - Collect supporting evidence

2. **Trust Score Calculation**
   - Calculate individual category scores
   - Apply weighted averaging
   - Generate overall trust score

### Phase 4: Report Generation
1. **Issue Prioritization**
   - Sort issues by severity and impact
   - Generate actionable recommendations
   - Create update plans

2. **Documentation Enhancement**
   - Identify missing documentation
   - Suggest improvements to existing content
   - Recommend structural changes

## Evidence Sources

### Primary Sources
- **Package Files**: `package.json`, `requirements.txt`, `pom.xml`
- **Configuration Files**: `.env`, `config.js`, settings files
- **Source Code**: Route definitions, class declarations, imports
- **Build Files**: `webpack.config.js`, `vite.config.ts`

### Secondary Sources
- **Test Files**: API tests, component tests
- **Example Files**: Sample code, demos
- **CI/CD Configs**: Deployment scripts, workflows
- **Documentation Tools**: OpenAPI specs, JSDoc

### Tertiary Sources
- **Git History**: Recent changes, feature additions
- **Issue Trackers**: Bug reports, feature requests
- **Community Resources**: Stack Overflow, GitHub issues

## False Positive Mitigation

### Common False Positives
1. **Optional Dependencies**: Technologies mentioned as options but not required
2. **Multiple Environments**: Different configs for dev/staging/prod
3. **Legacy Code**: Old implementations still referenced
4. **External Services**: Third-party APIs and services

### Mitigation Strategies
1. **Context Analysis**: Consider surrounding documentation context
2. **Conditional Logic**: Handle optional/conditional mentions
3. **Version Awareness**: Account for different versions
4. **Environment Specifics**: Recognize environment-specific configurations

## Continuous Improvement

### Rule Refinement
- Monitor validation accuracy
- Collect feedback on false positives/negatives
- Update patterns based on new technologies
- Adjust scoring weights based on real-world impact

### Pattern Learning
- Analyze successful validation patterns
- Learn from correction feedback
- Adapt to project-specific conventions
- Improve detection algorithms

This validation framework ensures comprehensive and accurate assessment of documentation quality while minimizing false positives and providing actionable improvement recommendations.