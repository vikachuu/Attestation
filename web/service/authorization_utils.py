from web import db
from web.model.user_model import User


class Authorization:

    @staticmethod
    def login_user(data):
        try:
            user = User.query.filter_by(login=data.get('login')).first()  # TODO: write sql query and execute
            if user and user.check_password(data.get('password')):
                auth_token = User.encode_auth_token(user.user_id)
                if auth_token:
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'token': auth_token.decode(),
                        'access_level': user.access_level
                    }
                    return response_object, 200
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'login or password does not match (no such user).'
                }
                return response_object, 401

        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'Failed login. Try again. {}'.format(e)
            }
            return response_object, 500


class Register:
    @staticmethod
    def register_user(data):
        # check if user already exists
        user = User.query.filter_by(login=data.get('login')).first()  # TODO: rewrite to sql query
        if not user:
            try:
                user = User(
                    login=data.get('login'),
                    password=data.get('password'),
                    access_level=data.get('access_level'),
                    personnel_number=data.get('personnel_number')
                )

                # insert the user
                db.session.add(user)  # TODO: insert user to table
                db.session.commit()
                # generate the auth token
                auth_token = user.encode_auth_token(user.user_id)
                response_object = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return response_object, 201
            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': 'Some error occurred in register. Please try again. {}'.format(e)
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return response_object, 202
