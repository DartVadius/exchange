from wtforms import Form, BooleanField, StringField, validators, PasswordField
from app.validators.db_validators import Unique
from app.dbmodels import StockExchanges, User


# class StockForm(Form):
#     name = StringField('name', [validators.DataRequired(), validators.Length(min=1, max=255),
#                                 Unique(StockExchanges, StockExchanges.name)])
#     url = StringField('url', [validators.DataRequired(), validators.Length(min=1, max=255),
#                               Unique(StockExchanges, StockExchanges.url)])
#     api_key = StringField('api_key', [validators.Length(min=0, max=45)])
#     api_secret = StringField('api_secret', [validators.Length(min=0, max=45)])


class LoginForm(Form):
    login = StringField("Login", validators=[validators.DataRequired(), validators.Length(min=6, max=25)])
    password = PasswordField("Password", validators=[validators.DataRequired(), validators.Length(min=8, max=25)])
    remember_me = BooleanField("Remember me?", default=True)

    def validate(self):
        if not super(LoginForm, self).validate():
            return False
        self.user = User.authenticate(self.login.data, self.password.data)
        if not self.user or self.user.admin != 1 or self.user.active != 1:
            self.password.errors.append("Access denied")
            return False
        return True
