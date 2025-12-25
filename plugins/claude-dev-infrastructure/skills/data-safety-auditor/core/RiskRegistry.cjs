/**
 * Risk Registry - Defines all data safety risks with severity, impact, and detection methods
 *
 * Categories:
 * - A: Browser-specific (IndexedDB quota, Safari ITP, private mode)
 * - B: Storage-specific (LocalForage race conditions)
 * - C: Sync patterns (PouchDB conflicts, network failures)
 * - D: Vue/Pinia risks (hydration races, persistence)
 * - E: Data integrity (checksums, corruption, backups)
 * - F: Testing coverage
 */

const SEVERITY_LEVELS = {
  CRITICAL: {
    level: 1,
    label: 'CRITICAL',
    color: '\x1b[31m',
    blocksDeployment: true,
    description: 'Immediate data loss risk - MUST fix before deployment'
  },
  HIGH: {
    level: 2,
    label: 'HIGH',
    color: '\x1b[33m',
    blocksDeployment: false,
    description: 'Likely data loss under certain conditions'
  },
  MEDIUM: {
    level: 3,
    label: 'MEDIUM',
    color: '\x1b[36m',
    blocksDeployment: false,
    description: 'Potential data integrity issues'
  },
  LOW: {
    level: 4,
    label: 'LOW',
    color: '\x1b[37m',
    blocksDeployment: false,
    description: 'Minor risk or missing best practice'
  }
};

const RISKS = {
  // === SECTION A: Browser-Specific ===
  QUOTA_EXCEEDED: {
    id: 'QUOTA_EXCEEDED',
    severity: 'CRITICAL',
    category: 'indexeddb',
    title: 'Storage Quota Exceeded',
    description: 'Storage quota exceeded - data cannot be saved',
    impact: 'User data silently lost when storage is full',
    detection: 'QuotaExceededError thrown or storage >95%',
    remediation: 'Implement quota monitoring, graceful degradation',
    pattern: /localforage\.setItem|localStorage\.setItem|indexedDB/
  },

  UNHANDLED_QUOTA_ERROR: {
    id: 'UNHANDLED_QUOTA_ERROR',
    severity: 'CRITICAL',
    category: 'indexeddb',
    title: 'Unhandled QuotaExceededError',
    description: 'QuotaExceededError not caught in storage operations',
    impact: 'App crashes when storage is full',
    detection: 'Storage write without try/catch',
    remediation: 'Wrap storage writes in try/catch, check error.name',
    pattern: /await\s+(localforage|db)\.setItem/
  },

  NO_QUOTA_MONITORING: {
    id: 'NO_QUOTA_MONITORING',
    severity: 'HIGH',
    category: 'indexeddb',
    title: 'No Storage Quota Monitoring',
    description: 'Storage quota not monitored',
    impact: 'Users surprised by sudden data loss',
    detection: 'No navigator.storage.estimate() calls',
    remediation: 'Add quota monitoring: warn at 80%, critical at 95%',
    pattern: /navigator\.storage\.estimate/
  },

  NO_PERSISTENT_STORAGE: {
    id: 'NO_PERSISTENT_STORAGE',
    severity: 'HIGH',
    category: 'indexeddb',
    title: 'Persistent Storage Not Requested',
    description: 'Not requesting persistent storage',
    impact: 'Browser may evict data under pressure',
    detection: 'No navigator.storage.persist() call',
    remediation: 'Call navigator.storage.persist() on init',
    pattern: /navigator\.storage\.persist/
  },

  SAFARI_ITP_EXPIRATION: {
    id: 'SAFARI_ITP_EXPIRATION',
    severity: 'CRITICAL',
    category: 'indexeddb',
    title: 'Safari ITP 7-Day Expiration',
    description: 'Safari ITP 7-day storage expiration not handled',
    impact: 'ALL data deleted after 7 days on Safari',
    detection: 'No forced sync within 7 days on Safari',
    remediation: 'Implement 3-day forced server sync',
    pattern: /safari|webkit/i
  },

  NO_SAFARI_DETECTION: {
    id: 'NO_SAFARI_DETECTION',
    severity: 'CRITICAL',
    category: 'indexeddb',
    title: 'No Safari Browser Detection',
    description: 'Safari not detected for ITP mitigations',
    impact: 'Safari-specific data loss unhandled',
    detection: 'No userAgent Safari check with IndexedDB',
    remediation: 'Add Safari detection and ITP mitigations',
    pattern: /navigator\.userAgent.*safari/i
  },

  NO_PRIVATE_MODE_DETECTION: {
    id: 'NO_PRIVATE_MODE_DETECTION',
    severity: 'MEDIUM',
    category: 'indexeddb',
    title: 'Private Mode Not Detected',
    description: 'Private browsing mode not detected',
    impact: 'User unaware data lost on browser close',
    detection: 'IndexedDB used without private mode check',
    remediation: 'Detect private mode, warn user',
    pattern: /private|incognito/i
  },

  STORAGE_PARTITIONING: {
    id: 'STORAGE_PARTITIONING',
    severity: 'MEDIUM',
    category: 'indexeddb',
    title: 'Storage Partitioning Not Handled',
    description: 'Third-party storage partitioning not handled',
    impact: 'Data isolated in iframe contexts',
    detection: 'IndexedDB used but no iframe check',
    remediation: 'Detect iframe, require server sync',
    pattern: /window\.parent|frameElement/
  },

  // === SECTION B: LocalForage ===
  RACE_CONDITION_SAME_KEY: {
    id: 'RACE_CONDITION_SAME_KEY',
    severity: 'HIGH',
    category: 'localforage',
    title: 'Race Condition on Same Key',
    description: 'Concurrent writes to same key',
    impact: 'Last write wins - earlier data lost',
    detection: 'getItem then setItem without lock',
    remediation: 'Implement write queue or mutex',
    pattern: /getItem.*setItem|setItem.*setItem/s
  },

  NON_ATOMIC_UPDATE: {
    id: 'NON_ATOMIC_UPDATE',
    severity: 'HIGH',
    category: 'localforage',
    title: 'Non-Atomic Multi-Item Update',
    description: 'Multiple items updated without atomicity',
    impact: 'Partial persistence possible',
    detection: 'Multiple setItem without transaction',
    remediation: 'Use single key or transaction pattern',
    pattern: /setItem.*setItem/s
  },

  UNHANDLED_STORAGE_ERROR: {
    id: 'UNHANDLED_STORAGE_ERROR',
    severity: 'MEDIUM',
    category: 'localforage',
    title: 'Unhandled Storage Error',
    description: 'LocalForage operations without error handling',
    impact: 'App may crash on storage failure',
    detection: 'localforage calls without try/catch',
    remediation: 'Wrap all storage operations in try/catch',
    pattern: /localforage\.(setItem|getItem)/
  },

  DRIVER_NOT_VALIDATED: {
    id: 'DRIVER_NOT_VALIDATED',
    severity: 'MEDIUM',
    category: 'localforage',
    title: 'LocalForage Driver Not Validated',
    description: 'No check for active driver',
    impact: 'Slow fallback driver may timeout',
    detection: 'No localforage.driver() check',
    remediation: 'Check driver after ready(), warn if not IndexedDB',
    pattern: /localforage\.driver|localforage\.ready/
  },

  LOCALFORAGE_NOT_CONFIGURED: {
    id: 'LOCALFORAGE_NOT_CONFIGURED',
    severity: 'MEDIUM',
    category: 'localforage',
    title: 'LocalForage Not Configured',
    description: 'Using default configuration',
    impact: 'Database name conflicts possible',
    detection: 'No localforage.config() call',
    remediation: 'Call localforage.config({ name, storeName })',
    pattern: /localforage\.config/
  },

  // === SECTION C: PouchDB/Sync ===
  NO_CONFLICT_DETECTION: {
    id: 'NO_CONFLICT_DETECTION',
    severity: 'HIGH',
    category: 'pouchdb',
    title: 'No Conflict Detection',
    description: 'PouchDB conflicts not detected',
    impact: 'Conflicting changes silently lost',
    detection: 'No { conflicts: true } in gets',
    remediation: 'Check _conflicts on critical reads',
    pattern: /conflicts:\s*true/
  },

  NO_CONFLICT_RESOLUTION: {
    id: 'NO_CONFLICT_RESOLUTION',
    severity: 'CRITICAL',
    category: 'pouchdb',
    title: 'No Conflict Resolution Strategy',
    description: 'Conflicts detected but not resolved',
    impact: 'Conflicts accumulate, data degrades',
    detection: 'Conflict detection but no resolution',
    remediation: 'Implement merge/latest-wins resolution',
    pattern: /_conflicts|resolveConflict/
  },

  NO_SYNC_ERROR_HANDLING: {
    id: 'NO_SYNC_ERROR_HANDLING',
    severity: 'HIGH',
    category: 'pouchdb',
    title: 'No Sync Error Handling',
    description: 'Replication without error handler',
    impact: 'Network failures cause silent sync failures',
    detection: 'replicate/sync without error callback',
    remediation: 'Add .on("error") handler',
    pattern: /\.(replicate|sync)\(/
  },

  INCOMPLETE_SYNC_UNDETECTED: {
    id: 'INCOMPLETE_SYNC_UNDETECTED',
    severity: 'HIGH',
    category: 'pouchdb',
    title: 'Incomplete Sync Not Detected',
    description: 'No detection of interrupted sync',
    impact: 'User believes data synced when stranded',
    detection: 'No pending document tracking',
    remediation: 'Track lastSuccessfulSync, detect stranded docs',
    pattern: /lastSuccessfulSync|pendingSync/
  },

  NO_SYNC_RETRY: {
    id: 'NO_SYNC_RETRY',
    severity: 'MEDIUM',
    category: 'pouchdb',
    title: 'No Sync Retry Logic',
    description: 'Failed sync not retried',
    impact: 'Single glitch causes permanent data stranding',
    detection: 'No retry pattern after sync failure',
    remediation: 'Implement exponential backoff retry',
    pattern: /retry|backoff/
  },

  SYNC_DISABLED: {
    id: 'SYNC_DISABLED',
    severity: 'CRITICAL',
    category: 'pouchdb',
    title: 'Sync Disabled',
    description: 'Database sync is disabled',
    impact: 'Local-only data, no backup, no cross-device',
    detection: 'Sync explicitly disabled in config',
    remediation: 'Enable sync or implement alternative backup',
    pattern: /sync.*disabled|disabled.*sync/i
  },

  // === SECTION D: Pinia/Vue ===
  HYDRATION_RACE: {
    id: 'HYDRATION_RACE',
    severity: 'HIGH',
    category: 'pinia',
    title: 'Hydration Race Condition',
    description: 'Component renders before hydration completes',
    impact: 'UI shows stale data, actions may overwrite',
    detection: 'onMounted fetch without hydration guard',
    remediation: 'Add isHydrated flag, await before render',
    pattern: /isHydrated|hydrationComplete/
  },

  NO_HYDRATION_GUARD: {
    id: 'NO_HYDRATION_GUARD',
    severity: 'HIGH',
    category: 'pinia',
    title: 'No Hydration Guard',
    description: 'Persist enabled but no isHydrated flag',
    impact: 'Components render before state loaded',
    detection: 'persist: true without isHydrated',
    remediation: 'Add isHydrated ref, set in afterRestore',
    pattern: /persist:\s*true/
  },

  MISSING_RESTORE_HOOK: {
    id: 'MISSING_RESTORE_HOOK',
    severity: 'MEDIUM',
    category: 'pinia',
    title: 'Missing afterRestore Hook',
    description: 'Persist without afterRestore hook',
    impact: 'Object references may break',
    detection: 'pinia-plugin-persistedstate without hooks',
    remediation: 'Add afterRestore hook',
    pattern: /afterRestore|beforeRestore/
  },

  MULTIPLE_PERSISTENCE: {
    id: 'MULTIPLE_PERSISTENCE',
    severity: 'MEDIUM',
    category: 'pinia',
    title: 'Multiple Persistence Sources',
    description: 'Using plugin AND manual storage',
    impact: 'Data can desync between sources',
    detection: 'persist: true AND localStorage.setItem',
    remediation: 'Use single persistence source',
    pattern: /persist.*localStorage|localStorage.*persist/s
  },

  // === SECTION E: Data Integrity ===
  NO_SCHEMA_VALIDATION: {
    id: 'NO_SCHEMA_VALIDATION',
    severity: 'HIGH',
    category: 'integrity',
    title: 'No Schema Validation',
    description: 'Data loaded without schema validation',
    impact: 'Corrupted data breaks app',
    detection: 'Data loaded without validation',
    remediation: 'Validate against schema, migrate if needed',
    pattern: /validateSchema|zod|yup|ajv/
  },

  NO_CHECKSUM: {
    id: 'NO_CHECKSUM',
    severity: 'MEDIUM',
    category: 'integrity',
    title: 'No Checksum Verification',
    description: 'Data integrity not verified',
    impact: 'Silent corruption undetected',
    detection: 'No hash comparison on load',
    remediation: 'Store and verify checksums',
    pattern: /checksum|hash|sha256/i
  },

  NO_BACKUP_STRATEGY: {
    id: 'NO_BACKUP_STRATEGY',
    severity: 'MEDIUM',
    category: 'integrity',
    title: 'No Backup Strategy',
    description: 'No backup capability',
    impact: 'Unrecoverable data loss possible',
    detection: 'No backup/export functionality',
    remediation: 'Implement periodic backup + export',
    pattern: /exportBackup|createBackup/
  },

  EMPTY_CANVAS_DATA: {
    id: 'EMPTY_CANVAS_DATA',
    severity: 'CRITICAL',
    category: 'integrity',
    title: 'Empty Canvas Data',
    description: 'Canvas layout data is empty',
    impact: 'All task positions lost',
    detection: 'canvas:data has empty nodes/sections',
    remediation: 'Restore from backup or rebuild',
    pattern: null
  },

  DATA_MISMATCH: {
    id: 'DATA_MISMATCH',
    severity: 'CRITICAL',
    category: 'integrity',
    title: 'Local/Remote Data Mismatch',
    description: 'Local and remote data differ significantly',
    impact: 'Data may be lost on sync',
    detection: 'Document counts differ >10%',
    remediation: 'Review and merge differences',
    pattern: null
  },

  // === SECTION F: Testing ===
  NO_PERSISTENCE_TESTS: {
    id: 'NO_PERSISTENCE_TESTS',
    severity: 'MEDIUM',
    category: 'testing',
    title: 'No Persistence Tests',
    description: 'No tests for data persistence',
    impact: 'Persistence bugs found in production',
    detection: 'No tests with page reload + data check',
    remediation: 'Add E2E persistence tests',
    pattern: /reload.*expect.*data|persist.*test/i
  },

  NO_QUOTA_TESTS: {
    id: 'NO_QUOTA_TESTS',
    severity: 'MEDIUM',
    category: 'testing',
    title: 'No Quota Failure Tests',
    description: 'No tests for QuotaExceededError',
    impact: 'Unknown behavior when full',
    detection: 'No tests mocking quota error',
    remediation: 'Add quota failure test',
    pattern: /QuotaExceededError|mock.*quota/i
  },

  NO_OFFLINE_TESTS: {
    id: 'NO_OFFLINE_TESTS',
    severity: 'MEDIUM',
    category: 'testing',
    title: 'No Offline Tests',
    description: 'No tests for offline behavior',
    impact: 'Unknown sync behavior offline',
    detection: 'Uses sync but no offline test',
    remediation: 'Add offline sync recovery test',
    pattern: /offline.*test|network.*fail/i
  },

  NO_CONFLICT_TESTS: {
    id: 'NO_CONFLICT_TESTS',
    severity: 'HIGH',
    category: 'testing',
    title: 'No Conflict Tests',
    description: 'No conflict resolution tests',
    impact: 'Conflict handling untested',
    detection: 'Uses PouchDB but no conflict test',
    remediation: 'Add conflict scenario test',
    pattern: /conflict.*test/i
  }
};

class SeverityMatrix {
  constructor() {
    this.levels = SEVERITY_LEVELS;
  }

  blocksDeployment(severity) {
    return this.levels[severity]?.blocksDeployment ?? false;
  }

  compare(a, b) {
    return (this.levels[a]?.level ?? 99) - (this.levels[b]?.level ?? 99);
  }

  getColor(severity) {
    return this.levels[severity]?.color ?? '\x1b[0m';
  }

  get resetColor() {
    return '\x1b[0m';
  }
}

class RiskRegistry {
  constructor() {
    this.risks = RISKS;
    this.severityMatrix = new SeverityMatrix();
  }

  getRisk(riskId) {
    return this.risks[riskId] ?? null;
  }

  getAllRisks() {
    return Object.values(this.risks);
  }

  getRisksByCategory(category) {
    return Object.values(this.risks).filter(r => r.category === category);
  }

  getRisksBySeverity(severity) {
    return Object.values(this.risks).filter(r => r.severity === severity);
  }

  getBlockingRisks() {
    return Object.values(this.risks).filter(r =>
      this.severityMatrix.blocksDeployment(r.severity)
    );
  }

  getCategories() {
    return [...new Set(Object.values(this.risks).map(r => r.category))];
  }

  getCountBySeverity() {
    const counts = { CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 };
    Object.values(this.risks).forEach(r => {
      counts[r.severity] = (counts[r.severity] || 0) + 1;
    });
    return counts;
  }
}

module.exports = { RiskRegistry, SeverityMatrix, RISKS, SEVERITY_LEVELS };
