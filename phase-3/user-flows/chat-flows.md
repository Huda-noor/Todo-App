# Phase III - Chat User Flows

## Flow 1: First Conversation

```
┌─────────────────────────────────────────────────────────────┐
│ CHAT PAGE - First Visit                                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ View: [List] [💬 Chat]                              │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │  ┌──────────┐                                        │   │
│  │  │ 🤖      │  👋 Hi! I'm your todo assistant.      │   │
│  │  │         │                                        │   │
│  │  │         │  You can chat with me to:              │   │
│  │  │         │                                        │   │
│  │  │         │  • Add new tasks                       │   │
│  │  │         │  • Check your todo list                │   │
│  │  │         │  • Mark tasks as done                  │   │
│  │  │         │  • Update or delete tasks              │   │
│  │  │         │                                        │   │
│  │  │         │  What would you like to do?            │   │
│  │  └──────────┘                                        │   │
│  │                                                     │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │ "Show me my todos"                           │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │ "Add a task to buy groceries"                │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │  ┌──────────────────────────────────────────────┐  │   │
│  │  │ "Help me organize my tasks"                  │  │   │
│  │  └──────────────────────────────────────────────┘  │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │ [ Type a message...                              ] [Send]│ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Flow 2: Create Todo via Chat

```
User: "Add a task to buy groceries"

AI: (typing indicator...)
    ┌──────────┐
    │ ✓ Done!  │  I've created a new todo: "Buy groceries"
    └──────────┘

    Is there anything else you'd like to do?
    ┌──────────────────────────────────────────────┐
    │ "Show me all my tasks"                       │
    │ "Add another task"                           │
    └──────────────────────────────────────────────┘
```

**Ambiguous Case**:
```
User: "Add a task"

AI: ┌──────────┐
    │ 🤔       │  What would you like the task to be?
    └──────────┘

User: "Buy groceries"

AI: ┌──────────┐
    │ ✓ Done!  │  I've created: "Buy groceries"
    └──────────┘
```

---

## Flow 3: List Todos via Chat

```
User: "Show me my todos"

AI: (typing indicator...)
    ┌──────────┐
    │ 📋      │  Here are your current tasks (3 total):
    └──────────┘

    ☑ Buy groceries
    ☐ Clean the house
    ☐ Call the dentist

    ┌──────────────────────────────────────────────┐
    │ "Mark the first task as done"                │
    │ "What's left to do?"                         │
    └──────────────────────────────────────────────┘
```

**Empty List**:
```
User: "What do I have to do?"

AI: ┌──────────┐
    │ 📭      │  Your todo list is empty!
    └──────────┘

    Ready to add some tasks?
    ┌──────────────────────────────────────────────┐
    │ "Add a task to buy groceries"                │
    └──────────────────────────────────────────────┘
```

---

## Flow 4: Toggle Complete via Chat

```
User: "I finished buying groceries"

AI: (typing indicator...)
    ┌──────────┐
    │ ✅      │  Great! I've marked "Buy groceries" as done.
    └──────────┘

    ☑ Buy groceries (completed)

    ┌──────────────────────────────────────────────┐
    │ "What else do I have?"                       │
    │ "Show me incomplete tasks"                   │
    └──────────────────────────────────────────────┘
```

**Clarification Needed**:
```
User: "Mark that as done"

AI: ┌──────────┐
    │ 🤔       │  Which task would you like to mark as done?
    └──────────┘

    (Recent tasks shown)
    ☑ Buy groceries
    ☐ Clean the house

User: "The second one"

AI: ┌──────────┐
    │ ✅      │  Done! "Clean the house" is now complete.
    └──────────┘
```

---

## Flow 5: Delete Todo via Chat

```
User: "Delete the task about groceries"

AI: ┌──────────┐
    │ 🗑️      │  Ready to delete: "Buy groceries"
    └──────────┘

    ┌──────────────────────────────────────────────┐
    │ [ Cancel ]          [ Delete ]               │
    └──────────────────────────────────────────────┘

User: [Delete]

AI: ┌──────────┐
    │ ✅      │  Deleted "Buy groceries"
    └──────────┘
```

---

## Flow 6: Multi-Turn Conversation

```
User: "Add a task"
AI: ┌──────────┐
    │ 🤔       │  What would you like the task to be?
    └──────────┘

User: "to call my dentist"
AI: ┌──────────┐
    │ ✅      │  Created: "Call my dentist"
    └──────────┘

User: "and also book the appointment"
AI: ┌──────────┐
    │ 🤔       │  I've got it! Should I create a separate task
    │          │  for booking the appointment, or update the
    │          │  current task to "Call my dentist and book
    │          │  the appointment"?
    └──────────┘

User: "Create a new task"
AI: ┌──────────┐
    │ ✅      │  Created: "Book the dentist appointment"
    └──────────┘

User: "show me my list"
AI: ┌──────────┐
    │ 📋      │  Here are your tasks:
    └──────────┘

    ☐ Call my dentist
    ☐ Book the dentist appointment
```

---

## Flow 7: Conversation Context

```
Session 1:
User: "Add buy milk"
AI: ✓ Created "Buy milk"

User: "add bread"
AI: ✓ Created "Bread"

User: "show all"
AI: Shows 2 tasks

Session 2 (next day):
User: "what did I add yesterday?"
AI: Based on our conversation, you added:
    • "Buy milk"
    • "Bread"
```

---

## Flow 8: Error Handling

**Tool Failure**:
```
User: "Add a task to buy milk"

AI: ┌──────────┐
    │ ⚠️      │  I'm having trouble creating that task.
    │          │  Please try again in a moment.
    └──────────┘
```

**Rate Limiting**:
```
User: (makes many requests quickly)

AI: ┌──────────┐
    │ ⏳      │  I'm a bit busy right now. Please wait
    │          │  a moment before trying again.
    └──────────┘
```

**Ambiguous Intent**:
```
User: "Do something"

AI: ┌──────────┐
    │ 🤔       │  I can help you with your todos. What would
    │          │  you like to do? For example:
    └──────────┘

    ┌──────────────────────────────────────────────┐
    │ "Show my tasks"                              │
    │ "Add a new task"                             │
    │ "Check what's done"                          │
    └──────────────────────────────────────────────┘
```

---

## Quick Action Mapping

| User Phrasing | Detected Intent | Action |
|---------------|-----------------|--------|
| "Add task...", "Create todo..." | create_todo | Call create_todo tool |
| "Show me...", "What do I have..." | list_todos | Call list_todos tool |
| "Mark as done", "I'm finished with..." | toggle_complete | Call toggle_todo_complete |
| "Change...", "Update...", "Rename..." | update_todo | Call update_todo tool |
| "Delete...", "Remove...", "Get rid of..." | delete_todo | Call delete_todo tool |
| "How many...", "Count my..." | list_todos + count | Call list_todos, return count |
| "What's first...", "Prioritize..." | clarification | Ask about preferences |
