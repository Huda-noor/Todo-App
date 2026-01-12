// User types
export interface User {
  id: string;
  email: string;
  created_at: string;
}

// Todo types
export interface Todo {
  id: string;
  description: string;
  is_complete: boolean;
  created_at: string;
  updated_at: string;
}

export interface TodoListResponse {
  todos: Todo[];
  count: number;
}

export interface CreateTodoRequest {
  description: string;
}

export interface UpdateTodoRequest {
  description: string;
}

// API response types
export interface ErrorResponse {
  error: string;
}

export interface MessageResponse {
  message: string;
}

// Form state types
export interface FormState {
  isLoading: boolean;
  error: string | null;
}
