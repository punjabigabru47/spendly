# Spec: Login and Logout

## Overview

Login and logout give registered users the ability to authenticate and manage their session. The login form already exists as a static template (`login.html`); this step wires it up so that submitted credentials are validated against the database, a session is created on success, and the user is redirected to a future dashboard page. Logout clears the session and redirects to the landing page. The navbar is updated to show contextual links based on whether the user is logged in. This is the first feature that introduces session management and access control patterns that all future authenticated features will build on.

---

## Depends on

- **Step 1 — Database Setup** (users table, `get_db` must be working)
- **Step 2 — Registration** (ability to create user accounts)

---

## Routes

| Method | Path      | Description                                              | Access    |
|--------|-----------|----------------------------------------------------------|-----------|
| GET    | `/login`  | Display the login form (template exists)                 | Public    |
| POST   | `/login`  | Validate credentials, create session, redirect           | Public    |
| GET    | `/logout` | Clear the session and redirect to landing page           | Logged-in |

---

## Database changes

No new tables or columns. Uses the existing `users` table to look up users by email and verify password hashes.

---

## Templates

### Modify

- **`templates/login.html`** — Add `value="{{ email }}"` to the email input so it persists on validation error. The template already has an `{% if error %}` block.
- **`templates/base.html`** — Update the navbar to show different links depending on session state:
  - **Logged out:** Show "Sign in" and "Get started" (current behavior)
  - **Logged in:** Show user's name and a "Sign out" link

### Create

- None

---

## Files to change

- **`app.py`** — Convert the `/login` route to handle both GET and POST. Add credential validation, session management, and logout logic. Add a `load_logged_in_user` function that runs before each request to make the current user available to all templates via `g.user`.
- **`templates/login.html`** — Add `value` attribute to email input to retain on error.
- **`templates/base.html`** — Update navbar to show contextual links based on login state.

---

## Files to create

- None

---

## New dependencies

No new dependencies. Uses:
- `werkzeug.security.check_password_hash` (already installed)
- `flask.session` (built into Flask)
- `flask.g` (built into Flask)

---

## Rules for implementation

1. No SQLAlchemy or ORMs — raw SQL only
2. Parameterised queries only — never use string formatting in SQL
3. Passwords verified with `werkzeug.security.check_password_hash`
4. Use CSS variables — never hardcode hex values in templates or styles
5. All templates extend `base.html`
6. Store only the user's `id` in `session["user_id"]` — do not store the entire user row
7. Use `@app.before_request` to load the current user into `g.user` on every request by querying the database with `session["user_id"]`
8. On login failure, show a generic error message like "Invalid email or password" — do not reveal whether the email exists
9. On successful login, redirect to `/` (landing page for now; will change to dashboard in a later step)
10. On logout, clear the session with `session.clear()` and redirect to `/`
11. Strip whitespace from email and convert to lowercase before lookup
12. The login form should retain the email value on failed attempts (not the password)
13. Do not auto-login after registration (already handled — registration redirects to `/login`)

---

## Definition of done

- [ ] GET `/login` renders the login form without errors
- [ ] Submitting valid email and password for an existing user logs the user in and redirects to `/`
- [ ] Submitting an incorrect password shows "Invalid email or password" error
- [ ] Submitting a non-existent email shows the same generic error (no email enumeration)
- [ ] After login, the navbar shows the user's name and a "Sign out" link instead of "Sign in" / "Get started"
- [ ] Clicking "Sign out" clears the session and redirects to the landing page
- [ ] After logout, the navbar shows "Sign in" and "Get started" again
- [ ] The email field retains its value on failed login attempts
- [ ] Flash message from registration ("Account created successfully! Please sign in.") is visible on the login page
- [ ] The demo user (demo@spendly.com / demo123) can log in successfully
- [ ] Session persists across page refreshes until the user logs out
- [ ] App starts without errors after changes
