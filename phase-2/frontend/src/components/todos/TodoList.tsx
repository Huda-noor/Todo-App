"use client";

import type { Todo } from "@/types";
import TodoItem from "./TodoItem";
import EmptyState from "./EmptyState";

interface TodoListProps {
  todos: Todo[];
  onToggle: (id: string) => Promise<void>;
  onUpdate: (id: string, description: string) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
}

export default function TodoList({
  todos,
  onToggle,
  onUpdate,
  onDelete,
}: TodoListProps) {
  if (todos.length === 0) {
    return <EmptyState />;
  }

  return (
    <div className="todo-list" role="list" aria-label="Todo list">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={onToggle}
          onUpdate={onUpdate}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
