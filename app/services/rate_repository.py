from app.database import db_session
from app.dbmodels import ExchangeRates


def get_rates_by_stock_id(stock_id):
    exchange_rates = db_session.query(ExchangeRates).filter_by(stock_exchange_id=stock_id).all()
    return exchange_rates


def get_date_by_stock_id(stock_id):
    result = db_session.query(ExchangeRates.date).filter_by(stock_exchange_id=stock_id).first()
    if result is not None:
        return result[0]
    return None
