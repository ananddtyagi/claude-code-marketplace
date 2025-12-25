/**
 * DataSafetyAuditor - Main orchestration class for data safety audits
 *
 * Coordinates all detectors, generates reports, and provides remediation guidance
 */

const fs = require('fs');
const path = require('path');
const { RiskRegistry } = require('./RiskRegistry.cjs');
const { AuditFinding, FindingsCollection } = require('./AuditFinding.cjs');

// Import all detectors
const { StorageQuotaDetector } = require('../detectors/StorageQuotaDetector.cjs');
const { SafariITPDetector } = require('../detectors/SafariITPDetector.cjs');
const { PiniaHydrationDetector } = require('../detectors/PiniaHydrationDetector.cjs');
const { PouchDBSyncDetector } = require('../detectors/PouchDBSyncDetector.cjs');
const { LocalForageDetector } = require('../detectors/LocalForageDetector.cjs');
const { DataIntegrityDetector } = require('../detectors/DataIntegrityDetector.cjs');

class DataSafetyAuditor {
  constructor(options = {}) {
    this.riskRegistry = new RiskRegistry();
    this.options = {
      strict: options.strict ?? false,
      minSeverity: options.minSeverity ?? 'LOW',
      includeTesting: options.includeTesting ?? true,
      projectRoot: options.projectRoot ?? process.cwd(),
      ...options
    };
    this.findings = new FindingsCollection();

    // Auto-register all detectors
    this.detectors = {
      'StorageQuota': new StorageQuotaDetector(),
      'SafariITP': new SafariITPDetector(),
      'PiniaHydration': new PiniaHydrationDetector(),
      'PouchDBSync': new PouchDBSyncDetector(),
      'LocalForage': new LocalForageDetector(),
      'DataIntegrity': new DataIntegrityDetector()
    };
  }

  /**
   * Register a detector
   */
  registerDetector(name, detector) {
    this.detectors[name] = detector;
  }

  /**
   * Run full audit on a Vue app
   */
  async auditVueApp(sourcePath) {
    const startTime = Date.now();
    this.findings = new FindingsCollection();

    console.log('\n🛡️  Data Safety Audit Starting...\n');
    console.log(`📁 Scanning: ${sourcePath}\n`);

    // Collect all relevant files
    const files = this._collectFiles(sourcePath);
    console.log(`📄 Found ${files.length} files to analyze\n`);

    // Run all registered detectors
    for (const [name, detector] of Object.entries(this.detectors)) {
      console.log(`🔍 Running ${name}...`);
      try {
        const detectorFindings = await detector.detect(files, this.options);
        this.findings.addAll(detectorFindings);
        console.log(`   Found ${detectorFindings.length} issues`);
      } catch (err) {
        console.error(`   Error in ${name}: ${err.message}`);
      }
    }

    // Run built-in checks
    await this._runBuiltInChecks(sourcePath);

    const duration = Date.now() - startTime;
    console.log(`\n✅ Audit completed in ${duration}ms\n`);

    return this.generateReport();
  }

  /**
   * Run built-in checks that don't require file parsing
   */
  async _runBuiltInChecks(sourcePath) {
    // Check for sync disabled
    const syncDisabledFiles = this._grepFiles(sourcePath, /sync.*disabled|disabled.*sync/i);
    if (syncDisabledFiles.length > 0) {
      const risk = this.riskRegistry.getRisk('SYNC_DISABLED');
      this.findings.add(AuditFinding.fromRisk(risk, syncDisabledFiles[0], {
        metadata: { files: syncDisabledFiles }
      }));
    }

    // Check for quota handling
    const storageFiles = this._grepFiles(sourcePath, /localforage\.setItem|indexedDB/);
    const quotaHandling = this._grepFiles(sourcePath, /QuotaExceededError|catch.*quota/i);
    if (storageFiles.length > 0 && quotaHandling.length === 0) {
      const risk = this.riskRegistry.getRisk('UNHANDLED_QUOTA_ERROR');
      this.findings.add(AuditFinding.fromRisk(risk, 'Multiple files', {
        metadata: { storageFiles }
      }));
    }

    // Check for Safari ITP handling
    const safariHandling = this._grepFiles(sourcePath, /safari.*itp|itp.*safari|7.*day/i);
    if (storageFiles.length > 0 && safariHandling.length === 0) {
      const risk = this.riskRegistry.getRisk('SAFARI_ITP_EXPIRATION');
      this.findings.add(AuditFinding.fromRisk(risk, 'Project-wide'));
    }

    // Check for hydration guards
    const persistStores = this._grepFiles(sourcePath, /persist:\s*true/);
    const hydrationGuards = this._grepFiles(sourcePath, /isHydrated|hydrationComplete/);
    if (persistStores.length > 0 && hydrationGuards.length === 0) {
      const risk = this.riskRegistry.getRisk('NO_HYDRATION_GUARD');
      this.findings.add(AuditFinding.fromRisk(risk, persistStores[0]));
    }

    // Check for conflict handling
    const pouchdbUsage = this._grepFiles(sourcePath, /PouchDB|\.replicate|\.sync\(/);
    const conflictHandling = this._grepFiles(sourcePath, /conflicts:\s*true|_conflicts/);
    if (pouchdbUsage.length > 0 && conflictHandling.length === 0) {
      const risk = this.riskRegistry.getRisk('NO_CONFLICT_DETECTION');
      this.findings.add(AuditFinding.fromRisk(risk, 'Project-wide'));
    }
  }

  /**
   * Audit specific aspects
   */
  async checkQuotaRisks(sourcePath) {
    const findings = new FindingsCollection();
    const files = this._grepFiles(sourcePath, /localforage|indexedDB|localStorage/);

    for (const file of files) {
      const content = fs.readFileSync(file, 'utf8');

      // Check for unhandled setItem
      if (/\.setItem\(/.test(content) && !/try\s*\{[^}]*setItem/.test(content)) {
        const risk = this.riskRegistry.getRisk('UNHANDLED_QUOTA_ERROR');
        findings.add(AuditFinding.fromRisk(risk, file));
      }

      // Check for quota monitoring
      if (!/navigator\.storage\.estimate/.test(content)) {
        const risk = this.riskRegistry.getRisk('NO_QUOTA_MONITORING');
        findings.add(AuditFinding.fromRisk(risk, file));
      }
    }

    return findings;
  }

  async checkSafariCompat(sourcePath) {
    const findings = new FindingsCollection();

    // Check for Safari detection
    const safariCheck = this._grepFiles(sourcePath, /safari|webkit/i);
    if (safariCheck.length === 0) {
      const risk = this.riskRegistry.getRisk('NO_SAFARI_DETECTION');
      findings.add(AuditFinding.fromRisk(risk, 'Project-wide'));
    }

    // Check for ITP mitigation
    const itpMitigation = this._grepFiles(sourcePath, /itp|7.*day.*sync|sync.*3.*day/i);
    if (itpMitigation.length === 0) {
      const risk = this.riskRegistry.getRisk('SAFARI_ITP_EXPIRATION');
      findings.add(AuditFinding.fromRisk(risk, 'Project-wide'));
    }

    return findings;
  }

  async checkPiniaPersistence(sourcePath) {
    const findings = new FindingsCollection();
    const storeFiles = this._grepFiles(sourcePath, /defineStore/);

    for (const file of storeFiles) {
      const content = fs.readFileSync(file, 'utf8');

      // Check for persist without hydration guard
      if (/persist:\s*true/.test(content) && !/isHydrated/.test(content)) {
        const risk = this.riskRegistry.getRisk('NO_HYDRATION_GUARD');
        findings.add(AuditFinding.fromRisk(risk, file));
      }

      // Check for afterRestore hook
      if (/persist:\s*true/.test(content) && !/afterRestore/.test(content)) {
        const risk = this.riskRegistry.getRisk('MISSING_RESTORE_HOOK');
        findings.add(AuditFinding.fromRisk(risk, file));
      }
    }

    return findings;
  }

  async checkSyncIntegrity(sourcePath) {
    const findings = new FindingsCollection();
    const syncFiles = this._grepFiles(sourcePath, /\.replicate|\.sync\(|PouchDB/);

    for (const file of syncFiles) {
      const content = fs.readFileSync(file, 'utf8');

      // Check for error handling
      if (/\.(replicate|sync)\(/.test(content) && !/.on\(['"]error/.test(content)) {
        const risk = this.riskRegistry.getRisk('NO_SYNC_ERROR_HANDLING');
        findings.add(AuditFinding.fromRisk(risk, file));
      }

      // Check for conflict detection
      if (!/{[^}]*conflicts:\s*true/.test(content)) {
        const risk = this.riskRegistry.getRisk('NO_CONFLICT_DETECTION');
        findings.add(AuditFinding.fromRisk(risk, file));
      }
    }

    return findings;
  }

  /**
   * Check live database state
   */
  async checkDatabaseState(dbInfo) {
    const findings = new FindingsCollection();

    // Check for empty canvas data
    if (dbInfo.canvasNodes === 0 && dbInfo.totalTasks > 0) {
      const risk = this.riskRegistry.getRisk('EMPTY_CANVAS_DATA');
      findings.add(AuditFinding.fromRisk(risk, 'canvas:data', {
        metadata: { canvasNodes: 0, totalTasks: dbInfo.totalTasks }
      }));
    }

    // Check for data mismatch
    if (dbInfo.localCount && dbInfo.remoteCount) {
      const diff = Math.abs(dbInfo.localCount - dbInfo.remoteCount);
      const threshold = Math.max(dbInfo.localCount, dbInfo.remoteCount) * 0.1;
      if (diff > threshold) {
        const risk = this.riskRegistry.getRisk('DATA_MISMATCH');
        findings.add(AuditFinding.fromRisk(risk, 'Database', {
          metadata: { local: dbInfo.localCount, remote: dbInfo.remoteCount }
        }));
      }
    }

    return findings;
  }

  /**
   * Generate test suite for missing coverage
   */
  generateTestSuite() {
    const tests = [];

    // Persistence test
    tests.push({
      name: 'data persists after reload',
      code: `
test('data persists after page reload', async ({ page }) => {
  await page.goto('http://localhost:5546');
  await page.fill('[data-testid="task-input"]', 'Persistence Test');
  await page.click('[data-testid="save-task"]');
  await page.reload();
  await expect(page.locator('text=Persistence Test')).toBeVisible();
});`
    });

    // Quota test
    tests.push({
      name: 'handles quota exceeded gracefully',
      code: `
test('handles storage quota exceeded', async ({ page }) => {
  // Fill storage to simulate quota exceeded
  await page.evaluate(() => {
    const largeData = 'x'.repeat(5 * 1024 * 1024);
    for (let i = 0; i < 100; i++) {
      localStorage.setItem('fill_' + i, largeData);
    }
  });
  // Try to save - should show warning, not crash
  await page.fill('[data-testid="task-input"]', 'Quota Test');
  await expect(page.locator('text=Storage')).toBeVisible();
});`
    });

    // Offline sync test
    tests.push({
      name: 'syncs after coming back online',
      code: `
test('syncs data after offline period', async ({ page, context }) => {
  await page.goto('http://localhost:5546');
  await context.setOffline(true);
  await page.fill('[data-testid="task-input"]', 'Offline Task');
  await page.click('[data-testid="save-task"]');
  await context.setOffline(false);
  // Wait for sync indicator
  await expect(page.locator('[data-testid="sync-status"]')).toContainText('Synced');
});`
    });

    return tests;
  }

  /**
   * Generate report
   */
  generateReport() {
    const summary = this.findings.getSummary();
    const sorted = this.findings.sortBySeverity();

    return {
      timestamp: new Date().toISOString(),
      summary,
      findings: sorted,
      hasBlockers: this.findings.hasBlockers(),
      blockers: this.findings.getBlockers(),

      toConsole: () => this._formatConsole(summary, sorted),
      toJSON: () => JSON.stringify({ summary, findings: sorted.map(f => f.toJSON()) }, null, 2),
      toMarkdown: () => this._formatMarkdown(summary, sorted),
      toHTML: () => this._formatHTML(summary, sorted)
    };
  }

  /**
   * Format for console output
   */
  _formatConsole(summary, findings) {
    const RED = '\x1b[31m';
    const YELLOW = '\x1b[33m';
    const CYAN = '\x1b[36m';
    const GREEN = '\x1b[32m';
    const RESET = '\x1b[0m';

    let output = '\n';
    output += '╔══════════════════════════════════════════════════════════════╗\n';
    output += '║              🛡️  DATA SAFETY AUDIT REPORT                    ║\n';
    output += '╠══════════════════════════════════════════════════════════════╣\n';

    if (summary.blockers > 0) {
      output += `║  ${RED}⛔ DEPLOYMENT BLOCKED${RESET}                                       ║\n`;
    } else if (summary.high > 0) {
      output += `║  ${YELLOW}⚠️  WARNINGS FOUND${RESET}                                          ║\n`;
    } else {
      output += `║  ${GREEN}✅ PASSED${RESET}                                                   ║\n`;
    }

    output += '╠══════════════════════════════════════════════════════════════╣\n';
    output += `║  Total Issues: ${summary.total.toString().padEnd(46)}║\n`;
    output += `║  ${RED}Critical: ${summary.critical}${RESET}  ${YELLOW}High: ${summary.high}${RESET}  ${CYAN}Medium: ${summary.medium}${RESET}  Low: ${summary.low}         ║\n`;
    output += '╚══════════════════════════════════════════════════════════════╝\n\n';

    if (findings.length > 0) {
      output += '📋 FINDINGS:\n\n';
      findings.forEach(f => {
        output += f.toConsoleString() + '\n';
      });
    }

    return output;
  }

  /**
   * Format for markdown
   */
  _formatMarkdown(summary, findings) {
    let md = '# Data Safety Audit Report\n\n';
    md += `**Date:** ${new Date().toISOString()}\n\n`;

    md += '## Summary\n\n';
    md += `| Severity | Count |\n|----------|-------|\n`;
    md += `| Critical | ${summary.critical} |\n`;
    md += `| High | ${summary.high} |\n`;
    md += `| Medium | ${summary.medium} |\n`;
    md += `| Low | ${summary.low} |\n`;
    md += `| **Total** | **${summary.total}** |\n\n`;

    if (summary.blockers > 0) {
      md += '> ⛔ **DEPLOYMENT BLOCKED** - Critical issues must be resolved\n\n';
    }

    md += '## Findings\n\n';
    findings.forEach(f => {
      md += f.toMarkdown();
    });

    return md;
  }

  /**
   * Format for HTML
   */
  _formatHTML(summary, findings) {
    return `<!DOCTYPE html>
<html>
<head>
  <title>Data Safety Audit Report</title>
  <style>
    body { font-family: -apple-system, sans-serif; padding: 20px; max-width: 900px; margin: 0 auto; }
    .summary { background: #f5f5f5; padding: 20px; border-radius: 8px; margin-bottom: 20px; }
    .critical { color: #dc3545; }
    .high { color: #fd7e14; }
    .medium { color: #17a2b8; }
    .low { color: #6c757d; }
    .finding { border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 4px; }
    .finding.critical { border-left: 4px solid #dc3545; }
    .finding.high { border-left: 4px solid #fd7e14; }
    .finding.medium { border-left: 4px solid #17a2b8; }
    .blocker { background: #fff5f5; border: 2px solid #dc3545; padding: 10px; margin: 10px 0; }
  </style>
</head>
<body>
  <h1>🛡️ Data Safety Audit Report</h1>
  <div class="summary">
    <h2>Summary</h2>
    <p><span class="critical">Critical: ${summary.critical}</span> |
       <span class="high">High: ${summary.high}</span> |
       <span class="medium">Medium: ${summary.medium}</span> |
       <span class="low">Low: ${summary.low}</span></p>
    ${summary.blockers > 0 ? '<div class="blocker">⛔ DEPLOYMENT BLOCKED</div>' : ''}
  </div>
  <h2>Findings</h2>
  ${findings.map(f => `
    <div class="finding ${f.severity.toLowerCase()}">
      <h3>[${f.severity}] ${f.title}</h3>
      <p><strong>Location:</strong> ${f.location}</p>
      <p>${f.description}</p>
      ${f.suggestion ? `<p><strong>Fix:</strong> ${f.suggestion}</p>` : ''}
    </div>
  `).join('')}
</body>
</html>`;
  }

  /**
   * Collect source files
   */
  _collectFiles(dir, extensions = ['.js', '.ts', '.vue']) {
    const files = [];
    if (!fs.existsSync(dir)) return files;

    const items = fs.readdirSync(dir, { withFileTypes: true });
    for (const item of items) {
      const fullPath = path.join(dir, item.name);
      if (item.isDirectory() && !item.name.startsWith('.') && item.name !== 'node_modules') {
        files.push(...this._collectFiles(fullPath, extensions));
      } else if (item.isFile() && extensions.some(ext => item.name.endsWith(ext))) {
        files.push(fullPath);
      }
    }
    return files;
  }

  /**
   * Grep files for pattern
   */
  _grepFiles(dir, pattern) {
    const matches = [];
    const files = this._collectFiles(dir);

    for (const file of files) {
      try {
        const content = fs.readFileSync(file, 'utf8');
        if (pattern.test(content)) {
          matches.push(file);
        }
      } catch (err) {
        // Skip unreadable files
      }
    }

    return matches;
  }
}

module.exports = { DataSafetyAuditor };
