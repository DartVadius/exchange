import json
from abc import ABCMeta, abstractmethod

import urllib3.request


class StockBase:
    __metaclass__ = ABCMeta
    currencies = []
    markets = []

    def get_request(self, url):
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        response = request.data
        response = json.loads(response.decode('utf-8'))
        return response

    def get_currencies(self):
        return self.currencies

    def get_markets(self):
        return self.markets

    @abstractmethod
    def set_currencies(self):
        """Return list of site's available currencies"""
        """example ['BTC', 'USD']"""

    @abstractmethod
    def set_markets(self):
        """Return list of dictionaries with currencies rates"""
        """example [{
                'base_currency': 'USD',
                'compare_currency': 'BTC',
                'date': '2017-05-01 13:14:45',
                'high_price': '7000.464',
                'low_price': '7000.464',
                'last_price': '7000.464',
                'average_price': '7000.464',
                'btc_price': 1,
                'volume': 46446464565.46,
                'base_volume': None,
                'ask': None,
                'bid': None
                }, {
                    etc...
                }]"""


    @abstractmethod
    def set_countries(self):
        """Return list of available countries or None"""
        """example ['US', 'UA']"""

    @abstractmethod
    def set_payment_methods(self):
        """Return list of dictionaries with available payment methods or None"""

    @abstractmethod
    def set_payment_methods_for_country(self, country_code):
        """Return list of dictionaries with available payment methods for current country or None"""
