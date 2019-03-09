from datetime import date
from functools import wraps

from flask.json import JSONEncoder

from web.model.user_model import User


def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(data, token):
            user_id = User.decode_auth_token(token)

            user = User.query.filter_by(user_id=user_id).first()
            if user:
                if user.access_level != access_level:
                    response_object = {
                        'status': 'fail',
                        'message': 'You have not enough access level'
                    }
                    return response_object, 401
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'not authorized access'
                }
                return response_object, 401
            return f(data, token)
        return decorated_function
    return decorator


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)