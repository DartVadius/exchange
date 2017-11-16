import json
import urllib3.request
from app.dbmodels import CurrencyStatistic
from app.dbmodels import CurrencyStatisticHistory


class StatisticService:
    def set_statistic(self):
        url = 'https://api.coinmarketcap.com/v1/ticker/'
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        response = request.data
        response = json.loads(response.decode('utf-8'))
        for currency in response:
            model = CurrencyStatistic()
            model_history = CurrencyStatisticHistory()
            print(currency)
