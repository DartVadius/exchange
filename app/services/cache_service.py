from app.services.exchange_service import ExchangeService
from werkzeug.contrib.cache import SimpleCache
from app.dbmodels import SellersCache
from app import db


class CacheService:
    def __init__(self):
        self.cache = SimpleCache()
        self.exchange_service = ExchangeService()

    def set_currency_count(self):
        currency_count = self.cache.get('currency_count')
        if currency_count is None:
            currency_count = self.exchange_service.get_currency_count()
            self.cache.set('currency_count', currency_count, timeout=60 * 60 * 24 * 30)
        return currency_count

    def set_markets_count(self):
        market_count = self.cache.get('market_count')
        if market_count is None:
            market_count = self.exchange_service.get_market_count()
            self.cache.set('market_count', market_count, timeout=60 * 60 * 24 * 30)
        return market_count

    def set_sellers(self, code, data):
        sellers_cache = SellersCache.query.filter_by(code=code).first()
        if sellers_cache is None:
            sellers_cache = SellersCache()
            sellers_cache.code = code
            sellers_cache.data = data
            db.session.add(sellers_cache)
        else:
            sellers_cache.data = data
            db.session.add(sellers_cache)
        db.session.commit()
        return sellers_cache

    def get_sellers(self, code):
        return SellersCache.query.filter_by(code=code).first()
