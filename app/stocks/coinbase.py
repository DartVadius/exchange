import datetime
import time

from app.stocks.stock_base import StockBase


class Coinbase(StockBase):
    STOCK_URL = 'https://www.coinbase.com/'
    markets = []
    currencies = []

    def __init__(self, stock=None):
        self.name = 'coinbase'
        self.url = 'https://www.coinbase.com/'
        if stock is not None:
            self.id = stock.id
            self.api_key = stock.api_key
            self.api_secret = stock.api_secret

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.url!r}>'.format(self)

    def set_currencies(self):
        url = 'https://api.coinbase.com/v2/currencies'
        response = self.get_request(url)
        if response['errors']:
            return False
        self.currencies = [currency['id'].upper() for currency in response['data']]
        return self

    def set_countries(self):
        return None

    def set_payment_methods(self):
        return None

    def set_payment_methods_for_country(self, country_code):
        return None

    def set_markets(self):
        markets = []
        url = 'https://api.coinbase.com/v2/exchange-rates?currency=BTC'
        response_btc = self.get_request(url)
        if not response_btc['data']:
            return False

        for market in response_btc['data']['rates']:
            if market == 'BTC':
                continue
            if response_btc['data']['rates'][market] == 0:
                continue
            markets.append({
                'base_currency': 'BTC',
                'compare_currency': market,
                'date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                'high_price': 1 / float(response_btc['data']['rates'][market]),
                'low_price': 1 / float(response_btc['data']['rates'][market]),
                'last_price': 1 / float(response_btc['data']['rates'][market]),
                'average_price': 1 / float(response_btc['data']['rates'][market]),
                'btc_price': 1 / float(response_btc['data']['rates'][market]),
                'volume': 0,
                'base_volume': 0,
                'ask': 0,
                'bid': 0
            })

        url = 'https://api.coinbase.com/v2/exchange-rates'
        response_usd = self.get_request(url)
        if not response_usd['data']:
            return False

        for market in response_usd['data']['rates']:
            if market == 'USD':
                continue
            if float(response_usd['data']['rates'][market]) == 0:
                continue
            markets.append({
                'base_currency': 'USD',
                'compare_currency': market,
                'date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                'high_price': 1 / float(response_usd['data']['rates'][market]),
                'low_price': 1 / float(response_usd['data']['rates'][market]),
                'last_price': 1 / float(response_usd['data']['rates'][market]),
                'average_price': 1 / float(response_usd['data']['rates'][market]),
                'btc_price': 1 / float(response_btc['data']['rates'][market]),
                'volume': 0,
                'base_volume': 0,
                'ask': 0,
                'bid': 0
            })

        currencies = ['ETH', 'LTC']
        for currency in currencies:
            url_tmp = 'https://api.coinbase.com/v2/exchange-rates?currency=' + currency
            response_tmp = self.get_request(url_tmp)
            if not response_tmp['data']:
                continue

            for market in response_usd['data']['rates']:
                if market == currency:
                    continue
                if float(response_tmp['data']['rates'][market]) == 0:
                    continue
                markets.append({
                    'base_currency': currency,
                    'compare_currency': market,
                    'date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                    'high_price': 1 / float(response_tmp['data']['rates'][market]),
                    'low_price': 1 / float(response_tmp['data']['rates'][market]),
                    'last_price': 1 / float(response_tmp['data']['rates'][market]),
                    'average_price': 1 / float(response_tmp['data']['rates'][market]),
                    'btc_price': 1 / float(response_btc['data']['rates'][market]),
                    'volume': 0,
                    'base_volume': 0,
                    'ask': 0,
                    'bid': 0
                })
        self.markets = markets
        return self
