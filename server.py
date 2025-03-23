import sqlite3

from flask import Flask, request, jsonify
from dotenv import load_dotenv

from plaid_client import (
    create_link_token, 
    exchange_public_token, 
    fetch_transactions,
    save_access_token,
    fetch_access_token
    )

app = Flask(__name__)

load_dotenv()

# Link Token Endpoint
@app.route('/create-link-token', methods=['GET'])
def create_link():
    try:
        link_token = create_link_token()

        return jsonify({"link_token": link_token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Token Exchange Endpoint
@app.route('/exchange_public_token', methods=['POST'])
def get_access_token():
    data = request.json
    public_token = data.get("public_token")
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    try:
        access_token = exchange_public_token(public_token)

        save_access_token(user_id, access_token)
        
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
    
@app.route('/get_access_token', methods=['POST'])
def get_access_token_from_db():
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    result = fetch_access_token(user_id)

    if result:
        return jsonify({"access_token": result[0]}), 200
    else:
        return jsonify({"error": "No access token found"}), 404
    
if __name__ == '__main__':
    app.run(debug=True)
