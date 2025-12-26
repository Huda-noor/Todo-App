---
id: 001
title: Initial Constitution Creation
stage: constitution
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5
feature: none
branch: 001-physical-ai-book
user: Huda Noor
command: /sp.constitution
labels: ["constitution", "governance", "initial-setup", "spec-driven-development"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/001-initial-constitution-creation.constitution.prompt.md
tests:
  - N/A (documentation only)
---

## Prompt

create # Global Constitution — Evolution of Todo

This constitution is the supreme, immutable governing document for the entire "Evolution of Todo" project, covering Phase I through Phase V.
No agent, tool, or human instruction may override this constitution unless it is explicitly revised through :
- Treat specifications as law, not guidance
- Reject ambiguous or incomplete instructions
- Request clarification only at the specification level
- Report conflicts between specs, plans, and tasks immediately

Agents are not allowed to "improve" the product beyond what is specified.

## 3. Phase Governance & Isolation

The project is divided into strictly isolated phases (Phase I to Phase V).

#a formal specification update.

## 1. Spec-Driven Development (Mandatory)

All development **must** follow strict Spec-Driven Development (SDD).
The **only** allowed execution flow is:

**Constitution → Specifications → Architecture Plan → Task Breakdown → Implementation**

### Rules:
- No agent may write code without approved specifications and tasks.
- No planning or implementation may occur before specifications are finalized.
- Code must be a direct and literal execution of specifications.
- Refinement, correction, or improvement **must** occur at the specification level, never directly at the code level.
- Any output that violates this flow is invalid and must be rejected.

## 2. Agent Behavior Rules (Zero Deviation)

All agents must behave as deterministic executors of specifications.

### Strictly Prohibited:
- Manual coding by humans
- Feature invention or assumption
- Guessing missing requirements
- Deviating from approved specifications
- Adding optimizations or enhancements not explicitly## Rules:
- Each phase is fully scoped by its own specification.
- No future-phase feature may be implemented, scaffolded, hinted, or prepared in an earlier phase.
- No partial implementations for future phases are allowed.
- Architecture may evolve **only** through updated specifications and plans.

Phase leakage is a constitutional violation.

## 4. Technology Constraints (Non-Negotiable)

All agents **must** comply with the following technology stack:

### Backend:
- Python
- FastAPI
- SQLModel
- Neon DB (PostgreSQL-compatible)

### Frontend (later phases only):
- Next.js

### AI & Agent Infrastructure:
- OpenAI Agents SDK
- MCP (Model Context Protocol)

### Infrastructure (later phases only):
- Docker
- Kubernetes
- Kafka
- Dapr

### Rules:
- No alternative languages, frameworks, or tools may be introduced.
- Any change to the technology stack requires a formal specification update.

## 5. Quality & Architecture Principles

All deliverables must adhere to the following principles:

- Clean Architecture
- Clear separation of concerns
- Modular and layered design
- Stateless services where required
- Deterministic and predictable behavior
- Cloud-native readiness from the start

Quality is mandatory and cannot be postponed to later phases.

## 6. Stability & Enforcement

- This constitution remains stable across all phases.
- Any violation invalidates the output.
- Non-compliant work must be rolled back to the last compliant state.
- All agents must explicitly acknowledge and obey this constitution before contributing to the project.

======================================================================
**END OF GLOBAL CONSTITUTION**
======================================================================

## Response snapshot

Created the initial project constitution for "Evolution of Todo" covering all five phases. The constitution establishes:

**Six Core Principles**:
1. Spec-Driven Development (Mandatory) - Enforces Constitution → Spec → Plan → Tasks → Implementation flow
2. Agent Behavior Rules (Zero Deviation) - Agents as deterministic executors, no autonomous improvements
3. Phase Governance & Isolation - Strict phase boundaries, no future-phase work in current phase
4. Technology Constraints (Non-Negotiable) - Standardized stack (Python/FastAPI/SQLModel/Neon DB, Next.js, OpenAI SDK, MCP, Docker/K8s/Kafka/Dapr)
5. Quality & Architecture Principles - Clean Architecture, separation of concerns, cloud-native from start
6. Test-First Development (When Specified) - Red-Green-Refactor when tests are required

**Additional Sections**:
- Development Workflow with execution contracts and acceptance criteria
- Human as Tool Strategy for managing ambiguity and architectural decisions
- Documentation & Traceability (PHR and ADR guidelines)
- Default Policies for implementation
- Governance with amendment procedures

**Version**: 1.0.0 (initial ratification)
**Templates**: Verified alignment with plan-template.md, spec-template.md, and tasks-template.md

## Outcome

- ✅ Impact: Established supreme governing document for all project phases, defining mandatory execution flow and technology stack
- 🧪 Tests: N/A (documentation only)
- 📁 Files: Created .specify/memory/constitution.md (237 lines) and this PHR
- 🔁 Next prompts: User should now create feature specifications using /sp.specify, followed by /sp.plan and /sp.tasks
- 🧠 Reflection: Constitution successfully enforces Spec-Driven Development with clear phase isolation and zero-deviation agent behavior rules

## Evaluation notes (flywheel)

- Failure modes observed: None - constitution creation successful on first attempt
- Graders run and results (PASS/FAIL): Manual review - PASS (all placeholders filled, no bracketed tokens, proper versioning)
- Prompt variant (if applicable): Standard constitution creation from user-provided structured input
- Next experiment (smallest change to try): Monitor adherence to SDD flow in subsequent specification and planning commands
