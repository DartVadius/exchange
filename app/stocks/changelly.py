import datetime
import hashlib
import hmac
import json
import time

import urllib3.request

from app.stocks.stock_base import StockBase


class Changelly(StockBase):
    STOCK_URL = 'https://changelly.com/'
    API_KEY = 'b67925c2f53647af9f837f43e851047c'
    API_SECRET = 'b4598e2136e8c893074374d9101a7e2ed07495c79ebf7970c938c46b17608ee7'
    markets = []
    currencies = []

    def __init__(self, stock=None):
        self.name = 'changelly'
        self.url = 'https://changelly.com/'
        if stock is not None:
            self.id = stock.id
            self.api_key = stock.api_key
            self.api_secret = stock.api_secret

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.url!r}>'.format(self)

    def get_request(self, method):
        http = urllib3.PoolManager()
        data = {"id": "test", "jsonrpc": "2.0", "method": method, "params": {}}
        data = json.dumps(data)
        sign = hmac.new(self.API_SECRET.encode('utf-8'), data.encode('utf-8'), hashlib.sha512).hexdigest()
        headers = {'api-key': self.API_KEY, 'sign': sign, 'content-type': 'application/json'}
        request = http.request('POST', 'http://api.changelly.com', body=data, headers=headers)
        response = request.data
        response = json.loads(response.decode('utf-8'))
        return response

    def set_currencies(self):
        response = self.get_request('getCurrenciesFull')
        if not response['result']:
            return False
        currencies = []
        for currency in response['result']:
            if not currency['enabled']:
                continue
            currencies.append(currency['name'].upper())
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
        url = 'https://indacoin.com/api/ticker'
        response = self.get_request(url)
        for market in response:
            val = market.split('_')
            if response[market]['last_price'] == '' or val[0] == 'LXC':
                continue
            if val[1] == 'BTC':
                btc_price = 1
            else:
                btc_price = response['BTC_USD']['last_price']
            markets.append({
                'base_currency': val[0],
                'compare_currency': val[1],
                'date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                'high_price': 1 / float(response[market]['last_price']),
                'low_price': 1 / float(response[market]['last_price']),
                'last_price': 1 / float(response[market]['last_price']),
                'average_price': 1 / float(response[market]['last_price']),
                'btc_price': 1 / float(btc_price),
                'volume': 0,
                'base_volume': 0,
                'ask': 0,
                'bid': 0
            })
        self.markets = markets
        return self
