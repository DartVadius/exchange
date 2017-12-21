import json

import urllib3.request


class LocalbitcoinsService:
    def get_request(self, url):
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        response = request.data
        response = json.loads(response.decode('utf-8'))
        return response

    def buy_bitcoins_country(self, country_code, country_name):
        url = 'https://localbitcoins.com/buy-bitcoins-online/' + country_code + '/' + country_name + '/.json'
        return self.get_request(url)
