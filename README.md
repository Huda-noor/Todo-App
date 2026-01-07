# Todo App - Full-Stack Task Management Application

A modern, full-stack task management application built following Spec-Driven Development (SDD) principles with authentication, real-time updates, and a beautiful user interface.

## Project Overview

The Todo App is a comprehensive task management solution featuring:
- **Multi-user Support**: User authentication via Neon Auth (Google & GitHub OAuth)
- **Persistent Storage**: PostgreSQL database via Neon
- **Modern UI**: Responsive web interface built with Next.js 14
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Real-time State Management**: Optimistic UI updates for seamless user experience

## Phase II: Full-Stack Web Application ✅

Phase II transforms the CLI application into a complete full-stack web application with user authentication and persistent database storage.

### Features

- ✅ **User Authentication** - Sign up/sign in with Google & GitHub OAuth via Neon Auth
- ✅ **User Management** - Session-based authentication with secure token handling
- ✅ **Todo CRUD Operations** - Create, read, update, delete todos
- ✅ **Todo Status Toggle** - Mark todos as complete/incomplete
- ✅ **User-Specific Data** - Each user sees only their own todos
- ✅ **Optimistic UI** - Instant feedback on all operations
- ✅ **Responsive Design** - Works on desktop and mobile devices
- ✅ **Error Handling** - Comprehensive error messages and validation

### Technical Stack

**Backend (FastAPI)**
- Python 3.13+
- FastAPI - Modern, fast web framework
- SQLModel - ORM with Pydantic models
- PostgreSQL - Persistent database via Neon
- Neon Auth - Managed authentication service
- Alembic - Database migrations

**Frontend (Next.js 14)**
- React 18+ with TypeScript
- Next.js App Router
- Tailwind CSS - Utility-first styling
- Neon Auth Client - Authentication integration
- Custom hooks for state management

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Huda-noor/Todo-App.git
cd Todo-App

# Backend Setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Create .env file in backend/
cp .env.example .env
# Edit .env with your DATABASE_URL and NEON_AUTH_URL

# Run database migrations
python -m alembic upgrade head

# Start backend server
python -m uvicorn app.main:app --reload --port 8000

# Frontend Setup (in new terminal)
cd frontend
npm install

# Create .env.local file
cp .env.example .env.local
# Edit .env.local with your NEON_AUTH_URL and API_URL

# Start frontend server
npm run dev

# Access the application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Usage Example

1. **Sign Up/Sign In**
   - Visit `http://localhost:3000`
   - Click "Get Started"
   - Sign up with email or use Google/GitHub OAuth

2. **Create Todos**
   - Enter a task description
   - Press Enter or click "Add Todo"
   - Todo appears instantly at the top of the list

3. **Manage Todos**
   - Toggle completion status by clicking the checkbox
   - Edit by clicking "Edit" button
   - Delete by clicking "Delete" button

4. **View Progress**
   - See your email in the header
   - Sign out anytime using the "Sign Out" button

## Phase I: In-Memory Todo CLI ✅

Phase I delivers a simple, single-user console application for task management with in-memory storage.

### Features

- ✅ **Add Tasks** - Create new tasks with auto-generated sequential IDs
- ✅ **View Tasks** - Display all tasks with completion status ([X] complete, [ ] incomplete)
- ✅ **Update Tasks** - Modify task descriptions by ID
- ✅ **Delete Tasks** - Remove tasks by ID (IDs never reused)
- ✅ **Toggle Status** - Mark tasks as complete or incomplete
- ✅ **Graceful Error Handling** - User-friendly error messages for all edge cases

### Technical Stack

- **Language**: Python 3.13+ (standard library only)
- **Architecture**: Clean architecture with three layers
  - Data Layer: Task storage and CRUD operations
  - Presentation Layer: CLI interface and user interaction
  - Control Flow: Menu handlers and main application loop
- **Storage**: In-memory only (data lost on exit)
- **Dependencies**: None (no external packages)

### Quick Start

```bash
# Clone the repository
git clone https://github.com/Huda-noor/Todo-App.git
cd Todo-App

# Run the application
python src/todo_phase1.py
```

### Usage Example

```
========================================
=== Todo Application - Phase I ===
========================================

Main Menu:
1. Add a new task
2. View all tasks
3. Update a task
4. Delete a task
5. Mark task as complete/incomplete
6. Exit

Enter your choice (1-6): 1
Enter task description: Buy groceries
Task added successfully with ID 1

Enter your choice (1-6): 2

========================================
=== Your Tasks ===
========================================
1. [ ] Buy groceries

Total: 1 tasks (0 complete, 1 incomplete)
```

### Architecture

The application follows clean architecture principles with clear separation of concerns:

**Data Layer (`add_task()`, `find_task_by_id()`, `update_task()`, etc.)**
- Pure functions for task management
- No dependencies on presentation layer
- In-memory storage with list of dictionaries

**Presentation Layer (`display_menu()`, `get_task_description()`, etc.)**
- User input/output handling
- Input validation and error display
- Formatted task list display

**Control Flow (`handle_add_task()`, `handle_view_tasks()`, `main()`, etc.)**
- Orchestrates data and presentation layers
- Menu dispatch and application loop
- Business logic coordination

### Development Process

This project follows strict **Spec-Driven Development (SDD)**:

1. **Constitution** → Project principles and governance
2. **Specification** → User stories and acceptance criteria
3. **Technical Plan** → Architecture decisions and design
4. **Task Breakdown** → Atomic implementation work units
5. **Implementation** → Code execution following tasks

All artifacts are version-controlled in the repository:
- `specs/001-phase-one-todo/` - Phase I specification and planning
- `history/prompts/` - Complete development history (Prompt History Records)
- `.specify/` - Project templates and constitution

### Constitutional Principles

- ✅ **Spec-Driven Development**: All code derives from approved specifications
- ✅ **Phase Isolation**: No future-phase features or scaffolding
- ✅ **Clean Architecture**: Separation of concerns enforced
- ✅ **Quality First**: No technical debt or shortcuts
- ✅ **Deterministic Behavior**: Predictable, testable code

### Project Structure

```
Todo-App/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI application entry
│   │   ├── config.py          # Configuration management
│   │   ├── database.py        # Database connection
│   │   ├── models/            # SQLModel models
│   │   │   ├── user.py        # User model
│   │   │   ├── todo.py        # Todo model
│   │   │   └── session.py     # Session model
│   │   ├── schemas/           # Pydantic schemas
│   │   │   ├── user.py        # User schemas
│   │   │   └── todo.py        # Todo schemas
│   │   ├── routers/           # API routes
│   │   │   ├── auth.py        # Authentication endpoints
│   │   │   └── todos.py       # Todo CRUD endpoints
│   │   └── dependencies/      # FastAPI dependencies
│   │       └── auth.py        # Auth dependency injection
│   ├── alembic/
│   │   ├── versions/          # Database migrations
│   │   └── env.py             # Alembic configuration
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   └── alembic.ini            # Alembic config
├── frontend/                   # Next.js frontend
│   ├── src/
│   │   ├── app/               # App router pages
│   │   │   ├── layout.tsx     # Root layout
│   │   │   ├── page.tsx       # Landing page
│   │   │   ├── signin/
│   │   │   │   └── page.tsx   # Sign in page
│   │   │   ├── signup/
│   │   │   │   └── page.tsx   # Sign up page
│   │   │   └── todos/
│   │   │       └── page.tsx   # Todos page
│   │   ├── components/
│   │   │   ├── auth/          # Auth components
│   │   │   │   ├── AuthGuard.tsx
│   │   │   │   ├── SignInForm.tsx
│   │   │   │   └── SignUpForm.tsx
│   │   │   ├── todos/         # Todo components
│   │   │   │   ├── TodoList.tsx
│   │   │   │   ├── TodoItem.tsx
│   │   │   │   ├── TodoForm.tsx
│   │   │   │   └── EmptyState.tsx
│   │   │   └── ui/            # UI components
│   │   │       ├── Button.tsx
│   │   │       ├── Input.tsx
│   │   │       └── Loading.tsx
│   │   ├── lib/
│   │   │   ├── auth-client.ts # Neon Auth client
│   │   │   ├── api-client.ts  # API client
│   │   │   └── types.ts       # TypeScript types
│   │   └── styles/
│   │       └── globals.css    # Global styles (Tailwind)
│   ├── package.json           # Node dependencies
│   ├── tsconfig.json          # TypeScript config
│   ├── tailwind.config.js     # Tailwind config
│   ├── next.config.js         # Next.js config
│   └── .env.local             # Environment variables
├── src/
│   └── todo_phase1.py          # Phase I implementation
├── specs/
│   ├── 001-phase-one-todo/     # Phase I artifacts
│   │   ├── spec.md
│   │   ├── plan.md
│   │   ├── tasks.md
│   │   ├── data-model.md
│   │   └── quickstart.md
│   └── 002-phase-ii-fullstack-todo/  # Phase II artifacts
│       ├── spec.md             # Phase II specification
│       ├── plan.md             # Technical plan
│       └── tasks.md            # Implementation tasks
├── history/
│   ├── prompts/
│   │   ├── 001-phase-one-todo/
│   │   └── 002-phase-ii-fullstack-todo/  # Phase II PHRs
│   └── adr/                    # Architecture Decision Records
├── .specify/
│   ├── memory/
│   │   └── constitution.md     # Project governance
│   ├── templates/              # SDD templates
│   └── scripts/                # Utility scripts
├── .gitignore
└── README.md
```

### Testing

Phase I includes comprehensive manual testing scenarios:
- Add/view/update/delete/toggle operations
- Error handling (invalid IDs, empty descriptions)
- Edge cases (empty list, whitespace, special characters)
- Performance (50-100 tasks)
- Usability (self-explanatory interface)

See `specs/001-phase-one-todo/tasks.md` (Tasks 034-042) for detailed test scenarios.

### Future Phases

This is Phase II of the Todo App evolution. Previous phases:
- **Phase I**: In-memory CLI (completed)
- **Phase II**: Full-stack web application with authentication (current)

Each phase is fully specified, planned, and implemented following SDD principles.

### Contributing

This project follows strict Spec-Driven Development. All changes must:
1. Have an approved specification
2. Follow the technical plan
3. Maintain constitutional compliance
4. Pass all acceptance criteria

### License

MIT License - Feel free to use and modify for your projects.

### Credits

Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
