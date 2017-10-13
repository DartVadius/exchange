from app.dbmodels import StockExchanges


class Bittrex:
    STOCK_URL = 'https://bittrex.com'
    id = None
    name = None
    url = None
    api_key = None
    api_secret = None
    currencies = []

    def __init__(self):
        # stock = db_session.query(StockExchanges).filter_by(url=self.STOCK_URL).first()
        stock = StockExchanges()
        stock.id = '5555'
        stock.name = 'name'
        stock.url = 'https://bittrex.com'
        if stock is not None:
            # for attr in dir(stock):
            #     if not attr.startswith('__'):
            #         # setattr(self, attr, attr.)
            #         # self.attr = stock.attr
            #         print(attr)
            #         print(val)

            self.id = stock.id
            self.name = stock.name
            self.url = stock.url
            self.api_key = stock.api_key
            self.api_secret = stock.api_secret

    def __repr__(self):
        return '<Stock %r>' % (self.name)

    def get_currencies(self):
        if self.url is None:
            return False
