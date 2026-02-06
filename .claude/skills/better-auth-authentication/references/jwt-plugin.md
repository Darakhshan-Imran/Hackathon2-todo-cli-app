# Better Auth JWT Plugin Reference

## Overview

The JWT plugin enables stateless token-based authentication for microservices, APIs, and services that cannot use session-based auth.

## Installation

```typescript
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  database: { /* config */ },
  plugins: [
    jwt({
      jwt: {
        expirationTime: "15m",        // Token lifetime
        issuer: "your-app",           // JWT issuer claim
        audience: "your-app",         // JWT audience claim
      },
    }),
  ],
});
```

## Token Retrieval Methods

### 1. Client Plugin (Recommended)

```typescript
// lib/auth-client.ts
import { createAuthClient } from "better-auth/react";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  plugins: [jwtClient()],
});

// Usage
const { token } = await authClient.getToken();

// Use token in API calls
fetch("/api/protected", {
  headers: {
    Authorization: `Bearer ${token}`,
  },
});
```

### 2. Direct /token Endpoint

```typescript
const response = await fetch("/api/auth/token", {
  method: "POST",
  headers: {
    Authorization: `Bearer ${sessionToken}`,
  },
});
const { token } = await response.json();
```

### 3. Header Response (getSession)

```typescript
const jwt = jwt({
  jwt: {
    // ... config
  },
});

// JWT returned in `set-auth-jwt` header during getSession calls
```

## JWKS Verification

Public keys available at `/api/auth/jwks` for stateless verification.

```typescript
import { createRemoteJWKSet, jwtVerify } from "jose";

const JWKS = createRemoteJWKSet(
  new URL("https://your-app.com/api/auth/jwks")
);

async function verifyToken(token: string) {
  try {
    const { payload } = await jwtVerify(token, JWKS, {
      issuer: "your-app",
      audience: "your-app",
    });
    return payload;
  } catch (error) {
    return null;
  }
}
```

## Algorithm Options

| Algorithm | Type | Notes |
|-----------|------|-------|
| EdDSA | Default | Ed25519/Ed448, recommended |
| ES256 | ECDSA | P-256 curve |
| ES512 | ECDSA | P-521 curve |
| RS256 | RSA | 2048-bit minimum |
| PS256 | RSA-PSS | More secure RSA variant |

```typescript
jwt({
  jwt: {
    algorithm: "ES256",  // Override default EdDSA
  },
});
```

## Key Rotation

```typescript
jwt({
  jwks: {
    rotationInterval: 7 * 24 * 60 * 60,  // 7 days in seconds
    gracePeriod: 24 * 60 * 60,           // 24 hours old keys remain valid
  },
});
```

## Custom Claims

```typescript
jwt({
  jwt: {
    expirationTime: "15m",
    issuer: "my-app",
    audience: "my-api",

    // Custom subject
    getSubject: async (user) => user.id,

    // Custom payload
    definePayload: async ({ user, session }) => ({
      email: user.email,
      name: user.name,
      // Exclude sensitive data
    }),
  },
});
```

## Custom JWKS Path

```typescript
jwt({
  jwks: {
    keysetEndpoint: "/.well-known/jwks.json",  // Override default /jwks
  },
});
```

## Security Considerations

1. **Short Expiration**: Keep JWT expiration short (15 minutes recommended)
2. **Secure Storage**: Never store JWTs in localStorage; use httpOnly cookies or memory
3. **HTTPS Only**: Always transmit over HTTPS
4. **Validate Claims**: Always verify issuer and audience
5. **Key Encryption**: Private keys encrypted by default (AES256 GCM)

```typescript
jwt({
  jwks: {
    disablePrivateKeyEncryption: false,  // Keep enabled for security
  },
});
```

## API Protection Pattern

```typescript
// app/api/protected/route.ts
import { jwtVerify, createRemoteJWKSet } from "jose";
import { NextRequest, NextResponse } from "next/server";

const JWKS = createRemoteJWKSet(
  new URL(`${process.env.BETTER_AUTH_URL}/api/auth/jwks`)
);

export async function GET(request: NextRequest) {
  const authHeader = request.headers.get("authorization");

  if (!authHeader?.startsWith("Bearer ")) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const token = authHeader.slice(7);

  try {
    const { payload } = await jwtVerify(token, JWKS, {
      issuer: "your-app",
      audience: "your-app",
    });

    // Token valid, payload contains user claims
    return NextResponse.json({ user: payload });
  } catch (error) {
    return NextResponse.json({ error: "Invalid token" }, { status: 401 });
  }
}
```

## Microservice Architecture

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Client    │─────▶│  Auth API   │─────▶│   JWKS      │
│             │      │ (Better Auth)│      │  Endpoint   │
└─────────────┘      └─────────────┘      └──────┬──────┘
       │                                          │
       │ JWT Token                                │ Public Keys
       ▼                                          ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  Service A  │      │  Service B  │      │  Service C  │
│ (Verifies)  │      │ (Verifies)  │      │ (Verifies)  │
└─────────────┘      └─────────────┘      └─────────────┘
```

Each service fetches JWKS once and caches it, enabling stateless verification without auth server roundtrips.
