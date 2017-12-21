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
        result = self.get_request(url)
        if 'pagination' in result:
            val = list()
            val.append(result)
            return self.recursive_data(result['pagination']['next'], val)
        return [result]

    def buy_bitcoins_method(self, payment_method):
        url = 'https://localbitcoins.com/buy-bitcoins-online/' + payment_method + '/.json'
        result = self.get_request(url)
        if 'pagination' in result:
            val = list()
            val.append(result)
            return self.recursive_data(result['pagination']['next'], val)
        return [result]

    def buy_bitcoins_currency(self, currency):
        url = 'https://localbitcoins.com/buy-bitcoins-online/' + currency + '/.json'
        result = self.get_request(url)
        if 'pagination' in result:
            val = list()
            val.append(result)
            return self.recursive_data(result['pagination']['next'], val)
        return [result]

    def find_common_sellers(self, country_sellers, method_sellers, currency_sellers):
        res_country = dict()
        res_method = dict()
        res_currency = dict()
        if country_sellers is not None:
            for value in country_sellers:
                country_sellers_loc = value['data']['ad_list']
                country_dict = {value['data']['ad_id']: value['data']['profile'] for value in country_sellers_loc}
                res_country.update(country_dict)
            country_set = set(res_country)

        if method_sellers is not None:
            for value in method_sellers:
                method_sellers_loc = value['data']['ad_list']
                method_dict = {value['data']['ad_id']: value['data']['profile'] for value in method_sellers_loc}
                res_method.update(method_dict)
            method_set = set(res_method)

        if currency_sellers is not None:
            for value in method_sellers:
                currency_sellers_loc = value['data']['ad_list']
                currency_dict = {value['data']['ad_id']: value['data']['profile'] for value in currency_sellers_loc}
                res_currency.update(currency_dict)
            currency_set = set(res_currency)

        for name in country_set.intersection(method_set):
            print(res_method[name])

        # print(country_set)
        # print(method_set)
        # print(currency_set)

    def recursive_data(self, url, val=[]):
        result = self.get_request(url)
        val.append(result)
        if 'pagination' in result and 'next' in result['pagination']:
            self.recursive_data(result['pagination']['next'], val)
        return val
