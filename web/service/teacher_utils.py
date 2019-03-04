from functools import wraps

from web import db
from web.model.teacher_model import Teacher
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
            return f(data)
        return decorated_function
    return decorator


class TeacherUtils:

    @staticmethod
    # @requires_access_level(0)
    def create_teacher(data):
        print("teacher created")
        teacher = Teacher.query.filter_by(teacher_id=data.get('teacher_id')).first()
        if not teacher:
            try:
                teacher = Teacher(
                    teacher_id=data.get('teacher_id'),
                    last_name=data.get('last_name')
                )

                # insert the user
                db.session.add(teacher)  # TODO: insert teacher to table sql query
                db.session.commit()

                response_object = {
                    'status': 'success',
                    'message': 'Successfully created teacher {}.'.format(teacher.last_name)
                }
                return response_object, 201
            except Exception as e:
                response_object = {
                    'status': 'fail',
                    'message': 'Error occurred creating teacher. Please try again. {}'.format(e)
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Teacher already exists.',
            }
            return response_object, 202
