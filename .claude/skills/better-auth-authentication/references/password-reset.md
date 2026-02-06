# Password Reset Reference

## Configuration

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: { /* config */ },
  emailAndPassword: {
    enabled: true,
    sendResetPassword: async ({ user, url, token }) => {
      await sendEmail({
        to: user.email,
        subject: "Reset your password",
        html: `
          <h1>Password Reset Request</h1>
          <p>Click the link below to reset your password:</p>
          <a href="${url}">Reset Password</a>
          <p>This link expires in 1 hour.</p>
          <p>If you didn't request this, ignore this email.</p>
        `,
      });
    },
    resetPasswordTokenExpiresIn: 60 * 60,  // 1 hour
  },
});
```

## Password Reset Flow

```
1. User clicks "Forgot Password"
   ↓
2. User enters email address
   ↓
3. Call forgetPassword({ email })
   ↓
4. sendResetPassword() sends email with reset link
   ↓
5. User clicks link → redirects to reset page with token
   ↓
6. User enters new password
   ↓
7. Call resetPassword({ token, newPassword })
   ↓
8. Password updated, user can sign in
```

## Client-Side Implementation

### Forgot Password Form

```tsx
"use client";
import { useState } from "react";
import { authClient } from "@/lib/auth-client";

export function ForgotPasswordForm() {
  const [email, setEmail] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "sent" | "error">("idle");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("loading");

    try {
      await authClient.forgetPassword({
        email,
        redirectTo: "/auth/reset-password",
      });
      setStatus("sent");
    } catch (error) {
      setStatus("error");
    }
  };

  if (status === "sent") {
    return (
      <div>
        <h2>Check your email</h2>
        <p>We sent a password reset link to {email}</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Forgot Password</h2>
      <input
        type="email"
        placeholder="Enter your email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <button type="submit" disabled={status === "loading"}>
        {status === "loading" ? "Sending..." : "Send Reset Link"}
      </button>
      {status === "error" && <p>Failed to send reset email. Try again.</p>}
    </form>
  );
}
```

### Reset Password Form

```tsx
"use client";
import { useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import { authClient } from "@/lib/auth-client";

export function ResetPasswordForm() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get("token");

  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      setError("Passwords don't match");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    if (!token) {
      setError("Invalid reset link");
      return;
    }

    setStatus("loading");
    setError("");

    try {
      await authClient.resetPassword({
        token,
        newPassword: password,
      });
      setStatus("success");
      setTimeout(() => router.push("/login"), 2000);
    } catch (err) {
      setStatus("error");
      setError("Failed to reset password. Link may have expired.");
    }
  };

  if (status === "success") {
    return (
      <div>
        <h2>Password Reset Successful</h2>
        <p>Redirecting to login...</p>
      </div>
    );
  }

  return (
    <form onSubmit={handleSubmit}>
      <h2>Reset Password</h2>

      <input
        type="password"
        placeholder="New password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
        minLength={8}
      />

      <input
        type="password"
        placeholder="Confirm new password"
        value={confirmPassword}
        onChange={(e) => setConfirmPassword(e.target.value)}
        required
      />

      {error && <p className="error">{error}</p>}

      <button type="submit" disabled={status === "loading"}>
        {status === "loading" ? "Resetting..." : "Reset Password"}
      </button>
    </form>
  );
}
```

## Custom Reset URL

```typescript
export const auth = betterAuth({
  emailAndPassword: {
    sendResetPassword: async ({ user, url, token }) => {
      // Use custom URL
      const resetUrl = `${process.env.NEXT_PUBLIC_APP_URL}/auth/reset-password?token=${token}`;

      await sendEmail({
        to: user.email,
        subject: "Reset your password",
        html: `<a href="${resetUrl}">Reset Password</a>`,
      });
    },
  },
});
```

## Password Validation

### Server-Side Validation

```typescript
export const auth = betterAuth({
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
    // Custom password validation
    password: {
      hash: async (password) => {
        // Custom hashing (default uses bcrypt)
        return await bcrypt.hash(password, 12);
      },
      verify: async (data) => {
        return await bcrypt.compare(data.password, data.hash);
      },
    },
  },
});
```

### Client-Side Validation

```typescript
function validatePassword(password: string): string[] {
  const errors: string[] = [];

  if (password.length < 8) {
    errors.push("Must be at least 8 characters");
  }
  if (!/[A-Z]/.test(password)) {
    errors.push("Must contain uppercase letter");
  }
  if (!/[a-z]/.test(password)) {
    errors.push("Must contain lowercase letter");
  }
  if (!/[0-9]/.test(password)) {
    errors.push("Must contain number");
  }
  if (!/[^A-Za-z0-9]/.test(password)) {
    errors.push("Must contain special character");
  }

  return errors;
}
```

## Change Password (Authenticated Users)

```typescript
// User must be authenticated
await authClient.changePassword({
  currentPassword: "old-password",
  newPassword: "new-password",
  revokeOtherSessions: true,  // Optional: sign out other devices
});
```

### Change Password Form

```tsx
"use client";
import { useState } from "react";
import { authClient } from "@/lib/auth-client";

export function ChangePasswordForm() {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("loading");

    try {
      await authClient.changePassword({
        currentPassword,
        newPassword,
        revokeOtherSessions: true,
      });
      setStatus("success");
      setCurrentPassword("");
      setNewPassword("");
    } catch (error) {
      setStatus("error");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Change Password</h2>
      <input
        type="password"
        placeholder="Current password"
        value={currentPassword}
        onChange={(e) => setCurrentPassword(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="New password"
        value={newPassword}
        onChange={(e) => setNewPassword(e.target.value)}
        required
        minLength={8}
      />
      <button type="submit" disabled={status === "loading"}>
        {status === "loading" ? "Updating..." : "Change Password"}
      </button>
      {status === "success" && <p>Password updated successfully!</p>}
      {status === "error" && <p>Failed to update password.</p>}
    </form>
  );
}
```

## Security Considerations

1. **Rate Limiting**: Limit password reset requests per email
2. **Token Expiration**: Keep reset tokens short-lived (1 hour max)
3. **Single Use**: Tokens should be invalidated after use
4. **Email Enumeration**: Don't reveal if email exists (show same message)
5. **Session Invalidation**: Optionally revoke all sessions after reset

```typescript
// Don't reveal if email exists
await authClient.forgetPassword({ email });
// Always show: "If an account exists, we sent a reset link"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Token expired | Increase resetPasswordTokenExpiresIn |
| Invalid token | Check URL encoding, verify token format |
| Email not received | Check spam, verify SMTP configuration |
| Password not updating | Verify token hasn't been used already |
