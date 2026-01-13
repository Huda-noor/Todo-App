# Phase III - UI/UX Design Guide

## Design Philosophy

Phase III adds a conversational interface to the existing todo management app. The chat UI should feel natural, helpful, and integrated with the core todo experience.

### Core Principles
1. **Conversational First** — Chat feels like talking to a helpful assistant
2. **Contextual** — AI knows user's todo list and history
3. **Actionable** — Easy to switch between chat and list views
4. **Trustworthy** — Clear about what's happening, no surprises
5. **Accessible** — Works with screen readers, keyboard navigation

---

## Color System (Extends Phase II)

### Chat-Specific Colors
```css
/* User message */
--chat-user-bg: var(--color-primary);
--chat-user-text: white;

/* AI message */
--chat-ai-bg: var(--color-bg-secondary);
--chat-ai-text: var(--color-text-primary);

/* Typing indicator */
--chat-typing-bg: var(--color-border);

/* Quick actions */
--chat-quick-action-bg: var(--color-primary-light);
--chat-quick-action-text: var(--color-primary);
```

### Message Bubble Styles
```css
/* User message (right-aligned) */
.message.user {
    background-color: var(--chat-user-bg);
    color: var(--chat-user-text);
    border-radius: var(--radius-lg) var(--radius-lg) var(--radius-sm) var(--radius-lg);
    margin-left: auto;
    max-width: 80%;
}

/* AI message (left-aligned) */
.message.assistant {
    background-color: var(--chat-ai-bg);
    color: var(--chat-ai-text);
    border-radius: var(--radius-lg) var(--radius-lg) var(--radius-lg) var(--radius-sm);
    margin-right: auto;
    max-width: 80%;
}
```

---

## Typography (Extends Phase II)

```css
/* Message text */
.message-text {
    font-size: var(--text-base);
    line-height: var(--leading-relaxed);
}

/* Quick actions */
.quick-action {
    font-size: var(--text-sm);
    font-weight: 500;
}

/* Suggestions */
.suggestion {
    font-size: var(--text-sm);
    color: var(--color-text-secondary);
}
```

---

## Layout Structure

### Chat Page Layout
```
┌─────────────────────────────────────────────────────────────┐
│ Header (same as Phase II)                                   │
│ [Logo]  user@example.com  [Sign out]                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ View: [List] [Chat]                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  ┌──────────┐                                        │   │
│  │  │ 💬      │  Hello! I'm your todo assistant.      │   │
│  │  │ AI Icon │  How can I help you today?            │   │
│  │  └──────────┘                                        │   │
│  │                                                        │   │
│  │  ┌──────────────────────────────────────────────┐    │   │
│  │  │ I'd like to add a task to buy groceries.    │    │   │
│  │  └──────────────────────────────────────────────┘    │   │
│  │  │                                              │    │   │
│  │  │  ┌──────────┐                                │    │   │
│  │  │  │ ✓ Done!  │  I've created: "Buy groceries"│    │   │
│  │  │  └──────────┘                                │    │   │
│  │  │                                              │    │   │
│  │  └──────────────────────────────────────────────┘    │   │
│  │                                                             │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │                                                         │ │
│  │  Type a message...                        [Send] [🎤] │ │
│  │                                                         │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## Component Specifications

### Chat Input Area
```css
.chat-input-container {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-3);
    background: white;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-xl);
    margin: var(--space-4);
}

.chat-input {
    flex: 1;
    border: none;
    outline: none;
    font-size: var(--text-base);
    resize: none;
    max-height: 120px;
}

.chat-send-btn {
    background: var(--color-primary);
    color: white;
    border: none;
    border-radius: var(--radius-full);
    width: 40px;
    height: 40px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.chat-send-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}
```

### Message Bubbles
```css
.message {
    display: flex;
    flex-direction: column;
    max-width: 80%;
    padding: var(--space-3) var(--space-4);
    margin-bottom: var(--space-2);
}

.message.user {
    align-self: flex-end;
    background: var(--chat-user-bg);
    color: var(--chat-user-text);
    border-radius: var(--radius-xl) var(--radius-xl) var(--radius-sm) var(--radius-xl);
}

.message.assistant {
    align-self: flex-start;
    background: var(--chat-ai-bg);
    color: var(--chat-ai-text);
    border-radius: var(--radius-xl) var(--radius-xl) var(--radius-xl) var(--radius-sm);
}

/* Message timestamp */
.message-time {
    font-size: var(--text-xs);
    opacity: 0.7;
    margin-top: var(--space-1);
}

.message.user .message-time {
    text-align: right;
}
```

### Quick Reply Actions
```css
.quick-replies {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-2);
    padding: var(--space-2) var(--space-4);
}

.quick-reply-btn {
    background: var(--chat-quick-action-bg);
    color: var(--chat-quick-action-text);
    border: 1px solid var(--color-primary);
    border-radius: var(--radius-full);
    padding: var(--space-2) var(--space-3);
    font-size: var(--text-sm);
    cursor: pointer;
    transition: all 0.2s;
}

.quick-reply-btn:hover {
    background: var(--color-primary-light);
    transform: translateY(-1px);
}
```

### Typing Indicator
```css
.typing-indicator {
    display: flex;
    gap: 4px;
    padding: var(--space-3);
    background: var(--chat-typing-bg);
    border-radius: var(--radius-xl);
    width: fit-content;
}

.typing-dot {
    width: 8px;
    height: 8px;
    background: var(--color-text-muted);
    border-radius: 50%;
    animation: typingBounce 1.4s infinite ease-in-out;
}

.typing-dot:nth-child(1) { animation-delay: 0s; }
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typingBounce {
    0%, 80%, 100% { transform: translateY(0); }
    40% { transform: translateY(-6px); }
}
```

---

## Suggested Responses

After AI responses, show contextual suggestions:

```css
.suggestions {
    display: flex;
    flex-direction: column;
    gap: var(--space-1);
    margin-top: var(--space-2);
    padding-left: var(--space-4);
}

.suggestion-item {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    color: var(--color-text-secondary);
    font-size: var(--text-sm);
    cursor: pointer;
}

.suggestion-item:hover {
    color: var(--color-primary);
}

.suggestion-icon {
    width: 16px;
    height: 16px;
}
```

**Example suggestions after creating a todo:**
```
💡 Suggestions:
→ "Add another task"
→ "Show me my todos"
→ "What's on my list?"
```

---

## Todo Cards in Chat

When the AI references todos, show them as compact cards:

```css
.chat-todo-card {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-2) var(--space-3);
    background: white;
    border: 1px solid var(--color-border);
    border-radius: var(--radius-md);
    margin-top: var(--space-2);
}

.chat-todo-checkbox {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    border: 2px solid var(--color-border);
    cursor: pointer;
}

.chat-todo-checkbox.checked {
    background: var(--color-success);
    border-color: var(--color-success);
}

.chat-todo-text {
    flex: 1;
    font-size: var(--text-sm);
}

.chat-todo-card.completed .chat-todo-text {
    text-decoration: line-through;
    color: var(--color-text-muted);
}
```

---

## Confirmation Dialogs

For destructive actions, show inline confirmation:

```css
.confirmation-inline {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-2) var(--space-3);
    background: var(--color-warning-light);
    border-radius: var(--radius-md);
    margin-top: var(--space-2);
}

.confirm-btn {
    background: var(--color-error);
    color: white;
    border: none;
    padding: var(--space-1) var(--space-3);
    border-radius: var(--radius-md);
    cursor: pointer;
}

.cancel-btn {
    background: transparent;
    color: var(--color-text-secondary);
    border: none;
    cursor: pointer;
}
```

**Example:**
```
🗑️ Delete "Buy old groceries"?
[ Cancel ] [ Delete ]
```

---

## Empty State

```css
.chat-empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--space-12);
    text-align: center;
}

.chat-empty-icon {
    width: 64px;
    height: 64px;
    margin-bottom: var(--space-4);
    color: var(--color-text-muted);
}

.chat-empty-title {
    font-size: var(--text-xl);
    font-weight: 600;
    color: var(--color-text-primary);
    margin-bottom: var(--space-2);
}

.chat-empty-description {
    color: var(--color-text-secondary);
    max-width: 300px;
    margin-bottom: var(--space-6);
}

.chat-empty-suggestions {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
    text-align: left;
}
```

---

## Responsive Design

```css
/* Mobile: Full width messages */
@media (max-width: 640px) {
    .message {
        max-width: 90%;
    }

    .chat-input-container {
        margin: var(--space-2);
    }

    .quick-replies {
        padding: var(--space-2);
    }
}

/* Desktop: Constrained width */
@media (min-width: 1024px) {
    .chat-container {
        max-width: 800px;
        margin: 0 auto;
    }
}
```

---

## Accessibility

### ARIA Labels
```tsx
<div role="log" aria-live="polite">
    <div role="article" aria-label="User message">
        {/* Message content */}
    </div>
</div>

<input
    type="text"
    aria-label="Chat message"
    aria-multiline="true"
    placeholder="Type a message..."
/>

<button
    aria-label="Send message"
    aria-disabled={!message.trim()}
/>
    <SendIcon />
</button>
```

### Keyboard Navigation
```css
/* Focus visible */
.chat-input:focus-visible,
.quick-reply-btn:focus-visible,
.send-btn:focus-visible {
    outline: 2px solid var(--color-primary);
    outline-offset: 2px;
}

/* Skip to chat */
.skip-to-chat {
    position: absolute;
    top: -40px;
    left: 0;
    background: var(--color-primary);
    color: white;
    padding: var(--space-2) var(--space-4);
    z-index: 100;
}

.skip-to-chat:focus {
    top: 0;
}
```

### Screen Reader Messages
```tsx
// Announce new messages
useEffect(() => {
    if (newMessage) {
        announceToScreenReader(`New message from ${newMessage.role}: ${newMessage.content}`);
    }
}, [newMessage]);

// Announce loading state
announceToScreenReader("Assistant is typing...");
```

---

## Animations

```css
/* Message appear */
@keyframes messageAppear {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.message {
    animation: messageAppear 0.3s ease-out;
}

/* Send button hover */
.send-btn:active {
    transform: scale(0.95);
}

/* Pulse for important actions */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.urgent-message {
    animation: pulse 2s ease-in-out infinite;
}
```

---

## Error Handling UI

### Inline Error in Chat
```css
.chat-error {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-3);
    background: var(--color-error-light);
    color: var(--color-error);
    border-radius: var(--radius-md);
    margin-top: var(--space-2);
}

.chat-error-icon {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
}
```

**Example:**
```
⚠️ I couldn't find that task. Could you try again?
```

---

## Design Checklist

- [ ] Messages are readable and well-spaced
- [ ] User/AI distinction is clear (alignment, colors)
- [ ] Typing indicator shows during AI processing
- [ ] Quick replies for common actions
- [ ] Suggestions for follow-up actions
- [ ] Confirmation before destructive actions
- [ ] Empty state is friendly and helpful
- [ ] Loading states for all async operations
- [ ] Error messages are clear and actionable
- [ ] Works on mobile and desktop
- [ ] Keyboard navigation fully supported
- [ ] Screen reader announcements work
- [ ] Respects `prefers-reduced-motion`
