"use client";

import Stack from "@mui/material/Stack";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import CircularProgress from "@mui/material/CircularProgress";
import InboxIcon from "@mui/icons-material/Inbox";
import { TodoItem } from "./TodoItem";
import type { Todo, TodoStatus } from "@/types/todo";

interface TodoListProps {
  todos: Todo[];
  isLoading: boolean;
  onStatusChange: (id: string, status: TodoStatus) => void;
  onDelete: (id: string) => void;
}

export function TodoList({
  todos,
  isLoading,
  onStatusChange,
  onDelete,
}: TodoListProps) {
  if (isLoading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", py: 8 }}>
        <CircularProgress size={48} />
      </Box>
    );
  }

  if (todos.length === 0) {
    return (
      <Box sx={{ textAlign: "center", py: 8 }}>
        <InboxIcon sx={{ fontSize: 48, color: "text.secondary", mb: 2 }} />
        <Typography variant="h6" color="text.primary">
          No todos yet
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          Get started by creating a new todo.
        </Typography>
      </Box>
    );
  }

  return (
    <Stack spacing={1.5}>
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onStatusChange={onStatusChange}
          onDelete={onDelete}
        />
      ))}
    </Stack>
  );
}
