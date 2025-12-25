/**
 * SafariITPDetector - Detects Safari ITP related risks
 */

const fs = require('fs');
const { AuditFinding } = require('../core/AuditFinding.cjs');
const { RiskRegistry } = require('../core/RiskRegistry.cjs');

class SafariITPDetector {
  constructor() {
    this.registry = new RiskRegistry();
  }

  async detect(files, options = {}) {
    const findings = [];
    let hasSafariDetection = false;
    let hasITPMitigation = false;
    let hasPrivateModeCheck = false;
    let usesIndexedDB = false;

    for (const file of files) {
      if (!file.endsWith('.js') && !file.endsWith('.ts') && !file.endsWith('.vue')) continue;

      try {
        const content = fs.readFileSync(file, 'utf8');

        if (/indexedDB|localforage|PouchDB/.test(content)) {
          usesIndexedDB = true;
        }

        if (/safari|webkit/i.test(content) && /userAgent|platform/i.test(content)) {
          hasSafariDetection = true;
        }

        // More precise ITP detection - look for actual ITP handling code
        if (/\bITP\b|safari.*expir|7.day.*expir|forcedSync|ITP_SAFETY|storage.*expire/i.test(content)) {
          hasITPMitigation = true;
        }

        // More precise private mode detection - avoid matching TS 'private' keyword
        if (/privateMode|private.browsing|incognito.mode|isPrivateBrowsing|detectPrivate/i.test(content)) {
          hasPrivateModeCheck = true;
        }
      } catch (err) {
        // Skip
      }
    }

    if (usesIndexedDB && !hasSafariDetection) {
      findings.push(AuditFinding.fromRisk(
        this.registry.getRisk('NO_SAFARI_DETECTION'),
        'Project-wide',
        { suggestion: 'Add Safari browser detection to apply ITP mitigations' }
      ));
    }

    if (usesIndexedDB && !hasITPMitigation) {
      findings.push(AuditFinding.fromRisk(
        this.registry.getRisk('SAFARI_ITP_EXPIRATION'),
        'Project-wide',
        { suggestion: 'Implement forced sync every 3 days for Safari users' }
      ));
    }

    if (usesIndexedDB && !hasPrivateModeCheck) {
      findings.push(AuditFinding.fromRisk(
        this.registry.getRisk('NO_PRIVATE_MODE_DETECTION'),
        'Project-wide',
        { suggestion: 'Detect private mode and warn users data will not persist' }
      ));
    }

    return findings;
  }
}

module.exports = { SafariITPDetector };
