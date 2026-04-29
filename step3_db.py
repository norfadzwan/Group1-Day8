import sqlite3
import json
import os
from datetime import datetime

DB_FILE = "currency.db"

def get_connection():
    """Create and return a database connection."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Create the 'records' table if it doesn't exist yet.
    Columns match the currency JSON: amount, base, MYR, EUR, GBP, date.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Amount REAL,
            Base TEXT,
            MYR REAL,
            EUR REAL,
            GBP REAL,
            Date TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("[DB] Database initialized. Table 'records' is ready.")

def save_to_db(currency_data):
    """
    Insert a new record into the database.
    Expects a dict like:
    {
      "amount": 1,
      "base": "USD",
      "date": "2026-04-28",
      "rates": {"EUR": 0.85616, "GBP": 0.74242, "MYR": 3.952}
    }
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO records (Amount, Base, MYR, EUR, GBP, Date)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        currency_data["amount"],
        currency_data["base"],
        currency_data["rates"]["MYR"],
        currency_data["rates"]["EUR"],
        currency_data["rates"]["GBP"],
        currency_data["date"]
    ))

    conn.commit()
    record_id = cursor.lastrowid
    conn.close()

    print(f"[DB] Saved! Record ID: {record_id}")
    return record_id

def get_all_records():
    """Fetch all records from the database (for viewing/debugging)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM records ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    from step1_scrape import scrape_country
    data = scrape_country()

    init_db()
    db_data=save_to_db(data)
    print(json.dumps(db_data, indent=2))
