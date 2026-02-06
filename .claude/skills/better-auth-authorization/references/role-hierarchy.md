# Role Hierarchy Reference

## Overview

Role hierarchy allows higher roles to inherit permissions from lower roles, reducing duplication in permission definitions.

## Hierarchical Role Pattern

### Define Permission Hierarchy

```typescript
import { betterAuth } from "better-auth";
import { admin, createAccessControl } from "better-auth/plugins";

// Define all resources and actions
const ac = createAccessControl({
  user: ["read", "update", "delete", "manage"],
  post: ["create", "read", "update", "delete", "publish"],
  comment: ["create", "read", "delete", "moderate"],
  settings: ["read", "update"],
  analytics: ["read", "export"],
  billing: ["read", "update"],
});

// Base permissions for each level
const basePermissions = {
  user: {
    user: ["read", "update"],  // Own profile only
    post: ["read"],
    comment: ["create", "read"],
  },
  moderator: {
    post: ["update"],
    comment: ["moderate", "delete"],
  },
  editor: {
    post: ["create", "update", "publish"],
    comment: ["delete"],
  },
  admin: {
    user: ["read", "update", "delete"],
    settings: ["read", "update"],
    analytics: ["read"],
  },
  superAdmin: {
    user: ["manage"],
    analytics: ["export"],
    billing: ["read", "update"],
  },
};

// Build hierarchical roles
function buildRole(levels: (keyof typeof basePermissions)[]) {
  const combined: Record<string, string[]> = {};

  for (const level of levels) {
    const perms = basePermissions[level];
    for (const [resource, actions] of Object.entries(perms)) {
      combined[resource] = [...new Set([...(combined[resource] || []), ...actions])];
    }
  }

  return ac.newRole(combined);
}

const roles = {
  user: buildRole(["user"]),
  moderator: buildRole(["user", "moderator"]),
  editor: buildRole(["user", "editor"]),
  admin: buildRole(["user", "moderator", "editor", "admin"]),
  "super-admin": buildRole(["user", "moderator", "editor", "admin", "superAdmin"]),
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

## Resulting Permissions

| Role | User | Post | Comment | Settings | Analytics | Billing |
|------|------|------|---------|----------|-----------|---------|
| user | read, update | read | create, read | - | - | - |
| moderator | read, update | read, update | create, read, delete, moderate | - | - | - |
| editor | read, update | create, read, update, publish | create, read, delete | - | - | - |
| admin | read, update, delete | all | all | all | read | - |
| super-admin | all | all | all | all | all | all |

## Alternative: Explicit Hierarchy

```typescript
const roleHierarchy = {
  "super-admin": ["admin", "editor", "moderator", "user"],
  admin: ["editor", "moderator", "user"],
  editor: ["user"],
  moderator: ["user"],
  user: [],
};

function roleIncludes(userRole: string, targetRole: string): boolean {
  if (userRole === targetRole) return true;
  const subordinates = roleHierarchy[userRole] || [];
  return subordinates.includes(targetRole);
}

// Usage
roleIncludes("admin", "user");      // true
roleIncludes("moderator", "admin"); // false
```

## Organization Role Hierarchy

```typescript
organization({
  roles: {
    owner: {
      organization: ["create", "read", "update", "delete"],
      member: ["create", "read", "update", "delete"],
      invitation: ["create", "read", "cancel"],
      project: ["create", "read", "update", "delete"],
      billing: ["read", "update"],
    },
    admin: {
      // Inherits from member + additional
      organization: ["read", "update"],
      member: ["create", "read", "update", "delete"],
      invitation: ["create", "read", "cancel"],
      project: ["create", "read", "update", "delete"],
    },
    member: {
      organization: ["read"],
      member: ["read"],
      project: ["read"],
    },
  },
});
```

## Dynamic Role Checking with Hierarchy

```typescript
// lib/role-utils.ts
const roleWeight: Record<string, number> = {
  "super-admin": 100,
  admin: 80,
  editor: 60,
  moderator: 40,
  user: 20,
};

export function hasMinimumRole(userRole: string, requiredRole: string): boolean {
  return (roleWeight[userRole] || 0) >= (roleWeight[requiredRole] || 0);
}

export function getRoleLevel(role: string): number {
  return roleWeight[role] || 0;
}

// Usage in guards
export async function requireMinRole(minRole: string) {
  const session = await requireAuth();

  if (!hasMinimumRole(session.user.role, minRole)) {
    redirect("/forbidden");
  }

  return session;
}

// Usage
await requireMinRole("editor");  // Allows editor, admin, super-admin
```

## React Hook for Role Hierarchy

```typescript
"use client";
import { useSession } from "@/lib/auth-client";
import { hasMinimumRole, roleWeight } from "@/lib/role-utils";

export function useRole() {
  const { data: session, isPending } = useSession();

  const role = session?.user?.role || "guest";
  const level = roleWeight[role] || 0;

  return {
    role,
    level,
    isPending,
    isAuthenticated: !!session,
    hasRole: (r: string) => role === r,
    hasMinRole: (r: string) => hasMinimumRole(role, r),
    isAdmin: hasMinimumRole(role, "admin"),
    isModerator: hasMinimumRole(role, "moderator"),
  };
}

// Usage
function AdminPanel() {
  const { isAdmin, isPending } = useRole();

  if (isPending) return <Loading />;
  if (!isAdmin) return <Forbidden />;

  return <Panel />;
}
```

## Conditional UI Based on Role Level

```tsx
function Navigation() {
  const { hasMinRole } = useRole();

  return (
    <nav>
      <Link href="/dashboard">Dashboard</Link>

      {hasMinRole("editor") && (
        <Link href="/posts/new">Create Post</Link>
      )}

      {hasMinRole("moderator") && (
        <Link href="/moderation">Moderation</Link>
      )}

      {hasMinRole("admin") && (
        <Link href="/admin">Admin</Link>
      )}
    </nav>
  );
}
```

## Best Practices

1. **Clear hierarchy**: Document role relationships clearly
2. **Principle of least privilege**: Start with minimal permissions
3. **Consistent naming**: Use descriptive role names
4. **Separate concerns**: Keep app roles and org roles distinct
5. **Audit trail**: Log role changes

```typescript
// Log role changes
databaseHooks: {
  user: {
    update: {
      after: async (user, ctx) => {
        if (ctx.query?.set?.role) {
          await logRoleChange({
            userId: user.id,
            oldRole: ctx.query.where.id, // Get from before
            newRole: ctx.query.set.role,
            changedBy: ctx.session?.user?.id,
          });
        }
      },
    },
  },
},
```

## Migration Between Roles

```typescript
// Safely upgrade user role
async function upgradeUserRole(userId: string, newRole: string) {
  const user = await getUser(userId);

  if (!user) {
    throw new Error("User not found");
  }

  // Validate role upgrade
  if (getRoleLevel(newRole) <= getRoleLevel(user.role)) {
    throw new Error("Can only upgrade to higher role");
  }

  await auth.api.setRole({
    body: { userId, role: newRole },
    headers: await headers(),
  });

  // Optional: Invalidate sessions to force re-auth
  await auth.api.revokeUserSessions({
    body: { userId },
    headers: await headers(),
  });
}
```
