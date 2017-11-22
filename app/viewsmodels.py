from flask import render_template, redirect, request, url_for, session
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
from app.dbmodels import Currencies
from app.stocks.changelly import Changelly


class ViewsModels:
    def __init__(self):
        user_session = SessionService()
        user_session.set_count()

    def currencies(self, page, all_currencies):
        currency_repository = CurrencyRepository()
        stat_serv = StatisticService()
        if all_currencies == 'all':
            curr = Currencies()
            currencies = currency_repository.get_currencies_statistic_paginate(1, curr.count())
            all_pages = True
        else:
            currencies = currency_repository.get_currencies_statistic_paginate(page, 100)
            all_pages = False
        # for currency in currencies.items:
        #     currency.graph = stat_serv.create_graph_main(currency.symbol)
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

    def stocks(self):
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
