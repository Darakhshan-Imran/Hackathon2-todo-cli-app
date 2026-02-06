"use client";

import Box from "@mui/material/Box";
import Pagination from "@mui/material/Pagination";
import Typography from "@mui/material/Typography";

interface TodoPaginationProps {
  page: number;
  totalPages: number;
  total: number;
  perPage: number;
  onPageChange: (page: number) => void;
}

export function TodoPagination({
  page,
  totalPages,
  total,
  perPage,
  onPageChange,
}: TodoPaginationProps) {
  if (totalPages <= 1) {
    return null;
  }

  const startItem = (page - 1) * perPage + 1;
  const endItem = Math.min(page * perPage, total);

  return (
    <Box
      sx={{
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        flexWrap: "wrap",
        gap: 2,
        pt: 2,
      }}
    >
      <Typography variant="body2" color="text.secondary">
        Showing {startItem} to {endItem} of {total} results
      </Typography>
      <Pagination
        count={totalPages}
        page={page}
        onChange={(_, value) => onPageChange(value)}
        color="primary"
        shape="rounded"
      />
    </Box>
  );
}
