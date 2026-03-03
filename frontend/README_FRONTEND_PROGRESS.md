# Frontend Development

## Running

```bash
cd frontend
npm run dev          # dev server → http://localhost:3000
npm run build        # production build (tsc + vite)
npm run type-check   # TypeScript only
npm run test         # vitest
npm run lint         # eslint
```

## Environment Variables

Copy `.env.example` → `.env`. The only required variable:

```env
VITE_API_URL=http://localhost:5000/api/v1
```

## Project Structure

```
src/
├── components/
│   ├── AppLayout.tsx          # Sidebar + top-bar shell for authenticated pages
│   ├── ProtectedRoute.tsx     # Redirects to /login when unauthenticated
│   └── SessionTimer.tsx       # Pomodoro / study-session timer widget
├── config/
│   └── constants.ts           # API endpoint paths, storage keys, app config
├── hooks/                     # (empty — ready for custom hooks)
├── pages/
│   ├── auth/
│   │   ├── LoginPage.tsx      # Email + password login with zod validation
│   │   ├── RegisterPage.tsx   # Registration with password-strength meter
│   │   └── VerifyEmailPage.tsx
│   ├── AnalyticsPage.tsx      # Study-time charts and productivity trends
│   ├── DashboardPage.tsx      # Main overview after login
│   ├── DeadlinesPage.tsx      # Upcoming deadlines list
│   ├── StudySessionsPage.tsx  # Session history + start new session
│   ├── SubjectsPage.tsx       # Subject CRUD with colour coding
│   └── WellnessPage.tsx       # Daily sleep / stress / mood logger
├── services/
│   ├── aiService.ts           # ML prediction endpoint calls
│   ├── analyticsService.ts    # Analytics API (study-time, trends, streak)
│   ├── apiClient.ts           # Axios instance, token injection, 401 refresh
│   ├── authService.ts         # Login, register, refresh, password reset
│   ├── sessionService.ts      # Study-session CRUD + start/complete
│   └── subjectService.ts      # Subject CRUD + archive/unarchive
├── store/
│   ├── hooks.ts               # Typed useAppSelector / useAppDispatch
│   ├── index.ts               # Redux store configuration
│   └── slices/
│       ├── authSlice.ts       # Auth state + login/register/logout thunks
│       ├── sessionsSlice.ts   # Study-session state
│       └── subjectsSlice.ts   # Subject state
├── styles/
│   └── globals.css            # Tailwind base + custom utilities
├── types/
│   └── index.ts               # Shared TypeScript types for all entities
├── utils/                     # (empty — ready for helper functions)
├── App.tsx                    # Redux Provider + Router + Toaster
├── index.tsx                  # ReactDOM entry point
├── routes.tsx                 # Route definitions (public + protected)
└── vite-env.d.ts              # Vite client type shims
```

## Tech Stack

| Library | Purpose |
|---------|---------|
| React 18 | UI |
| TypeScript 5 | Type safety |
| Vite 5 | Build / dev server |
| Redux Toolkit | State management |
| React Router 6 | Routing |
| Axios | HTTP client |
| React Hook Form + Zod | Form handling & validation |
| Tailwind CSS 3 | Styling |
| Recharts | Charts (analytics page) |
| Lucide React | Icons |
| react-hot-toast | Toast notifications |
| date-fns | Date formatting |
| Vitest + Testing Library | Tests |

## Key Patterns

- **Token management** — `apiClient.ts` attaches the JWT on every request and silently refreshes on 401.
- **Protected routes** — `ProtectedRoute` checks the Redux auth state; unauthenticated users are redirected to `/login`.
- **Typed Redux** — `useAppSelector` / `useAppDispatch` hooks are pre-typed so slices don't need manual generics.
- **Form validation** — pages use `react-hook-form` with a `zod` resolver for schema-based validation.
