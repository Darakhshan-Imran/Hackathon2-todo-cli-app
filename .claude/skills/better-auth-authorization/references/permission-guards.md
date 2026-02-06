# Permission Guards Reference

## Overview

Permission guards protect routes and components based on user roles and permissions.

## Server Component Guards

### Higher-Order Component Pattern

```typescript
// lib/guards.ts
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { redirect } from "next/navigation";

type Permission = { resource: string; action: string };

export async function requireAuth() {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) {
    redirect("/login");
  }

  return session;
}

export async function requireRole(allowedRoles: string[]) {
  const session = await requireAuth();

  if (!allowedRoles.includes(session.user.role)) {
    redirect("/forbidden");
  }

  return session;
}

export async function requirePermission(permission: Permission) {
  const session = await requireAuth();

  const hasPermission = await auth.api.userHasPermission({
    body: {
      userId: session.user.id,
      permission,
    },
  });

  if (!hasPermission) {
    redirect("/forbidden");
  }

  return session;
}
```

### Usage in Server Components

```tsx
// app/admin/page.tsx
import { requireRole } from "@/lib/guards";

export default async function AdminPage() {
  const session = await requireRole(["admin", "super-admin"]);

  return (
    <div>
      <h1>Admin Dashboard</h1>
      <p>Welcome, {session.user.name}</p>
    </div>
  );
}
```

```tsx
// app/posts/new/page.tsx
import { requirePermission } from "@/lib/guards";

export default async function NewPostPage() {
  await requirePermission({ resource: "post", action: "create" });

  return <PostEditor />;
}
```

## Client Component Guards

### PermissionGate Component

```tsx
"use client";
import { useSession } from "@/lib/auth-client";
import { authClient } from "@/lib/auth-client";

interface PermissionGateProps {
  permission: { resource: string; action: string };
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function PermissionGate({
  permission,
  children,
  fallback = null,
}: PermissionGateProps) {
  const { data: session, isPending } = useSession();

  if (isPending) {
    return null; // or loading state
  }

  if (!session) {
    return <>{fallback}</>;
  }

  const hasPermission = authClient.admin.checkRolePermission({
    role: session.user.role,
    permission,
  });

  if (!hasPermission) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
}
```

### Usage

```tsx
<PermissionGate
  permission={{ resource: "post", action: "delete" }}
  fallback={<span>You cannot delete posts</span>}
>
  <DeleteButton postId={post.id} />
</PermissionGate>
```

### RoleGate Component

```tsx
"use client";
import { useSession } from "@/lib/auth-client";

interface RoleGateProps {
  allowedRoles: string[];
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

export function RoleGate({
  allowedRoles,
  children,
  fallback = null,
}: RoleGateProps) {
  const { data: session, isPending } = useSession();

  if (isPending) {
    return null;
  }

  if (!session || !allowedRoles.includes(session.user.role)) {
    return <>{fallback}</>;
  }

  return <>{children}</>;
}
```

### Usage

```tsx
<RoleGate allowedRoles={["admin", "moderator"]}>
  <ModeratorPanel />
</RoleGate>
```

## API Route Guards

### Middleware Helper

```typescript
// lib/api-guards.ts
import { auth } from "@/lib/auth";
import { NextRequest, NextResponse } from "next/server";

type Permission = { resource: string; action: string };

export function withAuth(
  handler: (request: NextRequest, session: any) => Promise<NextResponse>
) {
  return async (request: NextRequest) => {
    const session = await auth.api.getSession({
      headers: request.headers,
    });

    if (!session) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    return handler(request, session);
  };
}

export function withPermission(
  permission: Permission,
  handler: (request: NextRequest, session: any) => Promise<NextResponse>
) {
  return async (request: NextRequest) => {
    const session = await auth.api.getSession({
      headers: request.headers,
    });

    if (!session) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const hasPermission = await auth.api.userHasPermission({
      body: { userId: session.user.id, permission },
    });

    if (!hasPermission) {
      return NextResponse.json({ error: "Forbidden" }, { status: 403 });
    }

    return handler(request, session);
  };
}

export function withRole(
  allowedRoles: string[],
  handler: (request: NextRequest, session: any) => Promise<NextResponse>
) {
  return async (request: NextRequest) => {
    const session = await auth.api.getSession({
      headers: request.headers,
    });

    if (!session) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    if (!allowedRoles.includes(session.user.role)) {
      return NextResponse.json({ error: "Forbidden" }, { status: 403 });
    }

    return handler(request, session);
  };
}
```

### Usage in API Routes

```typescript
// app/api/admin/users/route.ts
import { withRole } from "@/lib/api-guards";

export const GET = withRole(["admin"], async (request, session) => {
  // Admin-only logic
  const users = await getUsers();
  return NextResponse.json({ users });
});
```

```typescript
// app/api/posts/route.ts
import { withPermission } from "@/lib/api-guards";

export const POST = withPermission(
  { resource: "post", action: "create" },
  async (request, session) => {
    const body = await request.json();
    const post = await createPost({ ...body, authorId: session.user.id });
    return NextResponse.json({ post });
  }
);
```

## Organization Permission Guards

### Server Component

```typescript
// lib/org-guards.ts
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { redirect } from "next/navigation";

export async function requireOrgMember(organizationId: string) {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) {
    redirect("/login");
  }

  const membership = await auth.api.getOrgMembership({
    body: { organizationId, userId: session.user.id },
  });

  if (!membership) {
    redirect("/forbidden");
  }

  return { session, membership };
}

export async function requireOrgPermission(
  organizationId: string,
  permission: { resource: string; action: string }
) {
  const { session, membership } = await requireOrgMember(organizationId);

  const hasPermission = await auth.api.hasOrgPermission({
    body: { organizationId, userId: session.user.id, permission },
  });

  if (!hasPermission) {
    redirect("/forbidden");
  }

  return { session, membership };
}
```

### Usage

```tsx
// app/org/[orgId]/settings/page.tsx
import { requireOrgPermission } from "@/lib/org-guards";

export default async function OrgSettingsPage({
  params,
}: {
  params: { orgId: string };
}) {
  const { session, membership } = await requireOrgPermission(
    params.orgId,
    { resource: "organization", action: "update" }
  );

  return <SettingsForm organizationId={params.orgId} />;
}
```

## Custom Hook for Permissions

```typescript
// hooks/usePermission.ts
"use client";
import { useSession } from "@/lib/auth-client";
import { authClient } from "@/lib/auth-client";
import { useMemo } from "react";

export function usePermission(permission: { resource: string; action: string }) {
  const { data: session, isPending } = useSession();

  const hasPermission = useMemo(() => {
    if (!session) return false;

    return authClient.admin.checkRolePermission({
      role: session.user.role,
      permission,
    });
  }, [session, permission.resource, permission.action]);

  return {
    hasPermission,
    isPending,
    isAuthenticated: !!session,
  };
}

// Usage
function MyComponent() {
  const { hasPermission, isPending } = usePermission({
    resource: "post",
    action: "delete",
  });

  if (isPending) return <Loading />;

  return hasPermission ? <DeleteButton /> : null;
}
```

## Best Practices

1. **Always verify server-side**: Client guards are for UX, not security
2. **Fail closed**: Default to denying access
3. **Consistent patterns**: Use the same guard patterns throughout
4. **Audit sensitive operations**: Log permission checks for admin actions
5. **Cache wisely**: Permission checks can be cached for performance

```typescript
// Log admin actions
export function withAdminAudit(
  handler: (request: NextRequest, session: any) => Promise<NextResponse>
) {
  return withRole(["admin"], async (request, session) => {
    console.log(`Admin action by ${session.user.email}: ${request.url}`);
    return handler(request, session);
  });
}
```
