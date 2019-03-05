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
            return f(data, token)
        return decorated_function
    return decorator


class TeacherUtils:

    @staticmethod
    @requires_access_level(2)
    def create_teacher(data, token):
        teacher = Teacher.query.filter_by(personnel_number=data.get('personnel_number')).first()
        if not teacher:
            try:
                teacher = Teacher(
                    personnel_number=data.get('personnel_number'),
                    employment_history=data.get('employment_history'),
                    surname=data.get('surname'),
                    name=data.get('name'),
                    middle_name=data.get('middle_name'),
                    birth_date=data.get('birth_date'),

                    educational_institution=data.get('educational_institution'),
                    specialty=data.get('specialty'),
                    accreditation_level=data.get('accreditation_level'),
                    graduation_year=data.get('graduation_year'),
                    position=data.get('position'),
                    experience=data.get('experience'),

                    qualification_category=data.get('qualification_category'),
                    rank=data.get('rank'),
                    previous_attestation_date=data.get('previous_attestation_date'),
                    next_attestation_date=data.get('next_attestation_date'),
                    degree=data.get('degree')
                )

                # insert the user
                db.session.add(teacher)  # TODO: insert teacher to table sql query
                db.session.commit()

                response_object = {
                    'status': 'success',
                    'message': 'Successfully created teacher {}.'.format(teacher.surname)
                }
                return response_object, 200
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

    @staticmethod
    def get_teacher_by_id(personnel_number):
        teacher = Teacher.query.filter_by(personnel_number=personnel_number).first()  # TODO: query
        print(type(teacher))
        if teacher:
            return teacher.json(), 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'No teacher exists with such id.',
            }
            return response_object, 202

    @staticmethod
    def get_all_teachers():
        teachers = Teacher.query.all()
        if teachers:
            return [teacher.json() for teacher in teachers], 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Table teachers is empty.',  # TODO: empty or error? ever get here?
            }
            return response_object, 202
