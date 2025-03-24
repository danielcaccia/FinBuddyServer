# Main imports
import os
import uuid
import datetime
import sqlite3

from dotenv import load_dotenv

# General Plaid API imports
import plaid
from plaid import Configuration, ApiClient
from plaid.api.plaid_api import PlaidApi

# Public Token imports
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

# Access Token imports
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

# Transactions imports
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions

load_dotenv()

# API Configuration
configuration = Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        "clientId": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET"),
    }
)

api_client = ApiClient(configuration)
plaid_client = PlaidApi(api_client)

# Public Token request
def create_link_token():
    request = LinkTokenCreateRequest(
        user={"client_user_id": str(uuid.uuid4())},
        client_name="FinBuddy",
        products=[Products('transactions')],
        country_codes=[CountryCode('US')],
        language="en",
    )

    response = plaid_client.link_token_create(request)

    return response["link_token"]

# Access Token request
def exchange_public_token(public_token):
    request = ItemPublicTokenExchangeRequest(public_token=public_token)
    response = plaid_client.item_public_token_exchange(request)

    return response["access_token"]

# Transactions
def fetch_transactions(access_token):
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2025, 3, 1)
    
    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=start_date,
        end_date=end_date,
        options=TransactionsGetRequestOptions(count=50)
    )

    response = plaid_client.transactions_get(request)
    transactions = []

    for txn in response["transactions"]:
        transactions.append({
            "id": txn["transaction_id"],
            "name": txn["merchant_name"] or txn["name"],
            "amount": txn["amount"],
            "date": txn["date"]
        })

    return transactions

# Save Access Token
def save_access_token(user_id, access_token):
    conn = sqlite3.connect("finbuddy.db")
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
    conn.close()

# Fetch Access Token
def fetch_access_token(user_id):
    conn = sqlite3.connect("finbuddy.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT access_token FROM users WHERE user_id = ?", (user_id,))
    result = cursor.fetchone()
    
    conn.commit()
    conn.close()
    
    return result
    