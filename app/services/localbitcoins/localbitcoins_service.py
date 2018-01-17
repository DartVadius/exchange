import json
import pprint

import urllib3.request

from app.services.cache_service import CacheService


class LocalbitcoinsService:
    # buy/sell page of application

    @staticmethod
    def get_request(url):
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

    def sell_bitcoins_country(self, country_code, country_name):
        url = 'https://localbitcoins.com/sell-bitcoins-online/' + country_code + '/' + country_name + '/.json'
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

    def sell_bitcoins_method(self, payment_method):
        url = 'https://localbitcoins.com/sell-bitcoins-online/' + payment_method + '/.json'
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

    def sell_bitcoins_currency(self, currency):
        url = 'https://localbitcoins.com/sell-bitcoins-online/' + currency + '/.json'
        result = self.get_request(url)
        if 'pagination' in result:
            val = list()
            val.append(result)
            return self.recursive_data(result['pagination']['next'], val)
        return [result]

    def get_sellers(self, country_find, method_find, currency_find):
        country_sellers = None
        method_sellers = None
        currency_sellers = None
        if country_find is not None:
            cache = CacheService.get_sellers(country_find.name_alpha2)
            if cache is not None:
                country_sellers = json.loads(cache.data)
            else:
                country_sellers = self.buy_bitcoins_country(country_find.name_alpha2, country_find.description)
                CacheService.set_sellers(country_find.name_alpha2, json.dumps(country_sellers))

        if method_find is not None:
            cache = CacheService.get_sellers(method_find.method)
            if cache is not None:
                method_sellers = json.loads(cache.data)
            else:
                method_sellers = self.buy_bitcoins_method(method_find.method)
                CacheService.set_sellers(method_find.method, json.dumps(method_sellers))

        if currency_find is not None:
            cache = CacheService.get_sellers(currency_find.name.lower())
            if cache is not None:
                currency_sellers = json.loads(cache.data)
            else:
                currency_sellers = self.buy_bitcoins_currency(currency_find.name.lower())
                CacheService.set_sellers(currency_find.name.lower(), json.dumps(currency_sellers))
        return self.find_common_result(country_sellers,
                                       method_sellers,
                                       currency_sellers)

    def get_buyers(self, country_find, method_find, currency_find):
        country_buyers = None
        method_buyers = None
        currency_buyers = None
        if country_find is not None:
            cache = CacheService.get_buyers(country_find.name_alpha2)
            if cache is not None:
                country_buyers = json.loads(cache.data)
            else:
                country_buyers = self.sell_bitcoins_country(country_find.name_alpha2, country_find.description)
                CacheService.set_buyers(country_find.name_alpha2, json.dumps(country_buyers))

        if method_find is not None:
            cache = CacheService.get_buyers(method_find.method)
            if cache is not None:
                method_buyers = json.loads(cache.data)
            else:
                method_buyers = self.sell_bitcoins_method(method_find.method)
                CacheService.set_buyers(method_find.method, json.dumps(method_buyers))

        if currency_find is not None:
            cache = CacheService.get_buyers(currency_find.name.lower())
            if cache is not None:
                currency_buyers = json.loads(cache.data)
            else:
                currency_buyers = self.sell_bitcoins_currency(currency_find.name.lower())
                CacheService.set_buyers(currency_find.name.lower(), json.dumps(currency_buyers))

        return self.find_common_result(country_buyers,
                                       method_buyers,
                                       currency_buyers)

    def get_sellers_cash(self, lat, lng):
        url = 'https://localbitcoins.com/api/places/?lat=' + str(lat) + '&lon=' + str(lng)
        result = self.get_request(url)
        url = result['data']['places'][0]
        result = self.get_request(url['buy_local_url'])
        return self.get_sellers_dict([result])

    def get_users_cash_link(self, lat, lng):
        url = 'https://localbitcoins.com/api/places/?lat=' + str(lat) + '&lon=' + str(lng)
        result = self.get_request(url)
        url = result['data']['places'][0]
        return url

    def get_users_cash_list(self, url):
        result = self.get_request(url)
        return self.get_sellers_dict([result])

    def get_buyers_cash(self, lat, lng):
        url = 'https://localbitcoins.com/api/places/?lat=' + str(lat) + '&lon=' + str(lng)
        result = self.get_request(url)
        url = result['data']['places'][0]
        result = self.get_request(url['sell_local_url'])
        return self.get_sellers_dict([result])

    def find_common_result(self, country_sellers, method_sellers, currency_sellers):
        if country_sellers is None and method_sellers is None and currency_sellers is None:
            return None
        if country_sellers is not None and method_sellers is not None and currency_sellers is not None:
            return self.find_common_result_all(country_sellers, method_sellers, currency_sellers)
        if country_sellers is not None and method_sellers is not None:
            return self.find_common_result_two_list(country_sellers, method_sellers)
        if country_sellers is not None and currency_sellers is not None:
            return self.find_common_result_two_list(country_sellers, currency_sellers)
        if method_sellers is not None and currency_sellers is not None:
            return self.find_common_result_two_list(method_sellers, currency_sellers)
        if method_sellers is not None:
            return self.get_sellers_dict(method_sellers)
        if country_sellers is not None:
            return self.get_sellers_dict(country_sellers)
        if currency_sellers is not None:
            return self.get_sellers_dict(currency_sellers)
        return None

    def find_common_result_two_list(self, list_one, list_two):
        res_one = self.get_sellers_dict(list_one)
        one_set = set(res_one)
        res_two = self.get_sellers_dict(list_two)
        two_set = set(res_two)
        tmp_list = dict()
        for name in one_set.intersection(two_set):
            tmp_list.update({name: res_one[name]})
        if bool(tmp_list) is not True:
            return None
        return tmp_list

    def find_common_result_all(self, country_sellers, method_sellers, currency_sellers):
        res_country = self.get_sellers_dict(country_sellers)
        country_set = set(res_country)
        res_method = self.get_sellers_dict(method_sellers)
        method_set = set(res_method)
        res_currency = self.get_sellers_dict(currency_sellers)
        currency_set = set(res_currency)
        tmp_set = set()
        for name in country_set.intersection(method_set):
            tmp_set.add(name)
        if bool(tmp_set) is not True:
            return None
        tmp_list = dict()
        for name in tmp_set.intersection(currency_set):
            tmp_list.update({name: res_method[name]})
        if bool(tmp_list) is not True:
            return None
        return tmp_list

    @staticmethod
    def get_sellers_dict(sellers):
        resp_dict = dict()
        print(sellers)
        for value in sellers:
            if isinstance(value, list):
                sellers_loc = [value[0]]
            else:
                sellers_loc = value['data']['ad_list']
            sellers_dict = {value['data']['ad_id']: value['data']['profile'] for value in sellers_loc}
            resp_dict.update(sellers_dict)
        return resp_dict

    def recursive_data(self, url, val):
        result = self.get_request(url)
        val.append(result)
        CacheService.set_buyers('tmp', '1')
        CacheService.set_sellers('tmp', '1')
        if 'pagination' in result and 'next' in result['pagination']:
            self.recursive_data(result['pagination']['next'], val)
        return val
