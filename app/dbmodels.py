from sqlalchemy import Column, INTEGER, String, UniqueConstraint, TIMESTAMP, DECIMAL, ForeignKey, Text
from sqlalchemy.orm import relationship
from flask_admin import Admin
from app import app, login_manager, bcrypt
from flask_admin.contrib.sqla import ModelView
from app.database import db_session
from flask_admin.form import Select2Field
from flask_migrate import Migrate
from app import db

migrate = Migrate(app, db)


@login_manager.user_loader
def _user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id = Column(INTEGER, primary_key=True)
    login = Column(String(25), nullable=False, unique=True)
    password = Column(String(25), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.is_active

    def is_admin(self):
        return self.is_admin()

    def is_anonymous(self):
        return False

    @staticmethod
    def make_password(plaintext):
        return bcrypt.generate_password_hash(plaintext)

    def check_password(self, raw_password):
        return bcrypt.check_password_hash(self.password_hash, raw_password)

    @classmethod
    def create(cls, login, password, **kwargs):
        return User(login=login, password_hash=User.make_password(password), **kwargs)

    @staticmethod
    def authenticate(login, password):
        user = User.query.filter(User.login == login).first()
        if user and user.check_password(password):
            return user
        return False


class Currencies(db.Model):
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

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.description!r}>'.format(self)

    def count(self):
        return db_session.query(self).count()


class StockExchanges(db.Model):
    __tablename__ = 'stock_exchanges'
    __table_args__ = {'mysql_engine': 'InnoDB'}

    id = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    url = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    meta_tags = Column(String(255), nullable=True, unique=False)
    meta_description = Column(Text(), nullable=True, unique=False)
    api_key = Column(String(45), nullable=True)
    api_secret = Column(String(45), nullable=True)
    active = Column(INTEGER, nullable=True, default=1)
    exchange_rates = relationship('ExchangeRates', backref='stock_exchanges', lazy=True)
    exchange_history = relationship('ExchangeHistory', backref='stock_history', lazy=True)

    def __repr__(self):
        return '<Stats: name={0.name!r}, description={0.url!r}>'.format(self)


class ExchangeHistory(db.Model):
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


class ExchangeRates(db.Model):
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


class UserAdmin(ModelView):
    column_hide_backrefs = True
    can_edit = False
    can_delete = False


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
    column_list = ('name', 'url', 'slug', 'meta_tags', 'meta_description', 'api_key', 'api_secret', 'active')
    # column_formatters = dict(active=lambda name, url, api_secret, active: {1: 'Enable', 0: 'Disable'})
    column_hide_backrefs = True
    column_display_all_relations = False
    form_columns = ['name', 'url', 'slug', 'meta_tags', 'meta_description', 'active', 'api_key', 'api_secret']
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


db.create_all()

admin = Admin(app, name='exchange', template_mode='bootstrap3')
admin.add_view(CurrenciesAdmin(Currencies, db_session))
admin.add_view(StockExchangesAdmin(StockExchanges, db_session))
admin.add_view(UserAdmin(User, db_session))
