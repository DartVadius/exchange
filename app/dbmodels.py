from sqlalchemy import Column, INTEGER, String, UniqueConstraint, TIMESTAMP, DECIMAL
from app.database import Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(INTEGER, primary_key=True)
    author = Column(String(255), index=True, unique=False)
    title = Column(String(255), index=True, unique=True)

    def __init__(self, author, title):
        self.author = author
        self.title = title

    def __repr__(self):
        return '<Book %r>' % (self.author + self.title)


class Currencies(Base):
    __tablename__ = 'currencies'
    __table_args__ = {'mysql_engine': 'MyISAM'}

    id = Column(INTEGER, primary_key=True)
    name = Column(String(10), nullable=False, unique=True)
    description = Column(String(255), nullable=True)


class StockExchanges(Base):
    __tablename__ = 'stock_exchanges'
    __table_args__ = {'mysql_engine': 'MyISAM'}

    id = Column(INTEGER, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    url = Column(String(255), nullable=False)
    api_key = Column(String(45), nullable=True)
    api_secret = Column(String(45), nullable=True)


class ExchangeRates(Base):
    __tablename__ = 'exchange_rates'
    __table_args__ = {'mysql_engine': 'MyISAM'}
    # __table_args__ = tuple(UniqueConstraint('stock_exchange_id', 'current_currency_id', 'compare_currency_id'))

    id = Column(INTEGER, primary_key=True)
    stock_exchange_id = Column(INTEGER, nullable=False, index=True)
    current_currency_id = Column(INTEGER, nullable=False, index=True)
    compare_currency_id = Column(INTEGER, nullable=False, index=True)
    date = Column(TIMESTAMP, nullable=False)
    high_price = Column(DECIMAL(precision=14, scale=10))
    low_price = Column(DECIMAL(precision=14, scale=10))
    last_price = Column(DECIMAL(precision=14, scale=10))
    volume = Column(DECIMAL(precision=14, scale=5))
    bid = Column(DECIMAL(precision=14, scale=10))
    ask = Column(DECIMAL(precision=14, scale=10))

# CREATE TABLE IF NOT EXISTS `exchange_rates` (
#   `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
#   `stock_exchange_id` INT(10) UNSIGNED NOT NULL,
#   `date` TIMESTAMP NOT NULL,
#   `current_currency_id` INT(10) UNSIGNED NOT NULL,
#   `compare_currency_id` INT(10) UNSIGNED NOT NULL,
#   `high_price` DECIMAL UNSIGNED NULL,
#   `low_price` DECIMAL UNSIGNED NULL,
#   `last_price` DECIMAL UNSIGNED NULL,
#   `volume` DECIMAL UNSIGNED NULL,
#   `bid` DECIMAL UNSIGNED NULL,
#   `ask` DECIMAL UNSIGNED NULL,


#   UNIQUE INDEX `current_compare_stock` (`current_currency_id` ASC, `compare_currency_id` ASC, `stock_exchange_id` ASC),
#   CONSTRAINT `fk_exchange_rates_stocks`
#     FOREIGN KEY (`stock_exchange_id`)
#     REFERENCES `stock_exchenges` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION,
#   CONSTRAINT `fk_exchange_rates_current`
#     FOREIGN KEY (`current_currency_id`)
#     REFERENCES `currencies` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION,
#   CONSTRAINT `fk_exchange_rates_compare`
#     FOREIGN KEY (`compare_currency_id`)
#     REFERENCES `currencies` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION)
# ENGINE = InnoDB
# DEFAULT CHARACTER SET = utf8;
#
#
# -- -----------------------------------------------------
# -- Table `exchange_history`
# -- -----------------------------------------------------
# CREATE TABLE IF NOT EXISTS `exchange_history` (
#   `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
#   `stock_exchange_id` INT(10) UNSIGNED NOT NULL,
#   `date` TIMESTAMP NOT NULL,
#   `current_currency_id` INT(10) UNSIGNED NOT NULL,
#   `compare_currency_id` INT(10) UNSIGNED NOT NULL,
#   `high_price` DECIMAL UNSIGNED NULL,
#   `low_price` DECIMAL UNSIGNED NULL,
#   `last_price` DECIMAL UNSIGNED NULL,
#   `volume` DECIMAL UNSIGNED NULL,
#   `bid` DECIMAL UNSIGNED NULL,
#   `ask` DECIMAL UNSIGNED NULL,
#   PRIMARY KEY (`id`),
#   UNIQUE INDEX `id_UNIQUE` (`id` ASC),
#   INDEX `fk_exchange_history_current_idx` (`current_currency_id` ASC),
#   INDEX `fk_exchange_history_compare_idx` (`compare_currency_id` ASC),
#   INDEX `fk_exchange_stock_idx` (`stock_exchange_id` ASC),
#   CONSTRAINT `fk_exchange_history_current`
#     FOREIGN KEY (`current_currency_id`)
#     REFERENCES `currencies` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION,
#   CONSTRAINT `fk_exchange_history_compare`
#     FOREIGN KEY (`compare_currency_id`)
#     REFERENCES `currencies` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION,
#   CONSTRAINT `fk_exchange_stock`
#     FOREIGN KEY (`stock_exchange_id`)
#     REFERENCES `stock_exchenges` (`id`)
#     ON DELETE NO ACTION
#     ON UPDATE NO ACTION)
# ENGINE = InnoDB
# DEFAULT CHARACTER SET = utf8;
#
#
# SET SQL_MODE=@OLD_SQL_MODE;
# SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
# SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
