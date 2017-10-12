from flask import Flask
from app import database

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'None'
app.config['SECRET_KEY'] = 'very-very-secret-key'

database.init_db()

@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()


from app import views, dbmodels
