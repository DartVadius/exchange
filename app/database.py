import os

basedir = os.path.abspath(os.path.dirname(__file__))

dev = False
if dev:
    connect = 'mysql+pymysql://root:1111@localhost/mypy?charset=utf8'
else:
    connect = 'mysql+pymysql://coins:VfytnrJ@localhost/coins?charset=utf8'
