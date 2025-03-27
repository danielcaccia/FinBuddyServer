import os
import uuid
import datetime

from dotenv import load_dotenv
import plaid
from plaid import Configuration, ApiClient
from plaid.api.plaid_api import PlaidApi
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest

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
    """
    Create a Plaid link-tokenthat will be used on the frontend.
    """
    request = LinkTokenCreateRequest(
        user={"client_user_id": str(uuid.uuid4())},
        client_name="FinBuddy",
        products=[Products('transactions')],
        country_codes=[CountryCode('US')],
        language="en",
    )

    response = plaid_client.link_token_create(request)
    return response["link_token"]


def exchange_public_token(public_token):
    """
    Exchange a public token for an access token.
    """
    request = ItemPublicTokenExchangeRequest(public_token=public_token)
    response = plaid_client.item_public_token_exchange(request)
    return response["access_token"]


def fetch_transactions(access_token):
    """
    Fetch the transactions of a user using the access token.
    """
    start_date = datetime.date(2024, 1, 1)
    end_date = datetime.date(2025, 3, 27)
    
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


def get_institution_by_id(institution_id):
    """
    Fetch information of an institution by a given Id.
    """
    request = InstitutionsGetByIdRequest(
        institution_id=institution_id,
        country_codes=[CountryCode('US')]
    )

    response = plaid_client.institutions_get_by_id(request)
    return response["institution"]
