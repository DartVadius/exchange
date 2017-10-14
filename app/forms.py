from wtforms import Form, BooleanField, StringField, validators
from app.validators.db_validators import Unique
from app.dbmodels import StockExchanges


class LoginForm(Form):
    name = StringField('name', [validators.DataRequired(), validators.Length(min=4, max=25)])


class Book(Form):
    author = StringField('author', [validators.DataRequired(), validators.Length(min=1, max=255)])
    title = StringField('title', [validators.DataRequired(), validators.Length(min=1, max=255)])


class StockForm(Form):
    name = StringField('name', [validators.DataRequired(), validators.Length(min=1, max=255),
                                Unique(StockExchanges, StockExchanges.name)])
    url = StringField('url', [validators.DataRequired(), validators.Length(min=1, max=255),
                              Unique(StockExchanges, StockExchanges.url)])
    api_key = StringField('api_key', [validators.Length(min=0, max=45)])
    api_secret = StringField('api_secret', [validators.Length(min=0, max=45)])
