from flask import Flask, g
from app import database
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'None'
app.config['SECRET_KEY'] = 'v89gs9dgyd9d256s9fy96jifp80yhpSEEEous'
app.config['SQLALCHEMY_DATABASE_URI'] = database.connect
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

bcrypt = Bcrypt(app)


@app.before_request
def _before_request():
    g.user = current_user


@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()


from app import views
