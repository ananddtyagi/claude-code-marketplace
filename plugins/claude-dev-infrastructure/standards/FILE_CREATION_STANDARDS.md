# 📋 Claude Code File Creation Standards

**Mandatory standards for all Claude Code instances creating files in the Pomo-Flow project**

**Last Updated**: November 25, 2025
**Version**: 1.0
**Purpose**: Prevent root directory clutter and ensure organized file placement

---

## 🚨 **CRITICAL RULE: No Root Directory File Creation**

**ABSOLUTELY FORBIDDEN**: Creating any files in the project root directory (`/`) except for:
- `README.md` (project overview)
- `package.json` (dependencies)
- `package-lock.json` (lock file)
- `.gitignore` (git exclusions)
- `tsconfig.json` (TypeScript config)
- `vite.config.ts` (Vite config)
- `index.html` (entry point)

**ALL OTHER FILES MUST BE CREATED IN PROPER ORGANIZED LOCATIONS**

---

## 📁 **Mandatory File Path Standards**

### **Verification & Fix Reports**
```
docs/reports/verification/{YYYY-MM-DD}/filename.md
docs/reports/fixes/{YYYY-MM-DD}/filename.md
docs/reports/analysis/{YYYY-MM-DD}/filename.md
```

**Examples:**
- ✅ `docs/reports/verification/2025-11-25/vue-mount-fix-success.md`
- ✅ `docs/reports/fixes/2025-11-25/duplicate-function-resolution.md`
- ❌ `vue-mount-fix-success.md` (FORBIDDEN - root directory)

### **Emergency & Crisis Documentation**
```
docs/emergency/{YYYY-MM-DD}/filename.md
docs/crisis/{YYYY-MM-DD}/filename.md
```

**Examples:**
- ✅ `docs/emergency/2025-11-25/critical-failure-recovery.md`
- ✅ `docs/crisis/2025-11-25/system-outage-report.md`

### **Test Artifacts & Debug Files**
```
tests/artifacts/{type}/{YYYY-MM-DD}/filename.ext
tests/debug/{category}/{YYYY-MM-DD}/filename.ext
```

**Examples:**
- ✅ `tests/artifacts/screenshots/2025-11-25/canvas-test-1.png`
- ✅ `tests/debug/console/2025-11-25/error-logs.txt`

### **Technical Documentation**
```
docs/technical/{category}/filename.md
docs/api/{version}/filename.md
docs/architecture/{component}/filename.md
```

**Examples:**
- ✅ `docs/technical/state-management/pinia-stores.md`
- ✅ `docs/architecture/canvas/vue-flow-integration.md`

### **Configuration Files**
```
config/{category}/filename.ext
.claude/config/{purpose}/filename.ext
```

**Examples:**
- ✅ `config/testing/playwright.config.js`
- ✅ `.claude/config/skill-rules.json`

---

## 🔧 **Implementation Requirements for Claude Code Skills**

### **1. Use Smart File Path Resolver**
```javascript
// REQUIRED: Import the file path resolver
const { getSmartPath } = require('../../scripts/file-path-resolver.cjs');

// FOR VERIFICATION REPORTS:
const reportPath = getSmartPath('verification', 'vue-mount-fix-success.md');
// Result: docs/reports/verification/2025-11-25/vue-mount-fix-success.md

// FOR FIX DOCUMENTATION:
const fixPath = getSmartPath('fixes', 'duplicate-function-resolution.md');
// Result: docs/reports/fixes/2025-11-25/duplicate-function-resolution.md
```

### **2. Never Use Hardcoded Root Paths**
```javascript
// ❌ FORBIDDEN:
const filePath = path.join(this.projectRoot, 'fix-report.md');

// ✅ REQUIRED:
const filePath = getSmartPath('verification', 'fix-report.md');
```

### **3. Validate Before File Creation**
```javascript
// REQUIRED: Validate file path before creation
const { validateFilePath } = require('../../scripts/file-creation-validator.cjs');

if (!validateFilePath(filePath)) {
  throw new Error(`Invalid file path: ${filePath}. Use getSmartPath() instead.`);
}

// Then create the file
fs.writeFileSync(filePath, content);
```

---

## 🛠️ **File Type Classification System**

### **Verification Files** (`getSmartPath('verification', 'filename.md')`)
- Fix success reports
- Bug verification documentation
- Test completion reports
- Feature validation results

### **Fix Files** (`getSmartPath('fixes', 'filename.md')`)
- Bug fix documentation
- Issue resolution reports
- Problem-solving procedures
- Code change summaries

### **Analysis Files** (`getSmartPath('analysis', 'filename.md')`)
- System analysis results
- Performance reports
- Code review findings
- Architecture assessments

### **Emergency Files** (`getSmartPath('emergency', 'filename.md')`)
- Crisis response procedures
- Emergency recovery steps
- Critical failure reports
- System outage documentation

---

## 📋 **File Naming Conventions**

### **Use Descriptive, Action-Oriented Names**
```
✅ GOOD:
- vue-mount-fix-success.md
- duplicate-function-resolution.md
- canvas-performance-optimization.md
- timer-state-synchronization-fix.md

❌ AVOID:
- temp.md
- report.md
- fix.md
- debug.log
```

### **Include Date in File Path (Automatic)**
The `getSmartPath()` function automatically includes the date, so filenames don't need dates:
- ✅ `docs/reports/verification/2025-11-25/vue-mount-fix-success.md`
- ❌ `docs/reports/verification/2025-11-25/vue-mount-fix-success-2025-11-25.md`

### **Use Kebab-Case for Filenames**
- ✅ `canvas-drag-drop-fix.md`
- ✅ `timer-integration-improvements.md`
- ❌ `CanvasDragDropFix.md`
- ❌ `Timer Integration Improvements.md`

---

## ⚡ **Quick Reference for Common File Types**

```javascript
const { getSmartPath } = require('../../scripts/file-path-resolver.cjs');

// Verification Reports
const verificationPath = getSmartPath('verification', 'feature-name-verification.md');

// Fix Documentation
const fixPath = getSmartPath('fixes', 'issue-name-fix.md');

// Analysis Reports
const analysisPath = getSmartPath('analysis', 'system-component-analysis.md');

// Emergency Documentation
const emergencyPath = getSmartPath('emergency', 'critical-incident-report.md');

// Test Artifacts
const testArtifactPath = getSmartPath('test-artifacts', 'screenshot.png');

// Debug Files
const debugPath = getSmartPath('debug', 'error-log.txt');
```

---

## 🚨 **Enforcement & Violation Handling**

### **Automatic Violation Detection**
The file creation validator will:
1. **Reject** any attempt to create files in root directory
2. **Log** violations with stack traces for debugging
3. **Suggest** correct file paths using smart resolver
4. **Prevent** file creation until compliant

### **Common Violations & Solutions**

| Violation | Problem | Solution |
|-----------|---------|----------|
| `path.join(this.projectRoot, 'report.md')` | Root directory creation | Use `getSmartPath('verification', 'report.md')` |
| `fs.writeFileSync('fix.md', ...)` | Hardcoded root path | Use `getSmartPath('fixes', 'fix.md')` |
| Creating temp files in root | Temporary file clutter | Use `getSmartPath('debug', 'temp-file.log')` |

---

## ✅ **Compliance Checklist**

Before creating any file, Claude Code MUST:

- [ ] **NEVER** create files in root directory (except essential config files)
- [ ] **ALWAYS** use `getSmartPath()` for determining file locations
- [ ] **ALWAYS** validate file paths with `validateFilePath()`
- [ ] **USE** descriptive, kebab-case filenames
- [ ] **FOLLOW** file type classification system
- [ ] **INCLUDE** proper file extensions (.md, .txt, .log, .png)

---

**Violation Consequences:**
- 🚫 **File creation blocked**
- 📝 **Violation logged**
- 🔧 **Correct path suggested**
- ⚠️ **Developer notified**

**Goal: Zero root directory file creation from Claude Code skills while maintaining organized, discoverable documentation structure.**

---

**Last Updated**: November 25, 2025
**Next Review**: January 1, 2026
**Status**: ✅ Active Enforcement