from app.dbmodels import ExchangeRates


class RateRepository:
    def get_rates_by_stock_id(self, stock_id):
        exchange_rates = ExchangeRates.query.filter_by(stock_exchange_id=stock_id).all()
        return exchange_rates

    def get_date_by_stock_id(self, stock_id):
        result = ExchangeRates.query.filter_by(stock_exchange_id=stock_id).first()
        if result is not None:
            return result.date
        return None
