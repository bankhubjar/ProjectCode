import os 
from flask import Flask

def create_app():
    app = Flask(__name__)

    from . import app_01_home
    app.secret_key = os.environ.get('SECRET_KEY')
    app.register_blueprint(app_01_home.appBlueprint)


    return app

