# Phase II - Todo Operation User Flows

## Flow 1: Create Todo

```
┌─────────────────────────────────────────────────────────────────────┐
│ TODOS PAGE (/todos) - Authenticated User                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Header: [Logo]  user@example.com  [Sign out]                      │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  [ ________________ Create a new task...            ] [Add] │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  Your Tasks (3)                                             │   │
│  │  ├───────────────────────────────────────────────────────┐  │   │
│  │  │ ☐  Buy groceries                     [✏️] [🗑]       │  │   │
│  │  ├───────────────────────────────────────────────────────┤  │   │
│  │  │ ☑  Clean house                         [✏️] [🗑]       │  │   │
│  │  ├───────────────────────────────────────────────────────┤  │   │
│  │  │ ☐  Call the dentist                    [✏️] [🗑]       │  │   │
│  │  └───────────────────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘

Happy Path:
1. User types "Buy groceries" in input field
2. User clicks "Add" button
3. Loading state on button
4. New todo appears at top of list:
   ├───────────────────────────────────────────────────────┐
   │ ☐  Buy groceries                     [✏️] [🗑]       │
   └───────────────────────────────────────────────────────┘
5. Input field clears
6. Count updates: "Your Tasks (4)"

Error - Empty Description:
1. User clicks "Add" with empty input
2. Error message: "Todo description cannot be empty"
3. Input border turns red
4. No todo created

Error - Too Long:
1. User enters 501+ characters
2. Error message: "Todo description cannot exceed 500 characters"
3. Input border turns red
```

---

## Flow 2: View Todos

```
Initial Page Load:
1. User navigates to /todos
2. AuthGuard verifies session
3. API call: GET /api/todos
4. Loading skeleton shown
5. On success: Todos displayed
6. On error: Error message shown

Display States:

Empty State:
┌─────────────────────────────────────────────────────────────┐
│  ┌───────────────────────────────────────────────────────┐  │
│  │                                                       │  │
│  │         📋 No tasks yet                               │  │
│  │                                                       │  │
│  │    Create your first task to get started!             │  │
│  │                                                       │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  [ ________________ Create a new task... ] [Add]│  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │                                                       │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘

With Tasks:
┌─────────────────────────────────────────────────────────────┐
│  ┌─────────────────────────────────────────────────────────┐│
│  │  [ ________________ Create a new task...          ][Add]││
│  └─────────────────────────────────────────────────────────┘│
│                                                                 │
│  Your Tasks (3)                                                │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ ☐  Buy groceries                        [Edit] [Delete]││
│  └─────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────┐│
│  │ ☑  Clean house                          [Edit] [Delete]││
│  └─────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────┐│
│  │ ☐  Call the dentist                     [Edit] [Delete]││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘

Each todo shows:
- Checkbox (☐ incomplete / ☑ complete)
- Description
- Edit button (✏️)
- Delete button (🗑)
- Visual distinction for completed (strikethrough)
```

---

## Flow 3: Toggle Completion

```
Incomplete Todo:
┌─────────────────────────────────────────────────────────┐
│ ☐  Buy groceries                        [Edit] [Delete] │
└─────────────────────────────────────────────────────────┘

Action: User clicks checkbox

Immediate Feedback (Optimistic):
┌─────────────────────────────────────────────────────────┐
│ ☑  Buy groceries                        [Edit] [Delete] │
└─────────────────────────────────────────────────────────┘
(Checkbox immediately shows ☑)

API Call: PATCH /api/todos/{id}/toggle

Success: State confirmed, no further action
Failure: Checkbox reverts to original state, toast error

Completed Todo:
┌─────────────────────────────────────────────────────────┐
│ ☑  Buy groceries                        [Edit] [Delete] │
└─────────────────────────────────────────────────────────┘

Action: User clicks checkbox again

Result:
┌─────────────────────────────────────────────────────────┐
│ ☐  Buy groceries                        [Edit] [Delete] │
└─────────────────────────────────────────────────────────┘
```

---

## Flow 4: Update Todo

```
Inline Edit Mode:

Before (Hover shows edit button):
┌─────────────────────────────────────────────────────────┐
│ ☑  Clean house                          [✏️] [Delete]   │
└─────────────────────────────────────────────────────────┘
              ↓ User clicks ✏️
              ↓

After (Inline edit):
┌─────────────────────────────────────────────────────────┐
│ [ ☑  _______________________________________ ] [✓] [✕] │
└─────────────────────────────────────────────────────────┘

User types new description
User clicks:
- ✓ (Save): Updates todo, exits edit mode
- ✕ (Cancel): Discards changes, exits edit mode
- Esc key: Cancels edit, restores original

Success:
┌─────────────────────────────────────────────────────────┐
│ ☑  Clean the entire house                   [Edit] [Delete] │
└─────────────────────────────────────────────────────────┘

Error - Empty:
┌─────────────────────────────────────────────────────────┐
│ [ ☑  _______________________________________ ]          │
│              Description cannot be empty                 │
└─────────────────────────────────────────────────────────┘
```

---

## Flow 5: Delete Todo

```
Delete Flow (with confirmation):

Before:
┌─────────────────────────────────────────────────────────┐
│ ☐  Old task                              [Edit] [🗑]   │
└─────────────────────────────────────────────────────────┘
              ↓ User clicks 🗑
              ↓

Confirmation Modal:
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│       Delete Task?                                          │
│                                                             │
│       Are you sure you want to delete "Old task"?           │
│       This action cannot be undone.                         │
│                                                             │
│       [ Cancel ]          [ Delete ]                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘

User clicks "Delete":
1. API call: DELETE /api/todos/{id}
2. Todo removed from list
3. Toast: "Task deleted successfully"

User clicks "Cancel":
1. Modal closes
2. Todo remains in list

Alternative (Simple confirm):
┌─────────────────────────────────────────────────────────┐
│ ☐  Old task                              [Edit] [🗑]   │
└─────────────────────────────────────────────────────────┘
              ↓ User clicks 🗑
              ↓
Browser confirm dialog:
"Delete 'Old task'? This cannot be undone."
[Cancel] [Delete]
```

---

## Flow 6: Mobile View

```
Mobile Layout (Stacked):

┌─────────────────────────┐
│ Header                  │
│ TodoApp      [Sign out] │
└─────────────────────────┘

┌─────────────────────────┐
│ [ + Add task... ]       │
└─────────────────────────┘

┌─────────────────────────┐
│ Task 1                  │
│ [ ] Buy groceries       │
│ [Edit] [Delete]         │
└─────────────────────────┘

┌─────────────────────────┐
│ Task 2                  │
│ [✓] Clean house         │
│ [Edit] [Delete]         │
└─────────────────────────┘

Differences from desktop:
- Actions always visible (no hover reveal)
- Full-width touch targets
- Stacked layout
```

---

## Data Flow Diagrams

### Create Todo Flow
```
User Input
    │
    ▼
┌───────────────┐
│ Form Submit   │─── Validate (client-side)
└───────┬───────┘
        │ Invalid
        ▼
    Show Error

        │ Valid
        ▼
┌───────────────┐
│ API: POST     │─── Loading state on button
│ /api/todos    │
└───────┬───────┘
        │
        ▼
    ┌────┴────┐
    │         │
 Success   Error
    │         │
    ▼         ▼
Update    Show Error
UI        Revert
```

### Toggle Flow (Optimistic)
```
User clicks checkbox
        │
        ▼
┌───────────────┐
│ Toggle local  │─── Immediate UI update
│ state         │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│ API: PATCH    │─── Background request
│ /todos/{id}   │   (spinner on checkbox)
└───────┬───────┘
        │
        ┌────┴────┐
        │         │
    Success    Error
        │         │
   Confirm     Revert
   state       UI + Toast
```

---

## Edge Cases

| Scenario | Behavior |
|----------|----------|
| Network failure during operation | Show error, allow retry |
| Rapid successive clicks | Debounce, ignore duplicates |
| API returns old data | Optimistic update, then sync |
| User deletes todo while editing | Cancel edit, close form |
| Empty todo list, then create | Empty state replaced with list |
| Very long description | Wrap text, show ellipsis if needed |
| Special characters | Render as-is (UTF-8) |
| Emoji in description | Render emoji (proper encoding) |
