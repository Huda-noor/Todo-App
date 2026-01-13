# Phase II - UI/UX Design Guide

## Design Philosophy

### Core Principles
1. **Minimalist & Focused** — Clean interface, task management is the priority
2. **Responsive** — Works seamlessly on desktop and mobile
3. **Accessible** — Keyboard navigation, proper ARIA labels
4. **Feedback-Rich** — Immediate visual feedback for all actions
5. **Progressive Disclosure** — Show only what's needed, reveal more on demand

---

## Color System

### Primary Palette
```css
--color-primary: #4F46E5;      /* Indigo - main actions */
--color-primary-hover: #4338CA;
--color-primary-light: #EEF2FF;

--color-success: #10B981;      /* Green - completed tasks */
--color-success-light: #D1FAE5;

--color-warning: #F59E0B;      /* Amber - confirmations */
--color-warning-light: #FEF3C7;

--color-error: #EF4444;        /* Red - errors, delete */
--color-error-light: #FEE2E2;
```

### Neutral Palette
```css
--color-bg: #FFFFFF;
--color-bg-secondary: #F9FAFB;
--color-border: #E5E7EB;
--color-text-primary: #111827;
--color-text-secondary: #6B7280;
--color-text-muted: #9CA3AF;
```

### Status Colors
```css
/* Completed task */
.todo-item.completed .todo-text {
    text-decoration: line-through;
    color: var(--color-text-muted);
}

/* Incomplete task */
.todo-item:not(.completed) .todo-text {
    color: var(--color-text-primary);
}
```

---

## Typography

### Font Family
```css
--font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto,
             'Helvetica Neue', Arial, sans-serif;
```

### Font Sizes
```css
--text-xs: 0.75rem;    /* 12px - labels, muted */
--text-sm: 0.875rem;   /* 14px - body */
--text-base: 1rem;     /* 16px - main content */
--text-lg: 1.125rem;   /* 18px - headings */
--text-xl: 1.25rem;    /* 20px - page titles */
--text-2xl: 1.5rem;    /* 24px - main headings */
```

### Line Heights
```css
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.625;
```

---

## Spacing System

### Base Unit: 4px
```css
--space-1: 4px;
--space-2: 8px;
--space-3: 12px;
--space-4: 16px;
--space-5: 20px;
--space-6: 24px;
--space-8: 32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
```

### Usage Examples
```css
/* Component padding */
.todo-item { padding: var(--space-3) var(--space-4); }

/* Gap between elements */
.todo-list { gap: var(--space-2); }

/* Margins */
.page-container { margin: var(--space-6) auto; }
```

---

## Component Specifications

### Button

#### Primary Button
```css
.btn-primary {
    background-color: var(--color-primary);
    color: white;
    padding: var(--space-2) var(--space-4);
    border-radius: var(--radius-md);
    font-weight: 500;
    border: none;
    cursor: pointer;
    transition: background-color 0.2s;
}

.btn-primary:hover {
    background-color: var(--color-primary-hover);
}

.btn-primary:disabled {
    opacity: 0.6;
    cursor: not-allowed;
}
```

#### Secondary Button
```css
.btn-secondary {
    background-color: transparent;
    color: var(--color-text-secondary);
    padding: var(--space-2) var(--space-4);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    cursor: pointer;
}

.btn-secondary:hover {
    background-color: var(--color-bg-secondary);
}
```

#### Danger Button (Delete)
```css
.btn-danger {
    background-color: transparent;
    color: var(--color-error);
    padding: var(--space-1) var(--space-2);
    border: none;
    cursor: pointer;
}

.btn-danger:hover {
    background-color: var(--color-error-light);
    border-radius: var(--radius-sm);
}
```

---

### Input Field

```css
.input {
    width: 100%;
    padding: var(--space-2) var(--space-3);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    font-size: var(--text-base);
    transition: border-color 0.2s, box-shadow 0.2s;
}

.input:focus {
    outline: none;
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px var(--color-primary-light);
}

.input.error {
    border-color: var(--color-error);
}

.input-error-message {
    color: var(--color-error);
    font-size: var(--text-sm);
    margin-top: var(--space-1);
}
```

---

### Card/Todo Item

```css
.todo-item {
    display: flex;
    align-items: center;
    gap: var(--space-3);
    padding: var(--space-3) var(--space-4);
    background: white;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-lg);
    transition: box-shadow 0.2s, border-color 0.2s;
}

.todo-item:hover {
    box-shadow: var(--shadow-sm);
}

.todo-item.completed {
    background-color: var(--color-bg-secondary);
}

/* Checkbox */
.todo-checkbox {
    width: 20px;
    height: 20px;
    border-radius: var(--radius-full);
    border: 2px solid var(--color-border);
    cursor: pointer;
    transition: all 0.2s;
}

.todo-checkbox.checked {
    background-color: var(--color-success);
    border-color: var(--color-success);
}

/* Text */
.todo-text {
    flex: 1;
    font-size: var(--text-base);
}

.todo-item.completed .todo-text {
    text-decoration: line-through;
    color: var(--color-text-muted);
}

/* Actions */
.todo-actions {
    display: flex;
    gap: var(--space-1);
    opacity: 0;
    transition: opacity 0.2s;
}

.todo-item:hover .todo-actions {
    opacity: 1;
}
```

---

### Form Layout

```css
.form-group {
    margin-bottom: var(--space-4);
}

.form-label {
    display: block;
    font-size: var(--text-sm);
    font-weight: 500;
    color: var(--color-text-primary);
    margin-bottom: var(--space-2);
}

.form-error {
    color: var(--color-error);
    font-size: var(--text-sm);
    margin-top: var(--space-1);
}
```

---

## Layout Structure

### Page Layout
```
┌─────────────────────────────────────────────────────────┐
│  Header                                                  │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Logo    │  User: user@example.com  [Logout]   │    │
│  └─────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Page Title                                     │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
│  ┌─────────────────────────────────────────────────┐    │
│  │  Main Content                                   │    │
│  │                                                 │    │
│  │  ┌─────────────────────────────────────────┐   │    │
│  │  │  Create Todo Form                       │   │    │
│  │  └─────────────────────────────────────────┘   │    │
│  │                                                 │    │
│  │  ┌─────────────────────────────────────────┐   │    │
│  │  │  Todo List                              │   │    │
│  │  │  ┌─────┐  ┌─────────────────────────┐   │   │    │
│  │  │  │ ☑ │  │ Buy groceries      [✏️][🗑] │   │   │    │
│  │  │  └─────┘  └─────────────────────────┘   │   │    │
│  │  │  ┌─────┐  ┌─────────────────────────┐   │   │    │
│  │  │  │ ☐ │  │ Clean house        [✏️][🗑] │   │   │    │
│  │  │  └─────┘  └─────────────────────────┘   │   │    │
│  │  └─────────────────────────────────────────┘   │    │
│  │                                                 │    │
│  └─────────────────────────────────────────────────┘    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Auth Page Layout
```
┌─────────────────────────────────────────────────────────┐
│  ┌─────────────────────────────────────────────────┐    │
│  │                                                 │    │
│  │         Evolution of Todo                       │    │
│  │                                                 │    │
│  │  ┌─────────────────────────────────────────┐   │    │
│  │  │  Email    [__________________]          │   │    │
│  │  └─────────────────────────────────────────┘   │    │
│  │  ┌─────────────────────────────────────────┐   │    │
│  │  │  Password [__________________]          │   │    │
│  │  └─────────────────────────────────────────┘   │    │
│  │  ┌─────────────────────────────────────────┐   │    │
│  │  │  [ Sign In ]                            │   │    │
│  │  └─────────────────────────────────────────┘   │    │
│  │                                                 │    │
│  │  Don't have an account? [Sign up]             │    │
│  │                                                 │    │
│  └─────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────┘
```

---

## Responsive Breakpoints

```css
/* Mobile First */

.container {
    max-width: 1024px;
    margin: 0 auto;
    padding: var(--space-4);
}

/* Tablet */
@media (min-width: 640px) {
    .container {
        padding: var(--space-6);
    }
}

/* Desktop */
@media (min-width: 1024px) {
    .container {
        padding: var(--space-8);
    }
}

/* Mobile: Stack actions */
.todo-actions {
    opacity: 1; /* Always visible on mobile */
}
```

---

## Animations & Transitions

### Timing
```css
--transition-fast: 150ms;
--transition-normal: 200ms;
--transition-slow: 300ms;
```

### Usage
```css
/* Hover effects */
.btn {
    transition: background-color var(--transition-fast),
                transform var(--transition-fast);
}

/* Focus states */
.input:focus {
    transition: border-color var(--transition-fast),
                box-shadow var(--transition-fast);
}

/* Button press */
.btn:active {
    transform: scale(0.98);
}
```

---

## Loading States

### Spinner
```css
.spinner {
    width: 20px;
    height: 20px;
    border: 2px solid var(--color-border);
    border-top-color: var(--color-primary);
    border-radius: 50%;
    animation: spin 0.6s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
```

### Skeleton Loading
```css
.skeleton {
    background: linear-gradient(
        90deg,
        var(--color-bg-secondary) 25%,
        var(--color-border) 50%,
        var(--color-bg-secondary) 75%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: var(--radius-md);
}

@keyframes shimmer {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}
```

---

## Accessibility (A11y)

### ARIA Labels
```tsx
<button
    aria-label="Mark task as complete"
    aria-pressed={todo.is_complete}
>
    <Checkbox checked={todo.is_complete} />
</button>

<button
    aria-label="Edit todo"
    className="edit-btn"
>
    <EditIcon />
</button>

<button
    aria-label="Delete todo"
    aria-describedby="delete-confirm"
    className="delete-btn"
>
    <DeleteIcon />
</button>
```

### Keyboard Navigation
```css
/* Visible focus states */
.btn:focus-visible,
.input:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
}

/* Skip link */
.skip-link {
    position: absolute;
    top: -40px;
    left: 0;
    background: var(--color-primary);
    color: white;
    padding: var(--space-2) var(--space-4);
    z-index: 100;
}

.skip-link:focus {
    top: 0;
}
```

### Form Validation
```tsx
<label htmlFor="email">Email</label>
<input
    id="email"
    type="email"
    aria-invalid={errors.email ? "true" : "false"}
    aria-describedby={errors.email ? "email-error" : undefined}
/>
{errors.email && (
    <span id="email-error" role="alert">
        {errors.email}
    </span>
)}
```

---

## Error Handling UI

### Inline Form Errors
```
┌─────────────────────────────────────────┐
│  Email    [__________________]          │
│           Please enter a valid email    │  ← Red text, below input
└─────────────────────────────────────────┘
```

### Toast Notifications
```css
.toast {
    position: fixed;
    bottom: var(--space-4);
    right: var(--space-4);
    padding: var(--space-3) var(--space-4);
    background: white;
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-lg);
    border-left: 4px solid var(--color-primary);
    animation: slideIn var(--transition-normal);
}

.toast.error {
    border-left-color: var(--color-error);
}

.toast.success {
    border-left-color: var(--color-success);
}
```

---

## Empty States

### No Todos Yet
```
┌─────────────────────────────────────────┐
│                                         │
│           📋                            │
│                                         │
│      No todos yet                       │
│                                         │
│   Create your first task to get         │
│   started!                              │
│                                         │
│   ┌─────────────────────────────────┐   │
│   │  [ What's your first task? ]   │   │
│   └─────────────────────────────────┘   │
│                                         │
└─────────────────────────────────────────┘
```

### Empty Search Results
```
┌─────────────────────────────────────────┐
│                                         │
│           🔍                            │
│                                         │
│   No todos matching "groceries"         │
│                                         │
│   Try a different search term or        │
│   create a new task.                    │
│                                         │
└─────────────────────────────────────────┘
```

---

## Interaction Patterns

### Optimistic Updates

```tsx
// When user clicks complete:
const handleToggle = async (todoId) => {
    // 1. Immediately update UI (optimistic)
    setTodos(prev => prev.map(t =>
        t.id === todoId ? { ...t, is_complete: !t.is_complete } : t
    ));

    // 2. Make API call
    try {
        await api.toggleTodo(todoId);
    } catch (error) {
        // 3. Revert on error
        setTodos(prev => prev.map(t =>
            t.id === todoId ? { ...t, is_complete: !t.is_complete } : t
        ));
        showToast('Failed to update task', 'error');
    }
};
```

### Confirmation for Destructive Actions

```tsx
const handleDelete = (todoId) => {
    if (confirm('Are you sure you want to delete this task?')) {
        // Proceed with deletion
    }
};

// Or with a custom modal:
<DeleteConfirmModal
    isOpen={showModal}
    onConfirm={() => deleteTodo(todoId)}
    onCancel={() => setShowModal(false)}
    title="Delete Task"
    message="Are you sure you want to delete this task? This action cannot be undone."
/>
```

---

## Design Checklist

- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Focus states visible for keyboard navigation
- [ ] All interactive elements have hover states
- [ ] Loading states for async operations
- [ ] Error messages are descriptive and helpful
- [ ] Empty states are friendly and encouraging
- [ ] Mobile layout stacks elements vertically
- [ ] Touch targets minimum 44x44px on mobile
- [ ] Animations respect `prefers-reduced-motion`
