from flask import render_template, redirect, request, url_for
from app import forms
from app.dbmodels import StockExchanges
from app.services import exchange_service
from app.services.rate_repository import RateRepository
from app.services.session_service import SessionService
from app.services.stock_repository import StockRepository


class ViewsModels:
    def __init__(self):
        user_session = SessionService()
        user_session.set_count()

    def stock(self, stock_slug):
        rate_repository = RateRepository()
        stock_repository = StockRepository()
        stock_id = stock_repository.get_stock_id_by_slug(stock_slug)
        exchange_rates = rate_repository.get_rates_by_stock_id(stock_id)
        date = rate_repository.get_date_by_stock_id(stock_id)
        name = stock_repository.get_stock_name_by_id(stock_id)
        return render_template("stock_view/stock_exchange.html", title='Stocks', rates=exchange_rates, date=date,
                               name=name)

    def stocks(self):
        form = forms.StockForm(request.form)
        all_stocks = StockExchanges.query.filter_by(active='1').all()
        return render_template("stocks.html", title='Stocks', form=form, stocks=all_stocks)

    @staticmethod
    def update_rates():
        exchange_service_model = exchange_service.ExchangeService()
        exchange_service_model.set_currencies()
        exchange_service_model.set_markets()
        return redirect(url_for('stocks'))
