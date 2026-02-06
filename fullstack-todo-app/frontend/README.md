# Todo App Frontend

Next.js 14 frontend for the Full-Stack Todo Application.

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **Forms**: React Hook Form + Zod validation
- **HTTP Client**: Axios
- **State Management**: React Context

## Project Structure

```
frontend/
├── app/                      # Next.js App Router
│   ├── (auth)/               # Auth pages (public)
│   │   ├── login/
│   │   └── signup/
│   ├── (dashboard)/          # Protected pages
│   │   ├── todos/
│   │   │   ├── [id]/         # Todo detail/edit
│   │   │   └── new/          # Create todo
│   │   └── profile/
│   ├── globals.css
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   ├── auth/                 # Auth components
│   │   ├── AuthGuard.tsx
│   │   ├── LoginForm.tsx
│   │   └── SignupForm.tsx
│   ├── common/               # Reusable components
│   │   ├── Button.tsx
│   │   ├── ErrorAlert.tsx
│   │   ├── Input.tsx
│   │   └── LoadingSpinner.tsx
│   ├── layout/
│   │   └── Header.tsx
│   └── todos/                # Todo components
│       ├── TodoFilters.tsx
│       ├── TodoForm.tsx
│       ├── TodoItem.tsx
│       ├── TodoList.tsx
│       └── TodoPagination.tsx
├── context/
│   └── AuthContext.tsx       # Auth state management
├── hooks/
│   └── useTodos.ts           # Todo state hook
├── lib/
│   ├── auth.ts               # Token utilities
│   ├── utils.ts              # Helper functions
│   └── validators.ts         # Zod schemas
├── services/
│   ├── api.ts                # Axios instance
│   ├── auth.service.ts
│   ├── todo.service.ts
│   └── user.service.ts
├── types/
│   ├── api.ts                # API response types
│   ├── todo.ts               # Todo types
│   └── user.ts               # User types
├── Dockerfile
├── next.config.js
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

## Setup

### Prerequisites

- Node.js 20+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Or with yarn
yarn install
```

### Environment Variables

Copy `.env.example` to `.env.local`:

```bash
cp .env.example .env.local
```

Required variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |

### Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

### Production Build

```bash
# Build
npm run build

# Start production server
npm start
```

## Features

### Authentication
- User registration with validation
- Login with email/password
- Automatic token refresh
- Protected routes with AuthGuard

### Todo Management
- Create, read, update, delete todos
- Status management (pending, in_progress, completed)
- Priority levels (low, medium, high, urgent)
- Due dates and tags

### Filtering & Pagination
- Filter by status and priority
- Sort by created date, due date, or priority
- Paginated results (10 items per page)
- Clear filters functionality

### User Profile
- View profile information
- Update username
- Conflict handling for duplicate usernames

## Component Library

### Common Components

**Button**
```tsx
<Button variant="primary" size="md" isLoading={false}>
  Click me
</Button>
```

Variants: `primary`, `secondary`, `danger`, `ghost`
Sizes: `sm`, `md`, `lg`

**Input**
```tsx
<Input
  id="email"
  label="Email"
  type="email"
  error={errors.email?.message}
  {...register("email")}
/>
```

**LoadingSpinner**
```tsx
<LoadingSpinner size="md" />
```

**ErrorAlert**
```tsx
<ErrorAlert message="Something went wrong" onDismiss={() => {}} />
```

## API Integration

### Services

All API calls are centralized in the `services/` directory:

```typescript
// Auth
authService.signup(data)
authService.login(data)
authService.logout()
authService.refreshToken()

// Todos
todoService.getTodos(params)
todoService.getTodo(id)
todoService.createTodo(data)
todoService.updateTodo(id, data)
todoService.deleteTodo(id)

// User
userService.getProfile()
userService.updateProfile(data)
```

### Error Handling

The Axios instance includes:
- Automatic 401 handling with token refresh
- Consistent error extraction
- Request/response interceptors

## Form Validation

Zod schemas in `lib/validators.ts`:

```typescript
// Login
loginSchema.parse({ email, password })

// Signup
signupSchema.parse({ email, username, password, confirmPassword })

// Todo
todoCreateSchema.parse({ title, description, priority, due_date })
```

## Testing

```bash
# Run unit tests
npm test

# Run with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e
```

## Code Quality

```bash
# Linting
npm run lint

# Fix lint issues
npm run lint:fix

# Type checking
npm run type-check
```

## Docker

```bash
# Build image
docker build -t todo-frontend .

# Run container
docker run -p 3000:3000 todo-frontend
```

## Styling

### Tailwind Configuration

- Dark mode: class-based (`dark:` prefix)
- Custom colors defined in `tailwind.config.ts`
- Responsive breakpoints: `sm`, `md`, `lg`, `xl`, `2xl`

### Theme Classes

```css
/* Primary button */
bg-blue-600 hover:bg-blue-700 text-white

/* Secondary button */
bg-gray-200 hover:bg-gray-300 text-gray-900

/* Card */
bg-white dark:bg-gray-800 rounded-lg shadow

/* Input */
border-gray-300 dark:border-gray-600 rounded-md
```

## Security

- Access tokens stored in memory only (not localStorage)
- Refresh tokens in HttpOnly cookies (handled by backend)
- XSS protection via React's default escaping
- CSRF protection via SameSite cookies
- Input validation on all forms
