# Data Model: Phase III - Conversational AI Interface

**Feature**: Phase III - Conversational AI Interface
**Date**: 2026-01-10
**Status**: Ready for Implementation

---

## Overview

Phase III introduces two new data models for storing conversation history: `conversation_threads` and `conversation_messages`. These models extend the existing Phase II data schema without modifying any existing tables.

## Entities

### 1. Conversation Thread

**Purpose**: Container for messages exchanged between a user and the AI agent.

**Table Name**: `conversation_threads`

#### Attributes

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| id | UUID | Yes | auto-generated | Unique identifier for the thread (primary key) |
| user_id | UUID | Yes | - | Reference to the owning user (foreign key) |
| created_at | timestamp | Yes | NOW() | When the thread was created |
| updated_at | timestamp | Yes | NOW() | When the thread was last updated |

#### Relationships

- **Belongs to**: `User` (many-to-one)
- **Has many**: `ConversationMessage` (one-to-many)

#### Constraints

- Primary key: `id`
- Foreign key: `user_id` → `users.id`
- Cascade delete: Deleting a user deletes all their threads

#### Indexes

- `idx_conversation_threads_user_id` on `user_id` (for efficient user thread lookup)
- `idx_conversation_threads_created_at` on `created_at` (for chronological sorting)

#### Lifecycle

1. **Creation**: Created when user sends first chat message without `thread_id`
2. **Update**: `updated_at` updated on each new message
3. **Deletion**: Cascade deleted when user is deleted

---

### 2. Conversation Message

**Purpose**: Individual message in a conversation thread.

**Table Name**: `conversation_messages`

#### Attributes

| Attribute | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| id | UUID | Yes | auto-generated | Unique identifier for the message (primary key) |
| thread_id | UUID | Yes | - | Reference to the conversation thread (foreign key) |
| role | enum | Yes | - | Role of the sender: "user" or "assistant" |
| content | text | Yes | - | Message content (natural language text) |
| created_at | timestamp | Yes | NOW() | When the message was created |

#### Relationships

- **Belongs to**: `ConversationThread` (many-to-one)

#### Constraints

- Primary key: `id`
- Foreign key: `thread_id` → `conversation_threads.id`
- Role check: `role IN ('user', 'assistant')`
- Cascade delete: Deleting a thread deletes all its messages

#### Indexes

- `idx_conversation_messages_thread_id` on `thread_id` (for efficient message retrieval)
- `idx_conversation_messages_created_at` on `created_at` (for chronological ordering)

#### Lifecycle

1. **Creation**: Created when user sends a message (role="user") or agent responds (role="assistant")
2. **Immutability**: Messages are never modified after creation (append-only pattern)

---

## Entity Relationships

```
User (existing Phase II)
  |
  | (1:many)
  |
  +--- ConversationThread (new Phase III)
        |
        | (1:many)
        |
        +--- ConversationMessage (new Phase III)

User (existing Phase II)
  |
  | (1:many)
  |
  +--- Todo (existing Phase II)
```

---

## State Transitions

### Conversation Thread

| State | Description | Trigger |
|-------|-------------|---------|
| New | Thread created but no messages | First chat request |
| Active | Thread has messages | User message received or agent responded |

**Note**: Threads do not have a "deleted" state - they are cascade deleted when the user is deleted.

### Conversation Message

Messages are immutable - no state transitions after creation.

---

## Validation Rules

### Conversation Thread

| Rule | Condition | Error |
|------|-----------|-------|
| user_id required | `user_id` is null | Foreign key constraint |
| user_id exists | `user_id` not in users table | Foreign key constraint |
| Valid timestamps | `created_at` < `updated_at` | Application validation |

### Conversation Message

| Rule | Condition | Error |
|------|-----------|-------|
| thread_id required | `thread_id` is null | Foreign key constraint |
| thread_id exists | `thread_id` not in conversation_threads table | Foreign key constraint |
| role required | `role` is null or not 'user'/'assistant' | Check constraint |
| content required | `content` is null or empty | Application validation |
| content length | `content` length > 10000 characters | Application validation |

---

## Database Schema (DDL)

### Migration SQL

```sql
-- Create conversation_threads table
CREATE TABLE conversation_threads (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create indexes for conversation_threads
CREATE INDEX idx_conversation_threads_user_id ON conversation_threads(user_id);
CREATE INDEX idx_conversation_threads_created_at ON conversation_threads(created_at);

-- Create conversation_messages table
CREATE TABLE conversation_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    thread_id UUID NOT NULL REFERENCES conversation_threads(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL CHECK (char_length(content) > 0 AND char_length(content) <= 10000),
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Create indexes for conversation_messages
CREATE INDEX idx_conversation_messages_thread_id ON conversation_messages(thread_id);
CREATE INDEX idx_conversation_messages_created_at ON conversation_messages(created_at);
```

---

## Query Patterns

### Load Conversation Thread with Messages

```sql
-- Get thread and verify ownership
SELECT * FROM conversation_threads
WHERE id = $thread_id AND user_id = $user_id;

-- Get all messages for thread in chronological order
SELECT * FROM conversation_messages
WHERE thread_id = $thread_id
ORDER BY created_at ASC;
```

### Create New Thread

```sql
INSERT INTO conversation_threads (id, user_id, created_at, updated_at)
VALUES (gen_random_uuid(), $user_id, NOW(), NOW())
RETURNING id;
```

### Add Message to Thread

```sql
INSERT INTO conversation_messages (id, thread_id, role, content, created_at)
VALUES (gen_random_uuid(), $thread_id, $role, $content, NOW());

UPDATE conversation_threads
SET updated_at = NOW()
WHERE id = $thread_id;
```

### Get User's Threads

```sql
SELECT * FROM conversation_threads
WHERE user_id = $user_id
ORDER BY updated_at DESC;
```

---

## Migration Notes

### Backward Compatibility

- No modifications to existing `users` or `todos` tables
- New tables are additive only
- Existing Phase II functionality remains unaffected

### Deployment Order

1. Create `conversation_threads` table
2. Create indexes for `conversation_threads`
3. Create `conversation_messages` table
4. Create indexes for `conversation_messages`
5. Verify foreign key constraints

### Rollback Strategy

If rollback is needed:

```sql
DROP TABLE conversation_messages;
DROP TABLE conversation_threads;
```

---

**Status**: Ready for implementation
