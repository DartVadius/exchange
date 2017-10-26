from flask import render_template, redirect, request, url_for

from app import app, forms
from app.database import db_session
from app.dbmodels import StockExchanges
from app.services import rate_repository, exchange_service, stock_repository


@app.route('/stock/<int:stock_id>', methods=['GET'])
def stock(stock_id):
    exchange_rates = rate_repository.get_rates_by_stock_id(stock_id)
    date = rate_repository.get_date_by_stock_id(stock_id)
    name = stock_repository.get_stock_name_by_id(stock_id)
    return render_template("stock_view/stock_exchange.html", title='Stocks', rates=exchange_rates, date=date, name=name)


@app.route('/', methods=['GET', 'POST'])
def stocks():
    form = forms.StockForm(request.form)
    all_stocks = db_session.query(StockExchanges).filter_by(active='1').all()
    return render_template("stocks.html", title='Stocks', form=form, stocks=all_stocks)


@app.route('/update', methods=['GET'])
def update_rates():
    exchange_service_model = exchange_service.ExchangeService()
    exchange_service_model.set_currencies()
    exchange_service_model.set_markets()
    return redirect(url_for('stocks'))

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
