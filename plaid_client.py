import os
from dotenv import load_dotenv

# Plaid API imports
import plaid
from plaid import Configuration, ApiClient
from plaid.api.plaid_api import PlaidApi
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

load_dotenv()

configuration = Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        "clientId": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET"),
    }
)

api_client = ApiClient(configuration)
plaid_client = PlaidApi(api_client)

def create_link_token():
    request = LinkTokenCreateRequest(
        user={"client_user_id": "user123"},
        client_name="FinBuddy",
        products=[Products('transactions')],
        country_codes=[CountryCode('US')],
        language="en"
    )

    response = plaid_client.link_token_create(request)

    return response["link_token"]

def exchange_public_token(public_token):
    request = ItemPublicTokenExchangeRequest(public_token=public_token)
    response = plaid_client.item_public_token_exchange(request)

    return response["access_token"]
