import datetime
import time

from app.stocks.stock_base import StockBase


class Spectrocoin(StockBase):
    STOCK_URL = 'https://spectrocoin.com/'
    markets = []
    currencies = []

    def __init__(self, stock=None):
        self.name = 'spectrocoin'
        self.url = 'https://spectrocoin.com/'
        if stock is not None:
            self.id = stock.id
            self.api_key = stock.api_key
            self.api_secret = stock.api_secret

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.url!r}>'.format(self)

    def set_currencies(self):
        currencies = ['USD', 'EUR', 'GBP', 'UAH']
        self.currencies = currencies
        return self

    def set_countries(self):
        return None

    def set_payment_methods(self):
        return None

    def set_payment_methods_for_country(self, country_code):
        return None

    def set_markets(self):
        markets = []
        url = 'https://spectrocoin.com/scapi/ticker/BTC/'
        for currency in self.currencies:

            new_url = url + currency
            response = self.get_request(new_url)
            markets.append({
                'base_currency': 'BTC',
                'compare_currency': currency,
                'date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                'high_price': float(response['last']),
                'low_price': float(response['last']),
                'last_price': float(response['last']),
                'average_price': float(response['last']),
                'btc_price': float(response['last']),
                'volume': 0,
                'base_volume': 0,
                'ask': 0,
                'bid': 0
            })
        self.markets = markets
        return self
