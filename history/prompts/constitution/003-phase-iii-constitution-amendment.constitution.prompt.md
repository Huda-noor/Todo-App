---
id: 003
title: Phase III Constitution Amendment
stage: constitution
date: 2026-01-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-phase-ii-fullstack-todo
user: unspecified
command: sp.constitution
labels: [constitution,amendment,phase-iii,governance]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md (amended with Phase III authorizations)
tests:
  - none
---

## Prompt

Amend the Global Constitution for the "Evolution of Todo" project to authorize Phase III capabilities while maintaining strict phase isolation, clean architecture, and all existing governance principles.

This amendment must update only the required sections to enable AI-driven conversational interface and tool usage in Phase III, without relaxing any prior rules.

Specific changes to apply:

1. **Technology Constraints (Section 4)** – Extend the technology matrix:
   - Phase I & II (unchanged): As previously defined.
   - Phase III (new authorizations):
     - AI Logic: OpenAI Agents SDK
     - Tooling & Orchestration: Model Context Protocol (MCP) with official MCP SDK
     - MCP Server: Dedicated stateless MCP endpoint exposing task operations as tools
     - Conversational Interface: Stateless chat API endpoint
     - State Management: Conversation history and task state persisted in Neon PostgreSQL (existing database)
   - Phase IV–V: Retain existing allowances for Docker, Kubernetes, Kafka, Dapr (no changes)
   - Explicit rule: OpenAI Agents SDK and MCP are prohibited in Phase I and II; permitted only from Phase III onward.

2. **Phase Governance & Isolation (Section 3)** – Strengthen:
   - No leakage of Phase III technologies (OpenAI Agents SDK, MCP, chat endpoints) into earlier phases.
   - Phase III must extend the existing full-stack application (Phase II) by adding a conversational layer on top; core Todo CRUD and authentication remain unchanged.
   - AI agents must interact with the system **exclusively** through MCP tools — no direct database access or in-memory state.

3. **Agent Behavior Rules (Section 2)** – Add Phase III-specific clauses:
   - AI agents (via OpenAI Agents SDK) must be deterministic executors that only call approved MCP tools.
   - No invention of new tools or direct manipulation of data outside MCP.
   - All agent decisions must be traceable to user intent expressed in conversation.

4. **Quality & Architecture Principles (Section 5)** – Add:
   - Stateless services: Both chat endpoint and all MCP tools must be stateless.
   - Persistence: Conversation threads and task state must be stored in the database and retrieved per request.
   - Separation of concerns: Clear boundary between AI orchestration (OpenAI Agents SDK), tool execution (MCP server), and data persistence (existing backend).
   - No autonomous agents or background processes.

5. **New Section 7: Phase III AI & Tooling Principles**
   - AI agents may ONLY manage tasks via MCP tools.
   - MCP tools must be completely stateless and rely solely on database for persistence.
   - Conversation context must be loaded from and saved to the database on every request.
   - No multi-agent swarms or orchestration beyond single-agent tool-calling pattern.
   - All tool operations must respect existing user authentication and data isolation.

Rules for this amendment:
- Preserve the entire original constitution structure and wording except for the explicit additions/modifications above.
- Maintain supreme stability: this remains the single governing document across all phases.
- Phase isolation remains absolute — no back-porting, scaffolding, or hints of Phase III tech in earlier phases.
- All prior rules (spec-driven development, no manual coding, no feature invention) remain fully enforced.

Output the complete amended Global Constitution in clean, well-structured markdown format. Clearly mark updated or new sections with a note (e.g., "[Amended for Phase III]") for traceability, while keeping the document authoritative and readable. This amended version becomes the new supreme constitution effective for Phase III onward.

## Response snapshot

Constitution amended to version 1.2.0 with Phase III authorizations:

**Updated Sections**:
- Section II (Agent Behavior Rules): Added Phase III-specific rules for AI agents requiring deterministic execution via MCP tools only
- Section III (Phase Governance & Isolation): Strengthened with Phase III isolation rules, explicit prohibition of Phase III tech in earlier phases, and requirement that Phase III extends Phase II via conversational layer
- Section IV (Technology Constraints): Expanded with complete Phase III technology authorizations (OpenAI Agents SDK, MCP, stateless services) and explicit prohibitions for Phases I & II
- Section V (Quality & Architecture Principles): Added Phase III AI & Tool Architecture subsection covering stateless services, persistence, separation of concerns, and no autonomous agents

**New Section**:
- Section VII (Phase III AI & Tooling Principles): Comprehensive rules for AI agents, conversation management, MCP tool design, and AI orchestration boundaries

**Key Governance Preserved**:
- All prior rules (spec-driven development, no manual coding, no feature invention) remain fully enforced
- Phase isolation remains absolute with explicit prohibitions against technology leakage
- Version incremented from 1.1.0 to 1.2.0 (MINOR bump for new section and material expansions)

## Outcome

- ✅ Impact: Constitution now authorizes Phase III AI and tooling capabilities while maintaining all existing governance principles and strict phase isolation
- 🧪 Tests: none (constitutional amendment)
- 📁 Files: 1 file updated (.specify/memory/constitution.md)
- 🔁 Next prompts: Continue with Phase III specification and planning
- 🧠 Reflection: Amendment successfully adds Phase III capabilities without weakening prior rules. All new tech (OpenAI Agents SDK, MCP) is explicitly phase-locked to Phase III onward with clear prohibitions for earlier phases.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): none (amendment complete)
