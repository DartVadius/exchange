import urllib3.request
import json


class StockBase:
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
