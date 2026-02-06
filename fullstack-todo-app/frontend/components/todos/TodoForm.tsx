"use client";

import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import MenuItem from "@mui/material/MenuItem";
import Chip from "@mui/material/Chip";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import CircularProgress from "@mui/material/CircularProgress";
import { todoCreateSchema, type TodoCreateFormData } from "@/lib/validators";
import { formatDateForInput } from "@/lib/utils";
import type { Todo } from "@/types/todo";

interface TodoFormProps {
  todo?: Todo;
  onSubmit: (data: TodoCreateFormData) => Promise<void>;
  isLoading: boolean;
  submitLabel?: string;
}

export function TodoForm({
  todo,
  onSubmit,
  isLoading,
  submitLabel = "Save",
}: TodoFormProps) {
  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<TodoCreateFormData>({
    resolver: zodResolver(todoCreateSchema),
    defaultValues: todo
      ? {
          title: todo.title,
          description: todo.description || "",
          status: todo.status,
          priority: todo.priority,
          due_date: formatDateForInput(todo.due_date),
        }
      : {
          title: "",
          description: "",
          status: "pending",
          priority: "medium",
          due_date: "",
        },
  });

  return (
    <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
      <Stack spacing={3}>
        <Controller
          name="title"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              label="Title"
              placeholder="What needs to be done?"
              fullWidth
              error={!!errors.title}
              helperText={errors.title?.message}
            />
          )}
        />

        <Controller
          name="description"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              label="Description"
              placeholder="Add some details..."
              fullWidth
              multiline
              rows={3}
            />
          )}
        />

        <Box sx={{ display: "grid", gridTemplateColumns: { xs: "1fr", sm: "1fr 1fr" }, gap: 2 }}>
          <Controller
            name="status"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                select
                label="Status"
                fullWidth
              >
                <MenuItem value="pending">Pending</MenuItem>
                <MenuItem value="in_progress">In Progress</MenuItem>
                <MenuItem value="completed">Completed</MenuItem>
              </TextField>
            )}
          />

          <Controller
            name="priority"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                select
                label="Priority"
                fullWidth
              >
                <MenuItem value="low">Low</MenuItem>
                <MenuItem value="medium">Medium</MenuItem>
                <MenuItem value="high">High</MenuItem>
              </TextField>
            )}
          />
        </Box>

        <Controller
          name="due_date"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              label="Due Date (optional)"
              type="datetime-local"
              fullWidth
              slotProps={{ inputLabel: { shrink: true } }}
            />
          )}
        />

        {todo && todo.tags.length > 0 && (
          <Box>
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

        <Button
          type="submit"
          variant="contained"
          fullWidth
          size="large"
          disabled={isLoading}
        >
          {isLoading ? <CircularProgress size={24} color="inherit" /> : submitLabel}
        </Button>
      </Stack>
    </Box>
  );
}
