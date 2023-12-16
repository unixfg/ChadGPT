import sqlite3
import asyncio
import logging
from bot_config import load_config, set_logging

config = load_config()
set_logging(config)  # Set up logging configuration
logging.info("Configuration loaded and logging set up.")

def init_db(db_path):
    """
    Initialize the SQLite database.

    Args:
    db_path (str): Path to the SQLite database file.

    Returns:
    sqlite3.Connection: The connection to the SQLite database.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS thread_mapping (
                thread_id TEXT PRIMARY KEY,
                channel_id TEXT
            )
        """)
        conn.commit()
        logging.info("Database available.")
        return conn
    except Exception as error:
        logging.error(f"Error initializing database: {error}")
        raise

# For testing
async def main():
    config = load_config()
    set_logging(config)
    db_path = config['database'].get('path', "db.sqlite3")
    try:
        with init_db(db_path) as db_conn:
            cursor = db_conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            if tables:
                logging.info("Database is active with tables: %s", tables)
            else:
                logging.info("Database is empty.")
    except Exception as error:
        logging.error("Error in initializing database: %s", error)

if __name__ == '__main__':
    asyncio.run(main())