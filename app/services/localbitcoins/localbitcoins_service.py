import json

import urllib3.request


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
        if country_sellers is None and method_sellers is None and currency_sellers is None:
            return None
        if country_sellers is not None and method_sellers is not None and currency_sellers is not None:
            return self.find_common_sellers_all(country_sellers, method_sellers, currency_sellers)
        if country_sellers is not None and method_sellers is not None:
            return self.find_common_sellers_two_list(country_sellers, method_sellers)
        if country_sellers is not None and currency_sellers is not None:
            return self.find_common_sellers_two_list(country_sellers, currency_sellers)
        if method_sellers is not None and currency_sellers is not None:
            return self.find_common_sellers_two_list(method_sellers, currency_sellers)
        if method_sellers is not None:
            return self.get_sellers_dict(method_sellers)
        if country_sellers is not None:
            return self.get_sellers_dict(country_sellers)
        if currency_sellers is not None:
            return self.get_sellers_dict(currency_sellers)
        return None

    def find_common_sellers_two_list(self, list_one, list_two):
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

    def find_common_sellers_all(self, country_sellers, method_sellers, currency_sellers):
        # find intersecting for 3 arguments
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
        for value in sellers:
            sellers_loc = value['data']['ad_list']
            sellers_dict = {value['data']['ad_id']: value['data']['profile'] for value in sellers_loc}
            resp_dict.update(sellers_dict)
        return resp_dict

    def recursive_data(self, url, val):
        result = self.get_request(url)
        val.append(result)
        if 'pagination' in result and 'next' in result['pagination']:
            self.recursive_data(result['pagination']['next'], val)
        return val
