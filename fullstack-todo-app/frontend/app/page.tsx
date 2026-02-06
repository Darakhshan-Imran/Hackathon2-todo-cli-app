"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";
import { useAuth } from "@/context/AuthContext";

export default function HomePage() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      if (isAuthenticated) {
        router.push("/todos");
      } else {
        router.push("/login");
      }
    }
  }, [isAuthenticated, isLoading, router]);

  return (
    <Box
      sx={{
        display: "flex",
        minHeight: "80vh",
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <CircularProgress size={48} />
    </Box>
  );
}
