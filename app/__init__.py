from flask import Flask
from app import database
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'None'
app.config['SECRET_KEY'] = 'v89gs9dgyd9d256s9fy96jifp80yhpSEEEous'
app.config['SQLALCHEMY_DATABASE_URI'] = database.connect
db = SQLAlchemy(app)


@app.teardown_appcontext
def shutdown_session(exception=None):
    database.db_session.remove()


from app import dbmodels
from app.services.exchange_service import ExchangeService

# global currency_counter
# currency_counter = ExchangeService.get_count(dbmodels.Currencies)

from app import views
