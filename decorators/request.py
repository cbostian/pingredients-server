from flask import abort, request
from functools import wraps

from decorators.helpers import parametrized


@parametrized
def authorize(func, token_only=False):
    @wraps(func)
    def authorized_func(*args, **kwargs):
        oauth_token = request.headers.get('oauth_token')
        if not oauth_token:
            abort(401)
        if not token_only:
            user_id = request.headers.get('user_id')
            if not user_id:
                abort(401)
        return func(oauth_token, *args, **kwargs)
    return authorized_func
