"use client";

import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import Link from "next/link";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";
import { useAuth } from "@/context/AuthContext";
import { signupSchema, type SignupFormData } from "@/lib/validators";

export function SignupForm() {
  const { signup, isLoading, error, clearError } = useAuth();

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema),
    defaultValues: { email: "", username: "", password: "" },
  });

  const onSubmit = async (data: SignupFormData) => {
    await signup(data);
  };

  return (
    <Card sx={{ maxWidth: 440, width: "100%", mx: "auto" }}>
      <CardContent sx={{ p: 4 }}>
        <Box sx={{ textAlign: "center", mb: 3 }}>
          <Typography variant="h5" fontWeight={700}>
            Create your account
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Start managing your todos today
          </Typography>
        </Box>

        {error && (
          <Alert severity="error" onClose={clearError} sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate>
          <Controller
            name="email"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Email address"
                type="email"
                fullWidth
                margin="normal"
                autoComplete="email"
                error={!!errors.email}
                helperText={errors.email?.message}
              />
            )}
          />

          <Controller
            name="username"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Username"
                fullWidth
                margin="normal"
                autoComplete="username"
                error={!!errors.username}
                helperText={errors.username?.message}
              />
            )}
          />

          <Controller
            name="password"
            control={control}
            render={({ field }) => (
              <TextField
                {...field}
                label="Password"
                type="password"
                fullWidth
                margin="normal"
                autoComplete="new-password"
                error={!!errors.password}
                helperText={
                  errors.password?.message ||
                  "Min 8 characters with one uppercase, one lowercase, and one number."
                }
              />
            )}
          />

          <Button
            type="submit"
            variant="contained"
            fullWidth
            size="large"
            disabled={isLoading}
            sx={{ mt: 2, mb: 2 }}
          >
            {isLoading ? (
              <CircularProgress size={24} color="inherit" />
            ) : (
              "Create account"
            )}
          </Button>
        </Box>

        <Typography variant="body2" color="text.secondary" textAlign="center">
          Already have an account?{" "}
          <Link href="/login" style={{ color: "inherit", fontWeight: 600 }}>
            Sign in
          </Link>
        </Typography>
      </CardContent>
    </Card>
  );
}
