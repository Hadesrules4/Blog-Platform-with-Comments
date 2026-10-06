# REST API Reference

Base URL: `http://localhost:5000/api`

## Authentication

### POST /auth/login

Request:
```json
{"identity":"tester","password":"password123"}
```

Response:
```json
{"access_token":"<JWT>","token_type":"Bearer","user":{"id":1,"username":"tester","role":"user"}}
```

Use the returned token as:

```
Authorization: Bearer <JWT>
```

## Health

### GET /health

Returns service status.

## Posts

### GET /posts

Supports `q`, `page`, and `per_page`.

Example:
`GET /posts?q=python&page=1&per_page=10`

### GET /posts/{id}

Returns one post with comments.

### POST /posts

Authentication: JWT required.

```json
{"title":"My first API post","content":"Hello from REST."}
```

### PUT /posts/{id}

Authentication: JWT required and ownership/admin check required.

### DELETE /posts/{id}

Authentication: JWT required and ownership/admin check required.

## Comments

### POST /posts/{id}/comments

Authentication: JWT required.

```json
{"content":"Useful article!"}
```

### DELETE /comments/{id}

Authentication: JWT required and ownership/admin check required.

## Current user

### GET /users/me

Authentication: JWT required.

## HTTP status conventions

- 200 — successful request
- 201 — resource created
- 400 — validation error
- 401 — authentication required/invalid
- 403 — authenticated but not authorized
- 404 — resource not found
- 500 — unexpected server error
