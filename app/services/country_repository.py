from app.dbmodels import Countries


class CountryRepository:
    @staticmethod
    def get_all():
        return Countries.query.order_by(Countries.name_alpha2).all()

    @staticmethod
    def get_by_id(country_id):
        return Countries.query.filter(Countries.id == country_id).one()
