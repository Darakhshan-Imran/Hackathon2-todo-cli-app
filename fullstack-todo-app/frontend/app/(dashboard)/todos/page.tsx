"use client";

import { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Snackbar from "@mui/material/Snackbar";
import Alert from "@mui/material/Alert";
import Dialog from "@mui/material/Dialog";
import DialogTitle from "@mui/material/DialogTitle";
import DialogContent from "@mui/material/DialogContent";
import DialogContentText from "@mui/material/DialogContentText";
import DialogActions from "@mui/material/DialogActions";
import Button from "@mui/material/Button";
import { useTodos } from "@/hooks/useTodos";
import { TodoList } from "@/components/todos/TodoList";
import { TodoFilters } from "@/components/todos/TodoFilters";
import { TodoPagination } from "@/components/todos/TodoPagination";
import type { TodoStatus, Priority, DueFilter } from "@/types/todo";

export default function TodosPage() {
  const searchParams = useSearchParams();

  const statusFilter = searchParams.get("status") as TodoStatus | null;
  const priorityFilter = searchParams.get("priority") as Priority | null;
  const dueFilter = searchParams.get("due") as DueFilter | null;

  const {
    todos,
    pagination,
    isLoading,
    error,
    params,
    setParams,
    updateTodo,
    deleteTodo,
    clearError,
  } = useTodos({
    status: statusFilter || undefined,
    priority: priorityFilter || undefined,
    due: dueFilter || undefined,
  });

  // Sync URL params to useTodos params
  useEffect(() => {
    setParams((prev) => ({
      ...prev,
      status: statusFilter || undefined,
      priority: priorityFilter || undefined,
      due: dueFilter || undefined,
      page: 1,
    }));
  }, [statusFilter, priorityFilter, dueFilter, setParams]);

  const [deleteDialogId, setDeleteDialogId] = useState<string | null>(null);
  const [snackbar, setSnackbar] = useState<{
    open: boolean;
    message: string;
    severity: "success" | "error";
  }>({ open: false, message: "", severity: "success" });

  const handleStatusChange = async (id: string, status: TodoStatus) => {
    const result = await updateTodo(id, { status });
    if (result) {
      setSnackbar({ open: true, message: "Status updated", severity: "success" });
    }
  };

  const handleDeleteClick = (id: string) => {
    setDeleteDialogId(id);
  };

  const handleDeleteConfirm = async () => {
    if (deleteDialogId) {
      const success = await deleteTodo(deleteDialogId);
      if (success) {
        setSnackbar({ open: true, message: "Todo deleted", severity: "success" });
      }
      setDeleteDialogId(null);
    }
  };

  const handlePageChange = (page: number) => {
    setParams({ ...params, page });
  };

  return (
    <Box>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        {dueFilter === "today"
          ? "Today's Todos"
          : dueFilter === "upcoming"
          ? "Upcoming Todos"
          : statusFilter
          ? `${statusFilter.replace("_", " ").replace(/\b\w/g, (c) => c.toUpperCase())} Todos`
          : priorityFilter
          ? `${priorityFilter.charAt(0).toUpperCase() + priorityFilter.slice(1)} Priority`
          : "All Todos"}
      </Typography>

      {error && (
        <Alert severity="error" onClose={clearError} sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <TodoFilters params={params} onChange={setParams} />

      <Box sx={{ mt: 3 }}>
        <TodoList
          todos={todos}
          isLoading={isLoading}
          onStatusChange={handleStatusChange}
          onDelete={handleDeleteClick}
        />
      </Box>

      <Box sx={{ mt: 3 }}>
        <TodoPagination
          page={pagination.page}
          totalPages={pagination.total_pages}
          total={pagination.total}
          perPage={pagination.per_page}
          onPageChange={handlePageChange}
        />
      </Box>

      {/* Delete confirmation dialog */}
      <Dialog
        open={!!deleteDialogId}
        onClose={() => setDeleteDialogId(null)}
      >
        <DialogTitle>Delete Todo</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete this todo? This action cannot be
            undone.
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogId(null)}>Cancel</Button>
          <Button onClick={handleDeleteConfirm} color="error" variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={3000}
        onClose={() => setSnackbar((prev) => ({ ...prev, open: false }))}
        anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
      >
        <Alert
          onClose={() => setSnackbar((prev) => ({ ...prev, open: false }))}
          severity={snackbar.severity}
          variant="filled"
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}
