from flask import session
from app.services.cache_service import CacheService
from app.dbmodels import Countries, PaymentMethods


class SessionService:
    def __init__(self):
        self.cache_service = CacheService()

    def set_currency_count(self):
        if 'currency_count' not in session:
            session['currency_count'] = self.cache_service.set_currency_count()
            return True
        return False

    def set_markets_count(self):
        if 'market_count' not in session:
            session['market_count'] = self.cache_service.set_markets_count()
            return True
        return False

    def set_countries_count(self):
        if 'country_count' not in session:
            session['country_count'] = Countries.query.count()
            return True
        return False

    def set_methods_count(self):
        if 'method_count' not in session:
            session['method_count'] = PaymentMethods.query.count()
            return True
        return False

    def set_count(self):
        self.set_currency_count()
        self.set_markets_count()
        self.set_countries_count()
        self.set_methods_count()
