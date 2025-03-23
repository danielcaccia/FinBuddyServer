from flask import Flask, request, jsonify
from dotenv import load_dotenv

from plaid_client import create_link_token, exchange_public_token, fetch_transactions

app = Flask(__name__)

load_dotenv()

# Public Token Endpoint
@app.route('/create-link-token', methods=['GET'])
def create_link():
    try:
        link_token = create_link_token()

        return jsonify({"link_token": link_token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Access Token Endpoint
@app.route('/exchange_public_token', methods=['POST'])
def get_access_token():
    data = request.json
    public_token = data.get("public_token")

    try:
        access_token = exchange_public_token(public_token)

        return jsonify({"access_token": access_token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Transactions Endpoint
@app.route('/get_transactions', methods=['POST'])
def get_transactions():
    data = request.json
    access_token = data.get("access_token")
    
    if not access_token:
        return jsonify({"error": "Access token is required"}), 400

    try:
        transactions = fetch_transactions(access_token)
        
        return jsonify({"transactions": transactions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    app.run(debug=True)
