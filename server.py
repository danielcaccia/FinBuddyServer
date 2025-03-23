import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from plaid import ApiClient, Configuration
from plaid.api import plaid_api  # Corrigido
from plaid.model.transactions_get_request import TransactionsGetRequest

# Carregar variáveis de ambiente
load_dotenv()

# Inicializando o Flask
app = Flask(__name__)

# Configurações do Plaid
PLAID_CLIENT_ID = os.getenv('PLAID_CLIENT_ID')
PLAID_SECRET = os.getenv('PLAID_SECRET')
PLAID_ENVIRONMENT = os.getenv('PLAID_ENVIRONMENT')

# Configuração do cliente API do Plaid
configuration = Configuration(
    host=PLAID_ENVIRONMENT,
    api_key={
        'clientId': PLAID_CLIENT_ID,
        'secret': PLAID_SECRET,
    }
)

# Inicializando o ApiClient com a configuração
api_client = ApiClient(configuration)
plaid_api_client = plaid_api.PlaidApi(api_client)  # Alteração para usar a nova estrutura

@app.route('/get_transactions', methods=['POST'])
def get_transactions():
    try:
        # Recuperar o access_token (por exemplo, enviado no corpo da requisição)
        access_token = request.json.get('access_token')
        
        # Definir a data de início e fim (exemplo)
        start_date = '2024-01-01'
        end_date = '2024-03-01'
        
        # Preparar a solicitação
        request_data = TransactionsGetRequest(
            access_token=access_token,
            start_date=start_date,
            end_date=end_date
        )
        
        # Fazer a requisição para o Plaid
        response = plaid_api_client.transactions_get(request_data)

        # Retornar a resposta
        return jsonify(response.to_dict()['transactions'])

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
