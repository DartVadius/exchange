from app import app
from app.viewsmodels import ViewsModels


@app.route('/stock/<string:stock_slug>', methods=['GET'])
def stock(stock_slug):
    view = ViewsModels()
    return view.stock(stock_slug)


@app.route('/', methods=['GET'])
@app.route('/currencies/<string:currency>', methods=['GET'])
@app.route('/currencies/<int:page>', methods=['GET'])
def stocks(page=1, currency=''):
    view = ViewsModels()
    return view.currencies(page, currency)


@app.route('/stocks', methods=['GET'])
def currencies():
    view = ViewsModels()
    return view.stocks()


@app.route('/update-rates', methods=['GET'])
def update_rates():
    view = ViewsModels()
    return view.update_rates()


@app.route("/login", methods=["GET", "POST"])
def login():
    view = ViewsModels()
    return view.login()


@app.route("/logout")
def logout():
    view = ViewsModels()
    return view.logout()


@app.route("/update-countries", methods=['GET'])
def update_countries():
    view = ViewsModels()
    return view.update_countries()


@app.route("/exchange", methods=['GET'])
def exchange():
    view = ViewsModels()
    return view.exchange()


@app.route("/test", methods=['GET'])
def test():
    view = ViewsModels()
    return view.test()


from flask import Flask
from flask import render_template
from flask import jsonify
from flask import g, request, redirect, url_for
import json


from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy import event
from sqlalchemy.orm import mapper,sessionmaker
from sqlalchemy.orm.interfaces import EXT_STOP,EXT_CONTINUE
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import literal_column


import jinja2
from  jinja2schema import infer, to_json_schema

# SQLALCHEMY_DATABASE_URI = 'mysql://test@localhost/test' #web database

# app = Flask(__name__)
# app.config.from_object(__name__)
# db = SQLAlchemy(app)
# Base = declarative_base()


from app import db
from app.dbmodels import Content

@app.route("/cms")
def cms():
    return render_template('cms.html')


def rpcCheck(data):
    return {'ping': 'pong'}

def rpcGetContentList(data):
    res= []  
    for a in db.session.query(Content).all():
        del a.__dict__['_sa_instance_state']
        res.append(a.__dict__)
    return res

def beforeUpdate(record):
    if record.template != '' and record.template != 'null' and (not record.data or record.data == '{}'):
#        print to_json_schema(infer(open('templates/' + record.template, 'r').read()))
        print ('NEW DATA')
        schema = to_json_schema(infer(open('/home/coins/flask/exchange/app/templates/' + record.template, 'r').read()))
        record.schema = schema
        vars  = schema['properties']
        data  = {}
        for k,v in vars.items():
            data[k] = ''
        record.data = data
    return

        


def rpcUpdateContent(data):
    if data['id']:
        contentRecord = db.session.query(Content).get(int(data['id']))
        for key, value in data.items():
            setattr(contentRecord, key, value)
        beforeUpdate(contentRecord)
        db.session.add(contentRecord)
        db.session.commit()
        return {'errorCode': 0}
    return {'errorCode': -1}

def rpcDeleteContent(data):
    contentRecord = db.session.query(Content).get(int(data))
    db.session.delete(contentRecord)
    db.session.commit()
    return {'errorCode': 0}




def rpcNewContent(data):
    newOne = Content()
    db.session.add(newOne)
    db.session.commit()
    newOneData = newOne.__dict__
    del newOneData['_sa_instance_state']
    return newOneData


@app.route('/data', methods=['POST'])
def data():
    rpcCall =  json.loads(request.get_data(as_text=True))
    if 'func' in rpcCall and 'rpc' + rpcCall['func'] in globals() and 'data' in rpcCall:
        return jsonify(globals()[('rpc' + rpcCall['func'])](rpcCall['data']))
    else:
        print ('no func')

    return jsonify({'some': 'data'})

def merge_template(template, **kwargs):
    contentRecord = Content.query.filter_by(url=request.path).first()
    if type(contentRecord.data) is dict:
        data = contentRecord.data
    else:
        data = json.loads(contentRecord.data)

    for key,value in data.items():
        if key in kwargs:
            data[key] = kwargs[key]

    return render_template(template, **data)


@app.route("/some/route/<int:id>")
def some_route(id):
    return merge_template('test.html', data=['data','from python'])
    #return '<h1>' + str(id) + '</h1>'
    

if __name__ == "__main__":
    app.run(debug=True)
