# Spec: Registration

## Overview
Registration lets a new KharchMate visitor create a personal account so future roadmap steps can attach expenses, profile data, and authentication state to the correct user. This is the second roadmap step because the database layer from Step 1 already provides the `users` table and hashed password support needed to store new accounts safely.

## Depends on
- Step 01 — Database setup must be complete, including the `users` table with `id`, `name`, `email`, `password_hash`, and `created_at`.

## Routes
- `GET /register` — render the registration form and show success or error messages — public
- `POST /register` — validate submitted registration data, insert a new user, and show success or validation errors — public

## Database changes
No database changes. The existing `users` table in `database/db.py` already stores `name`, `email`, `password_hash`, and `created_at`.

## Templates
- **Create:** No new templates
- **Modify:** `templates/register.html` — keep extending `base.html`, display server-side validation errors, show a success message after account creation, enforce the password minimum in the form, and preserve links to the login page

## Files to change
- `app.py` — replace the placeholder registration route with GET and POST handling, validate input, check duplicate emails, hash passwords with `werkzeug`, and insert with parameterised queries
- `templates/register.html` — update the existing form to show validation/success messages and align with the implemented route behavior

## Files to create
No new project files.

## New dependencies
No new dependencies.

## Rules for implementation
- No SQLAlchemy or ORMs
- Parameterised queries only
- Passwords hashed with werkzeug
- Use CSS variables — never hardcode hex values
- All templates extend `base.html`
- Do not store plaintext passwords
- Reject missing name, invalid email, or password shorter than 8 characters
- Show a clear duplicate-email error without exposing database internals
- Use `email` uniqueness from the database as a final safeguard against duplicate accounts

## Definition of done
- [ ] App starts without errors and initializes the existing database
- [ ] `GET /register` returns the registration page and the page extends `base.html`
- [ ] Submitting a valid unique registration creates exactly one row in `users`
- [ ] The stored password is a werkzeug hash, not the submitted plaintext password
- [ ] Submitting the same email twice shows a duplicate-email error and does not create another user
- [ ] Missing name, invalid email, or a password shorter than 8 characters shows a validation error
- [ ] Successful registration shows a success message and a clear path to sign in
- [ ] All database writes use parameterised queries and no SQL string formatting
- [ ] No new pip packages are required
- [ ] UI styling uses existing CSS variables and does not introduce hardcoded hex values
