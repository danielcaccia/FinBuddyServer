import os

from flask import Flask, jsonify, request
from dotenv import load_dotenv
from plaid import ApiClient, Configuration
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest

# Load environment vars
load_dotenv()

# Init Flask
app = Flask(__name__)

# Get plaid configurations
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_ENVIRONMENT = os.getenv('PLAID_ENVIRONMENT')

# Configure ApiClient
configuration = Configuration(
    host=PLAID_ENVIRONMENT,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)

# Init ApiClient
api_client = ApiClient(configuration)
plaid_api_client = plaid_api.PlaidApi(api_client)  # Alteração para usar a nova estrutura

@app.route('/get_transactions', methods=['POST'])
def get_transactions():
    try:
        # Retrieve access token
        access_token = request.json.get('access_token')
        
        # Set dates (temporarily mocked dates)
        start_date = '2024-01-01'
        end_date = '2024-03-01'
        
        # Prepare request
        request_data = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date
        )
        
        # Make request
        response = plaid_api_client.transactions_get(request_data)

        # Return response
        return jsonify(response.to_dict()['transactions'])

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
