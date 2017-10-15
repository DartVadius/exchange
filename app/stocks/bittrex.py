from app.stocks.stock_base import StockBase
import time


class Bittrex(StockBase):
    STOCK_URL = 'https://bittrex.com'
    markets = []

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

    def set_markets(self):
        url = 'https://bittrex.com/api/v1.1/public/getmarketsummaries'
        response = self.get_request(url)
        if not response['success']:
            return False
        markets = []
        for market in response['result']:
            val = market['MarketName'].split('-')
            markets.append({
                'current_currency': val[0],
                'compare_currency': val[1],
                'date': time.time(),
                'high_price': market['High'],
                'low_price': market['Low'],
                'last_price': market['Last'],
                'volume': market['Volume'],
                'base_volume': market['BaseVolume'],
                'ask': market['Ask'],
                'bid': market['Bid']
            })
        self.markets = markets
        return self
