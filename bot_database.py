import sqlite3
import asyncio
from bot_config import load_config


def init_db(db_path):
    """
    Initialize the SQLite database.

    Args:
    db_path (str): Path to the SQLite database file.

    Returns:
    sqlite3.Connection: The connection to the SQLite database.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS thread_mapping (
            thread_id TEXT PRIMARY KEY,
            channel_id TEXT
        )
    """)
    conn.commit()
    return conn

# For testing
async def main():
    config = load_config()

    db_path = config['database'].get('path', "db.sqlite3")
    try:
        with init_db(db_path) as db_conn:
            cursor = db_conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            if tables:
                print("Database is active.")
            else:
                print("Database is empty.")
    except Exception as error:
        print("Error in initializing database:", error)

if __name__ == '__main__':
    asyncio.run(main())
