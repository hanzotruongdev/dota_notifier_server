import os
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import firebase_admin
from firebase_admin import credentials, messaging

# init SQLAlchemy
db = SQLAlchemy()
blacklist = set()

# must set environment variable FIREBASE_CONFIG before call Initialize parameters
# more information: https://firebase.google.com/docs/admin/setup
cred = credentials.Certificate(json.loads(os.environ['FIREBASE_CONFIG']))
firebase = firebase_admin.initialize_app(cred)

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    
    app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # JWT config
    app.config['JWT_HEADER_TYPE'] = ''
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    
    # set JWT
    jwt = JWTManager(app)

    # set db
    db.init_app(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist

    # setup blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
