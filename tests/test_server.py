import unittest
import json
import datetime
from unittest.mock import patch, MagicMock
from app import create_app

class ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_link_token(self):
        response = self.client.get('/create_link_token')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("link_token", data)

    @patch('app.server.exchange_public_token')
    @patch('app.sqlite_client.save_access_token')
    def test_exchange_public_token(self, mock_save_access_token, mock_exchange):
        mock_exchange.return_value = "mock_access_token"
        mock_save_access_token.return_value = True

        test_data = {
            "public_token": "test_public_token",
            "user_id": "test_user_id"
        }
        response = self.client.post('/exchange_public_token', json=test_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("access_token", data)

    @patch('app.server.fetch_transactions')
    def test_get_transactions(self, mock_fetch_transactions):
        mock_fetch_transactions.return_value = [
            {
                "id": "txn_123",
                "name": "Amazon",
                "amount": 29.99,
                "date": "2024-03-27",
                "logo_url": "https://logo.com/amazon.png",
                "merchant_id": "merchant_456"
            }
        ]
        
        test_data = {
            "access_token": "access-sandbox-de3ce8ef-33f8-452c-a685-8671031fc0f6",
            "start_date": "2024-01-01",
            "end_date": "2024-03-27"
        }

        response = self.client.post('/get_transactions', json=test_data)

        print(response.data)

        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("transactions", data)
        self.assertEqual(len(data["transactions"]), 1)
        self.assertEqual(data["transactions"][0]["name"], "Amazon")

    @patch('app.server.get_institution_by_id')
    def test_get_institution_by_id(self, mock_get_institution):
        mock_get_institution.return_value = {"institution": {"name": "Mock Bank"}}
        
        test_data = {
            "institution_id": "test_institution_id"
        }
        response = self.client.post('/get_institution_by_id', json=test_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("institution", data)

    @patch('app.server.get_access_token_from_db')
    def test_get_access_token_from_db(self, mock_get_access_token):
        mock_get_access_token.return_value = {"access_token": "mock_access_token"}
        
        test_data = {
            "user_id": "test_user_id"
        }
        response = self.client.post('/get_access_token', json=test_data)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn("access_token", data)

if __name__ == '__main__':
    unittest.main()
