import os

from dotenv import load_dotenv
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid import ApiClient, Configuration

# Carregar variáveis de ambiente
load_dotenv()

# Configuração da API do Plaid
configuration = Configuration(
    host=os.getenv("PLAID_ENV", "sandbox"),
    api_key={
        "clientId": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET"),
    }
)
api_client = ApiClient(configuration)
plaid_client = plaid_api.PlaidApi(api_client)

def create_link_token():
    request = LinkTokenCreateRequest(
        user={"client_user_id": "user123"},
        client_name="FinBuddy",
        products=["transactions"],
        country_codes=["US"],
        language="en"
    )
    response = plaid_client.link_token_create(request)
    return response["link_token"]

def exchange_public_token(public_token):
    request = ItemPublicTokenExchangeRequest(public_token=public_token)
    response = plaid_client.item_public_token_exchange(request)
    return response["access_token"]
