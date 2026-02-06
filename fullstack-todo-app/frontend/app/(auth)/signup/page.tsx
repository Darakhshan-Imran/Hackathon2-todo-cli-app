"use client";

import Container from "@mui/material/Container";
import Box from "@mui/material/Box";
import { SignupForm } from "@/components/auth/SignupForm";

export default function SignupPage() {
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
        <SignupForm />
      </Box>
    </Container>
  );
}
