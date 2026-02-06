# Social OAuth Providers Reference

## Supported Providers

Better Auth supports 20+ OAuth providers out of the box.

## Configuration Pattern

```typescript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  database: { /* config */ },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      // Optional: custom scopes
      scope: ["openid", "email", "profile"],
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID!,
      clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    },
    // Add more providers as needed
  },
});
```

## Provider Setup Guides

### Google OAuth

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create or select a project
3. Navigate to APIs & Services → Credentials
4. Create OAuth 2.0 Client ID
5. Add authorized redirect URI: `https://your-app.com/api/auth/callback/google`

```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
```

### GitHub OAuth

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. New OAuth App
3. Set callback URL: `https://your-app.com/api/auth/callback/github`

```env
GITHUB_CLIENT_ID=your-client-id
GITHUB_CLIENT_SECRET=your-client-secret
```

### Discord OAuth

```typescript
discord: {
  clientId: process.env.DISCORD_CLIENT_ID!,
  clientSecret: process.env.DISCORD_CLIENT_SECRET!,
  scope: ["identify", "email"],
},
```

Callback URL: `https://your-app.com/api/auth/callback/discord`

### Microsoft/Azure AD

```typescript
microsoft: {
  clientId: process.env.MICROSOFT_CLIENT_ID!,
  clientSecret: process.env.MICROSOFT_CLIENT_SECRET!,
  tenantId: process.env.MICROSOFT_TENANT_ID,  // Optional: for single tenant
},
```

### Apple Sign-In

```typescript
apple: {
  clientId: process.env.APPLE_CLIENT_ID!,
  clientSecret: process.env.APPLE_CLIENT_SECRET!,
  // Apple requires team ID and key ID
},
```

## Client-Side Implementation

### Sign In Button Component

```tsx
"use client";
import { signIn } from "@/lib/auth-client";

export function SocialLoginButtons() {
  const handleSocialLogin = async (provider: string) => {
    await signIn.social({
      provider,
      callbackURL: "/dashboard",
      errorCallbackURL: "/auth/error",
    });
  };

  return (
    <div className="flex flex-col gap-2">
      <button onClick={() => handleSocialLogin("google")}>
        Continue with Google
      </button>
      <button onClick={() => handleSocialLogin("github")}>
        Continue with GitHub
      </button>
    </div>
  );
}
```

### Advanced Options

```typescript
await signIn.social({
  provider: "google",
  callbackURL: "/dashboard",
  errorCallbackURL: "/auth/error",

  // For new users only
  newUserCallbackURL: "/onboarding",

  // Disable auto-redirect (handle manually)
  disableRedirect: true,

  // Use existing provider tokens
  idToken: "provider-id-token",
  accessToken: "provider-access-token",
});
```

## Account Linking

Allow users to link multiple social accounts:

```typescript
export const auth = betterAuth({
  // ... config
  account: {
    accountLinking: {
      enabled: true,
      trustedProviders: ["google", "github"],
    },
  },
});
```

## Callback URLs Summary

| Provider | Callback URL Pattern |
|----------|---------------------|
| Google | `/api/auth/callback/google` |
| GitHub | `/api/auth/callback/github` |
| Discord | `/api/auth/callback/discord` |
| Microsoft | `/api/auth/callback/microsoft` |
| Apple | `/api/auth/callback/apple` |
| Twitter | `/api/auth/callback/twitter` |
| Facebook | `/api/auth/callback/facebook` |

## Error Handling

```typescript
await signIn.social({
  provider: "google",
  callbackURL: "/dashboard",
  errorCallbackURL: "/auth/error",
  fetchOptions: {
    onError: (ctx) => {
      console.error("Social login error:", ctx.error);
      // Handle specific errors
      if (ctx.error.message.includes("email")) {
        // Email already exists with different provider
      }
    },
  },
});
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Redirect URI mismatch | Ensure exact match in provider console |
| Invalid client | Verify client ID and secret |
| Scope errors | Check required vs requested scopes |
| CORS errors | Add domain to trusted origins |

## Environment Variables Template

```env
# Google
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=

# GitHub
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=

# Discord
DISCORD_CLIENT_ID=
DISCORD_CLIENT_SECRET=

# Microsoft
MICROSOFT_CLIENT_ID=
MICROSOFT_CLIENT_SECRET=
MICROSOFT_TENANT_ID=

# Apple
APPLE_CLIENT_ID=
APPLE_CLIENT_SECRET=
APPLE_TEAM_ID=
APPLE_KEY_ID=
```
