import json
import urllib3.request
import datetime
import time
from app import db
from app.dbmodels import CurrencyStatistic, CurrencyStatisticHistory, Currencies


class StatisticService:
    def set_statistic(self):
        url = 'https://api.coinmarketcap.com/v1/ticker/?limit=0'
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        response = request.data
        response = json.loads(response.decode('utf-8'))
        for currency in response:
            currency_model = Currencies.query.filter_by(name=currency['symbol']).first()
            if currency_model is None:
                new_currency = Currencies(name=currency['symbol'], slug=currency['symbol'].lower(),
                                          description=currency['name'])
                db.session.add(new_currency)
                db.session.commit()
            stat_to_update = CurrencyStatistic.query.filter_by(symbol=currency['symbol']).first()
            if stat_to_update is None:
                statistic_model = CurrencyStatistic(
                    symbol=currency['symbol'],
                    name=currency['name'],
                    rank=currency['rank'],
                    price_usd=currency['price_usd'],
                    price_btc=currency['price_btc'],
                    volume_usd_day=currency['24h_volume_usd'],
                    market_cap_usd=currency['market_cap_usd'],
                    percent_change_hour=currency['percent_change_1h'],
                    percent_change_day=currency['percent_change_24h'],
                    percent_change_week=currency['percent_change_7d'],
                    date=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                )
                db.session.add(statistic_model)
            else:
                stat_to_update.symbol = currency['symbol'],
                stat_to_update.name = currency['name'],
                stat_to_update.rank = currency['rank'],
                stat_to_update.price_usd = currency['price_usd'],
                stat_to_update.price_btc = currency['price_btc'],
                stat_to_update.volume_usd_day = currency['24h_volume_usd'],
                stat_to_update.market_cap_usd = currency['market_cap_usd'],
                stat_to_update.percent_change_hour = currency['percent_change_1h'],
                stat_to_update.percent_change_day = currency['percent_change_24h'],
                stat_to_update.percent_change_week = currency['percent_change_7d'],
                stat_to_update.date = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                db.session.add(stat_to_update)

            statistic_history_model = CurrencyStatisticHistory(
                symbol=currency['symbol'],
                name=currency['name'],
                rank=currency['rank'],
                price_usd=currency['price_usd'],
                price_btc=currency['price_btc'],
                volume_usd_day=currency['24h_volume_usd'],
                market_cap_usd=currency['market_cap_usd'],
                percent_change_hour=currency['percent_change_1h'],
                percent_change_day=currency['percent_change_24h'],
                percent_change_week=currency['percent_change_7d'],
                date=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            )
            db.session.add(statistic_history_model)
        db.session.commit()
