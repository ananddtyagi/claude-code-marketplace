/**
 * Chief Architect - Strategic Development Orchestrator
 *
 * Implements enterprise-grade architectural decision making and
 * orchestration of specialized development skills.
 */

const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

class ChiefArchitect {
  constructor() {
    this.projectRoot = process.cwd();
    this.knowledgeBase = new Map();
    this.decisionHistory = [];
    this.activeSkills = new Map();
  }

  /**
   * Main orchestration entry point
   */
  async execute(input, context = {}) {
    const command = this.parseCommand(input);

    switch (command.action) {
      case 'analyze-project-context':
        return await this.analyzeProjectContext(command.options);

      case 'orchestrate-implementation':
        return await this.orchestrateImplementation(command.options);

      case 'make-architectural-decision':
        return await this.makeArchitecturalDecision(command.options);

      case 'analyze-rxdb-migration-readiness':
        return await this.analyzeRxDBMigrationReadiness(command.options);

      default:
        return this.generateArchitecturalRecommendation(input, context);
    }
  }

  /**
   * Parse command input
   */
  parseCommand(input) {
    const patterns = {
      'analyze-project-context': /analyze.*project.*context|project.*analysis/i,
      'orchestrate-implementation': /orchestrate.*implementation|implement.*rxdb/i,
      'make-architectural-decision': /architectural.*decision|decision.*making/i,
      'analyze-rxdb-migration-readiness': /rxdb.*migration.*readiness|migration.*analysis/i
    };

    for (const [action, pattern] of Object.entries(patterns)) {
      if (pattern.test(input)) {
        return { action, options: this.extractOptions(input) };
      }
    }

    return { action: 'generate-recommendation', options: {} };
  }

  /**
   * Extract options from command input
   */
  extractOptions(input) {
    const options = {};

    // Extract focus/scope
    const focusMatch = input.match(/--(?:focus|scope)\s+([^\s]+)/i);
    if (focusMatch) options.focus = focusMatch[1];

    // Extract decision
    const decisionMatch = input.match(/--(?:decision|strategy)\s+([^\s]+)/i);
    if (decisionMatch) options.decision = decisionMatch[1];

    // Extract architecture
    const archMatch = input.match(/--(?:architecture|arch)\s+([^\s]+)/i);
    if (archMatch) options.architecture = archMatch[1];

    return options;
  }

  /**
   * Analyze project context for architectural decisions
   */
  async analyzeProjectContext(options = {}) {
    const focus = options.focus || 'general';
    const scope = options.scope || 'src/';

    console.log(`🔍 Chief Architect: Analyzing project context...`);
    console.log(`   Focus: ${focus}`);
    console.log(`   Scope: ${scope}`);

    const analysis = {
      timestamp: new Date().toISOString(),
      focus,
      scope,
      findings: {},
      recommendations: [],
      readinessScore: 0
    };

    // Technology Stack Assessment
    analysis.findings.technologyStack = await this.analyzeTechnologyStack();

    // Codebase Structure Analysis
    analysis.findings.codebaseStructure = await this.analyzeCodebaseStructure(scope);

    // Database Assessment (for RxDB migration)
    if (focus.includes('rxdb') || focus.includes('migration')) {
      analysis.findings.databaseAssessment = await this.analyzeDatabaseReadiness();
    }

    // TypeScript Foundation Assessment
    analysis.findings.typeScriptAssessment = await this.analyzeTypeScriptFoundation();

    // Calculate readiness score
    analysis.readinessScore = this.calculateReadinessScore(analysis.findings);

    // Generate recommendations
    analysis.recommendations = this.generateRecommendations(analysis.findings);

    console.log(`✅ Analysis complete. Readiness Score: ${analysis.readinessScore}/10`);

    return analysis;
  }

  /**
   * Analyze current technology stack
   */
  async analyzeTechnologyStack() {
    const packageJsonPath = path.join(this.projectRoot, 'package.json');

    if (!fs.existsSync(packageJsonPath)) {
      return { error: 'package.json not found' };
    }

    const packageJson = JSON.parse(fs.readFileSync(packageJsonPath, 'utf8'));
    const dependencies = { ...packageJson.dependencies, ...packageJson.devDependencies };

    return {
      framework: dependencies.vue || 'Not found',
      typescript: dependencies.typescript || 'Not found',
      stateManagement: dependencies.pinia || 'Not found',
      buildTool: dependencies.vite || 'Not found',
      currentDatabase: dependencies.localforage || 'None found',
      targetDatabase: dependencies.rxdb || 'Not installed',
      testing: {
        vitest: dependencies.vitest || 'Not found',
        playwright: dependencies.playwright || 'Not found'
      }
    };
  }

  /**
   * Analyze codebase structure
   */
  async analyzeCodebaseStructure(scope) {
    const srcPath = path.join(this.projectRoot, scope);

    if (!fs.existsSync(srcPath)) {
      return { error: `Source directory ${scope} not found` };
    }

    const structure = {
      stores: this.findFiles(path.join(srcPath, 'stores'), '.ts'),
      composables: this.findFiles(path.join(srcPath, 'composables'), '.ts'),
      components: this.findFiles(path.join(srcPath, 'components'), '.vue'),
      database: this.findFiles(path.join(srcPath, 'database'), '.ts')
    };

    // Analyze stores complexity
    structure.storeAnalysis = await this.analyzeStores(structure.stores);

    return structure;
  }

  /**
   * Find files in directory
   */
  findFiles(dir, extension) {
    if (!fs.existsSync(dir)) return [];

    const files = [];
    const items = fs.readdirSync(dir);

    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);

      if (stat.isFile() && item.endsWith(extension)) {
        files.push(fullPath);
      } else if (stat.isDirectory()) {
        files.push(...this.findFiles(fullPath, extension));
      }
    }

    return files;
  }

  /**
   * Analyze stores complexity
   */
  async analyzeStores(storeFiles) {
    const analysis = {
      count: storeFiles.length,
      totalLines: 0,
      complexity: 'low',
      largestStore: null
    };

    for (const storeFile of storeFiles) {
      try {
        const content = fs.readFileSync(storeFile, 'utf8');
        const lines = content.split('\n').length;
        analysis.totalLines += lines;

        if (!analysis.largestStore || lines > analysis.largestStore.lines) {
          analysis.largestStore = {
            file: path.basename(storeFile),
            lines
          };
        }
      } catch (error) {
        console.warn(`Could not analyze ${storeFile}:`, error.message);
      }
    }

    if (analysis.totalLines > 2000) analysis.complexity = 'high';
    else if (analysis.totalLines > 1000) analysis.complexity = 'medium';

    return analysis;
  }

  /**
   * Analyze database readiness for RxDB migration
   */
  async analyzeDatabaseReadiness() {
    const databasePath = path.join(this.projectRoot, 'src', 'database');

    const assessment = {
      hasRxDBSchemas: false,
      hasDatabaseDirectory: fs.existsSync(databasePath),
      currentDatabase: 'localforage',
      migrationComplexity: 'medium'
    };

    // Check for RxDB schema file
    const schemaPath = path.join(databasePath, 'rxdb-schema.ts');
    if (fs.existsSync(schemaPath)) {
      assessment.hasRxDBSchemas = true;

      try {
        const schemaContent = fs.readFileSync(schemaPath, 'utf8');
        const lines = schemaContent.split('\n').length;
        assessment.schemaComplexity = lines > 500 ? 'comprehensive' : 'basic';
      } catch (error) {
        console.warn(`Could not read RxDB schemas:`, error.message);
      }
    }

    // Check current database composables
    const databaseComposablePath = path.join(this.projectRoot, 'src', 'composables', 'useDatabase.ts');
    if (fs.existsSync(databaseComposablePath)) {
      assessment.hasCurrentDatabaseLayer = true;
    }

    return assessment;
  }

  /**
   * Analyze TypeScript foundation
   */
  async analyzeTypeScriptFoundation() {
    const tsconfigPath = path.join(this.projectRoot, 'tsconfig.json');
    const typesPath = path.join(this.projectRoot, 'src', 'types');

    return {
      hasTsConfig: fs.existsSync(tsconfigPath),
      hasTypesDirectory: fs.existsSync(typesPath),
      typeFiles: this.findFiles(typesPath, '.ts'),
      compilationStatus: 'ready' // Assume ready based on documentation
    };
  }

  /**
   * Calculate overall readiness score
   */
  calculateReadinessScore(findings) {
    let score = 0;

    // Technology stack (30%)
    if (findings.technologyStack.framework !== 'Not found') score += 1;
    if (findings.technologyStack.typescript !== 'Not found') score += 1;
    if (findings.technologyStack.stateManagement !== 'Not found') score += 1;

    // Codebase structure (25%)
    if (findings.codebaseStructure.stores.length > 0) score += 1;
    if (findings.codebaseStructure.composables.length > 0) score += 1;
    if (findings.codebaseStructure.components.length > 0) score += 1;

    // Database readiness (25%)
    if (findings.databaseAssessment?.hasRxDBSchemas) score += 2;
    if (findings.databaseAssessment?.hasDatabaseDirectory) score += 1;

    // TypeScript foundation (20%)
    if (findings.typeScriptAssessment?.hasTsConfig) score += 1;
    if (findings.typeScriptAssessment?.typeFiles.length > 0) score += 1;

    return Math.min(10, score);
  }

  /**
   * Generate architectural recommendations
   */
  generateRecommendations(findings) {
    const recommendations = [];

    // Database recommendations
    if (findings.databaseAssessment?.hasRxDBSchemas) {
      recommendations.push({
        category: 'Database',
        priority: 'high',
        action: 'Proceed with RxDB migration using existing schemas',
        rationale: 'Professional schema design already in place'
      });
    }

    // Architecture recommendations
    if (findings.codebaseStructure.storeAnalysis?.complexity === 'high') {
      recommendations.push({
        category: 'Architecture',
        priority: 'medium',
        action: 'Migrate stores systematically, starting with smallest',
        rationale: 'Large stores require careful migration to avoid breaking changes'
      });
    }

    // TypeScript recommendations
    if (findings.typeScriptAssessment?.hasTsConfig) {
      recommendations.push({
        category: 'Type Safety',
        priority: 'high',
        action: 'Maintain TypeScript compilation throughout migration',
        rationale: 'Strong type foundation prevents runtime errors'
      });
    }

    return recommendations;
  }

  /**
   * Orchestrate implementation of architectural decisions
   */
  async orchestrateImplementation(options = {}) {
    console.log(`🎣 Chief Architect: Orchestrating implementation...`);

    const decision = options.decision || 'rxdb-clean-slate-migration';
    const strategy = options.strategy || 'frontend-coupled';
    const timeline = options.timeline || '2-3-days';

    const orchestration = {
      decision,
      strategy,
      timeline,
      phases: [],
      dependencies: [],
      risks: []
    };

    switch (decision) {
      case 'rxdb-clean-slate-migration':
        orchestration.phases = this.getRxDBMigrationPhases();
        orchestration.dependencies = ['rxdb', '@rxdb/storage-memory'];
        orchestration.risks = ['Breaking changes to stores', 'Performance regression'];
        break;

      default:
        orchestration.phases = [{
          name: 'Analysis',
          description: 'Analyze requirements and create implementation plan',
          duration: '2-4 hours'
        }];
    }

    console.log(`📋 Implementation orchestration created with ${orchestration.phases.length} phases`);

    return orchestration;
  }

  /**
   * Get RxDB migration phases
   */
  getRxDBMigrationPhases() {
    return [
      {
        name: 'Foundation Setup',
        description: 'Install RxDB dependencies and create database infrastructure',
        duration: '4 hours',
        tasks: [
          'Install RxDB packages',
          'Create database initialization',
          'Setup RxDB schemas'
        ]
      },
      {
        name: 'Store Migration',
        description: 'Migrate Pinia stores to use RxDB backing',
        duration: '6 hours',
        tasks: [
          'Migrate small stores (ui, notifications)',
          'Migrate medium stores (canvas, timer)',
          'Migrate large store (tasks)'
        ]
      },
      {
        name: 'Integration & Testing',
        description: 'Update composables and run comprehensive testing',
        duration: '4 hours',
        tasks: [
          'Update database-dependent composables',
          'Run integration tests',
          'Validate with Playwright'
        ]
      },
      {
        name: 'Quality Assurance',
        description: 'Final validation and documentation',
        duration: '2 hours',
        tasks: [
          'TypeScript compilation validation',
          'Performance benchmarking',
          'Documentation updates'
        ]
      }
    ];
  }

  /**
   * Generate architectural recommendation
   */
  generateArchitecturalRecommendation(input, context) {
    return {
      recommendation: 'Use Chief Architect for complex architectural decisions',
      suggestedActions: [
        'Run project context analysis',
        'Create architectural decision record',
        'Orchestrate implementation with specialized skills'
      ],
      nextSteps: [
        'chief-architect analyze-project-context --focus rxdb-migration',
        'chief-architect orchestrate-implementation --decision rxdb-clean-slate-migration'
      ]
    };
  }
}

// Export for use as skill
module.exports = {
  async execute(input, context = {}) {
    const architect = new ChiefArchitect();
    return await architect.execute(input, context);
  },

  // Skill metadata
  name: 'chief-architect',
  description: 'Strategic Development Orchestrator - Chief Enterprise Architect meta-skill',
  version: '1.0.0',
  category: 'Meta-Skill'
};