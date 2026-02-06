# Organization Plugin Reference

## Overview

The Organization plugin enables multi-tenant authorization with organization-specific roles, permissions, teams, and member management.

## Installation

```typescript
// lib/auth.ts
import { betterAuth } from "better-auth";
import { organization } from "better-auth/plugins";

export const auth = betterAuth({
  database: { /* config */ },
  plugins: [
    organization({
      allowUserToCreateOrganization: true,
      organizationLimit: 5,  // Max orgs per user
      membershipLimit: 100,  // Max members per org
      invitationExpiresIn: 48 * 60 * 60,  // 48 hours
    }),
  ],
});
```

### Client Setup

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react";
import { organizationClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [organizationClient()],
});

export const { useActiveOrganization, useListOrganizations } = authClient;
```

### Run Migration

```bash
npx @better-auth/cli migrate
```

## Organization Management

### Create Organization

```typescript
const { data: org } = await authClient.organization.create({
  name: "Acme Corp",
  slug: "acme-corp",  // URL-friendly identifier
  logo: "https://example.com/logo.png",  // Optional
  metadata: { plan: "pro" },  // Optional custom data
});
```

### Get Organization

```typescript
// By ID
const org = await authClient.organization.getFullOrganization({
  organizationId: "org-id",
});

// Active organization
const { data: activeOrg } = useActiveOrganization();
```

### Update Organization

```typescript
await authClient.organization.update({
  organizationId: "org-id",
  data: {
    name: "New Name",
    logo: "https://example.com/new-logo.png",
  },
});
```

### Delete Organization

```typescript
// Only owners can delete
await authClient.organization.delete({
  organizationId: "org-id",
});
```

### Set Active Organization

```typescript
// Store active org in session
await authClient.organization.setActive({
  organizationId: "org-id",
});

// Client-only (no persistence)
authClient.organization.setActiveLocal("org-id");
```

## Member Management

### Invite Members

```typescript
// Send invitation email
await authClient.organization.inviteMember({
  organizationId: "org-id",
  email: "user@example.com",
  role: "member",  // owner, admin, or member
});
```

### Accept Invitation

```typescript
// From invitation link with token
await authClient.organization.acceptInvitation({
  invitationId: "invitation-id",
});
```

### Add Member Directly (Server-Side)

```typescript
// No invitation, direct add (admin/owner only)
await auth.api.addMember({
  body: {
    organizationId: "org-id",
    userId: "user-id",
    role: "member",
  },
  headers: await headers(),
});
```

### List Members

```typescript
const members = await authClient.organization.getMembers({
  organizationId: "org-id",
});

// Returns:
// [{ id, userId, role, user: { name, email, image } }]
```

### Update Member Role

```typescript
await authClient.organization.updateMemberRole({
  organizationId: "org-id",
  memberId: "member-id",
  role: "admin",
});
```

### Remove Member

```typescript
await authClient.organization.removeMember({
  organizationId: "org-id",
  memberId: "member-id",
});
```

## Invitations

### List Invitations

```typescript
const invitations = await authClient.organization.getInvitations({
  organizationId: "org-id",
});
```

### Cancel Invitation

```typescript
await authClient.organization.cancelInvitation({
  invitationId: "invitation-id",
});
```

### Resend Invitation

```typescript
await authClient.organization.resendInvitation({
  invitationId: "invitation-id",
});
```

## Default Roles & Permissions

### Built-in Roles

| Role | Organization | Member | Invitation |
|------|--------------|--------|------------|
| **owner** | create, update, delete | create, read, update, delete | create, read, cancel |
| **admin** | read, update | create, read, update, delete | create, read, cancel |
| **member** | read | read | - |

### Custom Permissions

```typescript
import { betterAuth } from "better-auth";
import { organization } from "better-auth/plugins";

export const auth = betterAuth({
  plugins: [
    organization({
      ac: {
        // Define custom resources and actions
        project: ["create", "read", "update", "delete"],
        billing: ["read", "update"],
        analytics: ["read"],
      },
      roles: {
        owner: {
          project: ["create", "read", "update", "delete"],
          billing: ["read", "update"],
          analytics: ["read"],
        },
        admin: {
          project: ["create", "read", "update"],
          analytics: ["read"],
        },
        member: {
          project: ["read"],
          analytics: ["read"],
        },
        billing_admin: {
          billing: ["read", "update"],
        },
      },
    }),
  ],
});
```

### Check Organization Permission

```typescript
// Server-side
const hasPermission = await auth.api.hasOrgPermission({
  body: {
    organizationId: "org-id",
    userId: "user-id",
    permission: { resource: "project", action: "create" },
  },
  headers: await headers(),
});

// Client-side
const canCreate = await authClient.organization.hasPermission({
  organizationId: "org-id",
  permission: { resource: "project", action: "create" },
});
```

## Teams (Sub-Groups)

### Enable Teams

```typescript
organization({
  teams: {
    enabled: true,
    maximumTeams: 10,  // Per organization
    allowRemovingLastTeam: false,
  },
});
```

### Create Team

```typescript
await authClient.organization.createTeam({
  organizationId: "org-id",
  name: "Engineering",
});
```

### Add Member to Team

```typescript
await authClient.organization.addMemberToTeam({
  organizationId: "org-id",
  teamId: "team-id",
  memberId: "member-id",
});
```

## Organization Context in API Routes

```typescript
// app/api/org/[orgId]/projects/route.ts
import { auth } from "@/lib/auth";
import { NextRequest, NextResponse } from "next/server";

export async function GET(
  request: NextRequest,
  { params }: { params: { orgId: string } }
) {
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  // Check org membership
  const membership = await auth.api.getOrgMembership({
    body: {
      organizationId: params.orgId,
      userId: session.user.id,
    },
  });

  if (!membership) {
    return NextResponse.json({ error: "Not a member" }, { status: 403 });
  }

  // Check permission
  const hasPermission = await auth.api.hasOrgPermission({
    body: {
      organizationId: params.orgId,
      userId: session.user.id,
      permission: { resource: "project", action: "read" },
    },
  });

  if (!hasPermission) {
    return NextResponse.json({ error: "No permission" }, { status: 403 });
  }

  // Return projects...
}
```

## React Hooks

```tsx
"use client";
import { useActiveOrganization, useListOrganizations } from "@/lib/auth-client";

function OrganizationSwitcher() {
  const { data: activeOrg, isPending: orgPending } = useActiveOrganization();
  const { data: orgs, isPending: listPending } = useListOrganizations();

  if (orgPending || listPending) return <Loading />;

  return (
    <select
      value={activeOrg?.id || ""}
      onChange={(e) => {
        authClient.organization.setActive({ organizationId: e.target.value });
      }}
    >
      {orgs?.map((org) => (
        <option key={org.id} value={org.id}>
          {org.name}
        </option>
      ))}
    </select>
  );
}
```

## Lifecycle Hooks

```typescript
organization({
  hooks: {
    organization: {
      create: {
        before: async (org, ctx) => {
          // Validate before creation
          if (!ctx.user.emailVerified) {
            throw new Error("Verify email first");
          }
          return org;
        },
        after: async (org, ctx) => {
          // Create default resources
          await createDefaultProject(org.id);
        },
      },
    },
    member: {
      add: {
        after: async (member, ctx) => {
          // Send welcome notification
          await notifyNewMember(member);
        },
      },
      remove: {
        after: async (member, ctx) => {
          // Clean up member's org data
          await cleanupMemberData(member);
        },
      },
    },
  },
});
```

## Custom Invitation Email

```typescript
organization({
  sendInvitationEmail: async ({ organization, invitation, inviter }) => {
    await sendEmail({
      to: invitation.email,
      subject: `Join ${organization.name}`,
      html: `
        <h1>You're invited!</h1>
        <p>${inviter.name} invited you to join ${organization.name}.</p>
        <a href="${process.env.NEXT_PUBLIC_APP_URL}/invite/${invitation.id}">
          Accept Invitation
        </a>
      `,
    });
  },
});
```

## Database Schema

The plugin creates these tables:

| Table | Purpose |
|-------|---------|
| `organization` | Organization data |
| `member` | User-organization relationships |
| `invitation` | Pending invitations |
| `team` | Teams (if enabled) |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Not a member" | Verify membership exists |
| "Permission denied" | Check role has required permission |
| "Invitation expired" | Increase invitationExpiresIn |
| "Org limit reached" | Increase organizationLimit or delete orgs |
