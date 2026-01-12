# Phase I - Data Model

## Task Entity

### Structure
```python
Task = {
    "id": int,
    "description": str,
    "completed": bool
}
```

### Field Definitions

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | integer | Unique, sequential, 1-based, never reused | Unique identifier |
| `description` | string | Non-empty after trim, UTF-8 | Task content |
| `completed` | boolean | Default: False | Completion status |

---

## Task ID Generation

### Strategy: Sequential Integer Counter

```
next_id = 1  # Initial value

# On add_task():
task_id = next_id          # Assign current ID
tasks.append(task)         # Add to list
next_id += 1               # Increment for next task
```

### Properties
- **Unique**: Each task gets a unique ID
- **Sequential**: IDs increase by 1 (1, 2, 3...)
- **1-based**: First task gets ID 1
- **Never reused**: Deleted task IDs are not reassigned

### Examples
| Operation | next_id before | Task ID | next_id after |
|-----------|----------------|---------|---------------|
| Add task | 1 | 1 | 2 |
| Add task | 2 | 2 | 3 |
| Add task | 3 | 3 | 4 |
| Delete task 2 | 4 | - | 4 |
| Add task | 4 | 4 | 5 |

---

## Description Validation

### Rules
1. Trim leading and trailing whitespace
2. Must be non-empty after trimming
3. Accepts any UTF-8 characters (emojis, symbols, non-English)

### Examples
| User Input | After Trim | Valid? | Stored |
|------------|------------|--------|--------|
| "Buy milk" | "Buy milk" | ✅ | "Buy milk" |
| "  Clean house  " | "Clean house" | ✅ | "Clean house" |
| "" | "" | ❌ | Rejected |
| "   " | "" | ❌ | Rejected |

---

## Completion Status

### Default Value
- New tasks are always `completed = False`

### Toggle Behavior
```python
# In-place modification
task['completed'] = not task['completed']

# Result
False → True  (incomplete → complete)
True → False  (complete → incomplete)
```

### Examples
| Current Status | Toggle Result | Display |
|----------------|---------------|---------|
| False | True | [X] |
| True | False | [ ] |

---

## In-Memory Storage

### Data Structure
```python
# Global variables
tasks = []      # List of task dictionaries
next_id = 1     # Counter for next task ID
```

### Storage Example
```python
# After adding 3 tasks
tasks = [
    {'id': 1, 'description': 'Buy groceries', 'completed': False},
    {'id': 2, 'description': 'Clean house', 'completed': True},
    {'id': 3, 'description': 'Call dentist', 'completed': False}
]
next_id = 4
```

### Operations Impact
| Operation | Modifies `tasks`? | Modifies `next_id`? |
|-----------|-------------------|---------------------|
| add_task | ✅ Append | ✅ Increment |
| update_task | ✅ Modify dict | ❌ No |
| delete_task | ✅ Remove dict | ❌ No |
| toggle_status | ✅ Modify dict | ❌ No |
| get_all_tasks | ❌ No (returns copy) | ❌ No |

---

## Session Isolation

### Behavior
- Data exists only during application session
- Application restart = data lost
- No file I/O, no database, no persistence

### Example
```python
# Session 1
>>> add_task("Buy milk")
Task added successfully with ID 1
>>> get_all_tasks()
[{'id': 1, 'description': 'Buy milk', 'completed': False}]
>>> exit()
Thank you for using Todo Application. Goodbye!

# Session 2 (new terminal)
>>> get_all_tasks()
No tasks found. Your list is empty.
```

---

## Validation Summary

| Field | Validation | Error Message |
|-------|------------|---------------|
| `id` | Must exist in tasks list | "Task with ID {id} not found" |
| `description` | Non-empty after trim | "Task description cannot be empty" |
| `completed` | Boolean toggle | N/A (automatic) |

---

## Extensibility for Future Phases

### Phase II (Database)
```python
# Current (Phase I)
task = {'id': 1, 'description': 'Buy milk', 'completed': False}

# Future (Phase II - database model)
class TodoModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    user_id: UUID  # Multi-user support
    description: str
    completed: bool = False
```

### Phase III (AI Integration)
- Task operations through MCP tools
- Conversation history stored separately
- Same task model, different access pattern
