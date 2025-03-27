from flask import Flask, request, jsonify
from dotenv import load_dotenv

from plaid_client import create_link_token, exchange_public_token, fetch_transactions
from sqlite_client import save_access_token, fetch_access_token

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

@app.route('/create_link_token', methods=['GET'])
def create_link():
    """
    Endpoint to create a Plaid link-token.
    """
    try:
        link_token = create_link_token()
        return jsonify({"link_token": link_token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/exchange_public_token', methods=['POST'])
def get_access_token():
    """
    Endpoint to exchange the public token for an access token.
    """
    data = request.json
    public_token = data.get("public_token")
    user_id = data.get("user_id")

    if not public_token or not user_id:
        return jsonify({"error": "public_token and user_id are required"}), 400

    try:
        access_token = exchange_public_token(public_token)
        save_access_token(user_id, access_token)
        return jsonify({"access_token": access_token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_transactions', methods=['POST'])
def get_transactions():
    """
    Endpoint to fetch transactions using the access token.
    """
    data = request.json
    access_token = data.get("access_token")

    if not access_token:
        return jsonify({"error": "Access token is required"}), 400

    try:
        transactions = fetch_transactions(access_token)
        return jsonify({"transactions": transactions}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_institution_by_id', methods=['POST'])
def get_institution_by_id():
    """
    Endpoint to fetch information of an institution by a given Id.
    """
    data = request.json
    institution_id = data.get("institution_id")

    if not institution_id:
        return jsonify({"error": "Institution ID is required"}), 400

    try:
        institution = get_institution_by_id(institution_id)
        if institution:
            return jsonify({"institution": institution}), 200
        return jsonify({"error": "Institution not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_access_token', methods=['POST'])
def get_access_token_from_db():
    """
    Endpoint to fetch the access token from the database.
    """
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "User ID is required"}), 400

    result = fetch_access_token(user_id)
    if result:
        return jsonify({"access_token": result[0]}), 200
    return jsonify({"error": "No access token found"}), 404


if __name__ == '__main__':
    app.run(debug=True)
