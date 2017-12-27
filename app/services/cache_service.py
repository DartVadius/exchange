from werkzeug.contrib.cache import SimpleCache

from app import db
from app.dbmodels import SellersCache, BuyersCache
from app.services.exchange_service import ExchangeService
from sqlalchemy.orm import scoped_session, sessionmaker
from app import database
from sqlalchemy import create_engine


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

    @staticmethod
    def set_sellers(code, data):
        engine = create_engine(database.connect)
        Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        session = Session()
        sellers_cache = SellersCache.query.filter_by(code=code).first()
        if sellers_cache is None:
            sellers_cache = SellersCache()
            sellers_cache.code = code
            sellers_cache.data = data
            local_object = session.merge(sellers_cache)
            session.add(local_object)
            # db.session.add(sellers_cache)
        else:
            sellers_cache.data = data
            local_object = session.merge(sellers_cache)
            session.add(local_object)
            # db.session.add(sellers_cache)
        session.commit()
        session.close()
        # db.session.commit()
        return sellers_cache

    @staticmethod
    def get_sellers(code):
        return SellersCache.query.filter_by(code=code).first()

    @staticmethod
    def set_buyers(code, data):
        engine = create_engine(database.connect)
        Session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        session = Session()
        buyers_cache = BuyersCache.query.filter_by(code=code).first()
        if buyers_cache is None:
            buyers_cache = BuyersCache()
            buyers_cache.code = code
            buyers_cache.data = data
            local_object = session.merge(buyers_cache)
            session.add(local_object)
            # db.session.add(buyers_cache)
        else:
            buyers_cache.data = data
            local_object = session.merge(buyers_cache)
            session.add(local_object)
            # db.session.add(buyers_cache)
        # db.session.commit()
        session.commit()
        session.close()
        return buyers_cache

    @staticmethod
    def get_buyers(code):
        return BuyersCache.query.filter_by(code=code).first()
