import sqlite3
from datetime import datetime, timedelta
from config import SUBSCRIPTIONS

def init_db():
    conn = sqlite3.connect("subscriptions.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            user_id TEXT PRIMARY KEY,
            subscription_id TEXT,
            end_date TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_subscription(user_id: str, subscription_id: str):
    conn = sqlite3.connect("subscriptions.db")
    c = conn.cursor()
    end_date = (datetime.now() + timedelta(days=SUBSCRIPTIONS[subscription_id]["duration_days"])).isoformat()
    c.execute("INSERT OR REPLACE INTO subscriptions (user_id, subscription_id, end_date) VALUES (?, ?, ?)",
              (user_id, subscription_id, end_date))
    conn.commit()
    conn.close()

def get_subscription(user_id: str):
    conn = sqlite3.connect("subscriptions.db")
    c = conn.cursor()
    c.execute("SELECT subscription_id, end_date FROM subscriptions WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    conn.close()
    if result:
        subscription_id, end_date = result
        if datetime.fromisoformat(end_date) > datetime.now():
            return subscription_id, end_date
    return None, None
