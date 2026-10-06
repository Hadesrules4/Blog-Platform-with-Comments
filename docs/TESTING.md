# Testing Guide

The project uses pytest.

## Test coverage areas

The automated suite covers:

- Health endpoint.
- User registration.
- Login.
- Duplicate registration protection.
- Post creation.
- Post editing.
- Post deletion.
- Comment creation.
- JWT authentication requirements.
- API login.
- API post creation.
- API search.

## Run tests

```bash
pytest -q
```

The GitHub Actions workflow runs the test suite against Python 3.11, 3.12 and 3.13.

## Manual acceptance checklist

- Register a new account.
- Log in and log out.
- Create a post.
- Edit the post.
- Delete the post.
- Search for posts.
- Add a comment.
- Delete your own comment.
- Verify another user cannot edit/delete your content.
- Obtain a JWT through `/api/auth/login`.
- Use the JWT to create an API post.
- Verify unauthenticated API write requests are rejected.
