from flask import Flask, jsonify, g, request, make_response
from app.dbmodels import User, Tokens, db
import uuid
import datetime


class Api:
    def __init__(self):
        g.login_via_header = True

    def get_token(self):
        # auth = request.headers.get('Authorization')
        # x = self.parse_auth_header(auth)
        # print(x)
        # print(auth_info)
        if request.method != "POST":
            response = make_response(jsonify({'error': 'Method Not Allowed'}), 405)
            response = self.set_no_cache(response)
            return response
        if not request.json or not 'login' in request.json or not 'password' in request.json:
            response = make_response(jsonify({'error': 'bad request'}), 400)
            response = self.set_no_cache(response)
            return response
        user = User()
        user_auth = user.authenticate(request.json['login'], request.json['password'])
        if user_auth and user_auth.admin == 1 and user_auth.active == 1:
            token_model = Tokens()
            find_token = token_model.query.filter_by(user_id=user_auth.id).first()
            if find_token and find_token.expired > datetime.datetime.now():
                response = make_response(
                    jsonify({'token': find_token.token, 'expired': find_token.expired, 'success': True}), 200)
                response = self.set_no_cache(response)
                return response
            token = str(uuid.uuid4())
            expired = datetime.datetime.now() + datetime.timedelta(days=+1)
            expired = expired.strftime('%Y-%m-%d %H:%M:%S')
            if find_token:
                find_token.token = token
                find_token.expired = expired
                db.session.add(find_token)
            else:
                token_model.token = token
                token_model.expired = expired
                token_model.user_id = user_auth.id
                db.session.add(token_model)
            db.session.commit()
            response = make_response(jsonify({'token': token, 'expired': expired, 'success': True}), 200)
            response = self.set_no_cache(response)
            return response
        response = make_response(jsonify({'error': 'bad auth'}), 403)
        response = self.set_no_cache(response)
        return response

    def get_statistic(self):
        if request.method != "GET":
            response = make_response(jsonify({'error': 'Method Not Allowed'}), 405)
            response = self.set_no_cache(response)
            return response
        auth = request.headers.get('Authorization')
        auth = self.parse_auth_header(auth)
        if auth is None:
            response = make_response(jsonify({'error': 'bad auth'}), 403)
            response = self.set_no_cache(response)
            return response



    def parse_auth_header(self, header):
        try:
            auth_type, auth_info = header.split(None, 1)
            return {'auth_type': auth_type, 'auth_info': auth_info}
        except ValueError:
            return None

    def set_no_cache(self, response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        return response
