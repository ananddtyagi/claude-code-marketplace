# Agent Quick Reference

## 🎯 When to Use Each Agent

### API Architect (`/agent api-architect`)
**Use when:**
- Designing new REST, GraphQL, or gRPC APIs
- Reviewing endpoint structure and naming
- Planning API versioning strategies
- Implementing authentication flows
- Creating OpenAPI/Swagger specs
- Designing error handling and status codes

**Best for:** API design, endpoint structure, authentication, documentation

---

### Security Specialist (`/agent security-specialist`)
**Use when:**
- Conducting security code reviews
- Identifying vulnerabilities (SQL injection, XSS, CSRF)
- Implementing authentication/authorization
- Reviewing data encryption and storage
- Auditing dependency security
- Setting up security headers
- Designing secure session management

**Best for:** Security audits, vulnerability detection, secure coding practices

---

### Code Quality Reviewer (`/agent code-quality-reviewer`)
**Use when:**
- Conducting code reviews
- Identifying code smells and anti-patterns
- Refactoring complex code
- Improving code readability
- Applying SOLID principles
- Reducing technical debt
- Establishing coding standards

**Best for:** Code reviews, refactoring, clean code principles

---

### UX/UI Designer (`/agent ux-ui-designer`)
**Use when:**
- Designing user interfaces
- Reviewing accessibility compliance
- Improving user experience flows
- Creating design systems
- Optimizing responsive layouts
- Designing forms and interactions
- Ensuring proper color contrast

**Best for:** UI/UX design, accessibility, user flows, responsive design

---

### Database Architect (`/agent database-architect`)
**Use when:**
- Designing database schemas
- Optimizing slow queries
- Creating indexes and constraints
- Planning migrations
- Implementing transactions
- Choosing between SQL/NoSQL
- Designing for scalability

**Best for:** Schema design, query optimization, database performance

---

### Performance Engineer (`/agent performance-engineer`)
**Use when:**
- Investigating slow performance
- Identifying bottlenecks
- Optimizing algorithms and queries
- Implementing caching strategies
- Reducing memory usage
- Optimizing frontend rendering
- Planning performance monitoring

**Best for:** Performance optimization, bottleneck identification, profiling

---

### DevOps Engineer (`/agent devops-engineer`)
**Use when:**
- Setting up CI/CD pipelines
- Implementing infrastructure as code
- Configuring containers and Kubernetes
- Planning deployment strategies
- Setting up monitoring and logging
- Optimizing cloud costs
- Designing disaster recovery

**Best for:** CI/CD, infrastructure automation, deployments, monitoring

---

### Testing Specialist (`/agent testing-specialist`)
**Use when:**
- Designing testing strategies
- Writing unit, integration, or e2e tests
- Implementing test automation
- Improving test coverage
- Setting up testing frameworks
- Designing test data management
- Reviewing existing tests

**Best for:** Test strategy, test automation, comprehensive coverage

---

### Documentation Writer (`/agent documentation-writer`)
**Use when:**
- Creating API documentation
- Writing README files
- Documenting architecture decisions
- Creating setup guides
- Writing inline code documentation
- Documenting troubleshooting steps
- Maintaining changelogs

**Best for:** Technical documentation, API docs, README files

---

### Tech Lead (`/agent tech-lead`)
**Use when:**
- Making architecture decisions
- Planning technical roadmap
- Coordinating development efforts
- Balancing technical debt with features
- Evaluating technology choices
- Guiding team through challenges
- Establishing team standards

**Best for:** Architecture decisions, technical leadership, strategic planning

---

## 🔥 Common Workflows

### New Feature Development
1. **Tech Lead** - Architecture and approach
2. **API Architect** - API design (if needed)
3. **Database Architect** - Schema design (if needed)
4. **Testing Specialist** - Testing strategy
5. **Documentation Writer** - Documentation plan

### Code Review
1. **Code Quality Reviewer** - Clean code and patterns
2. **Security Specialist** - Security vulnerabilities
3. **Performance Engineer** - Performance issues
4. **Testing Specialist** - Test coverage

### Performance Investigation
1. **Performance Engineer** - Identify bottlenecks
2. **Database Architect** - Query optimization
3. **DevOps Engineer** - Infrastructure considerations

### Production Deployment
1. **DevOps Engineer** - Deployment strategy
2. **Testing Specialist** - Test automation in CI/CD
3. **Security Specialist** - Security review
4. **Tech Lead** - Final approval

### Refactoring
1. **Code Quality Reviewer** - Identify issues
2. **Tech Lead** - Strategic approach
3. **Testing Specialist** - Test coverage before/after
4. **Documentation Writer** - Update docs

---

## 💡 Pro Tips

1. **Combine Agents**: Use multiple specialists for comprehensive reviews
2. **Be Specific**: Provide file paths and specific concerns
3. **Iterate**: Ask follow-up questions to dive deeper
4. **Context Matters**: Share relevant background information
5. **Use `/code-explain` First**: Understand existing code before consulting agents

---

## 📝 Commands Reference

### `/code-explain <query>`
Deep dive into codebase to answer questions about how things work, what code does, where things are implemented, and why they're done a certain way.

**Examples:**
- `/code-explain How does authentication work?`
- `/code-explain Where is payment processing implemented?`
- `/code-explain What does the rate limiter middleware do?`

### `/update-claude`
Update the CLAUDE.md file to reflect major changes in the codebase. Keeps project documentation current for Claude and your team.

**When to use:**
- After major refactoring
- After adding new features or modules
- After architectural changes
- When structure changes significantly

---

**Quick Tip**: Type `/agents` to see the interactive agent selector!

