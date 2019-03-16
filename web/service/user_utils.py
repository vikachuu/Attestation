from flask import jsonify

from web import db
from web.model.user_model import User
from web.service.teacher_utils import TeacherUtils


class UserUtils:
    @staticmethod
    def get_personnel_number_by_user_id(user_id):
        sql = """
        SELECT personnel_number
        FROM \"user\"
        WHERE user_id=%s;
        """
        result = db.engine.execute(sql, (user_id,))
        personnel_number = [dict(row) for row in result]
        if personnel_number:
            return personnel_number[0]['personnel_number']
        else:
            response_object = {
                'status': 'fail',
                'message': 'No user exists with such id.',
            }
            return response_object

    @staticmethod
    def get_teacher_user_profile(token):
        user_id = User.decode_auth_token(token)
        personnel_number = UserUtils.get_personnel_number_by_user_id(user_id)
        return TeacherUtils.get_teacher_by_id(personnel_number)
