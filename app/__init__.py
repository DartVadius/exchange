from flask import Flask, g
from app import database
from app.custom_session_interface import CustomSessionInterface
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'None'
# app.config['SQLALCHEMY_POOL_TIMEOUT'] = 120
# app.config['SQLALCHEMY_POOL_SIZE'] = 100
# app.config['SQLALCHEMY_POOL_RECYCLE'] = 120
app.config['SECRET_KEY'] = 'v89gs9dgyd9d256s9fy96jifp80yhpSEEEous'
app.config['SQLALCHEMY_DATABASE_URI'] = database.connect
db = SQLAlchemy(app)


db.session.expire_on_commit = False
db.session.pool_pre_ping = True

migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = "login"

app.session_interface = CustomSessionInterface()

bcrypt = Bcrypt(app)

@app.before_request
def _before_request():
    g.user = current_user


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


from app import views
