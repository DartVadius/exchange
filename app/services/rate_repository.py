from app.dbmodels import StockExchanges, ExchangeRates, Currencies
from sqlalchemy.orm import aliased
from app.database import db_session


def get_rates_by_stock_id(stock_id):
    exchange_rates = db_session.query(ExchangeRates).filter_by(stock_exchange_id=stock_id).all()
    return exchange_rates


def get_date_by_stock_id(stock_id):
    return db_session.query(ExchangeRates.date).filter_by(stock_exchange_id=stock_id).first()[0]
