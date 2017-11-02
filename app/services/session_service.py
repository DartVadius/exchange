from flask import session
from app.services.cache_service import CacheService


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

    def set_count(self):
        self.set_currency_count()
        self.set_markets_count()
