# Data Model: AI Conversational Todo Interface (Phase III)

## Overview
This document defines the data models required for the AI Conversational Todo Interface (Phase III), extending the existing Phase II data model with conversation-specific entities while maintaining compatibility with existing structures.

## Entity Relationships

```
┌─────────────────┐       1:N       ┌─────────────────────────┐
│     user        │◄───────────────│  conversation_thread    │
├─────────────────┤                 ├─────────────────────────┤
│ id (PK)         │                 │ id (PK, UUID)           │
│ email           │                 │ user_id (FK)            │
│ password        │                 │ created_at              │
│ created_at      │                 │ updated_at              │
└─────────────────┘                 │ active                  │
                                    └─────────────────────────┘
                                        │
                                        │ 1:N
                                        ▼
                              ┌─────────────────────────┐
                              │  conversation_message   │
                              ├─────────────────────────┤
                              │ id (PK, UUID)           │
                              │ thread_id (FK)          │
                              │ role (enum)             │
                              │ content (text)          │
                              │ created_at              │
                              └─────────────────────────┘

Relationships:
- conversation_thread.user_id → user.id (CASCADE delete)
- conversation_message.thread_id → conversation_thread.id (CASCADE delete)
```

## Entity Definitions

### 1. ConversationThread
**Purpose**: Groups related messages into conversation sessions

**Fields**:
- `id`: UUID, Primary Key, auto-generated
- `user_id`: UUID, Foreign Key to user table, required
- `created_at`: DateTime, timestamp of thread creation, required, defaults to now
- `updated_at`: DateTime, timestamp of last activity, required, defaults to now
- `active`: Boolean, indicates if thread is currently active, defaults to true

**Validation Rules**:
- `user_id` must reference an existing user
- `created_at` must be before or equal to `updated_at`
- `active` can be updated but thread cannot be deleted while active

**State Transitions**:
- Active → Inactive: When conversation is concluded or archived
- Inactive → Active: When conversation is resumed (new message received)

### 2. ConversationMessage
**Purpose**: Individual messages in a conversation

**Fields**:
- `id`: UUID, Primary Key, auto-generated
- `thread_id`: UUID, Foreign Key to conversation_thread, required
- `role`: String enum ('user' | 'assistant'), required
- `content`: Text, message content, required, max length 10,000 characters
- `created_at`: DateTime, timestamp of message creation, required, defaults to now

**Validation Rules**:
- `thread_id` must reference an existing conversation_thread
- `role` must be either 'user' or 'assistant'
- `content` must not be empty or whitespace-only
- `content` must be less than 10,000 characters

**State Transitions**:
- Immutable: Once created, messages cannot be modified or deleted

## Integration with Existing Models

### 3. Todo (Extended from Phase II)
**Purpose**: Represents a todo item, referenced by conversation context

**Fields** (existing):
- `id`: Integer, Primary Key
- `user_id`: UUID, Foreign Key to user table
- `description`: Text, todo description
- `is_complete`: Boolean, completion status
- `created_at`: DateTime
- `updated_at`: DateTime

**Validation Rules** (existing):
- `user_id` must reference an existing user
- `description` must not be empty
- `is_complete` defaults to false

### 4. User (From Phase II)
**Purpose**: Represents an authenticated user, owner of conversations and todos

**Fields** (existing):
- `id`: UUID, Primary Key
- `email`: String, user email address
- `password`: String, hashed password
- `created_at`: DateTime

**Validation Rules** (existing):
- `email` must be unique and valid email format
- `password` must meet minimum security requirements

## Database Schema

### SQL Definition
```sql
-- Conversation thread table
CREATE TABLE conversation_thread (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    active BOOLEAN DEFAULT TRUE,

    CONSTRAINT fk_conversation_thread_user
        FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

-- Index for efficient user-based queries
CREATE INDEX idx_conversation_thread_user_id ON conversation_thread(user_id);

-- Index for efficient time-based queries
CREATE INDEX idx_conversation_thread_updated_at ON conversation_thread(updated_at DESC);

-- Conversation message table
CREATE TABLE conversation_message (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    thread_id UUID NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),

    CONSTRAINT fk_conversation_message_thread
        FOREIGN KEY (thread_id) REFERENCES conversation_thread(id) ON DELETE CASCADE
);

-- Index for efficient thread-based queries
CREATE INDEX idx_conversation_message_thread_id ON conversation_message(thread_id);

-- Index for efficient time-based queries
CREATE INDEX idx_conversation_message_created_at ON conversation_message(created_at ASC);
```

## API Data Transfer Objects

### 5. ChatRequest
**Purpose**: Represents a request to the chat API

**Fields**:
- `message`: String, required, user's message content
- `thread_id`: UUID, optional, existing conversation thread ID

**Validation**:
- `message` must be 1-10,000 characters
- `thread_id` must be a valid UUID format if provided

### 6. ChatResponse
**Purpose**: Represents a response from the chat API

**Fields**:
- `response`: String, required, AI-generated response
- `thread_id`: UUID, required, conversation thread ID
- `actions_taken`: Array of objects, optional, list of operations performed
- `suggestions`: Array of strings, optional, suggested follow-up actions

**Validation**:
- `response` must not be empty
- `thread_id` must be a valid UUID
- `actions_taken` items must follow the ActionObject schema

### 7. ActionObject
**Purpose**: Represents an action taken by the AI agent

**Fields**:
- `tool`: String, required, name of the tool called
- `description`: String, required, human-readable description of the action
- `result`: Object, optional, result of the tool execution

**Validation**:
- `tool` must be one of the five allowed tools
- `description` must not be empty

## Business Rules

### 1. Data Isolation
- Users can only access their own conversation threads and messages
- All database queries must be scoped by user_id

### 2. Conversation Context
- Messages within a thread are ordered chronologically
- Conversation history is loaded in chronological order for agent context

### 3. Data Retention
- Conversation threads and messages are retained for 1 year
- After 1 year, threads are soft-deleted and eventually purged

### 4. Thread Management
- Each user session starts a new conversation thread if none is provided
- Existing threads can be resumed by providing the thread_id
- Threads are marked inactive after 30 days of inactivity

## Performance Considerations

### 1. Indexing Strategy
- Index on user_id for efficient user-based queries
- Index on thread_id for efficient message retrieval
- Index on timestamps for chronological ordering

### 2. Pagination
- Conversation history should be paginated for long conversations
- Default page size: 50 messages
- Maximum page size: 200 messages

### 3. Context Window Management
- Limit conversation history to prevent exceeding token limits
- Retain most recent messages when context window is exceeded
- Maximum context: 50 most recent messages or 8,000 tokens, whichever is smaller

## Security Considerations

### 1. Access Control
- All data access must be validated against authenticated user
- No direct access to other users' conversations or messages

### 2. Data Encryption
- Sensitive data should be encrypted at rest
- Communication between services should be encrypted in transit

### 3. Input Validation
- All user input must be validated and sanitized
- Prevent injection attacks in message content