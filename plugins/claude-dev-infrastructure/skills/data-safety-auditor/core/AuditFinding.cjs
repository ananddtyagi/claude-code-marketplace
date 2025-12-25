/**
 * AuditFinding - Represents a single data safety issue found during audit
 */

class AuditFinding {
  constructor(riskId, severity, location, options = {}) {
    this.riskId = riskId;
    this.severity = severity;
    this.location = location; // file:line:column or description
    this.timestamp = new Date().toISOString();

    // Optional fields
    this.title = options.title || riskId;
    this.description = options.description || '';
    this.impact = options.impact || '';
    this.suggestion = options.suggestion || '';
    this.codeSnippet = options.codeSnippet || null;
    this.testCase = options.testCase || null;
    this.category = options.category || 'unknown';
    this.autoFixable = options.autoFixable || false;
    this.metadata = options.metadata || {};
  }

  /**
   * Create finding from risk definition
   */
  static fromRisk(risk, location, options = {}) {
    return new AuditFinding(risk.id, risk.severity, location, {
      title: risk.title,
      description: risk.description,
      impact: risk.impact,
      suggestion: risk.remediation,
      category: risk.category,
      ...options
    });
  }

  /**
   * Check if this finding blocks deployment
   */
  blocksDeployment() {
    return this.severity === 'CRITICAL';
  }

  /**
   * Get severity level (1-4, lower is worse)
   */
  getSeverityLevel() {
    const levels = { CRITICAL: 1, HIGH: 2, MEDIUM: 3, LOW: 4 };
    return levels[this.severity] ?? 99;
  }

  /**
   * Format for console output
   */
  toConsoleString(colors = true) {
    const severityColors = {
      CRITICAL: '\x1b[31m',
      HIGH: '\x1b[33m',
      MEDIUM: '\x1b[36m',
      LOW: '\x1b[37m'
    };
    const reset = '\x1b[0m';
    const color = colors ? (severityColors[this.severity] || '') : '';
    const r = colors ? reset : '';

    let output = `${color}[${this.severity}]${r} ${this.title}\n`;
    output += `  Location: ${this.location}\n`;
    if (this.description) output += `  Issue: ${this.description}\n`;
    if (this.impact) output += `  Impact: ${this.impact}\n`;
    if (this.suggestion) output += `  Fix: ${this.suggestion}\n`;
    if (this.codeSnippet) output += `  Code: ${this.codeSnippet.substring(0, 100)}...\n`;

    return output;
  }

  /**
   * Format for JSON output
   */
  toJSON() {
    return {
      riskId: this.riskId,
      severity: this.severity,
      location: this.location,
      title: this.title,
      description: this.description,
      impact: this.impact,
      suggestion: this.suggestion,
      category: this.category,
      codeSnippet: this.codeSnippet,
      testCase: this.testCase,
      autoFixable: this.autoFixable,
      timestamp: this.timestamp,
      metadata: this.metadata
    };
  }

  /**
   * Format for markdown output
   */
  toMarkdown() {
    let md = `### ${this.severity}: ${this.title}\n\n`;
    md += `**Location:** \`${this.location}\`\n\n`;
    if (this.description) md += `**Issue:** ${this.description}\n\n`;
    if (this.impact) md += `**Impact:** ${this.impact}\n\n`;
    if (this.suggestion) md += `**Fix:** ${this.suggestion}\n\n`;
    if (this.codeSnippet) {
      md += `**Code:**\n\`\`\`javascript\n${this.codeSnippet}\n\`\`\`\n\n`;
    }
    if (this.testCase) {
      md += `**Test Case:**\n\`\`\`javascript\n${this.testCase}\n\`\`\`\n\n`;
    }
    return md;
  }
}

/**
 * Collection of findings with aggregation methods
 */
class FindingsCollection {
  constructor(findings = []) {
    this.findings = findings;
  }

  add(finding) {
    this.findings.push(finding);
    return this;
  }

  addAll(findings) {
    this.findings.push(...findings);
    return this;
  }

  /**
   * Get all findings
   */
  all() {
    return this.findings;
  }

  /**
   * Get count
   */
  count() {
    return this.findings.length;
  }

  /**
   * Check if any findings exist
   */
  hasFindings() {
    return this.findings.length > 0;
  }

  /**
   * Check if any blockers exist
   */
  hasBlockers() {
    return this.findings.some(f => f.blocksDeployment());
  }

  /**
   * Get blockers only
   */
  getBlockers() {
    return this.findings.filter(f => f.blocksDeployment());
  }

  /**
   * Filter by severity
   */
  bySeverity(severity) {
    return this.findings.filter(f => f.severity === severity);
  }

  /**
   * Filter by category
   */
  byCategory(category) {
    return this.findings.filter(f => f.category === category);
  }

  /**
   * Sort by severity (critical first)
   */
  sortBySeverity() {
    return [...this.findings].sort((a, b) =>
      a.getSeverityLevel() - b.getSeverityLevel()
    );
  }

  /**
   * Group by severity
   */
  groupBySeverity() {
    return {
      CRITICAL: this.bySeverity('CRITICAL'),
      HIGH: this.bySeverity('HIGH'),
      MEDIUM: this.bySeverity('MEDIUM'),
      LOW: this.bySeverity('LOW')
    };
  }

  /**
   * Group by category
   */
  groupByCategory() {
    const groups = {};
    this.findings.forEach(f => {
      if (!groups[f.category]) groups[f.category] = [];
      groups[f.category].push(f);
    });
    return groups;
  }

  /**
   * Get summary statistics
   */
  getSummary() {
    const bySeverity = this.groupBySeverity();
    return {
      total: this.findings.length,
      critical: bySeverity.CRITICAL.length,
      high: bySeverity.HIGH.length,
      medium: bySeverity.MEDIUM.length,
      low: bySeverity.LOW.length,
      blockers: this.getBlockers().length,
      categories: Object.keys(this.groupByCategory())
    };
  }
}

module.exports = { AuditFinding, FindingsCollection };
