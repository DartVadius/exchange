from sqlalchemy import func
from app.dbmodels import StockExchanges, ExchangeRates


class StockRepository:
    def get_type_by_id(self, stock_id):
        return StockExchanges.query.with_entities(StockExchanges.type).filter_by(id=stock_id).first()[0]

    def get_stock_name_by_id(self, stock_id):
        return StockExchanges.query.with_entities(StockExchanges.name).filter_by(id=stock_id).first()[0]

    def get_stock_id_by_slug(self, slug):
        return StockExchanges.query.with_entities(StockExchanges.id).filter_by(slug=slug).first()[0]

    def get_stocks_with_volume_summary(self):
        all_stocks = StockExchanges.query.filter_by(active='1').all()
        for stock in all_stocks:
            volume = ExchangeRates.query.with_entities(func.sum(ExchangeRates.volume).label('volume')).filter(
                ExchangeRates.stock_exchange_id == stock.id).one()
            stock.volume = volume[0]
        return all_stocks
