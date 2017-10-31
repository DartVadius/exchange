from flask import session
from app.services.exchange_service import ExchangeService


class SessionService:
    def __init__(self):
        self.exchange_service = ExchangeService()

    def set_currency_count(self):
        if 'currency_count' not in session:
            session['currency_count'] = self.exchange_service.get_currency_count()
            return True
        return False

    def set_markets_count(self):
        if 'market_count' not in session:
            session['market_count'] = self.exchange_service.get_market_count()
            return True
        return False

    def set_count(self):
        self.set_currency_count()
        self.set_markets_count()
