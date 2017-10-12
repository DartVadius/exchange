from wtforms import Form, BooleanField, StringField, validators


class LoginForm(Form):
    name = StringField('name', [validators.DataRequired(), validators.Length(min=4, max=25)])


class Book(Form):
    author = StringField('author', [validators.DataRequired(), validators.Length(min=1, max=255)])
    title = StringField('title', [validators.DataRequired(), validators.Length(min=1, max=255)])
