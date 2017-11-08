from flask import render_template, redirect, request, url_for
from flask_login import login_user, logout_user, current_user

from app.forms import LoginForm
from app.services.exchange_service import ExchangeService
from app.services.rate_repository import RateRepository
from app.services.session_service import SessionService
from app.services.stock_repository import StockRepository
from app.services.currency_repository import CurrencyRepository


class ViewsModels:
    def __init__(self):
        user_session = SessionService()
        user_session.set_count()

    def currencies(self):
        currency_repository = CurrencyRepository()
        currencies = currency_repository.get_currencies_with_btc_volume()
        return render_template("currencies.html", title='Currencies', currencies=currencies)


    def stock(self, stock_slug):
        rate_repository = RateRepository()
        stock_repository = StockRepository()
        stock_id = stock_repository.get_stock_id_by_slug(stock_slug)
        exchange_rates = rate_repository.get_rates_by_stock_id(stock_id)
        date = rate_repository.get_date_by_stock_id(stock_id)
        name = stock_repository.get_stock_name_by_id(stock_id)
        # market_type = stock_repository.get_type_by_id(stock_id)
        # if market_type == 'market':
        #     return render_template("stock_view/stock_market.html", title=name.title(), rates=exchange_rates,
        #                            date=date, name=name.title())
        # if market_type == 'exchange':
        return render_template("stock_view/stock_exchange.html", title=name.title(), rates=exchange_rates,
                               date=date, name=name.title())

    def stocks(self):
        stock_model = StockRepository()
        all_stocks = stock_model.get_stocks_with_volume_summary()
        # all_stocks = StockExchanges.query.filter_by(active='1').all()
        return render_template("stocks.html", title='Market\'s list', stocks=all_stocks)

    @staticmethod
    def update_rates():
        exchange_service_model = ExchangeService()
        exchange_service_model.set_currencies()
        exchange_service_model.set_markets()
        return redirect(url_for('stocks'))

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
