from app.stocks.stock_base import StockBase


class Bitfinex(StockBase):
    STOCK_URL = 'https://www.bitfinex.com'

    def __init__(self, stock=None):
        if stock is not None:
            self.id = stock.id
            self.name = stock.name
            self.url = stock.url
            self.api_key = stock.api_key
            self.api_secret = stock.api_secret

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.url!r}>'.format(self)

    def set_currencies(self):
        if self.url is None:
            return False
        url = self.STOCK_URL + '/api/v1.1/public/getcurrencies'
        response = self.get_request(url)
        if not response['success']:
            return False
        self.currencies = [currency['Currency'] for currency in response['result'] if currency['IsActive']]

    def set_markets(self):
        if self.url is None:
            return False
        url = self.STOCK_URL + '/api/v1.1/public/getmarketsummaries'
        response = self.get_request(url)
        if not response['success']:
            return False

        # if not response['success']:
        #     return False
        # self.currencies = [currency['Currency'] for currency in response['result'] if currency['IsActive']]

        print(response)
