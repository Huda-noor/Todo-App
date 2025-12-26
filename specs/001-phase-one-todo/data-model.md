# Data Model: Phase I - In-Memory Todo CLI

**Feature**: Phase I - In-Memory Todo CLI
**Branch**: `001-phase-one-todo`
**Date**: 2025-12-27

## Overview

Phase I uses a minimal data model with a single entity (Task) stored in-memory using native Python data structures. No database, no ORM, no persistence layer.

## Entities

### Task

Represents a single todo item in the user's task list.

**Storage Implementation**: Dictionary within a Python list

**Fields**:

| Field       | Type    | Required | Validation Rules                           | Default | Description                                    |
|-------------|---------|----------|--------------------------------------------|---------|------------------------------------------------|
| id          | int     | Yes      | Unique, sequential, > 0, never reused     | Auto-generated | Unique identifier for the task                |
| description | str     | Yes      | Non-empty after trimming whitespace       | None    | Text describing what needs to be done         |
| completed   | bool    | Yes      | Must be True or False                      | False   | Indicates whether task is complete            |

**Field Details**:

- **id**:
  - Generated sequentially starting from 1
  - Incremented for each new task
  - Never reused after deletion
  - Unique across current session
  - User-facing identifier for all operations

- **description**:
  - UTF-8 encoded text
  - No maximum length constraint
  - Leading and trailing whitespace trimmed before storage
  - Must be non-empty after trimming
  - Examples: "Buy groceries", "Call the dentist", "Finish report"

- **completed**:
  - Boolean value only (True = complete, False = incomplete)
  - Defaults to False when task is created
  - Can be toggled between True and False
  - No partial completion states

**Relationships**: None (single entity system in Phase I)

**Constraints**:

- Uniqueness: `id` must be unique within the task list
- Non-null: All three fields are required (no None values)
- Immutability: `id` cannot be changed after task creation
- Validation: `description` cannot be empty string after trimming

**Example Data Structure**:

```python
# Conceptual representation (not actual code)
tasks = [
    {'id': 1, 'description': 'Buy groceries', 'completed': False},
    {'id': 2, 'description': 'Clean the house', 'completed': True},
    {'id': 3, 'description': 'Call the dentist', 'completed': False},
]

next_id = 4  # Counter for next task ID
```

## Storage Strategy

**In-Memory Storage**:
- Global list variable containing task dictionaries
- Global integer counter for next ID
- No serialization or deserialization
- Data exists only during application runtime
- All data lost when application exits

**Rationale**:
- Simplest implementation for Phase I requirements
- No external dependencies
- Fast performance (no I/O)
- Meets specification requirement for session-based, non-persistent storage

## Data Operations

### Create Task
**Input**: description (string)
**Process**:
1. Trim whitespace from description
2. Validate non-empty
3. Generate new ID (current counter value)
4. Create dictionary: `{id, description, completed: False}`
5. Append to tasks list
6. Increment counter
**Output**: New task dictionary

### Read Tasks
**Input**: None (reads all tasks)
**Process**:
1. Return current tasks list
**Output**: List of all task dictionaries

### Read Single Task
**Input**: task_id (integer)
**Process**:
1. Search tasks list for task with matching id
2. Return task if found, None if not found
**Output**: Task dictionary or None

### Update Task
**Input**: task_id (integer), new_description (string)
**Process**:
1. Find task by ID
2. Validate task exists
3. Trim whitespace from new description
4. Validate non-empty
5. Update task's description field
**Output**: Updated task dictionary

### Delete Task
**Input**: task_id (integer)
**Process**:
1. Find task by ID
2. Validate task exists
3. Remove task from list
**Output**: None (task removed)

### Toggle Task Status
**Input**: task_id (integer)
**Process**:
1. Find task by ID
2. Validate task exists
3. Flip completed boolean (True → False or False → True)
**Output**: Updated task dictionary

## State Management

**Application State**:
- **tasks**: List of task dictionaries (initially empty)
- **next_id**: Integer counter (initially 1)

**State Transitions**:
- **Add Task**: Append to list, increment counter
- **Delete Task**: Remove from list, counter unchanged
- **Update Task**: Modify dict in place
- **Toggle Status**: Modify dict in place

**State Invariants**:
- All task IDs are unique and sequential
- All tasks have non-empty descriptions
- All tasks have valid completed boolean
- Counter never decrements
- List remains valid (no null entries)

## Data Validation

**Validation Points**:

1. **Task Creation**:
   - Description must be non-empty after trimming
   - ID auto-generated (no validation needed)
   - Completed defaults to False (no validation needed)

2. **Task Update**:
   - Task ID must exist in list
   - New description must be non-empty after trimming

3. **Task Deletion**:
   - Task ID must exist in list

4. **Status Toggle**:
   - Task ID must exist in list
   - No validation of boolean value (just flip)

**Validation Strategy**:
- Pre-condition checks before operations
- User-friendly error messages on validation failure
- No operation performed if validation fails
- Application state remains consistent after validation failure

## Performance Characteristics

**Time Complexity**:
- Create Task: O(1) - append to list
- Read All Tasks: O(1) - return reference
- Find Task by ID: O(n) - linear search
- Update Task: O(n) - linear search + O(1) update
- Delete Task: O(n) - linear search + O(n) removal
- Toggle Status: O(n) - linear search + O(1) update

**Space Complexity**:
- O(n) where n = number of tasks
- Each task: ~100 bytes (int + string + bool)
- 1000 tasks: ~100KB memory (well within limits)

**Performance Goals**:
- All operations < 1 second (easily met with in-memory list)
- Support up to 1000 tasks (linear search acceptable)
- No optimization needed for Phase I scale

## Data Integrity

**Integrity Guarantees**:
- ID uniqueness: Counter ensures monotonic increase
- No orphaned data: Single data structure
- No foreign key violations: No relationships
- No transaction conflicts: Single-threaded
- No race conditions: Single-user, single-process

**Data Loss Scenarios**:
- Application exit (expected behavior per spec)
- Application crash (expected behavior per spec)
- System shutdown (expected behavior per spec)

**Note**: Data loss on exit is intentional and specified in Phase I requirements. No recovery mechanism needed or implemented.

## Future Evolution

**Phase II and Beyond** (NOT implemented in Phase I):
- Potential migration to database (SQLModel + Neon DB)
- Potential addition of fields (priority, due_date, category)
- Potential relationships (user, project, tags)
- Potential persistence layer (file or database)

**Migration Considerations** (for future phases):
- Dictionary structure easily serializable to JSON
- Schema maps cleanly to database table
- IDs can become primary keys
- No Phase I code should assume future schema

**Important**: Phase I code must not include any scaffolding, placeholders, or assumptions about future data models. All future evolution will occur through updated specifications.

---

**End of Data Model**
