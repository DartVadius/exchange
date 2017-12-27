import datetime
import hashlib
import hmac
import json
import time

import urllib3.request

from app.stocks.stock_base import StockBase


class Changelly(StockBase):
    STOCK_URL = 'https://changelly.com/'
    # API_KEY = 'b67925c2f53647af9f837f43e851047c'
    # API_SECRET = 'b4598e2136e8c893074374d9101a7e2ed07495c79ebf7970c938c46b17608ee7'
    API_KEY = ''
    API_SECRET = ''
    markets = []
    currencies = []

    def __init__(self, stock=None):
        self.name = 'changelly'
        self.url = 'https://changelly.com/'
        if stock is not None:
            self.id = stock.id
            self.API_KEY = stock.api_key
            self.API_SECRET = stock.api_secret

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.url!r}>'.format(self)

    def set_currencies(self):
        http = urllib3.PoolManager()
        data = {"id": "test", "jsonrpc": "2.0", "method": 'getCurrenciesFull', "params": {}}
        data = json.dumps(data)
        sign = hmac.new(self.API_SECRET.encode('utf-8'), data.encode('utf-8'), hashlib.sha512).hexdigest()
        headers = {'api-key': self.API_KEY, 'sign': sign, 'content-type': 'application/json'}
        request = http.request('POST', 'http://api.changelly.com', body=data, headers=headers)
        response = request.data
        response = json.loads(response.decode('utf-8'))
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
        data_currency = []
        for currency in self.currencies:
            data_currency.append({"from": currency, "to": "btc", "amount": "1"})
        http = urllib3.PoolManager()
        for params in data_currency:
            data = {"id": "test", "jsonrpc": "2.0", "method": 'getExchangeAmount', "params": params}
            data = json.dumps(data)
            sign = hmac.new(self.API_SECRET.encode('utf-8'), data.encode('utf-8'), hashlib.sha512).hexdigest()
            headers = {'api-key': self.API_KEY, 'sign': sign, 'content-type': 'application/json'}
            request = http.request('POST', 'http://api.changelly.com', body=data, headers=headers)
            response = request.data
            response = json.loads(response.decode('utf-8'))
            markets.append({
                'base_currency': 'BTC',
                'compare_currency': params['from'],
                'date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                'high_price': float(response['result']),
                'low_price': float(response['result']),
                'last_price': float(response['result']),
                'average_price': float(response['result']),
                'btc_price': float(response['result']),
                'volume': 0,
                'base_volume': 0,
                'ask': 0,
                'bid': 0
            })
        # print(markets)
        self.markets = markets
        return self
