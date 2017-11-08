import datetime
import time

from app.stocks.stock_base import StockBase


class Bittrex(StockBase):
    STOCK_URL = 'https://bittrex.com'
    markets = []
    currencies = []

    def __init__(self, stock=None):
        self.name = 'bittrex'
        self.url = 'https://bittrex.com'
        if stock is not None:
            self.id = stock.id
            self.api_key = stock.api_key
            self.api_secret = stock.api_secret

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.url!r}>'.format(self)

    def set_currencies(self):
        url = 'https://bittrex.com/api/v1.1/public/getcurrencies'
        response = self.get_request(url)
        if not response['success']:
            return False
        self.currencies = [currency['Currency'].upper() for currency in response['result'] if currency['IsActive']]
        return self

    def set_countries(self):
        return None

    def set_payment_methods(self):
        return None

    def set_payment_methods_for_country(self, country_code):
        return None

    def set_markets(self):
        url = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'
        response = self.get_request(url)
        if not response['success']:
            return False
        markets = []
        for market in response['result']:
            val = market['MarketName'].split('-')
            btc = self.getByBaseCompareCurrency(response['result'], 'BTC', val[1])
            if btc is not None:
                btc_price = (float(btc['High']) + float(btc['Low'])) / 2.0
            else:
                btc_price = 1
            average_price = (float(market['High']) + float(market['Low'])) / 2.0
            markets.append({
                'base_currency': val[0],
                'compare_currency': val[1],
                'date': datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                'high_price': market['High'],
                'low_price': market['Low'],
                'last_price': market['Last'],
                'average_price': average_price,
                'btc_price': btc_price,
                'volume': market['Volume'],
                'base_volume': market['BaseVolume'],
                'ask': market['Ask'],
                'bid': market['Bid']
            })
        self.markets = markets
        return self

    def getByBaseCompareCurrency(self, list_of_dict, base_currency, compare_currency):
        for current_dict in list_of_dict:
            if current_dict['MarketName'] == base_currency + '-' + compare_currency:
                return current_dict
        return None
