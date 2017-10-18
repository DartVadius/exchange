from sqlalchemy.orm import aliased

from app.database import db_session
from app.dbmodels import StockExchanges, ExchangeRates, Currencies


def get_rates_by_stock_id(stock_id):
    currency_compare = aliased(Currencies)
    currency_current = aliased(Currencies)
    exchange_rates = db_session.query(
        ExchangeRates.high_price, ExchangeRates.low_price, ExchangeRates.last_price, ExchangeRates.ask,
        ExchangeRates.bid, ExchangeRates.volume,
        StockExchanges.name.label('stock_exchange_name'),
        currency_compare.name.label('compare_currency_name'),
        currency_current.name.label('current_currency_name')
    ).filter_by(stock_exchange_id=stock_id).join(StockExchanges).join(
        currency_compare, ExchangeRates.compare_currency_id == currency_compare.id
    ).join(
        currency_current, ExchangeRates.current_currency_id == currency_current.id
    ).all()
    return exchange_rates


def get_date_by_stock_id(stock_id):
    result = db_session.query(ExchangeRates.date).filter_by(stock_exchange_id=stock_id).first()
    if result is not None:
        return result[0]
    return None
