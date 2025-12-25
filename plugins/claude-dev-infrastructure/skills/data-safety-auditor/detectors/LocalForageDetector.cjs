/**
 * LocalForageDetector - Detects LocalForage usage risks
 */

const fs = require('fs');
const { AuditFinding } = require('../core/AuditFinding.cjs');
const { RiskRegistry } = require('../core/RiskRegistry.cjs');

class LocalForageDetector {
  constructor() {
    this.registry = new RiskRegistry();
  }

  async detect(files, options = {}) {
    const findings = [];
    let usesLocalForage = false;
    let hasConfig = false;
    let hasDriverCheck = false;
    let hasErrorHandling = false;

    for (const file of files) {
      try {
        const content = fs.readFileSync(file, 'utf8');

        if (/localforage/.test(content)) {
          usesLocalForage = true;
          findings.push(...this._analyzeFile(file, content));
        }

        if (/localforage\.config/.test(content)) {
          hasConfig = true;
        }

        if (/localforage\.(driver|ready)/.test(content)) {
          hasDriverCheck = true;
        }

        if (/try\s*\{[^}]*localforage/.test(content)) {
          hasErrorHandling = true;
        }
      } catch (err) {
        // Skip
      }
    }

    if (usesLocalForage) {
      if (!hasConfig) {
        findings.push(AuditFinding.fromRisk(
          this.registry.getRisk('LOCALFORAGE_NOT_CONFIGURED'),
          'Project-wide',
          {
            suggestion: 'Configure LocalForage with unique name and store',
            codeSnippet: `localforage.config({
  name: 'pomo-flow',
  storeName: 'app_data'
});`
          }
        ));
      }

      if (!hasDriverCheck) {
        findings.push(AuditFinding.fromRisk(
          this.registry.getRisk('DRIVER_NOT_VALIDATED'),
          'Project-wide',
          {
            suggestion: 'Check driver after ready() to ensure IndexedDB is used',
            codeSnippet: `await localforage.ready();
const driver = localforage.driver();
if (driver !== localforage.INDEXEDDB) {
  console.warn('Using fallback storage driver:', driver);
}`
          }
        ));
      }

      if (!hasErrorHandling) {
        findings.push(AuditFinding.fromRisk(
          this.registry.getRisk('UNHANDLED_STORAGE_ERROR'),
          'Project-wide',
          { suggestion: 'Wrap all LocalForage operations in try/catch' }
        ));
      }
    }

    return findings;
  }

  _analyzeFile(file, content) {
    const findings = [];

    // Check for race conditions - multiple setItem without queue
    const setItemCount = (content.match(/localforage\.setItem/g) || []).length;
    const hasQueue = /queue|mutex|lock/i.test(content);

    if (setItemCount > 3 && !hasQueue) {
      findings.push(AuditFinding.fromRisk(
        this.registry.getRisk('RACE_CONDITION_SAME_KEY'),
        file,
        { suggestion: 'Implement write queue for concurrent operations' }
      ));
    }

    // Check for non-atomic multi-item updates
    const consecutiveSetItems = /setItem[^;]*;\s*(?:await\s+)?localforage\.setItem/.test(content);
    if (consecutiveSetItems) {
      findings.push(AuditFinding.fromRisk(
        this.registry.getRisk('NON_ATOMIC_UPDATE'),
        file,
        { suggestion: 'Use single key with object, or implement transaction pattern' }
      ));
    }

    return findings;
  }
}

module.exports = { LocalForageDetector };
