from flask import request, redirect, url_for
from flask_admin import Admin, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.filters import FilterEqual
from flask_admin.form import Select2Field
from flask_login import current_user
from sqlalchemy import Column, INTEGER, String, UniqueConstraint, TIMESTAMP, DECIMAL, ForeignKey, Text
from sqlalchemy.dialects.mysql.base import LONGTEXT
from sqlalchemy.orm import relationship

from app import app, login_manager, bcrypt, db


@login_manager.user_loader
def _user_loader(user_id):
    return User.query.get(int(user_id))


class Content(db.Model):
    __tablename__ = 'contents'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))
    template = db.Column(db.String(256))
    schema = db.Column(db.Text)
    data = db.Column(db.Text)

    def __unicode__(self):
        return u'content for ' + self.url

    def __str__(self):
        return 'content for ' + self.url


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column(INTEGER, primary_key=True)
    login = Column(String(25), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    admin = Column(INTEGER, nullable=False, default=0)
    active = Column(INTEGER, nullable=False, default=0)

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_admin(self):
        return self.admin

    def is_anonymous(self):
        return False

    @staticmethod
    def make_password(plaintext):
        return bcrypt.generate_password_hash(plaintext)

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password, raw_password)

    @classmethod
    def create(cls, login, password, **kwargs):
        return User(login=login, password=User.make_password(password), admin=False, active=False, **kwargs)

    @staticmethod
    def authenticate(login, password):
        user = User.query.filter(User.login == login).first()
        if user and user.check_password(password):
            return user
        return False


class Tokens(db.Model):
    __tablename__ = 'tokens'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True)
    token = Column(String(50), nullable=False, unique=True)
    expired = Column(TIMESTAMP, nullable=False)
    user_id = Column(INTEGER, nullable=False, index=True)


class Currencies(db.Model):
    __tablename__ = 'currencies'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    COIN = '1'
    TOKEN = '2'
    FIAT_MONEY = '3'

    id = Column(INTEGER, primary_key=True)
    name = Column(String(10), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    slug = Column(String(255), nullable=False, unique=True)
    meta_tags = Column(String(255), nullable=True, unique=False)
    meta_description = Column(Text(), nullable=True, unique=False)
    type = Column(INTEGER, nullable=True, default=1)
    priority = Column(INTEGER, nullable=True, default=0)
    rate_base = relationship("ExchangeRates", foreign_keys='ExchangeRates.base_currency_id',
                             back_populates="rate_base_currency")
    rate_compare = relationship("ExchangeRates", foreign_keys='ExchangeRates.compare_currency_id',
                                back_populates="rate_compare_currency")
    history_base = relationship("ExchangeHistory", foreign_keys='ExchangeHistory.base_currency_id',
                                back_populates="history_base_currency")
    history_compare = relationship("ExchangeHistory", foreign_keys='ExchangeHistory.compare_currency_id',
                                   back_populates="history_compare_currency")
    statistic = relationship("CurrencyStatistic", foreign_keys='CurrencyStatistic.symbol',
                             back_populates="statistic_currency")
    statistic_history = relationship("CurrencyStatisticHistory", foreign_keys='CurrencyStatisticHistory.symbol',
                                     back_populates="statistic_currency_history")

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.description!r}>'.format(self)

    def count(self):
        return self.query.count()


class CurrencyStatistic(db.Model):
    __tablename__ = 'currency_statistic'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column(INTEGER, primary_key=True)
    symbol = Column(String(10), ForeignKey('currencies.name', ondelete='CASCADE', onupdate='CASCADE'),
                    nullable=False, unique=True)
    name = Column(String(255), nullable=False, unique=False)
    rank = Column(INTEGER, nullable=False)
    price_usd = Column(DECIMAL(precision=30, scale=10), nullable=True)
    price_btc = Column(DECIMAL(precision=30, scale=10), nullable=True)
    volume_usd_day = Column(DECIMAL(precision=60, scale=20), nullable=True)
    market_cap_usd = Column(DECIMAL(precision=60, scale=20), nullable=True)
    percent_change_hour = Column(DECIMAL(precision=20, scale=10), nullable=True)
    percent_change_day = Column(DECIMAL(precision=20, scale=10), nullable=True)
    percent_change_week = Column(DECIMAL(precision=20, scale=10), nullable=True)
    available_supply = Column(DECIMAL(precision=65, scale=20), nullable=True)
    total_supply = Column(DECIMAL(precision=65, scale=20), nullable=True)
    max_supply = Column(DECIMAL(precision=65, scale=20), nullable=True)
    date = Column(TIMESTAMP, nullable=False)

    statistic_currency = relationship("Currencies", back_populates="statistic", uselist=False,
                                      foreign_keys=[symbol])

    def __repr__(self):
        return '<Stats: name={0.symbol!r}, description={0.name!r}>'.format(self)

    def count(self):
        return self.query.count()

    def serialaze(self):
        return {
            "id": self.id,
            "name": self.name,
            "symbol": self.symbol,
            "date": self.date.strftime('%Y-%m-%d %H:%M:%S'),
            "rank": self.rank,
            "price_usd": str(self.price_usd),
            "price_btc": str(self.price_btc),
            "volume_usd_day": str(self.volume_usd_day),
            "market_cap_usd": str(self.market_cap_usd),
            "percent_change_hour": str(self.percent_change_hour),
            "percent_change_day": str(self.percent_change_day),
            "percent_change_week": str(self.percent_change_week),
            "available_supply": str(self.available_supply),
            "total_supply": str(self.total_supply),
            "max_supply": str(self.max_supply)
        }


class CurrencyStatisticHistory(db.Model):
    __tablename__ = 'currency_statistic_history'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column(INTEGER, primary_key=True)
    symbol = Column(String(10), ForeignKey('currencies.name', ondelete='CASCADE', onupdate='CASCADE'), nullable=False,
                    unique=False)
    name = Column(String(255), nullable=False, unique=False)
    rank = Column(INTEGER, nullable=False)
    price_usd = Column(DECIMAL(precision=30, scale=10), nullable=True)
    price_btc = Column(DECIMAL(precision=30, scale=10), nullable=True)
    volume_usd_day = Column(DECIMAL(precision=60, scale=20), nullable=True)
    market_cap_usd = Column(DECIMAL(precision=60, scale=20), nullable=True)
    percent_change_hour = Column(DECIMAL(precision=20, scale=10), nullable=True)
    percent_change_day = Column(DECIMAL(precision=20, scale=10), nullable=True)
    percent_change_week = Column(DECIMAL(precision=20, scale=10), nullable=True)
    available_supply = Column(DECIMAL(precision=65, scale=20), nullable=True)
    total_supply = Column(DECIMAL(precision=65, scale=20), nullable=True)
    max_supply = Column(DECIMAL(precision=65, scale=20), nullable=True)
    date = Column(TIMESTAMP, nullable=False)

    statistic_currency_history = relationship("Currencies", back_populates="statistic_history", uselist=False,
                                              foreign_keys=[symbol])

    def __repr__(self):
        return '<Stats: name={0.symbol!r}, description={0.name!r}>'.format(self)

    def count(self):
        return self.query.count()

    def serialaze(self):
        return {
            "id": self.id,
            "name": self.name,
            "symbol": self.symbol,
            "date": self.date.strftime('%Y-%m-%d %H:%M:%S'),
            "rank": self.rank,
            "price_usd": str(self.price_usd),
            "price_btc": str(self.price_btc),
            "volume_usd_day": str(self.volume_usd_day),
            "market_cap_usd": str(self.market_cap_usd),
            "percent_change_hour": str(self.percent_change_hour),
            "percent_change_day": str(self.percent_change_day),
            "percent_change_week": str(self.percent_change_week),
            "available_supply": str(self.available_supply),
            "total_supply": str(self.total_supply),
            "max_supply": str(self.max_supply)
        }


class CountryMethod(db.Model):
    __tablename__ = 'country_method'
    country_id = Column(INTEGER, ForeignKey('countries.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    method_id = Column(INTEGER, ForeignKey('payment_methods.id', ondelete='CASCADE', onupdate='CASCADE'),
                       primary_key=True)
    exchange_id = Column(INTEGER, ForeignKey('stock_exchanges.id', ondelete='CASCADE', onupdate='CASCADE'),
                         primary_key=True)

    def __init__(self, countries_id, payment_methods_id, stock_exchanges_id):
        self.country_id = countries_id
        self.method_id = payment_methods_id
        self.exchange_id = stock_exchanges_id


class Countries(db.Model):
    __tablename__ = 'countries'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column(INTEGER, primary_key=True)
    name_alpha2 = Column(String(10), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    slug = Column(String(255), nullable=False, unique=True)
    meta_tags = Column(String(255), nullable=True, unique=False)
    meta_description = Column(Text(), nullable=True, unique=False)
    priority = Column(INTEGER, nullable=True, default=0)
    method_country = relationship("PaymentMethods", secondary='country_method', back_populates="payment_country")
    stock_country = relationship("StockExchanges", secondary='country_method', back_populates="exchange_country")

    def __repr__(self):
        return '<Stats: name={0.name_alpha2!r}, description={0.description!r}>'.format(self)

    def count(self):
        return self.query.count()


class PaymentMethods(db.Model):
    __tablename__ = 'payment_methods'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    method = Column(String(255), nullable=False, unique=True)
    code = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=True)
    slug = Column(String(255), nullable=False, unique=True)
    meta_tags = Column(String(255), nullable=True, unique=False)
    meta_description = Column(Text(), nullable=True, unique=False)
    priority = Column(INTEGER, nullable=True, default=0)
    payment_country = relationship("Countries", secondary='country_method', back_populates="method_country")
    payment_stock = relationship("StockExchanges", secondary='country_method', back_populates="exchange_payment")

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.description!r}>'.format(self)

    def count(self):
        return self.query.count()


class StockExchanges(db.Model):
    __tablename__ = 'stock_exchanges'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    url = Column(String(255), nullable=False)
    refferal_link = Column(String(255), nullable=True)
    slug = Column(String(255), nullable=False, unique=True)
    meta_tags = Column(String(255), nullable=True, unique=False)
    meta_description = Column(Text(), nullable=True, unique=False)
    api_key = Column(String(255), nullable=True)
    api_secret = Column(String(255), nullable=True)
    active = Column(INTEGER, nullable=True, default=1)
    type = Column(String(45), nullable=False, default='market')
    exchange_rates = relationship('ExchangeRates', backref='stock_exchanges', lazy=True)
    exchange_history = relationship('ExchangeHistory', backref='stock_history', lazy=True)
    exchange_country = relationship("Countries", secondary='country_method', back_populates="stock_country")
    exchange_payment = relationship("PaymentMethods", secondary='country_method', back_populates="payment_stock")

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.url!r}>'.format(self)


class ExchangeHistory(db.Model):
    __tablename__ = 'exchange_history'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True)
    stock_exchange_id = Column(INTEGER, ForeignKey('stock_exchanges.id', ondelete='CASCADE', onupdate='CASCADE'),
                               nullable=False, index=True)
    base_currency_id = Column(INTEGER, ForeignKey('currencies.id', ondelete='CASCADE', onupdate='CASCADE'),
                              nullable=False, index=True)
    compare_currency_id = Column(INTEGER, ForeignKey('currencies.id', ondelete='CASCADE', onupdate='CASCADE'),
                                 nullable=False, index=True)
    date = Column(TIMESTAMP, nullable=False)
    high_price = Column(DECIMAL(precision=30, scale=20))
    low_price = Column(DECIMAL(precision=30, scale=20))
    last_price = Column(DECIMAL(precision=30, scale=20))
    average_price = Column(DECIMAL(precision=30, scale=20))
    btc_price = Column(DECIMAL(precision=30, scale=20))
    volume = Column(DECIMAL(precision=60, scale=10))
    base_volume = Column(DECIMAL(precision=30, scale=20))
    bid = Column(DECIMAL(precision=30, scale=20))
    ask = Column(DECIMAL(precision=30, scale=20))

    history_base_currency = relationship("Currencies", back_populates="history_base", uselist=False,
                                         foreign_keys=[base_currency_id])
    history_compare_currency = relationship("Currencies", back_populates="history_compare", uselist=False,
                                            foreign_keys=[compare_currency_id])

    def __init__(self, stock):
        self.stock_exchange_id = stock['stock_exchange_id']
        self.base_currency_id = stock['base_currency_id']
        self.compare_currency_id = stock['compare_currency_id']
        self.date = stock['date']
        self.high_price = stock['high_price']
        self.low_price = stock['low_price']
        self.last_price = stock['last_price']
        self.average_price = stock['average_price']
        self.btc_price = stock['btc_price']
        self.volume = stock['volume']
        self.base_volume = stock['base_volume']
        self.bid = stock['bid']
        self.ask = stock['ask']


class ExchangeRates(db.Model):
    __tablename__ = 'exchange_rates'

    id = Column(INTEGER, primary_key=True)
    stock_exchange_id = Column(INTEGER, ForeignKey('stock_exchanges.id', ondelete='CASCADE', onupdate='CASCADE'),
                               nullable=False, index=True)
    base_currency_id = Column(INTEGER, ForeignKey('currencies.id', ondelete='CASCADE', onupdate='CASCADE'),
                              nullable=False, index=True)
    compare_currency_id = Column(INTEGER, ForeignKey('currencies.id', ondelete='CASCADE', onupdate='CASCADE'),
                                 nullable=False, index=True)
    date = Column(TIMESTAMP, nullable=False)
    high_price = Column(DECIMAL(precision=30, scale=20))
    low_price = Column(DECIMAL(precision=30, scale=20))
    last_price = Column(DECIMAL(precision=30, scale=20))
    average_price = Column(DECIMAL(precision=30, scale=20))
    btc_price = Column(DECIMAL(precision=30, scale=20))
    volume = Column(DECIMAL(precision=60, scale=10))
    base_volume = Column(DECIMAL(precision=30, scale=20))
    bid = Column(DECIMAL(precision=30, scale=20))
    ask = Column(DECIMAL(precision=30, scale=20))

    rate_base_currency = relationship("Currencies", back_populates="rate_base", uselist=False,
                                      foreign_keys=[base_currency_id])
    rate_compare_currency = relationship("Currencies", back_populates="rate_compare", uselist=False,
                                         foreign_keys=[compare_currency_id])

    __table_args__ = (
        UniqueConstraint('stock_exchange_id', 'base_currency_id', 'compare_currency_id',
                         name='_base_compare_stock'),
        {'mysql_engine': 'InnoDB'})

    def __init__(self, stock):
        self.stock_exchange_id = stock['stock_exchange_id']
        self.base_currency_id = stock['base_currency_id']
        self.compare_currency_id = stock['compare_currency_id']
        self.date = stock['date']
        self.high_price = stock['high_price']
        self.low_price = stock['low_price']
        self.last_price = stock['last_price']
        self.average_price = stock['average_price']
        self.btc_price = stock['btc_price']
        self.volume = stock['volume']
        self.base_volume = stock['base_volume']
        self.bid = stock['bid']
        self.ask = stock['ask']


class SellersCache(db.Model):
    __tablename__ = 'sellers_cache'
    code = Column(String(255), primary_key=True)
    data = Column(LONGTEXT, nullable=False, unique=False)

    def find(self, code):
        return self.query.filter(self.code == code).first()


class BuyersCache(db.Model):
    __tablename__ = 'buyers_cache'
    code = Column(String(255), primary_key=True)
    data = Column(LONGTEXT, nullable=False, unique=False)

    def find(self, code):
        return self.query.filter(self.code == code).first()


class Cities(db.Model):
    __tablename__ = 'cities'
    id = Column(INTEGER, primary_key=True)
    country_code = Column(String(3))
    city_name = Column(String(255))
    lat = Column(DECIMAL(precision=13, scale=10))
    lng = Column(DECIMAL(precision=13, scale=10))
    link_sellers = Column(String(255))
    link_buyers = Column(String(255))


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class AdminHomeView(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html')

    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class UserAdmin(AdminModelView):
    column_hide_backrefs = True
    can_edit = False
    can_delete = False


class CurrenciesAdmin(AdminModelView):
    page_size = 50
    column_hide_backrefs = True
    column_display_all_relations = False
    column_list = ('name', 'description', 'slug', 'type', 'priority')
    form_columns = ['name', 'description', 'slug', 'type', 'priority', 'meta_tags', 'meta_description', ]
    can_edit = True
    column_editable_list = ('description', 'slug', 'meta_tags', 'meta_description',)
    form_overrides = dict(
        type=Select2Field,
        priority=Select2Field
    )
    form_args = dict(
        type=dict(
            choices=[
                ('1', 'Coin'),
                ('2', 'Token'),
                ('3', 'Fiat')
            ]
        ),
        priority=dict(
            choices=[
                ('1', 'High priority'),
                ('0', 'Low priority')
            ]
        ),
    )


class CountriesAdmin(AdminModelView):
    page_size = 50
    can_create = False
    can_edit = True
    column_list = ('description', 'name_alpha2', 'slug', 'priority', 'meta_tags', 'meta_description')
    column_hide_backrefs = True
    column_display_all_relations = False
    form_columns = ['description', 'priority', 'meta_tags', 'meta_description']
    form_overrides = dict(
        priority=Select2Field
    )
    form_args = dict(
        priority=dict(
            choices=[
                ('1', 'High priority'),
                ('0', 'Low priority')
            ]
        ),
    )


class CitiesAdmin(AdminModelView):
    page_size = 100
    can_create = True
    can_edit = True
    column_list = ('country_code', 'city_name', 'lat', 'lng')
    column_hide_backrefs = True
    column_display_all_relations = False
    form_columns = ['country_code', 'city_name', 'lat', 'lng']
    column_filters = [
        FilterEqual(column=Cities.country_code, name='Country code'),
    ]


class PaymentMethodsAdmin(AdminModelView):
    page_size = 50
    can_create = False
    can_edit = True
    column_list = ('name', 'method', 'code', 'description', 'slug', 'priority', 'meta_tags', 'meta_description')
    column_hide_backrefs = True
    column_display_all_relations = False
    form_columns = ['description', 'priority', 'meta_tags', 'meta_description']
    form_overrides = dict(
        priority=Select2Field
    )
    form_args = dict(
        priority=dict(
            choices=[
                ('1', 'High priority'),
                ('0', 'Low priority')
            ]
        ),
    )


class StockExchangesAdmin(AdminModelView):
    column_list = ('name', 'url', 'refferal_link', 'slug', 'type', 'active')
    # column_formatters = dict(active=lambda name, url, api_secret, active: {1: 'Enable', 0: 'Disable'})
    column_hide_backrefs = True
    column_display_all_relations = False
    form_columns = ['name', 'url', 'refferal_link', 'slug', 'meta_tags', 'meta_description', 'active', 'type', 'api_key', 'api_secret']
    form_overrides = dict(
        active=Select2Field,
        type=Select2Field
    )
    form_args = dict(
        active=dict(
            choices=[
                ('1', 'Enable'),
                ('0', 'Disable')
            ]
        ),
        type=dict(
            choices=[
                ('market', 'Market'),
                ('exchange', 'Exchange')
            ]
        ),
    )


db.create_all()

admin = Admin(app, index_view=AdminHomeView(), name='exchange', template_mode='bootstrap3')
admin.add_view(CurrenciesAdmin(Currencies, db.session))
admin.add_view(StockExchangesAdmin(StockExchanges, db.session))
admin.add_view(CountriesAdmin(Countries, db.session))
admin.add_view(CitiesAdmin(Cities, db.session))
admin.add_view(PaymentMethodsAdmin(PaymentMethods, db.session))
admin.add_view(UserAdmin(User, db.session))
