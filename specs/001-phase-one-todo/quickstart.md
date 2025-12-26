# Quickstart Guide: Phase I - In-Memory Todo CLI

**Feature**: Phase I - In-Memory Todo CLI
**Branch**: `001-phase-one-todo`
**Date**: 2025-12-27

## Prerequisites

- **Python**: Version 3.8 or higher
- **Operating System**: Windows, Linux, or macOS
- **Terminal**: Command-line interface (CMD, PowerShell, Terminal, etc.)

## Checking Python Installation

Before running the application, verify Python is installed:

```bash
python --version
```

or

```bash
python3 --version
```

You should see output like: `Python 3.8.x`, `Python 3.9.x`, `Python 3.10.x`, etc.

If Python is not installed:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **macOS**: Use Homebrew (`brew install python3`) or download from python.org
- **Linux**: Use package manager (`sudo apt install python3` for Ubuntu/Debian)

## Running the Application

### Step 1: Navigate to Source Directory

```bash
cd src
```

### Step 2: Run the Application

```bash
python todo_cli.py
```

or (if `python` command not available):

```bash
python3 todo_cli.py
```

### Step 3: Interact with the Menu

You should see the main menu:

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

## Basic Usage Examples

### Example 1: Add Your First Task

1. Select option `1` (Add a new task)
2. Enter task description: `Buy groceries`
3. Press Enter
4. You'll see: `Task added successfully with ID 1`

### Example 2: View Your Tasks

1. Select option `2` (View all tasks)
2. You'll see:
   ```
   === Your Tasks ===
   1. [ ] Buy groceries

   Total: 1 tasks (0 complete, 1 incomplete)
   ```

### Example 3: Mark Task as Complete

1. Select option `5` (Mark task as complete/incomplete)
2. Enter task ID: `1`
3. Press Enter
4. You'll see: `Task 1 marked as complete`

### Example 4: View Updated Tasks

1. Select option `2` (View all tasks)
2. You'll see:
   ```
   === Your Tasks ===
   1. [X] Buy groceries

   Total: 1 tasks (1 complete, 0 incomplete)
   ```

### Example 5: Add More Tasks

1. Select option `1` (Add a new task)
2. Enter: `Clean the house`
3. Select option `1` again
4. Enter: `Call the dentist`
5. View tasks to see all three

### Example 6: Update a Task

1. Select option `3` (Update a task)
2. Enter task ID: `2`
3. Enter new description: `Clean the entire house`
4. You'll see: `Task 2 updated successfully`

### Example 7: Delete a Task

1. Select option `4` (Delete a task)
2. Enter task ID: `3`
3. You'll see: `Task 3 deleted successfully`
4. View tasks to confirm deletion

### Example 8: Exit the Application

1. Select option `6` (Exit)
2. You'll see: `Thank you for using Todo Application. Goodbye!`
3. Application terminates

**Important**: All tasks are lost when you exit. This is expected behavior for Phase I.

## Common Usage Scenarios

### Scenario: Planning Your Day

```
1. Add task: "Review emails"
2. Add task: "Attend team meeting"
3. Add task: "Complete project report"
4. View tasks to see your day's agenda
5. Mark tasks complete as you finish them
6. View tasks to track progress
```

### Scenario: Quick Todo List

```
1. Add several tasks quickly
2. Mark some as complete
3. Delete tasks you no longer need
4. View remaining tasks
```

### Scenario: Correcting Mistakes

```
1. Add task with typo: "Buy grocieries"
2. Update task: "Buy groceries"
3. View tasks to confirm correction
```

## Error Handling Examples

### Error: Empty Description

```
Enter your choice (1-6): 1
Enter task description:
Error: Task description cannot be empty
[Returns to main menu]
```

### Error: Invalid Task ID

```
Enter your choice (1-6): 4
Enter task ID to delete: 99
Error: Task with ID 99 not found
[Returns to main menu]
```

### Error: Non-Numeric Input

```
Enter your choice (1-6): 3
Enter task ID to update: abc
Error: Invalid task ID. Please enter a number
[Returns to main menu]
```

### Error: Invalid Menu Choice

```
Enter your choice (1-6): 9
Error: Invalid choice. Please enter a number between 1 and 6
[Returns to main menu]
```

## Tips and Best Practices

1. **Keep Descriptions Clear**: Use concise, actionable task descriptions
2. **Use IDs Carefully**: Note the task ID when viewing tasks before updating/deleting
3. **Mark Complete Promptly**: Update task status as you complete work for accurate tracking
4. **Delete Finished Tasks**: Remove completed tasks to keep your list manageable
5. **Exit Cleanly**: Always use option 6 to exit (don't force-quit)

## Known Limitations (Phase I)

- **No Persistence**: All tasks lost when application exits
- **No Sorting**: Tasks displayed in creation order
- **No Filtering**: Cannot filter by status or search descriptions
- **No Priorities**: All tasks treated equally
- **No Due Dates**: No deadline tracking
- **No Undo**: Cannot undo deletions or changes
- **Single User**: No multi-user support
- **Session-Based**: No save/load functionality

**Note**: These limitations are intentional for Phase I. Future phases may add these features.

## Troubleshooting

### Problem: `python: command not found`

**Solution**: Try `python3` instead of `python`, or install Python

### Problem: `ModuleNotFoundError` or Import Errors

**Solution**: Phase I has no dependencies. If you see import errors, check that you're running the correct file (`todo_cli.py`)

### Problem: Script Won't Run

**Solution**:
1. Verify you're in the `src` directory
2. Check file exists: `ls todo_cli.py` (Linux/macOS) or `dir todo_cli.py` (Windows)
3. Check Python version: `python --version` (must be 3.8+)
4. Check file permissions: `chmod +x todo_cli.py` (Linux/macOS only)

### Problem: Application Crashes

**Solution**:
1. Phase I handles all expected errors gracefully
2. If crash occurs, it may indicate a bug—report to development team
3. Restart application and retry operation

### Problem: Tasks Disappeared

**Solution**: This is expected behavior. Phase I is session-based. Tasks exist only while application is running. Exiting the application deletes all data.

## Performance Notes

- **Response Time**: All operations complete instantly (< 1 second)
- **Capacity**: Supports up to 1000 tasks per session
- **Memory Usage**: Minimal (~100KB for 1000 tasks)
- **CPU Usage**: Negligible (simple Python operations)

## Support and Feedback

- **Bug Reports**: Report to development team with error details
- **Feature Requests**: Will be considered for future phases
- **Questions**: Refer to specification in `specs/001-phase-one-todo/spec.md`

## Next Steps

After familiarizing yourself with Phase I:

1. **Use Daily**: Incorporate into your workflow
2. **Provide Feedback**: Note any usability issues
3. **Await Phase II**: Future phases will add persistence, web interface, and more

---

**End of Quickstart Guide**
