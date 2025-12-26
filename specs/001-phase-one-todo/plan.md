# Implementation Plan: Phase I - In-Memory Todo CLI

**Branch**: `001-phase-one-todo` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase-one-todo/spec.md`

## Summary

Phase I delivers a single-file, in-memory, console-based Todo application in Python implementing basic CRUD operations (Add, View, Update, Delete, Mark Complete/Incomplete). The application maintains strict phase isolation with no persistence, no external dependencies, and no future-phase scaffolding. Architecture follows clean separation of concerns with distinct data and presentation layers.

## Technical Context

**Language/Version**: Python 3.8+ (minimum version for compatibility; no version-specific features required)
**Primary Dependencies**: None (Python standard library only)
**Storage**: In-memory list of dictionaries (no persistence)
**Testing**: Manual testing via CLI (automated testing not specified for Phase I)
**Target Platform**: Any OS with Python 3.8+ installed (Windows, Linux, macOS)
**Project Type**: Single-file console application
**Performance Goals**: < 1 second response time for all operations, handles up to 1000 tasks
**Constraints**: No file I/O, no database, no external libraries, no network, single-user only, session-based (data lost on exit)
**Scale/Scope**: Single user, single session, up to 1000 tasks per session

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Spec-Driven Development Compliance
- ✅ **Implementation derives exclusively from specification**: All features map directly to FR-001 through FR-016
- ✅ **No feature invention or assumption**: Only specified CRUD operations included
- ✅ **Specification defines WHAT, plan defines HOW**: Clear separation maintained

### Phase Governance & Isolation Compliance
- ✅ **No future-phase features**: No FastAPI, SQLModel, Neon DB, Next.js, Docker, Kubernetes, Kafka, Dapr
- ✅ **No database or file I/O**: In-memory only as specified
- ✅ **No web/API scaffolding**: Console-only as specified
- ✅ **No multi-user preparation**: Single-user as specified
- ✅ **No persistence scaffolding**: Session-based as specified

### Technology Constraints Compliance
- ✅ **Python only**: No other languages used
- ✅ **Standard library only**: No external dependencies
- ✅ **No framework imports**: No FastAPI, Flask, Django, or any web frameworks

### Quality & Architecture Principles Compliance
- ✅ **Clean Architecture**: Separation of data layer and presentation layer
- ✅ **Separation of Concerns**: Distinct responsibilities for storage, business logic, and UI
- ✅ **Modular Design**: Functions organized by responsibility
- ✅ **Deterministic Behavior**: Same inputs produce same outputs
- ✅ **Stateless Operations**: Each operation is independent (within session state)

### Agent Behavior Compliance
- ✅ **No optimizations beyond specification**: Only specified features included
- ✅ **No "improvements"**: Strict adherence to requirements
- ✅ **Testable requirements**: All features have clear acceptance criteria

**Status**: ✅ ALL GATES PASSED - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-phase-one-todo/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (technical decisions)
├── data-model.md        # Phase 1 output (data structure design)
├── quickstart.md        # Phase 1 output (how to run the application)
└── checklists/
    └── requirements.md  # Specification quality checklist
```

### Source Code (repository root)

```text
src/
└── todo_cli.py          # Single-file application (main entry point)

tests/                   # Future phase (not included in Phase I)
```

**Structure Decision**: Single-file application at `src/todo_cli.py` as this is the simplest structure for Phase I requirements. No modules, packages, or multiple files needed. The single file contains all data layer and presentation layer logic.

**Rationale**:
- Specification explicitly states "single-file" application
- No complexity justification needed for multi-file structure
- Maintains maximum simplicity for Phase I
- Future phases can evolve structure through updated specifications

## Complexity Tracking

> **No constitutional violations - this section intentionally left empty**

All architectural decisions align with constitutional principles:
- Single-file structure is the simplest approach
- No additional complexity beyond requirements
- No future-phase scaffolding
- No external dependencies

---

## Phase 0: Research & Technical Decisions

### Python Version Selection

**Decision**: Python 3.8 minimum

**Rationale**:
- Python 3.8+ widely available across platforms (released 2019)
- No version-specific features needed for Phase I requirements
- Provides good balance of compatibility and modern language features
- Standard library functionality (input(), print(), list, dict) unchanged since Python 2
- Allows users with Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13 to run application

**Alternatives Considered**:
- Python 3.6: Too old, approaching end-of-life
- Python 3.12: Too new, reduces user compatibility
- Python 2.7: Deprecated, security issues

### Data Structure Selection

**Decision**: List of dictionaries for task storage

**Rationale**:
- Native Python data structures (no classes needed for MVP)
- Simple to understand and maintain
- Efficient for Phase I scale (up to 1000 tasks)
- Easy to iterate, filter, and modify
- No serialization/deserialization complexity (in-memory only)
- Dictionary provides named fields (id, description, completed)

**Schema**:
```python
# Conceptual structure (not actual code)
tasks = [
    {'id': 1, 'description': 'Buy groceries', 'completed': False},
    {'id': 2, 'description': 'Clean house', 'completed': True},
]
```

**Alternatives Considered**:
- Custom Task class: Over-engineering for Phase I (violates simplicity principle)
- Tuple/List: Less readable, no named fields
- Named tuple: Additional complexity without clear benefit

### ID Generation Strategy

**Decision**: Sequential integer counter starting at 1

**Rationale**:
- Simple to implement with a single integer variable
- Human-readable IDs (1, 2, 3... not UUIDs)
- Meets specification requirement "unique, sequential integer ID starting from 1"
- No ID reuse after deletion (counter only increments)
- Deterministic behavior (always generates next integer)

**Implementation Approach**:
- Maintain `next_id` counter initialized to 1
- Increment after each task creation
- Never decrement (even after deletions)

**Alternatives Considered**:
- UUID: Overkill for single-user, in-memory system
- Timestamp-based: Not sequential as specified
- Hash-based: Unnecessary complexity

### Input Validation Strategy

**Decision**: Defensive validation with try-except for type safety

**Rationale**:
- User input is always strings (from CLI)
- Need to convert to integers for task IDs
- Must handle non-numeric input gracefully
- Trim whitespace from descriptions per FR-015
- Validate non-empty descriptions per FR-002

**Validation Rules**:
1. Task ID: Must be convertible to integer, must exist in task list
2. Description: Must be non-empty after trimming whitespace
3. Menu choice: Must be integer 1-6

**Alternatives Considered**:
- Regular expressions: Overkill for simple integer/string validation
- External validation library: Violates no-dependencies constraint

### Error Handling Strategy

**Decision**: User-friendly error messages with graceful recovery

**Rationale**:
- NFR-008: Handle invalid input without crashing
- NFR-004 & NFR-005: Clear error messages explain what went wrong
- All errors return user to main menu (never exit on error)
- Errors printed to console, then menu re-displayed

**Error Categories**:
1. **Invalid Task ID**: "Error: Task with ID {id} not found"
2. **Empty Description**: "Error: Task description cannot be empty"
3. **Invalid Input Type**: "Error: Invalid task ID. Please enter a number"
4. **Invalid Menu Choice**: "Error: Invalid choice. Please enter a number between 1 and 6"

**Alternatives Considered**:
- Silent failures: Violates usability requirements
- Exception propagation: Would crash application
- Error codes: Less user-friendly than messages

### CLI Display Format

**Decision**: Text-based menu with numbered options and checkbox-style status indicators

**Rationale**:
- NFR-004: Clearly labeled, numbered menu options
- Specification example shows "[X]" for complete, "[ ]" for incomplete
- Simple, universally compatible (no special characters needed)
- Matches specification's CLI interaction flows exactly

**Display Conventions**:
- Menu: Numbered 1-6 with descriptive labels
- Task list: Format `ID. [STATUS] Description`
- Status: `[X]` for complete, `[ ]` for incomplete
- Empty list message: "No tasks found. Your list is empty."
- Confirmation messages: "{Action} {ID} successfully"

**Alternatives Considered**:
- Checkmark symbols (✓/✗): May not render in all terminals
- Color coding: Not specified, adds complexity
- Table format: Over-engineering for Phase I

## Phase 1: Design Artifacts

### Data Model

See [data-model.md](./data-model.md) for complete entity and field definitions.

**Summary**:
- **Task Entity**: 3 fields (id: int, description: str, completed: bool)
- **Validation Rules**: Non-empty description (after trim), unique ID, boolean status
- **Relationships**: None (single entity system)

### Architecture Design

**Layer Separation**:

1. **Data Layer** (Task Storage & Operations)
   - Responsibility: Maintain task list, generate IDs, perform CRUD operations
   - Functions:
     - Initialize storage (empty list + counter)
     - Add task (validate, assign ID, append to list)
     - Get all tasks (return list copy)
     - Find task by ID (search list, return task or None)
     - Update task description (find + modify)
     - Delete task (find + remove from list)
     - Toggle task status (find + flip boolean)

2. **Presentation Layer** (CLI Interface)
   - Responsibility: Display menu, get input, show results, format output
   - Functions:
     - Display main menu (print numbered options)
     - Get menu choice (input + validate integer 1-6)
     - Display task list (format and print all tasks)
     - Get task description (input + validate non-empty)
     - Get task ID (input + validate integer + exists)
     - Display confirmation message (print success)
     - Display error message (print error)

3. **Control Flow** (Main Loop)
   - Responsibility: Coordinate data and presentation layers
   - Functions:
     - Main loop (display menu → get choice → dispatch → repeat)
     - Command dispatcher (route choice to appropriate handler)
     - Handler functions for each menu option

**Dependencies**:
- Presentation layer depends on Data layer (calls CRUD functions)
- Data layer has no dependencies (pure logic)
- Control flow coordinates both layers

**Rationale**: This separation enables independent testing (future phase) and maintains clean architecture principles from constitution.

### Feature Implementation Strategy

#### Feature 1: Add Task

**Flow**:
1. Presentation: Display "Enter task description:"
2. Presentation: Get user input (string)
3. Presentation: Trim whitespace from input
4. Presentation: Validate non-empty (if empty, show error and return to menu)
5. Data: Generate next ID (increment counter)
6. Data: Create task dictionary {id, description, completed: False}
7. Data: Append task to list
8. Presentation: Display "Task added successfully with ID {id}"
9. Control: Return to main menu

**Edge Cases**:
- Empty string: Validation catches, displays error
- Whitespace-only: Trim makes empty, validation catches
- Very long description: Accepted as-is (no max length limit in spec)

#### Feature 2: View Tasks

**Flow**:
1. Data: Get all tasks (return list)
2. Presentation: Check if list is empty
3. If empty: Display "No tasks found. Your list is empty." and return
4. If not empty: Display header "=== Your Tasks ==="
5. Presentation: For each task, format and print: "{id}. [{status}] {description}"
6. Presentation: Count completed and incomplete tasks
7. Presentation: Display summary "Total: {total} tasks ({complete} complete, {incomplete} incomplete)"
8. Control: Return to main menu

**Display Format**:
```
=== Your Tasks ===
1. [ ] Buy groceries
2. [X] Clean the house
3. [ ] Call the dentist

Total: 3 tasks (1 complete, 2 incomplete)
```

**Edge Cases**:
- Empty list: Display special message, no error
- Single task: Display correctly with summary
- All complete/incomplete: Summary reflects actual counts

#### Feature 3: Update Task

**Flow**:
1. Presentation: Display "Enter task ID to update:"
2. Presentation: Get user input (string)
3. Presentation: Validate input is integer (try-except)
4. If invalid: Display "Error: Invalid task ID. Please enter a number" and return
5. Data: Find task by ID (search list)
6. If not found: Display "Error: Task with ID {id} not found" and return
7. Presentation: Display "Enter new description:"
8. Presentation: Get user input (string)
9. Presentation: Trim whitespace
10. Presentation: Validate non-empty
11. If empty: Display "Error: Task description cannot be empty" and return
12. Data: Update task description (modify dict in list)
13. Presentation: Display "Task {id} updated successfully"
14. Control: Return to main menu

**Edge Cases**:
- Non-numeric ID: Try-except catches, displays error
- Non-existent ID: Search returns None, displays error
- Empty new description: Validation catches, displays error

#### Feature 4: Delete Task

**Flow**:
1. Presentation: Display "Enter task ID to delete:"
2. Presentation: Get user input (string)
3. Presentation: Validate input is integer (try-except)
4. If invalid: Display "Error: Invalid task ID. Please enter a number" and return
5. Data: Find task by ID (search list)
6. If not found: Display "Error: Task with ID {id} not found" and return
7. Data: Remove task from list (list.remove)
8. Presentation: Display "Task {id} deleted successfully"
9. Control: Return to main menu

**Edge Cases**:
- Non-numeric ID: Try-except catches, displays error
- Non-existent ID: Search returns None, displays error
- Last task deleted: List becomes empty (valid state)
- Deleted ID not reused: Counter never decrements

#### Feature 5: Mark Complete/Incomplete

**Flow**:
1. Presentation: Display "Enter task ID to toggle status:"
2. Presentation: Get user input (string)
3. Presentation: Validate input is integer (try-except)
4. If invalid: Display "Error: Invalid task ID. Please enter a number" and return
5. Data: Find task by ID (search list)
6. If not found: Display "Error: Task with ID {id} not found" and return
7. Data: Toggle completed status (if True → False, if False → True)
8. Presentation: Display "Task {id} marked as {complete|incomplete}"
9. Control: Return to main menu

**Edge Cases**:
- Already complete: Toggles to incomplete (idempotent operation)
- Already incomplete: Toggles to complete (idempotent operation)
- Non-numeric ID: Try-except catches, displays error
- Non-existent ID: Search returns None, displays error

#### Feature 6: Exit Application

**Flow**:
1. Presentation: Display "Thank you for using Todo Application. Goodbye!"
2. Control: Exit main loop
3. Program terminates

**Edge Cases**: None (always succeeds)

### Error Handling and Edge Cases

**Comprehensive Error Strategy**:

1. **Type Errors** (user enters text when number expected):
   - Catch with try-except on int() conversion
   - Display "Error: Invalid task ID. Please enter a number"
   - Return to main menu (never crash)

2. **Value Errors** (user enters valid type but invalid value):
   - Empty description: Validation before processing
   - Non-existent ID: Search returns None, check before operating
   - Display appropriate error message
   - Return to main menu

3. **Empty List Operations**:
   - View tasks: Display "No tasks found" (not an error)
   - Update/Delete/Toggle on empty list: ID won't exist, shows "not found" error

4. **Unexpected Input**:
   - Very large numbers: Treated as non-existent ID
   - Negative numbers: Treated as non-existent ID
   - Special characters: Try-except catches, shows invalid input error

5. **Application State**:
   - No invalid states possible (list always valid, IDs always unique)
   - No race conditions (single-user, single-threaded)
   - No data corruption risk (in-memory, no I/O)

**Recovery Path**: All errors return to main menu with clear message. User can immediately retry or choose different action. Application never exits due to user error.

### Main Application Flow

**Pseudocode** (not actual code):

```
INITIALIZE:
  tasks = empty list
  next_id = 1

FUNCTION main():
  WHILE True:
    DISPLAY main menu
    choice = GET user input (1-6)

    IF choice == 1:
      CALL handle_add_task()
    ELSE IF choice == 2:
      CALL handle_view_tasks()
    ELSE IF choice == 3:
      CALL handle_update_task()
    ELSE IF choice == 4:
      CALL handle_delete_task()
    ELSE IF choice == 5:
      CALL handle_toggle_status()
    ELSE IF choice == 6:
      DISPLAY goodbye message
      EXIT loop
    ELSE:
      DISPLAY "Invalid choice" error

FUNCTION handle_add_task():
  description = GET input "Enter task description:"
  description = TRIM whitespace

  IF description is empty:
    DISPLAY error "Task description cannot be empty"
    RETURN

  task = CREATE {id: next_id, description: description, completed: False}
  ADD task to tasks list
  INCREMENT next_id
  DISPLAY "Task added successfully with ID {id}"

FUNCTION handle_view_tasks():
  IF tasks list is empty:
    DISPLAY "No tasks found. Your list is empty."
    RETURN

  DISPLAY "=== Your Tasks ==="
  FOR each task in tasks:
    status = "[X]" if task.completed else "[ ]"
    DISPLAY "{task.id}. {status} {task.description}"

  complete_count = COUNT tasks where completed == True
  incomplete_count = COUNT tasks where completed == False
  DISPLAY "Total: {len(tasks)} tasks ({complete_count} complete, {incomplete_count} incomplete)"

FUNCTION handle_update_task():
  id_input = GET input "Enter task ID to update:"

  TRY:
    task_id = CONVERT id_input to integer
  EXCEPT:
    DISPLAY error "Invalid task ID. Please enter a number"
    RETURN

  task = FIND task in tasks where id == task_id
  IF task is None:
    DISPLAY error "Task with ID {task_id} not found"
    RETURN

  new_description = GET input "Enter new description:"
  new_description = TRIM whitespace

  IF new_description is empty:
    DISPLAY error "Task description cannot be empty"
    RETURN

  task.description = new_description
  DISPLAY "Task {task_id} updated successfully"

FUNCTION handle_delete_task():
  id_input = GET input "Enter task ID to delete:"

  TRY:
    task_id = CONVERT id_input to integer
  EXCEPT:
    DISPLAY error "Invalid task ID. Please enter a number"
    RETURN

  task = FIND task in tasks where id == task_id
  IF task is None:
    DISPLAY error "Task with ID {task_id} not found"
    RETURN

  REMOVE task from tasks list
  DISPLAY "Task {task_id} deleted successfully"

FUNCTION handle_toggle_status():
  id_input = GET input "Enter task ID to toggle status:"

  TRY:
    task_id = CONVERT id_input to integer
  EXCEPT:
    DISPLAY error "Invalid task ID. Please enter a number"
    RETURN

  task = FIND task in tasks where id == task_id
  IF task is None:
    DISPLAY error "Task with ID {task_id} not found"
    RETURN

  task.completed = NOT task.completed
  status_text = "complete" if task.completed else "incomplete"
  DISPLAY "Task {task_id} marked as {status_text}"

ENTRY POINT:
  CALL main()
```

### Non-Functional Considerations

**Responsiveness** (NFR-001, NFR-002, NFR-003):
- All operations are in-memory: instant response (< 1 millisecond)
- No I/O operations: no waiting for disk/network
- Linear search through list: O(n) acceptable for up to 1000 tasks
- Application startup: Python interpreter + script load (< 3 seconds)

**Deterministic Behavior** (NFR-009):
- No randomness: ID generation is sequential
- No timestamps: status is boolean only
- No external dependencies: behavior fully controlled
- Same inputs always produce same outputs

**Code Organization** (NFR-011, NFR-012):
- Functions grouped by layer (data functions together, presentation functions together)
- Meaningful names (add_task, find_task_by_id, display_menu)
- Data layer independent of presentation (can be tested separately)
- Single file structure: all code in logical order (imports, data layer, presentation, control, main)

**Input Validation** (NFR-014, NFR-015):
- All user inputs validated before processing
- Type checking with try-except
- Value checking before database operations
- Trim whitespace per specification
- No internal errors exposed to user

## Constitutional Compliance Verification

### Phase Isolation Verification ✅

**Confirmed Exclusions**:
- ❌ No FastAPI, Flask, Django (web frameworks)
- ❌ No SQLModel, SQLAlchemy, Neon DB (databases)
- ❌ No file I/O (open, read, write, json, pickle)
- ❌ No Next.js references (frontend)
- ❌ No Docker, Kubernetes (infrastructure)
- ❌ No Kafka, Dapr (distributed systems)
- ❌ No API endpoints, REST concepts
- ❌ No authentication, user management
- ❌ No persistence layer, DAO pattern for future use

**Confirmed Inclusions Only**:
- ✅ Python standard library only (input, print, list, dict)
- ✅ In-memory storage (list of dicts)
- ✅ Console I/O only (stdin/stdout)
- ✅ Single-user, single-session
- ✅ Basic CRUD operations as specified

### Technology Stack Verification ✅

**Allowed for Phase I**:
- ✅ Python (constitutional technology for backend)
- ✅ Standard library (no restriction on built-ins)

**Prohibited and Not Used**:
- ❌ External pip packages
- ❌ Framework imports
- ❌ Database drivers
- ❌ Network libraries

### Quality Principles Verification ✅

- ✅ **Clean Architecture**: Data and presentation layers separated
- ✅ **Separation of Concerns**: Each function has single responsibility
- ✅ **Modular Design**: Functions are independently testable (future phase)
- ✅ **Deterministic**: No randomness or external dependencies
- ✅ **Cloud-Native Ready**: Architecture can scale (future phases will add persistence, etc.)

## Next Steps

This plan is complete. Next commands:

1. **`/sp.tasks`** - Generate task breakdown from this plan
2. **`/sp.implement`** - Execute tasks and implement the application

---

**End of Implementation Plan**
