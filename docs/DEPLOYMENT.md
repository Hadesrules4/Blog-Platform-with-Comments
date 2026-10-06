# Deployment Notes

## Recommended production shape

Internet → HTTPS reverse proxy → Gunicorn → Flask application → managed MySQL

## Environment variables

Required:

- `SECRET_KEY`
- `JWT_SECRET_KEY`
- `DATABASE_URL`

Recommended:

- `CORS_ORIGINS`
- `SESSION_COOKIE_SECURE=1`
- `JWT_ACCESS_TOKEN_EXPIRES`

## Container deployment

The included Dockerfile runs Gunicorn. Docker Compose provides a repeatable local environment with MySQL.

For a real deployment, replace development credentials with platform secrets and use a managed database.

## Operational improvements

For production readiness, add:

- HTTPS certificates.
- Rate limiting.
- Structured logs.
- Application monitoring.
- Database backups.
- Health checks.
- Automated dependency updates.
- A deployment pipeline with staging before production.
