/**
 * PouchDBSyncDetector - Detects PouchDB/CouchDB sync risks
 */

const fs = require('fs');
const { AuditFinding } = require('../core/AuditFinding.cjs');
const { RiskRegistry } = require('../core/RiskRegistry.cjs');

class PouchDBSyncDetector {
  constructor() {
    this.registry = new RiskRegistry();
  }

  async detect(files, options = {}) {
    const findings = [];
    let usesPouchDB = false;
    let hasConflictDetection = false;
    let hasConflictResolution = false;
    let hasSyncErrorHandling = false;
    let hasRetryLogic = false;
    let syncDisabled = false;

    for (const file of files) {
      try {
        const content = fs.readFileSync(file, 'utf8');

        if (/PouchDB|pouchdb|\.replicate|\.sync\(/.test(content)) {
          usesPouchDB = true;
        }

        if (/conflicts:\s*true/.test(content)) {
          hasConflictDetection = true;
        }

        if (/_conflicts|resolveConflict|mergeConflict/.test(content)) {
          hasConflictResolution = true;
        }

        if (/\.on\(\s*['"]error['"]/.test(content)) {
          hasSyncErrorHandling = true;
        }

        if (/retry|backoff|setTimeout.*sync/i.test(content)) {
          hasRetryLogic = true;
        }

        if (/sync.*disabled|disabled.*sync|SYNCING_DISABLED/i.test(content)) {
          syncDisabled = true;
          findings.push(AuditFinding.fromRisk(
            this.registry.getRisk('SYNC_DISABLED'),
            file,
            { metadata: { reason: 'Sync explicitly disabled in code' } }
          ));
        }
      } catch (err) {
        // Skip
      }
    }

    if (usesPouchDB) {
      if (!hasConflictDetection) {
        findings.push(AuditFinding.fromRisk(
          this.registry.getRisk('NO_CONFLICT_DETECTION'),
          'Project-wide',
          {
            suggestion: 'Use db.get(id, { conflicts: true }) for critical reads',
            codeSnippet: `const doc = await db.get(docId, { conflicts: true });
if (doc._conflicts && doc._conflicts.length > 0) {
  // Handle conflicts
}`
          }
        ));
      }

      if (hasConflictDetection && !hasConflictResolution) {
        findings.push(AuditFinding.fromRisk(
          this.registry.getRisk('NO_CONFLICT_RESOLUTION'),
          'Project-wide',
          { suggestion: 'Implement conflict resolution strategy (merge, latest-wins, or prompt user)' }
        ));
      }

      if (!hasSyncErrorHandling) {
        findings.push(AuditFinding.fromRisk(
          this.registry.getRisk('NO_SYNC_ERROR_HANDLING'),
          'Project-wide',
          {
            suggestion: 'Add error handler to sync operations',
            codeSnippet: `db.sync(remoteDb, { live: true })
  .on('error', (err) => {
    console.error('Sync failed:', err);
    // Implement retry logic
  });`
          }
        ));
      }

      if (!hasRetryLogic && !syncDisabled) {
        findings.push(AuditFinding.fromRisk(
          this.registry.getRisk('NO_SYNC_RETRY'),
          'Project-wide',
          { suggestion: 'Implement exponential backoff retry for failed syncs' }
        ));
      }
    }

    return findings;
  }
}

module.exports = { PouchDBSyncDetector };
