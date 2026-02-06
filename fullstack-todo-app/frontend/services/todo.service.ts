/**
 * Todo API service.
 */

import { api } from "./api";
import type { APIResponse, PaginatedData } from "@/types/api";
import type { Todo, TodoCreate, TodoUpdate, TodoListParams } from "@/types/todo";

export const todoService = {
  /**
   * Get all todos for the current user with optional filtering.
   */
  async getTodos(
    params?: TodoListParams
  ): Promise<APIResponse<PaginatedData<Todo>>> {
    const response = await api.get<APIResponse<PaginatedData<Todo>>>("/todos", {
      params,
    });
    return response.data;
  },

  /**
   * Get a single todo by ID.
   */
  async getTodo(id: string): Promise<APIResponse<Todo>> {
    const response = await api.get<APIResponse<Todo>>(`/todos/${id}`);
    return response.data;
  },

  /**
   * Create a new todo.
   */
  async createTodo(data: TodoCreate): Promise<APIResponse<Todo>> {
    const response = await api.post<APIResponse<Todo>>("/todos", data);
    return response.data;
  },

  /**
   * Update a todo.
   */
  async updateTodo(id: string, data: TodoUpdate): Promise<APIResponse<Todo>> {
    const response = await api.patch<APIResponse<Todo>>(`/todos/${id}`, data);
    return response.data;
  },

  /**
   * Delete a todo (soft delete).
   */
  async deleteTodo(id: string): Promise<APIResponse<null>> {
    const response = await api.delete<APIResponse<null>>(`/todos/${id}`);
    return response.data;
  },
};
