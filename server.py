from flask import Flask, request, jsonify
from plaid_client import create_link_token, exchange_public_token
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

@app.route('/create-link-token', methods=['GET'])
def create_link():
    try:
        link_token = create_link_token()
        return jsonify({"link_token": link_token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/exchange_public_token', methods=['POST'])
def get_access_token():
    data = request.json
    public_token = data.get("public_token")
    try:
        access_token = exchange_public_token(public_token)
        return jsonify({"access_token": access_token}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
