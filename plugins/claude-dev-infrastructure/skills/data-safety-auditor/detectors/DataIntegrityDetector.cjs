/**
 * DataIntegrityDetector - Detects data integrity and backup risks
 */

const fs = require('fs');
const { AuditFinding } = require('../core/AuditFinding.cjs');
const { RiskRegistry } = require('../core/RiskRegistry.cjs');

class DataIntegrityDetector {
  constructor() {
    this.registry = new RiskRegistry();
  }

  async detect(files, options = {}) {
    const findings = [];
    let hasSchemaValidation = false;
    let hasChecksum = false;
    let hasBackupStrategy = false;
    let loadsData = false;

    for (const file of files) {
      try {
        const content = fs.readFileSync(file, 'utf8');

        if (/getItem|\.get\(|\.allDocs/.test(content)) {
          loadsData = true;
        }

        // More precise schema validation - actual validation libraries or explicit validation functions
        if (/validateSchema|validateTask|validateData|zod\.|yup\.|ajv\.|Joi\.|z\.object|schema\.validate/i.test(content)) {
          hasSchemaValidation = true;
        }

        if (/checksum|hash|sha256|md5|integrity/i.test(content)) {
          hasChecksum = true;
        }

        if (/backup|export.*data|download.*json/i.test(content)) {
          hasBackupStrategy = true;
        }
      } catch (err) {
        // Skip
      }
    }

    if (loadsData && !hasSchemaValidation) {
      findings.push(AuditFinding.fromRisk(
        this.registry.getRisk('NO_SCHEMA_VALIDATION'),
        'Project-wide',
        {
          suggestion: 'Validate data after loading from storage',
          codeSnippet: `function validateTask(data) {
  return data &&
    typeof data.id === 'string' &&
    typeof data.title === 'string' &&
    ['planned', 'in_progress', 'done'].includes(data.status);
}`
        }
      ));
    }

    if (loadsData && !hasChecksum) {
      findings.push(AuditFinding.fromRisk(
        this.registry.getRisk('NO_CHECKSUM'),
        'Project-wide',
        { suggestion: 'Store checksums for critical data to detect corruption' }
      ));
    }

    if (!hasBackupStrategy) {
      findings.push(AuditFinding.fromRisk(
        this.registry.getRisk('NO_BACKUP_STRATEGY'),
        'Project-wide',
        {
          suggestion: 'Implement data export feature for user backups',
          codeSnippet: `function exportBackup() {
  const data = { tasks, projects, settings };
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  // Trigger download
}`
        }
      ));
    }

    return findings;
  }

  /**
   * Check live database state for integrity issues
   */
  async checkDatabaseIntegrity(dbState) {
    const findings = [];

    // Check for empty canvas with tasks
    if (dbState.canvasNodes === 0 && dbState.totalTasks > 0) {
      findings.push(AuditFinding.fromRisk(
        this.registry.getRisk('EMPTY_CANVAS_DATA'),
        'canvas:data',
        {
          metadata: {
            canvasNodes: 0,
            totalTasks: dbState.totalTasks,
            recommendation: 'Tasks exist but canvas layout is empty. Drag tasks from inbox to canvas.'
          }
        }
      ));
    }

    // Check for local/remote mismatch
    if (dbState.localCount !== undefined && dbState.remoteCount !== undefined) {
      const diff = Math.abs(dbState.localCount - dbState.remoteCount);
      if (diff > 0) {
        const percentDiff = (diff / Math.max(dbState.localCount, dbState.remoteCount)) * 100;
        if (percentDiff > 10) {
          findings.push(AuditFinding.fromRisk(
            this.registry.getRisk('DATA_MISMATCH'),
            'Database',
            {
              metadata: {
                localCount: dbState.localCount,
                remoteCount: dbState.remoteCount,
                difference: diff,
                percentDiff: percentDiff.toFixed(1) + '%'
              }
            }
          ));
        }
      }
    }

    return findings;
  }
}

module.exports = { DataIntegrityDetector };
