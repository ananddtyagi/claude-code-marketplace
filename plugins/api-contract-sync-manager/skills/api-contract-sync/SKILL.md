---
name: API Contract Sync Manager
description: Validate OpenAPI, Swagger, and GraphQL schemas match backend implementation. Detect breaking changes, generate TypeScript clients, and ensure API documentation stays synchronized. Use when working with API spec files (.yaml, .json, .graphql), reviewing API changes, generating frontend types, or validating endpoint implementations.
allowed-tools: Read, Grep, Glob, RunTerminalCmd
---

# API Contract Sync Manager

Maintain synchronization between API specifications and their implementations, detect breaking changes, and generate client code to ensure contracts stay reliable across frontend and backend teams.

## When to Use This Skill

Use this skill when:
- Working with OpenAPI/Swagger specification files (`.yaml`, `.json`)
- Managing GraphQL schemas (`.graphql`, `.gql`)
- Reviewing API changes in pull requests
- Generating TypeScript types or client code from specs
- Validating that implementations match documented APIs
- Detecting breaking vs. non-breaking API changes
- Creating API versioning strategies
- Onboarding new developers to an API-driven codebase

## Core Capabilities

### 1. Spec Validation

Validate API specification files for correctness and completeness:

**OpenAPI/Swagger Validation**:
- Check schema syntax and structure
- Validate against OpenAPI 3.0/3.1 standards
- Ensure all endpoints have proper descriptions
- Verify request/response schemas are complete
- Check for required security definitions
- Validate parameter types and constraints

**GraphQL Validation**:
- Parse and validate SDL (Schema Definition Language)
- Check for schema stitching issues
- Validate resolver coverage
- Detect circular dependencies
- Verify input/output type consistency

**Validation Approach**:
1. Read the spec file using the Read tool
2. Parse the structure (YAML/JSON for OpenAPI, SDL for GraphQL)
3. Check for common issues:
   - Missing required fields
   - Invalid references (`$ref`)
   - Inconsistent naming conventions
   - Missing examples or descriptions
   - Security scheme gaps
4. Report findings with line numbers and suggestions

### 2. Implementation Matching

Cross-reference API specifications with actual code implementations:

**For REST APIs**:
1. Extract all endpoints from OpenAPI spec (paths, methods)
2. Search codebase for route definitions:
   - Express.js: `app.get()`, `router.post()`, etc.
   - FastAPI: `@app.get()`, `@router.post()`
   - Django: `path()`, `urlpatterns`
   - Spring Boot: `@GetMapping`, `@PostMapping`
3. Compare spec endpoints against implemented routes
4. Flag discrepancies:
   - Documented but not implemented
   - Implemented but not documented
   - Parameter mismatches
   - Response type differences

**For GraphQL**:
1. Extract types, queries, mutations from schema
2. Search for resolver implementations
3. Verify all schema fields have resolvers
4. Check resolver signatures match schema types

**Implementation Matching Steps**:
```
1. Parse spec → extract endpoints/operations
2. Use Grep to find route handlers in codebase
3. Compare and categorize:
   - ✓ Matched: spec and implementation align
   - ⚠ Drift: partial match with differences
   - ✗ Missing: documented but not implemented
   - ⚠ Undocumented: implemented but not in spec
4. Generate coverage report
```

### 3. Breaking Change Detection

Compare two versions of an API spec to detect breaking vs. non-breaking changes:

**Breaking Changes** (require version bump):
- Removed endpoints or operations
- Removed required request parameters
- Changed parameter types (e.g., string → number)
- Made optional parameters required
- Removed response properties that clients depend on
- Changed response status codes
- Renamed endpoints, parameters, or fields
- Stricter validation rules (e.g., regex patterns)

**Non-Breaking Changes** (safe to deploy):
- Added new endpoints
- Added optional parameters
- Made required parameters optional
- Added new response properties
- Expanded enum values
- Improved descriptions/examples
- Added deprecation warnings

**Change Detection Process**:
1. Read both spec versions (old and new)
2. Compare schemas field by field
3. Categorize each change as breaking or non-breaking
4. Generate migration guide with:
   - Summary of breaking changes
   - Impact on existing clients
   - Required client updates
   - Recommended versioning strategy

### 4. Client Code Generation

Generate type-safe client code from API specifications:

**TypeScript Interfaces**:
```typescript
// From OpenAPI schema
interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: Date;
}

interface CreateUserRequest {
  email: string;
  name?: string;
}

interface CreateUserResponse {
  user: User;
  token: string;
}
```

**API Client Functions**:
```typescript
// HTTP client with proper typing
async function createUser(
  data: CreateUserRequest
): Promise<CreateUserResponse> {
  const response = await fetch('/api/users', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  return response.json();
}
```

**React Query Hooks**:
```typescript
// Auto-generated hooks for data fetching
function useUser(userId: string) {
  return useQuery(['user', userId], () => 
    fetch(`/api/users/${userId}`).then(r => r.json())
  );
}

function useCreateUser() {
  return useMutation((data: CreateUserRequest) =>
    fetch('/api/users', {
      method: 'POST',
      body: JSON.stringify(data)
    }).then(r => r.json())
  );
}
```

**Generation Steps**:
1. Parse OpenAPI/GraphQL schema
2. Extract all data models (schemas, types)
3. Generate TypeScript interfaces with proper types
4. Create client functions for each endpoint
5. Optionally generate hooks for React Query/SWR
6. Add JSDoc comments from spec descriptions

### 5. Coverage Analysis

Identify gaps between documentation and implementation:

**Analysis Report Structure**:
```
API Coverage Report
==================

Documented Endpoints: 45
Implemented Endpoints: 42
Coverage: 93%

Missing Implementations:
- DELETE /api/users/{id} (documented but not found)
- POST /api/users/{id}/suspend (documented but not found)

Undocumented Endpoints:
- GET /api/internal/health (found in code, not in spec)
- POST /api/debug/reset (found in code, not in spec)

Mismatched Signatures:
- POST /api/users
  Spec expects: { email, name, role }
  Code accepts: { email, name } (missing 'role')
```

**Coverage Analysis Process**:
1. Run implementation matching (see section 2)
2. Calculate coverage percentage
3. List all discrepancies with file locations
4. Prioritize issues by severity
5. Suggest next steps to achieve 100% coverage

### 6. Migration Guides

Create upgrade guides when API versions change:

**Migration Guide Template**:
```markdown
# API v2.0 Migration Guide

## Breaking Changes

### 1. User Creation Endpoint
**Change**: Required `role` field added to POST /api/users
**Impact**: All user creation calls will fail without this field
**Action Required**:
- Update all POST /api/users calls to include `role`
- Default to 'member' if no specific role needed

Before:
```json
{ "email": "user@example.com", "name": "John" }
```

After:
```json
{ "email": "user@example.com", "name": "John", "role": "member" }
```

### 2. Authentication Token Format
**Change**: JWT tokens now use RS256 instead of HS256
**Impact**: Token validation must be updated
**Action Required**:
- Update JWT verification libraries
- Fetch new public key from /.well-known/jwks.json
```

**Guide Generation Steps**:
1. Detect all breaking changes (see section 3)
2. Group changes by endpoint or feature
3. For each change, document:
   - What changed and why
   - Impact on existing clients
   - Required code updates with before/after examples
   - Timeline for deprecation
4. Add general upgrade instructions

## Best Practices

### For OpenAPI Specs
1. **Use $ref liberally**: Define schemas once, reference everywhere
2. **Version your APIs**: Use `/v1/`, `/v2/` prefixes or version headers
3. **Add examples**: Include request/response examples in spec
4. **Document errors**: Define all possible error responses
5. **Security first**: Always specify security requirements

### For GraphQL Schemas
1. **Use descriptions**: Document all types, fields, and arguments
2. **Deprecate, don't remove**: Use `@deprecated` directive
3. **Input validation**: Use custom scalars for validated types
4. **Pagination patterns**: Use connection/edge patterns consistently
5. **Error handling**: Define custom error types

### For Breaking Changes
1. **Version bump**: Major version for breaking changes
2. **Deprecation period**: Maintain old version for transition
3. **Clear communication**: Document changes prominently
4. **Backward compatibility**: Provide adapters when possible
5. **Client coordination**: Ensure clients can update before removal

## Common Workflows

### Workflow 1: Validate Existing Spec
```
1. User: "Validate the OpenAPI spec"
2. Read the spec file (usually openapi.yaml or swagger.json)
3. Parse and validate structure
4. Report any issues with suggestions
```

### Workflow 2: Check Implementation Match
```
1. User: "Does our API implementation match the spec?"
2. Read spec file
3. Extract all endpoints
4. Search codebase for route handlers
5. Compare and generate coverage report
```

### Workflow 3: Detect Breaking Changes
```
1. User: "Compare API v1 and v2 specs"
2. Read both spec files
3. Diff schemas systematically
4. Categorize changes as breaking/non-breaking
5. Generate migration guide
```

### Workflow 4: Generate TypeScript Types
```
1. User: "Generate TypeScript types from the API spec"
2. Read OpenAPI/GraphQL schema
3. Extract all data models
4. Generate TypeScript interfaces
5. Create client functions or hooks if requested
```

### Workflow 5: Find Coverage Gaps
```
1. User: "What endpoints are missing in our spec?"
2. Run implementation matching
3. Identify undocumented endpoints
4. Suggest adding them to spec with proper schemas
```

## Tools and Commands

### Validation Tools
When validation tools are available, use them:
- **OpenAPI**: `npx @stoplight/spectral-cli lint openapi.yaml`
- **GraphQL**: `npx graphql-inspector validate schema.graphql`

### Comparison Tools
For advanced diff analysis:
- **OpenAPI**: `npx openapi-diff old.yaml new.yaml`
- **GraphQL**: `npx graphql-inspector diff old.graphql new.graphql`

### Code Generation
Recommend these tools for automated generation:
- **openapi-typescript**: Generate TypeScript from OpenAPI
- **graphql-code-generator**: Generate TypeScript from GraphQL
- **orval**: Generate React Query hooks from OpenAPI

## Error Handling

When encountering issues:

**Invalid Spec File**:
- Report specific syntax errors with line numbers
- Suggest corrections based on spec version
- Provide valid example structure

**Missing Implementation**:
- List file locations where handlers should exist
- Suggest framework-specific code to implement
- Estimate implementation effort

**Type Mismatches**:
- Show expected vs. actual types clearly
- Explain impact of the mismatch
- Suggest type coercion or spec updates

## Additional Resources

For more detailed information on specific topics, see:
- [REFERENCE.md](REFERENCE.md) - Technical details on OpenAPI and GraphQL structures
- [EXAMPLES.md](EXAMPLES.md) - Real-world usage scenarios and code samples

## Requirements

This skill works best with:
- API spec files in the codebase
- Structured routing in backend code
- TypeScript for type generation (optional but recommended)

No additional packages are required for basic validation and comparison. Advanced features may suggest installing validation tools via npm.

