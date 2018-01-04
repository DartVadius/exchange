import os
import platform

basedir = os.path.abspath(os.path.dirname(__file__))

dev = platform.system() != 'Linux'
if dev:
    connect = 'mysql+pymysql://root:@localhost/mypy?charset=utf8'
else:
    connect = 'mysql+pymysql://coins:VfytnrJ@localhost/coins?charset=utf8'
