"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import { signOut, useSession, clearSessionToken } from "@/lib/auth-client";
import AuthGuard from "@/components/auth/AuthGuard";
import TodoForm from "@/components/todos/TodoForm";
import TodoList from "@/components/todos/TodoList";
import Loading from "@/components/ui/Loading";
import Button from "@/components/ui/Button";
import {
  listTodos,
  createTodo,
  updateTodo,
  deleteTodo,
  toggleTodo,
} from "@/lib/api-client";
import type { Todo } from "@/types";

function TodosContent() {
  const router = useRouter();
  const { data: session } = useSession();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const fetchTodos = useCallback(async () => {
    try {
      setError(null);
      const response = await listTodos();
      setTodos(response.todos);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load todos");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTodos();
  }, [fetchTodos]);

  const handleCreateTodo = async (description: string) => {
    const newTodo = await createTodo({ description });
    setTodos((prev) => [newTodo, ...prev]);
  };

  const handleToggleTodo = async (id: string) => {
    const updatedTodo = await toggleTodo(id);
    setTodos((prev) =>
      prev.map((todo) => (todo.id === id ? updatedTodo : todo))
    );
  };

  const handleUpdateTodo = async (id: string, description: string) => {
    const updatedTodo = await updateTodo(id, { description });
    setTodos((prev) =>
      prev.map((todo) => (todo.id === id ? updatedTodo : todo))
    );
  };

  const handleDeleteTodo = async (id: string) => {
    await deleteTodo(id);
    setTodos((prev) => prev.filter((todo) => todo.id !== id));
  };

  const handleLogout = async () => {
    setIsLoggingOut(true);
    try {
      await signOut();
      clearSessionToken(); // Clear local session token
      router.replace("/signin");
    } catch (err) {
      setError("Failed to sign out. Please try again.");
      setIsLoggingOut(false);
    }
  };

  if (isLoading) {
    return (
      <div className="todo-page">
        <Loading message="Loading your todos..." />
      </div>
    );
  }

  return (
    <div className="todo-page">
      <header className="header">
        <div className="container">
          <div className="header-content">
            <h1 className="header-title">My Todos</h1>
            <div className="header-user">
              <span className="header-email">{session?.user?.email}</span>
              <Button
                variant="secondary"
                size="sm"
                onClick={handleLogout}
                isLoading={isLoggingOut}
              >
                Sign Out
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="container">
        {error && (
          <div className="alert alert-error" role="alert">
            {error}
          </div>
        )}

        <TodoForm onSubmit={handleCreateTodo} />

        <TodoList
          todos={todos}
          onToggle={handleToggleTodo}
          onUpdate={handleUpdateTodo}
          onDelete={handleDeleteTodo}
        />
      </main>
    </div>
  );
}

export default function TodosPage() {
  return (
    <AuthGuard>
      <TodosContent />
    </AuthGuard>
  );
}
