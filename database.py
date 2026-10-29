import sqlite3

DB_NAME = "database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            subscription_url TEXT,
            expire_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            order_id TEXT PRIMARY KEY,
            user_id INTEGER,
            amount REAL,
            days INTEGER,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def add_or_update_user(user_id, username, full_name, subscription_url=None, expire_date=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, username, full_name, subscription_url, expire_date)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            username = excluded.username,
            full_name = excluded.full_name,
            subscription_url = COALESCE(excluded.subscription_url, users.subscription_url),
            expire_date = COALESCE(excluded.expire_date, users.expire_date)
    """, (user_id, username, full_name, subscription_url, expire_date))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, full_name, subscription_url, expire_date FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "user_id": row[0],
            "username": row[1],
            "full_name": row[2],
            "subscription_url": row[3],
            "expire_date": row[4]
        }
    return None

def create_payment(order_id, user_id, amount, days):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO payments (order_id, user_id, amount, days, status)
        VALUES (?, ?, ?, ?, 'pending')
    """, (order_id, user_id, amount, days))
    conn.commit()
    conn.close()

def get_payment(order_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT order_id, user_id, amount, days, status FROM payments WHERE order_id = ?", (order_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "order_id": row[0],
            "user_id": row[1],
            "amount": row[2],
            "days": row[3],
            "status": row[4]
        }
    return None

def update_payment_status(order_id, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE payments SET status = ? WHERE order_id = ?", (status, order_id))
    conn.commit()
    conn.close()
