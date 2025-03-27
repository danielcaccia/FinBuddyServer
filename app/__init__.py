from flask import Flask
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    
    load_dotenv()

    from .server import app as server_blueprint
    app.register_blueprint(server_blueprint)

    return app
