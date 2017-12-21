from app.dbmodels import PaymentMethods


class PaymentMethodRepository:
    @staticmethod
    def get_all():
        return PaymentMethods.query.order_by(PaymentMethods.name).all()

    @staticmethod
    def get_by_id(pm_id):
        return PaymentMethods.query.filter(PaymentMethods.id == pm_id).one()
