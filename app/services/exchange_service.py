from app.dbmodels import StockExchanges, Currencies
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
                local_currency = [item.name for item in self.currencies]
                result = [item for item in set(stock_currency).difference(local_currency)]
                for currency in result:
                    new_currency = Currencies(currency)
                    self.currencies.append(new_currency)
                    db_session.add(new_currency)
        db_session.commit()
        # self.currencies = db_session.query(Currencies).all()
        return self

    def get_stock_id_by_name(self, name):
        for market in self.markets:
            if name.lower() == market.name.lower():
                return market.id
        return None

    def get_currency_id_by_name(self, name):
        for currency in self.currencies:
            if name.lower() == currency.name.lower():
                return currency.id
        return None
