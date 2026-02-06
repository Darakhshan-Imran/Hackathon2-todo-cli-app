# Email Verification Reference

## Configuration

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: { /* config */ },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: true,
  },
  emailVerification: {
    sendVerificationEmail: async ({ user, url, token }) => {
      // Implement email sending
      await sendEmail({
        to: user.email,
        subject: "Verify your email",
        html: `
          <h1>Welcome!</h1>
          <p>Click the link below to verify your email:</p>
          <a href="${url}">Verify Email</a>
        `,
      });
    },
    sendOnSignUp: true,
    autoSignInAfterVerification: true,
    expiresIn: 60 * 60,  // 1 hour
  },
});
```

## Email Service Integration

### Using Resend

```typescript
import { Resend } from "resend";

const resend = new Resend(process.env.RESEND_API_KEY);

export const auth = betterAuth({
  emailVerification: {
    sendVerificationEmail: async ({ user, url }) => {
      await resend.emails.send({
        from: "noreply@yourapp.com",
        to: user.email,
        subject: "Verify your email",
        html: `<a href="${url}">Verify Email</a>`,
      });
    },
  },
});
```

### Using Nodemailer

```typescript
import nodemailer from "nodemailer";

const transporter = nodemailer.createTransport({
  host: process.env.SMTP_HOST,
  port: 587,
  auth: {
    user: process.env.SMTP_USER,
    pass: process.env.SMTP_PASS,
  },
});

export const auth = betterAuth({
  emailVerification: {
    sendVerificationEmail: async ({ user, url }) => {
      await transporter.sendMail({
        from: "noreply@yourapp.com",
        to: user.email,
        subject: "Verify your email",
        html: `<a href="${url}">Verify Email</a>`,
      });
    },
  },
});
```

## Client-Side Implementation

### Request Verification Email

```typescript
// Send/resend verification email
await authClient.sendVerificationEmail({
  email: "user@example.com",
  callbackURL: "/auth/verified",
});
```

### Check Verification Status

```typescript
const { data: session } = useSession();

if (session && !session.user.emailVerified) {
  // Show verification prompt
}
```

### Verification Page

```tsx
// app/auth/verify/page.tsx
"use client";
import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import { authClient } from "@/lib/auth-client";

export default function VerifyPage() {
  const searchParams = useSearchParams();
  const token = searchParams.get("token");
  const [status, setStatus] = useState<"loading" | "success" | "error">("loading");

  useEffect(() => {
    if (token) {
      authClient.verifyEmail({ token })
        .then(() => setStatus("success"))
        .catch(() => setStatus("error"));
    }
  }, [token]);

  if (status === "loading") return <div>Verifying...</div>;
  if (status === "success") return <div>Email verified! Redirecting...</div>;
  return <div>Verification failed. Please try again.</div>;
}
```

## Verification Flow

```
1. User signs up
   ↓
2. sendVerificationEmail() called automatically (if sendOnSignUp: true)
   ↓
3. User receives email with verification link
   ↓
4. User clicks link → redirects to your app with token
   ↓
5. Call verifyEmail({ token })
   ↓
6. User's emailVerified set to true
   ↓
7. Auto sign-in (if autoSignInAfterVerification: true)
```

## Custom Verification URL

```typescript
export const auth = betterAuth({
  emailVerification: {
    sendVerificationEmail: async ({ user, url, token }) => {
      // Use custom URL structure
      const customUrl = `${process.env.NEXT_PUBLIC_APP_URL}/verify?token=${token}`;

      await sendEmail({
        to: user.email,
        subject: "Verify your email",
        html: `<a href="${customUrl}">Verify</a>`,
      });
    },
  },
});
```

## Blocking Unverified Users

### Middleware Approach

```typescript
// middleware.ts
export async function middleware(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  if (session && !session.user.emailVerified) {
    const { pathname } = request.nextUrl;

    // Allow verification-related routes
    if (!pathname.startsWith("/verify") && !pathname.startsWith("/resend")) {
      return NextResponse.redirect(new URL("/verify-required", request.url));
    }
  }

  return NextResponse.next();
}
```

### Component Approach

```tsx
function ProtectedContent({ children }: { children: React.ReactNode }) {
  const { data: session } = useSession();

  if (!session) {
    return <Redirect to="/login" />;
  }

  if (!session.user.emailVerified) {
    return (
      <div>
        <p>Please verify your email to continue.</p>
        <button onClick={() => authClient.sendVerificationEmail({
          email: session.user.email
        })}>
          Resend Verification Email
        </button>
      </div>
    );
  }

  return <>{children}</>;
}
```

## Email Templates

### HTML Template Example

```typescript
const verificationEmailTemplate = (url: string, userName: string) => `
<!DOCTYPE html>
<html>
<head>
  <style>
    .container { max-width: 600px; margin: 0 auto; font-family: sans-serif; }
    .button { background: #0070f3; color: white; padding: 12px 24px;
              text-decoration: none; border-radius: 4px; display: inline-block; }
  </style>
</head>
<body>
  <div class="container">
    <h1>Welcome, ${userName}!</h1>
    <p>Thanks for signing up. Please verify your email address by clicking the button below:</p>
    <p><a href="${url}" class="button">Verify Email</a></p>
    <p>This link will expire in 1 hour.</p>
    <p>If you didn't create an account, you can safely ignore this email.</p>
  </div>
</body>
</html>
`;
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Email not received | Check spam folder, verify SMTP config |
| Token expired | Increase expiresIn, resend verification |
| Invalid token | Ensure URL encoding is preserved |
| Auto sign-in not working | Check autoSignInAfterVerification setting |
