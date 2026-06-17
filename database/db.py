import sqlite3
from datetime import date, timedelta
from pathlib import Path

from werkzeug.security import generate_password_hash


DB_NAME = "KharchMate.db"
DB_PATH = Path(__file__).resolve().parents[1] / DB_NAME


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            )
            """
        )

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )


def seed_db():
    with get_db() as conn:
        existing_user = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
        if existing_user is not None:
            return

        password_hash = generate_password_hash("demo123")
        cursor = conn.execute(
            """
            INSERT INTO users (name, email, password_hash)
            VALUES (?, ?, ?)
            """,
            ("Demo User", "demo@spendly.com", password_hash),
        )
        user_id = cursor.lastrowid

        current_month = date.today().replace(day=1)
        sample_expenses = [
            (42.50, "Food", "Groceries", 3),
            (18.75, "Transport", "Bus fare", 6),
            (95.00, "Bills", "Internet bill", 10),
            (24.99, "Health", "Pharmacy", 13),
            (32.00, "Entertainment", "Movie night", 17),
            (67.40, "Shopping", "Household items", 21),
            (15.00, "Other", "Miscellaneous", 24),
            (12.30, "Food", "Coffee and snacks", 27),
        ]

        conn.executemany(
            """
            INSERT INTO expenses (
                user_id,
                amount,
                category,
                date,
                description
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            [
                (
                    user_id,
                    amount,
                    category,
                    (current_month + timedelta(days=day)).isoformat(),
                    description,
                )
                for amount, category, description, day in sample_expenses
            ],
        )
