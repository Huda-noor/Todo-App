"use client";

import { useState, FormEvent } from "react";
import Button from "@/components/ui/Button";

interface TodoFormProps {
  onSubmit: (description: string) => Promise<void>;
}

export default function TodoForm({ onSubmit }: TodoFormProps) {
  const [description, setDescription] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const validateDescription = (value: string): string | null => {
    if (!value.trim()) {
      return "Todo description cannot be empty";
    }
    if (value.length > 500) {
      return "Todo description cannot exceed 500 characters";
    }
    return null;
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    const validationError = validateDescription(description);
    if (validationError) {
      setError(validationError);
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      await onSubmit(description.trim());
      setDescription("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create todo");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="todo-form">
      <input
        type="text"
        className={`form-input ${error ? "error" : ""}`}
        value={description}
        onChange={(e) => {
          setDescription(e.target.value);
          if (error) setError(null);
        }}
        placeholder="What needs to be done?"
        disabled={isLoading}
        aria-label="New todo description"
        maxLength={500}
      />
      <Button type="submit" isLoading={isLoading} disabled={isLoading}>
        Add
      </Button>
      {error && <p className="form-error" role="alert">{error}</p>}
    </form>
  );
}
