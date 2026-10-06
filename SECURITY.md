# Security Policy

## Supported versions

The current `main` branch is the supported development version.

## Reporting a vulnerability

Please do not publish sensitive vulnerability details in a public issue. Contact the repository maintainer privately through GitHub before disclosure.

## Security controls

BlogSphere currently includes:

- Bcrypt password hashing
- JWT authentication for protected API endpoints
- HttpOnly and SameSite session cookies
- Environment-based secrets
- SQLAlchemy ORM instead of hand-built SQL queries
- Input validation and content-length limits
- Ownership and role authorization
- Configurable CORS
- Secret values excluded from Git with `.gitignore`

## Production checklist

Before deploying publicly:

- Use long, unique production secrets.
- Enable HTTPS.
- Set `SESSION_COOKIE_SECURE=1`.
- Restrict CORS to trusted origins.
- Add rate limiting.
- Enable GitHub Dependabot, secret scanning and code scanning.
- Review GitHub Actions permissions.
- Keep dependencies patched.
- Use managed database backups and monitoring.
- Never commit `.env` files or credentials.

This policy is intended for a portfolio project and is not a substitute for a production security review.
