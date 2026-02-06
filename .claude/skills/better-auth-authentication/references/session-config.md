# Session Management Reference

## Session Configuration

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: { /* config */ },
  session: {
    // Session expiration (default: 7 days)
    expiresIn: 60 * 60 * 24 * 7,  // seconds

    // Update session expiry on activity (default: 1 day before expiry)
    updateAge: 60 * 60 * 24,  // seconds

    // Store session in database (default: true)
    storeSessionInDatabase: true,

    // Cookie-based session caching
    cookieCache: {
      enabled: true,
      maxAge: 60 * 5,  // 5 minutes cache
    },
  },
});
```

## Client-Side Session Access

### React Hook

```tsx
"use client";
import { useSession } from "@/lib/auth-client";

export function UserProfile() {
  const { data: session, isPending, error, refetch } = useSession();

  if (isPending) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  if (!session) {
    return <div>Not authenticated</div>;
  }

  return (
    <div>
      <p>Name: {session.user.name}</p>
      <p>Email: {session.user.email}</p>
      <img src={session.user.image} alt="Avatar" />
      <button onClick={() => refetch()}>Refresh Session</button>
    </div>
  );
}
```

### Non-Hook Method

```typescript
import { authClient } from "@/lib/auth-client";

async function checkSession() {
  const session = await authClient.getSession();
  return session;
}
```

## Server-Side Session Access

### Next.js App Router

```typescript
// app/dashboard/page.tsx
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { redirect } from "next/navigation";

export default async function DashboardPage() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) {
    redirect("/login");
  }

  return <div>Welcome, {session.user.name}</div>;
}
```

### API Routes

```typescript
// app/api/user/route.ts
import { auth } from "@/lib/auth";
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  return NextResponse.json({ user: session.user });
}
```

### Server Actions

```typescript
"use server";
import { auth } from "@/lib/auth";
import { headers } from "next/headers";

export async function updateProfile(formData: FormData) {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) {
    throw new Error("Unauthorized");
  }

  // Update user profile
}
```

## Session Object Structure

```typescript
interface Session {
  session: {
    id: string;
    userId: string;
    expiresAt: Date;
    ipAddress?: string;
    userAgent?: string;
  };
  user: {
    id: string;
    email: string;
    name: string;
    image?: string;
    emailVerified: boolean;
    createdAt: Date;
    updatedAt: Date;
  };
}
```

## Multi-Session Support

Allow users to have multiple active sessions:

```typescript
export const auth = betterAuth({
  // Multiple sessions per user (default behavior)
  session: {
    // No session limit by default
  },
});
```

### List User Sessions

```typescript
// Client-side
const sessions = await authClient.listSessions();

// Server-side (with admin plugin)
const sessions = await auth.api.listUserSessions({
  body: { userId: "user-id" },
  headers: await headers(),
});
```

### Revoke Sessions

```typescript
// Revoke current session (sign out)
await authClient.signOut();

// Revoke specific session
await authClient.revokeSession({ token: "session-token" });

// Revoke all sessions (server-side with admin plugin)
await auth.api.revokeUserSessions({
  body: { userId: "user-id" },
  headers: await headers(),
});
```

## Session Security

### Secure Cookies

```typescript
export const auth = betterAuth({
  advanced: {
    useSecureCookies: process.env.NODE_ENV === "production",
  },
  cookies: {
    sessionToken: {
      name: "session",
      attributes: {
        httpOnly: true,
        secure: process.env.NODE_ENV === "production",
        sameSite: "lax",
        path: "/",
      },
    },
  },
});
```

### IP and User Agent Tracking

```typescript
export const auth = betterAuth({
  advanced: {
    ipAddress: {
      ipAddressHeaders: ["x-forwarded-for", "x-real-ip"],
      disableIpTracking: false,
    },
  },
});
```

## Remember Me

```typescript
// Client-side sign in with remember me
await signIn.email({
  email: "user@example.com",
  password: "password",
  rememberMe: true,  // Extended session duration
});
```

## Session Hooks

```typescript
export const auth = betterAuth({
  databaseHooks: {
    session: {
      create: {
        before: async (session) => {
          // Modify session before creation
          return session;
        },
        after: async (session) => {
          // Log session creation
          console.log("New session:", session.id);
        },
      },
      delete: {
        after: async (session) => {
          // Clean up on logout
        },
      },
    },
  },
});
```

## Secondary Storage (Redis)

For high-performance session storage:

```typescript
import { betterAuth } from "better-auth";
import { Redis } from "ioredis";

const redis = new Redis(process.env.REDIS_URL);

export const auth = betterAuth({
  database: { /* primary database */ },
  secondaryStorage: {
    get: async (key) => {
      const value = await redis.get(key);
      return value ? JSON.parse(value) : null;
    },
    set: async (key, value, ttl) => {
      if (ttl) {
        await redis.setex(key, ttl, JSON.stringify(value));
      } else {
        await redis.set(key, JSON.stringify(value));
      }
    },
    delete: async (key) => {
      await redis.del(key);
    },
  },
});
```
