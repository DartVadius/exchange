import urllib.request
import json


class StockBase:
    currencies = []

    def get_request(self, url):
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request).read()
        response = json.loads(response.decode('utf-8'))
        return response

    def get_currencies(self):
        return self.currencies
