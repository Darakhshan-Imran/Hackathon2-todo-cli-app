"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Alert from "@mui/material/Alert";
import Breadcrumbs from "@mui/material/Breadcrumbs";
import MuiLink from "@mui/material/Link";
import Link from "next/link";
import { todoService } from "@/services/todo.service";
import { getErrorMessage } from "@/services/api";
import { TodoForm } from "@/components/todos/TodoForm";
import type { TodoCreateFormData } from "@/lib/validators";

export default function NewTodoPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: TodoCreateFormData) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await todoService.createTodo({
        ...data,
        due_date: data.due_date || undefined,
      });
      if (response.success) {
        router.push("/todos");
      } else {
        setError(response.error || "Failed to create todo");
      }
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <Breadcrumbs sx={{ mb: 2 }}>
        <MuiLink component={Link} href="/todos" underline="hover" color="inherit">
          Todos
        </MuiLink>
        <Typography color="text.primary">New</Typography>
      </Breadcrumbs>

      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Create New Todo
      </Typography>

      {error && (
        <Alert severity="error" onClose={() => setError(null)} sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Paper sx={{ p: 3 }}>
        <TodoForm
          onSubmit={handleSubmit}
          isLoading={isLoading}
          submitLabel="Create Todo"
        />
      </Paper>
    </>
  );
}
