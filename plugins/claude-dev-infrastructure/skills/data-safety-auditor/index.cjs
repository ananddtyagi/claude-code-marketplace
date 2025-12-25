/**
 * Data Safety Auditor
 *
 * Comprehensive data loss risk detection for Vue 3 + Pinia + IndexedDB + PouchDB applications.
 *
 * @example
 * const { DataSafetyAuditor, RiskRegistry, RISKS } = require('./index.cjs');
 *
 * // Run full audit
 * const auditor = new DataSafetyAuditor();
 * const findings = await auditor.auditVueApp('/path/to/src');
 * console.log(auditor.generateReport(findings, 'console'));
 *
 * // Check specific risks
 * const quotaFindings = await auditor.checkQuotaRisks(files);
 * const safariFindings = await auditor.checkSafariCompat(files);
 *
 * // Check live database state
 * const integrityFindings = await auditor.checkDatabaseState({
 *   canvasNodes: 0,
 *   totalTasks: 15,
 *   localCount: 20,
 *   remoteCount: 25
 * });
 */

// Core modules
const { RiskRegistry, RISKS, SEVERITY_LEVELS, SeverityMatrix } = require('./core/RiskRegistry.cjs');
const { AuditFinding, FindingsCollection } = require('./core/AuditFinding.cjs');
const { DataSafetyAuditor } = require('./core/DataSafetyAuditor.cjs');

// Detectors
const { StorageQuotaDetector } = require('./detectors/StorageQuotaDetector.cjs');
const { SafariITPDetector } = require('./detectors/SafariITPDetector.cjs');
const { PiniaHydrationDetector } = require('./detectors/PiniaHydrationDetector.cjs');
const { PouchDBSyncDetector } = require('./detectors/PouchDBSyncDetector.cjs');
const { LocalForageDetector } = require('./detectors/LocalForageDetector.cjs');
const { DataIntegrityDetector } = require('./detectors/DataIntegrityDetector.cjs');

/**
 * Quick audit helper - runs full audit and returns summary
 *
 * @param {string} srcPath - Path to source directory
 * @param {Object} options - Audit options
 * @returns {Promise<Object>} Audit summary with findings and deployment gate status
 */
async function quickAudit(srcPath, options = {}) {
  const auditor = new DataSafetyAuditor();
  const findings = await auditor.auditVueApp(srcPath, options);

  const summary = {
    totalFindings: findings.length,
    criticalCount: findings.filter(f => f.severity === 'CRITICAL').length,
    highCount: findings.filter(f => f.severity === 'HIGH').length,
    mediumCount: findings.filter(f => f.severity === 'MEDIUM').length,
    lowCount: findings.filter(f => f.severity === 'LOW').length,
    blocksDeployment: findings.some(f => f.severity === 'CRITICAL'),
    categories: [...new Set(findings.map(f => f.category))],
    findings
  };

  return summary;
}

/**
 * Check database state for integrity issues
 *
 * @param {Object} dbState - Current database state
 * @param {number} dbState.canvasNodes - Number of canvas nodes
 * @param {number} dbState.totalTasks - Total task count
 * @param {number} [dbState.localCount] - Local document count
 * @param {number} [dbState.remoteCount] - Remote document count
 * @returns {Promise<Array>} Array of findings
 */
async function checkDbIntegrity(dbState) {
  const detector = new DataIntegrityDetector();
  return detector.checkDatabaseIntegrity(dbState);
}

/**
 * Generate test cases for detected risks
 *
 * @param {Array} findings - Array of AuditFinding objects
 * @returns {string} Generated test code
 */
function generateTests(findings) {
  const auditor = new DataSafetyAuditor();
  return auditor.generateTestSuite(findings);
}

// Export everything
module.exports = {
  // Main auditor
  DataSafetyAuditor,

  // Core classes
  RiskRegistry,
  AuditFinding,
  FindingsCollection,
  SeverityMatrix,

  // Constants
  RISKS,
  SEVERITY_LEVELS,

  // Detectors (for individual use)
  StorageQuotaDetector,
  SafariITPDetector,
  PiniaHydrationDetector,
  PouchDBSyncDetector,
  LocalForageDetector,
  DataIntegrityDetector,

  // Helper functions
  quickAudit,
  checkDbIntegrity,
  generateTests
};
