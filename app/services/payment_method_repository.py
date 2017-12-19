from app.dbmodels import PaymentMethods


class PaymentMethodRepository:
    @staticmethod
    def get_all():
        return PaymentMethods.query.order_by(PaymentMethods.name).all()
