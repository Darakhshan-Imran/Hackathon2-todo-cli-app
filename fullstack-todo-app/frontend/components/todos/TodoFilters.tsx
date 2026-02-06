"use client";

import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import MenuItem from "@mui/material/MenuItem";
import type { TodoListParams } from "@/types/todo";

interface TodoFiltersProps {
  params: TodoListParams;
  onChange: (params: TodoListParams) => void;
}

export function TodoFilters({ params, onChange }: TodoFiltersProps) {
  const handleSortChange = (sortBy: string) => {
    onChange({
      ...params,
      sort_by: sortBy as "created_at" | "due_date" | "priority",
      page: 1,
    });
  };

  const handleOrderChange = (order: string) => {
    onChange({
      ...params,
      sort_order: order as "asc" | "desc",
      page: 1,
    });
  };

  return (
    <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap" }}>
      <TextField
        select
        size="small"
        label="Sort by"
        value={params.sort_by || "created_at"}
        onChange={(e) => handleSortChange(e.target.value)}
        sx={{ minWidth: 150 }}
      >
        <MenuItem value="created_at">Created Date</MenuItem>
        <MenuItem value="due_date">Due Date</MenuItem>
        <MenuItem value="priority">Priority</MenuItem>
      </TextField>

      <TextField
        select
        size="small"
        label="Order"
        value={params.sort_order || "desc"}
        onChange={(e) => handleOrderChange(e.target.value)}
        sx={{ minWidth: 150 }}
      >
        <MenuItem value="desc">Newest First</MenuItem>
        <MenuItem value="asc">Oldest First</MenuItem>
      </TextField>
    </Box>
  );
}
