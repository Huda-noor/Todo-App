# Todo App - Evolution of Todo Project

A progressively evolving task management application built following Spec-Driven Development (SDD) principles.

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
├── src/
│   └── todo_phase1.py          # Phase I implementation
├── specs/
│   └── 001-phase-one-todo/     # Phase I artifacts
│       ├── spec.md             # Feature specification
│       ├── plan.md             # Technical plan
│       ├── tasks.md            # Implementation tasks
│       ├── data-model.md       # Data structure design
│       └── quickstart.md       # Getting started guide
├── history/
│   └── prompts/                # Development history (PHRs)
├── .specify/
│   ├── memory/
│   │   └── constitution.md     # Project governance
│   └── templates/              # SDD templates
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

This is Phase I of a multi-phase evolution:
- **Phase II**: Data persistence (file storage)
- **Phase III**: Database integration (PostgreSQL)
- **Phase IV**: Web API (FastAPI)
- **Phase V**: Frontend application (Next.js)

Each phase will be fully specified, planned, and implemented following SDD principles.

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
