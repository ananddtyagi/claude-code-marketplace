---
name: data-safety-auditor
emoji: "🛡️"
description: Comprehensive data safety auditor for Vue 3 + Pinia + IndexedDB + PouchDB applications. Detects data loss risks, sync issues, race conditions, and browser-specific vulnerabilities with actionable remediation guidance.
triggers:
  - "audit data safety"
  - "check data loss risks"
  - "data safety auditor"
  - "activate data-safety-auditor"
keywords:
  - data safety
  - data loss
  - IndexedDB
  - LocalForage
  - PouchDB
  - CouchDB
  - sync
  - persistence
  - Safari ITP
  - quota
  - backup
  - integrity
activation_count: 0
last_used: null
related_skills:
  - indexeddb-backup-debugger
  - comprehensive-system-analyzer
  - qa-testing
  - couchdb-cross-device-sync
---

# Data Safety Auditor

**Purpose**: Comprehensive audit tool that identifies data loss risks in Vue 3 + Pinia + IndexedDB + PouchDB applications with actionable remediation guidance.

## Philosophy

This skill provides **rigorous data safety analysis** with:
- **Zero tolerance for data loss** - Identifies every potential failure point
- **Complete coverage** - Storage, sync, hydration, integrity, testing
- **Evidence-based findings** - Code locations, patterns, severity
- **Actionable fixes** - Specific remediation with code examples
- **Test generation** - Creates missing safety tests

## What It Detects

### CRITICAL Risks (Deployment Blockers)
- `QUOTA_EXCEEDED` - Storage full, data can't save
- `SAFARI_ITP_EXPIRATION` - 7-day data loss on Safari
- `UNHANDLED_QUOTA_ERROR` - QuotaExceededError not caught
- `NO_CONFLICT_RESOLUTION` - PouchDB conflicts not handled
- `NON_ATOMIC_UPDATES` - Multi-item updates can partially fail

### HIGH Risks (Must Fix)
- `HYDRATION_RACE_CONDITION` - Pinia data loads after render
- `NO_SYNC_ERROR_HANDLING` - Sync failures silently fail
- `INCOMPLETE_SYNC_UNDETECTED` - Stranded data not detected
- `RACE_CONDITION_SAME_KEY` - Concurrent LocalForage writes
- `UNHANDLED_STORAGE_ERROR` - Storage calls have no try/catch

### MEDIUM Risks (Should Fix)
- `NO_CHECKSUM_VERIFICATION` - Data corruption undetected
- `NO_PRIVATE_MODE_HANDLING` - Private mode data loss unhandled
- `NO_PERSISTENT_STORAGE_REQUEST` - PWA not requesting persist
- `STORAGE_PARTITIONING_UNACCOUNTED` - iframe storage isolated
- `DRIVER_VALIDATION_MISSING` - LocalForage driver not checked

### LOW Risks (Consider Fixing)
- `NO_PERSISTENCE_TESTS` - Missing persistence test coverage
- `NO_OFFLINE_TESTS` - Offline sync not tested
- `MISSING_SAFARI_TESTS` - Safari-specific tests missing

## Detection Categories

### A. Browser-Specific Data Loss Vectors
- Storage quota limits and eviction policies per browser
- Safari ITP 7-day storage limitations
- Private/incognito mode behavior
- Storage partitioning impacts

### B. Storage-Specific Patterns
- LocalForage race conditions
- Concurrent write conflicts
- Driver fallback behavior
- Configuration issues

### C. Sync Patterns
- PouchDB/CouchDB conflict detection
- Network failure handling
- Incomplete sync detection
- Sync integrity verification

### D. Vue/Pinia Risks
- Hydration race conditions
- beforeRestore/afterRestore hooks
- Object reference breakage
- Multiple persistence sources

### E. Data Integrity Checks
- Schema validation on load
- Checksum verification
- Corruption detection
- Backup/recovery validation

### F. Testing & Compliance
- Persistence test coverage
- Quota failure tests
- OWASP compliance
- GDPR data integrity

## Usage

```javascript
const auditor = new DataSafetyAuditor();

// Full project audit
const report = await auditor.auditVueApp('./src');
console.log(report.toConsole());

// Targeted audits
const quotaFindings = await auditor.checkQuotaRisks(codeAST);
const itpFindings = await auditor.checkSafariCompat(codeAST);
const piniaFindings = await auditor.checkPiniaPersistence(piniaStore);
const syncFindings = await auditor.checkSyncIntegrity(pouchdbCode);

// Generate missing tests
const tests = await auditor.generateTestSuite();

// Get detailed remediation
const fixes = await auditor.suggestRemediations(findings);
```

## Report Formats

- **Console** - Colored, readable CLI output with severity indicators
- **JSON** - Machine-readable for CI/CD integration
- **Markdown** - Documentation and reports
- **HTML** - Interactive dashboard view

## Deployment Gate

The auditor enforces deployment gates:
- **CRITICAL findings** = Deployment blocked
- **HIGH findings** = Warning, recommend fixing
- **MEDIUM/LOW** = Information only

## When to Use

Use this skill when:
- Before deploying to production
- After adding new persistence features
- When debugging data loss issues
- During code review of storage code
- Setting up CI/CD quality gates
- Auditing third-party storage libraries

## Integration

### CI/CD Pipeline
```javascript
const report = await auditor.auditVueApp('./src');
if (report.hasBlockers()) {
  console.error('DEPLOYMENT BLOCKED: Critical data safety issues found');
  process.exit(1);
}
```

### Custom Rules
```javascript
auditor.rules.addRule('MUST_USE_ENCRYPTION', (code) => {
  if (code.includes('sensitive_data') && !code.includes('crypto.subtle')) {
    return { severity: 'CRITICAL', msg: 'Sensitive data must be encrypted' };
  }
});
```

---

## MANDATORY USER VERIFICATION REQUIREMENT

### Policy: No Safety Claims Without User Confirmation

**CRITICAL**: Before claiming ANY data safety issue is "fixed", "resolved", or "safe", the following verification protocol is MANDATORY:

#### Step 1: Technical Verification
- Run full audit with all detectors
- Verify no CRITICAL or HIGH findings
- Take screenshots/evidence of clean audit

#### Step 2: User Verification Request
**REQUIRED**: Use the `AskUserQuestion` tool to explicitly ask the user to verify:

```
"I've completed the data safety audit. Before confirming your app is safe, please verify:
1. [Specific storage operations to test]
2. [Sync scenarios to test]
3. [Browser-specific tests to run]

Please confirm the data persists correctly, or let me know what's failing."
```

#### Step 3: Wait for User Confirmation
- **DO NOT** claim app is "data safe" until user confirms
- **DO NOT** approve deployment without user verification
- **DO NOT** skip any CRITICAL finding verification

**Remember: The user is the final authority on data safety. No exceptions.**
