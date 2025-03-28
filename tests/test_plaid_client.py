import unittest
from unittest.mock import patch
from app.plaid_client import create_link_token, exchange_public_token, fetch_transactions

class PlaidClientTestCase(unittest.TestCase):
    @patch('app.plaid_client.plaid_client.link_token_create')
    def test_create_link_token(self, mock_link_token_create):
        mock_link_token_create.return_value = {"link_token": "mock_link_token"}

        link_token = create_link_token()
        self.assertEqual(link_token, "mock_link_token")

    @patch('app.plaid_client.plaid_client.item_public_token_exchange')
    def test_exchange_public_token(self, mock_exchange_token):
        mock_exchange_token.return_value = {"access_token": "mock_access_token"}

        access_token = exchange_public_token("mock_public_token")
        self.assertEqual(access_token, "mock_access_token")

    @patch('app.plaid_client.plaid_client.transactions_get')
    def test_fetch_transactions(self, mock_transactions_get):
        mock_transactions_get.return_value = {
            "transactions": [{"transaction_id": "1", "name": "Test", "amount": 100, "date": "2024-01-01"}]
        }

        transactions = fetch_transactions("mock_access_token")
        self.assertEqual(len(transactions), 1)
        self.assertEqual(transactions[0]["name"], "Test")

if __name__ == '__main__':
    unittest.main()
