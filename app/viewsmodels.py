from flask import render_template, redirect, request, url_for, session, make_response, abort, jsonify
from flask_login import login_user, logout_user, current_user

from app.forms import LoginForm
from app.services.exchange_service import ExchangeService
from app.services.rate_repository import RateRepository
from app.services.session_service import SessionService
from app.services.stock_repository import StockRepository
from app.services.currency_repository import CurrencyRepository
from app.services.country_repository import CountryRepository
from app.services.payment_method_repository import PaymentMethodRepository
from app.services.statistic_service import StatisticService
from app.services.localbitcoins.localbitcoins_service import LocalbitcoinsService
from app.dbmodels import CurrencyStatistic, Countries, PaymentMethods
from app.apiV10 import Api
from app.stocks.changelly import Changelly
import datetime
import time


class ViewsModels:
    def __init__(self):
        user_session = SessionService()
        user_session.set_count()

    def currencies(self, page, currency):
        currency_repository = CurrencyRepository()
        statistic_service = StatisticService()
        if currency != 'all' and currency != '':
            rate_repository = RateRepository()
            currency_data = rate_repository.get_currency_rates_by_name(currency)
            date_end = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            date_start = datetime.date.today() + datetime.timedelta(days=-7)
            date_start = date_start.strftime('%Y-%m-%d %H:%M:%S')
            graph = statistic_service.create_graph_strait(currency, date_start, date_end)
            return render_template("currency.html", title=currency.upper(), currency_data=currency_data, graph=graph)
        if currency == 'all':
            curr = CurrencyStatistic()
            currencies = currency_repository.get_currencies_statistic_paginate(1, curr.count())
            all_pages = True
        if currency == '':
            currencies = currency_repository.get_currencies_statistic_paginate(page, 100)
            all_pages = False
        return render_template("currencies.html", title='Currencies', currencies=currencies, all=all_pages)

    def stock(self, stock_slug):
        rate_repository = RateRepository()
        stock_repository = StockRepository()
        stock_id = stock_repository.get_stock_id_by_slug(stock_slug)
        exchange_rates = rate_repository.get_rates_by_stock_id(stock_id)
        date = rate_repository.get_date_by_stock_id(stock_id)
        name = stock_repository.get_stock_name_by_id(stock_id)
        return render_template("stock_view/stock_exchange.html", title=name.title(), rates=exchange_rates,
                               date=date, name=name.title())

    def buy_btc(self):
        country = CountryRepository()
        methods = PaymentMethodRepository()
        currency = CurrencyRepository()
        countries = country.get_all()
        payment_methods = methods.get_all()
        currencies = currency.get_fiat_currencies()
        return render_template("buy_currency.html", title='Buy Bitcoin', data=countries, methods=payment_methods,
                               currencies=currencies)

    def get_payment_method(self):
        country_id = request.json
        country_find = Countries.query.filter(Countries.id == country_id).one()
        h = []
        for method_x in country_find.method_country:
            h.append({method_x.id: method_x.name})
        return jsonify(h)

    def get_sellers(self):
        model = LocalbitcoinsService()
        data = request.json
        country_find = CountryRepository.get_by_id(data['country_id'])
        method_find = PaymentMethodRepository.get_by_id(data['payment_method_id'])
        currency_find = CurrencyRepository.get_by_id(data['currency_id'])
        country_sellers = None
        method_sellers = None
        currency_sellers = None
        if country_find is not None:
            country_sellers = model.buy_bitcoins_country(country_find.name_alpha2, country_find.description)
            # print(country_sellers)
        if method_find is not None:
            method_sellers = model.buy_bitcoins_method(method_find.method)
        if currency_find is not None:
            currency_sellers = model.buy_bitcoins_currency(currency_find.name.lower())
        common_sellers = model.find_common_sellers(country_sellers,
                                                   method_sellers,
                                                   currency_sellers)
        return jsonify('s')

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
        # model.create_graph('BTC')
        model.set_statistic()
        # model.set_markets()
        # model.set_markets()
        # print(model.set_markets())
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
