# Phase I - In-Memory Todo CLI

**Feature Branch**: `phase-1/core` | **Status**: Implemented
**Constitution**: [phase-i-constitution.md](../constitution/phase-i-constitution.md)

## Overview

Phase I delivers a single-file, in-memory, console-based Todo application in Python implementing basic CRUD operations. The application maintains strict phase isolation with no persistence, no external dependencies, and no future-phase scaffolding.

---

## Features Delivered

| Feature | Status | Priority |
|---------|--------|----------|
| Add new task | ✅ Complete | P1 |
| View all tasks | ✅ Complete | P1 |
| Toggle completion | ✅ Complete | P1 |
| Update task | ✅ Complete | P2 |
| Delete task | ✅ Complete | P2 |

---

## User Stories & Acceptance

### Story 1: Add Task ✅
- Task receives unique sequential ID starting at 1
- Description validated (non-empty after trim)
- Confirmation displayed on success

### Story 2: View Tasks ✅
- All tasks displayed with status indicators
- Empty list shows friendly message
- Summary count displayed

### Story 3: Toggle Completion ✅
- Status toggles between complete/incomplete
- Idempotent operation
- Clear confirmation message

### Story 4: Update Task ✅
- Task identified by ID
- New description validated
- Success/error feedback

### Story 5: Delete Task ✅
- Task identified by ID
- Permanent removal from memory
- Success/error feedback

---

## Technical Implementation

### Data Layer
```python
# Global task storage
tasks = []          # List of task dictionaries
next_id = 1         # Sequential ID counter

# Functions
add_task(description) → task_id
get_all_tasks() → list
find_task_by_id(task_id) → dict|None
update_task(task_id, description) → bool
delete_task(task_id) → bool
toggle_task_status(task_id) → bool|None
```

### Presentation Layer
```python
display_main_menu()     # Print menu options
get_menu_choice() → int # Validate and return choice
get_task_description() → str|None
get_task_id(prompt) → int|None
display_task_list()     # Format and print tasks
display_confirmation(msg)
display_error(msg)
```

### Control Flow
```python
main()  # Main application loop
handle_add_task()
handle_view_tasks()
handle_update_task()
handle_delete_task()
handle_toggle_status()
handle_exit() → bool
```

---

## Data Model

```python
Task = {
    "id": int,           # 1, 2, 3... (never reused)
    "description": str,  # Non-empty, trimmed
    "completed": bool    # False default
}
```

---

## CLI Interaction

### Main Menu
```
=== Todo Application - Phase I ===

Main Menu:
1. Add a new task
2. View all tasks
3. Update a task
4. Delete a task
5. Mark task as complete/incomplete
6. Exit

Enter your choice (1-6):
```

### Task List Display
```
=== Your Tasks ===
1. [ ] Buy groceries
2. [X] Clean the house
3. [ ] Call the dentist

Total: 3 tasks (1 complete, 2 incomplete)
```

---

## Usage

```bash
# Run the application
python src/todo_phase1.py

# Or from phase-1 directory
python source-code/todo_phase1.py
```

---

## Verification

| Test | Status |
|------|--------|
| Add task creates with unique ID | ✅ |
| View displays all tasks | ✅ |
| Toggle changes status | ✅ |
| Update modifies description | ✅ |
| Delete removes task | ✅ |
| Empty description rejected | ✅ |
| Invalid ID shows error | ✅ |
| Session isolation (no persistence) | ✅ |

---

## Files Reference

| Path | Purpose |
|------|---------|
| `source-code/todo_phase1.py` | Main application |
| `specs/spec.md` | Feature specification |
| `specs/plan.md` | Implementation plan |
| `specs/tasks.md` | Task breakdown |
| `data-models/task-model.md` | Data structure |
| `constitution/phase-i-constitution.md` | Phase I constitution |

---

**Phase I Complete** — Ready for Phase II transition
