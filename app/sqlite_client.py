import sqlite3

def save_access_token(user_id, access_token):
    """
    Save or update the access token on the database.
    """
    with sqlite3.connect("finbuddy.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            access_token TEXT
        )
        """)

        cursor.execute("""
        INSERT INTO users (user_id, access_token) 
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET access_token = excluded.access_token
        """, (user_id, access_token))

        conn.commit()


def fetch_access_token(user_id):
    """
    Fetch the access token for the user with a given Id.
    """
    with sqlite3.connect("finbuddy.db") as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT access_token FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()

        return result
