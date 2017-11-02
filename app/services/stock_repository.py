from app.dbmodels import StockExchanges


class StockRepository:
    def get_stock_name_by_id(self, stock_id):
        return StockExchanges.query.with_entities(StockExchanges.name).filter_by(id=stock_id).first()[0]

    def get_stock_id_by_slug(self, slug):
        return StockExchanges.query.with_entities(StockExchanges.id).filter_by(slug=slug).first()[0]
