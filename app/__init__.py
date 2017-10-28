from flask import Flask
from app import database
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'None'
app.config['SECRET_KEY'] = 'very-very-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = database.connect
db = SQLAlchemy(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()


from app import views, dbmodels
