/**
 * Todo types matching backend schema.
 */

export type TodoStatus = "pending" | "in_progress" | "completed";
export type Priority = "low" | "medium" | "high";

export interface Todo {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  status: TodoStatus;
  priority: Priority;
  due_date: string | null;
  tags: string[];
  created_at: string;
  updated_at: string;
}

export interface TodoCreate {
  title: string;
  description?: string;
  status?: TodoStatus;
  priority?: Priority;
  due_date?: string;
}

export interface TodoUpdate {
  title?: string;
  description?: string;
  status?: TodoStatus;
  priority?: Priority;
  due_date?: string;
}

export type DueFilter = "today" | "upcoming";

export interface TodoListParams {
  page?: number;
  per_page?: number;
  status?: TodoStatus;
  priority?: Priority;
  due?: DueFilter;
  sort_by?: "created_at" | "due_date" | "priority";
  sort_order?: "asc" | "desc";
}
