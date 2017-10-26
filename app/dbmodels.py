from sqlalchemy import Column, INTEGER, String, UniqueConstraint, TIMESTAMP, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from flask_admin import Admin
from app import app
from app.database import Base
from flask_admin.contrib.sqla import ModelView
from app.database import db_session
from flask_admin.form import rules, Select2Field


class Currencies(Base):
    __tablename__ = 'currencies'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True)
    name = Column(String(10), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    rate_current = relationship("ExchangeRates", foreign_keys='ExchangeRates.current_currency_id',
                                back_populates="rate_current_currency")
    rate_compare = relationship("ExchangeRates", foreign_keys='ExchangeRates.compare_currency_id',
                                back_populates="rate_compare_currency")
    history_current = relationship("ExchangeHistory", foreign_keys='ExchangeHistory.current_currency_id',
                                   back_populates="history_current_currency")
    history_compare = relationship("ExchangeHistory", foreign_keys='ExchangeHistory.compare_currency_id',
                                   back_populates="history_compare_currency")

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.description!r}>'.format(self)


class StockExchanges(Base):
    __tablename__ = 'stock_exchanges'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    url = Column(String(255), nullable=False)
    api_key = Column(String(45), nullable=True)
    api_secret = Column(String(45), nullable=True)
    active = Column(INTEGER, nullable=True, default=1)
    exchange_rates = relationship('ExchangeRates', backref='stock_exchanges', lazy=True)
    exchange_history = relationship('ExchangeHistory', backref='stock_history', lazy=True)

    # def __init__(self, name, url, api_key, api_secret):
    #     self.name = name
    #     self.url = url
    #     self.api_key = api_key
    #     self.api_secret = api_secret

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.url!r}>'.format(self)


class ExchangeHistory(Base):
    __tablename__ = 'exchange_history'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True)
    stock_exchange_id = Column(INTEGER, ForeignKey('stock_exchanges.id', ondelete='CASCADE', onupdate='NO ACTION'),
                               nullable=False, index=True)
    current_currency_id = Column(INTEGER, ForeignKey('currencies.id', ondelete='CASCADE', onupdate='NO ACTION'),
                                 nullable=False, index=True)
    compare_currency_id = Column(INTEGER, ForeignKey('currencies.id', ondelete='CASCADE', onupdate='NO ACTION'),
                                 nullable=False, index=True)
    date = Column(TIMESTAMP, nullable=False)
    high_price = Column(DECIMAL(precision=20, scale=10))
    low_price = Column(DECIMAL(precision=20, scale=10))
    last_price = Column(DECIMAL(precision=20, scale=10))
    volume = Column(DECIMAL(precision=20, scale=10))
    base_volume = Column(DECIMAL(precision=20, scale=10))
    bid = Column(DECIMAL(precision=20, scale=10))
    ask = Column(DECIMAL(precision=20, scale=10))

    history_current_currency = relationship("Currencies", back_populates="history_current", uselist=False,
                                            foreign_keys=[current_currency_id])
    history_compare_currency = relationship("Currencies", back_populates="history_compare", uselist=False,
                                            foreign_keys=[compare_currency_id])

    def __init__(self, stock):
        self.stock_exchange_id = stock['stock_exchange_id']
        self.current_currency_id = stock['current_currency_id']
        self.compare_currency_id = stock['compare_currency_id']
        self.date = stock['date']
        self.high_price = stock['high_price']
        self.low_price = stock['low_price']
        self.last_price = stock['last_price']
        self.volume = stock['volume']
        self.base_volume = stock['base_volume']
        self.bid = stock['bid']
        self.ask = stock['ask']


class ExchangeRates(Base):
    __tablename__ = 'exchange_rates'

    id = Column(INTEGER, primary_key=True)
    stock_exchange_id = Column(INTEGER, ForeignKey('stock_exchanges.id', ondelete='CASCADE', onupdate='NO ACTION'),
                               nullable=False, index=True)
    current_currency_id = Column(INTEGER, ForeignKey('currencies.id', ondelete='CASCADE', onupdate='NO ACTION'),
                                 nullable=False, index=True)
    compare_currency_id = Column(INTEGER, ForeignKey('currencies.id', ondelete='CASCADE', onupdate='NO ACTION'),
                                 nullable=False, index=True)
    date = Column(TIMESTAMP, nullable=False)
    high_price = Column(DECIMAL(precision=20, scale=10))
    low_price = Column(DECIMAL(precision=20, scale=10))
    last_price = Column(DECIMAL(precision=20, scale=10))
    volume = Column(DECIMAL(precision=20, scale=10))
    base_volume = Column(DECIMAL(precision=20, scale=10))
    bid = Column(DECIMAL(precision=20, scale=10))
    ask = Column(DECIMAL(precision=20, scale=10))

    rate_current_currency = relationship("Currencies", back_populates="rate_current", uselist=False,
                                         foreign_keys=[current_currency_id])
    rate_compare_currency = relationship("Currencies", back_populates="rate_compare", uselist=False,
                                         foreign_keys=[compare_currency_id])

    __table_args__ = (
        UniqueConstraint('stock_exchange_id', 'current_currency_id', 'compare_currency_id',
                         name='_current_compare_stock'),
        {'mysql_engine': 'InnoDB'})

    def __init__(self, stock):
        self.stock_exchange_id = stock['stock_exchange_id']
        self.current_currency_id = stock['current_currency_id']
        self.compare_currency_id = stock['compare_currency_id']
        self.date = stock['date']
        self.high_price = stock['high_price']
        self.low_price = stock['low_price']
        self.last_price = stock['last_price']
        self.volume = stock['volume']
        self.base_volume = stock['base_volume']
        self.bid = stock['bid']
        self.ask = stock['ask']


class CurrenciesAdmin(ModelView):
    page_size = 30
    column_hide_backrefs = True
    column_display_all_relations = False
    form_columns = ['name', 'description', ]
    can_edit = False
    # form_create_rules = ('name', 'description',)
    # form_edit_rules = [
    #     rules.FieldSet(('description',), 'Edit currency')
    # ]
    column_editable_list = ('description',)


class StockExchangesAdmin(ModelView):
    column_list = ('name', 'url', 'api_key', 'api_secret', 'active')
    # column_formatters = dict(active=lambda name, url, api_secret, active: {1: 'Enable', 0: 'Disable'})
    column_hide_backrefs = True
    column_display_all_relations = False
    form_columns = ['name', 'url', 'active', 'api_key', 'api_secret']
    form_overrides = dict(
        active=Select2Field
    )
    form_args = dict(
        active=dict(
            choices=[
                ('1', 'Enable'),
                ('0', 'Disable')
            ]
        )
    )


admin = Admin(app, name='exchange', template_mode='bootstrap3')
admin.add_view(CurrenciesAdmin(Currencies, db_session))
admin.add_view(StockExchangesAdmin(StockExchanges, db_session))
