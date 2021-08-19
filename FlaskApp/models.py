from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime
@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    Products = db.relationship('Product', backref='user', lazy=True)
    description = db.Column(db.String(120), nullable=False)
    datejoined = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    location = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Product(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), nullable=False)
    condition = db.Column(db.String(20), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    soldstatus = db.Column(db.Boolean, default=0, nullable=False)
    price = db.Column(db.Integer, server_default='0')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    bidder_name = db.Column(db.String(80), default=None)
    image_name = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Product %r>' % self.name
