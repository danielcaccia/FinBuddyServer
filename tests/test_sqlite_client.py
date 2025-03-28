import unittest
import sqlite3
from app.sqlite_client import save_access_token, fetch_access_token

class SQLiteClientTestCase(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect("finbuddy.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            access_token TEXT
        )
        """)
    
    def tearDown(self):
        self.cursor.execute("DELETE FROM users")
        self.conn.close()

    def test_save_access_token(self):
        save_access_token("test_user_id", "mock_access_token")
        self.cursor.execute("SELECT access_token FROM users WHERE user_id = ?", ("test_user_id",))
        result = self.cursor.fetchone()
        self.assertEqual(result[0], "mock_access_token")

    def test_fetch_access_token(self):
        save_access_token("test_user_id", "mock_access_token")
        access_token = fetch_access_token("test_user_id")
        self.assertEqual(access_token[0], "mock_access_token")

if __name__ == '__main__':
    unittest.main()
