from app.dbmodels import StockExchanges
from app.database import db_session


def get_stock_name_by_id(stock_id):
    return db_session.query(StockExchanges.name).filter_by(id=stock_id).first()[0]
