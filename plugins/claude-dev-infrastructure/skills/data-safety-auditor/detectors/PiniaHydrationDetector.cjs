/**
 * PiniaHydrationDetector - Detects Pinia persistence and hydration risks
 */

const fs = require('fs');
const { AuditFinding } = require('../core/AuditFinding.cjs');
const { RiskRegistry } = require('../core/RiskRegistry.cjs');

class PiniaHydrationDetector {
  constructor() {
    this.registry = new RiskRegistry();
  }

  async detect(files, options = {}) {
    const findings = [];

    for (const file of files) {
      if (!file.includes('store') && !file.endsWith('.ts')) continue;

      try {
        const content = fs.readFileSync(file, 'utf8');

        if (!/defineStore/.test(content)) continue;

        findings.push(...this._analyzeStore(file, content));
      } catch (err) {
        // Skip
      }
    }

    return findings;
  }

  _analyzeStore(file, content) {
    const findings = [];

    const hasPersist = /persist:\s*true/.test(content);

    if (hasPersist) {
      // Check for hydration guard
      if (!/isHydrated|hydrationComplete|hydrated/.test(content)) {
        findings.push(AuditFinding.fromRisk(
          this.registry.getRisk('NO_HYDRATION_GUARD'),
          file,
          {
            suggestion: 'Add isHydrated ref, set true in afterRestore hook',
            codeSnippet: `const isHydrated = ref(false)
// In persist config:
afterRestore: () => { isHydrated.value = true }`
          }
        ));
      }

      // Check for afterRestore hook
      if (!/afterRestore/.test(content)) {
        findings.push(AuditFinding.fromRisk(
          this.registry.getRisk('MISSING_RESTORE_HOOK'),
          file,
          { suggestion: 'Add afterRestore hook to handle post-hydration setup' }
        ));
      }

      // Check for multiple persistence sources
      if (/localStorage\.(setItem|getItem)/.test(content)) {
        findings.push(AuditFinding.fromRisk(
          this.registry.getRisk('MULTIPLE_PERSISTENCE'),
          file,
          { suggestion: 'Remove manual localStorage calls, use only pinia-plugin-persistedstate' }
        ));
      }
    }

    // Check for onMounted fetch race with persist
    if (hasPersist && /onMounted.*fetch|onMounted.*axios/.test(content)) {
      findings.push(AuditFinding.fromRisk(
        this.registry.getRisk('HYDRATION_RACE'),
        file,
        { suggestion: 'Wait for isHydrated before fetching in onMounted' }
      ));
    }

    return findings;
  }
}

module.exports = { PiniaHydrationDetector };
