from flask import g
from flask.sessions import SecureCookieSessionInterface
from flask_login import user_loaded_from_header


class CustomSessionInterface(SecureCookieSessionInterface):
    """Prevent creating session from API requests."""

    def save_session(self, *args, **kwargs):
        if g.get('login_via_header'):
            return
        return super(CustomSessionInterface, self).save_session(*args, ** kwargs)