"""
database/db.py — SQLite data layer for Spendly.

get_db()   — returns a SQLite connection (row_factory=Row, foreign_keys=ON)
init_db()  — creates tables if they don't exist
seed_db()  — inserts demo data once, idempotent
"""

import calendar
import os
import sqlite3
from datetime import date

from werkzeug.security import generate_password_hash

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "expense_tracker.db")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
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
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """
    )
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()
    cur = conn.cursor()

    existing = cur.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if existing > 0:
        conn.close()
        return

    password_hash = generate_password_hash("demo123", method="pbkdf2:sha256")
    cur.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash),
    )
    user_id = cur.lastrowid

    today = date.today()
    last_day = calendar.monthrange(today.year, today.month)[1]

    def day(n):
        return date(today.year, today.month, min(n, last_day)).isoformat()

    sample_expenses = [
        (45.50, "Food", day(2), "Groceries at Trader Joe's"),
        (15.00, "Transport", day(4), "Uber ride to office"),
        (120.00, "Bills", day(5), "Electricity bill"),
        (60.00, "Health", day(8), "Pharmacy - prescription"),
        (32.75, "Entertainment", day(10), "Movie tickets"),
        (89.99, "Shopping", day(14), "New running shoes"),
        (22.40, "Food", day(18), "Dinner with friends"),
        (10.00, "Other", day(21), "Miscellaneous donation"),
    ]

    cur.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) "
        "VALUES (?, ?, ?, ?, ?)",
        [(user_id, amt, cat, d, desc) for amt, cat, d, desc in sample_expenses],
    )

    conn.commit()
    conn.close()
