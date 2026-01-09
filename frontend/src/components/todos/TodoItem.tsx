"use client";

import { useState, FormEvent } from "react";
import type { Todo } from "@/types";
import Button from "@/components/ui/Button";

interface TodoItemProps {
  todo: Todo;
  onToggle: (id: string) => Promise<void>;
  onUpdate: (id: string, description: string) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
}

export default function TodoItem({
  todo,
  onToggle,
  onUpdate,
  onDelete,
}: TodoItemProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editDescription, setEditDescription] = useState(todo.description);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  const handleToggle = async () => {
    setIsLoading(true);
    setError(null);
    try {
      await onToggle(todo.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to toggle todo");
    } finally {
      setIsLoading(false);
    }
  };

  const handleEditSubmit = async (e: FormEvent) => {
    e.preventDefault();

    const trimmed = editDescription.trim();
    if (!trimmed) {
      setError("Todo description cannot be empty");
      return;
    }
    if (trimmed.length > 500) {
      setError("Todo description cannot exceed 500 characters");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      await onUpdate(todo.id, trimmed);
      setIsEditing(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update todo");
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    setIsLoading(true);
    setError(null);
    try {
      await onDelete(todo.id);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete todo");
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditDescription(todo.description);
    setError(null);
  };

  return (
    <div className="todo-item" role="listitem">
      <input
        type="checkbox"
        className="todo-checkbox"
        checked={todo.is_complete}
        onChange={handleToggle}
        disabled={isLoading || isEditing}
        aria-label={`Mark "${todo.description}" as ${todo.is_complete ? "incomplete" : "complete"}`}
      />

      {isEditing ? (
        <form onSubmit={handleEditSubmit} className="todo-edit-form">
          <input
            type="text"
            className={`form-input ${error ? "error" : ""}`}
            value={editDescription}
            onChange={(e) => {
              setEditDescription(e.target.value);
              if (error) setError(null);
            }}
            disabled={isLoading}
            autoFocus
            maxLength={500}
            aria-label="Edit todo description"
          />
          <Button type="submit" variant="primary" size="sm" isLoading={isLoading}>
            Save
          </Button>
          <Button
            type="button"
            variant="secondary"
            size="sm"
            onClick={handleCancelEdit}
            disabled={isLoading}
          >
            Cancel
          </Button>
        </form>
      ) : (
        <>
          <div className="todo-content">
            <p className={`todo-description ${todo.is_complete ? "completed" : ""}`}>
              {todo.description}
            </p>
            <p className="todo-meta">Created {formatDate(todo.created_at)}</p>
            {error && <p className="form-error" role="alert">{error}</p>}
          </div>

          <div className="todo-actions">
            <Button
              type="button"
              variant="secondary"
              size="sm"
              onClick={() => setIsEditing(true)}
              disabled={isLoading}
            >
              Edit
            </Button>
            <Button
              type="button"
              variant="danger"
              size="sm"
              onClick={handleDelete}
              isLoading={isLoading}
            >
              Delete
            </Button>
          </div>
        </>
      )}
    </div>
  );
}
