from app.dbmodels import ExchangeRates
from sqlalchemy import func
from app.dbmodels import Currencies


class RateRepository:
    def get_rates_by_stock_id(self, stock_id):
        exchange_rates = ExchangeRates.query.filter_by(stock_exchange_id=stock_id).all()
        return exchange_rates

    def get_date_by_stock_id(self, stock_id):
        result = ExchangeRates.query.filter_by(stock_exchange_id=stock_id).first()
        if result is not None:
            return result.date
        return None

    def get_currency_volume(self, currency_id):
        result = ExchangeRates.query.with_entities(
            func.sum(ExchangeRates.volume * ExchangeRates.btc_price).label('sum')).filter(
            (ExchangeRates.compare_currency_id == currency_id) | (ExchangeRates.base_currency_id == currency_id)).one()
        return result[0]
