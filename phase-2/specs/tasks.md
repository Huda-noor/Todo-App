# Tasks: Phase II Full-Stack Todo Web Application

**Input**: Design documents from `/specs/001-phase-ii-fullstack-todo/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/openapi.yaml
**Branch**: `001-phase-ii-fullstack-todo`
**Date**: 2025-12-28

**Tests**: Not explicitly requested - implementation tasks only.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `backend/app/` for source, `backend/tests/` for tests
- **Frontend**: `frontend/src/` for source, `frontend/tests/` for tests

---

## Phase 1: Setup (Backend & Frontend Initialization)

**Purpose**: Project structure and dependencies for both backend and frontend

### Backend Setup

- [ ] T001 Create backend project directory structure per plan.md in `backend/`
- [ ] T002 Create `backend/requirements.txt` with FastAPI, SQLModel, psycopg2-binary, pydantic-settings, uvicorn, alembic
- [ ] T003 Create `backend/app/__init__.py` package initializer
- [ ] T004 [P] Create `backend/.env.example` with DATABASE_URL, FRONTEND_URL, CORS_ORIGINS placeholders
- [ ] T005 [P] Create `backend/pytest.ini` with pytest configuration

### Frontend Setup

- [ ] T006 Initialize Next.js project with TypeScript in `frontend/` using create-next-app
- [ ] T007 Install Better Auth dependencies: `better-auth`, `@better-auth/nextjs`
- [ ] T008 [P] Create `frontend/.env.example` with BETTER_AUTH_SECRET, DATABASE_URL, NEXT_PUBLIC_API_URL placeholders
- [ ] T009 [P] Create TypeScript types file in `frontend/src/types/index.ts`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure required before ANY user story implementation

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Backend Foundation

- [ ] T010 Create environment configuration in `backend/app/config.py` using pydantic-settings
- [ ] T011 Create database connection in `backend/app/database.py` with SQLModel engine and session factory
- [ ] T012 [P] Create User model (read-only) in `backend/app/models/user.py` per data-model.md
- [ ] T013 [P] Create Session model (read-only) in `backend/app/models/session.py` per data-model.md
- [ ] T014 [P] Create Todo model in `backend/app/models/todo.py` per data-model.md
- [ ] T015 Create models package exports in `backend/app/models/__init__.py`
- [ ] T016 Initialize Alembic in `backend/alembic/` with env.py configured for SQLModel
- [ ] T017 Create initial migration for Todo table in `backend/alembic/versions/`
- [ ] T018 Create session validation dependency in `backend/app/dependencies/auth.py`
- [ ] T019 Create dependencies package exports in `backend/app/dependencies/__init__.py`
- [ ] T020 Create FastAPI app with CORS in `backend/app/main.py`

### Frontend Foundation

- [ ] T021 Create Better Auth server configuration in `frontend/src/lib/auth.ts`
- [ ] T022 Create Better Auth client instance in `frontend/src/lib/auth-client.ts`
- [ ] T023 Create API client wrapper in `frontend/src/lib/api-client.ts` with credentials and error handling
- [ ] T024 Create root layout with auth provider in `frontend/src/app/layout.tsx`
- [ ] T025 Create landing page with auth redirect logic in `frontend/src/app/page.tsx`
- [ ] T026 Create Better Auth route handler in `frontend/src/app/api/auth/[...all]/route.ts`
- [ ] T027 [P] Create reusable Button component in `frontend/src/components/ui/Button.tsx`
- [ ] T028 [P] Create reusable Input component in `frontend/src/components/ui/Input.tsx`
- [ ] T029 [P] Create Loading indicator component in `frontend/src/components/ui/Loading.tsx`

**Checkpoint**: Foundation ready - Better Auth configured, database connected, base components ready

---

## Phase 3: User Story 1 - User Signup (Priority: P1) 🎯 MVP

**Goal**: New visitors can create accounts with email and password

**Independent Test**: Visit /signup, enter valid email and password (8+ chars), verify account creation and redirect to /todos

**Acceptance Criteria** (from spec.md):
- Valid email + password (min 8 chars) creates account, redirects to /todos
- Duplicate email shows error: "An account with this email already exists"
- Invalid email format shows error: "Please enter a valid email address"
- Password < 8 chars shows error: "Password must be at least 8 characters"
- Empty fields show validation errors

### Backend for US1

- [ ] T030 [US1] Create user response schema in `backend/app/schemas/user.py`
- [ ] T031 [US1] Create schemas package exports in `backend/app/schemas/__init__.py`

### Frontend for US1

- [ ] T032 [US1] Create SignUpForm component in `frontend/src/components/auth/SignUpForm.tsx`
- [ ] T033 [US1] Create signup page in `frontend/src/app/signup/page.tsx`
- [ ] T034 [US1] Add form validation (email format, password length) to SignUpForm
- [ ] T035 [US1] Add error handling and display to SignUpForm (duplicate email, validation errors)
- [ ] T036 [US1] Add loading state and button disable during submission

**Checkpoint**: User signup fully functional - new users can create accounts

---

## Phase 4: User Story 2 - User Signin (Priority: P1) 🎯 MVP

**Goal**: Returning users can sign in with email and password

**Independent Test**: Sign in with valid credentials from existing account, verify access to /todos

**Acceptance Criteria** (from spec.md):
- Correct email + password authenticates and redirects to /todos
- Incorrect credentials show error: "Invalid email or password"
- Empty fields show validation errors
- Unauthenticated access to /todos redirects to /signin

### Frontend for US2

- [ ] T037 [US2] Create SignInForm component in `frontend/src/components/auth/SignInForm.tsx`
- [ ] T038 [US2] Create signin page in `frontend/src/app/signin/page.tsx`
- [ ] T039 [US2] Add form validation and error handling to SignInForm
- [ ] T040 [US2] Add loading state and button disable during submission
- [ ] T041 [US2] Create AuthGuard component in `frontend/src/components/auth/AuthGuard.tsx`
- [ ] T042 [US2] Add link between signin and signup pages ("Don't have an account?", "Already have an account?")

**Checkpoint**: User signin fully functional - existing users can authenticate

---

## Phase 5: User Story 3 - User Logout (Priority: P2)

**Goal**: Signed-in users can securely end their session

**Independent Test**: While logged in, click logout, verify redirect to /signin and session terminated

**Acceptance Criteria** (from spec.md):
- Click logout terminates session and redirects to /signin
- After logout, accessing /todos redirects to /signin
- Browser back button doesn't show authenticated content

### Frontend for US3

- [ ] T043 [US3] Add logout button and handler in `frontend/src/app/todos/page.tsx` header section
- [ ] T044 [US3] Implement signout call via Better Auth client
- [ ] T045 [US3] Handle post-logout redirect to /signin

**Checkpoint**: User logout functional - users can securely end sessions

---

## Phase 6: User Story 4 - Create Todo (Priority: P2)

**Goal**: Authenticated users can create new todo items

**Independent Test**: While logged in, enter description and submit, verify todo appears in list

**Acceptance Criteria** (from spec.md):
- Enter description and submit creates todo with status "incomplete"
- Empty description shows error: "Todo description cannot be empty"
- Description > 500 chars shows error: "Todo description cannot exceed 500 characters"
- Created todo persists across page refresh and re-signin

### Backend for US4

- [ ] T046 [US4] Create todo request/response schemas in `backend/app/schemas/todo.py`
- [ ] T047 [US4] Create todos router in `backend/app/routers/todos.py`
- [ ] T048 [US4] Implement POST /api/todos endpoint with validation in todos router
- [ ] T049 [US4] Register todos router in `backend/app/main.py`

### Frontend for US4

- [ ] T050 [US4] Create TodoForm component in `frontend/src/components/todos/TodoForm.tsx`
- [ ] T051 [US4] Add create todo API call in api-client.ts
- [ ] T052 [US4] Add TodoForm to todos page with validation (non-empty, max 500 chars)
- [ ] T053 [US4] Add error handling and loading state to TodoForm

**Checkpoint**: Todo creation functional - users can add new tasks

---

## Phase 7: User Story 5 - View Todo List (Priority: P2)

**Goal**: Authenticated users can view all their todos

**Independent Test**: After creating todos, navigate to /todos and verify all todos display with description, status, date

**Acceptance Criteria** (from spec.md):
- Todos display with description, completion status, and creation date
- Empty list shows message: "No todos yet. Create your first todo!"
- User sees only their own todos (not other users')

### Backend for US5

- [ ] T054 [US5] Implement GET /api/todos endpoint in todos router (user-scoped query)
- [ ] T055 [US5] Implement GET /api/todos/{id} endpoint in todos router
- [ ] T056 [US5] Create auth router with GET /api/auth/me endpoint in `backend/app/routers/auth.py`
- [ ] T057 [US5] Register auth router in `backend/app/main.py`

### Frontend for US5

- [ ] T058 [US5] Add list todos API call in api-client.ts
- [ ] T059 [US5] Create TodoItem component in `frontend/src/components/todos/TodoItem.tsx`
- [ ] T060 [US5] Create TodoList component in `frontend/src/components/todos/TodoList.tsx`
- [ ] T061 [US5] Create EmptyState component in `frontend/src/components/todos/EmptyState.tsx`
- [ ] T062 [US5] Create protected todos page in `frontend/src/app/todos/page.tsx` with AuthGuard
- [ ] T063 [US5] Add header with user email display (from GET /api/auth/me)
- [ ] T064 [US5] Display todos with description, completion status (checkbox), creation date

**Checkpoint**: Todo list view functional - users can see all their tasks

---

## Phase 8: User Story 6 - Update Todo Description (Priority: P3)

**Goal**: Authenticated users can edit todo descriptions

**Independent Test**: Click edit on existing todo, change description, save, verify change persists

**Acceptance Criteria** (from spec.md):
- Edit and save updates description and displays new text
- Empty description shows error: "Todo description cannot be empty"
- Cannot update another user's todo (returns not found)
- Description > 500 chars shows error

### Backend for US6

- [ ] T065 [US6] Implement PUT /api/todos/{id} endpoint in todos router with user ownership check

### Frontend for US6

- [ ] T066 [US6] Add update todo API call in api-client.ts
- [ ] T067 [US6] Add inline edit mode to TodoItem component (edit button, editable field, save/cancel)
- [ ] T068 [US6] Add validation and error handling for edit mode
- [ ] T069 [US6] Update TodoList state on successful edit

**Checkpoint**: Todo editing functional - users can modify task descriptions

---

## Phase 9: User Story 7 - Delete Todo (Priority: P3)

**Goal**: Authenticated users can remove todos

**Independent Test**: Click delete on existing todo, verify it's removed from list

**Acceptance Criteria** (from spec.md):
- Delete removes todo permanently from list
- Deleting non-existent todo shows error: "Todo not found"
- Cannot delete another user's todo (returns not found)

### Backend for US7

- [ ] T070 [US7] Implement DELETE /api/todos/{id} endpoint in todos router with user ownership check

### Frontend for US7

- [ ] T071 [US7] Add delete todo API call in api-client.ts
- [ ] T072 [US7] Add delete button to TodoItem component
- [ ] T073 [US7] Add delete confirmation (optional) or immediate delete with feedback
- [ ] T074 [US7] Update TodoList state on successful delete

**Checkpoint**: Todo deletion functional - users can remove tasks

---

## Phase 10: User Story 8 - Toggle Todo Completion (Priority: P3)

**Goal**: Authenticated users can mark todos complete/incomplete

**Independent Test**: Click checkbox on incomplete todo, verify it shows as complete. Click again to toggle back.

**Acceptance Criteria** (from spec.md):
- Click complete on incomplete todo changes status to complete (visual indication)
- Click incomplete on complete todo changes status back
- Toggling non-existent todo shows error: "Todo not found"
- Cannot toggle another user's todo (returns not found)

### Backend for US8

- [ ] T075 [US8] Implement PATCH /api/todos/{id}/toggle endpoint in todos router

### Frontend for US8

- [ ] T076 [US8] Add toggle todo API call in api-client.ts
- [ ] T077 [US8] Implement checkbox click handler in TodoItem
- [ ] T078 [US8] Add visual distinction for completed todos (strikethrough)
- [ ] T079 [US8] Add optimistic update with error rollback

**Checkpoint**: Todo toggle functional - users can track completion status

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Final touches and validation across all user stories

- [ ] T080 Add global error handling middleware in `backend/app/main.py`
- [ ] T081 [P] Add responsive styling to all pages (mobile-first)
- [ ] T082 [P] Ensure proper form labels and accessibility attributes
- [ ] T083 Add expired session handling (redirect with message)
- [ ] T084 Verify CORS configuration works for local development
- [ ] T085 Run quickstart.md validation (both servers, full flow test)
- [ ] T086 Verify all acceptance scenarios from spec.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies - start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 - BLOCKS all user stories
- **Phases 3-10 (User Stories)**: All depend on Phase 2 completion
- **Phase 11 (Polish)**: Depends on all user stories complete

### User Story Dependencies

| Story | Priority | Dependencies | Can Parallel With |
|-------|----------|--------------|-------------------|
| US1 Signup | P1 | Phase 2 | US2 (different pages) |
| US2 Signin | P1 | Phase 2 | US1 (different pages) |
| US3 Logout | P2 | US1 or US2 (need auth) | US4, US5 |
| US4 Create | P2 | US2 (need auth) | US5 (different endpoints) |
| US5 View | P2 | US2 (need auth) | US4 (different endpoints) |
| US6 Update | P3 | US4 or US5 (need todos) | US7, US8 |
| US7 Delete | P3 | US4 or US5 (need todos) | US6, US8 |
| US8 Toggle | P3 | US4 or US5 (need todos) | US6, US7 |

### Within Each Phase

- Tasks marked [P] can run in parallel
- Models before schemas
- Schemas before routers
- Backend endpoints before frontend API calls
- API calls before UI components

---

## Parallel Opportunities

### Phase 1 Parallel (Setup)
```
T004 [P] .env.example (backend) | T005 [P] pytest.ini
T008 [P] .env.example (frontend) | T009 [P] types/index.ts
```

### Phase 2 Parallel (Foundation)
```
T012 [P] User model | T013 [P] Session model | T014 [P] Todo model
T027 [P] Button | T028 [P] Input | T029 [P] Loading
```

### User Stories Parallel (after Phase 2)
```
US1 (Signup) | US2 (Signin) - different pages, can develop simultaneously
US4 (Create) | US5 (View) - different endpoints, can develop simultaneously
US6 (Update) | US7 (Delete) | US8 (Toggle) - different endpoints, can develop simultaneously
```

---

## Implementation Strategy

### MVP First (US1 + US2 + US4 + US5)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Signup (US1)
4. Complete Phase 4: User Signin (US2)
5. Complete Phase 6: Create Todo (US4)
6. Complete Phase 7: View Todo List (US5)
7. **STOP and VALIDATE**: Full signup → signin → create → view flow works
8. Deploy/demo MVP

### Full Feature Set

Continue with:
- Phase 5: User Logout (US3)
- Phase 8: Update Todo (US6)
- Phase 9: Delete Todo (US7)
- Phase 10: Toggle Todo (US8)
- Phase 11: Polish

### Suggested MVP Scope

**Minimum Viable Product** = US1 + US2 + US4 + US5 (Phases 1-2, 3-4, 6-7)

This delivers:
- User can signup
- User can signin
- User can create todos
- User can view their todos

All other stories enhance but aren't required for basic functionality.

---

## Task Summary

| Phase | Focus | Task Count |
|-------|-------|------------|
| 1 | Setup | 9 |
| 2 | Foundational | 20 |
| 3 | US1 Signup | 7 |
| 4 | US2 Signin | 6 |
| 5 | US3 Logout | 3 |
| 6 | US4 Create | 8 |
| 7 | US5 View | 11 |
| 8 | US6 Update | 5 |
| 9 | US7 Delete | 5 |
| 10 | US8 Toggle | 5 |
| 11 | Polish | 7 |
| **Total** | | **86** |

---

## Notes

- All tasks follow checklist format: `- [ ] TXX [P?] [US?] Description with file path`
- [P] tasks can be parallelized within their phase
- Each user story checkpoint verifies independent functionality
- Stop at any checkpoint to validate and potentially deploy
- Commit after each task or logical group
- Reference spec.md for exact acceptance criteria and error messages
