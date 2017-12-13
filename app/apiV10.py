import base64
import datetime
import uuid

from flask import jsonify, g, request, make_response
from sqlalchemy import and_

from app.dbmodels import User, Tokens, db, CurrencyStatistic, CurrencyStatisticHistory


class Api:
    def __init__(self):
        g.login_via_header = True

    def get_token(self):
        if request.method != "POST":
            return self.set_error_405()
        auth = request.headers.get('Authorization')
        auth = self.parse_auth_header(auth)
        if auth is None or auth['auth_type'] != 'Basic':
            return self.set_error_400()
        auth = self.get_login_pass(auth['auth_info'])
        user = User()
        user_auth = user.authenticate(auth['login'], auth['password'])
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
        return self.set_error_403()

    def is_valid_request(self, method):
        check = False
        if request.method != method.upper():
            check = self.set_error_405()
        auth = request.headers.get('Authorization')
        auth = self.parse_auth_header(auth)
        if auth is None or auth['auth_type'] != 'Bearer' or self.check_token(auth['auth_info']) is False:
            check = self.set_error_403()
        if request.json is None:
            check = self.set_error_400()
        return check

    def get_statistic(self):
        check = self.is_valid_request('GET')
        if check is not False:
            return check

        data = request.json

        if 'page' in data:
            page = data['page']
        else:
            page = None

        if 'page_count' in data:
            page_count = data['page_count']
        else:
            page_count = 20

        if 'date' in data and 'from' in data['date']:
            date_from = data['date']['from']
            date_from = datetime.datetime.strptime(date_from, '%Y-%m-%d %H:%M:%S')
        else:
            date_from = None

        if 'date' in data and 'to' in data['date']:
            date_to = data['date']['to']
            date_to = datetime.datetime.strptime(date_to, '%Y-%m-%d %H:%M:%S')
        else:
            date_to = None

        if date_from is None and date_to is None:
            count = CurrencyStatistic.query.count()
            select = CurrencyStatistic.query.order_by(CurrencyStatistic.rank)
        elif date_to is not None and date_from is not None:
            select = CurrencyStatisticHistory.query.filter(
                and_(
                    CurrencyStatisticHistory.date <= date_to,
                    CurrencyStatisticHistory.date >= date_from,
                )
            )
            count = select.count()
        elif date_from is not None:
            select = CurrencyStatisticHistory.query.filter(
                CurrencyStatisticHistory.date >= date_from
            )
            count = select.count()
        elif date_to is not None:
            select = CurrencyStatisticHistory.query.filter(
                CurrencyStatisticHistory.date <= date_to
            )
            count = select.count()

        if page is None or page == '':
            page = 1
            select = select.paginate(page, int(count), False)
        else:
            if page_count is None or page_count == '':
                count = 20
                select = select.paginate(int(page), count, False)
            else:
                count = page_count
                select = select.paginate(int(page), int(count), False)

        # print(select.pages)
        # print(select.has_next)
        # print(select.has_prev)

        val = [i.serialaze() for i in select.items]
        res = {
            'pages total': select.pages,
            'current page': page,
            'items per page': count,
            'result': val
        }

        response = make_response(jsonify(res), 200)
        response = self.set_no_cache(response)
        return response

    def set_error_405(self):
        response = make_response(jsonify({'error': 'Method Not Allowed'}), 405)
        response = self.set_no_cache(response)
        return response

    def set_error_403(self):
        response = make_response(jsonify({'error': 'bad auth'}), 403)
        response = self.set_no_cache(response)
        return response

    def set_error_400(self):
        response = make_response(jsonify({'error': 'bad request'}), 400)
        response = self.set_no_cache(response)
        return response

    def parse_auth_header(self, header):
        if header is None:
            return None
        try:
            auth_type, auth_info = header.split(None, 1)
            return {'auth_type': auth_type, 'auth_info': auth_info}
        except ValueError:
            return None

    def get_login_pass(self, value):
        try:
            value = base64.b64decode(value).decode('utf-8')
            login, password = value.split(':', 1)
            return {'login': login, 'password': password}
        except ValueError:
            return None

    def set_no_cache(self, response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        return response

    def check_token(self, token):
        token_model = Tokens()
        find_token = token_model.query.filter_by(token=token).first()
        if find_token and find_token.expired > datetime.datetime.now():
            return True
        return False
