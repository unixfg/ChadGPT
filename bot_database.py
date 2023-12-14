import sqlite3

def init_db():
    # Load config
    from bot_config import load_config
    config=load_config()

    # Set up logging
    import logging
    logging.basicConfig(level=config['logging'].get('level', 'INFO'),format=config['logging']['format'])

    conn = sqlite3.connect(config['database'].get('path', "db.sqlite3"))
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS thread_mapping (
            thread_id TEXT PRIMARY KEY,
            channel_id TEXT
        )
    """)
    conn.commit()
    return conn

# If you want to validate or test loading the config when this file is run directly
if __name__ == '__main__':
    try:
        db_conn = init_db()
        cursor = db_conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if tables:
            print("Database is active.")
        else:
            print("Database is empty.")
    except Exception as error:
        print("Failed to load configuration:", error)