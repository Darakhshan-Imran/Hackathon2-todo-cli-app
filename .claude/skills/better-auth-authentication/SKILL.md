---
name: better-auth-authentication
description: |
  Implements authentication with Better Auth and JWT for Next.js applications.
  This skill should be used when users need to add authentication (sign-up, sign-in,
  sign-out, OAuth, JWT tokens, sessions) to TypeScript/Next.js projects using Better Auth.
---

# Better Auth Authentication

Implement production-ready authentication with Better Auth - the comprehensive TypeScript authentication framework.

## Before Implementation

| Source | Gather |
|--------|--------|
| **Codebase** | Existing auth setup, database schema, API routes, middleware |
| **Conversation** | User's auth requirements, OAuth providers needed, security constraints |
| **Skill References** | Better Auth patterns from `references/` |
| **User Guidelines** | Project conventions, environment setup |

## Workflow

```
1. Setup → 2. Configure → 3. Implement → 4. Secure → 5. Test
```

### Step 1: Installation & Setup

```bash
npm install better-auth
```

**Environment Variables** (`.env`):
```env
BETTER_AUTH_SECRET=your-32-char-secret-key  # openssl rand -base64 32
BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://user:pass@localhost:5432/db
```

**Create Auth Instance** (`lib/auth.ts`):
```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: {
    provider: "pg",
    url: process.env.DATABASE_URL!,
  },
  emailAndPassword: {
    enabled: true,
    minPasswordLength: 8,
  },
});
```

### Step 2: Database Migration

```bash
npx @better-auth/cli generate  # Creates migration files
npx @better-auth/cli migrate   # Applies migrations
```

### Step 3: API Route Handler

**Next.js App Router** (`app/api/auth/[...all]/route.ts`):
```typescript
import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

### Step 4: Client Setup

**Create Client** (`lib/auth-client.ts`):
```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL,
});

export const { signIn, signUp, signOut, useSession } = authClient;
```

## Authentication Methods

### Email/Password

```typescript
// Sign Up
const { data, error } = await signUp.email({
  email: "user@example.com",
  password: "securepassword123",
  name: "John Doe",
  callbackURL: "/dashboard",
});

// Sign In
const { data, error } = await signIn.email({
  email: "user@example.com",
  password: "securepassword123",
  rememberMe: true,
});

// Sign Out
await signOut();
```

### Social OAuth Providers

**Server Configuration** (`lib/auth.ts`):
```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  // ... database config
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
  },
});
```

**Client Usage**:
```typescript
await signIn.social({
  provider: "google",
  callbackURL: "/dashboard",
  errorCallbackURL: "/auth/error",
});
```

### Session Management

**Client-Side (React Hook)**:
```typescript
function Dashboard() {
  const { data: session, isPending, error } = useSession();

  if (isPending) return <Loading />;
  if (!session) return <Redirect to="/login" />;

  return <div>Welcome, {session.user.name}</div>;
}
```

**Server-Side (Next.js)**:
```typescript
import { auth } from "@/lib/auth";
import { headers } from "next/headers";

export async function getServerSession() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });
  return session;
}
```

## JWT Token Integration

See `references/jwt-plugin.md` for detailed JWT configuration.

**Quick Setup**:
```typescript
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  // ... other config
  plugins: [
    jwt({
      jwt: {
        expirationTime: "15m",
        issuer: "your-app",
        audience: "your-app",
      },
    }),
  ],
});
```

**Client JWT Retrieval**:
```typescript
import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [jwtClient()],
});

// Get JWT token
const { token } = await authClient.getToken();
```

## Middleware Protection

**Next.js Middleware** (`middleware.ts`):
```typescript
import { auth } from "@/lib/auth";
import { NextRequest, NextResponse } from "next/server";

const protectedRoutes = ["/dashboard", "/settings", "/api/protected"];
const authRoutes = ["/login", "/signup"];

export async function middleware(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  const { pathname } = request.nextUrl;

  // Redirect authenticated users away from auth pages
  if (authRoutes.some(route => pathname.startsWith(route)) && session) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  // Protect routes
  if (protectedRoutes.some(route => pathname.startsWith(route)) && !session) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"],
};
```

## Security Best Practices

1. **Secret Key**: Use `openssl rand -base64 32` for BETTER_AUTH_SECRET
2. **HTTPS**: Always use HTTPS in production
3. **Cookie Settings**: Enable secure cookies in production
4. **Rate Limiting**: Configure rate limiting for auth endpoints
5. **Password Policy**: Enforce minimum 8 characters, consider complexity rules

```typescript
export const auth = betterAuth({
  // ... config
  advanced: {
    useSecureCookies: process.env.NODE_ENV === "production",
  },
  rateLimit: {
    window: 60,
    max: 10,
  },
});
```

## Common Patterns

| Pattern | Reference |
|---------|-----------|
| Email verification | `references/email-verification.md` |
| Password reset | `references/password-reset.md` |
| JWT configuration | `references/jwt-plugin.md` |
| OAuth providers | `references/social-providers.md` |
| Session options | `references/session-config.md` |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Invalid session" | Check BETTER_AUTH_SECRET consistency |
| OAuth redirect error | Verify callback URLs in provider console |
| Database connection | Validate DATABASE_URL format |
| CORS errors | Configure trustedOrigins in auth config |

## Output Checklist

- [ ] Environment variables configured
- [ ] Database migrated
- [ ] Auth instance created
- [ ] API route handler set up
- [ ] Client configured
- [ ] Middleware protection added
- [ ] Secure cookies enabled (production)
