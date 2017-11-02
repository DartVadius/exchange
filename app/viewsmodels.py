from flask import render_template, redirect, request, url_for, flash
from app import forms
from app.database import db_session
from app.dbmodels import StockExchanges
from app.services import exchange_service
from app.services.rate_repository import RateRepository
from app.services.stock_repository import StockRepository
from app.services.session_service import SessionService
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
        all_stocks = db_session.query(StockExchanges).filter_by(active='1').all()
        return render_template("stocks.html", title='Market\'s list', form=form, stocks=all_stocks)

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

# @app.route('/books')
# def index():
#     books = db_session.query(Book).all()
#     if 'username' in session:
#         return render_template("books.html",
#                                title='Home',
#                                books=books)
#     # print(books)
#     return redirect(url_for('login'))
#
#
# @app.route('/', methods=['GET', 'POST'])
# @app.route('/index', methods=['GET', 'POST'])
# def login():
#     form = forms.LoginForm(request.form)
#     if request.method == 'POST' and form.validate():
#         name = form.name.data
#         session['username'] = name
#         flash('Hi, ' + name + '!')
#         return redirect(url_for('index'))
#     return render_template('login.html',
#                            title='Sign In',
#                            form=form)
#
#
# @app.route('/odminko', methods=['GET', 'POST'])
# def odminko():
#     books = db_session.query(Book).all()
#     form = forms.Book(request.form)
#
#     if request.method == 'POST' and form.validate() and 'username' in session:
#         author = form.author.data
#         title = form.title.data
#         book = Book(author, title)
#         db_session.add(book)
#         db_session.commit()
#         return redirect(url_for('odminko'))
#
#     if 'username' in session:
#         return render_template("odminko.html",
#                                title='Odminko',
#                                books=books,
#                                form=form)
#     return redirect(url_for('login'))
#
#
# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('login'))
#
#
# @app.route('/kill', methods=['GET', 'POST'])
# def kill():
#     if request.method == "POST":
#         book_id = request.json
#         book = db_session.query(Book).filter_by(id=book_id).first()
#         db_session.delete(book)
#         db_session.commit()
#         return redirect(url_for('odminko'))
