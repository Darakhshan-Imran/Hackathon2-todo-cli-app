"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import Link from "next/link";
import Paper from "@mui/material/Paper";
import Typography from "@mui/material/Typography";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Breadcrumbs from "@mui/material/Breadcrumbs";
import MuiLink from "@mui/material/Link";
import CircularProgress from "@mui/material/CircularProgress";
import Chip from "@mui/material/Chip";
import Stack from "@mui/material/Stack";
import { todoService } from "@/services/todo.service";
import { getErrorMessage } from "@/services/api";
import { TodoForm } from "@/components/todos/TodoForm";
import type { Todo } from "@/types/todo";
import type { TodoCreateFormData } from "@/lib/validators";

export default function TodoDetailPage() {
  const router = useRouter();
  const params = useParams();
  const todoId = params.id as string;

  const [todo, setTodo] = useState<Todo | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTodo = async () => {
      try {
        const response = await todoService.getTodo(todoId);
        if (response.success && response.data) {
          setTodo(response.data);
        } else {
          setError(response.error || "Todo not found");
        }
      } catch (err) {
        setError(getErrorMessage(err));
      } finally {
        setIsLoading(false);
      }
    };

    fetchTodo();
  }, [todoId]);

  const handleSubmit = async (data: TodoCreateFormData) => {
    setIsSaving(true);
    setError(null);
    try {
      const response = await todoService.updateTodo(todoId, {
        ...data,
        due_date: data.due_date || undefined,
      });
      if (response.success) {
        router.push("/todos");
      } else {
        setError(response.error || "Failed to update todo");
      }
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <Box
        sx={{
          display: "flex",
          minHeight: "60vh",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <CircularProgress size={48} />
      </Box>
    );
  }

  if (!todo) {
    return (
      <Box sx={{ textAlign: "center", py: 8 }}>
        <Typography variant="h5" fontWeight={700}>
          Todo not found
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          The todo you&apos;re looking for doesn&apos;t exist or has been deleted.
        </Typography>
        <Button
          component={Link}
          href="/todos"
          variant="contained"
          sx={{ mt: 3 }}
        >
          Back to Todos
        </Button>
      </Box>
    );
  }

  return (
    <>
      <Breadcrumbs sx={{ mb: 2 }}>
        <MuiLink component={Link} href="/todos" underline="hover" color="inherit">
          Todos
        </MuiLink>
        <Typography color="text.primary">Edit</Typography>
      </Breadcrumbs>

      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Edit Todo
      </Typography>

      {error && (
        <Alert severity="error" onClose={() => setError(null)} sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {todo.tags.length > 0 && (
        <Box sx={{ mb: 2 }}>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
            Auto-generated Tags
          </Typography>
          <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap>
            {todo.tags.map((tag) => (
              <Chip key={tag} label={tag} size="small" variant="outlined" />
            ))}
          </Stack>
        </Box>
      )}

      <Paper sx={{ p: 3 }}>
        <TodoForm
          todo={todo}
          onSubmit={handleSubmit}
          isLoading={isSaving}
          submitLabel="Save Changes"
        />
      </Paper>
    </>
  );
}
