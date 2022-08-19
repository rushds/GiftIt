from . import db
from flask_login import UserMixin

class Gift(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    price = db.Column(db.Integer)
    description = db.Column(db.String(400))
    link = db.Column(db.String(200))
    gift_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    access_phrase = db.Column(db.String(150))
    gifts = db.relationship('Gift')
