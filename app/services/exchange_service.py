from app.dbmodels import StockExchanges, Currencies, ExchangeRates, ExchangeHistory
from app.database import db_session
from app.stocks.class_map import classmap


class ExchangeService:
    # modules = {name: cls for name, cls in stocks.__dict__.items() if '__' not in name}

    def __init__(self):
        self.stocks = db_session.query(StockExchanges).all()
        self.currencies = db_session.query(Currencies).all()
        self.classmap = classmap

    def set_currencies(self):
        for stock in self.stocks:
            if stock.name in self.classmap and stock.active == 1:
                model = self.classmap[stock.name](stock)
                stock_currency = model.set_currencies().get_currencies()
                if not stock_currency:
                    continue
                local_currency = [item.name for item in self.currencies]
                difference = [item for item in set(stock_currency).difference(local_currency)]
                for currency in difference:
                    new_currency = Currencies(currency)
                    db_session.add(new_currency)
                    db_session.commit()
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
                    rate = ExchangeRates(market)
                    history = ExchangeHistory(market)
                    print(rate)
                    print(history)
                # local_currency = [item.name for item in self.currencies]
                # result = [item for item in set(stock_currency).difference(local_currency)]
                # for currency in result:
                #     new_currency = Currencies(currency)
                #     db_session.add(new_currency)
                #     db_session.commit()
                #     self.currencies.append(new_currency)
        # self.currencies = db_session.query(Currencies).all()
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
