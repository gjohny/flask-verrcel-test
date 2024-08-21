from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    date_joined = db.Column(db.DateTime(timezone=True), default=func.now())
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    calories = db.Column(db.Integer)
    protein = db.Column(db.Integer)
    carbs = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    notes = db.relationship('Note')
    logs = db.relationship('Log', backref='user')

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    calories = db.Column(db.Integer)
    protien = db.Column(db.String(100))
    carbs = db.Column(db.String(100))
    fat = db.Column(db.String(100))
    # foods = db.relationship('Food')

class Food(db.Model):
    __tablename__ = "food"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(100))
    calories = db.Column(db.String(100))
    protien = db.Column(db.Integer)
    carbs = db.Column(db.Integer)
    fat = db.Column(db.Integer)
    logs = db.relationship('Log', backref='food')

class Log(db.Model):
    __tablename__ = "log"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime)
    servings = db.Column(db.Integer)
    food_id = db.Column(db.Integer, db.ForeignKey('food.id'))







