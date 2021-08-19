from FlaskApp import db
from FlaskApp.models import User, Product
from werkzeug.security import generate_password_hash, check_password_hash

db.drop_all()
db.create_all()

U1 = User(username="TomRowland",password=generate_password_hash("password"),description="I make electronic music and like sell stuff",location="Manchester, UK")
U2 = User(username="EdSimons",password=generate_password_hash("password"),description="I make block rockin beats with a friend of mine.",location="Manchester, UK")
U3 = User(username="ThomasBang",password=generate_password_hash("password"),description="I had a breakup with a friend who I made music with.",location="Paris, France")

P1 = Product(name="Dell Mouse",condition="New",status=0,user_id=1,image_name="dell.jpg")
P2 = Product(name="Redgear Controller",condition="New",status=0,user_id=1,image_name="redgear.jpg")
P3 = Product(name="Logitech Keyboard",condition="Used",status=0,user_id=2,image_name="logitech.jpg")


db.session.add(U1)
db.session.add(U2)
db.session.add(U3)
db.session.add(P1)
db.session.add(P2)
db.session.add(P3)
db.session.commit()

print("Data added")
