from app.stocks.stock_base import StockBase
import time
import datetime
import sys


class Localbitcoins(StockBase):
    STOCK_URL = 'https://localbitcoins.com/'
    markets = []
    currencies = []

    def __init__(self, stock=None):
        self.name = 'localbitcoins'
        self.url = 'https://localbitcoins.com/'
        if stock is not None:
            self.id = stock.id
            self.api_key = stock.api_key
            self.api_secret = stock.api_secret

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.url!r}>'.format(self)

    def set_currencies(self):
        url = 'https://localbitcoins.com/api/currencies/'
        response = self.get_request(url)
        if not response['data']:
            return False
        self.currencies = [currency for currency in response['data']['currencies']]
        return self

    def set_markets(self):
        url = 'https://localbitcoins.com/bitcoinaverage/ticker-all-currencies/'
        response = self.get_request(url)
        if not response:
            return False
        markets = []
        for market in response:
            val = response[market]
            markets.append({
                'base_currency': market,
                'compare_currency': 'BTC',
                'date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                'high_price': val['avg_24h'],
                'low_price': val['avg_24h'],
                'last_price': val['rates']['last'],
                'average_price': val['avg_24h'],
                'btc_price': 1,
                'volume': val['volume_btc'],
                'base_volume': None,
                'ask': None,
                'bid': None
            })
        self.markets = markets
        return self
