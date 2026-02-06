---
name: better-auth-authorization
description: |
  Implements authorization with Better Auth using RBAC, permissions, and organization-based access control.
  This skill should be used when users need role-based access control, custom permissions, organization
  management, or multi-tenant authorization in Next.js applications using Better Auth.
---

# Better Auth Authorization

Implement production-ready authorization with Better Auth's Admin and Organization plugins.

## Before Implementation

| Source | Gather |
|--------|--------|
| **Codebase** | Existing auth setup, user schema, API routes |
| **Conversation** | User's authorization model (roles, permissions, multi-tenant) |
| **Skill References** | RBAC patterns from `references/` |
| **User Guidelines** | Security requirements, permission granularity |

## Authorization Models

| Model | Use Case | Plugin |
|-------|----------|--------|
| **Simple RBAC** | User roles (admin, user, moderator) | Admin Plugin |
| **Permission-Based** | Granular actions (create, read, update, delete) | Admin Plugin |
| **Organization-Based** | Multi-tenant with org-specific roles | Organization Plugin |
| **Hybrid** | Both app-level and org-level permissions | Admin + Organization |

## Admin Plugin (Simple RBAC)

### Installation

```bash
npm install better-auth
```

### Configuration

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { admin } from "better-auth/plugins";

export const auth = betterAuth({
  database: { /* config */ },
  plugins: [
    admin({
      defaultRole: "user",
      adminRoles: ["admin", "super-admin"],
    }),
  ],
});
```

### Run Migration

```bash
npx @better-auth/cli migrate
```

### Client Setup

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react";
import { adminClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [adminClient()],
});
```

### Default Roles

| Role | Permissions |
|------|-------------|
| `user` | Basic access (default) |
| `admin` | Full access except system operations |

## Custom Access Control

### Define Permissions

```typescript
import { betterAuth } from "better-auth";
import { admin, createAccessControl } from "better-auth/plugins";

// Define access control structure
const ac = createAccessControl({
  user: ["create", "read", "update", "delete"],
  post: ["create", "read", "update", "delete", "publish"],
  comment: ["create", "read", "delete"],
  settings: ["read", "update"],
});

// Define roles with permissions
const roles = {
  user: ac.newRole({
    user: ["read"],
    post: ["read"],
    comment: ["create", "read"],
  }),
  moderator: ac.newRole({
    user: ["read"],
    post: ["read", "update"],
    comment: ["create", "read", "delete"],
  }),
  editor: ac.newRole({
    user: ["read"],
    post: ["create", "read", "update", "publish"],
    comment: ["create", "read", "delete"],
  }),
  admin: ac.newRole({
    user: ["create", "read", "update", "delete"],
    post: ["create", "read", "update", "delete", "publish"],
    comment: ["create", "read", "delete"],
    settings: ["read", "update"],
  }),
};

export const auth = betterAuth({
  database: { /* config */ },
  plugins: [
    admin({
      defaultRole: "user",
      roles,
    }),
  ],
});
```

## Permission Verification

### Server-Side (API Routes)

```typescript
// app/api/posts/route.ts
import { auth } from "@/lib/auth";
import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  // Check permission
  const hasPermission = await auth.api.userHasPermission({
    body: {
      userId: session.user.id,
      permission: { resource: "post", action: "create" },
    },
  });

  if (!hasPermission) {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  // Create post...
  return NextResponse.json({ success: true });
}
```

### Client-Side Check

```typescript
import { authClient } from "@/lib/auth-client";

// Synchronous check (uses cached role)
const canCreatePost = authClient.admin.checkRolePermission({
  role: "editor",
  permission: { resource: "post", action: "create" },
});

// Use in component
function CreatePostButton() {
  const { data: session } = useSession();
  const canCreate = session && authClient.admin.checkRolePermission({
    role: session.user.role,
    permission: { resource: "post", action: "create" },
  });

  if (!canCreate) return null;
  return <button>Create Post</button>;
}
```

### Middleware Protection

```typescript
// middleware.ts
import { auth } from "@/lib/auth";
import { NextRequest, NextResponse } from "next/server";

const routePermissions: Record<string, { resource: string; action: string }> = {
  "/admin": { resource: "settings", action: "read" },
  "/posts/new": { resource: "post", action: "create" },
  "/posts/publish": { resource: "post", action: "publish" },
};

export async function middleware(request: NextRequest) {
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  const { pathname } = request.nextUrl;
  const permission = routePermissions[pathname];

  if (permission && session) {
    const hasPermission = await auth.api.userHasPermission({
      body: {
        userId: session.user.id,
        permission,
      },
    });

    if (!hasPermission) {
      return NextResponse.redirect(new URL("/forbidden", request.url));
    }
  }

  return NextResponse.next();
}
```

## User Management (Admin)

### Set User Role

```typescript
// Server-side
await auth.api.setRole({
  body: { userId: "user-id", role: "moderator" },
  headers: await headers(),
});

// Client-side (admin only)
await authClient.admin.setRole({
  userId: "user-id",
  role: "moderator",
});
```

### List Users

```typescript
const users = await authClient.admin.listUsers({
  query: {
    limit: 10,
    offset: 0,
    sortBy: "createdAt",
    sortDirection: "desc",
    search: "john",  // Search by name/email
  },
});
```

### Ban/Unban Users

```typescript
// Ban user
await authClient.admin.banUser({
  userId: "user-id",
  banReason: "Policy violation",
  banExpiresIn: 60 * 60 * 24 * 7,  // 7 days (optional)
});

// Unban user
await authClient.admin.unbanUser({ userId: "user-id" });
```

### Session Management

```typescript
// List user sessions
const sessions = await authClient.admin.listUserSessions({
  userId: "user-id",
});

// Revoke specific session
await authClient.admin.revokeUserSession({
  userId: "user-id",
  sessionToken: "token",
});

// Revoke all sessions
await authClient.admin.revokeUserSessions({
  userId: "user-id",
});
```

## Organization Plugin (Multi-Tenant)

See `references/organization-plugin.md` for complete organization-based authorization.

### Quick Setup

```typescript
import { betterAuth } from "better-auth";
import { organization } from "better-auth/plugins";

export const auth = betterAuth({
  database: { /* config */ },
  plugins: [
    organization({
      allowUserToCreateOrganization: true,
      organizationLimit: 5,
    }),
  ],
});
```

### Organization Roles

| Role | Permissions |
|------|-------------|
| `owner` | Full control including delete |
| `admin` | Full access except ownership transfer |
| `member` | Read-only access |

## Common Patterns

| Pattern | Reference |
|---------|-----------|
| Organization RBAC | `references/organization-plugin.md` |
| Permission guards | `references/permission-guards.md` |
| Role hierarchy | `references/role-hierarchy.md` |

## Security Best Practices

1. **Server-Side Verification**: Always verify permissions server-side
2. **Principle of Least Privilege**: Start with minimal permissions
3. **Audit Logging**: Log permission-sensitive operations
4. **Role Separation**: Keep admin and user roles distinct
5. **Session Invalidation**: Revoke sessions on role changes

```typescript
// Invalidate sessions when role changes
await auth.api.setRole({
  body: { userId: "user-id", role: "admin" },
});
await auth.api.revokeUserSessions({
  body: { userId: "user-id" },
});
```

## Output Checklist

- [ ] Authorization model chosen (RBAC, permissions, org-based)
- [ ] Plugin configured (Admin and/or Organization)
- [ ] Database migrated
- [ ] Roles and permissions defined
- [ ] Server-side verification implemented
- [ ] Client-side permission checks added
- [ ] Middleware protection configured
- [ ] Admin interfaces built (if needed)
