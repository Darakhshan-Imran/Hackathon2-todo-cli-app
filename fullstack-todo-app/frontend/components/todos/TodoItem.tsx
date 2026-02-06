"use client";

import Link from "next/link";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Checkbox from "@mui/material/Checkbox";
import Chip from "@mui/material/Chip";
import IconButton from "@mui/material/IconButton";
import Stack from "@mui/material/Stack";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import { formatDate, isOverdue } from "@/lib/utils";
import { priorityColors, statusColors } from "@/lib/theme";
import type { Todo, TodoStatus } from "@/types/todo";

interface TodoItemProps {
  todo: Todo;
  onStatusChange: (id: string, status: TodoStatus) => void;
  onDelete: (id: string) => void;
}

const statusLabels: Record<TodoStatus, string> = {
  pending: "Pending",
  in_progress: "In Progress",
  completed: "Completed",
};

export function TodoItem({ todo, onStatusChange, onDelete }: TodoItemProps) {
  const overdue = isOverdue(todo.due_date);

  const handleStatusToggle = () => {
    const nextStatus: Record<TodoStatus, TodoStatus> = {
      pending: "in_progress",
      in_progress: "completed",
      completed: "pending",
    };
    onStatusChange(todo.id, nextStatus[todo.status]);
  };

  return (
    <Paper
      variant="outlined"
      sx={{
        p: 2,
        transition: "box-shadow 0.2s",
        "&:hover": { boxShadow: 2 },
        borderColor:
          overdue && todo.status !== "completed" ? "error.main" : "divider",
      }}
    >
      <Box sx={{ display: "flex", alignItems: "flex-start", gap: 1 }}>
        <Checkbox
          checked={todo.status === "completed"}
          onChange={handleStatusToggle}
          sx={{
            color: priorityColors[todo.priority],
            "&.Mui-checked": {
              color: priorityColors[todo.priority],
            },
            mt: -0.5,
          }}
        />

        <Box sx={{ flex: 1, minWidth: 0 }}>
          <Link href={`/todos/${todo.id}`} style={{ textDecoration: "none", color: "inherit" }}>
            <Typography
              variant="body1"
              fontWeight={500}
              sx={{
                textDecoration: todo.status === "completed" ? "line-through" : "none",
                color: todo.status === "completed" ? "text.secondary" : "text.primary",
                "&:hover": { color: "primary.main" },
              }}
            >
              {todo.title}
            </Typography>
          </Link>

          {todo.description && (
            <Typography
              variant="body2"
              color="text.secondary"
              sx={{
                mt: 0.5,
                overflow: "hidden",
                textOverflow: "ellipsis",
                display: "-webkit-box",
                WebkitLineClamp: 2,
                WebkitBoxOrient: "vertical",
              }}
            >
              {todo.description}
            </Typography>
          )}

          <Stack direction="row" spacing={1} sx={{ mt: 1 }} flexWrap="wrap" useFlexGap>
            <Chip
              label={statusLabels[todo.status]}
              size="small"
              sx={{
                bgcolor: `${statusColors[todo.status]}20`,
                color: statusColors[todo.status],
                fontWeight: 500,
              }}
            />
            <Chip
              label={todo.priority}
              size="small"
              sx={{
                bgcolor: `${priorityColors[todo.priority]}20`,
                color: priorityColors[todo.priority],
                fontWeight: 500,
                textTransform: "capitalize",
              }}
            />
            {todo.due_date && (
              <Chip
                label={`Due: ${formatDate(todo.due_date)}`}
                size="small"
                color={overdue && todo.status !== "completed" ? "error" : "default"}
                variant="outlined"
              />
            )}
            {todo.tags.map((tag) => (
              <Chip
                key={tag}
                label={tag}
                size="small"
                variant="outlined"
              />
            ))}
          </Stack>
        </Box>

        <Stack direction="row" spacing={0.5}>
          <IconButton
            size="small"
            component={Link}
            href={`/todos/${todo.id}`}
            color="default"
          >
            <EditIcon fontSize="small" />
          </IconButton>
          <IconButton
            size="small"
            onClick={() => onDelete(todo.id)}
            color="error"
          >
            <DeleteIcon fontSize="small" />
          </IconButton>
        </Stack>
      </Box>
    </Paper>
  );
}
