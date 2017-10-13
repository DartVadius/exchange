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
    # currency_current_rates = relationship('ExchangeRates', backref='currencies', lazy=True)
    # currency_compare_rates = relationship('ExchangeRates', backref='currencies', lazy=True)
    # currencie = relationship('Currencies',
    #                           primaryjoin="or_(Currencies.id==ExchangeRates.compare_currency_id, Currencies.id==ExchangeRates.current_currency_id)",
    #                           lazy=True, backref='currencies', viewonly=True)


class StockExchanges(Base):
    __tablename__ = 'stock_exchanges'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    url = Column(String(255), nullable=False)
    api_key = Column(String(45), nullable=True)
    api_secret = Column(String(45), nullable=True)
    # exchange_rates = relationship('ExchangeRates', backref='stock_exchanges', lazy=True)


class ExchangeRates(Base):
    __tablename__ = 'exchange_rates'

    id = Column(INTEGER, primary_key=True)
    stock_exchange_id = Column(INTEGER,
                               nullable=False, index=True)
    current_currency_id = Column(INTEGER,
                                 nullable=False, index=True)
    compare_currency_id = Column(INTEGER,
                                 nullable=False, index=True)
    date = Column(TIMESTAMP, nullable=False)
    high_price = Column(DECIMAL(precision=14, scale=10))
    low_price = Column(DECIMAL(precision=14, scale=10))
    last_price = Column(DECIMAL(precision=14, scale=10))
    volume = Column(DECIMAL(precision=14, scale=5))
    bid = Column(DECIMAL(precision=14, scale=10))
    ask = Column(DECIMAL(precision=14, scale=10))

    __table_args__ = (
        UniqueConstraint('stock_exchange_id', 'current_currency_id', 'compare_currency_id',
                         name='_current_compare_stock'),
        {'mysql_engine': 'InnoDB'})
