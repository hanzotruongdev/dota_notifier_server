from flask import Blueprint, jsonify, request
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from app import db
from .models import User, Player, Subscription
from firebase_admin import messaging

main = Blueprint('main', __name__)

@main.route('/')
def main_root():
    return jsonify(msg='welcome to Dotanotifier!'), 200

@main.route('/api')
def api_root():
    return jsonify(msg='Welcome to Dotanotifier api v1.0'), 200

@main.route('/api/users/profile', methods=['GET'])
@jwt_required
def api_profile_get():
    
    user_email = get_jwt_identity()
    print("user identity (email): ", user_email)
    
    user = User.query.filter_by(email=user_email).first()

    return jsonify(id=user.id, name=user.name, email=user.email, subscribeAll= 1 if user.subscribeAll else 0), 200

@main.route('/api/users/profile', methods=['PATCH'])
@jwt_required
def api_profile_update():

    user_email = get_jwt_identity()
    print("user identity (email): ", user_email)
    
    subscribeAll=request.headers.get('subscribeAll')
    firebaseToken = request.headers.get('firebaseToken')

    user = User.query.filter_by(email=user_email).first()

    if subscribeAll == 0 or subscribeAll == '0':
        user.subscribeAll = False
        messaging.unsubscribe_from_topic(firebaseToken, "all")
    elif subscribeAll == 1 or subscribeAll == '1':
        user.subscribeAll = True
        messaging.subscribe_to_topic(firebaseToken, "all")
    else:
        return jsonify(msg = "Invalid value"), 400

    db.session.commit()
    
    return jsonify(msg = "Successfully update subscribe/Unsubscribe to all"), 200



@main.route('/api/subscribes', methods=['GET'])
@jwt_required
def api_subscribes_get():
    user_email = get_jwt_identity()
    print("user identity (email): ", user_email)

    user = User.query.filter_by(email=user_email).first()

    res = []
    for c in user.channels:
        res.append(c.id)
        
    print("subscrition channels: ", res)

    return jsonify(res), 200
    

@main.route('/api/subscribes', methods=['POST'])
@jwt_required
def api_subscribes_post():
    
    user_email = get_jwt_identity()
    print("user identity (email): ", user_email)

    id = request.headers.get("playerid")
    token = request.headers.get('firebasetoken')

    user = User.query.filter_by(email=user_email).first()
    player = Player.query.filter_by(id=id).first()

    if user and player and token:

        res = messaging.subscribe_to_topic(tokens = [token], topic=id)
        user.channels.append(player)
        db.session.commit()

        return jsonify(msg="Successfully create new relation"), 200
    else:
        return jsonify(msg="There is no Pro Player with id %s" % id), 400

@main.route('/api/subscribes', methods=['DELETE'])
@jwt_required
def api_subscribes_delete():
    user_email = get_jwt_identity()
    print("user identity (email): ", user_email)

    player_id = request.headers.get("playerid")
    token = request.headers.get('firebasetoken')

    user = User.query.filter_by(email=user_email).first()
    player = Player.query.filter_by(id=player_id).first()

    print("player: ", player)

    if user and player and token:

        res = messaging.unsubscribe_from_topic(tokens = [token], topic=player_id)

        Subscription.query.filter_by(user_id=user.id, player_id=player_id).delete()
        db.session.commit()
        
        return jsonify(msg="Successfully unsubscribe!"), 200
    else:
        return jsonify(msg="Error while delete subscription"), 500

    



    