# API Contract Sync Manager - Technical Reference

This document provides technical details for working with OpenAPI and GraphQL specifications, including structure, breaking change patterns, and validation strategies.

## OpenAPI Specification Structure

### OpenAPI 3.0/3.1 Schema

```yaml
openapi: 3.0.0
info:
  title: API Name
  version: 1.0.0
  description: API description
servers:
  - url: https://api.example.com/v1
paths:
  /users:
    get:
      summary: List users
      operationId: listUsers
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/User'
components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
      properties:
        id:
          type: string
          format: uuid
        email:
          type: string
          format: email
        name:
          type: string
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
```

### Key OpenAPI Fields

**info**: Metadata about the API
- `title`: API name
- `version`: Semantic version
- `description`: Overview of API purpose

**servers**: Base URLs for API
- `url`: Full base URL
- `description`: Environment name (optional)

**paths**: API endpoints
- Key is the path (e.g., `/users`, `/users/{id}`)
- Operations: `get`, `post`, `put`, `patch`, `delete`

**components**: Reusable definitions
- `schemas`: Data models
- `parameters`: Reusable parameters
- `responses`: Reusable responses
- `securitySchemes`: Auth methods

### OpenAPI Data Types

| Type | Format | Description | Example |
|------|--------|-------------|---------|
| string | - | Text | "hello" |
| string | date | ISO 8601 date | "2025-10-16" |
| string | date-time | ISO 8601 timestamp | "2025-10-16T10:30:00Z" |
| string | email | Email address | "user@example.com" |
| string | uuid | UUID v4 | "123e4567-e89b..." |
| integer | int32 | 32-bit integer | 42 |
| integer | int64 | 64-bit integer | 9007199254740991 |
| number | float | Floating point | 3.14 |
| number | double | Double precision | 3.141592653589793 |
| boolean | - | True/false | true |
| array | - | List of items | [1, 2, 3] |
| object | - | Key-value pairs | {"key": "value"} |

### OpenAPI References

Use `$ref` to avoid duplication:

```yaml
# Define once
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string

# Reference multiple times
paths:
  /users/{id}:
    get:
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
  /users:
    post:
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User'
```

## GraphQL Schema Structure

### GraphQL SDL (Schema Definition Language)

```graphql
# Scalar types
scalar DateTime
scalar Email

# Enum types
enum UserRole {
  ADMIN
  MEMBER
  GUEST
}

# Object types
type User {
  id: ID!
  email: Email!
  name: String
  role: UserRole!
  createdAt: DateTime!
  posts: [Post!]!
}

type Post {
  id: ID!
  title: String!
  content: String!
  author: User!
  published: Boolean!
}

# Input types (for mutations)
input CreateUserInput {
  email: Email!
  name: String
  role: UserRole = MEMBER
}

# Query operations
type Query {
  user(id: ID!): User
  users(limit: Int = 10, offset: Int = 0): [User!]!
  posts(authorId: ID): [Post!]!
}

# Mutation operations
type Mutation {
  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!
}

# Subscription operations
type Subscription {
  userCreated: User!
  postPublished: Post!
}
```

### GraphQL Type Modifiers

| Modifier | Meaning | Example |
|----------|---------|---------|
| `Type` | Nullable | Can be `User` or `null` |
| `Type!` | Non-null | Must be `User`, never `null` |
| `[Type]` | Nullable list of nullable items | `[User]`, `null`, or `[User, null]` |
| `[Type]!` | Non-null list of nullable items | `[User]` or `[User, null]` but never `null` |
| `[Type!]` | Nullable list of non-null items | `[User]` or `null`, never `[User, null]` |
| `[Type!]!` | Non-null list of non-null items | `[User]`, never `null` or `[User, null]` |

### GraphQL Directives

```graphql
type User {
  id: ID!
  email: String!
  oldEmail: String @deprecated(reason: "Use 'email' field instead")
  internalId: String @internal
}

type Query {
  users: [User!]! @auth(requires: ADMIN)
}
```

Common directives:
- `@deprecated`: Mark field as deprecated
- `@auth`, `@requires`: Custom authorization
- `@skip`, `@include`: Conditional inclusion (query-side)

## Breaking Change Patterns

### OpenAPI Breaking Changes

#### 1. Removed Endpoints
```yaml
# Before
paths:
  /users/{id}:
    delete:
      # ...

# After
paths:
  # /users/{id} delete operation removed
```
**Impact**: Clients calling DELETE /users/{id} will get 404

#### 2. Required Parameters Added
```yaml
# Before
parameters:
  - name: email
    in: query
    required: false

# After
parameters:
  - name: email
    in: query
    required: true  # Changed to required
```
**Impact**: Existing calls without `email` parameter will fail validation

#### 3. Parameter Type Changed
```yaml
# Before
parameters:
  - name: limit
    in: query
    schema:
      type: string

# After
parameters:
  - name: limit
    in: query
    schema:
      type: integer  # Changed from string
```
**Impact**: Clients sending "10" as string may fail validation

#### 4. Required Property Added to Request
```yaml
# Before
CreateUserRequest:
  type: object
  required:
    - email
  properties:
    email:
      type: string

# After
CreateUserRequest:
  type: object
  required:
    - email
    - role  # New required field
  properties:
    email:
      type: string
    role:
      type: string
```
**Impact**: Requests without `role` field will be rejected

#### 5. Response Property Removed
```yaml
# Before
User:
  properties:
    id:
      type: string
    email:
      type: string
    phone:
      type: string

# After
User:
  properties:
    id:
      type: string
    email:
      type: string
    # phone removed
```
**Impact**: Clients accessing `user.phone` will get undefined/null

#### 6. Property Type Changed
```yaml
# Before
User:
  properties:
    id:
      type: string

# After
User:
  properties:
    id:
      type: integer  # Changed type
```
**Impact**: Type mismatches in strongly-typed clients

#### 7. Enum Values Removed
```yaml
# Before
UserRole:
  type: string
  enum:
    - admin
    - member
    - guest

# After
UserRole:
  type: string
  enum:
    - admin
    - member
    # guest removed
```
**Impact**: Requests with `role: "guest"` will fail validation

### GraphQL Breaking Changes

#### 1. Field Removed from Type
```graphql
# Before
type User {
  id: ID!
  email: String!
  phone: String
}

# After
type User {
  id: ID!
  email: String!
  # phone removed
}
```
**Impact**: Queries requesting `phone` field will fail

#### 2. Argument Added to Field
```graphql
# Before
type Query {
  users: [User!]!
}

# After
type Query {
  users(role: UserRole!): [User!]!  # New required argument
}
```
**Impact**: Existing queries without `role` argument will fail

#### 3. Non-Null Modifier Added
```graphql
# Before
type User {
  email: String
}

# After
type User {
  email: String!  # Now non-null
}
```
**Impact**: Clients expecting nullable email may fail

#### 4. Argument Type Changed
```graphql
# Before
type Query {
  user(id: String!): User
}

# After
type Query {
  user(id: ID!): User  # Changed from String to ID
}
```
**Impact**: May cause validation issues depending on implementation

#### 5. Field Type Changed
```graphql
# Before
type User {
  createdAt: String
}

# After
type User {
  createdAt: DateTime!  # Changed scalar type
}
```
**Impact**: Clients expecting string format may break

### Non-Breaking Changes (Safe)

#### OpenAPI Non-Breaking
- ✓ Add new endpoint
- ✓ Add optional parameter
- ✓ Add optional request body property
- ✓ Add response property
- ✓ Make required field optional
- ✓ Add new enum value
- ✓ Expand validation (e.g., increase maxLength)
- ✓ Add default values

#### GraphQL Non-Breaking
- ✓ Add new field to type
- ✓ Add new type
- ✓ Add new query/mutation
- ✓ Add optional argument to field
- ✓ Remove non-null modifier (make nullable)
- ✓ Add value to enum
- ✓ Deprecate field (with @deprecated)

## Validation Strategies

### OpenAPI Validation

#### Structural Validation
1. **Schema adherence**: Validate against OpenAPI 3.0/3.1 spec
2. **Reference integrity**: Ensure all `$ref` point to valid schemas
3. **Required fields**: Check all required fields exist
4. **Type consistency**: Verify types match throughout

#### Content Validation
1. **Descriptions**: All operations and schemas should have descriptions
2. **Examples**: Include request/response examples
3. **Error responses**: Document 4xx and 5xx responses
4. **Security**: All protected endpoints have security requirements
5. **Tags**: Operations grouped with consistent tags

#### Common Issues to Check
```yaml
# ❌ Bad: Missing description
/users:
  get:
    responses:
      '200':
        description: Success

# ✓ Good: Descriptive
/users:
  get:
    summary: List all users
    description: Returns a paginated list of users with optional filtering
    responses:
      '200':
        description: Successfully retrieved user list
```

### GraphQL Validation

#### Schema Validation
1. **Type definitions**: All types properly defined
2. **Field types**: All fields reference valid types
3. **Arguments**: Argument types are valid scalars, enums, or input types
4. **Resolver coverage**: All fields have resolvers (implementation check)
5. **Circular references**: Detect and handle circular dependencies

#### Naming Conventions
- **Types**: PascalCase (e.g., `User`, `BlogPost`)
- **Fields**: camelCase (e.g., `firstName`, `createdAt`)
- **Enums**: UPPER_SNAKE_CASE (e.g., `USER_ROLE`, `POST_STATUS`)
- **Arguments**: camelCase (e.g., `userId`, `includeDeleted`)

#### Common Issues
```graphql
# ❌ Bad: Query returns nullable when it shouldn't
type Query {
  user(id: ID!): User  # Could return null
}

# ✓ Good: Clear nullability
type Query {
  user(id: ID!): User  # Can return null if not found
  requireUser(id: ID!): User!  # Always returns user or throws error
}
```

## Type Generation Strategies

### OpenAPI to TypeScript

#### Basic Type Mapping
```typescript
// OpenAPI schema
{
  "type": "object",
  "required": ["id", "email"],
  "properties": {
    "id": { "type": "string", "format": "uuid" },
    "email": { "type": "string", "format": "email" },
    "name": { "type": "string" },
    "age": { "type": "integer" }
  }
}

// Generated TypeScript
interface User {
  id: string;  // uuid format → string
  email: string;  // email format → string
  name?: string;  // optional → ?
  age?: number;  // integer → number
}
```

#### Union Types from oneOf
```yaml
# OpenAPI
PaymentMethod:
  oneOf:
    - $ref: '#/components/schemas/CreditCard'
    - $ref: '#/components/schemas/BankAccount'
```

```typescript
// TypeScript
type PaymentMethod = CreditCard | BankAccount;
```

#### Enum Mapping
```yaml
# OpenAPI
UserRole:
  type: string
  enum:
    - admin
    - member
    - guest
```

```typescript
// TypeScript
enum UserRole {
  Admin = 'admin',
  Member = 'member',
  Guest = 'guest'
}
// or
type UserRole = 'admin' | 'member' | 'guest';
```

### GraphQL to TypeScript

```graphql
# GraphQL
type User {
  id: ID!
  email: String!
  name: String
  posts: [Post!]!
}
```

```typescript
// TypeScript
interface User {
  id: string;  // ID! → string
  email: string;  // String! → string
  name: string | null;  // String → string | null
  posts: Post[];  // [Post!]! → Post[]
}
```

## Validation Tools Integration

### Spectral (OpenAPI)
```bash
# Install
npm install -g @stoplight/spectral-cli

# Validate
spectral lint openapi.yaml

# Custom ruleset
spectral lint openapi.yaml --ruleset .spectral.yaml
```

### GraphQL Inspector
```bash
# Install
npm install -g @graphql-inspector/cli

# Validate schema
graphql-inspector validate schema.graphql

# Compare schemas
graphql-inspector diff old.graphql new.graphql

# Coverage check
graphql-inspector coverage schema.graphql documents/*.graphql
```

### OpenAPI Diff
```bash
# Install
npm install -g openapi-diff

# Compare versions
openapi-diff old.yaml new.yaml

# Output markdown report
openapi-diff old.yaml new.yaml --format markdown > changes.md
```

## Security Considerations

### OpenAPI Security
1. **Authentication**: Always define security schemes
2. **Authorization**: Document which roles can access endpoints
3. **Sensitive data**: Mark PII fields in schemas
4. **Rate limiting**: Document rate limit headers
5. **HTTPS only**: Use https:// in server URLs

### GraphQL Security
1. **Query depth limiting**: Prevent deeply nested queries
2. **Query cost analysis**: Limit expensive operations
3. **Field-level auth**: Use directives like @auth
4. **Input validation**: Validate all arguments
5. **Disable introspection**: In production environments

## Best Practices Summary

### OpenAPI
- Use semantic versioning in `info.version`
- Group related operations with tags
- Always include request/response examples
- Document all error responses (4xx, 5xx)
- Use `$ref` to keep specs DRY
- Validate specs in CI/CD pipeline

### GraphQL
- Use meaningful type and field names
- Add descriptions to all types and fields
- Use custom scalars for validated types (Email, URL, etc.)
- Implement pagination for list fields
- Use @deprecated instead of removing fields
- Version schema with additive changes only

### Both
- Automate validation in CI/CD
- Generate client code from specs
- Keep specs in version control
- Review API changes in pull requests
- Maintain changelog of API versions
- Test generated client code

