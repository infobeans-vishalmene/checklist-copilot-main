# Checklist  App

A minimal Django REST + React (Vite) checklist application packaged with Docker, Nginx, and Docker Compose.
This project focuses on rapid prototyping ("vibe coding") and ships with defaults for local development.

## Quick start

1. Build & run:
```bash
docker-compose up --build
```

2. #ToDo: The frontend will be served at `http://localhost` (port 80).
   - The React app calls the backend at `/api/`.
3. Backend migrations are run automatically via the docker-compose backend command.
4. Backend Accessible on : http://0.0.0.0:8000/admin/
5. REST API Endpoint: http://0.0.0.0:8000/api/
   

## Notes

- Database: SQLite (file at backend/db.sqlite3)
- Authentication: None (public API) — adjust `checklist/views.py` permission classes to `IsAuthenticated` if you add auth.
- To create initial data, use Django admin (`/admin`) after creating a superuser inside the backend container.

## To-Do / Improvements
- Switch to Postgres for production.
- Add JWT auth and user flows.
- Add collectstatic and serve static files properly in production.
