# Hugging Face Spaces Deployment

## Files Required

1. **Dockerfile** - For containerized deployment
2. **requirements-hf.txt** - Python dependencies
3. **secrets.toml** - Environment variables (create in HF Spaces Settings)

## Environment Variables (secrets.toml)

Create these in your Hugging Face Spaces Settings > Repository secrets:

```toml
DATABASE_URL = "postgresql://neondb_owner:npg_Ck0Jbg2ReLtd@ep-still-morning-addr90s2-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require"
FRONTEND_URL = "https://frontend-jei1yp699-huda-noors-projects.vercel.app"
CORS_ORIGINS = "https://frontend-jei1yp699-huda-noors-projects.vercel.app"
```

## Deploy Steps

1. Create a new Space at https://huggingface.co/spaces
2. Select "Docker" as the SDK
3. Set Hardware to "CPU basic" (or GPU if needed)
4. Clone this repository to your Space
5. Add the secrets in Settings > Repository secrets
6. The space will automatically build and deploy

## API Endpoints

- `/health` - Health check
- `/api/auth/...` - Authentication endpoints
- `/api/todos/...` - Todo CRUD endpoints
