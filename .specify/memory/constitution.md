<!--
Sync Impact Report:
- Version change: none → 1.0.0
- Modified principles: Initial constitution creation
- Added sections:
  * Spec-Driven Development (Mandatory)
  * Agent Behavior Rules (Zero Deviation)
  * Phase Governance & Isolation
  * Technology Constraints (Non-Negotiable)
  * Quality & Architecture Principles
  * Stability & Enforcement
- Removed sections: N/A (initial creation)
- Templates requiring updates:
  ✅ plan-template.md - Verified Constitution Check section aligns
  ✅ spec-template.md - Verified requirements alignment with SDD principles
  ✅ tasks-template.md - Verified task categorization reflects constitutional principles
- Follow-up TODOs: None
-->

# Evolution of Todo — Constitution

This constitution is the supreme, immutable governing document for the entire "Evolution of Todo" project, covering Phase I through Phase V.

No agent, tool, or human instruction may override this constitution unless it is explicitly revised through a formal specification update.

## Core Principles

### I. Spec-Driven Development (Mandatory)

All development **MUST** follow strict Spec-Driven Development (SDD).

The **ONLY** allowed execution flow is:

**Constitution → Specifications → Architecture Plan → Task Breakdown → Implementation**

**Rules**:
- No agent may write code without approved specifications and tasks
- No planning or implementation may occur before specifications are finalized
- Code must be a direct and literal execution of specifications
- Refinement, correction, or improvement **MUST** occur at the specification level, never directly at the code level
- Any output that violates this flow is invalid and must be rejected
- Treat specifications as law, not guidance
- Reject ambiguous or incomplete instructions
- Request clarification only at the specification level
- Report conflicts between specs, plans, and tasks immediately

**Rationale**: Spec-Driven Development ensures consistency, traceability, and prevents scope creep. All decisions are documented and approved before implementation, reducing rework and maintaining architectural integrity.

### II. Agent Behavior Rules (Zero Deviation)

All agents must behave as deterministic executors of specifications.

**Strictly Prohibited**:
- Manual coding by humans
- Feature invention or assumption
- Guessing missing requirements
- Deviating from approved specifications
- Adding optimizations or enhancements not explicitly specified
- "Improving" the product beyond what is specified

**Rationale**: Agents are execution tools, not decision-makers. Human oversight and specification approval ensure quality control and prevent unauthorized changes that could introduce bugs or violate requirements.

### III. Phase Governance & Isolation

The project is divided into strictly isolated phases (Phase I to Phase V).

**Rules**:
- Each phase is fully scoped by its own specification
- No future-phase feature may be implemented, scaffolded, hinted, or prepared in an earlier phase
- No partial implementations for future phases are allowed
- Architecture may evolve **ONLY** through updated specifications and plans

**Consequence**: Phase leakage is a constitutional violation.

**Rationale**: Phase isolation prevents complexity creep, ensures each phase delivers working software, and maintains focus on current requirements without prematurely optimizing for uncertain futures.

### IV. Technology Constraints (Non-Negotiable)

All agents **MUST** comply with the following technology stack:

**Backend**:
- Python
- FastAPI
- SQLModel
- Neon DB (PostgreSQL-compatible)

**Frontend** (later phases only):
- Next.js

**AI & Agent Infrastructure**:
- OpenAI Agents SDK
- MCP (Model Context Protocol)

**Infrastructure** (later phases only):
- Docker
- Kubernetes
- Kafka
- Dapr

**Rules**:
- No alternative languages, frameworks, or tools may be introduced
- Any change to the technology stack requires a formal specification update

**Rationale**: Technology standardization reduces complexity, ensures team expertise concentration, and maintains consistent patterns across the codebase. Changes require formal review to assess ecosystem impacts.

### V. Quality & Architecture Principles

All deliverables must adhere to the following principles:

- **Clean Architecture**: Clear separation of concerns and dependency rules
- **Separation of Concerns**: Each module has a single, well-defined responsibility
- **Modular and Layered Design**: Components are independently testable and replaceable
- **Stateless Services**: Where required for scalability and reliability
- **Deterministic and Predictable Behavior**: No hidden side effects
- **Cloud-Native Readiness**: Design for distributed systems from the start

**Rules**:
- Quality is mandatory and cannot be postponed to later phases
- Architecture decisions must be documented in specifications before implementation
- Code reviews must verify adherence to these principles

**Rationale**: Quality debt compounds exponentially. Building quality in from the start is cheaper than retrofitting it later. Cloud-native patterns ensure scalability and maintainability as the system grows.

### VI. Test-First Development (When Specified)

When tests are explicitly required in specifications:

**Rules**:
- Tests MUST be written before implementation
- Tests MUST fail initially (Red-Green-Refactor cycle)
- Implementation proceeds only after test approval
- All tests MUST pass before task completion

**Rationale**: Test-first development ensures requirements are testable, reduces defects, and provides living documentation of system behavior.

## Development Workflow

### Execution Contract for Every Request

1. **Confirm surface and success criteria** (one sentence)
2. **List constraints, invariants, non-goals**
3. **Produce the artifact** with acceptance checks inlined (checkboxes or tests where applicable)
4. **Add follow-ups and risks** (max 3 bullets)
5. **Create PHR** in appropriate subdirectory under `history/prompts/` (constitution, feature-name, or general)
6. **If plan/tasks identified architectural decisions**, suggest ADR documentation (never auto-create)

### Minimum Acceptance Criteria

- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

### Human as Tool Strategy

Agents are not expected to solve every problem autonomously. Agents **MUST** invoke the user for input when encountering situations requiring human judgment.

**Invocation Triggers**:
1. **Ambiguous Requirements**: Ask 2-3 targeted clarifying questions before proceeding
2. **Unforeseen Dependencies**: Surface them and ask for prioritization
3. **Architectural Uncertainty**: Present options with tradeoffs and get user preference
4. **Completion Checkpoint**: After major milestones, summarize and confirm next steps

**Rationale**: Humans provide context, priorities, and business judgment that agents cannot infer. Structured questions are more efficient than autonomous guessing.

## Documentation & Traceability

### Prompt History Records (PHR)

After completing requests, agents **MUST** create a PHR (Prompt History Record).

**When to Create PHRs**:
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Routing** (all under `history/prompts/`):
- Constitution → `history/prompts/constitution/`
- Feature-specific → `history/prompts/<feature-name>/`
- General → `history/prompts/general/`

### Architecture Decision Records (ADR)

When significant architectural decisions are detected (typically during planning):

**Significance Test** (ALL must be true):
- **Impact**: Long-term consequences (framework, data model, API, security, platform)
- **Alternatives**: Multiple viable options considered
- **Scope**: Cross-cutting and influences system design

**Process**:
- Suggest: "📋 Architectural decision detected: [brief-description] — Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`"
- Wait for user consent
- Never auto-create ADRs
- Group related decisions when appropriate

**Rationale**: ADRs capture the "why" behind important decisions, preventing future confusion and enabling informed evolution as context changes.

## Default Policies

All agents must follow these policies:

- **Clarify and plan first**: Keep business understanding separate from technical plan; carefully architect and implement
- **Do not invent**: APIs, data, or contracts—ask targeted clarifiers if missing
- **Never hardcode secrets**: Use `.env` and document configuration requirements
- **Prefer smallest viable diff**: Do not refactor unrelated code
- **Cite existing code**: Use code references (start:end:path); propose new code in fenced blocks
- **Keep reasoning private**: Output only decisions, artifacts, and justifications

## Governance

### Constitution Authority

- This constitution supersedes all other practices, preferences, and conventions
- Amendments require formal documentation, approval, and migration plan
- All PRs and reviews must verify compliance with constitutional principles
- Non-compliant work must be rolled back to the last compliant state

### Enforcement & Stability

- This constitution remains stable across all phases
- Any violation invalidates the output
- All agents must explicitly acknowledge and obey this constitution before contributing
- Complexity must be justified against constitutional principles

### Amendment Procedure

Constitutional changes require:
1. Formal proposal with rationale
2. Impact analysis on existing specifications and implementations
3. Migration plan if retroactive changes needed
4. User approval
5. Version increment following semantic versioning

**Version**: 1.0.0 | **Ratified**: 2025-12-27 | **Last Amended**: 2025-12-27
