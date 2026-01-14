# Phase II - Non-Functional Requirements

## Performance

| ID | Requirement | Target | Measurement |
|----|-------------|--------|-------------|
| NFR-P001 | Page load time | < 3 seconds | First contentful paint |
| NFR-P002 | API response time | < 2 seconds | Under normal load |
| NFR-P003 | UI feedback | < 200ms | After user action |
| NFR-P004 | Database query | < 100ms | Simple CRUD operations |
| NFR-P005 | Session validation | < 50ms | Cookie check + query |

---

## Scalability

| ID | Requirement | Description |
|----|-------------|-------------|
| NFR-S001 | Concurrent users | Support 100+ concurrent sessions |
| NFR-S002 | Todo storage | Unlimited per user |
| NFR-S003 | Database connections | Connection pooling (Neon serverless) |
| NFR-S004 | API horizontal | Stateless API for scaling (future) |

---

## Security

| ID | Requirement | Implementation |
|----|-------------|----------------|
| NFR-SC001 | Password hashing | bcrypt (cost factor 12) |
| NFR-SC002 | Session security | HTTP-only, SameSite=Lax, Secure |
| NFR-SC003 | Session expiration | Configurable (default 7 days) |
| NFR-SC004 | Input validation | Pydantic schemas, server-side |
| NFR-SC005 | SQL injection prevention | SQLModel ORM, parameterized queries |
| NFR-SC006 | CORS configuration | Strict origin allowlist |
| NFR-SC007 | Error masking | No internal details exposed |
| NFR-SC008 | Data isolation | 100% user-todo scoping |

---

## Reliability

| ID | Requirement | Target |
|----|-------------|--------|
| NFR-R001 | API availability | 99.9% uptime |
| NFR-R002 | Error recovery | Graceful degradation |
| NFR-R003 | Data consistency | ACID for todo operations |
| NFR-R004 | No data loss | Transaction safety |
| NFR-R005 | Recovery time | < 5 minutes (database) |

---

## Usability

| ID | Requirement | Description |
|----|-------------|-------------|
| NFR-U001 | Responsive design | 320px to 1920px viewports |
| NFR-U002 | Mobile support | Touch-friendly interfaces |
| NFR-U003 | Accessibility | WCAG 2.1 AA compliance |
| NFR-U004 | Keyboard navigation | Full functionality via keyboard |
| NFR-U005 | Loading states | Visual feedback during API calls |
| NFR-U006 | Error messages | User-friendly, actionable |
| NFR-U007 | Empty states | Encouraging, helpful |

---

## Accessibility (A11y)

| ID | Requirement | Implementation |
|----|-------------|----------------|
| NFR-A001 | Color contrast | 4.5:1 minimum ratio |
| NFR-A002 | Focus indicators | Visible focus states |
| NFR-A003 | ARIA labels | Interactive elements |
| NFR-A004 | Form labels | Associated labels for inputs |
| NFR-A005 | Screen reader | Semantic HTML structure |
| NFR-A006 | Motion preferences | Respect `prefers-reduced-motion` |

---

## Browser Support

| Browser | Version | Support Level |
|---------|---------|---------------|
| Chrome | Last 2 versions | Full |
| Firefox | Last 2 versions | Full |
| Safari | Last 2 versions | Full |
| Edge | Last 2 versions | Full |
| iOS Safari | Last 2 versions | Full |
| Chrome Android | Last 2 versions | Full |

---

## Technical Constraints

| Constraint | Value | Notes |
|------------|-------|-------|
| Python version | 3.11+ | Backend |
| TypeScript version | 5.x | Frontend |
| Node.js version | 18+ | Frontend build |
| Database | Neon PostgreSQL | Serverless |
| Auth library | Better Auth | As specified |
| API framework | FastAPI | As specified |
| Frontend framework | Next.js 14+ | App Router |

---

## Quality Gates

### Code Quality
- [ ] TypeScript strict mode enabled
- [ ] No `any` types (except external libraries)
- [ ] Pydantic models for all API inputs/outputs
- [ ] SQLModel for database operations
- [ ] Environment-based configuration
- [ ] No hardcoded secrets

### Testing
- [ ] Manual integration testing for all flows
- [ ] API endpoint testing
- [ ] Edge case handling verified
- [ ] Error path testing

### Documentation
- [ ] API contract documented
- [ ] Database schema documented
- [ ] Environment variables documented
- [ ] Setup instructions clear

---

## Monitoring (Future)

Not implemented in Phase II, but prepare for:
- Error logging (Sentry, etc.)
- Performance metrics (APM)
- User analytics
- Health check endpoints

---

## Compliance

| Standard | Compliance |
|----------|------------|
| OWASP Top 10 | Address security fundamentals |
| GDPR | User data protection (future) |
| WCAG 2.1 AA | Accessibility requirements |
