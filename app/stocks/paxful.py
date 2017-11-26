import datetime
import json
import time
from urllib import parse
from hashlib import sha256

import urllib3.request

from app.stocks.stock_base import StockBase


class Paxful(StockBase):
    STOCK_URL = 'https://paxful.com/'
    markets = []
    currencies = []
    key = 'HEjnCYnypvQkvzH6-u5qMrHeTkKh87LI'
    secret = 'F5LBsYIQRGQRFO5FNUN1hyGFbeHmrH8R'

    def __init__(self, stock=None):
        self.name = 'paxful'
        self.url = 'https://paxful.com/'
        if stock is not None:
            self.id = stock.id
            self.api_key = stock.api_key
            self.api_secret = stock.api_secret

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.url!r}>'.format(self)

    def set_currencies(self):
        http = urllib3.PoolManager()
        url = 'https://paxful.com/api/currency/rates'
        headers = {'Accept': 'application/json', 'Content-Type': 'text/plain'}
        request = http.request('POST', url, headers=headers)
        response = request.data
        response = json.loads(response.decode('utf-8'))
        if not response['status'] or response['status'] != 'success':
            return False
        currencies = []
        for rate in response['data']:
            if rate['rate_USD'] == 0 or rate['rate_BTC'] == 0:
                continue
            currencies.append(rate['code'].upper())
        filtered = set(currencies)
        self.currencies = list(filtered)
        return self

    def set_countries(self):
        return None

    def set_payment_methods(self):
        return None

    def set_payment_methods_for_country(self, country_code):
        return None

    def set_markets(self):
        markets = []
        http = urllib3.PoolManager()
        url = 'https://paxful.com/api/currency/rates'
        headers = {'Accept': 'application/json', 'Content-Type': 'text/plain'}
        request = http.request('POST', url, headers=headers)
        response = request.data
        response = json.loads(response.decode('utf-8'))
        if not response['status'] or response['status'] != 'success':
            return False
        for rate in response['data']:
            if rate['rate_USD'] == 0 or rate['rate_BTC'] == 0:
                continue
            markets.append({
                'base_currency': 'BTC',
                'compare_currency': rate['code'],
                'date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                'high_price': 1 / float(rate['rate_BTC']),
                'low_price': 1 / float(rate['rate_BTC']),
                'last_price': 1 / float(rate['rate_BTC']),
                'average_price': 1 / float(rate['rate_BTC']),
                'btc_price': 1 / float(rate['rate_BTC']),
                'volume': 0,
                'base_volume': 0,
                'ask': 0,
                'bid': 0
            })
        self.markets = markets
        return self
