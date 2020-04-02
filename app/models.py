
from app import db
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    subscribeAll = db.Column(db.Boolean)
    channels = relationship('Player', secondary='subscription')

class Player(db.Model):
    __tablename__ = "player"
    id = db.Column(db.String(100), primary_key=True)
    steam_id = db.Column(db.String(100))
    name = db.Column(db.String(256))
    team_tag = db.Column(db.String(100))
    subscribers = relationship('User', secondary='subscription')


class LiveMatch(db.Model):
    __tablename__ = "livematch"
    id = db.Column(db.String(100), primary_key=True)


class Subscription(db.Model):
    __tablename__ = 'subscription'
    user_id = db.Column(
        db.Integer, 
        db.ForeignKey('user.id'), 
        primary_key = True)

    player_id = db.Column(
        db.String, 
        db.ForeignKey('player.id'), 
        primary_key = True)