from app.dbmodels import Countries


class CountryRepository:
    @staticmethod
    def get_all():
        return Countries.query.order_by(Countries.description).all()

    @staticmethod
    def get_by_id(country_id):
        if country_id == '':
            return None
        return Countries.query.filter(Countries.id == country_id).one()
