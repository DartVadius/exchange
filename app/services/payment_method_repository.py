from app.dbmodels import PaymentMethods


class PaymentMethodRepository:
    @staticmethod
    def get_all():
        return PaymentMethods.query.order_by(PaymentMethods.name).all()

    @staticmethod
    def get_by_id(pm_id):
        if pm_id == '':
            return None
        return PaymentMethods.query.filter_by(id=pm_id).first()
