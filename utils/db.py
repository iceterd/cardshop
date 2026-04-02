"""
Cardshop — SQLite database layer
Handles all persistence: users, wallet balances, and transactions.
"""

import sqlite3
import os
from datetime import datetime
from contextlib import contextmanager

DB_PATH = os.environ.get("DB_PATH", "cardshop.db")


@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db():
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                email           TEXT    UNIQUE NOT NULL,
                password_hash   TEXT    NOT NULL,
                full_name       TEXT    NOT NULL DEFAULT '',
                wallet_balance  REAL    NOT NULL DEFAULT 0.0,
                created_at      TEXT    NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS transactions (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id     INTEGER NOT NULL,
                order_id    TEXT    NOT NULL,
                type        TEXT    NOT NULL,
                description TEXT    NOT NULL DEFAULT '',
                amount      REAL    NOT NULL,
                status      TEXT    NOT NULL DEFAULT 'Completed',
                created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );

            CREATE INDEX IF NOT EXISTS idx_transactions_user
                ON transactions(user_id);
        """)


def create_user(email: str, password_hash: str, full_name: str) -> int | None:
    try:
        with get_conn() as conn:
            cur = conn.execute(
                "INSERT INTO users (email, password_hash, full_name) VALUES (?, ?, ?)",
                (email.lower().strip(), password_hash, full_name.strip()),
            )
            return cur.lastrowid
    except sqlite3.IntegrityError:
        return None


def get_user_by_email(email: str) -> sqlite3.Row | None:
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email.lower().strip(),),
        ).fetchone()


def get_user_by_id(user_id: int) -> sqlite3.Row | None:
    with get_conn() as conn:
        return conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()


def get_wallet_balance(user_id: int) -> float:
    with get_conn() as conn:
        row = conn.execute(
            "SELECT wallet_balance FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return row["wallet_balance"] if row else 0.0


def update_wallet(user_id: int, delta: float) -> float:
    with get_conn() as conn:
        conn.execute(
            "UPDATE users SET wallet_balance = wallet_balance + ? WHERE id = ?",
            (delta, user_id),
        )
        row = conn.execute(
            "SELECT wallet_balance FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        return row["wallet_balance"]


def add_transaction(
    user_id: int,
    order_id: str,
    txn_type: str,
    description: str,
    amount: float,
    status: str = "Completed",
):
    with get_conn() as conn:
        conn.execute(
            """INSERT INTO transactions
               (user_id, order_id, type, description, amount, status)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (user_id, order_id, txn_type, description, amount, status),
        )


def get_transactions(user_id: int, limit: int = 50) -> list:
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT * FROM transactions
               WHERE user_id = ?
               ORDER BY created_at DESC
               LIMIT ?""",
            (user_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]


def get_transaction_stats(user_id: int) -> dict:
    with get_conn() as conn:
        row = conn.execute(
            """SELECT
                COUNT(*) AS total_transactions,
                SUM(CASE WHEN type NOT IN ('Wallet', 'Crypto Deposit', 'PayPal Deposit')
                         THEN 1 ELSE 0 END) AS total_orders,
                COALESCE(SUM(CASE WHEN type NOT IN ('Wallet', 'Crypto Deposit', 'PayPal Deposit')
                         THEN amount ELSE 0 END), 0) AS total_spent
               FROM transactions
               WHERE user_id = ?""",
            (user_id,),
        ).fetchone()
        return dict(row) if row else {"total_transactions": 0, "total_orders": 0, "total_spent": 0.0}
