from app.dbmodels import Countries
from sqlalchemy import func
from app.dbmodels import Currencies


class CountryRepository:
    @staticmethod
    def get_all():
        return Countries.query.order_by(Countries.name_alpha2).all()
