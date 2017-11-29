import json
import pygal
from pygal.style import LightStyle
import urllib3.request
import datetime
import time
from app import db
from app.dbmodels import CurrencyStatistic, CurrencyStatisticHistory, Currencies
from sqlalchemy import and_


class StatisticService:
    def set_statistic(self):
        url = 'https://api.coinmarketcap.com/v1/ticker/?limit=0'
        http = urllib3.PoolManager()
        request = http.request('GET', url)
        response = request.data
        response = json.loads(response.decode('utf-8'))
        date_end = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        for currency in response:
            currency_model = Currencies.query.filter_by(name=currency['symbol']).first()
            if currency_model is None:
                continue
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
                    available_supply=currency['available_supply'],
                    total_supply=currency['total_supply'],
                    max_supply=currency['max_supply'],
                    date=date_end
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
                stat_to_update.available_supply = currency['available_supply'],
                stat_to_update.total_supply = currency['total_supply'],
                stat_to_update.max_supply = currency['max_supply'],
                stat_to_update.date = date_end
                db.session.add(stat_to_update)
        db.session.commit()
        statistic = CurrencyStatistic.query.order_by(CurrencyStatistic.rank).all()
        rank = 1
        for statistic_item in statistic:
            statistic_item.rank = rank
            db.session.add(statistic_item)
            statistic_history_model = CurrencyStatisticHistory(
                symbol=statistic_item.symbol,
                name=statistic_item.name,
                rank=statistic_item.rank,
                price_usd=statistic_item.price_usd,
                price_btc=statistic_item.price_btc,
                volume_usd_day=statistic_item.volume_usd_day,
                market_cap_usd=statistic_item.market_cap_usd,
                percent_change_hour=statistic_item.percent_change_hour,
                percent_change_day=statistic_item.percent_change_day,
                percent_change_week=statistic_item.percent_change_week,
                available_supply=statistic_item.available_supply,
                total_supply=statistic_item.total_supply,
                max_supply=statistic_item.max_supply,
                date=date_end
            )
            db.session.add(statistic_history_model)
            rank += 1
        db.session.commit()
        date_start = datetime.date.today() + datetime.timedelta(days=-7)
        date_start = date_start.strftime('%Y-%m-%d %H:%M:%S')
        for statistic_item in statistic:
            self.create_graph_main(statistic_item.symbol, date_start, date_end)

    def create_graph_main(self, symbol, start=None, end=None):
        if start is not None and end is not None:
            stats = CurrencyStatisticHistory.query.filter_by(symbol=symbol).filter(
                and_(CurrencyStatisticHistory.date >= start, CurrencyStatisticHistory.date <= end)
            ).all()
        else:
            stats = CurrencyStatisticHistory.query.filter_by(symbol=symbol).all()
        prices = [float(stat.price_usd) for stat in stats]
        # times = ['%s' % stat.date for stat in stats]
        bar_chart = pygal.Line(show_legend=False, show_y_labels=False, width=166, height=100, explicit_size=True,
                               show_dots=False, style=LightStyle)
        bar_chart.add('USD', prices)
        bar_chart.render_to_png('app/static/img/graphs/' + symbol + '.png')

    def create_graph_strait(self, symbol, start=None, end=None):
        if start is not None and end is not None:
            stats = CurrencyStatisticHistory.query.filter_by(symbol=symbol).filter(
                and_(CurrencyStatisticHistory.date >= start, CurrencyStatisticHistory.date <= end)
            ).all()
        else:
            stats = CurrencyStatisticHistory.query.filter_by(symbol=symbol).all()
        prices = [float(stat.price_usd) for stat in stats]
        times = ['%s' % stat.date for stat in stats]
        bar_chart = pygal.Line(width=800, height=500, explicit_size=True, style=LightStyle, x_label_rotation=70,
                               dots_size=2)
        bar_chart.add('USD', prices)
        bar_chart.x_labels = times
        return bar_chart.render_data_uri()
