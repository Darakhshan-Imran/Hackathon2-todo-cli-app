"use client";

/**
 * Hook for managing todo state.
 */

import { useState, useCallback, useEffect, type Dispatch, type SetStateAction } from "react";
import { todoService } from "@/services/todo.service";
import { getErrorMessage } from "@/services/api";
import type { Todo, TodoCreate, TodoUpdate, TodoListParams } from "@/types/todo";

interface UseTodosReturn {
  todos: Todo[];
  pagination: {
    page: number;
    per_page: number;
    total: number;
    total_pages: number;
  };
  isLoading: boolean;
  error: string | null;
  params: TodoListParams;
  setParams: Dispatch<SetStateAction<TodoListParams>>;
  refresh: () => Promise<void>;
  createTodo: (data: TodoCreate) => Promise<Todo | null>;
  updateTodo: (id: string, data: TodoUpdate) => Promise<Todo | null>;
  deleteTodo: (id: string) => Promise<boolean>;
  clearError: () => void;
}

export function useTodos(initialParams?: TodoListParams): UseTodosReturn {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [pagination, setPagination] = useState({
    page: 1,
    per_page: 20,
    total: 0,
    total_pages: 0,
  });
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [params, setParams] = useState<TodoListParams>(initialParams || {});

  const fetchTodos = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await todoService.getTodos(params);
      if (response.success && response.data) {
        setTodos(response.data.items);
        setPagination({
          page: response.data.page,
          per_page: response.data.per_page,
          total: response.data.total,
          total_pages: response.data.total_pages,
        });
      } else {
        setError(response.error || "Failed to fetch todos");
      }
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setIsLoading(false);
    }
  }, [params]);

  useEffect(() => {
    fetchTodos();
  }, [fetchTodos]);

  const createTodo = useCallback(async (data: TodoCreate): Promise<Todo | null> => {
    setError(null);
    try {
      const response = await todoService.createTodo(data);
      if (response.success && response.data) {
        // Add to list
        setTodos((prev) => [response.data!, ...prev]);
        setPagination((prev) => ({ ...prev, total: prev.total + 1 }));
        return response.data;
      }
      setError(response.error || "Failed to create todo");
      return null;
    } catch (err) {
      setError(getErrorMessage(err));
      return null;
    }
  }, []);

  const updateTodo = useCallback(
    async (id: string, data: TodoUpdate): Promise<Todo | null> => {
      setError(null);
      try {
        const response = await todoService.updateTodo(id, data);
        if (response.success && response.data) {
          // Update in list
          setTodos((prev) =>
            prev.map((todo) => (todo.id === id ? response.data! : todo))
          );
          return response.data;
        }
        setError(response.error || "Failed to update todo");
        return null;
      } catch (err) {
        setError(getErrorMessage(err));
        return null;
      }
    },
    []
  );

  const deleteTodo = useCallback(async (id: string): Promise<boolean> => {
    setError(null);
    try {
      const response = await todoService.deleteTodo(id);
      if (response.success) {
        // Remove from list
        setTodos((prev) => prev.filter((todo) => todo.id !== id));
        setPagination((prev) => ({ ...prev, total: prev.total - 1 }));
        return true;
      }
      setError(response.error || "Failed to delete todo");
      return false;
    } catch (err) {
      setError(getErrorMessage(err));
      return false;
    }
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    todos,
    pagination,
    isLoading,
    error,
    params,
    setParams,
    refresh: fetchTodos,
    createTodo,
    updateTodo,
    deleteTodo,
    clearError,
  };
}
