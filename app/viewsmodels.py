from flask import render_template, redirect, request, url_for, flash
from app import forms
from app.dbmodels import StockExchanges
from app.services import exchange_service
from app.services.rate_repository import RateRepository
from app.services.session_service import SessionService
from app.services.stock_repository import StockRepository
from app.forms import LoginForm
from flask_login import login_user, logout_user


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
        type = stock_repository.get_type_by_id(stock_id)
        if type == 'market':
            return render_template("stock_view/stock_market.html", title=name.title(), rates=exchange_rates,
                                   date=date, name=name.title())
        if type == 'exchange':
            return render_template("stock_view/stock_exchange.html", title=name.title(), rates=exchange_rates,
                                   date=date, name=name.title())

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

    def login(self):
        if request.method == "POST":
            form = LoginForm(request.form)
            if form.validate():
                login_user(form.user, remember=form.remember_me.data)
                flash("Successfully logged in as %s." % form.user.email, "success")
                return redirect(request.args.get("next") or url_for("stocks"))
        else:
            form = LoginForm()
        return render_template("login.html", form=form)

    def logout(self):
        logout_user()
        flash('You have been logged out.', 'success')
        return redirect(request.args.get('next') or url_for('stocks'))
