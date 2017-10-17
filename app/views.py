from flask import render_template, flash, redirect, request, url_for, session

from app import app
from app import forms
from app.database import db_session
from app.dbmodels import Book, StockExchanges, ExchangeRates, Currencies


@app.route('/stock/<int:stock_id>', methods=['GET'])
def stock(stock_id):
    # stock_id = request.form['id']
    exchange_rates = db_session.query(ExchangeRates, StockExchanges).filter_by(stock_exchange_id=stock_id).join(
        StockExchanges).add_columns(StockExchanges.name).join(
        Currencies, ExchangeRates.compare_currency_id == Currencies.id).add_columns(Currencies.name).all()
    for name in exchange_rates:
        print(name.name)
    return render_template("stock_view/stock_exchange.html", title='Stocks', rates=exchange_rates)


@app.route('/stocks', methods=['GET', 'POST'])
def stocks():
    form = forms.StockForm(request.form)
    stocks = db_session.query(StockExchanges).all()
    if request.method == 'POST' and form.validate():
        name = form.name.data
        url = form.url.data
        api_key = form.api_key.data
        api_secret = form.api_secret.data
        exchange_stock = StockExchanges(name.lower(), url, api_key, api_secret)
        db_session.add(exchange_stock)
        db_session.commit()
        return redirect(url_for('stocks'))
    return render_template("stocks.html", title='Stocks', form=form, stocks=stocks)


@app.route('/books')
def index():
    books = db_session.query(Book).all()
    if 'username' in session:
        return render_template("books.html",
                               title='Home',
                               books=books)
    # print(books)
    return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        session['username'] = name
        flash('Hi, ' + name + '!')
        return redirect(url_for('index'))
    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/odminko', methods=['GET', 'POST'])
def odminko():
    books = db_session.query(Book).all()
    form = forms.Book(request.form)

    if request.method == 'POST' and form.validate() and 'username' in session:
        author = form.author.data
        title = form.title.data
        book = Book(author, title)
        db_session.add(book)
        db_session.commit()
        return redirect(url_for('odminko'))

    if 'username' in session:
        return render_template("odminko.html",
                               title='Odminko',
                               books=books,
                               form=form)
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/kill', methods=['GET', 'POST'])
def kill():
    if request.method == "POST":
        book_id = request.json
        book = db_session.query(Book).filter_by(id=book_id).first()
        db_session.delete(book)
        db_session.commit()
        return redirect(url_for('odminko'))
