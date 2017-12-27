import datetime
import time

from app.stocks.stock_base import StockBase


class Shapeshift(StockBase):
    STOCK_URL = 'https://shapeshift.io/'
    markets = []
    currencies = []

    def __init__(self, stock=None):
        self.name = 'shapeshift'
        self.url = 'https://shapeshift.io/'
        if stock is not None:
            self.id = stock.id
            self.api_key = stock.api_key
            self.api_secret = stock.api_secret

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.url!r}>'.format(self)

    def set_currencies(self):
        url = 'https://shapeshift.io/getcoins'
        response = self.get_request(url)
        if not response:
            return False
        self.currencies = [response[currency]['symbol'] for currency in response if
                           response[currency]['status'] == 'available']
        return self

    def set_countries(self):
        return None

    def set_payment_methods(self):
        return None

    def set_payment_methods_for_country(self, country_code):
        return None

    def set_markets(self):
        markets = []
        url = 'https://shapeshift.io/rate/'
        for currency in self.currencies:
            if currency == 'BTC':
                continue
            new_url = url + currency.lower() + '_btc'
            response = self.get_request(new_url)
            if 'error' in response:
                continue
            markets.append({
                'base_currency': 'BTC',
                'compare_currency': currency,
                'date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                'high_price': float(response['rate']),
                'low_price': float(response['rate']),
                'last_price': float(response['rate']),
                'average_price': float(response['rate']),
                'btc_price': float(response['rate']),
                'volume': 0,
                'base_volume': 0,
                'ask': 0,
                'bid': 0
            })
        self.markets = markets
        return self
