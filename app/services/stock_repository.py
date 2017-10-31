from app.dbmodels import StockExchanges
from app.database import db_session


class StockRepository:
    def get_type_by_id(self, stock_id):
        return db_session.query(StockExchanges.type).filter_by(id=stock_id).first()[0]

    def get_stock_name_by_id(self, stock_id):
        return db_session.query(StockExchanges.name).filter_by(id=stock_id).first()[0]

    def get_stock_id_by_slug(self, slug):
        return db_session.query(StockExchanges.id).filter_by(slug=slug).first()[0]
