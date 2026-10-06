# Contributing

## Development workflow

1. Create a feature branch.
2. Make a focused change.
3. Add or update tests.
4. Run `pytest -q`.
5. Update documentation when behavior changes.
6. Open a pull request against `main`.

## Code expectations

- Keep route handlers focused.
- Validate user input.
- Avoid hard-coded secrets.
- Preserve authorization checks.
- Prefer SQLAlchemy ORM operations.
- Add regression tests for fixed bugs.

## Commit examples

- `feat: add post search filters`
- `fix: prevent unauthorized comment deletion`
- `docs: improve API reference`
- `test: cover duplicate registration`
