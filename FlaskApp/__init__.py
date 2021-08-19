from flask import (Flask)
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
db = SQLAlchemy(app)
login_manager = LoginManager()


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = 'secretKey'
app.config['FLASK_APP'] = "FlaskApp"
login_manager.init_app(app)
login_manager.login_view = "login"


from . import routes
