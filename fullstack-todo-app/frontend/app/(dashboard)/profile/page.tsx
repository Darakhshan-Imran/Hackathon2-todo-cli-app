"use client";

import { useState } from "react";
import { useForm, Controller } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import Alert from "@mui/material/Alert";
import Avatar from "@mui/material/Avatar";
import Box from "@mui/material/Box";
import Stack from "@mui/material/Stack";
import Divider from "@mui/material/Divider";
import CircularProgress from "@mui/material/CircularProgress";
import EditIcon from "@mui/icons-material/Edit";
import { useAuth } from "@/context/AuthContext";
import { userService } from "@/services/user.service";
import { getErrorMessage } from "@/services/api";
import { usernameUpdateSchema, type UsernameUpdateFormData } from "@/lib/validators";
import { formatDate } from "@/lib/utils";

export default function ProfilePage() {
  const { user } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const {
    control,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<UsernameUpdateFormData>({
    resolver: zodResolver(usernameUpdateSchema),
    defaultValues: {
      username: user?.username || "",
    },
  });

  const onSubmit = async (data: UsernameUpdateFormData) => {
    setIsSaving(true);
    setError(null);
    setSuccess(false);
    try {
      const response = await userService.updateProfile(data);
      if (response.success) {
        setSuccess(true);
        setIsEditing(false);
        window.location.reload();
      } else {
        setError(response.error || "Failed to update profile");
      }
    } catch (err) {
      setError(getErrorMessage(err));
    } finally {
      setIsSaving(false);
    }
  };

  const handleCancel = () => {
    setIsEditing(false);
    reset({ username: user?.username || "" });
    setError(null);
  };

  if (!user) {
    return null;
  }

  return (
    <>
      <Typography variant="h5" fontWeight={700} sx={{ mb: 3 }}>
        Profile
      </Typography>

      {error && (
        <Alert severity="error" onClose={() => setError(null)} sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          Profile updated successfully!
        </Alert>
      )}

      <Card>
        <CardContent sx={{ p: 3 }}>
          <Box sx={{ display: "flex", alignItems: "center", mb: 3 }}>
            <Avatar
              sx={{
                width: 64,
                height: 64,
                bgcolor: "primary.main",
                fontSize: 28,
                mr: 2,
              }}
            >
              {user.username.charAt(0).toUpperCase()}
            </Avatar>
            <Box>
              <Typography variant="h6">{user.username}</Typography>
              <Typography variant="body2" color="text.secondary">
                {user.email}
              </Typography>
            </Box>
          </Box>

          <Divider sx={{ my: 2 }} />

          <Stack spacing={3}>
            <Box>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                Email
              </Typography>
              <Typography variant="body1">{user.email}</Typography>
              <Typography variant="caption" color="text.secondary">
                Email cannot be changed
              </Typography>
            </Box>

            {isEditing ? (
              <Box component="form" onSubmit={handleSubmit(onSubmit)}>
                <Controller
                  name="username"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Username"
                      fullWidth
                      error={!!errors.username}
                      helperText={errors.username?.message}
                      sx={{ mb: 2 }}
                    />
                  )}
                />
                <Stack direction="row" spacing={1}>
                  <Button
                    type="submit"
                    variant="contained"
                    disabled={isSaving}
                  >
                    {isSaving ? (
                      <CircularProgress size={20} color="inherit" />
                    ) : (
                      "Save"
                    )}
                  </Button>
                  <Button variant="outlined" onClick={handleCancel}>
                    Cancel
                  </Button>
                </Stack>
              </Box>
            ) : (
              <Box>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                  Username
                </Typography>
                <Box sx={{ display: "flex", alignItems: "center", justifyContent: "space-between" }}>
                  <Typography variant="body1">{user.username}</Typography>
                  <Button
                    size="small"
                    startIcon={<EditIcon />}
                    onClick={() => setIsEditing(true)}
                  >
                    Edit
                  </Button>
                </Box>
              </Box>
            )}

            <Box>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                Member since
              </Typography>
              <Typography variant="body1">{formatDate(user.created_at)}</Typography>
            </Box>
          </Stack>
        </CardContent>
      </Card>
    </>
  );
}
