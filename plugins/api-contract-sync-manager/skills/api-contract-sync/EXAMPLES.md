# API Contract Sync Manager - Examples

Real-world usage scenarios and code samples for common API contract synchronization tasks.

## Example 1: Validating an OpenAPI Spec Against Express.js Routes

### Scenario
You have an Express.js backend with an OpenAPI spec, and you want to verify that all documented endpoints are actually implemented.

### OpenAPI Spec (`openapi.yaml`)
```yaml
openapi: 3.0.0
info:
  title: User API
  version: 1.0.0
paths:
  /api/users:
    get:
      summary: List users
      operationId: listUsers
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
    post:
      summary: Create user
      operationId: createUser
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: Created
  /api/users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Success
    delete:
      summary: Delete user
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: Deleted
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
        name:
          type: string
    CreateUserRequest:
      type: object
      required:
        - email
      properties:
        email:
          type: string
        name:
          type: string
```

### Express.js Implementation (`routes/users.js`)
```javascript
const express = require('express');
const router = express.Router();

// GET /api/users - List users
router.get('/users', async (req, res) => {
  const users = await db.users.findAll();
  res.json(users);
});

// POST /api/users - Create user
router.post('/users', async (req, res) => {
  const { email, name } = req.body;
  const user = await db.users.create({ email, name });
  res.status(201).json(user);
});

// GET /api/users/:id - Get user by ID
router.get('/users/:id', async (req, res) => {
  const user = await db.users.findById(req.params.id);
  if (!user) {
    return res.status(404).json({ error: 'User not found' });
  }
  res.json(user);
});

// Note: DELETE /api/users/:id is NOT implemented

module.exports = router;
```

### Usage
**User asks**: "Does our Express API implementation match the OpenAPI spec?"

**Analysis Process**:
1. Read and parse `openapi.yaml`
2. Extract endpoints:
   - GET /api/users
   - POST /api/users
   - GET /api/users/{id}
   - DELETE /api/users/{id}
3. Search for Express route handlers using Grep
4. Match implementations to spec

**Result Report**:
```
API Implementation Coverage Report
===================================

✓ GET /api/users - IMPLEMENTED
  File: routes/users.js:5
  
✓ POST /api/users - IMPLEMENTED
  File: routes/users.js:11
  
✓ GET /api/users/:id - IMPLEMENTED
  File: routes/users.js:18

✗ DELETE /api/users/:id - MISSING
  Documented in spec but not found in implementation
  Expected location: routes/users.js
  
Coverage: 75% (3/4 endpoints)

Recommendation:
Implement the missing DELETE endpoint or remove it from the spec if it's not needed.
```

---

## Example 2: Detecting Breaking Changes Between API Versions

### Scenario
You're preparing to release API v2 and need to identify all breaking changes from v1 to inform client teams.

### API v1 Spec
```yaml
paths:
  /api/users:
    post:
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required:
                - email
              properties:
                email:
                  type: string
                name:
                  type: string
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
        name:
          type: string
        phone:
          type: string
```

### API v2 Spec
```yaml
paths:
  /api/users:
    post:
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required:
                - email
                - role  # NEW: Required field added
              properties:
                email:
                  type: string
                name:
                  type: string
                role:
                  type: string
                  enum:
                    - admin
                    - member
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
        email:
          type: string
        name:
          type: string
        role:
          type: string
        # phone removed
```

### Usage
**User asks**: "Compare API v1 and v2 specs and tell me about breaking changes"

**Breaking Changes Detected**:
```
API v2.0 Breaking Changes Report
=================================

🔴 BREAKING CHANGES (2)

1. POST /api/users - Required field added
   Field: role
   Type: string (enum: admin, member)
   Impact: All existing POST /api/users requests will fail validation
   Migration: Add "role" field to request body

2. User schema - Property removed
   Property: phone
   Impact: Clients reading user.phone will get undefined
   Migration: Remove phone field usage or use alternative data source

⚠️ NON-BREAKING CHANGES (1)

1. User schema - Property added
   Property: role
   Type: string
   Impact: Safe - clients will simply ignore this new field

RECOMMENDATION: This requires a MAJOR version bump (v1 → v2)

Client Migration Required:
- Update all POST /api/users calls to include role field
- Remove dependencies on user.phone property
- Update TypeScript interfaces if using typed clients
```

**Generated Migration Guide**:
```markdown
# Migration Guide: API v1 → v2

## Breaking Changes

### 1. User Creation Requires Role
POST /api/users now requires a `role` field.

**Before (v1)**:
```json
{
  "email": "user@example.com",
  "name": "John Doe"
}
```

**After (v2)**:
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "role": "member"
}
```

**Action Required**: Update all user creation calls to include role.

### 2. User Phone Field Removed
The `phone` field has been removed from the User object.

**Before (v1)**:
```javascript
const phone = user.phone;
```

**After (v2)**:
```javascript
// phone field no longer available
// Use contact service API if phone is needed
```

**Action Required**: Remove code that depends on user.phone.

## Timeline
- **Now**: v1 and v2 both available
- **March 1, 2026**: v1 deprecated
- **June 1, 2026**: v1 removed

## Testing
Test your integration against v2 at: https://api-v2.example.com
```

---

## Example 3: Generating TypeScript Types from OpenAPI

### Scenario
Your frontend team needs TypeScript interfaces for a newly documented API.

### OpenAPI Spec
```yaml
components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - role
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
        role:
          type: string
          enum:
            - admin
            - member
            - guest
        createdAt:
          type: string
          format: date-time
        settings:
          $ref: '#/components/schemas/UserSettings'
    
    UserSettings:
      type: object
      properties:
        theme:
          type: string
          enum:
            - light
            - dark
        notifications:
          type: boolean
    
    CreateUserRequest:
      type: object
      required:
        - email
        - role
      properties:
        email:
          type: string
        name:
          type: string
        role:
          type: string
          enum:
            - admin
            - member
            - guest
    
    CreateUserResponse:
      type: object
      properties:
        user:
          $ref: '#/components/schemas/User'
        token:
          type: string
```

### Usage
**User asks**: "Generate TypeScript types from the OpenAPI spec"

### Generated TypeScript
```typescript
// Auto-generated from OpenAPI spec
// Do not edit manually

/**
 * User role enum
 */
export enum UserRole {
  Admin = 'admin',
  Member = 'member',
  Guest = 'guest'
}

/**
 * UI theme options
 */
export enum Theme {
  Light = 'light',
  Dark = 'dark'
}

/**
 * User settings configuration
 */
export interface UserSettings {
  theme?: Theme;
  notifications?: boolean;
}

/**
 * User entity
 */
export interface User {
  /** UUID identifier */
  id: string;
  
  /** User email address */
  email: string;
  
  /** Optional display name */
  name?: string;
  
  /** User role */
  role: UserRole;
  
  /** Account creation timestamp */
  createdAt?: Date;
  
  /** User preferences */
  settings?: UserSettings;
}

/**
 * Request body for creating a new user
 */
export interface CreateUserRequest {
  email: string;
  name?: string;
  role: UserRole;
}

/**
 * Response from user creation
 */
export interface CreateUserResponse {
  user?: User;
  token?: string;
}
```

**Additional Generation**: API Client Functions

```typescript
// API client with type safety
export class UserApiClient {
  constructor(private baseUrl: string) {}

  /**
   * Create a new user
   */
  async createUser(
    data: CreateUserRequest
  ): Promise<CreateUserResponse> {
    const response = await fetch(`${this.baseUrl}/api/users`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get user by ID
   */
  async getUser(id: string): Promise<User> {
    const response = await fetch(`${this.baseUrl}/api/users/${id}`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * List all users
   */
  async listUsers(): Promise<User[]> {
    const response = await fetch(`${this.baseUrl}/api/users`);

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response.json();
  }
}
```

---

## Example 4: Creating React Query Hooks from REST Endpoints

### Scenario
Generate React Query hooks for type-safe data fetching.

### OpenAPI Endpoints
```yaml
paths:
  /api/users/{id}:
    get:
      operationId: getUser
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
  
  /api/users:
    post:
      operationId: createUser
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
```

### Usage
**User asks**: "Generate React Query hooks from the API spec"

### Generated Hooks
```typescript
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

/**
 * Hook to fetch a user by ID
 * @param userId - User UUID
 */
export function useUser(userId: string) {
  return useQuery({
    queryKey: ['users', userId],
    queryFn: async () => {
      const response = await fetch(`/api/users/${userId}`);
      if (!response.ok) {
        throw new Error('Failed to fetch user');
      }
      return response.json() as Promise<User>;
    },
    enabled: !!userId, // Only fetch if userId is provided
  });
}

/**
 * Hook to create a new user
 */
export function useCreateUser() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (data: CreateUserRequest) => {
      const response = await fetch('/api/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Failed to create user');
      }

      return response.json() as Promise<User>;
    },
    onSuccess: (newUser) => {
      // Invalidate users list to refetch
      queryClient.invalidateQueries({ queryKey: ['users'] });
      
      // Optimistically update cache with new user
      queryClient.setQueryData(['users', newUser.id], newUser);
    },
  });
}

/**
 * Hook to list all users
 */
export function useUsers() {
  return useQuery({
    queryKey: ['users'],
    queryFn: async () => {
      const response = await fetch('/api/users');
      if (!response.ok) {
        throw new Error('Failed to fetch users');
      }
      return response.json() as Promise<User[]>;
    },
  });
}
```

### Usage in React Components
```typescript
// List users
function UserList() {
  const { data: users, isLoading, error } = useUsers();

  if (isLoading) return <div>Loading...</div>;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <ul>
      {users?.map(user => (
        <li key={user.id}>{user.name}</li>
      ))}
    </ul>
  );
}

// Get single user
function UserProfile({ userId }: { userId: string }) {
  const { data: user, isLoading } = useUser(userId);

  if (isLoading) return <div>Loading...</div>;
  if (!user) return <div>User not found</div>;

  return (
    <div>
      <h1>{user.name}</h1>
      <p>{user.email}</p>
      <p>Role: {user.role}</p>
    </div>
  );
}

// Create user
function CreateUserForm() {
  const createUser = useCreateUser();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      await createUser.mutateAsync({
        email: 'user@example.com',
        name: 'John Doe',
        role: UserRole.Member,
      });
      alert('User created!');
    } catch (error) {
      alert('Failed to create user');
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* form fields */}
      <button type="submit" disabled={createUser.isPending}>
        {createUser.isPending ? 'Creating...' : 'Create User'}
      </button>
    </form>
  );
}
```

---

## Example 5: GraphQL Schema Evolution Best Practices

### Scenario
Your GraphQL schema needs to evolve, and you want to ensure backward compatibility.

### Current Schema (v1)
```graphql
type User {
  id: ID!
  email: String!
  name: String!
  avatar: String
  createdAt: String!
}

type Query {
  user(id: ID!): User
  users: [User!]!
}

type Mutation {
  createUser(email: String!, name: String!): User!
}
```

### Proposed Schema (v2)
```graphql
scalar DateTime
scalar URL

type User {
  id: ID!
  email: String!
  # Deprecated: use 'displayName' instead
  name: String! @deprecated(reason: "Use 'displayName' for consistency")
  displayName: String!
  avatar: URL
  createdAt: DateTime!
  # New field (non-breaking)
  updatedAt: DateTime
}

input CreateUserInput {
  email: String!
  name: String!  # Keep for backward compatibility
  displayName: String  # New optional field
}

type Query {
  user(id: ID!): User
  # Enhanced with pagination (non-breaking)
  users(limit: Int = 10, offset: Int = 0): UserConnection!
}

type UserConnection {
  nodes: [User!]!
  totalCount: Int!
  pageInfo: PageInfo!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
}

type Mutation {
  # Updated to use input type (non-breaking if backward compatible)
  createUser(input: CreateUserInput!): User!
}
```

### Usage
**User asks**: "Review the GraphQL schema changes for breaking changes"

### Analysis Report
```
GraphQL Schema Evolution Analysis
==================================

✅ NON-BREAKING CHANGES (5)

1. Added new field: User.displayName
   - Type: String!
   - Impact: None - clients can ignore new fields
   
2. Added new field: User.updatedAt
   - Type: DateTime
   - Impact: None - optional field

3. Deprecated field: User.name
   - Reason: "Use 'displayName' for consistency"
   - Impact: None - field still available
   - Action: Clients should migrate to displayName over time

4. Enhanced Query.users with pagination
   - Added arguments: limit, offset
   - Changed return type: [User!]! → UserConnection!
   - Impact: POTENTIALLY BREAKING if not handled correctly
   - Mitigation: Keep old resolver temporarily

5. Added custom scalars
   - DateTime, URL
   - Impact: None - improved type safety

⚠️ POTENTIALLY BREAKING CHANGES (1)

1. Query.users return type changed
   - Old: [User!]!
   - New: UserConnection!
   - Risk: Existing queries expecting array will break
   
RECOMMENDATION: This change needs careful migration

Suggested Migration Strategy:
```graphql
type Query {
  # Keep old field for backward compatibility
  users: [User!]! @deprecated(reason: "Use usersConnection for pagination")
  
  # Add new field with different name
  usersConnection(limit: Int = 10, offset: Int = 0): UserConnection!
}
```

This allows gradual migration without breaking existing clients.
```

### Recommended Final Schema (v2 - Backward Compatible)
```graphql
scalar DateTime
scalar URL

type User {
  id: ID!
  email: String!
  name: String! @deprecated(reason: "Use 'displayName' for consistency")
  displayName: String!
  avatar: URL
  createdAt: DateTime!
  updatedAt: DateTime
}

input CreateUserInput {
  email: String!
  displayName: String!
}

type Query {
  user(id: ID!): User
  
  # Keep old version for backward compatibility
  users: [User!]! @deprecated(reason: "Use 'usersConnection' for pagination support")
  
  # Add new version with pagination
  usersConnection(limit: Int = 10, offset: Int = 0): UserConnection!
}

type UserConnection {
  nodes: [User!]!
  totalCount: Int!
  pageInfo: PageInfo!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
}

type Mutation {
  createUser(input: CreateUserInput!): User!
}
```

**Migration Timeline**:
```
Phase 1 (Now): Deploy v2 with both old and new fields
- users (deprecated) → returns [User!]!
- usersConnection (new) → returns UserConnection!

Phase 2 (3 months): Monitor usage
- Track which clients still use deprecated fields
- Contact teams to migrate

Phase 3 (6 months): Remove deprecated fields
- Remove users query
- Remove User.name field
- Only usersConnection and displayName remain
```

---

## Example 6: Finding Undocumented Endpoints

### Scenario
You suspect some endpoints are implemented but not documented in the OpenAPI spec.

### OpenAPI Spec
```yaml
paths:
  /api/users:
    get:
      summary: List users
  /api/users/{id}:
    get:
      summary: Get user
```

### Actual Implementation
```javascript
// routes/users.js
router.get('/users', listUsers);
router.get('/users/:id', getUser);
router.post('/users', createUser);  // Not in spec!
router.delete('/users/:id', deleteUser);  // Not in spec!

// routes/admin.js
router.get('/admin/stats', getStats);  // Not in spec!
router.post('/admin/reset', resetDatabase);  // Not in spec!
```

### Usage
**User asks**: "Find any API endpoints that exist in code but aren't documented"

### Analysis Process
1. Parse OpenAPI spec → extract documented endpoints
2. Search codebase for route definitions (Grep for Express patterns)
3. Compare and identify undocumented routes

### Result Report
```
Undocumented Endpoints Report
==============================

Found 4 implemented endpoints not in OpenAPI spec:

1. POST /api/users
   File: routes/users.js:15
   Handler: createUser
   Status: PRODUCTION (likely intentional)
   Recommendation: Add to OpenAPI spec with proper schema

2. DELETE /api/users/:id
   File: routes/users.js:23
   Handler: deleteUser
   Status: PRODUCTION (likely intentional)
   Recommendation: Add to OpenAPI spec

3. GET /admin/stats
   File: routes/admin.js:8
   Handler: getStats
   Status: INTERNAL (admin only)
   Recommendation: Consider separate internal API spec or document with security note

4. POST /admin/reset
   File: routes/admin.js:18
   Handler: resetDatabase
   Status: DANGEROUS (database reset)
   Recommendation: Remove from production or add strict authorization

SUMMARY:
- 2 documented endpoints (50% coverage)
- 4 undocumented endpoints (50% missing)

Next Steps:
1. Add POST /users and DELETE /users/:id to public spec
2. Create separate admin-api.yaml for internal endpoints
3. Secure or remove dangerous /admin/reset endpoint
```

---

## Summary

These examples demonstrate how the API Contract Sync Manager skill helps with:

1. **Validation** - Ensuring specs match implementations
2. **Change Detection** - Identifying breaking vs. non-breaking changes
3. **Code Generation** - Creating type-safe clients and hooks
4. **Evolution** - Managing schema changes over time
5. **Coverage** - Finding undocumented or unimplemented endpoints

The skill adapts to your specific tech stack (Express, FastAPI, GraphQL, etc.) and provides actionable insights for maintaining healthy API contracts.

