#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, session
from flask_script import Manager
from app.dbmodels import Cities, User
from app import database
from app.services.exchange_service import ExchangeService
from app.services.statistic_service import StatisticService
from flask_sqlalchemy import SQLAlchemy
import json
import csv

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'None'
app.config['SECRET_KEY'] = 'v89gs9dgyd9d256s9fy96jifp80yhpSEEEous'
app.config['SQLALCHEMY_DATABASE_URI'] = database.connect
db = SQLAlchemy(app)
manager = Manager(app)


@manager.command
def init_cities_json():
    # все города с населением более 1000 челоек, дохуя городов короче
    # добавляем в базу список городов из текстового файла
    # использовать 1 раз для инициализации приложения
    with open('app/files/cities.json', encoding="utf8") as json_file:
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
def init_cities_csv():
    # поменьше городов
    # добавляем в базу список городов из текстового файла
    # использовать 1 раз для инициализации приложения
    with open('app/files/simplemaps-worldcities-basic.csv', encoding="utf8") as csv_file:
        read_csv = csv.reader(csv_file, delimiter=',')
        count = 1
        for row in read_csv:
            if count == 1:
                count = 2
                continue
            try:
                city = Cities()
                city.country_code = row[6]
                city.city_name = row[0]
                city.lat = row[2]
                city.lng = row[3]
                db.session.add(city)
            except Exception as e:
                print(e.__traceback__)
        db.session.commit()


@manager.command
def update_countries_and_payment_methods():
    # обновляем список стран и методов оплаты, привязываем методы оплаты к стране и обменнику
    model = ExchangeService()
    model.set_countries()
    model.set_payment_methods()
    model.set_payment_methods_by_country_codes()
    session.clear()
    return True


@manager.command
def update_rates():
    # обновляем статиститку по обменникам + добавляем новые валюты, если они есть
    exchange_service_model = ExchangeService()
    exchange_service_model.set_rates()
    session.clear()
    return True


@manager.command
def update_statistic():
    # обновляем статистику для главной страницы
    model = StatisticService()
    model.set_statistic()
    return True


@manager.command
def add_user(login, password):
    # добавление пользователя в дб, пользователь добавляется как неактивный
    user = User.create(login, password)
    db.session.add(user)
    db.session.commit()
    return True


if __name__ == "__main__":
    manager.run()
