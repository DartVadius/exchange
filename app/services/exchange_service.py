from app.dbmodels import StockExchanges, Currencies, ExchangeRates, ExchangeHistory
from app import db
from app.stocks.class_map import classmap
import threading


class ExchangeService:
    def __init__(self):
        self.stocks = StockExchanges.query.all()
        self.currencies = Currencies.query.all()
        self.classmap = classmap

    def set_currencies(self):
        for stock in self.stocks:
            if stock.name in self.classmap and stock.active == 1:
                model = self.classmap[stock.name](stock)
                stock_currency = model.set_currencies().get_currencies()
                if not stock_currency:
                    continue
                local_currency = [item.name for item in self.currencies]
                difference = [{'name': item} for item in set(stock_currency).difference(local_currency)]
                for currency in difference:
                    new_currency = Currencies(name=currency['name'])
                    db.session.add(new_currency)
                    # db_session.add(new_currency)
                    db.session.commit()
                    self.currencies.append(new_currency)
        return self

    def set_markets(self):
        for stock in self.stocks:
            if stock.name in self.classmap and stock.active == 1:
                model = self.classmap[stock.name](stock)
                stock_markets = model.set_markets().get_markets()
                if not stock_markets:
                    continue
                for market in stock_markets:
                    market['compare_currency_id'] = self.get_currency_id_by_name(market['compare_currency'])
                    market['current_currency_id'] = self.get_currency_id_by_name(market['current_currency'])
                    market['stock_exchange_id'] = self.get_stock_id_by_name(stock.name)
                    if market['compare_currency_id'] and market['current_currency_id']:
                        # self.update_rate(market)
                        # self.update_history(market)
                        thread_rate = threading.Thread(target=self.update_rate, args=(market,))
                        thread_rate.daemon = True
                        thread_rate.start()
                        thread_history = threading.Thread(target=self.update_history, args=(market,))
                        thread_history.daemon = True
                        thread_history.start()
        return self

    def update_rate(self, market):
        rate_to_update = ExchangeRates.query.filter_by(
            stock_exchange_id=market['stock_exchange_id'],
            current_currency_id=market['current_currency_id'],
            compare_currency_id=market['compare_currency_id']
        ).first()
        if rate_to_update is None:
            rate = ExchangeRates(market)
            db.session.add(rate)
        else:
            rate_to_update.current_currency_id = market['current_currency_id'],
            rate_to_update.compare_currency_id = market['compare_currency_id'],
            rate_to_update.date = market['date'],
            rate_to_update.high_price = market['high_price'],
            rate_to_update.low_price = market['low_price'],
            rate_to_update.last_price = market['last_price'],
            rate_to_update.volume = market['volume'],
            rate_to_update.base_volume = market['base_volume'],
            rate_to_update.ask = market['ask'],
            rate_to_update.bid = market['bid'],
        db.session.commit()

    def update_history(self, market):
        history = ExchangeHistory(market)
        db.session.add(history)
        db.session.commit()

    def get_stock_id_by_name(self, name):
        for stock in self.stocks:
            if name.lower() == stock.name.lower():
                return stock.id
        return None

    def get_currency_id_by_name(self, name):
        for currency in self.currencies:
            if name.lower() == currency.name.lower():
                return currency.id
        return None

    def get_currency_count(self):
        return Currencies.query.count()

    def get_market_count(self):
        return StockExchanges.query.count()
