from app.dbmodels import Currencies
from app.services.rate_repository import RateRepository


class CurrencyRepository:
    def get_currencies_with_btc_volume(self):
        rate_repository = RateRepository()
        currencies = Currencies.query.all()
        for currency in currencies:
            volume = rate_repository.get_currency_volume(currency.id)
            currency.volume = volume
        return currencies
