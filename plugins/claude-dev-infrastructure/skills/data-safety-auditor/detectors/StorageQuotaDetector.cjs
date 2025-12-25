/**
 * StorageQuotaDetector - Detects storage quota related risks
 */

const fs = require('fs');
const { AuditFinding } = require('../core/AuditFinding.cjs');
const { RiskRegistry } = require('../core/RiskRegistry.cjs');

class StorageQuotaDetector {
  constructor() {
    this.registry = new RiskRegistry();
  }

  async detect(files, options = {}) {
    const findings = [];

    for (const file of files) {
      if (!file.endsWith('.js') && !file.endsWith('.ts') && !file.endsWith('.vue')) continue;

      try {
        const content = fs.readFileSync(file, 'utf8');
        findings.push(...this._analyzeFile(file, content));
      } catch (err) {
        // Skip unreadable
      }
    }

    return findings;
  }

  _analyzeFile(file, content) {
    const findings = [];

    // Check for unhandled setItem
    const setItemMatches = content.match(/await\s+\w*\.?setItem\s*\(/g) || [];
    const hasTryCatch = /try\s*\{[^}]*setItem[^}]*\}\s*catch/.test(content);

    if (setItemMatches.length > 0 && !hasTryCatch) {
      findings.push(AuditFinding.fromRisk(
        this.registry.getRisk('UNHANDLED_QUOTA_ERROR'),
        file,
        { codeSnippet: setItemMatches[0] }
      ));
    }

    // Check for quota monitoring
    if (/localforage|indexedDB/.test(content) && !/navigator\.storage\.estimate/.test(content)) {
      findings.push(AuditFinding.fromRisk(
        this.registry.getRisk('NO_QUOTA_MONITORING'),
        file
      ));
    }

    // Check for persistent storage request
    if (/indexedDB/.test(content) && !/navigator\.storage\.persist/.test(content)) {
      findings.push(AuditFinding.fromRisk(
        this.registry.getRisk('NO_PERSISTENT_STORAGE'),
        file
      ));
    }

    return findings;
  }
}

module.exports = { StorageQuotaDetector };
