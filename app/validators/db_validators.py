from wtforms import ValidationError


class Unique(object):
    """ validator that checks field uniqueness """

    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = 'this element already exists'
        self.message = message

    def __call__(self, form, field):
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)
