# Spec: Registration

## Overview

Registration allows new users to create a Spendly account by providing their name, email, and password. The form already exists as a static template (`register.html`); this step wires it up to the backend so that submitted data is validated, the password is hashed, the user is stored in the database, and on success the user is shown with success message and the user is redirected to the login page on success. This is the first feature that writes user-generated data to the database.

---

## Depends on

- **Step 1 — Database Setup** (users table, `get_db`, `init_db`, `seed_db` must be working)

---

## Routes

| Method | Path        | Description                              | Access |
|--------|-------------|------------------------------------------|--------|
| GET    | `/register` | Display the registration form (exists)   | Public |
| POST   | `/register` | Validate input, create user, redirect    | Public |

---

## Database changes

No new tables or columns. Uses the existing `users` table:

| Column        | Type    | Constraints                      |
|---------------|---------|----------------------------------|
| id            | INTEGER | Primary key, autoincrement       |
| name          | TEXT    | Not null                         |
| email         | TEXT    | Unique, not null                 |
| password_hash | TEXT    | Not null                         |
| created_at    | TEXT    | Default datetime('now')          |

---

## Templates

### Modify

- **`templates/register.html`** — Add flash message or `error` display for validation failures. Preserve form values on error so the user doesn't have to retype name and email. The template already has an `{% if error %}` block and a `POST` form action, so minimal changes are needed — just ensure `value="{{ name }}"` and `value="{{ email }}"` attributes are added to retain input on validation failure.

### Create

- None

---

## Files to change

- **`app.py`** — Convert the `/register` route to handle both GET and POST. Add validation logic, password hashing, database insert, error handling, and redirect on success.
- **`templates/register.html`** — Add `value` attributes to name and email inputs so they persist on validation error.

---

## Files to create

- None

---

## New dependencies

No new dependencies. Uses:
- `werkzeug.security.generate_password_hash` (already installed)
- `sqlite3` (standard library)
- `flask.redirect`, `flask.url_for`, `flask.request` (already installed)

---

## Rules for implementation

1. No SQLAlchemy or ORMs — raw SQL only
2. Parameterised queries only — never use string formatting in SQL
3. Passwords hashed with `werkzeug.security.generate_password_hash` using `method="pbkdf2:sha256"`
4. Use CSS variables — never hardcode hex values in templates or styles
5. All templates extend `base.html`
6. Validate server-side: name, email, and password must all be non-empty after stripping whitespace
7. Password must be at least 8 characters
8. Email must not already exist in the database — catch the UNIQUE constraint violation and show a friendly error
9. On successful registration, redirect to `/login` (do not auto-login)
10. On validation failure, re-render the form with the error message and previously entered name/email (not password)
11. Strip whitespace from name and email before storing
12. Email should be stored lowercase

---

## Definition of done

- [ ] GET `/register` still renders the registration form without errors
- [ ] Submitting the form with valid name, email, and password creates a new row in the `users` table
- [ ] Password is stored as a hash, not plaintext
- [ ] After successful registration, user is redirected to `/login`
- [ ] Submitting with an empty name shows a validation error
- [ ] Submitting with an empty email shows a validation error
- [ ] Submitting with a password shorter than 8 characters shows a validation error
- [ ] Submitting with an already-registered email shows a "email already registered" error
- [ ] On validation error, the name and email fields retain their values
- [ ] The demo user from seed data is not affected by registration
- [ ] App starts without errors after changes
