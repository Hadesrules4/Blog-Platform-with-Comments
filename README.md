# BlogSphere — Blog Platform with Comments

A portfolio-ready full-stack blogging platform built with Python Flask, MySQL, SQLAlchemy, Bootstrap, JavaScript, Flask-Login, JWT and RESTful APIs.

## Features
- Registration, login and logout
- Bcrypt password hashing
- Role-aware authorization
- Create, edit and delete posts
- Unique SEO-friendly slugs
- Search and pagination
- Comments and comment deletion
- JWT-protected REST API
- MySQL relational database with SQLAlchemy
- Responsive Bootstrap UI
- Input validation and size limits
- Custom 404/500 pages
- Pytest test suite
- GitHub Actions CI
- Docker and Docker Compose
- Environment-based configuration

## Run locally
Requirements: Python 3.11+ and MySQL 8+.

```sql
CREATE DATABASE blog_platform CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy .env.example to .env, configure DATABASE_URL and strong secrets, then:

```bash
python run.py
```

Open http://127.0.0.1:5000.

## Docker
```bash
docker compose up --build
```

## REST API
Public:
- GET /api/health
- POST /api/auth/login
- GET /api/posts
- GET /api/posts/<id>

Protected with Authorization: Bearer <access_token>:
- POST /api/posts
- PUT /api/posts/<id>
- DELETE /api/posts/<id>
- POST /api/posts/<id>/comments
- DELETE /api/comments/<id>
- GET /api/users/me

Search/pagination: GET /api/posts?q=python&page=1&per_page=10

## Security
Bcrypt hashing, JWT authentication, session cookies with HttpOnly/SameSite, authorization checks, SQLAlchemy ORM, validation, environment secrets and configurable CORS.

For production add HTTPS, rate limiting, monitoring, backups, centralized logging and a reverse proxy.

## Testing
```bash
pytest -q
```

## Interview talking points
1. Relational data modeling and ORM relationships.
2. Authentication and authorization.
3. CRUD workflows and REST API design.
4. Session authentication versus JWT API authentication.
5. Validation of user-generated content.
6. Automated tests and CI.
7. Docker-based deployment.
8. Professional Git/GitHub workflow.
