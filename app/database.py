import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

basedir = os.path.abspath(os.path.dirname(__file__))


dev = False
if dev:
    connect = 'mysql+pymysql://root:1111@localhost/mypy?charset=utf8'
else:
    connect = 'mysql+pymysql://coins:VfytnrJ@localhost/coins?charset=utf8'

engine = create_engine(connect)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
