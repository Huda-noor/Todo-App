# Phase I - User Flows

## Flow 1: Add a New Task

```
User selects: 1

System displays: "Enter task description:"
User enters: "Buy groceries"

System responds: "Task added successfully with ID 1"
System returns to: Main Menu
```

**Error Path**:
```
User selects: 1
System displays: "Enter task description:"
User enters: ""

System responds: "Error: Task description cannot be empty"
System returns to: Main Menu
```

---

## Flow 2: View All Tasks

```
User selects: 2

System displays:
"=== Your Tasks ===
1. [ ] Buy groceries
2. [X] Clean the house
3. [ ] Call the dentist

Total: 3 tasks (1 complete, 2 incomplete)"

System returns to: Main Menu
```

**Empty List Path**:
```
User selects: 2

System displays: "No tasks found. Your list is empty."
System returns to: Main Menu
```

---

## Flow 3: Update a Task

```
User selects: 3

System displays: "Enter task ID to update:"
User enters: "1"

System displays: "Enter new description:"
User enters: "Buy groceries and milk"

System responds: "Task 1 updated successfully"
System returns to: Main Menu
```

**Error Path - Task Not Found**:
```
User selects: 3
System displays: "Enter task ID to update:"
User enters: "99"

System responds: "Error: Task with ID 99 not found"
System returns to: Main Menu
```

**Error Path - Invalid ID**:
```
User selects: 3
System displays: "Enter task ID to update:"
User enters: "abc"

System responds: "Error: Invalid task ID. Please enter a number"
System returns to: Main Menu
```

---

## Flow 4: Delete a Task

```
User selects: 4

System displays: "Enter task ID to delete:"
User enters: "2"

System responds: "Task 2 deleted successfully"
System returns to: Main Menu
```

**Error Path**:
```
User selects: 4
System displays: "Enter task ID to delete:"
User enters: "abc"

System responds: "Error: Invalid task ID. Please enter a number"
System returns to: Main Menu
```

---

## Flow 5: Mark Task Complete/Incomplete

```
User selects: 5

System displays: "Enter task ID to toggle status:"
User enters: "1"

System responds: "Task 1 marked as complete"
System returns to: Main Menu
```

**Second Toggle (Complete → Incomplete)**:
```
User selects: 5

System displays: "Enter task ID to toggle status:"
User enters: "1"

System responds: "Task 1 marked as incomplete"
System returns to: Main Menu
```

---

## Flow 6: Exit Application

```
User selects: 6

System displays: "Thank you for using Todo Application. Goodbye!"
System terminates
```

---

## Edge Case Flows

### Invalid Menu Choice
```
User enters: "99"

System displays: "Error: Invalid choice. Please enter a number between 1 and 6."
System returns to: Main Menu
```

### Non-Numeric Task ID
```
User enters: "abc" when prompted for task ID

System displays: "Error: Invalid task ID. Please enter a number"
System returns to: Main Menu
```

### Session Restart (No Persistence)
```
Session 1:
User adds 3 tasks, views them, exits

Session 2 (new terminal):
User selects: 2 (View tasks)

System displays: "No tasks found. Your list is empty."
```
