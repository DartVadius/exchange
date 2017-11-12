import threading

from werkzeug.contrib.cache import SimpleCache

from app import db
from app.dbmodels import StockExchanges, Currencies, ExchangeRates, ExchangeHistory, Countries, PaymentMethods
from app.stocks.class_map import classmap
from time import sleep


class ExchangeService:
    def __init__(self):
        self.stocks = StockExchanges.query.all()
        self.currencies = Currencies.query.all()
        self.countries = Countries.query.all()
        self.payment_methods = PaymentMethods.query.all()
        self.classmap = classmap
        self.cache = SimpleCache()
        self.cache.set('market_count', self.stocks.count(self), timeout=60 * 60 * 24 * 30)

    def set_rates(self):
        for stock in self.stocks:
            if stock.name in self.classmap and stock.active == 1:
                model = self.classmap[stock.name](stock)
                model.set_currencies()
                model.set_markets()
                stock_currency = model.get_currencies()
                if stock_currency:
                    self.set_currencies(stock_currency)
                stock_markets = model.get_markets()
                if stock_markets:
                    self.set_markets(stock_markets, stock)
        return self

    def set_currencies(self, stock_currency):
        local_currency = [item.name for item in self.currencies]
        difference = [{'name': item} for item in set(stock_currency).difference(local_currency)]
        for currency in difference:
            new_currency = Currencies(name=currency['name'], slug=currency['name'])
            db.session.add(new_currency)
            db.session.commit()
            self.currencies.append(new_currency)
        self.cache.set('currency_count', self.currencies.count(self), timeout=60 * 60 * 24 * 30)
        return self

    def set_markets(self, stock_markets, stock):
        for market in stock_markets:
            market['compare_currency_id'] = self.get_currency_id_by_name(market['compare_currency'])
            market['base_currency_id'] = self.get_currency_id_by_name(market['base_currency'])
            market['stock_exchange_id'] = self.get_stock_id_by_name(stock.name)
            if market['compare_currency_id'] and market['base_currency_id']:
                # self.update_rate(market)
                # self.update_history(market)
                thread_rate = threading.Thread(target=self.update_rate, args=(market,))
                thread_rate.daemon = True
                thread_rate.start()
                thread_history = threading.Thread(target=self.update_history, args=(market,))
                thread_history.daemon = True
                thread_history.start()
        self.cache.set('market_count', self.stocks.count(self), timeout=60 * 60 * 24 * 30)
        return self

    def update_rate(self, market):
        rate_to_update = ExchangeRates.query.filter_by(
            stock_exchange_id=market['stock_exchange_id'],
            base_currency_id=market['base_currency_id'],
            compare_currency_id=market['compare_currency_id']
        ).first()
        if rate_to_update is None:
            rate = ExchangeRates(market)
            db.session.add(rate)
        else:
            rate_to_update.base_currency_id = market['base_currency_id'],
            rate_to_update.compare_currency_id = market['compare_currency_id'],
            rate_to_update.date = market['date'],
            rate_to_update.high_price = market['high_price'],
            rate_to_update.low_price = market['low_price'],
            rate_to_update.last_price = market['last_price'],
            rate_to_update.average_price = market['average_price'],
            rate_to_update.btc_price = market['btc_price'],
            rate_to_update.volume = market['volume'],
            rate_to_update.base_volume = market['base_volume'],
            rate_to_update.ask = market['ask'],
            rate_to_update.bid = market['bid'],
        db.session.commit()

    def update_history(self, market):
        history = ExchangeHistory(market)
        db.session.add(history)
        db.session.commit()

    def set_countries(self):
        for stock in self.stocks:
            if stock.name in self.classmap and stock.active == 1:
                model = self.classmap[stock.name](stock)
                stock_country = model.set_countries()
                if not stock_country:
                    continue
                local_country = [item.name_alpha2.upper() for item in self.countries]
                difference = [{'code': item} for item in set(stock_country).difference(local_country)]
                for country in difference:
                    new_country = Countries(name_alpha2=country['code'].upper(), slug=country['code'].lower())
                    db.session.add(new_country)
                    db.session.commit()
                    self.countries.append(new_country)
        self.cache.set('country_count', self.countries.count(self), timeout=60 * 60 * 24 * 30)
        return self

    def set_payment_methods(self):
        for stock in self.stocks:
            if stock.name in self.classmap and stock.active == 1:
                model = self.classmap[stock.name](stock)
                stock_methods = model.set_payment_methods()
                if not stock_methods:
                    continue
                stock_methods_compare = [key for key in stock_methods.keys()]
                local_methods = [item.code for item in self.payment_methods]
                difference = [item for item in set(stock_methods_compare).difference(local_methods)]
                for method in difference:
                    new_method = PaymentMethods(name=stock_methods[method]['name'],
                                                code=stock_methods[method]['code'],
                                                slug=stock_methods[method]['method'].lower(),
                                                method=stock_methods[method]['method']
                                                )
                    db.session.add(new_method)
                    db.session.commit()
                    self.payment_methods.append(new_method)
        self.cache.set('method_count', self.payment_methods.count(self), timeout=60 * 60 * 24 * 30)
        return self

    def set_payment_methods_by_country_codes(self):
        for stock in self.stocks:
            if stock.name in self.classmap and stock.active == 1:
                model = self.classmap[stock.name](stock)
                for country in self.countries:
                    aviable_methods = model.set_payment_methods_for_country(country.name_alpha2)
                    if not aviable_methods:
                        continue
                    for aviable_method in aviable_methods:
                        method = PaymentMethods.query.filter_by(code=aviable_method['code']).first()
                        country.methods.append(method)
                        db.session.add(country)
                        db.session.commit()
                        # sleep(10)
        return self

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
        return StockExchanges.query.filter_by(active='1').count()
