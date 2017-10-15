from sqlalchemy import Column, INTEGER, String, UniqueConstraint, TIMESTAMP, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(INTEGER, primary_key=True)
    author = Column(String(255), index=True, unique=False)
    title = Column(String(255), index=True, unique=True)

    def __init__(self, author, title):
        self.author = author
        self.title = title

    def __repr__(self):
        return '<Book %r>' % (self.author + self.title)


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

    def __init__(self, name, url, api_key, api_secret):
        self.name = name
        self.url = url
        self.api_key = api_key
        self.api_secret = api_secret


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
    high_price = Column(DECIMAL(precision=14, scale=10))
    low_price = Column(DECIMAL(precision=14, scale=10))
    last_price = Column(DECIMAL(precision=14, scale=10))
    volume = Column(DECIMAL(precision=14, scale=5))
    bid = Column(DECIMAL(precision=14, scale=10))
    ask = Column(DECIMAL(precision=14, scale=10))

    history_current_currency = relationship("Currencies", back_populates="history_current", uselist=False,
                                            foreign_keys=[current_currency_id])
    history_compare_currency = relationship("Currencies", back_populates="history_compare", uselist=False,
                                            foreign_keys=[compare_currency_id])

    def __init__(self, stock_exchange_id, current_currency_id, compare_currency_id, date, high_price, low_price,
                 last_price, volume, bid, ask):
        self.stock_exchange_id = stock_exchange_id
        self.current_currency_id = current_currency_id
        self.compare_currency_id = compare_currency_id
        self.date = date
        self.high_price = high_price
        self.low_price = low_price
        self.last_price = last_price
        self.volume = volume
        self.bid = bid
        self.ask = ask


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
    high_price = Column(DECIMAL(precision=14, scale=10))
    low_price = Column(DECIMAL(precision=14, scale=10))
    last_price = Column(DECIMAL(precision=14, scale=10))
    volume = Column(DECIMAL(precision=14, scale=5))
    bid = Column(DECIMAL(precision=14, scale=10))
    ask = Column(DECIMAL(precision=14, scale=10))

    rate_current_currency = relationship("Currencies", back_populates="rate_current", uselist=False,
                                         foreign_keys=[current_currency_id])
    rate_compare_currency = relationship("Currencies", back_populates="rate_compare", uselist=False,
                                         foreign_keys=[compare_currency_id])

    __table_args__ = (
        UniqueConstraint('stock_exchange_id', 'current_currency_id', 'compare_currency_id',
                         name='_current_compare_stock'),
        {'mysql_engine': 'InnoDB'})

    def __init__(self, stock_exchange_id, current_currency_id, compare_currency_id, date, high_price, low_price,
                 last_price, volume, bid, ask):
        self.stock_exchange_id = stock_exchange_id
        self.current_currency_id = current_currency_id
        self.compare_currency_id = compare_currency_id
        self.date = date
        self.high_price = high_price
        self.low_price = low_price
        self.last_price = last_price
        self.volume = volume
        self.bid = bid
        self.ask = ask
