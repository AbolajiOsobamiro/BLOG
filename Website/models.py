from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique = True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    blogs = db.relationship('Blog', backref='user', lazy=True)



class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(10000), unique = True, nullable = False)
    category = db.Column(db.String(1500), nullable=False, default="Uncategorized")
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    content = db.Column(db.String(9999999999999999999999999999999999999), unique = True, nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
   