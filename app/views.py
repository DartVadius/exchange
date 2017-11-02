from app import app
from app.viewsmodels import ViewsModels


@app.route('/stock/<string:stock_slug>', methods=['GET'])
def stock(stock_slug):
    view = ViewsModels()
    return view.stock(stock_slug)


@app.route('/', methods=['GET'])
def stocks():
    view = ViewsModels()
    return view.stocks()


@app.route('/update', methods=['GET'])
def update_rates():
    view = ViewsModels()
    return view.update_rates()


@app.route("/login", methods=["GET", "POST"])
def login():
    view = ViewsModels()
    return view.login()


@app.route("/logout")
def logout():
    view = ViewsModels()
    return view.logout()

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
