import datetime
import time

from app.stocks.stock_base import StockBase


class BitcoinDe(StockBase):
    STOCK_URL = 'https://www.bitcoin.de/en'
    markets = []
    currencies = []

    def __init__(self, stock=None):
        self.name = 'bitcoin.de'
        self.url = 'https://www.bitcoin.de/en'
        if stock is not None:
            self.id = stock.id
            self.api_key = stock.api_key
            self.api_secret = stock.api_secret

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.url!r}>'.format(self)

    # def set_currencies(self):
    #     url = 'https://indacoin.com/api/ticker'
    #     response = self.get_request(url)
    #     if not response:
    #         return False
    #     currencies = []
    #     for currency in response:
    #         val = currency.split('_')
    #         currencies.append(val[0])
    #         currencies.append(val[1])
    #     filtered = set(currencies)
    #     self.currencies = list(filtered)
    #     return self
    #
    # def set_countries(self):
    #     return None
    #
    # def set_payment_methods(self):
    #     return None
    #
    # def set_payment_methods_for_country(self, country_code):
    #     return None
    #
    # def set_markets(self):
    #     markets = []
    #     url = 'https://indacoin.com/api/ticker'
    #     response = self.get_request(url)
    #     for market in response:
    #         val = market.split('_')
    #         if response[market]['last_price'] == '' or val[0] == 'LXC':
    #             continue
    #         if val[1] == 'BTC':
    #             btc_price = 1
    #         else:
    #             btc_price = response['BTC_USD']['last_price']
    #         markets.append({
    #             'base_currency': val[0],
    #             'compare_currency': val[1],
    #             'date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
    #             'high_price': 1 / float(response[market]['last_price']),
    #             'low_price': 1 / float(response[market]['last_price']),
    #             'last_price': 1 / float(response[market]['last_price']),
    #             'average_price': 1 / float(response[market]['last_price']),
    #             'btc_price': btc_price,
    #             'volume': 0,
    #             'base_volume': 0,
    #             'ask': 0,
    #             'bid': 0
    #         })
    #     self.markets = markets
    #     return self
