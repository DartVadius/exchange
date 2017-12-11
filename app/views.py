from app import app
from app.viewsmodels import ViewsModels


@app.route('/stock/<string:stock_slug>', methods=['GET'])
def stock(stock_slug):
    view = ViewsModels()
    return view.stock(stock_slug)


@app.route('/', methods=['GET'])
@app.route('/currencies', methods=['GET'])
@app.route('/currencies/<string:currency>', methods=['GET'])
@app.route('/currencies/<int:page>', methods=['GET'])
def stocks(page=1, currency=''):
    view = ViewsModels()
    return view.currencies(page, currency)


@app.route('/stocks', methods=['GET'])
def currencies():
    view = ViewsModels()
    return view.stocks()


@app.route('/update-rates', methods=['GET'])
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


@app.route("/update-countries", methods=['GET'])
def update_countries():
    view = ViewsModels()
    return view.update_countries()


@app.route("/exchange", methods=['GET'])
def exchange():
    view = ViewsModels()
    return view.exchange()


@app.route("/test", methods=['GET'])
def test():
    view = ViewsModels()
    return view.test()


@app.route('/api/v1.0/auth', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
def auth():
    view = ViewsModels()
    return view.get_token()


@app.route('/api/v1.0/statistic', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
# @app.route('/api/v1.0/statistic/<int:page>', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
# @app.route('/api/v1.0/statistic/<int:page>/<int:page_count>', methods=['POST', 'GET', 'PUT', 'DELETE', 'PATCH'])
def get_statistic():
    view = ViewsModels()
    return view.get_statistic()
