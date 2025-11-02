# API Contract Sync Manager

> Validate and synchronize API contracts with implementation, detect breaking changes, and generate client code

## Overview

The API Contract Sync Manager is a comprehensive skill for Claude Code that helps you maintain alignment between API specifications (OpenAPI/Swagger, GraphQL) and their implementations. It automates validation, detects breaking changes, generates type-safe client code, and ensures your API documentation stays synchronized with your codebase.

## Key Features

### 🔍 **Spec Validation**
- Validate OpenAPI 3.0/3.1 and GraphQL schemas
- Check for syntax errors and structural issues
- Verify completeness (descriptions, examples, security)
- Identify common anti-patterns and suggest improvements

### 🔄 **Implementation Matching**
- Cross-reference API specs with actual route handlers
- Support for Express.js, FastAPI, Django, Spring Boot, and more
- Identify documented but unimplemented endpoints
- Find implemented but undocumented endpoints
- Generate coverage reports

### 🚨 **Breaking Change Detection**
- Compare API spec versions automatically
- Categorize changes as breaking vs. non-breaking
- Generate detailed migration guides
- Suggest versioning strategies
- Prevent accidental breaking changes in PRs

### 💻 **Client Code Generation**
- Generate TypeScript interfaces from OpenAPI/GraphQL schemas
- Create type-safe API client functions
- Generate React Query/SWR hooks for data fetching
- Export Zod/Yup validation schemas
- Support for custom code generation templates

### 📊 **Coverage Analysis**
- Calculate API documentation coverage percentage
- Identify gaps in specification or implementation
- Track API health metrics over time
- Prioritize documentation improvements

### 📝 **Migration Guides**
- Automatically generate upgrade guides for API versions
- Include before/after code examples
- Highlight impact and required actions
- Provide deprecation timelines

## Use Cases

### For Backend Developers
- Ensure all endpoints are properly documented
- Validate OpenAPI/GraphQL schemas before deployment
- Catch breaking changes before they reach production
- Maintain consistent API patterns across services

### For Frontend Developers
- Generate type-safe TypeScript interfaces
- Create React Query hooks from API specs
- Stay informed about API changes
- Reduce manual type definition work

### For API Product Managers
- Track API evolution and breaking changes
- Ensure backward compatibility
- Plan deprecation strategies
- Maintain API governance standards

### For DevOps/Platform Teams
- Automate API validation in CI/CD pipelines
- Enforce API design standards
- Monitor API contract health
- Prevent spec drift in production

## Installation

### Via Plugin Marketplace

1. Open Claude Code
2. Navigate to Plugin Settings
3. Search for "API Contract Sync Manager"
4. Click "Install"

### Manual Installation

1. Clone or download this plugin
2. Copy the `api-contract-sync-manager` directory to your Claude plugins folder:
   ```bash
   cp -r api-contract-sync-manager ~/.claude/plugins/
   ```
3. Restart Claude Code

## Usage

The skill activates automatically when Claude detects API-related work. You can also explicitly request help:

### Validate a Spec
```
"Validate the OpenAPI spec in openapi.yaml"
```

### Check Implementation Match
```
"Does our API implementation match the spec?"
```

### Detect Breaking Changes
```
"Compare api-v1.yaml and api-v2.yaml for breaking changes"
```

### Generate TypeScript Types
```
"Generate TypeScript types from the OpenAPI spec"
```

### Generate React Query Hooks
```
"Create React Query hooks from our API endpoints"
```

### Find Coverage Gaps
```
"What API endpoints are missing from our documentation?"
```

## Supported Technologies

### API Specifications
- ✅ OpenAPI 3.0
- ✅ OpenAPI 3.1
- ✅ Swagger 2.0
- ✅ GraphQL SDL (Schema Definition Language)

### Backend Frameworks
- ✅ Express.js (Node.js)
- ✅ FastAPI (Python)
- ✅ Django REST Framework (Python)
- ✅ Flask (Python)
- ✅ Spring Boot (Java)
- ✅ ASP.NET Core (C#)
- ✅ GraphQL (Apollo, Yoga, etc.)

### Frontend Frameworks
- ✅ React (with React Query, SWR)
- ✅ Vue.js
- ✅ Angular
- ✅ Svelte
- ✅ TypeScript (all frameworks)

## Examples

### Example 1: Validate OpenAPI Spec

**Input**: OpenAPI spec with potential issues

**Command**: "Validate the OpenAPI spec"

**Output**:
```
OpenAPI Validation Report
=========================

✓ Valid OpenAPI 3.0.0 structure
✓ All $ref references resolved

Issues Found (3):

1. Line 45: Missing description for POST /api/users
   Recommendation: Add operation description

2. Line 78: No examples provided for User schema
   Recommendation: Add example for better documentation

3. Line 102: Security requirement missing for DELETE operations
   Recommendation: Add security scheme (e.g., bearerAuth)
```

### Example 2: Breaking Change Detection

**Input**: Two versions of an API spec

**Command**: "Compare v1 and v2 specs"

**Output**:
```
Breaking Changes Report
=======================

🔴 BREAKING CHANGES (2):

1. POST /api/users - Required field added
   New required field: "role"
   Impact: Existing requests without role will fail

2. User schema - Property removed
   Removed property: "phone"
   Impact: Clients accessing user.phone will break

Recommendation: Major version bump required (v1 → v2)
```

### Example 3: Generate TypeScript Types

**Input**: OpenAPI spec with User schema

**Command**: "Generate TypeScript types"

**Output**:
```typescript
// Auto-generated from OpenAPI spec

export interface User {
  id: string;
  email: string;
  name?: string;
  role: UserRole;
  createdAt: Date;
}

export enum UserRole {
  Admin = 'admin',
  Member = 'member',
  Guest = 'guest'
}

export interface CreateUserRequest {
  email: string;
  name?: string;
  role: UserRole;
}
```

## Configuration

No configuration required! The skill works out-of-the-box with sensible defaults.

### Optional: Validation Tools

For enhanced validation, you can install these tools:

```bash
# OpenAPI validation
npm install -g @stoplight/spectral-cli

# GraphQL validation
npm install -g @graphql-inspector/cli

# OpenAPI diffing
npm install -g openapi-diff
```

The skill will automatically use these tools if available, but they're not required.

## Documentation

- **[SKILL.md](skills/api-contract-sync/SKILL.md)** - Complete skill instructions and capabilities
- **[REFERENCE.md](skills/api-contract-sync/REFERENCE.md)** - Technical reference for OpenAPI and GraphQL
- **[EXAMPLES.md](skills/api-contract-sync/EXAMPLES.md)** - Real-world usage examples

## Best Practices

### 1. **Validate Early and Often**
Run validation in your CI/CD pipeline to catch issues before they reach production.

### 2. **Version Your APIs**
Use semantic versioning for your API specs and bump major versions for breaking changes.

### 3. **Automate Code Generation**
Generate client code from specs as part of your build process to ensure type safety.

### 4. **Review Breaking Changes**
Always run breaking change detection before releasing new API versions.

### 5. **Maintain Documentation**
Keep your API specs in version control alongside your code and update them with every change.

### 6. **Use TypeScript**
Take advantage of generated TypeScript types for compile-time safety in your frontend.

## Troubleshooting

### Skill Not Activating

**Issue**: Claude doesn't use the skill when working with API files.

**Solution**: 
- Ensure your API spec files have standard extensions (`.yaml`, `.json`, `.graphql`)
- Mention "API", "OpenAPI", or "GraphQL" explicitly in your request
- Restart Claude Code to reload skills

### Validation Errors

**Issue**: Spec validation fails with cryptic errors.

**Solution**:
- Check YAML/JSON syntax with a linter
- Verify OpenAPI version in spec matches validator version
- Look at the line numbers provided in error messages

### Missing Routes in Implementation Match

**Issue**: Routes are implemented but not detected.

**Solution**:
- Ensure routes follow standard framework patterns
- Check if routes are in separate files that need to be searched
- Verify path parameter format matches (`{id}` in spec, `:id` in Express)

## Contributing

Found a bug or want to suggest an improvement? Please open an issue or submit a pull request!

## Version History

### v1.0.0 (2025-10-16)
- Initial release
- OpenAPI 3.0/3.1 support
- GraphQL support
- Breaking change detection
- TypeScript code generation
- React Query hook generation
- Implementation matching for popular frameworks

## License

MIT License - see LICENSE file for details

## Support

For questions or issues:
- Open an issue in the marketplace repository
- Consult the [documentation](skills/api-contract-sync/)
- Ask Claude directly when using the skill

---

**Made with ❤️ for the Claude Code community**

