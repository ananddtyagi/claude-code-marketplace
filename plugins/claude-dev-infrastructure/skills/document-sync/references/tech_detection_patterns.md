# Technology Detection Patterns

This reference document contains the patterns and rules used by the Document Sync skill to detect technologies, frameworks, and architectural patterns in codebases.

## Framework Detection

### Frontend Frameworks

#### React
**Package Names:**
- `react`
- `react-dom`
- `@types/react`
- `react-scripts`

**File Patterns:**
- `jsx` or `tsx` extensions
- Import statements: `import React from 'react'`
- Component patterns: `function Component()`, `class Component extends React.Component`
- JSX syntax: `<div>`, `{variable}`

**Build Tools:**
- `create-react-app`
- Next.js: `next`, `@next/*`
- Vite React plugin: `@vitejs/plugin-react`

#### Vue.js
**Package Names:**
- `vue`
- `@vue/*`
- `vue-router`
- `vuex`
- `pinia`

**File Patterns:**
- `.vue` single file components
- `export default {` (Options API)
- `setup()` function (Composition API)
- `<template>`, `<script>`, `<style>` sections

#### Angular
**Package Names:**
- `@angular/*`
- `angular`

**File Patterns:**
- `.component.ts`, `.module.ts`, `.service.ts`
- `@Component()` decorators
- `@NgModule()` decorators
- `[()]` two-way binding syntax

#### Svelte
**Package Names:**
- `svelte`
- `@sveltejs/*`

**File Patterns:**
- `.svelte` files
- `export let` prop declarations
- `$:` reactive statements

### Backend Frameworks

#### Node.js Frameworks
**Express.js:**
- `express`
- `app.get()`, `app.post()` patterns
- `req`, `res` parameters

**Fastify:**
- `fastify`
- `fastify.get()`, `fastify.post()`

**Koa.js:**
- `koa`
- `ctx` context parameter

**NestJS:**
- `@nestjs/*`
- `@Controller()`, `@Injectable()` decorators
- Module pattern with `@Module()`

#### Python Frameworks
**Django:**
- `django`
- `settings.py` configuration
- `models.py` with Django models
- `urlpatterns` patterns
- `@csrf_exempt` decorators

**Flask:**
- `flask`
- `@app.route()` decorators
- `request`, `session` imports
- `render_template()`, `jsonify()`

**FastAPI:**
- `fastapi`
- `@app.get()`, `@app.post()` with async
- Pydantic models: `BaseModel`
- Automatic OpenAPI docs

#### Java Frameworks
**Spring Boot:**
- `spring-boot-starter-*`
- `@RestController`, `@Service`, `@Repository`
- `@SpringBootApplication`
- `application.properties` or `application.yml`

## Database Detection

### Relational Databases
**PostgreSQL:**
- `pg`, `pg-pool`, `knex-postgis`
- Connection strings: `postgresql://`, `postgres://`
- ORM patterns: `typeorm.postgresql`

**MySQL:**
- `mysql`, `mysql2`
- Connection strings: `mysql://`
- ORM patterns: `typeorm.mysql`

**SQLite:**
- `sqlite3`, `better-sqlite3`
- File extensions: `.db`, `.sqlite`, `.sqlite3`
- Connection: `sqlite:`

### NoSQL Databases
**MongoDB:**
- `mongodb`, `mongoose`
- Connection strings: `mongodb://`, `mongodb+srv://`
- Collection operations: `.find()`, `.insertOne()`

**CouchDB:**
- `couchdb`, `nano`, `pouchdb`
- Connection patterns: `couchdb://`, `http://localhost:5984`

**Redis:**
- `redis`, `ioredis`
- Connection strings: `redis://`
- Command patterns: `.get()`, `.set()`, `.hget()`

### Cloud Databases
**Firebase:**
- `firebase`, `@firebase/*`
- Firestore patterns: `firebase.firestore()`
- Realtime database: `firebase.database()`

**Supabase:**
- `supabase`, `@supabase/*`
- Client patterns: `supabase.from()`

## State Management Detection

### Frontend State Management
**Redux:**
- `redux`, `@reduxjs/*`
- Patterns: `createStore()`, `useSelector()`, `useDispatch()`
- Toolkit: `@reduxjs/toolkit`

**MobX:**
- `mobx`, `mobx-react`
- Patterns: `observable`, `action`, `computed`

**Zustand:**
- `zustand`
- Pattern: `create()` function

**Context API:**
- `createContext()`, `useContext()`
- Provider patterns: `<Context.Provider>`

## Authentication Detection

### JWT Authentication
**Packages:**
- `jsonwebtoken`, `jose`
- `@types/jsonwebtoken`

**Patterns:**
- `jwt.sign()`, `jwt.verify()`
- Authorization header: `Bearer <token>`

### OAuth
**Packages:**
- `passport`, `passport-*` strategies
- `@auth0/*`

**Patterns:**
- OAuth URL patterns: `/oauth/*`
- Scopes and redirect URIs

### Session Authentication
**Packages:**
- `express-session`, `cookie-session`
- `client-sessions`

**Patterns:**
- `req.session`
- Session middleware configuration

## Testing Frameworks

### JavaScript/TypeScript
**Jest:**
- `jest`, `@jest/*`
- Patterns: `describe()`, `it()`, `test()`, `expect()`
- Mock functions: `jest.fn()`

**Vitest:**
- `vitest`
- Similar patterns to Jest

**Cypress:**
- `cypress`
- E2E test patterns: `cy.visit()`, `cy.get()`

**Playwright:**
- `playwright`, `@playwright/*`
- Patterns: `page.goto()`, `page.locator()`

### Python
**Pytest:**
- `pytest`
- Patterns: `def test_*()`, `@pytest.fixture`

**Unittest:**
- `unittest`
- Patterns: `unittest.TestCase`, `self.assertEqual()`

## Build Tools and Bundlers

### JavaScript Bundlers
**Vite:**
- `vite`
- Config files: `vite.config.js`, `vite.config.ts`
- Plugins: `@vitejs/plugin-*`

**Webpack:**
- `webpack`, `webpack-cli`
- Config files: `webpack.config.js`
- Loaders and plugins patterns

**Rollup:**
- `rollup`
- Config files: `rollup.config.js`

**Parcel:**
- `parcel`, `parcel-bundler`

### CSS Tools
**Tailwind CSS:**
- `tailwindcss`
- Config: `tailwind.config.js`
- Utility classes patterns

**PostCSS:**
- `postcss`
- Config: `postcss.config.js`

**Sass/Less:**
- `sass`, `node-sass`, `less`

## Deployment Patterns

### Containerization
**Docker:**
- `Dockerfile`
- `docker-compose.yml`, `docker-compose.yaml`
- `.dockerignore`

### Kubernetes
**Kubernetes:**
- `k8s/`, `kubernetes/` directories
- `.yaml`, `.yml` files with Kubernetes resources
- `deployment.yaml`, `service.yaml`

### Cloud Services
**AWS:**
- `aws-sdk`
- Serverless framework: `serverless.yml`
- SAM templates: `template.yaml`

**Vercel:**
- `vercel.json`
- `.vercelignore`

**Netlify:**
- `netlify.toml`

### CI/CD
**GitHub Actions:**
- `.github/workflows/`
- `*.yml`, `*.yaml` workflow files

**GitLab CI:**
- `.gitlab-ci.yml`

**Azure Pipelines:**
- `azure-pipelines.yml`

## Configuration File Patterns

### Environment Configuration
**Node.js:**
- `.env`, `.env.local`, `.env.production`
- `process.env.VARIABLE` patterns

**Python:**
- `.env`
- `os.getenv()`, `environ.get()`

### Configuration Files
**TypeScript:**
- `tsconfig.json`
- Type definitions and compiler options

**JavaScript:**
- `jsconfig.json`

**Python:**
- `settings.py`, `config.py`
- `pyproject.toml`, `setup.cfg`

**Java:**
- `application.properties`, `application.yml`

## API Pattern Detection

### REST API Patterns
**HTTP Methods:**
- `app.get()`, `app.post()`, `app.put()`, `app.delete()`
- `router.get()`, `router.post()`

**URL Patterns:**
- `/api/v1/*` versioned APIs
- `/users/:id` parameterized routes
- Query parameters: `req.query`

### GraphQL Patterns
**Packages:**
- `graphql`, `apollo-server*`, `@apollo/*`

**Patterns:**
- Schema definitions: `type Query { }`
- Resolvers: `Query: { users() }`
- GraphQL endpoint: `/graphql`

## Architecture Patterns

### Microservices
**Service Discovery:**
- `consul`, `etcd`
- Service registry patterns

**API Gateway:**
- `express-gateway`
- Gateway middleware patterns

### Event-Driven Architecture
**Message Queues:**
- `redis`, `bull` (Node.js)
- `celery` (Python)
- `kafka`, `rabbitmq`

**Event Patterns:**
- Event emitters: `EventEmitter`
- Pub/Sub patterns: `publish()`, `subscribe()`

### Monolithic Patterns
**MVC Architecture:**
- Models, Views, Controllers separation
- Repository patterns

**Layered Architecture:**
- Service layer patterns
- Data access layer patterns

This reference document serves as a comprehensive guide for understanding how the Document Sync skill identifies and categorizes different technologies in modern software projects.