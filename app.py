import re

import sqlite3
from flask import Flask, render_template, request
from werkzeug.security import generate_password_hash

from database.db import get_db, init_db, seed_db

app = Flask(__name__)

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ------------------------------------------------------------------ #
# Helpers                                                             #
# ------------------------------------------------------------------ #

def validate_registration(name, email, password):
    errors = []

    if not name:
        errors.append("Please enter your name.")

    if not EMAIL_PATTERN.match(email):
        errors.append("Please enter a valid email address.")

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")

    return errors


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    errors = validate_registration(name, email, password)
    if errors:
        return render_template(
            "register.html",
            errors=errors,
            name=name,
            email=email,
        )

    with get_db() as conn:
        existing_user = conn.execute(
            "SELECT id FROM users WHERE LOWER(email) = LOWER(?)",
            (email,),
        ).fetchone()

        if existing_user is not None:
            return render_template(
                "register.html",
                errors=["An account with this email address already exists."],
                name=name,
                email=email,
            )

        password_hash = generate_password_hash(password)

        try:
            conn.execute(
                """
                INSERT INTO users (name, email, password_hash)
                VALUES (?, ?, ?)
                """,
                (name, email, password_hash),
            )
        except sqlite3.IntegrityError:
            return render_template(
                "register.html",
                errors=["An account with this email address already exists."],
                name=name,
                email=email,
            )

    return render_template(
        "register.html",
        success="Account created successfully. You can now sign in.",
    )


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/logout")
def logout():
    return "Logout — coming in Step 3"


@app.route("/profile")
def profile():
    return "Profile page — coming in Step 4"


@app.route("/expenses/add")
def add_expense():
    return "Add expense — coming in Step 7"


@app.route("/expenses/<int:id>/edit")
def edit_expense(id):
    return "Edit expense — coming in Step 8"


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


if __name__ == "__main__":
    with app.app_context():
        init_db()
        seed_db()

    app.run(debug=True, port=5001)
