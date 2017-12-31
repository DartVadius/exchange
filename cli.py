from flask import Flask, session
from flask_script import Manager
from app.dbmodels import Cities
from app import database
from app.services.exchange_service import ExchangeService
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'None'
app.config['SECRET_KEY'] = 'v89gs9dgyd9d256s9fy96jifp80yhpSEEEous'
app.config['SQLALCHEMY_DATABASE_URI'] = database.connect
db = SQLAlchemy(app)
manager = Manager(app)


@manager.command
def init_cities():
    with open('app/json/cities.json', encoding="utf8") as json_file:
        data = json.load(json_file)
    for value in data:
        city = Cities()
        city.country_code = value['country']
        city.city_name = value['name']
        city.lat = value['lat']
        city.lng = value['lng']
        db.session.add(city)
    db.session.commit()
    return True


@manager.command
def update_countries():
    test = ExchangeService()
    test.set_countries()
    test.set_payment_methods()
    test.set_payment_methods_by_country_codes()
    session.clear()
    return True


if __name__ == "__main__":
    manager.run()
