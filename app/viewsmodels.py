import datetime
import json
import threading
import time
import pprint

from flask import render_template, redirect, request, url_for, session, jsonify
from flask_login import login_user, logout_user, current_user

from app.apiV10 import Api
from app.dbmodels import Content, CurrencyStatistic, Countries, Cities
from app.forms import LoginForm
from app.services.cache_service import CacheService
from app.services.country_repository import CountryRepository
from app.services.currency_repository import CurrencyRepository
from app.services.exchange_service import ExchangeService
from app.services.localbitcoins.localbitcoins_service import LocalbitcoinsService
from app.services.payment_method_repository import PaymentMethodRepository
from app.services.rate_repository import RateRepository
from app.services.session_service import SessionService
from app.services.statistic_service import StatisticService
from app.services.stock_repository import StockRepository
from app.dbmodels import db


def merge_template(template, **kwargs):
    contentRecord = Content.query.filter_by(url=request.path).first()
    if (not contentRecord):
        return render_template(template, **kwargs)

    if type(contentRecord.data) is dict:
        data = contentRecord.data
    else:
        data = json.loads(contentRecord.data)

    for key, value in data.items():
        if key in kwargs:
            data[key] = kwargs[key]

    return render_template(template, **data)


class ViewsModels:
    def __init__(self):
        user_session = SessionService()
        user_session.set_count()

    def currencies(self, page, currency):
        currency_repository = CurrencyRepository()
        if currency != 'all' and currency != '':
            statistic_service = StatisticService()
            currency_data = RateRepository.get_currency_rates_by_name(currency)
            graph = statistic_service.create_graph_for_single_page(currency)
            return render_template("currency.html", title=currency.upper(), currency_data=currency_data, graph=graph)
        if currency == 'all':
            curr = CurrencyStatistic()
            currencies = currency_repository.get_currencies_statistic_paginate(1, curr.count())
            all_pages = True
        if currency == '':
            currencies = currency_repository.get_currencies_statistic_paginate(page, 100)
            all_pages = False
        return merge_template("currencies.html", title='Currencies', currencies=currencies, all=all_pages)

    def stock(self, stock_slug):
        rate_repository = RateRepository()
        stock_repository = StockRepository()
        stock_id = stock_repository.get_stock_id_by_slug(stock_slug)
        exchange_rates = rate_repository.get_rates_by_stock_id(stock_id)
        date = rate_repository.get_date_by_stock_id(stock_id)
        name = stock_repository.get_stock_name_by_id(stock_id)
        return render_template("stock_view/stock_exchange.html", title=name.title(), rates=exchange_rates,
                               date=date, name=name.title())

    def buy_btc(self, buy_type, params):
        country = CountryRepository()
        methods = PaymentMethodRepository()
        currency = CurrencyRepository()
        countries = country.get_all()
        payment_methods = methods.get_all()
        currencies = currency.get_fiat_currencies()
        count = None
        country_id = country_id_cash = method_id = currency_id = city = None
        h = []
        if buy_type == 'online':
            country_id = request.form.get('country_id')
            method_id = request.form.get('payment_method_id')
            currency_id = request.form.get('currency_id')
            if country_id is not None or method_id is not None or currency_id is not None:
                count = self.get_sellers(country_id, method_id, currency_id)
        if buy_type == 'cash':
            country_id_cash = request.form.get('country_id_cash')
            country_find = Countries.query.filter(Countries.id == country_id_cash).first()
            cities_find = Cities.query.filter(Cities.country_code == country_find.name_alpha2).order_by(
                Cities.city_name).all()
            for city in cities_find:
                h.append({'city_id': city.id, 'city_name': city.city_name})
            city = request.form.get('city_id')
            if city is not None:
                count = self.get_sellers_cash(city)
        select = {'country': country_id, 'method': method_id, 'currency': currency_id, 'country_cash': country_id_cash,
                  'city': city, 'cities': h}
        return render_template("buy_currency.html", title='Buy Bitcoins', data=countries, methods=payment_methods,
                               currencies=currencies, count=count, select=select)

    def sell_btc(self):
        country = CountryRepository()
        methods = PaymentMethodRepository()
        currency = CurrencyRepository()
        countries = country.get_all()
        payment_methods = methods.get_all()
        currencies = currency.get_fiat_currencies()
        return render_template("sell_currency.html", title='Sell Bitcoins', data=countries, methods=payment_methods,
                               currencies=currencies)

    def get_cities(self):
        country_id = request.json['country_id']
        country_find = Countries.query.filter(Countries.id == country_id).first()
        cities_find = Cities.query.filter(Cities.country_code == country_find.name_alpha2).order_by(
            Cities.city_name).all()
        h = []
        for city in cities_find:
            h.append({'city_id': city.id, 'city_name': city.city_name})
        return jsonify(h)

    def get_sellers(self, country, method, currency):
        model = LocalbitcoinsService()
        country_find = CountryRepository.get_by_id(country)
        method_find = PaymentMethodRepository.get_by_id(method)
        currency_find = CurrencyRepository.get_by_id(currency)
        common_sellers = model.get_sellers(country_find, method_find, currency_find)
        thread_rate = threading.Thread(target=self.update_sellers_thread, args=(country, method, currency,))
        thread_rate.daemon = True
        thread_rate.start()
        if common_sellers is None:
            return 0
        return len(common_sellers.keys())

    def get_sellers_cash(self, city_id):
        model = LocalbitcoinsService()
        cities_find = Cities.query.filter_by(id=city_id).first()
        if cities_find.link_sellers is None:
            url = model.get_users_cash_link(cities_find.lat, cities_find.lng)
            cities_find.link_sellers = url['buy_local_url']
            db.session.add(cities_find)
            db.session.commit()
        user_list = model.get_users_cash_list(cities_find.link_sellers)
        # pprint.pprint(len(user_list.keys()))
        # places = model.get_sellers_cash(data['lat'], data['lng'])
        return len(user_list.keys())

    def get_buyers(self):
        model = LocalbitcoinsService()
        data = request.json
        country_find = CountryRepository.get_by_id(data['country_id'])
        method_find = PaymentMethodRepository.get_by_id(data['payment_method_id'])
        currency_find = CurrencyRepository.get_by_id(data['currency_id'])
        common_sellers = model.get_buyers(country_find, method_find, currency_find)
        thread_rate = threading.Thread(target=self.update_buyers_thread, args=(data,))
        thread_rate.daemon = True
        thread_rate.start()
        return jsonify(len(common_sellers.keys()))

    def get_buyers_cash(self):
        model = LocalbitcoinsService()
        city_id = request.json['city_id']
        cities_find = Cities.query.filter_by(id=city_id).first()
        if cities_find.link_buyers is None:
            url = model.get_users_cash_link(cities_find.lat, cities_find.lng)
            cities_find.link_buyers = url['sell_local_url']
            db.session.add(cities_find)
            db.session.commit()
        user_list = model.get_users_cash_list(cities_find.link_buyers)
        # places = model.get_sellers_cash(data['lat'], data['lng'])
        return jsonify(len(user_list.keys()))

    @staticmethod
    def update_sellers_thread(country, method, currency):
        bitcoin_service = LocalbitcoinsService()
        if bool(method):
            method_find = PaymentMethodRepository.get_by_id(method)
            method_sellers = bitcoin_service.buy_bitcoins_method(method_find.method)
            CacheService.set_sellers(method_find.method, json.dumps(method_sellers))
        if bool(country):
            country_find = CountryRepository.get_by_id(country)
            country_sellers = bitcoin_service.buy_bitcoins_country(country_find.name_alpha2, country_find.description)
            CacheService.set_sellers(country_find.name_alpha2, json.dumps(country_sellers))
        if bool(currency):
            currency_find = CurrencyRepository.get_by_id(currency)
            currency_sellers = bitcoin_service.buy_bitcoins_currency(currency_find.name.lower())
            CacheService.set_sellers(currency_find.name.lower(), json.dumps(currency_sellers))

    @staticmethod
    def update_buyers_thread(data):
        bitcoin_service = LocalbitcoinsService()
        if bool(data['payment_method_id']):
            method_find = PaymentMethodRepository.get_by_id(data['payment_method_id'])
            method_sellers = bitcoin_service.sell_bitcoins_method(method_find.method)
            CacheService.set_buyers(method_find.method, json.dumps(method_sellers))
        if bool(data['country_id']):
            country_find = CountryRepository.get_by_id(data['country_id'])
            country_sellers = bitcoin_service.sell_bitcoins_country(country_find.name_alpha2, country_find.description)
            CacheService.set_buyers(country_find.name_alpha2, json.dumps(country_sellers))
        if bool(data['currency_id']):
            currency_find = CurrencyRepository.get_by_id(data['currency_id'])
            currency_sellers = bitcoin_service.sell_bitcoins_currency(currency_find.name.lower())
            CacheService.set_buyers(currency_find.name.lower(), json.dumps(currency_sellers))

    @staticmethod
    def stocks():
        stock_model = StockRepository()
        all_stocks = stock_model.get_stocks_with_volume_summary()
        return render_template("stocks.html", title='Market\'s list', stocks=all_stocks)

    @staticmethod
    def update_rates():
        exchange_service_model = ExchangeService()
        exchange_service_model.set_rates()
        session.clear()
        return redirect(url_for('stocks'))

    @staticmethod
    def exchange():
        countries = CountryRepository.get_all()
        methods = PaymentMethodRepository.get_all()
        return render_template('exchange.html', title='Exchange', countries=countries, methods=methods)

    @staticmethod
    def update_countries():
        test = ExchangeService()
        test.set_countries()
        test.set_payment_methods()
        test.set_payment_methods_by_country_codes()
        session.clear()
        return redirect(url_for('admin.index'))

    def login(self):
        if current_user.is_authenticated:
            return redirect('/')
        if request.method == "POST":
            form = LoginForm(request.form)
            if form.validate():
                login_user(form.user, remember=form.remember_me.data)
                return redirect('admin')
        else:
            form = LoginForm()
        return render_template("login.html", form=form)

    def logout(self):
        logout_user()
        return redirect('/')

    @staticmethod
    def test():
        model = StatisticService()
        model.set_statistic()
        return redirect(url_for('admin.index'))

    # api

    @staticmethod
    def get_token():
        model = Api()
        return model.get_token()

    @staticmethod
    def get_statistic():
        model = Api()
        return model.get_statistic()
