# Quickstart: Phase II Full-Stack Todo Web Application

**Feature**: 001-phase-ii-fullstack-todo
**Date**: 2025-12-28

## Prerequisites

- Python 3.11+
- Node.js 18+ and npm/pnpm
- Neon PostgreSQL account (free tier available)
- Git

## Project Structure

```
Todo/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # FastAPI app entry
│   │   ├── config.py       # Environment config
│   │   ├── database.py     # DB connection
│   │   ├── models/         # SQLModel models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── routers/        # API routes
│   │   └── dependencies/   # Auth dependencies
│   ├── tests/
│   ├── alembic/            # Migrations
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App Router pages
│   │   ├── components/    # React components
│   │   ├── lib/           # Auth & API clients
│   │   └── types/         # TypeScript types
│   ├── tests/
│   ├── package.json
│   └── .env.example
│
└── specs/                  # This documentation
```

## Step 1: Database Setup (Neon)

1. Create a Neon project at https://neon.tech
2. Get connection string from dashboard
3. Note the format: `postgresql://user:password@host/database?sslmode=require`

## Step 2: Backend Setup (FastAPI)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Unix/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your Neon connection string
# DATABASE_URL=postgresql://...
```

**Environment Variables (backend/.env)**:
```
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
FRONTEND_URL=http://localhost:3000
CORS_ORIGINS=http://localhost:3000
```

## Step 3: Frontend Setup (Next.js)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
pnpm install

# Copy environment template
cp .env.example .env.local

# Edit .env.local
```

**Environment Variables (frontend/.env.local)**:
```
# Better Auth
BETTER_AUTH_SECRET=your-32-character-secret-key-here
BETTER_AUTH_URL=http://localhost:3000

# Database (same as backend)
DATABASE_URL=postgresql://user:password@host/database?sslmode=require

# Backend API
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Step 4: Database Migrations

**Better Auth tables** (run from frontend):
```bash
cd frontend
npx @better-auth/cli generate
npx @better-auth/cli migrate
```

**Todo table** (run from backend):
```bash
cd backend
alembic upgrade head
```

## Step 5: Run Development Servers

**Terminal 1 - Backend**:
```bash
cd backend
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

## Step 6: Verify Setup

1. Open http://localhost:3000 - Should see landing page
2. Navigate to /signup - Create test account
3. Navigate to /signin - Sign in with test account
4. Navigate to /todos - Should see empty todo list
5. Create a todo - Verify it appears
6. Check http://localhost:8000/docs - FastAPI Swagger UI

## Development Workflow

### Backend Development

```bash
# Run tests
pytest

# Run with auto-reload
uvicorn app.main:app --reload

# Check API docs
open http://localhost:8000/docs
```

### Frontend Development

```bash
# Run development server
npm run dev

# Run tests
npm test

# Build for production
npm run build
```

### Database Changes

```bash
# Create new migration (backend)
cd backend
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## API Testing (curl)

**Create Todo** (requires session cookie):
```bash
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -H "Cookie: better-auth.session_token=YOUR_TOKEN" \
  -d '{"description": "Test todo"}'
```

**List Todos**:
```bash
curl http://localhost:8000/api/todos \
  -H "Cookie: better-auth.session_token=YOUR_TOKEN"
```

## Troubleshooting

### CORS Errors
- Ensure `CORS_ORIGINS` in backend includes frontend URL
- Ensure `FRONTEND_URL` matches actual frontend URL

### Database Connection
- Verify Neon connection string includes `?sslmode=require`
- Check Neon dashboard for connection limits

### Session Not Working
- Clear browser cookies and re-signin
- Verify Better Auth secret matches between restarts
- Check session table in database

### Better Auth Tables Missing
- Run `npx @better-auth/cli migrate` from frontend directory
- Verify DATABASE_URL in frontend .env.local

## Key URLs

| Service | URL | Purpose |
|---------|-----|---------|
| Frontend | http://localhost:3000 | Web application |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Neon Console | https://console.neon.tech | Database management |
