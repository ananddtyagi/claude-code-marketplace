# Documentation Update Templates

This reference document provides templates and patterns for automatically updating different types of documentation sections based on verification results.

## API Documentation Templates

### API Endpoint Updates

#### Missing Endpoints Template
```markdown
## API Endpoints

### Update Required
The following endpoints were mentioned in documentation but not detected in the codebase:

<!-- AUTO-GENERATED: Missing Endpoints -->
- **GET /users** - Not found in codebase
- **POST /products** - Not found in codebase

### Current Endpoints
Based on codebase analysis, the following endpoints are available:

<!-- AUTO-GENERATED: Current Endpoints -->
```python
# Example from system scan
app.get('/api/v1/users', get_all_users)
app.post('/api/v1/users', create_user)
```

### Suggested Updates
1. Remove missing endpoints from documentation
2. Add current endpoints with examples
3. Update request/response schemas
```

#### Outdated HTTP Methods Template
```markdown
### HTTP Method Correction
**Original Documentation:**
```
GET /api/users/:id  # Update user information
```

**Code Analysis:**
```javascript
app.put('/api/users/:id', updateUser)  // Correct method is PUT
```

**Recommended Update:**
```
PUT /api/users/:id  # Update user information
```
```

### Response Schema Updates

#### Missing Response Examples Template
```markdown
### Response Examples

<!-- AUTO-GENERATED: Response Examples -->
**GET /api/users**
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "created_at": "2024-01-01T00:00:00Z"
}
```

**POST /api/users**
Request Body:
```json
{
  "name": "New User",
  "email": "user@example.com"
}
```

Response:
```json
{
  "id": 2,
  "name": "New User",
  "email": "user@example.com",
  "created_at": "2024-01-01T00:00:00Z"
}
```
```

## Framework Documentation Templates

### Framework Version Updates

#### Version Mismatch Template
```markdown
## Technology Stack

### Detected vs Documented

<!-- AUTO-GENERATED: Framework Versions -->
| Technology | Documented Version | Detected Version | Status |
|------------|-------------------|------------------|---------|
| React | ^17.0.0 | ^18.2.0 | ⚠️ Outdated |
| Node.js | 16.x | 18.x | ⚠️ Outdated |
| TypeScript | 4.5.x | 5.0.x | ⚠️ Outdated |

### Recommended Updates
- Update React documentation to reflect v18 features
- Update Node.js installation instructions
- Add TypeScript v5 specific patterns
```

#### New Framework Features Template
```markdown
### New Framework Features
Based on the detected version, consider documenting these new features:

<!-- AUTO-GENERATED: New Features -->
- **React 18**: Concurrent features, automatic batching
- **TypeScript 5**: Decorators, const type parameters
- **Node.js 18**: Fetch API, built-in test runner

### Examples
```typescript
// React 18 Concurrent Features
const deferredValue = useDeferredValue(value);

// TypeScript 5 Decorators
@Component
class MyClass {
  @loggedMethod
  greet(name: string) {
    console.log(`Hello, ${name}!`);
  }
}
```
```

## Configuration Documentation Templates

### Environment Variables Template

```markdown
## Configuration

### Environment Variables
<!-- AUTO-GENERATED: Environment Variables -->
Required environment variables detected in codebase:

| Variable | Description | Default Value | Required |
|----------|-------------|---------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | None | ✅ Yes |
| `API_PORT` | Server port number | `3000` | ❌ No |
| `JWT_SECRET` | JWT signing secret | None | ✅ Yes |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379` | ❌ No |

### .env.example Template
```bash
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/mydb

# Server Configuration
API_PORT=3000

# Authentication
JWT_SECRET=your-secret-key

# Optional: Redis for caching
REDIS_URL=redis://localhost:6379
```

### Installation Steps Update
1. Copy `.env.example` to `.env`
2. Fill in required environment variables
3. Run database migrations
```

### Configuration File Updates Template

```markdown
### Configuration Files

#### TypeScript Configuration (tsconfig.json)
<!-- AUTO-GENERATED: Config Updates -->
Detected TypeScript configuration differs from documentation:

**Recommended tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

#### Build Configuration (vite.config.ts)
```typescript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    envPrefix: 'API_'
  },
  build: {
    outDir: 'dist',
    sourcemap: true
  }
});
```
```

## Code Example Updates Template

### Syntax Correction Template

```markdown
### Code Examples Update

#### Before (with syntax errors)
```javascript
// Original example had syntax issues
const user = getUser(id);
console.log(user.name

// Missing closing parenthesis and semicolon
```

#### After (corrected)
```javascript
// Fixed syntax
const user = getUser(id);
console.log(user.name);  // Added missing semicolon and parenthesis
```

### Modern API Usage Template

```markdown
### Updated API Usage

#### Legacy Approach
```javascript
// Older way of handling async operations
function fetchUser(id) {
  return fetch(`/api/users/${id}`)
    .then(response => response.json())
    .then(data => data.user)
    .catch(error => console.error('Error:', error));
}
```

#### Modern Approach
```javascript
// Modern async/await with proper error handling
async function fetchUser(id) {
  try {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data.user;
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw error;
  }
}
```

### Import Path Updates Template

```markdown
### Import Path Corrections

#### Outdated Imports
```javascript
// Old import paths (may not exist)
import { UserService } from '../services/user.service';
import { validateUser } from '../utils/validation';
```

#### Corrected Imports
```javascript
// Updated import paths based on actual file structure
import { UserService } from '../services/user';
import { validateUser } from '../utils/validators';
```
```

## Feature Documentation Templates

### New Features Template

```markdown
## Features

### Recently Added Features
<!-- AUTO-GENERATED: New Features -->
The following features were detected in the codebase but not documented:

#### User Authentication
- Email/password authentication
- JWT token management
- Password reset functionality

#### Data Export
- CSV export functionality
- PDF report generation
- Scheduled export jobs

#### Real-time Updates
- WebSocket connections
- Live data synchronization
- Real-time notifications

### Usage Examples

#### User Authentication
```typescript
// Login example
const loginResult = await authService.login(email, password);
localStorage.setItem('token', loginResult.token);

// Protected API call
const userData = await apiClient.get('/user/profile', {
  headers: {
    'Authorization': `Bearer ${loginResult.token}`
  }
});
```

#### Data Export
```typescript
// Export to CSV
const csvData = await exportService.toCSV(userData);
downloadFile(csvData, 'users.csv', 'text/csv');

// Generate PDF report
const pdfReport = await reportService.generatePDF(userData);
downloadFile(pdfReport, 'user-report.pdf', 'application/pdf');
```
```

### Deprecated Features Template

```markdown
## Deprecated Features

### Features No Longer Available
<!-- AUTO-GENERATED: Deprecated Features -->
The following features are mentioned in documentation but were not found in the current codebase:

#### Legacy Analytics System (Removed)
**Previous Documentation:**
> The system includes Google Analytics integration with custom event tracking.

**Current Status:** This feature has been removed and replaced with the new analytics dashboard.

**Migration Guide:**
1. Remove Google Analytics scripts
2. Use new analytics dashboard at `/analytics`
3. Update event tracking to use new API

#### XML Data Export (Deprecated)
**Previous Documentation:**
> Export data in XML format using the export endpoint.

**Current Status:** XML export has been deprecated in favor of JSON and CSV formats.

**Recommended Replacement:**
```javascript
// Instead of XML export
const xmlData = await exportService.toXML(data);

// Use JSON or CSV export
const jsonData = await exportService.toJSON(data);
const csvData = await exportService.toCSV(data);
```
```

## Structural Update Templates

### Table of Contents Template

```markdown
## Table of Contents

<!-- AUTO-GENERATED: TOC -->
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [API Reference](#api-reference)
  - [Authentication](#authentication)
  - [Endpoints](#endpoints)
- [Features](#features)
  - [User Management](#user-management)
  - [Data Export](#data-export)
- [Development](#development)
  - [Local Setup](#local-setup)
  - [Testing](#testing)
```

### Navigation Updates Template

```markdown
### Navigation Structure Updates

#### Updated File Structure
```
project/
├── src/
│   ├── components/          # React components
│   ├── services/           # API services
│   ├── utils/              # Utility functions
│   └── types/              # TypeScript definitions
├── docs/
│   ├── api/                # API documentation
│   ├── guides/             # User guides
│   └── examples/           # Code examples
└── tests/                  # Test files
```

#### Updated Navigation Links
- [API Reference](./docs/api/) - Updated to match new structure
- [User Guides](./docs/guides/) - New location
- [Code Examples](./docs/examples/) - New examples section
```

## Integration Update Templates

### Dependency Updates Template

```markdown
## Dependencies

### Updated Package.json
<!-- AUTO-GENERATED: Dependencies -->
```json
{
  "name": "my-project",
  "version": "2.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "axios": "^1.4.0",
    "express": "^4.18.2"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@vitejs/plugin-react": "^4.0.0",
    "typescript": "^5.0.0",
    "vite": "^4.4.0"
  }
}
```

### Breaking Changes
- **React 18**: Update to concurrent features
- **TypeScript 5**: New syntax features available
- **Vite 4**: Updated build configuration

### Migration Steps
1. Update dependencies: `npm install`
2. Update React imports for new features
3. Review TypeScript strict mode settings
4. Test build process with new Vite configuration
```

These templates provide a comprehensive foundation for automatically updating documentation while maintaining consistency and accuracy across different types of content.