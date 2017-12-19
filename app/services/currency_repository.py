from app.dbmodels import Currencies, CurrencyStatistic
from app.services.rate_repository import RateRepository


class CurrencyRepository:
    def get_currencies_with_btc_volume(self):
        rate_repository = RateRepository()
        currencies = Currencies.query.all()
        for currency in currencies:
            volume = rate_repository.get_currency_volume(currency.id)
            currency.volume = volume
        return currencies

    def get_fiat_currencies(self):
        return Currencies.query.filter_by(type=Currencies.FIAT_MONEY).order_by(Currencies.name).all()

    def get_currencies_statistic(self):
        return CurrencyStatistic.query.order_by(CurrencyStatistic.rank).all()

    def get_currencies_statistic_paginate(self, page, item_per_page):
        return CurrencyStatistic.query.order_by(CurrencyStatistic.rank).paginate(page, item_per_page, False)
