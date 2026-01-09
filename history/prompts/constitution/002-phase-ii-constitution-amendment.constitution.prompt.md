---
id: 002
title: Phase II Constitution Amendment
stage: constitution
date: 2025-12-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: architect
command: /sp.constitution
labels: ["constitution", "phase-ii", "amendment", "technology-matrix"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

Amend the Global Constitution for the "Evolution of Todo" project to incorporate Phase II requirements while preserving strict phase isolation and all existing principles.

This amendment must update only the necessary sections to authorize new technologies and scope for Phase II, without weakening any rules from the original constitution.

Specific changes to apply:

1. **Technology Constraints (Section 4)** – Update the technology matrix as follows:
   - Phase I (unchanged): Pure in-memory Python console application, standard library only, no persistence, no web, no authentication.
   - Phase II (new authorizations):
     - Backend: Python with FastAPI for REST API
     - Database: Neon Serverless PostgreSQL (introduced in Phase II)
     - ORM/Data layer: SQLModel
     - Frontend: Next.js (React + TypeScript)
     - Authentication: Better Auth library for signup/signin (email/password only in Phase II)
     - Architecture: Full-stack web application (separate backend and frontend repositories)
   - Phase III–V: Retain existing allowances for Docker, Kubernetes, Kafka, Dapr, OpenAI Agents SDK, MCP, etc. (no changes)
   - Explicit rule: Authentication, web frontend, and persistent database are prohibited in Phase I and permitted only from Phase II onward.

2. **Phase Governance & Isolation (Section 3)** – Reinforce:
   - No back-porting of Phase II technologies (FastAPI, SQLModel, Neon DB, Next.js, authentication) into Phase I.
   - Phase II must build incrementally on Phase I concepts but implement persistence, API, and web UI from scratch as new layers.
   - No AI, agent frameworks, or advanced infrastructure until their designated later phases.

3. **Quality & Architecture Principles (Section 5)** – Add:
   - Full-stack separation: Clear boundary between backend API and frontend client.
   - Stateless API endpoints where possible.
   - Secure authentication practices (password hashing, token expiration, etc.).

## Response snapshot

Constitutional amendment v1.0.0 → v1.1.0 completed successfully with the following changes:

**Section III (Phase Governance & Isolation)** - Expanded with:
- Back-Porting Prohibition rules explicitly listing Phase II technologies as prohibited in Phase I
- Phase Progression Rules defining how Phase II builds on Phase I concepts
- Explicit prohibition of AI, agent frameworks, and advanced infrastructure until designated phases

**Section IV (Technology Constraints)** - Restructured as phase-specific matrix:
- Phase I: Python standard library ONLY, with explicit prohibitions listed
- Phase II: FastAPI, SQLModel, Neon PostgreSQL, Next.js, Better Auth (email/password only)
- Phase III–V: Docker, Kubernetes, Kafka, Dapr, OpenAI Agents SDK, MCP

**Section V (Quality & Architecture Principles)** - Expanded with:
- Full-Stack Separation principles (Phase II+)
- API Design principles (Phase II+)
- Authentication Security principles (Phase II+)

All existing principles preserved. Templates verified compatible (no updates required).

## Outcome

- ✅ Impact: Constitution amended to authorize Phase II technologies while preserving Phase I isolation
- 🧪 Tests: N/A (governance document)
- 📁 Files: .specify/memory/constitution.md modified
- 🔁 Next prompts: Begin Phase II specification work with authorized technology stack
- 🧠 Reflection: Amendment follows semantic versioning (MINOR bump) as it adds new guidance without removing existing principles

## Evaluation notes (flywheel)

- Failure modes observed: None - amendment applied successfully
- Graders run and results (PASS/FAIL): Manual review PASS - all requested changes applied, no principle weakening
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
