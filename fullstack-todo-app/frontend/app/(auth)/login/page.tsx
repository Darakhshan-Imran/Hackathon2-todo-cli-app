"use client";

import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import { LoginForm } from "@/components/auth/LoginForm";

export default function LoginPage() {
  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          display: "flex",
          minHeight: "100vh",
          alignItems: "center",
          justifyContent: "center",
          py: 4,
        }}
      >
        <LoginForm />
      </Box>
    </Container>
  );
}
