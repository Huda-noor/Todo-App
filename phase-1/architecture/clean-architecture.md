# Phase I - Architecture

## Clean Architecture Layers

```
┌─────────────────────────────────────────────────────────┐
│                    CONTROL FLOW                          │
│                  (Main Loop & Handlers)                  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │                 PRESENTATION LAYER                 │  │
│  │        (CLI Interface & User Interaction)          │  │
│  │                                                   │  │
│  │  - display_main_menu()     - get_menu_choice()    │  │
│  │  - get_task_description()  - get_task_id()        │  │
│  │  - display_task_list()     - display_confirmation │  │
│  │  - display_error()                                │  │
│  └───────────────────────────────────────────────────┘  │
│                         ▲                                │
│                         │ calls                          │
│                         ▼                                │
│  ┌───────────────────────────────────────────────────┐  │
│  │                    DATA LAYER                      │  │
│  │              (Storage & CRUD Operations)           │  │
│  │                                                   │  │
│  │  - add_task()            - update_task()          │  │
│  │  - get_all_tasks()       - delete_task()          │  │
│  │  - find_task_by_id()     - toggle_task_status()   │  │
│  │                                                   │  │
│  │  Global State:                                    │  │
│  │  - tasks = []                                     │  │
│  │  - next_id = 1                                    │  │
│  └───────────────────────────────────────────────────┘  │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Layer Responsibilities

### Data Layer
**Responsibility**: Maintain task list and perform CRUD operations

| Function | Input | Output | Side Effect |
|----------|-------|--------|-------------|
| `add_task(description)` | string | int (task_id) | Appends to tasks list, increments next_id |
| `get_all_tasks()` | none | list | Returns copy of tasks |
| `find_task_by_id(id)` | int | dict\|None | None (read-only) |
| `update_task(id, desc)` | int, string | bool | Modifies task dict |
| `delete_task(id)` | int | bool | Removes from tasks list |
| `toggle_task_status(id)` | int | bool\|None | Modifies task dict |

**Design Decisions**:
- Functions are pure operations (no I/O)
- Return copies or booleans, not internal state references
- Deterministic behavior (same inputs = same outputs)

### Presentation Layer
**Responsibility**: Display information and collect user input

| Function | Input | Output | Purpose |
|----------|-------|--------|---------|
| `display_main_menu()` | none | printed menu | Show options |
| `get_menu_choice()` | none | int (1-6) | Validate input |
| `get_task_description()` | none | str\|None | Get validated description |
| `get_task_id(prompt)` | string | int\|None | Get validated ID |
| `display_task_list()` | none | printed list | Format and show tasks |
| `display_confirmation()` | string | printed message | Success feedback |
| `display_error()` | string | printed error | Error feedback |

**Design Decisions**:
- All validation happens here (not in data layer)
- User-friendly messages
- No business logic

### Control Flow
**Responsibility**: Coordinate data and presentation layers

| Handler | Purpose |
|---------|---------|
| `handle_add_task()` | Orchestrate add flow |
| `handle_view_tasks()` | Orchestrate view flow |
| `handle_update_task()` | Orchestrate update flow |
| `handle_delete_task()` | Orchestrate delete flow |
| `handle_toggle_status()` | Orchestrate toggle flow |
| `handle_exit()` | Clean termination |
| `main()` | Main application loop |

---

## Data Flow

### Add Task Flow
```
User Input → Presentation → Validation → Data Layer → Storage
              ↓                               ↓
        Display Menu                  Append to tasks
              ↓                               ↓
        Get Description                Return task_id
              ↓                               ↓
         Validate               →  Presentation
              ↓                               ↓
         Call add_task()              Display success
```

### View Tasks Flow
```
User Input → Presentation → Call get_all_tasks()
              ↓                    ↓
        Display Menu         Data Layer
              ↓                    ↓
        Get Choice           Return copy
              ↓                    ↓
    Call display_task_list()  ←  Presentation
              ↓
         Format & Print
```

---

## State Management

### Global State (In-Memory)
```python
tasks = []      # List of task dictionaries
next_id = 1     # Sequential ID counter
```

**State Lifetime**:
- Initialized when module loads
- Persists for session duration
- Lost when application exits (no persistence)

**State Access**:
- All data layer functions read/modify global state
- Presentation and control flow call data layer only
- No direct state access from presentation layer

---

## Error Handling Strategy

### Error Categories

| Category | Example | Handler | User Message |
|----------|---------|---------|--------------|
| Invalid input type | "abc" for ID | get_task_id() | "Invalid task ID. Please enter a number" |
| Empty validation | "" for description | get_task_description() | "Task description cannot be empty" |
| Not found | ID 999 | Handler function | "Task with ID 999 not found" |
| Invalid choice | 99 | get_menu_choice() | "Invalid choice. Please enter 1-6" |

### Error Recovery
- All errors return to main menu
- No application crashes
- User can retry immediately
- State remains consistent

---

## Dependencies

```
Control Flow
    │
    ├──► Presentation Layer
    │        │
    │        └──► Data Layer (no dependencies)
    │
    └──► Data Layer (no dependencies)
```

**Dependency Direction**:
- Presentation depends on Data (calls CRUD functions)
- Data has no dependencies (pure logic)
- Control flow coordinates both

---

## Scalability Considerations

### Current (Phase I)
- Single user, single session
- Up to 1000 tasks
- In-memory operations < 1ms

### Future Phases
- Phase II: Database persistence, multiple users
- Phase III: Conversational AI interface
- Phase IV+: Infrastructure scaling

**Architecture prepared for**:
- Data layer can be replaced with database calls
- Presentation layer can be replaced with web/UI
- Control flow remains the orchestration logic
