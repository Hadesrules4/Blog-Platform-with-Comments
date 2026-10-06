# Architecture

## Overview

BlogSphere follows a modular Flask architecture:

Browser UI → Flask routes → service/model layer → SQLAlchemy → MySQL

REST clients use:

REST Client → JWT authentication → API blueprints → SQLAlchemy → MySQL

## Application layers

- **Presentation:** Jinja2 templates, Bootstrap and JavaScript.
- **Web routes:** authentication, post CRUD and comments.
- **API routes:** JSON REST endpoints protected with JWT where required.
- **Data layer:** SQLAlchemy models and relationships.
- **Configuration:** environment-driven secrets, database URL, CORS and cookie settings.
- **Testing:** pytest tests covering web and API behavior.
- **Delivery:** Docker Compose for local multi-container execution and GitHub Actions for CI.

## Database model

### users
- id — primary key
- username — unique
- email — unique
- password_hash
- role
- created_at

### posts
- id — primary key
- title
- slug — unique
- content
- author_id — foreign key → users.id
- created_at
- updated_at

### comments
- id — primary key
- content
- author_id — foreign key → users.id
- post_id — foreign key → posts.id
- created_at

Relationships:
- One user can create many posts.
- One user can create many comments.
- One post can contain many comments.
- Deleting a user or post cascades to dependent records.

## Authentication design

The browser uses Flask-Login session authentication. REST clients use JWT bearer tokens. Passwords are never stored directly; bcrypt hashes are stored instead.

## Authorization

A normal user can modify their own posts/comments. An administrator can manage any post/comment. API authorization checks ownership before update/delete operations.

## Request lifecycle

1. Request enters Flask.
2. Blueprint resolves the route.
3. Authentication/authorization is checked where required.
4. Input is validated.
5. SQLAlchemy performs database work.
6. HTML or JSON is returned.
7. Errors are converted into user-friendly responses.

## Future scaling

For larger deployments, the application can be extended with Redis caching, background jobs, object storage for media, a reverse proxy, centralized logging and managed MySQL.
