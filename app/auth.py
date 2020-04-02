from flask import Blueprint, request, Response, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    jwt_required, jwt_refresh_token_required,
    create_access_token, create_refresh_token, 
    get_raw_jwt,
    get_jwt_identity
)
from firebase_admin import messaging
from .models import User, Player, Subscription
from . import db
from . import blacklist
from .utils import validate_email



auth = Blueprint('auth', __name__)

@auth.route('/api/auth/login', methods=['POST'])
def api_login_post():
    # process user login
    email = request.headers.get('email')
    password = request.headers.get('password')
    remember = True if request.headers.get('remember') else False
    firebaseToken = request.headers.get('firebase_token')

    user = User.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):

        print("==> New user logged in: ", email)

        if firebaseToken and firebaseToken != '':
            print("This user need to setup firebase...")
            # subscribe to followed topic using new firebase token
            if user.subscribeAll:
                messaging.subscribe_to_topic([firebaseToken], 'all')
                print('Subscribe to all')
            
            cs = []
            for c in user.channels:
                cs.append(c.id)
                messaging.subscribe_to_topic([firebaseToken], c.id)

            print('Subscribe to channels: ', cs)

        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=email)
        refresh_token = create_refresh_token(identity=email)
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        return jsonify(msg='Email or password is incorrect!'), 400

@auth.route('/api/auth/refresh', methods=['POST'])
@jwt_refresh_token_required
def api_refresh():
    # refersh token
    email = get_jwt_identity()
    access_token = create_access_token(identity=email)

    return jsonify(access_token=access_token), 200

@auth.route('/api/auth/signup', methods=['POST'])
def api_signup_post():
    # process signup
    email = request.headers.get('email')
    name = request.headers.get('name')
    password = request.headers.get('password')

    if not validate_email(email):
        return jsonify(msg='Invalid email address!'), 400

    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify(msg='User existed!'), 400
    
    # create new user
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), subscribeAll = True)
    db.session.add(new_user)
    db.session.commit()

    # return http status
    return jsonify(msg='User creaated successfully'), 200

# Endpoint for revoking the current users access token
@auth.route('/api/auth/logout', methods=['DELETE'])
@jwt_required
def api_logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify(msg ="Successfully logged out"), 200